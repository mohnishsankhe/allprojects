"""Shared helpers for the diagnosis layer build (layers/diagnosis.json)."""
def c(slug):
    return lambda r: f"tea:{slug}:{r}"
YS, YB, BG = c('yoga-sutra'), c('yoga-bhasya'), c('bhagavad-gita')
KU, TU, MU, GK = c('katha-upanisad'), c('taittiriya-upanisad'), c('mandukya-upanisad'), c('mandukya-karika')
MN10 = lambda r: f"tea:satipatthana-sutta:mn10:{r}"
DN22 = lambda r: f"tea:mahasatipatthana-sutta:dn22:{r}"
MN118 = lambda r: f"tea:anapanasati-sutta:mn118:{r}"
DHP, TS = c('dhammapada'), c('tattvartha-sutra')
VSM = lambda ch, p: f"tea:visuddhimagga:{ch}.p{p}"   # orchestrator-specified id form: <chapter>.p<PTS page>
DN2 = "tea:samannaphala-sutta:67-74"                    # existing id; text checked in bilara root dn2:68-74

LIN_YOGA, LIN_GITA, LIN_UPA, LIN_GK = 'lin:patanjala-yoga', 'lin:epic-teaching', 'lin:upanisadic', 'lin:advaita-vedanta'
LIN_EB, LIN_TH, LIN_JAIN = 'lin:early-buddhism', 'lin:theravada', 'lin:jainism'

def E(id, name, kind, group, lens, refs, defs, markers, not_read, states=None, eq=None, px=None):
    return {
        "id": id, "name": name, "kind": kind, "group": group, "lens": lens,
        "ontology_refs": list(refs),
        "definitions": [{"tradition": t, "text": x, "cites": list(cs)} for t, x, cs in defs],
        "markers": [{"marker": m, "cues": list(cu), "cites": list(cs)} for m, cu, cs in markers],
        "states": [{"name": n, "text": x, "cites": list(cs)} for n, x, cs in (states or [])],
        "equivalences": [{"id": i, "grade": g, "note": n, "cites": list(cs)} for i, g, n, cs in (eq or [])],
        "paired_practices": [{"practice": p, "cites": list(cs)} for p, cs in (px or [])],
        "not_to_be_read_as": not_read,
        "user_facing": True,
    }
