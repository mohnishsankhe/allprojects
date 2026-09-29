"""Web API (FastAPI): a thin layer over insight.service.Service. No rule lives here.

Run:  uvicorn insight.api:app

- Person routes take an opaque person id (body or query `person_id`, or the X-Person-Id header).
- Admin routes need the header X-Admin-Token to equal the environment variable ONTO_ADMIN_TOKEN;
  if that variable is unset or empty, every admin route answers 403.
- ServiceError becomes {"error": code, "message": text} with its status. Any other failure becomes
  500 {"error": "internal"}; only the exception type is logged, never any user text.
- Request bodies over MAX_BODY bytes are refused with 413. There is no CORS: only the same origin can call the API.
"""
from __future__ import annotations

import hmac
import json
import logging
import os
from contextlib import contextmanager
from typing import Any, Optional

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import run_in_threadpool

from . import config, content
from .llm import ModelClient
from .service import Service, ServiceError, consent_info, intake_questions
from .store import Store

log = logging.getLogger("insight.api")

WEB_DIR = config.ROOT / "web"
MAX_BODY = 24 * 1024          # bytes; about 20 KB of text plus JSON overhead (a full intake is under 19,000 characters)
ENGINES = ("rules", "model")

# Tests (and only tests) may inject a model client here; in production it stays None and Service builds its own.
_client: Optional[ModelClient] = None


def set_client(client: Optional[ModelClient]) -> None:
    global _client
    _client = client


@contextmanager
def _service():
    """One Store per request (SQLite connections are not shared between worker threads)."""
    svc = Service(store=Store(), client=_client)
    try:
        yield svc
    finally:
        try:
            svc.store.db.close()
        except Exception:
            pass


def _err(code: str, message: str, status: int = 400) -> ServiceError:
    return ServiceError(code, message, status)


# --- request helpers -------------------------------------------------------------------------------
async def _json_body(request: Request, limit: int = MAX_BODY) -> dict:
    declared = request.headers.get("content-length")
    if declared and declared.isdigit() and int(declared) > limit:
        raise _err("too_large", "That is too much text for one request. Please shorten it.", 413)
    chunks, size = [], 0
    async for chunk in request.stream():
        size += len(chunk)
        if size > limit:
            raise _err("too_large", "That is too much text for one request. Please shorten it.", 413)
        chunks.append(chunk)
    raw = b"".join(chunks)
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except (ValueError, UnicodeDecodeError):
        raise _err("bad_request", "The request was not valid JSON.") from None
    if not isinstance(data, dict):
        raise _err("bad_request", "The request body must be a JSON object.")
    return data


def _pid(request: Request, body: Optional[dict] = None) -> str:
    pid = (body or {}).get("person_id") or request.query_params.get("person_id") or request.headers.get("x-person-id") or ""
    if not isinstance(pid, str) or len(pid) > 64:
        raise _err("bad_request", "The person id is not valid.")
    return pid


def _admin(request: Request) -> None:
    expected = os.environ.get("ONTO_ADMIN_TOKEN", "")
    given = request.headers.get("x-admin-token", "")
    if not expected or not hmac.compare_digest(given.encode(), expected.encode()):
        raise _err("forbidden", "Admin access is not allowed.", 403)


def _str(d: dict, key: str, max_len: int, required: bool = False) -> str:
    v = d.get(key, "")
    if v is None:
        v = ""
    if not isinstance(v, str):
        raise _err("bad_request", f"'{key}' must be text.")
    if required and not v.strip():
        raise _err("bad_request", f"'{key}' is required.")
    if len(v) > max_len:
        raise _err("too_large", f"'{key}' is too long.", 413)
    return v


def _clean_inputs(raw: Any) -> dict:
    """Shape the intake into {age?, answers{qid: text}, free_text, dialogue, dialogue_speaker}; nothing else passes."""
    if not isinstance(raw, dict):
        raise _err("bad_request", "'inputs' must be an object.")
    out: dict = {}
    if raw.get("age") not in (None, ""):
        out["age"] = raw["age"] if isinstance(raw["age"], (int, str)) and not isinstance(raw["age"], bool) else None
    answers = raw.get("answers") or {}
    if not isinstance(answers, dict):
        raise _err("bad_request", "'answers' must be an object.")
    out["answers"] = {str(k)[:16]: v for k, v in answers.items() if isinstance(v, (str, int)) and not isinstance(v, bool)
                      and (isinstance(v, int) or v.strip())}
    for key, cap in (("free_text", 12000), ("dialogue", 12000), ("dialogue_speaker", 40)):
        out[key] = _str(raw, key, cap)
    return out


def _engine(body: dict) -> Optional[str]:
    e = body.get("engine")
    if e in (None, ""):
        return None
    if e not in ENGINES:
        raise _err("bad_request", "The engine must be 'rules' or 'model'.")
    return e


# --- app --------------------------------------------------------------------------------------------
app = FastAPI(title="Ontology Insight Generator", docs_url=None, redoc_url=None, openapi_url=None)

CSP = ("default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; "
       "object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
SECURITY_HEADERS = {
    "content-security-policy": CSP,
    "x-content-type-options": "nosniff",
    "referrer-policy": "no-referrer",
    "x-frame-options": "DENY",
    "cross-origin-resource-policy": "same-origin",
    "permissions-policy": "camera=(), microphone=(), geolocation=()",
}


class GuardMiddleware:
    """Outermost ASGI layer: adds the security headers to every response and turns any unexpected failure into
    500 {"error": "internal"} (logging the exception type only, so no user text can reach a log)."""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.inner(scope, receive, send)
        started = {"v": False}

        async def send_wrapped(message):
            if message["type"] == "http.response.start":
                started["v"] = True
                headers = list(message.get("headers") or [])
                present = {k.lower() for k, _ in headers}
                for k, v in SECURITY_HEADERS.items():
                    if k.encode() not in present:
                        headers.append((k.encode(), v.encode()))
                if scope.get("path", "").startswith("/api/") and b"cache-control" not in present:
                    headers.append((b"cache-control", b"no-store"))
                message = {**message, "headers": headers}
            await send(message)

        try:
            await self.inner(scope, receive, send_wrapped)
        except Exception as e:  # noqa: BLE001 - last line of defence; the type is all we record
            log.error("unhandled error type=%s", type(e).__name__)
            if not started["v"]:
                resp = JSONResponse({"error": "internal"}, status_code=500)
                await resp(scope, receive, send_wrapped)


@app.exception_handler(ServiceError)
async def _service_error(_request: Request, exc: ServiceError):
    return JSONResponse({"error": exc.code, "message": exc.message}, status_code=exc.status)


@app.exception_handler(RequestValidationError)
async def _validation_error(_request: Request, _exc: RequestValidationError):
    # the default handler echoes the offending input; ours never does
    return JSONResponse({"error": "bad_request", "message": "The request was not valid."}, status_code=400)


@app.exception_handler(404)
async def _not_found(_request: Request, _exc):
    return JSONResponse({"error": "not_found", "message": "Not found."}, status_code=404)


@app.exception_handler(405)
async def _method(_request: Request, _exc):
    return JSONResponse({"error": "method_not_allowed", "message": "Method not allowed."}, status_code=405)


# --- pages ------------------------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def index():
    return FileResponse(WEB_DIR / "index.html", media_type="text/html; charset=utf-8")


if WEB_DIR.is_dir():
    app.mount("/static", StaticFiles(directory=str(WEB_DIR)), name="static")


# --- person routes ----------------------------------------------------------------------------------
@app.get("/api/consent")
def api_consent():
    return consent_info()


@app.get("/api/questions")
def api_questions():
    return intake_questions()


@app.post("/api/start")
async def api_start(request: Request):
    body = await _json_body(request)

    def go():
        with _service() as svc:
            return svc.start(body.get("age"), body.get("consent"))
    return await run_in_threadpool(go)


@app.post("/api/reading")
async def api_reading(request: Request):
    body = await _json_body(request)
    pid = _pid(request, body)
    inputs = _clean_inputs(body.get("inputs") or {})
    engine = _engine(body)

    def go():
        with _service() as svc:
            return svc.reading(pid, inputs, engine=engine)
    return await run_in_threadpool(go)


@app.get("/api/reading/{rid}")
def api_get_reading(rid: str, request: Request):
    pid = _pid(request)
    fmt = request.query_params.get("format", "md")
    if fmt not in ("md", "html", "json"):
        raise _err("bad_request", "The format must be md, html or json.")
    with _service() as svc:
        out = svc.get_report(pid, rid[:64], fmt)
    if fmt == "json":
        return JSONResponse(out)
    if fmt == "html":
        # the HTML is built from escaped text and carries its own small stylesheet, so it gets its own policy
        return HTMLResponse(out, headers={"content-security-policy": "default-src 'none'; style-src 'unsafe-inline'"})
    return PlainTextResponse(out, media_type="text/markdown; charset=utf-8")


@app.post("/api/checkin")
async def api_checkin(request: Request):
    body = await _json_body(request)
    pid = _pid(request, body)
    text = _str(body, "text", 4000, required=True)
    rid = body.get("reading_id")
    if rid is not None and (not isinstance(rid, str) or len(rid) > 64):
        raise _err("bad_request", "The reading id is not valid.")
    day = body.get("day")
    if isinstance(day, bool) or not isinstance(day, int):
        raise _err("bad_day", "Day must be a whole number between 1 and 60.")
    engine = _engine(body)

    def go():
        with _service() as svc:
            return svc.checkin(pid, rid, day, text, engine=engine)
    return await run_in_threadpool(go)


@app.get("/api/checkins")
def api_checkins(request: Request):
    pid = _pid(request)
    with _service() as svc:
        return svc.checkins(pid)


@app.get("/api/me")
def api_me(request: Request):
    pid = _pid(request)
    with _service() as svc:
        return svc.my_data(pid)


@app.delete("/api/me")
def api_delete_me(request: Request):
    pid = _pid(request)
    with _service() as svc:
        return svc.delete_me(pid)


# --- admin routes -----------------------------------------------------------------------------------
@app.get("/api/admin/costs")
def admin_costs(request: Request):
    _admin(request)
    with _service() as svc:
        return svc.costs()


@app.get("/api/admin/posts")
def admin_posts(request: Request):
    _admin(request)
    status = request.query_params.get("status") or None
    if status and status not in ("pending", "approved", "edited", "rejected"):
        raise _err("bad_request", "Unknown status.")
    with _service() as svc:
        return svc.posts(status)


@app.post("/api/admin/posts/{post_id}/review")
async def admin_review(post_id: str, request: Request):
    _admin(request)
    body = await _json_body(request)
    action = _str(body, "action", 16)
    note = _str(body, "note", 1000)
    new_body = body.get("body")
    if new_body is not None and not isinstance(new_body, dict):
        raise _err("bad_request", "'body' must be an object.")

    def go():
        with _service() as svc:
            return svc.review(post_id[:64], action, note, new_body)
    return await run_in_threadpool(go)


@app.post("/api/admin/drafts")
async def admin_drafts(request: Request):
    _admin(request)
    body = await _json_body(request)
    bucket = _str(body, "bucket", 64, required=True)
    fmt = _str(body, "format", 32, required=True)
    n = body.get("n", 1)
    if isinstance(n, bool) or not isinstance(n, int) or not 1 <= n <= 20:
        raise _err("bad_request", "'n' must be a whole number from 1 to 20.")
    if bucket not in content.buckets():
        raise _err("unknown_bucket", "That bucket is not known.")
    if fmt not in content.formats() and fmt not in content.DEFAULT_FORMATS:
        raise _err("unknown_format", "That format is not known.")
    engine = _engine(body)

    def go():
        with _service() as svc:
            return content.draft_batch(svc.store, bucket, fmt, n, engine=engine, client=_client)
    return await run_in_threadpool(go)


@app.get("/api/admin/calendar")
def admin_calendar(request: Request):
    _admin(request)
    bucket = request.query_params.get("bucket", "")
    if bucket not in content.buckets():
        raise _err("unknown_bucket", "That bucket is not known.")
    with _service() as svc:
        return content.calendar(svc.store, bucket)


@app.post("/api/admin/purge")
async def admin_purge(request: Request):
    _admin(request)
    body = await _json_body(request)
    days = body.get("days")
    if days is not None and (isinstance(days, bool) or not isinstance(days, int) or days < 0):
        raise _err("bad_request", "'days' must be a whole number.")

    def go():
        with _service() as svc:
            return svc.purge(days)
    return await run_in_threadpool(go)


@app.get("/api/admin/buckets")
def admin_buckets(request: Request):
    """Bucket and format names for the review page's draft form (no other data)."""
    _admin(request)
    return {"buckets": [{"id": k, "name": v.get("name", k)} for k, v in content.buckets().items()],
            "formats": sorted(set(content.formats()) | set(content.DEFAULT_FORMATS))}


app = GuardMiddleware(app)  # type: ignore[assignment]  # uvicorn insight.api:app serves the guarded app
