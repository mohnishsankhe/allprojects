"""Stage 2: exchange rates (`fx`) and the room mask (`mask`).

`fx` validates RUN/fx_rates.json. `mask` merges the model's mask parts, runs
the price checker on every spend item, applies the six tests (reach, depth,
spend, ladder, supply, exclusions), ranks the survivors, keeps at most
max_rooms, sends every killed or cut room to graveyard.md with the tests it
failed, and writes 02_mask.json and 02_mask.md.

Public API
----------
    TESTS = ("reach", "depth", "spend", "ladder", "supply", "exclusions")
    NEEDS = ("license_not_rentable", "large_capital", "ritual", "licensed_advocacy")
    validate_fx(run) -> (data, fx, warnings)      raises ValidationErrors
    parts_dir(run) -> Path                        RUN/02_mask.parts
    merge_parts(run) -> dict                      {"rooms": [...], "parts": [...]} (nothing written)
    load_rooms(run) -> dict[slug -> room]         kept rooms of RUN/01_rooms.json
    ledger_ids(ledger) -> dict                    {"warm": {...}, "search": {...}, "depth": {...}, "exclusions": {...}, ...}
    validate_entry(entry, where, ids) -> list[str]
    run_tests(entry, room, ids, rules, price_results) -> (tests, points)
    rank_key(verdict, rank_by) -> tuple
    mask(run, merge_parts=False, max_rooms=None) -> dict   the 02_mask.json content (files and graveyard written)
    render_md(result, run) -> str
    register(subparsers)                          adds `fx` and `mask [--merge-parts] [--max-rooms N]`
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

import common
import prices

STAGE = 2
TESTS = ("reach", "depth", "spend", "ladder", "supply", "exclusions")
NEEDS = ("license_not_rentable", "large_capital", "ritual", "licensed_advocacy")
EMPLOYER_WARM_IDS = ("w2", "w4")
EMPLOYER_EXCLUSION_ID = "x2"
DEFAULT_RANK_BY = ["ladder_steps", "spend_points_verified", "spend_points", "warm_reach"]
TEST_MEANING = {
    "reach": "the founder can reach the room: a warm path from the ledger, or the room already buys this kind of product through search, app stores or public marketplaces (with an evidence URL)",
    "depth": "the room's subject is one where the founder can tell good from bad (a ledger depth id)",
    "spend": "at least one concrete price people in the room pay, with a URL, that the price checker did not rule out",
    "ladder": "the room has enough paid problems in sequence (ladder steps)",
    "supply": "the room's core pains do not need something the founder lacks and cannot rent",
    "exclusions": "the room does not fall under a ledger exclusion",
}


# --------------------------------------------------------------------------- fx
def validate_fx(run) -> tuple:
    rd = common.run_dir(run)
    p = rd / "fx_rates.json"
    data = common.read_fx_file(run)
    errors: list = []
    warnings: list = []
    base = data.get("base")
    if base != "USD":
        errors.append(f"{common.rel(p)}: 'base' must be USD (got {base!r}).")
    as_of = data.get("as_of")
    if not common.is_date(as_of):
        errors.append(f"{common.rel(p)}: 'as_of' must be a date YYYY-MM-DD (got {as_of!r}).")
    else:
        age = (common.run_date(run) - _dt.date.fromisoformat(as_of)).days
        if age > 7:
            warnings.append(f"fx_rates.json is {age} days older than the run date. Refresh the rates if you can.")
    for code, entry in sorted(data["rates"].items()):
        where = f"{common.rel(p)}: {code}"
        if not isinstance(entry, dict):
            errors.append(f"{where}: must be an object with per_usd, url, seen_via, reasoning and confidence.")
            continue
        per_usd = entry.get("per_usd")
        if not isinstance(per_usd, (int, float)) or isinstance(per_usd, bool) or per_usd <= 0:
            errors.append(f"{where}: 'per_usd' must be a positive number (units of {code} per 1 US dollar; got {per_usd!r}).")
        url = entry.get("url")
        if not isinstance(url, str) or not url.startswith(("http://", "https://")):
            errors.append(f"{where}: 'url' must start with http:// or https:// (where the rate was seen).")
        if entry.get("seen_via") not in common.SEEN_VIA:
            errors.append(f"{where}: 'seen_via' must be page or search (got {entry.get('seen_via')!r}).")
        errors.extend(common.check_judgment(entry, where))
    if errors:
        raise common.ValidationErrors(errors)
    fx = common.load_fx(run)
    return data, fx, warnings


def cmd_fx(args) -> int:
    run = common.run_dir(args.run)
    data, fx, warnings = validate_fx(run)
    print(f"Exchange rates as of {data.get('as_of')} (units per 1 US dollar):")
    print(f"{'currency':9} {'per USD':>12}  {'seen via':8}  {'confidence':10}  source")
    print(f"{'USD':9} {1.0:>12.4f}  {'-':8}  {'-':10}  base currency")
    for code in sorted(data["rates"]):
        e = data["rates"][code]
        print(f"{code:9} {fx[code]:>12.4f}  {e.get('seen_via'):8}  {e.get('confidence'):10}  {e.get('url')}")
    for w in warnings:
        print(f"warning: {w}")
    common.log_event(run, STAGE, "fx", "check", what="fx_rates", currencies=sorted(fx), as_of=data.get("as_of"),
                     warnings=warnings)
    return 0


# --------------------------------------------------------------------------- inputs
def parts_dir(run) -> Path:
    return common.run_dir(run) / "02_mask.parts"


def _natural_key(p: Path) -> tuple:
    return tuple((0, int(t)) if t.isdigit() else (1, t) for t in re.split(r"(\d+)", p.stem) if t) + ((p.name,),)


def merge_parts(run) -> dict:
    d = parts_dir(run)
    files = sorted((p for p in d.glob("*.json") if p.is_file()), key=_natural_key) if d.exists() else []
    if not files:
        raise common.MissingInput(f"No part files in {common.rel(d)}/. The mask agents write <n>.json there "
                                  f"(see config/formats.md, Stage 2).")
    rooms: list = []
    errors: list = []
    for p in files:
        try:
            data = common.read_json(p)
        except ValueError as e:
            errors.append(f"{common.rel(p)}: not valid JSON ({e}). Fix the file.")
            continue
        part_rooms = data.get("rooms") if isinstance(data, dict) else data
        if not isinstance(part_rooms, list):
            errors.append(f"{common.rel(p)}: needs a 'rooms' list.")
            continue
        for i, entry in enumerate(part_rooms, 1):
            if not isinstance(entry, dict):
                errors.append(f"{common.rel(p)}: room {i}: must be an object.")
                continue
            e = dict(entry)
            e["_part"] = p.name
            rooms.append(e)
    if errors:
        raise common.ValidationErrors(errors)
    return {"rooms": rooms, "parts": [p.name for p in files]}


def load_rooms(run) -> dict:
    p = common.run_dir(run) / "01_rooms.json"
    common.require_file(p, "Run `funnel rooms --merge-parts` first.")
    data = common.read_json(p)
    rooms = data.get("rooms") if isinstance(data, dict) else None
    if not isinstance(rooms, list):
        raise common.ValidationErrors([f"{common.rel(p)}: needs a 'rooms' list."])
    out: dict = {}
    for r in rooms:
        if isinstance(r, dict) and common.is_slug(r.get("slug")) and r.get("status", "kept") == "kept":
            out[r["slug"]] = r
    if not out:
        raise common.ValidationErrors([f"{common.rel(p)}: no kept rooms. Fix Stage 1 first."])
    return out


def ledger_ids(ledger=None) -> dict:
    ledger = ledger if ledger is not None else common.load_ledger()
    reach = ledger.get("reach") or {}

    def by_id(items):
        out = {}
        for it in items or []:
            if isinstance(it, dict) and it.get("id"):
                out[str(it["id"])] = it
        return out

    return {
        "warm": by_id(reach.get("warm")),
        "search": by_id(reach.get("search")),
        "depth": by_id(ledger.get("depth")),
        "exclusions": by_id(ledger.get("exclusions")),
        "ventures": by_id(ledger.get("existing_ventures")),
    }


# --------------------------------------------------------------------------- validation
def _is_bool(v) -> bool:
    return isinstance(v, bool)


def validate_entry(entry: dict, where: str, ids: dict) -> list:
    errors: list = []
    reach = entry.get("reach")
    if not isinstance(reach, dict):
        errors.append(f"{where}: 'reach' must be an object with kind, ledger_id, evidence_url, reasoning, confidence.")
    else:
        kind = reach.get("kind")
        if kind not in ("warm", "search", None):
            errors.append(f"{where}: reach.kind must be warm, search or null (got {kind!r}).")
        lid = reach.get("ledger_id")
        if kind == "warm" and lid not in ids["warm"]:
            errors.append(f"{where}: reach.ledger_id {lid!r} is not a warm path id "
                          f"({', '.join(sorted(ids['warm'])) or 'none in the ledger'}).")
        if kind == "search":
            if lid not in ids["search"]:
                errors.append(f"{where}: search reach needs reach.ledger_id {', '.join(sorted(ids['search'])) or 's1'} (got {lid!r}).")
            url = reach.get("evidence_url")
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                errors.append(f"{where}: search reach needs reach.evidence_url (a page showing this room buying "
                              f"this kind of product through search, an app store or a marketplace).")
        errors.extend(common.check_judgment(reach, f"{where}: reach"))
    depth = entry.get("depth")
    if not isinstance(depth, dict):
        errors.append(f"{where}: 'depth' must be an object with ledger_id, reasoning, confidence.")
    else:
        did = depth.get("ledger_id")
        if did is not None and did not in ids["depth"]:
            errors.append(f"{where}: depth.ledger_id {did!r} is not a ledger depth id "
                          f"({', '.join(sorted(ids['depth']))}) or null.")
        errors.extend(common.check_judgment(depth, f"{where}: depth"))
    spend = entry.get("spend")
    if not isinstance(spend, list):
        errors.append(f"{where}: 'spend' must be a list of price items (use [] when none was found).")
    else:
        for i, item in enumerate(spend, 1):
            errors.extend(common.check_price(item, f"{where}: spend item {i}"))
    supply = entry.get("supply")
    if not isinstance(supply, dict):
        errors.append(f"{where}: 'supply' must be an object with blocked, needs, reasoning, confidence.")
    else:
        if not _is_bool(supply.get("blocked")):
            errors.append(f"{where}: supply.blocked must be true or false.")
        needs = supply.get("needs")
        if not isinstance(needs, list):
            errors.append(f"{where}: supply.needs must be a list (use [] when nothing is missing).")
        else:
            for n in needs:
                if n not in NEEDS:
                    errors.append(f"{where}: supply.needs {n!r} is not one of {', '.join(NEEDS)}.")
        errors.extend(common.check_judgment(supply, f"{where}: supply"))
    excl = entry.get("excluded")
    if not isinstance(excl, dict):
        errors.append(f"{where}: 'excluded' must be an object with is_excluded, exclusion_id, reasoning, confidence.")
    else:
        if not _is_bool(excl.get("is_excluded")):
            errors.append(f"{where}: excluded.is_excluded must be true or false.")
        xid = excl.get("exclusion_id")
        if xid is not None and xid not in ids["exclusions"]:
            errors.append(f"{where}: excluded.exclusion_id {xid!r} is not a ledger exclusion id "
                          f"({', '.join(sorted(ids['exclusions']))}) or null.")
        if excl.get("is_excluded") is True and xid is None:
            errors.append(f"{where}: an excluded room needs excluded.exclusion_id (which ledger exclusion applies).")
        errors.extend(common.check_judgment(excl, f"{where}: excluded"))
    trust = entry.get("trust_needed")
    if not isinstance(trust, dict):
        errors.append(f"{where}: 'trust_needed' must be an object with value, reasoning, confidence.")
    else:
        if not _is_bool(trust.get("value")):
            errors.append(f"{where}: trust_needed.value must be true or false.")
        errors.extend(common.check_judgment(trust, f"{where}: trust_needed"))
    return errors


# --------------------------------------------------------------------------- tests
def run_tests(entry: dict, room: dict, ids: dict, rules: dict, price_results: list) -> tuple:
    """The six tests for one room. Returns ({test: {"pass", "reason"}}, points)."""
    s2 = rules.get("stage2") or {}
    reach_kinds = [str(k) for k in (s2.get("reach_kinds") or ["warm", "search"])]
    tests: dict = {}
    reach = entry["reach"]
    kind = reach.get("kind")
    if kind is None:
        tests["reach"] = {"pass": False, "reason": "no reach: the founder has no warm path here and the room does not buy this kind of product through search, app stores or marketplaces"}
    elif kind not in reach_kinds:
        tests["reach"] = {"pass": False, "reason": f"reach kind {kind} is not allowed (allowed: {', '.join(reach_kinds)})"}
    elif kind == "warm":
        w = ids["warm"].get(reach.get("ledger_id"), {})
        tests["reach"] = {"pass": True, "reason": f"warm path {reach.get('ledger_id')}: {w.get('covers') or w.get('text', '')}"}
    else:
        tests["reach"] = {"pass": True, "reason": f"search reach ({reach.get('ledger_id')}); evidence: {reach.get('evidence_url')}"}

    depth_id = entry["depth"].get("ledger_id")
    must_match = bool(s2.get("depth_must_match_ledger", True))
    if depth_id in ids["depth"]:
        d = ids["depth"][depth_id]
        tests["depth"] = {"pass": True, "reason": f"{depth_id}: {d.get('domain') or d.get('text', '')} ({d.get('strength', '?')})"}
    elif not must_match:
        tests["depth"] = {"pass": True, "reason": "no ledger depth match, but depth_must_match_ledger is off"}
    else:
        tests["depth"] = {"pass": False, "reason": "no ledger depth domain matches this room (depth.ledger_id is null)"}

    n_items = len(price_results)
    n_spend = sum(1 for r in price_results if prices.counts_as_spend(r["status"]))
    n_verified = sum(1 for r in price_results if r["status"] == "found")
    require_spend = bool(s2.get("require_measured_spend", True))
    if n_spend >= 1:
        tests["spend"] = {"pass": True, "reason": f"{n_spend} price(s) with a URL ({n_verified} confirmed on the page, "
                                                   f"{n_spend - n_verified} not checked)"}
    elif not require_spend:
        tests["spend"] = {"pass": True, "reason": "no measured spend, but require_measured_spend is off"}
    elif n_items == 0:
        tests["spend"] = {"pass": False, "reason": "no spend item: no concrete price with a URL was given"}
    else:
        tests["spend"] = {"pass": False, "reason": f"{n_items} spend item(s), none confirmed: the price text was not found on the page"}

    steps = len(room.get("ladder") or [])
    min_steps = int(s2.get("min_ladder_steps", 3))
    tests["ladder"] = {"pass": steps >= min_steps,
                       "reason": f"{steps} ladder step(s); needs at least {min_steps}" if steps < min_steps
                       else f"{steps} ladder steps (at least {min_steps} needed)"}

    supply = entry["supply"]
    if supply.get("blocked"):
        needs = ", ".join(supply.get("needs") or []) or "something the ledger says the founder lacks"
        tests["supply"] = {"pass": False, "reason": f"blocked: the room's core pains need {needs}"}
    else:
        tests["supply"] = {"pass": True, "reason": "nothing needed that the founder lacks and cannot rent"}

    excl = entry["excluded"]
    if excl.get("is_excluded"):
        x = ids["exclusions"].get(excl.get("exclusion_id"), {})
        tests["exclusions"] = {"pass": False, "reason": f"excluded by {excl.get('exclusion_id')}: {x.get('text', '')}"}
    else:
        tests["exclusions"] = {"pass": True, "reason": "no ledger exclusion applies"}

    # Ladder steps that carry a price seen at a URL: evidence that the step is really paid.
    priced = sum(1 for st in (room.get("ladder") or []) if st.get("price_text") and st.get("url"))
    points = {"ladder_steps": steps, "spend_points": n_spend, "spend_points_verified": n_verified,
              "priced_ladder_steps": priced, "warm_reach": kind == "warm"}
    return tests, points


def rank_key(verdict: dict, rank_by) -> tuple:
    key: list = []
    for name in rank_by:
        if name == "ladder_steps":
            key.append(-int(verdict["ladder_steps"]))
        elif name == "spend_points_verified":
            key.append(-int(verdict["spend_points_verified"]))
        elif name == "spend_points":
            key.append(-int(verdict["spend_points"]))
        elif name == "priced_ladder_steps":
            key.append(-int(verdict.get("priced_ladder_steps", 0)))
        elif name == "warm_reach":
            key.append(0 if verdict["reach_kind"] == "warm" else 1)
    key.append(verdict["slug"])
    return tuple(key)


# --------------------------------------------------------------------------- the mask
def mask(run, merge_parts_flag: bool = False, max_rooms=None) -> dict:
    rd = common.run_dir(run)
    rules = common.load_kill_rules()
    s2 = rules.get("stage2") or {}
    ledger = common.load_ledger()
    ids = ledger_ids(ledger)
    rooms = load_rooms(run)
    _data, fx, fx_warnings = validate_fx(run)

    merged_path = rd / "02_mask_input.json"
    if merge_parts_flag:
        merged = merge_parts(run)
        common.write_json(merged_path, {"rooms": [{k: v for k, v in e.items() if not k.startswith("_")} for e in merged["rooms"]],
                                        "parts": merged["parts"]})
        entries = merged["rooms"]
    else:
        common.require_file(merged_path, "Run `funnel mask --merge-parts` to build it from RUN/02_mask.parts/.")
        data = common.read_json(merged_path)
        entries = data.get("rooms") if isinstance(data, dict) else None
        if not isinstance(entries, list):
            raise common.ValidationErrors([f"{common.rel(merged_path)}: needs a 'rooms' list."])
        entries = [dict(e) for e in entries if isinstance(e, dict)]

    errors: list = []
    warnings: list = list(fx_warnings)
    by_slug: dict = {}
    index_in_part: dict = {}
    for entry in entries:
        part = entry.get("_part") or "02_mask_input.json"
        index_in_part[part] = index_in_part.get(part, 0) + 1
        where = f"{part}: room {index_in_part[part]} ({entry.get('slug', '?')})"
        slug = entry.get("slug")
        if not common.is_slug(slug):
            errors.append(f"{where}: 'slug' must be a valid slug.")
            continue
        if slug not in rooms:
            errors.append(f"{where}: {slug} is not a kept room in 01_rooms.json. Use the slugs from 01_rooms.md.")
            continue
        if slug in by_slug:
            errors.append(f"{where}: {slug} appears twice across the parts. Keep one entry.")
            continue
        errors.extend(validate_entry(entry, where, ids))
        by_slug[slug] = entry
    missing = sorted(s for s in rooms if s not in by_slug)
    if missing:
        msg = (f"02_mask.parts: {len(missing)} kept room(s) have no mask entry: {', '.join(missing)}. "
               f"Every room in 01_rooms.json needs a verdict.")
        if common.is_dry_run():
            warnings.append(msg + " (dry run: they were skipped)")
        else:
            errors.append(msg)
    if errors:
        raise common.ValidationErrors(errors)

    # price check on every spend item (offline -> blocked_by_network, kept as [measured, page not checked])
    items = []
    for slug in sorted(by_slug):
        for i, item in enumerate(by_slug[slug].get("spend") or [], 1):
            items.append((f"room {slug} spend item {i}", item))
    checked = prices.check_items(run, STAGE, "mask", items)
    price_by_where = {r["where"]: r for r in checked["items"]}

    max_keep = int(max_rooms if max_rooms is not None else s2.get("max_rooms", 15))
    if max_keep < 1:
        raise common.ValidationErrors(["--max-rooms must be at least 1."])
    rank_by = [str(x) for x in (s2.get("rank_by") or DEFAULT_RANK_BY)]
    warn_below = int(s2.get("warn_below_rooms", 5))

    verdicts: list = []
    for slug in sorted(by_slug):
        entry = by_slug[slug]
        room = rooms[slug]
        spend_out = []
        results = []
        for i, item in enumerate(entry.get("spend") or [], 1):
            r = price_by_where[f"room {slug} spend item {i}"]
            results.append(r)
            it = dict(item)
            it["price_status"] = r["status"]
            it["price_tag"] = r["tag"]
            it["price_detail"] = r["detail"]
            it["amount_usd"] = round(common.to_usd(item["amount"], item["currency"], fx), 2)
            spend_out.append(it)
        tests, points = run_tests(entry, room, ids, rules, results)
        failed = [t for t in TESTS if not tests[t]["pass"]]
        reach = entry["reach"]
        depth_id = entry["depth"].get("ledger_id")
        depth = ids["depth"].get(depth_id, {}) if depth_id else {}
        xid = entry["excluded"].get("exclusion_id")
        v = {
            "slug": slug,
            "name": room.get("name", slug),
            "lens": room.get("lens"),
            "status": "killed" if failed else "survived",
            "rank": None,
            "failed_tests": failed,
            "tests": tests,
            "reach_kind": reach.get("kind"),
            "reach_ledger_id": reach.get("ledger_id"),
            "evidence_url": reach.get("evidence_url"),
            "depth_ledger_id": depth_id,
            "depth_strength": depth.get("strength"),
            "ladder_steps": points["ladder_steps"],
            "spend_points": points["spend_points"],
            "spend_points_verified": points["spend_points_verified"],
            "priced_ladder_steps": points["priced_ladder_steps"],
            "spend": spend_out,
            "supply_blocked": bool(entry["supply"].get("blocked")),
            "supply_needs": list(entry["supply"].get("needs") or []),
            "is_excluded": bool(entry["excluded"].get("is_excluded")),
            "exclusion_id": xid,
            "trust_needed": bool(entry["trust_needed"].get("value")),
            "trust_flag": reach.get("kind") == "search" and bool(entry["trust_needed"].get("value")),
            "venture_overlap": list(room.get("venture_overlap") or []),
            "employer_overlap": (reach.get("kind") == "warm" and reach.get("ledger_id") in EMPLOYER_WARM_IDS)
                                or xid == EMPLOYER_EXCLUSION_ID,
            "reach": {k: v for k, v in reach.items()},
            "depth": {k: v for k, v in entry["depth"].items()},
            "supply": {k: v for k, v in entry["supply"].items()},
            "excluded": {k: v for k, v in entry["excluded"].items()},
            "trust_needed_judgment": {k: v for k, v in entry["trust_needed"].items()},
        }
        verdicts.append(v)

    survivors = sorted((v for v in verdicts if not v["failed_tests"]), key=lambda v: rank_key(v, rank_by))
    for i, v in enumerate(survivors, 1):
        v["rank"] = i
        v["status"] = "kept" if i <= max_keep else "cut"
    killed = sorted((v for v in verdicts if v["failed_tests"]), key=lambda v: v["slug"])
    kept = [v for v in survivors if v["status"] == "kept"]
    cut = [v for v in survivors if v["status"] == "cut"]

    date = common.run_date(run)
    kills: dict = {}
    for v in killed:
        kills[f"room:{v['slug']}"] = "failed " + "; ".join(f"{t}: {v['tests'][t]['reason']}" for t in v["failed_tests"])
    for v in cut:
        kills[f"room:{v['slug']}"] = (f"cut: ranked {v['rank']} of {len(survivors)} survivors and max_rooms is {max_keep}; "
                                     f"passed every test (ladder {v['ladder_steps']}, spend {v['spend_points_verified']}/{v['spend_points']}, "
                                     f"reach {v['reach_kind']})")
    # the graveyard says exactly what this run of the mask killed: a room a rerun keeps loses its same-date line
    common.sync_graveyard(date, STAGE, [f"room:{v['slug']}" for v in verdicts], kills)
    if common.is_dry_run() and kills:
        common.log_event(run, STAGE, "mask", "note", review=False, dry_run=True,
                         note="dry run: no graveyard line was written for " + ", ".join(sorted(kills)))

    review_notes: list = []
    if len(survivors) < warn_below:
        near = [v["slug"] for v in killed if set(v["failed_tests"]) <= {"depth", "supply"}]
        review_notes.append(f"Only {len(survivors)} room(s) passed the mask; fewer than {warn_below}. Rooms that failed "
                            f"only on depth and/or supply: {', '.join(near) or 'none'}.")
    trust_rooms = [v["slug"] for v in kept if v["trust_flag"]]
    if trust_rooms:
        review_notes.append(f"Search-reach rooms whose product needs trust: {', '.join(trust_rooms)}. Search reach suits "
                            f"self-serve products; a product that needs trust usually needs a warm path.")
    employer_rooms = [v["slug"] for v in kept if v["employer_overlap"]]
    if employer_rooms:
        review_notes.append(f"Rooms that overlap the founder's job (warm path w2/w4 or exclusion x2): "
                            f"{', '.join(employer_rooms)}. Check the employer's outside-business rules before pursuing.")
    venture_rooms = [f"{v['slug']} ({', '.join(v['venture_overlap'])})" for v in kept if v["venture_overlap"]]
    if venture_rooms:
        review_notes.append(f"Kept rooms that touch existing ventures (tagged, not excluded): {'; '.join(venture_rooms)}.")
    for note in review_notes:
        common.log_event(run, STAGE, "mask", "note", note=note, review=True)
    for w in warnings:
        common.log_event(run, STAGE, "mask", "note", note=w, review=False)

    result = {
        "max_rooms": max_keep,
        "rank_by": rank_by,
        "counts": {"in": len(verdicts), "survived": len(survivors), "kept": len(kept), "cut": len(cut), "killed": len(killed)},
        "kept": [v["slug"] for v in kept],
        "cut": [v["slug"] for v in cut],
        "killed": [v["slug"] for v in killed],
        "rooms": kept + cut + killed,
        "review_notes": review_notes,
        "warnings": warnings,
        "price_check": {"counts": checked["counts"], "blocked_domains": checked["blocked_domains"]},
        "test_meaning": TEST_MEANING,
    }
    common.write_json(rd / "02_mask.json", result)
    common.write_text(rd / "02_mask.md", render_md(result, run))
    common.log_event(run, STAGE, "mask", "count", rooms_in=len(verdicts), survived=len(survivors), kept=len(kept),
                     cut=len(cut), killed=len(killed), max_rooms=max_keep,
                     failed_by_test={t: sum(1 for v in killed if t in v["failed_tests"]) for t in TESTS})
    return result


# --------------------------------------------------------------------------- rendering
def _cell(s) -> str:
    return common.normalize_ws(str(s if s is not None else "")).replace("|", "/")


def _flags(v: dict) -> str:
    flags = []
    if v["trust_flag"]:
        flags.append("needs trust (search reach)")
    if v["employer_overlap"]:
        flags.append("employer overlap")
    if v["venture_overlap"]:
        flags.append("ventures: " + ", ".join(v["venture_overlap"]))
    return "; ".join(flags) or "none"


def render_md(result: dict, run) -> str:
    c = result["counts"]
    lines = [
        "# Stage 2: room mask",
        "",
        f"Run: {common.run_name(run)}.",
        f"{c['in']} rooms tested. {c['survived']} passed every test. {c['kept']} kept (at most {result['max_rooms']}), "
        f"{c['cut']} cut for rank, {c['killed']} killed.",
        "",
        "A room passes only if all six tests pass:",
        "",
    ]
    for t in TESTS:
        lines.append(f"- **{t}**: {TEST_MEANING[t]}.")
    lines += ["", f"Survivors are ranked by {', '.join(result['rank_by'])}, then slug. "
                  "Spend points count prices with a URL; verified spend points count prices found on the page itself. "
                  "`[measured, page not checked]` means the price was read in a search result or the page could not be opened."]
    lines += ["", f"## Kept rooms ({c['kept']})", ""]
    if result["kept"]:
        lines.append("| Rank | Room | Reach | Depth | Ladder steps | Spend (verified/all) | Flags |")
        lines.append("|---|---|---|---|---|---|---|")
        for v in result["rooms"]:
            if v["status"] != "kept":
                continue
            reach = f"{v['reach_kind']} ({v['reach_ledger_id']})"
            depth = f"{v['depth_ledger_id']} ({v['depth_strength']})" if v["depth_ledger_id"] else "none"
            lines.append(f"| {v['rank']} | {v['slug']} | {reach} | {depth} | {v['ladder_steps']} | "
                         f"{v['spend_points_verified']}/{v['spend_points']} | {_cell(_flags(v))} |")
        for v in result["rooms"]:
            if v["status"] != "kept":
                continue
            lines += ["", f"### {v['rank']}. {_cell(v['name'])} (`{v['slug']}`)", ""]
            lines.append(f"- Reach: {_cell(v['tests']['reach']['reason'])}. {_cell(v['reach'].get('reasoning'))} "
                         f"(confidence {v['reach'].get('confidence')})")
            lines.append(f"- Depth: {_cell(v['tests']['depth']['reason'])}. {_cell(v['depth'].get('reasoning'))}")
            lines.append(f"- Supply: {_cell(v['tests']['supply']['reason'])}. {_cell(v['supply'].get('reasoning'))}")
            lines.append(f"- Trust needed: {'yes' if v['trust_needed'] else 'no'}. {_cell(v['trust_needed_judgment'].get('reasoning'))}")
            if v["spend"]:
                lines.append("- Spend evidence:")
                for it in v["spend"]:
                    lines.append(f"  - {_cell(it.get('what'))}: {_cell(it.get('price_text'))} ({it.get('currency')} "
                                 f"{it.get('amount')} per {it.get('unit')}, about USD {it['amount_usd']:,.2f}) {it['price_tag']} "
                                 f"<{it.get('url')}>")
            else:
                lines.append("- Spend evidence: none given.")
    else:
        lines.append("No room passed every test.")
    lines += ["", f"## Cut for rank ({c['cut']})", ""]
    if result["cut"]:
        lines.append("These rooms passed every test but ranked below the limit. They are in graveyard.md.")
        lines.append("")
        for v in result["rooms"]:
            if v["status"] == "cut":
                lines.append(f"- rank {v['rank']}: {v['slug']} (ladder {v['ladder_steps']}, spend "
                             f"{v['spend_points_verified']}/{v['spend_points']}, reach {v['reach_kind']})")
    else:
        lines.append("None.")
    lines += ["", f"## Killed rooms ({c['killed']})", ""]
    if result["killed"]:
        lines.append("| Room | Failed tests | Why |")
        lines.append("|---|---|---|")
        for v in result["rooms"]:
            if v["status"] == "killed":
                why = "; ".join(f"{t}: {v['tests'][t]['reason']}" for t in v["failed_tests"])
                lines.append(f"| {v['slug']} | {', '.join(v['failed_tests'])} | {_cell(why)} |")
    else:
        lines.append("None.")
    lines += ["", "## For REVIEW.md", ""]
    if result["review_notes"]:
        lines += [f"- {n}" for n in result["review_notes"]]
    else:
        lines.append("Nothing to flag.")
    pc = result["price_check"]
    lines += ["", "## Price checks", ""]
    lines.append("Counts: " + (", ".join(f"{k} {v}" for k, v in sorted(pc["counts"].items())) or "no spend items") + ".")
    if pc["blocked_domains"]:
        lines.append("Domains to allow so the price pages can be opened: " + ", ".join(pc["blocked_domains"]) + ".")
    if result["warnings"]:
        lines += ["", "## Warnings", ""]
        lines += [f"- {w}" for w in result["warnings"]]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- commands
def cmd_mask(args) -> int:
    run = common.run_dir(args.run)
    result = mask(run, merge_parts_flag=args.merge_parts, max_rooms=args.max_rooms)
    c = result["counts"]
    print(f"Mask: {c['in']} rooms in, {c['survived']} passed, {c['kept']} kept (max {result['max_rooms']}), "
          f"{c['cut']} cut, {c['killed']} killed.")
    for v in result["rooms"]:
        if v["status"] == "kept":
            print(f"  kept #{v['rank']}: {v['slug']} (ladder {v['ladder_steps']}, spend {v['spend_points_verified']}/{v['spend_points']}, "
                  f"reach {v['reach_kind']}, flags: {_flags(v)})")
    for v in result["rooms"]:
        if v["status"] == "cut":
            print(f"  cut #{v['rank']}: {v['slug']}")
    for v in result["rooms"]:
        if v["status"] == "killed":
            print(f"  killed: {v['slug']}: failed {', '.join(v['failed_tests'])}")
    for n in result["review_notes"]:
        print(f"review: {n}")
    for w in result["warnings"]:
        print(f"warning: {w}")
    if result["price_check"]["blocked_domains"]:
        print("Domains to allow for price pages: " + ", ".join(result["price_check"]["blocked_domains"]))
    print(f"Wrote {common.rel(run / '02_mask.json')}, {common.rel(run / '02_mask.md')} and graveyard.md")
    return 0


def register(subparsers) -> None:
    f = subparsers.add_parser("fx", help="Validate RUN/fx_rates.json and print the table.")
    f.set_defaults(func=cmd_fx, stage_no=STAGE)
    m = subparsers.add_parser("mask", help="Apply the Stage 2 tests, rank rooms, keep at most max_rooms; write 02_mask.json and 02_mask.md.")
    m.add_argument("--merge-parts", action="store_true", help="read RUN/02_mask.parts/*.json into 02_mask_input.json first")
    m.add_argument("--max-rooms", type=int, default=None, help="keep at most this many rooms (default: kill_rules stage2.max_rooms)")
    m.set_defaults(func=cmd_mask, stage_no=STAGE)
