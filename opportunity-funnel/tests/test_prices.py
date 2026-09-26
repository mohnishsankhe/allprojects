import json

import common
import netfetch
import prices


class FakeResponse:
    def __init__(self, status=200, text="", headers=None):
        self.status_code = status
        self.text = text
        self.headers = headers or {}


def item(price_text="₹22,550", url="https://fees.test/gre", seen_via="page", **over):
    d = {"what": "GRE exam fee", "price_text": price_text, "amount": 22550, "currency": "INR", "unit": "one-off",
         "url": url, "seen_via": seen_via}
    d.update(over)
    return d


def _online(monkeypatch, pages):
    """Serve `pages` (url -> html) through netfetch's one network function; robots.txt answers 404."""
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")
    calls = []

    def fake_get(url, params=None, headers=None, timeout=30):
        calls.append(url)
        if url.endswith("/robots.txt"):
            return FakeResponse(404, "")
        if url in pages:
            return FakeResponse(200, pages[url], {"Content-Type": "text/html"})
        return FakeResponse(404, "nope")

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    return calls


def test_offline_page_price_is_blocked_and_kept_as_not_checked(run):
    r = prices.check_item(item(), "room x spend item 1")
    assert r["status"] == "blocked_by_network" and r["tag"] == "[measured, page not checked]"
    assert r["domain"] == "fees.test" and "fees.test" in r["detail"]
    assert prices.counts_as_spend("blocked_by_network") is True
    out = prices.check_items(run, 2, "mask", [("room x spend item 1", item())])
    assert out["counts"] == {"blocked_by_network": 1} and out["blocked_domains"] == ["fees.test"]
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "blocked" and e["domain"] == "fees.test" and e["stage"] == 2 for e in events)
    assert any(e["kind"] == "check" and e["what"] == "price-check" and e["items"] == 1 for e in events)


def test_seen_via_search_is_never_fetched(run, monkeypatch):
    calls = _online(monkeypatch, {})
    r = prices.check_item(item(seen_via="search"), "w")
    assert r["status"] == "seen_via_search" and r["tag"] == "[measured, page not checked]"
    assert "page was not opened" in r["detail"]
    assert calls == []
    assert prices.counts_as_spend("seen_via_search") is True


def test_page_found_not_found_and_ignoring_spaces(run, monkeypatch):
    pages = {
        "https://fees.test/gre": "<html><body><p>The GRE costs <b>₹ 22,550</b> in India.</p><script>x=1</script></body></html>",
        "https://fees.test/other": "<html><body><p>Registration is $220 here</p></body></html>",
        "https://fees.test/exact": "<html><body><p>Fee: ₹22,550 per attempt</p></body></html>",
    }
    calls = _online(monkeypatch, pages)
    exact = prices.check_item(item(url="https://fees.test/exact"), "a")
    assert exact["status"] == "found" and exact["tag"] == "[measured]" and "word for word" in exact["detail"]
    loose = prices.check_item(item(url="https://fees.test/gre"), "b")
    assert loose["status"] == "found" and "ignoring spaces" in loose["detail"]
    missing = prices.check_item(item(url="https://fees.test/other"), "c")
    assert missing["status"] == "not_found" and missing["tag"] == "[not found on page]"
    assert prices.counts_as_spend("not_found") is False
    gone = prices.check_item(item(url="https://fees.test/404"), "d")
    assert gone["status"] == "fetch_error" and gone["tag"] == "[measured, page not checked]"
    # the second look at the same page comes from the cache
    n = len([c for c in calls if c == "https://fees.test/exact"])
    again = prices.check_item(item(url="https://fees.test/exact"), "a")
    assert again["status"] == "found" and "from cache" in again["detail"]
    assert len([c for c in calls if c == "https://fees.test/exact"]) == n


def test_robots_disallow_is_its_own_status(run, monkeypatch):
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")

    def fake_get(url, params=None, headers=None, timeout=30):
        if url.endswith("/robots.txt"):
            return FakeResponse(200, "User-agent: *\nDisallow: /\n")
        return FakeResponse(200, "₹22,550")

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    r = prices.check_item(item(url="https://closed.test/p"), "w")
    assert r["status"] == "robots_disallowed" and r["tag"] == "[measured, page not checked]"


def test_invalid_item_is_reported_not_fetched(run):
    bad = item(price_text="", currency="rupees", seen_via="guess")
    r = prices.check_item(bad, "room x spend item 2")
    assert r["status"] == "invalid" and prices.counts_as_spend("invalid") is False
    assert "'price_text' is missing" in r["detail"] and "'currency' must be a 3-letter ISO code" in r["detail"]


def test_tag_for_every_status():
    assert prices.tag_for("found") == "[measured]"
    assert prices.tag_for("not_found") == "[not found on page]"
    for s in ("seen_via_search", "blocked_by_network", "robots_disallowed", "fetch_error", "invalid"):
        assert prices.tag_for(s) == "[measured, page not checked]"


def _mask_part(run, n, rooms):
    p = run / "02_mask.parts" / f"{n}.json"
    common.write_json(p, {"rooms": rooms})


def _entry(slug, spend):
    return {"slug": slug,
            "reach": {"kind": "warm", "ledger_id": "w1", "evidence_url": None, "reasoning": "r", "confidence": "high"},
            "depth": {"ledger_id": "d1", "reasoning": "r", "confidence": "high"},
            "spend": spend,
            "supply": {"blocked": False, "needs": [], "reasoning": "r", "confidence": "moderate"},
            "excluded": {"is_excluded": False, "exclusion_id": None, "reasoning": "r", "confidence": "high"},
            "trust_needed": {"value": False, "reasoning": "r", "confidence": "moderate"}}


def test_cli_stage2_reads_parts_when_no_merged_file(run, cli):
    _mask_part(run, 2, [_entry("room-b", [item(seen_via="search", url="https://b.test/p")])])
    _mask_part(run, 10, [_entry("room-c", [])])
    _mask_part(run, 1, [_entry("room-a", [item(), item(price_text="", url="https://a.test/bad")])])
    r = cli("price-check", "--stage", "2", "--run", "2026-09-26")
    assert r.returncode == 1, r.stdout  # the invalid item is listed as something to fix
    assert "room room-a spend item 2: " in r.stderr and "'price_text' is missing" in r.stderr
    data = json.loads((run / "price_check_stage2.json").read_text(encoding="utf-8"))
    by = {x["where"]: x for x in data["items"]}
    assert by["room room-a spend item 1"]["status"] == "blocked_by_network"
    assert by["room room-b spend item 1"]["status"] == "seen_via_search"
    assert data["counts"] == {"blocked_by_network": 1, "invalid": 1, "seen_via_search": 1}
    assert data["blocked_domains"] == ["fees.test"]
    assert "Domains to allow so these pages can be checked: fees.test" in r.stdout
    assert [x["where"] for x in data["items"]] == ["room room-a spend item 1", "room room-a spend item 2", "room room-b spend item 1"]


def test_cli_stage3_and_stage6_and_missing_inputs(run, cli):
    r = cli("price-check", "--stage", "3", "--run", "2026-09-26")
    assert r.returncode == 2 and "No room has a pains_draft.json yet" in r.stderr
    draft = common.room_dir(run, "gre-engineers-india") / "pains_draft.json"
    common.write_json(draft, {"pains": [{"pain_key": "fees", "alternatives": [item(seen_via="search"), item(url="https://tutor.test/p")]}]})
    r = cli("price-check", "--stage", "3", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "price_check_stage3.json").read_text(encoding="utf-8"))
    assert [x["where"] for x in data["items"]] == ["gre-engineers-india--fees alternative 1", "gre-engineers-india--fees alternative 2"]
    assert data["items"][1]["status"] == "blocked_by_network" and data["blocked_domains"] == ["tutor.test"]
    r = cli("price-check", "--stage", "6", "--run", "2026-09-26")
    assert r.returncode == 2 and "06_inputs/ is missing" in r.stderr
    common.write_json(run / "06_inputs" / "gre-engineers-india--fees.json",
                      {"pain_id": "gre-engineers-india--fees", "price_anchor": dict(item(seen_via="search"), reasoning="r", confidence="moderate")})
    r = cli("price-check", "--stage", "6", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    data = json.loads((run / "price_check_stage6.json").read_text(encoding="utf-8"))
    assert data["items"] == [dict(where="gre-engineers-india--fees price_anchor", url="https://fees.test/gre", domain="fees.test",
                                  price_text="₹22,550", seen_via="search", status="seen_via_search",
                                  tag="[measured, page not checked]",
                                  detail="price read in a web-search result; the page was not opened")]
    r = cli("price-check", "--stage", "4", "--run", "2026-09-26")
    assert r.returncode == 2  # argparse rejects a stage outside 2, 3, 6
