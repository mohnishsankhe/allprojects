"""Stage 4 (`walks`) and Stage 5 (`pairs`).

`walks`: for each pain kept by Stage 3, validate the two walker files
(`RUN/04_walks/<pain-id>.a.json`, `.b.json`) and the comparator's merged file
(`<pain-id>.json`), re-derive the conservative merge from the walker files and
reject a merged file that is less conservative (naming the exact field), kill a
pain whose merged outcome is reached today, hint `trade` when every wall melts,
render `04_walks/<pain-id>.md` and write `04_walks/_stage4.json`.
`walks --check PAIN_ID` validates one pain's files and writes nothing.

Conservative merge (config/kill_rules.yaml, stage4): the outcome is reached
today if EITHER walker says so; a wall persists only if BOTH say it persists
(unsure counts as `unsure_counts_as`, melts by default); a wall is in
`walls_both` only if both walkers put it, or a reconciled equivalent
(`agreement.reconciled_ids`), on the path.

`pairs`: for each Stage 4 survivor, validate every alternative in the merged
file's `pairs` mechanically (entry, walls_both, adjacency, hold, persistence,
lane), keep the strongest valid one (lane order from the kill rules, then the
comparator's rank), kill a pain with none, and write `05_pairs.json` and
`05_pairs.md` showing every alternative.

Public API
----------
    STAGE4, STAGE5 = 4, 5
    WALL_STATUSES = ("persists", "melts", "unsure")
    LANES = ("business", "partner", "trade")
    CHECKS = ("entry", "walls_both", "adjacency", "hold", "persistence", "lane")
    walks_dir(run) -> Path
    walk_paths(run, pain_id) -> dict           {"a", "b", "merged", "md"}
    load_kept_pains(run) -> list[dict]         kept pains of RUN/03_listen/pains.json, in rank order
    validate_walk(data, where, pain_id, walls, letter=None, stored=None) -> list[str]
    validate_merged(data, where, pain_id, walls, supply, stored=None) -> list[str]
    validate_pair_shape(pair, where, walls, supply) -> list[str]
    path_walls(walk) -> dict[wall -> first step]
    reconciliation_maps(reconciled_ids) -> (map_a, map_b)
    derive_merge(a, b, reconciled_ids, unsure_as="melts") -> dict
    check_conservative(merged, derived, where, unsure_as="melts") -> list[str]
    effective_forward(merged, derived, unsure_as="melts") -> dict[wall -> persists|melts]
    walks(run, check=None) -> dict             the _stage4.json content (or the check report)
    render_walk_md(entry, merged, a, b, walls, run) -> str
    ledger_supply(ledger=None) -> dict         {"can_be", "can_rent", "cannot", "not_mentioned"}
    depth_strength_by_room(run, ledger=None) -> dict[slug -> {"depth_ledger_id", "strength"}]
    evaluate_pair(pair, index, ctx, rules, supply, walls, run_date) -> dict
    choose_alternative(alternatives, lane_preference) -> dict | None
    pairs(run) -> dict                         the 05_pairs.json content
    render_pairs_md(result, run) -> str
    register(subparsers)                       adds `walks [--check PAIN_ID]` and `pairs`
"""
from __future__ import annotations

import datetime as _dt
from pathlib import Path

import common
import records

STAGE4 = 4
STAGE5 = 5
WALL_STATUSES = ("persists", "melts", "unsure")
LANES = ("business", "partner", "trade")
CHECKS = ("entry", "walls_both", "adjacency", "hold", "persistence", "lane")
CHECK_MEANING = {
    "entry": "at least min_entry_walls distinct machine walls (W1–W16): the walls the product gets in through",
    "walls_both": "every entry wall and the hold wall are in walls_both (both walkers put them on the path)",
    "adjacency": "the entry walls sit next to each other on the path (first-appearance steps span at most "
                 "len(entry) + adjacency_slack_steps) and the hold wall is within adjacency_slack_steps of that span",
    "hold": "one human wall (W17–W29) that is not in the ledger's cannot list (trade: not needed)",
    "persistence": "the hold wall persists in the merged 12-month walk (trade: not needed)",
    "lane": "business: the founder can be the hold (ledger can_be); partner: a partner can supply it (ledger can_rent "
            "or a named partner kind); trade: no hold wall named and every trade condition holds",
}
LANE_MEANING = {
    "business": "a real pair exists and the founder can credibly supply the holding human wall",
    "partner": "the pair needs a human wall the founder cannot supply; a partner rents it for a share of revenue",
    "trade": "machine walls only; allowed if the build is short, payment is upfront, there is no subscription and an exit "
             "date is written from day one",
}


# --------------------------------------------------------------------------- paths and inputs
def walks_dir(run) -> Path:
    return common.run_dir(run) / "04_walks"


def walk_paths(run, pain_id: str) -> dict:
    d = walks_dir(run)
    return {"a": d / f"{pain_id}.a.json", "b": d / f"{pain_id}.b.json", "merged": d / f"{pain_id}.json",
            "md": d / f"{pain_id}.md"}


def load_kept_pains(run) -> list:
    p = common.listen_dir(run) / "pains.json"
    common.require_file(p, "Run `funnel pains` first.")
    data = common.read_json(p)
    pains_list = data.get("pains") if isinstance(data, dict) else None
    if not isinstance(pains_list, list):
        raise common.ValidationErrors([f"{common.rel(p)}: needs a 'pains' list. Rerun `funnel pains`."])
    kept = [x for x in pains_list if isinstance(x, dict) and x.get("status") == "kept" and isinstance(x.get("pain_id"), str)]
    kept.sort(key=lambda x: (x.get("rank") if isinstance(x.get("rank"), int) else 10 ** 9, x["pain_id"]))
    return kept


def _read(path: Path):
    try:
        return common.read_json(path), None
    except ValueError as e:  # json.JSONDecodeError is a ValueError
        return None, f"{common.rel(path)}: not valid JSON ({e}). Fix the file."


def _wall_num(w: str) -> int:
    try:
        return int(str(w)[1:])
    except ValueError:
        return 10 ** 6


def _sorted_walls(ws) -> list:
    return sorted(set(ws), key=_wall_num)


def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


# --------------------------------------------------------------------------- walk validation
def validate_walk(data, where: str, pain_id: str, walls: dict, letter=None, stored=None) -> list:
    """Every problem with one walk file (walker a, walker b or the merged walk)."""
    if not isinstance(data, dict):
        return [f"{where}: must be an object (see config/formats.md, Stage 4)."]
    errors: list = []
    if data.get("pain_id") != pain_id:
        errors.append(f"{where}: 'pain_id' must be {pain_id} (got {data.get('pain_id')!r}).")
    if letter is not None and data.get("walker") != letter:
        errors.append(f"{where}: 'walker' must be {letter!r} (got {data.get('walker')!r}).")
    persona = data.get("persona")
    if not isinstance(persona, dict):
        errors.append(f"{where}: 'persona' must be an object with description and record_ids.")
    else:
        if not _nonempty_str(persona.get("description")):
            errors.append(f"{where}: persona.description is missing or empty.")
        ids = persona.get("record_ids")
        if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids) or not ids:
            errors.append(f"{where}: persona.record_ids must be a non-empty list of record ids the persona is built from.")
        elif stored:
            for rid in ids:
                if rid not in stored:
                    errors.append(f"{where}: persona.record_ids: record {rid} is not stored for this room.")
    if not _nonempty_str(data.get("outcome")):
        errors.append(f"{where}: 'outcome' is missing or empty (the result they want, not the answer).")
    today = data.get("today")
    path: set = set()
    if not isinstance(today, list) or not today:
        errors.append(f"{where}: 'today' must be a non-empty list of steps.")
    else:
        for i, step in enumerate(today, 1):
            sw = f"{where}: today step {i}"
            if not isinstance(step, dict):
                errors.append(f"{sw}: must be an object with step, does, drops_out, why, walls, reasoning, confidence.")
                continue
            n = step.get("step")
            if not _is_int(n) or n != i:
                errors.append(f"{sw}: 'step' must be {i} (steps are numbered 1, 2, 3 in order; got {n!r}).")
            if not _nonempty_str(step.get("does")):
                errors.append(f"{sw}: 'does' is missing or empty.")
            if not isinstance(step.get("drops_out"), bool):
                errors.append(f"{sw}: 'drops_out' must be true or false.")
            if not isinstance(step.get("why"), str):
                errors.append(f"{sw}: 'why' must be text (use \"\" when nothing stops them).")
            ws = step.get("walls")
            if not isinstance(ws, list) or not all(isinstance(w, str) for w in ws):
                errors.append(f"{sw}: 'walls' must be a list of wall ids like W2 (use [] when no wall stops them).")
            else:
                for w in ws:
                    if w not in walls:
                        errors.append(f"{sw}: wall {w!r} is not in config/walls.md (W1–W29).")
                    else:
                        path.add(w)
            errors.extend(common.check_judgment(step, sw))
    ort = data.get("outcome_reached_today")
    if not isinstance(ort, dict):
        errors.append(f"{where}: 'outcome_reached_today' must be an object with value (true/false), reasoning, confidence.")
    else:
        if not isinstance(ort.get("value"), bool):
            errors.append(f"{where}: outcome_reached_today.value must be true or false.")
        errors.extend(common.check_judgment(ort, f"{where}: outcome_reached_today"))
    fwd = data.get("forward_12m")
    if not isinstance(fwd, list):
        errors.append(f"{where}: 'forward_12m' must be a list of {{wall, status, reasoning, confidence}}, one per wall on the path.")
    else:
        seen: set = set()
        for i, entry in enumerate(fwd, 1):
            fw = f"{where}: forward_12m {i}"
            if not isinstance(entry, dict):
                errors.append(f"{fw}: must be an object with wall, status, reasoning, confidence.")
                continue
            w = entry.get("wall")
            if w not in walls:
                errors.append(f"{fw}: wall {w!r} is not in config/walls.md (W1–W29).")
            elif w in seen:
                errors.append(f"{fw}: wall {w} appears twice in forward_12m. Keep one entry per wall.")
            else:
                seen.add(w)
                if w not in path:
                    errors.append(f"{fw}: wall {w} is not on the today path. forward_12m holds exactly the walls of today.")
            if entry.get("status") not in WALL_STATUSES:
                errors.append(f"{fw}: 'status' must be persists, melts or unsure (got {entry.get('status')!r}).")
            errors.extend(common.check_judgment(entry, fw))
        missing = _sorted_walls(path - seen)
        if missing:
            errors.append(f"{where}: forward_12m does not cover every wall in today: missing {', '.join(missing)}.")
    return errors


def validate_pair_shape(pair, where: str, walls: dict, supply: dict) -> list:
    if not isinstance(pair, dict):
        return [f"{where}: must be an object (see config/formats.md, Stage 5 PAIR)."]
    errors: list = []
    if not _is_int(pair.get("rank")) or pair.get("rank") < 1:
        errors.append(f"{where}: 'rank' must be a whole number from 1 (1 = the comparator's strongest).")
    ew = pair.get("entry_walls")
    if not isinstance(ew, list) or not all(isinstance(w, str) for w in ew):
        errors.append(f"{where}: 'entry_walls' must be a list of wall ids like W2.")
    else:
        for w in ew:
            if w not in walls:
                errors.append(f"{where}: entry wall {w!r} is not in config/walls.md (W1–W29).")
    hw = pair.get("hold_wall")
    if hw is not None and hw not in walls:
        errors.append(f"{where}: 'hold_wall' must be a wall id like W20, or null for a trade (got {hw!r}).")
    hs = pair.get("hold_supply_id")
    if hs is not None and hs not in supply["can_be"]:
        errors.append(f"{where}: 'hold_supply_id' {hs!r} is not a ledger can_be id "
                      f"({', '.join(sorted(supply['can_be'])) or 'none'}) or null.")
    pi = pair.get("partner_id")
    if pi is not None and pi not in supply["can_rent"]:
        errors.append(f"{where}: 'partner_id' {pi!r} is not a ledger can_rent id "
                      f"({', '.join(sorted(supply['can_rent'])) or 'none'}) or null.")
    pk = pair.get("partner_kind")
    if pk is not None and not isinstance(pk, str):
        errors.append(f"{where}: 'partner_kind' must be text or null.")
    tr = pair.get("trade")
    if tr is not None:
        if not isinstance(tr, dict):
            errors.append(f"{where}: 'trade' must be null or an object with build_weeks, payment_upfront, subscription, exit_date.")
        else:
            bw = tr.get("build_weeks")
            if not isinstance(bw, (int, float)) or isinstance(bw, bool) or bw < 0:
                errors.append(f"{where}: trade.build_weeks must be a number of weeks, 0 or more.")
            for flag in ("payment_upfront", "subscription"):
                if not isinstance(tr.get(flag), bool):
                    errors.append(f"{where}: trade.{flag} must be true or false.")
            ed = tr.get("exit_date")
            if ed is not None and not common.is_date(ed):
                errors.append(f"{where}: trade.exit_date must be a date YYYY-MM-DD or null (got {ed!r}).")
    for field in ("one_liner", "crux", "credibility_question"):
        if not _nonempty_str(pair.get(field)):
            errors.append(f"{where}: '{field}' is missing or empty.")
    errors.extend(common.check_judgment(pair, where))
    return errors


def validate_merged(data, where: str, pain_id: str, walls: dict, supply: dict, stored=None) -> list:
    """The merged walk: a walk plus agreement, disagreements and pairs (shape only; `pairs` applies the rules)."""
    errors = validate_walk(data, where, pain_id, walls, letter=None, stored=stored)
    if not isinstance(data, dict):
        return errors
    ag = data.get("agreement")
    if not isinstance(ag, dict):
        errors.append(f"{where}: 'agreement' must be an object with outcome, walls_both, walls_one, reconciled_ids.")
    else:
        if ag.get("outcome") not in ("agree", "disagree"):
            errors.append(f"{where}: agreement.outcome must be agree or disagree (got {ag.get('outcome')!r}).")
        for field in ("walls_both", "walls_one"):
            ws = ag.get(field)
            if not isinstance(ws, list) or not all(isinstance(w, str) for w in ws):
                errors.append(f"{where}: agreement.{field} must be a list of wall ids (use [] for none).")
            else:
                for w in ws:
                    if w not in walls:
                        errors.append(f"{where}: agreement.{field}: wall {w!r} is not in config/walls.md (W1–W29).")
        rec = ag.get("reconciled_ids")
        if rec is None:
            rec = []
        if not isinstance(rec, list):
            errors.append(f"{where}: agreement.reconciled_ids must be a list of {{a, b, as, reasoning}} (use [] for none).")
        else:
            for i, r in enumerate(rec, 1):
                rw = f"{where}: agreement.reconciled_ids {i}"
                if not isinstance(r, dict):
                    errors.append(f"{rw}: must be an object with a, b, as, reasoning.")
                    continue
                ok = True
                for field in ("a", "b", "as"):
                    if r.get(field) not in walls:
                        errors.append(f"{rw}: '{field}' must be a wall id (got {r.get(field)!r}).")
                        ok = False
                if ok:
                    if r["as"] not in (r["a"], r["b"]):
                        errors.append(f"{rw}: 'as' must be one of the two reconciled walls ({r['a']} or {r['b']}), not a third wall.")
                    if walls[r["a"]]["kind"] != walls[r["b"]]["kind"]:
                        errors.append(f"{rw}: {r['a']} and {r['b']} are not the same kind of wall (machine vs human); "
                                      f"they cannot be the same obstacle.")
                if not _nonempty_str(r.get("reasoning")):
                    errors.append(f"{rw}: 'reasoning' is missing (why these two ids name the same obstacle).")
    dis = data.get("disagreements")
    if dis is None:
        dis = []
    if not isinstance(dis, list) or not all(isinstance(x, str) for x in dis):
        errors.append(f"{where}: 'disagreements' must be a list of one-line texts (use [] for none).")
    pr = data.get("pairs")
    if pr is None:
        pr = []
    if not isinstance(pr, list):
        errors.append(f"{where}: 'pairs' must be a list of PAIR objects (use [] when the outcome is reached today).")
    else:
        ranks: dict = {}
        for i, pair in enumerate(pr, 1):
            pw = f"{where}: pair {i}"
            errors.extend(validate_pair_shape(pair, pw, walls, supply))
            if isinstance(pair, dict) and _is_int(pair.get("rank")):
                if pair["rank"] in ranks:
                    errors.append(f"{pw}: rank {pair['rank']} is also used by pair {ranks[pair['rank']]}. Ranks must differ.")
                ranks.setdefault(pair["rank"], i)
    return errors


# --------------------------------------------------------------------------- the conservative merge
def path_walls(walk: dict) -> dict:
    """wall -> the first step it appears on."""
    out: dict = {}
    for step in walk.get("today") or []:
        if not isinstance(step, dict):
            continue
        n = step.get("step")
        for w in step.get("walls") or []:
            if isinstance(w, str) and w not in out:
                out[w] = n
    return out


def reconciliation_maps(reconciled_ids) -> tuple:
    map_a: dict = {}
    map_b: dict = {}
    for r in reconciled_ids or []:
        if not isinstance(r, dict):
            continue
        a, b, as_ = r.get("a"), r.get("b"), r.get("as")
        if isinstance(a, str) and isinstance(as_, str):
            map_a[a] = as_
        if isinstance(b, str) and isinstance(as_, str):
            map_b[b] = as_
    return map_a, map_b


def _mapped_path(walk: dict, mapping: dict) -> dict:
    out: dict = {}
    for w, step in path_walls(walk).items():
        m = mapping.get(w, w)
        if m not in out or (isinstance(step, int) and isinstance(out[m], int) and step < out[m]):
            out[m] = step
    return out


def _norm_status(status, unsure_as: str) -> str:
    if status == "persists":
        return "persists"
    if status == "unsure":
        return "persists" if unsure_as == "persists" else "melts"
    return "melts"


def _raw_forward(walk: dict) -> dict:
    out: dict = {}
    for e in walk.get("forward_12m") or []:
        if isinstance(e, dict) and isinstance(e.get("wall"), str):
            out[e["wall"]] = e.get("status")
    return out


def _mapped_forward(walk: dict, mapping: dict, unsure_as: str) -> dict:
    """wall -> persists|melts after reconciliation (two walls merged into one persist only if both persist)."""
    out: dict = {}
    for w, status in _raw_forward(walk).items():
        m = mapping.get(w, w)
        s = _norm_status(status, unsure_as)
        if m in out:
            out[m] = "persists" if out[m] == "persists" and s == "persists" else "melts"
        else:
            out[m] = s
    return out


def _raw_status_for(w: str, raw: dict, mapping: dict):
    """The walker's own status for merged wall `w` (through its reconciled id when it used another id)."""
    if w in raw:
        return raw[w]
    for orig, as_ in mapping.items():
        if as_ == w and orig in raw:
            return raw[orig]
    return None


def derive_merge(a: dict, b: dict, reconciled_ids, unsure_as: str = "melts") -> dict:
    map_a, map_b = reconciliation_maps(reconciled_ids)
    pa, pb = _mapped_path(a, map_a), _mapped_path(b, map_b)
    both = _sorted_walls(set(pa) & set(pb))
    union = set(pa) | set(pb)
    one = _sorted_walls(union - set(both))
    fa, fb = _mapped_forward(a, map_a, unsure_as), _mapped_forward(b, map_b, unsure_as)
    raw_a, raw_b = _raw_forward(a), _raw_forward(b)
    forward: dict = {}
    for w in _sorted_walls(union):
        forward[w] = "persists" if fa.get(w) == "persists" and fb.get(w) == "persists" else "melts"
    ra = bool((a.get("outcome_reached_today") or {}).get("value"))
    rb = bool((b.get("outcome_reached_today") or {}).get("value"))
    disagreements: list = []
    if ra != rb:
        disagreements.append(f"outcome today: walker a says {'reached' if ra else 'not reached'}, walker b says "
                             f"{'reached' if rb else 'not reached'} (merge: reached if either says so).")
    only_a = _sorted_walls(set(pa) - set(pb))
    only_b = _sorted_walls(set(pb) - set(pa))
    if only_a:
        disagreements.append(f"walls only walker a put on the path: {', '.join(only_a)}.")
    if only_b:
        disagreements.append(f"walls only walker b put on the path: {', '.join(only_b)}.")
    for w in both:
        sa, sb = _raw_status_for(w, raw_a, map_a), _raw_status_for(w, raw_b, map_b)
        if sa != sb:
            disagreements.append(f"{w} in 12 months: walker a says {sa}, walker b says {sb} (merge: {forward[w]}).")
    return {"outcome_reached": ra or rb, "outcome_a": ra, "outcome_b": rb,
            "walls_both": both, "walls_one": one, "forward": forward,
            "path_a": pa, "path_b": pb, "forward_a": fa, "forward_b": fb,
            "raw_forward_a": raw_a, "raw_forward_b": raw_b, "map_a": map_a, "map_b": map_b,
            "disagreements": disagreements}


def check_conservative(merged: dict, derived: dict, where: str, unsure_as: str = "melts") -> list:
    """Reject a merged file that is less conservative than the derived merge. Names the exact field."""
    errors: list = []
    mv = bool((merged.get("outcome_reached_today") or {}).get("value"))
    if derived["outcome_reached"] and not mv:
        who = " and ".join(x for x, v in (("walker a", derived["outcome_a"]), ("walker b", derived["outcome_b"])) if v)
        errors.append(f"{where}: outcome_reached_today.value must be true: {who} say(s) the outcome is reached today, "
                      f"and the conservative merge takes either walker's yes.")
    ag = merged.get("agreement") or {}
    expected = "agree" if derived["outcome_a"] == derived["outcome_b"] else "disagree"
    if ag.get("outcome") != expected:
        errors.append(f"{where}: agreement.outcome must be {expected}: walker a says "
                      f"{'reached' if derived['outcome_a'] else 'not reached'}, walker b says "
                      f"{'reached' if derived['outcome_b'] else 'not reached'}.")
    both = set(derived["walls_both"])
    pa, pb = set(derived["path_a"]), set(derived["path_b"])
    for w in ag.get("walls_both") or []:
        if w in both:
            continue
        if w in pa and w not in pb:
            errors.append(f"{where}: agreement.walls_both holds {w}, but only walker a put it on the path. A wall counts "
                          f"only when both walkers put it, or a reconciled equivalent, on the path.")
        elif w in pb and w not in pa:
            errors.append(f"{where}: agreement.walls_both holds {w}, but only walker b put it on the path. A wall counts "
                          f"only when both walkers put it, or a reconciled equivalent, on the path.")
        else:
            errors.append(f"{where}: agreement.walls_both holds {w}, but neither walker put it on the path "
                          f"(after reconciliation).")
    got_one = set(w for w in (ag.get("walls_one") or []) if isinstance(w, str))
    exp_one = set(derived["walls_one"])
    if got_one != exp_one:
        errors.append(f"{where}: agreement.walls_one must list exactly the walls only one walker put on the path: "
                      f"{', '.join(derived['walls_one']) or 'none'} (got {', '.join(_sorted_walls(got_one)) or 'none'}).")
    mpath = path_walls(merged)
    for w in _sorted_walls(mpath):
        if w not in pa and w not in pb:
            hint = ""
            for src, mp in (("a", derived["map_a"]), ("b", derived["map_b"])):
                if w in mp:
                    hint = f" (walker {src}'s {w} was reconciled as {mp[w]}; use {mp[w]})"
                    break
            errors.append(f"{where}: today: wall {w} appears in the merged walk, but neither walker put it on the path{hint}.")
    for w in ag.get("walls_both") or []:
        if w in both and w not in mpath:
            errors.append(f"{where}: today: wall {w} is in agreement.walls_both but not on the merged today path. "
                          f"Put it on the step where both walkers met it.")
    for w, status in _raw_forward(merged).items():
        if _norm_status(status, unsure_as) == "persists" and derived["forward"].get(w) != "persists":
            sa = derived["raw_forward_a"].get(w)
            sb = derived["raw_forward_b"].get(w)
            errors.append(f"{where}: forward_12m: {w} is marked {status}, but walker a says {sa or 'nothing (not on its path)'} "
                          f"and walker b says {sb or 'nothing (not on its path)'}. A wall persists only if both say "
                          f"persists (unsure counts as {unsure_as}).")
    return errors


def effective_forward(merged: dict, derived: dict, unsure_as: str = "melts") -> dict:
    out: dict = {}
    for w, status in _raw_forward(merged).items():
        out[w] = "persists" if _norm_status(status, unsure_as) == "persists" and derived["forward"].get(w) == "persists" else "melts"
    return dict(sorted(out.items(), key=lambda kv: _wall_num(kv[0])))


# --------------------------------------------------------------------------- ledger supply
def ledger_supply(ledger=None) -> dict:
    ledger = ledger if ledger is not None else common.load_ledger()
    supply = ledger.get("supply") or {}

    def by_id(items):
        out = {}
        for it in items or []:
            if isinstance(it, dict) and it.get("id"):
                out[str(it["id"])] = it
        return out

    cannot = supply.get("cannot") or {}
    not_mentioned = supply.get("not_mentioned") or {}
    return {
        "can_be": by_id(supply.get("can_be")),
        "can_rent": by_id(supply.get("can_rent")),
        "cannot": set(str(w) for w in (cannot.get("walls") or [])),
        "not_mentioned": set(str(w) for w in (not_mentioned.get("walls") or [])),
    }


def depth_strength_by_room(run, ledger=None) -> dict:
    """slug -> {"depth_ledger_id", "strength"} from RUN/02_mask.json (strength looked up in the ledger)."""
    p = common.run_dir(run) / "02_mask.json"
    common.require_file(p, "Run `funnel mask` first (Stage 5 needs each room's depth strength for the c2 Judgment lane).")
    data = common.read_json(p)
    ledger = ledger if ledger is not None else common.load_ledger()
    depth = {}
    for d in ledger.get("depth") or []:
        if isinstance(d, dict) and d.get("id"):
            depth[str(d["id"])] = d
    out: dict = {}
    for v in (data.get("rooms") or []) if isinstance(data, dict) else []:
        if not isinstance(v, dict) or not common.is_slug(v.get("slug")):
            continue
        did = v.get("depth_ledger_id")
        strength = (depth.get(did) or {}).get("strength") if did else None
        if strength is None:
            strength = v.get("depth_strength")
        out[v["slug"]] = {"depth_ledger_id": did, "strength": strength}
    return out


# --------------------------------------------------------------------------- stage 4
def _walk_summary(walk: dict, mapping: dict, unsure_as: str) -> dict:
    return {"outcome_reached_today": bool((walk.get("outcome_reached_today") or {}).get("value")),
            "outcome_reasoning": (walk.get("outcome_reached_today") or {}).get("reasoning"),
            "steps": len(walk.get("today") or []),
            "path": _sorted_walls(_mapped_path(walk, mapping)),
            "forward": {w: s for w, s in sorted(_raw_forward(walk).items(), key=lambda kv: _wall_num(kv[0]))},
            "persona": (walk.get("persona") or {}).get("description")}


def _stage4_entry(pid: str, room: str, merged: dict, a: dict, b: dict, derived: dict, rules4: dict) -> dict:
    unsure_as = str(rules4.get("unsure_counts_as", "melts"))
    kill_rule = bool(rules4.get("kill_only_if_outcome_reached_today", True))
    fwd = effective_forward(merged, derived, unsure_as)
    persisting = [w for w, s in fwd.items() if s == "persists"]
    reached = bool((merged.get("outcome_reached_today") or {}).get("value")) or derived["outcome_reached"]
    ag = merged.get("agreement") or {}
    walls_both = _sorted_walls(w for w in (ag.get("walls_both") or []) if w in set(derived["walls_both"]))
    left_out = _sorted_walls(set(derived["walls_both"]) - set(walls_both))
    warnings: list = []
    if left_out:
        warnings.append(f"the comparator left {', '.join(left_out)} out of walls_both although both walkers put them on "
                        f"the path (allowed: it is more conservative).")
    kill_reason = None
    status = "kept"
    if reached and kill_rule:
        who = " and ".join(x for x, v in (("walker a", derived["outcome_a"]), ("walker b", derived["outcome_b"]),
                                          ("the comparator", bool((merged.get("outcome_reached_today") or {}).get("value")))) if v)
        reason = common.normalize_ws((merged.get("outcome_reached_today") or {}).get("reasoning") or "")
        kill_reason = f"outcome reached today with their own AI ({who} say so): {reason}"
        status = "killed"
    elif reached:
        warnings.append("the outcome is reached today, but kill_only_if_outcome_reached_today is off; the pain was kept.")
    lane_hint = "trade" if not persisting else None
    return {
        "pain_id": pid, "room": room, "status": status, "kill_reason": kill_reason,
        "outcome": merged.get("outcome"),
        "outcome_reached_today": reached,
        "outcome_reasoning": (merged.get("outcome_reached_today") or {}).get("reasoning"),
        "walls_both": walls_both, "walls_one": list(derived["walls_one"]),
        "path_walls": {w: s for w, s in sorted(path_walls(merged).items(), key=lambda kv: _wall_num(kv[0]))},
        "steps": len(merged.get("today") or []),
        "forward_12m": fwd,
        "persisting_walls": persisting,
        "lane_hint": lane_hint,
        "reconciled_ids": list(ag.get("reconciled_ids") or []),
        "disagreements": {"comparator": list(merged.get("disagreements") or []), "computed": list(derived["disagreements"])},
        "walkers": {"a": _walk_summary(a, derived["map_a"], unsure_as), "b": _walk_summary(b, derived["map_b"], unsure_as)},
        "pairs_drafted": len(merged.get("pairs") or []),
        "warnings": warnings,
    }


def _cell(s) -> str:
    return common.normalize_ws(str(s if s is not None else "")).replace("|", "/")


def render_walk_md(entry: dict, merged: dict, a: dict, b: dict, walls: dict, run) -> str:
    pid = entry["pain_id"]
    lines = [
        f"# Walk: {pid}",
        "",
        f"Run: {common.run_name(run)}. Status: {entry['status']}" + (f" ({_cell(entry['kill_reason'])})" if entry["kill_reason"] else "") + ".",
        "A walk follows one typical person, with today's best AI assistant in their pocket, from the moment the problem "
        "appears to the moment it is gone. A wall is a point where they still fail. Machine walls (W1–W16) melt as AI "
        "improves; human walls (W17–W29) hold. Two walkers walked independently; the comparator merged them the "
        "conservative way: the outcome counts as reached if either walker says so, a wall persists only if both say so, "
        "and a wall counts for a pair only if both put it on the path.",
        "",
        "## Persona",
        "",
        f"{_cell((merged.get('persona') or {}).get('description'))} (records: "
        f"{', '.join((merged.get('persona') or {}).get('record_ids') or []) or 'none'})",
        "",
        "## Outcome they want",
        "",
        _cell(merged.get("outcome")),
        "",
        "## Today",
        "",
        "| Step | What they do | Drops out? | Why | Walls |",
        "|---|---|---|---|---|",
    ]
    for step in merged.get("today") or []:
        ws = ", ".join(f"{w} {walls.get(w, {}).get('name', '')}".strip() for w in (step.get("walls") or [])) or "none"
        lines.append(f"| {step.get('step')} | {_cell(step.get('does'))} | {'yes' if step.get('drops_out') else 'no'} | "
                     f"{_cell(step.get('why'))} | {ws} |")
    wa, wb = entry["walkers"]["a"], entry["walkers"]["b"]
    lines += ["", f"Outcome reached today: {'yes' if entry['outcome_reached_today'] else 'no'}. "
                  f"{_cell(entry['outcome_reasoning'])} (walker a: {'yes' if wa['outcome_reached_today'] else 'no'}; "
                  f"walker b: {'yes' if wb['outcome_reached_today'] else 'no'})"]
    lines += ["", "## Twelve months from now", "",
              "| Wall | Name | Kind | Walker a | Walker b | Comparator | Used |",
              "|---|---|---|---|---|---|---|"]
    mraw = _raw_forward(merged)
    for w, used in entry["forward_12m"].items():
        info = walls.get(w, {})
        sa = wa["forward"].get(w) or _status_via_map(w, entry, a, "a") or "not on path"
        sb = wb["forward"].get(w) or _status_via_map(w, entry, b, "b") or "not on path"
        lines.append(f"| {w} | {info.get('name', '')} | {info.get('kind', '')} | {sa} | {sb} | {mraw.get(w, '')} | {used} |")
    lines += ["", f"Walls both walkers met: {', '.join(entry['walls_both']) or 'none'}. "
                  f"Walls only one walker met: {', '.join(entry['walls_one']) or 'none'}."]
    if entry["persisting_walls"]:
        lines.append(f"Walls that persist (both walkers agree): {', '.join(entry['persisting_walls'])}.")
    else:
        lines.append("No wall persists: every wall melts within 12 months. Lane hint: trade (machine walls only).")
    if entry["reconciled_ids"]:
        lines += ["", "Reconciled wall ids (the comparator judged these to be the same obstacle):"]
        for r in entry["reconciled_ids"]:
            lines.append(f"- walker a {r.get('a')} = walker b {r.get('b')} -> {r.get('as')}: {_cell(r.get('reasoning'))}")
    lines += ["", "## Where the walkers disagreed", ""]
    dis = entry["disagreements"]
    if dis["comparator"] or dis["computed"]:
        for d in dis["comparator"]:
            lines.append(f"- {_cell(d)}")
        for d in dis["computed"]:
            lines.append(f"- (computed) {_cell(d)}")
    else:
        lines.append("None: both walkers saw the same walls, the same outcome and the same 12-month picture.")
    lines += ["", f"## Pairs drafted ({entry['pairs_drafted']})", ""]
    if merged.get("pairs"):
        lines.append("Checked mechanically by `funnel pairs` (see 05_pairs.md).")
        lines.append("")
        for i, p in enumerate(merged["pairs"], 1):
            hold = p.get("hold_wall") or "none (trade)"
            lines.append(f"- rank {p.get('rank')}: entry {', '.join(p.get('entry_walls') or []) or 'none'}; hold {hold}"
                         + (f" ({p.get('hold_supply_id')})" if p.get("hold_supply_id") else "")
                         + (f" (partner {p.get('partner_id') or p.get('partner_kind')})" if p.get("partner_id") or p.get("partner_kind") else "")
                         + f". {_cell(p.get('one_liner'))}")
    else:
        lines.append("None drafted.")
    if entry["warnings"]:
        lines += ["", "## Warnings", ""]
        lines += [f"- {w}" for w in entry["warnings"]]
    return "\n".join(lines) + "\n"


def _status_via_map(w: str, entry: dict, walk: dict, letter: str):
    """The walker's raw status for a wall that was reconciled into `w`."""
    for r in entry["reconciled_ids"]:
        if r.get("as") == w and r.get(letter) and r.get(letter) != w:
            return _raw_forward(walk).get(r[letter])
    return None


def _check_one(run, pid: str, room: str, walls: dict, supply: dict, rules4: dict, stored: dict) -> dict:
    """Validate one pain's files. Returns {"errors", "notes", "a", "b", "merged", "derived", "present"}."""
    paths = walk_paths(run, pid)
    unsure_as = str(rules4.get("unsure_counts_as", "melts"))
    errors: list = []
    notes: list = []
    present = {k: paths[k].exists() for k in ("a", "b", "merged")}
    data: dict = {"a": None, "b": None, "merged": None}
    for k in ("a", "b", "merged"):
        if not present[k]:
            continue
        d, err = _read(paths[k])
        if err:
            errors.append(err)
            continue
        where = common.rel(paths[k])
        if k == "merged":
            errors.extend(validate_merged(d, where, pid, walls, supply, stored))
        else:
            errors.extend(validate_walk(d, where, pid, walls, letter=k, stored=stored))
        data[k] = d
    derived = None
    if data["a"] is not None and data["b"] is not None and not errors:
        rec = ((data["merged"] or {}).get("agreement") or {}).get("reconciled_ids") if data["merged"] else []
        derived = derive_merge(data["a"], data["b"], rec, unsure_as)
        if data["merged"] is not None and bool(rules4.get("conservative_merge", True)):
            errors.extend(check_conservative(data["merged"], derived, common.rel(paths["merged"]), unsure_as))
    if not stored:
        notes.append(f"{room}: no stored records found; persona record_ids were not checked.")
    return {"errors": errors, "notes": notes, "a": data["a"], "b": data["b"], "merged": data["merged"],
            "derived": derived, "present": present, "paths": paths}


def walks(run, check=None) -> dict:
    rd = common.run_dir(run)
    rules = common.load_kill_rules()
    rules4 = rules.get("stage4") or {}
    walls = common.load_walls()
    supply = ledger_supply()
    unsure_as = str(rules4.get("unsure_counts_as", "melts"))

    if check:
        pid = check
        room, _key = common.split_pain_id(pid)
        stored = records.records_by_id(run, room)
        r = _check_one(run, pid, room, walls, supply, rules4, stored)
        if not any(r["present"].values()):
            raise common.MissingInput(f"No walk files for {pid} in {common.rel(walks_dir(run))}/: expected {pid}.a.json, "
                                      f"{pid}.b.json and {pid}.json.")
        report = {"pain_id": pid, "present": r["present"], "errors": r["errors"], "notes": r["notes"], "derived": None,
                  "pair_checks": []}
        if r["derived"] is not None:
            d = r["derived"]
            report["derived"] = {"outcome_reached": d["outcome_reached"], "walls_both": d["walls_both"],
                                 "walls_one": d["walls_one"], "forward": d["forward"], "disagreements": d["disagreements"]}
            if r["merged"] is not None and not r["errors"]:
                entry = _stage4_entry(pid, room, r["merged"], r["a"], r["b"], d, rules4)
                report["lane_hint"] = entry["lane_hint"]
                report["status"] = entry["status"]
                report["pair_checks"] = _pair_checks_for(run, entry, r["merged"], rules, supply, walls)
        common.log_event(run, STAGE4, "walks", "check", pain=pid, files=r["present"], errors=len(r["errors"]))
        return report

    kept = load_kept_pains(run)
    if not kept:
        raise common.MissingInput(f"No kept pains in {common.rel(common.listen_dir(run) / 'pains.json')}. Nothing to walk.")
    errors: list = []
    missing: list = []
    notes: list = []
    entries: list = []
    date = common.run_date(run)
    stored_cache: dict = {}
    for pain in kept:
        pid = pain["pain_id"]
        room, _key = common.split_pain_id(pid)
        if room not in stored_cache:
            stored_cache[room] = records.records_by_id(run, room)
        r = _check_one(run, pid, room, walls, supply, rules4, stored_cache[room])
        absent = [k for k in ("a", "b", "merged") if not r["present"][k]]
        if absent:
            names = ", ".join(str(r["paths"][k].name) for k in absent)
            missing.append(f"{pid}: missing {names} in {common.rel(walks_dir(run))}/.")
            continue
        errors.extend(r["errors"])
        for n in r["notes"]:
            if n not in notes:
                notes.append(n)
        if r["errors"] or r["derived"] is None:
            continue
        entries.append((pain, r))
    if missing:
        if common.is_dry_run():
            for m in missing:
                notes.append(f"dry run: skipped {m}")
        else:
            raise common.MissingInput("Walk files are missing. Two walkers (a, b) and a comparator write them per pain: "
                                      + " ".join(missing))
    if errors:
        raise common.ValidationErrors(errors)

    out_pains: list = []
    for pain, r in entries:
        pid = pain["pain_id"]
        entry = _stage4_entry(pid, pain.get("room") or common.split_pain_id(pid)[0], r["merged"], r["a"], r["b"], r["derived"], rules4)
        entry["stage3_rank"] = pain.get("rank")
        entry["tags"] = list(pain.get("tags") or [])
        if entry["status"] == "killed":
            common.append_graveyard(date, STAGE4, f"pain:{pid}", entry["kill_reason"])
        common.write_text(r["paths"]["md"], render_walk_md(entry, r["merged"], r["a"], r["b"], walls, run))
        out_pains.append(entry)
    kept_ids = [e["pain_id"] for e in out_pains if e["status"] == "kept"]
    killed_ids = [e["pain_id"] for e in out_pains if e["status"] == "killed"]
    trade_hints = [e["pain_id"] for e in out_pains if e["status"] == "kept" and e["lane_hint"] == "trade"]
    for e in out_pains:
        for w in e["warnings"]:
            common.log_event(run, STAGE4, "walks", "note", pain=e["pain_id"], note=w, review=False)
    for n in notes:
        common.log_event(run, STAGE4, "walks", "note", note=n, review=False)
    result = {
        "rules": {"unsure_counts_as": unsure_as, "kill_only_if_outcome_reached_today": bool(rules4.get("kill_only_if_outcome_reached_today", True)),
                  "conservative_merge": bool(rules4.get("conservative_merge", True))},
        "counts": {"in": len(kept), "walked": len(out_pains), "kept": len(kept_ids), "killed": len(killed_ids),
                   "lane_hint_trade": len(trade_hints)},
        "kept": kept_ids,
        "killed": killed_ids,
        "lane_hint_trade": trade_hints,
        "pains": out_pains,
        "notes": notes,
    }
    common.write_json(walks_dir(run) / "_stage4.json", result)
    common.log_event(run, STAGE4, "walks", "count", pains_in=len(kept), walked=len(out_pains), kept=len(kept_ids),
                     killed=len(killed_ids), lane_hint_trade=trade_hints)
    return result


# --------------------------------------------------------------------------- stage 5
def _dedupe(seq) -> list:
    out = []
    for x in seq:
        if x not in out:
            out.append(x)
    return out


def _wall_label(w: str, walls: dict) -> str:
    name = walls.get(w, {}).get("name")
    return f"{w} {name}" if name else str(w)


def evaluate_pair(pair: dict, index: int, ctx: dict, rules: dict, supply: dict, walls: dict, run_date) -> dict:
    """One alternative against every rule. ctx: walls_both, forward, path_walls, lane_hint, room, depth."""
    s5 = rules.get("stage5") or {}
    min_entry = int(s5.get("min_entry_walls", 3))
    slack = int(s5.get("adjacency_slack_steps", 1))
    trade_rules = s5.get("trade") or {}
    walls_both = set(ctx["walls_both"])
    forward = ctx["forward"]
    first = ctx["path_walls"]
    checks: dict = {}

    entry = _dedupe([w for w in (pair.get("entry_walls") or []) if isinstance(w, str)])
    problems = []
    if len(entry) < min_entry:
        problems.append(f"only {len(entry)} distinct entry wall(s); needs at least {min_entry}")
    human = [w for w in entry if walls.get(w, {}).get("kind") != "machine"]
    if human:
        problems.append(f"{', '.join(human)} not machine walls (entry walls are W1–W16)")
    checks["entry"] = {"pass": not problems, "reason": "; ".join(problems) if problems
                       else f"{len(entry)} machine walls: {', '.join(_wall_label(w, walls) for w in entry)}"}

    hold = pair.get("hold_wall")
    wb_problems = [f"entry wall {w} is not in walls_both" for w in entry if w not in walls_both]
    if hold is not None and hold not in walls_both:
        wb_problems.append(f"hold wall {hold} is not in walls_both")
    checks["walls_both"] = {"pass": not wb_problems, "reason": "; ".join(wb_problems) if wb_problems
                            else ("every entry wall and the hold wall sit in walls_both" if hold else "every entry wall sits in walls_both")}

    adj_problems = []
    steps = [first[w] for w in entry if w in first and isinstance(first[w], int)]
    off_path = [w for w in entry if w not in first]
    if off_path:
        adj_problems.append(f"{', '.join(off_path)} not on the merged path")
    span_text = ""
    if steps:
        lo, hi = min(steps), max(steps)
        span = hi - lo + 1
        allowed = len(entry) + slack
        span_text = f"entry walls first appear on steps {lo}–{hi} (span {span}, allowed {allowed})"
        if span > allowed:
            adj_problems.append(f"entry walls are spread over {span} steps (steps {lo}–{hi}); allowed {allowed} "
                                f"({len(entry)} walls + slack {slack})")
        if hold is not None:
            hs = first.get(hold)
            if not isinstance(hs, int):
                adj_problems.append(f"hold wall {hold} is not on the merged path")
            else:
                dist = max(0, lo - hs, hs - hi)
                span_text += f"; hold {hold} on step {hs} (distance {dist} from the entry span, allowed {slack})"
                if dist > slack:
                    adj_problems.append(f"hold wall {hold} is {dist} step(s) away from the entry span (steps {lo}–{hi}); "
                                        f"allowed {slack}")
    elif not off_path:
        adj_problems.append("no entry walls to place")
    checks["adjacency"] = {"pass": not adj_problems, "reason": "; ".join(adj_problems) if adj_problems else span_text}

    if hold is None:
        checks["hold"] = {"pass": None, "reason": "no hold wall (a trade needs none)"}
        checks["persistence"] = {"pass": None, "reason": "no hold wall (a trade needs none)"}
        hold_valid = False
    else:
        h_problems = []
        if walls.get(hold, {}).get("kind") != "human":
            h_problems.append(f"{hold} is a machine wall; the hold must be a human wall (W17–W29)")
        if hold in supply["cannot"]:
            h_problems.append(f"{_wall_label(hold, walls)} is in the ledger's cannot list; it can never be a hold")
        checks["hold"] = {"pass": not h_problems, "reason": "; ".join(h_problems) if h_problems
                          else f"{_wall_label(hold, walls)} is a human wall the ledger does not rule out"}
        st = forward.get(hold)
        if st == "persists":
            checks["persistence"] = {"pass": True, "reason": f"{hold} persists in the merged 12-month walk (both walkers agree)"}
        elif st is None:
            checks["persistence"] = {"pass": False, "reason": f"{hold} has no 12-month verdict in the merged walk (not on the path)"}
        else:
            checks["persistence"] = {"pass": False, "reason": f"{hold} melts in the merged 12-month walk; a hold must persist"}
        hold_valid = (checks["hold"]["pass"] and checks["persistence"]["pass"]
                      and hold in walls_both and checks["adjacency"]["pass"] is True)

    # lanes
    reasons: dict = {}
    lanes_ok: list = []
    hs_id = pair.get("hold_supply_id")
    if hold is None:
        reasons["business"] = "no hold wall (a business needs one human wall that holds)"
    elif not hold_valid:
        reasons["business"] = "no valid hold wall"
    elif hs_id is None:
        reasons["business"] = "no hold_supply_id (the ledger id under which the founder can be this wall)"
    else:
        cb = supply["can_be"].get(hs_id) or {}
        if str(cb.get("wall")) != hold:
            reasons["business"] = f"hold_supply_id {hs_id} is for {cb.get('wall')}, not {hold}"
        elif not ("any" in [str(x) for x in (cb.get("rooms") or [])] or ctx["room"] in [str(x) for x in (cb.get("rooms") or [])]):
            reasons["business"] = f"hold_supply_id {hs_id} does not cover this room (rooms: {', '.join(str(x) for x in cb.get('rooms') or [])})"
        elif cb.get("depth_strength_required") and str(ctx.get("depth", {}).get("strength")) != str(cb.get("depth_strength_required")):
            d = ctx.get("depth") or {}
            reasons["business"] = (f"{hs_id} ({cb.get('text', '')}) needs {cb.get('depth_strength_required')} depth; this room's "
                                   f"Stage 2 depth is {d.get('depth_ledger_id') or 'none'} ({d.get('strength') or 'unknown'})")
        else:
            lanes_ok.append("business")
            reasons["business"] = f"the founder can be {_wall_label(hold, walls)} ({hs_id}: {cb.get('text', '')})"
    p_id = pair.get("partner_id")
    p_kind = pair.get("partner_kind")
    if hold is None:
        reasons["partner"] = "no hold wall (a partner rents one human wall that holds)"
    elif not hold_valid:
        reasons["partner"] = "no valid hold wall"
    elif p_id is not None:
        cr = supply["can_rent"].get(p_id) or {}
        if str(cr.get("wall")) != hold:
            reasons["partner"] = f"partner_id {p_id} is for {cr.get('wall')}, not {hold}"
        else:
            lanes_ok.append("partner")
            reasons["partner"] = f"a partner can supply {_wall_label(hold, walls)} ({p_id}: {cr.get('text', '')})"
    elif _nonempty_str(p_kind):
        if hold in supply["cannot"]:
            reasons["partner"] = f"{hold} is in the ledger's cannot list"
        else:
            lanes_ok.append("partner")
            reasons["partner"] = f"a partner ({common.normalize_ws(p_kind)}) supplies {_wall_label(hold, walls)}"
    else:
        reasons["partner"] = "no partner_id or partner_kind"
    tr = pair.get("trade")
    if hold is not None:
        reasons["trade"] = (f"this alternative names a hold wall ({hold}); a trade has none (set hold_wall to null "
                            f"and drop the supply and partner ids to draft a trade)")
    elif tr is None:
        reasons["trade"] = "no trade object (build_weeks, payment_upfront, subscription, exit_date)"
    else:
        t_problems = []
        max_weeks = trade_rules.get("max_build_weeks", 2)
        bw = tr.get("build_weeks")
        if isinstance(bw, (int, float)) and bw > max_weeks:
            t_problems.append(f"build takes {bw} weeks; allowed {max_weeks}")
        if trade_rules.get("payment_upfront", True) and tr.get("payment_upfront") is not True:
            t_problems.append("payment is not upfront")
        if not trade_rules.get("subscriptions_allowed", False) and tr.get("subscription") is True:
            t_problems.append("a subscription is not allowed in a trade")
        if trade_rules.get("exit_date_required", True):
            ed = tr.get("exit_date")
            if not common.is_date(ed):
                t_problems.append("no exit_date written from day one")
            elif _dt.date.fromisoformat(ed) <= run_date:
                t_problems.append(f"exit_date {ed} is not after the run date {run_date.isoformat()}")
        if t_problems:
            reasons["trade"] = "; ".join(t_problems)
        else:
            lanes_ok.append("trade")
            reasons["trade"] = (f"no holding wall; build {bw} week(s), payment {'upfront' if tr.get('payment_upfront') else 'not upfront'}, "
                                f"{'a subscription' if tr.get('subscription') else 'no subscription'}, exit "
                                f"{tr.get('exit_date') or 'not required'}")
    if ctx.get("lane_hint") == "trade":
        for lane in ("business", "partner"):
            if lane in lanes_ok:
                lanes_ok.remove(lane)
                reasons[lane] = "the merged walk says every wall melts; only a trade is allowed (lane_hint: trade)"
    lane_pref = [str(x) for x in (s5.get("lane_preference") or list(LANES))]
    lane = next((x for x in lane_pref if x in lanes_ok), None)
    if lane:
        checks["lane"] = {"pass": True, "lane": lane, "reason": f"{lane}: {reasons[lane]}"}
    else:
        checks["lane"] = {"pass": False, "lane": None,
                          "reason": "; ".join(f"{x}: {reasons.get(x, 'not possible')}" for x in lane_pref)}
    failed = [name for name in CHECKS if checks[name]["pass"] is False]
    return {
        "index": index, "rank": pair.get("rank"),
        "entry_walls": entry, "hold_wall": hold, "hold_supply_id": hs_id, "partner_id": p_id, "partner_kind": p_kind,
        "trade": tr, "one_liner": pair.get("one_liner"), "crux": pair.get("crux"),
        "credibility_question": pair.get("credibility_question"),
        "reasoning": pair.get("reasoning"), "confidence": pair.get("confidence"),
        "checks": checks, "failed": failed, "valid": not failed, "lane": lane if not failed else None,
        "lane_reasons": reasons,
    }


def choose_alternative(alternatives, lane_preference):
    pref = [str(x) for x in lane_preference]
    valid = [a for a in alternatives if a["valid"]]
    if not valid:
        return None
    return sorted(valid, key=lambda a: (pref.index(a["lane"]) if a["lane"] in pref else len(pref),
                                        a["rank"] if _is_int(a["rank"]) else 10 ** 9, a["index"]))[0]


PAIR_FIELDS = ("rank", "entry_walls", "hold_wall", "hold_supply_id", "partner_id", "partner_kind", "trade",
               "one_liner", "crux", "credibility_question", "reasoning", "confidence")


def _kept_pair(alt: dict) -> dict:
    """The kept alternative as a PAIR object (plus its lane and index) for later stages."""
    out = {k: alt.get(k) for k in PAIR_FIELDS}
    out["lane"] = alt["lane"]
    out["index"] = alt["index"]
    return out


def _pair_checks_for(run, entry: dict, merged: dict, rules: dict, supply: dict, walls: dict) -> list:
    """Evaluate the merged file's alternatives for one Stage 4 entry (used by `pairs` and `walks --check`)."""
    try:
        depth = depth_strength_by_room(run).get(entry["room"], {})
    except common.MissingInput:
        depth = {"depth_ledger_id": None, "strength": None}
    ctx = {"walls_both": entry["walls_both"], "forward": entry["forward_12m"], "path_walls": entry["path_walls"],
           "lane_hint": entry["lane_hint"], "room": entry["room"], "depth": depth}
    return [evaluate_pair(p, i, ctx, rules, supply, walls, common.run_date(run))
            for i, p in enumerate(merged.get("pairs") or [], 1) if isinstance(p, dict)]


def pairs(run) -> dict:
    rd = common.run_dir(run)
    rules = common.load_kill_rules()
    s5 = rules.get("stage5") or {}
    lane_pref = [str(x) for x in (s5.get("lane_preference") or list(LANES))]
    alt_min = int(s5.get("alternative_pairs_min", 2))
    alt_max = int(s5.get("alternative_pairs_max", 3))
    walls = common.load_walls()
    supply = ledger_supply()
    depth_by_room = depth_strength_by_room(run)
    p4 = walks_dir(run) / "_stage4.json"
    common.require_file(p4, "Run `funnel walks` first.")
    stage4 = common.read_json(p4)
    entries = [e for e in (stage4.get("pains") or []) if isinstance(e, dict) and e.get("status") == "kept"]
    if not entries:
        raise common.MissingInput(f"No Stage 4 survivors in {common.rel(p4)}. Nothing to pair.")

    errors: list = []
    warnings: list = []
    out: list = []
    date = common.run_date(run)
    for entry in entries:
        pid = entry["pain_id"]
        mp = walk_paths(run, pid)["merged"]
        common.require_file(mp, "The comparator writes the merged walk with its pairs.")
        merged, err = _read(mp)
        if err:
            errors.append(err)
            continue
        where = common.rel(mp)
        plist = merged.get("pairs") if isinstance(merged, dict) else None
        if plist is None:
            plist = []
        if not isinstance(plist, list):
            errors.append(f"{where}: 'pairs' must be a list of PAIR objects.")
            continue
        shape_errors = []
        ranks: dict = {}
        for i, pair in enumerate(plist, 1):
            shape_errors.extend(validate_pair_shape(pair, f"{where}: pair {i}", walls, supply))
            if isinstance(pair, dict) and _is_int(pair.get("rank")):
                if pair["rank"] in ranks:
                    shape_errors.append(f"{where}: pair {i}: rank {pair['rank']} is also used by pair {ranks[pair['rank']]}.")
                ranks.setdefault(pair["rank"], i)
        if not alt_min <= len(plist) <= alt_max:
            msg = (f"{where}: {len(plist)} alternative pair(s); the comparator drafts {alt_min} to {alt_max} "
                   f"(alternative_pairs_min/max).")
            if common.is_dry_run():
                warnings.append(msg)
            else:
                shape_errors.append(msg)
        if shape_errors:
            errors.extend(shape_errors)
            continue
        depth = depth_by_room.get(entry["room"]) or {"depth_ledger_id": None, "strength": None}
        ctx = {"walls_both": entry["walls_both"], "forward": entry["forward_12m"], "path_walls": entry["path_walls"],
               "lane_hint": entry.get("lane_hint"), "room": entry["room"], "depth": depth}
        alts = [evaluate_pair(p, i, ctx, rules, supply, walls, date) for i, p in enumerate(plist, 1)]
        chosen = choose_alternative(alts, lane_pref)
        item = {
            "pain_id": pid, "room": entry["room"], "stage3_rank": entry.get("stage3_rank"),
            "status": "kept" if chosen else "killed", "kill_reason": None,
            "lane": chosen["lane"] if chosen else None,
            "lane_hint": entry.get("lane_hint"),
            "walls_both": entry["walls_both"], "persisting_walls": entry.get("persisting_walls") or [],
            "depth": depth,
            "kept_index": chosen["index"] if chosen else None,
            "kept_reason": None,
            "kept": _kept_pair(chosen) if chosen else None,
            "alternatives": alts,
        }
        if chosen:
            others = [a for a in alts if a["valid"] and a is not chosen]
            why = f"lane {chosen['lane']} (lane order {' > '.join(lane_pref)})"
            if others:
                why += "; " + ", ".join(f"alternative {a['index']} is {a['lane']} rank {a['rank']}" for a in others) + \
                       f"; kept alternative {chosen['index']} (rank {chosen['rank']})"
            else:
                why += f"; the only valid alternative (rank {chosen['rank']})"
            item["kept_reason"] = why
        else:
            parts = []
            for a in alts:
                fails = "; ".join(f"{name}: {a['checks'][name]['reason']}" for name in a["failed"])
                parts.append(f"alternative {a['index']} (rank {a['rank']}): {fails}")
            item["kill_reason"] = ("no pair, no clean trade, no plausible partner: " + " / ".join(parts)) if parts \
                else "no pair, no clean trade, no plausible partner: no alternative pairs were drafted"
            common.append_graveyard(date, STAGE5, f"pain:{pid}", item["kill_reason"])
        out.append(item)
    if errors:
        raise common.ValidationErrors(errors)
    out.sort(key=lambda x: (x["stage3_rank"] if _is_int(x.get("stage3_rank")) else 10 ** 9, x["pain_id"]))
    kept_ids = [x["pain_id"] for x in out if x["status"] == "kept"]
    killed_ids = [x["pain_id"] for x in out if x["status"] == "killed"]
    by_lane = {lane: sum(1 for x in out if x["lane"] == lane) for lane in lane_pref}
    for w in warnings:
        common.log_event(run, STAGE5, "pairs", "note", note=w, review=False)
    result = {
        "lane_preference": lane_pref,
        "rules": {"min_entry_walls": int(s5.get("min_entry_walls", 3)), "adjacency_slack_steps": int(s5.get("adjacency_slack_steps", 1)),
                  "alternative_pairs_min": alt_min, "alternative_pairs_max": alt_max, "trade": dict(s5.get("trade") or {})},
        "counts": {"in": len(entries), "kept": len(kept_ids), "killed": len(killed_ids), "by_lane": by_lane},
        "kept": kept_ids,
        "killed": killed_ids,
        "pains": out,
        "warnings": warnings,
        "check_meaning": CHECK_MEANING,
        "lane_meaning": LANE_MEANING,
    }
    common.write_json(rd / "05_pairs.json", result)
    common.write_text(rd / "05_pairs.md", render_pairs_md(result, run, walls))
    common.log_event(run, STAGE5, "pairs", "count", pains_in=len(entries), kept=len(kept_ids), killed=len(killed_ids),
                     by_lane=by_lane)
    return result


def _check_cell(c: dict) -> str:
    if c["pass"] is None:
        return "n/a"
    return "pass" if c["pass"] else "FAIL"


def render_pairs_md(result: dict, run, walls=None) -> str:
    walls = walls if walls is not None else common.load_walls()
    c = result["counts"]
    r = result["rules"]
    lines = [
        "# Stage 5: pairs",
        "",
        f"Run: {common.run_name(run)}.",
        f"{c['in']} pain(s) came out of the walk. {c['kept']} kept, {c['killed']} killed. By lane: "
        + ", ".join(f"{k} {v}" for k, v in c["by_lane"].items()) + ".",
        "",
        "A pair is the product: the machine walls it gets in through (the entry) plus one human wall that holds it. "
        "Every alternative the comparator drafted was checked by code; the strongest valid one was kept "
        f"(lane order {' > '.join(result['lane_preference'])}, then the comparator's rank).",
        "",
        "Lanes:",
        "",
    ]
    for lane, meaning in result["lane_meaning"].items():
        lines.append(f"- **{lane}**: {meaning}.")
    lines += ["", "Checks:", ""]
    for name in CHECKS:
        lines.append(f"- **{name}**: {result['check_meaning'][name]}.")
    lines += ["", f"Rules: min_entry_walls {r['min_entry_walls']}, adjacency_slack_steps {r['adjacency_slack_steps']}, trade: "
                  + ", ".join(f"{k} {v}" for k, v in r["trade"].items()) + ".", ""]
    lines += [f"## Kept pains ({c['kept']})", ""]
    kept = [x for x in result["pains"] if x["status"] == "kept"]
    if kept:
        lines.append("| Pain | Lane | Entry walls | Hold wall | Supplied by | Kept alternative |")
        lines.append("|---|---|---|---|---|---|")
        for x in kept:
            a = x["alternatives"][x["kept_index"] - 1]
            sup = a["hold_supply_id"] or a["partner_id"] or a["partner_kind"] or ("trade" if a["lane"] == "trade" else "-")
            lines.append(f"| {x['pain_id']} | {x['lane']} | {', '.join(a['entry_walls'])} | {a['hold_wall'] or 'none'} | "
                         f"{_cell(sup)} | {a['index']} (rank {a['rank']}) |")
    else:
        lines.append("None.")
    for x in result["pains"]:
        lines += ["", f"## {x['pain_id']} ({x['status']}" + (f", lane {x['lane']}" if x["lane"] else "") + ")", ""]
        lines.append(f"Room {x['room']}. Walls both walkers met: {', '.join(x['walls_both']) or 'none'}. "
                     f"Persisting walls: {', '.join(x['persisting_walls']) or 'none'}."
                     + (" Lane hint: trade (every wall melts)." if x["lane_hint"] == "trade" else ""))
        if x["status"] == "kept":
            lines.append(f"Kept alternative {x['kept_index']}: {_cell(x['kept_reason'])}.")
        else:
            lines.append(f"Killed: {_cell(x['kill_reason'])}")
        lines.append("")
        lines.append("| Alt | Rank | Entry | Hold | Supply / partner / trade | " + " | ".join(CHECKS) + " | Valid | Lane |")
        lines.append("|---|---|---|---|---|" + "---|" * len(CHECKS) + "---|---|")
        for a in x["alternatives"]:
            if a["trade"]:
                sup = (f"trade: {a['trade'].get('build_weeks')} wk, upfront {'yes' if a['trade'].get('payment_upfront') else 'no'}, "
                       f"subscription {'yes' if a['trade'].get('subscription') else 'no'}, exit {a['trade'].get('exit_date') or 'none'}")
            else:
                sup = a["hold_supply_id"] or a["partner_id"] or a["partner_kind"] or "-"
            lines.append(f"| {a['index']} | {a['rank']} | {', '.join(a['entry_walls']) or 'none'} | {a['hold_wall'] or 'none'} | "
                         f"{_cell(sup)} | " + " | ".join(_check_cell(a["checks"][n]) for n in CHECKS)
                         + f" | {'yes' if a['valid'] else 'no'} | {a['lane'] or '-'} |")
        for a in x["alternatives"]:
            lines.append("")
            lines.append(f"### Alternative {a['index']} (rank {a['rank']}): {_cell(a['one_liner'])}")
            lines.append("")
            for n in CHECKS:
                lines.append(f"- {n}: {_check_cell(a['checks'][n])}. {_cell(a['checks'][n]['reason'])}")
            lines.append(f"- crux: {_cell(a['crux'])}")
            lines.append(f"- credibility question: {_cell(a['credibility_question'])}")
            lines.append(f"- comparator: {_cell(a['reasoning'])} (confidence {a['confidence']})")
    if result["warnings"]:
        lines += ["", "## Warnings", ""]
        lines += [f"- {w}" for w in result["warnings"]]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- commands
def cmd_walks(args) -> int:
    run = common.run_dir(args.run)
    if args.check:
        report = walks(run, check=args.check)
        pid = report["pain_id"]
        for k, name in (("a", f"{pid}.a.json"), ("b", f"{pid}.b.json"), ("merged", f"{pid}.json")):
            print(f"{name}: {'present' if report['present'][k] else 'missing'}")
        d = report.get("derived")
        if d:
            print(f"Conservative merge from the walker files: outcome reached today {'yes' if d['outcome_reached'] else 'no'}; "
                  f"walls both: {', '.join(d['walls_both']) or 'none'}; walls one: {', '.join(d['walls_one']) or 'none'}; "
                  f"persists: {', '.join(w for w, s in d['forward'].items() if s == 'persists') or 'none'}.")
            for line in d["disagreements"]:
                print(f"  disagreement: {line}")
        if report.get("status"):
            print(f"Stage 4 verdict: {report['status']}" + (f"; lane hint: {report['lane_hint']}" if report.get("lane_hint") else "") + ".")
        for a in report.get("pair_checks") or []:
            fails = "; ".join(f"{n}: {a['checks'][n]['reason']}" for n in a["failed"])
            print(f"  pair {a['index']} (rank {a['rank']}): {'valid, lane ' + a['lane'] if a['valid'] else 'invalid: ' + fails}")
        for n in report["notes"]:
            print(f"note: {n}")
        if report["errors"]:
            raise common.ValidationErrors(report["errors"])
        print(f"{pid}: no errors. Nothing was written.")
        return 0
    result = walks(run)
    c = result["counts"]
    print(f"Walks: {c['in']} kept pain(s) in, {c['walked']} walked, {c['kept']} kept, {c['killed']} killed "
          f"(outcome reached today), {c['lane_hint_trade']} hinted trade.")
    for e in result["pains"]:
        if e["status"] == "kept":
            print(f"  kept: {e['pain_id']} (walls both: {', '.join(e['walls_both']) or 'none'}; persists: "
                  f"{', '.join(e['persisting_walls']) or 'none'}" + ("; lane hint: trade" if e["lane_hint"] == "trade" else "")
                  + f"; pairs drafted: {e['pairs_drafted']})")
    for e in result["pains"]:
        if e["status"] == "killed":
            print(f"  killed: {e['pain_id']}: {e['kill_reason']}")
    for n in result["notes"]:
        print(f"note: {n}")
    print(f"Wrote {common.rel(walks_dir(run) / '_stage4.json')}, one <pain-id>.md per pain and graveyard.md")
    return 0


def cmd_pairs(args) -> int:
    run = common.run_dir(args.run)
    result = pairs(run)
    c = result["counts"]
    print(f"Pairs: {c['in']} pain(s) in, {c['kept']} kept, {c['killed']} killed. By lane: "
          + ", ".join(f"{k} {v}" for k, v in c["by_lane"].items()) + ".")
    for x in result["pains"]:
        if x["status"] == "kept":
            a = x["alternatives"][x["kept_index"] - 1]
            print(f"  kept: {x['pain_id']}: lane {x['lane']}, alternative {a['index']} (rank {a['rank']}): entry "
                  f"{', '.join(a['entry_walls'])}, hold {a['hold_wall'] or 'none'}")
    for x in result["pains"]:
        if x["status"] == "killed":
            print(f"  killed: {x['pain_id']}: {x['kill_reason']}")
    for w in result["warnings"]:
        print(f"warning: {w}")
    print(f"Wrote {common.rel(run / '05_pairs.json')}, {common.rel(run / '05_pairs.md')} and graveyard.md")
    return 0


def register(subparsers) -> None:
    w = subparsers.add_parser("walks", help="Validate the walker and comparator files, re-derive the conservative merge, "
                                            "kill pains whose outcome is reached today; write 04_walks/<pain-id>.md and _stage4.json.")
    w.add_argument("--check", metavar="PAIN_ID", default=None, help="validate one pain's files and exit (nothing written)")
    w.set_defaults(func=cmd_walks)
    p = subparsers.add_parser("pairs", help="Check every alternative pair mechanically, keep the strongest valid one per pain; "
                                            "write 05_pairs.json and 05_pairs.md.")
    p.set_defaults(func=cmd_pairs)
