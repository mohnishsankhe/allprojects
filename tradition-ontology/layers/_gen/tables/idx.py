#!/usr/bin/env python3
"""Fetch teachings by id (or by slug:ref prefix) with level and a short paraphrase. Read-only helper.
    python3 layers/_gen/tables/idx.py tea:bhagavad-gita:12.8 tea:mandukya-upanisad:7 ...
    python3 layers/_gen/tables/idx.py --prefix tea:satipatthana-sutta:mn10:
"""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from insight import ontology as o  # noqa: E402

def show(tid, n=260):
    t = o.teaching(tid)
    if not t:
        print(f"{tid}  MISSING")
        return
    via = "" if t["id"] == tid else f" (resolved->{t['id']})"
    print(f"{tid}{via}  [{t['level']}{' UNVER' if t['unverified'] else ''}{' RESTR' if t['restricted'] else ''}] ref={t['ref']} :: {(t['paraphrase'] or '')[:n]}")

if __name__ == "__main__":
    args = sys.argv[1:]
    n = 260
    if args and args[0].startswith("--n="):
        n = int(args.pop(0)[4:])
    if args and args[0] == "--prefix":
        for p in args[1:]:
            for k in sorted(o.teachings()):
                if k.startswith(p):
                    show(k, n)
    else:
        for a in args:
            show(a, n)
