"""Helpers for subagents writing shards.

Usage (from the tradition-ontology/ directory), in a generator script such as
shards/skeleton/U13-advaita/_gen/part1.py:

    import sys; sys.path.insert(0, "scripts")
    from shardlib import Shard, V, D, T
    sh = Shard("skeleton", "U13-advaita")
    sh.add("sources", {"id": "src:vivekacudamani", "title": "Vivekacūḍāmaṇi", ..., "verification": V("high")})
    sh.add("teachings", {"id": "tea:vivekacudamani:20", "source": "src:vivekacudamani",
                         "location": {"ref": "20"}, "paraphrase": "...",
                         "tags": T("ultimate", "absolute", ["knowledge"], "advanced"),
                         "types": ["ultimate"], "verification": V("moderate")})
    sh.save()

save() merges with what is already on disk (same id -> the newer object replaces the older one),
so you can write your unit in several parts and re-run any part safely.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def V(confidence="moderate", level="skeleton"):
    """Verification block. confidence: high | moderate | low."""
    return {"level": level, "confidence": confidence, "unverified": False, "checks": []}


def D(trad=None, trad_from=None, trad_to=None, sch=None, sch_from=None, sch_to=None, confidence=None):
    """Dating block with the tradition's and the scholarly account kept apart. Years: int, negative = BCE."""
    d = {}
    if trad:
        d["tradition"] = {"text": trad, "from": trad_from, "to": trad_to}
    if sch:
        d["scholarly"] = {"text": sch, "from": sch_from, "to": sch_to}
    if confidence:
        d["confidence"] = confidence
    return d


def T(level, standpoint, path, stage, naya=None, stage_native=None):
    """The four tags. See config/principles.md for the vocabularies."""
    if isinstance(path, str):
        path = [path]
    t = {"level": level, "standpoint": standpoint, "naya": naya, "path": path, "stage": stage}
    if stage_native:
        t["stage_native"] = stage_native
    return t


class Shard:
    def __init__(self, phase, unit):
        self.dir = os.path.join(ROOT, "shards", phase, unit)
        os.makedirs(self.dir, exist_ok=True)
        self.buf = {}

    def add(self, entity, obj):
        self.buf.setdefault(entity, []).append(obj)
        return obj

    def extend(self, entity, objs):
        for o in objs:
            self.add(entity, o)

    def log(self, kind, entity, change, reason, principle=None, rests_on=None, by=None):
        o = {"kind": kind, "entity": entity, "change": change, "reason": reason}
        if principle:
            o["principle"] = principle
        if rests_on:
            o["rests_on"] = rests_on
        o["by"] = by or os.path.basename(self.dir)
        self.buf.setdefault("interpretation_log", []).append(o)

    def save(self):
        for entity, objs in self.buf.items():
            path = os.path.join(self.dir, f"{entity}.jsonl")
            existing = []
            if os.path.exists(path):
                with open(path, encoding="utf-8") as fh:
                    existing = [json.loads(l) for l in fh if l.strip()]
            if entity == "interpretation_log":
                seen = {json.dumps(o, sort_keys=True, ensure_ascii=False) for o in existing}
                merged = existing + [o for o in objs if json.dumps(o, sort_keys=True, ensure_ascii=False) not in seen]
            else:
                order, byid = [], {}
                for o in existing + objs:
                    k = o.get("id") or json.dumps(o, sort_keys=True, ensure_ascii=False)
                    if k not in byid:
                        order.append(k)
                    byid[k] = o
                merged = [byid[k] for k in order]
            with open(path, "w", encoding="utf-8") as fh:
                for o in merged:
                    fh.write(json.dumps(o, ensure_ascii=False) + "\n")
        n = {e: len(v) for e, v in self.buf.items()}
        self.buf = {}
        print("saved", json.dumps(n))
