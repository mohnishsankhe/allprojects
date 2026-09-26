"""Stage 1: merge, validate and dedupe the rooms (command `rooms`).

Rooms are written by the model in RUN/01_rooms.parts/<lens>.json, gap_<lens>.json
and external.json. This script merges them, checks every field against
config/formats.md, removes rooms dead in graveyard.md (unless revived), removes
exact duplicates and rooms marked `duplicate_of`, lists near-duplicates, checks
the counts (80–120 rooms, a minimum per lens) and writes 01_rooms.json and
01_rooms.md. Geography is never checked against anything (rule 14).

Public API
----------
    ORIGINS = ("generated", "gap_pass", "external")
    lens_order(rules=None) -> list[str]           the six lenses, in kill-rule order
    parts_dir(run) -> Path
    part_order_key(name, lenses) -> tuple         lens files first (lens order), then gap_<lens>, then external
    load_parts(run) -> (rooms, part_names)        every room with "_part" set to its file name
    validate_room(room, where, venture_ids) -> list[str]
    normalized_name(name) -> str                  lower case, punctuation removed, one space between words
    name_tokens(name) -> set[str]                 words of the normalized name without stopwords
    jaccard(a, b) -> float
    normalize_url(url) -> str                     for the shared-`where` check
    process_rooms(run, rooms, rules=None) -> dict  graveyard, duplicates, near-duplicates, counts (no files written)
    render_md(result, run) -> str
    rooms_command(run, merge_parts) -> dict       process and write 01_rooms.json + 01_rooms.md
    register(subparsers)                          adds `rooms [--merge-parts]`
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import common

STAGE = 1
ORIGINS = ("generated", "gap_pass", "external")
DEFAULT_LENSES = ["life_stage", "profession", "transition", "obligation", "business_type", "identity_community"]
STOPWORDS = frozenset({
    "a", "an", "and", "are", "as", "at", "by", "for", "from", "in", "into", "is", "of", "on", "or", "the", "their",
    "to", "who", "whose", "with", "that", "this", "these", "those", "its", "it", "be", "being", "they", "them",
})
NEAR_DUPLICATE_JACCARD = 0.6
_NON_WORD_RE = re.compile(r"[^0-9a-z]+")


# --------------------------------------------------------------------------- helpers
def lens_order(rules=None) -> list:
    rules = rules if rules is not None else common.load_kill_rules()
    lenses = (rules.get("stage1") or {}).get("lenses")
    if isinstance(lenses, list) and lenses:
        return [str(x) for x in lenses]
    return list(DEFAULT_LENSES)


def parts_dir(run) -> Path:
    return common.run_dir(run) / "01_rooms.parts"


def part_order_key(name: str, lenses) -> tuple:
    stem = Path(name).stem
    if stem in lenses:
        return (0, lenses.index(stem), stem)
    if stem.startswith("gap_") and stem[4:] in lenses:
        return (1, lenses.index(stem[4:]), stem)
    if stem == "external":
        return (2, 0, stem)
    return (3, 0, stem)


def normalized_name(name) -> str:
    s = unicodedata.normalize("NFKC", str(name or "")).lower()
    s = _NON_WORD_RE.sub(" ", s)
    return common.normalize_ws(s)


def name_tokens(name) -> set:
    return {t for t in normalized_name(name).split() if t not in STOPWORDS}


def jaccard(a, b) -> float:
    a, b = set(a), set(b)
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def normalize_url(url) -> str:
    s = str(url or "").strip().lower()
    s = re.sub(r"^https?://", "", s)
    s = re.sub(r"^www\.", "", s)
    s = s.split("#", 1)[0]
    return s.rstrip("/")


def _slugify(name) -> str:
    return "-".join(normalized_name(name).split())


# --------------------------------------------------------------------------- inputs
def load_parts(run) -> tuple:
    d = parts_dir(run)
    lenses = lens_order()
    files = sorted((p for p in d.glob("*.json") if p.is_file()), key=lambda p: part_order_key(p.name, lenses)) if d.exists() else []
    if not files:
        raise common.MissingInput(f"No part files in {common.rel(d)}/. The lens agents write <lens>.json, "
                                  f"gap_<lens>.json and external.json there (see config/formats.md, Stage 1).")
    rooms: list = []
    errors: list = []
    for p in files:
        try:
            data = common.read_json(p)
        except ValueError as e:  # json.JSONDecodeError is a ValueError
            errors.append(f"{common.rel(p)}: not valid JSON ({e}). Fix the file.")
            continue
        if isinstance(data, dict):
            part_rooms = data.get("rooms")
        else:
            part_rooms = data
        if not isinstance(part_rooms, list):
            errors.append(f"{common.rel(p)}: needs a 'rooms' list.")
            continue
        for i, room in enumerate(part_rooms, 1):
            if not isinstance(room, dict):
                errors.append(f"{common.rel(p)}: room {i}: must be an object.")
                continue
            r = dict(room)
            r["_part"] = p.name
            rooms.append(r)
    if errors:
        raise common.ValidationErrors(errors)
    return rooms, [p.name for p in files]


# --------------------------------------------------------------------------- validation
def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def validate_room(room: dict, where: str, venture_ids, lenses=None) -> list:
    """Every problem with one room, in plain English. Geography is never checked."""
    lenses = lenses or DEFAULT_LENSES
    errors: list = []
    slug = room.get("slug")
    if not common.is_slug(slug):
        errors.append(f"{where}: 'slug' {slug!r} must use lowercase letters, digits and hyphens only.")
    if not _nonempty_str(room.get("name")):
        errors.append(f"{where}: 'name' is missing or empty.")
    if room.get("lens") not in lenses:
        errors.append(f"{where}: 'lens' must be one of {', '.join(lenses)} (got {room.get('lens')!r}).")
    if room.get("origin") not in ORIGINS:
        errors.append(f"{where}: 'origin' must be generated, gap_pass or external (got {room.get('origin')!r}).")
    for field in ("who", "who_pays"):
        if not _nonempty_str(room.get(field)):
            errors.append(f"{where}: '{field}' is missing or empty.")
    where_list = room.get("where")
    if not isinstance(where_list, list) or not where_list:
        errors.append(f"{where}: 'where' must be a non-empty list of places, each with 'name' and 'url'.")
    else:
        for i, place in enumerate(where_list, 1):
            if not isinstance(place, dict) or not _nonempty_str(place.get("name")):
                errors.append(f"{where}: where[{i}]: needs a 'name'.")
            url = place.get("url") if isinstance(place, dict) else None
            if not isinstance(url, str) or not url.startswith(("http://", "https://")):
                errors.append(f"{where}: where[{i}]: 'url' must start with http:// or https://.")
    size = room.get("size")
    errors.extend(common.check_number(size, f"{where}: size"))
    if isinstance(size, dict) and not _nonempty_str(size.get("unit")):
        errors.append(f"{where}: size: 'unit' is missing (for example 'test takers per year').")
    ladder = room.get("ladder")
    if not isinstance(ladder, list):
        errors.append(f"{where}: 'ladder' must be a list of steps ({{'step', 'problem', 'price_text', 'url'}}).")
    else:
        for i, step in enumerate(ladder, 1):
            if not isinstance(step, dict):
                errors.append(f"{where}: ladder step {i}: must be an object.")
                continue
            n = step.get("step")
            if not isinstance(n, int) or isinstance(n, bool) or n != i:
                errors.append(f"{where}: ladder step {i}: 'step' must be {i} (steps are numbered 1, 2, 3 in order; got {n!r}).")
            if not _nonempty_str(step.get("problem")):
                errors.append(f"{where}: ladder step {i}: 'problem' is missing or empty.")
            pt = step.get("price_text")
            if pt is not None and not isinstance(pt, str):
                errors.append(f"{where}: ladder step {i}: 'price_text' must be text or null.")
            url = step.get("url")
            if url is not None and (not isinstance(url, str) or not url.startswith(("http://", "https://"))):
                errors.append(f"{where}: ladder step {i}: 'url' must start with http:// or https://, or be left out.")
    vo = room.get("venture_overlap")
    if not isinstance(vo, list):
        errors.append(f"{where}: 'venture_overlap' must be a list of ledger venture ids (use [] for none).")
    else:
        for vid in vo:
            if vid not in venture_ids:
                errors.append(f"{where}: venture_overlap id {vid!r} is not in config/ledger.yaml "
                              f"(known: {', '.join(venture_ids) or 'none'}).")
    dup = room.get("duplicate_of")
    if dup is not None and not common.is_slug(dup):
        errors.append(f"{where}: 'duplicate_of' must be null or the slug of the room this one duplicates.")
    errors.extend(common.check_judgment(room, where))
    return errors


def _venture_ids(ledger=None) -> list:
    ledger = ledger if ledger is not None else common.load_ledger()
    out = []
    for v in ledger.get("existing_ventures") or []:
        if isinstance(v, dict) and v.get("id"):
            out.append(str(v["id"]))
    return out


# --------------------------------------------------------------------------- processing
def _sort_key(room: dict, lenses, order_index: int) -> tuple:
    lens_i = lenses.index(room["lens"]) if room.get("lens") in lenses else len(lenses)
    origin_i = ORIGINS.index(room["origin"]) if room.get("origin") in ORIGINS else len(ORIGINS)
    return (lens_i, origin_i, order_index)


def _clean(room: dict) -> dict:
    out = {k: v for k, v in room.items() if not k.startswith("_")}
    geo = out.get("geography")
    if geo is None:
        out["geography"] = []
    elif isinstance(geo, str):
        out["geography"] = [geo]
    elif not isinstance(geo, list):
        out["geography"] = [str(geo)]
    out.setdefault("duplicate_of", None)
    return out


def process_rooms(run, rooms: list, rules=None) -> dict:
    """Validate, remove dead and duplicate rooms, list near-duplicates, check counts. Writes nothing."""
    rules = rules if rules is not None else common.load_kill_rules()
    s1 = rules.get("stage1") or {}
    lenses = lens_order(rules)
    venture_ids = _venture_ids()
    errors: list = []
    warnings: list = []

    index_in_part: dict = {}
    for room in rooms:
        part = room.get("_part") or "01_rooms.json"
        index_in_part[part] = index_in_part.get(part, 0) + 1
        where = f"{part}: room {index_in_part[part]} ({room.get('slug', '?')})"
        errors.extend(validate_room(room, where, venture_ids, lenses))
        part = room.get("_part") or ""
        stem = Path(part).stem
        file_lens = stem[4:] if stem.startswith("gap_") else stem
        if file_lens in lenses and room.get("lens") in lenses and room["lens"] != file_lens:
            warnings.append(f"{where}: lens is {room['lens']} but the file is for {file_lens}. The room's own lens is used.")
    if errors:
        raise common.ValidationErrors(errors)

    ordered = sorted(enumerate(rooms), key=lambda t: _sort_key(t[1], lenses, t[0]))
    ordered_rooms = [r for _, r in ordered]
    all_slugs = {r["slug"] for r in ordered_rooms}

    dead = common.dead_items("room")
    dead_slugs = {item.split(":", 1)[1] for item in dead}
    grave_by_item = {}
    for e in common.parse_graveyard():
        if e["item"] in dead:
            grave_by_item.setdefault(e["item"], e)

    removed: list = []
    kept: list = []
    seen_slug: dict = {}
    seen_name: dict = {}
    for room in ordered_rooms:
        slug = room["slug"]
        nname = normalized_name(room["name"])
        dead_hit = None
        for cand in (slug, _slugify(room["name"])):
            if cand in dead_slugs:
                dead_hit = cand
                break
        if dead_hit:
            g = grave_by_item.get(f"room:{dead_hit}") or {}
            removed.append({"slug": slug, "name": room["name"], "lens": room["lens"], "origin": room["origin"],
                            "part": room.get("_part"), "status": "graveyard", "of": None,
                            "reason": f"dead in graveyard.md since {g.get('date', '?')} ({g.get('stage', '?')}): "
                                      f"{g.get('reason', 'no reason recorded')}. Revive it with a new-evidence line first."})
            continue
        if room.get("duplicate_of"):
            target = room["duplicate_of"]
            if target not in all_slugs:
                errors.append(f"{room.get('_part') or '01_rooms.json'}: room {slug}: duplicate_of {target!r} is not a "
                              f"slug in the parts. Point it at an existing room or set it to null.")
                continue
            if target == slug:
                errors.append(f"{room.get('_part') or '01_rooms.json'}: room {slug}: duplicate_of points at itself.")
                continue
            removed.append({"slug": slug, "name": room["name"], "lens": room["lens"], "origin": room["origin"],
                            "part": room.get("_part"), "status": "duplicate_of", "of": target,
                            "reason": f"marked duplicate_of {target}"})
            continue
        if slug in seen_slug:
            removed.append({"slug": slug, "name": room["name"], "lens": room["lens"], "origin": room["origin"],
                            "part": room.get("_part"), "status": "duplicate", "of": seen_slug[slug],
                            "reason": f"same slug as {seen_slug[slug]} (kept the first by lens order, then origin order)"})
            continue
        if nname in seen_name:
            removed.append({"slug": slug, "name": room["name"], "lens": room["lens"], "origin": room["origin"],
                            "part": room.get("_part"), "status": "duplicate", "of": seen_name[nname],
                            "reason": f"same name as {seen_name[nname]} (kept the first by lens order, then origin order)"})
            continue
        seen_slug[slug] = slug
        seen_name[nname] = slug
        kept.append(room)
    if errors:
        raise common.ValidationErrors(errors)
    removed.sort(key=lambda x: (x["slug"], x["status"]))

    near: list = []
    for i in range(len(kept)):
        a = kept[i]
        ta = name_tokens(a["name"])
        ua = {normalize_url(p.get("url")) for p in a.get("where") or [] if p.get("url")}
        for j in range(i + 1, len(kept)):
            b = kept[j]
            why = []
            jac = jaccard(ta, name_tokens(b["name"]))
            if jac >= NEAR_DUPLICATE_JACCARD:
                why.append(f"names share {jac:.2f} of their words")
            shared = sorted(ua & {normalize_url(p.get("url")) for p in b.get("where") or [] if p.get("url")})
            if shared:
                why.append("same place: " + ", ".join(shared))
            if why:
                near.append({"a": a["slug"], "b": b["slug"], "why": "; ".join(why)})
    near.sort(key=lambda x: (x["a"], x["b"]))

    by_lens = {lens: 0 for lens in lenses}
    by_origin = {o: 0 for o in ORIGINS}
    for r in kept:
        by_lens[r["lens"]] = by_lens.get(r["lens"], 0) + 1
        by_origin[r["origin"]] = by_origin.get(r["origin"], 0) + 1
    rooms_min = int(s1.get("rooms_min", 80))
    rooms_max = int(s1.get("rooms_max", 120))
    min_per_lens = int(s1.get("min_rooms_per_lens", 8))
    count_problems: list = []
    total = len(kept)
    if total < rooms_min:
        count_problems.append(f"01_rooms.json: {total} rooms kept; the run needs at least {rooms_min}. "
                              f"Add rooms (gap pass) and rerun `funnel rooms --merge-parts`.")
    if total > rooms_max:
        count_problems.append(f"01_rooms.json: {total} rooms kept; the maximum is {rooms_max}. Merge near-duplicates "
                              f"with duplicate_of or drop the weakest rooms, then rerun.")
    for lens in lenses:
        if by_lens.get(lens, 0) < min_per_lens:
            count_problems.append(f"01_rooms.json: lens {lens} has {by_lens.get(lens, 0)} rooms; it needs at least "
                                  f"{min_per_lens}. Add rooms for this lens (gap_{lens}.json) and rerun.")

    kept_out = []
    for r in kept:
        c = _clean(r)
        c["status"] = "kept"
        kept_out.append(c)
    return {
        "status": "ok" if not count_problems else "counts_out_of_range",
        "counts": {"in": len(rooms), "kept": total, "removed": len(removed), "by_lens": by_lens,
                   "by_origin": by_origin, "rooms_min": rooms_min, "rooms_max": rooms_max,
                   "min_rooms_per_lens": min_per_lens, "near_duplicates": len(near)},
        "rooms": kept_out,
        "removed": removed,
        "near_duplicates": near,
        "count_problems": count_problems,
        "warnings": warnings,
        "lenses": lenses,
    }


# --------------------------------------------------------------------------- rendering
def _size_text(size: dict) -> str:
    v = size.get("value")
    unit = size.get("unit", "")
    tag = size.get("tag", "estimate")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        vs = f"{v:,.0f}" if float(v).is_integer() else f"{v:,}"
    else:
        vs = str(v)
    return f"{vs} {unit} [{tag}]".strip()


def _md_cell(s) -> str:
    return common.normalize_ws(str(s if s is not None else "")).replace("|", "/")


def render_md(result: dict, run) -> str:
    c = result["counts"]
    lenses = result["lenses"]
    lines = [
        "# Stage 1: rooms",
        "",
        f"Run: {common.run_name(run)}.",
        "A room is a group of people in the same life situation who gather in findable places.",
        "A lens is one way of slicing people into rooms. A ladder is the list of paid problems a room meets in order.",
        "Geography is written down but never used as a filter.",
        "",
        f"Rooms in: {c['in']}. Kept: {c['kept']} (the run needs {c['rooms_min']} to {c['rooms_max']}). "
        f"Removed: {c['removed']}. Near-duplicates to look at: {c['near_duplicates']}.",
        f"Status: {'counts are within range' if result['status'] == 'ok' else 'counts are out of range (see below)'}.",
        "",
        "## Rooms per lens",
        "",
        "| Lens | Rooms | Minimum | Enough? |",
        "|---|---|---|---|",
    ]
    for lens in lenses:
        n = c["by_lens"].get(lens, 0)
        lines.append(f"| {lens} | {n} | {c['min_rooms_per_lens']} | {'yes' if n >= c['min_rooms_per_lens'] else 'no'} |")
    lines.append("")
    lines.append("By origin: " + ", ".join(f"{k} {v}" for k, v in c["by_origin"].items()) + ".")
    if result["count_problems"]:
        lines += ["", "## Count problems", ""]
        lines += [f"- {p}" for p in result["count_problems"]]
    for lens in lenses:
        rooms = [r for r in result["rooms"] if r["lens"] == lens]
        lines += ["", f"## Lens: {lens} ({len(rooms)} rooms)", ""]
        if not rooms:
            lines.append("No rooms yet.")
            continue
        lines.append("| # | Slug | Room | Origin | Size | Ladder steps | Gathers at | Ventures touched |")
        lines.append("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(rooms, 1):
            places = "; ".join(f"[{_md_cell(p.get('name'))}]({p.get('url')})" for p in (r.get("where") or [])[:3])
            vo = ", ".join(r.get("venture_overlap") or []) or "none"
            lines.append(f"| {i} | {r['slug']} | {_md_cell(r['name'])} | {r['origin']} | {_md_cell(_size_text(r['size']))} | "
                         f"{len(r.get('ladder') or [])} | {places} | {vo} |")
        for r in rooms:
            steps = "; ".join(f"{s['step']}. {_md_cell(s['problem'])}" + (f" ({_md_cell(s['price_text'])})" if s.get("price_text") else "")
                              for s in (r.get("ladder") or []))
            lines.append("")
            lines.append(f"**{r['slug']}**: {_md_cell(r['who'])} Who pays: {_md_cell(r['who_pays'])} "
                         f"Ladder: {steps or 'none yet'}. Confidence: {r.get('confidence')}.")
    lines += ["", f"## Removed rooms ({len(result['removed'])})", ""]
    if result["removed"]:
        for r in result["removed"]:
            lines.append(f"- {r['slug']} ({r['lens']}, {r['origin']}): {r['status']}. {_md_cell(r['reason'])}")
    else:
        lines.append("None.")
    lines += ["", f"## Near-duplicates to review ({len(result['near_duplicates'])})", ""]
    if result["near_duplicates"]:
        lines.append("These pairs may be the same room. If they are, set `duplicate_of` on the weaker one and rerun. "
                     "If they are truly different rooms, leave them.")
        lines.append("")
        for n in result["near_duplicates"]:
            lines.append(f"- {n['a']} and {n['b']}: {n['why']}")
    else:
        lines.append("None found (names share fewer than 60% of their words and no gathering place is shared).")
    if result["warnings"]:
        lines += ["", "## Warnings", ""]
        lines += [f"- {w}" for w in result["warnings"]]
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- command
def rooms_command(run, merge_parts: bool) -> dict:
    rd = common.run_dir(run)
    out_json = rd / "01_rooms.json"
    carried_removed: list = []
    if merge_parts:
        rooms, part_names = load_parts(run)
    else:
        common.require_file(out_json, "Run `funnel rooms --merge-parts` to build it from RUN/01_rooms.parts/.")
        data = common.read_json(out_json)
        rooms = data.get("rooms") if isinstance(data, dict) else None
        if not isinstance(rooms, list):
            raise common.ValidationErrors([f"{common.rel(out_json)}: needs a 'rooms' list."])
        rooms = [dict(r) for r in rooms if isinstance(r, dict)]
        for r in rooms:
            r.pop("status", None)
        carried_removed = [x for x in (data.get("removed") or []) if isinstance(x, dict)]
        part_names = list(data.get("parts") or [])
    result = process_rooms(run, rooms)
    if carried_removed:
        have = {(x.get("slug"), x.get("status")) for x in result["removed"]}
        for x in carried_removed:
            if (x.get("slug"), x.get("status")) not in have:
                result["removed"].append(x)
        result["removed"].sort(key=lambda x: (str(x.get("slug")), str(x.get("status"))))
        result["counts"]["removed"] = len(result["removed"])
    payload = {
        "status": result["status"],
        "counts": result["counts"],
        "parts": part_names,
        "rooms": result["rooms"],
        "removed": result["removed"],
        "near_duplicates": result["near_duplicates"],
        "count_problems": result["count_problems"],
        "warnings": result["warnings"],
    }
    common.write_json(out_json, payload)
    common.write_text(rd / "01_rooms.md", render_md(result, run))
    return payload


def cmd_rooms(args) -> int:
    run = common.run_dir(args.run)
    payload = rooms_command(run, merge_parts=args.merge_parts)
    c = payload["counts"]
    print(f"Rooms: {c['in']} in, {c['kept']} kept, {c['removed']} removed.")
    print("Per lens: " + ", ".join(f"{k} {v}" for k, v in c["by_lens"].items()) + ".")
    for r in payload["removed"]:
        print(f"removed {r['slug']}: {r['status']} ({r['reason']})")
    if payload["near_duplicates"]:
        print(f"{len(payload['near_duplicates'])} near-duplicate pair(s) to review (set duplicate_of on the weaker room if they are the same):")
        for n in payload["near_duplicates"]:
            print(f"  - {n['a']} and {n['b']}: {n['why']}")
    for w in payload["warnings"]:
        print(f"warning: {w}")
    print(f"Wrote {common.rel(run / '01_rooms.json')} and {common.rel(run / '01_rooms.md')}")
    common.log_event(run, STAGE, "rooms", "count", rooms_in=c["in"], rooms_kept=c["kept"], rooms_removed=c["removed"],
                     by_lens=c["by_lens"], by_origin=c["by_origin"], near_duplicates=c["near_duplicates"],
                     status=payload["status"])
    if payload["count_problems"]:
        if common.is_dry_run():
            for p in payload["count_problems"]:
                print(f"warning (dry run): {p}")
            common.log_event(run, STAGE, "rooms", "note", note="dry run: count problems reported as warnings",
                             problems=payload["count_problems"], review=False)
        else:
            raise common.ValidationErrors(payload["count_problems"])
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("rooms", help="Merge, validate and dedupe the Stage 1 rooms; write 01_rooms.json and 01_rooms.md.")
    p.add_argument("--merge-parts", action="store_true", help="read RUN/01_rooms.parts/*.json (otherwise re-check 01_rooms.json)")
    p.set_defaults(func=cmd_rooms)
