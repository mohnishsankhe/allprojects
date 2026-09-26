"""The quote checker (rule 1) and the `quote-check` self-check command.

A quote passes only if its record_id exists among the room's stored records,
normalize_ws(quote) is a substring of normalize_ws(record.text), and it has at
least quote_min_words words. Case, punctuation, curly quotes and dashes must
match. A quote may be the whole record (a title). If the quote's url or date
differs from the record, the stored values replace them (citation corrected).

Public API
----------
    REASONS = ("ok", "record_missing", "not_substring", "too_short", "empty")
    CSV_COLUMNS                       the quote_check.csv columns
    count_words(text) -> int
    check_quote(quote, records_by_id, min_words) -> dict
        {"status": "pass"|"fail", "reason", "citation_corrected": bool, "record_id", "url", "date", "quote"}
        url and date are the stored record's when it exists.
    check_quotes(pain_id, quotes, records_by_id, min_words) -> (verified, rows)
        verified: quotes that pass, as {"record_id", "url", "date", "text"} with corrected citations
        rows: one CSV row dict per quote (pain_id, record_id, status, reason, citation_corrected, url, date, quote)
    write_csv(path, rows) -> None
    min_words_from_rules(rules=None) -> int
    register(subparsers)              adds `quote-check --room R`
"""
from __future__ import annotations

import csv
from pathlib import Path

import common
import records

STAGE = 3
REASONS = ("ok", "record_missing", "not_substring", "too_short", "empty")
CSV_COLUMNS = ["pain_id", "record_id", "status", "reason", "citation_corrected", "url", "date", "quote"]


def count_words(text) -> int:
    return len(common.normalize_ws(text or "").split())


def min_words_from_rules(rules=None) -> int:
    rules = rules if rules is not None else common.load_kill_rules()
    return int(rules.get("stage3", {}).get("quote_min_words", 5))


def check_quote(quote, records_by_id: dict, min_words: int) -> dict:
    q = quote if isinstance(quote, dict) else {}
    text = q.get("text") if isinstance(q.get("text"), str) else ""
    rid = q.get("record_id") if isinstance(q.get("record_id"), str) else ""
    url = q.get("url") if isinstance(q.get("url"), str) else None
    date = q.get("date") if isinstance(q.get("date"), str) else None
    norm_q = common.normalize_ws(text)
    rec = records_by_id.get(rid) if rid else None
    corrected = False
    out_url, out_date = url, date
    if rec is not None:
        out_url = rec.get("url") or ""
        out_date = rec.get("date")
        corrected = (url != out_url) or (date != out_date)
    if not norm_q:
        reason = "empty"
    elif rec is None:
        reason = "record_missing"
    elif norm_q not in common.normalize_ws(rec.get("text") or ""):
        reason = "not_substring"
    elif count_words(norm_q) < min_words:
        reason = "too_short"
    else:
        reason = "ok"
    return {
        "status": "pass" if reason == "ok" else "fail",
        "reason": reason,
        "citation_corrected": bool(corrected and reason == "ok"),
        "record_id": rid,
        "url": out_url or "",
        "date": out_date,
        "quote": text,
    }


def check_quotes(pain_id: str, quotes, records_by_id: dict, min_words: int) -> tuple:
    verified = []
    rows = []
    for q in quotes or []:
        r = check_quote(q, records_by_id, min_words)
        rows.append({
            "pain_id": pain_id,
            "record_id": r["record_id"],
            "status": r["status"],
            "reason": r["reason"],
            "citation_corrected": "yes" if r["citation_corrected"] else "no",
            "url": r["url"],
            "date": r["date"] or "",
            "quote": r["quote"],
        })
        if r["status"] == "pass":
            verified.append({"record_id": r["record_id"], "url": r["url"], "date": r["date"], "text": r["quote"]})
    return verified, rows


def write_csv(path, rows) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS, lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in CSV_COLUMNS})


def _explain(reason: str, rid: str, room: str) -> str:
    if reason == "empty":
        return "the quote text is empty. Copy exact words from a record."
    if reason == "record_missing":
        return f"record {rid or '(none)'} is not stored for room {room}. Use a record_id from the batches."
    if reason == "not_substring":
        return (f"not an exact substring of record {rid}. Copy the text character for character from "
                f"`funnel show --room {room} --ids {rid}`.")
    if reason == "too_short":
        return "too few words. Quote a longer passage."
    return reason


def cmd_quote_check(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    draft = common.room_dir(run, room) / "pains_draft.json"
    common.require_file(draft, "The listener writes it in mode synthesize.")
    data = common.read_json(draft)
    pains = data.get("pains") if isinstance(data, dict) else None
    if not isinstance(pains, list):
        raise common.ValidationErrors([f"{common.rel(draft)}: needs a 'pains' list."])
    rules = common.load_kill_rules()
    min_words = min_words_from_rules(rules)
    min_verified = int(rules.get("stage3", {}).get("min_verified_quotes", 2))
    by_id = records.records_by_id(run, room)
    errors = []
    total_pass = total_fail = 0
    for i, pain in enumerate(pains):
        key = pain.get("pain_key") if isinstance(pain, dict) else None
        if not common.is_slug(key):
            errors.append(f"{common.rel(draft)}: pain {i + 1}: 'pain_key' {key!r} must be a slug.")
            continue
        pid = common.pain_id(room, key)
        quotes = pain.get("quotes") or []
        verified, rows = check_quotes(pid, quotes, by_id, min_words)
        for n, row in enumerate(rows, 1):
            if row["status"] == "pass":
                total_pass += 1
                fix = " (citation corrected to the stored url/date)" if row["citation_corrected"] == "yes" else ""
                print(f"{pid} quote {n}: ok{fix}")
            else:
                total_fail += 1
                print(f"{pid} quote {n}: FAIL {row['reason']}")
                errors.append(f"{common.rel(draft)}: pain {key} quote {n}: {_explain(row['reason'], row['record_id'], room)}")
        verdict = "ok" if len(verified) >= min_verified else f"below the minimum of {min_verified}: `pains` will drop it"
        print(f"{pid}: {len(verified)} of {len(rows)} quotes verified ({verdict}).")
    print(f"Quotes: {total_pass} pass, {total_fail} fail. Nothing was written.")
    common.log_event(run, STAGE, "quote-check", "check", room=room, quotes_pass=total_pass, quotes_fail=total_fail)
    if errors:
        raise common.ValidationErrors(errors)
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("quote-check", help="Check every quote in a room's pains_draft.json against stored records.")
    p.add_argument("--room", required=True, help="room slug")
    p.set_defaults(func=cmd_quote_check)
