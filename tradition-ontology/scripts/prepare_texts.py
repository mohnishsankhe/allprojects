#!/usr/bin/env python3
"""Prepare verse-level segments of root texts for extraction (Phase D and waves).

    python3 scripts/prepare_texts.py bhagavad-gita
    python3 scripts/prepare_texts.py list

Writes sources_raw/prepared/<source-slug>/segments.jsonl  (git-ignored: full texts are never committed)
       sources_raw/prepared/<source-slug>/META.json       (edition, licence, counts, chunk plan)
Each segment: {"ref": "2.47", "chapter": "2", "verse": "47", "deva": "...", "iast": "...", "speaker": "..."}
"""
import json, os, re, sys
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "sources_raw")
OUT = os.path.join(RAW, "prepared")


def iast(s):
    return transliterate(s, sanscript.DEVANAGARI, sanscript.IAST)


def write(slug, segs, meta):
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, "segments.jsonl"), "w", encoding="utf-8") as fh:
        for s in segs:
            fh.write(json.dumps(s, ensure_ascii=False) + "\n")
    meta["segments"] = len(segs)
    json.dump(meta, open(os.path.join(d, "META.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(slug, len(segs), "segments")


def bhagavad_gita():
    verses = json.load(open(os.path.join(RAW, "gita", "data", "verse.json"), encoding="utf-8"))
    segs = []
    for v in sorted(verses, key=lambda x: (x["chapter_number"], x["verse_number"])):
        txt = v["text"].strip()
        speaker = None
        m = re.match(r"^\s*([^\n।]+?उवाच)\s*\n", txt)
        if m:
            speaker = iast(m.group(1).strip())
            txt = txt[m.end():]
        txt = re.sub(r"।।\s*[\d\.]+\s*।।", "", txt)
        txt = re.sub(r"\n\s*\n", "\n", txt).strip()
        ref = f"{v['chapter_number']}.{v['verse_number']}"
        segs.append({"ref": ref, "chapter": str(v["chapter_number"]), "verse": str(v["verse_number"]),
                     "deva": txt, "iast": iast(txt), "speaker": speaker})
    meta = {"source": "src:bhagavad-gita", "edition": "Sanskrit text from github.com/gita/gita data/verse.json (vulgate; 701 entries incl. the extra verse at the start of ch. 13 found in some editions)",
            "licence": "Sanskrit root text: public domain. The repository is released under the Unlicense; its bundled modern translations/commentaries are third-party works and are NOT used or stored here.",
            "transliteration": "IAST generated with indic_transliteration from the Devanāgarī",
            "chunks": [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["10", "11", "12"], ["13", "14", "15"], ["16", "17", "18"]],
            "pd_translation_for_cross_check": "K. T. Telang, SBE vol. 8 (1882) — not available offline here; paraphrases are made directly from the Sanskrit"}
    write("bhagavad-gita", segs, meta)


def yoga_sutra():
    f = os.path.join(RAW, "dcs", "corpus", "GRETIL", "sa_pataJjali-yogasUtra-with-bhASya.txt")
    lines = open(f, encoding="utf-8", errors="replace").read().split("\n")
    segs, cur = [], None
    for ln in lines:
        m = re.match(r"^\|\|mula:(.*?)//\s*(\d+)\.(\d+)\s*//\s*(.*)$", ln.strip())
        m2 = None if m else re.match(r"^(.*?)---\s*(.*?)//\s*(\d+)\.(\d+)\s*//\s*$", ln.strip())
        if m or m2:
            if cur:
                segs.append(cur)
            if m:
                sutra, c, v, rest, pre = m.group(1), m.group(2), m.group(3), m.group(4), ""
            else:
                pre, sutra, c, v, rest = m2.group(1), m2.group(2), m2.group(3), m2.group(4), ""
            if pre.strip() and cur is not None:
                segs[-1]["commentary_iast"].append(pre.strip() + " ---")
            cur = {"ref": f"{c}.{v}", "chapter": c, "verse": v,
                   "iast": sutra.strip(), "commentary_iast": [rest.strip()] if rest.strip() else [], "commentary_source": "src:yoga-bhasya"}
            continue
        if cur is not None and ln.strip():
            if re.match(r"^\s*\d+\.\d+\s*$", ln.strip()):
                continue
            cur["commentary_iast"].append(ln.strip())
    if cur:
        segs.append(cur)
    for sg in segs:
        sg["commentary_iast"] = "\n".join(sg["commentary_iast"])
    meta = {"source": "src:yoga-sutra", "commentary_source": "src:yoga-bhasya",
            "edition": "GRETIL e-text 'pataJjali-yogasUtra-with-bhASya' (data entry Philipp A. Maas; based on K. Ś. Āgāśe's Ānandāśrama edition, 1904). The file header mislabels the text as Bhoja's Rājamārtaṇḍa; its content is the sūtras with Vyāsa's Yogabhāṣya.",
            "licence": "Root text public domain; GRETIL e-text CC BY-NC-SA 4.0 — verse-level quotations stored with attribution; commentary text not stored in committed data",
            "chunks": [["1"], ["2"], ["3"], ["4"]],
            "pd_translation_for_cross_check": "J. H. Woods, The Yoga-System of Patañjali (HOS 17, 1914) — not available offline here"}
    write("yoga-sutra", segs, meta)


def _bilara(uid):
    import glob as _g
    base = os.path.join(RAW, "bilara-data")
    rf = _g.glob(os.path.join(base, "root", "pli", "ms", "sutta", "**", f"{uid}_root-pli-ms.json"), recursive=True)
    tf = _g.glob(os.path.join(base, "translation", "en", "sujato", "sutta", "**", f"{uid}_translation-en-sujato.json"), recursive=True)
    root = json.load(open(rf[0], encoding="utf-8")) if rf else {}
    tr = json.load(open(tf[0], encoding="utf-8")) if tf else {}
    return root, tr


def pali_sutta(uid, slug, source_id, group="section"):
    """Group bilara segments into units: prose suttas by section number (mn10:3.x -> 3); verse texts by verse."""
    root, tr = _bilara(uid)
    units, order = {}, []
    for k, v in root.items():
        key = k.split(":", 1)[1]
        sec = key.split(".")[0]
        if sec == "0":
            continue
        if sec not in units:
            units[sec] = {"pli": [], "en": [], "segments": []}
            order.append(sec)
        units[sec]["pli"].append(v.strip())
        units[sec]["en"].append((tr.get(k) or "").strip())
        units[sec]["segments"].append(k)
    segs = []
    for sec in order:
        u = units[sec]
        segs.append({"ref": f"{uid}:{sec}", "chapter": uid, "verse": sec, "pali": " ".join(u["pli"]),
                     "en_sujato": " ".join(u["en"]), "segments": [u["segments"][0], u["segments"][-1]]})
    title = root.get(f"{uid}:0.2", "") or root.get(f"{uid}:0.1", "")
    return segs, title


def pali_suttas():
    for uid, slug, sid in [("dn22", "mahasatipatthana-sutta", "src:mahasatipatthana-sutta"),
                           ("mn10", "satipatthana-sutta", "src:satipatthana-sutta"),
                           ("mn118", "anapanasati-sutta", "src:anapanasati-sutta"),
                           ("sn56.11", "dhammacakkappavattana-sutta", "src:dhammacakkappavattana-sutta")]:
        segs, title = pali_sutta(uid, slug, sid)
        meta = {"source": sid, "title_in_edition": title,
                "edition": "SuttaCentral bilara-data, Pali root text (Mahāsaṅgīti edition, 'ms'), with Bhikkhu Sujato's English translation",
                "licence": "CC0 (root text and Sujato translation, per SuttaCentral) — may be stored in full",
                "unit": "one unit per SuttaCentral section number (e.g. mn10:3 = segments mn10:3.1…)",
                "chunks": [["all"]]}
        write(slug, segs, meta)
    # Dhammapada: one unit per verse
    import glob as _g
    base = os.path.join(RAW, "bilara-data")
    segs = []
    files = sorted(_g.glob(os.path.join(base, "root", "pli", "ms", "sutta", "kn", "dhp", "*_root-pli-ms.json")),
                   key=lambda f: int(re.search(r"dhp(\d+)", f).group(1)))
    for f in files:
        uidv = os.path.basename(f).split("_")[0]
        root = json.load(open(f, encoding="utf-8"))
        tf = _g.glob(os.path.join(base, "translation", "en", "sujato", "sutta", "kn", "dhp", f"{uidv}_translation-en-sujato.json"))
        tr = json.load(open(tf[0], encoding="utf-8")) if tf else {}
        byv = {}
        vag = root.get(f"{uidv}:0.2", "")
        for k, v in root.items():
            vs = k.split(":")[0]  # e.g. dhp1
            m = re.match(r"dhp(\d+)", vs)
            loc = k.split(":")[1]
            if loc.startswith("0."):
                continue
            n = m.group(1)
            byv.setdefault(n, {"pli": [], "en": [], "vagga": vag})
            byv[n]["pli"].append(v.strip())
            byv[n]["en"].append((tr.get(k) or "").strip())
        for n in sorted(byv, key=int):
            b = byv[n]
            segs.append({"ref": n, "chapter": b["vagga"], "verse": n, "pali": " ".join(b["pli"]), "en_sujato": " ".join(b["en"])})
    meta = {"source": "src:dhammapada", "edition": "SuttaCentral bilara-data (Mahāsaṅgīti Pali) with Bhikkhu Sujato's translation",
            "licence": "CC0", "chunks": [["1-100"], ["101-255"], ["256-423"]]}
    write("dhammapada", segs, meta)


DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
ORDINALS = [("प्रथम", 1), ("द्वितीय", 2), ("तृतीय", 3), ("चतुर्थ", 4), ("पञ्चम", 5), ("षष्ठ", 6), ("सप्तम", 7), ("अष्टम", 8), ("नवम", 9), ("दशम", 10)]


def sharada_parse(fname):
    """Parse an advaita-shAradA mUla file: '#' = part, '##' = section; verses end with ॥ N ॥ (markers may wrap lines)."""
    f = os.path.join(RAW, "raw_etexts", "vedAntam", "advaitam", "advaita-shAradA", "mUla", fname)
    lines = open(f, encoding="utf-8").read().split("\n")
    state = {"l1": 0, "l2": 0, "implicit": 1 if fname in ("svt.md",) else 0}
    segs, heads, buf = [], {}, []
    marker = re.compile(r"॥\s*([०-९0-9]+)\s*॥")

    colophon = re.compile(r"इ[तद]ि?\s*\S*(भाष्य|खण्ड|वल्ली|अध्याय|प्रपाठक|उपनिष)\S*[^॥]*॥|इत्य\S*भाष्य\S*[^॥]*॥|इति\s+श्रीमत्[^॥]*॥")
    invoc = re.compile(r"^(.{0,600}?ॐ\s*शान्तिः\s*शान्तिः\s*शान्तिः\s*॥)")

    def flush():
        text = " ".join(x.strip() for x in buf if x.strip() and x.strip() != "**")
        buf.clear()
        text = colophon.sub(" ", text).strip()
        inv = None
        mi = invoc.match(text)
        # split off a śānti invocation only when real text follows it (in TU 1.1 the invocation IS the section's text)
        if mi and not marker.search(mi.group(1)) and re.sub(r"[\s॥।०-९0-9]", "", text[mi.end():]):
            inv, text = mi.group(1).strip(), text[mi.end():].strip()
        pos = 0
        if text and not marker.search(text):
            # a section whose text carries no verse number (e.g. TU 3.8, 3.9): keep it as verse 1 of the section
            text = text.rstrip("। ॥") + " ॥ १ ॥"
            state["_unnumbered"] = True
        for m in marker.finditer(text):
            chunk = text[pos:m.start()].strip()
            pos = m.end()
            n = m.group(1).translate(DEV_DIGITS)
            if state["l1"] == 0 and n == "1" and segs and segs[-1].get("_top") == state["implicit"]:
                state["implicit"] += 1
            top = state["l1"] or state["implicit"]
            base = [str(x) for x in (top, state["l2"]) if x]
            chap = ".".join(base) or "1"
            key = (chap,)
            if n == "1" and any(sg["chapter"] == chap and sg["verse"] == "1" for sg in segs[-80:]):
                prev = [int(sg["verse"]) for sg in segs if sg["chapter"] == chap and sg["verse"].isdigit()]
                state.setdefault("subrun", {})[key] = str(max(prev) + 1 if prev else 1)
            sub = state.get("subrun", {}).get(key)
            parts = base + ([sub, n] if sub else [n])
            sg = {"ref": ".".join(parts), "chapter": chap, "verse": (sub + "." + n) if sub else n,
                  "deva": chunk, "iast": iast(chunk), "_top": top}
            if inv:
                sg["invocation_deva"], sg["invocation_iast"], inv = inv, iast(inv), None
            if state.pop("_unnumbered", False):
                sg["note"] = "the edition prints this section without a verse number; numbered 1 here"
            segs.append(sg)
        tail = text[pos:].strip()
        if tail and segs:
            segs[-1].setdefault("trailing", tail)

    seen_title = False
    for ln in lines:
        st = ln.strip()
        if st.startswith("# ") or st.startswith("## "):
            flush()
            if st.startswith("# "):
                if not seen_title:
                    seen_title = True
                    continue
                h = st[2:].strip()
                num = None
                for w, k in ORDINALS:
                    if h.startswith(w):
                        num = k; break
                state["l1"] = num if num else state["l1"] + 1
                state["l2"] = 0
                heads[str(state["l1"])] = h
            else:
                state["l2"] += 1
                heads[f"{state['l1']}.{state['l2']}"] = st[3:].strip()
            continue
        buf.append(st)
    flush()
    for sg in segs:
        sg.pop("_top", None)
    return segs, heads


UPANISADS = [("Isha.md", "isa-upanisad"), ("Kena_pada.md", "kena-upanisad"), ("Kathaka.md", "katha-upanisad"),
             ("Prashna.md", "prasna-upanisad"), ("Mundaka.md", "mundaka-upanisad"), ("Taitiriya.md", "taittiriya-upanisad"),
             ("Aitareya.md", "aitareya-upanisad"), ("Chandogya.md", "chandogya-upanisad"), ("Brha.md", "brhadaranyaka-upanisad"),
             ("svt.md", "svetasvatara-upanisad"), ("kst.md", "kausitaki-upanisad-sharada")]


def upanisads():
    for fname, slug in UPANISADS:
        segs, heads = sharada_parse(fname)
        meta = {"source": f"src:{slug}", "edition": f"Advaita Śāradā (Śṛṅgeri) mūla text, raw_etexts/vedAntam/advaitam/advaita-shAradA/mUla/{fname} — the text as commented on in the Śaṅkara tradition; traditional numbering (part.section.verse)",
                "licence": "Root text public domain (Vedic); e-text from the Advaita Śāradā project via sanskrit/raw_etexts — verse-level quotations with attribution",
                "headings": heads, "chunks": [["all"]]}
        write(slug, segs, meta)


def mandukya():
    f = os.path.join(RAW, "raw_etexts", "mixed", "gretil_devanAgarI", "1_sanskr", "1_veda", "4_upa", "mandukya-upanisad.md")
    body = open(f, encoding="utf-8").read().split("## पाठः", 1)[1]
    segs, buf = [], []
    for ln in body.split("\n"):
        st = ln.strip()
        if not st:
            continue
        buf.append(st)
        m = re.search(r"॥\s*मन्दुप्_([०-९0-9]+)\s*॥\s*$", st)
        if m:
            n = m.group(1).translate(DEV_DIGITS)
            text = re.sub(r"॥\s*मन्दुप्_[०-९0-9]+\s*॥\s*$", "", " ".join(buf)).strip()
            segs.append({"ref": n, "chapter": "1", "verse": n, "deva": text, "iast": iast(text)})
            buf = []
    write("mandukya-upanisad", segs, {"source": "src:mandukya-upanisad", "edition": "GRETIL e-text (Devanāgarī mirror in sanskrit/raw_etexts)", "licence": "Root text public domain; GRETIL e-text CC BY-NC-SA 4.0 — quotations with attribution", "chunks": [["all"]]})
    g = os.path.join(RAW, "dcs", "corpus", "GRETIL", "sa_mANDUkyopaniSatkArikA.txt")
    segs, buf = [], []
    for ln in open(g, encoding="utf-8"):
        st = ln.strip()
        if not st or st.startswith("#"):
            continue
        buf.append(st)
        m = re.search(r"//\s*(\d+)\.(\d+)\s*//\s*$", st)
        if m:
            text = re.sub(r"//\s*\d+\.\d+\s*//\s*$", "", " ".join(buf)).strip()
            segs.append({"ref": f"{m.group(1)}.{m.group(2)}", "chapter": m.group(1), "verse": m.group(2), "iast": text})
            buf = []
    write("mandukya-karika", segs, {"source": "src:mandukya-karika", "edition": "GRETIL e-text 'mANDUkyopaniSatkArikA' (via the DCS corpus)", "licence": "Root text public domain; GRETIL e-text CC BY-NC-SA 4.0 — quotations with attribution",
                                    "prakaranas": {"1": "Āgama", "2": "Vaitathya", "3": "Advaita", "4": "Alātaśānti"}, "chunks": [["1", "2"], ["3"], ["4"]]})


def dcs_text(title, slug, source_id, chunks, note=""):
    """Reconstruct a text from the DCS CoNLL-U files: one segment per DCS 'chapter' unit (e.g. SāṃKār, 1 = kārikā 1)."""
    import glob as _g
    files = _g.glob(os.path.join(RAW, "dcs", "dcs", "data", "conllu", "files", title, "*.conllu"))
    units = {}
    for f in files:
        chap, sents = None, []
        for ln in open(f, encoding="utf-8"):
            if ln.startswith("## chapter:"):
                chap = ln.split(":", 1)[1].strip()
            elif ln.startswith("# text ="):
                sents.append(ln.split("=", 1)[1].strip())
        if chap:
            units.setdefault(chap, []).extend(sents)
    def key(c):
        nums = re.findall(r"\d+", c)
        return [int(x) for x in nums] or [0]
    segs = []
    for c in sorted(units, key=key):
        ref = ".".join(re.findall(r"\d+", c)) or c
        segs.append({"ref": ref, "chapter": c.split(",")[0], "verse": ref, "iast": " / ".join(units[c]), "dcs_chapter": c})
    write(slug, segs, {"source": source_id, "edition": f"Digital Corpus of Sanskrit (Hellwig), text '{title}' — sentence-split; reconstructed per DCS unit. {note}",
                       "licence": "Root text public domain; DCS data CC BY 4.0 — quotations with attribution", "chunks": chunks})


def gretil_iast_verses(fname, slug, source_id, chunks, marker=r"//\s*(\d+)\s*//"):
    f = os.path.join(RAW, "dcs", "corpus", "GRETIL", fname)
    segs, buf, spk = [], [], None
    for ln in open(f, encoding="utf-8"):
        st = ln.strip()
        if not st or st.startswith("#"):
            continue
        m = re.search(marker, st)
        buf.append(re.sub(marker, "", st).strip())
        if m:
            n = m.group(1)
            segs.append({"ref": n, "chapter": "1", "verse": n, "iast": " ".join(x for x in buf if x)})
            buf = []
    write(slug, segs, {"source": source_id, "edition": f"GRETIL e-text {fname} (via the DCS corpus)", "licence": "Root text public domain; GRETIL CC BY-NC-SA 4.0 — quotations with attribution", "chunks": chunks})


def gretil_dev_marked(relpath, abbr, slug, source_id, chunks):
    """GRETIL Devanāgarī mirror: root lines end with ॥ <abbr>_<a>।<b> ॥ ; commentary lines start with '*'."""
    f = os.path.join(RAW, "raw_etexts", "mixed", "gretil_devanAgarI", "1_sanskr", relpath)
    body = open(f, encoding="utf-8").read().split("## पाठः", 1)[1]
    segs, buf = [], []
    pat = re.compile("॥\\s*" + abbr + "_([०-९0-9]+)[।.]([०-९0-9]+)\\s*(?:\\?+\\s*)?॥")  # '???' = GRETIL editor's doubt mark
    for ln in body.split("\n"):
        st = ln.strip()
        if not st or st.startswith("*") or st.startswith("_"):
            if st.startswith("*"):
                buf = []
            continue
        m = pat.search(st)
        buf.append(pat.sub("", st).strip())
        if m:
            a, b = m.group(1).translate(DEV_DIGITS), m.group(2).translate(DEV_DIGITS)
            text = " ".join(x for x in buf if x and not re.search("उन्मेष|निःष्यन्द", x))
            segs.append({"ref": f"{a}.{b}", "chapter": a, "verse": b, "deva": text, "iast": iast(text)})
            buf = []
    write(slug, segs, {"source": source_id, "edition": f"GRETIL e-text (Devanāgarī mirror) {relpath}", "licence": "Root text public domain; GRETIL CC BY-NC-SA 4.0 — quotations with attribution", "chunks": chunks})


def kashmir_and_samkhya():
    samkhya_karika()
    gretil_iast_verses("sa_vijJAnabhairava.txt", "vijnana-bhairava-tantra", "src:vijnana-bhairava-tantra", [["1-80"], ["81-163"]])
    gretil_dev_marked("4_rellit/saiva/sivasutra_with_vartika.md", "सिव्स्", "siva-sutra", "src:siva-sutra", [["all"]])
    gretil_dev_marked("6_sastra/3_phil/saiva/vasugupta_or_kallata_bhatta_spandakrika.md", "व्स्प्क्", "spanda-karika", "src:spanda-karika", [["all"]])


def samkhya_karika():
    f = os.path.join(RAW, "dcs", "corpus", "GRETIL", "sa_IzvarakRSNa-sAMkhyakArikA-comm3.txt")
    lines = open(f, encoding="utf-8").read().split("\n")
    head = "\n".join(l for l in lines[:20] if l.startswith("#"))
    segs, cur = [], None
    for ln in lines:
        st = ln.strip()
        if st.startswith("||mula:"):
            cur = [st[len("||mula:"):]]
        elif cur is not None:
            cur.append(st)
        if cur is not None:
            m = re.search(r"//\s*(\d+)\s*//\s*$", st)
            if m:
                text = re.sub(r"//\s*\d+\s*//\s*$", "", " ".join(cur)).strip()
                segs.append({"ref": m.group(1), "chapter": "1", "verse": m.group(1), "iast": text})
                cur = None
    write("samkhya-karika", segs, {"source": "src:samkhya-karika", "edition": "GRETIL e-text 'IzvarakRSNa-sAMkhyakArikA-comm3' (root verses marked ||mula) via the DCS corpus. Header: " + head.replace("\n", " | ")[:400],
                                   "licence": "Root text public domain; GRETIL CC BY-NC-SA 4.0 — quotations with attribution", "chunks": [["all"]]})


def deva_reset_parse(path, slug, source_id, edition, chunks, drop_before_first=False):
    """Devanāgarī verses ending with ॥ N ॥ (markers may wrap); a new chapter starts whenever numbering resets to 1."""
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^\+\+\+.*?\+\+\+", "", text, flags=re.S)
    text = re.sub(r"^#+ .*$", " ", text, flags=re.M)
    text = re.sub(r"\s+", " ", text)
    segs, pos, ch, lastn = [], 0, 0, None
    for m in re.finditer(r"॥\s*([०-९0-9]+)\s*॥?", text):
        n = m.group(1).translate(DEV_DIGITS)
        chunk = text[pos:m.start()].strip(" ।॥")
        pos = m.end()
        if n == "1" or ch == 0:
            ch += 1
        if not chunk:
            continue
        segs.append({"ref": f"{ch}.{n}", "chapter": str(ch), "verse": n, "deva": chunk, "iast": iast(chunk)})
    write(slug, segs, {"source": source_id, "edition": edition, "licence": "Root text public domain; e-text via sanskrit/raw_etexts — quotations with attribution", "chunks": chunks})


def hatha_and_gitas():
    R = os.path.join(RAW, "raw_etexts")
    deva_reset_parse(os.path.join(R, "yogaH", "haTha-yoga-pradIpikA", "haTha-yoga-pradIpikA.md"), "hatha-yoga-pradipika",
                     "src:hatha-yoga-pradipika", "sanskrit/raw_etexts yogaH/haTha-yoga-pradIpikA (vulgate, 4 upadeśas)", [["1"], ["2"], ["3"], ["4"]])
    # Aṣṭāvakra/Avadhūta: the eBhāratī files mix commentary with the root text; use the GRETIL Aṣṭāvakra later (TODO).


def dcs_chapters(title, slug, source_id, chunks, note):
    import glob as _g
    files = _g.glob(os.path.join(RAW, "dcs", "dcs", "data", "conllu", "files", title, "*.conllu"))
    units = {}
    for f in files:
        chap, sents = None, []
        for ln in open(f, encoding="utf-8"):
            if ln.startswith("## chapter:"):
                chap = ln.split(":", 1)[1].strip()
            elif ln.startswith("# text ="):
                sents.append(ln.split("=", 1)[1].strip())
        if chap:
            units.setdefault(chap, []).extend(sents)
    segs = []
    for c in sorted(units, key=lambda c: [int(x) for x in re.findall(r"\d+", c)] or [0]):
        n = ".".join(re.findall(r"\d+", c))
        segs.append({"ref": f"ch{n}", "chapter": n, "verse": None, "lines_iast": units[c], "iast": " / ".join(units[c])})
    write(slug, segs, {"source": source_id, "edition": f"Digital Corpus of Sanskrit (Hellwig), text '{title}'", "licence": "Root text public domain; DCS CC BY 4.0 — quotations with attribution",
                       "unit": "one segment per chapter; `lines_iast` are DCS sentences (usually half-verses). The extractor must establish verse numbers by pairing half-verses, cross-checking against its knowledge of the standard numbering, and flag any uncertainty. " + note,
                       "chunks": chunks})


def buddhist_and_advaita_gitas():
    """Verse-level MMK and Aṣṭāvakra Gītā from the GRETIL Devanāgarī mirror (markers ङ्ङ्क्_a।b = MMK_a.b; अव्ग्_a।b = AVG_a.b)."""
    gretil_dev_marked("6_sastra/3_phil/buddh/nagarjuna_mulamadhyamakakarika.md", "ङ्ङ्क्", "mulamadhyamakakarika", "src:mulamadhyamakakarika",
                      [[str(i) for i in range(1, 8)], [str(i) for i in range(8, 16)], [str(i) for i in range(16, 22)], [str(i) for i in range(22, 28)]])
    gretil_dev_marked("4_rellit/vaisn/astavakragita.md", "अव्ग्", "astavakra-gita", "src:astavakra-gita",
                      [[str(i) for i in range(1, 11)], [str(i) for i in range(11, 21)]])


def pratyabhijnahrdaya():
    """Kṣemarāja's Pratyabhijñāhṛdayam (GRETIL Devanāgarī mirror): 20 sūtras ending ॥ N ॥, each followed by his own commentary.
    The sūtra is the paragraph ending with the marker; `commentary_deva` holds the auto-commentary up to the next sūtra."""
    f = os.path.join(RAW, "raw_etexts", "mixed", "gretil_devanAgarI", "1_sanskr", "6_sastra", "3_phil", "saiva", "ksemaraja_pratyabhijnahrdaya.md")
    body = open(f, encoding="utf-8").read().split("## पाठः", 1)[1]
    paras, cur = [], []
    for ln in body.split("\n"):
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            paras.append(" ".join(cur)); cur = []
    if cur:
        paras.append(" ".join(cur))
    pat = re.compile("॥\\s*([०-९]+)\\s*॥\\s*$")
    segs, last = [], None
    intro = []
    for para in paras:
        m = pat.search(para)
        if m and int(m.group(1).translate(DEV_DIGITS)) == (len(segs) + 1):
            n = m.group(1).translate(DEV_DIGITS)
            text = pat.sub("", para).strip()
            # the sūtra is the last sentence of the paragraph (preceding words are commentary lead-in ending with 'आह' etc.)
            parts = re.split(r"(?<=[।॥])\s+|\s+आह\s+", text)
            sutra = parts[-1].strip() if len(parts) > 1 else text
            lead = text[: len(text) - len(sutra)].strip()
            if segs and lead:
                segs[-1]["commentary_deva"] += " " + lead
            elif lead:
                intro.append(lead)
            segs.append({"ref": n, "chapter": None, "verse": n, "deva": sutra, "iast": iast(sutra), "commentary_deva": ""})
        elif segs:
            segs[-1]["commentary_deva"] = (segs[-1]["commentary_deva"] + " " + para).strip()
        else:
            intro.append(para)
    for sg in segs:
        sg["commentary_iast"] = iast(sg["commentary_deva"])
    segs.insert(0, {"ref": "intro", "chapter": None, "verse": None, "deva": " ".join(intro), "iast": iast(" ".join(intro)), "note": "benedictory verses and Kṣemarāja's statement of purpose"})
    write("pratyabhijnahrdaya", segs, {"source": "src:pratyabhijnahrdaya", "edition": "GRETIL e-text (Devanāgarī mirror), encoded by M. Faliero (DSO Sanskrit Archive, 1998), text of the KSTS ed.",
          "licence": "Root text public domain; GRETIL CC BY-NC-SA 4.0 — quotations with attribution",
          "unit": "one segment per sūtra (20) plus 'intro'; each carries Kṣemarāja's own commentary (commentary_deva/_iast). The sūtra boundary is heuristic: the extractor must check that `deva` is exactly the sūtra and move stray lead-in words to the commentary.",
          "chunks": [["intro", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"], ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]]})


def avadhuta_gita():
    """Avadhūta Gītā from the eBhāratī copy of the 1917 Khemrāj (Veṅkaṭeśvara Press) edition with Hindi commentary:
    the root verse is the run of bold blocks immediately before each 'पदच्छेदः' header; its number is the printed ॥N॥
    (numbering restarts in each chapter) or, where the print omits it, the previous number + 1 (flagged)."""
    f = os.path.join(RAW, "raw_etexts", "mixed", "ebhAratI-sampat", "gItAH", "anyagItA", "dattAtreyaH", "avadhUtagItA.md")
    txt = open(f, encoding="utf-8").read()
    txt = txt[txt.index("अथावधूतगीता"):]
    blocks = [x.strip() for x in re.split(r"\n\s*\n", txt)]
    segs, chap, prev = [], 1, 0
    vpat = re.compile(r"॥\s*([०-९0-9]+)\s*॥")
    hdr = re.compile(r"^\*+\s*(पदच्छेद|पदार्थ|भावार्थ|अन्वय|इति|अथ)")
    for i, b in enumerate(blocks):
        if not re.match(r"^\*+\s*पदच्छेद", b):
            continue
        j, run = i - 1, []
        while j >= 0 and blocks[j].startswith("**") and not hdr.match(blocks[j]) and "MISSING_FIG" not in blocks[j]:
            run.insert(0, blocks[j]); j -= 1
        if not run:
            continue
        run = [r for r in run if not re.search(r"हैं|है।|है॥|कहते|जी |कहा |करके|अर्थात्", r)]  # drop bold Hindi commentary
        if not run:
            continue
        raw = re.sub(r"\*", "", "\n".join(run)).strip()
        m = re.search(r"(?:॥|\|)*\s*([०-९0-9]+)\s*(?:॥|\|)*\s*$", raw)
        flag = None
        if m:
            n = int(m.group(1).translate(DEV_DIGITS))
            if n == 1 and prev >= 1:
                chap += 1
        else:
            n, flag = prev + 1, "verse number not printed in the edition; inferred as previous + 1"
        prev = n
        text = re.sub(r"<[^>]+>|\\", "", raw[: m.start()] if m else raw).strip()
        text = " ".join(t.strip() for t in text.split("\n") if t.strip())
        sg = {"ref": f"{chap}.{n}", "chapter": str(chap), "verse": str(n), "deva": text, "iast": iast(text)}
        if flag:
            sg["note"] = flag
        segs.append(sg)
    write("avadhuta-gita", segs, {"source": "src:avadhuta-gita", "edition": "Avadhūtagītā with Hindi bhāṣāṭīkā by Svāmī Paramānanda, Khemrāj Śrīkṛṣṇadās (Veṅkaṭeśvara Steam Press), Bombay 1917 — eBhāratī-sampat e-text (Ebharati-6665); only the Sanskrit root verses are used",
          "licence": "Root text public domain; 1917 edition public domain; the Hindi commentary is not used",
          "unit": "one segment per verse; chapter numbers inferred from the verse numbering restarting at 1 (check against the chapter colophons).",
          "chunks": [["1", "2", "3"], ["4", "5", "6", "7", "8"]]})


def cbeta_text(tno, slug, source_id, edition_note):
    """CBETA TEI P5: segment by paragraph (<p>/<lg>) within <cb:mulu> sections; keep Taishō line refs (lb n)."""
    import xml.etree.ElementTree as ET
    f = os.path.join(RAW, "cbeta", "T", tno[:3], f"{tno}.xml")
    raw = open(f, encoding="utf-8").read()
    body = raw.split("<body>", 1)[1].split("</body>", 1)[0]
    body = re.sub(r"<note[^>]*>.*?</note>", "", body, flags=re.S)
    body = re.sub(r"<app>.*?<lem[^>]*>(.*?)</lem>.*?</app>", r"\1", body, flags=re.S)
    segs, sec, secname, n = [], 0, "", 0
    tokens = re.split(r"(<cb:mulu[^>]*>.*?</cb:mulu>|<p[ >].*?</p>|<lg[ >].*?</lg>)", body, flags=re.S)
    for t in tokens:
        if t.startswith("<cb:mulu"):
            name = re.sub(r"<[^>]+>", "", t).strip()
            if name:
                sec += 1; n = 0; secname = name
            continue
        if t.startswith("<p") or t.startswith("<lg"):
            lbs = re.findall(r'<lb[^>]*n="([^"]+)"', t)
            txt = re.sub(r"<[^>]+>", "", t)
            txt = re.sub(r"\s+", "", txt)
            if not txt:
                continue
            n += 1
            segs.append({"ref": f"{max(sec,1)}.{n}", "chapter": str(max(sec, 1)), "chapter_title": secname, "verse": str(n),
                         "zh": txt, "taisho_lines": [lbs[0], lbs[-1]] if lbs else []})
    write(slug, segs, {"source": source_id, "edition": f"CBETA XML P5, Taishō {tno}. {edition_note}", "licence": "CBETA (CC BY-NC-SA) — quotations with attribution",
                       "unit": "one segment per paragraph/verse group within each section (cb:mulu); taisho_lines give the Taishō page-register-line citations",
                       "chunks": [["all"]]})


def platform_sutra():
    cbeta_text("T48n2008", "platform-sutra", "src:platform-sutra", "六祖大師法寶壇經, the Zongbao edition (1291) — the version transmitted in the living Chan/Zen traditions.")
    cbeta_text("T48n2007", "platform-sutra-dunhuang", "src:platform-sutra-dunhuang", "南宗頓教最上大乘摩訶般若波羅蜜經六祖惠能大師於韶州大梵寺施法壇經, the Dunhuang version (the earliest extant).")


def heart_diamond():
    cbeta_text("T08n0235", "vajracchedika", "src:vajracchedika", "金剛般若波羅蜜經, Kumārajīva's Chinese translation (402) — the version transmitted in East Asia. The Sanskrit is not in the local corpora (see GAPS).")
    cbeta_text("T08n0251", "prajnaparamita-hrdaya", "src:prajnaparamita-hrdaya", "般若波羅蜜多心經, Xuanzang's Chinese translation (649).")
    f = os.path.join(RAW, "raw_etexts", "mixed", "gretil_devanAgarI", "1_sanskr", "4_rellit", "buddh", "prajnaparamitahrdayasutra_samksiptamatrka.md")
    body = open(f, encoding="utf-8").read().split("## पाठः", 1)[1]
    body = re.sub(r"\(वैद्य [^)]*\)", "", body)
    sents = [x.strip() for x in re.split(r"॥", re.sub(r"\s+", " ", body)) if x.strip()]
    segs = [{"ref": f"s{i}", "chapter": "1", "verse": str(i), "deva": t, "iast": iast(t)} for i, t in enumerate(sents, 1)]
    write("prajnaparamita-hrdaya-sanskrit-short", segs, {"source": "src:prajnaparamita-hrdaya", "edition": "GRETIL e-text of the shorter Sanskrit recension (after Vaidya, Mahāyāna-sūtra-saṃgraha I, p. 97), Devanāgarī mirror",
        "licence": "Root text public domain; GRETIL CC BY-NC-SA 4.0", "unit": "one segment per sentence (daṇḍa-delimited)", "chunks": [["all"]]})


def tibetan_canon_text(toh, slug, source_id, title_note, lines_per_stanza=4, coll="derge-tengyur"):
    """A text of the Esukhia digital Derge Tengyur/Kangyur (public domain) by Tohoku number: the title/homage block,
    then stanzas of `lines_per_stanza` verse lines (a line ends with a shad), then the colophon. Each segment keeps the
    Derge folio.line where it starts, the Tibetan and a Wylie transliteration (pyewts)."""
    import glob as _g
    import pyewts
    conv = pyewts.pyewts()
    fn = next(f for f in sorted(_g.glob(os.path.join(RAW, coll, "text", "*.txt"))) if "{" + toh + "}" in open(f, encoding="utf-8").read())
    t = open(fn, encoding="utf-8").read()
    i = t.index("{" + toh + "}") + len(toh) + 2
    m = re.search(r"\{D\d+[a-z]?\}", t[i:])
    body = t[i: i + m.start()] if m else t[i:]
    # tokens: folio markers and text
    prev_marks = re.findall(r"\[([0-9a-z]+\.[0-9]+)\]", t[:i])
    folio, lines, cur, cur_folio = (prev_marks[-1] if prev_marks else None), [], "", None
    for tok in re.split(r"(\[[0-9a-z.x]+\])", body.replace("\n", "")):
        if re.fullmatch(r"\[[0-9a-z.x]+\]", tok):
            if "." in tok:
                folio = tok[1:-1]
            continue
        for piece in re.split(r"(།+\s*།?)", tok.replace("#", "")):
            if not piece:
                continue
            if cur_folio is None and piece.strip():
                cur_folio = folio
            cur += piece
            if re.fullmatch(r"།+\s*།?", piece):
                if cur.strip(" །"):
                    lines.append((cur_folio, cur.strip()))
                cur, cur_folio = "", None
    if cur.strip(" །"):
        lines.append((cur_folio, cur.strip()))
    # title/homage: everything up to and including the homage line (ends with 'ཕྱག་འཚལ་ལོ')
    k = 0
    for n, (_, ln) in enumerate(lines[:8]):
        if "ཕྱག་འཚལ་ལོ" in ln:
            k = n + 1
    head, rest = lines[:k], lines[k:]
    # colophon: from the line containing 'རྫོགས་སོ' (text end) — keep the final line(s) that name the author/translation
    c = next((n for n in range(len(rest) - 1, -1, -1) if "རྫོགས" in rest[n][1]), None)
    colo, rest = (rest[c:], rest[:c]) if c is not None else ([], rest)
    # the author-statement line just before 'rdzogs so' belongs to the colophon when it names the author
    if rest and re.search(r"མཛད་པ|གསུངས་པ", rest[-1][1]) and not colo:
        colo, rest = [rest[-1]], rest[:-1]
    segs = []
    def mk(ref, grp, note=None):
        tib = " ".join(x[1] for x in grp)
        sg = {"ref": ref, "chapter": None, "verse": ref, "folio": grp[0][0] if grp else None, "tib": tib, "wylie": conv.toWylie(tib).replace("_", " ")}
        if note:
            sg["note"] = note
        return sg
    if head:
        segs.append(mk("title", head, "Sanskrit and Tibetan titles and homage"))
    for n in range(0, len(rest), lines_per_stanza):
        segs.append(mk(f"v{n // lines_per_stanza + 1}", rest[n:n + lines_per_stanza]))
    if colo:
        segs.append(mk("colophon", colo))
    nst = len(rest) // lines_per_stanza + (1 if len(rest) % lines_per_stanza else 0)
    write(slug, segs, {"source": source_id, "edition": f"Derge Tengyur/Kangyur, Tōhoku {toh}, digital edition by Esukhia and Barom Theksum Choling (github.com/Esukhia/{coll}), file {os.path.basename(fn)}",
          "licence": "Public domain (mechanical reproduction of a public-domain work, per the repository)",
          "language": "Classical Tibetan (translation from Sanskrit/Apabhraṃśa)", "script": "Tibetan (Unicode) with Wylie",
          "unit": f"stanzas of {lines_per_stanza} verse lines numbered v1…v{nst} in order (a mechanical grouping — the ontology's refs are 'v<N>' plus the Derge folio.line). Where a sense unit crosses a stanza boundary, the extractor says so in notes; the original is in Tibetan translation, so paraphrases must say 'the Tibetan reads …' where the wording matters. " + title_note,
          "chunks": [["title"] + [f"v{i}" for i in range(1, nst + 1)] + ["colophon"]] if nst <= 60 else [[f"v{i}" for i in range(a, min(a + 50, nst + 1))] for a in range(1, nst + 1, 50)]})


def tibetan_core():
    tibetan_canon_text("D2303", "tilopa-mahamudropadesa", "src:ganga-mahamudra", "Tilopa's Mahāmudrā instruction given to Nāropa on the bank of the Gaṅgā (colophon), the 'Gaṅgāmā'.")
    tibetan_canon_text("D2224", "saraha-dohakosa-people", "src:dohakosa-saraha", "Saraha's Dohākoṣagīti (the 'People Dohā'), Tibetan translation.")
    tibetan_canon_text("D2263", "saraha-dohakosa-king", "src:dohakosa-king-saraha", "Saraha's Dohākoṣa-nāma-caryāgīti (the 'King Dohā').")
    tibetan_canon_text("D2264", "saraha-dohakosa-queen", "src:dohakosa-queen-saraha", "Saraha's Dohākoṣa-upadeśagīti (the 'Queen Dohā').")


def tattvartha_sutra():
    """Umāsvāti/Umāsvāmin's Tattvārthasūtra, Digambara recension (the text Pūjyapāda comments on in the Sarvārthasiddhi),
    root sūtras only, from the nikkyjain.github.io Jain database (GitHub). One page per sūtra: <div class=gatha>…॥N॥</div>.
    The site's modern Hindi/English renderings and the commentaries are NOT stored."""
    import glob as _g, html as _h
    d = os.path.join(RAW, "nikkyjain", "jainDataBase", "shastra", "01_द्रव्यानुयोग", "13_तत्त्वार्थसूत्र--आचार्य-उमास्वामी", "html")
    segs = []
    for fn in sorted(_g.glob(os.path.join(d, "[0-9][0-9]-[0-9][0-9]*.html"))):
        chap = str(int(os.path.basename(fn)[:2]))
        t = open(fn, encoding="utf-8").read()
        for g in re.findall(r"<div class=gatha>(.*?)</div>", t, flags=re.S):
            txt = _h.unescape(re.sub(r"<[^>]+>", " ", g)).replace("\ufeff", "")
            m = re.search(r"॥\s*([0-9०-९]+)\s*॥", txt)
            if not m:
                continue
            n = m.group(1).translate(DEV_DIGITS)
            sutra = re.sub(r"\s+", " ", txt[: m.start()]).strip()
            sutra = re.sub(r"(?<=[\u0900-\u097F]):", "ः", sutra)  # the site types visarga as ':' 
            segs.append({"ref": f"{chap}.{n}", "chapter": chap, "verse": n, "deva": sutra, "iast": iast(sutra)})
    seen, out = set(), []
    for sg in segs:
        if sg["ref"] not in seen:
            seen.add(sg["ref"]); out.append(sg)
    write("tattvartha-sutra", out, {"source": "src:tattvartha-sutra", "edition": "Tattvārthasūtra, Digambara recension (as commented in Pūjyapāda's Sarvārthasiddhi and Akalaṅka's Rājavārttika), root sūtras from the Jain database at github.com/nikkyjain/nikkyjain.github.io (jainDataBase/shastra/01_द्रव्यानुयोग/13_तत्त्वार्थसूत्र--आचार्य-उमास्वामी)",
          "licence": "Root text public domain (c. 2nd–5th c. CE). The site's modern Hindi/English renderings and commentary translations are not used or stored.",
          "recension_note": "The Śvetāmbara recension (with the Svopajña-bhāṣya) differs in the number and wording of some sūtras (Digambara 357 vs Śvetāmbara 344 in the usual counts) and in their numbering within chapters; refs here follow the Digambara numbering. Where a teaching depends on a reading the two recensions do not share, the extractor must say so.",
          "chunks": [["1", "2", "3"], ["4", "5", "6"], ["7", "8"], ["9", "10"]]})


def maitri_upanisad():
    """Maitrī (Maitrāyaṇīya) Upaniṣad, root text only, from the eBhāratī e-text of the edition with Rāmatīrtha's Dīpikā
    (the recension and numbering of Cowell's Bibliotheca Indica edition: 7 prapāṭhakas). Root text = paragraphs set wholly
    in bold; a section may be split into several root pieces interleaved with the commentary and ends with ॥N॥."""
    f = os.path.join(RAW, "raw_etexts", "mixed", "ebhAratI-sampat", "upaniShadaH", "anyAH_upaniShadaH", "maitryupaniShat.md")
    t = open(f, encoding="utf-8").read()
    t = re.sub(r"\[\^\d+\]", "", t)
    t = re.sub(r"\[([^\]]*)\]\(http[^)]*\)", r"\1", t)
    ORD = {"द्वितीयः": 2, "तृतीयः": 3, "चतुर्थः": 4, "पञ्चमः": 5, "षष्ठः": 6, "सप्तमः": 7}
    paras = [x.strip() for x in re.split(r"\n\s*\n", t)]
    start = next(i for i, x in enumerate(paras) if x.startswith("**ब्रह्मयज्ञो"))
    chap, buf, segs = 1, [], []
    for x in paras[start:]:
        if x.startswith("[^"):
            continue
        y = x.rstrip(" \\\n")
        if not (y.startswith("**") and y.endswith("**")):
            # a commentary paragraph can carry the section-end marker of the root piece just given (e.g. 1.1)
            mc = re.search(r"॥\s*([०-९0-9]+)\s*॥\s*$", y)
            if mc and buf:
                n = mc.group(1).translate(DEV_DIGITS)
                exp = str(int(segs[-1]["verse"]) + 1) if segs and segs[-1]["chapter"] == str(chap) else "1"
                if n == exp:
                    text = " ".join(buf)
                    segs.append({"ref": f"{chap}.{n}", "chapter": str(chap), "verse": n, "deva": text, "iast": iast(text), "pieces": len(buf),
                                 "note": "section-end number printed in the commentary paragraph that follows the root"})
                    buf = []
            continue
        sp = re.sub(r"\s+", " ", y.strip("* ")).replace("**", "").strip()
        mo = re.match(r"अथ\s+(\S+)\s+प्रपाठकः", sp)
        if mo:
            chap, buf = ORD.get(mo.group(1), chap), []
            continue
        if "प्रपाठक" in sp:
            buf = []
            if "सप्तमः" in sp and "मैत्र्युपनिषदि" in sp:
                break
            continue
        if re.search(r"नमोऽस्तु\s*॥|नमो गुरुभ्यः|नुमः\s*॥|विरचित", sp):  # Rāmatīrtha's own benedictory verses / colophons
            continue
        if "॰" in sp or sp[:1] in "“\"'‘" or re.search(r"इति\s*[।॥]?\s*$", sp) and not re.search(r"॥\s*[०-९0-9]+\s*॥\s*$", sp):
            continue
        m = re.search(r"॥\s*([०-९0-9]+)\s*॥\s*$", sp)
        buf.append(sp[: m.start()].strip() if m else sp)
        if m:
            n = m.group(1).translate(DEV_DIGITS)
            text = " ".join(buf)
            segs.append({"ref": f"{chap}.{n}", "chapter": str(chap), "verse": n, "deva": text, "iast": iast(text), "pieces": len(buf)})
            buf = []
    write("maitri-upanisad", segs, {"source": "src:maitri-upanisad", "edition": "Maitryupaniṣat with Rāmatīrtha's Dīpikā — eBhāratī-sampat e-text Ebharati-9566 (contributed by the Deccan College Post-graduate and Research Institute); recension and numbering as in Cowell's Bibliotheca Indica edition (1870, with Rāmatīrtha's commentary): 7 prapāṭhakas",
          "licence": "Root text public domain; 19th-c. edition public domain; only the root text is stored",
          "unit": "one segment per section (khaṇḍa) N of prapāṭhaka P, ref 'P.N'; `pieces` = number of root pieces joined (the edition interleaves the root with the commentary). The Muktikā/Adyar 'Maitrāyaṇī' recension numbers sections differently (e.g. its prapāṭhaka 1 has 7 sections).",
          "chunks": [["1", "2", "3", "4", "5"], ["6"], ["7"]]})


HANDLERS = {"bhagavad-gita": bhagavad_gita, "yoga-sutra": yoga_sutra, "pali": pali_suttas, "upanisads": upanisads, "mandukya": mandukya, "kashmir_samkhya": kashmir_and_samkhya, "hatha_gitas": hatha_and_gitas, "mmk_astavakra": buddhist_and_advaita_gitas, "pratyabhijnahrdaya": pratyabhijnahrdaya, "tibetan": tibetan_core, "tattvartha": tattvartha_sutra, "maitri": maitri_upanisad, "avadhuta": avadhuta_gita, "platform": platform_sutra, "heart_diamond": heart_diamond}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        print("available:", ", ".join(HANDLERS))
    else:
        for s in sys.argv[1:]:
            HANDLERS[s]()
