"""Stage 4 `walks [--check PAIN_ID]` and Stage 5 `pairs` (pipeline/stage45.py).

Covers: walker and merged file validation, the conservative merge re-derived from
.a/.b and every way a merged file can be less conservative (each named by field),
reconciled_ids, the kill on outcome reached today, lane_hint trade, the rendered
walk markdown with walker disagreements, _stage4.json, --check; then every pair
check (entry, walls_both, adjacency, hold, persistence, lane), each lane
(business incl. c2 Judgment by depth strength, partner via can_rent or a partner
kind, trade conditions, the cannot list), the strongest-valid choice by lane order
then rank, the kill listing each alternative's failures, 05_pairs.json/.md,
determinism and the CLI.
"""
import json

import common
import records
import stage45
from conftest import Helpers

ROOM = "gre-engineers-india"      # Stage 2 depth d1 (strong)
ROOM2 = "mba-applicants"          # Stage 2 depth d6 (moderate)
DATE = "2026-09-26"
PID = f"{ROOM}--quant-plateau"


# --------------------------------------------------------------------------- builders
def setup(run, pains=(PID,), mask=True):
    """Stored records (for persona ids), a pains.json with kept pains, and 02_mask.json. Returns record ids by room."""
    ids = {}
    for room in sorted({common.split_pain_id(p)[0] for p in pains}):
        out = records.store_records(run, room, "websearch", [
            Helpers.make_record(f"https://forum.test/{room}/1", f"A member of {room} describing the problem in detail", rank=1),
            Helpers.make_record(f"https://forum.test/{room}/2", f"Another member of {room} who paid and is still stuck", rank=2),
        ])
        ids[room] = out["new_ids"]
    common.write_json(common.listen_dir(run) / "pains.json", {"pains": [
        {"pain_id": p, "room": common.split_pain_id(p)[0], "pain_key": common.split_pain_id(p)[1], "status": "kept",
         "rank": i, "tags": ["[thin]"]} for i, p in enumerate(pains, 1)
    ] + [{"pain_id": f"{ROOM}--dropped-one", "room": ROOM, "pain_key": "dropped-one", "status": "dropped", "rank": None}]})
    if mask:
        common.write_json(run / "02_mask.json", {"rooms": [
            {"slug": ROOM, "status": "kept", "depth_ledger_id": "d1", "depth_strength": "strong"},
            {"slug": ROOM2, "status": "kept", "depth_ledger_id": "d6", "depth_strength": "moderate"},
        ]})
    return ids


def walk(pid, letter, steps, forward, reached=False, persona_ids=None):
    today = [{"step": i, "does": f"they do step {i}", "drops_out": False, "why": "", "walls": list(ws),
              "reasoning": "from the records", "confidence": "moderate"} for i, ws in enumerate(steps, 1)]
    fwd = [{"wall": w, "status": s, "reasoning": "the assistant improves", "confidence": "low"} for w, s in forward.items()]
    d = {"pain_id": pid, "persona": {"description": "a typical member", "record_ids": list(persona_ids or ["x"])},
         "outcome": "a 165+ quant score", "today": today,
         "outcome_reached_today": {"value": reached, "reasoning": "judged from the walk", "confidence": "high"},
         "forward_12m": fwd}
    if letter:
        d["walker"] = letter
    return d


def merge(a, b, reconciled=(), pairs=(), disagreements=(), persona_ids=None):
    """A merged file that follows the conservative rule exactly (tests mutate it to break the rule)."""
    d = stage45.derive_merge(a, b, list(reconciled))
    steps = []
    for i in range(max(len(a["today"]), len(b["today"]))):
        ws = []
        for w_, mp in ((a, d["map_a"]), (b, d["map_b"])):
            if i < len(w_["today"]):
                for w in w_["today"][i]["walls"]:
                    m = mp.get(w, w)
                    if m not in ws:
                        ws.append(m)
        steps.append(ws)
    m = walk(a["pain_id"], None, steps, dict(d["forward"]), reached=d["outcome_reached"], persona_ids=persona_ids or a["persona"]["record_ids"])
    m["agreement"] = {"outcome": "agree" if d["outcome_a"] == d["outcome_b"] else "disagree",
                      "walls_both": list(d["walls_both"]), "walls_one": list(d["walls_one"]), "reconciled_ids": list(reconciled)}
    m["disagreements"] = list(disagreements)
    m["pairs"] = list(pairs)
    return m


def pair(rank, entry, hold=None, supply=None, partner=None, kind=None, trade=None):
    return {"rank": rank, "entry_walls": list(entry), "hold_wall": hold, "hold_supply_id": supply, "partner_id": partner,
            "partner_kind": kind, "trade": trade,
            "one_liner": f"For the room, a promise in a month, because {', '.join(entry)}, held by {hold or 'nothing'}.",
            "crux": "will they pay before the exam", "credibility_question": "Will this room accept the founder as a coach?",
            "reasoning": "the walls sit together on the path", "confidence": "moderate"}


def trade(weeks=1, upfront=True, sub=False, exit="2027-03-31"):
    return {"build_weeks": weeks, "payment_upfront": upfront, "subscription": sub, "exit_date": exit}


STD_STEPS = [["W2"], ["W4"], ["W9"], ["W20"]]
STD_FWD = {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}


def write_walk_set(run, pid, ids, a=None, b=None, merged=None, pairs=None, a_kw=None, b_kw=None, reconciled=()):
    a = a or walk(pid, "a", STD_STEPS, STD_FWD, persona_ids=ids, **(a_kw or {}))
    b = b or walk(pid, "b", STD_STEPS, STD_FWD, persona_ids=ids, **(b_kw or {}))
    merged = merged or merge(a, b, reconciled=reconciled, pairs=pairs if pairs is not None else
                             [pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], "W20", kind="a coach")])
    paths = stage45.walk_paths(run, pid)
    common.write_json(paths["a"], a)
    common.write_json(paths["b"], b)
    common.write_json(paths["merged"], merged)
    return a, b, merged


def stage4(run):
    return json.loads((run / "04_walks" / "_stage4.json").read_text(encoding="utf-8"))


def pairs_json(run):
    return json.loads((run / "05_pairs.json").read_text(encoding="utf-8"))


def graveyard(froot):
    return (froot / "graveyard.md").read_text(encoding="utf-8")


def errors_of(run, pid):
    return stage45.walks(run, check=pid)["errors"]


def where(pid, suffix=".json"):
    return f"runs/{DATE}/04_walks/{pid}{suffix}"


# =========================================================================== Stage 4: walks
def test_walks_validates_merges_renders_and_keeps(froot, run, cli):
    ids = setup(run)[ROOM]
    a = walk(PID, "a", [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    b = walk(PID, "b", [["W2"], ["W4", "W9"], ["W20"], []], {"W2": "melts", "W4": "unsure", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    merged = walk(PID, None, [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    merged["agreement"] = {"outcome": "agree", "walls_both": ["W2", "W4", "W9", "W20"], "walls_one": [],
                           "reconciled_ids": []}
    merged["disagreements"] = ["walker b was unsure whether W4 Context melts"]
    merged["pairs"] = [pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], "W20", kind="a coach")]
    write_walk_set(run, PID, ids, a=a, b=b, merged=merged)
    r = cli("walks", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert "Walks: 1 kept pain(s) in, 1 walked, 1 kept, 0 killed (outcome reached today), 0 hinted trade." in r.stdout
    assert f"kept: {PID} (walls both: W2, W4, W9, W20; persists: W20; pairs drafted: 2)" in r.stdout
    s4 = stage4(run)
    assert s4["kept"] == [PID] and s4["killed"] == [] and s4["lane_hint_trade"] == []
    assert s4["counts"] == {"in": 1, "walked": 1, "kept": 1, "killed": 0, "lane_hint_trade": 0}
    assert s4["rules"] == {"unsure_counts_as": "melts", "kill_only_if_outcome_reached_today": True, "conservative_merge": True}
    e = s4["pains"][0]
    assert e["status"] == "kept" and e["kill_reason"] is None and e["room"] == ROOM and e["stage3_rank"] == 1 and e["tags"] == ["[thin]"]
    assert e["walls_both"] == ["W2", "W4", "W9", "W20"] and e["walls_one"] == []
    assert e["forward_12m"] == {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}
    assert e["persisting_walls"] == ["W20"] and e["lane_hint"] is None and e["outcome_reached_today"] is False
    assert e["path_walls"] == {"W2": 1, "W4": 2, "W9": 3, "W20": 4} and e["steps"] == 4 and e["pairs_drafted"] == 2
    assert e["disagreements"]["comparator"] == ["walker b was unsure whether W4 Context melts"]
    assert e["disagreements"]["computed"] == ["W4 in 12 months: walker a says melts, walker b says unsure (merge: melts)."]
    assert e["walkers"]["a"]["path"] == ["W2", "W4", "W9", "W20"] and e["walkers"]["b"]["forward"]["W4"] == "unsure"
    assert e["walkers"]["b"]["steps"] == 4 and e["walkers"]["a"]["outcome_reached_today"] is False
    md = (run / "04_walks" / f"{PID}.md").read_text(encoding="utf-8")
    assert md.startswith(f"# Walk: {PID}\n\nRun: {DATE}. Status: kept.\n")
    assert "## Persona\n\na typical member (records: " + ", ".join(ids) + ")" in md
    assert "## Outcome they want\n\na 165+ quant score" in md
    assert "| Step | What they do | Drops out? | Why | Walls |" in md and "| 4 | they do step 4 | no |  | W20 Accountability |" in md
    assert "Outcome reached today: no. judged from the walk (walker a: no; walker b: no)" in md
    assert "## Twelve months from now" in md
    assert "| W4 | Context | machine | melts | unsure | melts | melts |" in md
    assert "| W20 | Accountability | human | persists | persists | persists | persists |" in md
    assert "Walls both walkers met: W2, W4, W9, W20. Walls only one walker met: none." in md
    assert "Walls that persist (both walkers agree): W20." in md
    assert "## Where the walkers disagreed\n\n- walker b was unsure whether W4 Context melts\n- (computed) W4 in 12 months: walker a says melts, walker b says unsure (merge: melts)." in md
    assert "## Pairs drafted (2)" in md and "- rank 1: entry W2, W4, W9; hold W20 (c1). For the room" in md
    assert "- rank 2: entry W2, W4, W9; hold W20 (partner a coach)." in md
    assert "pain:" not in graveyard(froot)
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(ev["kind"] == "count" and ev["command"] == "walks" and ev["kept"] == 1 for ev in events)


def test_kill_when_outcome_reached_today_by_either_walker(froot, run, cli):
    ids = setup(run)[ROOM]
    a, b, m = write_walk_set(run, PID, ids, a_kw={"reached": True})
    assert m["outcome_reached_today"]["value"] is True and m["agreement"]["outcome"] == "disagree"
    r = cli("walks", "--run", DATE)
    assert r.returncode == 0, r.stderr
    s4 = stage4(run)
    e = s4["pains"][0]
    assert s4["killed"] == [PID] and s4["kept"] == [] and e["status"] == "killed"
    assert e["kill_reason"] == "outcome reached today with their own AI (walker a and the comparator say so): judged from the walk"
    assert f"killed: {PID}: outcome reached today with their own AI (walker a and the comparator say so)" in r.stdout
    gy = graveyard(froot)
    assert f"- {DATE} | stage 4 | pain:{PID} | outcome reached today with their own AI (walker a and the comparator say so): judged from the walk" in gy
    md = (run / "04_walks" / f"{PID}.md").read_text(encoding="utf-8")
    assert "Status: killed (outcome reached today" in md and "(walker a: yes; walker b: no)" in md
    assert "- (computed) outcome today: walker a says reached, walker b says not reached (merge: reached if either says so)." in md
    # a merged file that denies it is less conservative
    m["outcome_reached_today"]["value"] = False
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    r = cli("walks", "--run", DATE)
    assert r.returncode == 1
    assert f"04_walks/{PID}.json: outcome_reached_today.value must be true: walker a say(s) the outcome is reached today, and the conservative merge takes either walker's yes." in r.stderr
    # the comparator alone may say reached (more conservative), and the kill rule can be switched off
    a2, b2, m2 = write_walk_set(run, PID, ids)
    m2["outcome_reached_today"]["value"] = True
    common.write_json(stage45.walk_paths(run, PID)["merged"], m2)
    assert stage45.walks(run)["killed"] == [PID]
    assert "(the comparator say so)" in stage4(run)["pains"][0]["kill_reason"]
    Helpers.set_rule(froot, "stage4", "kill_only_if_outcome_reached_today", False)
    result = stage45.walks(run)
    assert result["kept"] == [PID] and result["pains"][0]["outcome_reached_today"] is True
    assert "the outcome is reached today, but kill_only_if_outcome_reached_today is off; the pain was kept." in result["pains"][0]["warnings"]


def test_all_walls_melt_gives_lane_hint_trade(run):
    ids = setup(run)[ROOM]
    fwd = dict(STD_FWD, W20="melts")
    a = walk(PID, "a", STD_STEPS, fwd, persona_ids=ids)
    b = walk(PID, "b", STD_STEPS, dict(STD_FWD, W20="unsure"), persona_ids=ids)
    write_walk_set(run, PID, ids, a=a, b=b, pairs=[pair(1, ["W2", "W4", "W9"], trade=trade()), pair(2, ["W2", "W4", "W9"], trade=trade(weeks=2))])
    result = stage45.walks(run)
    e = result["pains"][0]
    assert result["lane_hint_trade"] == [PID] and e["lane_hint"] == "trade" and e["persisting_walls"] == []
    assert e["forward_12m"]["W20"] == "melts" and e["status"] == "kept"
    assert e["disagreements"]["computed"] == ["W20 in 12 months: walker a says melts, walker b says unsure (merge: melts)."]
    md = (run / "04_walks" / f"{PID}.md").read_text(encoding="utf-8")
    assert "No wall persists: every wall melts within 12 months. Lane hint: trade (machine walls only)." in md
    assert "- rank 1: entry W2, W4, W9; hold none (trade). For the room" in md


# --------------------------------------------------------------------------- the conservative merge
def test_derive_merge_rules():
    a = walk(PID, "a", [["W2"], ["W4", "W9"], ["W20"], ["W13"]], {"W2": "melts", "W4": "persists", "W9": "unsure", "W20": "persists", "W13": "persists"})
    b = walk(PID, "b", [["W2", "W4"], ["W9"], ["W20"], ["W25"]], {"W2": "persists", "W4": "persists", "W9": "persists", "W20": "unsure", "W25": "persists"}, reached=True)
    d = stage45.derive_merge(a, b, [])
    assert d["outcome_reached"] is True and d["outcome_a"] is False and d["outcome_b"] is True
    assert d["walls_both"] == ["W2", "W4", "W9", "W20"] and d["walls_one"] == ["W13", "W25"]
    assert d["forward"] == {"W2": "melts", "W4": "persists", "W9": "melts", "W13": "melts", "W20": "melts", "W25": "melts"}
    assert d["path_a"] == {"W2": 1, "W4": 2, "W9": 2, "W20": 3, "W13": 4} and d["path_b"]["W4"] == 1
    assert d["disagreements"] == [
        "outcome today: walker a says not reached, walker b says reached (merge: reached if either says so).",
        "walls only walker a put on the path: W13.",
        "walls only walker b put on the path: W25.",
        "W2 in 12 months: walker a says melts, walker b says persists (merge: melts).",
        "W9 in 12 months: walker a says unsure, walker b says persists (merge: melts).",
        "W20 in 12 months: walker a says persists, walker b says unsure (merge: melts).",
    ]
    # unsure may count as persists when the kill rules say so
    d2 = stage45.derive_merge(a, b, [], unsure_as="persists")
    assert d2["forward"]["W9"] == "persists" and d2["forward"]["W20"] == "persists" and d2["forward"]["W2"] == "melts"


def test_reconciled_ids_are_honored(run, cli):
    ids = setup(run)[ROOM]
    a = walk(PID, "a", [["W2"], ["W4"], ["W10"], ["W20"]], {"W2": "melts", "W4": "melts", "W10": "persists", "W20": "persists"}, persona_ids=ids)
    b = walk(PID, "b", [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    d = stage45.derive_merge(a, b, [])
    assert d["walls_both"] == ["W2", "W4", "W20"] and d["walls_one"] == ["W9", "W10"]
    rec = [{"a": "W10", "b": "W9", "as": "W9", "reasoning": "both mean the answer is not in a usable shape"}]
    d = stage45.derive_merge(a, b, rec)
    assert d["walls_both"] == ["W2", "W4", "W9", "W20"] and d["walls_one"] == [] and d["forward"]["W9"] == "melts"
    assert d["map_a"] == {"W10": "W9"} and d["map_b"] == {"W9": "W9"}
    assert d["disagreements"] == ["W9 in 12 months: walker a says persists, walker b says melts (merge: melts)."]
    # without reconciliation the comparator may not count W9 for both
    m = merge(a, b)
    m["agreement"]["walls_both"] = ["W2", "W4", "W9", "W20"]
    m["agreement"]["walls_one"] = ["W10"]
    write_walk_set(run, PID, ids, a=a, b=b, merged=m)
    errs = errors_of(run, PID)
    assert f"{where(PID)}: agreement.walls_both holds W9, but only walker b put it on the path. A wall counts only when both walkers put it, or a reconciled equivalent, on the path." in errs
    assert any("agreement.walls_one must list exactly the walls only one walker put on the path: W9, W10 (got W10)" in e for e in errs)
    # with reconciliation it counts, and the merged walk must use the reconciled id
    m = merge(a, b, reconciled=rec, pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], "W20", kind="a coach")])
    assert m["today"][2]["walls"] == ["W9"] and m["agreement"]["walls_both"] == ["W2", "W4", "W9", "W20"]
    write_walk_set(run, PID, ids, a=a, b=b, merged=m)
    assert errors_of(run, PID) == []
    result = stage45.walks(run)
    e = result["pains"][0]
    assert e["walls_both"] == ["W2", "W4", "W9", "W20"] and e["reconciled_ids"] == rec and e["walkers"]["a"]["path"] == ["W2", "W4", "W9", "W20"]
    md = (run / "04_walks" / f"{PID}.md").read_text(encoding="utf-8")
    assert "| W9 | Effort | machine | persists | melts | melts | melts |" in md
    assert "- walker a W10 = walker b W9 -> W9: both mean the answer is not in a usable shape" in md
    bad = json.loads(json.dumps(m))
    bad["today"][2]["walls"] = ["W10"]
    bad["forward_12m"][2]["wall"] = "W10"
    common.write_json(stage45.walk_paths(run, PID)["merged"], bad)
    r = cli("walks", "--run", DATE)
    assert r.returncode == 1
    assert "today: wall W10 appears in the merged walk, but neither walker put it on the path (walker a's W10 was reconciled as W9; use W9)." in r.stderr
    assert "today: wall W9 is in agreement.walls_both but not on the merged today path. Put it on the step where both walkers met it." in r.stderr
    # a reconciliation must name two walls of the same kind and pick one of them
    bad = json.loads(json.dumps(m))
    bad["agreement"]["reconciled_ids"] = [{"a": "W10", "b": "W20", "as": "W20", "reasoning": "x"}, {"a": "W10", "b": "W9", "as": "W11", "reasoning": ""}]
    common.write_json(stage45.walk_paths(run, PID)["merged"], bad)
    errs = errors_of(run, PID)
    assert any("reconciled_ids 1: W10 and W20 are not the same kind of wall (machine vs human)" in e for e in errs)
    assert any("reconciled_ids 2: 'as' must be one of the two reconciled walls (W10 or W9), not a third wall." in e for e in errs)
    assert any("reconciled_ids 2: 'reasoning' is missing" in e for e in errs)


def test_less_conservative_merged_files_are_rejected_naming_the_field(run, cli):
    ids = setup(run)[ROOM]
    a = walk(PID, "a", [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    b = walk(PID, "b", [["W2"], ["W4"], ["W20"], ["W13"]], {"W2": "melts", "W4": "unsure", "W20": "unsure", "W13": "persists"}, persona_ids=ids)
    good = merge(a, b, pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4"], "W20", kind="x")])
    assert good["agreement"] == {"outcome": "agree", "walls_both": ["W2", "W4", "W20"], "walls_one": ["W9", "W13"], "reconciled_ids": []}
    assert good["forward_12m"] == [{"wall": w, "status": "melts", "reasoning": "the assistant improves", "confidence": "low"} for w in ("W2", "W4", "W9", "W13", "W20")]
    write_walk_set(run, PID, ids, a=a, b=b, merged=good)
    assert errors_of(run, PID) == []
    here = where(PID)

    def check(mutate, *needles):
        m = json.loads(json.dumps(good))
        mutate(m)
        common.write_json(stage45.walk_paths(run, PID)["merged"], m)
        errs = errors_of(run, PID)
        for needle in needles:
            assert any(needle in e and e.startswith(here) for e in errs), (needle, errs)
        return errs

    def set_fwd(m, wall, status):
        for f in m["forward_12m"]:
            if f["wall"] == wall:
                f["status"] = status

    # a wall persists only if both say persists: unsure counts as melts
    check(lambda m: set_fwd(m, "W20", "persists"),
          "forward_12m: W20 is marked persists, but walker a says persists and walker b says unsure. A wall persists only if both say persists (unsure counts as melts).")
    check(lambda m: set_fwd(m, "W4", "persists"), "forward_12m: W4 is marked persists, but walker a says melts and walker b says unsure.")
    check(lambda m: set_fwd(m, "W9", "persists"), "forward_12m: W9 is marked persists, but walker a says melts and walker b says nothing (not on its path).")
    # unsure in the merged file counts as melts, so it is never less conservative
    m = json.loads(json.dumps(good))
    set_fwd(m, "W9", "unsure")
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    assert errors_of(run, PID) == []
    check(lambda m: set_fwd(m, "W13", "persists"), "forward_12m: W13 is marked persists, but walker a says nothing (not on its path) and walker b says persists.")
    # walls_both may only hold walls both walkers met
    check(lambda m: m["agreement"]["walls_both"].append("W9"), "agreement.walls_both holds W9, but only walker a put it on the path.")
    check(lambda m: m["agreement"]["walls_both"].append("W13"), "agreement.walls_both holds W13, but only walker b put it on the path.")
    check(lambda m: m["agreement"]["walls_both"].append("W15"), "agreement.walls_both holds W15, but neither walker put it on the path (after reconciliation).")
    check(lambda m: m["agreement"].update(outcome="disagree"), "agreement.outcome must be agree: walker a says not reached, walker b says not reached.")
    check(lambda m: m["agreement"].update(walls_one=["W9"]), "agreement.walls_one must list exactly the walls only one walker put on the path: W9, W13 (got W9).")
    # the merged path may only hold walls a walker met, and must hold every walls_both wall
    check(lambda m: m["today"][0]["walls"].append("W15") or m["forward_12m"].append({"wall": "W15", "status": "melts", "reasoning": "r", "confidence": "low"}),
          "today: wall W15 appears in the merged walk, but neither walker put it on the path.")
    def drop_w20(m):
        for st in m["today"]:
            st["walls"] = [w for w in st["walls"] if w != "W20"]
        m["forward_12m"] = [f for f in m["forward_12m"] if f["wall"] != "W20"]

    check(drop_w20, "today: wall W20 is in agreement.walls_both but not on the merged today path.")
    # leaving a shared wall out of walls_both is more conservative: allowed, with a warning
    m = json.loads(json.dumps(good))
    m["agreement"]["walls_both"] = ["W2", "W20"]
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    assert errors_of(run, PID) == []
    result = stage45.walks(run)
    e = result["pains"][0]
    assert e["walls_both"] == ["W2", "W20"] and e["warnings"] == ["the comparator left W4 out of walls_both although both walkers put them on the path (allowed: it is more conservative)."]
    # unsure may count as persists, and the whole check can be switched off, from the kill rules
    m = json.loads(json.dumps(good))
    set_fwd(m, "W20", "persists")
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    assert any("W20 is marked persists" in x for x in errors_of(run, PID))
    Helpers.set_rule(run.parent.parent, "stage4", "unsure_counts_as", "persists")
    assert errors_of(run, PID) == []
    assert stage45.walks(run)["pains"][0]["persisting_walls"] == ["W20"]
    Helpers.set_rule(run.parent.parent, "stage4", "unsure_counts_as", "melts")
    Helpers.set_rule(run.parent.parent, "stage4", "conservative_merge", False)
    assert errors_of(run, PID) == []
    assert stage45.walks(run)["pains"][0]["persisting_walls"] == []  # the used verdict still needs both walkers
    r = cli("walks", "--run", DATE)
    assert r.returncode == 0, r.stderr


# --------------------------------------------------------------------------- validation of the files
def test_walk_file_validation_lists_every_problem(run, cli):
    ids = setup(run)[ROOM]
    a = walk(PID, "a", [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    b = walk(PID, "b", [["W2"], ["W4"], ["W9"], ["W20"]], {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists"}, persona_ids=ids)
    m = merge(a, b, pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], "W20", kind="x")])
    bad_a = json.loads(json.dumps(a))
    bad_a["pain_id"] = "other--pain"
    bad_a["walker"] = "b"
    bad_a["persona"]["record_ids"] = ["0000000000000000"]
    bad_a["outcome"] = ""
    bad_a["today"][1]["step"] = 5
    bad_a["today"][1]["walls"].append("W99")
    bad_a["today"][2]["drops_out"] = "no"
    bad_a["today"][2]["why"] = None
    del bad_a["today"][3]["reasoning"]
    bad_a["outcome_reached_today"]["value"] = "yes"
    bad_a["forward_12m"] = [f for f in bad_a["forward_12m"] if f["wall"] != "W20"]
    bad_a["forward_12m"].append({"wall": "W5", "status": "gone", "reasoning": "r", "confidence": "low"})
    bad_a["forward_12m"].append({"wall": "W2", "status": "melts", "reasoning": "r", "confidence": "meh"})
    bad_m = json.loads(json.dumps(m))
    del bad_m["agreement"]
    bad_m["disagreements"] = "one line"
    bad_m["pairs"][0].update(hold_supply_id="c9", partner_id="r9", entry_walls="W2", crux="")
    bad_m["pairs"][1].update(rank=1, trade={"build_weeks": -1, "payment_upfront": "yes", "subscription": False, "exit_date": "soon"}, hold_wall="W30")
    write_walk_set(run, PID, ids, a=bad_a, b=b, merged=bad_m)
    r = cli("walks", "--run", DATE)
    assert r.returncode == 1, r.stdout
    err = r.stderr
    for needle in (
        f"04_walks/{PID}.a.json: 'pain_id' must be {PID} (got 'other--pain').", "'walker' must be 'a' (got 'b')",
        "persona.record_ids: record 0000000000000000 is not stored for this room", "'outcome' is missing or empty",
        "today step 2: 'step' must be 2", "today step 2: wall 'W99' is not in config/walls.md (W1–W29)",
        "today step 3: 'drops_out' must be true or false", "today step 3: 'why' must be text",
        "today step 4: missing 'reasoning'", "outcome_reached_today.value must be true or false",
        "forward_12m 4: wall W5 is not on the today path", "forward_12m 4: 'status' must be persists, melts or unsure (got 'gone')",
        "forward_12m 5: wall W2 appears twice in forward_12m", "forward_12m 5: 'confidence' must be high, moderate or low",
        "forward_12m does not cover every wall in today: missing W20.",
        f"04_walks/{PID}.json: 'agreement' must be an object", "'disagreements' must be a list of one-line texts",
        "pair 1: 'hold_supply_id' 'c9' is not a ledger can_be id (c1, c2, c3, c4) or null",
        "pair 1: 'partner_id' 'r9' is not a ledger can_rent id (r1, r2, r3) or null",
        "pair 1: 'entry_walls' must be a list of wall ids", "pair 1: 'crux' is missing or empty",
        "pair 2: 'hold_wall' must be a wall id like W20, or null for a trade (got 'W30')",
        "pair 2: trade.build_weeks must be a number of weeks, 0 or more", "pair 2: trade.payment_upfront must be true or false",
        "pair 2: trade.exit_date must be a date YYYY-MM-DD or null (got 'soon')",
        "pair 2: rank 1 is also used by pair 1. Ranks must differ.",
    ):
        assert needle in err, needle
    assert not (run / "04_walks" / "_stage4.json").exists() and not (run / "04_walks" / f"{PID}.md").exists()
    (stage45.walk_paths(run, PID)["b"]).write_text("{oops", encoding="utf-8")
    r = cli("walks", "--check", PID, "--run", DATE)
    assert r.returncode == 1 and f"04_walks/{PID}.b.json: not valid JSON" in r.stderr


def test_check_one_pain_and_missing_files(run, cli):
    ids = setup(run, pains=(PID, f"{ROOM}--fees"))[ROOM]
    r = cli("walks", "--check", PID, "--run", DATE)
    assert r.returncode == 2 and f"No walk files for {PID}" in r.stderr
    a = walk(PID, "a", STD_STEPS, STD_FWD, persona_ids=ids)
    b = walk(PID, "b", STD_STEPS, dict(STD_FWD, W4="unsure"), persona_ids=ids)
    common.write_json(stage45.walk_paths(run, PID)["a"], a)
    r = cli("walks", "--check", PID, "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert f"{PID}.a.json: present" in r.stdout and f"{PID}.b.json: missing" in r.stdout and f"{PID}.json: missing" in r.stdout
    assert f"{PID}: no errors. Nothing was written." in r.stdout and "Conservative merge" not in r.stdout
    common.write_json(stage45.walk_paths(run, PID)["b"], b)
    r = cli("walks", "--check", PID, "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert "Conservative merge from the walker files: outcome reached today no; walls both: W2, W4, W9, W20; walls one: none; persists: W20." in r.stdout
    assert "  disagreement: W4 in 12 months: walker a says melts, walker b says unsure (merge: melts)." in r.stdout
    assert "Stage 4 verdict" not in r.stdout
    assert not (run / "04_walks" / "_stage4.json").exists() and not (run / "04_walks" / f"{PID}.md").exists()
    m = merge(a, b, pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4"], "W20", kind="x")])
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    r = cli("walks", "--check", PID, "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert "Stage 4 verdict: kept." in r.stdout
    assert "  pair 1 (rank 1): valid, lane business" in r.stdout
    assert "  pair 2 (rank 2): invalid: entry: only 2 distinct entry wall(s); needs at least 3" in r.stdout
    assert not (run / "04_walks" / "_stage4.json").exists()
    report = stage45.walks(run, check=PID)
    assert report["present"] == {"a": True, "b": True, "merged": True} and report["errors"] == [] and report["status"] == "kept"
    assert report["derived"]["walls_both"] == ["W2", "W4", "W9", "W20"] and report["pair_checks"][1]["failed"] == ["entry", "adjacency", "lane"]
    # the full run needs every file of every kept pain
    r = cli("walks", "--run", DATE)
    assert r.returncode == 2
    assert f"Walk files are missing. Two walkers (a, b) and a comparator write them per pain: {ROOM}--fees: missing {ROOM}--fees.a.json, {ROOM}--fees.b.json, {ROOM}--fees.json in" in r.stderr
    r = cli("walks", "--run", DATE, "--dry-run")
    assert r.returncode == 0, r.stderr
    s4 = stage4(run)
    assert s4["kept"] == [PID] and any(n.startswith(f"dry run: skipped {ROOM}--fees: missing") for n in s4["notes"])
    (common.listen_dir(run) / "pains.json").unlink()
    r = cli("walks", "--run", DATE)
    assert r.returncode == 2 and "pains.json is missing. Run `funnel pains` first." in r.stderr
    common.write_json(common.listen_dir(run) / "pains.json", {"pains": []})
    # no kept pain: an empty _stage4.json and exit 0, so a run in which Stage 3 dropped everything still finishes
    r = cli("walks", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert "nothing to walk" in r.stdout and "Walks: 0 kept pain(s) in, 0 walked, 0 kept, 0 killed" in r.stdout
    s4 = stage4(run)
    assert s4["counts"] == {"in": 0, "walked": 0, "kept": 0, "killed": 0, "lane_hint_trade": 0} and s4["pains"] == [] and s4["kept"] == []
    assert any("No kept pains" in n for n in s4["notes"])


def test_walks_rerun_is_byte_identical(froot, run, cli):
    ids = setup(run, pains=(PID, f"{ROOM}--fees"))[ROOM]
    write_walk_set(run, PID, ids, a_kw={"reached": True})
    write_walk_set(run, f"{ROOM}--fees", ids)
    r1 = cli("walks", "--run", DATE)
    assert r1.returncode == 0, r1.stderr
    names = ["_stage4.json", f"{PID}.md", f"{ROOM}--fees.md"]
    first = {n: (run / "04_walks" / n).read_bytes() for n in names}
    gy1 = graveyard(froot)
    r2 = cli("walks", "--run", DATE)
    assert r2.returncode == 0 and r2.stdout == r1.stdout
    assert {n: (run / "04_walks" / n).read_bytes() for n in names} == first and graveyard(froot) == gy1
    assert gy1.count(f"pain:{PID}") == 1 and f"pain:{ROOM}--fees" not in gy1
    raw = first["_stage4.json"].decode("utf-8")
    assert raw == json.dumps(json.loads(raw), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    assert [e["pain_id"] for e in json.loads(raw)["pains"]] == [PID, f"{ROOM}--fees"]  # Stage 3 rank order


# =========================================================================== Stage 5: pairs
def std_ctx(**over):
    ctx = {"walls_both": ["W2", "W4", "W9", "W20"], "forward": {"W2": "melts", "W4": "melts", "W9": "melts", "W20": "persists", "W13": "melts"},
           "path_walls": {"W2": 1, "W4": 2, "W9": 3, "W20": 4, "W13": 7, "W15": 8}, "lane_hint": None, "room": ROOM,
           "depth": {"depth_ledger_id": "d1", "strength": "strong"}}
    ctx.update(over)
    return ctx


def evaluate(p, ctx=None, rules=None):
    import datetime
    return stage45.evaluate_pair(p, 1, ctx or std_ctx(), rules or common.load_kill_rules(), stage45.ledger_supply(),
                                 common.load_walls(), datetime.date(2026, 9, 26))


def test_pair_checks_entry_walls_both_adjacency_hold_persistence(froot):
    ok = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"))
    assert ok["valid"] is True and ok["lane"] == "business" and ok["failed"] == []
    assert ok["checks"]["entry"]["reason"] == "3 machine walls: W2 Diagnosis, W4 Context, W9 Effort"
    assert ok["checks"]["walls_both"]["reason"] == "every entry wall and the hold wall sit in walls_both"
    assert ok["checks"]["adjacency"]["reason"] == "entry walls first appear on steps 1–3 (span 3, allowed 4); hold W20 on step 4 (distance 1 from the entry span, allowed 1)"
    assert ok["checks"]["hold"]["reason"] == "W20 Accountability is a human wall the ledger does not rule out"
    assert ok["checks"]["persistence"]["reason"] == "W20 persists in the merged 12-month walk (both walkers agree)"
    assert ok["checks"]["lane"] == {"pass": True, "lane": "business", "reason": "business: the founder can be W20 Accountability (c1: Accountability: coaching and cohorts)"}
    # entry: too few, duplicates, human walls
    few = evaluate(pair(1, ["W2", "W4", "W4"], "W20", supply="c1"), std_ctx(path_walls={"W2": 1, "W4": 2, "W9": 3, "W20": 3}))
    assert few["failed"] == ["entry"] and few["checks"]["entry"]["reason"] == "only 2 distinct entry wall(s); needs at least 3"
    assert few["entry_walls"] == ["W2", "W4"] and few["lane"] is None and few["valid"] is False
    hum = evaluate(pair(1, ["W2", "W4", "W20"], "W20", supply="c1"))
    assert hum["checks"]["entry"] == {"pass": False, "reason": "W20 not machine walls (entry walls are W1–W16)"}
    hum = evaluate(pair(1, ["W2", "W4", "W9", "W25"], "W20", supply="c1"))
    assert hum["checks"]["entry"] == {"pass": False, "reason": "W25 not machine walls (entry walls are W1–W16)"}
    # walls_both and adjacency
    wb = evaluate(pair(1, ["W2", "W4", "W13"], "W20", supply="c1"))
    assert wb["checks"]["walls_both"] == {"pass": False, "reason": "entry wall W13 is not in walls_both"}
    assert wb["checks"]["adjacency"]["reason"] == "entry walls are spread over 7 steps (steps 1–7); allowed 4 (3 walls + slack 1)"
    assert wb["failed"] == ["walls_both", "adjacency", "lane"]
    off = evaluate(pair(1, ["W2", "W4", "W16"], "W20", supply="c1"), std_ctx(walls_both=["W2", "W4", "W16", "W20"]))
    assert off["checks"]["adjacency"]["pass"] is False and off["checks"]["adjacency"]["reason"].startswith("W16 not on the merged path")
    far = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), std_ctx(path_walls={"W2": 1, "W4": 2, "W9": 3, "W20": 6}))
    assert far["checks"]["adjacency"]["reason"].endswith("hold wall W20 is 3 step(s) away from the entry span (steps 1–3); allowed 1")
    assert far["failed"] == ["adjacency", "lane"] and far["lane_reasons"]["business"] == "no valid hold wall"
    Helpers.set_rule(froot, "stage5", "adjacency_slack_steps", 3)
    assert evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), std_ctx(path_walls={"W2": 1, "W4": 2, "W9": 3, "W20": 6}))["valid"] is True
    Helpers.set_rule(froot, "stage5", "adjacency_slack_steps", 1)
    Helpers.set_rule(froot, "stage5", "min_entry_walls", 2)
    assert evaluate(pair(1, ["W2", "W4"], "W20", supply="c1"), std_ctx(path_walls={"W2": 1, "W4": 2, "W9": 3, "W20": 3}))["valid"] is True
    Helpers.set_rule(froot, "stage5", "min_entry_walls", 3)
    # hold: human, not in the ledger's cannot list, in walls_both; persistence
    mach = evaluate(pair(1, ["W2", "W4", "W9"], "W13", kind="x"), std_ctx(walls_both=["W2", "W4", "W9", "W13"], path_walls={"W2": 1, "W4": 2, "W9": 3, "W13": 4}))
    assert mach["checks"]["hold"] == {"pass": False, "reason": "W13 is a machine wall; the hold must be a human wall (W17–W29)"}
    cannot = evaluate(pair(1, ["W2", "W4", "W9"], "W27", kind="a priest"), std_ctx(walls_both=["W2", "W4", "W9", "W27"], forward={"W27": "persists"}, path_walls={"W2": 1, "W4": 2, "W9": 3, "W27": 4}))
    assert cannot["checks"]["hold"] == {"pass": False, "reason": "W27 Ritual is in the ledger's cannot list; it can never be a hold"}
    assert cannot["failed"] == ["hold", "lane"] and cannot["lane_reasons"]["partner"] == "no valid hold wall"
    not_both = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), std_ctx(walls_both=["W2", "W4", "W9"]))
    assert not_both["checks"]["walls_both"] == {"pass": False, "reason": "hold wall W20 is not in walls_both"} and not_both["failed"] == ["walls_both", "lane"]
    melts = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), std_ctx(forward=dict(std_ctx()["forward"], W20="melts")))
    assert melts["checks"]["persistence"] == {"pass": False, "reason": "W20 melts in the merged 12-month walk; a hold must persist"}
    assert melts["failed"] == ["persistence", "lane"]
    no_verdict = evaluate(pair(1, ["W2", "W4", "W9"], "W25", supply="c4"), std_ctx(walls_both=["W2", "W4", "W9", "W25"], path_walls={"W2": 1, "W4": 2, "W9": 3, "W25": 4}))
    assert no_verdict["checks"]["persistence"]["reason"] == "W25 has no 12-month verdict in the merged walk (not on the path)"


def test_lanes_business_partner_trade_and_lane_hint(froot):
    # business: can_be with the same wall; c2 Judgment only for strong depth
    assert evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1"))["lane"] == "business"
    wrong = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c4"))
    assert wrong["lane"] is None and wrong["lane_reasons"]["business"] == "hold_supply_id c4 is for W25, not W20"
    none = evaluate(pair(1, ["W2", "W4", "W9"], "W20"))
    assert none["lane_reasons"] == {"business": "no hold_supply_id (the ledger id under which the founder can be this wall)",
                                    "partner": "no partner_id or partner_kind",
                                    "trade": "this alternative names a hold wall (W20); a trade has none (set hold_wall to null and drop the supply and partner ids to draft a trade)"}
    assert none["checks"]["lane"] == {"pass": False, "lane": None, "reason": "business: " + none["lane_reasons"]["business"] + "; partner: no partner_id or partner_kind; trade: " + none["lane_reasons"]["trade"]}
    jctx = std_ctx(walls_both=["W2", "W5", "W7", "W19"], forward={"W2": "melts", "W5": "melts", "W7": "melts", "W19": "persists"},
                   path_walls={"W2": 1, "W5": 2, "W7": 3, "W19": 4})
    strong = evaluate(pair(1, ["W2", "W5", "W7"], "W19", supply="c2"), jctx)
    assert strong["lane"] == "business" and "c2: Judgment: in the domains above where my depth is strong" in strong["lane_reasons"]["business"]
    moderate = evaluate(pair(1, ["W2", "W5", "W7"], "W19", supply="c2"), dict(jctx, room=ROOM2, depth={"depth_ledger_id": "d6", "strength": "moderate"}))
    assert moderate["lane"] is None
    assert moderate["lane_reasons"]["business"] == "c2 (Judgment: in the domains above where my depth is strong) needs strong depth; this room's Stage 2 depth is d6 (moderate)"
    unknown = evaluate(pair(1, ["W2", "W5", "W7"], "W19", supply="c2"), dict(jctx, depth={"depth_ledger_id": None, "strength": None}))
    assert "this room's Stage 2 depth is none (unknown)" in unknown["lane_reasons"]["business"]
    both = evaluate(pair(1, ["W2", "W5", "W7"], "W19", supply="c2", kind="a senior banker"), dict(jctx, depth={"depth_ledger_id": "d6", "strength": "moderate"}))
    assert both["lane"] == "partner" and both["lane_reasons"]["partner"] == "a partner (a senior banker) supplies W19 Judgment"
    # partner: can_rent with the same wall, or a partner kind for a wall not in cannot
    lctx = std_ctx(walls_both=["W2", "W6", "W7", "W18"], forward={"W2": "melts", "W6": "melts", "W7": "melts", "W18": "persists"},
                   path_walls={"W2": 1, "W6": 2, "W7": 3, "W18": 4})
    rent = evaluate(pair(1, ["W2", "W6", "W7"], "W18", partner="r1"), lctx)
    assert rent["lane"] == "partner" and rent["lane_reasons"]["partner"] == "a partner can supply W18 License (r1: License (accountants, lawyers, registered advisers, doctors))"
    assert rent["lane_reasons"]["business"] == "no hold_supply_id (the ledger id under which the founder can be this wall)"
    mismatch = evaluate(pair(1, ["W2", "W6", "W7"], "W18", partner="r2"), lctx)
    assert mismatch["lane"] is None and mismatch["lane_reasons"]["partner"] == "partner_id r2 is for W29, not W18"
    kind = evaluate(pair(1, ["W2", "W6", "W7"], "W18", kind="a chartered accountant"), lctx)
    assert kind["lane"] == "partner"
    blank = evaluate(pair(1, ["W2", "W6", "W7"], "W18", kind="   "), lctx)
    assert blank["lane"] is None and blank["lane_reasons"]["partner"] == "no partner_id or partner_kind"
    # a wall the ledger does not mention can be rented from a named partner but never supplied by the founder
    nctx = std_ctx(walls_both=["W2", "W4", "W9", "W24"], forward={"W2": "melts", "W4": "melts", "W9": "melts", "W24": "persists"},
                   path_walls={"W2": 1, "W4": 2, "W9": 3, "W24": 4})
    assert evaluate(pair(1, ["W2", "W4", "W9"], "W24", kind="an alumni network"), nctx)["lane"] == "partner"
    assert evaluate(pair(1, ["W2", "W4", "W9"], "W24", supply="c1"), nctx)["lane_reasons"]["business"] == "hold_supply_id c1 is for W20, not W24"
    # trade: no hold wall, and every trade condition
    tr = evaluate(pair(1, ["W2", "W4", "W9"], trade=trade()))
    assert tr["lane"] == "trade" and tr["valid"] is True and tr["failed"] == []
    assert tr["checks"]["hold"] == {"pass": None, "reason": "no hold wall (a trade needs none)"} and tr["checks"]["persistence"]["pass"] is None
    assert tr["lane_reasons"] == {"business": "no hold wall (a business needs one human wall that holds)",
                                  "partner": "no hold wall (a partner rents one human wall that holds)",
                                  "trade": "no holding wall; build 1 week(s), payment upfront, no subscription, exit 2027-03-31"}
    assert evaluate(pair(1, ["W2", "W4", "W9"], trade=trade(weeks=2)))["lane"] == "trade"
    bad = evaluate(pair(1, ["W2", "W4", "W9"], trade=trade(weeks=3, upfront=False, sub=True, exit=None)))
    assert bad["lane"] is None and bad["failed"] == ["lane"]
    assert bad["lane_reasons"]["trade"] == "build takes 3 weeks; allowed 2; payment is not upfront; a subscription is not allowed in a trade; no exit_date written from day one"
    past = evaluate(pair(1, ["W2", "W4", "W9"], trade=trade(exit="2026-09-26")))
    assert past["lane_reasons"]["trade"] == "exit_date 2026-09-26 is not after the run date 2026-09-26"
    assert evaluate(pair(1, ["W2", "W4", "W9"], trade=trade(exit="2026-09-27")))["lane"] == "trade"
    assert evaluate(pair(1, ["W2", "W4", "W9"]))["lane_reasons"]["trade"] == "no trade object (build_weeks, payment_upfront, subscription, exit_date)"
    Helpers.set_rule(froot, "stage5", "trade", {"max_build_weeks": 4, "payment_upfront": False, "subscriptions_allowed": True, "exit_date_required": False})
    loose = evaluate(pair(1, ["W2", "W4", "W9"], trade=trade(weeks=3, upfront=False, sub=True, exit=None)))
    assert loose["lane"] == "trade" and loose["lane_reasons"]["trade"].endswith("exit not required")
    Helpers.set_rule(froot, "stage5", "trade", {"max_build_weeks": 2, "payment_upfront": True, "subscriptions_allowed": False, "exit_date_required": True})
    # a lane_hint trade pain can only be a trade
    hinted = evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1", kind="a coach"), std_ctx(lane_hint="trade"))
    assert hinted["lane"] is None
    assert hinted["lane_reasons"]["business"] == "the merged walk says every wall melts; only a trade is allowed (lane_hint: trade)"
    assert hinted["lane_reasons"]["partner"] == hinted["lane_reasons"]["business"]
    assert evaluate(pair(1, ["W2", "W4", "W9"], trade=trade()), std_ctx(lane_hint="trade"))["lane"] == "trade"
    # lane preference from the kill rules
    Helpers.set_rule(froot, "stage5", "lane_preference", ["partner", "business", "trade"])
    assert evaluate(pair(1, ["W2", "W4", "W9"], "W20", supply="c1", kind="a coach"))["lane"] == "partner"


def test_choose_alternative_by_lane_order_then_rank():
    alts = [dict(index=1, valid=True, lane="partner", rank=1), dict(index=2, valid=True, lane="trade", rank=2),
            dict(index=3, valid=True, lane="business", rank=3), dict(index=4, valid=False, lane=None, rank=1),
            dict(index=5, valid=True, lane="business", rank=2)]
    assert stage45.choose_alternative(alts, ["business", "partner", "trade"])["index"] == 5
    assert stage45.choose_alternative(alts, ["trade", "business", "partner"])["index"] == 2
    assert stage45.choose_alternative(alts[:2], ["business", "partner", "trade"])["index"] == 1
    assert stage45.choose_alternative([alts[3]], ["business", "partner", "trade"]) is None
    assert stage45.choose_alternative([], ["business"]) is None


def test_pairs_end_to_end_every_lane_and_the_kill(froot, run, cli):
    pains = {
        "biz": f"{ROOM}--business-one", "judge": f"{ROOM}--judgment-strong", "judge2": f"{ROOM2}--judgment-moderate",
        "rent": f"{ROOM}--rent-a-license", "ritual": f"{ROOM}--cannot-be-a-hold", "melt": f"{ROOM}--everything-melts",
        "dead": f"{ROOM}--no-valid-pair", "order": f"{ROOM}--rank-decides",
    }
    ids = setup(run, pains=tuple(pains.values()))
    a1, b1 = ids[ROOM], ids[ROOM2]
    write_walk_set(run, pains["biz"], a1, pairs=[
        pair(1, ["W2", "W4", "W9"], "W20", kind="a coach"), pair(2, ["W2", "W4", "W9"], "W20", supply="c1"),
        pair(3, ["W2", "W4", "W9"], trade=trade())])
    jsteps, jfwd = [["W2"], ["W5"], ["W7"], ["W19"]], {"W2": "melts", "W5": "melts", "W7": "melts", "W19": "persists"}
    for key, room_ids in (("judge", a1), ("judge2", b1)):
        write_walk_set(run, pains[key], room_ids, a=walk(pains[key], "a", jsteps, jfwd, persona_ids=room_ids),
                       b=walk(pains[key], "b", jsteps, jfwd, persona_ids=room_ids),
                       pairs=[pair(1, ["W2", "W5", "W7"], "W19", supply="c2"), pair(2, ["W2", "W5", "W7"], "W19", kind="a senior banker")])
    lsteps, lfwd = [["W2"], ["W6"], ["W7"], ["W18"]], {"W2": "melts", "W6": "melts", "W7": "melts", "W18": "persists"}
    write_walk_set(run, pains["rent"], a1, a=walk(pains["rent"], "a", lsteps, lfwd, persona_ids=a1), b=walk(pains["rent"], "b", lsteps, lfwd, persona_ids=a1),
                   pairs=[pair(1, ["W2", "W6", "W7"], "W18", partner="r2"), pair(2, ["W2", "W6", "W7"], "W18", partner="r1")])
    rsteps, rfwd = [["W2"], ["W5"], ["W7"], ["W27"]], {"W2": "melts", "W5": "melts", "W7": "melts", "W27": "persists"}
    write_walk_set(run, pains["ritual"], a1, a=walk(pains["ritual"], "a", rsteps, rfwd, persona_ids=a1), b=walk(pains["ritual"], "b", rsteps, rfwd, persona_ids=a1),
                   pairs=[pair(1, ["W2", "W5", "W7"], "W27", kind="a priest"), pair(2, ["W2", "W5", "W7"], trade=trade())])
    mfwd = dict(STD_FWD, W20="melts")
    write_walk_set(run, pains["melt"], a1, a=walk(pains["melt"], "a", STD_STEPS, mfwd, persona_ids=a1), b=walk(pains["melt"], "b", STD_STEPS, mfwd, persona_ids=a1),
                   pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"], trade=trade(weeks=2))])
    write_walk_set(run, pains["dead"], a1, pairs=[
        pair(1, ["W2", "W4"], "W20", supply="c1"),
        pair(2, ["W2", "W4", "W9"], trade=trade(weeks=3, upfront=False, sub=True, exit=None)),
        pair(3, ["W2", "W4", "W9", "W13"], "W20", supply="c1")])
    write_walk_set(run, pains["order"], a1, pairs=[pair(2, ["W2", "W4", "W9"], "W20", supply="c1"), pair(1, ["W4", "W9", "W2"], "W20", supply="c1")])
    r = cli("walks", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert stage4(run)["lane_hint_trade"] == [pains["melt"]]
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 0, r.stderr
    data = pairs_json(run)
    by = {x["pain_id"]: x for x in data["pains"]}
    assert data["counts"] == {"in": 8, "kept": 7, "killed": 1, "by_lane": {"business": 3, "partner": 2, "trade": 2}}
    assert data["killed"] == [pains["dead"]] and data["lane_preference"] == ["business", "partner", "trade"]
    assert [x["pain_id"] for x in data["pains"]] == list(pains.values())  # Stage 3 rank order
    # business beats partner and trade whatever the comparator's rank
    biz = by[pains["biz"]]
    assert biz["status"] == "kept" and biz["lane"] == "business" and biz["kept_index"] == 2
    assert [a["lane"] for a in biz["alternatives"]] == ["partner", "business", "trade"] and all(a["valid"] for a in biz["alternatives"])
    assert biz["kept_reason"] == "lane business (lane order business > partner > trade); alternative 1 is partner rank 1, alternative 3 is trade rank 3; kept alternative 2 (rank 2)"
    assert biz["kept"] == dict(biz["alternatives"][1]["checks"] and {k: biz["alternatives"][1][k] for k in stage45.PAIR_FIELDS}, lane="business", index=2)
    assert biz["kept"]["entry_walls"] == ["W2", "W4", "W9"] and biz["kept"]["hold_wall"] == "W20" and biz["kept"]["hold_supply_id"] == "c1"
    assert biz["walls_both"] == ["W2", "W4", "W9", "W20"] and biz["persisting_walls"] == ["W20"] and biz["depth"] == {"depth_ledger_id": "d1", "strength": "strong"}
    # c2 Judgment: business in a strong-depth room, partner in a moderate one
    assert by[pains["judge"]]["lane"] == "business" and by[pains["judge"]]["kept_index"] == 1
    j2 = by[pains["judge2"]]
    assert j2["lane"] == "partner" and j2["kept_index"] == 2 and j2["depth"] == {"depth_ledger_id": "d6", "strength": "moderate"}
    assert j2["alternatives"][0]["valid"] is False and "needs strong depth; this room's Stage 2 depth is d6 (moderate)" in j2["alternatives"][0]["checks"]["lane"]["reason"]
    # partner via can_rent (the wall must match)
    rent = by[pains["rent"]]
    assert rent["lane"] == "partner" and rent["kept_index"] == 2 and rent["alternatives"][0]["valid"] is False
    assert rent["kept_reason"] == "lane partner (lane order business > partner > trade); the only valid alternative (rank 2)"
    # a cannot wall is never a hold; the trade alternative is kept
    rit = by[pains["ritual"]]
    assert rit["lane"] == "trade" and rit["kept_index"] == 2 and rit["alternatives"][0]["failed"] == ["hold", "lane"]
    # lane_hint trade: only a trade
    melt = by[pains["melt"]]
    assert melt["lane"] == "trade" and melt["lane_hint"] == "trade" and melt["kept_index"] == 2 and melt["persisting_walls"] == []
    assert melt["alternatives"][0]["failed"] == ["persistence", "lane"]
    # the kill lists each alternative's failed checks
    dead = by[pains["dead"]]
    assert dead["status"] == "killed" and dead["lane"] is None and dead["kept"] is None and dead["kept_index"] is None
    kr = dead["kill_reason"]
    assert kr.startswith("no pair, no clean trade, no plausible partner: alternative 1 (rank 1): entry: only 2 distinct entry wall(s); needs at least 3; adjacency: hold wall W20 is 2 step(s) away from the entry span (steps 1–2); allowed 1; lane: business: no valid hold wall; partner: no valid hold wall; trade: this alternative names a hold wall (W20)")
    assert "/ alternative 2 (rank 2): lane: business: no hold wall (a business needs one human wall that holds); partner: no hold wall (a partner rents one human wall that holds); trade: build takes 3 weeks; allowed 2; payment is not upfront; a subscription is not allowed in a trade; no exit_date written from day one" in kr
    assert "/ alternative 3 (rank 3): walls_both: entry wall W13 is not in walls_both; adjacency: W13 not on the merged path; lane:" in kr
    gy = graveyard(froot)
    assert f"- {DATE} | stage 5 | pain:{pains['dead']} | no pair, no clean trade, no plausible partner: alternative 1 (rank 1): entry: only 2 distinct" in gy
    assert gy.count("stage 5 |") == 1
    # ties in lane go to the comparator's rank
    order = by[pains["order"]]
    assert order["kept_index"] == 2 and order["kept"]["rank"] == 1 and order["kept"]["entry_walls"] == ["W4", "W9", "W2"]
    # CLI output
    assert "Pairs: 8 pain(s) in, 7 kept, 1 killed. By lane: business 3, partner 2, trade 2." in r.stdout
    assert f"kept: {pains['biz']}: lane business, alternative 2 (rank 2): entry W2, W4, W9, hold W20" in r.stdout
    assert f"kept: {pains['ritual']}: lane trade, alternative 2 (rank 2): entry W2, W5, W7, hold none" in r.stdout
    assert f"killed: {pains['dead']}: no pair, no clean trade, no plausible partner" in r.stdout
    # the markdown shows every alternative, its checks, and why one was kept
    md = (run / "05_pairs.md").read_text(encoding="utf-8")
    assert md.startswith("# Stage 5: pairs\n\nRun: 2026-09-26.\n8 pain(s) came out of the walk. 7 kept, 1 killed. By lane: business 3, partner 2, trade 2.")
    assert "- **business**: a real pair exists and the founder can credibly supply the holding human wall." in md
    assert "- **entry**: at least min_entry_walls distinct machine walls (W1–W16)" in md
    assert "Rules: min_entry_walls 3, adjacency_slack_steps 1, trade: max_build_weeks 2, payment_upfront True, subscriptions_allowed False, exit_date_required True." in md
    assert "## Kept pains (7)" in md and f"| {pains['biz']} | business | W2, W4, W9 | W20 | c1 | 2 (rank 2) |" in md
    assert f"| {pains['rent']} | partner | W2, W6, W7 | W18 | r1 | 2 (rank 2) |" in md
    assert f"| {pains['ritual']} | trade | W2, W5, W7 | none | trade | 2 (rank 2) |" in md
    assert f"## {pains['biz']} (kept, lane business)" in md and "Kept alternative 2: lane business (lane order business > partner > trade)" in md
    assert "| Alt | Rank | Entry | Hold | Supply / partner / trade | entry | walls_both | adjacency | hold | persistence | lane | Valid | Lane |" in md
    assert "| 1 | 1 | W2, W4, W9 | W20 | a coach | pass | pass | pass | pass | pass | pass | yes | partner |" in md
    assert "| 3 | 3 | W2, W4, W9 | none | trade: 1 wk, upfront yes, subscription no, exit 2027-03-31 | pass | pass | pass | n/a | n/a | pass | yes | trade |" in md
    assert f"## {pains['dead']} (killed)" in md and "Killed: no pair, no clean trade, no plausible partner: alternative 1 (rank 1): entry: only 2" in md
    assert "| 1 | 1 | W2, W4 | W20 | c1 | FAIL | pass | FAIL | pass | pass | FAIL | no | - |" in md
    assert "### Alternative 1 (rank 1): For the room, a promise in a month, because W2, W4, W9, held by W20." in md
    assert "- lane: pass. business: the founder can be W20 Accountability (c1: Accountability: coaching and cohorts)" in md
    assert "- crux: will they pay before the exam" in md and "- credibility question: Will this room accept the founder as a coach?" in md
    assert f"## {pains['melt']} (kept, lane trade)" in md and "Lane hint: trade (every wall melts)." in md
    events = common.read_jsonl(run / "runlog.jsonl")
    assert any(e["kind"] == "count" and e["command"] == "pairs" and e["killed"] == 1 and e["by_lane"]["business"] == 3 for e in events)


def test_pairs_alternative_count_shape_errors_and_missing_inputs(run, cli):
    ids = setup(run)[ROOM]
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 2 and "_stage4.json is missing. Run `funnel walks` first." in r.stderr
    write_walk_set(run, PID, ids, pairs=[pair(1, ["W2", "W4", "W9"], "W20", supply="c1")])
    assert cli("walks", "--run", DATE).returncode == 0
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 1 and f"{where(PID)}: 1 alternative pair(s); the comparator drafts 2 to 3 (alternative_pairs_min/max)." in r.stderr
    assert not (run / "05_pairs.json").exists()
    r = cli("pairs", "--run", DATE, "--dry-run")
    assert r.returncode == 0, r.stderr
    data = pairs_json(run)
    assert data["kept"] == [PID] and data["warnings"] == [f"{where(PID)}: 1 alternative pair(s); the comparator drafts 2 to 3 (alternative_pairs_min/max)."]
    assert "warning: " in r.stdout and "## Warnings" in (run / "05_pairs.md").read_text(encoding="utf-8")
    write_walk_set(run, PID, ids, pairs=[pair(i, ["W2", "W4", "W9"], "W20", supply="c1") for i in range(1, 5)])
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 1 and "4 alternative pair(s); the comparator drafts 2 to 3" in r.stderr
    # shape errors found after the walk stage (the comparator edited the file) are listed
    a, b, m = write_walk_set(run, PID, ids)
    m["pairs"][0]["hold_supply_id"] = "c9"
    m["pairs"][1]["rank"] = 1
    common.write_json(stage45.walk_paths(run, PID)["merged"], m)
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 1 and "pair 1: 'hold_supply_id' 'c9' is not a ledger can_be id" in r.stderr and "pair 2: rank 1 is also used by pair 1" in r.stderr
    stage45.walk_paths(run, PID)["merged"].unlink()
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 2 and f"04_walks/{PID}.json is missing. The comparator writes the merged walk with its pairs." in r.stderr
    write_walk_set(run, PID, ids)
    (run / "02_mask.json").unlink()
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 2 and "02_mask.json is missing. Run `funnel mask` first" in r.stderr
    common.write_json(run / "04_walks" / "_stage4.json", {"pains": [{"pain_id": PID, "status": "killed"}]})
    common.write_json(run / "02_mask.json", {"rooms": []})
    # no Stage 4 survivor: an empty 05_pairs.json and exit 0, so `numbers` and `shortlist` can still run
    r = cli("pairs", "--run", DATE)
    assert r.returncode == 0, r.stderr
    assert "No Stage 4 survivors" in r.stdout and "Pairs: 0 pain(s) in, 0 kept, 0 killed." in r.stdout
    data = pairs_json(run)
    assert data["pains"] == [] and data["kept"] == [] and data["killed"] == [] and data["counts"]["in"] == 0
    assert any("nothing to pair" in n for n in data["notes"]) and "## Notes" in (run / "05_pairs.md").read_text(encoding="utf-8")


def test_pairs_rerun_is_byte_identical(froot, run, cli):
    ids = setup(run, pains=(PID, f"{ROOM}--fees"))[ROOM]
    write_walk_set(run, PID, ids)
    write_walk_set(run, f"{ROOM}--fees", ids, pairs=[pair(1, ["W2", "W4"], "W20", supply="c1"), pair(2, ["W2", "W4", "W9"])])
    assert cli("walks", "--run", DATE).returncode == 0
    r1 = cli("pairs", "--run", DATE)
    assert r1.returncode == 0, r1.stderr
    first = {n: (run / n).read_bytes() for n in ("05_pairs.json", "05_pairs.md")}
    gy1 = graveyard(froot)
    assert gy1.count(f"pain:{ROOM}--fees") == 1 and f"pain:{PID}" not in gy1
    r2 = cli("pairs", "--run", DATE)
    assert r2.returncode == 0 and r2.stdout == r1.stdout
    assert {n: (run / n).read_bytes() for n in first} == first and graveyard(froot) == gy1
    raw = first["05_pairs.json"].decode("utf-8")
    assert raw == json.dumps(json.loads(raw), sort_keys=True, indent=2, ensure_ascii=False) + "\n"
    data = json.loads(raw)
    assert data["kept"] == [PID] and data["killed"] == [f"{ROOM}--fees"]
    assert data["check_meaning"]["persistence"].startswith("the hold wall persists") and set(data["lane_meaning"]) == {"business", "partner", "trade"}


def test_ledger_supply_and_depth_lookup(run):
    s = stage45.ledger_supply()
    assert set(s["can_be"]) == {"c1", "c2", "c3", "c4"} and s["can_be"]["c2"]["wall"] == "W19" and s["can_be"]["c2"]["depth_strength_required"] == "strong"
    assert set(s["can_rent"]) == {"r1", "r2", "r3"} and s["can_rent"]["r3"]["wall"] == "W22"
    assert s["cannot"] == {"W27"} and s["not_mentioned"] == {"W21", "W23", "W24", "W26", "W28"}
    setup(run)
    d = stage45.depth_strength_by_room(run)
    assert d == {ROOM: {"depth_ledger_id": "d1", "strength": "strong"}, ROOM2: {"depth_ledger_id": "d6", "strength": "moderate"}}
    common.write_json(run / "02_mask.json", {"rooms": [{"slug": ROOM, "depth_ledger_id": None, "depth_strength": None}, {"slug": "bad slug"}]})
    assert stage45.depth_strength_by_room(run) == {ROOM: {"depth_ledger_id": None, "strength": None}}
    assert stage45.load_kept_pains(run)[0]["pain_id"] == PID and len(stage45.load_kept_pains(run)) == 1
