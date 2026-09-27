"""End to end: one synthetic run through the CLI in subprocesses, then the same run again on the same folder.

Every command runs as `python3 pipeline/funnel.py <command> --run 2026-09-26` against a temporary funnel root
that holds a copy of the real config (FUNNEL_ROOT_OVERRIDE), offline (FUNNEL_OFFLINE=1), with synthetic session
transcripts in both forms the harvester reads (FUNNEL_TRANSCRIPTS_DIR). The files the model would write (room
parts, mask parts, queries, taxonomy, labels, pains drafts, walker and comparator files, Stage 6 inputs, red-team
files, the case against) are written by the test; every S file comes from the scripts.

Pass 1 asserts the contents: quote-check statuses, graveyard lines, lanes, survivor order, SHORTLIST section order
and the case against, REVIEW sections with the [assumed] items, and no raw email or phone number anywhere under
the funnel root. Pass 2 repeats every step on the same folder: every file except runlog.jsonl, RUNLOG.md and
PROGRESS.md is byte-identical, and graveyard.md holds no duplicate line.
"""
import copy
import csv
import json
import re

import common
import records
from anonymize import anonymize
from conftest import Helpers, RUN_NAME
from test_stage1 import make_room, write_part
from test_stage2 import entry, spend
from test_stage45 import merge, pair, trade, walk
from test_stage6 import base_inputs, set_in

R1 = "gre-engineers-india"          # warm reach w1, depth d1 (strong), touches venture v1
R2 = "us-freelancers"               # search reach s1, depth d2, product needs trust
DEAD_LADDER = "mba-applicants"      # killed by the mask: 2 ladder steps
DEAD_SUPPLY = "warehouse-developers"  # killed by the mask: supply blocked (large capital)
P1 = f"{R1}--quant-plateau"         # business lane, Stage 6 survivor
P2 = f"{R2}--late-invoices"         # partner lane, Stage 6 survivor
P3 = f"{R1}--coaching-fees"         # every wall melts -> trade -> killed by the numbers (cash30)
P4 = f"{R2}--tax-forms"             # killed at Stage 4: outcome reached today (walker b)
P5 = f"{R2}--client-ghosting"       # killed at Stage 5: no valid alternative
DROP_FLAT = f"{R1}--study-buddy"    # dropped at Stage 3: no money, no failed spend, urgency none
DROP_QUOTES = f"{R1}--lonely-forums"  # dropped at Stage 3: one verified quote

EMAIL = "gre.help@example.com"
PHONE = "+91 98765 43210"
SUMMARY = "SUMMARY-NEVER-STORED: the search tool's own reading of these results, which must never become a record."

# handle -> (web-search title, url). Titles are the record texts.
LINKS = {
    "r1": ("I paid 45k for a premium GRE course and my quant score did not move at all", "https://www.reddit.com/r/GRE/comments/1a/"),
    "r2": ("Stuck at 160 quant after three months of practice, what am I doing wrong", "https://www.reddit.com/r/GRE/comments/1b/"),
    "r3": ("Why my GRE quant score is stuck at 160 and the fix that worked", "https://blog.test/2025/06/01/gre-quant-stuck"),
    "r4": ("Coaching fees for GRE in India are insane, 60k for classes that do not help", "https://www.reddit.com/r/GRE/comments/2a/"),
    "r5": ("Is the 30k GRE class fee worth it or should I self study", "https://forum.test/t/5"),
    "r6": (f"Call {PHONE} or mail {EMAIL} for GRE quant coaching in Pune", "https://ads.test/gre-coaching"),
    "r7": ("GRE Prep Course pricing plans compared for 2026", "https://prices.test/course"),
    "old": ("GRE quant tips from a 2023 test taker that still apply today", "https://old.test/2023/01/05/gre-quant"),
    "r8": ("Deadline for fall 2026 applications is coming and my score is not ready", "https://www.reddit.com/r/GRE/comments/3a/"),
    "r9": ("Some GRE test takers just want a study buddy for the mornings", "https://blog.test/flat"),
    "r10": ("A study buddy for the GRE would be nice but nobody is paying for that", "https://www.reddit.com/r/GRE/comments/4a/"),
    "r11": ("Nobody ever talks about this GRE issue in the forums", "https://blog.test/no-evidence"),
    "s1": ("Client has not paid my invoice for 90 days and ignores every email", "https://www.reddit.com/r/freelance/comments/5a/"),
    "s2": ("I paid a collections agency 200 dollars and they recovered nothing", "https://www.reddit.com/r/freelance/comments/5b/"),
    "s3": ("Late invoice? Send a demand letter template that actually works", "https://blog.test/2025/03/10/demand-letter"),
    "s4": ("How to handle a client who ghosts after the first draft", "https://www.reddit.com/r/freelance/comments/5c/"),
    "s5": ("Freelance tax forms explained: 1099 and quarterly payments", "https://taxes.test/2025/01/15/freelance-taxes"),
    "s6": ("Client ghosted me after I delivered the logo and I am out 500 dollars", "https://www.reddit.com/r/freelance/comments/6a/"),
    "s7": ("Collections agency for freelancers pricing per case", "https://collect.test/pricing"),
    "s8": ("Which tax software do freelancers use for quarterly estimates", "https://www.reddit.com/r/freelance/comments/6b/"),
    "junk-domain": ("reddit.com", "https://www.reddit.com/"),
    "junk-empty": ("", "https://empty.test/"),
    "junk-short": ("GRE prep", "https://two.test/words"),
}

# room -> round -> [(query, kind, transcript form, link handles in rank order)]
SEARCHES = {
    R1: {1: [("GRE quant stuck at 160 reddit", "forum", "structured", ["r1", "r2", "junk-domain", "r3"]),
             ("GRE coaching fees waste of money", "qa", "text", ["r4", "r5", "r6", "r7", "r4", "old", "junk-empty", "junk-short"])],
         2: [("GRE application deadline score not ready", "forum", "structured", ["r8", "r9", "r10", "r11"])]},
    R2: {1: [("freelancer client not paying invoice", "forum", "text", ["s1", "s2", "s3", "s4", "s5"])],
         2: [("freelance client ghosting after delivery", "forum", "structured", ["s6", "s7", "s8"])]},
}
ROUND_OF = {h: rnd for room in SEARCHES for rnd, qs in SEARCHES[room].items() for q in qs for h in q[3]}

TAXONOMY = {R1: ["quant-plateau", "coaching-fees", "study-buddy", "lonely-forums"],
            R2: ["late-invoices", "client-ghosting", "tax-forms"]}
LABELS = {
    R1: {"r1": dict(keys=["quant-plateau"], money=True, failed=True), "r2": dict(keys=["quant-plateau"]),
         "r3": dict(keys=["quant-plateau"], money=True), "r4": dict(keys=["coaching-fees"], money=True, failed=True),
         "r5": dict(keys=["coaching-fees"], money=True), "r6": dict(voice="seller", keys=["coaching-fees"]),
         "r7": dict(voice="seller", keys=["quant-plateau"], money=True), "r8": dict(keys=["quant-plateau"]),
         "r9": dict(keys=["study-buddy"]), "r10": dict(keys=["study-buddy"]), "r11": dict(keys=["lonely-forums"])},
    R2: {"s1": dict(keys=["late-invoices"], money=True), "s2": dict(keys=["late-invoices"], money=True, failed=True),
         "s3": dict(voice="media", keys=["late-invoices"]), "s4": dict(keys=["client-ghosting"]),
         "s5": dict(voice="media", keys=["tax-forms"], money=True), "s6": dict(keys=["client-ghosting"], money=True, failed=True),
         "s7": dict(voice="seller", keys=["late-invoices"], money=True), "s8": dict(keys=["tax-forms"], money=True)},
}
SOURCES = {
    R1: {"used": ["websearch"], "skipped": [{"source": "reddit", "reason": "no API key", "would_add": "first-person posts with dates"}],
         "needs_calls": {"value": True, "reasoning": "older test takers rarely post", "confidence": "moderate"}},
    R2: {"used": ["websearch"], "skipped": [], "needs_calls": {"value": False, "reasoning": "freelancers post a lot", "confidence": "moderate"}},
}
OUTCOME = {P1: "a 165+ quant score", P2: "the invoice paid", P3: "a fair coaching fee", P4: "the tax forms filed", P5: "the client answers"}
MELT3 = {"W2": "melts", "W4": "melts", "W9": "melts"}
WALKS = {
    P1: dict(a=([["W2"], ["W4"], ["W9"], ["W20"]], dict(MELT3, W20="persists")),
            b=([["W2", "W5"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W5": "melts", "W4": "melts", "W9": "unsure", "W20": "persists"}),
            pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], "W20", kind="a study coach")]),
    P2: dict(a=([["W2"], ["W9"], ["W12"], ["W18"]], {"W2": "melts", "W9": "melts", "W12": "melts", "W18": "persists"}),
            b=([["W2"], ["W9"], ["W12"], ["W18"]], {"W2": "melts", "W9": "melts", "W12": "melts", "W18": "persists"}),
            pairs=[pair(1, ["W2", "W9", "W12"], "W18", partner="r1"), pair(2, ["W2", "W9", "W12"], "W18", supply="c1")]),
    P3: dict(a=([["W2"], ["W4"], ["W9"]], dict(MELT3)), b=([["W2"], ["W4"], ["W9"]], dict(MELT3)),
            pairs=[pair(1, ["W2", "W4", "W9"], trade=trade()), pair(2, ["W2", "W4", "W9"], "W20", supply="c1")]),
    P4: dict(a=([["W2"], ["W9"]], {"W2": "melts", "W9": "melts"}), b=([["W2"], ["W9"]], {"W2": "melts", "W9": "melts"}),
            b_reached=True, pairs=[]),
    P5: dict(a=([["W2"], ["W9"], ["W27"]], {"W2": "melts", "W9": "melts", "W27": "persists"}),
            b=([["W2"], ["W9"], ["W27"]], {"W2": "melts", "W9": "melts", "W27": "persists"}),
            pairs=[pair(1, ["W2", "W9"], "W27", kind="a priest"), pair(2, ["W2", "W9", "W27"], "W27", kind="a priest")]),
}
FX = {"base": "USD", "as_of": RUN_NAME, "rates": {"INR": {"per_usd": 88.0, "url": "https://fx.test/inr", "seen_via": "search",
                                                          "reasoning": "the rate shown in a search result", "confidence": "moderate"}}}
RED_TEAM = {
    P1: {"pain_id": P1, "points": [
        {"kind": "competitor", "claim": "A tutoring chain sells a two-week quant sprint.", "url": "https://competitor.test/sprint",
         "severity": "medium", "reasoning": "same offer, same room"},
        {"kind": "not_paid_for", "claim": "Free videos cover the same ground.", "url": "https://videos.test/quant", "severity": "low",
         "reasoning": "a free substitute exists"}],
         "verdict": {"new_rank_hint": "down", "reasoning": "a competitor exists", "confidence": "moderate"}},
    P2: {"pain_id": P2, "points": [], "verdict": {"new_rank_hint": "keep", "reasoning": "no evidence found", "confidence": "low"}},
}
CASE_AGAINST = {"survivors": [
    {"pain_id": P1, "points": [{"kind": "competitor", "claim": "A tutoring chain sells a two-week quant sprint.",
                                "url": "https://competitor.test/sprint", "severity": "high", "reasoning": "same offer", "origin": "red_team"}],
     "new_rank": 2, "rank_change_reason": "a competitor already delivers the same pair", "reasoning": "material", "confidence": "moderate"},
    {"pain_id": P2, "points": [], "new_rank": 1, "rank_change_reason": "no material point", "reasoning": "nothing found", "confidence": "low"}]}


# --------------------------------------------------------------------------- builders
def text_of(handle: str) -> str:
    """The record text as stored: the title, whitespace-normalized and anonymized."""
    return anonymize(common.normalize_ws(LINKS[handle][0]))


def rid(handle: str) -> str:
    return common.record_id(LINKS[handle][1], text_of(handle))


def write_transcripts(tdir) -> None:
    """Both forms: the structured toolUseResult line and the tool_result text line (with a summary to ignore)."""
    main, sub = [], []
    for room, rounds in SEARCHES.items():
        for rnd, queries in rounds.items():
            for query, _kind, form, handles in queries:
                links = [{"title": LINKS[h][0], "url": LINKS[h][1]} for h in handles]
                if form == "structured":
                    main.append({"type": "user", "message": {"role": "user", "content": []},
                                 "toolUseResult": {"query": query, "results": [{"content": links}]}})
                else:
                    text = f'Web search results for query: "{query}"\n\nLinks: {json.dumps(links)}\n\n{SUMMARY}'
                    sub.append({"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": text}]}})
    common.write_jsonl(tdir / "main.jsonl", main)
    common.write_jsonl(tdir / "subagents" / "agent-1.jsonl", sub)


def quote(handle, text=None, url=None, record_id=None):
    return {"record_id": record_id or rid(handle), "url": url or LINKS[handle][1], "date": None,
            "text": text_of(handle) if text is None else text}


def price(what, price_text, amount, currency, unit, url):
    return {"what": what, "price_text": price_text, "amount": amount, "currency": currency, "unit": unit, "url": url, "seen_via": "search"}


def pain(key, quotes, utype="none", evidence="", uids=(), spend=(), ladder=1, alternatives=()):
    return {"pain_key": key, "description": f"{key.replace('-', ' ')}, in their words",
            "urgency": {"type": utype, "evidence": evidence, "record_ids": list(uids), "reasoning": "from the records", "confidence": "moderate"},
            "who_pays": {"text": "the person themselves", "reasoning": "they already pay for fixes", "confidence": "moderate"},
            "alternatives": list(alternatives), "sellers": [], "spend_evidence": list(spend), "ladder_position": ladder, "quotes": quotes}


def drafts(room) -> list:
    if room == R1:
        return [
            pain("quant-plateau",
                 [quote("r1"),
                  quote("r2", text="Stuck at 160 quant after three months", url="https://wrong.test/x"),   # substring; citation corrected
                  quote("r3", text="GRE quant score is stuck at 165 and the fix that worked"),           # altered: not_substring
                  quote("r3", text="GRE quant score"),                                                   # too_short
                  quote("r1", record_id="deadbeefdeadbeef")],                                            # record_missing
                 utype="deadline_or_rule", evidence="applications close in the fall", uids=[rid("r8")],
                 spend=[{"kind": "record", "record_id": rid("r1")}, {"kind": "price", "url": "https://prices.test/course"}],
                 alternatives=[price("a private GRE tutor", "Rs 2,000/hour", 2000, "INR", "hour", "https://tutors.test/x")]),
            pain("coaching-fees", [quote("r4"), quote("r5")], spend=[{"kind": "record", "record_id": rid("r4")}], ladder=2),
            pain("study-buddy", [quote("r9"), quote("r10")]),
            pain("lonely-forums", [quote("r11"), quote("r11", text="Nobody ever talks about this issue")]),
        ]
    return [
        pain("late-invoices", [quote("s1"), quote("s2"), quote("s3")], utype="acute_pain", evidence="unpaid for 90 days", uids=[rid("s1")],
             spend=[{"kind": "record", "record_id": rid("s2")}, {"kind": "price", "url": "https://collect.test/pricing"}], ladder=2,
             alternatives=[price("a collections agency", "$49 per case", 49, "USD", "case", "https://collect.test/pricing")]),
        pain("client-ghosting", [quote("s4"), quote("s6")], utype="fear", evidence="they dread losing the fee", uids=[rid("s6")],
             spend=[{"kind": "record", "record_id": rid("s6")}]),
        pain("tax-forms", [quote("s8"), quote("s5")], utype="deadline_or_rule", evidence="quarterly filing dates", uids=[rid("s8")]),
    ]


def walk_files(pid):
    spec = WALKS[pid]
    ids = [rid("r1"), rid("r2")] if pid.startswith(R1) else [rid("s1")]
    a = walk(pid, "a", spec["a"][0], spec["a"][1], reached=spec.get("a_reached", False), persona_ids=ids)
    b = walk(pid, "b", spec["b"][0], spec["b"][1], reached=spec.get("b_reached", False), persona_ids=ids)
    a["outcome"] = b["outcome"] = OUTCOME[pid]
    m = merge(a, b, pairs=spec["pairs"], persona_ids=ids)
    m["outcome"] = OUTCOME[pid]
    return a, b, m


def stage6_inputs() -> list:
    d1 = base_inputs(pid=P1)
    d2 = base_inputs(pid=P2, currency="USD")
    d2["price"] = {"low": 60, "base": 90, "high": 150, "billing": "one_off", "months": 1, "payment_days_after_sale": 0, "reasoning": "a flat fee"}
    d2["price_anchor"].update({"amount": 400, "currency": "USD", "price_text": "$400 per letter", "what": "a collections lawyer's demand letter"})
    d2["test"] = {"n": 30, "who": "freelancers", "how": "by cold email", "days": 21}
    d2["offer"] = "a demand-letter kit"
    d2["price_anchor"]["url"] = "https://law.test/demand-letter"
    d2["channel"] = {"name": "cold email to freelancers", "where": "a public list of freelance designers", "reach_kind": "search",
                     "trust": "low", "reasoning": "search reach, no prior relationship", "confidence": "low"}
    d2["acquisition"]["cash_per_reach"] = {"low": 0, "base": 1, "high": 2, "reasoning": "a few cents of email tooling per reach"}
    set_in(d2, "delivery.cash_cost_per_customer.value", 5)
    set_in(d2, "guarantee.refund_per_customer", 20)
    set_in(d2, "ladder_test.position", 2)
    d3 = base_inputs(pid=P3)
    d3["offer"] = "a coaching fee comparison sheet"
    set_in(d3, "price.payment_days_after_sale", 45)   # nothing paid within 30 days -> cash30 fails
    return [d1, d2, d3]


# --------------------------------------------------------------------------- the run, as the skills drive it
class Flow:
    def __init__(self, froot, cli):
        self.root = froot
        self.cli = cli
        self.run = froot / "runs" / RUN_NAME
        self.out = {}

    def ok(self, *args):
        r = self.cli(*args, "--run", RUN_NAME)
        assert r.returncode == 0, f"funnel {' '.join(map(str, args))} exited {r.returncode}\n--- stdout\n{r.stdout}\n--- stderr\n{r.stderr}"
        return r

    def fails(self, code, *args):
        r = self.cli(*args, "--run", RUN_NAME)
        assert r.returncode == code, f"funnel {' '.join(map(str, args))} exited {r.returncode}, expected {code}\n{r.stdout}\n{r.stderr}"
        return r

    def queries(self, room, upto):
        rows = [{"round": rnd, "query": q, "kind": kind} for rnd in range(1, upto + 1) for q, kind, _f, _h in SEARCHES[room][rnd]]
        common.write_jsonl(common.room_dir(self.run, room) / "queries.jsonl", rows)

    def labels(self, room, rnd):
        rows = [Helpers.label(rid(h), **kw) for h, kw in LABELS[room].items() if ROUND_OF[h] == rnd]
        Helpers.write_labels(self.run, room, f"batch_r{rnd}_001", rows)

    def listen(self, room):
        rd = common.room_dir(self.run, room)
        self.queries(room, 1)
        self.out[f"harvest1:{room}"] = self.ok("harvest-search", "--room", room)
        self.ok("batches", "--room", room)
        Helpers.write_taxonomy(self.run, room, TAXONOMY[room])
        self.labels(room, 1)
        self.ok("count", "--room", room)
        self.ok("saturation", "--room", room)
        self.queries(room, 2)
        self.out[f"harvest2:{room}"] = self.ok("harvest-search", "--room", room)
        self.out[f"batches:{room}"] = self.ok("batches", "--room", room)
        self.labels(room, 2)
        self.ok("count", "--room", room)
        r = self.fails(1, "saturation", "--room", room, "--final", "--stop-reason", "saturated")
        assert "needs the last round to be saturated" in r.stderr
        self.ok("saturation", "--room", room, "--final", "--stop-reason", "exhausted")
        self.ok("listen-status", "--room", room)
        common.write_json(rd / "pains_draft.json", {"pains": drafts(room)})
        common.write_json(rd / "sources.json", SOURCES[room])
        self.out[f"quote-check:{room}"] = self.cli("quote-check", "--room", room, "--run", RUN_NAME)

    def run_pass(self):
        run = self.run
        # 0. preflight
        self.ok("init")
        self.out["preflight"] = self.ok("preflight")
        self.ok("ledger-check")
        self.ok("graveyard")
        # Stage 1: parts (a lens part, a second lens part and a gap part), merged in dry-run mode
        write_part(run, "transition.json", [make_room(R1, "transition", name="Indian engineers preparing for the GRE", ventures=("v1",)),
                                            make_room(DEAD_LADDER, "transition", name="MBA applicants in India", ladder_steps=2)])
        write_part(run, "profession.json", [make_room(R2, "profession", name="US freelancers chasing late invoices")])
        write_part(run, "gap_profession.json", [make_room(DEAD_SUPPLY, "profession", origin="gap_pass", name="Warehouse developers in India")])
        self.out["rooms"] = self.ok("rooms", "--merge-parts", "--dry-run")
        # Stage 2: fx and the mask
        common.write_json(run / "fx_rates.json", FX)
        self.ok("fx")
        common.write_json(run / "02_mask.parts" / "1.json", {"rooms": [
            entry(R1, kind="warm", lid="w1", depth="d1",
                  spend_items=[spend(url="https://prices.test/course", price_text="₹30,000", currency="INR", amount=30000)]),
            entry(R2, kind="search", lid="s1", url="https://apps.test/invoice-chaser", depth="d2", trust=True,
                  spend_items=[spend(url="https://collect.test/pricing", price_text="$49 per case", amount=49)]),
            entry(DEAD_LADDER, kind="warm", lid="w1", depth="d6"),
            entry(DEAD_SUPPLY, kind="warm", lid="w3", depth="d3", blocked=True, needs=("large_capital",)),
        ]})
        self.out["mask"] = self.ok("mask", "--merge-parts")
        self.ok("log", "--stage", "2", "--note", "Chose the low end of the hours range.", "--review")
        self.ok("price-check", "--stage", "2")
        self.ok("rooms-known")
        # Stage 3: two rooms, two rounds each, then the pains
        for room in (R1, R2):
            self.listen(room)
        self.ok("show", "--room", R1, "--ids", f"{rid('r1')},{rid('r6')}")
        self.ok("excerpt", "--room", R1, "--id", rid("r1"), "--start", "I paid", "--end", "at all")
        self.out["pains"] = self.ok("pains")
        self.ok("price-check", "--stage", "3")
        self.ok("show", "--pain", P1)
        # Stage 4: walker files, the check, a rejected merge, the corrected merge
        files = {pid: walk_files(pid) for pid in (P1, P2, P3, P4, P5)}
        for pid, (a, b, _m) in files.items():
            paths = common.run_dir(run) / "04_walks"
            common.write_json(paths / f"{pid}.a.json", a)
            common.write_json(paths / f"{pid}.b.json", b)
        self.ok("walks", "--check", P1)
        for pid, (_a, _b, m) in files.items():
            common.write_json(run / "04_walks" / f"{pid}.json", m)
        bad = copy.deepcopy(files[P1][2])
        for e in bad["forward_12m"]:
            if e["wall"] == "W9":
                e["status"] = "persists"      # walker a says melts, walker b says unsure: less conservative
        common.write_json(run / "04_walks" / f"{P1}.json", bad)
        r = self.fails(1, "walks")
        assert f"04_walks/{P1}.json: forward_12m: W9 is marked persists" in r.stderr and "walker b says unsure" in r.stderr
        common.write_json(run / "04_walks" / f"{P1}.json", files[P1][2])
        self.out["walks"] = self.ok("walks")
        # Stage 5
        self.out["pairs"] = self.ok("pairs")
        # Stage 6
        for d in stage6_inputs():
            common.write_json(run / "06_inputs" / f"{d['pain_id']}.json", d)
        self.out["numbers-check"] = self.ok("numbers", "--check", P3)
        self.ok("price-check", "--stage", "6")
        self.out["numbers"] = self.ok("numbers")
        # red team, the judge's case against, outputs
        for pid, data in RED_TEAM.items():
            common.write_json(run / "07_red_team" / f"{pid}.json", data)
        self.out["redteam"] = self.ok("redteam")
        common.write_json(run / "07_audit_packet" / "case_against.json", CASE_AGAINST)
        self.ok("audit-packet")
        self.out["shortlist"] = self.ok("shortlist")
        self.ok("review")
        self.ok("runlog")
        first_runlog = (run / "RUNLOG.md").read_bytes()
        self.ok("runlog")
        assert (run / "RUNLOG.md").read_bytes() == first_runlog, "RUNLOG.md changed on an immediate rebuild"
        self.ok("progress")
        self.out["status"] = self.ok("status")
        self.out["commit-message"] = self.ok("commit-message")
        self.ok("audit-status")


# --------------------------------------------------------------------------- helpers for the assertions
def read_json(p):
    return json.loads(p.read_text(encoding="utf-8"))


def snapshot(flow) -> dict:
    """Every file under the run folder (except the run log) plus graveyard.md, by relative path."""
    out = {}
    for p in sorted(flow.run.rglob("*")):
        if p.is_file():
            rel = p.relative_to(flow.run).as_posix()
            if rel not in ("runlog.jsonl", "RUNLOG.md"):
                out[rel] = p.read_bytes()
    out["../../graveyard.md"] = (flow.root / "graveyard.md").read_bytes()
    return out


def section(text: str, heading: str, level: str = "## ") -> str:
    """The text of one markdown section, from its heading (at a line start) to the next heading of the same level."""
    m = re.search(r"^" + re.escape(heading), text, re.M)
    assert m, f"no section {heading!r}"
    nxt = text.find("\n" + level, m.end())
    return text[m.start():] if nxt < 0 else text[m.start():nxt]


def check_pass_one(flow: Flow, first_pass: bool = True) -> None:
    run, root, out = flow.run, flow.root, flow.out
    # preflight: offline, every listed domain is blocked and named
    pre = read_json(run / "preflight.json")
    assert pre["ledger_ok"] is True and pre["domains_to_allow"] and "api.stackexchange.com" in pre["domains_to_allow"]
    assert all(p["status"] == "blocked_by_network" for p in pre["domains"])
    assert (run / "config_snapshot" / "ledger.yaml").exists()
    # Stage 1: dry run keeps the four rooms and warns instead of failing
    rooms = read_json(run / "01_rooms.json")
    assert [r["slug"] for r in rooms["rooms"]] == [R2, DEAD_SUPPLY, R1, DEAD_LADDER], "lens order, then origin order"
    assert rooms["status"] == "counts_out_of_range" and "warning (dry run)" in out["rooms"].stdout
    assert {r["slug"]: r["origin"] for r in rooms["rooms"]}[DEAD_SUPPLY] == "gap_pass"
    # Stage 2: two kept, two killed with the failed test in the graveyard
    mask = read_json(run / "02_mask.json")
    assert mask["kept"] == [R1, R2] and mask["killed"] == [DEAD_LADDER, DEAD_SUPPLY]
    by_slug = {v["slug"]: v for v in mask["rooms"]}
    assert by_slug[DEAD_LADDER]["failed_tests"] == ["ladder"] and by_slug[DEAD_SUPPLY]["failed_tests"] == ["supply"]
    assert by_slug[R2]["trust_flag"] is True and by_slug[R1]["venture_overlap"] == ["v1"]
    assert all(it["price_status"] == "seen_via_search" for v in mask["rooms"] for it in v["spend"])
    # Stage 3: harvest counts (first pass: new records; second pass: every URL is already stored)
    if first_pass:
        assert "Links seen: 12. Records new: 8. Duplicates: 1. Skipped junk titles: 3." in out[f"harvest1:{R1}"].stdout
        assert "Records new: 4." in out[f"harvest2:{R1}"].stdout
        assert "Records new: 5." in out[f"harvest1:{R2}"].stdout and "Records new: 3." in out[f"harvest2:{R2}"].stdout
    else:
        for key in (f"harvest1:{R1}", f"harvest2:{R1}", f"harvest1:{R2}", f"harvest2:{R2}"):
            assert "Records new: 0." in out[key].stdout, key
    assert "2 matched a search result in 2 transcript file(s)" in out[f"harvest1:{R1}"].stdout, "both transcript forms were read"
    # both transcript forms, lookback, dedupe, junk titles, anonymized text
    stored = {room: records.records_by_id(run, room) for room in (R1, R2)}
    assert len(stored[R1]) == 12 and len(stored[R2]) == 8
    assert stored[R1][rid("r6")]["text"] == "Call [phone] or mail [email] for GRE quant coaching in Pune"
    assert stored[R1][rid("r3")]["date"] == "2025-06-01" and stored[R2][rid("s5")]["date"] == "2025-01-15"
    assert stored[R1][rid("old")]["date"] == "2023-01-05"
    manifest = read_json(common.room_dir(run, R1) / "batches.json")
    assert manifest["filters"]["dropped_old"] == 1 and manifest["filters"]["kept"] == 11
    assert sorted(manifest["batches"]) == ["batch_r1_001", "batch_r2_001"] and len(manifest["batches"]["batch_r2_001"]) == 4
    sat = read_json(common.room_dir(run, R1) / "saturation.json")
    assert [e["round"] for e in sat["rounds"]] == [1, 2] and sat["stop_reason"] == "exhausted" and sat["final"] is True
    assert sat["rounds"][1]["evaluable"] is False and sat["rounds"][1]["records"] == 11
    counts1 = read_json(common.room_dir(run, R1) / "counts.json")["pains"]
    assert (counts1["quant-plateau"]["record_count"], counts1["quant-plateau"]["money_mentions"], counts1["quant-plateau"]["failed_spend_mentions"]) == (4, 2, 1)
    assert counts1["quant-plateau"]["seller_records"] == 1 and counts1["coaching-fees"]["seller_records"] == 1
    # the quote self-check: exit 1 for the room with failing quotes, 0 for the clean one
    qc1, qc2 = out[f"quote-check:{R1}"], out[f"quote-check:{R2}"]
    assert qc1.returncode == 1 and qc2.returncode == 0
    assert "FAIL not_substring" in qc1.stdout and "FAIL too_short" in qc1.stdout and "FAIL record_missing" in qc1.stdout
    assert "citation corrected" in qc1.stdout
    # Stage 3 pains: quote_check.csv statuses, drop rules, tags, ranks
    with open(run / "03_listen" / "quote_check.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        assert reader.fieldnames == ["pain_id", "record_id", "status", "reason", "citation_corrected", "url", "date", "quote"]
        rows = list(reader)
    p1_rows = [r for r in rows if r["pain_id"] == P1]
    assert [r["reason"] for r in p1_rows] == ["ok", "ok", "not_substring", "too_short", "record_missing"]
    assert [r["citation_corrected"] for r in p1_rows] == ["no", "yes", "no", "no", "no"]
    assert p1_rows[1]["url"] == LINKS["r2"][1], "the corrected citation carries the stored url"
    assert [r["reason"] for r in rows if r["pain_id"] == DROP_QUOTES] == ["ok", "not_substring"]
    assert [r["status"] for r in rows if r["pain_id"] == P2] == ["pass", "pass", "pass"]
    pains = read_json(run / "03_listen" / "pains.json")
    assert pains["kept"] == [P1, P2, P3, P5, P4] and pains["cut"] == [] and pains["dropped"] == [DROP_QUOTES, DROP_FLAT]
    by_pid = {p["pain_id"]: p for p in pains["pains"]}
    assert by_pid[P1]["verified_quote_count"] == 2 and by_pid[P1]["quote_check"]["failed_reasons"] == {"not_substring": 1, "record_missing": 1, "too_short": 1}
    assert by_pid[P1]["quotes"][1]["url"] == LINKS["r2"][1] and by_pid[P1]["quotes"][1]["date"] is None
    assert by_pid[P1]["spend_domains"] == ["prices.test", "reddit.com"]
    assert set(by_pid[P1]["tags"]) >= {"[thin]", "[titles only]"} and "[undated share: 75%]" in by_pid[P1]["tags"]
    assert "[spend: 1 source]" in by_pid[P3]["tags"] and "[spend: 0 sources]" in by_pid[P4]["tags"]
    assert by_pid[DROP_FLAT]["drop_reason"].startswith("no money mention, no failed spend and urgency none")
    assert by_pid[DROP_QUOTES]["drop_reason"].startswith("fewer than 2 verified quotes: 1 of 2 passed")
    assert pains["needs_calls"] == [R1]
    assert by_pid[P2]["urgency_type"] == "acute_pain" and by_pid[P2]["sources"] == {"websearch": 3}
    # Stage 4: the kill, the trade hint, walker disagreements, the rendered walk
    s4 = read_json(run / "04_walks" / "_stage4.json")
    assert s4["kept"] == [P1, P2, P3, P5] and s4["killed"] == [P4] and s4["lane_hint_trade"] == [P3]
    e1 = next(e for e in s4["pains"] if e["pain_id"] == P1)
    assert e1["walls_both"] == ["W2", "W4", "W9", "W20"] and e1["walls_one"] == ["W5"] and e1["persisting_walls"] == ["W20"]
    assert any("walker b says unsure" in d for d in e1["disagreements"]["computed"])
    e4 = next(e for e in s4["pains"] if e["pain_id"] == P4)
    assert e4["kill_reason"].startswith("outcome reached today with their own AI (walker b and the comparator say so)")
    walk_md = (run / "04_walks" / f"{P1}.md").read_text(encoding="utf-8")
    assert "## Where the walkers disagreed" in walk_md and "| W9 | Effort | machine | melts | unsure | melts | melts |" in walk_md
    # Stage 5: one lane each, one kill listing every failed check
    s5 = read_json(run / "05_pairs.json")
    lanes = {x["pain_id"]: x["lane"] for x in s5["pains"]}
    assert lanes == {P1: "business", P2: "partner", P3: "trade", P5: None}
    assert s5["kept"] == [P1, P2, P3] and s5["killed"] == [P5] and s5["counts"]["by_lane"] == {"business": 1, "partner": 1, "trade": 1}
    x1 = next(x for x in s5["pains"] if x["pain_id"] == P1)
    assert x1["kept"]["hold_supply_id"] == "c1" and x1["kept_index"] == 1 and x1["alternatives"][1]["lane"] == "partner"
    x2 = next(x for x in s5["pains"] if x["pain_id"] == P2)
    assert x2["kept"]["partner_id"] == "r1" and x2["alternatives"][1]["valid"] is False
    x3 = next(x for x in s5["pains"] if x["pain_id"] == P3)
    assert x3["kept"]["trade"]["exit_date"] == "2027-03-31" and x3["kept"]["hold_wall"] is None
    x5 = next(x for x in s5["pains"] if x["pain_id"] == P5)
    assert x5["kill_reason"].startswith("no pair, no clean trade, no plausible partner") and "cannot list" in x5["kill_reason"]
    # Stage 6: the numbers kill, two survivors in rank order, the --check verdict
    assert "Would be killed by `funnel numbers`: cash30" in out["numbers-check"].stdout
    s6 = read_json(run / "06_survivors.json")
    assert s6["kept"] == [P1, P2] and s6["killed"] == [P3] and s6["cut"] == []
    k3 = next(e for e in s6["pains"] if e["pain_id"] == P3)
    assert k3["failed_checks"] == ["cash30"] and k3["cases"]["base"]["cash30"] == 0.0
    k1 = next(e for e in s6["pains"] if e["pain_id"] == P1)
    assert k1["lane"] == "business" and k1["opens_ladder"] is True and k1["counts"]["failed_spend"] == 1 and k1["counts"]["records"] == 4
    assert k1["anchor"]["price_status"] == "seen_via_search"
    csv6 = (run / "06_numbers.csv").read_text(encoding="utf-8").splitlines()
    assert len(csv6) == 1 + 3 * 3
    # red team and the case against: the judge swaps the order
    red = read_json(run / "07_red_team" / "_redteam.json")
    assert red["counts"] == {"survivors": 2, "files": 2, "points": 2, "by_kind": {"competitor": 1, "failed_attempt": 0, "not_paid_for": 1, "legal_or_platform": 0},
                             "by_severity": {"high": 0, "medium": 1, "low": 1}, "verdicts": {"keep": 1, "down": 1, "kill": 0}}
    assert "ordered by case against: us-freelancers--late-invoices, gre-engineers-india--quant-plateau" in out["shortlist"].stdout
    # SHORTLIST: order, the ten sections in order, the case against with its rank change
    sl = (run / "SHORTLIST.md").read_text(encoding="utf-8")
    assert f"| 1 | {P2} | partner |" in sl and f"| 2 | {P1} | business |" in sl
    assert sl.index(f"## 1. {P2}") < sl.index(f"## 2. {P1}")
    for pid in (P1, P2):
        sec = section(sl, f"## {1 if pid == P2 else 2}. {pid}")
        heads = re.findall(r"^### (\d+)\. ", sec, re.M)
        assert heads == [str(i) for i in range(1, 11)], f"{pid}: {heads}"
        assert "### 10. Case against" in sec
    s1 = section(sl, f"## 2. {P1}")
    assert "Source: the judge's case_against.json. 1 point(s)." in s1 and "competitor (high; red_team)" in s1
    assert "Rank change: 1 -> 2 (a competitor already delivers the same pair)." in s1
    assert "Rank change: 2 -> 1 (no material point)." in section(sl, f"## 1. {P2}")
    assert "At least 1 of 20 room members, reached by WhatsApp, will pay INR 5,000.00 (USD 56.82)" in s1
    assert "Entry walls (how the product gets in): W2 Diagnosis, W4 Context, W9 Effort." in s1
    assert "Holding wall (why customers keep it): W20 Accountability; the founder can be it (c1: Accountability: coaching and cohorts)." in s1
    assert "Holding wall (why customers keep it): W18 License; a partner supplies it (r1:" in section(sl, f"## 1. {P2}")
    assert f'"{text_of("r1")}" <{LINKS["r1"][1]}>' in s1
    assert "[spend: 1 source]" not in s1 and "[thin] [titles only]" in s1
    # REVIEW: seven sections, the [assumed] items, the logged choices, calls, sources, trust, overlaps
    rv = (run / "REVIEW.md").read_text(encoding="utf-8")
    for n in range(1, 8):
        assert re.search(rf"^## {n}\. ", rv, re.M), f"REVIEW section {n}"
    assumed = re.findall(r"^- line \d+: .*\[assumed", rv, re.M)
    assert len(assumed) >= 5 and any("hour" in a.lower() for a in assumed)
    s_1 = section(rv, "## 1. ")
    assert "- stage 2 (log): Chose the low end of the hours range." in s_1
    assert "- stage 2 (mask): Only 2 room(s) passed the mask; fewer than 5." in s_1
    assert "- stage 3 (pains): Rooms that need calls" in s_1 and "Rooms that stopped before saturation" in s_1
    assert "kill-rule defaults used" in s_1.lower() and "stage3.quote_min_words = 5" in s_1
    assert "Human walls the ledger does not mention, treated as not supplied: W21 Advocacy" in s_1
    quotes = re.findall(r'^- "(.+)" \(', section(rv, "## 2. "), re.M)
    assert len(quotes) == 3 and all(any(q == text_of(h) or q in text_of(h) for h in LINKS) for q in quotes)
    s_3 = section(rv, "## 3. ")
    assert f"- 1. {P2}: Will this room accept the founder as a coach?" in s_3 and f"- 2. {P1}:" in s_3
    assert f"- {R1}: older test takers rarely post" in section(rv, "## 4. ") and R2 not in section(rv, "## 4. ")
    s_5 = section(rv, "## 5. ")
    assert f"| reddit | skipped | no API key | first-person posts with dates | room {R1} |" in s_5
    assert "| Reddit Data API | skip |" in s_5 and "config/sources.md" in s_5
    assert f"- {R2}: trust reasoning" in section(rv, "## 6. ") and R1 not in section(rv, "## 6. ")
    assert f"- {R1}: ventures v1 (GRE business: the GRE product and app)." in section(rv, "## 7. ")
    # RUNLOG: from the events only, no timestamp, every section
    rl = (run / "RUNLOG.md").read_text(encoding="utf-8")
    assert not re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}", rl)
    assert "api.stackexchange.com" in section(rl, "## Domains to allow")
    assert f"| {R1} | 12 | websearch 12 |" in rl and f"| {R2} | 8 | websearch 8 |" in rl
    assert f"| {R1} | 2 | 11 | 4 | none | 0 | no | exhausted |" in rl
    assert "| 3 | pains | rooms 2; drafted 7; kept 5; cut 0; dropped 2 |" in rl
    assert "| 6 | numbers | in 3; passed 2; kept 2; cut 0; killed 1 |" in rl
    assert "| 7 | shortlist | survivors 2; killed by the case against 0 |" in rl
    errs = section(rl, "## Errors")
    assert "(walks, exit 1)" in errs and "W9 is marked persists" in errs and "(saturation, exit 1)" in errs
    assert "Chose the low end of the hours range." not in section(rl, "## Build and test results")
    assert "## Notes logged with `funnel log`" not in rl, "a review note is not repeated as a plain note"
    # PROGRESS, status and the commit message
    pg = (root / "PROGRESS.md").read_text(encoding="utf-8")
    assert pg.startswith("# Progress\n") and "## Done" in pg and "## Next" in pg
    block = pg[pg.index("<!-- auto:status -->"):pg.index("<!-- /auto:status -->")]
    assert "| 3 | pains (`03_listen/pains.json`) | done |" in block and "| 7 | runlog (`RUNLOG.md`) | done |" in block
    assert f"| {R1} | 2 | 12 | 11 |" in block and "Rooms kept: 2. Pains kept: 5. Stage 6 kept: 2. Survivors (final): 2." in block
    assert f"survivors 2: {P2}, {P1}." in out["status"].stdout and "Next without an output: everything has an output." in out["status"].stdout
    assert out["commit-message"].stdout.strip() == f"funnel: run {RUN_NAME}: 2 rooms, 5 pains, 2 survivors"
    # graveyard: one line per kill, every stage, no duplicates
    gy = (root / "graveyard.md").read_text(encoding="utf-8")
    lines = [ln for ln in gy.splitlines() if ln.startswith("- ")]
    assert len(lines) == len(set(lines))
    expected = [
        f"- {RUN_NAME} | stage 2 | room:{DEAD_LADDER} | failed ladder: 2 ladder step(s); needs at least 3",
        f"- {RUN_NAME} | stage 2 | room:{DEAD_SUPPLY} | failed supply: blocked: the room's core pains need large_capital",
        f"- {RUN_NAME} | stage 3 | pain:{DROP_FLAT} | no money mention, no failed spend and urgency none",
        f"- {RUN_NAME} | stage 3 | pain:{DROP_QUOTES} | fewer than 2 verified quotes: 1 of 2 passed the quote check (not_substring 1)",
        f"- {RUN_NAME} | stage 4 | pain:{P4} | outcome reached today with their own AI (walker b and the comparator say so)",
        f"- {RUN_NAME} | stage 5 | pain:{P5} | no pair, no clean trade, no plausible partner: alternative 1 (rank 1): entry: only 2 distinct entry wall(s); needs at least 3",
        f"- {RUN_NAME} | stage 6 | pain:{P3} | numbers fail in the base case: cash30: cash in the first 30 days per customer is INR 0.00",
    ]
    for exp in expected:
        assert any(ln.startswith(exp) for ln in lines), exp
    assert len(lines) == len(expected)
    # privacy: the raw email, phone and the search summary appear nowhere under the funnel root
    for p in sorted(root.rglob("*")):
        if p.is_file():
            text = p.read_text(encoding="utf-8", errors="ignore")
            for needle in (EMAIL, "98765 43210", "9876543210", "SUMMARY-NEVER-STORED"):
                assert needle not in text, f"{needle} leaked into {p.relative_to(root)}"


def test_full_run_twice_through_the_cli(froot, cli, tmp_path, monkeypatch):
    tdir = tmp_path / "transcripts"
    write_transcripts(tdir)
    monkeypatch.setenv("FUNNEL_TRANSCRIPTS_DIR", str(tdir))
    flow = Flow(froot, cli)
    flow.run_pass()
    check_pass_one(flow)
    first = snapshot(flow)
    first_events = (flow.run / "runlog.jsonl").read_text(encoding="utf-8").count("\n")
    assert first and first_events > 50

    second = Flow(froot, cli)
    second.run_pass()
    check_pass_one(second, first_pass=False)
    again = snapshot(second)
    assert sorted(again) == sorted(first), (sorted(set(again) ^ set(first)))
    changed = [k for k in first if first[k] != again[k]]
    assert not changed, f"not byte-identical on the second pass: {changed}"
    events = (flow.run / "runlog.jsonl").read_text(encoding="utf-8").count("\n")
    assert events > first_events, "the run log keeps growing: it is the only file that records each pass"
    gy = (froot / "graveyard.md").read_text(encoding="utf-8")
    lines = [ln for ln in gy.splitlines() if ln.startswith("- ")]
    assert len(lines) == len(set(lines)) == 7
