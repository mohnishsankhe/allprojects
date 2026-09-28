#!/usr/bin/env python3
"""Generate the human-readable ATLAS/ from data/. Run after scripts/merge.py.

One page per lineage, text, teacher, concept, practice, obstacle, path map, debate and term, plus section indexes,
ATLAS/ULTIMATE.md and ATLAS/INDEX.md. Every entry shows its verification level.
"""
import glob, json, os, re, shutil, datetime
from collections import defaultdict, Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
ATLAS = os.path.join(ROOT, "ATLAS")
NOW = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %H:%M IST")
SECTIONS = {  # prefix -> (folder, data file, title field, heading)
    "lin": ("lineages", "lineages", "name", "Lineages"),
    "src": ("texts", "sources", "title", "Texts"),
    "tch": ("teachers", "teachers", "name", "Teachers"),
    "cpt": ("concepts", "concepts", "name", "Concepts"),
    "prc": ("practices", "practices", "name", "Practices"),
    "obs": ("obstacles", "obstacles", "name", "Obstacles"),
    "pth": ("paths", "paths", "name", "Path maps"),
    "dsp": ("debates", "disputes", "question", "Debates"),
    "trm": ("terms", "terms", "term", "Terms"),
}
IDX = {}
TEACH_BY_SRC = defaultdict(list)
TEACH = {}


def load(name):
    p = os.path.join(DATA, f"{name}.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []


def slug(eid):
    return re.sub(r"[^a-z0-9\-\.]", "_", eid.split(":", 1)[1])[:120]


def badge(o):
    v = o.get("verification") or {}
    lvl = v.get("level", "skeleton")
    s = f"`{lvl}`"
    if v.get("confidence"):
        s += f" · confidence {v['confidence']}"
    if v.get("unverified"):
        s += " · **[unverified]**"
    if o.get("retired"):
        s += " · **retired**"
    if o.get("recent"):
        s += " · _recent (post-1800)_"
    if o.get("restricted"):
        s += " · _restricted: summary only_"
    if o.get("ai_translated"):
        s += " · [AI-translated]"
    return s


def link(eid, frm):
    """markdown link from folder `frm` to entity eid (or plain text if unknown)."""
    if not isinstance(eid, str) or ":" not in eid:
        return str(eid)
    pfx = eid.split(":", 1)[0]
    if pfx == "tea":
        t = TEACH.get(eid)
        if t:
            sfold = "texts"
            rel = os.path.relpath(os.path.join(ATLAS, sfold, slug(t["source"]) + ".md"), os.path.join(ATLAS, frm))
            return f"[{eid.split(':',2)[-1]}]({rel}#{anchor(eid)})"
        return f"`{eid}`"
    if pfx not in SECTIONS or eid not in IDX:
        return f"`{eid}`"
    folder = SECTIONS[pfx][0]
    rel = os.path.relpath(os.path.join(ATLAS, folder, slug(eid) + ".md"), os.path.join(ATLAS, frm))
    return f"[{IDX[eid]}]({rel})"


def anchor(tid):
    return re.sub(r"[^a-z0-9]+", "-", tid.lower()).strip("-")


def fmt_dating(d):
    if not isinstance(d, dict) or not d:
        return None
    parts = []
    for acc, lab in (("tradition", "Tradition's account"), ("scholarly", "Scholarly account")):
        a = d.get(acc)
        if isinstance(a, dict) and a.get("text"):
            parts.append(f"{lab}: {a['text']}")
    if d.get("confidence"):
        parts.append(f"(confidence {d['confidence']})")
    return "; ".join(parts) if parts else None


def lst(vals, frm):
    if not vals:
        return ""
    out = []
    for v in vals:
        if isinstance(v, str):
            out.append(link(v, frm))
        elif isinstance(v, dict):
            key = v.get("source") or v.get("teacher") or v.get("target") or v.get("lineage") or v.get("to") or v.get("from")
            rest = {k: x for k, x in v.items() if x not in (None, "", [], {}) and x != key}
            out.append((link(key, frm) + " — " if key else "") + "; ".join(f"{k}: {x if isinstance(x,str) else json.dumps(x,ensure_ascii=False)}" for k, x in rest.items()))
    return ", ".join(out) if all(isinstance(v, str) for v in vals) else "\n" + "\n".join(f"  - {x}" for x in out)


def page(folder, o, title, body_lines):
    path = os.path.join(ATLAS, folder, slug(o["id"]) + ".md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(f"# {title}\n\n`{o['id']}` · {badge(o)}\n\n")
        fh.write("\n".join(l for l in body_lines if l is not None) + "\n")
        prov = o.get("provenance") or {}
        checks = (o.get("verification") or {}).get("checks") or []
        fh.write("\n---\n")
        if checks:
            fh.write("**Verification checks**\n\n")
            for c in checks[:8]:
                ev = ", ".join(c.get("evidence") or [])[:300]
                fh.write(f"- {c.get('date','')} {c.get('method','')}: {c.get('result','')}{' — ' + ev if ev else ''}{' — ' + c['note'] if c.get('note') else ''}\n")
            fh.write("\n")
        if o.get("correction_log"):
            fh.write("**Corrections**\n\n" + "\n".join(f"- {c.get('field')}: {c.get('reason','')}" for c in o["correction_log"][:10]) + "\n\n")
        fh.write(f"_Contributed by: {', '.join(prov.get('units', []))}. Generated {NOW}._\n")


def field(label, val):
    if val in (None, "", [], {}):
        return None
    return f"**{label}:** {val}"


def teaching_block(t, frm):
    tg = t.get("tags") or {}
    orig = (t.get("original") or {}).get("text")
    lines = [f"### {t['location'].get('ref') if isinstance(t.get('location'), dict) else ''} <a id=\"{anchor(t['id'])}\"></a>",
             f"{badge(t)}", "", t.get("paraphrase", "")]
    if orig:
        lines += ["", f"> {orig}"]
    lines += ["", f"_level: {tg.get('level')} · standpoint: {tg.get('standpoint')}{' ('+tg['naya']+')' if tg.get('naya') else ''} · path: {', '.join(tg.get('path') or [])} · stage: {tg.get('stage')}{' ('+tg['stage_native']+')' if tg.get('stage_native') else ''} · types: {', '.join(t.get('types') or [])}_"]
    rel = []
    for k in ("terms", "concepts", "practices", "obstacles", "teachers", "disputes"):
        if t.get(k):
            rel.append(f"{k}: " + ", ".join(link(x, frm) for x in t[k][:12]))
    if rel:
        lines.append("")
        lines.append(" · ".join(rel))
    if t.get("superseded_by"):
        lines.append(f"\n_Superseded by {link(t['superseded_by'], frm)}_")
    if t.get("retired"):
        lines.append(f"\n_Retired: {t['retired'].get('reason')}_")
    return lines


def main():
    if os.path.exists(ATLAS):
        shutil.rmtree(ATLAS)
    os.makedirs(ATLAS)
    D = {k: load(v[1]) for k, v in SECTIONS.items()}
    for pfx, items in D.items():
        for o in items:
            IDX[o["id"]] = o.get(SECTIONS[pfx][2]) or o["id"]
    for f in glob.glob(os.path.join(DATA, "teachings", "*.jsonl")):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                t = json.loads(line)
                TEACH[t["id"]] = t
                TEACH_BY_SRC[t.get("source")].append(t)
    ult = json.load(open(os.path.join(DATA, "ultimate.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "ultimate.json")) else {"node": {}, "views": []}
    disputes_by_lin = defaultdict(list)
    for o in D["dsp"]:
        for s in o.get("sides") or []:
            if isinstance(s, dict) and s.get("lineage"):
                disputes_by_lin[s["lineage"]].append(o["id"])
    prac_by_lin = defaultdict(list)
    for o in D["prc"]:
        for l in (o.get("convergence") or {}).get("lineages") or o.get("lineages") or []:
            prac_by_lin[l].append(o["id"])
    texts_by_lin, teachers_by_lin, comm_on = defaultdict(list), defaultdict(list), defaultdict(list)
    for o in D["src"]:
        for l in o.get("lineages") or []:
            texts_by_lin[l].append(o["id"])
        if o.get("commentary_on"):
            comm_on[o["commentary_on"]].append(o["id"])
    for o in D["tch"]:
        for l in o.get("lineages") or []:
            teachers_by_lin[l].append(o["id"])
    ult_by_lin = {v.get("lineage"): v for v in ult.get("views", [])}

    for pfx, (folder, _, tf, heading) in SECTIONS.items():
        os.makedirs(os.path.join(ATLAS, folder), exist_ok=True)
        for o in D[pfx]:
            t = o.get(tf) or o["id"]
            L = []
            if pfx == "lin":
                L += [field("Family", o.get("family")), field("Alternate names", ", ".join(o.get("alt_names") or [])),
                      field("Parent", link(o["parent"], folder) if o.get("parent") else None),
                      field("Sub-lineages", lst(o.get("sub_lineages"), folder)), field("Founders", lst(o.get("founders"), folder)),
                      field("Key teachers", lst(o.get("key_teachers"), folder)), field("Regions", ", ".join(o.get("regions") or [])),
                      field("Dates", fmt_dating(o.get("dating"))), field("Status", o.get("status")), "", o.get("summary", ""), "",
                      "## Distinctive positions", *[f"- {p}" for p in o.get("distinctive_positions") or []], "",
                      field("Transmissions received", lst(o.get("transmissions_received"), folder)),
                      field("Transmissions given", lst(o.get("transmissions_given"), folder))]
                v = ult_by_lin.get(o["id"])
                if v:
                    L += ["", "## The ultimate in this lineage", f"{badge(v)}", "",
                          field("Names", ", ".join(n.get("name", "") if isinstance(n, dict) else str(n) for n in v.get("names") or [])),
                          field("Descriptions", "; ".join(v.get("descriptions") or [])), field("Negations", "; ".join(v.get("negations") or [])),
                          field("Relation to self", v.get("relation_to_self")), field("Relation to world", v.get("relation_to_world")),
                          field("Caveat", v.get("caveat"))]
                L += ["", "## Texts", lst(sorted(set(texts_by_lin[o["id"]]) | set(o.get("texts") or [])), folder) or "_none recorded_",
                      "", "## Teachers", lst(sorted(set(teachers_by_lin[o["id"]]) | set(o.get("key_teachers") or [])), folder) or "_none recorded_",
                      "", "## Practices", lst(sorted(set(prac_by_lin[o["id"]])), folder) or "_none recorded_",
                      "", "## Path maps", lst(o.get("path_maps"), folder) or "_none recorded_",
                      "", "## Debates", lst(sorted(set(disputes_by_lin[o["id"]])), folder) or "_none recorded_"]
            elif pfx == "src":
                L += [field("Alternate titles", ", ".join(o.get("alt_titles") or [])), field("Original title", o.get("title_original")),
                      field("Language", ", ".join(o.get("language") or [])), field("Family", o.get("family")),
                      field("Lineages", lst(o.get("lineages"), folder)), field("Genre", o.get("genre")),
                      field("Part of", link(o["part_of"], folder) if o.get("part_of") else None), field("Location in parent", o.get("location_in_parent")),
                      field("Commentary on", link(o["commentary_on"], folder) if o.get("commentary_on") else None),
                      field("Authors", lst(o.get("authors"), folder)),
                      field("Attribution", "; ".join(f"{k}: {v}" for k, v in (o.get("attribution") or {}).items())),
                      field("Dates", fmt_dating(o.get("dating"))),
                      field("Structure", (o.get("structure") or {}).get("description") if isinstance(o.get("structure"), dict) else o.get("structure")),
                      field("Availability", o.get("availability")), "", o.get("summary", ""),
                      field("Editions / translations", lst(o.get("editions"), folder)),
                      field("Commentaries on this text", lst(sorted(comm_on[o["id"]]), folder))]
                def _rk(t):
                    ref = str((t.get("location") or {}).get("ref", "0")) if isinstance(t.get("location"), dict) else "0"
                    return [(0, int(x), "") if x.isdigit() else (1, 0, x) for x in re.split(r"[.\-/:]", ref)]
                ts = sorted(TEACH_BY_SRC.get(o["id"], []), key=_rk)
                if ts:
                    lv = Counter((t.get("verification") or {}).get("level") for t in ts)
                    L += ["", f"## Teachings ({len(ts)}: " + ", ".join(f"{k} {v}" for k, v in lv.items()) + ")", ""]
                    for tt in ts:
                        try:
                            L += teaching_block(tt, folder) + [""]
                        except Exception:
                            L += [f"- `{tt.get('id')}`"]
            elif pfx == "tch":
                ra = o.get("realization_account") or {}
                L += [field("Alternate names", ", ".join(o.get("alt_names") or [])), field("Lineages", lst(o.get("lineages"), folder)),
                      field("Dates", fmt_dating(o.get("dating"))), field("Places", ", ".join(o.get("places") or [])),
                      field("Historicity", o.get("historicity")), field("Teachers", lst(o.get("teachers"), folder)),
                      field("Students", lst(o.get("students"), folder)), field("Works", lst(o.get("works"), folder)), "",
                      o.get("summary", ""),
                      field("Realization — " + (ra.get("label") or "the tradition's account"), ra.get("text")) if ra else None]
            elif pfx == "cpt":
                L += [field("Category", o.get("category")), field("Members", ", ".join(map(str, o.get("members") or []))),
                      "", "## Names", *[f"- {link(n.get('lineage'), folder)}: {n.get('name')}" for n in o.get("names") or [] if isinstance(n, dict)],
                      "", "## Definitions", *[f"- {link(d.get('lineage'), folder)}: {d.get('definition')}" for d in o.get("definitions") or [] if isinstance(d, dict)],
                      "", "## Relations (interpretation layer)", *[f"- {r.get('rel')} → {link(r.get('target'), folder)}{' ('+r['standpoint']+')' if r.get('standpoint') else ''}{': '+r['note'] if r.get('note') else ''}{' — rests on '+', '.join(link(x, folder) for x in r.get('rests_on') or []) if r.get('rests_on') else ''}" for r in o.get("relations") or [] if isinstance(r, dict)]]
            elif pfx in ("prc", "obs"):
                cv = o.get("convergence") or {}
                L += [field("Category", o.get("category")), field("Convergence", f"{cv.get('count', 0)} independent lineage(s): " + lst(cv.get("schools"), folder) if cv else None),
                      field("Taught in", lst(cv.get("lineages") or o.get("lineages"), folder)), "",
                      o.get("method_summary") or o.get("description") or "",
                      field("Stage", o.get("stage")), field("Prerequisites", o.get("prerequisites")), field("Duration", o.get("duration")),
                      field("Signs of progress", o.get("signs_of_progress")), field("Antidotes", lst(o.get("antidotes"), folder)),
                      field("Members", ", ".join(map(str, o.get("members") or []))),
                      field("Sources", lst(o.get("sources"), folder)), field("Sequences", lst(o.get("sequences"), folder))]
                if o.get("warnings"):
                    L += ["", "## The texts' own warnings", *[f"- {w.get('text') if isinstance(w, dict) else w}{' — ' + link(w.get('source'), folder) + ' ' + str(w.get('ref') or '') if isinstance(w, dict) and w.get('source') else ''}" for w in o["warnings"]]]
                if o.get("equivalents"):
                    L += ["", "## Equivalents (interpretation layer)", *[f"- {e.get('grade')}: {link(e.get('target'), folder)}{' ('+e['standpoint']+')' if e.get('standpoint') else ''}{' — '+e['note'] if e.get('note') else ''}" for e in o["equivalents"] if isinstance(e, dict)]]
            elif pfx == "pth":
                L += [field("Lineage", link(o.get("lineage"), folder)), field("Sources", lst(o.get("sources"), folder)), "",
                      "| # | stage | gloss | ref | band |", "|---|---|---|---|---|",
                      *[f"| {s.get('order','')} | {s.get('name','')} | {s.get('gloss','') or ''} | {s.get('ref','') or ''} | {s.get('band','') or ''} |" for s in o.get("stages") or [] if isinstance(s, dict)],
                      "", o.get("notes", "") or ""]
            elif pfx == "dsp":
                L += [field("Coverage", o.get("coverage_ref")), "", "## Sides (recorded before any reconciliation)"]
                for s in o.get("sides") or []:
                    if isinstance(s, dict):
                        L += [f"### {link(s.get('lineage'), folder)}", s.get("position", ""), *[f"- {a}" for a in s.get("arguments") or []],
                              field("Texts", lst(s.get("texts"), folder))]
                for h in o.get("historical_debates") or []:
                    if isinstance(h, dict):
                        L += ["", f"**Historical debate — {h.get('name')}** ({h.get('date','')}): {h.get('accounts','')} {h.get('outcome_by_tradition','')}"]
                rec = o.get("reconciliation") or {}
                if rec:
                    st = rec.get("status")
                    L += ["", "## Reconciliation (interpretation layer)", f"**Status:** {'not yet reconciled (queued)' if st == 'queued' else st}",
                          field("Principles", ", ".join(rec.get("principles") or [])), field("Explanation", rec.get("explanation")),
                          rec.get("detail"), field("The traditions' own objections", rec.get("tradition_objections")),
                          field("Candidate readings", "; ".join(map(str, rec.get("candidate_readings") or []))),
                          field("Queue", o.get("queue_ref"))]
            elif pfx == "trm":
                L += [field("Language", o.get("language")), field("Native script", o.get("native")), field("Literal", o.get("literal")),
                      "", "## Definitions by tradition", *[f"- {link(d.get('lineage'), folder)}: {d.get('definition')}" for d in o.get("definitions") or [] if isinstance(d, dict)],
                      "", "## Forms in other languages", *[f"- {c.get('language')}: {c.get('form')} {c.get('native','') or ''} — {c.get('grade')}{' ('+c['standpoint']+')' if c.get('standpoint') else ''}{' — '+c['note'] if c.get('note') else ''}" for c in o.get("cross_language") or [] if isinstance(c, dict)],
                      "", "## Equivalents (interpretation layer)", *[f"- {e.get('grade')}: {link(e.get('target'), folder)}{' ('+e['standpoint']+')' if e.get('standpoint') else ''}{' — '+e['note'] if e.get('note') else ''}" for e in o.get("equivalents") or [] if isinstance(e, dict)],
                      field("Related", lst(o.get("related"), folder))]
            if o.get("notes") and pfx not in ("pth",):
                L += ["", f"_Notes: {o['notes']}_"]
            page(folder, o, t, L)
        # section index
        rows = sorted(D[pfx], key=lambda o: (str(o.get(tf) or o["id"]).lower()))
        with open(os.path.join(ATLAS, folder, "INDEX.md"), "w", encoding="utf-8") as fh:
            lv = Counter((o.get("verification") or {}).get("level") for o in rows)
            fh.write(f"# {heading} ({len(rows)})\n\n" + " · ".join(f"{k}: {v}" for k, v in lv.items()) + "\n\n")
            for o in rows:
                v = o.get("verification") or {}
                fh.write(f"- [{o.get(tf) or o['id']}]({slug(o['id'])}.md) — `{v.get('level','skeleton')}`{' [unverified]' if v.get('unverified') else ''}{' _(recent)_' if o.get('recent') else ''}\n")
    # ULTIMATE.md
    with open(os.path.join(ATLAS, "ULTIMATE.md"), "w", encoding="utf-8") as fh:
        n = ult.get("node") or {}
        fh.write("# The one truth — every tradition's view of the ultimate\n\n")
        if n:
            fh.write(f"> {n.get('principle','')}\n\n{n.get('how_to_read','')}\n\n")
        fh.write("| lineage | names | how it is described | negations | relation to self | relation to world | personal? | level |\n|---|---|---|---|---|---|---|---|\n")
        for v in sorted(ult.get("views", []), key=lambda v: v.get("lineage") or ""):
            names = ", ".join(x.get("name", "") if isinstance(x, dict) else str(x) for x in v.get("names") or [])
            cell = lambda s: (s or "").replace("|", "/").replace("\n", " ")[:300]
            fh.write(f"| {link(v.get('lineage'), '.')} | {cell(names)} | {cell('; '.join(v.get('descriptions') or []))} | {cell('; '.join(v.get('negations') or []))} | {cell(v.get('relation_to_self'))} | {cell(v.get('relation_to_world'))} | {v.get('personal_or_impersonal','')} | {(v.get('verification') or {}).get('level','')} |\n")
    # INDEX.md
    st = json.load(open(os.path.join(DATA, "reports", "stats.json"), encoding="utf-8")) if os.path.exists(os.path.join(DATA, "reports", "stats.json")) else {}
    with open(os.path.join(ATLAS, "INDEX.md"), "w", encoding="utf-8") as fh:
        fh.write(f"# Tradition Ontology — Atlas\n\n_Generated {NOW}._\n\n")
        fh.write("Every page shows each entry's verification level: `skeleton` (from model knowledge, unchecked), `sourced` (existence and basic facts confirmed externally), `text-verified` (extracted from the text and fidelity-checked); **[unverified]** marks items the hallucination sweep could not confirm (kept, never deleted).\n\n")
        fh.write("## Sections\n\n")
        for pfx, (folder, _, _, heading) in SECTIONS.items():
            fh.write(f"- [{heading}]({folder}/INDEX.md) — {len(D[pfx])}\n")
        fh.write(f"- [The one truth: every tradition's ultimate](ULTIMATE.md) — {len(ult.get('views', []))} views\n")
        fh.write("- [Reconciliation queue](../RECONCILE_QUEUE.md) · [Gaps](../GAPS.md) · [Decisions](../DECISIONS.md) · [Progress](../PROGRESS.md)\n\n")
        if st:
            fh.write("## Counts\n\n")
            fh.write(open(os.path.join(DATA, "reports", "stats.md"), encoding="utf-8").read().split("\n", 2)[-1])
    print("atlas pages:", sum(len(D[p]) for p in D), "+ indexes")


if __name__ == "__main__":
    main()
