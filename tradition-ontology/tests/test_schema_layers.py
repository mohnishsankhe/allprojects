"""The product layers (layers/diagnosis.json, layers/practices.json): they load, and what is user-facing resolves."""
import json

import pytest

from insight import config, ontology

DIAG = json.loads((config.LAYERS / "diagnosis.json").read_text("utf-8"))
PRAC = json.loads((config.LAYERS / "practices.json").read_text("utf-8"))


def _cites(obj):
    out = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == "cites" and isinstance(v, list):
                out += [x for x in v if isinstance(x, str)]
            else:
                out += _cites(v)
    elif isinstance(obj, list):
        for v in obj:
            out += _cites(v)
    return out


def test_layers_load_and_have_the_expected_shape():
    assert isinstance(DIAG, list) and len(DIAG) > 50 and isinstance(PRAC, list) and len(PRAC) > 20
    for e in DIAG:
        assert e["id"].startswith("dx:") and e["name"] and e["lens"] in ("vedic-yogic", "ascetic-buddhist", "ascetic-jain")
    for p in PRAC:
        assert p["id"].startswith("px:") and p["safety_tier"] in ("gentle", "needs-teacher", "never-recommend")
    assert len({e["id"] for e in DIAG}) == len(DIAG) and len({p["id"] for p in PRAC}) == len(PRAC)


def test_ontology_loaders_return_the_user_facing_entries():
    dx, px = ontology.diagnosis(), ontology.practices()
    assert dx and px
    assert set(dx) <= {e["id"] for e in DIAG} and set(px) <= {p["id"] for p in PRAC}
    assert all(e.get("user_facing") is not False for e in dx.values())


def test_every_user_facing_diagnosis_cite_is_citable():
    for eid, e in ontology.diagnosis().items():
        cites = _cites({k: v for k, v in e.items() if k in ("definitions", "markers", "states", "equivalences", "paired_practices", "warnings", "cites")})
        assert cites, eid
        for c in cites:
            assert ontology.citable(c), (eid, c)
            r = ontology.citation(c)
            assert r["level"] in ("sourced", "text-verified") and r["title"] and r["paraphrase"] is not None


def test_every_user_facing_diagnosis_entry_has_a_definition_with_cites():
    for eid, e in ontology.diagnosis().items():
        assert e["definitions"] and all(d["cites"] for d in e["definitions"]), eid


def test_every_user_facing_practice_cite_is_citable():
    for pid, p in ontology.practices().items():
        for c in _cites(p):
            assert ontology.citable(c), (pid, c)
            assert ontology.citation(c)["level"] in ("sourced", "text-verified")


def test_every_gentle_practice_has_steps_and_cited_warnings():
    g = ontology.gentle_practices()
    assert len(g) >= 10
    for pid, p in g.items():
        assert p["safety_tier"] == "gentle" and p.get("user_facing") is not False
        assert p["steps"] and all(isinstance(s, str) and s.strip() for s in p["steps"]), pid
        assert p["warnings"], pid
        for w in p["warnings"]:
            assert w["text"].strip() and w["cites"], (pid, w)
            assert all(ontology.citable(c) for c in w["cites"]), (pid, w["cites"])
        assert p["cites"] and (p["duration"].get("minutes_per_session")), pid


def test_no_gentle_practice_is_restricted():
    restricted = ontology.restricted_practices()
    for pid, p in ontology.gentle_practices().items():
        assert not ({pid} & restricted)
        for c in _cites(p):
            assert not ontology.teaching(c)["restricted"], (pid, c)


def test_gentle_practices_do_not_hold_dangerous_techniques():
    danger = ("mercury", "metal", "cutting the body", "breath retention", "kumbhaka", "sexual", "fast for", "prolonged fast", "fasting for")
    for pid, p in ontology.gentle_practices().items():
        text = " ".join([p["name"], p["summary"]] + p["steps"]).lower()
        assert not [d for d in danger if d in text], (pid, [d for d in danger if d in text])


def test_a_practice_with_an_uncitable_warning_is_not_usable():
    # the loader drops any practice whose warning has lost its citation (a practice is never shown with a cut-down caution)
    for pid, p in ontology.practices().items():
        assert all(any(ontology.citable(c) for c in w["cites"]) for w in p["warnings"]), pid


def test_skeleton_teachings_are_never_citable():
    skeletons = [t for t in ontology.teachings().values() if t["level"] == "skeleton" and not t.get("superseded_by")][:200]
    assert skeletons
    for t in skeletons:
        cov = ontology.teaching(t["id"])
        # either the id itself is refused, or it resolves (mechanically) to a verified passage of the same source
        assert (not ontology.citable(t["id"])) or (cov["level"] in ("sourced", "text-verified") and cov["source"] == t["source"])


def test_equivalence_targets_exist_and_grades_are_known():
    dx = ontology.diagnosis()
    grades = {"exact", "same-under-standpoint", "partial", "analogous"}
    for eid, e in dx.items():
        for q in e.get("equivalences") or []:
            if q["id"] in dx:
                assert q.get("grade") in grades and q.get("note"), (eid, q["id"])
