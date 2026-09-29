"""Encrypted store: nothing personal at rest in plaintext; export, delete and purge work."""
import sqlite3
import time

import pytest

from insight import config
from insight.store import Store

SECRET = "PLAINTEXT-MARKER-zebra-quartz-8812"


def _raw_bytes(store):
    store.db.commit()
    out = b""
    for p in config.data_dir().iterdir():
        if p.name.startswith("insight.sqlite3"):
            out += p.read_bytes()
    return out


def test_encryption_at_rest(store):
    pid = store.new_person()
    store.give_consent(pid, "v1")
    store.save_reading(pid, "ok", "continue", "rules", {"answers": {"q01": SECRET}}, {"summary": SECRET + " report"})
    store.add_checkin(pid, None, 1, {"text": SECRET + " checkin"})
    raw = _raw_bytes(store)
    assert raw and SECRET.encode() not in raw
    # the stored values are Fernet tokens
    row = store.db.execute("SELECT input_enc, report_enc FROM readings").fetchone()
    assert row["input_enc"].startswith(b"gAAAA") and row["report_enc"].startswith(b"gAAAA")
    # and they round-trip
    rid = store.db.execute("SELECT id FROM readings").fetchone()["id"]
    assert store.get_reading(rid)["inputs"]["answers"]["q01"] == SECRET


def test_key_file_is_private_and_used_again(store):
    kf = config.data_dir() / "data.key"
    assert kf.exists() and (kf.stat().st_mode & 0o777) == 0o600
    pid = store.new_person(); store.give_consent(pid, "v1")
    rid = store.save_reading(pid, "ok", "continue", "rules", {"a": 1}, {"b": 2})
    again = Store()
    assert again.get_reading(rid)["report"] == {"b": 2}
    again.db.close()


def test_env_key_is_used(monkeypatch, tmp_path):
    from cryptography.fernet import Fernet
    k = Fernet.generate_key().decode()
    monkeypatch.setenv("ONTO_DATA_KEY", k)
    monkeypatch.setenv("ONTO_DATA_DIR", str(tmp_path / "other"))
    s = Store()
    assert not (config.data_dir() / "data.key").exists()
    pid = s.new_person(); s.give_consent(pid, "v1")
    rid = s.save_reading(pid, "ok", "continue", "rules", {"a": SECRET}, {})
    assert s.get_reading(rid)["inputs"]["a"] == SECRET
    s.db.close()


def test_wrong_key_cannot_read(store, monkeypatch):
    from cryptography.fernet import Fernet
    pid = store.new_person(); store.give_consent(pid, "v1")
    rid = store.save_reading(pid, "ok", "continue", "rules", {"a": 1}, {})
    monkeypatch.setenv("ONTO_DATA_KEY", Fernet.generate_key().decode())
    other = Store()
    with pytest.raises(RuntimeError):
        other.get_reading(rid)
    other.db.close()


def test_consent_required_flag(store):
    pid = store.new_person()
    assert not store.has_consent(pid)
    store.give_consent(pid, "v1")
    assert store.has_consent(pid)
    assert not store.has_consent("nope")


def test_export_holds_everything(store):
    pid = store.new_person(); store.give_consent(pid, "v1")
    rid = store.save_reading(pid, "ok", "continue", "rules", {"x": 1}, {"summary": "s"})
    store.add_checkin(pid, rid, 2, {"text": "t"})
    ex = store.export_person(pid)
    assert ex["person"]["id"] == pid and ex["person"]["consent_version"] == "v1"
    assert ex["readings"][0]["report"] == {"summary": "s"} and ex["checkins"][0]["body"] == {"text": "t"}
    assert store.export_person("nobody") == {}


def test_export_excludes_other_persons(store):
    a, b = store.new_person(), store.new_person()
    store.give_consent(a, "v1"); store.give_consent(b, "v1")
    store.save_reading(a, "ok", "continue", "rules", {"who": "a"}, {})
    store.save_reading(b, "ok", "continue", "rules", {"who": "b"}, {})
    assert [r["inputs"]["who"] for r in store.export_person(a)["readings"]] == ["a"]


def test_delete_removes_rows_and_bytes(store):
    pid = store.new_person(); store.give_consent(pid, "v1")
    other = store.new_person(); store.give_consent(other, "v1")
    store.save_reading(pid, "ok", "continue", "rules", {"x": 1}, {})
    store.add_checkin(pid, None, 1, {"text": "t"})
    store.save_reading(other, "ok", "continue", "rules", {"x": 2}, {})
    assert store.delete_person(pid) == 2
    for t in ("readings", "checkins"):
        assert store.db.execute(f"SELECT COUNT(*) c FROM {t} WHERE person_id=?", (pid,)).fetchone()["c"] == 0
    assert store.db.execute("SELECT COUNT(*) c FROM persons WHERE id=?", (pid,)).fetchone()["c"] == 0
    assert not store.has_consent(pid)
    assert store.export_person(other)["readings"]          # someone else's data is untouched


def test_purge_by_age(store):
    pid = store.new_person(); store.give_consent(pid, "v1")
    old = store.save_reading(pid, "ok", "continue", "rules", {"x": 1}, {})
    new = store.save_reading(pid, "ok", "continue", "rules", {"x": 2}, {})
    store.add_checkin(pid, None, 1, {"text": "old"})
    long_ago = time.time() - 100 * 86400
    store.db.execute("UPDATE readings SET created=? WHERE id=?", (long_ago, old))
    store.db.execute("UPDATE checkins SET created=?", (long_ago,))
    store.db.commit()
    assert store.purge_expired() == 2                       # default retention is 90 days
    assert store.get_reading(old) is None and store.get_reading(new) is not None
    assert store.purge_expired(days=0) >= 1                 # explicit days
    assert store.get_reading(new) is None


def test_purge_honours_env_retention(store, monkeypatch):
    monkeypatch.setenv("ONTO_RETENTION_DAYS", "1")
    pid = store.new_person(); store.give_consent(pid, "v1")
    rid = store.save_reading(pid, "ok", "continue", "rules", {"x": 1}, {})
    store.db.execute("UPDATE readings SET created=?", (time.time() - 2 * 86400,))
    store.db.commit()
    assert store.purge_expired() == 1 and store.get_reading(rid) is None


def test_posts_and_costs_hold_no_personal_columns(store):
    cols = {r["name"] for r in store.db.execute("PRAGMA table_info(posts)")}
    assert not ({"person_id", "input_enc"} & cols)
    store.add_cost("reading", "r1", {"cost_usd": 0.5, "input_tokens": 10, "output_tokens": 5})
    store.add_cost("reading", "r2", {"cost_usd": 0.25, "input_tokens": 10, "output_tokens": 5})
    s = store.cost_summary()["reading"]
    assert s["count"] == 2 and s["cost_usd"] == 0.75 and s["avg_cost_usd"] == 0.375


def test_review_post(store):
    pid = store.add_post("b", "b", "x_post", {"parts": ["a"]}, {"passed": True})
    assert store.review_post(pid, "approve", "ok")
    assert store.list_posts("approved")[0]["id"] == pid
    assert not store.review_post("missing", "reject")
    with pytest.raises(ValueError):
        store.review_post(pid, "publish")
