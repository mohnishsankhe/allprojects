"""Stage 3 synthesis: `funnel pains` (pipeline/stage3.py).

Covers: the counts join (missing key = error), the quote checker and quote_check.csv,
the drop rules in order, [thin], the spend distinct-domain check, [titles only],
[undated share: X%], ranking, max_pains_total with graveyard lines for every drop
and cut, needs_calls and saturation verdicts, validation errors, graveyard-dead
pains from earlier runs, determinism and the CLI.
"""
import csv
import json

import common
import counts
import records
import stage3
from conftest import Helpers

ROOM = "gre-engineers-india"
DATE = "2026-09-26"


import pytest


@pytest.fixture(autouse=True)
def _one_record_makes_a_kind(froot, h):
    """The fixture room is tiny: a kind of source counts from one record here (the run's rule is 5)."""
    h.set_rule(froot, "stage3", "source_kind_min_records", 1)

# url, text, date
RECS = {
    "r1": ("https://www.reddit.com/r/GRE/comments/1/", "I paid 45k for a premium GRE course and my quant score did not move at all", "2025-02-03"),
    "r2": ("https://www.quora.com/gre-quant-stuck", "Stuck at 160 quant after three months of practice, what am I doing wrong", None),
    "r3": ("https://www.youtube.com/watch?v=abc", "Why my GRE quant score is stuck at 160 and the fix that worked", "2025-06-01"),
    "r4": ("https://www.reddit.com/r/GRE/comments/2/", "Coaching fees for GRE in India are insane, 60k for classes that do not help", "2025-03-03"),
    "r5": ("https://forum.test/t/5", "Is the 30k GRE class fee worth it or should I self study", None),
    "r6": ("https://www.reddit.com/r/GRE/comments/3/", "Deadline for fall 2026 applications is coming and my score is not ready", "2025-08-01"),
    "r7": ("https://jobs.test/gre-tutor", "Hiring GRE quant tutor for weekend batches in Pune", None),
    "r8": ("https://prices.test/course", "GRE Prep Course pricing plans compared for 2026", None),
    "r9": ("https://blog.test/no-evidence", "Nobody ever talks about this GRE issue in the forums", None),
    "r10": ("https://blog.test/flat", "Some GRE test takers just want a study buddy for the mornings", None),
    "r11": ("https://www.reddit.com/r/GRE/comments/4/", "A study buddy for the GRE would be nice but nobody is paying for that", None),
}
KEYS = ["quant-plateau", "fees", "no-evidence", "flat"]
LABELS = {
    "r1": {"keys": ["quant-plateau"], "money": True, "failed": True},
    "r2": {"keys": ["quant-plateau"]},
    "r3": {"keys": ["quant-plateau"], "money": True},
    "r4": {"keys": ["fees"], "money": True, "failed": True},
    "r5": {"keys": ["fees"], "money": True},
    "r6": {"keys": ["quant-plateau"]},
    "r7": {"voice": "seller", "keys": ["fees"]},
    "r8": {"voice": "seller", "keys": ["quant-plateau"], "money": True},
    "r9": {"keys": ["no-evidence"]},
    "r10": {"keys": ["flat"]},
    "r11": {"keys": ["flat"]},
}


def rid(name):
    url, text, _ = RECS[name]
    return common.record_id(url, text)


def quote(name, text=None, url=None, date="keep"):
    u, t, d = RECS[name]
    return {"record_id": rid(name), "url": u if url is None else url, "date": d if date == "keep" else date,
            "text": t if text is None else text}


def price(url="https://prices.test/course", what="a prep course"):
    return {"what": what, "price_text": "₹30,000", "amount": 30000, "currency": "INR", "unit": "package", "url": url,
            "seen_via": "search"}


def judged(text, utype="none", ids=()):
    return {"type": utype, "evidence": text, "record_ids": list(ids), "reasoning": "from the records", "confidence": "moderate"}


def pain(key, quotes, urgency=None, spend=None, description=None, ladder=1, alternatives=None, sellers=None):
    return {
        "pain_key": key,
        "description": description or f"{key} in their words",
        "urgency": urgency or judged("", "none"),
        "who_pays": {"text": "the student", "reasoning": "they pay for prep", "confidence": "moderate"},
        "alternatives": [price()] if alternatives is None else alternatives,
        "sellers": [{"name": "Big Prep", "url": "https://prices.test/course", "complaints": ["no refund"],
                     "complaint_record_ids": [rid("r1")]}] if sellers is None else sellers,
        "spend_evidence": spend if spend is not None else [],
        "ladder_position": ladder,
        "quotes": quotes,
    }


def draft_pains():
    return [
        pain("quant-plateau", [quote("r1"), quote("r2", "Stuck at 160 quant after three months"), quote("r3", "GRE quant score is stuck at 160")],
             urgency=judged("applications close in the fall", "deadline_or_rule", [rid("r6")]),
             spend=[{"kind": "record", "record_id": rid("r1")}, {"kind": "price", "url": "https://prices.test/course"}]),
        pain("fees", [quote("r4", "60k for classes that do not help"), quote("r5", url="https://wrong.test/x", date="2020-01-01"),
                      quote("r4", "sixty thousand for classes that do not help")],
             spend=[{"kind": "record", "record_id": rid("r4")}, {"kind": "job_posting", "record_id": rid("r1")}]),
        pain("no-evidence", [quote("r9"), quote("r9", "issue in the forums")]),
        pain("flat", [quote("r10"), quote("r11")]),
    ]


def setup_room(run, h, room=ROOM, pains=None, sources=True, saturation=True, extra_sources=()):
    recs = [Helpers.make_record(url, text, date=date, rank=i) for i, (url, text, date) in enumerate(RECS.values(), 1)]
    records.store_records(run, room, "websearch", recs)
    for src, url, text, keys in extra_sources:
        records.store_records(run, room, src, [Helpers.make_record(url, text, rank=90)])
    records.make_batches(run, room)
    h.write_taxonomy(run, room, KEYS)
    rows = [h.label(rid(n), **LABELS[n]) for n in RECS]
    for src, url, text, keys in extra_sources:
        rows.append(h.label(common.record_id(url, text), keys=keys, money=True))
    h.write_labels(run, room, "batch_r1_001", rows)
    common.write_json(common.room_dir(run, room) / "counts.json", counts.compute_counts(run, room))
    if sources:
        common.write_json(common.room_dir(run, room) / "sources.json", {
            "used": ["websearch"], "skipped": [],
            "needs_calls": {"value": True, "reasoning": "older test takers rarely post", "confidence": "moderate"}})
    if saturation:
        common.write_json(common.room_dir(run, room) / "saturation.json", {
            "room": room, "window": 300, "final": True, "stop_reason": "exhausted",
            "rounds": [{"round": 1, "records": 11, "new_records": 11, "window": 300, "evaluable": False,
                        "new_pains": [], "rank_changes": [], "saturated": False}]})
    common.write_json(common.room_dir(run, room) / "pains_draft.json", {"pains": draft_pains() if pains is None else pains})


def pains_json(run):
    return json.loads((common.listen_dir(run) / "pains.json").read_text(encoding="utf-8"))


def by_id(result):
    return {p["pain_id"]: p for p in result["pains"]}


def graveyard(froot):
    return (froot / "graveyard.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- join, quotes, rules, tags, ranking
def test_join_quote_check_rules_tags_and_ranking(froot, run, h, cli):
    setup_room(run, h)
    r = cli("pains", "--run", DATE)
    assert r.returncode == 0, r.stderr
    data = pains_json(run)
    p = by_id(data)
    q, f, n, fl = (p[f"{ROOM}--{k}"] for k in KEYS)
    # the counts join
    assert q["record_count"] == 4 and q["money_mentions"] == 2 and q["failed_spend_mentions"] == 1
    assert q["seller_records"] == 1 and q["media_records"] == 0 and q["label"] == "quant-plateau"
    assert f["record_count"] == 2 and f["money_mentions"] == 2 and f["failed_spend_mentions"] == 1
    # the quote checker: pass, corrected citation, deleted failure
    assert q["verified_quote_count"] == 3 and q["quote_check"] == {"checked": 3, "passed": 3, "failed": 0, "citations_corrected": 0, "failed_reasons": {}}
    assert f["verified_quote_count"] == 2 and f["quote_check"]["failed_reasons"] == {"not_substring": 1}
    assert f["quote_check"]["citations_corrected"] == 1
    corrected = [x for x in f["quotes"] if x["record_id"] == rid("r5")][0]
    assert corrected["url"] == RECS["r5"][0] and corrected["date"] is None
    assert all(x["text"] != "sixty thousand for classes that do not help" for x in f["quotes"])
    assert "1 quote(s) failed the quote check and were deleted: not_substring 1." in f["notes"]
    assert "1 citation(s) corrected to the stored url and date." in f["notes"]
    # drop rules in order
    assert n["status"] == "dropped" and n["drop_reason"].startswith("fewer than 2 verified quotes: 1 of 2 passed the quote check (too_short 1)")
    assert fl["status"] == "dropped" and fl["drop_reason"].startswith("no money mention, no failed spend and urgency none")
    # tags
    assert q["tags"] == ["[thin]", "[titles only]", "[undated share: 25%]"]
    assert q["spend_domains"] == ["prices.test", "reddit.com"] and q["spend_sources"] == 2
    assert f["tags"] == ["[thin]", "[spend: 1 source]", "[titles only]", "[undated share: 33%]"]
    assert f["spend_domains"] == ["reddit.com"]
    assert f["spend_evidence"][1]["domain"] == "reddit.com"  # a record's domain comes from its stored URL
    assert q["supporting_records"] == 4 and q["undated_records"] == 1 and q["sources"] == {"websearch": 4}
    # ranking: equal failed spend and money, urgency breaks the tie
    assert data["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--fees"] and data["cut"] == []
    assert data["dropped"] == [f"{ROOM}--flat", f"{ROOM}--no-evidence"]
    assert q["rank"] == 1 and f["rank"] == 2 and q["urgency_type"] == "deadline_or_rule"
    assert data["counts"] == {"rooms": 1, "drafted": 4, "survived": 2, "kept": 2, "cut": 0, "dropped": 2, "quotes_pass": 8, "quotes_fail": 2}
    # graveyard: one line per drop, none for kept
    gy = graveyard(froot)
    assert f"- {DATE} | stage 3 | pain:{ROOM}--no-evidence | fewer than 2 verified quotes" in gy
    assert f"- {DATE} | stage 3 | pain:{ROOM}--flat | no money mention, no failed spend and urgency none" in gy
    assert "quant-plateau" not in gy and "pain:gre-engineers-india--fees" not in gy
    assert common.dead_items("pain") == {f"pain:{ROOM}--flat", f"pain:{ROOM}--no-evidence"}
    # needs_calls and saturation verdicts
    assert data["needs_calls"] == [ROOM]
    info = data["rooms"][ROOM]
    assert info["needs_calls"] is True and info["needs_calls_reasoning"] == "older test takers rarely post"
    assert info["saturation"]["verdict"] == "not evaluable after round 1: 11 records (needs window + 1); stopped: exhausted"
    assert info["saturation"]["saturated"] is False and info["saturation"]["stop_reason"] == "exhausted"
    assert info == dict(info, labeled=11, member_records=9, pains_drafted=4, pains_kept=2, pains_cut=0, pains_dropped=2)
    assert "Rooms that need calls (public text under-represents their people): gre-engineers-india." in data["review_notes"]
    assert any(n.startswith("Rooms that stopped before saturation: gre-engineers-india (not evaluable") for n in data["review_notes"])
    # CLI output
    assert "Pains: 1 room(s), 4 drafted, 2 kept (max 25), 0 cut, 2 dropped. Quotes: 8 pass, 2 fail." in r.stdout
    assert f"kept #1: {ROOM}--quant-plateau (failed spend 1, money 2, urgency deadline_or_rule, records 4, quotes 3/3, tags: [thin] [titles only] [undated share: 25%])" in r.stdout
    assert f"dropped: {ROOM}--flat: no money mention" in r.stdout
    assert "review: Rooms that need calls" in r.stdout and "needs calls: yes" in r.stdout
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "count" and e["command"] == "pains" and e["kept"] == 2 and e["needs_calls"] == [ROOM] for e in events)
    assert any(e["kind"] == "note" and e.get("review") is True and "need calls" in e["note"] for e in events)


def test_quote_check_csv(run, h):
    setup_room(run, h)
    stage3.pains(run)
    with open(common.listen_dir(run) / "quote_check.csv", newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert list(rows[0].keys()) == ["pain_id", "record_id", "status", "reason", "citation_corrected", "url", "date", "quote"]
    assert [x["reason"] for x in rows] == ["ok", "ok", "ok", "ok", "ok", "not_substring", "ok", "too_short", "ok", "ok"]
    assert [x["pain_id"] for x in rows[:3]] == [f"{ROOM}--quant-plateau"] * 3
    assert rows[4]["citation_corrected"] == "yes" and rows[4]["url"] == RECS["r5"][0] and rows[4]["date"] == ""
    assert rows[0]["date"] == "2025-02-03" and rows[5]["status"] == "fail"
    raw = (common.listen_dir(run) / "quote_check.csv").read_bytes()
    assert raw.endswith(b"\n") and b"\r\n" not in raw


def test_rule_order_and_switches(froot, run, h):
    # a pain that fails rule 1 and rule 2 gets rule 1's reason; rule 2 can be switched off
    setup_room(run, h)
    n = by_id(stage3.pains(run))[f"{ROOM}--no-evidence"]
    assert n["money_mentions"] == 0 and n["failed_spend_mentions"] == 0 and n["urgency_type"] == "none"
    assert n["drop_reason"].startswith("fewer than 2 verified quotes")
    h.set_rule(froot, "stage3", "drop_if_no_money_no_failed_spend_no_urgency", False)
    result = stage3.pains(run)
    assert by_id(result)[f"{ROOM}--flat"]["status"] == "kept"
    assert result["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--fees", f"{ROOM}--flat"]
    h.set_rule(froot, "stage3", "min_verified_quotes", 1)
    result = stage3.pains(run)
    assert by_id(result)[f"{ROOM}--no-evidence"]["status"] == "kept" and result["counts"]["dropped"] == 0
    h.set_rule(froot, "stage3", "quote_min_words", 14)
    result = stage3.pains(run)
    assert by_id(result)[f"{ROOM}--fees"]["status"] == "dropped"  # its quotes are shorter than 14 words now
    assert by_id(result)[f"{ROOM}--fees"]["quote_check"]["failed_reasons"] == {"not_substring": 1, "too_short": 2}


def test_urgency_none_with_money_or_failed_spend_survives_rule_two(run, h):
    drafts = draft_pains()
    drafts[3]["quotes"] = [quote("r10"), quote("r11")]
    setup_room(run, h, pains=drafts)
    room = common.room_dir(run, ROOM)
    c = common.read_json(room / "counts.json")
    c["pains"]["flat"]["money_mentions"] = 1
    common.write_json(room / "counts.json", c)
    assert by_id(stage3.pains(run))[f"{ROOM}--flat"]["status"] == "kept"
    c["pains"]["flat"]["money_mentions"] = 0
    c["pains"]["flat"]["failed_spend_mentions"] = 1
    common.write_json(room / "counts.json", c)
    assert by_id(stage3.pains(run))[f"{ROOM}--flat"]["status"] == "kept"
    c["pains"]["flat"]["failed_spend_mentions"] = 0
    common.write_json(room / "counts.json", c)
    drafts[3]["urgency"] = judged("exam in two weeks", "fear", [rid("r10")])
    common.write_json(room / "pains_draft.json", {"pains": drafts})
    assert by_id(stage3.pains(run))[f"{ROOM}--flat"]["status"] == "kept"


def test_thin_threshold_and_spend_source_count(froot, run, h):
    setup_room(run, h)
    h.set_rule(froot, "stage3", "thin_below_records", 4)
    p = by_id(stage3.pains(run))
    assert "[thin]" not in p[f"{ROOM}--quant-plateau"]["tags"] and "[thin]" in p[f"{ROOM}--fees"]["tags"]
    h.set_rule(froot, "stage3", "spend_sources_min", 3)
    p = by_id(stage3.pains(run))
    assert "[spend: 2 sources]" in p[f"{ROOM}--quant-plateau"]["tags"]
    drafts = draft_pains()
    drafts[1]["spend_evidence"] = []
    common.write_json(common.room_dir(run, ROOM) / "pains_draft.json", {"pains": drafts})
    p = by_id(stage3.pains(run))
    assert "[spend: 0 sources]" in p[f"{ROOM}--fees"]["tags"] and p[f"{ROOM}--fees"]["status"] == "kept"  # tagged, never killed
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert "Spend evidence: 0 distinct domain(s): none." in md


def test_titles_only_lifts_when_a_full_text_source_supports_the_pain(run, h):
    setup_room(run, h, extra_sources=[("reddit", "https://www.reddit.com/r/GRE/comments/9/",
                                        "Long post: I bought two courses and my quant score is still 158", ["quant-plateau"])])
    p = by_id(stage3.pains(run))
    q, f = p[f"{ROOM}--quant-plateau"], p[f"{ROOM}--fees"]
    assert "[titles only]" not in q["tags"] and q["sources"] == {"reddit": 1, "websearch": 4}
    assert "[titles only]" in f["tags"]
    assert q["tags"][-1] == "[undated share: 40%]"  # 2 undated of 5 supporting records
    assert q["record_count"] == 5 and q["money_mentions"] == 3


def test_ranking_order_max_pains_total_and_cut_lines(froot, run, h):
    setup_room(run, h)
    h.set_rule(froot, "stage3", "drop_if_no_money_no_failed_spend_no_urgency", False)
    result = stage3.pains(run)
    # failed spend, then money, then urgency, then record count, then pain id
    assert result["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--fees", f"{ROOM}--flat"]
    c = common.read_json(common.room_dir(run, ROOM) / "counts.json")
    c["pains"]["flat"]["failed_spend_mentions"] = 2
    common.write_json(common.room_dir(run, ROOM) / "counts.json", c)
    assert stage3.pains(run)["kept"][0] == f"{ROOM}--flat"
    c["pains"]["flat"]["failed_spend_mentions"] = 1
    c["pains"]["flat"]["money_mentions"] = 3
    common.write_json(common.room_dir(run, ROOM) / "counts.json", c)
    assert stage3.pains(run)["kept"][0] == f"{ROOM}--flat"
    c["pains"]["flat"]["money_mentions"] = 2  # ties with the others; urgency none loses to quant, ties with fees; records 2 = 2; pain id
    common.write_json(common.room_dir(run, ROOM) / "counts.json", c)
    assert stage3.pains(run)["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--fees", f"{ROOM}--flat"]
    c["pains"]["flat"]["record_count"] = 3
    common.write_json(common.room_dir(run, ROOM) / "counts.json", c)
    assert stage3.pains(run)["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--flat", f"{ROOM}--fees"]
    h.set_rule(froot, "stage3", "rank_by", ["record_count"])
    assert stage3.pains(run)["kept"] == [f"{ROOM}--quant-plateau", f"{ROOM}--flat", f"{ROOM}--fees"]
    h.set_rule(froot, "stage3", "rank_by", ["urgency", "record_count"])
    h.set_rule(froot, "stage3", "urgency_order", ["none", "deadline_or_rule"])
    assert stage3.pains(run)["kept"] == [f"{ROOM}--flat", f"{ROOM}--fees", f"{ROOM}--quant-plateau"]
    # the cut
    h.set_rule(froot, "stage3", "rank_by", ["failed_spend_mentions", "money_mentions", "urgency", "record_count"])
    h.set_rule(froot, "stage3", "urgency_order", ["deadline_or_rule", "acute_pain", "fear", "expiring_gain", "none"])
    h.set_rule(froot, "stage3", "max_pains_total", 1)
    result = stage3.pains(run)
    assert result["kept"] == [f"{ROOM}--quant-plateau"] and result["cut"] == [f"{ROOM}--flat", f"{ROOM}--fees"]
    p = by_id(result)
    assert p[f"{ROOM}--fees"]["status"] == "cut" and p[f"{ROOM}--fees"]["rank"] == 3
    assert p[f"{ROOM}--fees"]["drop_reason"].startswith("cut: ranked 3 of 3 survivors and max_pains_total is 1;")
    gy = graveyard(froot)
    assert f"- {DATE} | stage 3 | pain:{ROOM}--fees | cut: ranked 3 of 3 survivors and max_pains_total is 1; failed spend 1, money 2, urgency none, member records 2" in gy
    assert f"pain:{ROOM}--flat | cut: ranked 2 of 3" in gy and f"pain:{ROOM}--quant-plateau" not in gy
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert "## Cut for rank (2)" in md and f"- rank 3: {ROOM}--fees (failed spend 1, money 2, urgency none" in md
    assert data_room_line(md) == "| gre-engineers-india | 11 | 9 | 4 | 1 |"


def data_room_line(md):
    line = [ln for ln in md.splitlines() if ln.startswith("| gre-engineers-india |")][0]
    return "|".join(line.split("|")[:6]) + "|"


# --------------------------------------------------------------------------- rooms, verdicts, notes
def test_second_room_missing_sources_and_saturation_are_noted_not_fatal(run, h):
    setup_room(run, h)
    other = "cfa-candidates"
    setup_room(run, h, room=other, sources=False, saturation=False, pains=[draft_pains()[0]])
    result = stage3.pains(run)
    assert sorted(result["rooms"]) == [other, ROOM] and result["counts"]["rooms"] == 2
    assert result["rooms"][other]["needs_calls"] is None and result["rooms"][other]["saturation"]["available"] is False
    assert result["rooms"][other]["saturation"]["verdict"] == "no saturation.json: the room never ran `funnel saturation`"
    assert result["needs_calls"] == [ROOM]
    assert f"room {other}: no sources.json, so needs_calls is unknown (the listener writes it in mode synthesize)." in result["notes"]
    assert f"Rooms with no saturation verdict (saturation.json missing): {other}." in result["review_notes"]
    assert result["kept"] == [f"{other}--quant-plateau", f"{ROOM}--quant-plateau", f"{ROOM}--fees"]  # tie -> pain id
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert "| cfa-candidates | 11 | 9 | 1 | 1 | no saturation.json: the room never ran `funnel saturation` | unknown |" in md


def test_saturated_room_verdict(run, h):
    setup_room(run, h)
    sat = common.room_dir(run, ROOM) / "saturation.json"
    data = common.read_json(sat)
    data["rounds"] = [{"round": 1, "records": 400, "new_records": 400, "window": 300, "evaluable": True, "new_pains": [], "rank_changes": [], "saturated": False},
                      {"round": 2, "records": 700, "new_records": 300, "window": 300, "evaluable": True, "new_pains": [], "rank_changes": [], "saturated": True}]
    data["stop_reason"] = "saturated"
    common.write_json(sat, data)
    result = stage3.pains(run)
    s = result["rooms"][ROOM]["saturation"]
    assert s["verdict"] == "round 2: 700 records; saturated; stopped: saturated" and s["rounds"] == 2 and s["saturated"] is True
    assert not any("stopped before saturation" in n for n in result["review_notes"])
    data["stop_reason"] = None
    data["rounds"][1]["saturated"] = False
    data["rounds"][1]["new_pains"] = ["new-one"]
    common.write_json(sat, data)
    result = stage3.pains(run)
    s = result["rooms"][ROOM]["saturation"]
    assert s["verdict"] == "round 2: 700 records; not saturated; not final (no stop reason recorded)" and s["new_pains"] == ["new-one"]
    assert any("stopped before saturation: gre-engineers-india (round 2: 700 records; not saturated" in n for n in result["review_notes"])


# --------------------------------------------------------------------------- validation
def test_validation_errors_list_every_problem_and_write_nothing(run, h, cli):
    drafts = draft_pains()
    drafts[0]["pain_key"] = "not-in-counts"
    drafts[1]["urgency"]["type"] = "panic"
    drafts[1]["urgency"]["record_ids"] = ["0000000000000000"]
    drafts[1]["who_pays"] = {"text": ""}
    drafts[1]["spend_evidence"].append({"kind": "invoice", "url": "ftp://x"})
    drafts[1]["spend_evidence"].append({"kind": "price"})
    drafts[1]["alternatives"] = [{"what": "x"}]
    drafts[1]["ladder_position"] = 0
    drafts[2]["urgency"] = judged("", "fear", [])
    drafts[2]["sellers"] = [{"name": "", "url": "nope", "complaints": "text", "complaint_record_ids": ["1111111111111111"]}]
    drafts[3]["pain_key"] = "Flat!"
    drafts.append(pain("fees", [quote("r4")]))
    setup_room(run, h, pains=drafts)
    common.write_json(common.room_dir(run, ROOM) / "sources.json", {"needs_calls": {"value": "yes"}})
    r = cli("pains", "--run", DATE)
    assert r.returncode == 1, r.stdout + r.stderr
    err = r.stderr
    for needle in (
        "pain 1 (not-in-counts): pain_key 'not-in-counts' is not in counts.json",
        "pain 2 (fees): urgency.type must be one of deadline_or_rule, acute_pain, fear, expiring_gain, none (got 'panic')",
        "urgency.record_ids: record 0000000000000000 is not stored for this room",
        "who_pays.text is missing or empty", "who_pays: missing 'reasoning'",
        "spend_evidence 3: 'kind' must be one of record, price, job_posting (got 'invoice')",
        "spend_evidence 3: 'url' must start with http:// or https://",
        "spend_evidence 4: a price item needs a 'url'",
        "alternative 1: 'price_text' is missing or empty", "alternative 1: 'url' must start with http",
        "'ladder_position' must be a whole number from 1",
        "pain 3 (no-evidence): urgency.evidence is empty", "urgency.record_ids is empty; an urgency of type fear must cite",
        "seller 1: 'name' is missing or empty", "seller 1: 'url' must start with http", "seller 1: 'complaints' must be a list",
        "seller 1: complaint_record_ids: record 1111111111111111 is not stored",
        "pain 4 (Flat!): 'pain_key' 'Flat!' must be a slug",
        "pain 5 (fees): pain_key 'fees' appears twice in the draft",
        "sources.json: needs_calls must be an object like",
    ):
        assert needle in err, needle
    assert not (common.listen_dir(run) / "pains.json").exists() and not (common.listen_dir(run) / "quote_check.csv").exists()
    assert "pain:" not in (run.parent.parent / "graveyard.md").read_text(encoding="utf-8")


def test_missing_inputs_exit_2(run, h, cli):
    r = cli("pains", "--run", DATE)
    assert r.returncode == 2 and "No pains_draft.json in any room" in r.stderr
    setup_room(run, h)
    (common.room_dir(run, ROOM) / "counts.json").unlink()
    r = cli("pains", "--run", DATE)
    assert r.returncode == 2 and "counts.json is missing. Run `funnel count --room gre-engineers-india` first." in r.stderr


def test_bad_json_and_bad_shape_are_validation_errors(run, h, cli):
    setup_room(run, h)
    draft = common.room_dir(run, ROOM) / "pains_draft.json"
    draft.write_text("{not json", encoding="utf-8")
    r = cli("pains", "--run", DATE)
    assert r.returncode == 1 and "pains_draft.json: not valid JSON" in r.stderr
    common.write_json(draft, {"pains": {"a": 1}})
    r = cli("pains", "--run", DATE)
    assert r.returncode == 1 and "needs a 'pains' list" in r.stderr
    common.write_json(draft, {"pains": ["text"]})
    r = cli("pains", "--run", DATE)
    assert r.returncode == 1 and "pain 1 (?): must be an object" in r.stderr


# --------------------------------------------------------------------------- graveyard
def test_pain_dead_in_an_earlier_run_stays_dropped_unless_revived(froot, run, h):
    setup_room(run, h)
    gy = froot / "graveyard.md"
    gy.write_text(gy.read_text(encoding="utf-8") + f"- 2026-09-20 | stage 5 | pain:{ROOM}--fees | no pair, no clean trade, no plausible partner\n"
                  f"- {DATE} | stage 4 | pain:{ROOM}--quant-plateau | outcome reached today\n", encoding="utf-8")
    result = stage3.pains(run)
    p = by_id(result)
    assert p[f"{ROOM}--fees"]["status"] == "dropped"
    assert p[f"{ROOM}--fees"]["drop_reason"] == ("dead in graveyard.md since 2026-09-20 (stage 5): no pair, no clean trade, no plausible partner. "
                                                "Revive it with a new-evidence line first.")
    assert p[f"{ROOM}--quant-plateau"]["status"] == "kept"  # this run's own later-stage kill is ignored
    text = gy.read_text(encoding="utf-8")
    assert text.count(f"pain:{ROOM}--fees") == 1  # no second line for a pain that is already dead
    gy.write_text(text.replace(f"no plausible partner\n", f"no plausible partner\n  - new evidence 2026-09-25: r4 shows a paid fix <{RECS['r4'][0]}>\n"),
                  encoding="utf-8")
    assert by_id(stage3.pains(run))[f"{ROOM}--fees"]["status"] == "kept"


# --------------------------------------------------------------------------- determinism and rendering
def test_rerun_is_byte_identical_and_never_duplicates_graveyard_lines(froot, run, h, cli):
    setup_room(run, h)
    h.set_rule(froot, "stage3", "max_pains_total", 1)
    r1 = cli("pains", "--run", DATE)
    assert r1.returncode == 0, r1.stderr
    ldir = common.listen_dir(run)
    first = {n: (ldir / n).read_bytes() for n in ("pains.json", "pains.md", "quote_check.csv")}
    gy1 = graveyard(froot)
    r2 = cli("pains", "--run", DATE)
    assert r2.returncode == 0 and r1.stdout == r2.stdout
    assert {n: (ldir / n).read_bytes() for n in first} == first
    assert graveyard(froot) == gy1
    assert gy1.count(f"pain:{ROOM}--fees") == 1 and gy1.count(f"pain:{ROOM}--flat") == 1
    raw = first["pains.json"].decode("utf-8")
    assert raw == json.dumps(json.loads(raw), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    assert "\\u" not in raw and "₹30,000" in raw


def test_pains_md_is_readable(run, h):
    setup_room(run, h)
    stage3.pains(run)
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert md.startswith("# Stage 3: pains\n\nRun: 2026-09-26.\n1 room(s) with a pains draft. 4 pains drafted. 2 kept (at most 25 across all rooms), 0 cut for rank, 2 dropped.")
    assert "Drop rules, in order:" in md and "1. fewer than 2 verified quotes (a quote needs at least 5 words);" in md
    assert "- `[spend: N source(s)]`: spending evidence comes from fewer distinct websites (domains) than spend_sources_min." in md
    assert "## Kept pains (2)" in md
    assert "| 1 | gre-engineers-india--quant-plateau | gre-engineers-india | deadline_or_rule | 1 | 2 | 4 | 3 | 2 | [thin] [titles only] [undated share: 25%] |" in md
    assert "### 1. gre-engineers-india--quant-plateau: quant-plateau" in md
    assert "- Urgency: deadline_or_rule. applications close in the fall from the records (confidence moderate; records: " + rid("r6") + ")" in md
    assert "- Counts [measured]: member records 4, money mentions 2, failed spend mentions 1, seller records 1, media records 0. Supporting records 4 (1 undated). Sources: websearch 4." in md
    assert "- Spend evidence: 2 distinct domain(s): prices.test, reddit.com." in md
    assert "  - a prep course: ₹30,000 (INR 30000 per package) [measured, page not checked] <https://prices.test/course>" in md
    assert "  - Big Prep <https://prices.test/course>: no refund (records: " + rid("r1") + ")" in md
    assert "- Quotes (3 verified of 3 checked):" in md
    assert f'  - "{RECS["r1"][1]}" <{RECS["r1"][0]}> (2025-02-03; record {rid("r1")})' in md
    assert '  - "Stuck at 160 quant after three months" <https://www.quora.com/gre-quant-stuck> (undated; record ' in md
    assert "## Dropped pains (2)" in md and "| gre-engineers-india--flat | no money mention, no failed spend and urgency none (money 0, failed spend 0, urgency none, member records 2) |" in md
    assert "## Rooms" in md and "| Room | Labeled records | Member records | Pains drafted | Kept | Saturation | Needs calls |" in md
    assert "## For REVIEW.md" in md and "- Rooms that need calls (public text under-represents their people): gre-engineers-india." in md
    assert "## Notes" in md and "Kept pains tagged [thin] (fewer than 15 member records): gre-engineers-india--quant-plateau, gre-engineers-india--fees." in md
    assert "Kept pains supported by web-search titles only: gre-engineers-india--quant-plateau, gre-engineers-india--fees." in md


def test_helpers(run, h):
    setup_room(run, h)
    stored = records.records_by_id(run, ROOM)
    assert stage3.spend_domains([{"kind": "record", "record_id": rid("r1")}, {"kind": "price", "url": "https://WWW.Prices.test/x"},
                                 {"kind": "record", "record_id": "nope"}, "junk"], stored) == ["prices.test", "reddit.com"]
    assert stage3.undated_share([rid("r1"), rid("r2"), "missing"], stored) == (50, 1, 2)
    assert stage3.undated_share([], stored) == (0, 0, 0)
    assert stage3.supporting_record_ids([rid("r1"), "x"], [{"record_id": rid("r2")}], [{"record_id": rid("r3")}], stored) == sorted([rid("r1"), rid("r2"), rid("r3")])
    assert stage3.draft_rooms(run) == [ROOM]
    assert stage3.rank_key({"failed_spend_mentions": 1, "money_mentions": 2, "urgency_type": "fear", "record_count": 7, "pain_id": "a--b"},
                           stage3.DEFAULT_RANK_BY, stage3.DEFAULT_URGENCY_ORDER) == (-1, -2, 2, -7, "a--b")
    assert stage3.rank_key({"failed_spend_mentions": 0, "money_mentions": 0, "urgency_type": "odd", "record_count": 0, "pain_id": "a--b"},
                           ["urgency"], stage3.DEFAULT_URGENCY_ORDER) == (5, "a--b")


# --------------------------------------------------------------------------- one piece of evidence counts once
def test_a_quote_listed_twice_does_not_reach_min_verified_quotes(froot, run, h):
    """Rule 1: at least two verified quotes means two pieces of evidence. The same quote twice (or a part of it)
    verifies once, so the pain is dropped, and quote_check.csv names the later copies `duplicate`. The same
    words from two records are two pieces of evidence."""
    setup_room(run, h, pains=[
        pain("quant-plateau", [quote("r1"), quote("r1"), quote("r1", "I paid 45k for a premium GRE course")],
             urgency=judged("applications close in the fall", "deadline_or_rule", [rid("r6")])),
        pain("fees", [quote("r4", "60k for classes that do not help"), quote("r5"), quote("r4", "60k for classes that do not help")]),
    ])
    result = stage3.pains(run)
    p = by_id(result)
    qp = p[f"{ROOM}--quant-plateau"]
    assert qp["status"] == "dropped" and qp["verified_quote_count"] == 1 and len(qp["quotes"]) == 1
    assert qp["drop_reason"] == "fewer than 2 verified quotes: 1 of 3 passed the quote check (duplicate 2)"
    assert qp["quote_check"] == {"checked": 3, "passed": 1, "failed": 2, "citations_corrected": 0, "failed_reasons": {"duplicate": 2}}
    assert "2 quote(s) failed the quote check and were deleted: duplicate 2." in qp["notes"]
    fees = p[f"{ROOM}--fees"]
    assert fees["status"] == "kept" and fees["verified_quote_count"] == 2 and fees["quote_check"]["failed_reasons"] == {"duplicate": 1}
    assert result["counts"]["quotes_pass"] == 3 and result["counts"]["quotes_fail"] == 3
    with open(common.listen_dir(run) / "quote_check.csv", newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert [r["reason"] for r in rows if r["pain_id"] == f"{ROOM}--quant-plateau"] == ["ok", "duplicate", "duplicate"]
    assert [r["reason"] for r in rows if r["pain_id"] == f"{ROOM}--fees"] == ["ok", "ok", "duplicate"]
    assert f"- {DATE} | stage 3 | pain:{ROOM}--quant-plateau | fewer than 2 verified quotes: 1 of 3 passed the quote check (duplicate 2)" in graveyard(froot)
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert md.count('"60k for classes that do not help"') == 1


# --------------------------------------------------------------------------- the graveyard says what the run finally decided
def test_rerun_that_keeps_a_pain_removes_its_stale_same_date_line(froot, run, h, cli):
    """A pain cut by the first run of `pains` (a line dated today) and kept by a rerun after the limit was
    raised loses its line, so a later run keeps it too instead of dropping it for a kill that was never final.
    The run's real drops keep their lines and still apply later."""
    setup_room(run, h)
    h.set_rule(froot, "stage3", "max_pains_total", 1)
    r = cli("pains", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert f"- {DATE} | stage 3 | pain:{ROOM}--fees | cut: ranked 2 of 2 survivors and max_pains_total is 1;" in graveyard(froot)
    h.set_rule(froot, "stage3", "max_pains_total", 25)
    r = cli("pains", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert by_id(pains_json(run))[f"{ROOM}--fees"]["status"] == "kept"
    gy = graveyard(froot)
    assert f"pain:{ROOM}--fees" not in gy
    assert gy.count(f"pain:{ROOM}--no-evidence") == 1 and gy.count(f"pain:{ROOM}--flat") == 1
    later = froot / "runs" / "2026-10-03"
    later.mkdir()
    setup_room(later, h)
    p = by_id(stage3.pains(later))
    assert p[f"{ROOM}--fees"]["status"] == "kept" and p[f"{ROOM}--quant-plateau"]["status"] == "kept"
    assert p[f"{ROOM}--flat"]["status"] == "dropped" and "dead in graveyard.md since 2026-09-26 (stage 3)" in p[f"{ROOM}--flat"]["drop_reason"]


def test_pain_killed_again_after_a_revival_stays_dropped(froot, run, h):
    """Rule 7: a revival note revives only the line it sits under; a later kill line kills the pain again."""
    setup_room(run, h)
    gy = froot / "graveyard.md"
    gy.write_text(gy.read_text(encoding="utf-8")
                  + f"- 2026-08-01 | stage 3 | pain:{ROOM}--fees | fewer than 2 verified quotes\n"
                  f"  - new evidence 2026-08-15: 3 verified quotes now, see record {rid('r4')}\n"
                  f"- 2026-09-01 | stage 6 | pain:{ROOM}--fees | numbers fail in the base case: usd_per_hour\n", encoding="utf-8")
    p = by_id(stage3.pains(run))
    assert p[f"{ROOM}--fees"]["status"] == "dropped"
    assert p[f"{ROOM}--fees"]["drop_reason"] == ("dead in graveyard.md since 2026-09-01 (stage 6): numbers fail in the base case: "
                                                "usd_per_hour. Revive it with a new-evidence line first.")
    text = gy.read_text(encoding="utf-8")
    assert text.count(f"pain:{ROOM}--fees") == 2  # no third line for a pain that is already dead
    gy.write_text(text.replace("usd_per_hour\n", "usd_per_hour\n  - new evidence 2026-09-20: a cheaper delivery, see record x\n"), encoding="utf-8")
    assert by_id(stage3.pains(run))[f"{ROOM}--fees"]["status"] == "kept"


# --------------------------------------------------------------------------- alternatives carry the checker's tag
def test_alternatives_carry_the_price_checkers_tag_not_the_models_claim(run, h, monkeypatch):
    """Rule 8: `seen_via: page` is [measured] only when the page was opened and shows the price text. Offline it
    is [measured, page not checked] (and the domain is listed); a page without the price is [not found on page]."""
    import netfetch
    alt = {"what": "a private tutor", "price_text": "$49/month", "amount": 49, "currency": "USD", "unit": "month",
           "url": "https://x.test/pricing", "seen_via": "page"}
    setup_room(run, h, pains=[pain("quant-plateau", [quote("r1"), quote("r2", "Stuck at 160 quant after three months")],
                                   urgency=judged("applications close in the fall", "deadline_or_rule", [rid("r6")]),
                                   alternatives=[alt, price()])])
    result = stage3.pains(run)
    alts = by_id(result)[f"{ROOM}--quant-plateau"]["alternatives"]
    assert [a["price_status"] for a in alts] == ["blocked_by_network", "seen_via_search"]
    assert [a["price_tag"] for a in alts] == ["[measured, page not checked]", "[measured, page not checked]"]
    assert alts[0]["price_detail"] == "the network blocks x.test; the page was not opened"
    assert result["price_check"] == {"counts": {"blocked_by_network": 1, "seen_via_search": 1}, "blocked_domains": ["x.test"]}
    md = (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert "  - a private tutor: $49/month (USD 49 per month) [measured, page not checked] <https://x.test/pricing>" in md
    assert "[measured] <" not in md
    assert "Domains to allow so the price pages can be opened: x.test." in md
    assert any(e["kind"] == "blocked" and e["domain"] == "x.test" and e["command"] == "pains" for e in common.read_jsonl(run / "runlog.jsonl"))
    pages = {"https://x.test/pricing": "<html><body><h1>Plans</h1><p>from $49/month</p></body></html>"}
    monkeypatch.setattr(netfetch, "fetch", lambda url, **kw: {"url": url, "status": 200, "text": pages[url], "headers": {}, "from_cache": False})
    a = by_id(stage3.pains(run))[f"{ROOM}--quant-plateau"]["alternatives"][0]
    assert a["price_status"] == "found" and a["price_tag"] == "[measured]"
    assert "  - a private tutor: $49/month (USD 49 per month) [measured] <https://x.test/pricing>" in (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    pages["https://x.test/pricing"] = "<html><body>Contact us for pricing</body></html>"
    a = by_id(stage3.pains(run))[f"{ROOM}--quant-plateau"]["alternatives"][0]
    assert a["price_status"] == "not_found" and a["price_tag"] == "[not found on page]"
    assert "[not found on page] <https://x.test/pricing>" in (common.listen_dir(run) / "pains.md").read_text(encoding="utf-8")
    assert stage3.price_tag_of({"seen_via": "page"}) == "[measured, page not checked]"


def test_room_with_too_few_source_kinds_is_tagged_and_noted(froot, run, h):
    # with 5 records needed per kind, the fixture room has one kind (forum: 4 reddit posts and one forum.* page)
    h.set_rule(froot, "stage3", "source_kind_min_records", 5)
    setup_room(run, h)
    result = stage3.pains(run)
    info = result["rooms"][ROOM]
    assert info["source_kinds"] == ["forum"] and info["by_kind"]["forum"] == 5
    for p in result["pains"]:
        if p["status"] != "dropped" or p.get("tags"):
            assert "[source kinds: 1]" in p["tags"]
    events = [json.loads(l) for l in (run / "runlog.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert any("Rooms with fewer than 3 kinds of source" in (e.get("note") or "") and e.get("review") for e in events)
