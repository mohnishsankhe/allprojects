"""The web API through FastAPI's TestClient. Model calls are faked; every test has its own data directory."""
import json
import logging
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from insight import api, content, service
from conftest import BENIGN, NO_FLAGS, client_with

WEB = Path(__file__).resolve().parent.parent / "web"
FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "content_fixture.json").read_text("utf-8"))


@pytest.fixture
def client():
    api.set_client(None)
    with TestClient(api.app, raise_server_exceptions=False) as c:
        yield c
    api.set_client(None)


def start(client, age=34):
    r = client.post("/api/start", json={"age": age, "consent": True})
    assert r.status_code == 200
    return r.json()["person_id"]


def test_consent_and_questions(client):
    c = client.get("/api/consent").json()
    assert c["min_age"] == 18 and c["text"] and c["checkbox"]
    q = client.get("/api/questions").json()
    assert q[0]["id"] == "age" and 1 < len(q) <= 15


def test_full_flow_consent_start_reading_report_checkin_export_delete(client, fake_mapper):
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "inputs": {"age": 34, "answers": {"q01": BENIGN}}})
    assert r.status_code == 200
    body = r.json()
    rid = body["reading_id"]
    assert rid and body["markdown"].startswith("# Your reading") and body["report"]["mappings"]
    assert body["report"]["claim_hits"] == []

    md = client.get(f"/api/reading/{rid}", params={"person_id": pid})
    assert md.status_code == 200 and md.text == body["markdown"] and "markdown" in md.headers["content-type"]
    html = client.get(f"/api/reading/{rid}", params={"person_id": pid, "format": "html"})
    assert "<h1>Your reading</h1>" in html.text and "text/html" in html.headers["content-type"]
    js = client.get(f"/api/reading/{rid}", params={"person_id": pid, "format": "json"}).json()
    assert js["mappings"][0]["dx_id"] == "dx:klesa-raga"
    assert client.get(f"/api/reading/{rid}", params={"person_id": pid, "format": "pdf"}).status_code == 400

    c = client.post("/api/checkin", json={"person_id": pid, "reading_id": rid, "day": 2, "text": "I did five minutes and it wandered."})
    assert c.status_code == 200 and c.json()["stored"] is True
    cs = client.get("/api/checkins", params={"person_id": pid}).json()
    assert len(cs) == 1 and cs[0]["day"] == 2

    me = client.get("/api/me", params={"person_id": pid}).json()
    assert me["person"]["id"] == pid and len(me["readings"]) == 1 and len(me["checkins"]) == 1

    d = client.delete("/api/me", params={"person_id": pid})
    assert d.status_code == 200 and d.json()["deleted"] is True and d.json()["rows"] == 2
    gone = client.get("/api/me", params={"person_id": pid})
    assert gone.status_code == 403 and gone.json()["error"] == "no_consent"
    assert client.get(f"/api/reading/{rid}", params={"person_id": pid}).status_code == 403


def test_person_id_may_come_from_a_header(client):
    pid = start(client)
    assert client.get("/api/me", headers={"X-Person-Id": pid}).status_code == 200
    assert client.get("/api/me").status_code == 403


def test_minor_is_declined_and_nothing_stored(client):
    r = client.post("/api/start", json={"age": 15, "consent": True})
    assert r.status_code == 200 and "declined" in r.json() and "person_id" not in r.json()
    assert "findahelpline.com" in r.json()["declined"]["body"]


def test_no_consent_is_an_error_json(client):
    r = client.post("/api/start", json={"age": 40, "consent": False})
    assert r.status_code == 400 and r.json()["error"] == "consent_required" and r.json()["message"]
    assert client.post("/api/start", json={"age": "abc", "consent": True}).json()["error"] == "age_required"


def test_reading_without_a_consented_person_is_403(client):
    r = client.post("/api/reading", json={"person_id": "nobody", "inputs": {"free_text": BENIGN}})
    assert r.status_code == 403 and r.json()["error"] == "no_consent"


def test_crisis_reading_shows_resources_and_keeps_no_words(client):
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "inputs": {"age": 40, "free_text": "I want to end my life, nothing helps."}})
    rep = r.json()["report"]
    assert rep["stopped"] and "14416" in json.dumps(rep["stopped"]["resources"])
    me = client.get("/api/me", params={"person_id": pid}).json()
    assert "end my life" not in json.dumps(me)


def test_checkin_crisis_is_not_stored(client):
    pid = start(client)
    r = client.post("/api/checkin", json={"person_id": pid, "day": 1, "text": "I want to kill myself"})
    assert r.json()["stored"] is False and r.json()["stopped"]["resources"]
    assert client.get("/api/checkins", params={"person_id": pid}).json() == []


def test_checkin_input_validation(client):
    pid = start(client)
    assert client.post("/api/checkin", json={"person_id": pid, "day": "x", "text": "a"}).json()["error"] == "bad_day"
    assert client.post("/api/checkin", json={"person_id": pid, "day": 99, "text": "a"}).json()["error"] == "bad_day"
    assert client.post("/api/checkin", json={"person_id": pid, "day": 1, "text": "  "}).status_code == 400
    assert client.post("/api/checkin", json={"person_id": pid, "day": 1, "text": 5}).status_code == 400


def test_bad_bodies_are_400_and_never_echo_input(client):
    r = client.post("/api/start", content=b"{not json SECRET-WORDS", headers={"content-type": "application/json"})
    assert r.status_code == 400 and "SECRET-WORDS" not in r.text
    r = client.post("/api/start", json=[1, 2])
    assert r.status_code == 400
    r = client.post("/api/reading", json={"person_id": "x" * 100, "inputs": {}})
    assert r.status_code == 400
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "inputs": "SECRET-WORDS"})
    assert r.status_code == 400 and "SECRET-WORDS" not in r.text
    r = client.post("/api/reading", json={"person_id": pid, "inputs": {}, "engine": "sonnet"})
    assert r.status_code == 400


def test_huge_body_is_413(client):
    pid = start(client)
    big = {"person_id": pid, "inputs": {"free_text": "word " * 40000}}
    for path in ("/api/reading", "/api/checkin"):
        r = client.post(path, json=big)
        assert r.status_code == 413 and r.json()["error"] == "too_large"
    # also without a content-length header (chunked upload)
    def gen():
        for _ in range(100):
            yield b"x" * 1024
    r = client.post("/api/reading", content=gen(), headers={"content-type": "application/json"})
    assert r.status_code == 413
    # a body just under the limit is not refused for size
    ok = client.post("/api/reading", json={"person_id": pid, "inputs": {"free_text": "a " * 5000}})
    assert ok.status_code == 200


def test_security_headers_on_every_kind_of_response(client):
    for r in (client.get("/"), client.get("/api/consent"), client.get("/api/nothing"), client.get("/static/app.js"),
              client.post("/api/start", json={})):
        assert "default-src 'self'" in r.headers["content-security-policy"], r.request.url
        assert r.headers["x-content-type-options"] == "nosniff"
        assert r.headers["referrer-policy"] == "no-referrer"
    csp = client.get("/").headers["content-security-policy"]
    assert "unsafe-inline" not in csp and "unsafe-eval" not in csp and "script-src 'self'" in csp
    assert client.get("/api/consent").headers["cache-control"] == "no-store"


def test_no_cors_for_other_origins(client):
    r = client.get("/api/consent", headers={"Origin": "https://evil.example"})
    assert "access-control-allow-origin" not in {k.lower() for k in r.headers}
    pre = client.options("/api/start", headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "POST"})
    assert "access-control-allow-origin" not in {k.lower() for k in pre.headers}


def test_index_and_static_files_are_served(client):
    r = client.get("/")
    assert r.status_code == 200 and "text/html" in r.headers["content-type"] and "consent" in r.text.lower()
    assert client.get("/static/app.js").status_code == 200 and client.get("/static/style.css").status_code == 200
    assert client.get("/static/../ENGINE_SPEC.md").status_code in (400, 404)
    assert client.get("/docs").status_code == 404 and client.get("/openapi.json").status_code == 404


def test_unexpected_error_is_500_internal_and_logs_only_the_type(client, monkeypatch, caplog):
    def boom(self, *a, **k):
        raise ValueError("SECRET USER WORDS I feel sad")
    monkeypatch.setattr(service.Service, "checkins", boom)
    pid = start(client)
    with caplog.at_level(logging.DEBUG):
        r = client.get("/api/checkins", params={"person_id": pid})
    assert r.status_code == 500 and r.json() == {"error": "internal"}
    assert "default-src 'self'" in r.headers["content-security-policy"]
    logged = " ".join(rec.getMessage() for rec in caplog.records)
    assert "ValueError" in logged and "SECRET USER WORDS" not in logged
    assert all(rec.exc_info is None for rec in caplog.records if rec.name.startswith("insight"))


def test_unexpected_error_in_reading_route_has_no_user_text(client, monkeypatch, caplog):
    monkeypatch.setattr(service.Service, "reading", lambda self, *a, **k: (_ for _ in ()).throw(RuntimeError("SECRET WORDS")))
    pid = start(client)
    with caplog.at_level(logging.DEBUG):
        r = client.post("/api/reading", json={"person_id": pid, "inputs": {"free_text": "SECRET WORDS"}})
    assert r.status_code == 500 and "SECRET" not in r.text
    assert "SECRET" not in " ".join(rec.getMessage() for rec in caplog.records)


# --- model engine through the API (fake transport) -----------------------------------------------------
def test_model_engine_unavailable_is_503(client):
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "engine": "model", "inputs": {"free_text": BENIGN}})
    assert r.status_code == 503 and r.json()["error"] == "model_unavailable"


def test_model_engine_with_fake_transport(client, fake_mapper):
    c, t = client_with({"safety_screen": NO_FLAGS, "synthesis": RuntimeError("down")})
    api.set_client(c)
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "engine": "model", "inputs": {"age": 30, "answers": {"q01": BENIGN}}})
    rep = r.json()["report"]
    assert r.status_code == 200 and rep["engine"] == "model" and rep["safety"]["model_checked"]
    assert any("standard wording" in n for n in rep["notices"])
    assert t.calls[0][0] == "safety_screen"
    costs_before = t.calls
    assert costs_before


def test_model_screen_failure_through_the_api_is_a_stop(client, fake_mapper):
    c, _ = client_with({"safety_screen": RuntimeError("down")})
    api.set_client(c)
    pid = start(client)
    r = client.post("/api/reading", json={"person_id": pid, "engine": "model", "inputs": {"answers": {"q01": BENIGN}}})
    assert r.json()["report"]["safety"]["route"] == "stop_unavailable"


# --- admin ---------------------------------------------------------------------------------------------
ADMIN = [("get", "/api/admin/costs"), ("get", "/api/admin/posts"), ("post", "/api/admin/posts/x/review"),
         ("post", "/api/admin/drafts"), ("get", "/api/admin/calendar?bucket=work"), ("post", "/api/admin/purge"),
         ("get", "/api/admin/buckets")]


@pytest.mark.parametrize("method,path", ADMIN)
def test_admin_is_403_when_no_token_is_configured(client, method, path):
    r = getattr(client, method)(path, headers={"X-Admin-Token": ""})
    assert r.status_code == 403 and r.json()["error"] == "forbidden"
    r = getattr(client, method)(path, headers={"X-Admin-Token": "anything"})     # unset env: even a guess is refused
    assert r.status_code == 403


@pytest.mark.parametrize("method,path", ADMIN)
def test_admin_is_403_with_a_missing_or_wrong_token(client, monkeypatch, method, path):
    monkeypatch.setenv("ONTO_ADMIN_TOKEN", "s3cret-token")
    assert getattr(client, method)(path).status_code == 403
    assert getattr(client, method)(path, headers={"X-Admin-Token": "wrong"}).status_code == 403
    assert getattr(client, method)(path, headers={"X-Admin-Token": "s3cret-token "}).status_code == 403


@pytest.fixture
def admin(client, monkeypatch):
    monkeypatch.setenv("ONTO_ADMIN_TOKEN", "s3cret-token")
    b = {x["id"]: x for x in FIXTURE["buckets"]}
    if not b or (content.buckets() and set(content.buckets()) != set(b)):
        b = content.buckets()
    monkeypatch.setattr(content, "buckets", lambda: b)
    monkeypatch.setattr(content, "formats", lambda: FIXTURE["formats"])
    return {"X-Admin-Token": "s3cret-token"}, next(iter(b))


def test_admin_costs_after_a_model_reading(client, admin, fake_mapper):
    h, _ = admin
    assert client.get("/api/admin/costs", headers=h).json() == {}
    c, _ = client_with({"safety_screen": NO_FLAGS, "synthesis": RuntimeError("down")})
    api.set_client(c)
    pid = start(client)
    client.post("/api/reading", json={"person_id": pid, "engine": "model", "inputs": {"answers": {"q01": BENIGN}}})
    costs = client.get("/api/admin/costs", headers=h).json()
    assert costs["reading"]["count"] == 1 and costs["reading"]["input_tokens"] > 0


def test_admin_draft_review_calendar_purge(client, admin):
    h, bucket = admin
    d = client.post("/api/admin/drafts", headers=h, json={"bucket": bucket, "format": "x_post", "n": 2, "engine": "rules"})
    assert d.status_code == 200 and len(d.json()["queued"]) == 2
    posts = client.get("/api/admin/posts", params={"status": "pending"}, headers=h).json()
    assert len(posts) == 2 and posts[0]["body"]["parts"]
    pid = posts[0]["id"]
    assert client.post(f"/api/admin/posts/{pid}/review", headers=h, json={"action": "approve", "note": "ok"}).json() == {"ok": True}
    assert len(client.get("/api/admin/posts", params={"status": "approved"}, headers=h).json()) == 1
    other = posts[1]
    edit = client.post(f"/api/admin/posts/{other['id']}/review", headers=h,
                       json={"action": "edit", "body": dict(other["body"], parts=["A calmer line. " + other["body"]["parts"][0]])})
    assert edit.status_code == 200
    claim = client.post(f"/api/admin/posts/{other['id']}/review", headers=h,
                        json={"action": "edit", "body": dict(other["body"], parts=["This will cure your anxiety."])})
    assert claim.status_code == 400 and claim.json()["error"] == "claims_in_edit"
    assert client.post("/api/admin/posts/nope/review", headers=h, json={"action": "reject"}).status_code == 404
    assert client.post(f"/api/admin/posts/{pid}/review", headers=h, json={"action": "publish"}).json()["error"] == "bad_action"
    cal = client.get("/api/admin/calendar", params={"bucket": bucket}, headers=h).json()
    assert len(cal) == 30
    assert client.get("/api/admin/calendar", params={"bucket": "nope"}, headers=h).status_code == 400
    assert client.get("/api/admin/posts", params={"status": "weird"}, headers=h).status_code == 400
    assert client.post("/api/admin/purge", headers=h, json={"days": 0}).json()["purged"] >= 0
    assert client.post("/api/admin/purge", headers=h, json={"days": -1}).status_code == 400


def test_admin_draft_validation(client, admin):
    h, bucket = admin
    assert client.post("/api/admin/drafts", headers=h, json={"bucket": "nope", "format": "x_post", "n": 1}).json()["error"] == "unknown_bucket"
    assert client.post("/api/admin/drafts", headers=h, json={"bucket": bucket, "format": "nope", "n": 1}).json()["error"] == "unknown_format"
    assert client.post("/api/admin/drafts", headers=h, json={"bucket": bucket, "format": "x_post", "n": 500}).status_code == 400
    b = client.get("/api/admin/buckets", headers=h).json()
    assert bucket in [x["id"] for x in b["buckets"]] and "x_post" in b["formats"]


def test_admin_purge_removes_old_person_data(client, admin):
    h, _ = admin
    pid = start(client)
    client.post("/api/checkin", json={"person_id": pid, "day": 1, "text": "did it"})
    assert client.post("/api/admin/purge", headers=h, json={"days": 0}).json()["purged"] >= 1
    assert client.get("/api/checkins", params={"person_id": pid}).status_code == 403     # the whole record is gone


# --- the page ------------------------------------------------------------------------------------------
def test_page_has_no_inline_script_and_no_external_resources():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    for m in re.finditer(r"<script\b([^>]*)>", html):
        assert "src=" in m.group(1)
    assert not re.search(r"(src|href)=[\"']https?://", html) and "onclick=" not in html.lower()
    assert 'lang="en"' in html and "prefers-color-scheme" in (WEB / "style.css").read_text()
    for label in ("for=\"age\"", "for=\"consent-box\"", "for=\"admin-token\""):
        assert label in html


def test_page_script_never_writes_html_from_text():
    js = (WEB / "app.js").read_text(encoding="utf-8")
    for bad in ("innerHTML", "outerHTML", "insertAdjacentHTML", "document.write", "eval(", "new Function", "localStorage"):
        assert bad not in js, bad
    assert "sessionStorage" in js and "textContent" in js
    assert not re.search(r"https?://", js)
