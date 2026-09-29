#!/usr/bin/env python3
"""Independent check of the written tables (reads only layers/tables/*.json, layers/diagnosis.json, data/).
    python3 layers/_gen/tables/validate.py
"""
import json
import re
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from insight import ontology as o  # noqa: E402

P = {"P1-level": "Level of truth", "P2-standpoint": "Standpoint", "P3-path": "Path by temperament",
     "P4-stage": "Stage of the student", "P5-neyartha": "Provisional vs definitive", "P6-upaya": "Skillful means",
     "P7-arthavada": "Praise passages", "P8-six-marks": "The six marks of purport"}
D = {e["id"]: e for e in json.loads((ROOT / "layers/diagnosis.json").read_text(encoding="utf-8"))}
T = o.teachings()
errs, n = [], {"rows": 0, "cites": 0}


def load(name):
    return json.loads((ROOT / "layers/tables" / f"{name}.json").read_text(encoding="utf-8"))


def chk_cites(cites, where, uf):
    if not cites:
        errs.append(f"{where}: no cites")
    for c in cites:
        n["cites"] += 1
        if c not in T:
            errs.append(f"{where}: {c} not in data/")
        elif uf and not o.citable(c):
            errs.append(f"{where}: user_facing but {c} not citable")


def chk_pr(p, where):
    if P.get(p.get("id")) != p.get("name") or not p.get("reason"):
        errs.append(f"{where}: principle {p}")


ob = load("obstacle_correspondence")
for r in ob["rows"]:
    n["rows"] += 1
    if r["grade"] not in ("exact", "partial", "same-under-standpoint"):
        errs.append(f"{r['id']}: grade")
    for m in r["members"]:
        if m["dx"] not in D or D[m["dx"]]["lens"] != m["lens"]:
            errs.append(f"{r['id']}: member {m['dx']} missing or lens mismatch")
        chk_cites(m["cites"], f"{r['id']}/{m['dx']}", r["user_facing"])
        if not set(m["cites"]) <= set(r["cites"]):
            errs.append(f"{r['id']}: member cites not in row cites")
    if len({m['lens'] for m in r['members']}) < 2:
        errs.append(f"{r['id']}: <2 lenses")
    if not r["what_differs"]:
        errs.append(f"{r['id']}: no what_differs")
    chk_cites(r["cites"], r["id"], r["user_facing"])
    chk_pr(r["principle"], r["id"])
ot = load("one_truth")
if ot["first_principle"]["cites"] != ["tea:rgveda:1.164.46"] or not o.citable("tea:rgveda:1.164.46"):
    errs.append("first principle")
for r in ot["rows"]:
    n["rows"] += 1
    chk_cites(r["cites"], r["id"], r["user_facing"])
    chk_pr(r["principle_relating_it"], r["id"])
    if r.get("provisional") and (r["user_facing"] or r.get("status") != "not yet reconciled"):
        errs.append(f"{r['id']}: provisional row must be user_facing false and 'not yet reconciled'")
pm = load("path_map_correspondence")
ids = set()
for r in pm["rows"]:
    n["rows"] += 1
    ids.add(r["id"])
    if r["band"] is not None and r["band"] not in pm["bands"]:
        errs.append(f"{r['id']}: band")
    chk_cites(r["cites"], r["id"], r["user_facing"])
for m in pm["maps"]:
    chk_pr(m["principle"], m["id"])
    chk_cites(m["objection_to_alignment"]["cites"], m["id"], m["objection_to_alignment"]["user_facing"])
    if not set(m["stages"]) <= ids:
        errs.append(f"{m['id']}: stage ids")
bb = [x for v in pm["by_band"].values() for x in v]
if sorted(bb) != sorted(ids):
    errs.append("by_band does not cover every row exactly once")
blob = json.dumps([ob, ot, pm], ensure_ascii=False).lower()
for w in ("contradiction", "contradict"):
    if w in blob:
        errs.append(f"banned word {w}")
print(json.dumps(n), "errors:", len(errs))
for e in errs[:40]:
    print(" ", e)
sys.exit(1 if errs else 0)
