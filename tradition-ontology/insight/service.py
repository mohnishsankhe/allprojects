"""The one service layer behind both the web app (insight/api.py) and the CLI (insight/cli.py).

Every rule that protects the person lives here or below, so the two interfaces cannot drift apart:
- adults only, and explicit consent before any processing;
- the safety screen runs first on every reading and every check-in;
- personal data is stored only encrypted, and only for the person's own use (view, export, delete);
- logs carry ids, routes and error kinds, never text.
"""
from __future__ import annotations

import logging
from typing import Optional

from . import config, report as report_mod, safety
from .engine import run_reading
from .llm import Ledger, ModelClient
from .store import Store

log = logging.getLogger("insight")


class ServiceError(Exception):
    def __init__(self, code: str, message: str, status: int = 400):
        super().__init__(message)
        self.code, self.message, self.status = code, message, status


def consent_info() -> dict:
    return config.json_file("rules/consent.json")


def intake_questions() -> list[dict]:
    return [{k: q[k] for k in ("id", "text", "type", "optional") if k in q}
            for q in config.json_file("rules/intake.json")["questions"]]


def _age_ok(age) -> Optional[int]:
    try:
        a = int(float(str(age).strip()))          # '17.5' is 17 (red team F6): never rounded up into adulthood
    except (TypeError, ValueError, OverflowError):   # 'inf' and 'nan' are not ages
        return None
    return a if 0 < a < 130 else None


def _stop_report(msg: dict, route: str, engine: str) -> dict:
    """A stop or decline that keeps nothing still has the report's shape (schema-valid): no words, no mappings."""
    import time
    return {"engine": engine, "created": time.time(), "stopped": msg,
            "safety": {"route": route, "categories": [], "model_checked": False, "injection": False}}


class Service:
    def __init__(self, store: Optional[Store] = None, client: Optional[ModelClient] = None):
        self.store = store or Store()
        self.client = client

    # --- consent -----------------------------------------------------------------------------
    def start(self, age, consent: bool) -> dict:
        """Returns {"person_id"} or {"declined": message}. Nothing is stored for a minor or without consent."""
        c = consent_info()
        a = _age_ok(age)
        if a is None:
            raise ServiceError("age_required", "Please give your age as a number.")
        if a < c["min_age"]:
            return {"declined": safety.messages()["decline_minor"]}
        if consent is not True:
            raise ServiceError("consent_required", "The reading needs your explicit consent first.")
        pid = self.store.new_person()
        self.store.give_consent(pid, c["version"])
        log.info("person started id=%s consent=%s", pid[:8], c["version"])
        return {"person_id": pid}

    def _need(self, pid: str) -> None:
        if not pid or not self.store.has_consent(pid):
            raise ServiceError("no_consent", "No consented session was found. Please start again.", 403)

    # --- reading -----------------------------------------------------------------------------
    def _engine(self, engine: Optional[str]) -> tuple[str, Optional[ModelClient]]:
        configured = config.reading_engine()
        e = engine or configured
        if e == "rules" and configured != "rules":
            # a caller may ask for the model engine, but never step down from it: the model safety screen would be skipped
            if configured == "unavailable":
                raise ServiceError("model_unavailable", "Readings need the model engine, which is not configured on this server.", 503)
            raise ServiceError("engine_not_allowed", "This server does not make rule-only readings.", 403)
        if e == "model":
            client = self.client or ModelClient()
            if not client.available():
                raise ServiceError("model_unavailable", "The model engine is not configured on this server.", 503)
            return e, client
        if e == "rules":
            return "rules", None
        # red team F23: 'unavailable', or any value the product does not know, never falls through to rules
        raise ServiceError("model_unavailable", "Readings need the model engine, which is not configured on this server.", 503)

    def _refused(self, pid: str, texts: list[str], own: list[str], err: ServiceError) -> dict:
        """Red team F24: while readings are refused, the rules screen still runs, so a person in crisis gets the crisis
        message and helplines (a minor is declined and removed), and everyone else gets a refusal that lists help.
        Nothing is stored."""
        scr = safety.rule_screen_fields([t for t in texts if t.strip()], [o for o in own if o.strip()])
        if scr.route == "decline_minor":
            self.store.delete_person(pid)
            return {"stopped": safety.messages()["decline_minor"], "route": scr.route}
        if scr.stop:
            return {"stopped": scr.message(), "route": scr.route}
        m = safety.messages()["stop_unavailable"]
        raise ServiceError(err.code, m["body"], err.status)

    def reading(self, pid: str, inputs: dict, engine: Optional[str] = None, premium: bool = False) -> dict:
        self._need(pid)
        inputs = dict(inputs or {})
        answers = inputs.get("answers") or {}
        if "age" not in inputs and "age" in answers:
            inputs["age"] = answers.pop("age")
        a = _age_ok(inputs.get("age"))
        if a is None and inputs.get("age") not in (None, ""):
            # red team F6: an age that is not a number ("seventeen", "16 yrs") is asked again, never read as "no age"
            raise ServiceError("age_required", "Please give your age as a number.")
        if a is not None and a < consent_info()["min_age"]:
            self.store.delete_person(pid)             # red team F15: a minor is removed, whatever the route of discovery
            rep = _stop_report(safety.messages()["decline_minor"], "decline_minor", engine or "none")
            return {"reading_id": None, "report": rep, "markdown": report_mod.to_markdown(rep)}
        try:
            e, client = self._engine(engine)
        except ServiceError as err:
            if err.code != "model_unavailable":
                raise
            from .engine import build_segments
            texts = [*(str(v) for v in (inputs.get("answers") or {}).values() if isinstance(v, (str, int))),
                     inputs.get("free_text") or "", inputs.get("dialogue") or ""]
            own = [s_["text"] for s_ in build_segments(inputs)]
            if (inputs.get("dialogue") or "").strip() and not any(s_["source"] == "dialogue" for s_ in build_segments(inputs)):
                own.append(inputs["dialogue"])
            out = self._refused(pid, texts, own, err)
            rep = _stop_report(out["stopped"], out["route"], "none")
            return {"reading_id": None, "report": rep, "markdown": report_mod.to_markdown(rep)}
        rep = run_reading(inputs, engine=e, client=client, premium=premium)
        if (rep.get("safety") or {}).get("route") == "decline_minor":
            # a minor found in the text: nothing is kept, and the person record itself is removed
            self.store.delete_person(pid)
            log.info("minor detected in text: person removed id=%s", pid[:8])
            kept = _stop_report(rep.get("stopped"), "decline_minor", rep.get("engine") or e)
            kept["safety"] = rep.get("safety") or kept["safety"]
            return {"reading_id": None, "report": kept, "markdown": report_mod.to_markdown(kept)}
        status = "stopped" if rep.get("stopped") else ("insufficient" if rep.get("insufficient") else "ok")
        route = (rep.get("safety") or {}).get("route", "")
        # minimisation: after a stop, keep only the route, not the words that triggered it
        stored_inputs = inputs if status != "stopped" else {"withheld": "not kept after a safety stop"}
        rid = self.store.save_reading(pid, status, route, e, stored_inputs, rep, rep.get("cost"))
        if rep.get("cost", {}).get("calls"):
            self.store.add_cost("reading", rid, rep["cost"])
        log.info("reading id=%s status=%s route=%s engine=%s", rid[:8], status, route, e)
        return {"reading_id": rid, "report": rep, "markdown": report_mod.to_markdown(rep)}

    def get_report(self, pid: str, rid: str, fmt: str = "md"):
        self._need(pid)
        r = self.store.get_reading(rid)
        if not r or r["person_id"] != pid:
            raise ServiceError("not_found", "Reading not found.", 404)
        rep = r["report"] or {}
        if fmt == "json":
            return rep
        return report_mod.to_html(rep) if fmt == "html" else report_mod.to_markdown(rep)

    # --- check-ins ----------------------------------------------------------------------------
    def checkin(self, pid: str, rid: Optional[str], day: int, text: str, engine: Optional[str] = None) -> dict:
        """A daily check-in is screened like a reading: a crisis signal stops everything and shows help."""
        self._need(pid)
        if not (1 <= int(day) <= 60):
            raise ServiceError("bad_day", "Day must be between 1 and 60.")
        try:
            e, client = self._engine(engine)
        except ServiceError as err:
            if err.code != "model_unavailable":
                raise
            out = self._refused(pid, [text or ""], [text or ""], err)
            return {"stored": False, "stopped": out["stopped"]}
        ledger = Ledger()
        if rid:
            r = self.store.get_reading(rid)
            if not r or r["person_id"] != pid:      # red team F9: a check-in belongs to the person's own reading
                raise ServiceError("not_found", "Reading not found.", 404)
        scr = safety.screen(text or "", client=client, ledger=ledger, require_model=(e == "model"))
        msg = scr.message()
        if scr.route == "decline_minor":
            self.store.delete_person(pid)             # red team F15
            return {"stored": False, "stopped": msg}
        if scr.stop:
            log.info("checkin stopped route=%s", scr.route)
            return {"stored": False, "stopped": msg}
        cid = self.store.add_checkin(pid, rid, int(day), {"text": text, "route": scr.route})
        if ledger.totals().get("calls"):
            self.store.add_cost("checkin", cid, ledger.totals())
        return {"stored": True, "checkin_id": cid, "notes": msg.get("notes") or []}

    def checkins(self, pid: str) -> list:
        self._need(pid)
        return self.store.list_checkins(pid)

    # --- data controls ------------------------------------------------------------------------
    def my_data(self, pid: str) -> dict:
        self._need(pid)
        return self.store.export_person(pid)

    def delete_me(self, pid: str) -> dict:
        if not pid:
            raise ServiceError("no_person", "No person id given.")
        n = self.store.delete_person(pid)
        log.info("person deleted id=%s rows=%d", pid[:8], n)
        return {"deleted": True, "rows": n}

    def purge(self, days: Optional[int] = None) -> dict:
        return {"purged": self.store.purge_expired(days)}

    # --- review queue and admin ---------------------------------------------------------------
    def posts(self, status: Optional[str] = None) -> list:
        return self.store.list_posts(status)

    def review(self, post_id: str, action: str, note: str = "", new_body: Optional[dict] = None) -> dict:
        if action not in ("approve", "edit", "reject"):
            raise ServiceError("bad_action", "Action must be approve, edit or reject.")
        if action == "edit" and not new_body:
            raise ServiceError("edit_needs_body", "An edit needs the new text.")
        if new_body:
            from . import claims, content
            hits = claims.scan_fields(new_body)
            if hits:
                raise ServiceError("claims_in_edit", f"The edited text contains a forbidden claim: {hits[0]['match']!r}.")
            cur = next((p for p in self.store.list_posts() if p["id"] == post_id), None)
            if cur is None:
                raise ServiceError("not_found", "Post not found.", 404)
            # an edit keeps the post's identity (bucket, format, teaching, source) and passes the same checks as a draft
            body = {**cur["body"], **{k: v for k, v in new_body.items() if k in ("parts", "caption")}}
            chk = content.rules_check(self.store, body, exclude_id=post_id)
            if not chk["passed"]:
                raise ServiceError("edit_fails_checks", "The edited post fails the checks: " + "; ".join(chk["problems"]))
            new_body = body
        ok = self.store.review_post(post_id, action, note, new_body)
        if not ok:
            raise ServiceError("not_found", "Post not found.", 404)
        return {"ok": True}

    def costs(self) -> dict:
        return self.store.cost_summary()
