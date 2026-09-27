"""Outputs: redteam, audit-packet, shortlist (with and without survivors), review, runlog, progress, status,
commit-message, compare and audit-status, on a synthetic run built from every stage's file shape."""
import json
import re

import common
import outputs
import stage6
from conftest import REAL_ROOT
from test_stage6 import base_inputs, set_in

R1 = "gre-engineers-india"
R2 = "us-freelancers"
P1 = f"{R1}--quant-plateau"       # kept through Stage 6
P2 = f"{R2}--late-invoices"       # kept through Stage 6
P3 = f"{R1}--visa-docs"           # killed at Stage 4
P4 = f"{R2}--tax-forms"           # cut at Stage 3
P5 = f"{R1}--essay-help"          # dropped at Stage 3
P6 = f"{R2}--client-ghosting"     # killed at Stage 5


def _quote(rid, i):
    return {"record_id": rid, "url": f"https://forum.test/{rid}", "date": None, "text": f"quote {i} with enough words in it"}


def _pain(pid, rank, status, fs, money, rc, quotes, drop_reason=None, tags=("[undated share: 100%]",)):
    room, key = pid.split("--")
    return {"pain_id": pid, "room": room, "pain_key": key, "status": status, "rank": rank, "drop_reason": drop_reason,
            "label": key.replace("-", " "), "description": f"people in {room} struggle with {key.replace('-', ' ')}",
            "urgency": {"type": "deadline_or_rule", "evidence": "the exam date", "record_ids": [], "reasoning": "a date forces action",
                        "confidence": "high"},
            "urgency_type": "deadline_or_rule",
            "who_pays": {"text": "the person themselves", "reasoning": "they already pay tutors", "confidence": "moderate"},
            "alternatives": [{"what": "a private tutor", "price_text": "Rs 2,000/hour", "amount": 2000, "currency": "INR", "unit": "hour",
                              "url": "https://tutors.test/x", "seen_via": "search"}],
            "sellers": [], "spend_evidence": [], "spend_domains": ["tutors.test", "forum.test"], "spend_sources": 2,
            "ladder_position": 1, "record_count": rc, "money_mentions": money, "failed_spend_mentions": fs,
            "seller_records": 1, "media_records": 0, "member_record_ids": [],
            "quotes": quotes, "verified_quote_count": len(quotes),
            "quote_check": {"checked": len(quotes) + 1, "passed": len(quotes), "failed": 1, "citations_corrected": 0, "failed_reasons": {"not_substring": 1}},
            "supporting_records": rc, "undated_records": rc, "undated_share": 100, "sources": {"websearch": rc},
            "tags": list(tags), "notes": []}


def _stage4(pid, status="kept", kill_reason=None):
    return {"pain_id": pid, "room": pid.split("--")[0], "status": status, "kill_reason": kill_reason,
            "outcome": "a higher quant score", "outcome_reached_today": status == "killed",
            "outcome_reasoning": "their AI explains but they do not practise" if status == "kept" else "their AI already gets them there",
            "walls_both": ["W2", "W9", "W14", "W20"], "walls_one": ["W5"],
            "path_walls": {"W2": 1, "W9": 2, "W14": 3, "W20": 3}, "steps": 4,
            "forward_12m": {"W2": "melts", "W9": "melts", "W14": "melts", "W20": "persists"},
            "persisting_walls": ["W20"], "lane_hint": None, "reconciled_ids": [],
            "disagreements": {"comparator": ["walker a saw W5, walker b did not"], "computed": []},
            "walkers": {}, "pairs_drafted": 2, "warnings": []}


def _alt(index, rank, valid=True, lane="business", failed=()):
    return {"index": index, "rank": rank, "entry_walls": ["W2", "W9", "W14"], "hold_wall": "W20", "hold_supply_id": "c1",
            "partner_id": None, "partner_kind": None, "trade": None,
            "one_liner": f"For the room, a promise in two weeks (alternative {index}).", "crux": f"crux {index}",
            "credibility_question": f"Will this room accept the founder as accountability (alternative {index})?",
            "reasoning": "r", "confidence": "moderate",
            "checks": {n: {"pass": n not in failed, "reason": f"{n} {'failed' if n in failed else 'ok'}"} for n in
                       ("entry", "walls_both", "adjacency", "hold", "persistence", "lane")},
            "failed": list(failed), "valid": valid, "lane": lane if valid else None}


def _stage5(pid, status="kept"):
    if status == "kept":
        return {"pain_id": pid, "room": pid.split("--")[0], "status": "kept", "kill_reason": None, "lane": "business", "lane_hint": None,
                "walls_both": ["W2", "W9", "W14", "W20"], "persisting_walls": ["W20"], "kept_index": 1,
                "kept_reason": "lane business (lane order business > partner > trade); the only valid alternative (rank 1)",
                "alternatives": [_alt(1, 1), _alt(2, 2, valid=False, failed=("persistence",))]}
    return {"pain_id": pid, "room": pid.split("--")[0], "status": "killed", "lane": None,
            "kill_reason": "no pair, no clean trade, no plausible partner: alternative 1 (rank 1): hold: W27 is in the cannot list",
            "kept_index": None, "alternatives": [_alt(1, 1, valid=False, failed=("hold",))]}


def build_run(froot, run, h, fail_numbers=False, case=None, red=True):
    """A synthetic run with every stage file. Returns the record ids per room."""
    common.write_json(run / "01_rooms.json", {"status": "ok", "parts": [], "removed": [], "counts": {"in": 2, "kept": 2, "removed": 0}, "rooms": [
        {"slug": R1, "name": "Indian engineers preparing for the GRE", "who": "engineers applying abroad", "lens": "transition",
         "origin": "generated", "ladder": [{"step": 1, "problem": "GRE prep"}, {"step": 2, "problem": "applications"}, {"step": 3, "problem": "visa"}],
         "venture_overlap": ["v1"], "status": "kept"},
        {"slug": R2, "name": "US freelancers chasing invoices", "who": "solo designers and writers", "lens": "profession",
         "origin": "generated", "ladder": [{"step": 1, "problem": "invoicing"}, {"step": 2, "problem": "contracts"}, {"step": 3, "problem": "taxes"}],
         "venture_overlap": [], "status": "kept"}]})
    common.write_json(run / "02_mask.json", {"kept": [R1, R2], "cut": [], "killed": [], "review_notes": [], "rooms": [
        {"slug": R1, "name": "Indian engineers preparing for the GRE", "status": "kept", "rank": 1, "reach_kind": "warm", "reach_ledger_id": "w1",
         "trust_flag": False, "venture_overlap": ["v1"], "employer_overlap": False, "depth_ledger_id": "d1", "depth_strength": "strong",
         "trust_needed_judgment": {"value": True, "reasoning": "tutoring needs trust", "confidence": "moderate"}},
        {"slug": R2, "name": "US freelancers chasing invoices", "status": "kept", "rank": 2, "reach_kind": "search", "reach_ledger_id": "s1",
         "trust_flag": True, "venture_overlap": [], "employer_overlap": True, "depth_ledger_id": "d2", "depth_strength": "strong",
         "trust_needed_judgment": {"value": True, "reasoning": "money advice needs trust", "confidence": "moderate"}}]})
    ids = {}
    for room in (R1, R2):
        recs = [h.make_record(f"https://forum.test/{room}/{i}", f"quote {i} with enough words in it and more", round=1, qi=i) for i in (1, 2)]
        ids[room] = h.store(run, room, recs)["new_ids"]
        rdir = common.room_dir(run, room)
        common.write_jsonl(rdir / "queries.jsonl", [{"round": 1, "query": f"{room} q1", "kind": "forum"}, {"round": 1, "query": f"{room} q2", "kind": "qa"}])
        common.write_json(rdir / "saturation.json", {"room": room, "window": 300, "stop_reason": "exhausted", "final": True, "rounds": [
            {"round": 1, "records": 2, "new_records": 2, "window": 300, "evaluable": False, "new_pains": [], "rank_changes": [], "saturated": False}]})
        common.write_json(rdir / "pains_draft.json", {"pains": []})
        common.write_json(rdir / "taxonomy.json", {"pains": [{"key": "k", "label": "k", "definition": "k", "added_round": 1}]})
    common.write_json(common.room_dir(run, R1) / "sources.json", {
        "used": ["websearch"], "skipped": [{"source": "reddit", "reason": "no API key", "would_add": "first-person posts with dates"}],
        "needs_calls": {"value": True, "reasoning": "many are offline students", "confidence": "moderate"}})
    q1 = [_quote(ids[R1][0], 1), _quote(ids[R1][1], 2), _quote(ids[R1][0], 3)]
    q2 = [_quote(ids[R2][0], 4), _quote(ids[R2][1], 5)]
    pains = [_pain(P1, 1, "kept", 3, 5, 40, q1), _pain(P2, 2, "kept", 1, 2, 20, q2), _pain(P3, 3, "kept", 0, 4, 18, q1[:2]),
             _pain(P6, 4, "kept", 0, 3, 16, q2), _pain(P4, 5, "cut", 0, 1, 15, q2, drop_reason="cut: ranked 5 of 5 survivors and max_pains_total is 4"),
             _pain(P5, None, "dropped", 0, 0, 3, [], drop_reason="fewer than 2 verified quotes: 0 of 1 passed the quote check")]
    common.write_json(run / "03_listen" / "pains.json", {
        "pains": pains, "kept": [P1, P2, P3, P6], "cut": [P4], "dropped": [P5], "needs_calls": [R1],
        "rooms": {R1: {"needs_calls": True, "needs_calls_reasoning": "many are offline students", "saturation": {"verdict": "round 1: 2 records; not saturated"}},
                  R2: {"needs_calls": False, "needs_calls_reasoning": "", "saturation": {"verdict": "round 1: 2 records; not saturated"}}},
        "review_notes": [], "notes": []})
    common.write_json(run / "04_walks" / "_stage4.json", {"kept": [P1, P2, P6], "killed": [P3], "pains": [
        _stage4(P1), _stage4(P2), _stage4(P6), _stage4(P3, "killed", "outcome reached today with their own AI (walker a say so): the AI lists the documents")]})
    common.write_json(run / "05_pairs.json", {"kept": [P1, P2], "killed": [P6], "pains": [_stage5(P1), _stage5(P2), _stage5(P6, "killed")]})
    d1 = base_inputs(pid=P1)
    d2 = base_inputs(pid=P2, currency="USD")
    d2["price"] = {"low": 60, "base": 90, "high": 150, "billing": "one_off", "months": 1, "payment_days_after_sale": 0, "reasoning": "a flat fee"}
    d2["price_anchor"].update({"amount": 400, "currency": "USD", "price_text": "$400 per letter", "what": "a collections lawyer's demand letter"})
    d2["test"] = {"n": 30, "who": "freelancers", "how": "by cold email", "days": 21}
    d2["offer"] = "a demand-letter kit"
    d2["acquisition"]["cash_per_reach"] = {"low": 0, "base": 1, "high": 2, "reasoning": "a few cents of email tooling per reach"}
    set_in(d2, "delivery.cash_cost_per_customer.value", 5)
    set_in(d2, "guarantee.refund_per_customer", 20)
    set_in(d2, "ladder_test.position", 2)
    if fail_numbers:
        set_in(d1, "price.payment_days_after_sale", 45)
        set_in(d2, "price.payment_days_after_sale", 45)
    for d in (d1, d2):
        common.write_json(run / "06_inputs" / f"{d['pain_id']}.json", d)
    # the run log, as the earlier stages would have left it
    ev = [
        (0, "preflight", "blocked", {"domain": "api.stackexchange.com", "detail": "FUNNEL_OFFLINE=1"}),
        (0, "preflight", "ran", {"domains_blocked": ["api.stackexchange.com", "hn.algolia.com"], "domains_reachable": []}),
        (0, "ledger-check", "check", {"ok": True, "texts_checked": 40, "assumed": 11, "errors": 0, "warnings": []}),
        (1, "rooms", "count", {"rooms_in": 90, "rooms_kept": 88, "rooms_removed": 2}),
        (2, "mask", "count", {"rooms_in": 88, "survived": 2, "kept": 2, "cut": 0, "killed": 86}),
        (3, "harvest-search", "source", {"room": R1, "source": "websearch", "records_new": 2}),
        (3, "fetch", "source", {"room": R2, "source": "hackernews", "adapter": "hackernews", "records_new": 2, "requests": 3}),
        (3, "saturation", "count", {"room": R1, "round": 1, "records": 2, "new_records": 2, "saturated": False, "new_pains": [], "rank_changes": 0, "stop_reason": "exhausted"}),
        (3, "fetch", "skip", {"source": "reddit", "domain": "www.reddit.com", "reason": "no key given"}),
        (3, "fetch", "blocked", {"source": "stackexchange", "domain": "api.stackexchange.com", "reason": "FUNNEL_OFFLINE=1"}),
        (3, "pains", "count", {"rooms": 2, "drafted": 6, "kept": 4, "cut": 1, "dropped": 1}),
        (3, "pains", "note", {"note": "Rooms that need calls (public text under-represents their people): gre-engineers-india.", "review": True}),
        (4, "walks", "count", {"pains_in": 4, "walked": 4, "kept": 3, "killed": 1}),
        (5, "pairs", "count", {"pains_in": 3, "kept": 2, "killed": 1}),
        (0, "numbers", "error", {"code": 1, "errors": ["06_inputs/x.json: price.low must be a number"]}),
        (3, "log", "cost", {"text": "2.50 USD for 40 model calls", "amount": 2.5, "tag": "estimate", "review": False}),
        (0, "log", "note", {"text": "build: 157 tests pass", "review": False}),
        (2, "log", "note", {"text": "Chose the low end of the hours range.", "review": True}),
    ]
    for stage, cmd, kind, fields in ev:
        common.log_event(run, stage, cmd, kind, **fields)
    stage6.numbers(run)
    if red:
        common.write_json(run / "07_red_team" / f"{P1}.json", {"pain_id": P1, "points": [
            {"kind": "competitor", "claim": "A tutoring chain sells a two-week quant sprint.", "url": "https://competitor.test/sprint",
             "severity": "medium", "reasoning": "same offer, same room"},
            {"kind": "not_paid_for", "claim": "Free videos cover the same ground.", "url": "https://videos.test/quant", "severity": "low",
             "reasoning": "a free substitute exists"}],
            "verdict": {"new_rank_hint": "down", "reasoning": "a competitor exists", "confidence": "moderate"}})
        common.write_json(run / "07_red_team" / f"{P2}.json", {"pain_id": P2, "points": [],
                                                                "verdict": {"new_rank_hint": "keep", "reasoning": "no evidence found", "confidence": "low"}})
    if case is not None:
        common.write_json(run / "07_audit_packet" / "case_against.json", case)
    return ids


CASE_SWAP = {"survivors": [
    {"pain_id": P1, "points": [{"kind": "competitor", "claim": "A tutoring chain sells a two-week quant sprint.", "url": "https://competitor.test/sprint",
                                "severity": "high", "reasoning": "same offer", "origin": "red_team"}],
     "new_rank": 2, "rank_change_reason": "a competitor already delivers the same pair", "reasoning": "material", "confidence": "moderate"},
    {"pain_id": P2, "points": [], "new_rank": 1, "rank_change_reason": "no material point", "reasoning": "nothing found", "confidence": "low"}]}
CASE_KILL = {"survivors": [
    {"pain_id": P2, "points": [{"kind": "legal_or_platform", "claim": "Demand letters need a licensed lawyer in some states.",
                                "url": "https://law.test/x", "severity": "high", "reasoning": "a licence block"}],
     "new_rank": None, "rank_change_reason": "a licence block in the room's main market", "reasoning": "killed", "confidence": "moderate"}]}


def read(run, name):
    return (run / name).read_text(encoding="utf-8")


def events(run):
    return [json.loads(ln) for ln in read(run, "runlog.jsonl").splitlines() if ln.strip()]


# --------------------------------------------------------------------------- redteam
def test_redteam_validates_every_file_and_writes_a_summary(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("redteam", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Red team: 2 file(s) for 2 survivor(s), 2 point(s) (competitor 1, failed attempt 0, not paid for 1, legal or platform 0); verdicts: keep 1, down 1, kill 0." in r.stdout
    assert f"{P1}: 2 point(s) (high 0, medium 1, low 1); verdict down (moderate): a competitor exists" in r.stdout
    s = json.loads(read(run, "07_red_team/_redteam.json"))
    assert s["survivors"] == [P1, P2] and s["counts"]["points"] == 2
    assert s["pains"][0]["urls"] == ["https://competitor.test/sprint", "https://videos.test/quant"]
    # a file for a non-survivor is ignored with a warning; a missing file exits 2
    common.write_json(run / "07_red_team" / f"{P6}.json", {"pain_id": P6, "points": [], "verdict": {"new_rank_hint": "keep", "reasoning": "x", "confidence": "low"}})
    (run / "07_red_team" / f"{P2}.json").unlink()
    r = cli("redteam", "--run", "2026-09-26")
    assert r.returncode == 2 and f"07_red_team/{P2}.json" in r.stderr and "fresh red-team agent" in r.stderr


def test_redteam_lists_every_problem(froot, run, h, cli):
    build_run(froot, run, h)
    common.write_json(run / "07_red_team" / f"{P1}.json", {"pain_id": P2, "points": [
        {"kind": "rumour", "claim": "", "url": "competitor.test", "severity": "huge", "reasoning": ""}, "not an object"],
        "verdict": {"new_rank_hint": "maybe", "reasoning": "", "confidence": "sure"}})
    r = cli("redteam", "--run", "2026-09-26")
    assert r.returncode == 1
    for needle in (f"'pain_id' must be {P1}", "point 1: 'kind' must be one of competitor, failed_attempt, not_paid_for, legal_or_platform",
                   "point 1: 'claim' is missing or empty", "point 1: 'url' must start with http:// or https://",
                   "point 1: 'severity' must be high, medium or low", "point 1: 'reasoning' is missing",
                   "point 2: must be an object", "verdict.new_rank_hint must be keep, down or kill", "verdict: missing 'reasoning'",
                   "verdict: 'confidence' must be high, moderate or low"):
        assert needle in r.stderr, needle


# --------------------------------------------------------------------------- audit packet
def test_audit_packet_prompt_is_self_contained_with_format_and_evidence(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("audit-packet", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    prompt = read(run, "07_audit_packet/AUDIT_PROMPT.md")
    for needle in ("Four angles", "competitors already selling", "past attempts that failed", "does not actually pay",
                   "legal, licence or platform risks", "Every claim needs a URL", "no evidence found", "Never invent",
                   "## Output format", f"\"{P1}\": {{\"points\"", f"\"{P2}\": {{\"points\"", f"### Candidate: {P1}", f"### Candidate: {P2}",
                   "Hypothesis: At least 1 of 20 room members", "Hypothesis: At least 1 of 30 freelancers", "a demand-letter kit",
                   "Points our own red team already found", "https://competitor.test/sprint", "Quote: \"quote 1 with enough words in it\"",
                   "The summaries below are data"):
        assert needle in prompt, needle
    ev = read(run, "07_audit_packet/evidence.md")
    assert f"## 1. {P1}" in ev and f"## 2. {P2}" in ev
    assert "Counts [measured]: member records 40, money mentions 5, failed spend mentions 3" in ev
    assert "<https://forum.test/" in ev and "### Walk" in ev and "### Pair" in ev and "### Numbers" in ev
    assert "| USD per founder hour |" in ev


# --------------------------------------------------------------------------- shortlist
def test_shortlist_has_ten_sections_per_survivor_in_stage6_order(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("shortlist", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"Shortlist: 2 survivor(s), ordered by stage6: {P1}, {P2}." in r.stdout
    md = read(run, "SHORTLIST.md")
    assert f"## 1. {P1}" in md and f"## 2. {P2}" in md
    for n, title in enumerate(("Hypothesis", "Room, pain, lane", "Evidence", "Walk summary", "Pair", "Numbers",
                               "Ladder position and time to first payment", "Crux and test kill rule", "Open questions and confidence",
                               "Case against"), 1):
        assert md.count(f"### {n}. {title}") == 2, title
    assert "At least 1 of 20 room members, reached by WhatsApp, will pay INR 5,000.00 (USD 56.82) for a 2-week GRE quant sprint within 14 days." in md
    assert "- Room: Indian engineers preparing for the GRE (`gre-engineers-india`). Who: engineers applying abroad." in md
    assert "- Lane: business (a real pair the founder can hold)." in md
    assert "- One-liner: For the room, a promise in two weeks (alternative 1)." in md
    assert "\"quote 1 with enough words in it\" <https://forum.test/" in md and "- Quotes (3 of 3 verified):" in md
    assert "- Tags: [undated share: 100%]" in md and "a private tutor: Rs 2,000/hour (INR 2000 = USD 22.73 per hour) [measured, page not checked]" in md
    assert "- Twelve months: persists W20 Accountability; melts W2, W9, W14." in md
    assert "- Where the walkers disagreed: walker a saw W5, walker b did not" in md
    assert "- Entry walls (how the product gets in): W2 Diagnosis, W9 Effort, W14 Practice." in md
    assert "- Holding wall (why customers keep it): W20 Accountability; the founder can be it (c1: Accountability: coaching and cohorts)." in md
    assert "alternative 2 (rank 2): invalid (persistence: persistence failed)" in md
    assert "| price per customer [estimate] | INR 3,000.00 (USD 34.09) | INR 5,000.00 (USD 56.82) | INR 8,000.00 (USD 90.91) |" in md
    assert "| USD per founder hour | USD 1.19 | USD 18.32 | USD 62.57 |" in md
    assert "- Ladder step 1: opens the ladder" in md and "- Ladder step 2: does not open the ladder" in md
    assert "- First payment expected on day 12: first conversation 3 + close 7 + build 2 days [estimate]." in md
    assert "- Crux: crux 1" in md and "- Kill rule: Kill it if fewer than 1 of the 20 pays INR 5,000.00 (USD 56.82) within 14 days" in md
    assert "- Will users pay before the score jump is proven?" in md and "- Confidence: moderate (the walker). Evidence strength: strong." in md
    assert "- Source: the red team (no judge verdict yet). 2 point(s)." in md
    assert "competitor (medium): A tutoring chain sells a two-week quant sprint. <https://competitor.test/sprint>" in md
    assert "- Red-team hint: down (a competitor exists). No rank change until the judge rules." in md
    assert "| 1 | " + P1 + " | business | 1.19 / 18.32 / 62.57 | day 12 | strong | moderate |" in md


def test_shortlist_applies_case_against_order_and_kills(froot, run, h, cli):
    build_run(froot, run, h, case=CASE_SWAP)
    r = cli("shortlist", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"ordered by case against: {P2}, {P1}." in r.stdout and f"rank change: {P1}: 1 -> 2" in r.stdout
    md = read(run, "SHORTLIST.md")
    assert f"## 1. {P2}" in md and f"## 2. {P1}" in md
    assert "- Source: the judge's case_against.json. 1 point(s)." in md
    assert "competitor (high; red_team): A tutoring chain sells a two-week quant sprint. <https://competitor.test/sprint> same offer" in md
    assert "- Rank change: 1 -> 2 (a competitor already delivers the same pair)." in md
    assert "- Rank change: 2 -> 1 (no material point)." in md
    assert "2 survivor(s) after the case against (0 killed by it)" in md
    # a null new_rank kills the survivor and writes a graveyard line
    common.write_json(run / "07_audit_packet" / "case_against.json", CASE_KILL)
    r = cli("shortlist", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert f"killed by the case against: {P2} (graveyard line added)" in r.stdout
    gy = (froot / "graveyard.md").read_text(encoding="utf-8")
    assert f"- 2026-09-26 | stage 7 | pain:{P2} | killed by the case against (new_rank null): a licence block in the room's main market" in gy
    md = read(run, "SHORTLIST.md")
    assert f"## 1. {P1}" in md and f"## 1. {P2}" not in md and "1 survivor(s) after the case against (1 killed by it)" in md
    cli("shortlist", "--run", "2026-09-26")
    assert (froot / "graveyard.md").read_text(encoding="utf-8").count(f"pain:{P2}") == 1
    assert cli("commit-message", "--run", "2026-09-26").stdout.strip() == "funnel: run 2026-09-26: 2 rooms, 4 pains, 1 survivors"


def test_shortlist_without_survivors_lists_the_five_closest_candidates(froot, run, h, cli):
    build_run(froot, run, h, fail_numbers=True, red=False)
    r = cli("shortlist", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Shortlist: no survivor." in r.stdout
    md = read(run, "SHORTLIST.md")
    assert "## No survivor" in md and "No opportunity survived every stage." in md
    assert "## The five closest candidates" in md
    body = md.split("## The five closest candidates")[1]
    order = re.findall(r"^\d\. (\S+): killed at stage (\d)", body, re.M)
    assert order == [(P1, "6"), (P2, "6"), (P6, "5"), (P3, "4"), (P4, "3")]
    assert f"1. {P1}: killed at stage 6 (numbers). numbers fail in the base case: cash30:" in md
    assert "Evidence: failed spend 3, money 5, member records 40." in md
    assert f"3. {P6}: killed at stage 5 (pairs). no pair, no clean trade, no plausible partner" in md
    assert f"4. {P3}: killed at stage 4 (walks). outcome reached today" in md
    assert f"5. {P4}: killed at stage 3 (pains). cut: ranked 5 of 5" in md
    assert P5 not in body
    assert cli("commit-message", "--run", "2026-09-26").stdout.strip() == "funnel: run 2026-09-26: 2 rooms, 4 pains, 0 survivors"
    r = cli("audit-packet", "--run", "2026-09-26")
    assert r.returncode == 0 and "There is no candidate to audit" in read(run, "07_audit_packet/AUDIT_PROMPT.md")


def test_shortlist_needs_stage6(run, cli):
    r = cli("shortlist", "--run", "2026-09-26")
    assert r.returncode == 2 and "06_survivors.json is missing" in r.stderr


# --------------------------------------------------------------------------- review
def test_review_has_seven_sections_with_assumed_items_defaults_and_gaps(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("review", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    md = read(run, "REVIEW.md")
    for head in ("## 1. Assumed items, defaults and gaps", "## 2. Three quotes to read", "## 3. The credibility question for each survivor",
                 "## 4. Rooms that need calls", "## 5. Skipped and blocked sources", "## 6. Search-reach rooms whose product needs trust",
                 "## 7. Overlaps with existing ventures or the founder's job"):
        assert head in md, head
    # 1: [assumed] lines from the real ledger, transcription notes, kill-rule defaults, logged choices
    assert "Value of one of my hours: ₹1,500. [assumed]" in md
    assert "Full-time investment banking job. Roughly 8–12 hours a week for a new opportunity, shared with my existing ventures. [assumed]" in md
    assert "Human walls the ledger does not mention, treated as not supplied: W21 Advocacy, W23 Private data, W24 Network, W26 Facilitation, W28 Witness." in md
    assert "No runway in the ledger" in md
    assert "constraints.hours_per_week: Capacity checks use the low end, 8 hours (conservative)." in md
    assert "- stage6.opens_ladder_max_position = 1: \"opens the ladder\" = step 1 of the room's ladder" in md
    assert "- stage3.quote_min_words = 5" in md and "- stage1.min_rooms_per_lens = 8: so no lens is token-sized" in md
    assert "- stage 2 (log): Chose the low end of the hours range." in md
    assert "- stage 3 (pains): Rooms that need calls (public text under-represents their people): gre-engineers-india." in md
    assert "build: 157 tests pass" not in md
    # 2: three quotes with links, from kept pains only
    sec2 = md.split("## 2.")[1].split("## 3.")[0]
    assert sec2.count("<https://forum.test/") == 3
    # 3: credibility questions in the final order
    assert f"- 1. {P1}: Will this room accept the founder as accountability (alternative 1)?" in md
    assert f"- 2. {P2}: Will this room accept the founder as accountability (alternative 1)?" in md
    # 4: needs calls
    assert "- gre-engineers-india: many are offline students" in md
    # 5: sources from sources.json, the run log and config/sources.md
    assert "| reddit | skipped | no API key | first-person posts with dates | room gre-engineers-india |" in md
    assert "| stackexchange | blocked | FUNNEL_OFFLINE=1 | see config/sources.md | stage 3 fetch |" in md
    assert "| YouTube Data API v3 | skip |" in md and "| api.stackexchange.com | blocked | FUNNEL_OFFLINE=1 | see config/sources.md | stage 0 preflight |" in md
    # 6 and 7
    assert "- us-freelancers: money advice needs trust" in md and "- gre-engineers-india: tutoring" not in md
    assert "- gre-engineers-india: ventures v1 (GRE business: the GRE product and app)." in md
    assert "- us-freelancers: the founder's job (warm path w2/w4 or exclusion x2)" in md


def test_review_random_quotes_are_stable_across_reruns_and_change_with_the_run_name(froot, run, h, cli):
    build_run(froot, run, h)
    cli("review", "--run", "2026-09-26")
    first = read(run, "REVIEW.md")
    cli("review", "--run", "2026-09-26")
    assert read(run, "REVIEW.md") == first
    pool = []
    for p in json.loads(read(run, "03_listen/pains.json"))["pains"]:
        if p["status"] == "kept":
            pool += [(p["pain_id"], q["record_id"], q["text"], q["url"], None) for q in p["quotes"]]
    pool.sort()
    expected = sorted(common.rng_for_run("2026-09-26").sample(pool, 3))
    sec2 = first.split("## 2.")[1].split("## 3.")[0]
    for pid, _rid, text, url, _d in expected:
        assert f"- \"{text}\" ({pid}; undated) <{url}>" in sec2


# --------------------------------------------------------------------------- runlog
def test_runlog_renders_every_section_from_the_events_and_is_idempotent(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("runlog", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Domains to allow: api.stackexchange.com, hn.algolia.com." in r.stdout
    md = read(run, "RUNLOG.md")
    for head in ("## What ran", "## Counts in and out of every stage", "## Records per room and per source", "## Saturation per room",
                 "## Sources used", "## Sources skipped or blocked, with reasons", "## Domains to allow", "## Errors", "## Approximate cost",
                 "## Build and test results (check events)", "## Notes logged with `funnel log`"):
        assert head in md, head
    assert "| 1 | rooms | in 90; kept 88; removed 2 |" in md
    assert "| 2 | mask | in 88; passed 2; kept 2; cut 0; killed 86 |" in md
    assert "| 3 | pains | rooms 2; drafted 6; kept 4; cut 1; dropped 1 |" in md
    assert "| 6 | numbers | in 2; passed 2; kept 2; cut 0; killed 0 |" in md
    assert "| 7 | shortlist | not run |" in md
    assert "| gre-engineers-india | 2 | websearch 2 |" in md and "| us-freelancers | 2 | hackernews 2 |" in md
    assert "| gre-engineers-india | 1 | 2 | 2 | none | 0 | no | exhausted |" in md
    assert "- hackernews: 2 new record(s) in 1 room(s) (via hackernews)" in md
    assert "- skip: reddit (www.reddit.com): no key given" in md and "- blocked: stackexchange (api.stackexchange.com): FUNNEL_OFFLINE=1" in md
    assert "Set the environment's network access to allow: api.stackexchange.com, hn.algolia.com." in md
    assert "- stage 0 (numbers, exit 1): 06_inputs/x.json: price.low must be a number" in md
    assert "- API requests made by the fetch adapters: 3." in md and "- Model cost logged: 2.50 (sum of the amounts in cost events) [estimate]." in md
    assert "- stage 3 (log): 2.50 USD for 40 model calls [estimate]" in md
    assert "- stage 0 (ledger-check): assumed 11; errors 0; ok True; texts_checked 40; warnings none" in md
    assert "- stage 6 (numbers): blocked_domains none; counts seen_via_search 2; items 2; what price-check" in md
    assert "- stage 0: build: 157 tests pass" in md
    assert "20" + "26-09-26T" not in md   # no timestamp
    cli("status", "--run", "2026-09-26")
    cli("runlog", "--run", "2026-09-26")
    assert read(run, "RUNLOG.md") == md


def test_runlog_needs_events(run, cli):
    r = cli("runlog", "--run", "2026-09-26")
    assert r.returncode == 2 and "runlog.jsonl is missing" in r.stderr


# --------------------------------------------------------------------------- progress and status
def test_progress_regenerates_only_the_auto_block(froot, run, h, cli):
    build_run(froot, run, h)
    p = froot / "PROGRESS.md"
    p.write_text("# Progress\n\nHand-written intro.\n\n<!-- auto:status -->\nold\n<!-- /auto:status -->\n\n## Done\n- something\n\n## Next\n- more\n",
                 encoding="utf-8")
    r = cli("progress", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "PROGRESS.md: auto:status block replaced (updated)." in r.stdout
    text = p.read_text(encoding="utf-8")
    assert text.startswith("# Progress\n\nHand-written intro.\n\n<!-- auto:status -->\n")
    assert text.endswith("<!-- /auto:status -->\n\n## Done\n- something\n\n## Next\n- more\n")
    assert "\nold\n" not in text
    assert "| 6 | numbers (`06_survivors.json`) | done |" in text and "| 7 | shortlist (`SHORTLIST.md`) | missing |" in text
    assert "| 7 | red team files (`07_red_team/*.json`) | done |" in text
    assert "| gre-engineers-india | 1 | 2 | 0 | round 1: 2 records, not saturated, stopped: exhausted | yes | 5 pass / 3 fail (funnel pains) |" in text
    assert "| us-freelancers | 1 | 2 | 0 | round 1: 2 records, not saturated, stopped: exhausted | yes | 6 pass / 3 fail (funnel pains) |" in text
    assert "Rooms kept: 2. Pains kept: 4. Stage 6 kept: 2. Survivors (final): 2." in text
    r = cli("progress", "--run", "2026-09-26")
    assert "(no change)" in r.stdout and p.read_text(encoding="utf-8") == text
    # markers missing: the block is appended, the rest untouched
    p.write_text("# Progress\n\nNo markers here.\n", encoding="utf-8")
    r = cli("progress", "--run", "2026-09-26")
    assert "appended" in r.stdout
    text = p.read_text(encoding="utf-8")
    assert text.startswith("# Progress\n\nNo markers here.\n\n<!-- auto:status -->") and text.endswith("<!-- /auto:status -->\n")


def test_status_prints_stages_counts_rooms_and_next(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("status", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Run runs/2026-09-26:" in r.stdout
    assert re.search(r"stage 6 numbers\s+done", r.stdout) and re.search(r"stage 7 shortlist\s+missing", r.stdout)
    assert f"Rooms kept 2, pains kept 4, Stage 6 kept 2, survivors 2: {P1}, {P2}." in r.stdout
    assert "room us-freelancers: 1 round(s), 2 records, 0 labeled; round 1: 2 records, not saturated, stopped: exhausted; draft yes; quotes 6 pass / 3 fail (funnel pains)" in r.stdout
    assert "Next without an output: preflight." in r.stdout
    r = cli("status", "--run", "2026-09-01")
    assert r.returncode == 2 and "does not exist" in r.stderr


def test_commit_message_counts_rooms_pains_and_survivors(froot, run, h, cli):
    r = cli("commit-message", "--run", "2026-09-26")
    assert r.returncode == 0 and r.stdout.strip() == "funnel: run 2026-09-26: 0 rooms, 0 pains, 0 survivors"
    build_run(froot, run, h)
    assert cli("commit-message", "--run", "2026-09-26").stdout.strip() == "funnel: run 2026-09-26: 2 rooms, 4 pains, 2 survivors"


# --------------------------------------------------------------------------- compare
def test_compare_with_latest_writes_changes_and_the_runlog_section(froot, run, h, cli):
    build_run(froot, run, h)
    r = cli("compare", "--with", "latest", "--run", "2026-09-26")
    assert r.returncode == 2 and "No earlier run to compare" in r.stderr
    old = froot / "runs" / "2026-09-10"
    old.mkdir()
    common.write_json(old / "02_mask.json", {"rooms": [{"slug": R1, "status": "kept"}, {"slug": "old-room", "status": "kept"}]})
    pains = json.loads(read(run, "03_listen/pains.json"))
    for p in pains["pains"]:
        if p["pain_id"] == P2:
            p["rank"] = 1
        elif p["pain_id"] == P1:
            p["rank"] = 2
        elif p["pain_id"] == P6:
            p["status"] = "dropped"
    common.write_json(old / "03_listen" / "pains.json", pains)
    s6 = json.loads(read(run, "06_survivors.json"))
    s6["pains"] = [e for e in s6["pains"] if e["pain_id"] == P1]
    s6["pains"][0]["cases"]["base"]["usd_per_hour"] = 10.0
    common.write_json(old / "06_survivors.json", s6)
    h.store(old, R1, [h.make_record("https://forum.test/old/1", "an old record with enough words")])
    r = cli("compare", "--with", "latest", "--run", "2026-09-26")
    assert r.returncode == 0, r.stderr
    assert "Compared runs/2026-09-26 with runs/2026-09-10: " in r.stdout
    c = json.loads(read(run, "compare.json"))
    assert c["with"] == "2026-09-10" and c["room"] is None
    assert "rooms kept now but not before: us-freelancers" in c["changes"]
    assert "rooms kept before but not now: old-room" in c["changes"]
    assert "records in gre-engineers-india: 1 -> 2 (customer messages 0 -> 0)" in c["changes"]
    assert "records in us-freelancers: 0 -> 2 (customer messages 0 -> 0)" in c["changes"]
    assert f"pains kept now but not before: {P6}" in c["changes"]
    assert f"pain rank {P1}: 2 -> 1" in c["changes"] and f"pain rank {P2}: 1 -> 2" in c["changes"]
    p2_usd = next(e for e in json.loads(read(run, "06_survivors.json"))["pains"] if e["pain_id"] == P2)["cases"]["base"]["usd_per_hour"]
    assert f"new survivor: {P2} (rank 2, USD {p2_usd:,.2f} per hour)" in c["changes"]
    assert f"USD per hour (base) {P1}: 10.00 -> 18.32" in c["changes"]
    md = read(run, "RUNLOG.md")
    assert "## What changed since the last run (compared with 2026-09-10)" in md and f"- pain rank {P1}: 2 -> 1" in md
    r = cli("compare", "--with", "2026-09-10", "--run", "2026-09-26")
    assert r.returncode == 0 and json.loads(read(run, "compare.json")) == c
    r = cli("compare", "--with", "2026-01-01", "--run", "2026-09-26")
    assert r.returncode == 2


def test_compare_in_a_loop_run_uses_the_source_run_and_only_that_room(froot, run, h, cli):
    build_run(froot, run, h)
    loop = froot / "runs" / f"2026-09-26-loop-{R1}"
    loop.mkdir()
    common.write_json(loop / "02_mask.json", {"loop_room": R1, "source_run": "2026-09-26", "rooms": [{"slug": R1, "status": "kept"}]})
    h.store(loop, R1, [h.make_record("https://forum.test/new/1", "a new record with enough words"),
                       h.make_record("https://forum.test/new/2", "a customer message with enough words")], source="inbox:customers")
    common.log_event(loop, 3, "ingest-inbox", "source", room=R1, source="inbox:customers", records_new=2)
    r = cli("compare", "--with", "latest", "--run", f"2026-09-26-loop-{R1}")
    assert r.returncode == 0, r.stderr
    c = json.loads(read(loop, "compare.json"))
    assert c["with"] == "2026-09-26" and c["room"] == R1
    assert "records in gre-engineers-india: 2 -> 2 (customer messages 0 -> 2)" in c["changes"]
    assert not any("us-freelancers" in ch for ch in c["changes"])
    assert f"survivor gone: {P1} (was rank 1)" in c["changes"]
    assert "## What changed since the last run in this room (compared with 2026-09-26)" in read(loop, "RUNLOG.md")


# --------------------------------------------------------------------------- audit status
def test_audit_status_finds_the_latest_run_with_a_shortlist_and_lists_inbox_files(froot, run, h, cli):
    r = cli("audit-status")
    assert r.returncode == 2 and "No run has a SHORTLIST.md yet" in r.stderr
    build_run(froot, run, h, case=CASE_SWAP)
    cli("shortlist", "--run", "2026-09-26")
    r = cli("audit-status")
    assert r.returncode == 0, r.stderr
    assert "Run: runs/2026-09-26 (SHORTLIST.md present; AUDIT_PROMPT.md missing)." in r.stdout
    assert f"Survivors (2): 1. {P2}, 2. {P1}." in r.stdout
    assert "case_against.json: present, 1 point(s)." in r.stdout
    assert "Audit results in inbox/audit_results/: none." in r.stdout
    (froot / "inbox" / "audit_results" / "gemini.md").write_text("claims", encoding="utf-8")
    (froot / "inbox" / "audit_results" / ".keep").write_text("", encoding="utf-8")
    r = cli("audit-status", "--run", "2026-09-26")
    assert "Audit results in inbox/audit_results/ (1): gemini.md." in r.stdout


# --------------------------------------------------------------------------- docs and determinism
def test_every_documented_output_command_and_flag_exists(cli):
    parser_help = cli("--help").stdout
    mine = {"redteam", "audit-packet", "shortlist", "review", "runlog", "progress", "status", "commit-message", "compare", "audit-status",
            "numbers"}
    for cmd in mine:
        assert re.search(rf"^\s+{re.escape(cmd)}\b", parser_help, re.M), cmd
    docs = ""
    for p in list((REAL_ROOT / ".claude").rglob("*.md")) + [REAL_ROOT / "pipeline" / "README.md"]:
        docs += p.read_text(encoding="utf-8")
    seen = set()
    for m in re.finditer(r"funnel (%s)((?: --[a-z-]+)*)" % "|".join(sorted(mine, key=len, reverse=True)), docs):
        cmd, flags = m.group(1), m.group(2).split()
        seen.add(cmd)
        help_text = cli(cmd, "--help").stdout
        for flag in flags:
            assert flag in help_text, f"{cmd} {flag}"
    assert {"compare", "commit-message", "audit-status", "numbers"} <= seen


def test_all_outputs_are_byte_identical_on_a_second_run(froot, run, h, cli):
    build_run(froot, run, h, case=CASE_SWAP)
    names = ("SHORTLIST.md", "REVIEW.md", "RUNLOG.md", "07_audit_packet/AUDIT_PROMPT.md", "07_audit_packet/evidence.md", "07_red_team/_redteam.json")
    for cmd in ("redteam", "audit-packet", "shortlist", "review", "runlog", "progress"):
        assert cli(cmd, "--run", "2026-09-26").returncode == 0, cmd
    first = {n: (run / n).read_bytes() for n in names}
    progress1 = (froot / "PROGRESS.md").read_bytes()
    for cmd in ("redteam", "audit-packet", "shortlist", "review", "runlog", "progress"):
        assert cli(cmd, "--run", "2026-09-26").returncode == 0, cmd
    assert {n: (run / n).read_bytes() for n in names} == first
    assert (froot / "PROGRESS.md").read_bytes() == progress1
    for n in names:
        assert first[n].endswith(b"\n")
    evs = events(run)
    assert any(e["kind"] == "count" and e["command"] == "shortlist" and e["order"] == [P2, P1] for e in evs)
    assert any(e["kind"] == "ran" and e["command"] == "audit-packet" for e in evs)
