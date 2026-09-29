"""Read-only access to the ontology (data/) and the product layers (layers/).

The product may only show sourced or text-verified entries. Every citation is resolved here: a teaching is citable
only if it exists, its level is 'sourced' or 'text-verified', it is not flagged [unverified], and it does not belong
to a restricted practice. Layer entries keep only the citations that resolve; an entry with none left is not usable.
"""
from __future__ import annotations

import glob
import json
import os
from functools import lru_cache
from typing import Optional

from . import config

CITABLE_LEVELS = ("sourced", "text-verified")


@lru_cache(maxsize=1)
def sources() -> dict:
    p = config.DATA / "sources.json"
    if not p.exists():
        return {}
    return {o["id"]: o for o in json.loads(p.read_text(encoding="utf-8"))}


@lru_cache(maxsize=1)
def restricted_practices() -> set:
    p = config.DATA / "practices.json"
    if not p.exists():
        return set()
    return {o["id"] for o in json.loads(p.read_text(encoding="utf-8")) if o.get("restricted")}


@lru_cache(maxsize=1)
def teachings() -> dict:
    """id -> compact teaching record. Loads data/teachings/*.jsonl once."""
    out = {}
    for f in glob.glob(str(config.DATA / "teachings" / "*.jsonl")):
        with open(f, encoding="utf-8") as fh:
            for line in fh:
                if not line.strip():
                    continue
                o = json.loads(line)
                v = o.get("verification") or {}
                orig = o.get("original") or {}
                out[o["id"]] = {
                    "id": o["id"], "source": o.get("source"), "ref": (o.get("location") or {}).get("ref"),
                    "original": orig.get("text") if isinstance(orig, dict) else None,
                    "script": orig.get("script") if isinstance(orig, dict) else None,
                    "paraphrase": o.get("paraphrase") or o.get("summary") or "",
                    "level": v.get("level", "skeleton"), "unverified": bool(v.get("unverified")),
                    "restricted": bool(o.get("restricted")) or bool(set(o.get("practices") or []) & restricted_practices()),
                    "retired": bool(o.get("retired")), "superseded_by": o.get("superseded_by"),
                    "speaker": o.get("speaker"),
                }
    return out


def teaching(tid: str) -> Optional[dict]:
    t = teachings().get(tid)
    # follow a superseded skeleton entry to the verified entry that replaced it
    seen = set()
    while t and t.get("superseded_by") and t["superseded_by"] not in seen:
        seen.add(t["superseded_by"])
        nxt = teachings().get(t["superseded_by"])
        if not nxt:
            break
        t = nxt
    return t


def citable(tid: str, allow_restricted: bool = False) -> bool:
    t = teaching(tid)
    return bool(t and t["level"] in CITABLE_LEVELS and not t["unverified"] and not t["retired"]
                and (allow_restricted or not t["restricted"]))


def citation(tid: str) -> dict:
    """A resolved, displayable citation. Raises KeyError if not citable."""
    if not citable(tid):
        raise KeyError(tid)
    t = teaching(tid)
    src = sources().get(t["source"] or "", {})
    return {"id": t["id"], "source": t["source"], "title": src.get("title") or src.get("name") or t["source"],
            "ref": t["ref"], "original": t["original"], "paraphrase": t["paraphrase"], "level": t["level"]}


def _filter_cites(cites) -> list:
    return [c for c in (cites or []) if isinstance(c, str) and citable(c)]


def _clean_entry(e: dict, list_fields=("definitions", "markers", "states", "equivalences", "paired_practices", "warnings")) -> Optional[dict]:
    """Keep only sub-items whose citations resolve; drop the entry if nothing citable remains."""
    if e.get("user_facing") is False:
        return None
    e = json.loads(json.dumps(e))
    total = 0
    for f in list_fields:
        items = []
        for it in e.get(f) or []:
            if isinstance(it, dict) and "cites" in it:
                it["cites"] = _filter_cites(it["cites"])
                if not it["cites"]:
                    continue
                total += len(it["cites"])
            items.append(it)
        if f in e:
            e[f] = items
    if "cites" in e:
        e["cites"] = _filter_cites(e["cites"])
        total += len(e["cites"])
    return e if total else None


@lru_cache(maxsize=1)
def diagnosis() -> dict:
    p = config.LAYERS / "diagnosis.json"
    if not p.exists():
        return {}
    out = {}
    for e in json.loads(p.read_text(encoding="utf-8")):
        c = _clean_entry(e)
        if c and c.get("definitions"):
            out[c["id"]] = c
    return out


@lru_cache(maxsize=1)
def practices() -> dict:
    p = config.LAYERS / "practices.json"
    if not p.exists():
        return {}
    out = {}
    for e in json.loads(p.read_text(encoding="utf-8")):
        c = _clean_entry(e)
        if c:
            out[c["id"]] = c
    return out


def gentle_practices() -> dict:
    return {k: v for k, v in practices().items() if v.get("safety_tier") == "gentle"}


@lru_cache(maxsize=None)
def table(name: str):
    p = config.LAYERS / "tables" / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else None


def reset_caches() -> None:
    for f in (sources, restricted_practices, teachings, diagnosis, practices, table):
        f.cache_clear()
