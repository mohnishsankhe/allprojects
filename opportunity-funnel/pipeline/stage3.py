"""Stage 3 synthesis: the `pains` command.

For every room with a `pains_draft.json`, join each drafted pain with the
room's `counts.json`, run the quote checker (rule 1), apply the drop rules in
order, tag thin or weak evidence honestly (rule 8), rank, keep at most
`max_pains_total` across all rooms, send every drop and cut to graveyard.md
(rule 7), collect each room's `needs_calls` flag and saturation verdict, and
write `RUN/03_listen/pains.json`, `pains.md` and `quote_check.csv`.

Rules, in order (config/kill_rules.yaml, stage3):
  1. fewer than `min_verified_quotes` verified quotes -> dropped;
  2. money mentions 0, failed spend 0 and urgency `none` -> dropped;
  3. fewer than `thin_below_records` member records -> tagged [thin].
Spend check: distinct domains across `spend_evidence` (a record's domain comes
from its URL); fewer than `spend_sources_min` -> tagged [spend: N source(s)].
[titles only] when every supporting record is a web-search title (source
`websearch`); [undated share: X%] always.
Every alternative's price goes through the price checker (prices.check_items),
exactly as the mask does for spend items: `seen_via: page` is `[measured]` only
when the page was opened and shows the price text; a page the network blocks,
or a price read in a search result, is `[measured, page not checked]`. The
status, tag and detail are stored on the alternative in pains.json and every
renderer prints the checker's tag, never the model's claim (rule 8).
The graveyard lines dated on the run date for stage 3 say exactly what this run
of `pains` dropped or cut (common.sync_graveyard): a pain a rerun keeps loses
its stale line.

Public API
----------
    STAGE = 3
    SPEND_KINDS = ("record", "price", "job_posting")
    TAG_MEANING                         plain-English meaning of every tag
    draft_rooms(run) -> list[str]       rooms (sorted) that have a pains_draft.json
    load_draft(run, room) -> list[dict] the draft's pains (raises on a bad file)
    load_counts(run, room) -> dict      the room's counts.json (exit 2 when missing)
    validate_pain(pain, where, counts_pains, stored, urgency_types) -> list[str]
    spend_domains(spend_evidence, stored) -> list[str]      sorted distinct domains
    supporting_record_ids(member_ids, verified, spend_evidence, stored) -> list[str]
    undated_share(record_ids, stored) -> (percent, undated, total)
    rank_key(pain, rank_by, urgency_order) -> tuple
    saturation_verdict(run, room) -> dict
    needs_calls_of(run, room) -> (value | None, reasoning, notes, errors)
    dead_pains_from_other_runs(run) -> dict[item -> graveyard entry]
    pains(run) -> dict                  the pains.json content (files and graveyard written)
    render_md(result, run) -> str
    register(subparsers)                adds `pains`
"""
from __future__ import annotations

from pathlib import Path

import common
import prices
import quote_check
import records

STAGE = 3
SPEND_KINDS = ("record", "price", "job_posting")
DEFAULT_URGENCY_ORDER = ["deadline_or_rule", "acute_pain", "fear", "expiring_gain", "none"]
DEFAULT_RANK_BY = ["failed_spend_mentions", "money_mentions", "urgency", "record_count"]
TAG_MEANING = {
    "[thin]": "fewer member records than thin_below_records: too little data to trust the conclusion much",
    "[spend: N source(s)]": "spending evidence comes from fewer distinct websites (domains) than spend_sources_min",
    "[titles only]": "every supporting record is a web-search title; no full text was read",
    "[undated share: X%]": "the share of supporting records that carry no date",
}
STATUS_ORDER = {"kept": 0, "cut": 1, "dropped": 2}


# --------------------------------------------------------------------------- inputs
def draft_rooms(run) -> list:
    """Rooms (sorted slugs) whose folder holds a pains_draft.json."""
    rooms_dir = common.listen_dir(run) / "rooms"
    if not rooms_dir.exists():
        return []
    out = []
    for p in sorted(rooms_dir.glob("*/pains_draft.json")):
        slug = p.parent.name
        if common.is_slug(slug):
            out.append(slug)
    return out


def load_draft(run, room: str) -> list:
    p = common.room_dir(run, room) / "pains_draft.json"
    common.require_file(p, "The listener writes it in mode synthesize.")
    try:
        data = common.read_json(p)
    except ValueError as e:  # json.JSONDecodeError is a ValueError
        raise common.ValidationErrors([f"{common.rel(p)}: not valid JSON ({e}). Fix the file."])
    pains_list = data.get("pains") if isinstance(data, dict) else None
    if not isinstance(pains_list, list):
        raise common.ValidationErrors([f"{common.rel(p)}: needs a 'pains' list (see config/formats.md, Stage 3)."])
    return pains_list


def load_counts(run, room: str) -> dict:
    p = common.room_dir(run, room) / "counts.json"
    common.require_file(p, f"Run `funnel count --room {room}` first.")
    data = common.read_json(p)
    if not isinstance(data, dict) or not isinstance(data.get("pains"), dict):
        raise common.ValidationErrors([f"{common.rel(p)}: needs a 'pains' object. Rerun `funnel count --room {room}`."])
    return data


# --------------------------------------------------------------------------- validation
def _nonempty_str(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _is_int(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)


def _is_url(v) -> bool:
    return isinstance(v, str) and v.startswith(("http://", "https://"))


def _check_record_ids(ids, where: str, stored: dict, what: str) -> list:
    errors = []
    if not isinstance(ids, list) or not all(isinstance(x, str) for x in ids):
        return [f"{where}: {what} must be a list of record ids (strings)."]
    for rid in ids:
        if rid not in stored:
            errors.append(f"{where}: {what}: record {rid} is not stored for this room. Use ids from the batch files.")
    return errors


def validate_pain(pain, where: str, counts_pains: dict, stored: dict, urgency_types) -> list:
    """Every problem with one drafted pain, in plain English. Quotes are checked separately."""
    if not isinstance(pain, dict):
        return [f"{where}: must be an object (see config/formats.md, pains_draft.json)."]
    errors: list = []
    key = pain.get("pain_key")
    if not common.is_slug(key):
        errors.append(f"{where}: 'pain_key' {key!r} must be a slug (lowercase letters, digits, hyphens).")
    elif key not in counts_pains:
        errors.append(f"{where}: pain_key {key!r} is not in counts.json. Use a key from taxonomy.json and rerun "
                      f"`funnel count`, or fix the key.")
    if not _nonempty_str(pain.get("description")):
        errors.append(f"{where}: 'description' is missing or empty (write it in the room's words).")
    urg = pain.get("urgency")
    if not isinstance(urg, dict):
        errors.append(f"{where}: 'urgency' must be an object with type, evidence, record_ids, reasoning, confidence.")
    else:
        utype = urg.get("type")
        if utype not in urgency_types:
            errors.append(f"{where}: urgency.type must be one of {', '.join(urgency_types)} (got {utype!r}).")
        ids = urg.get("record_ids")
        if ids is None:
            ids = []
        errors.extend(_check_record_ids(ids, where, stored, "urgency.record_ids"))
        if utype in urgency_types and utype != "none":
            if not _nonempty_str(urg.get("evidence")):
                errors.append(f"{where}: urgency.evidence is empty; say what forces action (or set type to none).")
            if isinstance(ids, list) and not ids:
                errors.append(f"{where}: urgency.record_ids is empty; an urgency of type {utype} must cite at least one "
                              f"stored record (or set type to none).")
        errors.extend(common.check_judgment(urg, f"{where}: urgency"))
    who = pain.get("who_pays")
    if not isinstance(who, dict):
        errors.append(f"{where}: 'who_pays' must be an object with text, reasoning, confidence.")
    else:
        if not _nonempty_str(who.get("text")):
            errors.append(f"{where}: who_pays.text is missing or empty.")
        errors.extend(common.check_judgment(who, f"{where}: who_pays"))
    alts = pain.get("alternatives")
    if alts is None:
        alts = []
    if not isinstance(alts, list):
        errors.append(f"{where}: 'alternatives' must be a list of price items (use [] when none was found).")
    else:
        for i, item in enumerate(alts, 1):
            errors.extend(common.check_price(item, f"{where}: alternative {i}"))
    sellers = pain.get("sellers")
    if sellers is None:
        sellers = []
    if not isinstance(sellers, list):
        errors.append(f"{where}: 'sellers' must be a list (use [] when none was found).")
    else:
        for i, s in enumerate(sellers, 1):
            sw = f"{where}: seller {i}"
            if not isinstance(s, dict):
                errors.append(f"{sw}: must be an object with name, url, complaints, complaint_record_ids.")
                continue
            if not _nonempty_str(s.get("name")):
                errors.append(f"{sw}: 'name' is missing or empty.")
            url = s.get("url")
            if url is not None and not _is_url(url):
                errors.append(f"{sw}: 'url' must start with http:// or https://, or be null.")
            comp = s.get("complaints")
            if comp is not None and (not isinstance(comp, list) or not all(isinstance(c, str) for c in comp)):
                errors.append(f"{sw}: 'complaints' must be a list of short texts.")
            errors.extend(_check_record_ids(s.get("complaint_record_ids") or [], sw, stored, "complaint_record_ids"))
    spend = pain.get("spend_evidence")
    if spend is None:
        spend = []
    if not isinstance(spend, list):
        errors.append(f"{where}: 'spend_evidence' must be a list (use [] when none was found).")
    else:
        for i, item in enumerate(spend, 1):
            sw = f"{where}: spend_evidence {i}"
            if not isinstance(item, dict):
                errors.append(f"{sw}: must be an object with kind and record_id or url.")
                continue
            kind = item.get("kind")
            if kind not in SPEND_KINDS:
                errors.append(f"{sw}: 'kind' must be one of {', '.join(SPEND_KINDS)} (got {kind!r}).")
            rid = item.get("record_id")
            url = item.get("url")
            if rid is not None and not isinstance(rid, str):
                errors.append(f"{sw}: 'record_id' must be a string.")
            elif isinstance(rid, str) and rid not in stored:
                errors.append(f"{sw}: record {rid} is not stored for this room. Use ids from the batch files.")
            if url is not None and not _is_url(url):
                errors.append(f"{sw}: 'url' must start with http:// or https://.")
            if kind == "price" and not _is_url(url):
                errors.append(f"{sw}: a price item needs a 'url' (the page or search result that shows the price).")
            if kind in ("record", "job_posting") and not isinstance(rid, str):
                errors.append(f"{sw}: a {kind} item needs a 'record_id'.")
    lp = pain.get("ladder_position")
    if not _is_int(lp) or lp < 1:
        errors.append(f"{where}: 'ladder_position' must be a whole number from 1 (1 = the room's first paid problem).")
    quotes = pain.get("quotes")
    if quotes is not None and not isinstance(quotes, list):
        errors.append(f"{where}: 'quotes' must be a list of {{record_id, url, date, text}} objects.")
    return errors


# --------------------------------------------------------------------------- evidence helpers
def spend_domains(spend_evidence, stored: dict) -> list:
    """Distinct domains across spend_evidence. A record's domain comes from its stored URL."""
    domains: set = set()
    for item in spend_evidence or []:
        if not isinstance(item, dict):
            continue
        url = item.get("url")
        if not _is_url(url):
            rec = stored.get(item.get("record_id")) if isinstance(item.get("record_id"), str) else None
            url = (rec or {}).get("url")
        d = common.domain_of(url or "")
        if d:
            domains.add(d)
    return sorted(domains)


def supporting_record_ids(member_ids, verified, spend_evidence, stored: dict) -> list:
    """Member records of the pain, the records behind its verified quotes and its spend records (stored ones only)."""
    ids: set = set()
    for rid in member_ids or []:
        if rid in stored:
            ids.add(rid)
    for q in verified or []:
        rid = q.get("record_id") if isinstance(q, dict) else None
        if rid in stored:
            ids.add(rid)
    for item in spend_evidence or []:
        rid = item.get("record_id") if isinstance(item, dict) else None
        if isinstance(rid, str) and rid in stored:
            ids.add(rid)
    return sorted(ids)


def undated_share(record_ids, stored: dict) -> tuple:
    """(percent rounded to a whole number, undated count, total) over the given stored records."""
    total = 0
    undated = 0
    for rid in record_ids or []:
        rec = stored.get(rid)
        if rec is None:
            continue
        total += 1
        if not rec.get("date"):
            undated += 1
    pct = int(100 * undated / total + 0.5) if total else 0
    return pct, undated, total


def _sources_of(record_ids, stored: dict) -> dict:
    out: dict = {}
    for rid in record_ids or []:
        src = (stored.get(rid) or {}).get("source") or "unknown"
        out[src] = out.get(src, 0) + 1
    return dict(sorted(out.items()))


def rank_key(pain: dict, rank_by, urgency_order) -> tuple:
    key: list = []
    for name in rank_by:
        if name == "failed_spend_mentions":
            key.append(-int(pain["failed_spend_mentions"]))
        elif name == "money_mentions":
            key.append(-int(pain["money_mentions"]))
        elif name == "urgency":
            ut = pain["urgency_type"]
            key.append(urgency_order.index(ut) if ut in urgency_order else len(urgency_order))
        elif name == "record_count":
            key.append(-int(pain["record_count"]))
        elif name == "verified_quotes":
            key.append(-int(pain["verified_quote_count"]))
    key.append(pain["pain_id"])
    return tuple(key)


# --------------------------------------------------------------------------- room-level verdicts
def saturation_verdict(run, room: str) -> dict:
    p = common.room_dir(run, room) / "saturation.json"
    if not p.exists():
        return {"available": False, "rounds": 0, "records": None, "saturated": None, "stop_reason": None,
                "final": False, "new_pains": [], "rank_changes": 0,
                "verdict": "no saturation.json: the room never ran `funnel saturation`"}
    data = common.read_json(p)
    rounds = [e for e in (data.get("rounds") or []) if isinstance(e, dict)] if isinstance(data, dict) else []
    last = rounds[-1] if rounds else {}
    saturated = bool(last.get("saturated")) if last else None
    stop = data.get("stop_reason") if isinstance(data, dict) else None
    final = bool(data.get("final")) if isinstance(data, dict) else False
    if not rounds:
        verdict = "saturation.json has no round entries"
    elif not last.get("evaluable", True):
        why = str(last.get("note") or "needs window + 1").removeprefix("not evaluable: ")
        why = why.removeprefix(f"{last.get('records')} records, ")
        verdict = f"not evaluable after round {last.get('round')}: {last.get('records')} records ({why})"
    else:
        verdict = (f"round {last.get('round')}: {last.get('records')} records; "
                   f"{'saturated' if saturated else 'not saturated'}")
    if stop:
        verdict += f"; stopped: {stop}"
    elif rounds:
        verdict += "; not final (no stop reason recorded)"
    return {"available": True, "rounds": len(rounds), "records": last.get("records") if last else None,
            "saturated": saturated, "stop_reason": stop, "final": final,
            "new_pains": list(last.get("new_pains") or []) if last else [],
            "rank_changes": len(last.get("rank_changes") or []) if last else 0, "verdict": verdict}


def needs_calls_of(run, room: str) -> tuple:
    """(value or None, reasoning, notes, errors). A missing sources.json gives None and a note."""
    p = common.room_dir(run, room) / "sources.json"
    if not p.exists():
        return None, "", [f"room {room}: no sources.json, so needs_calls is unknown (the listener writes it in mode synthesize)."], []
    try:
        data = common.read_json(p)
    except ValueError as e:  # json.JSONDecodeError is a ValueError
        return None, "", [], [f"{common.rel(p)}: not valid JSON ({e}). Fix the file."]
    nc = data.get("needs_calls") if isinstance(data, dict) else None
    if not isinstance(nc, dict) or not isinstance(nc.get("value"), bool):
        return None, "", [], [f"{common.rel(p)}: needs_calls must be an object like "
                              f"{{\"value\": false, \"reasoning\": \"...\", \"confidence\": \"moderate\"}}."]
    errors = common.check_judgment(nc, f"{common.rel(p)}: needs_calls")
    if errors:
        return None, "", [], errors
    return bool(nc["value"]), str(nc.get("reasoning") or ""), [], []


def dead_pains_from_other_runs(run) -> dict:
    """pain item -> its graveyard entry, for pains still dead in graveyard.md.

    Lines dated on this run's own date are ignored: they are this run's own kills
    (this stage on an earlier rerun, or a later stage), and rerunning `pains`
    must give the same answer whatever ran after it.
    """
    return common.dead_entries("pain", ignore_date=common.run_date(run).isoformat())


# --------------------------------------------------------------------------- the stage
def _tags_for(record_count: int, thin_below: int, n_domains: int, spend_min: int, sources: dict, pct: int, total: int) -> list:
    tags = []
    if record_count < thin_below:
        tags.append("[thin]")
    if n_domains < spend_min:
        tags.append(f"[spend: {n_domains} source{'s' if n_domains != 1 else ''}]")
    if total > 0 and set(sources) == {"websearch"}:
        tags.append("[titles only]")
    tags.append(f"[undated share: {pct}%]")
    return tags


def pains(run) -> dict:
    rd = common.run_dir(run)
    rules = common.load_kill_rules()
    s3 = rules.get("stage3") or {}
    min_verified = int(s3.get("min_verified_quotes", 2))
    min_words = quote_check.min_words_from_rules(rules)
    drop_flat = bool(s3.get("drop_if_no_money_no_failed_spend_no_urgency", True))
    thin_below = int(s3.get("thin_below_records", 15))
    spend_min = int(s3.get("spend_sources_min", 2))
    max_keep = int(s3.get("max_pains_total", 25))
    q_min = int(s3.get("quotes_per_pain_min", 3))
    q_max = int(s3.get("quotes_per_pain_max", 5))
    urgency_order = [str(x) for x in (s3.get("urgency_order") or DEFAULT_URGENCY_ORDER)]
    rank_by = [str(x) for x in (s3.get("rank_by") or DEFAULT_RANK_BY)]
    if max_keep < 1:
        raise common.ValidationErrors(["kill_rules.yaml: stage3.max_pains_total must be at least 1."])

    rooms = draft_rooms(run)
    if not rooms:
        raise common.MissingInput(f"No pains_draft.json in any room under {common.rel(common.listen_dir(run) / 'rooms')}/. "
                                  f"The listeners write it in mode synthesize.")
    grave_by_item = dead_pains_from_other_runs(run)

    errors: list = []
    review_notes: list = []
    info_notes: list = []
    all_pains: list = []
    csv_rows: list = []
    room_info: dict = {}
    alt_items: list = []
    quotes_pass = quotes_fail = 0
    for room in rooms:
        draft = load_draft(run, room)
        counts = load_counts(run, room)
        cpains = counts["pains"]
        stored = records.records_by_id(run, room)
        draft_rel = common.rel(common.room_dir(run, room) / "pains_draft.json")
        seen_keys: set = set()
        room_pains: list = []
        for i, pain in enumerate(draft, 1):
            where = f"{draft_rel}: pain {i} ({pain.get('pain_key', '?') if isinstance(pain, dict) else '?'})"
            errs = validate_pain(pain, where, cpains, stored, urgency_order)
            key = pain.get("pain_key") if isinstance(pain, dict) else None
            if common.is_slug(key):
                if key in seen_keys:
                    errs.append(f"{where}: pain_key {key!r} appears twice in the draft. Keep one.")
                seen_keys.add(key)
            if errs:
                errors.extend(errs)
                continue
            pid = common.pain_id(room, key)
            c = cpains[key]
            quotes = pain.get("quotes") or []
            verified, rows = quote_check.check_quotes(pid, quotes, stored, min_words)
            csv_rows.extend(rows)
            n_pass = len(verified)
            n_fail = len(rows) - n_pass
            quotes_pass += n_pass
            quotes_fail += n_fail
            corrected = sum(1 for r in rows if r["citation_corrected"] == "yes")
            fail_reasons: dict = {}
            for r in rows:
                if r["status"] != "pass":
                    fail_reasons[r["reason"]] = fail_reasons.get(r["reason"], 0) + 1
            member_ids = sorted(c.get("member_record_ids") or [])
            spend = pain.get("spend_evidence") or []
            domains = spend_domains(spend, stored)
            support = supporting_record_ids(member_ids, verified, spend, stored)
            sources = _sources_of(support, stored)
            pct, undated, total = undated_share(support, stored)
            record_count = int(c.get("record_count", len(member_ids)))
            money = int(c.get("money_mentions", 0))
            failed = int(c.get("failed_spend_mentions", 0))
            utype = pain["urgency"].get("type")
            tags = _tags_for(record_count, thin_below, len(domains), spend_min, sources, pct, total)
            notes: list = []
            if len(quotes) < q_min:
                notes.append(f"{len(quotes)} quote(s) drafted; the target is {q_min} to {q_max}.")
            elif len(quotes) > q_max:
                notes.append(f"{len(quotes)} quotes drafted; the target is {q_min} to {q_max}.")
            if n_fail:
                notes.append(f"{n_fail} quote(s) failed the quote check and were deleted: "
                             + ", ".join(f"{k} {v}" for k, v in sorted(fail_reasons.items())) + ".")
            if corrected:
                notes.append(f"{corrected} citation(s) corrected to the stored url and date.")
            spend_out = []
            for item in spend:
                it = dict(item)
                url = it.get("url")
                if not _is_url(url):
                    url = (stored.get(it.get("record_id")) or {}).get("url") if isinstance(it.get("record_id"), str) else None
                it["domain"] = common.domain_of(url or "")
                spend_out.append(it)
            alternatives = [dict(a) for a in (pain.get("alternatives") or [])]
            for i_alt, a in enumerate(alternatives, 1):
                alt_items.append((f"{pid} alternative {i_alt}", a))
            entry = {
                "pain_id": pid, "room": room, "pain_key": key,
                "status": "kept", "rank": None, "drop_reason": None,
                "label": c.get("label", ""),
                "description": pain.get("description"),
                "urgency": dict(pain["urgency"]), "urgency_type": utype,
                "who_pays": dict(pain["who_pays"]),
                "alternatives": alternatives,
                "sellers": list(pain.get("sellers") or []),
                "spend_evidence": spend_out,
                "spend_domains": domains, "spend_sources": len(domains),
                "ladder_position": pain.get("ladder_position"),
                "record_count": record_count, "money_mentions": money, "failed_spend_mentions": failed,
                "seller_records": int(c.get("seller_records", 0)), "media_records": int(c.get("media_records", 0)),
                "member_record_ids": member_ids,
                "quotes": verified, "verified_quote_count": n_pass,
                "quote_check": {"checked": len(rows), "passed": n_pass, "failed": n_fail, "citations_corrected": corrected,
                                "failed_reasons": dict(sorted(fail_reasons.items()))},
                "supporting_records": total, "undated_records": undated, "undated_share": pct,
                "sources": sources,
                "tags": tags,
                "notes": notes,
            }
            # drop rules, in order
            item_name = f"pain:{pid}"
            if item_name in grave_by_item:
                g = grave_by_item[item_name]
                entry["status"] = "dropped"
                entry["drop_reason"] = (f"dead in graveyard.md since {g.get('date', '?')} ({g.get('stage', '?')}): "
                                        f"{g.get('reason', 'no reason recorded')}. Revive it with a new-evidence line first.")
                entry["graveyard_line_added"] = False
            elif n_pass < min_verified:
                entry["status"] = "dropped"
                entry["drop_reason"] = (f"fewer than {min_verified} verified quotes: {n_pass} of {len(rows)} passed the "
                                        f"quote check" + (" (" + ", ".join(f"{k} {v}" for k, v in sorted(fail_reasons.items())) + ")"
                                                          if fail_reasons else ""))
            elif drop_flat and money == 0 and failed == 0 and utype == "none":
                entry["status"] = "dropped"
                entry["drop_reason"] = ("no money mention, no failed spend and urgency none "
                                        f"(money 0, failed spend 0, urgency none, member records {record_count})")
            room_pains.append(entry)
        all_pains.extend(room_pains)
        nc_value, nc_reasoning, nc_notes, nc_errors = needs_calls_of(run, room)
        info_notes.extend(nc_notes)
        errors.extend(nc_errors)
        sat = saturation_verdict(run, room)
        totals = counts.get("totals") or {}
        room_info[room] = {
            "labeled": int(counts.get("labeled", 0)),
            "member_records": int(totals.get("member_records", 0)),
            "by_source": dict(totals.get("by_source") or {}),
            "pains_drafted": len(draft), "pains_kept": 0, "pains_cut": 0, "pains_dropped": 0,
            "needs_calls": nc_value, "needs_calls_reasoning": nc_reasoning,
            "saturation": sat,
        }
    if errors:
        raise common.ValidationErrors(errors)

    # the price checker on every alternative (offline -> blocked_by_network, shown as [measured, page not checked])
    checked = prices.check_items(run, STAGE, "pains", alt_items)
    price_by_where = {r["where"]: r for r in checked["items"]}
    for p in all_pains:
        for i_alt, a in enumerate(p["alternatives"], 1):
            r = price_by_where[f"{p['pain_id']} alternative {i_alt}"]
            a["price_status"] = r["status"]
            a["price_tag"] = r["tag"]
            a["price_detail"] = r["detail"]

    survivors = sorted((p for p in all_pains if p["status"] != "dropped"), key=lambda p: rank_key(p, rank_by, urgency_order))
    for i, p in enumerate(survivors, 1):
        p["rank"] = i
        p["status"] = "kept" if i <= max_keep else "cut"
    dropped = sorted((p for p in all_pains if p["status"] == "dropped"), key=lambda p: p["pain_id"])
    kept = [p for p in survivors if p["status"] == "kept"]
    cut = [p for p in survivors if p["status"] == "cut"]
    for p in all_pains:
        room_info[p["room"]][f"pains_{p['status']}"] += 1

    date = common.run_date(run)
    kills: dict = {}
    for p in dropped:
        if p.get("graveyard_line_added") is False:
            continue  # already dead in the graveyard; no second line
        kills[f"pain:{p['pain_id']}"] = p["drop_reason"]
        p["graveyard_line_added"] = not common.is_dry_run()
    for p in cut:
        p["drop_reason"] = (f"cut: ranked {p['rank']} of {len(survivors)} survivors and max_pains_total is {max_keep}; "
                            f"failed spend {p['failed_spend_mentions']}, money {p['money_mentions']}, urgency "
                            f"{p['urgency_type']}, member records {p['record_count']}")
        kills[f"pain:{p['pain_id']}"] = p["drop_reason"]
        p["graveyard_line_added"] = not common.is_dry_run()
    for p in kept:
        p["graveyard_line_added"] = False
    # the graveyard says exactly what this run of `pains` dropped or cut: a pain a rerun keeps loses its same-date line
    common.sync_graveyard(date, STAGE, [f"pain:{p['pain_id']}" for p in all_pains], kills)
    if common.is_dry_run() and kills:
        info_notes.append("dry run: no graveyard line was written for " + ", ".join(sorted(kills)) + ".")

    needs_calls_rooms = sorted(r for r, info in room_info.items() if info["needs_calls"] is True)
    if needs_calls_rooms:
        review_notes.append("Rooms that need calls (public text under-represents their people): "
                            + ", ".join(needs_calls_rooms) + ".")
    no_sat = sorted(r for r, info in room_info.items() if not info["saturation"]["available"])
    if no_sat:
        review_notes.append("Rooms with no saturation verdict (saturation.json missing): " + ", ".join(no_sat) + ".")
    not_sat = sorted(r for r, info in room_info.items()
                     if info["saturation"]["available"] and info["saturation"]["saturated"] is not True)
    if not_sat:
        review_notes.append("Rooms that stopped before saturation: "
                            + "; ".join(f"{r} ({room_info[r]['saturation']['verdict']})" for r in not_sat) + ".")
    thin = [p["pain_id"] for p in kept if "[thin]" in p["tags"]]
    if thin:
        info_notes.append(f"Kept pains tagged [thin] (fewer than {thin_below} member records): {', '.join(thin)}.")
    titles_only = [p["pain_id"] for p in kept if "[titles only]" in p["tags"]]
    if titles_only:
        info_notes.append(f"Kept pains supported by web-search titles only: {', '.join(titles_only)}.")
    for n in review_notes:
        common.log_event(run, STAGE, "pains", "note", note=n, review=True)
    for n in info_notes:
        common.log_event(run, STAGE, "pains", "note", note=n, review=False)

    result = {
        "max_pains_total": max_keep,
        "rank_by": rank_by,
        "urgency_order": urgency_order,
        "rules": {"min_verified_quotes": min_verified, "quote_min_words": min_words,
                  "drop_if_no_money_no_failed_spend_no_urgency": drop_flat,
                  "thin_below_records": thin_below, "spend_sources_min": spend_min},
        "counts": {"rooms": len(rooms), "drafted": len(all_pains), "survived": len(survivors), "kept": len(kept),
                   "cut": len(cut), "dropped": len(dropped), "quotes_pass": quotes_pass, "quotes_fail": quotes_fail},
        "kept": [p["pain_id"] for p in kept],
        "cut": [p["pain_id"] for p in cut],
        "dropped": [p["pain_id"] for p in dropped],
        "pains": kept + cut + dropped,
        "rooms": dict(sorted(room_info.items())),
        "needs_calls": needs_calls_rooms,
        "review_notes": review_notes,
        "notes": info_notes,
        "price_check": {"counts": checked["counts"], "blocked_domains": checked["blocked_domains"]},
        "tag_meaning": TAG_MEANING,
    }
    ldir = common.listen_dir(run)
    quote_check.write_csv(ldir / "quote_check.csv", csv_rows)
    common.write_json(ldir / "pains.json", result)
    common.write_text(ldir / "pains.md", render_md(result, run))
    common.log_event(run, STAGE, "pains", "count", rooms=len(rooms), drafted=len(all_pains), kept=len(kept),
                     cut=len(cut), dropped=len(dropped), max_pains_total=max_keep, quotes_pass=quotes_pass,
                     quotes_fail=quotes_fail,
                     by_room={r: {"drafted": i["pains_drafted"], "kept": i["pains_kept"]} for r, i in result["rooms"].items()},
                     needs_calls=needs_calls_rooms)
    return result


# --------------------------------------------------------------------------- rendering
def _cell(s) -> str:
    return common.normalize_ws(str(s if s is not None else "")).replace("|", "/")


def price_tag_of(item: dict) -> str:
    """The price checker's tag for an alternative; without a check on record the page counts as not checked."""
    tag = item.get("price_tag") if isinstance(item, dict) else None
    return tag if isinstance(tag, str) and tag else prices.TAG_NOT_CHECKED


def _price_line(item: dict) -> str:
    return (f"{_cell(item.get('what'))}: {_cell(item.get('price_text'))} ({item.get('currency')} {item.get('amount')} "
            f"per {item.get('unit')}) {price_tag_of(item)} <{item.get('url')}>")


def _pain_section(p: dict, heading: str) -> list:
    lines = ["", heading, ""]
    lines.append(f"- Room: {p['room']}. Pain key: {p['pain_key']}. Ladder position: {p['ladder_position']}.")
    lines.append(f"- In their words: {_cell(p['description'])}")
    u = p["urgency"]
    ev = _cell(u.get("evidence"))
    lines.append(f"- Urgency: {p['urgency_type']}." + (f" {ev}" if ev else "") + f" {_cell(u.get('reasoning'))} "
                 f"(confidence {u.get('confidence')}; records: {', '.join(u.get('record_ids') or []) or 'none'})")
    lines.append(f"- Who pays: {_cell(p['who_pays'].get('text'))} {_cell(p['who_pays'].get('reasoning'))} "
                 f"(confidence {p['who_pays'].get('confidence')})")
    lines.append(f"- Counts [measured]: member records {p['record_count']}, money mentions {p['money_mentions']}, "
                 f"failed spend mentions {p['failed_spend_mentions']}, seller records {p['seller_records']}, "
                 f"media records {p['media_records']}. Supporting records {p['supporting_records']} "
                 f"({p['undated_records']} undated). Sources: "
                 + (", ".join(f"{k} {v}" for k, v in p["sources"].items()) or "none") + ".")
    lines.append(f"- Spend evidence: {p['spend_sources']} distinct domain(s): {', '.join(p['spend_domains']) or 'none'}.")
    if p["alternatives"]:
        lines.append("- Alternatives and prices:")
        for a in p["alternatives"]:
            lines.append(f"  - {_price_line(a)}")
    else:
        lines.append("- Alternatives and prices: none given.")
    if p["sellers"]:
        lines.append("- Sellers and their complaints:")
        for s in p["sellers"]:
            comp = "; ".join(_cell(c) for c in (s.get("complaints") or [])) or "no complaints recorded"
            ids = ", ".join(s.get("complaint_record_ids") or [])
            lines.append(f"  - {_cell(s.get('name'))}" + (f" <{s.get('url')}>" if s.get("url") else "") + f": {comp}"
                         + (f" (records: {ids})" if ids else ""))
    else:
        lines.append("- Sellers: none listed.")
    lines.append(f"- Tags: {' '.join(p['tags'])}")
    lines.append(f"- Quotes ({p['verified_quote_count']} verified of {p['quote_check']['checked']} checked):")
    for q in p["quotes"]:
        lines.append(f"  - \"{_cell(q.get('text'))}\" <{q.get('url')}> ({q.get('date') or 'undated'}; record {q.get('record_id')})")
    for n in p["notes"]:
        lines.append(f"- Note: {_cell(n)}")
    return lines


def render_md(result: dict, run) -> str:
    c = result["counts"]
    r = result["rules"]
    lines = [
        "# Stage 3: pains",
        "",
        f"Run: {common.run_name(run)}.",
        f"{c['rooms']} room(s) with a pains draft. {c['drafted']} pains drafted. {c['kept']} kept (at most "
        f"{result['max_pains_total']} across all rooms), {c['cut']} cut for rank, {c['dropped']} dropped.",
        f"Quotes: {c['quotes_pass']} passed the quote check, {c['quotes_fail']} failed and were deleted "
        f"(details in quote_check.csv).",
        "",
        "A pain is a problem a room describes in its own words. A verified quote is one the checker found word for word "
        "inside the stored record it cites. Failed spend means someone paid for something that did not solve the problem.",
        "",
        "Drop rules, in order:",
        "",
        f"1. fewer than {r['min_verified_quotes']} verified quotes (a quote needs at least {r['quote_min_words']} words);",
        "2. no money mention, no failed spend and urgency none"
        + ("" if r["drop_if_no_money_no_failed_spend_no_urgency"] else " (switched off in kill_rules.yaml)") + ";",
        "3. a pain that an earlier run sent to graveyard.md stays dropped unless a new-evidence line revives it.",
        "",
        "Tags:",
        "",
    ]
    for tag, meaning in TAG_MEANING.items():
        lines.append(f"- `{tag}`: {meaning}.")
    lines += ["", f"Ranking: {', '.join(result['rank_by'])}, then pain id. Urgency order: "
                  f"{' > '.join(result['urgency_order'])}.", ""]
    lines += [f"## Kept pains ({c['kept']})", ""]
    kept = [p for p in result["pains"] if p["status"] == "kept"]
    if kept:
        lines.append("| Rank | Pain | Room | Urgency | Failed spend | Money | Member records | Verified quotes | Spend sources | Tags |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for p in kept:
            lines.append(f"| {p['rank']} | {p['pain_id']} | {p['room']} | {p['urgency_type']} | {p['failed_spend_mentions']} | "
                         f"{p['money_mentions']} | {p['record_count']} | {p['verified_quote_count']} | {p['spend_sources']} | "
                         f"{_cell(' '.join(p['tags']))} |")
        for p in kept:
            lines += _pain_section(p, f"### {p['rank']}. {p['pain_id']}" + (f": {_cell(p['label'])}" if p.get("label") else ""))
    else:
        lines.append("No pain survived the drop rules.")
    lines += ["", f"## Cut for rank ({c['cut']})", ""]
    cut = [p for p in result["pains"] if p["status"] == "cut"]
    if cut:
        lines.append("These pains passed every rule but ranked below the limit. They are in graveyard.md.")
        lines.append("")
        for p in cut:
            lines.append(f"- rank {p['rank']}: {p['pain_id']} (failed spend {p['failed_spend_mentions']}, money "
                         f"{p['money_mentions']}, urgency {p['urgency_type']}, member records {p['record_count']}, "
                         f"tags {_cell(' '.join(p['tags']))})")
    else:
        lines.append("None.")
    lines += ["", f"## Dropped pains ({c['dropped']})", ""]
    dropped = [p for p in result["pains"] if p["status"] == "dropped"]
    if dropped:
        lines.append("| Pain | Why |")
        lines.append("|---|---|")
        for p in dropped:
            lines.append(f"| {p['pain_id']} | {_cell(p['drop_reason'])} |")
    else:
        lines.append("None.")
    lines += ["", "## Rooms", "",
              "Saturation means the last window of new records added no new pain and changed no pain's rank. "
              "Needs calls means the room's people are under-represented in public text (older, offline or businesses).",
              "",
              "| Room | Labeled records | Member records | Pains drafted | Kept | Saturation | Needs calls |",
              "|---|---|---|---|---|---|---|"]
    for room, info in result["rooms"].items():
        nc = info["needs_calls"]
        nc_s = "unknown" if nc is None else ("yes" if nc else "no")
        lines.append(f"| {room} | {info['labeled']} | {info['member_records']} | {info['pains_drafted']} | {info['pains_kept']} | "
                     f"{_cell(info['saturation']['verdict'])} | {nc_s} |")
    lines += ["", "## For REVIEW.md", ""]
    if result["review_notes"]:
        lines += [f"- {n}" for n in result["review_notes"]]
    else:
        lines.append("Nothing to flag.")
    if result["notes"]:
        lines += ["", "## Notes", ""]
        lines += [f"- {n}" for n in result["notes"]]
    pc = result.get("price_check") or {}
    lines += ["", "## Price checks on the alternatives", "",
              "Counts: " + (", ".join(f"{k} {v}" for k, v in sorted((pc.get("counts") or {}).items())) or "no alternatives") + ". "
              "`[measured]` = the page was opened and shows the price text; `[measured, page not checked]` = the price was "
              "read in a search result or the page could not be opened; `[not found on page]` = the page was opened and "
              "does not show it."]
    if pc.get("blocked_domains"):
        lines.append("Domains to allow so the price pages can be opened: " + ", ".join(pc["blocked_domains"]) + ".")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------------------- command
def cmd_pains(args) -> int:
    run = common.run_dir(args.run)
    result = pains(run)
    c = result["counts"]
    print(f"Pains: {c['rooms']} room(s), {c['drafted']} drafted, {c['kept']} kept (max {result['max_pains_total']}), "
          f"{c['cut']} cut, {c['dropped']} dropped. Quotes: {c['quotes_pass']} pass, {c['quotes_fail']} fail.")
    for p in result["pains"]:
        if p["status"] == "kept":
            print(f"  kept #{p['rank']}: {p['pain_id']} (failed spend {p['failed_spend_mentions']}, money {p['money_mentions']}, "
                  f"urgency {p['urgency_type']}, records {p['record_count']}, quotes {p['verified_quote_count']}/"
                  f"{p['quote_check']['checked']}, tags: {' '.join(p['tags'])})")
    for p in result["pains"]:
        if p["status"] == "cut":
            print(f"  cut #{p['rank']}: {p['pain_id']}")
    for p in result["pains"]:
        if p["status"] == "dropped":
            print(f"  dropped: {p['pain_id']}: {p['drop_reason']}")
    for room, info in result["rooms"].items():
        nc = info["needs_calls"]
        print(f"  room {room}: {info['saturation']['verdict']}; needs calls: "
              f"{'unknown' if nc is None else ('yes' if nc else 'no')}")
    for n in result["review_notes"]:
        print(f"review: {n}")
    for n in result["notes"]:
        print(f"note: {n}")
    if result["price_check"]["blocked_domains"]:
        print("Domains to allow for the alternatives' price pages: " + ", ".join(result["price_check"]["blocked_domains"]))
    ldir = common.listen_dir(run)
    print(f"Wrote {common.rel(ldir / 'pains.json')}, {common.rel(ldir / 'pains.md')}, "
          f"{common.rel(ldir / 'quote_check.csv')} and graveyard.md")
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("pains", help="Join every room's pains draft with its counts, check quotes, apply the drop rules, "
                                            "rank and keep at most max_pains_total; write pains.json, pains.md and quote_check.csv.")
    p.set_defaults(func=cmd_pains, stage_no=STAGE)
