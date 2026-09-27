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


def load_labels(run, room: str, manifest: dict, taxonomy: dict, only_batch=None) -> tuple:
    """Every label of the room, validated. Returns (labels_by_id, notes).

    `only_batch`: validate just labels/<batch>.jsonl against that batch's records (a per-batch labeler's check)."""
    ldir = common.room_dir(run, room) / "labels"
    if only_batch is not None:
        batches = manifest.get("batches") or {}
        if only_batch not in batches:
            raise common.ValidationErrors([f"{only_batch!r} is not a batch of room {room}. "
                                           f"Batches: {', '.join(sorted(batches)) or 'none'}."])
        p = ldir / f"{only_batch}.jsonl"
        if not p.exists():
            raise common.MissingInput(f"No label file {common.rel(p)}. Write one line per record of {only_batch}.md.")
        files = [p]
        manifest_ids = list(batches[only_batch])
    else:
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
    kind_min = int(common.load_kill_rules().get("stage3", {}).get("source_kind_min_records", 5))

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
    by_kind: dict = {}
    member_with_pain = money_total = failed_total = 0
    for rid in ids:
        label = labels[rid]
        voice = label["voice"]
        by_voice[voice] += 1
        src = (stored.get(rid) or {}).get("source", "unknown")
        by_source[src] = by_source.get(src, 0) + 1
        kind = records.source_kind((stored.get(rid) or {}).get("url", ""))
        by_kind[kind] = by_kind.get(kind, 0) + 1
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
            "by_kind": dict(sorted(by_kind.items())),
            "source_kinds": sorted(k for k, n in by_kind.items() if n >= kind_min),
            "source_kind_min_records": kind_min,
            "member_records": by_voice["member"],
            "member_records_with_pain": member_with_pain,
            "money_mentions": money_total,
            "failed_spend_mentions": failed_total,
        },
        "notes": sorted(notes),
    }


def label_todo(run, room: str, all_batches: bool = False) -> list:
    """Batches that need labels: no labels file, a file that misses records of its batch or cannot be read, or a
    pain key that is not in the taxonomy. With all_batches, every batch (after a taxonomy change)."""
    manifest = load_manifest(run, room)
    batches = manifest.get("batches") or {}
    if all_batches:
        return sorted(batches)
    tax_path = common.room_dir(run, room) / "taxonomy.json"
    keys = None
    if tax_path.exists():
        try:
            keys = set(load_taxonomy(run, room))
        except (common.FunnelError, ValueError):
            keys = None
    if keys is None:
        return sorted(batches)
    ldir = common.room_dir(run, room) / "labels"
    todo = []
    for name in sorted(batches):
        p = ldir / f"{name}.jsonl"
        if not p.exists():
            todo.append(name)
            continue
        try:
            rows = [r for r in common.read_jsonl(p) if isinstance(r, dict)]
        except (common.FunnelError, ValueError):
            todo.append(name)
            continue
        ids = {r.get("record_id") for r in rows}
        stale = any(k not in keys for r in rows for k in (r.get("pain_keys") or []) if isinstance(k, str))
        if not set(batches[name]) <= ids or stale:
            todo.append(name)
    return todo


def cmd_label_todo(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    total = len(load_manifest(run, room).get("batches") or {})
    todo = label_todo(run, room, all_batches=args.all)
    why = "every batch (--all)" if args.all else "no labels, missing records, or unknown pain keys"
    print(f"Room {room}: {total} batches; {len(todo)} need labels ({why}).")
    print("TODO: " + (" ".join(todo) if todo else "none"))
    return 0


# --------------------------------------------------------------------------- member re-check after new pains
# When label-prep adds pains in round N, the member records of earlier rounds are re-checked for the new pains
# (pain counts, ranks and saturation use member records only), instead of relabeling every batch.
def packs_dir(run, room: str):
    return common.raw_dir(run, room) / "_packs"


def patches_dir(run, room: str):
    return common.room_dir(run, room) / "labels" / "_patches"


def _label_rows(run, room: str, batch_names) -> dict:
    """record_id -> label row from the given batches' label files (lenient: unreadable files are skipped)."""
    out: dict = {}
    ldir = common.room_dir(run, room) / "labels"
    for b in batch_names:
        p = ldir / f"{b}.jsonl"
        if not p.exists():
            continue
        try:
            rows = common.read_jsonl(p)
        except (common.FunnelError, ValueError):
            continue
        for row in rows:
            if isinstance(row, dict) and isinstance(row.get("record_id"), str):
                out[row["record_id"]] = row
    return out


def make_packs(run, room: str, round_no: int, keys, size: int = 80) -> list:
    """Write RUN/03_listen/raw/<room>/_packs/pack_r<N>_NNN.md: the member records of rounds before N, with their
    current pain keys, for a re-check against the pains added in round N. Returns the pack names."""
    manifest = load_manifest(run, room)
    taxonomy = load_taxonomy(run, room)
    keys = [k for k in dict.fromkeys(keys)]
    bad = [k for k in keys if k not in taxonomy]
    if not keys or bad:
        raise common.ValidationErrors([f"--keys must list pains that are in taxonomy.json (unknown: {', '.join(bad) or 'none given'})."])
    old = [b for r, info in sorted((manifest.get("rounds") or {}).items(), key=lambda x: int(x[0]))
           if int(r) < round_no for b in info.get("batches") or []]
    rows = _label_rows(run, room, old)
    members = [rid for b in old for rid in manifest["batches"][b] if (rows.get(rid) or {}).get("voice") == "member"]
    stored = records.records_by_id(run, room)
    pdir = packs_dir(run, room)
    pdir.mkdir(parents=True, exist_ok=True)
    for stale in pdir.glob(f"pack_r{round_no}_*.md"):
        stale.unlink()
    packs: dict = {}
    for i in range(0, len(members), size):
        chunk = members[i:i + size]
        name = f"pack_r{round_no}_{i // size + 1:03d}"
        lines = [f"# {name} | room {room} | re-check for the pains added in round {round_no}: {', '.join(keys)} | "
                 f"{len(chunk)} member records", ""]
        for rid in chunk:
            rec = stored.get(rid) or {}
            cur = rows[rid].get("pain_keys") or []
            lines.append(f"### {rid} | {rec.get('source', '-')} | {rec.get('date') or 'undated'} | "
                         f"{common.domain_of(rec.get('url') or '') or '-'}")
            lines.append(records._cut(rec.get("text") or "", int(manifest.get("chars") or 1500)))
            lines.append(f"current pain_keys: {', '.join(cur) if cur else 'none'}")
            lines.append("")
        common.write_text(pdir / f"{name}.md", "\n".join(lines))
        packs[name] = chunk
    common.write_json(pdir / f"pack_r{round_no}.json", {"room": room, "round": round_no, "keys": keys, "packs": packs,
                                                        "current": {rid: list(rows[rid].get("pain_keys") or []) for rid in members}})
    return sorted(packs)


def _pack_index(run, room: str) -> dict:
    """pack name -> (round, new keys, record ids, current keys by id) from every pack_r<N>.json."""
    out: dict = {}
    for m in sorted(packs_dir(run, room).glob("pack_r*.json")):
        data = common.read_json(m)
        for name, ids in (data.get("packs") or {}).items():
            out[name] = (int(data["round"]), list(data["keys"]), list(ids), dict(data.get("current") or {}))
    return out


def check_patch(run, room: str, pack: str, taxonomy: dict) -> tuple:
    """Validate labels/_patches/<pack>.jsonl. Returns (rows by record_id, errors)."""
    idx = _pack_index(run, room)
    if pack not in idx:
        return {}, [f"{pack!r} is not a pack of room {room}. Packs: {', '.join(sorted(idx)) or 'none'}."]
    _rnd, new_keys, ids, current = idx[pack]
    p = patches_dir(run, room) / f"{pack}.jsonl"
    if not p.exists():
        return {}, [f"No patch file {common.rel(p)}. Write one line per record of {pack}.md."]
    errors: list = []
    out: dict = {}
    for n, row in enumerate(common.read_jsonl(p), 1):
        where = f"{common.rel(p)}: line {n}"
        rid = row.get("record_id") if isinstance(row, dict) else None
        if rid not in ids:
            errors.append(f"{where}: record_id {rid!r} is not in {pack}.md.")
            continue
        if rid in out:
            errors.append(f"{where} ({rid}): appears twice. Keep one line per record.")
            continue
        keys = row.get("pain_keys")
        cur = current.get(rid) or []
        if not isinstance(keys, list) or not all(isinstance(k, str) for k in keys) or len(set(keys)) > 2:
            errors.append(f"{where} ({rid}): 'pain_keys' must be a list of 0 to 2 keys.")
            continue
        keys = list(dict.fromkeys(keys))
        extra = [k for k in keys if k not in cur and k not in new_keys]
        if extra:
            errors.append(f"{where} ({rid}): {', '.join(extra)} is neither a current key of this record nor a new pain "
                          f"({', '.join(new_keys)}). The re-check only adds the new pains.")
        unknown = [k for k in keys if k not in taxonomy]
        if unknown:
            errors.append(f"{where} ({rid}): unknown pain key(s) {', '.join(unknown)}.")
        dropped = [k for k in cur if k not in keys]
        if dropped and not any(k in new_keys for k in keys):
            errors.append(f"{where} ({rid}): drops {', '.join(dropped)} without adding a new pain. Keep the current keys "
                          f"unless a new pain replaces one (at most 2 keys).")
        errors.extend(f"{where} ({rid}): {e}" for e in common.check_judgment(row, "patch"))
        out[rid] = dict(row, pain_keys=keys)
    missing = [rid for rid in ids if rid not in out and not any(rid in e for e in errors)]
    if missing:
        errors.append(f"{common.rel(p)}: {len(missing)} record(s) of {pack}.md have no line: {', '.join(missing[:10])}"
                      + (f" and {len(missing) - 10} more" if len(missing) > 10 else "") + ".")
    return out, errors


def apply_patches(run, room: str) -> dict:
    """Apply every pending patch to the batch label files (pain_keys only), then move it to _patches/applied/."""
    taxonomy = load_taxonomy(run, room)
    manifest = load_manifest(run, room)
    id_to_batch = {rid: name for name, ids in (manifest.get("batches") or {}).items() for rid in ids}
    pdir = patches_dir(run, room)
    pending = sorted(pdir.glob("pack_r*_*.jsonl")) if pdir.exists() else []
    idx = _pack_index(run, room)
    errors: list = []
    checked: dict = {}
    for p in pending:
        rows, errs = check_patch(run, room, p.stem, taxonomy)
        errors.extend(errs)
        checked[p.stem] = rows
    if errors:
        raise common.ValidationErrors(errors)
    ldir = common.room_dir(run, room) / "labels"
    changed = 0
    by_batch: dict = {}
    for pack, rows in checked.items():
        rnd = idx[pack][0]
        for rid, row in rows.items():
            by_batch.setdefault(id_to_batch[rid], {})[rid] = (rnd, row)
    for batch, updates in sorted(by_batch.items()):
        path = ldir / f"{batch}.jsonl"
        out = []
        for label in common.read_jsonl(path):
            upd = updates.get(label.get("record_id")) if isinstance(label, dict) else None
            if upd and list(upd[1]["pain_keys"]) != list(label.get("pain_keys") or []):
                rnd, row = upd
                label = dict(label, pain_keys=row["pain_keys"], confidence=row["confidence"],
                             reasoning=f"{label.get('reasoning', '').rstrip()} Re-check round {rnd}: {row['reasoning']}".strip())
                changed += 1
            out.append(label)
        common.write_jsonl(path, out)
    done = pdir / "applied"
    for p in pending:
        done.mkdir(parents=True, exist_ok=True)
        p.replace(done / p.name)
    return {"patches": [p.stem for p in pending], "changed": changed}


def packs_already_checked(run, room: str, names) -> list:
    """Packs whose re-check is done: a pending patch that passes the check, or an applied patch with the same records."""
    taxonomy = load_taxonomy(run, room)
    idx = _pack_index(run, room)
    done = []
    for name in names:
        applied = patches_dir(run, room) / "applied" / f"{name}.jsonl"
        if applied.exists():
            try:
                ids = {r.get("record_id") for r in common.read_jsonl(applied) if isinstance(r, dict)}
            except (common.FunnelError, ValueError):
                ids = set()
            if name in idx and ids == set(idx[name][2]):
                done.append(name)
                continue
        if (patches_dir(run, room) / f"{name}.jsonl").exists():
            _rows, errors = check_patch(run, room, name, taxonomy)
            if not errors:
                done.append(name)
    return done


def cmd_relabel_pack(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    keys = [k.strip() for k in (args.keys or "").split(",") if k.strip()]
    names = make_packs(run, room, int(args.round), keys, size=args.size)
    done = packs_already_checked(run, room, names)
    todo = [n for n in names if n not in done]
    print(f"Room {room}: {len(names)} pack(s) of member records from rounds before {args.round}, to re-check for: "
          f"{', '.join(keys)}. {len(done)} already checked (a valid patch exists).")
    print("PACKS: " + (" ".join(todo) if todo else "none"))
    if done:
        print("ALREADY CHECKED: " + " ".join(done))
    common.log_event(run, STAGE, "relabel-pack", "ran", room=room, round=int(args.round), keys=keys, packs=len(names),
                     already_checked=len(done))
    return 0


def cmd_apply_patches(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    if args.check:
        rows, errors = check_patch(run, room, args.check, load_taxonomy(run, room))
        if errors:
            raise common.ValidationErrors(errors)
        print(f"{args.check}: {len(rows)} lines, no errors (not applied yet; label-finish applies it).")
        return 0
    r = apply_patches(run, room)
    print(f"Room {room}: applied {len(r['patches'])} patch(es) ({', '.join(r['patches']) or 'none'}); "
          f"{r['changed']} label(s) changed.")
    common.log_event(run, STAGE, "apply-patches", "ran", room=room, patches=r["patches"], changed=r["changed"])
    return 0


def cmd_count(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    if args.batch:
        manifest = load_manifest(run, room)
        labels, notes = load_labels(run, room, manifest, load_taxonomy(run, room), only_batch=args.batch)
        by_voice = {v: sum(1 for x in labels.values() if x.get("voice") == v) for v in VOICES}
        print(f"{args.batch}: {len(manifest['batches'][args.batch])} records, {len(labels)} labels, no errors "
              f"(member {by_voice['member']}, seller {by_voice['seller']}, media {by_voice['media']}, "
              f"other {by_voice['other']}). counts.json was not written (batch check only).")
        for note in notes:
            print(f"note: {note}")
        return 0
    counts = compute_counts(run, room)
    out = common.room_dir(run, room) / "counts.json"
    common.write_json(out, counts)
    t = counts["totals"]
    bv = t["by_voice"]
    print(f"Room {room}: {counts['labeled']} labeled records "
          f"(member {bv['member']}, seller {bv['seller']}, media {bv['media']}, other {bv['other']}).")
    print("Sources: " + ", ".join(f"{k} {v}" for k, v in t["by_source"].items()))
    need = int(common.load_kill_rules().get("stage3", {}).get("min_source_kinds", 3))
    print("Source kinds (kind of site each record points to): " + ", ".join(f"{k} {v}" for k, v in t["by_kind"].items())
          + f". Kinds with at least {t['source_kind_min_records']} records: {len(t['source_kinds'])} (the rule asks for {need}).")
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
                     by_source=t["by_source"], by_kind=t["by_kind"], source_kinds=len(t["source_kinds"]),
                     pains=len(counts["pains"]))
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


def saturation_entry(ordered_ids, labels_by_id: dict, window: int, round_no: int, new_records: int,
                     from_round: int = 1, whole_round: bool = False, min_member_records: int = 0,
                     taxonomy_added=()) -> dict:
    """One round's saturation verdict over records in collection order.

    `from_round`: earlier rounds are not evaluable (round 1 builds the pain list, so its own tail cannot test it).
    `whole_round`: when the latest round brought more than `window` records, the window is that whole round, because
    the order inside a round is only query order. `min_member_records`: a window with fewer member records cannot
    show a new pain, so it is not evaluable. `taxonomy_added`: pains the taxonomy gained this round; they count as
    new pains even when relabeling found them in earlier records too (the new records are what revealed them).
    """
    n = len(ordered_ids)
    w = max(window, new_records) if whole_round else window
    entry = {"round": round_no, "records": n, "new_records": new_records, "window": window, "window_used": w,
             "evaluable": False, "new_pains": [], "rank_changes": [], "saturated": False}
    if taxonomy_added:
        entry["taxonomy_added"] = sorted(taxonomy_added)
    if round_no < from_round:
        entry["note"] = (f"not evaluable: round {round_no} builds the pain list; saturation is tested on the records "
                         f"of round {from_round} and later")
        return entry
    if n < w + 1:
        entry["note"] = f"not evaluable: {n} records, need at least {w + 1} (window {w} + 1)"
        return entry
    members = sum(1 for rid in ordered_ids[n - w:] if (labels_by_id.get(rid) or {}).get("voice") == "member")
    entry["window_member_records"] = members
    if members < min_member_records:
        entry["note"] = (f"not evaluable: the last {w} records hold {members} member records, fewer than "
                         f"{min_member_records}, too few to show a new pain")
        return entry
    entry["evaluable"] = True
    window = w
    before = member_pain_stats(ordered_ids[: n - window], labels_by_id)
    after = member_pain_stats(ordered_ids, labels_by_id)
    entry["new_pains"] = sorted({k for k in after if k not in before} | set(taxonomy_added))
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

    out = common.room_dir(run, room) / "saturation.json"
    data = common.read_json(out) if out.exists() else {}
    if not isinstance(data, dict):
        data = {}
    # Pains the taxonomy gained this round: marked added_round = this round, or missing from the last earlier
    # round's key list (so a forgotten added_round cannot hide a new pain).
    added = set()
    if round_no > 1:
        added = {k for k, e in taxonomy.items() if isinstance(e, dict) and e.get("added_round") == round_no}
        earlier = sorted((e for e in (data.get("rounds") or []) if isinstance(e, dict)
                          and isinstance(e.get("round"), int) and e["round"] < round_no), key=lambda e: e["round"])
        if earlier and isinstance(earlier[-1].get("taxonomy_keys"), list):
            added |= set(taxonomy) - set(earlier[-1]["taxonomy_keys"])
    entry = saturation_entry(ordered, labels, window, round_no, new_records,
                             from_round=int(rules.get("saturation_from_round", 1)),
                             whole_round=bool(rules.get("saturation_window_whole_round", False)),
                             min_member_records=int(rules.get("saturation_min_member_records", 0)),
                             taxonomy_added=sorted(added))
    entry["taxonomy_keys"] = sorted(taxonomy)
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

    w = entry["window_used"]
    if not entry["evaluable"]:
        if round_no < int(rules.get("saturation_from_round", 1)):
            why = f"round {round_no} builds the pain list; saturation is tested from round {rules.get('saturation_from_round')}"
        elif entry["records"] < w + 1:
            why = f"need at least {w + 1}"
        else:
            why = (f"the last {w} records hold only {entry.get('window_member_records', 0)} member records "
                   f"(need {rules.get('saturation_min_member_records')})")
        verdict = (f"Round {round_no}: {entry['records']} records ({new_records} new). Not evaluable yet: "
                   f"{why}. Saturated: no.")
    else:
        changes = "; ".join(f"{c['key']} ({c['rank_before']} -> {c['rank_after']})" for c in entry["rank_changes"])
        verdict = (f"Round {round_no}: {entry['records']} records ({new_records} new). "
                   f"Saturated: {'yes' if entry['saturated'] else 'no'}. "
                   f"New pains in the last {w}: {', '.join(entry['new_pains']) or 'none'}. "
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
    p.add_argument("--batch", default=None, help="check only labels/<batch>.jsonl against that batch (writes nothing)")
    p.set_defaults(func=cmd_count, stage_no=STAGE)
    k = subparsers.add_parser("relabel-pack", help="Pack earlier rounds' member records for a re-check against new pains.")
    k.add_argument("--room", required=True, help="room slug")
    k.add_argument("--round", required=True, type=int, help="the round in which the pains were added")
    k.add_argument("--keys", required=True, help="the added pain keys, comma-separated")
    k.add_argument("--size", type=int, default=80, help="records per pack (default 80)")
    k.set_defaults(func=cmd_relabel_pack, stage_no=STAGE)
    a = subparsers.add_parser("apply-patches", help="Validate and apply the re-check patches to the label files.")
    a.add_argument("--room", required=True, help="room slug")
    a.add_argument("--check", default=None, help="only validate labels/_patches/<pack>.jsonl (applies nothing)")
    a.set_defaults(func=cmd_apply_patches, stage_no=STAGE)
    t = subparsers.add_parser("label-todo", help="List the batches of a room that still need labels.")
    t.add_argument("--room", required=True, help="room slug")
    t.add_argument("--all", action="store_true", help="every batch (after the taxonomy changed)")
    t.set_defaults(func=cmd_label_todo, stage_no=STAGE)
    s = subparsers.add_parser("saturation", help="Decide whether a room's last window of records changed the answer.")
    s.add_argument("--room", required=True, help="room slug")
    s.add_argument("--final", action="store_true", help="record why the room stopped (with --stop-reason)")
    s.add_argument("--stop-reason", choices=STOP_REASONS, default=None, help="saturated, exhausted or max_rounds")
    s.set_defaults(func=cmd_saturation, stage_no=STAGE)
