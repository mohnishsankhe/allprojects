"""Pathway: gentle tier only; the no-diet route drops food and exercise (warnings included); at most 4; 14 days."""
from types import SimpleNamespace

import pytest

from insight import ontology, pathway
from conftest import NO_FLAGS, client_with

DX = ["dx:gita-restless-mind", "dx:gita-kama-krodha", "dx:nivarana-byapada", "dx:root-dosa", "dx:gita-anger-chain",
      "dx:guna-rajas", "dx:gita-sthitaprajna"]


def maps(ids=DX, conf="moderate"):
    dx = ontology.diagnosis()
    out = []
    for i, d in enumerate(ids):
        q = f"my mind will not settle number {i}"
        out.append({"dx_id": d, "name": dx[d]["name"], "lens": dx[d]["lens"], "confidence": conf,
                    "evidence": [{"qid": f"q{i}", "quote": q, "strength": "direct", "unit": "u"}], "cites": ["x"]})
    return out


def build(route="continue", ids=DX, **kw):
    return pathway.build([{"id": "free", "source": "free_text", "text": "x"}], maps(ids), SimpleNamespace(route=route), **kw)


def test_only_gentle_practices_are_ever_chosen():
    pw, _ = build()
    gentle = ontology.gentle_practices()
    allp = ontology.practices()
    assert pw["practices"]
    for p in pw["practices"]:
        assert p["px_id"] in gentle and allp[p["px_id"]]["safety_tier"] == "gentle"
    assert "gentle" in pw["tier_rule"].lower()


def test_no_tier_other_than_gentle_is_eligible_even_if_it_targets_the_entry():
    for pid, p in ontology.practices().items():
        if p["safety_tier"] != "gentle":
            assert not pathway._eligible(p, "continue")
    ranked = {p["id"] for _, p, _ in pathway.rank(maps(), "continue")}
    assert ranked <= set(ontology.gentle_practices())


def test_never_more_than_four_and_at_least_one_here():
    pw, _ = build()
    assert 1 <= len(pw["practices"]) <= 4
    assert len(pathway.select(maps(), "continue", max_n=10)) <= 10
    assert len(pathway.select(maps(), "continue")) <= 4


def test_every_practice_has_steps_and_cited_warnings_and_cites():
    for p in build()[0]["practices"]:
        assert p["steps"] and p["warnings"] and p["cites"]
        assert all(w["cites"] and all(ontology.citable(c) for c in w["cites"]) for w in p["warnings"])
        assert p["duration"].get("minutes_per_session") and "basis" in p["duration"]
        assert p["why"].startswith("You wrote") and p["evidence_refs"]


def test_no_diet_route_excludes_food_and_exercise_including_warnings():
    normal = {p["px_id"] for p in build("continue")[0]["practices"]}
    nodiet_pw, _ = build("continue_no_diet")
    nodiet = {p["px_id"] for p in nodiet_pw["practices"]}
    food_ones = {pid for pid, p in ontology.gentle_practices().items()
                 if pathway.EXCLUDE_IF_NO_DIET.search(" ".join([p["name"], p["summary"]] + p["steps"] + [w["text"] for w in p["warnings"]]))}
    assert food_ones, "the layer should hold practices whose warnings touch food"
    assert not (nodiet & food_ones)
    assert normal & food_ones, "without the no-diet route, food-touching practices are eligible"
    blob = " ".join(" ".join([p["name"]] + p["steps"] + [w["text"] for w in p["warnings"]]) for p in nodiet_pw["practices"])
    assert not pathway.EXCLUDE_IF_NO_DIET.search(blob)


def test_no_diet_route_can_leave_a_short_pathway_with_a_note():
    pw, note = build("continue_no_diet", ids=["dx:gita-restless-mind"])
    assert len(pw["practices"]) < 2 and note


def test_no_entry_no_pathway():
    pw, note = pathway.build([], [], SimpleNamespace(route="continue"))
    assert pw["practices"] == [] and note and pw["sequence"] == []


def test_ranking_prefers_higher_confidence():
    hi = maps(["dx:gita-restless-mind"], "high")
    lo = maps(["dx:gita-restless-mind"], "low")
    s_hi = pathway.rank(hi, "continue")[0][0]
    s_lo = pathway.rank(lo, "continue")[0][0]
    assert s_hi > s_lo


def test_fourteen_day_sequence_adds_one_practice_on_days_1_4_8_11():
    chosen = [ontology.gentle_practices()[k] for k in list(ontology.gentle_practices())[:4]]
    seq = pathway.sequence(chosen)
    assert [s["day"] for s in seq] == list(range(1, 15))
    count = lambda s: s["plan"].split(". Then")[0].count(" min)")
    counts = [count(s) for s in seq]
    assert counts[0] == 1 and counts[2] == 1 and counts[3] == 2 and counts[6] == 2
    assert counts[7] == 3 and counts[9] == 3 and counts[10] == 4 and counts[13] == 4
    assert all(s["plan"].endswith("Then the check-in.") for s in seq)
    # week 1 sessions use the short end of the range
    lo = chosen[0]["duration"]["minutes_per_session"]
    assert f"({lo[0]} min)" in seq[0]["plan"] and f"({lo[-1]} min)" in seq[9]["plan"]


def test_sequence_matches_the_report_schema_days():
    pw, _ = build()
    assert len(pw["sequence"]) == 14 and pw["checkin_prompt"]


def test_model_may_only_reword_why_and_only_if_it_quotes_the_person():
    m = maps(["dx:gita-restless-mind", "dx:gita-kama-krodha"])
    base, _ = pathway.build([], m, SimpleNamespace(route="continue"))
    ids = [p["px_id"] for p in base["practices"]]
    good_quote = m[0]["evidence"][0]["quote"]

    def handler(_kw):
        return {"practices": [{"px_id": ids[0], "why": f"You wrote “{good_quote}”, and the texts pair it with this."},
                              {"px_id": ids[-1], "why": "This will cure your anxiety."},
                              {"px_id": "px:invented", "why": f"You wrote {good_quote}"}]}
    c, t = client_with({"pathway": handler})
    pw, note = pathway.build([{"id": "free", "source": "free_text", "text": good_quote}], m, SimpleNamespace(route="continue"),
                             engine="model", client=c)
    assert [p["px_id"] for p in pw["practices"]] == ids                 # no practice added, swapped or removed
    assert good_quote in pw["practices"][0]["why"]
    if len(ids) > 1:
        assert "cure" not in pw["practices"][-1]["why"]                 # claims scan rejects the rewording
    assert "px:invented" not in [p["px_id"] for p in pw["practices"]]


def test_model_failure_keeps_rules_wording_and_adds_a_note():
    m = maps(["dx:gita-restless-mind"])
    c, _ = client_with({"pathway": RuntimeError("down")})
    base, _ = pathway.build([], m, SimpleNamespace(route="continue"))
    pw, note = pathway.build([], m, SimpleNamespace(route="continue"), engine="model", client=c)
    assert pw["practices"][0]["why"] == base["practices"][0]["why"] and "standard template" in note
