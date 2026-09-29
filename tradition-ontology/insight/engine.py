"""Person-map pipeline: intake -> safety screen (first) -> mapping -> two-lens synthesis -> pathway -> report.

Two engines share this pipeline and the same validators:
- 'rules': deterministic, offline (cue matching, templated synthesis from the layers, rule-based pathway);
- 'model': the Claude API steps in config/model_routing.json (needs ANTHROPIC_API_KEY).
If a model step fails, the pipeline falls back to the rules engine for that step and says so in the report.
"""
from __future__ import annotations

import re
import time
from typing import Optional

from . import claims, ontology, safety, specificity
from .llm import Ledger, ModelClient


INSUFFICIENT = {
    None: ("This reading did not find, in what you wrote, a pattern the texts describe closely enough to say anything "
           "honest about. There are two possible reasons, and this reading cannot tell them apart: there may be nothing "
           "here to name, or it may be a limit of this reading, which only speaks when your words clearly fit a "
           "description in the texts. Either way it is not a judgement about you. If you like, add a few sentences in "
           "your own words about what troubles you: when it happens, what goes through your mind, and what you do next."),
    "short": ("What you shared is short, and this reading did not find in it a pattern the texts describe closely "
              "enough to name. There may be nothing here to name, or there may not yet be enough to go on. It is not a "
              "judgement about you. If you like, add a few sentences about a recent situation: what happened, what "
              "went through your mind, and what you did next."),
    "not_enough_own_words": ("There is not yet enough of your own writing for a reading: it needs at least a few "
                             "sentences. If you like, describe a recent situation: what happened, what went through "
                             "your mind, and what you did next."),
    "dialogue_speaker_unresolved": ("To use a pasted conversation, please tell us which speaker label is you "
                                    "(for example 'Me'). We never guess."),
    "language_not_supported": "This first version reads English only. Please write your answers in English.",
}


def _audit_summary(audit: dict) -> dict:
    """Counts and codes only: the mapper's full audit holds some of the person's words and never leaves the mapper."""
    from collections import Counter
    rej = audit.get("rejected") or []
    return {"unmapped_reason": audit.get("unmapped_reason"),
            "rejected_by_code": dict(Counter(r.get("code") for r in rej if isinstance(r, dict))),
            "counter_only_entries": list(audit.get("counter_only_entries") or []),
            "excluded_entries": [e if isinstance(e, str) else e.get("entry_id") for e in audit.get("excluded_entries") or []]}


def build_segments(inputs: dict) -> list[dict]:
    """The person's own words, as quotable segments with their origin. Dialogue: only the person's lines."""
    segs = []
    for qid, ans in (inputs.get("answers") or {}).items():
        if isinstance(ans, str) and ans.strip():
            segs.append({"id": f"a:{qid}", "source": qid, "text": ans.strip()})
    if (inputs.get("free_text") or "").strip():
        segs.append({"id": "free", "source": "free_text", "text": inputs["free_text"].strip()})
    dlg = inputs.get("dialogue") or ""
    if dlg.strip():
        # same parser as the mapper: timestamps and [date, time] prefixes, continuation lines, self-speaker aliases
        from . import mapper
        turns = mapper._parse_dialogue(dlg)
        me = mapper._resolve_self(turns, inputs.get("dialogue_speaker") or "")
        n = 0
        for lab, txt in turns:
            if me and lab.lower() == me and txt:
                n += 1
                segs.append({"id": f"d:{n}", "source": "dialogue", "text": txt})
    return segs


def person_text(segs: list[dict]) -> str:
    return "\n".join(s["text"] for s in segs)


def _age(inputs: dict) -> Optional[int]:
    try:
        return int(float(str(inputs.get("age")).strip())) if inputs.get("age") not in (None, "") else None
    except (TypeError, ValueError):
        return None


def run_reading(inputs: dict, engine: str = "rules", client: Optional[ModelClient] = None,
                premium: bool = False) -> dict:
    """Returns the report object (see ENGINE_SPEC.md). Never raises on model failure; fails safe."""
    from . import mapper, synthesizer, pathway   # local imports keep module load light

    t0 = time.time()
    ledger = Ledger()
    segs = build_segments(inputs)
    text = person_text(segs)
    report: dict = {"engine": engine, "created": t0, "notices": [], "citations": {}}

    # 1. safety screen — always first
    use_model = engine == "model"
    raw = "\n".join([*(str(v) for v in (inputs.get("answers") or {}).values() if isinstance(v, (str, int))),
                      inputs.get("free_text") or "", inputs.get("dialogue") or ""])
    # the screen reads everything the person pasted (all speakers, unparsed lines): a crisis signal anywhere stops it
    scr = safety.screen(raw + (f"\nAge: {inputs.get('age')}" if inputs.get("age") else ""), age=_age(inputs),
                        client=client if use_model else None, ledger=ledger, require_model=use_model)
    report["safety"] = {"route": scr.route, "categories": sorted(scr.flags), "model_checked": scr.model_checked,
                        "injection": scr.injection}
    msg = scr.message()
    if scr.stop:
        report["stopped"] = msg
        report["cost"] = ledger.totals()
        return report
    report["notices"].extend(msg.get("notes") or [])
    if engine != "model":
        # red team X03: say plainly when the reading is offline and the model safety check did not run
        report["notices"].append("This reading was made offline, by rule-based matching only; the fuller model-based "
                                 "safety check and reading did not run.")
    if not segs:
        report["insufficient"] = "Nothing was shared yet, so there is nothing to reflect on."
        report["cost"] = ledger.totals()
        return report

    # 2. mapping (rules/mapping_rules.json; the reading gate of 25 own words is applied inside the mapper)
    res = mapper.map_person(inputs, scr, engine=engine, client=client, ledger=ledger)
    maps = res.get("mappings") or []
    if res.get("notice"):
        report["notices"].append(res["notice"])
    report["mapping_audit"] = _audit_summary(res.get("audit") or {})
    if not maps:
        audit = res.get("audit") or {}
        why = audit.get("unmapped_reason")
        sents = [x for sg in segs for x in re.split(r"(?<=[.!?।])\s+", sg["text"].strip()) if x.strip()]
        n_sent = len(sents)
        n_ne = sum(1 for x in sents if not mapper.english_ok(x))    # counted here: the mapper may stop at its gate first
        if why != "dialogue_speaker_unresolved" and n_sent and n_ne * 2 >= n_sent:
            why = "language_not_supported"          # mostly not English: say so, instead of asking for more writing
        elif why in (None, "no_entry_met_floor") and len(text.split()) < 80:
            why = "short"
        report["insufficient"] = INSUFFICIENT.get(why, INSUFFICIENT[None])
        report["cost"] = ledger.totals()
        return report
    report["mappings"] = maps
    report["groups"] = res.get("groups") or []

    # 3. two-lens synthesis
    syn, syn_note = synthesizer.synthesize(segs, maps, engine=engine, client=client, ledger=ledger, premium=premium)
    if syn_note:
        report["notices"].append(syn_note)
    report.update(syn)

    # 4. pathway (rules first, model second)
    pw, pw_note = pathway.build(segs, maps, scr, engine=engine, client=client, ledger=ledger)
    if pw_note:
        report["notices"].append(pw_note)
    report["pathway"] = pw

    # 5. citations, final validation
    finalize(report, segs)
    report["cost"] = ledger.totals()
    return report


def collect_cites(obj) -> set:
    out = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "cites" and isinstance(v, list):
                out.update(x for x in v if isinstance(x, str))
            elif k != "citations":
                out |= collect_cites(v)
    elif isinstance(obj, list):
        for v in obj:
            out |= collect_cites(v)
    return out


LENS_EMPTY_NOTE = {
    "vedic": ("Among the teachings checked so far, the Vedic and yogic texts do not describe what you wrote closely "
              "enough, in their own terms, for this reading to say more."),
    "ascetic": ("Among the teachings checked so far, the Buddhist and Jain texts do not describe what you wrote closely "
                "enough, in their own terms, for this reading to say more."),
}


def finalize(report: dict, segs: list[dict]) -> None:
    """Resolve citations; drop uncitable ones; enforce specificity and the claim scan on every insight."""
    quotes = {}
    for m in report.get("mappings") or []:
        for e in m.get("evidence") or []:
            quotes[e["qid"]] = e["quote"]
    for key, lens in (report.get("lenses") or {}).items():
        kept, _ = specificity.filter_insights(lens.get("points") or [], quotes)
        lens["points"] = [p for p in kept if not claims.scan(p["text"])]
        if not lens["points"] and not lens.get("note"):
            lens["note"] = LENS_EMPTY_NOTE[key]
    rec = report.get("reconciliation") or {}
    for key in ("points", "differences"):
        kept, _ = specificity.filter_insights(rec.get(key) or [], quotes)
        rec[key] = [p for p in kept if not claims.scan(p["text"])]
    _strip_uncitable(report)
    cits = {}
    for tid in sorted(collect_cites(report)):
        try:
            cits[tid] = ontology.citation(tid)
        except KeyError:
            pass
    report["citations"] = cits
    report["claim_hits"] = claims.scan_fields({k: v for k, v in report.items()
                                               if k not in ("citations", "safety", "mapping_audit")},
                                              skip_keys=("original", "quote", "evidence", "counter_evidence", "person_words",
                                                         "basis_quote"))


def _strip_uncitable(obj) -> None:
    """In place: keep only citable ids in every 'cites' list; scrub forbidden-claim sentences from free-text fields."""
    if isinstance(obj, dict):
        for k, v in list(obj.items()):
            if k == "cites" and isinstance(v, list):
                obj[k] = [t for t in v if isinstance(t, str) and ontology.citable(t)]
            elif k in ("why", "summary", "text", "plan", "checkin_prompt") and isinstance(v, str):
                obj[k] = claims.strip_sentences(v)
            elif k not in ("citations", "evidence", "counter_evidence", "original", "stopped", "safety", "mapping_audit"):
                _strip_uncitable(v)
    elif isinstance(obj, list):
        for v in obj:
            _strip_uncitable(v)
