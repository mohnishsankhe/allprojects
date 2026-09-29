#!/usr/bin/env python3
"""Orchestrator overrides on layers/practices.json (idempotent; run after build.py and refresh_p1.py).

1. Vijñāna Bhairava practices are never 'gentle': VBT 157–159 say the teaching is to be kept secret and given only to
   devotees within the teacher's circle. Respecting the text's own rule of transmission is the conservative reading,
   so every VBT-based gentle entry becomes 'needs-teacher' (DECISIONS 2026-09-29).
"""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PX = os.path.join(ROOT, "layers", "practices.json")
NOTE = (" Tier set to needs-teacher by the orchestrator: the Vijñāna Bhairava itself says its teaching is to be kept "
        "secret and given only within the teacher's circle (VBT 157–159), so the product does not suggest it on its own.")

P = json.load(open(PX, encoding="utf-8"))
# 0. user_facing convention (DECISIONS 2026-09-29 22:24): citation status is computed at load time by the app;
#    user_facing:false is only for manual exclusion, so a rebuild must not bring back the old computed flags.
for p in P:
    if p.get("user_facing") is False and not p.get("manual_exclusion"):
        p["user_facing"] = True
n = 0
for p in P:
    vbt = any(str(c).startswith("tea:vijnana-bhairava-tantra:") for c in p.get("cites") or [])
    if vbt and p.get("safety_tier") == "gentle":
        p["safety_tier"] = "needs-teacher"
        p["tier_reason"] = (p.get("tier_reason") or "").rstrip() + NOTE
        n += 1
with open(PX, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(P, indent=1, ensure_ascii=False) + "\n")
print("VBT gentle -> needs-teacher:", n)
