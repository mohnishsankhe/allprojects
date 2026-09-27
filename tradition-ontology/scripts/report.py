#!/usr/bin/env python3
"""Build report tables from data/ (used for MORNING_REPORT.md, wave reports and MAP_OF_THE_ONE_TRUTH.md).

    python3 scripts/report.py tables  > reports_tmp.md   # prints all tables as markdown
    python3 scripts/report.py coverage                    # coverage-gap check against config/coverage_map.md

Tables: counts by type x level; the ultimate as each tradition names it; path-map correspondence by band;
obstacle correspondence (equivalence clusters); most convergent practices (per practice and per equivalence cluster);
the most important open queue items; sourcing results; coverage gaps.
"""
import json, os, re, sys, unicodedata
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
BANDS = [("B0", "entry, turning, faith, qualification, preliminaries"), ("B1", "ethical foundation, purification"),
         ("B2", "preparatory discipline"), ("B3", "withdrawal, one-pointed concentration"), ("B4", "absorption with support"),
         ("B5", "first direct seeing / recognition"), ("B6", "cultivation after seeing"), ("B7", "final liberation"),
         ("B8", "activity after liberation")]


def load(n):
    p = os.path.join(DATA, f"{n}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def lvl(o):
    v = o.get("verification") or {}
    return v.get("level", "skeleton") + (" [unverified]" if v.get("unverified") else "")


def cell(s, n=160):
    return (s or "").replace("|", "/").replace("\n", " ")[:n]


def name_of(eid, idx):
    return idx.get(eid, eid.split(":", 1)[-1] if isinstance(eid, str) else str(eid))


def clusters(items):
    """Connected components over equivalents (exact/partial/same-under-standpoint)."""
    ids = {o["id"] for o in items}
    par = {i: i for i in ids}

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for o in items:
        for e in o.get("equivalents") or []:
            if isinstance(e, dict) and e.get("target") in ids and e.get("grade") in ("exact", "partial", "same-under-standpoint"):
                a, b = find(o["id"]), find(e["target"])
                if a != b:
                    par[a] = b
    comp = defaultdict(list)
    for i in ids:
        comp[find(i)].append(i)
    return list(comp.values())


def tables():
    lineages = {o["id"]: o for o in load("lineages")}
    lname = {k: v.get("name", k) for k, v in lineages.items()}
    st = json.load(open(os.path.join(DATA, "reports", "stats.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "reports", "stats.json")) else {}
    out = []
    # 1 counts
    out.append("### 1. What exists — counts by type and verification level\n")
    out.append(open(os.path.join(DATA, "reports", "stats.md"), encoding="utf-8").read().split("\n", 2)[-1] if os.path.exists(os.path.join(DATA, "reports", "stats.md")) else "_no data yet_")
    # 2 ultimate
    ult = json.load(open(os.path.join(DATA, "ultimate.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "ultimate.json")) else {"views": []}
    out.append("\n### 2. The Map of the One Truth — the ultimate as each tradition names and describes it\n")
    out.append("| lineage | names | description | negations | self | world | personal? | caveat (the tradition's own objection) | level |\n|---|---|---|---|---|---|---|---|---|")
    fam_order = {"vedic": 0, "shared": 1, "ascetic": 2}
    for v in sorted(ult.get("views", []), key=lambda v: (fam_order.get((lineages.get(v.get("lineage")) or {}).get("family"), 3), v.get("lineage") or "")):
        names = ", ".join(x.get("name", "") if isinstance(x, dict) else str(x) for x in v.get("names") or [])
        out.append(f"| {cell(name_of(v.get('lineage'), lname), 40)} | {cell(names, 90)} | {cell('; '.join(v.get('descriptions') or []), 150)} | {cell('; '.join(v.get('negations') or []), 90)} | {cell(v.get('relation_to_self'), 90)} | {cell(v.get('relation_to_world'), 90)} | {v.get('personal_or_impersonal','')} | {cell(v.get('caveat'), 120)} | {lvl(v)} |")
    # 3 path maps
    paths = load("paths")
    out.append("\n### 3. Path-map correspondence — every map aligned stage by stage (bands are interpretive)\n")
    out.append("| map | " + " | ".join(f"{b} {d.split(',')[0]}" for b, d in BANDS) + " | level |\n|---|" + "---|" * (len(BANDS) + 1))
    for p in sorted(paths, key=lambda p: p.get("name", "")):
        byb = defaultdict(list)
        for s in p.get("stages") or []:
            if isinstance(s, dict):
                byb[s.get("band") or "?"].append(s.get("name", ""))
        out.append(f"| {cell(p.get('name'), 60)} | " + " | ".join(cell(", ".join(byb.get(b, [])), 90) for b, _ in BANDS) + f" | {lvl(p)} |")
    # 4 obstacles
    obs = load("obstacles")
    out.append("\n### 4. Obstacle correspondence — kleśas, hindrances, fetters, passions, guṇas and every other diagnosis, aligned by equivalence clusters\n")
    comps = sorted(clusters(obs), key=len, reverse=True)
    oidx = {o["id"]: o for o in obs}
    out.append("| cluster | members (lineage: name) | lineages | levels |\n|---|---|---|---|")
    for i, c in enumerate(comps[:60], 1):
        if len(c) < 2:
            continue
        mem = []
        lins = set()
        for x in c:
            o = oidx[x]
            ls = o.get("lineages") or []
            lins |= set(ls)
            mem.append(f"{name_of(ls[0], lname) if ls else '?'}: {o.get('name')}")
        out.append(f"| {i} | {cell('; '.join(mem), 600)} | {len(lins)} | {cell(', '.join(sorted(Counter(lvl(oidx[x]) for x in c))), 60)} |")
    singles = [oidx[c[0]] for c in comps if len(c) == 1]
    out.append(f"\n_{len(singles)} further obstacles are not yet linked by any equivalence (listed in ATLAS/obstacles)._")
    # 5 practices
    prc = load("practices")
    out.append("\n### 5. The thirty most convergent practices\n")
    out.append("By independent lineages teaching the practice as named, and (second table) by equivalence cluster.\n")
    out.append("| practice | independent lineages | lineages | level |\n|---|---|---|---|")
    for p in sorted(prc, key=lambda p: -(p.get("convergence") or {}).get("count", 0))[:30]:
        cv = p.get("convergence") or {}
        out.append(f"| {cell(p.get('name'), 60)} | {cv.get('count', 0)} | {cell(', '.join(name_of(l, lname) for l in cv.get('schools') or []), 300)} | {lvl(p)} |")
    pidx = {p["id"]: p for p in prc}
    rows = []
    for c in clusters(prc):
        if len(c) < 2:
            continue
        schools, names = set(), []
        for x in c:
            cv = pidx[x].get("convergence") or {}
            schools |= set(cv.get("schools") or [])
            names.append(pidx[x].get("name"))
        rows.append((len(schools), names, schools))
    rows.sort(key=lambda r: -r[0])
    out.append("\n| practice family (equivalence cluster) | independent lineages | lineages |\n|---|---|---|")
    for n, names, schools in rows[:30]:
        out.append(f"| {cell('; '.join(names), 200)} | {n} | {cell(', '.join(name_of(l, lname) for l in sorted(schools)), 300)} |")
    # 6 queue
    dsp = load("disputes")
    q = [d for d in dsp if (d.get("reconciliation") or {}).get("status") == "queued"]
    def imp(d):
        return (0 if d.get("coverage_ref", "").startswith("G") or d["id"] in REG_G else 1, -len(d.get("sides") or []))
    out.append(f"\n### 6. The most important open items in the reconciliation queue ({len(q)} queued in total)\n")
    for d in sorted(q, key=imp)[:20]:
        sides = "; ".join(f"{name_of(s.get('lineage'), lname)}: {cell(s.get('position'), 110)}" for s in d.get("sides") or [] if isinstance(s, dict))
        out.append(f"- **{d.get('queue_ref', '')} {d.get('question')}** — {sides}")
    rec = [d for d in dsp if (d.get("reconciliation") or {}).get("status") in ("reconciled", "partially-reconciled")]
    out.append(f"\n_{len(rec)} disputes reconciled or partially reconciled; {len(dsp)} recorded in total._")
    # 7 sourcing
    out.append("\n### 7. Hallucination sweep\n")
    chk = st.get("sourcing_checks", {})
    out.append(f"Checks applied: {sum(chk.values()) if chk else 0} — " + ", ".join(f"{k}: {v}" for k, v in chk.items()))
    return "\n".join(out)


REG_G = {"dsp:is-there-a-self", "dsp:causation", "dsp:world-real-or-appearance", "dsp:souls-one-or-distinct",
         "dsp:advaita-crypto-buddhism", "dsp:sudden-or-gradual", "dsp:rangtong-shentong", "dsp:prasangika-svatantrika",
         "dsp:works-knowledge-grace", "dsp:isvara", "dsp:status-of-veda", "dsp:women-caste-liberation",
         "dsp:saguna-nirguna", "dsp:kundalini-effort-grace", "dsp:number-of-pramanas"}


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn").lower()
    s = s.replace("upanishad", "upanisad").replace("sh", "s")
    return re.sub(r"[^a-z0-9]+", "", s)


def coverage():
    """Crude check: named items in the coverage map (diacritic-bearing or capitalized words/phrases) not found in any entry name."""
    cm = open(os.path.join(ROOT, "config", "coverage_map.md"), encoding="utf-8").read()
    names = set()
    for ent in ("sources", "lineages", "teachers", "terms", "concepts", "practices", "obstacles", "paths", "disputes"):
        for o in load(ent):
            for k in ("title", "name", "term", "question"):
                if o.get(k):
                    names.add(norm(str(o[k])))
            for k in ("alt_titles", "alt_names"):
                for a in o.get(k) or []:
                    names.add(norm(str(a)))
            names.add(norm(o["id"].split(":", 1)[1]))
    blob = " ".join(names)
    cands = set()
    for m in re.finditer(r"\b([A-ZĀĪŪṚṜḶṄÑṬḌṆŚṢ][\wāīūṛṝḷṅñṭḍṇśṣṃḥ'’\-]+(?:\s+[A-ZĀĪŪṚṜḶṄÑṬḌṆŚṢ][\wāīūṛṝḷṅñṭḍṇśṣṃḥ'’\-]+)*)", cm):
        c = m.group(1)
        if len(c) > 3 and not c.startswith(("Part", "Record", "Texts", "Concepts", "Teachers", "Later", "Key", "Sects", "Canon", "Songs", "Tantras", "Sūtras", "The ", "Their", "Treat", "This", "Capture", "Recent", "Also", "Every")):
            cands.add(c)
    missing = sorted(c for c in cands if norm(c) and norm(c) not in blob)
    print(f"{len(cands)} candidate names in the coverage map; {len(missing)} not found in any entry name/title/alt:")
    for c in missing:
        print("-", c)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "coverage":
        coverage()
    else:
        print(tables())
