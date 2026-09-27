#!/usr/bin/env python3
"""Validate a shard directory (shards/<phase>/<unit>/) against config/data_model.md.

Usage: python3 scripts/validate_shard.py shards/skeleton/U13-advaita [--quiet]
Exit code 1 if any ERROR. Warnings are advisory.
"""
import json, os, re, sys

ENTITY_PREFIX = {
    "sources": "src", "lineages": "lin", "teachers": "tch", "teachings": "tea", "terms": "trm",
    "concepts": "cpt", "ultimate": "ult", "obstacles": "obs", "practices": "prc", "paths": "pth",
    "phenomenology": "phn", "disputes": "dsp", "borrowings": "brw", "interpretation_log": None,
    "checks": None, "A": "tea", "B": "tea", "disagreements": None, "fidelity": None, "skeleton_decisions": None,
}
REQUIRED = {
    "sources": ["id", "title", "language", "family", "lineages", "summary", "verification"],
    "lineages": ["id", "name", "family", "distinctive_positions", "summary", "verification"],
    "teachers": ["id", "name", "lineages", "summary", "verification"],
    "teachings": ["id", "source", "location", "paraphrase", "tags", "types", "verification"],
    "A": ["id", "source", "location", "paraphrase", "tags", "types"],
    "B": ["id", "source", "location", "paraphrase", "tags", "types"],
    "terms": ["id", "term", "language", "definitions", "verification"],
    "concepts": ["id", "name", "category", "definitions", "verification"],
    "ultimate": ["id", "lineage", "names", "verification"],
    "obstacles": ["id", "name", "category", "description", "lineages", "verification"],
    "practices": ["id", "name", "category", "method_summary", "lineages", "verification"],
    "paths": ["id", "name", "lineage", "stages", "verification"],
    "phenomenology": ["id", "lineage", "kind", "description", "verification"],
    "disputes": ["id", "question", "sides", "verification"],
    "borrowings": ["id", "from", "to", "what", "verification"],
    "interpretation_log": ["kind", "entity", "change", "reason"],
    "checks": ["id", "result", "method"],
}
LEVELS = {"skeleton", "sourced", "text-verified"}
CONF = {"high", "moderate", "low"}
TAG_LEVEL = {"ultimate", "conventional", "illusory", "bridging", "unmarked"}
TAG_STANDPOINT = {"absolute", "seeker", "divine", "cosmic", "substance", "mode", "causal", "experiential", "analytic",
                  "apophatic", "devotional", "ritual", "ethical-social", "polemical"}
TAG_NAYA = {None, "", "niscaya", "vyavahara", "naigama", "sangraha", "vyavahara-jain", "rjusutra", "sabda",
            "samabhirudha", "evambhuta", "dravyarthika", "paryayarthika"}
TAG_PATH = {"action", "knowledge", "devotion", "meditation", "body-breath", "ritual", "sound", "general"}
TAG_STAGE = {"beginner", "intermediate", "advanced", "realized", "all", "unmarked"}
TYPES = {"ultimate", "consciousness-mind", "body-layers", "practice", "ethics", "karma-liberation", "world-fate",
         "powers-experiences", "teacher-transmission", "sound-language", "death-dying", "dispute", "narrative"}
FAMILY = {"vedic", "ascetic", "shared"}
CONCEPT_CAT = {"ultimate", "consciousness-states", "self", "mind", "body-energy", "matter-qualities", "obstacles",
               "ethics", "karma-rebirth", "stages-maps", "signs-powers", "teacher-transmission", "cosmology-time",
               "sound-language", "death-dying", "disputes"}
PRACTICE_CAT = {"posture", "breath", "lock-seal", "cleansing", "sense-withdrawal-concentration", "meditation", "inquiry",
                "mantra-sound", "visualization-deity", "energy", "sleep-dream-death", "devotion-service", "ethics",
                "mind-training", "body-daily-rhythm", "ritual"}
OBSTACLE_CAT = {"affliction", "hindrance", "fetter", "passion", "obstacle", "poison", "impurity", "bond",
                "dosa-imbalance", "guna", "karma-type", "meditation-fault", "other"}
BANDS = {"B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", None, ""}
GRADES = {"exact", "partial", "same-under-standpoint", "analogous", "contested"}
ID_RE = re.compile(r"^[a-z]{2,3}:[a-z0-9][a-z0-9\-\.\/:~_]*$")
REF_FIELDS = {  # field -> expected prefix (list or scalar)
    "lineages": "lin", "parent": "lin", "sub_lineages": "lin", "founders": "tch", "key_teachers": "tch",
    "texts": "src", "teachers": "tch", "students": "tch", "source": "src", "lineage": "lin", "part_of": "src",
    "concepts": "cpt", "terms": "trm", "practices": "prc", "obstacles": "obs", "paths": "pth", "disputes": "dsp",
    "rests_on": "tea", "cross_refs": "tea", "key_teachings": "tea", "sequences": "pth", "path_maps": "pth",
    "related": "trm", "from": "lin", "to": "lin",
}


def check_refs(obj, entity, errs, warns, where):
    for f, pfx in REF_FIELDS.items():
        if f not in obj:
            continue
        if entity == "borrowings" and f in ("from", "to"):
            pass
        v = obj[f]
        vals = v if isinstance(v, list) else [v]
        for x in vals:
            if x is None or x == "":
                continue
            if not isinstance(x, str):
                if f in ("teachers",) and isinstance(x, dict):
                    continue
                warns.append(f"{where}: field '{f}' contains non-string {str(x)[:60]}")
                continue
            if not x.startswith(pfx + ":"):
                if f == "source" and entity in ("checks",):
                    continue
                # 'source' inside sub-objects handled separately; commentary refs etc. may be tea:
                if f in ("from", "to") and entity not in ("borrowings",):
                    continue
                errs.append(f"{where}: field '{f}' value '{x}' should start with '{pfx}:'")
            elif not ID_RE.match(x):
                warns.append(f"{where}: reference '{x}' in '{f}' is not a clean id (ascii lowercase slug)")


def validate_file(path, entity, errs, warns, seen):
    pfx = ENTITY_PREFIX.get(entity)
    with open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            where = f"{os.path.basename(path)}:{n}"
            try:
                obj = json.loads(line)
            except Exception as e:
                errs.append(f"{where}: invalid JSON ({e})")
                continue
            if not isinstance(obj, dict):
                errs.append(f"{where}: line is not a JSON object")
                continue
            for f in REQUIRED.get(entity, []):
                if f not in obj or obj[f] in (None, "", [], {}):
                    if entity == "sources" and f == "summary":
                        warns.append(f"{where}: missing '{f}'")
                    else:
                        errs.append(f"{where}: missing required field '{f}'")
            oid = obj.get("id")
            if pfx and oid:
                if not isinstance(oid, str) or not oid.startswith(pfx + ":"):
                    errs.append(f"{where}: id '{oid}' must start with '{pfx}:'")
                elif not ID_RE.match(oid):
                    errs.append(f"{where}: id '{oid}' is not a clean id (lowercase ascii, digits, - . / : ~)")
                key = (entity, oid)
                if key in seen:
                    errs.append(f"{where}: duplicate id '{oid}' (also at {seen[key]}) — merge them into one line")
                else:
                    seen[key] = where
            ver = obj.get("verification")
            if ver is not None:
                if not isinstance(ver, dict):
                    errs.append(f"{where}: verification must be an object")
                else:
                    if ver.get("level") not in LEVELS:
                        errs.append(f"{where}: verification.level '{ver.get('level')}' not in {sorted(LEVELS)}")
                    if ver.get("confidence") not in CONF:
                        errs.append(f"{where}: verification.confidence '{ver.get('confidence')}' not in {sorted(CONF)}")
            if entity in ("sources", "lineages") and obj.get("family") not in FAMILY:
                errs.append(f"{where}: family '{obj.get('family')}' not in {sorted(FAMILY)}")
            if entity in ("teachings", "A", "B"):
                t = obj.get("tags") or {}
                if t.get("level") not in TAG_LEVEL:
                    errs.append(f"{where}: tags.level '{t.get('level')}' not in {sorted(TAG_LEVEL)}")
                if t.get("standpoint") not in TAG_STANDPOINT:
                    errs.append(f"{where}: tags.standpoint '{t.get('standpoint')}' not in {sorted(TAG_STANDPOINT)}")
                if t.get("naya") not in TAG_NAYA:
                    errs.append(f"{where}: tags.naya '{t.get('naya')}' invalid")
                p = t.get("path")
                if not isinstance(p, list) or not p or any(x not in TAG_PATH for x in p):
                    errs.append(f"{where}: tags.path must be a non-empty list from {sorted(TAG_PATH)}")
                if t.get("stage") not in TAG_STAGE:
                    errs.append(f"{where}: tags.stage '{t.get('stage')}' not in {sorted(TAG_STAGE)}")
                ty = obj.get("types")
                if not isinstance(ty, list) or not ty or any(x not in TYPES for x in ty):
                    errs.append(f"{where}: types must be a non-empty list from {sorted(TYPES)}")
                loc = obj.get("location") or {}
                if not isinstance(loc, dict) or not loc.get("ref"):
                    errs.append(f"{where}: location.ref required")
                src = obj.get("source", "")
                if oid and src and isinstance(oid, str) and isinstance(src, str):
                    slug = src.split(":", 1)[-1]
                    if not oid.startswith(f"tea:{slug}:"):
                        errs.append(f"{where}: teaching id '{oid}' must start with 'tea:{slug}:'")
                if obj.get("original") and not isinstance(obj.get("original"), dict):
                    errs.append(f"{where}: original must be an object {{text, script, edition, licence}}")
            if entity == "concepts" and obj.get("category") not in CONCEPT_CAT:
                errs.append(f"{where}: concept category '{obj.get('category')}' not in {sorted(CONCEPT_CAT)}")
            if entity == "practices":
                if obj.get("category") not in PRACTICE_CAT:
                    errs.append(f"{where}: practice category '{obj.get('category')}' not in {sorted(PRACTICE_CAT)}")
                if obj.get("restricted") and len(str(obj.get("method_summary", ""))) > 900:
                    warns.append(f"{where}: restricted practice has a long method_summary — keep it a summary, no steps")
                if "convergence" in obj:
                    warns.append(f"{where}: do not write 'convergence' (computed by merge)")
            if entity == "obstacles" and obj.get("category") not in OBSTACLE_CAT:
                errs.append(f"{where}: obstacle category '{obj.get('category')}' not in {sorted(OBSTACLE_CAT)}")
            if entity == "paths":
                st = obj.get("stages")
                if isinstance(st, list):
                    for s in st:
                        if not isinstance(s, dict) or "name" not in s:
                            errs.append(f"{where}: each stage must be an object with at least 'name'")
                            break
                        if s.get("band") not in BANDS:
                            errs.append(f"{where}: stage band '{s.get('band')}' not in B0..B8")
            for listf in ("equivalents",):
                for e in obj.get(listf, []) or []:
                    if isinstance(e, dict) and e.get("grade") and e.get("grade") not in GRADES:
                        errs.append(f"{where}: equivalents grade '{e.get('grade')}' not in {sorted(GRADES)}")
            if entity == "terms":
                for c in obj.get("cross_language", []) or []:
                    if isinstance(c, dict) and c.get("grade") and c["grade"] not in {"exact", "partial", "same-under-standpoint"}:
                        errs.append(f"{where}: cross_language grade '{c.get('grade')}' must be exact|partial|same-under-standpoint")
            if entity == "disputes":
                rec = obj.get("reconciliation") or {}
                if rec and rec.get("status") not in ("reconciled", "partially-reconciled", "queued"):
                    errs.append(f"{where}: reconciliation.status must be reconciled|partially-reconciled|queued")
                txt = json.dumps(obj, ensure_ascii=False).lower()
                if "contradiction" in txt and "not yet reconciled" not in txt:
                    warns.append(f"{where}: avoid the word 'contradiction'; use 'not yet reconciled'")
                if len(obj.get("sides") or []) < 2:
                    errs.append(f"{where}: a dispute needs at least two sides")
            if entity != "checks":
                check_refs(obj, entity, errs, warns, where)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    d = sys.argv[1]
    quiet = "--quiet" in sys.argv
    errs, warns, seen = [], [], {}
    counts = {}
    for fn in sorted(os.listdir(d)):
        p = os.path.join(d, fn)
        if fn.endswith(".md") or os.path.isdir(p):
            continue
        if not fn.endswith(".jsonl"):
            warns.append(f"{fn}: unexpected file (only <entity>.jsonl and REPORT.md)")
            continue
        entity = fn[:-6]
        if entity not in ENTITY_PREFIX:
            errs.append(f"{fn}: unknown entity file name; allowed: {sorted(ENTITY_PREFIX)}")
            continue
        before = len(seen)
        validate_file(p, entity, errs, warns, seen)
        with open(p, encoding="utf-8") as fh:
            counts[entity] = sum(1 for l in fh if l.strip())
    if not os.path.exists(os.path.join(d, "REPORT.md")):
        warns.append("REPORT.md missing")
    print("counts:", json.dumps(counts))
    print(f"{len(errs)} errors, {len(warns)} warnings")
    lim = 40 if quiet else 400
    for e in errs[:lim]:
        print("ERROR", e)
    if not quiet:
        for w in warns[:200]:
            print("WARN ", w)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
