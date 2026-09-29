"""The specificity rule (anti-horoscope): every insight must rest on this person's own words.

filter_insights() drops any insight without a valid evidence reference or that matches a generic pattern.
swap_overlap() is an evaluation helper: how many of a report's evidence quotes also appear in another person's text.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache

from . import config


@lru_cache(maxsize=None)
def _rules():
    d = json.loads((config.RULES / "specificity.json").read_text(encoding="utf-8"))
    return d, [re.compile(p, re.I) for p in d["generic_patterns"]]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip().lower()


def is_generic(text: str) -> bool:
    _, pats = _rules()
    return any(p.search(text or "") for p in pats)


def filter_insights(insights: list, quotes: dict) -> tuple[list, list]:
    """insights: [{text, evidence_refs:[quote_id], ...}]; quotes: {quote_id: quote_text}. Returns (kept, dropped)."""
    d, _ = _rules()
    kept, dropped = [], []
    for ins in insights or []:
        refs = [q for q in ins.get("evidence_refs") or [] if q in quotes]
        if len(refs) < d["min_evidence_refs_per_insight"]:
            dropped.append({**ins, "_why": "no evidence from this person"})
        elif is_generic(ins.get("text", "")):
            dropped.append({**ins, "_why": "generic statement"})
        else:
            kept.append({**ins, "evidence_refs": refs})
    return kept, dropped


def swap_overlap(report: dict, other_text: str) -> float:
    """Share of the report's evidence quotes that also occur verbatim in another person's text (0.0 = fully specific)."""
    qs = [e["quote"] for m in report.get("mappings") or [] for e in m.get("evidence") or []]
    if not qs:
        return 0.0
    o = norm(other_text)
    return sum(1 for q in qs if norm(q) in o) / len(qs)
