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
    """Normalize IAST / Harvard-Kyoto / ITRANS / plain spellings to a crude comparable key (CJK characters are kept)."""
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
    s = re.sub(r"[^a-z0-9\u3400-\u9fff\uf900-\ufaff]+", " ", s).strip()
    s = re.sub(r"([\u3400-\u9fff\uf900-\ufaff])", r"\1 ", s).strip()  # CJK: one token per character
    return re.sub(r"\s+", " ", s)


def iast_of(s):
    try:
        from indic_transliteration import sanscript
        return sanscript.transliterate(s, sanscript.DEVANAGARI, sanscript.IAST)
    except Exception:
        return ""


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
            m = re.search(r'<title level="m"[^>]*>([^<]+)</title>', head)
            no = re.search(r"No\. (\w+)", head)
            t = ((m.group(1) if m else os.path.basename(f)) + (f" T{no.group(1)}" if no else "")).strip()
        except Exception:
            t = os.path.basename(f)
        rows.append({"coll": "CBETA", "key": os.path.basename(f)[:-4], "title": t, "path": os.path.relpath(f, ROOT)})
    # Tibetan canon (Esukhia digital Derge Kangyur/Tengyur): Tōhoku number, Sanskrit title (as transliterated in Tibetan
    # script, converted to Wylie) and Tibetan title (Wylie). Built by the orchestrator into sources_raw/tibetan_canon_titles.json.
    tpath = os.path.join(RAW, "tibetan_canon_titles.json")
    if os.path.exists(tpath):
        try:
            import pyewts
            conv = pyewts.pyewts().toWylie
        except Exception:
            conv = lambda x: x
        for o in json.load(open(tpath, encoding="utf-8")):
            skt, tib = conv(o.get("skt", "")).replace("_", " "), conv(o.get("tib", "")).replace("_", " ")
            rows.append({"coll": "Derge-" + ("Tengyur" if "tengyur" in o["coll"] else "Kangyur"), "key": o["toh"],
                         "title": (skt + " | " + tib).strip(" |"), "path": os.path.relpath(os.path.join(RAW, o["file"]), ROOT)})
    # Digambara Jain root texts in the nikkyjain.github.io repository (directory names: "<title>--<author>")
    nj = os.path.join(RAW, "nikkyjain")
    if os.path.isdir(os.path.join(nj, ".git")):
        import subprocess
        try:
            out = subprocess.run(["git", "-C", nj, "-c", "core.quotepath=off", "ls-tree", "-d", "-r", "--name-only", "HEAD", "jainDataBase/shastra"],
                                 capture_output=True, text=True, timeout=60).stdout.split("\n")
        except Exception:
            out = []
        for d in out:
            parts = d.split("/")
            if len(parts) == 4 and re.match(r"\d\d_", parts[3]):
                name = parts[3][3:]
                title, _, author = name.partition("--")
                t = title.replace("-", " ")
                rows.append({"coll": "JainDB", "key": name, "title": t + " " + iast_of(t) + (" | " + author.replace("-", " ") + " " + iast_of(author.replace("-", " ")) if author else ""),
                             "path": os.path.relpath(os.path.join(nj, d), ROOT), "context": parts[2]})
    # OpenPecha-Data repositories P000001-P001200 (README titles probed by the orchestrator into sources_raw/openpecha_titles_P.tsv):
    # Tibetan-authored works outside the Kangyur/Tengyur (Kagyu, Nyingma, Sakya, Kadam/lojong ...). Tibetan converted to Wylie.
    opath = os.path.join(RAW, "openpecha_titles_P.tsv")
    if os.path.exists(opath):
        try:
            import pyewts
            conv = pyewts.pyewts().toWylie
        except Exception:
            conv = lambda x: x
        for ln in open(opath, encoding="utf-8"):
            parts = ln.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            fields = [f.strip() for f in parts[2].split("|") if f.strip()]
            fields = [f for f in fields if not re.search(r"https?://|^\[|^---|^None$|^Missing$|^test", f, re.I)]
            if not fields:
                continue
            txt = " | ".join(conv(f).replace("_", " ") if re.search(r"[\u0f00-\u0fff]", f) else f for f in fields[:5])
            rows.append({"coll": "OpenPecha", "key": parts[0], "title": txt[:400],
                         "path": "https://github.com/OpenPecha-Data/" + parts[0]})
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
