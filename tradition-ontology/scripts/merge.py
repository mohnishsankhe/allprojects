#!/usr/bin/env python3
"""Merge all shards into the canonical data/ files.

    python3 scripts/merge.py            # full merge
    python3 scripts/merge.py --quiet

Reads   shards/skeleton/*/<entity>.jsonl          (Phase B and later skeleton additions)
        shards/extraction/*/final/<entity>.jsonl  (Phase D+ text-verified output; teachings upgrade skeleton ones)
        shards/extraction/*/final/skeleton_decisions.jsonl  (upgrade | correct | retire decisions)
        shards/synthesis/*/<entity>.jsonl         (interpretation-layer passes)
        shards/sourcing/*/checks.jsonl            (Phase C hallucination sweep results)
        config/ultimate_node.json
Writes  data/<entity>.json, data/teachings/<source-slug>.jsonl, data/timeline.json,
        data/interpretation_log.jsonl, data/reports/{stats.json,stats.md,conflicts.jsonl,dangling.json}
        RECONCILE_QUEUE.md (regenerated from queued disputes)
Rules: see config/data_model.md. Never deletes an entry; retired / unverified entries are kept and flagged.
"""
import glob, json, os, re, sys, datetime
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORTS = os.path.join(DATA, "reports")
ENTITIES = ["sources", "lineages", "teachers", "teachings", "terms", "concepts", "ultimate", "obstacles",
            "practices", "paths", "phenomenology", "disputes", "borrowings"]
LEVEL_RANK = {"skeleton": 0, "sourced": 1, "text-verified": 2}
CONF_RANK = {"low": 0, "moderate": 1, "high": 2}
# list-of-object fields merged by key (others: union by JSON value)
KEYED_LISTS = {
    "definitions": lambda o: (o.get("lineage"), (o.get("definition") or "")[:80]),
    "names": lambda o: (o.get("lineage"), o.get("name")),
    "cross_language": lambda o: (o.get("language"), o.get("form")),
    "equivalents": lambda o: (o.get("target"), o.get("grade")),
    "relations": lambda o: (o.get("rel"), o.get("target")),
    "sides": lambda o: (o.get("lineage"), (o.get("position") or "")[:60]),
    "works": lambda o: (o.get("source"),),
    "authors": lambda o: (o.get("teacher"), o.get("role")),
    "warnings": lambda o: ((o.get("text") or "")[:80],),
    "sources": lambda o: (o.get("source"), o.get("ref")),
    "checks": lambda o: json.dumps(o, sort_keys=True, ensure_ascii=False),
    "editions": lambda o: (o.get("name"), o.get("kind")),
}
NO_UNION = {"stages"}  # take from primary only (conflicts logged)
UMBRELLAS = {"lin:vedanta", "lin:mahayana", "lin:sakta", "lin:jainism", "lin:sramana", "lin:mantramarga",
             "lin:atimarga", "lin:tantra-movement", "lin:early-buddhism", "lin:vajrayana", "lin:kashmir-saivism",
             "lin:sant",
             "lin:regional-bhakti-poets", "lin:epic-teaching", "lin:sthavira"}  # classificatory groupings, not independent roots
# Transmission lineages whose branches are NOT independent witnesses: lin:chan (with Seon/Zen), lin:pure-land and lin:kagyu
# are real transmissions, so their branches collapse into them (DECISIONS 2026-09-29). A lineage listed here is its own root
# whatever its parent says (a separate transmission filed under a family name).
OWN_ROOTS = {"lin:shangpa-kagyu"}

conflicts, ilog_new = [], []
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST")


def read_jsonl(path):
    out = []
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                o = json.loads(line)
                if isinstance(o, dict):
                    out.append(o)
            except Exception as e:
                conflicts.append({"kind": "bad-json", "file": os.path.relpath(path, ROOT), "line": n, "error": str(e)})
    return out


def vrank(o):
    v = o.get("verification") or {}
    return (LEVEL_RANK.get(v.get("level"), 0), CONF_RANK.get(v.get("confidence"), 0),
            sum(1 for k, x in o.items() if x not in (None, "", [], {})))


def merge_lists(a, b, field):
    if field in KEYED_LISTS and all(isinstance(x, dict) for x in (a or []) + (b or [])):
        keyf = KEYED_LISTS[field]
        out, idx = [], {}
        for x in (a or []) + (b or []):
            try:
                k = keyf(x)
            except Exception:
                k = json.dumps(x, sort_keys=True, ensure_ascii=False)
            if k in idx:
                merged = merge_obj(out[idx[k]], x, field, top=False)
                out[idx[k]] = merged
            else:
                idx[k] = len(out)
                out.append(x)
        return out
    out, seen = [], set()
    for x in (a or []) + (b or []):
        k = json.dumps(x, sort_keys=True, ensure_ascii=False)
        if k not in seen:
            seen.add(k)
            out.append(x)
    return out


def merge_obj(primary, other, ctx="", top=True, eid=None):
    out = dict(primary)
    for k, v in other.items():
        if k in ("provenance",):
            continue
        if k not in out or out[k] in (None, "", [], {}):
            out[k] = v
            continue
        pv = out[k]
        if isinstance(pv, list) and isinstance(v, list):
            if k in NO_UNION:
                if json.dumps(pv, sort_keys=True) != json.dumps(v, sort_keys=True):
                    conflicts.append({"kind": "list-kept-primary", "id": eid, "field": k})
                continue
            out[k] = merge_lists(pv, v, k)
        elif isinstance(pv, dict) and isinstance(v, dict):
            if k == "verification":
                pv2 = dict(pv)
                pv2["checks"] = merge_lists(pv.get("checks") or [], v.get("checks") or [], "checks")
                if LEVEL_RANK.get(v.get("level"), 0) > LEVEL_RANK.get(pv.get("level"), 0):
                    pv2["level"] = v.get("level")
                pv2["unverified"] = bool(pv.get("unverified")) and bool(v.get("unverified", True))
                out[k] = pv2
            else:
                out[k] = merge_obj(pv, v, k, top=False, eid=eid)
        else:
            if pv != v and top and k not in ("summary", "notes", "description", "method_summary", "paraphrase"):
                conflicts.append({"kind": "scalar", "id": eid, "field": k, "kept": pv, "other": v})
            elif pv != v and top and k in ("summary", "notes", "description", "method_summary"):
                # keep the primary text, but preserve the other contribution
                alt = out.get("alt_" + k, [])
                if isinstance(alt, list) and v not in alt and len(alt) < 6:
                    out["alt_" + k] = alt + [v]
    return out


def unit_of(path):
    parts = os.path.relpath(path, os.path.join(ROOT, "shards")).split(os.sep)
    if parts[0] == "extraction" and len(parts) > 3:
        return "extraction:" + "/".join(parts[1:-2])
    return parts[0] + ":" + parts[1]


REMAP_PATH = os.path.join(ROOT, "config", "id_remap.json")
REMAP = {k: v for k, v in (json.load(open(REMAP_PATH, encoding="utf-8")) if os.path.exists(REMAP_PATH) else {}).items() if not k.startswith("_")}


def remap_ids(x, table):
    """Replace every string exactly equal to an old id (anywhere in the object) by the new id."""
    if isinstance(x, str):
        return table.get(x, x)
    if isinstance(x, list):
        return [remap_ids(y, table) for y in x]
    if isinstance(x, dict):
        return {k: remap_ids(v, table) for k, v in x.items()}
    return x


def load_unit_corrections():
    """Sourcing corrections apply to the checked unit's OWN shard entries (before entities from several units are
    merged), so a correction never overwrites what another unit contributed to a shared id."""
    out = defaultdict(dict)  # "skeleton:<UNIT>" -> id -> (corrections, note, checker-unit)
    for path in sorted(glob.glob(os.path.join(ROOT, "shards", "sourcing", "*", "checks.jsonl"))):
        checked_unit = "skeleton:" + os.path.basename(os.path.dirname(path))
        for c in read_jsonl(path):
            if c.get("corrections") and c.get("id"):
                out[checked_unit][c["id"]] = (c["corrections"], c.get("note", "sourcing correction"), unit_of(path))
    return out


UNIT_CORR = None


GITA13 = re.compile(r"^tea:bhagavad-gita:13\.(\d+)(?:-(\d+))?((?:/\d+)?)$")


def _shift13(a, b=None):
    return f"{int(a) + 1}" + (f"-{int(b) + 1}" if b else "")


def gita13_to_edition(x):
    """Skeleton units cite Gītā ch. 13 in the 700-verse (vulgate) numbering; the text layer follows this edition, whose
    extra opening verse 13.1 makes 13.N(vulgate) = 13.N+1 (DECISIONS 2026-09-29). Rewrites every such id (and the
    location of the skeleton's own ch. 13 teachings) to this edition's numbering."""
    if isinstance(x, str):
        m = GITA13.match(x)
        return f"tea:bhagavad-gita:13.{_shift13(m.group(1), m.group(2))}{m.group(3)}" if m else x
    if isinstance(x, list):
        return [gita13_to_edition(v) for v in x]
    if isinstance(x, dict):
        y = {k: gita13_to_edition(v) for k, v in x.items()}
        loc = y.get("location")
        if (isinstance(loc, dict) and y.get("source") == "src:bhagavad-gita" and str(loc.get("chapter")) == "13"
                and isinstance(loc.get("verse"), str) and re.fullmatch(r"\d+(-\d+)?", loc["verse"])):
            a, _, b = loc["verse"].partition("-")
            v = _shift13(a, b or None)
            y["location"] = dict(loc, verse=v, ref=f"13.{v}", numbering_note=f"700-verse numbering 13.{loc['verse']} shifted to this edition")
        return y
    return x


def load_all():
    global UNIT_CORR
    if UNIT_CORR is None:
        UNIT_CORR = load_unit_corrections()
    by_entity = defaultdict(lambda: defaultdict(list))  # entity -> id -> [(obj, unit)]
    logs = []
    patterns = [os.path.join(ROOT, "shards", "skeleton", "*", "*.jsonl"),
                os.path.join(ROOT, "shards", "synthesis", "*", "*.jsonl"),
                os.path.join(ROOT, "shards", "extraction", "**", "final", "*.jsonl")]
    for pat in patterns:
        for path in sorted(glob.glob(pat, recursive=True)):
            ent = os.path.basename(path)[:-6]
            unit = unit_of(path)
            table = REMAP.get(unit, {})
            if ent == "interpretation_log":
                for o in read_jsonl(path):
                    o = gita13_to_edition(o) if unit.startswith("skeleton:") else o
                    o = remap_ids(o, table) if table else o
                    o.setdefault("by", unit)
                    logs.append(o)
                continue
            if ent not in ENTITIES:
                continue
            for o in read_jsonl(path):
                orig_id = o.get("id")
                if unit.startswith("skeleton:"):
                    o = gita13_to_edition(o)
                if table:
                    o2 = remap_ids(o, table)
                    if o2 != o:
                        conflicts.append({"kind": "id-remap", "unit": unit, "id": o.get("id"), "new_id": o2.get("id"), "table": "config/id_remap.json"})
                    o = o2
                if not o.get("id"):
                    conflicts.append({"kind": "no-id", "file": os.path.relpath(path, ROOT)})
                    continue
                corr = UNIT_CORR.get(unit, {}).get(orig_id) or UNIT_CORR.get(unit, {}).get(o["id"])
                if corr:
                    fields, note, by = corr
                    for field, val in fields.items():
                        old = o.get(field)
                        if old != val:
                            o.setdefault("correction_log", []).append({"field": field, "old": old, "new": val,
                                                                       "reason": note, "date": NOW, "by": by})
                            o[field] = val
                            ilog_new.append({"ts": NOW, "kind": "sourcing-correction", "entity": o["id"],
                                             "change": f"{field}: {json.dumps(old, ensure_ascii=False)[:120]} -> {json.dumps(val, ensure_ascii=False)[:120]}",
                                             "reason": note, "by": by})
                by_entity[ent][o["id"]].append((o, unit))
    return by_entity, logs


def merge_entity(items):
    """items: list of (obj, unit). Returns merged obj."""
    # extraction (text-verified) teachings replace skeleton ones outright for text fields
    items = sorted(items, key=lambda t: vrank(t[0]), reverse=True)
    primary, punit = items[0]
    out = dict(primary)
    units = [punit]
    for o, u in items[1:]:
        out = merge_obj(out, o, top=True, eid=primary.get("id"))
        if u not in units:
            units.append(u)
    phases = sorted({u.split(":")[0] for u in units})
    out["provenance"] = {"units": units, "phases": phases}
    return out


def apply_decisions(merged_teachings):
    for path in sorted(glob.glob(os.path.join(ROOT, "shards", "extraction", "**", "final", "skeleton_decisions.jsonl"), recursive=True)):
        for d in read_jsonl(path):
            tid, act = d.get("skeleton_id_edition") or gita13_to_edition(d.get("skeleton_id")), d.get("decision")
            t = merged_teachings.get(tid)
            if not t:
                continue
            if act == "retire":
                t["retired"] = {"reason": d.get("reason"), "replaced_by": d.get("replaced_by"), "date": NOW}
                ilog_new.append({"ts": NOW, "kind": "retire", "entity": tid, "change": "skeleton teaching retired",
                                 "reason": d.get("reason"), "by": unit_of(path)})
            elif act in ("upgrade", "correct") and d.get("replaced_by") and d["replaced_by"] != tid:
                t["superseded_by"] = d["replaced_by"]
                ilog_new.append({"ts": NOW, "kind": "upgrade" if act == "upgrade" else "text-correction",
                                 "entity": tid, "change": f"superseded by {d['replaced_by']}",
                                 "reason": d.get("reason"), "by": unit_of(path)})


def apply_checks(data):
    index = {}
    for ent in ENTITIES:
        for oid, o in data[ent].items():
            index[oid] = o
    n = Counter()
    for path in sorted(glob.glob(os.path.join(ROOT, "shards", "sourcing", "*", "checks.jsonl"))):
        unit = unit_of(path)
        for c in read_jsonl(path):
            o = index.get(gita13_to_edition(c.get("id")))
            if o is None:
                n["unknown-id"] += 1
                continue
            v = o.setdefault("verification", {"level": "skeleton", "confidence": "low", "unverified": False, "checks": []})
            chk = {"phase": c.get("phase", "C"), "date": c.get("date", NOW[:10]), "method": c.get("method"),
                   "queries": c.get("queries", []), "evidence": c.get("evidence", []), "result": c.get("result"),
                   "note": c.get("note", ""), "by": unit}
            v["checks"] = merge_lists(v.get("checks") or [], [chk], "checks")
            res = c.get("result")
            if res in ("confirmed", "partially-confirmed", "corrected"):
                if v.get("level") == "skeleton":
                    v["level"] = "sourced"
                v["unverified"] = False
                n[res] += 1
            elif res == "not-found":
                if v.get("level") == "skeleton":
                    v["unverified"] = True
                n[res] += 1
            # field corrections were already applied to the checked unit's own entries in load_all()
    return n


def lineage_root(lid, lineages, cache={}):
    if lid in cache:
        return cache[lid]
    seen, cur = set(), lid
    while cur not in OWN_ROOTS:
        seen.add(cur)
        par = (lineages.get(cur) or {}).get("parent")
        if not par or par in seen or par in UMBRELLAS or par not in lineages:
            break
        cur = par
    cache[lid] = cur
    return cur


def convergence(data):
    lineages = data["lineages"]
    for ent in ("practices", "obstacles", "paths"):
        for o in data[ent].values():
            lins = set(o.get("lineages") or [])
            if o.get("lineage"):
                lins.add(o["lineage"])
            for s in o.get("names") or []:
                if isinstance(s, dict) and s.get("lineage"):
                    lins.add(s["lineage"])
            lins = {l for l in lins if isinstance(l, str) and l.startswith("lin:")}
            roots = {lineage_root(l, lineages) for l in lins}
            fams = {(lineages.get(l) or {}).get("family") for l in lins} - {None}
            o["convergence"] = {"count": len(roots), "lineages": sorted(lins), "schools": sorted(roots),
                                "families": sorted(fams), "computed": NOW}


def timeline(data):
    tl = []
    for ent, pfx in (("sources", "src"), ("teachers", "tch"), ("lineages", "lin")):
        for o in data[ent].values():
            d = o.get("dating") or {}
            for acc in ("scholarly", "tradition"):
                a = d.get(acc)
                if isinstance(a, dict) and (a.get("from") is not None or a.get("to") is not None):
                    tl.append({"entity": o["id"], "label": o.get("title") or o.get("name"), "account": acc,
                               "from": a.get("from"), "to": a.get("to"), "text": a.get("text"),
                               "confidence": d.get("confidence") or (o.get("verification") or {}).get("confidence"),
                               "level": (o.get("verification") or {}).get("level")})
    tl.sort(key=lambda x: (x["from"] if isinstance(x["from"], int) else (x["to"] if isinstance(x["to"], int) else 99999)))
    return tl


def dangling(data):
    ids = set()
    for ent in ENTITIES:
        ids |= set(data[ent].keys())
    refs = Counter()
    where = defaultdict(set)

    def walk(x, owner):
        if isinstance(x, dict):
            for v in x.values():
                walk(v, owner)
        elif isinstance(x, list):
            for v in x:
                walk(v, owner)
        elif isinstance(x, str) and re.match(r"^(src|lin|tch|tea|trm|cpt|prc|obs|pth|phn|dsp|brw|ult):[a-z0-9]", x):
            if x not in ids:
                refs[x] += 1
                if len(where[x]) < 3:
                    where[x].add(owner)
    for ent in ENTITIES:
        for oid, o in data[ent].items():
            walk({k: v for k, v in o.items() if k not in ("id", "provenance")}, oid)
    by_pfx = Counter(r.split(":")[0] for r in refs)
    top = [{"id": r, "refs": c, "e.g.": sorted(where[r])} for r, c in refs.most_common(400)]
    return {"total_distinct": len(refs), "by_prefix": dict(by_pfx), "top": top}


def stats(data):
    s = {}
    for ent in ENTITIES:
        c = Counter()
        for o in data[ent].values():
            v = o.get("verification") or {}
            lvl = v.get("level", "skeleton")
            c[lvl] += 1
            if v.get("unverified"):
                c["unverified"] += 1
            if o.get("retired"):
                c["retired"] += 1
            if o.get("recent"):
                c["recent"] += 1
        c["total"] = len(data[ent])
        s[ent] = dict(c)
    return s


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=1)
        fh.write("\n")


def regen_queue(data):
    q = [o for o in data["disputes"].values() if (o.get("reconciliation") or {}).get("status") == "queued"]
    q.sort(key=lambda o: o["id"])
    lines = ["# Reconciliation queue", "",
             "Generated by `scripts/merge.py` from disputes whose reconciliation status is `queued`, plus items added by the",
             "reconciliation passes. Status is always **not yet reconciled** — never \"contradiction\". Each item lists the",
             "sides and candidate readings. Verification level of the underlying entries is shown.", "",
             f"_Last generated: {NOW}. Items: {len(q)}._", ""]
    for i, o in enumerate(q, 1):
        rq = o.get("queue_ref") or f"RQ-{i:03d}"
        o["queue_ref"] = rq
        v = (o.get("verification") or {}).get("level", "skeleton")
        lines.append(f"## {rq} — {o.get('question')}  ")
        lines.append(f"`{o['id']}` · {v}{' · [unverified]' if (o.get('verification') or {}).get('unverified') else ''}")
        lines.append("")
        for sd in o.get("sides") or []:
            lines.append(f"- **{sd.get('lineage')}**: {sd.get('position')}")
        rec = o.get("reconciliation") or {}
        cands = rec.get("candidate_readings") or o.get("candidate_readings") or []
        if cands:
            lines.append("- Candidate readings:")
            for c in cands:
                lines.append(f"  - {c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)}")
        if rec.get("explanation"):
            lines.append(f"- Note: {rec['explanation']}")
        lines.append("")
    with open(os.path.join(ROOT, "RECONCILE_QUEUE.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return len(q)


def main():
    quiet = "--quiet" in sys.argv
    by_entity, logs = load_all()
    data = {}
    for ent in ENTITIES:
        data[ent] = {}
        for oid, items in by_entity[ent].items():
            data[ent][oid] = merge_entity(items)
    apply_decisions(data["teachings"])
    chk = apply_checks(data)
    convergence(data)
    # write entity files
    for ent in ENTITIES:
        if ent in ("teachings", "ultimate"):
            continue
        write_json(os.path.join(DATA, f"{ent}.json"), [data[ent][k] for k in sorted(data[ent])])
    # ultimate
    node = {}
    np = os.path.join(ROOT, "config", "ultimate_node.json")
    if os.path.exists(np):
        node = json.load(open(np, encoding="utf-8"))
    write_json(os.path.join(DATA, "ultimate.json"), {"node": node, "views": [data["ultimate"][k] for k in sorted(data["ultimate"])]})
    # teachings split by source
    tdir = os.path.join(DATA, "teachings")
    os.makedirs(tdir, exist_ok=True)
    for f in glob.glob(os.path.join(tdir, "*.jsonl")):
        os.remove(f)
    by_src = defaultdict(list)
    for k in sorted(data["teachings"]):
        t = data["teachings"][k]
        slug = (t.get("source") or "src:unknown").split(":", 1)[-1] or "unknown"
        by_src[slug].append(t)
    for slug, ts in by_src.items():
        with open(os.path.join(tdir, f"{slug}.jsonl"), "w", encoding="utf-8") as fh:
            for t in ts:
                fh.write(json.dumps(t, ensure_ascii=False) + "\n")
    write_json(os.path.join(DATA, "timeline.json"), timeline(data))
    # interpretation log: shard logs + merge-generated lines (deduplicated)
    seen, all_logs = set(), []
    for o in logs + ilog_new:
        k = json.dumps({x: o.get(x) for x in ("kind", "entity", "change", "reason")}, sort_keys=True, ensure_ascii=False)
        if k not in seen:
            seen.add(k)
            all_logs.append(o)
    with open(os.path.join(DATA, "interpretation_log.jsonl"), "w", encoding="utf-8") as fh:
        for o in all_logs:
            fh.write(json.dumps(o, ensure_ascii=False) + "\n")
    nq = regen_queue(data)
    st = stats(data)
    dg = dangling(data)
    os.makedirs(REPORTS, exist_ok=True)
    write_json(os.path.join(REPORTS, "stats.json"), {"generated": NOW, "entities": st, "sourcing_checks": dict(chk),
                                                     "queue": nq, "interpretation_log": len(all_logs),
                                                     "conflicts": len(conflicts), "dangling_refs": dg["total_distinct"]})
    write_json(os.path.join(REPORTS, "dangling.json"), dg)
    with open(os.path.join(REPORTS, "conflicts.jsonl"), "w", encoding="utf-8") as fh:
        for c in conflicts:
            fh.write(json.dumps(c, ensure_ascii=False, default=str) + "\n")
    # size guard
    big = []
    for f in glob.glob(os.path.join(DATA, "**", "*.json*"), recursive=True):
        if os.path.getsize(f) > 45 * 1024 * 1024:
            big.append(os.path.relpath(f, ROOT))
    md = ["| entity | total | skeleton | sourced | text-verified | [unverified] | recent |", "|---|---|---|---|---|---|---|"]
    for ent in ENTITIES:
        c = st[ent]
        md.append(f"| {ent} | {c.get('total',0)} | {c.get('skeleton',0)} | {c.get('sourced',0)} | {c.get('text-verified',0)} | {c.get('unverified',0)} | {c.get('recent',0)} |")
    with open(os.path.join(REPORTS, "stats.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Counts ({NOW})\n\n" + "\n".join(md) + f"\n\nReconciliation queue: {nq} · interpretation-log lines: {len(all_logs)} · merge conflicts logged: {len(conflicts)} · dangling references: {dg['total_distinct']}\n")
    if not quiet:
        print("\n".join(md))
        print(f"queue={nq} ilog={len(all_logs)} conflicts={len(conflicts)} dangling={dg['total_distinct']} checks={dict(chk)}")
    if big:
        print("WARNING files over 45MB:", big)


if __name__ == "__main__":
    main()
