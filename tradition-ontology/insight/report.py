"""Report renderer: Markdown and HTML from the report object (see ENGINE_SPEC.md, 'Report object').

Everything shown is taken from the report object; the renderer adds no content of its own except fixed headings and
the standing notice. Citations are shown with source title and exact reference.
"""
from __future__ import annotations

import html

STANDING_NOTICE = ("This reading reflects what you wrote through the lens of traditional texts. It is not a diagnosis, "
                   "not medical or psychological advice, and it does not predict anything.")


def _cite_list(ids, cites: dict) -> str:
    out = []
    for t in ids or []:
        c = cites.get(t)
        if c:
            out.append(f"{c['title']} {c['ref']}")
    return "; ".join(out)


def to_markdown(r: dict) -> str:
    L = [f"# Your reading", "", f"_{STANDING_NOTICE}_", ""]
    for n in r.get("notices") or []:
        L += [f"> {n}", ""]
    if r.get("stopped"):
        m = r["stopped"]
        if m.get("lead"):
            L += [f"**{m['lead']}**", ""]
        L += [f"## {m.get('title','')}", "", m.get("body", ""), ""]
        for x in m.get("extra") or []:
            L += [x, ""]
        for res in m.get("resources") or []:
            L.append(f"- **{res['region']}** — {res['name']}: {res['contact']}")
        return "\n".join(L).strip() + "\n"
    if r.get("insufficient"):
        L += ["## Not enough to connect, honestly", "", r["insufficient"], ""]
    cites = r.get("citations") or {}
    if r.get("summary"):
        L += ["## What you shared, in brief", "", r["summary"], ""]
    if r.get("mappings"):
        L += ["## Patterns the texts describe", ""]
        for m in r["mappings"]:
            q = "; ".join(f"“{e['quote']}”" for e in m.get("evidence", []))
            L += [f"### {m['name']} ({m['lens_label']})", "",
                  f"- Your words: {q}", f"- Why this fits: {m.get('why','')}",
                  f"- How sure: {m['confidence']}", f"- Texts: {_cite_list(m.get('cites'), cites)}", ""]
    for key, title in (("vedic", "The Vedic and yogic reading"), ("ascetic", "The ascetic reading (Buddhist and Jain)")):
        lens = (r.get("lenses") or {}).get(key) or {}
        if lens.get("points") or (lens.get("note") and r.get("mappings")):
            L += [f"## {title}", ""]
            for p in lens.get("points") or []:
                L.append(f"- {p['text']} _({_cite_list(p.get('cites'), cites)})_")
            if not lens.get("points") and lens.get("note"):
                L.append(lens["note"])
            L.append("")
    rec = r.get("reconciliation") or {}
    if rec.get("points") or rec.get("differences"):
        L += ["## How the two readings fit together", ""]
        for p in rec.get("points") or []:
            L.append(f"- {p['text']} _({p.get('basis','')}; {_cite_list(p.get('cites'), cites)})_")
        for d in rec.get("differences") or []:
            L.append(f"- Where they differ: {d['text']} _({_cite_list(d.get('cites'), cites)})_")
        L.append("")
    pw = r.get("pathway") or {}
    if pw.get("practices"):
        L += ["## A gentle practice pathway", ""]
        for p in pw["practices"]:
            d = p.get("duration") or {}
            mins = d.get("minutes_per_session")
            L += [f"### {p['name']}", "", p.get("why", ""), ""]
            for i, s in enumerate(p.get("steps") or [], 1):
                L.append(f"{i}. {s}")
            if mins:
                L.append(f"\nLength: {mins[0]}–{mins[-1]} minutes, {d.get('sessions_per_day',1)} time(s) a day ({d.get('basis','')}).")
            for w in p.get("warnings") or []:
                L.append(f"\n**The texts' caution:** {w['text']} _({_cite_list(w.get('cites'), cites)})_")
            L.append(f"\n_Texts: {_cite_list(p.get('cites'), cites)}_\n")
        if pw.get("sequence"):
            L += ["### Your 14 days", ""]
            for s in pw["sequence"]:
                L.append(f"- Day {s['day']}: {s['plan']}")
            L.append("")
        if pw.get("checkin_prompt"):
            L += ["### Daily check-in", "", pw["checkin_prompt"], ""]
    if cites:
        L += ["## Sources", ""]
        for c in cites.values():
            orig = f" — “{c['original'][:160]}”" if c.get("original") else ""
            L.append(f"- **{c['title']} {c['ref']}** ({c['level']}){orig}")
        L.append("")
    return "\n".join(L).strip() + "\n"


def to_html(r: dict) -> str:
    """Minimal, dependency-free HTML: the Markdown is escaped and laid out with simple block rules."""
    md = to_markdown(r)
    out = []
    in_list = False
    for line in md.splitlines():
        esc = html.escape(line)
        if line.startswith("- ") or (line[:3].strip(". ").isdigit() and ". " in line[:4]):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{html.escape(line.split(' ', 1)[1] if ' ' in line else line)}</li>")
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        if line.startswith("### "):
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("> "):
            out.append(f"<blockquote>{html.escape(line[2:])}</blockquote>")
        elif line.strip():
            out.append(f"<p>{esc}</p>")
    if in_list:
        out.append("</ul>")
    body = "\n".join(out)
    return ("<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
            "<title>Your reading</title><style>body{font-family:system-ui,sans-serif;max-width:46rem;margin:2rem auto;padding:0 1rem;"
            "line-height:1.55;color:#1d1d1f;background:#fff}blockquote{border-left:3px solid #999;margin:1rem 0;padding:.2rem 1rem;color:#444}"
            "h2{margin-top:2rem}@media(prefers-color-scheme:dark){body{background:#141414;color:#eee}blockquote{color:#bbb}}</style></head>"
            f"<body>{body}</body></html>")
