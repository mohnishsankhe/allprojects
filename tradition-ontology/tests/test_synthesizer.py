"""Two-lens synthesis: both lenses speak, every point is tied to the person's words and to citable texts."""
from insight import ontology, synthesizer
from conftest import client_with, fake_map_person, BENIGN, QUOTE


def maps():
    return fake_map_person({"free_text": BENIGN})["mappings"]


def _all_points(res):
    pts = list(res["lenses"]["vedic"].get("points", [])) + list(res["lenses"]["ascetic"].get("points", []))
    pts += res["reconciliation"]["points"] + res["reconciliation"]["differences"]
    return pts


def test_both_lenses_are_present_and_speak():
    res = synthesizer.rules_synthesis(maps())
    assert set(res["lenses"]) == {"vedic", "ascetic"}
    assert res["lenses"]["vedic"]["points"] and res["lenses"]["ascetic"]["points"]
    assert res["summary"] and "note" not in res["lenses"]["vedic"]


def test_ascetic_lens_speaks_only_through_a_cited_equivalence_and_says_so():
    res = synthesizer.rules_synthesis(maps())
    dx = ontology.diagnosis()
    for p in res["lenses"]["ascetic"]["points"]:
        assert p["via"] == "dx:klesa-raga"                          # never a direct claim about the person
        assert any(e["id"] == p["dx_id"] for e in dx["dx:klesa-raga"]["equivalences"])
        assert "partial match" in p["text"] or "same" in p["text"] or "analogy" in p["text"]
    # evidence never transfers: the point quotes the words that mapped the original entry
    assert all(QUOTE in p["text"] for p in res["lenses"]["ascetic"]["points"])


def test_every_point_has_cites_and_evidence_refs_that_resolve():
    res = synthesizer.rules_synthesis(maps())
    qids = {e["qid"] for m in maps() for e in m["evidence"]}
    pts = _all_points(res)
    assert pts
    for p in pts:
        assert p["cites"] and p["evidence_refs"] and set(p["evidence_refs"]) <= qids
        assert any(ontology.citable(c) for c in p["cites"])


def test_reconciliation_points_name_a_valid_basis():
    for p in synthesizer.rules_synthesis(maps())["reconciliation"]["points"]:
        assert p["basis"] in ("level", "standpoint", "path", "stage")


def test_partial_equivalence_is_never_called_exact():
    res = synthesizer.rules_synthesis(maps())
    text = " ".join(p["text"] for p in _all_points(res)).lower()
    assert "a partial match" in text and "the same thing under another name" not in text


def test_lens_with_nothing_to_say_says_so_plainly():
    # a mapped entry without equivalences leaves the other lens empty, with a plain note (never padded)
    dx = ontology.diagnosis()
    lone = next(e for e in dx.values() if e["lens"] == "vedic-yogic"
                and not [q for q in e.get("equivalences") or [] if q.get("id") in dx])
    m = maps()[0] | {"dx_id": lone["id"], "name": lone["name"], "lens": lone["lens"], "cites": lone["definitions"][0]["cites"]}
    res = synthesizer.rules_synthesis([m])
    assert res["lenses"]["ascetic"]["points"] == [] and "do not describe" in res["lenses"]["ascetic"]["note"]


def test_rules_engine_makes_no_model_call():
    res, note = synthesizer.synthesize([], maps(), engine="rules")
    assert note is None and res["lenses"]["vedic"]["points"]


def _model_output(base, **over):
    v = base["lenses"]["vedic"]["points"][0]
    a = base["lenses"]["ascetic"]["points"][0]
    good_v = {"text": f"You wrote “{QUOTE}”. The Yoga Sutra describes attachment as what follows pleasure.",
              "cites": v["cites"][:1], "evidence_refs": v["evidence_refs"]}
    good_a = {"text": f"The Buddhist texts have a close word for this, sensual desire, though it is only a partial match. You wrote “{QUOTE}”.",
              "cites": a["cites"][:1], "evidence_refs": a["evidence_refs"]}
    out = {"vedic": [good_v], "ascetic": [good_a], "reconciliation": [], "differences": []}
    out.update(over)
    return out


def test_model_synthesis_kept_when_it_carries_packet_cites_and_quote_refs():
    base = synthesizer.rules_synthesis(maps())
    c, t = client_with({"synthesis": _model_output(base)})
    res, note = synthesizer.synthesize([], maps(), engine="model", client=c)
    assert note is None and t.calls[0][0] == "synthesis"
    assert res["lenses"]["vedic"]["points"][0]["text"].startswith("You wrote")
    # empty reconciliation from the model falls back to the rules result
    assert res["reconciliation"]["points"] == base["reconciliation"]["points"]


def test_model_output_with_foreign_cites_or_evidence_is_dropped():
    base = synthesizer.rules_synthesis(maps())
    ok = _model_output(base)
    foreign_cite = {"text": "Some claim about attachment.", "cites": ["tea:not-in-the-packet:1.1"], "evidence_refs": ["intake:q01#s1:78"]}
    foreign_ref = {"text": "Some claim about attachment.", "cites": ok["vedic"][0]["cites"], "evidence_refs": ["intake:zz#s9:9"]}
    no_ref = {"text": "Some claim about attachment.", "cites": ok["vedic"][0]["cites"], "evidence_refs": []}
    claim = {"text": "This will cure your anxiety.", "cites": ok["vedic"][0]["cites"], "evidence_refs": ["intake:q01#s1:78"]}
    bad_basis = {"text": "They meet at different places.", "cites": ok["vedic"][0]["cites"], "evidence_refs": ["intake:q01#s1:78"], "basis": "vibes"}
    out = _model_output(base, vedic=ok["vedic"] + [foreign_cite, foreign_ref, no_ref, claim],
                        reconciliation=[bad_basis])
    c, _ = client_with({"synthesis": out})
    res, _ = synthesizer.synthesize([], maps(), engine="model", client=c)
    texts = [p["text"] for p in res["lenses"]["vedic"]["points"]]
    assert texts == [ok["vedic"][0]["text"]]
    assert res["reconciliation"]["points"] == base["reconciliation"]["points"]     # bad basis dropped, rules kept
    for p in _all_points(res):
        assert p["cites"] and p["evidence_refs"]


def test_model_output_with_nothing_valid_falls_back_per_lens():
    base = synthesizer.rules_synthesis(maps())
    junk = [{"text": "x", "cites": ["tea:nope:1"], "evidence_refs": ["nope"]}]
    c, _ = client_with({"synthesis": {"vedic": junk, "ascetic": junk, "reconciliation": junk, "differences": junk}})
    res, _ = synthesizer.synthesize([], maps(), engine="model", client=c)
    assert res["lenses"]["vedic"]["points"] == base["lenses"]["vedic"]["points"]
    assert res["lenses"]["ascetic"]["points"] == base["lenses"]["ascetic"]["points"]


def test_model_failure_falls_back_with_a_notice():
    c, _ = client_with({"synthesis": RuntimeError("down")})
    res, note = synthesizer.synthesize([], maps(), engine="model", client=c)
    assert note and "standard wording" in note and res["lenses"]["vedic"]["points"]


def test_model_synthesis_packet_wraps_person_text_as_data():
    base = synthesizer.rules_synthesis(maps())
    c, t = client_with({"synthesis": _model_output(base)})
    synthesizer.synthesize([], maps(), engine="model", client=c)
    user = t.calls[0][1]["messages"][0]["content"]
    assert user.startswith("<user_input>") and "Packet:" in user
