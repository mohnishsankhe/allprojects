"""Service layer: adults only, consent first, minimisation after a stop, check-ins screened."""
import pytest

from insight.service import Service, ServiceError, consent_info, intake_questions
from conftest import BENIGN, NO_FLAGS, client_with


def _started(svc, age=34):
    return svc.start(age, True)["person_id"]


def test_consent_and_questions_come_from_the_rules_files():
    c = consent_info()
    assert c["min_age"] == 18 and c["version"] and c["text"] and c["checkbox"]
    q = intake_questions()
    assert 1 < len(q) <= 15 and q[0]["id"] == "age" and all("purpose" not in x for x in q)


def test_minor_declined_and_nothing_stored(svc, store):
    out = svc.start(16, True)
    assert "declined" in out and "person_id" not in out
    assert store.db.execute("SELECT COUNT(*) c FROM persons").fetchone()["c"] == 0
    # even a bare age without consent: declined, nothing stored
    assert "declined" in svc.start(12, False)
    assert store.db.execute("SELECT COUNT(*) c FROM persons").fetchone()["c"] == 0


def test_no_consent_is_an_error_and_stores_nothing(svc, store):
    with pytest.raises(ServiceError) as e:
        svc.start(34, False)
    assert e.value.code == "consent_required"
    with pytest.raises(ServiceError) as e:
        svc.start(34, "yes")                    # only a real True counts
    assert e.value.code == "consent_required"
    assert store.db.execute("SELECT COUNT(*) c FROM persons").fetchone()["c"] == 0


def test_age_must_be_a_number(svc):
    for bad in (None, "", "abc", 0, -3, 200):
        with pytest.raises(ServiceError) as e:
            svc.start(bad, True)
        assert e.value.code == "age_required"


def test_reading_and_checkin_need_a_consented_person(svc):
    with pytest.raises(ServiceError) as e:
        svc.reading("no-such-person", {"free_text": BENIGN})
    assert e.value.code == "no_consent" and e.value.status == 403
    with pytest.raises(ServiceError):
        svc.checkin("no-such-person", None, 1, "hello")
    with pytest.raises(ServiceError):
        svc.my_data("")


def test_minor_age_in_reading_inputs_is_declined_and_nothing_stored(svc, store):
    pid = _started(svc)
    out = svc.reading(pid, {"age": 15, "free_text": BENIGN})
    assert out["reading_id"] is None and out["report"]["stopped"]["title"]
    assert store.db.execute("SELECT COUNT(*) c FROM readings").fetchone()["c"] == 0


def test_stopped_reading_keeps_no_inputs(svc, store):
    pid = _started(svc)
    words = "I have been thinking about how to end my life and nothing helps."
    out = svc.reading(pid, {"age": 40, "free_text": words})
    assert out["report"]["stopped"] and out["report"]["safety"]["route"] == "stop_crisis"
    assert "14416" in out["markdown"]
    rd = store.get_reading(out["reading_id"])
    assert rd["status"] == "stopped" and rd["route"] == "stop_crisis"
    assert "end my life" not in str(rd["inputs"]) and "end my life" not in str(rd["report"])
    raw = store.db.execute("SELECT input_enc FROM readings").fetchone()["input_enc"]
    assert store.dec(raw) == {"withheld": "not kept after a safety stop"}


def test_insufficient_reading_is_stored_with_inputs_and_says_so(svc, store, fake_mapper):
    pid = _started(svc)
    out = svc.reading(pid, {"age": 40, "free_text": "I feel restless."})
    assert out["report"].get("insufficient")
    assert store.get_reading(out["reading_id"])["status"] == "insufficient"


def test_full_reading_is_stored_and_retrievable_in_three_formats(svc, fake_mapper):
    pid = _started(svc)
    out = svc.reading(pid, {"age": 40, "free_text": BENIGN})
    rid = out["reading_id"]
    assert out["report"]["mappings"] and out["markdown"].startswith("# Your reading")
    assert svc.get_report(pid, rid, "json")["mappings"]
    assert "<h1>" in svc.get_report(pid, rid, "html")
    assert svc.get_report(pid, rid, "md") == out["markdown"]
    other = _started(svc)
    with pytest.raises(ServiceError) as e:              # someone else's reading is never visible
        svc.get_report(other, rid)
    assert e.value.status == 404


def test_unknown_engine_value_is_treated_as_rules(svc, fake_mapper):
    pid = _started(svc)
    out = svc.reading(pid, {"age": 40, "free_text": BENIGN}, engine="whatever")
    assert out["report"]["engine"] == "rules"


def test_model_engine_without_key_is_a_clear_error(svc):
    pid = _started(svc)
    with pytest.raises(ServiceError) as e:
        svc.reading(pid, {"age": 40, "free_text": BENIGN}, engine="model")
    assert e.value.code == "model_unavailable" and e.value.status == 503


def test_checkin_stored_and_listed(svc):
    pid = _started(svc)
    r = svc.checkin(pid, None, 3, "I did the practice for five minutes and my mind wandered twice.")
    assert r["stored"] is True
    cs = svc.checkins(pid)
    assert len(cs) == 1 and cs[0]["day"] == 3 and "wandered" in cs[0]["body"]["text"]


def test_checkin_crisis_not_stored_and_shows_resources(svc, store):
    pid = _started(svc)
    r = svc.checkin(pid, None, 2, "Today I want to end my life.")
    assert r["stored"] is False and "14416" in str(r["stopped"]["resources"])
    assert store.db.execute("SELECT COUNT(*) c FROM checkins").fetchone()["c"] == 0


def test_checkin_minor_sign_is_declined_not_stored(svc, store):
    pid = _started(svc)
    r = svc.checkin(pid, None, 2, "I am 15 years old and did the practice.")
    assert r["stored"] is False and r["stopped"]["title"]
    assert store.db.execute("SELECT COUNT(*) c FROM checkins").fetchone()["c"] == 0


def test_checkin_medical_note_is_returned(svc):
    pid = _started(svc)
    r = svc.checkin(pid, None, 2, "My doctor said to rest, and I did the practice.")
    assert r["stored"] and any("not medical advice" in n.lower() for n in r["notes"])


def test_checkin_day_range(svc):
    pid = _started(svc)
    for d in (0, 61):
        with pytest.raises(ServiceError) as e:
            svc.checkin(pid, None, d, "x")
        assert e.value.code == "bad_day"


def test_checkin_model_screen_failure_is_not_stored(store):
    c, _ = client_with({"safety_screen": RuntimeError("down")})
    s = Service(store=store, client=c)
    pid = s.start(30, True)["person_id"]
    r = s.checkin(pid, None, 1, "I did the practice.", engine="model")
    assert r["stored"] is False and r["stopped"]["title"]
    assert store.db.execute("SELECT COUNT(*) c FROM checkins").fetchone()["c"] == 0


def test_checkin_with_model_screen_ok_records_cost(store):
    c, _ = client_with({"safety_screen": NO_FLAGS})
    s = Service(store=store, client=c)
    pid = s.start(30, True)["person_id"]
    assert s.checkin(pid, None, 1, "I did the practice.", engine="model")["stored"]
    assert store.cost_summary()["checkin"]["count"] == 1


def test_delete_me_removes_everything(svc, store, fake_mapper):
    pid = _started(svc)
    svc.reading(pid, {"age": 40, "free_text": BENIGN})
    svc.checkin(pid, None, 1, "did it")
    r = svc.delete_me(pid)
    assert r["deleted"] and r["rows"] == 2
    with pytest.raises(ServiceError):
        svc.my_data(pid)
    assert store.db.execute("SELECT COUNT(*) c FROM persons").fetchone()["c"] == 0


def test_my_data_exports_the_person(svc, fake_mapper):
    pid = _started(svc)
    svc.reading(pid, {"age": 40, "free_text": BENIGN})
    ex = svc.my_data(pid)
    assert ex["person"]["id"] == pid and len(ex["readings"]) == 1
    assert "age" not in ex["person"] and "name" not in ex["person"]   # nothing beyond what the reading needs


def test_purge_via_service(svc):
    assert isinstance(svc.purge(days=0)["purged"], int)


def test_review_rules(svc, store):
    pid = store.add_post("b", "b", "x_post", {"parts": ["a"]}, {})
    with pytest.raises(ServiceError) as e:
        svc.review(pid, "publish")
    assert e.value.code == "bad_action"
    with pytest.raises(ServiceError) as e:
        svc.review(pid, "edit")
    assert e.value.code == "edit_needs_body"
    with pytest.raises(ServiceError) as e:                # an editor cannot introduce a forbidden claim
        svc.review(pid, "edit", "", {"parts": ["This will cure your anxiety."]})
    assert e.value.code == "claims_in_edit"
    with pytest.raises(ServiceError) as e:
        svc.review("missing", "approve")
    assert e.value.status == 404
    assert svc.review(pid, "approve", "good") == {"ok": True}
