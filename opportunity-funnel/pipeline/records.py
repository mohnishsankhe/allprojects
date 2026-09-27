"""Stored records (Stage 3 evidence) and the `batches` command.

A record is one piece of public text, anonymized, with a stable id, URL and date
(rule 1). Records live in RUN/03_listen/raw/<room>/<source>.jsonl, one JSON
object per line, in collection order. Only these fields are ever stored:
record_id, source, url, date, text, meta. Author fields never reach disk.

Public API
----------
    RECORD_FIELDS = ("record_id", "source", "url", "date", "text", "meta")
    source_file(run, room, source) -> Path
        raw/<room>/<source>.jsonl (characters outside [a-z0-9_-] become "_")
    store_records(run, room, source, records, known_names=(), command="store") -> dict
        Anonymizes each record's text (known_names are always removed), computes
        record_id(url, text), skips ids already stored in the room, appends the rest.
        A record whose url is a person's profile or channel page (anonymize.is_profile_url)
        is refused: rule 5 keeps only the URL of the post itself (counted in skipped_profile).
        Each input record: {"url", "text", "date": "YYYY-MM-DD"|None, "meta": {...}}.
        Returns {"new", "duplicates", "skipped_empty", "skipped_profile", "new_ids", "file"}.
    load_records(run, room) -> list[dict]
        All records of the room in collection order (files by name, then line order).
    records_by_id(run, room) -> dict[str, dict]
    record_round(rec) -> int          meta.round, else meta.order[0], else 0
    lookback_cutoff(date, months) -> datetime.date
    money_hint(text) -> bool          currency symbols/codes, amounts, pay/paid/fee/cost/price/refund/lakh/k
    batches_dir(run, room) -> Path    raw/<room>/_batches
    manifest_path(run, room) -> Path  rooms/<room>/batches.json
    make_batches(run, room, size=80, chars=1500) -> dict
        Filters (lookback from the RUN date, undated kept and tagged when
        include_undated_records, normalized-text duplicates dropped keeping the first
        in collection order), orders by meta.order (else newest first), writes
        batch_r<round>_<NNN>.md files and the manifest; removes stale batch files.
        A record dated only by month (meta.date_precision "month", from a /YYYY/MM/ URL)
        is dropped only when its whole month lies before the cutoff: a URL that shows
        only the cutoff month does not show a date older than the lookback (kept and
        counted in kept_month_at_cutoff; the conservative reading of the kill rule).
    register(subparsers)              adds the `batches` command
"""
from __future__ import annotations

import calendar
import datetime as _dt
import re
from pathlib import Path

import common
from anonymize import LIMIT_NOTE, anonymize, is_profile_url

RECORD_FIELDS = ("record_id", "source", "url", "date", "text", "meta")
STAGE = 3

_MONEY_RE = re.compile(
    r"[$₹€£¥]|"
    r"\b(?:usd|inr|eur|gbp|aed|sgd|cad|aud|rs\.?|rupees?|dollars?|euros?|pounds?|dirhams?|bucks)\b|"
    r"\b\d[\d,]*(?:\.\d+)?\s?(?:k|lakh|lakhs|lac|lacs|crore|crores|cr|mn|million|bn|billion)\b|"
    r"\b(?:pay|pays|paid|paying|payment|payments|fee|fees|cost|costs|costly|price|prices|priced|pricing|"
    r"refund|refunds|refunded|expensive|cheap|cheaper|afford|affordable|subscription|subscribe|charged|charges|"
    r"invoice|salary|budget|worth|discount|scam|scammed|waste of money|money)\b",
    re.IGNORECASE,
)


def _source_slug(source: str) -> str:
    s = re.sub(r"[^a-z0-9_-]+", "_", str(source).strip().lower())
    return s.strip("_") or "source"


def source_file(run, room: str, source: str) -> Path:
    return common.raw_dir(run, room) / f"{_source_slug(source)}.jsonl"


def batches_dir(run, room: str) -> Path:
    return common.raw_dir(run, room) / "_batches"


def manifest_path(run, room: str) -> Path:
    return common.room_dir(run, room) / "batches.json"


# --------------------------------------------------------------------------- load
def load_records(run, room: str) -> list:
    d = common.raw_dir(run, room)
    if not d.exists():
        return []
    out: list = []
    for p in sorted(d.glob("*.jsonl")):
        for rec in common.read_jsonl(p):
            if isinstance(rec, dict) and rec.get("record_id"):
                out.append(rec)
    return out


def records_by_id(run, room: str) -> dict:
    return {r["record_id"]: r for r in load_records(run, room)}


def record_round(rec: dict) -> int:
    meta = rec.get("meta") or {}
    r = meta.get("round")
    if isinstance(r, int) and not isinstance(r, bool):
        return r
    order = meta.get("order")
    if isinstance(order, list) and order and isinstance(order[0], int):
        return order[0]
    return 0


# --------------------------------------------------------------------------- store
def store_records(run, room: str, source: str, records, known_names=(), command: str = "store") -> dict:
    """Anonymize, fingerprint, dedupe against the room, append. Never stores author fields."""
    common.check_slug(room, "room")
    if not isinstance(source, str) or not source.strip():
        raise common.ValidationErrors(["store_records: source must be a non-empty name like 'websearch'."])
    existing = set(records_by_id(run, room).keys())
    path = source_file(run, room, source)
    new_ids: list = []
    duplicates = 0
    skipped_empty = 0
    skipped_profile = 0
    rows: list = []
    for i, rec in enumerate(records):
        if not isinstance(rec, dict):
            raise common.ValidationErrors([f"store_records: record {i} is not an object."])
        url = str(rec.get("url") or "").strip()
        if is_profile_url(url):
            skipped_profile += 1  # a person's page is not a post: never stored (rule 5)
            continue
        text = anonymize(rec.get("text") or "", known_names)
        if not common.normalize_ws(text):
            skipped_empty += 1
            continue
        date = rec.get("date")
        if date is not None and not common.is_date(date):
            raise common.ValidationErrors([f"store_records: record {i} ({url}): date {date!r} is not YYYY-MM-DD or null."])
        meta = rec.get("meta")
        meta = dict(meta) if isinstance(meta, dict) else {}
        rid = common.record_id(url, text)
        if rid in existing:
            duplicates += 1
            continue
        existing.add(rid)
        new_ids.append(rid)
        rows.append({"record_id": rid, "source": source, "url": url, "date": date, "text": text, "meta": meta})
    if rows:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            for row in rows:
                f.write(common.dumps_jsonl_row(row))
        common.log_event(run, STAGE, command, "note", room=room, source=source, note=LIMIT_NOTE, review=False)
    return {"new": len(new_ids), "duplicates": duplicates, "skipped_empty": skipped_empty,
            "skipped_profile": skipped_profile, "new_ids": new_ids, "file": common.rel(path)}


# --------------------------------------------------------------------------- batches
def lookback_cutoff(date: _dt.date, months: int) -> _dt.date:
    """The same day `months` months earlier (clamped to the month's last day)."""
    y, m = date.year, date.month - int(months)
    while m <= 0:
        m += 12
        y -= 1
    day = min(date.day, calendar.monthrange(y, m)[1])
    return _dt.date(y, m, day)


def money_hint(text: str) -> bool:
    return bool(_MONEY_RE.search(text or ""))


def _order_key(rec: dict):
    """Records with meta.order first (by that order), then the rest newest first, undated last."""
    meta = rec.get("meta") or {}
    order = meta.get("order")
    if isinstance(order, list) and order and all(isinstance(x, int) and not isinstance(x, bool) for x in order):
        return (0, tuple(order), 0, 0, rec["record_id"])
    date = rec.get("date")
    if date and common.is_date(date):
        return (1, (), 0, -_dt.date.fromisoformat(date).toordinal(), rec["record_id"])
    return (1, (), 1, 0, rec["record_id"])


def _cut(text: str, chars: int) -> str:
    t = text.strip()
    if chars and len(t) > chars:
        return t[:chars].rstrip() + " […cut]"
    return t


def _render_batch(name: str, room: str, rnd: int, recs: list, chars: int) -> str:
    lines = [f"# {name} | room {room} | round {rnd} | {len(recs)} records", ""]
    for rec in recs:
        date = rec.get("date") or "undated"
        domain = common.domain_of(rec.get("url") or "") or "-"
        lines.append(f"### {rec['record_id']} | {rec.get('source', '-')} | {date} | {domain}")
        lines.append(_cut(rec.get("text") or "", chars))
        lines.append(f"money_hint: {'yes' if money_hint(rec.get('text') or '') else 'no'}")
        lines.append("")
    return "\n".join(lines)


def make_batches(run, room: str, size: int = 80, chars: int = 1500) -> dict:
    common.check_slug(room, "room")
    if size < 1:
        raise common.ValidationErrors(["--size must be at least 1."])
    rules = common.load_kill_rules().get("stage3", {})
    months = int(rules.get("lookback_months", 24))
    include_undated = bool(rules.get("include_undated_records", True))
    cutoff = lookback_cutoff(common.run_date(run), months)

    loaded = load_records(run, room)
    kept: list = []
    seen_text: set = set()
    counts = {"loaded": len(loaded), "dropped_old": 0, "dropped_undated": 0, "undated_kept": 0,
              "dropped_duplicate_text": 0, "kept_month_at_cutoff": 0, "kept": 0}
    cutoff_s = cutoff.isoformat()
    for rec in loaded:  # collection order: the first copy of a text wins
        date = rec.get("date")
        if date:
            month_only = (rec.get("meta") or {}).get("date_precision") == "month"
            if month_only:
                if date[:7] < cutoff_s[:7]:
                    counts["dropped_old"] += 1
                    continue
                if date < cutoff_s:
                    counts["kept_month_at_cutoff"] += 1  # the URL shows only the cutoff month: not shown to be old
            elif date < cutoff_s:
                counts["dropped_old"] += 1
                continue
        elif not include_undated:
            counts["dropped_undated"] += 1
            continue
        key = common.normalize_ws(rec.get("text") or "")
        if key in seen_text:
            counts["dropped_duplicate_text"] += 1
            continue
        seen_text.add(key)
        if not date:
            counts["undated_kept"] += 1
        kept.append(rec)
    counts["kept"] = len(kept)

    kept.sort(key=_order_key)
    by_round: dict = {}
    for rec in kept:
        by_round.setdefault(record_round(rec), []).append(rec)

    bdir = batches_dir(run, room)
    bdir.mkdir(parents=True, exist_ok=True)
    batches: dict = {}
    rounds: dict = {}
    undated_ids: list = []
    files: dict = {}
    for rnd in sorted(by_round):
        recs = by_round[rnd]
        names = []
        for i in range(0, len(recs), size):
            chunk = recs[i:i + size]
            name = f"batch_r{rnd}_{i // size + 1:03d}"
            batches[name] = [r["record_id"] for r in chunk]
            files[name] = _render_batch(name, room, rnd, chunk, chars)
            names.append(name)
        rounds[str(rnd)] = {"batches": names, "records": len(recs)}
    undated_ids = sorted(r["record_id"] for r in kept if not r.get("date"))

    for stale in bdir.glob("batch_*.md"):
        if stale.stem not in files:
            stale.unlink()
    for name, text in files.items():
        common.write_text(bdir / f"{name}.md", text)

    manifest = {
        "room": room,
        "size": size,
        "chars": chars,
        "filters": dict(counts, lookback_months=months, lookback_cutoff=cutoff.isoformat(),
                        include_undated_records=include_undated),
        "batches": batches,
        "rounds": rounds,
        "undated_record_ids": undated_ids,
    }
    common.write_json(manifest_path(run, room), manifest)
    return manifest


# --------------------------------------------------------------------------- command
def cmd_batches(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    if not load_records(run, room):
        raise common.MissingInput(f"No records for room {room} in {common.rel(common.raw_dir(run, room))}. "
                                  f"Run `funnel harvest-search --room {room}` first.")
    manifest = make_batches(run, room, size=args.size, chars=args.chars)
    f = manifest["filters"]
    print(f"Room {room}: {f['loaded']} records loaded.")
    print(f"Dropped {f['dropped_old']} older than {f['lookback_cutoff']} ({f['lookback_months']} months before the run date).")
    if f["include_undated_records"]:
        print(f"Kept {f['undated_kept']} undated records (tagged undated in the batch files).")
    else:
        print(f"Dropped {f['dropped_undated']} undated records.")
    print(f"Dropped {f['dropped_duplicate_text']} duplicate texts. {f['kept']} records kept.")
    if f.get("kept_month_at_cutoff"):
        note = (f"Room {room}: {f['kept_month_at_cutoff']} record(s) dated only by month (a /YYYY/MM/ URL) fall in the "
                f"cutoff month {f['lookback_cutoff'][:7]} and were kept: the URL does not show a date older than the "
                f"lookback, so the conservative reading keeps them.")
        print(f"note: {note}")
        common.log_event(run, STAGE, "batches", "note", room=room, note=note, review=True)
    for rnd, info in manifest["rounds"].items():
        print(f"Round {rnd}: {info['records']} records in {len(info['batches'])} batch file(s): "
              f"{', '.join(info['batches'])}")
    print(f"Wrote {common.rel(manifest_path(run, room))} and {common.rel(batches_dir(run, room))}/")
    common.log_event(run, STAGE, "batches", "count", room=room, **{k: v for k, v in f.items()},
                     batches=len(manifest["batches"]))
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("batches", help="Split a room's records into batch files for labeling.")
    p.add_argument("--room", required=True, help="room slug")
    p.add_argument("--size", type=int, default=80, help="records per batch (default 80)")
    p.add_argument("--chars", type=int, default=1500, help="cut each record's text at this many characters (default 1500)")
    p.set_defaults(func=cmd_batches, stage_no=STAGE)
