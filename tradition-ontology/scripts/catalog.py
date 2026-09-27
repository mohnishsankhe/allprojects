#!/usr/bin/env python3
"""Local catalogue of the downloaded text corpora (sources_raw/), for existence checks in the hallucination sweep.

    python3 scripts/catalog.py build                 # (re)build sources_raw/catalog_index.jsonl
    python3 scripts/catalog.py search "Spandakarika"  # fuzzy title search; prints best matches with evidence strings
    python3 scripts/catalog.py sutta mn10             # SuttaCentral id -> Pali title (bilara-data)

Evidence strings look like  catalog:GRETIL:sa_vijJAnabhairava  or  catalog:SC:mn10 "Satipaṭṭhānasutta".
A catalogue hit confirms that a text of that title is extant and digitized; it does NOT confirm author or date.
"""
import glob, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "sources_raw")
INDEX = os.path.join(RAW, "catalog_index.jsonl")


def norm(s):
    """Normalize IAST / Harvard-Kyoto / ITRANS / plain spellings to a crude comparable key."""
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    # HK/ITRANS capitals before lowercasing
    rep = [("aa", "a"), ("ii", "i"), ("uu", "u"), ("Sh", "s"), ("sh", "s"), ("z", "s"), ("S", "s"), ("R", "r"), ("RRi", "r"),
           ("A", "a"), ("I", "i"), ("U", "u"), ("M", "m"), ("H", "h"), ("N", "n"), ("J", "n"), ("G", "n"), ("T", "t"),
           ("D", "d"), ("x", "ks"), ("Ch", "c"), ("ch", "c"), ("C", "c"), ("w", "v"), ("~n", "n")]
    for a, b in rep:
        s = s.replace(a, b)
    s = s.lower()
    s = re.sub(r"(upanishad|upanisat|upanisad|upanishat)", "upanisad", s)
    s = re.sub(r"[^a-z0-9]+", " ", s).strip()
    return s


def build():
    rows = []
    for f in glob.glob(os.path.join(RAW, "dcs", "corpus", "GRETIL", "sa_*.txt")):
        b = os.path.basename(f)[3:-4]
        rows.append({"coll": "GRETIL", "key": b, "title": b.replace("-", " "), "path": os.path.relpath(f, ROOT)})
    for d in glob.glob(os.path.join(RAW, "dcs", "dcs", "data", "conllu", "files", "*")):
        if os.path.isdir(d):
            b = os.path.basename(d)
            rows.append({"coll": "DCS", "key": b, "title": b, "path": os.path.relpath(d, ROOT)})
    for f in glob.glob(os.path.join(RAW, "raw_etexts", "**", "*.*"), recursive=True):
        if not re.search(r"\.(md|txt|html?|itx)$", f) or os.path.basename(f).startswith("_index"):
            continue
        rel = os.path.relpath(f, os.path.join(RAW, "raw_etexts"))
        coll = "raw_etexts"
        if "/gretil_devanAgarI/" in "/" + rel:
            coll = "GRETIL-dev"
        elif rel.startswith("mixed/mukta/"):
            coll = "Muktabodha"
        elif rel.startswith("mixed/ebhAratI-sampat/"):
            coll = "eBharati"
        title = os.path.splitext(os.path.basename(f))[0]
        rows.append({"coll": coll, "key": title, "title": title.replace("_", " "), "path": os.path.relpath(f, ROOT),
                     "context": " ".join(rel.split("/")[:-1])[-160:]})
    # SuttaCentral: sutta ids + titles from bilara-data root files (segment ":0.2" or ":0.3" holds the title)
    for f in glob.glob(os.path.join(RAW, "bilara-data", "root", "pli", "ms", "sutta", "**", "*_root-pli-ms.json"), recursive=True):
        sid = os.path.basename(f).split("_")[0]
        try:
            j = json.load(open(f, encoding="utf-8"))
            heads = [v for k, v in j.items() if re.search(r":0\.\d+$", k)]
            title = heads[-1].strip() if heads else sid
        except Exception:
            title = sid
        rows.append({"coll": "SC", "key": sid, "title": title, "path": os.path.relpath(f, ROOT), "context": " ".join(heads[:-1])[:120] if 'heads' in dir() else ""})
    for f in glob.glob(os.path.join(RAW, "cbeta", "T", "**", "*.xml"), recursive=True):
        try:
            head = open(f, encoding="utf-8").read(4000)
            m = re.search(r"<title[^>]*>([^<]+)</title>", head)
            t = m.group(1) if m else os.path.basename(f)
        except Exception:
            t = os.path.basename(f)
        rows.append({"coll": "CBETA", "key": os.path.basename(f)[:-4], "title": t, "path": os.path.relpath(f, ROOT)})
    with open(INDEX, "w", encoding="utf-8") as fh:
        for r in rows:
            r["n"] = norm(r["title"] + " " + r.get("context", ""))
            r["nk"] = norm(r["key"])
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("indexed", len(rows), "items ->", os.path.relpath(INDEX, ROOT))


def load():
    if not os.path.exists(INDEX):
        build()
    return [json.loads(l) for l in open(INDEX, encoding="utf-8")]


def search(q, k=12):
    rows = load()
    nq = norm(q)
    toks = [t for t in nq.split() if len(t) > 2]
    squash = nq.replace(" ", "")
    scored = []
    for r in rows:
        hay = r["n"] + " " + r["nk"]
        hs = hay.replace(" ", "")
        s = 0
        if squash and squash in hs:
            s += 10
        s += sum(2 for t in toks if t in hs)
        if s:
            scored.append((s, r))
    scored.sort(key=lambda x: (-x[0], len(x[1]["n"])))
    for s, r in scored[:k]:
        print(f"{s:>3}  catalog:{r['coll']}:{r['key']}  \"{r['title'][:90]}\"  {r['path'][:120]}")
    if not scored:
        print("no catalogue match for", repr(q))


def sutta(sid):
    for r in load():
        if r["coll"] == "SC" and r["key"] == sid:
            print(f"catalog:SC:{sid} \"{r['title']}\" {r['path']}")
            return
    print("not found:", sid)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
    elif sys.argv[1] == "build":
        build()
    elif sys.argv[1] == "search":
        search(" ".join(sys.argv[2:]))
    elif sys.argv[1] == "sutta":
        sutta(sys.argv[2])
