"""SQLite storage. Personal data (answers, free text, reports, check-ins) is encrypted at rest with Fernet.

- Key: ONTO_DATA_KEY (urlsafe base64 Fernet key) or a key file created on first use at <data_dir>/data.key (mode 0600).
  The data directory is outside the repository by default (ONTO_DATA_DIR, default ~/.onto-insight).
- Retention: records older than ONTO_RETENTION_DAYS (default 90) are purged by purge_expired().
- Nothing personal is ever logged; metadata columns hold only ids, timestamps, flags and token counts.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from cryptography.fernet import Fernet, InvalidToken

from . import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS persons (
  id TEXT PRIMARY KEY, created REAL NOT NULL, consent_at REAL, consent_version TEXT, deleted INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS readings (
  id TEXT PRIMARY KEY, person_id TEXT NOT NULL, created REAL NOT NULL, status TEXT NOT NULL,
  route TEXT, engine TEXT, input_enc BLOB, report_enc BLOB, cost_json TEXT
);
CREATE TABLE IF NOT EXISTS checkins (
  id TEXT PRIMARY KEY, person_id TEXT NOT NULL, reading_id TEXT, created REAL NOT NULL, day INTEGER, body_enc BLOB
);
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY, created REAL NOT NULL, bucket TEXT, voice TEXT, format TEXT, status TEXT NOT NULL,
  body_json TEXT NOT NULL, check_json TEXT, reviewer_note TEXT, updated REAL
);
CREATE TABLE IF NOT EXISTS costs (
  id TEXT PRIMARY KEY, created REAL NOT NULL, kind TEXT NOT NULL, ref TEXT, totals_json TEXT NOT NULL
);
"""


def _key() -> bytes:
    k = os.environ.get("ONTO_DATA_KEY")
    if k:
        return k.encode()
    p = config.data_dir() / "data.key"
    if not p.exists():
        p.write_bytes(Fernet.generate_key())
        p.chmod(0o600)
    return p.read_bytes().strip()


class Store:
    def __init__(self, path: Optional[Path] = None):
        self.path = Path(path) if path else config.data_dir() / "insight.sqlite3"
        self.db = sqlite3.connect(str(self.path), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.executescript(SCHEMA)
        self.f = Fernet(_key())

    # --- encryption helpers -------------------------------------------------------------
    def enc(self, obj: Any) -> bytes:
        return self.f.encrypt(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

    def dec(self, blob: Optional[bytes]) -> Any:
        if blob is None:
            return None
        try:
            return json.loads(self.f.decrypt(blob).decode("utf-8"))
        except InvalidToken:
            raise RuntimeError("cannot decrypt stored data: the data key has changed") from None

    # --- persons and consent ------------------------------------------------------------
    def new_person(self) -> str:
        pid = uuid.uuid4().hex
        self.db.execute("INSERT INTO persons(id, created) VALUES (?, ?)", (pid, time.time()))
        self.db.commit()
        return pid

    def give_consent(self, pid: str, version: str) -> None:
        self.db.execute("UPDATE persons SET consent_at=?, consent_version=? WHERE id=? AND deleted=0",
                        (time.time(), version, pid))
        self.db.commit()

    def has_consent(self, pid: str) -> bool:
        r = self.db.execute("SELECT consent_at FROM persons WHERE id=? AND deleted=0", (pid,)).fetchone()
        return bool(r and r["consent_at"])

    # --- readings -----------------------------------------------------------------------
    def save_reading(self, pid: str, status: str, route: str, engine: str, inputs: Any, report: Any,
                     cost: Optional[dict] = None) -> str:
        rid = uuid.uuid4().hex
        self.db.execute("INSERT INTO readings VALUES (?,?,?,?,?,?,?,?,?)",
                        (rid, pid, time.time(), status, route, engine, self.enc(inputs),
                         self.enc(report) if report is not None else None, json.dumps(cost or {})))
        self.db.commit()
        return rid

    def get_reading(self, rid: str) -> Optional[dict]:
        r = self.db.execute("SELECT * FROM readings WHERE id=?", (rid,)).fetchone()
        if not r:
            return None
        return {"id": r["id"], "person_id": r["person_id"], "created": r["created"], "status": r["status"],
                "route": r["route"], "engine": r["engine"], "inputs": self.dec(r["input_enc"]),
                "report": self.dec(r["report_enc"]), "cost": json.loads(r["cost_json"] or "{}")}

    # --- check-ins ----------------------------------------------------------------------
    def add_checkin(self, pid: str, rid: Optional[str], day: int, body: Any) -> str:
        cid = uuid.uuid4().hex
        self.db.execute("INSERT INTO checkins VALUES (?,?,?,?,?,?)", (cid, pid, rid, time.time(), day, self.enc(body)))
        self.db.commit()
        return cid

    def list_checkins(self, pid: str) -> list:
        rows = self.db.execute("SELECT * FROM checkins WHERE person_id=? ORDER BY created", (pid,)).fetchall()
        return [{"id": r["id"], "reading_id": r["reading_id"], "day": r["day"], "created": r["created"],
                 "body": self.dec(r["body_enc"])} for r in rows]

    # --- data controls ------------------------------------------------------------------
    def export_person(self, pid: str) -> dict:
        p = self.db.execute("SELECT * FROM persons WHERE id=?", (pid,)).fetchone()
        if not p:
            return {}
        rids = [r["id"] for r in self.db.execute("SELECT id FROM readings WHERE person_id=?", (pid,))]
        return {"person": {"id": p["id"], "created": p["created"], "consent_at": p["consent_at"],
                           "consent_version": p["consent_version"]},
                "readings": [self.get_reading(r) for r in rids], "checkins": self.list_checkins(pid)}

    def delete_person(self, pid: str) -> int:
        n = 0
        for t in ("readings", "checkins"):
            n += self.db.execute(f"DELETE FROM {t} WHERE person_id=?", (pid,)).rowcount
        self.db.execute("DELETE FROM persons WHERE id=?", (pid,))
        self.db.commit()
        self.db.execute("VACUUM")
        return n

    def purge_expired(self, days: Optional[int] = None) -> int:
        cutoff = time.time() - 86400 * (days if days is not None else config.retention_days())
        n = 0
        for t in ("readings", "checkins"):
            n += self.db.execute(f"DELETE FROM {t} WHERE created < ?", (cutoff,)).rowcount
        n += self.db.execute("DELETE FROM persons WHERE created < ? AND id NOT IN (SELECT person_id FROM readings) "
                             "AND id NOT IN (SELECT person_id FROM checkins)", (cutoff,)).rowcount
        self.db.commit()
        return n

    # --- posts (review queue; no personal data) -----------------------------------------
    def add_post(self, bucket: str, voice: str, fmt: str, body: dict, check: dict, status: str = "pending") -> str:
        pid = uuid.uuid4().hex
        self.db.execute("INSERT INTO posts VALUES (?,?,?,?,?,?,?,?,?,?)",
                        (pid, time.time(), bucket, voice, fmt, status, json.dumps(body, ensure_ascii=False),
                         json.dumps(check, ensure_ascii=False), None, time.time()))
        self.db.commit()
        return pid

    def list_posts(self, status: Optional[str] = None) -> list:
        q, a = "SELECT * FROM posts", ()
        if status:
            q, a = q + " WHERE status=?", (status,)
        rows = self.db.execute(q + " ORDER BY created", a).fetchall()
        return [dict(r) | {"body": json.loads(r["body_json"]), "check": json.loads(r["check_json"] or "{}")} for r in rows]

    def review_post(self, post_id: str, action: str, note: str = "", new_body: Optional[dict] = None) -> bool:
        status = {"approve": "approved", "reject": "rejected", "edit": "edited"}.get(action)
        if not status:
            raise ValueError("action must be approve, edit or reject")
        if new_body is not None:
            self.db.execute("UPDATE posts SET body_json=? WHERE id=?", (json.dumps(new_body, ensure_ascii=False), post_id))
        cur = self.db.execute("UPDATE posts SET status=?, reviewer_note=?, updated=? WHERE id=?",
                              (status, note, time.time(), post_id))
        self.db.commit()
        return cur.rowcount == 1

    # --- costs --------------------------------------------------------------------------
    def add_cost(self, kind: str, ref: str, totals: dict) -> None:
        self.db.execute("INSERT INTO costs VALUES (?,?,?,?,?)", (uuid.uuid4().hex, time.time(), kind, ref, json.dumps(totals)))
        self.db.commit()

    def cost_summary(self) -> dict:
        out = {}
        for r in self.db.execute("SELECT kind, totals_json FROM costs"):
            t = json.loads(r["totals_json"])
            s = out.setdefault(r["kind"], {"count": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0})
            s["count"] += 1
            s["cost_usd"] = round(s["cost_usd"] + t.get("cost_usd", 0.0), 6)
            s["input_tokens"] += t.get("input_tokens", 0)
            s["output_tokens"] += t.get("output_tokens", 0)
        for s in out.values():
            s["avg_cost_usd"] = round(s["cost_usd"] / s["count"], 6) if s["count"] else 0.0
        return out
