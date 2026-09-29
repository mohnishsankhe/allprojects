#!/usr/bin/env python3
"""Build and validate the three reconciliation tables (mechanical parts by code):
    python3 layers/_gen/tables/build.py
Writes layers/tables/{obstacle_correspondence,one_truth,path_map_correspondence}.json and
layers/_gen/tables/build_report.json. Exits non-zero if any validation fails.

Computed by code, never typed: member lens/name, row grade (weakest diagnosis.json grade on the edges joining the
members), connectivity of members under diagnosis.json equivalences, citation existence and citability,
user_facing (true only if every cite is sourced/text-verified, not unverified, not restricted), blocked_by,
principle names, by-band index, vocabulary checks.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from insight import ontology as o  # noqa: E402
import spec_obstacles  # noqa: E402
import spec_one_truth  # noqa: E402
import spec_paths  # noqa: E402

PRINCIPLES = {  # config/principles.md, exact ids and names
    "P1-level": "Level of truth",
    "P2-standpoint": "Standpoint",
    "P3-path": "Path by temperament",
    "P4-stage": "Stage of the student",
    "P5-neyartha": "Provisional vs definitive",
    "P6-upaya": "Skillful means",
    "P7-arthavada": "Praise passages",
    "P8-six-marks": "The six marks of purport",
}
GRADES = ("exact", "same-under-standpoint", "partial")  # strongest -> weakest for a row
LENSES = ("vedic-yogic", "ascetic-buddhist", "ascetic-jain")
# words that must not appear in table prose (no modern psychology, no medical framing, never 'contradiction')
BANNED = ["contradict", "psycholog", "depress", "anxiety", "trauma", "neuro", "therap", "diagnos", "disorder",
          "clinical", "mental health", "cure", "patient", "symptom", "brain", "dopamine", "personality type"]

ERR, WARN = [], []
DIAG = {e["id"]: e for e in json.loads((ROOT / "layers/diagnosis.json").read_text(encoding="utf-8"))}
LINEAGES = {x["id"] for x in json.loads((ROOT / "data/lineages.json").read_text(encoding="utf-8"))}
PATHS = {p["id"]: p for p in json.loads((ROOT / "data/paths.json").read_text(encoding="utf-8"))}
TEACH = o.teachings()


def cite_check(cites, where):
    """Every cite must exist as an exact teaching id in data/. Returns (citable_all, blocked_by)."""
    if not cites:
        ERR.append(f"{where}: no cites")
    blocked = []
    for c in cites:
        if not isinstance(c, str) or not c.startswith("tea:"):
            ERR.append(f"{where}: malformed cite {c!r}")
            continue
        if c not in TEACH:
            ERR.append(f"{where}: cite {c} does not exist in data/teachings")
            blocked.append({"cite": c, "why": "missing"})
            continue
        if not o.citable(c):
            t = o.teaching(c)
            why = "restricted" if t and t["restricted"] else ("unverified" if t and t["unverified"] else (t["level"] if t else "missing"))
            blocked.append({"cite": c, "why": why})
    return (not blocked), blocked


def principle(p, where):
    pid = p.get("id")
    if pid not in PRINCIPLES:
        ERR.append(f"{where}: bad principle id {pid}")
        return p
    if not p.get("reason"):
        ERR.append(f"{where}: principle without reason")
    return {"id": pid, "name": PRINCIPLES[pid], "reason": p["reason"]}


def uniq(xs):
    return list(dict.fromkeys(xs))


def text_fields(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("id", "dx", "cites", "cite", "blocked_by", "path_id", "lineage", "ultimate_view", "members_ids"):
                continue
            yield from text_fields(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from text_fields(v)


def vocab_check(obj, where):
    for s in text_fields(obj):
        low = s.lower().replace("diagnosis.json", "")
        for b in BANNED:
            if b in low:
                ERR.append(f"{where}: banned word '{b}' in: {s[:90]}")


# ---------------------------------------------------------------- obstacle_correspondence
def edges():
    E = {}
    for a, e in DIAG.items():
        for q in e.get("equivalences") or []:
            E[frozenset((a, q["id"]))] = q["grade"]
    return E


def build_obstacles():
    E = edges()
    rows, seen = [], set()
    for spec in spec_obstacles.ROWS:
        rid = spec["id"]
        if rid in seen or not rid.startswith("oc:"):
            ERR.append(f"{rid}: duplicate or bad id")
        seen.add(rid)
        members, all_cites = [], []
        ids = [m["dx"] for m in spec["members"]]
        for m in spec["members"]:
            dx = m["dx"]
            if dx not in DIAG:
                ERR.append(f"{rid}: dx {dx} not in layers/diagnosis.json")
                continue
            ok, bl = cite_check(m["cites"], f"{rid}/{dx}")
            members.append({"dx": dx, "lens": DIAG[dx]["lens"], "name": DIAG[dx]["name"], "group": DIAG[dx]["group"],
                            "term": m["term"], "cites": m["cites"], "user_facing": ok and DIAG[dx].get("user_facing") is not False})
            all_cites += m["cites"]
        lenses = uniq(m["lens"] for m in members)
        if len(lenses) < 2:
            ERR.append(f"{rid}: members span fewer than two lenses")
        # edges among members (from diagnosis.json), connectivity, grade
        links = []
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                g = E.get(frozenset((a, b)))
                if g:
                    links.append({"a": a, "b": b, "grade": g, "cross_lens": DIAG[a]["lens"] != DIAG[b]["lens"]})
        adj = {x: set() for x in ids}
        for lk in links:
            adj[lk["a"]].add(lk["b"])
            adj[lk["b"]].add(lk["a"])
        comp, st = set(), [ids[0]]
        while st:
            x = st.pop()
            if x not in comp:
                comp.add(x)
                st += list(adj[x] - comp)
        if comp != set(ids):
            ERR.append(f"{rid}: members not connected by diagnosis.json equivalences: {sorted(set(ids) - comp)}")
        cross = [lk["grade"] for lk in links if lk["cross_lens"]]
        if not cross:
            ERR.append(f"{rid}: no cross-lens equivalence among members")
        grade = max(cross or ["partial"], key=GRADES.index)
        cites = uniq(all_cites + spec.get("extra_cites", []))
        ok, blocked = cite_check(cites, rid)
        row = {
            "id": rid, "title": spec["title"], "members": members, "lenses": lenses,
            "grade": grade,
            "grade_basis": "weakest cross-lens grade among the diagnosis.json equivalences that join the members",
            "links": links,
            "what_is_shared": spec["what_is_shared"], "what_differs": spec["what_differs"],
            "principle": principle(spec["principle"], rid),
            "cites": cites,
            "pending_members": spec.get("pending_members", []),
            "user_facing": ok,
            "blocked_by": blocked,
        }
        if not row["what_differs"].strip():
            ERR.append(f"{rid}: empty what_differs")
        vocab_check(row, rid)
        rows.append(row)
    return {
        "table": "obstacle_correspondence",
        "about": "Corresponding obstacles and states across the three lenses, derived by code from the equivalences in layers/diagnosis.json and then reviewed against the cited teachings. A row never says two things are the same: it states what is shared and, always, what differs. Grades follow diagnosis.json (exact / partial / same-under-standpoint). Correspondences are interpretation-layer claims; the texts are quoted, not rewritten.",
        "grades": {"exact": "the texts define the same thing", "partial": "overlapping but defined differently; what differs is stated", "same-under-standpoint": "the same only when seen from the named standpoint"},
        "rows": rows,
    }


# ---------------------------------------------------------------- one_truth
def build_one_truth():
    fp = dict(spec_one_truth.FIRST_PRINCIPLE)
    ok, bl = cite_check(fp["cites"], "first_principle")
    if not ok:
        ERR.append("first_principle: RV 1.164.46 not citable")
    t = o.teaching("tea:rgveda:1.164.46")
    fp["original"] = t["original"] if t else None
    fp["user_facing"] = ok
    rows = []
    for spec in spec_one_truth.ROWS:
        rid = spec["id"]
        if spec["lineage"] != "cross-lineage" and spec["lineage"] not in LINEAGES:
            ERR.append(f"{rid}: lineage {spec['lineage']} not in data/lineages.json")
        ok, blocked = cite_check(spec["cites"], rid)
        row = {k: v for k, v in spec.items() if k != "force_user_facing_false"}
        row["principle_relating_it"] = principle(spec["principle_relating_it"], rid)
        for f in ("name_for_the_ultimate", "standpoint", "what_it_denies", "tradition_objections"):
            if not row.get(f):
                ERR.append(f"{rid}: empty {f}")
        row["user_facing"] = ok and not spec.get("force_user_facing_false")
        row["blocked_by"] = blocked
        if spec.get("provisional"):
            row["user_facing_reason"] = "provisional row: not yet reconciled; never shown as a settled correspondence"
        vocab_check(row, rid)
        rows.append(row)
    return {
        "table": "one_truth",
        "about": "Each lineage's own name for the ultimate, the standpoint it speaks from, what it denies, and the reconciliation principle (config/principles.md) that relates it to the others. The one-truth reading is an interpretation-layer hypothesis. Each row records the lineage's own objection, and denials are never erased.",
        "first_principle": fp,
        "rows": rows,
    }


# ---------------------------------------------------------------- path_map_correspondence
def ref_cites(pid, ref):
    rule = spec_paths.REF_RULES.get(pid)
    if not rule or not ref:
        return []
    pre, tpl = rule
    out = []
    for part in re.split(r"[;,]", ref):
        part = part.strip()
        if part.startswith(pre):
            part = part[len(pre):]
        part = part.replace("–", "-").strip()
        if re.fullmatch(r"\d+(\.\d+)?(-\d+)?", part) or re.fullmatch(r"\d+", part):
            if "-" in part and pid.startswith("pth:tattvartha"):  # '10.1-2' -> 10.1, 10.2
                head, a_b = part.rsplit(".", 1)
                a, b = a_b.split("-")
                out += [f"{tpl}{head}.{i}" for i in range(int(a), int(b) + 1)]
            else:
                out.append(tpl + part)
    return out


def build_paths():
    for pid, order, band in spec_paths.BAND_CLAIMS:
        st = [x for x in PATHS.get(pid, {}).get("stages", []) if x.get("order") == order]
        if not st or st[0].get("band") != band:
            ERR.append(f"band claim no longer true: {pid} stage {order} expected {band}, data has {st[0].get('band') if st else 'no stage'}")
    maps, rows = [], []
    for m in spec_paths.MAPS:
        mid = m["id"]
        if m["lineage"] not in LINEAGES:
            ERR.append(f"{mid}: lineage {m['lineage']} not in data/lineages.json")
        stages = []
        if m["path_id"]:
            p = PATHS.get(m["path_id"])
            if not p:
                ERR.append(f"{mid}: path {m['path_id']} not in data/paths.json")
            else:
                for s in p["stages"]:
                    cites = [c for c in (s.get("rests_on") or []) if c in TEACH]
                    dropped = [c for c in (s.get("rests_on") or []) if c not in TEACH]
                    ov = spec_paths.STAGE_CITE_OVERRIDES.get((m["path_id"], s.get("order")))
                    if ov:
                        cites = ov
                    elif not cites:
                        cites = [c for c in ref_cites(m["path_id"], s.get("ref")) if c in TEACH]
                    if dropped:
                        WARN.append(f"{mid}/{s.get('order')}: rests_on ids missing from data/ dropped: {dropped}")
                    stages.append({"order": s.get("order"), "name": s.get("name"), "gloss": s.get("gloss"),
                                   "ref": s.get("ref"), "band": s.get("band"), "band_source": "data/paths.json",
                                   "cites": cites})
        for s in m.get("extra_stages", []):
            stages.append({**{k: v for k, v in s.items() if k != "band_note"}, "band_source": "this table",
                           **({"band_note": s["band_note"]} if s.get("band_note") else {})})
        for s in stages:
            sid = f"pm:{mid[4:]}:{s['order']}"
            if s["band"] is not None and s["band"] not in spec_paths.BANDS:
                ERR.append(f"{sid}: bad band {s['band']}")
            ok, blocked = cite_check(s["cites"], sid)
            row = {"id": sid, "map": mid, "stage_order": s["order"], "stage": s["name"], "gloss": s["gloss"],
                   "ref": s["ref"], "band": s["band"], "band_source": s["band_source"], "cites": s["cites"],
                   "user_facing": ok and s["band"] is not None, "blocked_by": blocked}
            if s["band"] is None:
                row["band_note"] = "data/paths.json gives this stage no band; left unaligned"
            if s.get("band_note"):
                row["band_note"] = s["band_note"]
            note = (m.get("safety_notes") or {}).get(s["name"])
            if note:
                row["safety_note"] = note
            vocab_check(row, sid)
            rows.append(row)
        ok, blocked = cite_check(m["objection_to_alignment"]["cites"], f"{mid}/objection")
        mrow = {"id": mid, "path_id": m["path_id"], "lineage": m["lineage"], "name": m["name"],
                "objection_to_alignment": {**m["objection_to_alignment"], "user_facing": ok, "blocked_by": blocked},
                "principle": principle(m["principle"], mid),
                "stages": [r["id"] for r in rows if r["map"] == mid]}
        mrow["user_facing_stages"] = sum(1 for r in rows if r["map"] == mid and r["user_facing"])
        mrow["user_facing"] = ok and mrow["user_facing_stages"] > 0
        vocab_check(mrow, mid)
        maps.append(mrow)
    by_band = {b: [r["id"] for r in rows if r["band"] == b] for b in spec_paths.BANDS}
    by_band["unaligned"] = [r["id"] for r in rows if r["band"] is None]
    return {
        "table": "path_map_correspondence",
        "about": "Stages of the main path maps the product can name, each placed in an interpretive band (B0–B8, config/data_model.md). A shared band means only 'comparable place in a course of practice', never 'the same attainment'. Each map carries its own tradition's objection to being aligned. A stage row is user-facing only if every citation is sourced or text-verified and not restricted.",
        "bands": spec_paths.BANDS,
        "band_notes": spec_paths.BAND_NOTES,
        "maps": maps,
        "rows": rows,
        "by_band": by_band,
    }


def main():
    ob = build_obstacles()
    ot = build_one_truth()
    pm = build_paths()
    out = ROOT / "layers/tables"
    out.mkdir(parents=True, exist_ok=True)
    for name, obj in (("obstacle_correspondence", ob), ("one_truth", ot), ("path_map_correspondence", pm)):
        (out / f"{name}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    # re-read and re-validate the written files (round trip)
    for name in ("obstacle_correspondence", "one_truth", "path_map_correspondence"):
        json.loads((out / f"{name}.json").read_text(encoding="utf-8"))
    blockers = Counter()
    for r in ob["rows"] + ot["rows"] + pm["rows"]:
        for b in r["blocked_by"]:
            blockers[f"{b['cite']} ({b['why']})"] += 1
    rep = {
        "obstacle_rows": len(ob["rows"]), "obstacle_user_facing": sum(r["user_facing"] for r in ob["rows"]),
        "obstacle_grades": dict(Counter(r["grade"] for r in ob["rows"])),
        "obstacle_members": sum(len(r["members"]) for r in ob["rows"]),
        "obstacle_lens_coverage": dict(Counter(len(r["lenses"]) for r in ob["rows"])),
        "one_truth_rows": len(ot["rows"]), "one_truth_user_facing": sum(r["user_facing"] for r in ot["rows"]),
        "one_truth_provisional": [r["id"] for r in ot["rows"] if r.get("provisional")],
        "path_maps": len(pm["maps"]), "path_rows": len(pm["rows"]),
        "path_rows_user_facing": sum(r["user_facing"] for r in pm["rows"]),
        "path_rows_by_band": {b: len(v) for b, v in pm["by_band"].items()},
        "path_maps_user_facing": [m["id"] for m in pm["maps"] if m["user_facing"]],
        "principles_used": dict(Counter([r["principle"]["id"] for r in ob["rows"]] + [r["principle_relating_it"]["id"] for r in ot["rows"]] + [m["principle"]["id"] for m in pm["maps"]])),
        "top_blockers": blockers.most_common(40),
        "errors": ERR, "warnings": WARN,
    }
    (HERE / "build_report.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: v for k, v in rep.items() if k not in ("top_blockers", "warnings")}, ensure_ascii=False, indent=1))
    print("warnings:", len(WARN))
    for w in WARN[:20]:
        print("  W", w)
    print("top blockers:", blockers.most_common(15))
    if ERR:
        print("FAILED with", len(ERR), "errors")
        sys.exit(1)
    print("OK")


if __name__ == "__main__":
    main()
