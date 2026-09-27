"""Full-text adapters (`fetch <adapter>`) and the founder's chat exports (`ingest-inbox`).

Records come only from scripts (rule 1). This module collects public text through
official APIs or public pages (rule 4) and parses chat exports from inbox/ (rule 5),
then stores everything through records.store_records, which anonymizes first.
Author, username, display-name and avatar fields are never stored. Sender names from
chat exports are passed to the anonymizer as known names and never stored or printed.
API keys are read with common.get_key and never printed or written anywhere.

Before any adapter runs, config/sources.md must allow it:
- API adapters (stackexchange, hackernews, reddit, youtube, apple): the table row for the
  adapter must say `allowed` or `allowed-with-limits`, checked within DECISION_VALID_DAYS.
- web and discourse: the decision log must hold a line for that exact domain with status
  `allowed` or `allowed-with-limits`, checked within DECISION_VALID_DAYS, and the site's
  robots.txt must allow the page (netfetch checks it).
A source that is not allowed logs a `skip` event and exits 1 (the fix is a decision line).
A missing key logs a `blocked` event and exits 3 naming the exact environment variable.
A blocked domain logs a `blocked` event and exits 3 naming the exact domain.

Public API
----------
    ADAPTERS, API_ADAPTERS, DOMAIN_ADAPTERS, KEY_VARS, DECISION_VALID_DAYS, WEB_TEXT_CAP
    class SourceNotAllowed(common.ValidationErrors)   exit 1
    class MissingKey(common.Blocked)                  exit 3; .names = the missing variables
    parse_sources_md(text=None) -> {"rows": [...], "decisions": [...]}
    api_source_check(adapter, today=None) -> {"ok", "problem", "status", "checked", "source"}
    domain_decision_check(domain, today=None) -> same shape
    ensure_allowed(run, adapter, domain=None, command="fetch") -> dict
    require_keys(run, adapter, names, command="fetch") -> {name: value}   (values never printed)
    lookback(run) -> datetime.date            run date minus stage3.lookback_months
    epoch_of(date) -> int
    date_from_epoch(x) / date_from_iso(s) -> "YYYY-MM-DD" | None
    looks_like_person_name(s) -> bool
    class RateGate(per_minute, name=None)     a sliding-window request gate. With a name the window is shared
                                              across processes through netfetch.shared_window_wait (Reddit:
                                              60 per minute for ALL parallel room listeners together); without
                                              a name it is a plain in-process gate.
    strip_quote_headers(cooked) -> (html, usernames)
        Discourse renders a quoted post as <aside class="quote" data-username="..."><div class="title">
        ... <username>:</div>...: the title div is replaced with `[user]:` and every data-username is
        returned as a known name, so a quoted member's username never reaches the stored text (rule 5).
    inbox_label(rel_path) -> str              the content-free label of an inbox file: "file_" + 12 hex
                                              characters of sha256 over its path inside the room folder
    fetch_stackexchange(run, room, site, query, tagged=None, answers=False, max_records=500, round_no=1)
    fetch_hackernews(run, room, query, max_records=500, round_no=1)
    fetch_reddit(run, room, subreddit, query=None, max_records=500, round_no=1)
    fetch_youtube(run, room, videos=(), search=None, videos_k=5, max_records=500, round_no=1)
    fetch_apple(run, room, app_id, country="us", max_records=500, round_no=1)
    fetch_discourse(run, room, forum, query=None, topics=(), max_records=500, round_no=1)
    fetch_web(run, room, urls, round_no=1)
        Each returns a summary dict: adapter, room, source, seen, dropped_old, records_new,
        duplicates, requests, from_cache, plus adapter-specific counts.
    parse_whatsapp(text) -> {"messages": [{"line", "date", "sender", "text"}], "senders",
                             "system_dropped", "date_order", "detected_by"}
    parse_telegram(data) -> same shape (key "msg_id" instead of "line") or None if not a Telegram export
    parse_csv_chat(text) -> same shape (key "row") or None if the columns are missing
    parse_paragraphs(text) -> same shape (key "paragraph"); undated
    ingest_inbox(run, room, customers=False, round_no=1) -> summary dict
        Files are named after people all the time ("Anita Desai.txt", "priya_sharma_feedback.csv"), so
        no file name ever reaches a record URL, meta, the run log or the screen: every file gets the
        content-free label inbox_label(path). The label -> path map is written to
        RUN/03_listen/raw/<room>/_inbox_index.json, which .gitignore keeps out of git with the raw records.
    register(subparsers)                      adds `fetch <adapter>` and `ingest-inbox`

Stored record shape (see config/formats.md, Stage 3): url, text, date, meta. Every fetched
record's meta carries kind, domain, round, order [round, 0, n] (n = position in the room's
collection order), fetched_at (the run date, so `purge-expired` can work without a clock)
and date_from ("api", "page", "url", "file" or "none").
"""
from __future__ import annotations

import collections
import contextlib
import csv
import datetime as _dt
import html as _html
import io
import json
import re
import time
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import requests

import common
import netfetch
import records
from anonymize import anonymize

STAGE = 3
ADAPTERS = ("stackexchange", "hackernews", "reddit", "youtube", "apple", "discourse", "web")
API_ADAPTERS = ("stackexchange", "hackernews", "reddit", "youtube", "apple")
DOMAIN_ADAPTERS = ("discourse", "web")
ALLOWED_STATUSES = ("allowed", "allowed-with-limits")
DECISION_VALID_DAYS = 90
WEB_TEXT_CAP = 20000
DEFAULT_MAX = 500
KEY_VARS = {
    "stackexchange": (),  # STACKEXCHANGE_KEY is optional
    "hackernews": (),
    "reddit": ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"),
    "youtube": ("YOUTUBE_API_KEY",),
    "apple": (),
    "discourse": (),
    "web": (),
}
# The adapter name as it may appear in the config/sources.md table.
_TABLE_ALIASES = {
    "stackexchange": ("stackexchange",),
    "hackernews": ("hackernews",),
    "reddit": ("reddit",),
    "youtube": ("youtube",),
    "apple": ("apple_reviews", "apple"),
    "discourse": ("discourse",),
    "web": ("web",),
}
API_DOMAINS = {
    "stackexchange": "api.stackexchange.com",
    "hackernews": "hn.algolia.com",
    "reddit": "oauth.reddit.com",
    "youtube": "www.googleapis.com",
    "apple": "itunes.apple.com",
}

SE_API = "https://api.stackexchange.com/2.3"
HN_API = "https://hn.algolia.com/api/v1/search_by_date"
REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"
REDDIT_API = "https://oauth.reddit.com"
YT_API = "https://www.googleapis.com/youtube/v3"
YT_SEARCH_UNITS = 100
YT_COMMENTS_UNITS = 1
APPLE_PAGES = 10
REDDIT_PER_MINUTE = 60

_WORD_RE = re.compile(r"[^\W_]")


# --------------------------------------------------------------------------- errors
class SourceNotAllowed(common.ValidationErrors):
    """config/sources.md does not allow this source (yet). Exit 1: record a decision first."""


class MissingKey(common.Blocked):
    """A needed API key is not set. Exit 3. The message names the exact environment variable(s)."""

    def __init__(self, adapter: str, names):
        self.adapter = adapter
        self.names = list(names)
        first, rest = self.names[0], self.names[1:]
        msg = f"Missing API key for {adapter}: set the environment variable {first}"
        if rest:
            msg += " (and also " + ", ".join(rest) + ")"
        msg += ". Put it in the environment or in .env, or skip this source and log why."
        super().__init__(msg, common.EXIT_BLOCKED)


# --------------------------------------------------------------------------- config/sources.md
def sources_md_path() -> Path:
    return common.config_dir() / "sources.md"


def _strip_ticks(s: str) -> str:
    return str(s or "").strip().strip("`").strip()


def parse_sources_md(text=None) -> dict:
    """The table rows and the decision-log lines of config/sources.md.

    rows: [{"source", "adapter", "gives", "domains", "key", "terms", "status", "checked", "decision"}]
    decisions: [{"date", "source", "status", "reason", "url", "index"}] in file order
    """
    if text is None:
        p = sources_md_path()
        text = common.read_text(p) if p.exists() else ""
    rows: list = []
    decisions: list = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 9 or cells[0].lower() == "source":
                continue
            if all(set(c) <= set("-: ") for c in cells):
                continue
            rows.append({
                "source": cells[0], "adapter": _strip_ticks(cells[1]), "gives": cells[2], "domains": cells[3],
                "key": cells[4], "terms": cells[5], "status": _strip_ticks(cells[6]).lower(),
                "checked": _strip_ticks(cells[7]), "decision": cells[8],
            })
            continue
        if line.startswith("- ") and "|" in line:
            parts = [c.strip() for c in line[2:].split("|")]
            if len(parts) >= 3 and common.is_date(parts[0]):
                decisions.append({
                    "date": parts[0], "source": _strip_ticks(parts[1]), "status": _strip_ticks(parts[2]).lower(),
                    "reason": parts[3] if len(parts) > 3 else "", "url": parts[4] if len(parts) > 4 else "",
                    "index": len(decisions),
                })
    return {"rows": rows, "decisions": decisions}


def _find_row(rows, adapter: str):
    aliases = _TABLE_ALIASES.get(adapter, (adapter,))
    for row in rows:
        if row["adapter"].lower() in aliases:
            return row
    return None


def _days_since(date_str: str, today: _dt.date):
    if not common.is_date(date_str):
        return None
    return (today - _dt.date.fromisoformat(date_str)).days


def _fix_hint(source: str) -> str:
    return (f"Read its terms, then record the decision with `funnel source-decision --source \"{source}\" "
            f"--status allowed --reason \"...\" --url ...`, or skip this source and log why.")


def api_source_check(adapter: str, today: _dt.date | None = None) -> dict:
    """Is an API source allowed by the config/sources.md table? Never raises."""
    today = today or common.today()
    info = parse_sources_md()
    row = _find_row(info["rows"], adapter)
    out = {"ok": False, "problem": None, "status": None, "checked": None, "source": adapter}
    if row is None:
        out["problem"] = (f"config/sources.md has no table row with adapter `{adapter}`. Add the row and "
                          f"record a terms decision with `funnel source-decision`, or skip this source.")
        return out
    out.update(status=row["status"], checked=row["checked"], source=row["source"])
    if row["status"] not in ALLOWED_STATUSES:
        why = "" if row["status"] != "blocked-by-network" else " (that is a network note, not a terms decision)"
        out["problem"] = (f"config/sources.md: {row['source']} has status `{row['status']}`{why}, "
                          f"not allowed or allowed-with-limits. " + _fix_hint(row["source"]))
        return out
    days = _days_since(row["checked"], today)
    if days is None:
        out["problem"] = (f"config/sources.md: {row['source']} has no valid Checked date "
                          f"(got {row['checked']!r}). " + _fix_hint(row["source"]))
        return out
    if days > DECISION_VALID_DAYS:
        out["problem"] = (f"config/sources.md: {row['source']} was checked on {row['checked']}, {days} days ago; "
                          f"a decision is valid for {DECISION_VALID_DAYS} days. Re-read the terms and record a "
                          f"fresh decision with `funnel source-decision`.")
        return out
    out["ok"] = True
    return out


def _decision_domain(source_cell: str) -> str:
    s = _strip_ticks(source_cell)
    if not s or " " in s or "." not in s:
        return ""
    return common.domain_of(s)


def domain_decision_check(domain: str, today: _dt.date | None = None) -> dict:
    """Is there a valid decision-log line for this exact domain? Never raises."""
    today = today or common.today()
    domain = common.domain_of(domain) or str(domain or "").strip().lower()
    info = parse_sources_md()
    out = {"ok": False, "problem": None, "status": None, "checked": None, "source": domain}
    matches = [d for d in info["decisions"] if _decision_domain(d["source"]) == domain]
    if not matches:
        out["problem"] = (f"config/sources.md has no decision-log line for the domain {domain}. Read the site's "
                          f"terms and robots.txt, then run `funnel source-decision --source {domain} --status "
                          f"allowed --reason \"...\" --url ...`, or skip this page.")
        return out
    latest = sorted(matches, key=lambda d: (d["date"], d["index"]))[-1]
    out.update(status=latest["status"], checked=latest["date"])
    if latest["status"] not in ALLOWED_STATUSES:
        out["problem"] = (f"config/sources.md: the latest decision for {domain} ({latest['date']}) is "
                          f"`{latest['status']}`: {latest['reason'] or 'no reason given'}. Not fetched.")
        return out
    days = _days_since(latest["date"], today)
    if days is None or days > DECISION_VALID_DAYS:
        out["problem"] = (f"config/sources.md: the decision for {domain} is dated {latest['date']}, {days} days ago; "
                          f"a decision is valid for {DECISION_VALID_DAYS} days. Re-check the terms and robots.txt "
                          f"and record a fresh decision with `funnel source-decision`.")
        return out
    out["ok"] = True
    return out


def ensure_allowed(run, adapter: str, domain: str | None = None, command: str = "fetch") -> dict:
    """Raise SourceNotAllowed (after logging a skip event) unless config/sources.md allows the source."""
    if adapter in DOMAIN_ADAPTERS:
        if not domain:
            raise common.ValidationErrors([f"fetch {adapter}: a domain is needed to check config/sources.md."])
        check = domain_decision_check(domain)
    else:
        check = api_source_check(adapter)
    if not check["ok"]:
        common.log_event(run, STAGE, command, "skip", source=adapter, domain=domain or API_DOMAINS.get(adapter),
                         status=check.get("status"), reason=check["problem"])
        raise SourceNotAllowed([check["problem"]])
    return check


def require_keys(run, adapter: str, names, command: str = "fetch") -> dict:
    """Read the named keys (environment, then .env). Missing -> blocked event + MissingKey (exit 3)."""
    values = {n: common.get_key(n) for n in names}
    missing = [n for n in names if not values[n]]
    if missing:
        common.log_event(run, STAGE, command, "blocked", source=adapter, key_names=missing,
                         reason="missing API key: " + ", ".join(missing))
        raise MissingKey(adapter, missing)
    return values


# --------------------------------------------------------------------------- dates
def lookback(run) -> _dt.date:
    months = int(common.load_kill_rules().get("stage3", {}).get("lookback_months", 24))
    return records.lookback_cutoff(common.run_date(run), months)


def epoch_of(date: _dt.date) -> int:
    return int(_dt.datetime(date.year, date.month, date.day, tzinfo=_dt.timezone.utc).timestamp())


def date_from_epoch(x) -> str | None:
    try:
        return _dt.datetime.fromtimestamp(float(x), _dt.timezone.utc).date().isoformat()
    except (TypeError, ValueError, OverflowError, OSError):
        return None


def date_from_iso(s) -> str | None:
    """The UTC calendar date of an ISO timestamp (a naive timestamp keeps its own date)."""
    if not isinstance(s, str) or not s.strip():
        return None
    t = s.strip()
    if t.endswith("Z"):
        t = t[:-1] + "+00:00"
    try:
        d = _dt.datetime.fromisoformat(t)
    except ValueError:
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})", t)
        if not m:
            return None
        try:
            return _dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))).isoformat()
        except ValueError:
            return None
    if d.tzinfo is not None:
        d = d.astimezone(_dt.timezone.utc)
    return d.date().isoformat()


# --------------------------------------------------------------------------- names, words
_NAME_TOKEN_RE = re.compile(r"^[^\W\d_][^\W\d_'’.-]*$")


def looks_like_person_name(s) -> bool:
    """Two to four alphabetic words, none all-caps (so 'GRE Prep Club' or handles do not count)."""
    toks = str(s or "").split()
    if not 2 <= len(toks) <= 4:
        return False
    return all(_NAME_TOKEN_RE.match(t) and not (len(t) > 1 and t.isupper()) for t in toks)


def word_count(text) -> int:
    return len([w for w in str(text or "").split() if _WORD_RE.search(w)])


def _chunks(items, n):
    items = list(items)
    for i in range(0, len(items), n):
        yield items[i:i + n]


# --------------------------------------------------------------------------- rate gate
_now = time.monotonic


class RateGate:
    """At most `per_minute` calls in any 60-second window. Extra calls wait (netfetch._sleep)."""

    def __init__(self, per_minute: int):
        self.per_minute = int(per_minute)
        self.times: collections.deque = collections.deque()

    def wait(self) -> float:
        now = _now()
        while self.times and now - self.times[0] >= 60.0:
            self.times.popleft()
        waited = 0.0
        if len(self.times) >= self.per_minute:
            waited = max(0.0, 60.0 - (now - self.times[0]))
            netfetch._sleep(waited)
            self.times.popleft()
            now = _now()
        self.times.append(now)
        return waited


_REDDIT_GATE = RateGate(REDDIT_PER_MINUTE)


# --------------------------------------------------------------------------- http helpers
def _http_post(url: str, data=None, headers=None, auth=None, timeout: float = 30):
    """The one place that POSTs (Reddit's token endpoint). Tests replace it."""
    return requests.post(url, data=data, headers=headers, auth=auth, timeout=timeout, allow_redirects=False)


def _get_json(url: str, params=None, headers=None, respect_robots: bool = False, gate: RateGate | None = None):
    """(parsed JSON, from_cache). Cached answers do not count against a rate gate."""
    if gate is not None and not netfetch.cache_path(url, params).exists():
        gate.wait()
    r = netfetch.fetch(url, params=params, headers=headers, respect_robots=respect_robots)
    try:
        return json.loads(r["text"]), bool(r.get("from_cache"))
    except json.JSONDecodeError as e:
        raise netfetch.FetchError(f"{common.domain_of(url)} did not return JSON ({e.msg}).", url=r["url"], status=r["status"])


class _Collector:
    """Gathers records for one adapter call and stores them once, in collection order."""

    def __init__(self, run, room: str, source: str, round_no: int, command: str = "fetch"):
        self.run, self.room, self.source, self.command = run, room, source, command
        self.round = int(round_no)
        self.base = len(records.load_records(run, room))
        self.run_date = common.run_date(run).isoformat()
        self.records: list = []
        self.skipped_empty = 0
        self.names_applied = 0
        self.stored = None

    def __len__(self) -> int:
        return len(self.records)

    def add(self, rec: dict, author=None) -> bool:
        text = str(rec.get("text") or "")
        if not common.normalize_ws(text):
            self.skipped_empty += 1
            return False
        if author and looks_like_person_name(author):
            text = anonymize(text, known_names=(str(author),))  # only this author's own record; idempotent
            self.names_applied += 1
        meta = dict(rec.get("meta") or {})
        meta.setdefault("domain", common.domain_of(rec.get("url") or ""))
        meta["round"] = self.round
        meta["order"] = [self.round, 0, self.base + len(self.records) + 1]
        meta["fetched_at"] = self.run_date
        self.records.append({"url": str(rec.get("url") or "").strip(), "text": text, "date": rec.get("date"), "meta": meta})
        return True

    def store(self) -> dict:
        self.stored = records.store_records(self.run, self.room, self.source, self.records, command=self.command)
        return self.stored


@contextlib.contextmanager
def _guarded(run, adapter: str, coll: _Collector | None = None, command: str = "fetch"):
    """Map network and fetch failures to the funnel's exit codes, logging blocked/skip events.
    Records gathered before a failure are stored, so nothing fetched is lost."""
    try:
        yield
    except (MissingKey, SourceNotAllowed):
        raise
    except netfetch.NetworkBlocked as e:
        _store_partial(coll, command)
        common.log_event(run, STAGE, command, "blocked", source=adapter, domain=e.domain, reason=str(e))
        raise
    except common.Blocked as e:  # raised by an adapter itself, e.g. refused API credentials
        _store_partial(coll, command)
        common.log_event(run, STAGE, command, "blocked", source=adapter, domain=API_DOMAINS.get(adapter), reason=str(e))
        raise
    except netfetch.RobotsDisallowed as e:
        _store_partial(coll, command)
        common.log_event(run, STAGE, command, "skip", source=adapter, domain=common.domain_of(e.url), reason=str(e))
        raise common.ValidationErrors([f"{e} Skip this page, or choose another source."]) from e
    except netfetch.FetchError as e:
        _store_partial(coll, command)
        domain = common.domain_of(e.url) or API_DOMAINS.get(adapter, "")
        if e.status in (401, 403):
            common.log_event(run, STAGE, command, "blocked", source=adapter, domain=domain, reason=str(e))
            raise common.Blocked(f"{domain} refused the request (HTTP {e.status}). Check this source's key or "
                                 f"access rules, or skip it and log why.") from e
        raise common.ValidationErrors([f"fetch {adapter}: {e}"]) from e


def _store_partial(coll: _Collector | None, command: str) -> None:
    if coll is not None and coll.records and coll.stored is None:
        stored = coll.store()
        common.log_event(coll.run, STAGE, command, "note", room=coll.room, source=coll.source, review=False,
                         note=f"Stored {stored['new']} records gathered before the source failed.")


def _summary(adapter: str, coll: _Collector, stats: dict, requests_made: int, from_cache: int, **extra) -> dict:
    stored = coll.stored or coll.store()
    out = {
        "adapter": adapter, "room": coll.room, "source": coll.source, "seen": stats.get("seen", 0),
        "dropped_old": stats.get("dropped_old", 0), "skipped_empty": coll.skipped_empty,
        "collected": len(coll), "records_new": stored["new"], "duplicates": stored["duplicates"],
        "requests": requests_made, "from_cache": from_cache, "new_ids": stored["new_ids"], "file": stored["file"],
    }
    out.update(extra)
    return out


# --------------------------------------------------------------------------- Stack Exchange
def _se_text(title, body) -> str:
    t = _html.unescape(str(title or "")).strip()
    b = netfetch.html_to_text(str(body or "")).strip()
    return f"{t}\n\n{b}" if t and b else (t or b)


def fetch_stackexchange(run, room: str, site: str, query: str, tagged: str | None = None, answers: bool = False,
                        max_records: int = DEFAULT_MAX, round_no: int = 1, command: str = "fetch") -> dict:
    """Questions (and with `answers`, answers) from the Stack Exchange API 2.3 /search/advanced."""
    room = common.check_slug(room, "room")
    ensure_allowed(run, "stackexchange", command=command)
    site = str(site or "").strip()
    if not site or not str(query or "").strip():
        raise common.ValidationErrors(["fetch stackexchange: --site (like stackoverflow or academia) and --query are both needed."])
    key = common.get_key("STACKEXCHANGE_KEY")  # optional: raises the daily quota
    cutoff = lookback(run)
    base = {"site": site, "q": query, "filter": "withbody", "order": "desc", "sort": "creation",
            "pagesize": 100, "fromdate": epoch_of(cutoff)}
    if tagged:
        base["tagged"] = tagged
    if key:
        base["key"] = key
    coll = _Collector(run, room, "stackexchange", round_no, command)
    stats = {"seen": 0, "questions_seen": 0, "answers_seen": 0, "dropped_old": 0, "backoff_seconds": 0.0,
             "quota_remaining": None, "stopped": None}
    requests_made = from_cache = 0
    with_answers: list = []
    with _guarded(run, "stackexchange", coll, command):
        page = 1
        while len(coll) < max_records:
            data, cached = _get_json(f"{SE_API}/search/advanced", dict(base, page=page))
            requests_made += 1
            from_cache += 1 if cached else 0
            if data.get("error_id"):
                raise netfetch.FetchError(f"api.stackexchange.com answered error {data.get('error_name')}: "
                                          f"{data.get('error_message')}", url=SE_API, status=int(data.get("error_id") or 0))
            for item in data.get("items") or []:
                stats["seen"] += 1
                stats["questions_seen"] += 1
                date = date_from_epoch(item.get("creation_date"))
                if date and date < cutoff.isoformat():
                    stats["dropped_old"] += 1
                    continue
                rec = {"url": str(item.get("link") or ""), "text": _se_text(item.get("title"), item.get("body")), "date": date,
                       "meta": {"kind": "question", "site": site, "query": query, "question_id": item.get("question_id"),
                                "answer_count": item.get("answer_count"), "date_from": "api" if date else "none"}}
                if rec["url"] and coll.add(rec, author=(item.get("owner") or {}).get("display_name")):
                    if answers and item.get("answer_count"):
                        with_answers.append((item.get("question_id"), rec["url"]))
                if len(coll) >= max_records:
                    break
            stats["quota_remaining"] = data.get("quota_remaining", stats["quota_remaining"])
            if not data.get("has_more") or len(coll) >= max_records:
                break
            if data.get("quota_remaining") == 0:
                stats["stopped"] = "the API quota for today is used up"
                break
            backoff = data.get("backoff")
            if backoff and not cached:
                netfetch._sleep(float(backoff))
                stats["backoff_seconds"] += float(backoff)
            page += 1
        if answers and with_answers and len(coll) < max_records and stats["stopped"] is None:
            qlinks = {qid: link for qid, link in with_answers}
            for chunk in _chunks([qid for qid, _ in with_answers], 100):
                if len(coll) >= max_records or stats["stopped"]:
                    break
                page = 1
                ids = ";".join(str(q) for q in chunk)
                while len(coll) < max_records:
                    params = {k: v for k, v in base.items() if k not in ("q", "tagged", "fromdate")}
                    params["page"] = page
                    data, cached = _get_json(f"{SE_API}/questions/{ids}/answers", params)
                    requests_made += 1
                    from_cache += 1 if cached else 0
                    for a in data.get("items") or []:
                        stats["seen"] += 1
                        stats["answers_seen"] += 1
                        date = date_from_epoch(a.get("creation_date"))
                        if date and date < cutoff.isoformat():
                            stats["dropped_old"] += 1
                            continue
                        qid = a.get("question_id")
                        link = a.get("link") or (f"{qlinks.get(qid, '')}#{a.get('answer_id')}" if qlinks.get(qid) else "")
                        if not link:
                            link = f"https://{common.domain_of(next(iter(qlinks.values()), ''))}/a/{a.get('answer_id')}"
                        rec = {"url": link, "text": _se_text("", a.get("body")), "date": date,
                               "meta": {"kind": "answer", "site": site, "query": query, "question_id": qid,
                                        "answer_id": a.get("answer_id"), "is_accepted": bool(a.get("is_accepted")),
                                        "date_from": "api" if date else "none"}}
                        coll.add(rec, author=(a.get("owner") or {}).get("display_name"))
                        if len(coll) >= max_records:
                            break
                    stats["quota_remaining"] = data.get("quota_remaining", stats["quota_remaining"])
                    if not data.get("has_more") or len(coll) >= max_records:
                        break
                    if data.get("quota_remaining") == 0:
                        stats["stopped"] = "the API quota for today is used up"
                        break
                    backoff = data.get("backoff")
                    if backoff and not cached:
                        netfetch._sleep(float(backoff))
                        stats["backoff_seconds"] += float(backoff)
                    page += 1
    return _summary("stackexchange", coll, stats, requests_made, from_cache, site=site, query=query,
                    questions_seen=stats["questions_seen"], answers_seen=stats["answers_seen"],
                    backoff_seconds=stats["backoff_seconds"], quota_remaining=stats["quota_remaining"],
                    stopped=stats["stopped"], key_used=bool(key), lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- Hacker News
def fetch_hackernews(run, room: str, query: str, max_records: int = DEFAULT_MAX, round_no: int = 1,
                     command: str = "fetch") -> dict:
    """Stories and comments from the Algolia Hacker News search API (search_by_date)."""
    room = common.check_slug(room, "room")
    ensure_allowed(run, "hackernews", command=command)
    if not str(query or "").strip():
        raise common.ValidationErrors(["fetch hackernews: --query is needed."])
    cutoff = lookback(run)
    base = {"query": query, "tags": "(story,comment)", "numericFilters": f"created_at_i>{epoch_of(cutoff)}", "hitsPerPage": 100}
    coll = _Collector(run, room, "hackernews", round_no, command)
    stats = {"seen": 0, "stories_seen": 0, "comments_seen": 0, "dropped_old": 0}
    requests_made = from_cache = 0
    with _guarded(run, "hackernews", coll, command):
        page = 0
        while len(coll) < max_records:
            data, cached = _get_json(HN_API, dict(base, page=page))
            requests_made += 1
            from_cache += 1 if cached else 0
            hits = data.get("hits") or []
            for hit in hits:
                stats["seen"] += 1
                tags = hit.get("_tags") or []
                is_comment = "comment" in tags or hit.get("comment_text") is not None
                if is_comment:
                    stats["comments_seen"] += 1
                    text = netfetch.html_to_text(str(hit.get("comment_text") or ""))
                else:
                    stats["stories_seen"] += 1
                    text = _se_text(hit.get("title"), hit.get("story_text"))
                date = date_from_epoch(hit.get("created_at_i")) or date_from_iso(hit.get("created_at"))
                if date and date < cutoff.isoformat():
                    stats["dropped_old"] += 1
                    continue
                hn_id = hit.get("objectID")
                if not hn_id:
                    continue
                rec = {"url": f"https://news.ycombinator.com/item?id={hn_id}", "text": text, "date": date,
                       "meta": {"kind": "comment" if is_comment else "story", "query": query, "hn_id": str(hn_id),
                                "story_id": hit.get("story_id"), "date_from": "api" if date else "none"}}
                coll.add(rec)
                if len(coll) >= max_records:
                    break
            nb_pages = int(data.get("nbPages") or 0)
            page += 1
            if not hits or page >= nb_pages:
                break
    return _summary("hackernews", coll, stats, requests_made, from_cache, query=query, stories_seen=stats["stories_seen"],
                    comments_seen=stats["comments_seen"], lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- Reddit
def _reddit_token(keys: dict) -> str:
    """An app-only OAuth token (client credentials). Never cached, never printed."""
    domain = urlsplit(REDDIT_TOKEN_URL).hostname or "www.reddit.com"
    if netfetch.offline():
        raise netfetch.NetworkBlocked(domain, "FUNNEL_OFFLINE=1")
    headers = {"User-Agent": keys["REDDIT_USER_AGENT"]}
    try:
        resp = _http_post(REDDIT_TOKEN_URL, data={"grant_type": "client_credentials"}, headers=headers,
                          auth=(keys["REDDIT_CLIENT_ID"], keys["REDDIT_CLIENT_SECRET"]), timeout=30)
    except requests.exceptions.ProxyError as e:
        raise netfetch.NetworkBlocked(domain, "proxy refused the tunnel") from e
    except requests.exceptions.ConnectionError as e:
        raise netfetch.NetworkBlocked(domain, "connection failed") from e
    except requests.exceptions.Timeout as e:
        raise netfetch.FetchError(f"{domain} timed out while issuing a token.", url=REDDIT_TOKEN_URL) from e
    status = int(getattr(resp, "status_code", 0) or 0)
    if netfetch._response_is_proxy_block(resp):
        raise netfetch.NetworkBlocked(domain, f"proxy answered HTTP {status}")
    if status in (401, 403):
        raise common.Blocked(f"{domain} refused the API credentials (HTTP {status}). Check REDDIT_CLIENT_ID and "
                             f"REDDIT_CLIENT_SECRET, or skip this source.")
    if status >= 400:
        raise netfetch.FetchError(f"{domain} answered HTTP {status} for the token request.", url=REDDIT_TOKEN_URL, status=status)
    try:
        token = json.loads(resp.text or "").get("access_token")
    except (json.JSONDecodeError, AttributeError):
        token = None
    if not token:
        raise common.Blocked(f"{domain} did not issue an access token. Check REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET.")
    return str(token)


def _reddit_post_record(d: dict, sub: str, query) -> dict | None:
    title = str(d.get("title") or "").strip()
    body = str(d.get("selftext") or "").strip()
    if body in ("[removed]", "[deleted]"):
        body = ""
    text = f"{title}\n\n{body}" if title and body else (title or body)
    permalink = d.get("permalink")
    if not text or not permalink:
        return None
    date = date_from_epoch(d.get("created_utc"))
    return {"url": "https://www.reddit.com" + str(permalink), "text": text, "date": date,
            "meta": {"kind": "post", "subreddit": sub, "query": query, "post_id": d.get("id"),
                     "num_comments": d.get("num_comments"), "date_from": "api" if date else "none"}}


def fetch_reddit(run, room: str, subreddit: str, query: str | None = None, max_records: int = DEFAULT_MAX,
                 round_no: int = 1, command: str = "fetch") -> dict:
    """Posts and top-level comments of a subreddit through the official Data API (OAuth, 60 requests a minute)."""
    room = common.check_slug(room, "room")
    ensure_allowed(run, "reddit", command=command)
    keys = require_keys(run, "reddit", KEY_VARS["reddit"], command)
    sub = str(subreddit or "").strip().strip("/")
    if sub.lower().startswith("r/"):
        sub = sub[2:]
    if not re.match(r"^[A-Za-z0-9_]{2,21}$", sub):
        raise common.ValidationErrors([f"fetch reddit: --subreddit {subreddit!r} is not a subreddit name (letters, digits, underscores)."])
    cutoff = lookback(run)
    cutoff_epoch = epoch_of(cutoff)
    coll = _Collector(run, room, "reddit", round_no, command)
    stats = {"seen": 0, "posts_seen": 0, "comments_seen": 0, "dropped_old": 0}
    requests_made = from_cache = 0
    with _guarded(run, "reddit", coll, command):
        token = _reddit_token(keys)
        headers = {"Authorization": f"bearer {token}", "User-Agent": keys["REDDIT_USER_AGENT"]}
        if query:
            url = f"{REDDIT_API}/r/{sub}/search"
            base = {"q": query, "restrict_sr": 1, "sort": "new", "t": "all", "limit": 100, "raw_json": 1}
        else:
            url = f"{REDDIT_API}/r/{sub}/new"
            base = {"limit": 100, "raw_json": 1}
        after = None
        with_comments: list = []
        while len(coll) < max_records:
            params = dict(base, after=after) if after else dict(base)
            data, cached = _get_json(url, params, headers=headers, gate=_REDDIT_GATE)
            requests_made += 1
            from_cache += 1 if cached else 0
            listing = data.get("data") or {}
            children = listing.get("children") or []
            older = False
            for ch in children:
                if ch.get("kind") != "t3":
                    continue
                d = ch.get("data") or {}
                stats["seen"] += 1
                stats["posts_seen"] += 1
                created = d.get("created_utc")
                if created is not None and float(created) < cutoff_epoch:
                    stats["dropped_old"] += 1
                    older = True  # sorted newest first: everything after this is older
                    continue
                rec = _reddit_post_record(d, sub, query)
                if rec and coll.add(rec) and d.get("num_comments"):
                    with_comments.append(str(d.get("id")))
                if len(coll) >= max_records:
                    break
            after = listing.get("after")
            if older or not after or not children:
                break
        for pid in with_comments:
            if len(coll) >= max_records:
                break
            data, cached = _get_json(f"{REDDIT_API}/comments/{pid}", {"depth": 1, "limit": 100, "sort": "top", "raw_json": 1},
                                     headers=headers, gate=_REDDIT_GATE)
            requests_made += 1
            from_cache += 1 if cached else 0
            comments = data[1] if isinstance(data, list) and len(data) > 1 else {}
            for ch in (comments.get("data") or {}).get("children") or []:
                if ch.get("kind") != "t1":
                    continue
                d = ch.get("data") or {}
                stats["seen"] += 1
                stats["comments_seen"] += 1
                body = str(d.get("body") or "").strip()
                if not body or body in ("[removed]", "[deleted]") or not d.get("permalink"):
                    continue
                date = date_from_epoch(d.get("created_utc"))
                if date and date < cutoff.isoformat():
                    stats["dropped_old"] += 1
                    continue
                coll.add({"url": "https://www.reddit.com" + str(d.get("permalink")), "text": body, "date": date,
                          "meta": {"kind": "comment", "subreddit": sub, "query": query, "post_id": pid,
                                   "comment_id": d.get("id"), "date_from": "api" if date else "none"}})
                if len(coll) >= max_records:
                    break
    return _summary("reddit", coll, stats, requests_made, from_cache, subreddit=sub, query=query,
                    posts_seen=stats["posts_seen"], comments_seen=stats["comments_seen"], lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- YouTube
_YT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def youtube_video_id(s: str) -> str:
    """A video id from an id or any youtube.com / youtu.be URL form."""
    t = str(s or "").strip()
    if _YT_ID_RE.match(t):
        return t
    parts = urlsplit(t if "://" in t else "https://" + t)
    host = (parts.hostname or "").lower()
    segs = [x for x in parts.path.split("/") if x]
    cand = None
    if host.endswith("youtu.be") and segs:
        cand = segs[0]
    elif "youtube" in host:
        v = parse_qs(parts.query).get("v")
        if v:
            cand = v[0]
        elif len(segs) >= 2 and segs[0] in ("shorts", "embed", "live", "v"):
            cand = segs[1]
    if cand and _YT_ID_RE.match(cand):
        return cand
    raise common.ValidationErrors([f"fetch youtube: {s!r} is not a video id or a YouTube video URL."])


def fetch_youtube(run, room: str, videos=(), search: str | None = None, videos_k: int = 5,
                  max_records: int = DEFAULT_MAX, round_no: int = 1, command: str = "fetch") -> dict:
    """Top-level comments of videos (Data API v3 commentThreads.list, plain text). search.list costs 100 units."""
    room = common.check_slug(room, "room")
    ensure_allowed(run, "youtube", command=command)
    keys = require_keys(run, "youtube", KEY_VARS["youtube"], command)
    key = keys["YOUTUBE_API_KEY"]
    ids = [youtube_video_id(v) for v in (videos or [])]
    if not ids and not str(search or "").strip():
        raise common.ValidationErrors(["fetch youtube: give --video ID_OR_URL (one or more) or --search QUERY [--videos K]."])
    cutoff = lookback(run)
    coll = _Collector(run, room, "youtube", round_no, command)
    stats = {"seen": 0, "dropped_old": 0, "units": 0, "videos": [], "refused": [], "searched": 0}
    requests_made = from_cache = 0
    with _guarded(run, "youtube", coll, command):
        if search:
            k = max(1, min(int(videos_k or 5), 50))
            params = {"part": "snippet", "q": search, "type": "video", "maxResults": k,
                      "publishedAfter": f"{cutoff.isoformat()}T00:00:00Z", "key": key}
            data, cached = _get_json(f"{YT_API}/search", params)
            requests_made += 1
            from_cache += 1 if cached else 0
            stats["units"] += 0 if cached else YT_SEARCH_UNITS
            for item in data.get("items") or []:
                vid = ((item.get("id") or {}).get("videoId"))
                if vid and vid not in ids:
                    ids.append(vid)
                    stats["searched"] += 1
        for vid in ids:
            if len(coll) >= max_records:
                break
            stats["videos"].append(vid)
            page_token = None
            while len(coll) < max_records:
                params = {"part": "snippet", "videoId": vid, "textFormat": "plainText", "maxResults": 100, "order": "time", "key": key}
                if page_token:
                    params["pageToken"] = page_token
                try:
                    data, cached = _get_json(f"{YT_API}/commentThreads", params)
                except netfetch.FetchError as e:
                    if e.status == 403 and not isinstance(e, netfetch.NetworkBlocked):
                        stats["refused"].append(vid)
                        common.log_event(run, STAGE, command, "note", room=room, source="youtube", review=False,
                                         note=f"Video {vid}: HTTP 403 (comments disabled, or the API key or quota was refused). Skipped.")
                        break
                    raise
                requests_made += 1
                from_cache += 1 if cached else 0
                stats["units"] += 0 if cached else YT_COMMENTS_UNITS
                older = False
                for item in data.get("items") or []:
                    stats["seen"] += 1
                    top = (item.get("snippet") or {}).get("topLevelComment") or {}
                    sn = top.get("snippet") or {}
                    text = str(sn.get("textOriginal") or sn.get("textDisplay") or "")
                    date = date_from_iso(sn.get("publishedAt"))
                    if date and date < cutoff.isoformat():
                        stats["dropped_old"] += 1
                        older = True  # newest first: the rest of this page and later pages are older
                        continue
                    cid = item.get("id") or top.get("id")
                    if not cid:
                        continue
                    coll.add({"url": f"https://www.youtube.com/watch?v={vid}&lc={cid}", "text": text, "date": date,
                              "meta": {"kind": "comment", "video_id": vid, "comment_id": str(cid), "search": search,
                                       "like_count": sn.get("likeCount"), "date_from": "api" if date else "none"}},
                             author=sn.get("authorDisplayName"))
                    if len(coll) >= max_records:
                        break
                page_token = data.get("nextPageToken")
                if older or not page_token:
                    break
        if ids and stats["refused"] and len(stats["refused"]) == len(ids):
            raise common.Blocked(f"{API_DOMAINS['youtube']} refused every comment request (HTTP 403): comments are "
                                 f"disabled on these videos, or the key in YOUTUBE_API_KEY or its quota was refused.")
    common.log_event(run, STAGE, command, "cost", room=room, source="youtube", api="youtube", units=stats["units"],
                     tag="measured", note=f"search.list costs {YT_SEARCH_UNITS} units, commentThreads.list {YT_COMMENTS_UNITS} per page; cached calls cost 0")
    return _summary("youtube", coll, stats, requests_made, from_cache, videos=stats["videos"], search=search,
                    videos_from_search=stats["searched"], refused=stats["refused"], quota_units=stats["units"],
                    lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- Apple App Store reviews
def _label(x) -> str:
    if isinstance(x, dict):
        return str(x.get("label") or "")
    return str(x or "")


def fetch_apple(run, room: str, app_id: str, country: str = "us", max_records: int = DEFAULT_MAX, round_no: int = 1,
                command: str = "fetch") -> dict:
    """Customer reviews from the public iTunes RSS feed (most recent first, pages 1-10)."""
    room = common.check_slug(room, "room")
    ensure_allowed(run, "apple", command=command)
    app = re.sub(r"^id", "", str(app_id or "").strip().lower())
    cc = str(country or "us").strip().lower()
    if not app.isdigit() or not re.match(r"^[a-z]{2}$", cc):
        raise common.ValidationErrors(["fetch apple: --app must be the numeric app id (like 1234567890) and --country a two-letter code (like us or in)."])
    cutoff = lookback(run)
    coll = _Collector(run, room, "apple", round_no, command)
    stats = {"seen": 0, "dropped_old": 0, "pages": 0}
    requests_made = from_cache = 0
    page_url = f"https://apps.apple.com/{cc}/app/id{app}?see-all=reviews"
    with _guarded(run, "apple", coll, command):
        for page in range(1, APPLE_PAGES + 1):
            if len(coll) >= max_records:
                break
            url = f"https://itunes.apple.com/{cc}/rss/customerreviews/page={page}/id={app}/sortby=mostrecent/json"
            try:
                data, cached = _get_json(url, respect_robots=True)
            except netfetch.FetchError as e:
                if e.status == 404 and page > 1 and not isinstance(e, netfetch.NetworkBlocked):
                    break
                raise
            requests_made += 1
            from_cache += 1 if cached else 0
            stats["pages"] += 1
            entries = (data.get("feed") or {}).get("entry")
            if isinstance(entries, dict):
                entries = [entries]
            if not entries:
                break
            older = False
            for e in entries:
                if not isinstance(e, dict) or "im:name" in e or not e.get("content"):
                    continue  # the app's own entry, not a review
                stats["seen"] += 1
                date = date_from_iso(_label(e.get("updated")))
                if date and date < cutoff.isoformat():
                    stats["dropped_old"] += 1
                    older = True
                    continue
                rating = _label(e.get("im:rating"))
                rid = _label(e.get("id"))
                title = _label(e.get("title")).strip()
                content = _label(e.get("content")).strip()
                text = f"{title}\n\n{content}" if title and content else (title or content)
                coll.add({"url": page_url, "text": text, "date": date,
                          "meta": {"kind": "review", "app_id": app, "country": cc, "review_id": rid,
                                   "rating": int(rating) if rating.isdigit() else None, "version": _label(e.get("im:version")) or None,
                                   "date_from": "api" if date else "none"}},
                         author=_label((e.get("author") or {}).get("name")))
                if len(coll) >= max_records:
                    break
            if older:
                break
    return _summary("apple", coll, stats, requests_made, from_cache, app_id=app, country=cc, pages=stats["pages"],
                    lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- Discourse
def discourse_topic_id(s) -> int:
    """A topic id from a number or a topic URL (/t/<slug>/<id>[/<post>] or /t/<id>)."""
    t = str(s or "").strip()
    if t.isdigit():
        return int(t)
    segs = [x for x in urlsplit(t if "://" in t else "https://" + t).path.split("/") if x]
    if segs and segs[0] == "t":
        for seg in segs[1:]:
            if seg.isdigit():
                return int(seg)
    raise common.ValidationErrors([f"fetch discourse: {s!r} is not a topic id or a topic URL like https://forum.example/t/slug/123."])


def _forum_base(forum: str) -> str:
    t = str(forum or "").strip().rstrip("/")
    if not t:
        raise common.ValidationErrors(["fetch discourse: --forum is needed (like https://community.example.org)."])
    if "://" not in t:
        t = "https://" + t
    parts = urlsplit(t)
    return f"{parts.scheme}://{parts.netloc}{parts.path.rstrip('/')}"


def fetch_discourse(run, room: str, forum: str, query: str | None = None, topics=(), max_records: int = DEFAULT_MAX,
                    round_no: int = 1, command: str = "fetch") -> dict:
    """Posts of Discourse topics found through /search.json (if robots.txt allows it) or given with --topic."""
    room = common.check_slug(room, "room")
    base = _forum_base(forum)
    domain = common.domain_of(base)
    ensure_allowed(run, "discourse", domain=domain, command=command)
    topic_ids = [discourse_topic_id(t) for t in (topics or [])]
    if not topic_ids and not str(query or "").strip():
        raise common.ValidationErrors(["fetch discourse: give --query TEXT or --topic ID_OR_URL (one or more)."])
    cutoff = lookback(run)
    coll = _Collector(run, room, "discourse", round_no, command)
    stats = {"seen": 0, "dropped_old": 0, "topics": 0, "search_pages": 0}
    requests_made = from_cache = 0
    with _guarded(run, "discourse", coll, command):
        found: list = []
        if query:
            page = 1
            while True:
                data, cached = _get_json(f"{base}/search.json", {"q": f"{query} after:{cutoff.isoformat()}", "page": page},
                                         respect_robots=True)
                requests_made += 1
                from_cache += 1 if cached else 0
                stats["search_pages"] += 1
                for t in data.get("topics") or []:
                    if isinstance(t, dict) and t.get("id") is not None:
                        found.append(int(t["id"]))
                for p in data.get("posts") or []:
                    if isinstance(p, dict) and p.get("topic_id") is not None:
                        found.append(int(p["topic_id"]))
                more = (data.get("grouped_search_result") or {}).get("more_full_page_results")
                if not more or len(set(found)) >= max_records:
                    break
                page += 1
        ordered: list = []
        for tid in found + topic_ids:
            if tid not in ordered:
                ordered.append(tid)
        for tid in ordered:
            if len(coll) >= max_records:
                break
            data, cached = _get_json(f"{base}/t/{tid}.json", respect_robots=True)
            requests_made += 1
            from_cache += 1 if cached else 0
            stats["topics"] += 1
            title = str(data.get("title") or "").strip()
            slug = str(data.get("slug") or "topic")
            stream = data.get("post_stream") or {}
            posts = [p for p in (stream.get("posts") or []) if isinstance(p, dict)]
            have = {p.get("id") for p in posts}
            missing = [pid for pid in (stream.get("stream") or []) if pid not in have]
            for chunk in _chunks(missing, 20):
                if len(coll) + len(posts) >= max_records:
                    break
                url = f"{base}/t/{tid}/posts.json?" + "&".join(f"post_ids[]={pid}" for pid in chunk)
                more_data, cached = _get_json(url, respect_robots=True)
                requests_made += 1
                from_cache += 1 if cached else 0
                posts.extend(p for p in ((more_data.get("post_stream") or {}).get("posts") or []) if isinstance(p, dict))
            posts.sort(key=lambda p: (int(p.get("post_number") or 0), int(p.get("id") or 0)))
            for p in posts:
                if p.get("post_type") not in (None, 1):
                    continue  # small actions, whispers and moderator notes are not discussion
                stats["seen"] += 1
                text = netfetch.html_to_text(str(p.get("cooked") or "")).strip()
                if p.get("post_number") == 1 and title:
                    text = f"{title}\n\n{text}" if text else title
                date = date_from_iso(p.get("created_at"))
                if date and date < cutoff.isoformat():
                    stats["dropped_old"] += 1
                    continue
                coll.add({"url": f"{base}/t/{slug}/{tid}/{p.get('post_number')}", "text": text, "date": date,
                          "meta": {"kind": "post", "forum": domain, "topic_id": tid, "post_id": p.get("id"),
                                   "post_number": p.get("post_number"), "query": query, "date_from": "api" if date else "none"}},
                         author=p.get("name"))
                if len(coll) >= max_records:
                    break
    return _summary("discourse", coll, stats, requests_made, from_cache, forum=base, domain=domain, query=query,
                    topics=stats["topics"], search_pages=stats["search_pages"], lookback=cutoff.isoformat())


# --------------------------------------------------------------------------- web page
def fetch_web(run, room: str, urls, round_no: int = 1, command: str = "fetch") -> dict:
    """One public page = one record (text capped at WEB_TEXT_CAP characters). Robots.txt is honoured."""
    room = common.check_slug(room, "room")
    urls = [str(u).strip() for u in (urls if isinstance(urls, (list, tuple)) else [urls]) if str(u).strip()]
    if not urls:
        raise common.ValidationErrors(["fetch web: --url is needed (one or more page URLs)."])
    for u in urls:
        if not u.startswith(("http://", "https://")):
            raise common.ValidationErrors([f"fetch web: {u!r} must start with http:// or https://."])
        ensure_allowed(run, "web", domain=common.domain_of(u), command=command)
    coll = _Collector(run, room, "web", round_no, command)
    stats = {"seen": 0, "dropped_old": 0, "truncated": 0, "pages": []}
    requests_made = from_cache = 0
    with _guarded(run, "web", coll, command):
        for u in urls:
            r = netfetch.fetch(u)
            requests_made += 1
            from_cache += 1 if r.get("from_cache") else 0
            stats["seen"] += 1
            ctype = ""
            for k, v in (r.get("headers") or {}).items():
                if str(k).lower() == "content-type":
                    ctype = str(v).lower()
            raw = r.get("text") or ""
            if ctype.startswith("text/plain"):
                text = raw
                date = netfetch.date_from_url(u)
                date_from = "url" if date else "none"
            elif ctype and not any(x in ctype for x in ("html", "xml", "text/")):
                raise common.ValidationErrors([f"fetch web: {u} is not a text or HTML page (Content-Type {ctype}). "
                                               f"Only pages with readable text can be stored."])
            else:
                text = netfetch.html_to_text(raw)
                date, date_from = netfetch.extract_date(raw, u)
            total = len(text)
            truncated = total > WEB_TEXT_CAP
            if truncated:
                text = text[:WEB_TEXT_CAP]
                stats["truncated"] += 1
            coll.add({"url": r["url"], "text": text, "date": date,
                      "meta": {"kind": "page", "domain": common.domain_of(u), "date_from": date_from, "chars": total,
                               "truncated": truncated}})
            stats["pages"].append(r["url"])
    return _summary("web", coll, stats, requests_made, from_cache, pages=stats["pages"], truncated=stats["truncated"])


# --------------------------------------------------------------------------- chat export parsers
_INVISIBLE_RE = re.compile("[‎‏‪-‮﻿]")
_WA_HEADER_RE = re.compile(
    r"^\[?(?P<a>\d{1,4})[./-](?P<b>\d{1,2})[./-](?P<c>\d{2,4})[,\s]+"
    r"(?P<h>\d{1,2}):(?P<mi>\d{2})(?::(?P<s>\d{2}))?\s*(?P<ampm>[AaPp]\.?\s?[Mm]\.?)?\]?\s*(?:[-–—]\s+)?(?P<rest>.*)$"
)
_WA_SYSTEM_MSG_RE = re.compile(
    r"^(?:<media omitted>|<attached:.*>|(?:image|video|audio|sticker|gif|document|contact card|photo) omitted|"
    r"this message was deleted\.?|you deleted this message\.?|message deleted|null|"
    r"missed (?:voice|video|group voice|group video) call|waiting for this message.*|"
    r"messages and calls are end-to-end encrypted.*|.*joined using this group's invite link|"
    r"location: https?://\S+|poll:.*|.*changed (?:the subject|this group's icon|their phone number).*)$",
    re.IGNORECASE | re.DOTALL,
)


def _detect_date_order(triples) -> tuple:
    if any(a >= 1000 for a, b, c in triples):
        return "year-first", "the first field is a four-digit year"
    if any(a > 12 for a, b, c in triples):
        return "day-first", "a first field is over 12, so it must be the day"
    if any(b > 12 for a, b, c in triples):
        return "month-first", "a second field is over 12, so it must be the day"
    return "day-first", "no field is over 12; day-first assumed (the default)"


def _date_from_fields(a: int, b: int, c: int, order: str) -> str | None:
    if order == "year-first":
        y, m, d = a, b, c
    elif order == "month-first":
        m, d, y = a, b, c
    else:
        d, m, y = a, b, c
    if y < 100:
        y += 2000
    try:
        return _dt.date(y, m, d).isoformat()
    except ValueError:
        return None


def parse_whatsapp(text: str) -> dict:
    """WhatsApp .txt exports, iOS `[dd/mm/yyyy, hh:mm:ss] Name: msg` and Android `dd/mm/yyyy, hh:mm - Name: msg`.

    Lines that do not start a message continue the current one. Lines without `Name: ` are
    system lines (joined, left, added, encryption notice) and are dropped, as are media,
    deleted and call placeholders. Day/month order is detected once per file.
    """
    raw_msgs: list = []
    system = 0
    triples: list = []
    current = None
    for n, raw in enumerate(str(text or "").splitlines(), 1):
        line = _INVISIBLE_RE.sub("", raw).rstrip()
        m = _WA_HEADER_RE.match(line)
        if not m:
            if current is not None:
                current["lines"].append(line)
            continue
        if current is not None:
            raw_msgs.append(current)
            current = None
        rest = m.group("rest")
        sender, sep, msg = rest.partition(": ")
        if not sep or not sender.strip():
            if rest.strip().endswith(":") and not msg:  # `Name:` with an empty first line
                sender, msg = rest.strip()[:-1], ""
            else:
                system += 1
                continue
        triples.append((int(m.group("a")), int(m.group("b")), int(m.group("c"))))
        current = {"line": n, "fields": triples[-1], "sender": sender.strip(), "lines": [msg]}
    if current is not None:
        raw_msgs.append(current)
    order, detected_by = _detect_date_order(triples)
    messages: list = []
    senders: set = set()
    for msg in raw_msgs:
        senders.add(msg["sender"])
        body = "\n".join(msg["lines"]).strip()
        if not body or _WA_SYSTEM_MSG_RE.match(body):
            system += 1
            continue
        messages.append({"line": msg["line"], "date": _date_from_fields(*msg["fields"], order), "sender": msg["sender"], "text": body})
    return {"format": "whatsapp", "messages": messages, "senders": senders, "system_dropped": system,
            "date_order": order, "detected_by": detected_by}


def looks_like_whatsapp(text: str) -> bool:
    for raw in str(text or "").splitlines()[:400]:
        m = _WA_HEADER_RE.match(_INVISIBLE_RE.sub("", raw))
        if m and ": " in m.group("rest"):
            return True
    return False


def _telegram_text(value) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        parts = []
        for item in value:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict):
                parts.append(str(item.get("text") or ""))
        return "".join(parts)
    return ""


def parse_telegram(data) -> dict | None:
    """A Telegram Desktop `result.json` export: `messages[]` with `text` as a string or a list of entities."""
    if not isinstance(data, dict) or not isinstance(data.get("messages"), list):
        return None
    senders: set = set()
    if isinstance(data.get("name"), str) and "personal" in str(data.get("type") or ""):
        senders.add(data["name"].strip())
    messages: list = []
    system = 0
    for msg in data["messages"]:
        if not isinstance(msg, dict):
            continue
        for k in ("from", "actor", "forwarded_from", "saved_from"):
            v = msg.get(k)
            if isinstance(v, str) and v.strip():
                senders.add(v.strip())
        for mem in msg.get("members") or []:
            if isinstance(mem, str) and mem.strip():
                senders.add(mem.strip())
        for ent in (msg.get("text_entities") or []) + (msg.get("text") if isinstance(msg.get("text"), list) else []):
            if isinstance(ent, dict) and ent.get("type") == "mention_name" and isinstance(ent.get("text"), str):
                senders.add(ent["text"].strip())
        if msg.get("type") != "message":
            system += 1
            continue
        body = _telegram_text(msg.get("text")).strip()
        if not body:
            system += 1
            continue
        messages.append({"msg_id": msg.get("id"), "date": date_from_iso(msg.get("date")) if isinstance(msg.get("date"), str) else None,
                         "sender": str(msg.get("from") or ""), "text": body})
    senders.discard("")
    return {"format": "telegram", "messages": messages, "senders": senders, "system_dropped": system,
            "date_order": None, "detected_by": None}


_NAME_COLUMNS = ("sender", "name", "from", "author", "user", "username", "phone", "email", "sender name", "from name")
_DMY_RE = re.compile(r"^\s*(\d{1,4})[./-](\d{1,2})[./-](\d{2,4})")
_ISO_RE = re.compile(r"^\s*(\d{4})-(\d{2})-(\d{2})")


def parse_csv_chat(text: str) -> dict | None:
    """A .csv with `date` and `text` columns (any case). Name-like columns feed known names and are dropped."""
    reader = csv.DictReader(io.StringIO(str(text or ""), newline=""))
    fields = [str(f or "").strip().lstrip("﻿").lower() for f in (reader.fieldnames or [])]
    if "date" not in fields or "text" not in fields:
        return None
    rows: list = []
    for row in reader:
        rows.append({str(k or "").strip().lstrip("﻿").lower(): (v if isinstance(v, str) else "") for k, v in row.items()})
    triples = []
    for row in rows:
        d = row.get("date") or ""
        if not _ISO_RE.match(d):
            m = _DMY_RE.match(d)
            if m:
                triples.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
    order, detected_by = _detect_date_order(triples) if triples else ("iso", "dates are written YYYY-MM-DD")
    senders: set = set()
    messages: list = []
    system = 0
    for n, row in enumerate(rows, 1):
        for col in _NAME_COLUMNS:
            v = row.get(col)
            if v and v.strip():
                senders.add(v.strip())
        body = (row.get("text") or "").strip()
        if not body:
            system += 1
            continue
        d = row.get("date") or ""
        date = None
        m = _ISO_RE.match(d)
        if m:
            date = _date_from_fields(int(m.group(1)), int(m.group(2)), int(m.group(3)), "year-first")
        else:
            m = _DMY_RE.match(d)
            if m:
                date = _date_from_fields(int(m.group(1)), int(m.group(2)), int(m.group(3)), order)
        messages.append({"row": n, "date": date, "sender": "", "text": body})
    return {"format": "csv", "messages": messages, "senders": senders, "system_dropped": system,
            "date_order": order, "detected_by": detected_by}


def parse_paragraphs(text: str) -> dict:
    """Plain text or Markdown: one undated message per paragraph (blocks separated by blank lines)."""
    messages = []
    for n, para in enumerate(re.split(r"\n\s*\n", str(text or "").strip()), 1):
        body = para.strip()
        if body:
            messages.append({"paragraph": n, "date": None, "sender": "", "text": body})
    return {"format": "text", "messages": messages, "senders": set(), "system_dropped": 0, "date_order": None, "detected_by": None}


# --------------------------------------------------------------------------- ingest-inbox
def inbox_dir(room: str, customers: bool = False) -> Path:
    kind = "customers" if customers else "closed_groups"
    return common.funnel_root() / "inbox" / kind / common.check_slug(room, "room")


def _safe_label(rel_path: str, known_names) -> str:
    """A file label safe to store and print: sender names removed, odd characters replaced."""
    label = anonymize(rel_path, known_names=sorted(known_names))
    label = re.sub(r"\s+", "_", label)
    return re.sub(r"[^A-Za-z0-9._/\[\]-]+", "_", label)


_CHAT_WITH_RE = re.compile(r"^(?:whatsapp\s+)?chat\s+with\s+(.+?)\s*$", re.IGNORECASE)


def _names_from_filename(path: Path) -> set:
    """WhatsApp names an export "WhatsApp Chat with <contact>": that contact is a known name too."""
    m = _CHAT_WITH_RE.match(path.stem)
    return {m.group(1).strip()} if m and len(m.group(1).strip()) >= 2 else set()


def _parse_inbox_file(path: Path) -> dict | None:
    ext = path.suffix.lower()
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None
    if ext == ".json":
        try:
            return parse_telegram(json.loads(text))
        except json.JSONDecodeError:
            return None
    if ext == ".csv":
        return parse_csv_chat(text)
    if ext in (".txt", ".md", ".text", ".log"):
        return parse_whatsapp(text) if looks_like_whatsapp(text) else parse_paragraphs(text)
    return None


def ingest_inbox(run, room: str, customers: bool = False, round_no: int = 1, command: str = "ingest-inbox") -> dict:
    """Parse every export in inbox/<kind>/<room>/, anonymize with sender names as known names, store.

    Sender names never reach disk, the run log or the screen. Messages under 3 words and
    system lines are dropped. Returns counts only.
    """
    room = common.check_slug(room, "room")
    kind = "customers" if customers else "closed_groups"
    source = f"inbox:{kind}"
    folder = inbox_dir(room, customers)
    summary = {"room": room, "kind": kind, "source": source, "folder": common.rel(folder), "files": [], "files_read": 0,
               "files_skipped": 0, "messages": 0, "dropped_system": 0, "dropped_short": 0, "records_new": 0,
               "duplicates": 0, "senders_removed": 0, "formats": {}, "new_ids": [], "file": None}
    paths = sorted(p for p in folder.rglob("*") if folder.exists() and p.is_file()
                   and not any(part.startswith(".") for part in p.relative_to(folder).parts))
    parsed: list = []
    known: set = set()
    for p in paths:
        result = _parse_inbox_file(p)
        if result is None:
            summary["files_skipped"] += 1
            continue
        known |= {s for s in result["senders"] if isinstance(s, str) and len(s.strip()) >= 2}
        known |= _names_from_filename(p)
        parsed.append((p, result))
    if not parsed:
        reason = (f"no chat exports in {common.rel(folder)}/ (WhatsApp .txt, Telegram result.json, .csv with "
                  f"date,text, or .txt/.md)")
        common.log_event(run, STAGE, command, "skip", room=room, source=source, reason=reason,
                         would_add=f"the founder's own {kind.replace('_', ' ')} messages: first-person pains in the room's words")
        summary["skipped_reason"] = reason
        return summary
    all_records: list = []
    base = len(records.load_records(run, room))
    seq = 0
    for p, result in parsed:
        label = _safe_label(p.relative_to(folder).as_posix(), known)
        fmt = result["format"]
        entry = {"file": label, "format": fmt, "messages": len(result["messages"]), "dropped_system": result["system_dropped"],
                 "dropped_short": 0, "records": 0, "date_order": result["date_order"], "detected_by": result["detected_by"]}
        for msg in result["messages"]:
            if word_count(msg["text"]) < 3:
                entry["dropped_short"] += 1
                continue
            if "line" in msg:
                frag, where = str(msg["line"]), {"line": msg["line"]}
            elif "msg_id" in msg:
                frag, where = str(msg["msg_id"]), {"msg_id": msg["msg_id"]}
            elif "row" in msg:
                frag, where = f"r{msg['row']}", {"row": msg["row"]}
            else:
                frag, where = f"p{msg['paragraph']}", {"paragraph": msg["paragraph"]}
            seq += 1
            meta = {"kind": "chat_message", "format": fmt, "file": label, "inbox": kind, "round": int(round_no),
                    "order": [int(round_no), 0, base + seq], "date_from": "file" if msg["date"] else "none"}
            meta.update(where)
            all_records.append({"url": f"inbox://{kind}/{room}/{label}#{frag}", "text": msg["text"], "date": msg["date"], "meta": meta})
            entry["records"] += 1
        summary["files"].append(entry)
        summary["files_read"] += 1
        summary["messages"] += entry["messages"]
        summary["dropped_system"] += entry["dropped_system"]
        summary["dropped_short"] += entry["dropped_short"]
        summary["formats"][fmt] = summary["formats"].get(fmt, 0) + 1
        if result["date_order"]:
            common.log_event(run, STAGE, command, "note", room=room, source=source, file=label, review=False,
                             date_order=result["date_order"], note=f"Dates read as {result['date_order']}: {result['detected_by']}.")
    stored = records.store_records(run, room, source, all_records, known_names=sorted(known), command=command)
    summary.update(records_new=stored["new"], duplicates=stored["duplicates"], senders_removed=len(known),
                   new_ids=stored["new_ids"], file=stored["file"])
    return summary


# --------------------------------------------------------------------------- commands
def _print_fetch_summary(s: dict) -> None:
    a = s["adapter"]
    head = {
        "stackexchange": f"Stack Exchange site {s.get('site')}, query {s.get('query')!r}",
        "hackernews": f"Hacker News, query {s.get('query')!r}",
        "reddit": f"Reddit r/{s.get('subreddit')}" + (f", query {s.get('query')!r}" if s.get("query") else ", newest posts"),
        "youtube": f"YouTube, {len(s.get('videos') or [])} video(s)" + (f" (search {s.get('search')!r})" if s.get("search") else ""),
        "apple": f"Apple App Store reviews, app id {s.get('app_id')}, country {s.get('country')}",
        "discourse": f"Discourse forum {s.get('forum')}" + (f", query {s.get('query')!r}" if s.get("query") else ""),
        "web": f"Web page(s): {', '.join(s.get('pages') or [])}",
    }.get(a, a)
    print(f"{head}: {s['requests']} request(s), {s['from_cache']} answered from the cache.")
    parts = [f"{s['seen']} item(s) seen"]
    if a == "stackexchange":
        parts.append(f"{s['questions_seen']} questions and {s['answers_seen']} answers")
    if a == "hackernews":
        parts.append(f"{s['stories_seen']} stories and {s['comments_seen']} comments")
    if a == "reddit":
        parts.append(f"{s['posts_seen']} posts and {s['comments_seen']} comments")
    if s.get("dropped_old"):
        parts.append(f"{s['dropped_old']} older than {s.get('lookback')} dropped (the lookback window)")
    if s.get("skipped_empty"):
        parts.append(f"{s['skipped_empty']} empty skipped")
    print("; ".join(parts) + ".")
    print(f"Records new: {s['records_new']}. Duplicates: {s['duplicates']}. Stored in {s['file']}.")
    if a == "stackexchange":
        extra = [f"quota remaining {s['quota_remaining']}" if s.get("quota_remaining") is not None else "",
                 f"waited {s['backoff_seconds']:.0f}s on API backoff" if s.get("backoff_seconds") else "",
                 f"stopped early: {s['stopped']}" if s.get("stopped") else ""]
        extra = [e for e in extra if e]
        if extra:
            print("Stack Exchange: " + "; ".join(extra) + ".")
    if a == "youtube":
        print(f"YouTube API quota used this call: {s['quota_units']} unit(s) (cached calls cost nothing)."
              + (f" Videos refused (HTTP 403): {', '.join(s['refused'])}." if s.get("refused") else ""))
    if a == "web" and s.get("truncated"):
        print(f"{s['truncated']} page(s) cut at {WEB_TEXT_CAP} characters.")
    print("Author, username and profile fields were never stored; text was anonymized before storage.")


def cmd_fetch(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    adapter = args.adapter
    max_records = int(getattr(args, "max", DEFAULT_MAX) or DEFAULT_MAX)
    if max_records < 1:
        raise common.ValidationErrors(["--max must be at least 1."])
    round_no = int(getattr(args, "round", 1) or 1)
    if round_no < 1:
        raise common.ValidationErrors(["--round must be a whole number from 1."])
    if adapter == "stackexchange":
        s = fetch_stackexchange(run, room, args.site, args.query, tagged=args.tagged, answers=args.answers,
                                max_records=max_records, round_no=round_no)
    elif adapter == "hackernews":
        s = fetch_hackernews(run, room, args.query, max_records=max_records, round_no=round_no)
    elif adapter == "reddit":
        s = fetch_reddit(run, room, args.subreddit, query=args.query, max_records=max_records, round_no=round_no)
    elif adapter == "youtube":
        s = fetch_youtube(run, room, videos=args.video or [], search=args.search, videos_k=args.videos,
                          max_records=max_records, round_no=round_no)
    elif adapter == "apple":
        s = fetch_apple(run, room, args.app, country=args.country, max_records=max_records, round_no=round_no)
    elif adapter == "discourse":
        s = fetch_discourse(run, room, args.forum, query=args.query, topics=args.topic or [],
                            max_records=max_records, round_no=round_no)
    elif adapter == "web":
        s = fetch_web(run, room, args.url, round_no=round_no)
    else:
        raise common.ValidationErrors([f"fetch: unknown adapter {adapter!r}. Choose one of {', '.join(ADAPTERS)}."])
    _print_fetch_summary(s)
    common.log_event(run, STAGE, "fetch", "source", room=room, source=s["source"], adapter=adapter,
                     domain=s.get("domain") or API_DOMAINS.get(adapter), seen=s["seen"], dropped_old=s["dropped_old"],
                     records_new=s["records_new"], duplicates=s["duplicates"], requests=s["requests"],
                     from_cache=s["from_cache"], round=round_no,
                     **{k: s[k] for k in ("site", "query", "subreddit", "search", "app_id", "country", "forum", "pages",
                                          "quota_units", "quota_remaining", "stopped") if k in s})
    return 0


def cmd_ingest_inbox(args) -> int:
    run = common.run_dir(args.run)
    room = common.check_slug(args.room, "room")
    round_no = int(getattr(args, "round", 1) or 1)
    if round_no < 1:
        raise common.ValidationErrors(["--round must be a whole number from 1."])
    s = ingest_inbox(run, room, customers=bool(args.customers), round_no=round_no)
    if s.get("skipped_reason"):
        print(f"Nothing to ingest: {s['skipped_reason']}. Logged as skipped.")
        return 0
    fmts = ", ".join(f"{k} {v}" for k, v in sorted(s["formats"].items()))
    print(f"Inbox {s['kind']} for room {room}: {s['files_read']} file(s) read ({fmts}); {s['files_skipped']} skipped.")
    for f in s["files"]:
        order = f" Dates read as {f['date_order']} ({f['detected_by']})." if f.get("date_order") else ""
        print(f"  {f['file']}: {f['format']}, {f['messages']} messages, {f['dropped_system']} system lines dropped, "
              f"{f['dropped_short']} messages under 3 words dropped, {f['records']} kept.{order}")
    print(f"Sender names removed from every message: {s['senders_removed']} distinct (never stored or printed).")
    print(f"Records new: {s['records_new']}. Duplicates: {s['duplicates']}. Source {s['source']}, stored in {s['file']}.")
    common.log_event(run, STAGE, "ingest-inbox", "source", room=room, source=s["source"], files=s["files_read"],
                     files_skipped=s["files_skipped"], formats=s["formats"], messages=s["messages"],
                     dropped_system=s["dropped_system"], dropped_short=s["dropped_short"], records_new=s["records_new"],
                     duplicates=s["duplicates"], senders_removed=s["senders_removed"], round=round_no)
    return 0


def register(subparsers) -> None:
    p = subparsers.add_parser("fetch", help="Collect full-text records through an official API or from a public page.")
    ad = p.add_subparsers(dest="adapter", metavar="<adapter>", parser_class=type(p))
    ad.required = True

    def shared(sp):
        sp.add_argument("--room", required=True, help="room slug")
        sp.add_argument("--max", type=int, default=DEFAULT_MAX, help=f"stop after this many records (default {DEFAULT_MAX})")
        sp.add_argument("--round", type=int, default=1, help="the Stage 3 round these records belong to (default 1)")

    se = ad.add_parser("stackexchange", help="Stack Exchange API: questions (and answers) with full text and dates.")
    shared(se)
    se.add_argument("--site", required=True, help="site name, like stackoverflow, academia or money")
    se.add_argument("--query", required=True, help="free-text search")
    se.add_argument("--tagged", default=None, help="only questions with this tag (semicolon-separated for several)")
    se.add_argument("--answers", action="store_true", help="also store one record per answer")

    hn = ad.add_parser("hackernews", help="Hacker News (Algolia search API): stories and comments.")
    shared(hn)
    hn.add_argument("--query", required=True, help="free-text search")

    rd = ad.add_parser("reddit", help="Reddit Data API (needs REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT).")
    shared(rd)
    rd.add_argument("--subreddit", required=True, help="subreddit name without r/")
    rd.add_argument("--query", default=None, help="search inside the subreddit (default: newest posts)")

    yt = ad.add_parser("youtube", help="YouTube Data API v3 comments (needs YOUTUBE_API_KEY).")
    shared(yt)
    yt.add_argument("--video", nargs="*", default=None, metavar="ID_OR_URL", help="one or more video ids or URLs")
    yt.add_argument("--search", default=None, help="find videos by search (costs 100 quota units)")
    yt.add_argument("--videos", type=int, default=5, help="how many videos to take from --search (default 5, at most 50)")

    ap = ad.add_parser("apple", help="Apple App Store customer reviews (public RSS feed).")
    shared(ap)
    ap.add_argument("--app", required=True, help="numeric app id, like 1234567890")
    ap.add_argument("--country", default="us", help="two-letter storefront code (default us)")

    dc = ad.add_parser("discourse", help="A Discourse forum: posts of matching topics (needs a decision for its domain).")
    shared(dc)
    dc.add_argument("--forum", required=True, help="forum base URL, like https://community.example.org")
    dc.add_argument("--query", default=None, help="forum search (uses /search.json when robots.txt allows it)")
    dc.add_argument("--topic", nargs="*", default=None, metavar="ID_OR_URL", help="topic ids or URLs to fetch directly")

    wb = ad.add_parser("web", help="One public page as one record (needs a decision for its domain; robots.txt honoured).")
    wb.add_argument("--room", required=True, help="room slug")
    wb.add_argument("--url", nargs="+", required=True, help="page URL(s)")
    wb.add_argument("--round", type=int, default=1, help="the Stage 3 round these records belong to (default 1)")
    p.set_defaults(func=cmd_fetch)

    ii = subparsers.add_parser("ingest-inbox", help="Anonymize and store the founder's chat exports from inbox/.")
    ii.add_argument("--room", required=True, help="room slug")
    ii.add_argument("--customers", action="store_true", help="read inbox/customers/<room>/ instead of inbox/closed_groups/<room>/")
    ii.add_argument("--round", type=int, default=1, help="the Stage 3 round these records belong to (default 1)")
    ii.set_defaults(func=cmd_ingest_inbox)
