"""Polite HTTP for the full-text adapters (rule 4).

Rate-limited per domain, cached in cache/http/, robots.txt honoured (cached in
cache/robots/), retries on 429 and 5xx with Retry-After, no retries on 401/403.
`FUNNEL_OFFLINE=1` makes every network call raise NetworkBlocked at once.
API keys never reach the cache: query parameters named key, api_key, access_token,
client_secret and token are stripped from cache keys and stored URLs.

Public API
----------
    class FetchError(Exception)          .url, .status (HTTP status or None)
    class NetworkBlocked(common.Blocked, FetchError)   .domain; exit code 3
    class RobotsDisallowed(FetchError)   .url
    offline() -> bool                    FUNNEL_OFFLINE == "1"
    strip_key_params(url) -> str         the URL without secret query parameters
    cache_key(url, params=None) -> str   sha256 hex of the stripped URL (+ params)
    cache_path(url, params=None) -> Path cache/http/<key>.json
    fetch(url, params=None, headers=None, use_cache=True, respect_robots=True,
          timeout=30, max_tries=4) -> dict
        {"url": stripped url, "status": int, "text": str, "headers": {...}, "from_cache": bool}
    fetch_json(url, params=None, headers=None, **kw) -> object
    robots_allowed(url, user_agent=None) -> bool     raises NetworkBlocked when it cannot read robots.txt
    robots_text(domain) -> str                       the cached robots.txt (fetches it once)
    probe(domain, timeout=10) -> dict                {"domain", "status": reachable|blocked_by_network|error, "detail"}
    html_to_text(html) -> str
    extract_date(html, url=None) -> (date | None, "page"|"url"|"none")
    date_from_url(url) -> str | None     /YYYY/MM/DD/, /YYYY/MM/ (day 01) or YYYY-MM-DD in the path
    user_agent() -> str                  env FUNNEL_USER_AGENT or a plain research agent string

Environment knobs: FUNNEL_MIN_INTERVAL (seconds between requests to one domain, default 1.0),
FUNNEL_RETRY_BASE_SECONDS (default 1.0), FUNNEL_HTTP_TIMEOUT (default 30).
Tests replace `_http_get` and `_sleep`.
"""
from __future__ import annotations

import datetime as _dt
import email.utils
import hashlib
import html as _html
import json
import os
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib import robotparser
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import requests

import common

SECRET_PARAMS = frozenset({"key", "api_key", "access_token", "client_secret", "token"})
RETRY_STATUSES = frozenset({429, 500, 502, 503, 504})
NO_RETRY_STATUSES = frozenset({401, 403})
DEFAULT_USER_AGENT = "opportunity-funnel/1.0 (research; polite; respects robots.txt)"

_last_request_at: dict[str, float] = {}


# --------------------------------------------------------------------------- errors
class FetchError(Exception):
    def __init__(self, message: str, url: str = "", status: int | None = None):
        super().__init__(message)
        self.url = url
        self.status = status


class NetworkBlocked(common.Blocked, FetchError):
    """The network policy blocks a domain. Exit code 3. Names the domain."""

    def __init__(self, domain: str, detail: str = ""):
        self.domain = domain
        msg = f"Network blocked: cannot reach {domain}."
        if detail:
            msg += f" ({detail})"
        msg += f" Allow the domain {domain} or skip this source."
        common.Blocked.__init__(self, msg, common.EXIT_BLOCKED)
        self.url = ""
        self.status = None


class RobotsDisallowed(FetchError):
    def __init__(self, url: str, detail: str = ""):
        domain = common.domain_of(url)
        msg = f"robots.txt on {domain} does not allow fetching {url}."
        if detail:
            msg += f" ({detail})"
        super().__init__(msg, url=url, status=None)


# --------------------------------------------------------------------------- switches
def offline() -> bool:
    return os.environ.get("FUNNEL_OFFLINE", "") == "1"


def user_agent() -> str:
    return os.environ.get("FUNNEL_USER_AGENT") or DEFAULT_USER_AGENT


def _min_interval() -> float:
    try:
        return float(os.environ.get("FUNNEL_MIN_INTERVAL", "1.0"))
    except ValueError:
        return 1.0


def _retry_base() -> float:
    try:
        return float(os.environ.get("FUNNEL_RETRY_BASE_SECONDS", "1.0"))
    except ValueError:
        return 1.0


def _sleep(seconds: float) -> None:
    if seconds > 0:
        time.sleep(seconds)


def _http_get(url: str, params=None, headers=None, timeout: float = 30):
    """The one place that talks to the network. Tests replace it."""
    return requests.get(url, params=params, headers=headers, timeout=timeout, allow_redirects=True)


# --------------------------------------------------------------------------- urls and cache
def strip_key_params(url: str) -> str:
    parts = urlsplit(str(url))
    if not parts.query:
        return str(url)
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k.lower() not in SECRET_PARAMS]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), parts.fragment))


def _full_url(url: str, params=None) -> str:
    if not params:
        return str(url)
    items = sorted((str(k), str(v)) for k, v in dict(params).items())
    parts = urlsplit(str(url))
    query = parts.query
    extra = urlencode(items)
    query = f"{query}&{extra}" if query else extra
    return urlunsplit((parts.scheme, parts.netloc, parts.path, query, parts.fragment))


def public_url(url: str, params=None) -> str:
    """The URL as it may be stored or shown: parameters merged, secrets stripped."""
    return strip_key_params(_full_url(url, params))


def cache_key(url: str, params=None) -> str:
    return hashlib.sha256(public_url(url, params).encode("utf-8")).hexdigest()


def cache_dir() -> Path:
    return common.funnel_root() / "cache" / "http"


def robots_dir() -> Path:
    return common.funnel_root() / "cache" / "robots"


def cache_path(url: str, params=None) -> Path:
    return cache_dir() / f"{cache_key(url, params)}.json"


def _read_cache(url: str, params=None):
    p = cache_path(url, params)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    data["from_cache"] = True
    return data


def _write_cache(url: str, params, result: dict) -> None:
    p = cache_path(url, params)
    p.parent.mkdir(parents=True, exist_ok=True)
    stored = {k: v for k, v in result.items() if k != "from_cache"}
    stored["url"] = public_url(url, params)
    stored["fetched_at"] = _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat()
    p.write_text(json.dumps(stored, sort_keys=True, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- blocked detection
def _is_tunnel_block(exc: BaseException) -> bool:
    if isinstance(exc, requests.exceptions.ProxyError):
        return True
    text = str(exc).lower()
    return ("tunnel" in text and ("403" in text or "407" in text)) or "proxy" in text and "403" in text


def _response_is_proxy_block(resp) -> bool:
    if getattr(resp, "status_code", None) not in (403, 407):
        return False
    headers = {str(k).lower(): str(v).lower() for k, v in dict(getattr(resp, "headers", {}) or {}).items()}
    if any("agentproxy" in k or "agentproxy" in v for k, v in headers.items()):
        return True
    if resp.status_code == 407:
        return True
    body = (getattr(resp, "text", "") or "")[:2000].lower()
    return "agentproxy" in body or "egress policy" in body


# --------------------------------------------------------------------------- rate limit
def _rate_limit(domain: str) -> None:
    interval = _min_interval()
    last = _last_request_at.get(domain)
    now = time.monotonic()
    if last is not None and interval > 0:
        wait = interval - (now - last)
        if wait > 0:
            _sleep(wait)
    _last_request_at[domain] = time.monotonic()


def _retry_after_seconds(headers, attempt: int) -> float:
    value = None
    for k, v in dict(headers or {}).items():
        if str(k).lower() == "retry-after":
            value = str(v).strip()
            break
    if value:
        if value.isdigit():
            return min(float(value), 120.0)
        try:
            when = email.utils.parsedate_to_datetime(value)
            delta = (when - _dt.datetime.now(_dt.timezone.utc)).total_seconds()
            return max(0.0, min(delta, 120.0))
        except (TypeError, ValueError):
            pass
    return min(_retry_base() * (2 ** attempt), 60.0)


# --------------------------------------------------------------------------- raw request with retries
def _request(url: str, params=None, headers=None, timeout: float = 30, max_tries: int = 4):
    domain = common.domain_of(url)
    if offline():
        raise NetworkBlocked(domain, "FUNNEL_OFFLINE=1")
    hdrs = {"User-Agent": user_agent()}
    if headers:
        hdrs.update(headers)
    last_exc = None
    for attempt in range(max_tries):
        _rate_limit(domain)
        try:
            resp = _http_get(url, params=params, headers=hdrs, timeout=timeout)
        except requests.exceptions.ProxyError as e:
            raise NetworkBlocked(domain, "proxy refused the tunnel") from e
        except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout) as e:
            if _is_tunnel_block(e):
                raise NetworkBlocked(domain, "proxy refused the tunnel") from e
            raise NetworkBlocked(domain, "connection failed") from e
        except requests.exceptions.Timeout as e:
            last_exc = e
            _sleep(_retry_after_seconds({}, attempt))
            continue
        status = int(resp.status_code)
        if status in RETRY_STATUSES and attempt < max_tries - 1:
            _sleep(_retry_after_seconds(resp.headers, attempt))
            last_exc = FetchError(f"{domain} answered HTTP {status}", url=url, status=status)
            continue
        if _response_is_proxy_block(resp):
            raise NetworkBlocked(domain, f"proxy answered HTTP {status}")
        return resp
    if isinstance(last_exc, FetchError):
        raise FetchError(f"{domain} kept answering HTTP {last_exc.status} after {max_tries} tries.",
                         url=url, status=last_exc.status)
    raise FetchError(f"{domain} timed out {max_tries} times.", url=url, status=None)


# --------------------------------------------------------------------------- robots
def robots_text(domain: str) -> str:
    """The domain's robots.txt, from cache/robots/ or fetched once. "" means no rules."""
    p = robots_dir() / f"{domain}.txt"
    if p.exists():
        return p.read_text(encoding="utf-8")
    resp = _request(f"https://{domain}/robots.txt", timeout=15, max_tries=2)
    status = int(resp.status_code)
    if 200 <= status < 300:
        text = resp.text or ""
    elif 400 <= status < 500:
        text = ""  # no robots file: nothing is disallowed
    else:
        raise FetchError(f"{domain}/robots.txt answered HTTP {status}; treated as not allowed for now.",
                         url=f"https://{domain}/robots.txt", status=status)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return text


def robots_allowed(url: str, user_agent_name: str | None = None) -> bool:
    domain = common.domain_of(url)
    text = robots_text(domain)
    if not text.strip():
        return True
    rp = robotparser.RobotFileParser()
    rp.parse(text.splitlines())
    agent = user_agent_name or user_agent().split("/")[0]
    return bool(rp.can_fetch(agent, url))


# --------------------------------------------------------------------------- public fetch
def fetch(url: str, params=None, headers=None, use_cache: bool = True, respect_robots: bool = True,
          timeout: float | None = None, max_tries: int = 4) -> dict:
    """GET a page politely. Returns {"url", "status", "text", "headers", "from_cache"}.

    Raises NetworkBlocked (offline, proxy block, connection failure), RobotsDisallowed,
    or FetchError (401/403/404, other 4xx, exhausted retries).
    """
    if offline():
        raise NetworkBlocked(common.domain_of(url), "FUNNEL_OFFLINE=1")
    if timeout is None:
        try:
            timeout = float(os.environ.get("FUNNEL_HTTP_TIMEOUT", "30"))
        except ValueError:
            timeout = 30.0
    if use_cache:
        cached = _read_cache(url, params)
        if cached is not None:
            return cached
    if respect_robots and not robots_allowed(url):
        raise RobotsDisallowed(url)
    resp = _request(url, params=params, headers=headers, timeout=timeout, max_tries=max_tries)
    status = int(resp.status_code)
    domain = common.domain_of(url)
    if status in NO_RETRY_STATUSES:
        raise FetchError(f"{domain} refused the request (HTTP {status}). Not retried.", url=public_url(url, params), status=status)
    if status >= 400:
        raise FetchError(f"{domain} answered HTTP {status} for {public_url(url, params)}.", url=public_url(url, params), status=status)
    result = {
        "url": public_url(url, params),
        "status": status,
        "text": resp.text or "",
        "headers": {str(k): str(v) for k, v in dict(resp.headers or {}).items()},
        "from_cache": False,
    }
    if use_cache:
        _write_cache(url, params, result)
    return result


def fetch_json(url: str, params=None, headers=None, **kw):
    result = fetch(url, params=params, headers=headers, **kw)
    try:
        return json.loads(result["text"])
    except json.JSONDecodeError as e:
        raise FetchError(f"{common.domain_of(url)} did not return JSON ({e.msg}).", url=result["url"], status=result["status"])


def probe(domain: str, timeout: float = 10) -> dict:
    """One light request to classify a domain: reachable, blocked_by_network or error."""
    if offline():
        return {"domain": domain, "status": "blocked_by_network", "detail": "FUNNEL_OFFLINE=1"}
    try:
        resp = _http_get(f"https://{domain}/robots.txt", headers={"User-Agent": user_agent()}, timeout=timeout)
        if _response_is_proxy_block(resp):
            return {"domain": domain, "status": "blocked_by_network", "detail": f"proxy answered HTTP {resp.status_code}"}
        return {"domain": domain, "status": "reachable", "detail": f"HTTP {resp.status_code}"}
    except requests.exceptions.ProxyError:
        return {"domain": domain, "status": "blocked_by_network", "detail": "proxy refused the tunnel"}
    except requests.exceptions.ConnectionError:
        return {"domain": domain, "status": "blocked_by_network", "detail": "connection failed"}
    except Exception as e:  # noqa: BLE001 - a probe never crashes preflight
        return {"domain": domain, "status": "error", "detail": type(e).__name__}


# --------------------------------------------------------------------------- html
_BLOCK_TAGS = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr", "td", "th",
               "table", "section", "article", "header", "footer", "blockquote", "pre", "hr", "dd", "dt", "dl",
               "nav", "aside", "main", "form", "fieldset", "figure", "figcaption", "title"}
_SKIP_TAGS = {"script", "style", "noscript", "template", "svg"}


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in _SKIP_TAGS:
            self._skip += 1
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_endtag(self, tag):
        if tag in _SKIP_TAGS:
            self._skip = max(0, self._skip - 1)
        elif tag in _BLOCK_TAGS:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)


def html_to_text(html: str) -> str:
    """Visible text of an HTML page: scripts and styles dropped, blocks on their own lines."""
    parser = _TextExtractor()
    parser.feed(html or "")
    parser.close()
    raw = "".join(parser.parts)
    lines = [re.sub(r"[ \t\r\f\v ]+", " ", ln).strip() for ln in raw.split("\n")]
    return "\n".join(ln for ln in lines if ln)


# --------------------------------------------------------------------------- dates
_URL_DATE_RES = (
    re.compile(r"/((?:19|20)\d{2})/(0[1-9]|1[0-2])/(0[1-9]|[12]\d|3[01])(?:/|$)"),
    re.compile(r"(?<!\d)((?:19|20)\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])(?!\d)"),
    re.compile(r"/((?:19|20)\d{2})/(0[1-9]|1[0-2])(?:/|$)"),
)
_PAGE_DATE_RES = (
    re.compile(r"""<meta[^>]+(?:property|name)=["'](?:article:published_time|datePublished|date|pubdate|publish[-_]?date|og:published_time|dc\.date(?:\.issued)?|sailthru\.date|parsely-pub-date)["'][^>]+content=["']([^"']+)["']""", re.I),
    re.compile(r"""<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["'](?:article:published_time|datePublished|date|pubdate|publish[-_]?date|og:published_time)["']""", re.I),
    re.compile(r""""datePublished"\s*:\s*"([^"]+)\""""),
    re.compile(r"""<time[^>]+datetime=["']([^"']+)["']""", re.I),
)


def _valid_date(y: str, m: str, d: str) -> str | None:
    try:
        return _dt.date(int(y), int(m), int(d)).isoformat()
    except ValueError:
        return None


def url_date_info(url: str) -> tuple:
    """(date, precision) from the URL path: /YYYY/MM/DD/ or YYYY-MM-DD give ("YYYY-MM-DD", "day");
    /YYYY/MM/ gives the first of that month with precision "month"; otherwise (None, None)."""
    if not url:
        return None, None
    path = urlsplit(str(url)).path or ""
    for i, rx in enumerate(_URL_DATE_RES):
        m = rx.search(path)
        if not m:
            continue
        if i == 2:
            d = _valid_date(m.group(1), m.group(2), "01")
            return (d, "month") if d else (None, None)
        # a full date pattern with an impossible day is not a date at all
        d = _valid_date(m.group(1), m.group(2), m.group(3))
        return (d, "day") if d else (None, None)
    return None, None


def date_from_url(url: str) -> str | None:
    """A date in the URL path: /YYYY/MM/DD/, YYYY-MM-DD, or /YYYY/MM/ (day set to 01)."""
    return url_date_info(url)[0]


def _date_from_string(s: str) -> str | None:
    m = re.match(r"\s*((?:19|20)\d{2})-(\d{2})-(\d{2})", s or "")
    if m:
        return _valid_date(m.group(1), m.group(2), m.group(3))
    return None


def extract_date(html: str, url: str | None = None) -> tuple:
    """(YYYY-MM-DD or None, where it came from: "page", "url" or "none")."""
    for rx in _PAGE_DATE_RES:
        m = rx.search(html or "")
        if m:
            d = _date_from_string(m.group(1))
            if d:
                return d, "page"
    if url:
        d = date_from_url(url)
        if d:
            return d, "url"
    return None, "none"
