import json

import common
import netfetch
import stage2

ROOMS = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf"]


def write_rooms(run, slugs=ROOMS, ladder=None, ventures=None):
    ladder = ladder or {}
    ventures = ventures or {}
    rooms = []
    for s in slugs:
        steps = ladder.get(s, 3)
        rooms.append({"slug": s, "name": f"Room {s}", "lens": "profession", "origin": "generated", "status": "kept",
                      "ladder": [{"step": i, "problem": f"p{i}"} for i in range(1, steps + 1)],
                      "venture_overlap": ventures.get(s, [])})
    common.write_json(run / "01_rooms.json", {"status": "ok", "rooms": rooms, "removed": [], "parts": []})


def spend(url="https://price.test/p", seen_via="search", price_text="$49/month", currency="USD", amount=49):
    return {"what": "a course", "price_text": price_text, "amount": amount, "currency": currency, "unit": "month",
            "url": url, "seen_via": seen_via}


def entry(slug, kind="warm", lid="w1", url=None, depth="d1", spend_items=None, blocked=False, needs=(), excluded=False,
          xid=None, trust=False):
    return {"slug": slug,
            "reach": {"kind": kind, "ledger_id": lid, "evidence_url": url, "reasoning": "reach reasoning", "confidence": "high"},
            "depth": {"ledger_id": depth, "reasoning": "depth reasoning", "confidence": "moderate"},
            "spend": [spend()] if spend_items is None else spend_items,
            "supply": {"blocked": blocked, "needs": list(needs), "reasoning": "supply reasoning", "confidence": "moderate"},
            "excluded": {"is_excluded": excluded, "exclusion_id": xid, "reasoning": "excl reasoning", "confidence": "high"},
            "trust_needed": {"value": trust, "reasoning": "trust reasoning", "confidence": "low"}}


def write_parts(run, entries, per_file=3):
    d = run / "02_mask.parts"
    for i in range(0, len(entries), per_file):
        common.write_json(d / f"{i // per_file + 1}.json", {"rooms": entries[i:i + per_file]})


def mask_json(run):
    return json.loads((run / "02_mask.json").read_text(encoding="utf-8"))


def graveyard(froot):
    return (froot / "graveyard.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- fx
def test_fx_prints_table_and_rejects_bad_rates(run, cli):
    r = cli("fx", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "INR            88.0000  search    moderate    https://example.test/fx" in r.stdout
    assert "USD             1.0000" in r.stdout
    data = common.read_json(run / "fx_rates.json")
    data["base"] = "INR"
    data["rates"]["AED"]["per_usd"] = -1
    del data["rates"]["SGD"]["url"]
    data["rates"]["GBP"]["reasoning"] = ""
    data["rates"]["EUR"]["seen_via"] = "memory"
    common.write_json(run / "fx_rates.json", data)
    r = cli("fx", "--run", "2026-09-26")
    assert r.returncode == 1
    for needle in ("'base' must be USD", "AED: 'per_usd' must be a positive number", "SGD: 'url' must start with http",
                   "GBP: missing 'reasoning'", "EUR: 'seen_via' must be page or search"):
        assert needle in r.stderr, needle
    (run / "fx_rates.json").unlink()
    r = cli("fx", "--run", "2026-09-26")
    assert r.returncode == 2 and "fx_rates.json is missing" in r.stderr


def test_fx_warns_when_stale(run, cli):
    data = common.read_json(run / "fx_rates.json")
    data["as_of"] = "2026-09-01"
    common.write_json(run / "fx_rates.json", data)
    r = cli("fx", "--run", "2026-09-26")
    assert r.returncode == 0 and "warning: fx_rates.json is 25 days older than the run date" in r.stdout


# --------------------------------------------------------------------------- mask tests
def test_each_test_kills_with_its_reason_and_graveyard_lists_all_failed_tests(froot, run, cli):
    write_rooms(run, ladder={"delta": 2})
    write_parts(run, [
        entry("alpha"),
        entry("bravo", kind=None, lid=None),
        entry("charlie", depth=None),
        entry("delta"),
        entry("echo", spend_items=[]),
        entry("foxtrot", blocked=True, needs=["ritual", "large_capital"]),
        entry("golf", excluded=True, xid="x1", kind=None, lid=None, depth=None),
    ])
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    m = mask_json(run)
    assert m["kept"] == ["alpha"] and m["cut"] == []
    assert m["killed"] == ["bravo", "charlie", "delta", "echo", "foxtrot", "golf"]
    by = {v["slug"]: v for v in m["rooms"]}
    assert by["bravo"]["failed_tests"] == ["reach"] and "no reach" in by["bravo"]["tests"]["reach"]["reason"]
    assert by["charlie"]["failed_tests"] == ["depth"] and "depth.ledger_id is null" in by["charlie"]["tests"]["depth"]["reason"]
    assert by["delta"]["failed_tests"] == ["ladder"] and by["delta"]["tests"]["ladder"]["reason"] == "2 ladder step(s); needs at least 3"
    assert by["echo"]["failed_tests"] == ["spend"] and "no spend item" in by["echo"]["tests"]["spend"]["reason"]
    assert by["foxtrot"]["failed_tests"] == ["supply"] and "ritual, large_capital" in by["foxtrot"]["tests"]["supply"]["reason"]
    assert by["golf"]["failed_tests"] == ["reach", "depth", "exclusions"]
    assert "licence" in by["golf"]["tests"]["exclusions"]["reason"]
    assert by["alpha"]["status"] == "kept" and by["alpha"]["rank"] == 1 and by["alpha"]["failed_tests"] == []
    assert by["alpha"]["spend"][0]["price_status"] == "seen_via_search"
    assert by["alpha"]["spend"][0]["price_tag"] == "[measured, page not checked]" and by["alpha"]["spend"][0]["amount_usd"] == 49.0
    gy = graveyard(froot)
    assert "- 2026-09-26 | stage 2 | room:golf | failed reach: no reach" in gy
    assert "depth: no ledger depth domain matches" in gy and "exclusions: excluded by x1" in gy
    assert "room:alpha" not in gy
    assert common.dead_items("room") == {f"room:{s}" for s in m["killed"]}
    assert (run / "02_mask_input.json").exists()
    md = (run / "02_mask.md").read_text(encoding="utf-8")
    assert "## Kept rooms (1)" in md and "| 1 | alpha | warm (w1) | d1 (strong) | 3 | 0/1 |" in md
    assert "| golf | reach, depth, exclusions |" in md
    assert "Only 1 room(s) passed the mask; fewer than 5. Rooms that failed only on depth and/or supply: charlie, foxtrot." in md
    assert "review: Only 1 room(s) passed the mask" in r.stdout
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "note" and e.get("review") is True and "fewer than 5" in e["note"] for e in events)
    assert any(e["kind"] == "count" and e["command"] == "mask" and e["killed"] == 6 for e in events)


def test_ranking_max_rooms_and_cut_rooms(froot, run, cli, monkeypatch):
    slugs = ["a-warm-long", "b-search-long", "c-warm-short", "d-two-prices", "e-verified", "f-same-as-a"]
    write_rooms(run, slugs, ladder={"a-warm-long": 5, "b-search-long": 5, "c-warm-short": 3, "d-two-prices": 3,
                                    "e-verified": 3, "f-same-as-a": 5})
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")

    class Resp:
        def __init__(self, status, text):
            self.status_code, self.text, self.headers = status, text, {}

    def fake_get(url, params=None, headers=None, timeout=30):
        if url.endswith("/robots.txt"):
            return Resp(404, "")
        if url == "https://verified.test/p":
            return Resp(200, "<p>Plans from $49/month</p>")
        return Resp(200, "<p>nothing here</p>")

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    write_parts(run, [
        entry("a-warm-long"),
        entry("b-search-long", kind="search", lid="s1", url="https://store.test/app"),
        entry("c-warm-short"),
        entry("d-two-prices", spend_items=[spend(), spend(url="https://other.test/q")]),
        entry("e-verified", spend_items=[spend(url="https://verified.test/p", seen_via="page")]),
        entry("f-same-as-a"),
    ])
    import stage2 as s2

    result = s2.mask(run, merge_parts_flag=True, max_rooms=4)
    ranked = [v["slug"] for v in result["rooms"] if v["status"] != "killed"]
    assert ranked == ["a-warm-long", "f-same-as-a", "b-search-long", "e-verified", "d-two-prices", "c-warm-short"]
    assert result["kept"] == ["a-warm-long", "f-same-as-a", "b-search-long", "e-verified"]
    assert result["cut"] == ["d-two-prices", "c-warm-short"] and result["killed"] == []
    by = {v["slug"]: v for v in result["rooms"]}
    assert by["e-verified"]["spend_points_verified"] == 1 and by["e-verified"]["spend"][0]["price_tag"] == "[measured]"
    assert by["d-two-prices"]["spend_points"] == 2 and by["d-two-prices"]["rank"] == 5
    gy = graveyard(froot)
    assert "- 2026-09-26 | stage 2 | room:c-warm-short | cut: ranked 6 of 6 survivors and max_rooms is 4; passed every test" in gy
    assert "room:d-two-prices | cut: ranked 5 of 6" in gy and "room:a-warm-long" not in gy
    # --max-rooms on the command line and the kill-rule default
    r = cli("mask", "--run", "2026-09-26", "--max-rooms", "1")
    assert r.returncode == 0, r.stderr
    assert mask_json(run)["kept"] == ["a-warm-long"] and "cut #2: f-same-as-a" in r.stdout
    r = cli("mask", "--run", "2026-09-26")
    assert r.returncode == 0 and mask_json(run)["max_rooms"] == 15 and len(mask_json(run)["kept"]) == 6


def test_rank_by_from_kill_rules_is_honoured(froot, run, h):
    write_rooms(run, ["p-warm", "q-search"], ladder={"p-warm": 3, "q-search": 4})
    write_parts(run, [entry("p-warm"), entry("q-search", kind="search", lid="s1", url="https://store.test/x")])
    assert stage2.mask(run, merge_parts_flag=True)["kept"] == ["q-search", "p-warm"]
    h.set_rule(froot, "stage2", "rank_by", ["warm_reach", "ladder_steps"])
    assert stage2.mask(run, merge_parts_flag=True)["kept"] == ["p-warm", "q-search"]


def test_flags_trust_employer_and_venture_overlap(run):
    write_rooms(run, ["s-trust", "w2-room", "w4-room", "x2-room", "v-room", "plain"], ventures={"v-room": ["v1", "v4"]})
    write_parts(run, [
        entry("s-trust", kind="search", lid="s1", url="https://store.test/x", trust=True),
        entry("w2-room", lid="w2"),
        entry("w4-room", lid="w4"),
        entry("x2-room", xid="x2"),  # x2 mentioned but not excluded
        entry("v-room"),
        entry("plain", kind="search", lid="s1", url="https://store.test/y"),
    ])
    m = stage2.mask(run, merge_parts_flag=True)
    by = {v["slug"]: v for v in m["rooms"]}
    assert by["s-trust"]["trust_flag"] is True and by["s-trust"]["reach_kind"] == "search"
    assert by["plain"]["trust_flag"] is False and by["w2-room"]["trust_flag"] is False
    assert by["w2-room"]["employer_overlap"] is True and by["w4-room"]["employer_overlap"] is True
    assert by["x2-room"]["employer_overlap"] is True and by["plain"]["employer_overlap"] is False
    assert by["v-room"]["venture_overlap"] == ["v1", "v4"] and by["plain"]["venture_overlap"] == []
    notes = "\n".join(m["review_notes"])
    assert "Search-reach rooms whose product needs trust: s-trust." in notes
    assert "overlap the founder's job (warm path w2/w4 or exclusion x2): w2-room, w4-room, x2-room." in notes
    assert "touch existing ventures (tagged, not excluded): v-room (v1, v4)." in notes
    md = (run / "02_mask.md").read_text(encoding="utf-8")
    assert "needs trust (search reach)" in md and "employer overlap" in md and "ventures: v1, v4" in md


def test_validation_errors_list_every_problem(run, cli):
    write_rooms(run, ["alpha", "bravo", "charlie"])
    bad = entry("alpha", lid="w9")
    bad["spend"] = [spend(currency="usd")]
    bad["supply"]["needs"] = ["magic"]
    bad["excluded"]["exclusion_id"] = "x7"
    bad["trust_needed"]["value"] = "yes"
    bad["depth"]["confidence"] = "certain"
    write_parts(run, [bad, entry("bravo", kind="search", lid="s1", url=None), entry("bravo"), entry("nobody")])
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1, r.stdout
    err = r.stderr
    for needle in ("1.json: room 1 (alpha): reach.ledger_id 'w9' is not a warm path id (w1, w2, w3, w4, w5)",
                   "spend item 1: 'currency' must be a 3-letter ISO code", "supply.needs 'magic' is not one of",
                   "excluded.exclusion_id 'x7' is not a ledger exclusion id (x1, x2)", "trust_needed.value must be true or false",
                   "depth: 'confidence' must be high, moderate or low", "search reach needs reach.evidence_url",
                   "1.json: room 3 (bravo): bravo appears twice", "2.json: room 1 (nobody): nobody is not a kept room in 01_rooms.json",
                   "1 kept room(s) have no mask entry: charlie"):
        assert needle in err, needle
    assert not (run / "02_mask.json").exists()
    r = cli("mask", "--merge-parts", "--run", "2026-09-26", "--dry-run")
    assert r.returncode == 1  # field errors are never waived by --dry-run


def test_dry_run_skips_rooms_without_an_entry(run, cli):
    write_rooms(run, ["alpha", "bravo"])
    write_parts(run, [entry("alpha")])
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "have no mask entry: bravo" in r.stderr
    r = cli("mask", "--merge-parts", "--run", "2026-09-26", "--dry-run")
    assert r.returncode == 0, r.stderr
    m = mask_json(run)
    assert m["kept"] == ["alpha"] and m["killed"] == [] and any("dry run: they were skipped" in w for w in m["warnings"])


def test_missing_currency_names_it_and_missing_inputs_exit_2(run, cli):
    write_rooms(run, ["alpha"])
    r = cli("mask", "--run", "2026-09-26")
    assert r.returncode == 2 and "02_mask_input.json is missing" in r.stderr
    write_parts(run, [entry("alpha", spend_items=[spend(currency="JPY", amount=5000)])])
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 1 and "no rate for currency JPY" in r.stderr
    (run / "01_rooms.json").unlink()
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 2 and "01_rooms.json is missing" in r.stderr
    write_rooms(run, ["alpha"])
    (run / "fx_rates.json").unlink()
    r = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r.returncode == 2 and "fx_rates.json is missing" in r.stderr


def test_not_found_price_fails_spend_and_offline_prices_pass(run, monkeypatch):
    write_rooms(run, ["seen", "blocked", "wrong"])
    write_parts(run, [
        entry("seen"),
        entry("blocked", spend_items=[spend(url="https://blocked.test/p", seen_via="page")]),
        entry("wrong", spend_items=[spend(url="https://wrong.test/p", seen_via="page")]),
    ])
    m = stage2.mask(run, merge_parts_flag=True)
    by = {v["slug"]: v for v in m["rooms"]}
    assert by["blocked"]["status"] == "kept" and by["blocked"]["spend"][0]["price_status"] == "blocked_by_network"
    assert by["blocked"]["spend"][0]["price_tag"] == "[measured, page not checked]"
    assert m["price_check"]["blocked_domains"] == ["blocked.test", "wrong.test"]
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")

    class Resp:
        def __init__(self, status, text):
            self.status_code, self.text, self.headers = status, text, {}

    monkeypatch.setattr(netfetch, "_http_get", lambda url, params=None, headers=None, timeout=30:
                        Resp(404, "") if url.endswith("robots.txt") else Resp(200, "<p>no prices on this page</p>"))
    m = stage2.mask(run, merge_parts_flag=True)
    by = {v["slug"]: v for v in m["rooms"]}
    assert by["wrong"]["status"] == "killed" and by["wrong"]["failed_tests"] == ["spend"]
    assert "the price text was not found on the page" in by["wrong"]["tests"]["spend"]["reason"]
    assert by["blocked"]["status"] == "killed"  # the fake server answers for every domain now


def test_rerun_is_idempotent_and_never_duplicates_graveyard_lines(froot, run, cli):
    write_rooms(run, ["alpha", "bravo", "charlie"], ladder={"charlie": 1})
    write_parts(run, [entry("alpha"), entry("bravo", depth=None), entry("charlie")])
    r1 = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r1.returncode == 0, r1.stderr
    first = {p: (run / p).read_bytes() for p in ("02_mask.json", "02_mask.md", "02_mask_input.json")}
    gy1 = graveyard(froot)
    r2 = cli("mask", "--merge-parts", "--run", "2026-09-26")
    assert r2.returncode == 0
    assert {p: (run / p).read_bytes() for p in first} == first
    assert graveyard(froot) == gy1
    assert gy1.count("room:bravo") == 1 and gy1.count("room:charlie") == 1
    kinds = [e["kind"] for e in common.read_jsonl(run / "runlog.jsonl") if e["command"] == "mask"]
    assert kinds.count("count") == 2


def test_priced_ladder_steps_breaks_ties_before_slug():
    """Two rooms tied on ladder length and spend points: the one with more priced ladder steps ranks first."""
    import stage2
    a = {"slug": "a-room", "ladder_steps": 7, "spend_points": 4, "spend_points_verified": 0,
         "priced_ladder_steps": 6, "reach_kind": "warm"}
    b = {"slug": "b-room", "ladder_steps": 7, "spend_points": 4, "spend_points_verified": 0,
         "priced_ladder_steps": 7, "reach_kind": "warm"}
    rank_by = ["ladder_steps", "spend_points_verified", "spend_points", "priced_ladder_steps", "warm_reach"]
    ranked = sorted([a, b], key=lambda v: stage2.rank_key(v, rank_by))
    assert [v["slug"] for v in ranked] == ["b-room", "a-room"]
