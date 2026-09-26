"""Label validation, counting and saturation (Stage 3, rule 2).

Public API
----------
    VOICES = ("member", "seller", "media", "other")
    load_taxonomy(run, room) -> dict[key -> pain entry]
    load_manifest(run, room) -> dict                 rooms/<room>/batches.json
    manifest_record_ids(manifest) -> list[str]
    load_labels(run, room, manifest, taxonomy) -> (labels_by_id, notes)
        validated labels (raises ValidationErrors with every problem listed)
    compute_counts(run, room) -> dict                the counts.json content
    competition_rank(stats) -> dict[key -> rank]     stats: key -> (failed_spend, money, record_count)
    order_records(record_ids, records_by_id) -> list[str]   collection order: meta.order, then record_id
    member_pain_stats(record_ids, labels_by_id) -> dict[key -> (failed_spend, money, record_count)]
    saturation_entry(ordered_ids, labels_by_id, window, round_no, new_records) -> dict
    register(subparsers)                             adds `count` and `saturation`
"""
from __future__ import annotations

import common
import records

STAGE = 3
VOICES = ("member", "seller", "media", "other")
STOP_REASONS = ("saturated", "exhausted", "max_rounds")


# --------------------------------------------------------------------------- inputs
def load_taxonomy(run, room: str) -> dict:
    p = common.room_dir(run, room) / "taxonomy.json"
    common.require_file(p, "The listener writes it in round 1 (mode label).")
    data = common.read_json(p)
    pains = data.get("pains") if isinstance(data, dict) else None
    if not isinstance(pains, list) or not pains:
        raise common.ValidationErrors([f"{common.rel(p)}: needs a non-empty 'pains' list with a 'key' per pain."])
    out: dict = {}
    errors = []
    for i, entry in enumerate(pains, 1):
        key = entry.get("key") if isinstance(entry, dict) else None
        if not common.is_slug(key):
            errors.append(f"{common.rel(p)}: pain {i}: 'key' {key!r} must be a slug (lowercase letters, digits, hyphens).")
            continue
        if key in out:
            errors.append(f"{common.rel(p)}: pain {i}: key {key!r} appears twice. Keep one.")
            continue
        out[key] = entry
    if errors:
        raise common.ValidationErrors(errors)
    return out


def load_manifest(run, room: str) -> dict:
    p = records.manifest_path(run, room)
    common.require_file(p, f"Run `funnel batches --room {room}` first.")
    return common.read_json(p)


def manifest_record_ids(manifest: dict) -> list:
    ids: list = []
    for name in sorted((manifest.get("batches") or {}).keys()):
        ids.extend(manifest["batches"][name])
    return ids


def _label_signature(label: dict) -> tuple:
    return (label.get("voice"), tuple(sorted(label.get("pain_keys") or [])), label.get("money"), label.get("failed_spend"))


def load_labels(run, room: str, manifest: dict, taxonomy: dict) -> tuple:
    """Every label of the room, validated. Returns (labels_by_id, notes)."""
    ldir = common.room_dir(run, room) / "labels"
    files = sorted(ldir.glob("*.jsonl")) if ldir.exists() else []
    if not files:
        raise common.MissingInput(f"No label files in {common.rel(ldir)}/. The listener writes labels/<batch>.jsonl.")
    manifest_ids = manifest_record_ids(manifest)
    id_to_batch = {rid: name for name, ids in (manifest.get("batches") or {}).items() for rid in ids}
    known = set(manifest_ids)
    labels: dict = {}
    errors: list = []
    notes: list = []
    for p in files:
        rows = common.read_jsonl(p)
        for n, row in enumerate(rows, 1):
            where = f"{common.rel(p)}: line {n}"
            if not isinstance(row, dict):
                errors.append(f"{where}: must be an object.")
                continue
            rid = row.get("record_id")
            if not isinstance(rid, str) or rid not in known:
                errors.append(f"{where}: unknown record_id {rid!r}. Use ids from the batch files.")
                continue
            label = dict(row)
            voice = label.get("voice")
            if voice not in VOICES:
                errors.append(f"{where} ({rid}): 'voice' must be member, seller, media or other (got {voice!r}).")
            keys = label.get("pain_keys")
            if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys):
                errors.append(f"{where} ({rid}): 'pain_keys' must be a list of 0 to 2 keys.")
                keys = []
            else:
                deduped = []
                for k in keys:
                    if k not in deduped:
                        deduped.append(k)
                keys = deduped
                if len(keys) > 2:
                    errors.append(f"{where} ({rid}): more than 2 pain keys ({len(keys)}). Keep the two strongest.")
                for k in keys:
                    if k not in taxonomy:
                        errors.append(f"{where} ({rid}): unknown pain key {k!r}. Add it to taxonomy.json or fix the key.")
            label["pain_keys"] = keys
            for flag in ("money", "failed_spend"):
                if not isinstance(label.get(flag), bool):
                    errors.append(f"{where} ({rid}): '{flag}' must be true or false (got {label.get(flag)!r}).")
            errors.extend(f"{where} ({rid}): {e}" for e in common.check_judgment(label, "label"))
            if label.get("failed_spend") is True and label.get("money") is False:
                label["money"] = True
                notes.append(f"{rid}: failed_spend is true, so money was set to true.")
            if rid in labels:
                if _label_signature(labels[rid]) != _label_signature(label):
                    errors.append(f"{where} ({rid}): conflicts with an earlier label for the same record. Keep one.")
                continue
            labels[rid] = label
    missing_by_batch: dict = {}
    for rid in manifest_ids:
        if rid not in labels:
            missing_by_batch.setdefault(id_to_batch.get(rid, "?"), []).append(rid)
    for batch in sorted(missing_by_batch):
        ids = missing_by_batch[batch]
        shown = ", ".join(ids[:10]) + (f" and {len(ids) - 10} more" if len(ids) > 10 else "")
        errors.append(f"{common.rel(ldir)}/{batch}.jsonl: {len(ids)} record(s) in {batch}.md have no label: {shown}.")
    if errors:
        raise common.ValidationErrors(errors)
    return labels, notes


# --------------------------------------------------------------------------- counts
def compute_counts(run, room: str) -> dict:
    manifest = load_manifest(run, room)
    taxonomy = load_taxonomy(run, room)
    labels, notes = load_labels(run, room, manifest, taxonomy)
    stored = records.records_by_id(run, room)
    ids = manifest_record_ids(manifest)

    pains: dict = {}
    for key, entry in taxonomy.items():
        pains[key] = {
            "label": entry.get("label", ""),
            "record_count": 0, "member_record_ids": [],
            "money_mentions": 0, "money_record_ids": [],
            "failed_spend_mentions": 0, "failed_spend_record_ids": [],
            "seller_records": 0, "seller_record_ids": [],
            "media_records": 0, "media_record_ids": [],
        }
    by_voice = {v: 0 for v in VOICES}
    by_source: dict = {}
    member_with_pain = money_total = failed_total = 0
    for rid in ids:
        label = labels[rid]
        voice = label["voice"]
        by_voice[voice] += 1
        src = (stored.get(rid) or {}).get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
        keys = label["pain_keys"]
        if voice == "member":
            if keys:
                member_with_pain += 1
            if label["money"]:
                money_total += 1
            if label["failed_spend"]:
                failed_total += 1
            for k in keys:
                pains[k]["member_record_ids"].append(rid)
                if label["money"]:
                    pains[k]["money_record_ids"].append(rid)
                if label["failed_spend"]:
                    pains[k]["failed_spend_record_ids"].append(rid)
        elif voice == "seller":
            for k in keys:
                pains[k]["seller_record_ids"].append(rid)
        elif voice == "media":
            for k in keys:
                pains[k]["media_record_ids"].append(rid)
    for key, p in pains.items():
        for list_name, count_name in (("member_record_ids", "record_count"), ("money_record_ids", "money_mentions"),
                                      ("failed_spend_record_ids", "failed_spend_mentions"),
                                      ("seller_record_ids", "seller_records"), ("media_record_ids", "media_records")):
            p[list_name] = sorted(p[list_name])
            p[count_name] = len(p[list_name])
    return {
        "room": room,
        "records_in_manifest": len(ids),
        "labeled": len(ids),
        "pains": pains,
        "totals": {
            "by_voice": by_voice,
            "by_source": dict(sorted(by_source.items())),
            "member_records": by_voice["member"],
            "member_records_with_pain": member_with_pain,
            "money_mentions": money_total,
            "failed_spend_mentions": failed_total,
        },
        "notes": sorted(notes),
    }


def cmd_count(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    counts = compute_counts(run, room)
    out = common.room_dir(run, room) / "counts.json"
    common.write_json(out, counts)
    t = counts["totals"]
    bv = t["by_voice"]
    print(f"Room {room}: {counts['labeled']} labeled records "
          f"(member {bv['member']}, seller {bv['seller']}, media {bv['media']}, other {bv['other']}).")
    print("Sources: " + ", ".join(f"{k} {v}" for k, v in t["by_source"].items()))
    print(f"{'pain key':32} {'members':>8} {'money':>6} {'failed':>7} {'sellers':>8} {'media':>6}")
    for key in sorted(counts["pains"], key=lambda k: (-counts["pains"][k]["failed_spend_mentions"],
                                                     -counts["pains"][k]["money_mentions"],
                                                     -counts["pains"][k]["record_count"], k)):
        p = counts["pains"][key]
        print(f"{key:32} {p['record_count']:>8} {p['money_mentions']:>6} {p['failed_spend_mentions']:>7} "
              f"{p['seller_records']:>8} {p['media_records']:>6}")
    for note in counts["notes"]:
        print(f"note: {note}")
    print(f"Wrote {common.rel(out)}")
    common.log_event(run, STAGE, "count", "count", room=room, labeled=counts["labeled"], by_voice=bv,
                     by_source=t["by_source"], pains=len(counts["pains"]))
    return 0


# --------------------------------------------------------------------------- saturation
def competition_rank(stats: dict) -> dict:
    """Rank 1 = best by (failed_spend, money, record_count) descending; ties share a rank (1, 2, 2, 4)."""
    items = sorted(stats.items(), key=lambda kv: (-kv[1][0], -kv[1][1], -kv[1][2], kv[0]))
    ranks: dict = {}
    prev = None
    rank = 0
    for i, (key, tup) in enumerate(items, 1):
        if tup != prev:
            rank = i
            prev = tup
        ranks[key] = rank
    return ranks


def _collection_key(rid: str, stored: dict):
    rec = stored.get(rid)
    meta = (rec or {}).get("meta") or {}
    order = meta.get("order")
    if isinstance(order, list) and order and all(isinstance(x, int) and not isinstance(x, bool) for x in order):
        return (0, tuple(order), rid)
    return (1, (), rid)


def order_records(record_ids, stored: dict) -> list:
    return sorted(record_ids, key=lambda rid: _collection_key(rid, stored))


def member_pain_stats(record_ids, labels_by_id: dict) -> dict:
    stats: dict = {}
    for rid in record_ids:
        label = labels_by_id.get(rid)
        if not label or label.get("voice") != "member":
            continue
        for k in label.get("pain_keys") or []:
            fs, money, rc = stats.get(k, (0, 0, 0))
            stats[k] = (fs + (1 if label.get("failed_spend") else 0), money + (1 if label.get("money") else 0), rc + 1)
    return stats


def saturation_entry(ordered_ids, labels_by_id: dict, window: int, round_no: int, new_records: int) -> dict:
    n = len(ordered_ids)
    entry = {"round": round_no, "records": n, "new_records": new_records, "window": window,
             "evaluable": n >= window + 1, "new_pains": [], "rank_changes": [], "saturated": False}
    if not entry["evaluable"]:
        entry["note"] = f"not evaluable: {n} records, need at least {window + 1} (window {window} + 1)"
        return entry
    before = member_pain_stats(ordered_ids[: n - window], labels_by_id)
    after = member_pain_stats(ordered_ids, labels_by_id)
    entry["new_pains"] = sorted(k for k in after if k not in before)
    rb, ra = competition_rank(before), competition_rank(after)
    entry["rank_changes"] = [{"key": k, "rank_before": rb[k], "rank_after": ra[k]}
                             for k in sorted(before) if k in after and rb[k] != ra[k]]
    entry["saturated"] = not entry["new_pains"] and not entry["rank_changes"]
    return entry


def cmd_saturation(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    if bool(args.final) != bool(args.stop_reason):
        raise common.ValidationErrors(["--final and --stop-reason go together: "
                                       "`funnel saturation --room R --final --stop-reason saturated|exhausted|max_rounds`."])
    rules = common.load_kill_rules().get("stage3", {})
    window = int(rules.get("saturation_window", 300))
    manifest = load_manifest(run, room)
    taxonomy = load_taxonomy(run, room)
    labels, _notes = load_labels(run, room, manifest, taxonomy)
    stored = records.records_by_id(run, room)
    ids = manifest_record_ids(manifest)
    ordered = order_records(ids, stored)
    rounds = [records.record_round(stored[rid]) for rid in ids if rid in stored]
    round_no = max(rounds) if rounds else 0
    new_records = sum(1 for r in rounds if r == round_no)
    entry = saturation_entry(ordered, labels, window, round_no, new_records)

    out = common.room_dir(run, room) / "saturation.json"
    data = common.read_json(out) if out.exists() else {}
    if not isinstance(data, dict):
        data = {}
    entries = [e for e in (data.get("rounds") or []) if isinstance(e, dict) and e.get("round") != round_no]
    entries.append(entry)
    entries.sort(key=lambda e: e.get("round", 0))
    data.update({"room": room, "window": window, "rounds": entries})
    data.setdefault("stop_reason", None)
    data.setdefault("final", False)
    if args.final:
        if args.stop_reason == "saturated" and not entry["saturated"]:
            common.write_json(out, data)  # the round's verdict is still recorded; the stop reason is refused
            raise common.ValidationErrors([
                f"{common.rel(out)}: stop reason 'saturated' needs the last round to be saturated, but round "
                f"{round_no} is not (new pains: {', '.join(entry['new_pains']) or 'none'}; rank changes: "
                f"{len(entry['rank_changes'])}). Use exhausted or max_rounds, or run another round."])
        data["stop_reason"] = args.stop_reason
        data["final"] = True
    common.write_json(out, data)

    if not entry["evaluable"]:
        verdict = (f"Round {round_no}: {entry['records']} records ({new_records} new). Not evaluable yet: "
                   f"need at least {window + 1}. Saturated: no.")
    else:
        changes = "; ".join(f"{c['key']} ({c['rank_before']} -> {c['rank_after']})" for c in entry["rank_changes"])
        verdict = (f"Round {round_no}: {entry['records']} records ({new_records} new). "
                   f"Saturated: {'yes' if entry['saturated'] else 'no'}. "
                   f"New pains in the last {window}: {', '.join(entry['new_pains']) or 'none'}. "
                   f"Rank changes: {changes or 'none'}.")
    if args.final:
        verdict += f" Stopped: {args.stop_reason}."
    print(verdict)
    common.log_event(run, STAGE, "saturation", "count", room=room, round=round_no, records=entry["records"],
                     new_records=new_records, saturated=entry["saturated"], new_pains=entry["new_pains"],
                     rank_changes=len(entry["rank_changes"]), stop_reason=data.get("stop_reason"))
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("count", help="Validate a room's labels and write counts.json.")
    p.add_argument("--room", required=True, help="room slug")
    p.set_defaults(func=cmd_count)
    s = subparsers.add_parser("saturation", help="Decide whether a room's last window of records changed the answer.")
    s.add_argument("--room", required=True, help="room slug")
    s.add_argument("--final", action="store_true", help="record why the room stopped (with --stop-reason)")
    s.add_argument("--stop-reason", choices=STOP_REASONS, default=None, help="saturated, exhausted or max_rounds")
    s.set_defaults(func=cmd_saturation)
