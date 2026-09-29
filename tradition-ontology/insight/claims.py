"""Forbidden-claims scanner (health/cure, diagnosis, prediction, astrology). Deterministic; used on every output."""
from __future__ import annotations

import json
import re
from functools import lru_cache
from typing import Iterable

from . import config


@lru_cache(maxsize=None)
def _rules():
    d = json.loads((config.RULES / "forbidden_claims.json").read_text(encoding="utf-8"))
    cats = {c: [re.compile(p, re.I) for p in pats] for c, pats in d["categories"].items()}
    allow = [a.lower() for a in d.get("allow_phrases", [])]
    return cats, allow


def scan(text: str) -> list[dict]:
    """Return a list of hits {category, match, sentence}. Sentences that are standard disclaimers are exempt."""
    cats, allow = _rules()
    hits = []
    for sent in re.split(r"(?<=[.!?])\s+|\n+", text or ""):
        low = sent.lower()
        if any(a in low for a in allow):
            continue
        for c, pats in cats.items():
            for p in pats:
                m = p.search(sent)
                if m:
                    hits.append({"category": c, "match": m.group(0), "sentence": sent.strip()[:300]})
    return hits


def scan_fields(obj, skip_keys: Iterable[str] = ("original", "quote", "evidence", "counter_evidence", "person_words", "basis_quote")) -> list[dict]:
    """Scan every string in a nested object except verbatim fields (teaching originals, the person's own words)."""
    skip = set(skip_keys)
    out = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in skip:
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{path}[{i}]")
        elif isinstance(o, str):
            for h in scan(o):
                h["path"] = path
                out.append(h)

    walk(obj, "$")
    return out


def strip_sentences(text: str) -> str:
    """Drop any sentence that carries a forbidden claim (used by the rules engine as a last line of defence)."""
    keep = []
    for sent in re.split(r"(?<=[.!?])\s+", text or ""):
        if not scan(sent):
            keep.append(sent)
    return " ".join(keep).strip()
