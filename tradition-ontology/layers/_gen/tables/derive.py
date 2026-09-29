#!/usr/bin/env python3
"""Step 1 (mechanical): derive candidate obstacle correspondences from layers/diagnosis.json equivalences.
Writes layers/_gen/tables/derived_edges.json: every cross-lens equivalence edge (deduplicated, symmetric check),
its grade, its cites and their citability, plus connected components under cross-lens edges only.
    python3 layers/_gen/tables/derive.py
"""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from insight import ontology as o  # noqa: E402

D = {e["id"]: e for e in json.loads((ROOT / "layers/diagnosis.json").read_text(encoding="utf-8"))}
usable = o.diagnosis()


def main():
    edges = {}
    asym = []
    for a, e in D.items():
        for q in e.get("equivalences") or []:
            b = q["id"]
            key = tuple(sorted((a, b)))
            rev = [r for r in D[b].get("equivalences") or [] if r["id"] == a]
            if not rev or rev[0]["grade"] != q["grade"]:
                asym.append([a, b, q["grade"], rev[0]["grade"] if rev else None])
            ed = edges.setdefault(key, {"a": key[0], "b": key[1], "grade": q["grade"], "cites": [], "notes": []})
            for c in q.get("cites") or []:
                if c not in ed["cites"]:
                    ed["cites"].append(c)
            ed["notes"].append({"from": a, "note": q.get("note", "")})
    out = []
    for ed in edges.values():
        la, lb = D[ed["a"]]["lens"], D[ed["b"]]["lens"]
        ed["lenses"] = [la, lb]
        ed["cross_lens"] = la != lb
        ed["cites_citable"] = {c: o.citable(c) for c in ed["cites"]}
        out.append(ed)
    # components under cross-lens edges
    adj = {}
    for ed in out:
        if ed["cross_lens"]:
            adj.setdefault(ed["a"], set()).add(ed["b"])
            adj.setdefault(ed["b"], set()).add(ed["a"])
    seen, comps = set(), []
    for n in sorted(adj):
        if n in seen:
            continue
        st, comp = [n], []
        while st:
            x = st.pop()
            if x in seen:
                continue
            seen.add(x)
            comp.append(x)
            st += sorted(adj[x] - seen)
        comps.append(sorted(comp))
    rep = {"edges": sorted(out, key=lambda x: (x["a"], x["b"])), "asymmetric": asym, "cross_lens_components": comps,
           "dx_user_facing_now": sorted(usable)}
    (ROOT / "layers/_gen/tables/derived_edges.json").write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print("edges", len(out), "cross-lens", sum(e["cross_lens"] for e in out), "asymmetric", len(asym))
    print("components", [len(c) for c in comps])
    for ed in rep["edges"]:
        if ed["cross_lens"]:
            ok = sum(ed["cites_citable"].values())
            print(f'{ed["a"]:32s} {ed["b"]:32s} {ed["grade"]:22s} cites {ok}/{len(ed["cites"])}')


if __name__ == "__main__":
    main()
