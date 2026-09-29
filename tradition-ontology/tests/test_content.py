"""Content engine: rules drafts pass the rules checks, near-duplicates and claims are rejected, 30-day calendar.
If rules/content/buckets.json is absent, a small fixture (tests/fixtures/content_fixture.json) stands in for it."""
import json
from pathlib import Path

import pytest

from insight import config, content
from conftest import client_with

FIXTURE = json.loads((Path(__file__).parent / "fixtures" / "content_fixture.json").read_text("utf-8"))
REAL = (config.RULES / "content" / "buckets.json").exists()
FORMATS = ["x_post", "x_thread", "ig_carousel", "short_video", "long_video"]


@pytest.fixture(autouse=True)
def _cfg(monkeypatch):
    if not REAL:
        b = {x["id"]: x for x in FIXTURE["buckets"]}
        monkeypatch.setattr(content, "buckets", lambda: b)
        monkeypatch.setattr(content, "formats", lambda: FIXTURE["formats"])


@pytest.fixture
def bucket():
    return next(iter(content.buckets()))


def test_the_five_formats_exist():
    assert set(FORMATS) <= set(content.formats()) | set(content.DEFAULT_FORMATS)


@pytest.mark.parametrize("fmt", FORMATS)
def test_rules_draft_passes_rules_check(store, bucket, fmt):
    picked = content.pick(store, bucket, fmt)
    assert picked, "the bucket must have an unused (scene, teaching) pair"
    scene, item = picked
    body = content.rules_draft(bucket, fmt, scene, item)
    chk = content.rules_check(store, body)
    assert chk["passed"], chk["problems"]
    assert body["source"] in content.post_text(body) and body["parts"] and body["ai_label"]
    assert content.claims.scan(content.post_text(body)) == []


@pytest.mark.parametrize("fmt", FORMATS)
def test_draft_batch_queues_pending_posts_with_rules_engine(store, bucket, fmt):
    out = content.draft_batch(store, bucket, fmt, n=2, engine="rules")
    assert out["engine"] == "rules" and len(out["queued"]) == 2 and out["cost"]["calls"] == 0
    posts = store.list_posts("pending")
    assert len(posts) == 2 and all(p["format"] == fmt and p["bucket"] == bucket for p in posts)
    assert all(p["check"]["passed"] for p in posts)


def test_the_same_scene_and_teaching_are_not_reused_and_a_teaching_at_most_once_in_30_days(store, bucket):
    n = len(content.buckets()[bucket]["teaching_pool"])
    out = content.draft_batch(store, bucket, "x_post", n=n + 5, engine="rules")
    tids = [p["body"]["tid"] for p in store.list_posts()]
    assert len(tids) == len(set(tids)) <= n
    assert out["failed"] and "30 days" in json.dumps(out["failed"]) or len(out["queued"]) == n


def test_unknown_bucket_is_an_error(store):
    with pytest.raises(ValueError):
        content.draft_batch(store, "not-a-bucket", "x_post", 1, engine="rules")


def test_near_duplicate_is_rejected(store, bucket):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    assert content.rules_check(store, body)["passed"]
    store.add_post(bucket, bucket, "x_post", body, {"passed": True})
    again = content.rules_check(store, dict(body))
    assert not again["passed"] and any("near-duplicate" in p for p in again["problems"])
    assert again["max_similarity"] >= 0.5
    # a lightly reworded copy is still too close
    tweaked = dict(body, parts=[body["parts"][0].replace("Your", "The").replace(" and ", " & ")])
    assert not content.rules_check(store, tweaked)["passed"]


def test_rejected_posts_do_not_block_a_redraft(store, bucket):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    pid = store.add_post(bucket, bucket, "x_post", body, {"passed": True})
    store.review_post(pid, "reject", "no")
    assert content.rules_check(store, body)["passed"]


def test_claims_are_rejected(store, bucket):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    bad = dict(body, parts=[body["parts"][0] + " This will cure your anxiety."])
    chk = content.rules_check(store, bad)
    assert not chk["passed"] and any("forbidden claim" in p for p in chk["problems"])


def test_personal_data_and_missing_source_and_uncitable_teaching_are_rejected(store, bucket):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    email = dict(body, parts=[body["parts"][0] + " Write to me at someone@example.com"])
    assert any("personal data" in p for p in content.rules_check(store, email)["problems"])
    nosrc = dict(body, parts=[body["parts"][0].replace(body["source"], "an old text")])
    assert any("source line missing" in p for p in content.rules_check(store, nosrc)["problems"])
    fake = dict(body, tid="tea:invented-text:9.9")
    assert any("not citable" in p for p in content.rules_check(store, fake)["problems"])


def test_length_limits(store, bucket):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    long = dict(body, parts=[body["parts"][0] + " x" * 300])
    assert any("character limit" in p for p in content.rules_check(store, long)["problems"])
    two = dict(body, parts=body["parts"] * 2)
    assert any("parts" in p for p in content.rules_check(store, two)["problems"])


def test_every_pool_teaching_is_citable_and_not_restricted(bucket):
    from insight import ontology
    for b in content.buckets().values():
        for it in b["teaching_pool"]:
            assert ontology.citable(it["tid"]), it["tid"]
        assert b["scenes"] and not any("@" in s for s in b["scenes"])


def test_calendar_has_30_days_and_uses_only_live_posts(store, bucket):
    content.draft_batch(store, bucket, "x_post", n=1, engine="rules")
    content.draft_batch(store, bucket, "x_thread", n=1, engine="rules")
    rejected = store.list_posts()[0]["id"]
    store.review_post(rejected, "reject", "no")
    cal = content.calendar(store, bucket)
    assert len(cal) == 30 and [d["day"] for d in cal] == list(range(1, 31))
    ids = [d["post_id"] for d in cal if d["post_id"]]
    assert rejected not in ids and len(ids) == len(set(ids)) == 1
    assert all(d["status"] == "to draft" for d in cal if not d["post_id"])
    assert len(content.calendar(store, bucket, days=7)) == 7


def test_calendar_prefers_approved_over_pending(store, bucket):
    content.draft_batch(store, bucket, "x_post", n=2, engine="rules")
    first, second = [p["id"] for p in store.list_posts()]
    store.review_post(second, "approve", "")
    cal = content.calendar(store, bucket)
    assert cal[0]["post_id"] == second and cal[0]["status"] == "approved"


def test_the_app_has_no_posting_function():
    names = [n.lower() for n in dir(content)]
    assert not [n for n in names if n.startswith(("publish", "post_to", "tweet", "send_"))]


def _draft_from_request(kw):
    """A stand-in for the model: reads the scene and teaching in the request and writes one short, faithful post."""
    req = json.loads(kw["messages"][0]["content"])
    src, point = req["teaching"]["source_line"], req["teaching"]["point"]
    return {"parts": [f"{req['scene']} {point}"[:250 - len(src)] + f" ({src})"], "caption": ""}


CHECK_OK = {"faithful": True, "claims": [], "idea_specific": True, "stretch": False, "reason": "ok"}


def test_model_drafts_go_through_model_check(store, bucket):
    c, t = client_with({"content_draft": _draft_from_request, "content_check": CHECK_OK})
    out = content.draft_batch(store, bucket, "x_post", n=1, engine="model", client=c)
    steps = [s for s, _ in t.calls]
    assert out["engine"] == "model" and steps == ["content_draft", "content_check"]
    assert len(out["queued"]) == 1 and out["cost"]["calls"] == 2
    assert store.cost_summary()["content"]["count"] == 1
    assert store.list_posts()[0]["body"]["engine"] == "model"


def test_model_check_failure_keeps_the_draft_out_of_the_queue(store, bucket):
    bad = dict(CHECK_OK, faithful=False, stretch=True, reason="stretch")
    c, _ = client_with({"content_draft": _draft_from_request, "content_check": bad})
    out = content.draft_batch(store, bucket, "x_post", n=1, engine="model", client=c)
    assert out["queued"] == [] and store.list_posts() == []


def test_model_error_falls_back_to_rules_draft_but_check_step_error_blocks(store, bucket):
    c, _ = client_with({"content_draft": RuntimeError("down"), "content_check": RuntimeError("down")})
    out = content.draft_batch(store, bucket, "x_post", n=1, engine="model", client=c)
    assert out["queued"] == [] and any("draft step failed" in json.dumps(f) for f in out["failed"])


# --- red team F22: a line break cannot split a restricted practice; stop-medication and plural astrology terms ---------
@pytest.mark.parametrize("extra", ["Tonight, hold your\nbreath for as long as you can.",
                                   "Quit your medication; this verse is all the medicine you need.",
                                   "For all twelve rashis and the nine grahas, this verse pleases Shanidev."])
def test_red_team_rerun2_bad_edits_fail_the_checks(store, bucket, extra):
    scene, item = content.pick(store, bucket, "x_post")
    body = content.rules_draft(bucket, "x_post", scene, item)
    bad = dict(body, parts=[extra + " " + body["parts"][0]])
    assert not content.rules_check(store, bad)["passed"]
