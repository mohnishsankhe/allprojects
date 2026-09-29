#!/usr/bin/env python3
"""Build check for the product layers: which entries are user-facing now (all citations resolve to sourced or
text-verified, non-restricted teachings), which citations are still skeleton or missing. Mechanical; no judgement.
    python3 scripts/check_layers.py            # summary
    python3 scripts/check_layers.py --json     # full report to layers/_check.json
"""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from insight import ontology  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def cites_of(e):
    out = list(e.get("cites") or [])
    for f in ("definitions", "markers", "states", "equivalences", "paired_practices", "warnings"):
        for it in e.get(f) or []:
            if isinstance(it, dict):
                out += it.get("cites") or []
    return out


def main():
    rep = {}
    for layer, usable in (("diagnosis", ontology.diagnosis()), ("practices", ontology.practices())):
        p = ROOT / "layers" / f"{layer}.json"
        if not p.exists():
            rep[layer] = {"missing": True}
            continue
        raw = json.loads(p.read_text(encoding="utf-8"))
        status = Counter()
        unresolved = Counter()
        for e in raw:
            for c in cites_of(e):
                t = ontology.teaching(c)
                if not t:
                    status["missing"] += 1
                    unresolved[c] += 1
                elif ontology.citable(c):
                    status["citable"] += 1
                else:
                    status["not-citable:" + (t["level"] if not t["restricted"] else "restricted")] += 1
                    unresolved[c] += 1
        rep[layer] = {"entries": len(raw), "user_facing_now": len(usable), "citations": dict(status),
                      "top_unresolved": unresolved.most_common(40)}
        if layer == "practices":
            rep[layer]["gentle_user_facing"] = len(ontology.gentle_practices())
    if "--json" in sys.argv:
        (ROOT / "layers" / "_check.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding="utf-8")
    for k, v in rep.items():
        print(k, json.dumps({x: y for x, y in v.items() if x != "top_unresolved"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
