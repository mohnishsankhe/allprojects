#!/usr/bin/env python3
"""Cue calibration for the offline rules engine (MAPPING_RULES.md section 6: "a cue that fires on more than 10% of
bland synthetic baseline personas ..."). Mechanical; no judgement.

    python3 layers/_gen/diagnosis/cue_check.py            # report only
    python3 layers/_gen/diagnosis/cue_check.py --apply    # also remove offending cues_added (repeat until stable)

What it does, on the layer as it is in layers/diagnosis.json:
 1. lint: every cue in a marker's "cues_added" is checked against the cue-writing rules (length, first person, no
    clinical / body / food / sleep / tradition-term / hypothetical / hedge / "we" words, >= 2 content stems, not a
    duplicate) and against the safety screen (a cue must never trip a safety pattern);
 2. self-test: each added cue, written as a person's sentence, must give a direct evidence item on its own marker;
 3. bland baseline (tests/fixtures/bland_baseline.jsonl, 24 synthetic people): for every cue, on how many people the
    rules engine produces an evidence item for that marker through that cue. A cue firing on > 10% (>= 3 of 24) is
    generic. With --apply, an added cue that is generic is removed from "cues" and "cues_added" and recorded in
    cues_removed.json (add_cues.py never re-adds it). Original cues are reported, never removed here.
 4. bland mappings: map_person(..., safety.rule_screen(text), engine="rules") must give 0 mappings for every bland
    person; with --apply, the added cues behind any bland mapping are removed.
 5. dev recall: 10 short patterned DEV texts written here (not evaluation data), mapped with the layer as it is and
    with cues_added stripped (before/after).
Writes cue_check_report.json next to this file.
"""
import argparse
import collections
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT))
from insight import mapper, ontology, safety  # noqa: E402

DIAG = ROOT / "layers" / "diagnosis.json"
BLAND = ROOT / "tests" / "fixtures" / "bland_baseline.jsonl"
REPORT = HERE / "cue_check_report.json"
REMOVED = HERE / "cues_removed.json"
GENERIC_SHARE = 0.10

# ---------------------------------------------------------------------------------------------------------------
# DEV texts: one per common pattern. Synthetic, written for this check only; NOT evaluation data.
# "targets" = the entries whose markers describe the pattern (any of them counts as a hit).
# ---------------------------------------------------------------------------------------------------------------
DEV = [
    {"id": "dev-01", "pattern": "attachment to a remembered pleasure",
     "targets": ["dx:klesa-raga", "dx:nivarana-kamacchanda", "dx:root-lobha", "dx:tanha", "dx:kasaya-lobha",
                 "dx:fetter-kamaraga", "dx:gita-anger-chain", "dx:katha-outward-senses", "dx:guna-rajas"],
     "answers": {
         "q03": "When a holiday ends I'm already scrolling through the photos on the drive home and planning how to get "
                "back there. For weeks I keep replaying the best evenings and wanting them again.",
         "q10": "The feeling I had at the beach house last summer. I chase it with every trip I book."}},
    {"id": "dev-02", "pattern": "lasting anger",
     "targets": ["dx:kasaya-krodha", "dx:klesa-dvesa", "dx:root-dosa", "dx:fetter-patigha", "dx:nivarana-byapada",
                 "dx:gita-kama-krodha", "dx:gita-anger-chain", "dx:carita-dosa"],
     "answers": {
         "q04": "When a colleague lets me down I stay angry for days. I go over what she said on the way home and I'm "
                "still fuming at night.",
         "q02": "Last Tuesday my manager changed my plan without asking and I fumed about it all week, snapping at anyone "
                "who spoke to me."}},
    {"id": "dev-03", "pattern": "the wandering mind at study or prayer",
     "targets": ["dx:gita-restless-mind", "dx:citta-vikkhitta", "dx:gk-viksepa", "dx:nivarana-uddhacca-kukkucca",
                 "dx:fetter-uddhacca", "dx:nivarana-kamacchanda", "dx:antaraya-anavasthitatva"],
     "answers": {
         "q05": "When I sit down to pray my mind wanders off to emails and shopping lists within a minute. I bring it back "
                "and it has drifted again before I finish the first verse.",
         "q13": "I tried a mala for japa every evening. I lose count because my thoughts run off to work."}},
    {"id": "dev-04", "pattern": "going back over the past with regret",
     "targets": ["dx:nivarana-uddhacca-kukkucca"],
     "answers": {
         "q06": "At night my mind keeps going back to a conversation with my brother two years ago. I go over what I said "
                "and what I didn't say, and I regret it again every time."}},
    {"id": "dev-05", "pattern": "wavering about the path",
     "targets": ["dx:nivarana-vicikiccha", "dx:fetter-vicikiccha", "dx:antaraya-samsaya"],
     "answers": {
         "q07": "I keep switching between teachers and traditions. One month I'm sure the Gita is my path, the next I "
                "doubt the whole thing and stop practising.",
         "q13": "I have tried three different meditation methods this year and dropped each one because I wasn't sure it "
                "was right."}},
    {"id": "dev-06", "pattern": "pride when unnoticed",
     "targets": ["dx:kasaya-mana", "dx:fetter-mana", "dx:klesa-asmita", "dx:carita-dosa", "dx:gita-asuri-sampad"],
     "answers": {
         "q08": "When my work goes unnoticed I seethe inside, because I know I'm better than the others on the team. When "
                "someone else is praised I tell myself they don't deserve it."}},
    {"id": "dev-07", "pattern": "putting off what matters",
     "targets": ["dx:antaraya-pramada", "dx:antaraya-alasya", "dx:pamada", "dx:guna-tamas", "dx:antaraya-styana",
                 "dx:nivarana-thina-middha"],
     "answers": {
         "q09": "I've been meaning to start a daily practice for a year. Every evening I tell myself tomorrow, and then I "
                "scroll my phone until it's late.",
         "q05": "When I sit down to study I tidy the desk, make tea, check messages, and the hour is gone before I open "
                "the book."}},
    {"id": "dev-08", "pattern": "holding on",
     "targets": ["dx:root-lobha", "dx:fetter-kamaraga", "dx:kasaya-lobha", "dx:klesa-raga", "dx:tanha"],
     "answers": {
         "q10": "I can't let go of the house I grew up in. When my siblings talk about selling it I argue for hours and "
                "refuse to sign anything."}},
    {"id": "dev-09", "pattern": "concealment",
     "targets": ["dx:kasaya-maya", "dx:gita-asuri-sampad"],
     "answers": {
         "q11": "At work I smile and agree in meetings and then say the opposite behind their backs. I hide what I really "
                "want from my family too, and I tell little lies so nobody sees it."}},
    {"id": "dev-10", "pattern": "dullness at practice",
     "targets": ["dx:nivarana-thina-middha", "dx:gk-laya", "dx:antaraya-styana", "dx:antaraya-alasya", "dx:guna-tamas"],
     "answers": {
         "q05": "As soon as I sit for meditation my mind goes dull and foggy and I sink into a kind of blank. I end up just "
                "waiting for the timer.",
         "q13": "I've tried chanting in the morning instead, but even then my mind is sluggish and I lose the thread."}},
]

# ---------------------------------------------------------------------------------------------------------------
# cue-writing rules (mechanical part)
# ---------------------------------------------------------------------------------------------------------------
_R = mapper.rules()["patterns"]
BUILD_CLIN = (r"depress|anxiety|anxious|disorder|trauma|adhd|\bocd\b|ptsd|bipolar|psychiatr|psycholog|therap|clinical|"
              r"neuro|symptom|syndrome|insomnia|addict|compulsi|obsessi|phobi|panic|burnout|\bstress|cognitive|dopamine|"
              r"hormone|mental illness|mental health|patient|\bcure|\bheal|treatment|personality type|introvert|"
              r"extrovert|self-esteem|diagnos")
BANNED = [
    ("clinical", re.compile(_R["clinical_terms"], re.I)),
    ("clinical", re.compile(BUILD_CLIN, re.I)),
    ("body", re.compile(_R["body_never"], re.I)),
    ("body/sleep", re.compile(_R["body_practice_only"], re.I)),
    ("breath", re.compile(_R["breath_difficulty"], re.I)),
    ("food", re.compile(_R["food"], re.I)),
    ("body/sleep", re.compile(r"\b(?:body|bodies|bodily|bed|beds|awake|woken|wake|waking|nod|nods|nodding|fast|fasting|"
                              r"diet|weight|health|healthy|sick|hunger|thirst\w*|appetite\w*|limbs?|sweet\w*|sour|"
                              r"bitter|smok\w*|faint\w*|binge\w*|nurse\w*)\b", re.I)),
    ("tradition-term", re.compile(_R["tradition_terms"], re.I)),
    ("tradition-term", re.compile(r"\b(?:samadhi|jhana|dhamma|dharma|nirvana|nibbana|karma|yoga|guna\w*|klesh?a\w*|"
                                  r"nivarana|sattva|rajas|tamas|kasaya|kashaya)\b", re.I)),
    ("hypothetical", re.compile(r"\b(?:if|would|could|might|should|shall|gonna|imagine|suppose)\b|'d\b|'ll\b", re.I)),
    ("hedge", re.compile(_R["hedge"], re.I)),
    ("generic", re.compile(r"\b(?:sometimes|occasionally|at times|now and then|life is|everyone|everybody)\b", re.I)),
    ("sarcasm", re.compile(_R["sarcasm_strong"], re.I)),
    ("sarcasm", re.compile(_R["sarcasm_weak"], re.I)),
    ("past-resolved", re.compile(_R["past_resolved"], re.I)),
    ("we", re.compile(r"\b(?:we|us|our|ours|we're|we've)\b", re.I)),
    ("punctuation", re.compile(r"[?!\"“”]")),
]
_WILL = re.compile(r"\bwill\b|\bwon't\b", re.I)
_HABIT = re.compile(_R["habitual_refusal"], re.I)
FIRST = re.compile(r"\b(?:i|i'm|i've|me|my|myself|mine)\b", re.I)


def lint(cue: str, entry: dict) -> list:
    out = []
    n = len(cue.split())
    if not 4 <= n <= 14:
        out.append(f"length {n}")
    if not FIRST.search(cue):
        out.append("not first person")
    for name, rx in BANNED:
        if rx.search(cue):
            out.append(f"{name}: {rx.search(cue).group(0)}")
    if _WILL.search(_HABIT.sub(" ", cue)):
        out.append("hypothetical: will/won't")
    names = set()
    for s in (entry.get("name", ""), entry.get("group", "")):
        base = re.split(r"\s*\(", s)[0]
        for w in re.findall(r"[^\W\d_]+", mapper.fold(base).lower()):
            if len(w) >= 4 and any(ord(c) > 127 for c in base):
                names.add(w)
    toks = {mapper.fold(t).lower() for t in re.findall(r"[^\W\d_]+", cue)}
    if toks & names:
        out.append(f"tradition-term (entry name): {sorted(toks & names)}")
    if len(mapper.content_stems(cue)) < 2:
        out.append(f"fewer than 2 content stems: {mapper.content_stems(cue)}")
    scr = safety.rule_screen(cue)
    if scr.flags or scr.route != "continue":
        out.append(f"safety: {scr.route} {sorted(scr.flags)}")
    return out


# ---------------------------------------------------------------------------------------------------------------
# layer helpers
# ---------------------------------------------------------------------------------------------------------------
def load_raw() -> list:
    return json.loads(DIAG.read_text(encoding="utf-8"))


def write_raw(raw: list) -> None:
    DIAG.write_text(json.dumps(raw, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    back = json.loads(DIAG.read_text(encoding="utf-8"))
    assert len(back) == len(raw)


def usable_layer(raw: list, strip_added: bool = False) -> dict:
    """The user-facing layer exactly as insight.ontology.diagnosis() builds it (optionally without cues_added)."""
    out = {}
    for e in raw:
        e2 = json.loads(json.dumps(e))
        if strip_added:
            for m in e2.get("markers") or []:
                add = set(m.get("cues_added") or [])
                m["cues"] = [c for c in m.get("cues") or [] if c not in add]
        c = ontology._clean_entry(e2)
        if c and c.get("definitions"):
            out[c["id"]] = c
    return out


def text_of(answers: dict) -> str:
    return " ".join(v for v in answers.values() if isinstance(v, str))


def reading_items(answers: dict, layer: dict, scr=None):
    inputs = {"answers": answers}
    scr = scr if scr is not None else safety.rule_screen(text_of(answers))
    R = mapper.Reading(inputs, scr, layer, None, None)
    if getattr(scr, "route", "continue") in ("stop_crisis", "decline_minor", "stop_unavailable"):
        return R, []
    mapper.rules_engine(R)
    return R, R.items


def cue_of(layer: dict, it) -> tuple:
    """(entry id, marker text, cue text or None) of an evidence item."""
    m = layer[it.eid]["markers"][it.marker_index]
    cue = m["cues"][it.cue_index] if it.cue_index is not None else None
    return it.eid, m["marker"], cue


def added_set(raw: list) -> set:
    return {(e["id"], m["marker"], c) for e in raw for m in e.get("markers") or [] for c in m.get("cues_added") or []}


def remove_cues(raw: list, which: dict) -> int:
    """which: {(eid, marker, cue): reason}. Removes only added cues. Returns count removed."""
    n = 0
    for e in raw:
        for m in e.get("markers") or []:
            for c in list(m.get("cues_added") or []):
                key = (e["id"], m["marker"], c)
                if key in which:
                    m["cues_added"].remove(c)
                    if c in m["cues"]:
                        m["cues"].remove(c)
                    n += 1
            if "cues_added" in m and not m["cues_added"]:
                del m["cues_added"]
    return n


def mapped(answers: dict, layer: dict) -> list:
    out = mapper.map_person({"answers": answers}, safety.rule_screen(text_of(answers)), engine="rules", layer=layer)
    return [(m["dx_id"], m["confidence"]) for m in out["mappings"]]


# ---------------------------------------------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="remove generic added cues and those behind bland mappings")
    args = ap.parse_args()

    raw = load_raw()
    by_id = {e["id"]: e for e in raw}
    layer = usable_layer(raw)
    cat = mapper.build_catalog(layer)
    added = added_set(raw)
    bland = [json.loads(l) for l in BLAND.read_text(encoding="utf-8").splitlines() if l.strip()]
    N = len(bland)
    limit = GENERIC_SHARE * N           # firing on MORE than 10% of the baseline is generic
    rep: dict = {"bland_people": N, "generic_threshold": f"> {GENERIC_SHARE:.0%} of {N} (>= {int(limit) + 1} people)"}

    # 1. lint
    lint_fail = {}
    for e in raw:
        for m in e.get("markers") or []:
            for c in m.get("cues_added") or []:
                p = lint(c, e)
                if p:
                    lint_fail[f"{e['id']} | {c}"] = p
            dup = [c for c in m.get("cues_added") or [] if (m.get("cues") or []).count(c) != 1]
            if dup:
                lint_fail[f"{e['id']} | duplicates"] = dup
            orig = [c for c in m.get("cues") or [] if c not in set(m.get("cues_added") or [])]
            if m.get("cues_added") and orig != (m.get("cues") or [])[:len(orig)]:
                lint_fail[f"{e['id']} | order"] = ["original cues are not kept first"]
    rep["lint_failures"] = lint_fail

    # counts of added cues per kind / markers covered
    per_kind = collections.Counter()
    per_marker = []
    for e in raw:
        if e["id"] not in cat.mappable:
            continue
        for m in e.get("markers") or []:
            k = len(m.get("cues_added") or [])
            per_kind[e["kind"]] += k
            if k:
                per_marker.append(k)
    rep["cues_added_total"] = sum(per_kind.values())
    rep["cues_added_by_kind"] = dict(sorted(per_kind.items()))
    rep["markers_with_added_cues"] = len(per_marker)
    rep["added_per_marker_min_max"] = [min(per_marker), max(per_marker)] if per_marker else None
    uf_markers = [(eid, m.text) for eid in cat.mappable for m in cat.markers[eid]]
    rep["user_facing_mappable_markers_without_added_cues"] = [
        f"{eid} | {t[:70]}" for eid, t in uf_markers
        if not any(m["marker"] == t and m.get("cues_added") for m in by_id[eid]["markers"])]

    # 2. self-test: each added cue as a sentence must give a direct item on its own marker
    self_fail = []
    for (eid, mtext, c) in sorted(added):
        if eid not in cat.mappable:
            self_fail.append(f"{eid} | {c} | entry not mappable/user-facing")
            continue
        sent = c[0].upper() + c[1:] + "."
        R, items = reading_items({"q14": sent}, layer, safety.rule_screen(sent))
        ok = any(it.eid == eid and layer[eid]["markers"][it.marker_index]["marker"] == mtext
                 and it.strength == "direct" for it in items)
        if not ok:
            codes = sorted({r["code"] for r in R.rejected if r["entry_id"] == eid})
            self_fail.append(f"{eid} | {c} | {codes or 'no direct item'}")
    rep["self_test_failures"] = self_fail

    # 3. bland baseline: people per cue
    fired = collections.defaultdict(set)
    marker_text_hits = collections.defaultdict(set)
    for p in bland:
        R, items = reading_items(p["answers"], layer)
        for it in items:
            eid, mtext, cue = cue_of(layer, it)
            if cue is None:
                marker_text_hits[(eid, mtext)].add(p["id"])
            else:
                fired[(eid, mtext, cue)].add(p["id"])
    generic = {k: sorted(v) for k, v in fired.items() if len(v) > limit}
    rep["cues_firing_on_bland"] = {f"{k[0]} | {k[2]}": sorted(v) for k, v in sorted(fired.items(), key=lambda x: -len(x[1]))}
    rep["marker_text_firing_on_bland"] = {f"{k[0]} | {k[1][:60]}": sorted(v) for k, v in marker_text_hits.items()}
    rep["generic_added_cues"] = [f"{k[0]} | {k[2]} | {len(v)}/{N}" for k, v in generic.items() if k in added]
    rep["generic_original_cues"] = [f"{k[0]} | {k[2]} | {len(v)}/{N}" for k, v in generic.items() if k not in added]

    # 4. bland mappings
    bland_maps = {}
    behind = {}
    for p in bland:
        ms = mapped(p["answers"], layer)
        if ms:
            bland_maps[p["id"]] = ms
            R, items = reading_items(p["answers"], layer)
            for it in items:
                if it.eid in {x[0] for x in ms}:
                    k = cue_of(layer, it)
                    if k in added:
                        behind[k] = f"behind a bland mapping ({p['id']})"
    rep["bland_mappings"] = bland_maps

    # 5. dev recall, before (cues_added stripped) and after
    before_layer = usable_layer(raw, strip_added=True)
    dev_rep = []
    for d in DEV:
        after = mapped(d["answers"], layer)
        before = mapped(d["answers"], before_layer)
        hit = [x for x in after if x[0] in d["targets"]]
        hit_b = [x for x in before if x[0] in d["targets"]]
        dev_rep.append({"id": d["id"], "pattern": d["pattern"], "target_hit_after": bool(hit),
                        "target_hit_before": bool(hit_b), "after": after, "before": before})
    rep["dev"] = dev_rep
    rep["dev_recall_after"] = f"{sum(1 for x in dev_rep if x['target_hit_after'])}/{len(DEV)}"
    rep["dev_recall_before"] = f"{sum(1 for x in dev_rep if x['target_hit_before'])}/{len(DEV)}"
    rep["dev_confidence_after"] = dict(collections.Counter(
        max((c for _, c in x["after"] if _ in d["targets"]), key=["low", "moderate", "high"].index, default="none")
        for x, d in zip(dev_rep, DEV)))

    # apply
    removed_now = {}
    if args.apply:
        for k, v in generic.items():
            if k in added:
                removed_now[k] = f"generic: fires on {len(v)}/{N} bland people ({', '.join(sorted(v))})"
        for k, why in behind.items():
            removed_now.setdefault(k, why)
        if removed_now:
            n = remove_cues(raw, removed_now)
            write_raw(raw)
            prev = json.loads(REMOVED.read_text(encoding="utf-8")) if REMOVED.exists() else []
            have = {(r["id"], r["marker"], r["cue"]) for r in prev}
            for (eid, mtext, c), why in removed_now.items():
                if (eid, mtext, c) not in have:
                    prev.append({"id": eid, "marker": mtext, "cue": c, "reason": why})
            REMOVED.write_text(json.dumps(prev, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            rep["removed_this_run"] = n
    rep["removed_this_run_list"] = [f"{k[0]} | {k[2]} | {v}" for k, v in removed_now.items()]
    rep["removed_total"] = len(json.loads(REMOVED.read_text(encoding="utf-8"))) if REMOVED.exists() else 0

    REPORT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    show = ["cues_added_total", "cues_added_by_kind", "markers_with_added_cues", "added_per_marker_min_max",
            "generic_added_cues", "generic_original_cues", "bland_mappings", "dev_recall_before", "dev_recall_after",
            "dev_confidence_after", "removed_this_run_list", "removed_total"]
    for k in show:
        print(k, json.dumps(rep.get(k), ensure_ascii=False))
    print("lint_failures", len(lint_fail), "| self_test_failures", len(self_fail),
          "| uf mappable markers without added cues", len(rep["user_facing_mappable_markers_without_added_cues"]))
    for x in dev_rep:
        print(" ", x["id"], x["pattern"], "| before:", x["before"], "| after:", x["after"])
    bad = bool(lint_fail) or bool(self_fail) or bool(bland_maps) or bool(rep["generic_added_cues"])
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
