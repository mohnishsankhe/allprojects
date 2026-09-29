#!/usr/bin/env python3
"""Practice-safety judge fixes (P6) on layers/practices.json. Idempotent. build.py runs it after the last overrides.py.

Source of every change: the P5 practice-safety judge (onto-judge, 2026-09-29), eval/judge/practice_safety.jsonl and
eval/judge/PRACTICE_SAFETY.md; the demotions and the uttama exclusion are recorded in DECISIONS 2026-09-30 00:01.
Each fix edits entries by px id and carries a one-line reason that names the judge's verdict.

Why warnings are cleaned: insight/report.py prints every warning as "The texts' caution: ...", so a warning must be
the texts' own caution. Product notes go to tier_reason, which the app never renders.

    python3 judge_fixes.py            # apply, validate, write
    python3 judge_fixes.py --check    # apply in memory and validate only; do not write
Exits non-zero on any error: an expected source text that is missing (the layer drifted) or a failed check.
"""
import copy
import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)
from insight import ontology as O, claims  # noqa: E402

PX = os.path.join(ROOT, "layers", "practices.json")
FIELDS = ["id", "name", "lens", "ontology_refs", "tradition", "summary", "steps", "targets", "stage", "duration",
          "warnings", "safety_tier", "tier_reason", "cites", "user_facing"]
# the summary-only duration used by every other non-gentle entry (same dict as refresh_p1.NONE_DUR)
NONE_DUR = {"minutes_per_session": None, "sessions_per_day": None,
            "basis": "not set: summary only; the product gives no length for a practice it does not guide"}
UTTAMA_EXCLUSION = "their only real step rests on the Daśavaikālika 8.36–38 entry, still skeleton"
DEMOTED_NOTE = " Earlier tier: gentle; demoted by the practice-safety judge (P5; DECISIONS 2026-09-30)."

errors = []
log = []  # (px id, reason, what changed)


def ts(*v):
    return [f"tea:tattvartha-sutra:{x}" for x in v]


TS_ARTA = ts("9.30", "9.31", "9.32", "9.33")  # the four sūtras, in place of the superseded skeleton range 9.30-33


# ------------------------------------------------------------------ idempotent edit helpers (each returns a note or None)
def set_field(p, key, value):
    if p.get(key) == value:
        return None
    p[key] = copy.deepcopy(value)
    return f"{key} set"


def replace_step(p, olds, new):
    if new in p["steps"]:
        return None
    for old in olds:
        if old in p["steps"]:
            p["steps"] = [new if s == old else s for s in p["steps"]]
            return f"step replaced: {old[:50]!r}"
    errors.append(f"{p['id']}: none of the expected steps found for {new[:60]!r}")
    return None


def delete_step(p, old, done_marker):
    """done_marker: a substring that must not remain in any step once the fix is in (so drift is caught)."""
    if old in p["steps"]:
        p["steps"] = [s for s in p["steps"] if s != old]
        return f"step deleted: {old[:50]!r}"
    if any(done_marker in s for s in p["steps"]):
        errors.append(f"{p['id']}: step with {done_marker!r} present but not in the expected wording")
    return None


def _find_w(p, prefix):
    return [w for w in p["warnings"] if w["text"].startswith(prefix)]


def drop_warning(p, prefix):
    hit = _find_w(p, prefix)
    if not hit:
        return None
    p["warnings"] = [w for w in p["warnings"] if not w["text"].startswith(prefix)]
    return f"warning deleted: {prefix[:50]!r}"


def move_warning(p, prefix, note=None):
    """Take a product note out of the warnings and keep it in tier_reason (note defaults to the warning's text)."""
    hit = _find_w(p, prefix)
    if not hit:
        return None
    text = note or hit[0]["text"]
    p["warnings"] = [w for w in p["warnings"] if not w["text"].startswith(prefix)]
    if text not in p["tier_reason"]:
        p["tier_reason"] = p["tier_reason"].rstrip() + " " + text
    return f"warning moved to tier_reason: {prefix[:50]!r}"


def set_warning(p, old_prefix, new_text, cites=None):
    cur = [w for w in p["warnings"] if w["text"] == new_text]
    if cur:
        w = cur[0]
    else:
        hit = _find_w(p, old_prefix)
        if not hit:
            errors.append(f"{p['id']}: warning starting {old_prefix[:50]!r} not found")
            return None
        w = hit[0]
    changed = []
    if w["text"] != new_text:
        w["text"] = new_text
        changed.append("text")
    if cites is not None and w["cites"] != cites:
        w["cites"] = list(cites)
        changed.append("cites")
    return f"warning {'+'.join(changed)} set: {new_text[:50]!r}" if changed else None


def set_warning_cites(p, prefix, cites):
    hit = _find_w(p, prefix)
    if not hit:
        errors.append(f"{p['id']}: warning starting {prefix[:50]!r} not found")
        return None
    if hit[0]["cites"] == cites:
        return None
    hit[0]["cites"] = list(cites)
    return f"warning cites set: {prefix[:40]!r} -> {cites}"


def add_warning(p, w, pos=0):
    if any(x["text"] == w["text"] for x in p["warnings"]):
        return None
    p["warnings"].insert(pos, copy.deepcopy(w))
    return f"warning added: {w['text'][:50]!r}"


def replace_text(p, field, old, new):
    if old in p[field]:
        p[field] = p[field].replace(old, new)
        return f"{field}: replaced {old[:50]!r}"
    if new and new in p[field]:
        return None
    if not new:  # a pure deletion: absent means done
        return None
    errors.append(f"{p['id']}: {field} holds neither {old[:50]!r} nor {new[:50]!r}")
    return None


def append_reason(p, text):
    if text in p["tier_reason"]:
        return None
    p["tier_reason"] = p["tier_reason"].rstrip() + " " + text
    return "tier_reason appended"


def drop_cite(p, c):
    if c not in p["cites"]:
        return None
    p["cites"] = [x for x in p["cites"] if x != c]
    return f"cite dropped: {c}"


def add_cite(p, c, after=None):
    if c in p["cites"]:
        return None
    i = p["cites"].index(after) + 1 if after in p["cites"] else len(p["cites"])
    p["cites"].insert(i, c)
    return f"cite added: {c}"


def demote(p, reason_text, stage=None):
    out = [set_field(p, "safety_tier", "needs-teacher"), set_field(p, "steps", []), set_field(p, "duration", NONE_DUR),
           set_field(p, "tier_reason", reason_text)]
    if stage:
        out.append(set_field(p, "stage", stage))
    return out


# ------------------------------------------------------------------ the texts' own teacher conditions (new warnings)
W_ANAPANA_TEACHER = {
    "text": "The Visuddhimagga gives this first tetrad as the beginner's subject and has it learned from a teacher in "
            "five links (learning, questioning, establishing, absorption and the characteristic); the meditator then "
            "attends to it 'not forgetting a single word of the teacher's teaching' (Vism VIII p.277–278).",
    "cites": ["tea:visuddhimagga:8.p277/2", "tea:visuddhimagga:8.p278"]}
_METTA_COND = ("The Visuddhimagga addresses the development of loving-kindness to a beginner who has cut the impediments "
               "and taken the subject (IX p.295). The subject is taken by approaching a good friend who gives a "
               "meditation subject (III p.89/3); loving-kindness is named as the universal subject, and the one who "
               "gives it is the good friend (kalyāṇamitta) (III p.97/3, p.98/2).")
_METTA_CITES = ["tea:visuddhimagga:9.p295", "tea:visuddhimagga:3.p89/3", "tea:visuddhimagga:3.p97/3",
                "tea:visuddhimagga:3.p98/2"]
W_METTA_TEACHER = {"text": _METTA_COND, "cites": _METTA_CITES}
W_RECALL_TEACHER = {"text": "This is a step within that development. " + _METTA_COND, "cites": _METTA_CITES}


# ------------------------------------------------------------------ the fixes, by px id
def fix_inward(p):
    return demote(p, (
        "Needs a teacher by the text's own statement: the Upaniṣad says the understanding of the self, toward which "
        "this turning of the sight is directed, is not reached by reasoning, and unless taught by another there is no "
        "way to it (KU 1.2.8–9). The ontology tags KU 2.1.1 as advanced, and 'turning the sight back' could be taken "
        "as an eye technique, which the layer leaves to a teacher (as with the HYP śāmbhavī seal). This matches the "
        "Oṃ meditation (px:omkara-upasana-mau-8-12) and KU 1.3.13 (px:katha-inward-withdrawal-1-3-13) entries, which "
        "rest on the same caution. The verse says only that 'a certain wise one' saw the self; it does not promise "
        "that turning the sight inward brings this seeing." + DEMOTED_NOTE), stage="advanced") + [
        drop_warning(p, "The verse says only that 'a certain wise one' saw the self")]


def fix_anapana(p):
    return demote(p, (
        "Needs a teacher by the commentary's own statement: the Visuddhimagga gives the first tetrad as the beginner's "
        "subject and has it learned from a teacher in five links (Vism VIII p.277–278), the same ground on which the "
        "layer leaves the Visuddhimagga's breath-counting to a teacher. It also calls this subject weighty and asks "
        "for strong mindfulness (Vism VIII, PTS p.284). The sutta's first tetrad asks one to know the breath, long or "
        "short, and to experience the whole body, and goes on to training in stilling the bodily process (MN 118:18); "
        "no steps are given." + DEMOTED_NOTE)) + [
        drop_warning(p, "The sutta asks only that one know the breath as it is"),
        add_warning(p, W_ANAPANA_TEACHER, pos=len(p["warnings"]))]


def fix_metta(p):
    return demote(p, (
        "Needs a teacher by the text's own statement: Vism IX p.295 addresses the beginner who has 'taken the subject' "
        "(gahitakammaṭṭhāna), and Vism III has the subject received from a good friend who gives a meditation subject "
        "(p.89/3), names loving-kindness as the universal subject (p.97/3) and calls the one who gives either kind the "
        "good friend (p.98/2). Friendliness stays open to users through the gentle YS 1.33 "
        "(px:maitri-bhavana-ys-1-33) and TS 7.11 (px:maitri-pramoda-karunya-madhyastha-ts-7-11) entries."
        + DEMOTED_NOTE)) + [
        replace_text(p, "summary", "Vism IX: the beginner, in a secluded place,",
                     "Vism IX: the beginner who has cut the impediments and taken the subject, in a secluded place,"),
        add_warning(p, W_METTA_TEACHER, pos=0)]


def fix_recall(p):
    return demote(p, (
        "Needs a teacher by the text's own statement: this is a step within the Visuddhimagga's development of "
        "loving-kindness, which it addresses to a beginner who has taken the subject (IX p.295) from a good friend who "
        "gives a meditation subject (III p.89/3, p.97/3, p.98/2), as for px:metta-bhavana-vism-9. The Visuddhimagga's "
        "graphic stories and body analysis (IX p.302–306) are left out, and IX p.300 is not cited (it also carries "
        "imagery of the hells). It is not advice to stay in ongoing harm: a reading that mentions abuse is stopped by "
        "the safety screen (SAFETY.md)." + DEMOTED_NOTE)) + [
        drop_warning(p, "The Visuddhimagga's further means include stories of great bodily harm"),
        drop_cite(p, "tea:visuddhimagga:9.p300"),
        add_warning(p, W_RECALL_TEACHER, pos=0)]


ARTA_PREFIX = "Nearest general caution in the Tattvārtha (the sūtra gives none for this practice): reflection must not"


def fix_uttama(p):
    return [set_field(p, "user_facing", False), set_field(p, "manual_exclusion", UTTAMA_EXCLUSION),
            set_warning_cites(p, ARTA_PREFIX, TS_ARTA)]


def fix_sauca(p):
    return fix_uttama(p) + [
        set_warning(p, "The sūtra gives only the name; the pairing with greed is the commentaries' reading",
                    "The sūtra gives only the name; the Daśavaikālika names contentment, not śauca, against greed."),
        replace_text(p, "summary", "The sūtra gives no method; the ontology's reading of śauca here as purity from "
                                   "greed follows the commentaries (it is not bodily washing). ",
                     "The sūtra gives no method. ")]


def fix_pratipaksa(p):
    return [drop_warning(p, "Vyāsa's illustrations of the fruit of violence include births in hells"),
            append_reason(p, "Vyāsa's illustrations of the fruit of violence, which include births in hells (YB 2.34), "
                             "are left out of the steps and the cautions; the steps keep only the sūtra's own "
                             "reflection.")]


def fix_guarding(p):
    assert "The chapter's verse on the body's end is left out." in p["tier_reason"]
    return [drop_warning(p, "The chapter goes on to a verse on the body lying discarded on the earth")]


def fix_abhyasa_ys(p):
    return [replace_step(p, ["Return to the effort toward stability without strain; relax effort, as the sūtra says of "
                             "posture (YS 2.47)."],
                         "Return to the effort toward stability, without strain (YS 1.13); keep the posture easy, with "
                         "effort relaxed (YS 2.47)."),
            drop_cite(p, "tea:yoga-bhasya:1.11")]


def fix_ekatattva(p):
    return [replace_step(p, ["Choose one object and let the mind rest on it alone (YS 1.32 with Vyāsa: "
                             "ekatattvāvalambana)."],
                         "Choose one object for the mind to rest on. Hold it in mind; it is not a fixed gaze and not a "
                         "mantra (YS 1.32 with Vyāsa)."),
            replace_step(p, ["Keep the effort light: the effort toward stability is itself the practice (YS 1.13)."],
                         "Return to the effort toward stability, without strain; that effort is itself the practice "
                         "(YS 1.13)."),
            move_warning(p, "Vyāsa's gloss says only 'one principle'; the product does not choose")]


def fix_yathabhimata(p):
    return [replace_step(p, ["Choose one object that is agreeable to you (yathābhimata) (YS 1.39)."],
                         "Choose one agreeable object to hold in mind: not something you crave, and not a fixed gaze "
                         "at a light or the sun (YS 1.39; 1.15)."),
            set_warning(p, "Dispassion, the partner of practice (YS 1.12), is freedom from thirst",
                        "Dispassion, the partner of practice (YS 1.12), is freedom from thirst for objects seen or "
                        "heard of (YS 1.15 with Vyāsa)."),
            add_cite(p, "tea:yoga-sutra:1.15", after="tea:yoga-bhasya:1.39")]


def fix_bg635(p):
    # The judge's reword, with 'can be attained' for śakyo 'vāptum (6.36: 'it can be attained'), so that the
    # caution does not read as a promise.
    return [set_warning(p, "The Gītā itself grants that the mind is hard to restrain; it is held over time",
                        "The Gītā grants that the mind is hard to restrain; it is held by practice and dispassion "
                        "(6.35), and yoga can be attained by one who strives through the right means (6.36).",
                        cites=["tea:bhagavad-gita:6.35", "tea:bhagavad-gita:6.36"])]


def fix_surge(p):
    return [replace_step(p, ["Bear it (soḍhum) without acting from it: contacts that give pleasure and pain come and "
                             "go and are impermanent; endure them (5.23; 2.14)."],
                         "Bear the surge without acting from it (5.23); the Gītā says such contacts come and go and "
                         "are impermanent (2.14).")]


def fix_sreyas(p):
    return [set_warning(p, "The Upaniṣad calls the path sharp as a razor's edge and hard to cross, and bids one",
                        "The Upaniṣad calls the path sharp as a razor's edge, hard to cross and difficult to tread "
                        "(KU 1.3.14).", cites=["tea:katha-upanisad:1.3.14"])]


def fix_ts711(p):
    return [set_warning(p, "The sūtra pairs each attitude with its own object: equanimity, not argument",
                        "The sūtra pairs each attitude with its own object: friendliness toward all living beings, "
                        "delight toward those superior in virtue, compassion toward the afflicted, and equanimity "
                        "toward the undisciplined (TS 7.11).", cites=["tea:tattvartha-sutra:7.11"]),
            # same rule as the judge's criterion 2, applied to W2's second clause (a product note, not the sūtra's)
            set_warning(p, "In the sūtra these attitudes serve the steadiness of the vows; the vows themselves",
                        "In the sūtra these attitudes serve the steadiness of the vows (TS 7.1; 7.3).",
                        cites=["tea:tattvartha-sutra:7.3", "tea:tattvartha-sutra:7.1"]),
            append_reason(p, "The vows themselves are not taken through the product.")]


def fix_anupreksa(p):
    assert "leave out the reflections on the body's impurity" in p["tier_reason"]
    return [replace_step(p, ["Reflect on aloneness (ekatva) and on otherness (anyatva), as the sūtra names them "
                             "(TS 9.7); the commentaries read otherness as the self being other than the body.",
                             "Reflect on aloneness (ekatva) and on otherness (anyatva): the self is other than the "
                             "body (TS 9.7)."],
                         "Reflect on aloneness (ekatva) and on otherness (anyatva), as the sūtra names them (TS 9.7)."),
            replace_text(p, "summary", " (the commentaries read these as the otherness of self and body and the "
                                       "impurity of the body)", ""),
            set_warning_cites(p, ARTA_PREFIX, TS_ARTA),
            # W2 is a product note; tier_reason already says the same, so it is only removed from the warnings
            drop_warning(p, "The steps keep five of the sūtra's twelve reflections")]


def fix_speech(p):
    return [delete_step(p, "Once a day, spend a few minutes reciting a text you hold sacred (svādhyāya-abhyasana) "
                           "(BhG 17.15).", done_marker="reciting"),
            replace_text(p, "tier_reason", "Care in speech and a short daily recitation;", "Care in speech;"),
            append_reason(p, "The Gītā also counts the practice of recitation (svādhyāya-abhyasana) as austerity of "
                             "speech (17.15); it is not made a step, because this layer leaves recitation and mantra "
                             "practice to a teacher (px:pranava-japa-ys-1-27-29)."),
            move_warning(p, "The Gītā's austerity of the body (17.14) includes celibacy")]


def fix_not_harbouring(p):
    return [drop_warning(p, "The Visuddhimagga (a later Theravāda manual) advises that if resentment rises"),
            append_reason(p, "The Visuddhimagga's advice for resentment (IX p.298) belongs to its loving-kindness "
                             "method, which the layer leaves to a teacher (px:metta-bhavana-vism-9), so it is not "
                             "given here.")]


FIXES = [
    # 1. demotions to needs-teacher (the text's own statement that a teacher is needed)
    ("px:inward-turned-gaze-ku-2-1-1", fix_inward,
     "judge: demote; own W2 cites KU 1.2.8-9 'unless taught by another', KU 2.1.1 tagged advanced; W1 is a product note"),
    ("px:anapanasati-first-tetrad", fix_anapana,
     "judge: demote; Vism VIII p.277-278 has the subject learned from a teacher in five links; W2 a misstated product note"),
    ("px:metta-bhavana-vism-9", fix_metta,
     "judge: demote; Vism IX p.295 'taken the subject', III p.89/3, p.97/3, p.98/2 give it from a good friend"),
    ("px:recalling-the-good-in-one-who-wronged-vism-9", fix_recall,
     "judge: demote (step within Vism IX mettā); at any tier delete W2 (bodily harm) and drop cite p.300 (hells)"),
    # 2. substantive: uttama entries rest on a skeleton teaching; excluded by hand until it is verified
    ("px:uttama-ksama-ts-9-6", fix_uttama,
     "judge: substantive; S4 rests only on skeleton Daśavaikālika 8.36-38 -> user_facing false; cite TS 9.30-9.33"),
    ("px:uttama-mardava-ts-9-6", fix_uttama,
     "judge: substantive; S4 rests only on skeleton Daśavaikālika 8.36-38 -> user_facing false; cite TS 9.30-9.33"),
    ("px:uttama-arjava-ts-9-6", fix_uttama,
     "judge: substantive; S4 rests only on skeleton Daśavaikālika 8.36-38 -> user_facing false; cite TS 9.30-9.33"),
    ("px:uttama-sauca-ts-9-6", fix_sauca,
     "judge: substantive as above; also delete the unsourced 'commentaries' reading' of śauca"),
    # 3. editorial
    ("px:pratipaksa-bhavana-ys-2-33", fix_pratipaksa,
     "judge: W2 (YB 2.34 hells) is a product note with hell imagery -> delete; keep only in tier_reason"),
    ("px:guarding-the-mind-dhp-33-36", fix_guarding,
     "judge: W2 (Dhp 41 body discarded) is a product note with death imagery -> delete; tier_reason already has it"),
    ("px:abhyasa-vairagya-ys-1-12", fix_abhyasa_ys,
     "judge: S4 carried YS 2.47 (posture) over to the mind's effort -> judge's wording; drop cite YB 1.11"),
    ("px:ekatattva-abhyasa-ys-1-32", fix_ekatattva,
     "judge: S2 must bound the open object (no fixed gaze, no mantra); S4 drop 'Keep the effort light'; W3 product note"),
    ("px:yathabhimata-dhyana-ys-1-39", fix_yathabhimata,
     "judge: S2 bound the object (nothing craved, no fixed gaze at light or sun); W1 drop the inferred last clause"),
    ("px:abhyasa-vairagya-bg-6-35", fix_bg635,
     "judge: W3 'over time, not at once' is not in BhG 6.35-6.36 -> reworded to the verses"),
    ("px:bearing-the-surge-bg-5-23", fix_surge,
     "judge: S3 'endure them' could be read as enduring bodily pain -> limited to the surge"),
    ("px:sreyas-preyas-viveka-ku-1-2-2", fix_sreyas,
     "judge: W1 'approaching the excellent ones' is not the verified KU 1.3.14 -> razor's-edge line only"),
    ("px:maitri-pramoda-karunya-madhyastha-ts-7-11", fix_ts711,
     "judge: W1 misstated TS 7.11 (friendliness is toward all beings; nothing of argument) -> the four pairings; "
     "W2's product-note clause -> tier_reason (criterion 2 rule)"),
    ("px:anupreksa-ts-9-7", fix_anupreksa,
     "judge: S3 unverified commentary gloss deleted (and in summary); W1 cite TS 9.30-9.33 separately; W2 product note"),
    ("px:speech-that-does-not-agitate-bg-17-15", fix_speech,
     "judge: S5 daily recitation widens svādhyāya and sits on the teacher line -> deleted; W3 product note"),
    ("px:satipatthana-citta-contemplation-mn10-34", lambda p: [move_warning(p, "The steps stop at the first four pairs")],
     "judge: W3 is a product note, not the texts' caution -> tier_reason"),
    ("px:vitaraga-citta-ys-1-37", lambda p: [move_warning(p, "The sūtra and Vyāsa name no person; the product does not")],
     "judge: W1 is a product note, not the texts' caution -> tier_reason"),
    ("px:anitya-anupreksa-ts-9-7", lambda p: [move_warning(p, "This reflection is on impermanence, not on death.")],
     "judge: W2 is a product note, not the texts' caution -> tier_reason"),
    ("px:asrava-samvara-anupreksa-ts-9-7",
     lambda p: [move_warning(p, "The sūtra's means of stopping also include the conquest of hardships")],
     "judge: W2 is a product note, not the texts' caution -> tier_reason"),
    ("px:seeing-harm-in-the-faults-ts-7-9-10",
     lambda p: [move_warning(p, "The steps name four of the sūtra's five faults")],
     "judge: W3 is a product note, not the texts' caution -> tier_reason"),
    # judge's conditional note on a passing entry, triggered by the mettā demotion above
    ("px:not-harbouring-the-grievance-dhp-3-5", fix_not_harbouring,
     "judge note: if mettā is demoted, W2 (Vism IX p.298) points to the teacher-conditioned method -> removed"),
]

DEMOTED = FIXES[0][0], FIXES[1][0], FIXES[2][0], FIXES[3][0]
UTTAMA = tuple(f[0] for f in FIXES[4:8])


# ------------------------------------------------------------------ validation (all by code)
PRODUCT_NOTE = re.compile(r"\bproduct\b|not part of these steps|\bleft out\b|\bthe steps (keep|stop|name|are)\b|"
                          r"on purpose|\bthese steps\b", re.I)
DANGER = ("mercury", "metal", "cutting the body", "breath retention", "kumbhaka", "sexual", "fast for", "prolonged fast",
          "fasting for")  # tests/test_schema_layers.py
CLIN = re.compile(r"\b(cure[sd]?|curing|heal\w*|treat\w*|therap\w*|symptom\w*|anxiety|anxious|depress\w*|stress[- ]relief|"
                  r"lowers?|reduces?|diagnos\w*|disorder\w*|patient\w*|clinical\w*|medical\w*|health\w*|mental illness|"
                  r"wellness)\b", re.I)  # same pattern as build.py


def cites_of(e):
    return list(e["cites"]) + [c for w in e["warnings"] for c in w["cites"]]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


def validate(P, touched):
    errs, info = [], []
    by = {p["id"]: p for p in P}
    nd = Counter(json.dumps(p["duration"], ensure_ascii=False) for p in P if p["safety_tier"] != "gentle")
    for pid in touched:
        e = by[pid]
        extra = [k for k in e if k not in FIELDS]
        if [k for k in e if k in FIELDS] != FIELDS or extra not in ([], ["manual_exclusion"]):
            errs.append(f"{pid}: field order/keys {list(e)}")
        if extra and not e.get("manual_exclusion"):
            errs.append(f"{pid}: empty manual_exclusion")
        bad = sorted({c for c in cites_of(e) if not O.citable(c)})
        if bad and not e.get("manual_exclusion"):
            errs.append(f"{pid}: cites not citable {bad}")
        elif bad:
            info.append(f"{pid}: manual exclusion; not citable: {bad}")
        if not any(O.citable(c) for w in e["warnings"] for c in w["cites"]):
            errs.append(f"{pid}: no warning with a citable cite")
        if any(not w["text"].strip() or not w["cites"] for w in e["warnings"]):
            errs.append(f"{pid}: empty or uncited warning")
        if e["safety_tier"] == "gentle":
            if not 3 <= len(e["steps"]) <= 6:
                errs.append(f"{pid}: gentle with {len(e['steps'])} steps")
            txt = " ".join([e["name"], e["summary"]] + e["steps"]).lower()
            if [d for d in DANGER if d in txt]:
                errs.append(f"{pid}: danger words")
        elif e["steps"]:
            errs.append(f"{pid}: non-gentle entry with steps")
        for w in e["warnings"]:
            m = PRODUCT_NOTE.search(w["text"])
            if m and e.get("manual_exclusion"):
                info.append(f"{pid}: excluded, but a warning reads as a product note ({m.group(0)!r}); move it before "
                            f"the entry is re-enabled: {w['text'][:60]!r}")
            elif m and e["safety_tier"] == "gentle":
                errs.append(f"{pid}: warning still reads as a product note ({m.group(0)!r}): {w['text'][:70]!r}")
        for h in claims.scan_fields({k: e[k] for k in ("name", "summary", "steps", "warnings", "tier_reason")}):
            errs.append(f"{pid}: claims hit {h['category']}: {h['match']!r}")
        for s in strings(e):
            m = CLIN.search(s)
            if m:
                errs.append(f"{pid}: clinical/health word {m.group(0)!r}")
    for pid in DEMOTED:
        e = by[pid]
        if (e["safety_tier"], e["steps"], e["duration"]) != ("needs-teacher", [], NONE_DUR):
            errs.append(f"{pid}: not demoted to the summary-only needs-teacher form")
        if json.dumps(NONE_DUR, ensure_ascii=False) != nd.most_common(1)[0][0]:
            errs.append("NONE_DUR differs from the layer's usual summary-only duration")
        if "teacher" not in e["tier_reason"]:
            errs.append(f"{pid}: tier_reason does not give the teacher ground")
    for pid in UTTAMA:
        e = by[pid]
        if e.get("user_facing") is not False or e.get("manual_exclusion") != UTTAMA_EXCLUSION:
            errs.append(f"{pid}: not manually excluded")
        if "tea:tattvartha-sutra:9.30-33" in cites_of(e):
            errs.append(f"{pid}: still cites the skeleton range 9.30-33")
    # whole layer: every practice keeps at least one warning with a citable cite (reported; errors only for touched)
    no_w = [p["id"] for p in P if not any(O.citable(c) for w in p["warnings"] for c in w["cites"])]
    if no_w:
        info.append(f"entries (not touched here) without a citable warning: {no_w}")
    return errs, info


def main():
    P = json.load(open(PX, encoding="utf-8"))
    before_gentle = set(O.gentle_practices())
    by = {p["id"]: p for p in P}
    missing = [pid for pid, _, _ in FIXES if pid not in by]
    if missing:
        print("ERR px ids not in the layer:", missing)
        sys.exit(1)
    for pid, fn, reason in FIXES:
        notes = [n for n in fn(by[pid]) if n]
        log.append((pid, reason, notes))
    touched = [pid for pid, _, _ in FIXES]
    errs, info = validate(P, touched)
    errors.extend(errs)
    n_changed = sum(1 for _, _, n in log if n)
    for pid, reason, notes in log:
        print(("CHANGED " if notes else "ok      ") + pid + " | " + reason)
        for n in notes:
            print("         -", n)
    for x in info:
        print("INFO", x)
    if errors:
        for x in errors:
            print("ERR", x)
        print("judge_fixes: entries changed:", n_changed, "| errors:", len(errors))
        sys.exit(1)
    if "--check" not in sys.argv:
        with open(PX, "w", encoding="utf-8") as fh:
            fh.write(json.dumps(P, indent=1, ensure_ascii=False) + "\n")
        O.reset_caches()
        after = O.gentle_practices()
        leaked = [pid for pid in DEMOTED + UTTAMA if pid in after]
        raw = {p["id"]: p for p in json.load(open(PX, encoding="utf-8"))}
        dropped = {pid: sorted(c for c in cites_of(raw[pid]) if not O.citable(c)) for pid in after}
        dropped = {k: v for k, v in dropped.items() if v}
        if leaked or dropped:
            print("ERR after write: demoted/excluded still gentle-usable:", leaked, "| gentle cites dropped by loader:",
                  dropped)
            sys.exit(1)
        print("written:", PX)
        print("gentle usable before/after:", len(before_gentle), len(after),
              "| per lens after:", dict(Counter(v["lens"] for v in after.values())))
    else:
        print("check only; nothing written")
    print("judge_fixes: entries changed:", n_changed, "| errors: 0")


if __name__ == "__main__":
    main()
