"""Setup and admin commands.

Commands: init, preflight [--network-only], ledger-check, loop-init --room, rooms-known,
graveyard, log, source-decision, robots, purge-expired, show, excerpt, listen-status.
Every command appends events to RUN/runlog.jsonl. Nothing here prints or stores a key.

Public API
----------
    REQUIRED_LEDGER_SECTIONS
    ledger_check() -> dict            {"ok", "errors", "warnings", "assumed": [{"line", "text"}], "sections",
                                       "counts", "texts_checked", "not_mentioned_walls"}
    text_fields(obj, path="") -> list[(path, text)]   every `text` field in a YAML tree
    assumed_lines(md_text) -> list[{"line", "text"}]  lines of ledger.md containing "[assumed"
    parse_sources_table(text) -> dict  {"header": [...], "rows": [{"line_no", "cells"}], "columns": {name: index}}
    sources_domains(text) -> list[str]   every domain in the "Domains the script must reach" column
    sources_keys(text) -> list[str]      every KEY_NAME in the "Key needed" column (plus .env.example)
    snapshot_config(run) -> list[str]    copy config/* into RUN/config_snapshot/
    record_source_decision(source, status, reason, url, date) -> dict   edits config/sources.md
    known_rooms() -> list[dict]          rooms kept by any run's 02_mask.json (latest first)
    loop_init(room) -> dict
    purge_expired(run, source, days) -> dict
    excerpt(text, start, end) -> str     exact original substring; matching is whitespace-normalized
    listen_status(run, room) -> dict
    register(subparsers)
"""
from __future__ import annotations

import datetime as _dt
import re
import shutil
from pathlib import Path

import common
import netfetch
import records

STAGE = 0
REQUIRED_LEDGER_SECTIONS = ("reach", "depth", "supply", "constraints", "geography", "practical_limits",
                            "exclusions", "existing_ventures")
SOURCE_STATUSES = ("unchecked", "allowed", "allowed-with-limits", "skip", "blocked-by-network")
ID_PREFIXES = {"reach.warm": "w", "reach.search": "s", "depth": "d", "supply.can_be": "c", "supply.can_rent": "r",
               "exclusions": "x", "existing_ventures": "v"}
_DOMAIN_RE = re.compile(r"`([a-z0-9-]+(?:\.[a-z0-9-]+)+)`")
_KEY_RE = re.compile(r"`([A-Z][A-Z0-9_]{2,})`")
_ENV_KEY_RE = re.compile(r"^([A-Z][A-Z0-9_]{2,})\s*=")
_RUN_DIR_RE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:-loop-[a-z0-9-]+)?$")
_NUMBER_RE = re.compile(r"(-?\d+(?:\.\d+)?)")


# =========================================================================== ledger check
def text_fields(obj, path: str = "") -> list:
    out: list = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else str(k)
            if k == "text" and isinstance(v, str):
                out.append((p, v))
            else:
                out.extend(text_fields(v, p))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.extend(text_fields(v, f"{path}[{i}]"))
    return out


def assumed_lines(md_text: str) -> list:
    out = []
    for n, line in enumerate(md_text.splitlines(), 1):
        if "[assumed" in line:
            out.append({"line": n, "text": line.strip().lstrip("-").strip()})
    return out


def _items_with_ids(ledger: dict) -> list:
    """(section, item) for every list of id-bearing items in the ledger."""
    out = []
    reach = ledger.get("reach") or {}
    for sec, items in (("reach.warm", reach.get("warm")), ("reach.search", reach.get("search")),
                       ("depth", ledger.get("depth")),
                       ("supply.can_be", (ledger.get("supply") or {}).get("can_be")),
                       ("supply.can_rent", (ledger.get("supply") or {}).get("can_rent")),
                       ("exclusions", ledger.get("exclusions")),
                       ("existing_ventures", ledger.get("existing_ventures"))):
        for i, it in enumerate(items or []):
            out.append((sec, i, it))
    return out


def _is_num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def ledger_check() -> dict:
    yaml_path = common.config_dir() / "ledger.yaml"
    md_path = common.config_dir() / "ledger.md"
    common.require_file(md_path, "The founder writes it (template: the Ledger section of config/formats.md).")
    common.require_file(yaml_path, "Transcribe config/ledger.md into it (see /funnel-setup).")
    ledger = common.load_ledger()
    md = common.read_text(md_path)
    md_norm = common.normalize_ws(md)
    errors: list = []
    warnings: list = []

    for sec in REQUIRED_LEDGER_SECTIONS:
        if sec not in ledger:
            errors.append(f"config/ledger.yaml: section '{sec}' is missing.")

    seen_ids: dict = {}
    counts: dict = {}
    for sec, i, it in _items_with_ids(ledger):
        counts[sec] = counts.get(sec, 0) + 1
        where = f"config/ledger.yaml: {sec}[{i}]"
        if not isinstance(it, dict):
            errors.append(f"{where}: must be an object with an id and a text.")
            continue
        iid = it.get("id")
        if not isinstance(iid, str) or not iid:
            errors.append(f"{where}: 'id' is missing.")
            continue
        prefix = ID_PREFIXES[sec]
        if not re.match(rf"^{prefix}\d+$", iid):
            errors.append(f"{where}: id {iid!r} should look like {prefix}1, {prefix}2, ... (the {sec} prefix).")
        if iid in seen_ids:
            errors.append(f"{where}: id {iid!r} is also used at {seen_ids[iid]}. Ids must be unique.")
        else:
            seen_ids[iid] = where
        if not isinstance(it.get("text"), str) or not it["text"].strip():
            errors.append(f"{where}: 'text' is missing (copy the founder's bullet word for word).")
        if sec == "depth" and it.get("strength") not in ("strong", "moderate", "weak"):
            errors.append(f"{where}: 'strength' must be strong, moderate or weak (got {it.get('strength')!r}).")

    walls = common.load_walls()
    human = {w for w, info in walls.items() if info["kind"] == "human"}
    supply = ledger.get("supply") or {}
    mentioned: set = set()

    def check_wall(wid, where):
        if wid not in walls:
            errors.append(f"{where}: wall {wid!r} is not in config/walls.md.")
        elif wid not in human:
            errors.append(f"{where}: wall {wid} is a machine wall; supply lists human walls (W17–W29) only.")
        else:
            mentioned.add(wid)

    for sec in ("can_be", "can_rent"):
        for i, it in enumerate(supply.get(sec) or []):
            if isinstance(it, dict):
                check_wall(it.get("wall"), f"config/ledger.yaml: supply.{sec}[{i}]")
    cannot = supply.get("cannot") or {}
    for i, wid in enumerate(cannot.get("walls") or []):
        check_wall(wid, f"config/ledger.yaml: supply.cannot.walls[{i}]")
    for i, wid in enumerate((supply.get("not_mentioned") or {}).get("walls") or []):
        if wid not in walls:
            errors.append(f"config/ledger.yaml: supply.not_mentioned.walls[{i}]: wall {wid!r} is not in config/walls.md.")
    not_mentioned = sorted(human - mentioned, key=lambda w: int(w[1:]))
    listed_nm = set((supply.get("not_mentioned") or {}).get("walls") or [])
    if listed_nm != set(not_mentioned):
        warnings.append(f"supply.not_mentioned.walls lists {', '.join(sorted(listed_nm, key=lambda w: int(w[1:]))) or 'nothing'}; "
                        f"the walls the supply sections never mention are {', '.join(not_mentioned) or 'none'}.")

    cons = ledger.get("constraints") or {}
    hpw = cons.get("hours_per_week") or {}
    for f in ("low", "high", "use"):
        if not _is_num(hpw.get(f)) or hpw.get(f) <= 0:
            errors.append(f"config/ledger.yaml: constraints.hours_per_week.{f} must be a positive number.")
    if all(_is_num(hpw.get(f)) for f in ("low", "high", "use")) and not (hpw["low"] <= hpw["use"] <= hpw["high"]):
        errors.append("config/ledger.yaml: constraints.hours_per_week.use must lie between low and high.")
    rw = (cons.get("runway") or {}).get("runway_months")
    if rw is not None and (not _is_num(rw) or rw < 0):
        errors.append("config/ledger.yaml: constraints.runway.runway_months must be null or a number of months (0 or more).")
    gr = (cons.get("guarantee_reserve") or {}).get("value")
    if not _is_num(gr) or gr < 0:
        errors.append("config/ledger.yaml: constraints.guarantee_reserve.value must be a number (0 or more).")
    hv = (cons.get("hour_value") or {}).get("value")
    if not _is_num(hv) or hv <= 0:
        errors.append("config/ledger.yaml: constraints.hour_value.value must be a positive number.")

    texts = text_fields(ledger)
    for path, text in texts:
        if common.normalize_ws(text) not in md_norm:
            short = text if len(text) <= 70 else text[:67] + "..."
            errors.append(f"config/ledger.yaml: {path}: this text is not in config/ledger.md word for word: \"{short}\". "
                          f"Copy the founder's current wording exactly (or the founder changed ledger.md: retranscribe).")

    assumed = assumed_lines(md)
    yaml_assumed = sum(1 for _p, t in _walk_assumed(ledger))
    if len(assumed) != yaml_assumed:
        warnings.append(f"ledger.md has {len(assumed)} [assumed] line(s) but ledger.yaml marks {yaml_assumed} item(s) "
                        f"assumed: true. Check the transcription.")

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "assumed": assumed,
        "sections": [s for s in ledger if s not in ("source", "transcribed", "currency")],
        "counts": counts,
        "texts_checked": len(texts),
        "not_mentioned_walls": not_mentioned,
        "currency": ledger.get("currency"),
    }


def _walk_assumed(obj, path: str = ""):
    if isinstance(obj, dict):
        if obj.get("assumed") is True:
            yield path, obj
        for k, v in obj.items():
            yield from _walk_assumed(v, f"{path}.{k}" if path else str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _walk_assumed(v, f"{path}[{i}]")


def _print_ledger_report(r: dict) -> None:
    print(f"Ledger sections: {', '.join(r['sections'])}. Currency: {r.get('currency')}.")
    print("Entries: " + ", ".join(f"{k} {v}" for k, v in sorted(r["counts"].items())) + ".")
    if r["ok"]:
        print(f"{r['texts_checked']} text fields checked: every one appears word for word in config/ledger.md.")
    else:
        print(f"{r['texts_checked']} text fields checked: {len(r['errors'])} problem(s), listed below.")
    print(f"[assumed] items ({len(r['assumed'])}; they go to REVIEW.md):")
    for a in r["assumed"]:
        print(f"  - line {a['line']}: {a['text']}")
    print("Human walls the ledger does not mention (treated as not supplied): "
          + (", ".join(r["not_mentioned_walls"]) or "none") + ".")
    for w in r["warnings"]:
        print(f"warning: {w}")


def cmd_ledger_check(args) -> int:
    run = common.run_dir(args.run)
    r = ledger_check()
    _print_ledger_report(r)
    common.log_event(run, STAGE, "ledger-check", "check", ok=r["ok"], texts_checked=r["texts_checked"],
                     assumed=len(r["assumed"]), errors=len(r["errors"]), warnings=r["warnings"])
    if not r["ok"]:
        raise common.ValidationErrors(r["errors"])
    return 0


# =========================================================================== sources.md
def _split_row(line: str):
    s = line.strip()
    if not s.startswith("|"):
        return None
    inner = s[1:]
    if inner.endswith("|"):
        inner = inner[:-1]
    return [c.strip() for c in inner.split("|")]


def _is_separator(cells) -> bool:
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", c) for c in cells)


def parse_sources_table(text: str) -> dict:
    lines = text.splitlines()
    header = None
    rows: list = []
    columns: dict = {}
    i = 0
    while i < len(lines):
        cells = _split_row(lines[i])
        if cells and header is None and cells[0].lower() == "source":
            header = cells
            for idx, name in enumerate(cells):
                columns[name.lower()] = idx
            i += 1
            if i < len(lines):
                sep = _split_row(lines[i])
                if sep and _is_separator(sep):
                    i += 1
            while i < len(lines):
                cells = _split_row(lines[i])
                if not cells:
                    break
                rows.append({"line_no": i, "cells": cells})
                i += 1
            break
        i += 1
    return {"header": header or [], "rows": rows, "columns": columns}


def _col(table: dict, startswith: str):
    for name, idx in table["columns"].items():
        if name.startswith(startswith):
            return idx
    return None


def _cell(row: dict, idx) -> str:
    cells = row["cells"]
    return cells[idx] if idx is not None and idx < len(cells) else ""


def sources_domains(text: str) -> list:
    table = parse_sources_table(text)
    idx = _col(table, "domains")
    out: set = set()
    for row in table["rows"]:
        for d in _DOMAIN_RE.findall(_cell(row, idx)):
            out.add(d)
    return sorted(out)


def sources_keys(text: str) -> list:
    table = parse_sources_table(text)
    idx = _col(table, "key")
    out: set = set()
    for row in table["rows"]:
        for k in _KEY_RE.findall(_cell(row, idx)):
            out.add(k)
    example = common.funnel_root() / ".env.example"
    if example.exists():
        for line in common.read_text(example).splitlines():
            m = _ENV_KEY_RE.match(line.strip())
            if m:
                out.add(m.group(1))
    return sorted(out)


def _sources_path() -> Path:
    return common.config_dir() / "sources.md"


def record_source_decision(source: str, status: str, reason: str, url: str, date) -> dict:
    """Append a decision-log line to config/sources.md and update the matching table row."""
    if status not in SOURCE_STATUSES:
        raise common.ValidationErrors([f"--status must be one of {', '.join(SOURCE_STATUSES)} (got {status!r})."])
    p = _sources_path()
    common.require_file(p, "It lists every source and the terms decisions.")
    text = common.read_text(p)
    lines = text.splitlines()
    table = parse_sources_table(text)
    want = common.normalize_ws(source).lower().strip("`")
    src_idx, adapter_idx = _col(table, "source"), _col(table, "adapter")
    status_idx, checked_idx, decision_idx = _col(table, "status"), _col(table, "checked"), _col(table, "decision")

    def norm(c):
        return common.normalize_ws(c).lower().replace("`", "")

    exact = [r for r in table["rows"] if norm(_cell(r, src_idx)) == want or norm(_cell(r, adapter_idx)) == want]
    partial = [r for r in table["rows"] if want and want in norm(_cell(r, src_idx))]
    match = None
    if len(exact) == 1:
        match = exact[0]
    elif len(exact) > 1:
        raise common.ValidationErrors([f"--source {source!r} matches {len(exact)} table rows. Use the exact name."])
    elif len(partial) == 1:
        match = partial[0]
    elif len(partial) > 1:
        names = "; ".join(_cell(r, src_idx) for r in partial)
        raise common.ValidationErrors([f"--source {source!r} matches several table rows ({names}). Use the exact name."])

    reason_clean = common.normalize_ws(reason).replace("|", "/")
    url_clean = common.normalize_ws(url or "").replace("|", "/") or "(no URL given)"
    row_updated = False
    if match is not None:
        cells = list(match["cells"])
        if status_idx is None or checked_idx is None or decision_idx is None:
            raise common.ValidationErrors(["config/sources.md: the table needs Status, Checked and Decision columns."])
        cells[status_idx] = status
        cells[checked_idx] = str(date)
        cells[decision_idx] = reason_clean
        new_line = "| " + " | ".join(cells) + " |"
        if lines[match["line_no"]] != new_line:
            lines[match["line_no"]] = new_line
            row_updated = True
    log_line = f"- {date} | {common.normalize_ws(source).replace('|', '/')} | {status} | {reason_clean} | {url_clean}"
    appended = False
    if log_line not in lines:
        if not any(ln.strip().lower().startswith("## decision log") for ln in lines):
            lines += ["", "## Decision log", "Append one line per check: `- YYYY-MM-DD | source | status | reason | URL of the clause read`."]
        while lines and not lines[-1].strip():
            lines.pop()
        lines.append(log_line)
        appended = True
    common.write_text(p, "\n".join(lines))
    return {"row_updated": row_updated, "row_found": match is not None, "log_appended": appended, "log_line": log_line,
            "source_cell": _cell(match, src_idx) if match else None}


def cmd_source_decision(args) -> int:
    run = common.run_dir(args.run)
    r = record_source_decision(args.source, args.status, args.reason, args.url, common.today())
    if r["row_found"]:
        print(f"Table row '{r['source_cell']}': status {args.status}, checked {common.today()}"
              + (" (updated)." if r["row_updated"] else " (already up to date)."))
    else:
        print(f"No table row matches '{args.source}'; only the decision log was written (fine for a per-domain decision).")
    print(("Appended: " if r["log_appended"] else "Already logged: ") + r["log_line"])
    common.log_event(run, STAGE, "source-decision", "source", source=args.source, status=args.status, reason=args.reason,
                     url=args.url, row_updated=r["row_updated"])
    return 0


# =========================================================================== init and preflight
def cmd_init(args) -> int:
    root = common.funnel_root()
    made = []
    for d in ("inbox/closed_groups", "inbox/customers", "inbox/audit_results", "runs", "cache"):
        p = root / d
        if not p.exists():
            p.mkdir(parents=True)
            made.append(d)
    print("Folders ready: inbox/closed_groups, inbox/customers, inbox/audit_results, runs, cache"
          + (f" (created: {', '.join(made)})" if made else " (all existed)") + ".")
    md = common.config_dir() / "ledger.md"
    yml = common.config_dir() / "ledger.yaml"
    status = "missing"
    if not md.exists():
        print("Ledger: config/ledger.md is missing. The founder must write it (template: config/formats.md, Ledger).")
    elif not yml.exists():
        print("Ledger: config/ledger.md is present; config/ledger.yaml (its transcription) is missing. Run /funnel-setup.")
        status = "yaml_missing"
    else:
        r = ledger_check()
        status = "ok" if r["ok"] else "mismatch"
        print(f"Ledger: config/ledger.md and config/ledger.yaml present; ledger-check {'passes' if r['ok'] else 'fails'} "
              f"({r['texts_checked']} text fields, {len(r['assumed'])} [assumed] items"
              + (f", {len(r['errors'])} problem(s): run `funnel ledger-check`" if not r["ok"] else "") + ").")
    keys = sources_keys(common.read_text(_sources_path())) if _sources_path().exists() else []
    if keys:
        have = [k for k in keys if common.get_key(k)]
        print(f"API keys set (names only): {', '.join(have) or 'none'}. Not set: "
              f"{', '.join(k for k in keys if k not in have) or 'none'}.")
    print(f".env: {'present' if (root / '.env').exists() else 'absent (environment variables are used)'}.")
    common.log_event(common.run_dir(args.run), STAGE, "init", "ran", created=made, ledger=status)
    return 0


def snapshot_config(run) -> list:
    snap = common.run_dir(run) / "config_snapshot"
    snap.mkdir(parents=True, exist_ok=True)
    copied = []
    for p in sorted(common.config_dir().iterdir()):
        if p.is_file():
            shutil.copyfile(p, snap / p.name)
            copied.append(p.name)
    return copied


def cmd_preflight(args) -> int:
    run = common.run_dir(args.run)
    run.mkdir(parents=True, exist_ok=True)
    sources_text = common.read_text(_sources_path()) if _sources_path().exists() else ""
    report: dict = {"run": common.run_name(run), "network_only": bool(args.network_only)}
    ledger_errors: list = []
    if not args.network_only:
        report["config_snapshot"] = snapshot_config(run)
        print(f"Config snapshot: {len(report['config_snapshot'])} file(s) copied to {common.rel(run / 'config_snapshot')}/.")
        r = ledger_check()
        _print_ledger_report(r)
        report["ledger_ok"] = r["ok"]
        report["assumed_items"] = len(r["assumed"])
        ledger_errors = r["errors"]
        keys = sources_keys(sources_text)
        report["keys"] = {k: bool(common.get_key(k)) for k in keys}
        have = [k for k, v in report["keys"].items() if v]
        print(f"API keys set (names only): {', '.join(have) or 'none'}. Not set: "
              f"{', '.join(k for k, v in report['keys'].items() if not v) or 'none'}.")
    domains = sources_domains(sources_text)
    probes = [netfetch.probe(d) for d in domains]
    report["domains"] = probes
    to_allow = [p["domain"] for p in probes if p["status"] == "blocked_by_network"]
    report["domains_to_allow"] = to_allow
    print(f"Domains probed: {len(probes)} (one light request each).")
    for p in probes:
        print(f"  {p['domain']}: {p['status']} ({p['detail']})")
        if p["status"] == "blocked_by_network":
            common.log_event(run, STAGE, "preflight", "blocked", domain=p["domain"], detail=p["detail"])
    if to_allow:
        print("Domains to allow (exact list): " + ", ".join(to_allow))
    else:
        print("Domains to allow: none; every listed domain answered.")
    common.write_json(run / "preflight.json", report)
    print(f"Wrote {common.rel(run / 'preflight.json')}")
    common.log_event(run, STAGE, "preflight", "ran", network_only=bool(args.network_only),
                     domains_reachable=[p["domain"] for p in probes if p["status"] == "reachable"],
                     domains_blocked=to_allow, ledger_ok=report.get("ledger_ok"))
    if ledger_errors:
        raise common.ValidationErrors(ledger_errors)
    return 0


# =========================================================================== rooms known, loop-init, graveyard
def _run_dirs() -> list:
    runs = common.funnel_root() / "runs"
    if not runs.exists():
        return []
    return sorted((p for p in runs.iterdir() if p.is_dir() and _RUN_DIR_RE.match(p.name)), key=lambda p: p.name, reverse=True)


def _mask_kept(rd: Path) -> dict:
    p = rd / "02_mask.json"
    if not p.exists():
        return {}
    try:
        data = common.read_json(p)
    except ValueError:
        return {}
    out = {}
    for v in (data.get("rooms") or []) if isinstance(data, dict) else []:
        if isinstance(v, dict) and v.get("status") == "kept" and common.is_slug(v.get("slug")):
            out[v["slug"]] = v
    return out


def known_rooms() -> list:
    dead = common.dead_items("room")
    revived = {e["item"] for e in common.parse_graveyard() if e["status"] == "revived"}
    seen: dict = {}
    for rd in _run_dirs():
        for slug, v in _mask_kept(rd).items():
            if slug not in seen:
                item = f"room:{slug}"
                seen[slug] = {"slug": slug, "name": v.get("name", slug), "run": rd.name, "rank": v.get("rank"),
                              "graveyard": "dead" if item in dead else ("revived" if item in revived else "no")}
    rooms = sorted(seen.values(), key=lambda x: x["slug"])
    rooms.sort(key=lambda x: x["run"], reverse=True)
    return rooms


def cmd_rooms_known(args) -> int:
    rooms = known_rooms()
    if not rooms:
        print("No run has a 02_mask.json yet. Run /funnel-run first.")
    else:
        print(f"{len(rooms)} room(s) kept by earlier runs (latest run first):")
        for r in rooms:
            note = "" if r["graveyard"] == "no" else f" [graveyard: {r['graveyard']}]"
            print(f"  {r['slug']:40} run {r['run']}  rank {r['rank']}  {r['name']}{note}")
    common.log_event(common.run_dir(args.run), STAGE, "rooms-known", "ran", rooms=len(rooms))
    return 0


def loop_init(room: str) -> dict:
    room = common.check_slug(room, "room")
    item = f"room:{room}"
    if common.is_dead(item):
        g = next((e for e in common.parse_graveyard() if e["item"] == item and e["status"] == "dead"), {})
        raise common.ValidationErrors([f"room {room} is dead in graveyard.md ({g.get('date', '?')}, {g.get('stage', '?')}: "
                                       f"{g.get('reason', '')}). Add an indented `- new evidence YYYY-MM-DD: ...` line under it first."])
    source = None
    for rd in _run_dirs():
        kept = _mask_kept(rd)
        if room in kept:
            source = rd
            break
    if source is None:
        raise common.MissingInput(f"No run kept room {room} in its 02_mask.json. Run /funnel-run first, or pick a room from "
                                  f"`funnel rooms-known`.")
    rooms_data = common.read_json(source / "01_rooms.json") if (source / "01_rooms.json").exists() else {}
    room_entry = next((r for r in (rooms_data.get("rooms") or []) if isinstance(r, dict) and r.get("slug") == room), None)
    if room_entry is None:
        raise common.MissingInput(f"{common.rel(source / '01_rooms.json')} has no entry for {room}.")
    mask_data = common.read_json(source / "02_mask.json")
    mask_entry = _mask_kept(source)[room]
    name = f"{common.today().isoformat()}-loop-{room}"
    new = common.funnel_root() / "runs" / name
    new.mkdir(parents=True, exist_ok=True)
    common.write_json(new / "01_rooms.json", {"status": "loop", "loop_room": room, "source_run": source.name,
                                             "counts": {"in": 1, "kept": 1, "removed": 0}, "parts": [],
                                             "rooms": [room_entry], "removed": [], "near_duplicates": [],
                                             "count_problems": [], "warnings": []})
    common.write_json(new / "02_mask.json", {"loop_room": room, "source_run": source.name,
                                            "max_rooms": mask_data.get("max_rooms"), "rank_by": mask_data.get("rank_by"),
                                            "counts": {"in": 1, "survived": 1, "kept": 1, "cut": 0, "killed": 0},
                                            "kept": [room], "cut": [], "killed": [], "rooms": [mask_entry],
                                            "review_notes": [], "warnings": [], "price_check": {"counts": {}, "blocked_domains": []}})
    snapshot = snapshot_config(new)
    fx_note = "no fx_rates.json in the source run; write a fresh one and run `funnel fx`"
    fx_copied = False
    src_fx = source / "fx_rates.json"
    if src_fx.exists():
        try:
            as_of = common.read_json(src_fx).get("as_of")
            age = (common.today() - _dt.date.fromisoformat(as_of)).days if common.is_date(as_of) else None
        except (ValueError, AttributeError):
            age = None
        if age is not None and 0 <= age < 7:
            shutil.copyfile(src_fx, new / "fx_rates.json")
            fx_copied = True
            fx_note = f"fx_rates.json copied from {source.name} ({age} days old)"
        else:
            fx_note = f"fx_rates.json in {source.name} is {age if age is not None else 'of unknown'} days old; refresh the rates and run `funnel fx`"
    common.log_event(new, STAGE, "loop-init", "ran", room=room, source_run=source.name, fx_copied=fx_copied)
    return {"run": name, "source_run": source.name, "room": room, "snapshot": snapshot, "fx_note": fx_note, "fx_copied": fx_copied}


def cmd_loop_init(args) -> int:
    r = loop_init(args.room)
    print(f"RUN: runs/{r['run']}")
    print(f"Room {r['room']} copied from run {r['source_run']} (01_rooms.json and 02_mask.json entries; "
          f"{len(r['snapshot'])} config files snapshotted).")
    print(f"FX: {r['fx_note']}.")
    return 0


def cmd_graveyard(args) -> int:
    entries = common.parse_graveyard()
    dead = [e for e in entries if e["status"] == "dead"]
    revived = [e for e in entries if e["status"] == "revived"]
    print(f"Graveyard: {len(entries)} entries, {len(dead)} dead, {len(revived)} revived.")
    for e in entries:
        mark = "revived" if e["status"] == "revived" else "dead"
        print(f"  {e['date']} | {e['stage']} | {e['item']} | {e['reason']} [{mark}]")
        for rv in e["revivals"]:
            print(f"      {rv}")
    common.log_event(common.run_dir(args.run), STAGE, "graveyard", "ran", entries=len(entries), dead=len(dead), revived=len(revived))
    return 0


# =========================================================================== log, robots, purge
def cmd_log(args) -> int:
    run = common.run_dir(args.run)
    kind, text = next((k, v) for k, v in (("error", args.error), ("note", args.note), ("cost", args.cost)) if v is not None)
    fields = {"text": text, "review": bool(args.review)}
    if kind == "cost":
        m = _NUMBER_RE.search(text.replace(",", ""))
        fields["amount"] = float(m.group(1)) if m else None
        fields["tag"] = "estimate"
    common.log_event(run, args.stage, "log", kind, **fields)
    print(f"Logged {kind} for stage {args.stage}" + (" (marked for REVIEW.md)" if args.review else "") + f": {text}")
    return 0


def cmd_robots(args) -> int:
    run = common.run_dir(args.run)
    url = args.url
    domain = common.domain_of(url)
    if not domain or not url.startswith(("http://", "https://")):
        raise common.ValidationErrors([f"robots: {url!r} is not a full URL (start with http:// or https://)."])
    try:
        allowed = netfetch.robots_allowed(url)
    except netfetch.NetworkBlocked:
        raise
    except netfetch.FetchError as e:
        raise common.Blocked(f"{domain}: could not read robots.txt ({e}). Treat the page as not allowed for now.")
    cache = netfetch.robots_dir() / f"{domain}.txt"
    print(f"{url}: {'allowed' if allowed else 'NOT allowed'} for user agent '{netfetch.user_agent().split('/')[0]}' "
          f"by https://{domain}/robots.txt (cached at {common.rel(cache)}).")
    common.log_event(run, STAGE, "robots", "check", url=url, domain=domain, allowed=bool(allowed))
    return 0


def purge_expired(run, source: str, days: int) -> dict:
    if days < 0:
        raise common.ValidationErrors(["--days must be 0 or more."])
    cutoff = common.today() - _dt.timedelta(days=days)
    raw_root = common.listen_dir(run) / "raw"
    per_room: dict = {}
    if raw_root.exists():
        for room_dir in sorted(p for p in raw_root.iterdir() if p.is_dir()):
            f = records.source_file(run, room_dir.name, source) if common.is_slug(room_dir.name) else None
            if f is None or not f.exists():
                continue
            rows = common.read_jsonl(f)
            kept, dropped, undated = [], 0, 0
            for row in rows:
                fetched = ((row.get("meta") or {}).get("fetched_at") if isinstance(row, dict) else None)
                if not isinstance(fetched, str) or not common.is_date(fetched[:10]):
                    undated += 1
                    kept.append(row)
                    continue
                if _dt.date.fromisoformat(fetched[:10]) < cutoff:
                    dropped += 1
                else:
                    kept.append(row)
            if dropped:
                if kept:
                    common.write_jsonl(f, kept)
                else:
                    f.unlink()
            per_room[room_dir.name] = {"before": len(rows), "dropped": dropped, "kept": len(kept), "no_fetched_at": undated}
    total = sum(v["dropped"] for v in per_room.values())
    common.log_event(run, 3, "purge-expired", "count", source=source, days=days, cutoff=cutoff.isoformat(),
                     dropped=total, rooms=per_room)
    return {"source": source, "days": days, "cutoff": cutoff.isoformat(), "rooms": per_room, "dropped": total}


def cmd_purge_expired(args) -> int:
    run = common.run_dir(args.run)
    r = purge_expired(run, args.source, args.days)
    print(f"Purged records of source {r['source']} fetched before {r['cutoff']} ({r['days']} days): {r['dropped']} removed.")
    for room, v in r["rooms"].items():
        print(f"  {room}: {v['before']} before, {v['dropped']} removed, {v['kept']} kept ({v['no_fetched_at']} without meta.fetched_at, kept).")
    if not r["rooms"]:
        print("No room has records from that source.")
    if r["dropped"]:
        print("Rerun `funnel batches --room <room>` for the rooms above so the batch files match.")
    return 0


# =========================================================================== show, excerpt, listen-status
def _print_record(rec: dict) -> None:
    date = rec.get("date") or "undated"
    domain = common.domain_of(rec.get("url") or "") or "-"
    print(f"### {rec['record_id']} | {rec.get('source', '-')} | {date} | {domain}")
    print(f"url: {rec.get('url') or '-'}")
    print(rec.get("text") or "")
    print()


def _find_pain(run, pid: str):
    """The pain entry from RUN/03_listen/pains.json, else the room's pains_draft.json."""
    room, key = common.split_pain_id(pid)
    p = common.listen_dir(run) / "pains.json"
    if p.exists():
        data = common.read_json(p)
        pains = data.get("pains") if isinstance(data, dict) else data
        if isinstance(pains, dict):
            if pid in pains:
                return pains[pid], common.rel(p)
            pains = list(pains.values())
        for pain in pains or []:
            if isinstance(pain, dict) and (pain.get("pain_id") == pid or (pain.get("room") == room and pain.get("pain_key") == key)):
                return pain, common.rel(p)
    d = common.room_dir(run, room) / "pains_draft.json"
    if d.exists():
        data = common.read_json(d)
        for pain in (data.get("pains") or []) if isinstance(data, dict) else []:
            if isinstance(pain, dict) and pain.get("pain_key") == key:
                return pain, common.rel(d)
    return None, None


def cmd_show(args) -> int:
    run = common.run_dir(args.run)
    if args.pain and (args.room or args.ids):
        raise common.ValidationErrors(["show: use either --room R --ids a,b or --pain P, not both."])
    if args.pain:
        pid = args.pain
        room, key = common.split_pain_id(pid)
        pain, where = _find_pain(run, pid)
        if pain is None:
            raise common.MissingInput(f"No pain {pid} in {common.rel(common.listen_dir(run) / 'pains.json')} or in "
                                      f"{common.rel(common.room_dir(run, room) / 'pains_draft.json')}.")
        print(f"# Pain {pid} (from {where})")
        print(common.dumps_json({k: v for k, v in pain.items() if k != "quotes"}).rstrip())
        print()
        print(f"## Quotes ({len(pain.get('quotes') or [])})")
        for q in pain.get("quotes") or []:
            print(f"- [{q.get('record_id')}] {q.get('text')} <{q.get('url')}> {q.get('date') or 'undated'}")
        print()
        by_id = records.records_by_id(run, room)
        counts_p = common.room_dir(run, room) / "counts.json"
        member_ids: list = []
        if counts_p.exists():
            cdata = common.read_json(counts_p)
            member_ids = sorted(((cdata.get("pains") or {}).get(key) or {}).get("member_record_ids") or [])
        limit = max(0, int(args.limit))
        if member_ids:
            rng = common.rng_for_run(f"{common.run_name(run)}:{pid}")
            sample = member_ids if len(member_ids) <= limit else sorted(rng.sample(member_ids, limit))
            print(f"## Member records: {len(sample)} of {len(member_ids)} (a fixed random sample, seeded by the run name)")
            print()
            for rid in sample:
                rec = by_id.get(rid)
                if rec:
                    _print_record(rec)
                else:
                    print(f"### {rid} | (record not stored)\n")
        else:
            print("## Member records: none listed (counts.json missing or the pain has no member records).")
        common.log_event(run, 3, "show", "ran", pain=pid, member_records=len(member_ids))
        return 0
    if not args.room or not args.ids:
        raise common.ValidationErrors(["show: give --room R --ids a,b (records in full) or --pain P."])
    room = common.check_slug(args.room, "room")
    ids = [x.strip() for x in str(args.ids).split(",") if x.strip()]
    by_id = records.records_by_id(run, room)
    missing = []
    for rid in ids:
        rec = by_id.get(rid)
        if rec is None:
            missing.append(rid)
            continue
        _print_record(rec)
    common.log_event(run, 3, "show", "ran", room=room, ids=len(ids), missing=missing)
    if missing:
        raise common.ValidationErrors([f"record {rid} is not stored for room {room}. Use ids from the batch files." for rid in missing])
    return 0


def excerpt(text: str, start: str, end: str) -> str:
    """The exact original substring from `start` to the end of `end`. Matching is whitespace-normalized."""
    original = __import__("unicodedata").normalize("NFC", str(text or ""))
    collapsed: list = []
    index_map: list = []
    in_space = True  # strip leading whitespace
    for i, ch in enumerate(original):
        if ch.isspace():
            if not in_space:
                collapsed.append(" ")
                index_map.append(i)
                in_space = True
        else:
            collapsed.append(ch)
            index_map.append(i)
            in_space = False
    if collapsed and collapsed[-1] == " ":
        collapsed.pop()
        index_map.pop()
    hay = "".join(collapsed)
    ns, ne = common.normalize_ws(start), common.normalize_ws(end)
    if not ns or not ne:
        raise common.ValidationErrors(["excerpt: --start and --end must not be empty."])
    i = hay.find(ns)
    if i < 0:
        raise common.ValidationErrors([f"excerpt: the start text was not found in the record (matching ignores extra spaces): {start!r}."])
    j = hay.find(ne, i)
    if j < 0:
        raise common.ValidationErrors([f"excerpt: the end text was not found after the start text: {end!r}."])
    a = index_map[i]
    b = index_map[j + len(ne) - 1] + 1
    return original[a:b]


def cmd_excerpt(args) -> int:
    import sys

    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    rec = records.records_by_id(run, room).get(args.id)
    if rec is None:
        raise common.ValidationErrors([f"record {args.id} is not stored for room {room}."])
    out = excerpt(rec.get("text") or "", args.start, args.end)
    print(out)
    words = len(common.normalize_ws(out).split())
    min_words = int((common.load_kill_rules().get("stage3") or {}).get("quote_min_words", 5))
    print(f"[excerpt: {words} words from record {args.id} ({rec.get('url')}, {rec.get('date') or 'undated'}); "
          f"{'long enough' if words >= min_words else 'too short'} for a quote (minimum {min_words} words)]", file=sys.stderr)
    common.log_event(run, 3, "excerpt", "ran", room=room, record_id=args.id, words=words)
    return 0


def listen_status(run, room: str) -> dict:
    room = common.check_slug(room, "room")
    rdir = common.room_dir(run, room)
    raw = common.raw_dir(run, room)
    if not rdir.exists() and not raw.exists():
        raise common.MissingInput(f"Room {room} has no folder under {common.rel(common.listen_dir(run))}/. "
                                  f"Nothing was planned or harvested yet.")
    recs = records.load_records(run, room)
    per_source: dict = {}
    per_round: dict = {}
    dated = undated = 0
    domains: set = set()
    for r in recs:
        per_source[r.get("source", "?")] = per_source.get(r.get("source", "?"), 0) + 1
        rnd = str(records.record_round(r))
        per_round[rnd] = per_round.get(rnd, 0) + 1
        if r.get("date"):
            dated += 1
        else:
            undated += 1
        d = common.domain_of(r.get("url") or "")
        if d:
            domains.add(d)
    queries_per_round: dict = {}
    qp = rdir / "queries.jsonl"
    if qp.exists():
        for q in common.read_jsonl(qp):
            if isinstance(q, dict):
                key = str(q.get("round", "?"))
                queries_per_round[key] = queries_per_round.get(key, 0) + 1
    manifest = common.read_json(records.manifest_path(run, room)) if records.manifest_path(run, room).exists() else None
    labels_dir = rdir / "labels"
    label_files = sorted(p.stem for p in labels_dir.glob("*.jsonl")) if labels_dir.exists() else []
    labeled = 0
    for name in label_files:
        labeled += sum(1 for row in common.read_jsonl(labels_dir / f"{name}.jsonl") if isinstance(row, dict) and row.get("record_id"))
    taxonomy = common.read_json(rdir / "taxonomy.json") if (rdir / "taxonomy.json").exists() else None
    sat = common.read_json(rdir / "saturation.json") if (rdir / "saturation.json").exists() else None
    last = (sat.get("rounds") or [None])[-1] if isinstance(sat, dict) else None
    return {
        "room": room,
        "records": len(recs),
        "per_source": dict(sorted(per_source.items())),
        "per_round": dict(sorted(per_round.items(), key=lambda kv: (len(kv[0]), kv[0]))),
        "dated": dated,
        "undated": undated,
        "domains": len(domains),
        "queries_per_round": dict(sorted(queries_per_round.items(), key=lambda kv: (len(kv[0]), kv[0]))),
        "batches": sorted((manifest.get("batches") or {}).keys()) if manifest else [],
        "batch_records": len(counts_ids(manifest)) if manifest else 0,
        "label_files": label_files,
        "labeled": labeled,
        "pains_in_taxonomy": len(taxonomy.get("pains") or []) if isinstance(taxonomy, dict) else 0,
        "counts_json": (rdir / "counts.json").exists(),
        "saturation": {"round": last.get("round"), "records": last.get("records"), "saturated": last.get("saturated"),
                       "stop_reason": sat.get("stop_reason")} if isinstance(last, dict) else None,
        "pains_draft": (rdir / "pains_draft.json").exists(),
        "sources_json": (rdir / "sources.json").exists(),
    }


def counts_ids(manifest: dict) -> list:
    ids: list = []
    for name in sorted((manifest.get("batches") or {}).keys()):
        ids.extend(manifest["batches"][name])
    return ids


def cmd_listen_status(args) -> int:
    run = common.run_dir(args.run)
    s = listen_status(run, args.room)
    print(f"Room {s['room']}: {s['records']} records ({s['dated']} dated, {s['undated']} undated) from {s['domains']} domain(s).")
    print("Per source: " + (", ".join(f"{k} {v}" for k, v in s["per_source"].items()) or "none") + ".")
    print("Per round: " + (", ".join(f"round {k}: {v}" for k, v in s["per_round"].items()) or "none") + ".")
    print("Queries per round: " + (", ".join(f"round {k}: {v}" for k, v in s["queries_per_round"].items()) or "none planned") + ".")
    print(f"Batches: {len(s['batches'])} file(s) holding {s['batch_records']} records. Labels: {len(s['label_files'])} file(s), "
          f"{s['labeled']} records labeled. Taxonomy pains: {s['pains_in_taxonomy']}. counts.json: {'yes' if s['counts_json'] else 'no'}.")
    if s["saturation"]:
        sat = s["saturation"]
        print(f"Saturation: round {sat['round']}, {sat['records']} records, saturated {'yes' if sat['saturated'] else 'no'}"
              + (f", stopped: {sat['stop_reason']}" if sat.get("stop_reason") else "") + ".")
    else:
        print("Saturation: not evaluated yet.")
    print(f"pains_draft.json: {'yes' if s['pains_draft'] else 'no'}. sources.json: {'yes' if s['sources_json'] else 'no'}.")
    common.log_event(run, 3, "listen-status", "ran", room=s["room"], records=s["records"], per_source=s["per_source"],
                     per_round=s["per_round"], dated=s["dated"], undated=s["undated"])
    return 0


# =========================================================================== register
def register(subparsers) -> None:
    p = subparsers.add_parser("init", help="Create the inbox, runs and cache folders; print the ledger status.")
    p.set_defaults(func=cmd_init)

    p = subparsers.add_parser("preflight", help="Snapshot config, check the ledger, list keys set, probe every source domain.")
    p.add_argument("--network-only", action="store_true", help="only probe the domains")
    p.set_defaults(func=cmd_preflight)

    p = subparsers.add_parser("ledger-check", help="Check config/ledger.yaml against config/ledger.md; list [assumed] items.")
    p.set_defaults(func=cmd_ledger_check)

    p = subparsers.add_parser("loop-init", help="Create runs/<today>-loop-<room>/ from the latest run that kept the room.")
    p.add_argument("--room", required=True, help="room slug")
    p.set_defaults(func=cmd_loop_init)

    p = subparsers.add_parser("rooms-known", help="List rooms kept by earlier runs.")
    p.set_defaults(func=cmd_rooms_known)

    p = subparsers.add_parser("graveyard", help="Print graveyard.md entries and their status.")
    p.set_defaults(func=cmd_graveyard)

    p = subparsers.add_parser("log", help="Append an error, note or cost event to RUN/runlog.jsonl.")
    p.add_argument("--stage", type=int, required=True, help="stage number (0 for setup)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--error", metavar="TEXT", help="something went wrong")
    g.add_argument("--note", metavar="TEXT", help="a choice or observation")
    g.add_argument("--cost", metavar="TEXT", help="an approximate cost, for example '2.50 USD for 40 model calls'")
    p.add_argument("--review", action="store_true", help="mark the note for REVIEW.md")
    p.set_defaults(func=cmd_log)

    p = subparsers.add_parser("source-decision", help="Record a terms decision in config/sources.md (log line and table row).")
    p.add_argument("--source", required=True, help="source name or adapter as in the sources.md table")
    p.add_argument("--status", required=True, choices=SOURCE_STATUSES)
    p.add_argument("--reason", required=True, help="the decision and why, in one sentence")
    p.add_argument("--url", default="", help="URL of the terms clause read")
    p.set_defaults(func=cmd_source_decision)

    p = subparsers.add_parser("robots", help="Say whether robots.txt allows fetching a URL.")
    p.add_argument("url", help="full URL")
    p.set_defaults(func=cmd_robots)

    p = subparsers.add_parser("purge-expired", help="Remove stored records of a source fetched more than N days ago (meta.fetched_at).")
    p.add_argument("--source", required=True, help="source name, for example reddit")
    p.add_argument("--days", type=int, required=True, help="keep records fetched within this many days")
    p.set_defaults(func=cmd_purge_expired)

    p = subparsers.add_parser("show", help="Print records in full (--room R --ids a,b) or a pain with quotes and sample records (--pain P).")
    p.add_argument("--room", default=None, help="room slug")
    p.add_argument("--ids", default=None, help="comma-separated record ids")
    p.add_argument("--pain", default=None, help="pain id <room>--<key>")
    p.add_argument("--limit", type=int, default=15, help="member records to show with --pain (default 15)")
    p.set_defaults(func=cmd_show)

    p = subparsers.add_parser("excerpt", help="Print the exact original text of a record between two phrases.")
    p.add_argument("--room", required=True, help="room slug")
    p.add_argument("--id", required=True, help="record id")
    p.add_argument("--start", required=True, help="first words of the excerpt")
    p.add_argument("--end", required=True, help="last words of the excerpt")
    p.set_defaults(func=cmd_excerpt)

    p = subparsers.add_parser("listen-status", help="Records per source and round, dated/undated, batches, labels, saturation for a room.")
    p.add_argument("--room", required=True, help="room slug")
    p.set_defaults(func=cmd_listen_status)
