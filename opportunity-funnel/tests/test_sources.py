"""Tests for pipeline/sources.py `fetch` adapters: mocked payloads shaped like the real APIs,
config/sources.md enforcement, exit 3 for missing keys and blocked domains, no author fields stored."""
import json

import pytest

import common
import funnel
import netfetch
import records
import sources
from anonymize import anonymize

ROOM = "gre-engineers-india"
RUN = "2026-09-26"
CUTOFF_EPOCH = 1727308800  # 2024-09-26T00:00:00Z: 24 months before the run date
OLD_EPOCH = 1700000000  # 2023-11-14, outside the lookback
NEW_EPOCH = 1735689600  # 2025-01-01
NEWER_EPOCH = 1738404000  # 2025-02-01
AUTHOR_KEYS = ("author", "owner", "display_name", "username", "avatar", "avatar_template", "authorDisplayName",
               "authorChannelUrl", "authorProfileImageUrl", "from_id", "user_id")
AUTHOR_NAMES = ("Zubin Mistry", "Mistry", "Ann Lee", "throwaway_gre", "gre_thrower", "Ravi Kulkarni", "Kulkarni",
                "zubin", "AppFan99")

TABLE_HEADER = (
    "| Source | Adapter | What it gives | Domains the script must reach | Key needed | Terms to read | Status | Checked | Decision and reason |\n"
    "|---|---|---|---|---|---|---|---|---|\n"
)
TABLE_ROWS = {
    "stackexchange": ("Stack Exchange API", "`api.stackexchange.com`", "Optional `STACKEXCHANGE_KEY`"),
    "hackernews": ("Hacker News (Algolia search API)", "`hn.algolia.com`", "none"),
    "reddit": ("Reddit Data API", "`www.reddit.com`, `oauth.reddit.com`", "`REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`"),
    "youtube": ("YouTube Data API v3", "`www.googleapis.com`", "`YOUTUBE_API_KEY`"),
    "apple_reviews": ("Apple App Store reviews feed", "`itunes.apple.com`", "none"),
    "web": ("Public web pages", "each page's own domain", "none"),
    "discourse": ("Discourse forums", "each forum's domain", "none"),
    "inbox": ("Founder's chat exports", "none", "none"),
}


def write_sources_md(froot, statuses=None, checked=RUN, decisions=()):
    """A config/sources.md with every adapter row set to a status (default allowed) and decision-log lines."""
    statuses = statuses or {}
    lines = ["# Sources and terms decisions", "", TABLE_HEADER.rstrip("\n")]
    for adapter, (name, domains, key) in TABLE_ROWS.items():
        status = statuses.get(adapter, "allowed")
        lines.append(f"| {name} | `{adapter}` | text | {domains} | {key} | https://terms.test | {status} | {checked} | test decision |")
    lines += ["", "## Decision log", "Append one line per check: `- YYYY-MM-DD | source | status | reason | URL of the clause read`."]
    lines += list(decisions)
    (froot / "config" / "sources.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


class FakeResponse:
    def __init__(self, status=200, text="", headers=None):
        self.status_code = status
        self.text = text
        self.headers = headers or {}


def _json(obj, status=200):
    return FakeResponse(status, json.dumps(obj), {"Content-Type": "application/json; charset=utf-8"})


class Router:
    """A fake netfetch._http_get: routes by (url, params) predicate; robots.txt is 404 unless routed."""

    def __init__(self):
        self.routes = []
        self.calls = []

    def add(self, pred, response):
        self.routes.append((pred, response))
        return self

    def __call__(self, url, params=None, headers=None, timeout=30):
        self.calls.append({"url": url, "params": dict(params or {}), "headers": dict(headers or {})})
        for pred, response in self.routes:
            if pred(url, params or {}):
                return response(url, params or {}) if callable(response) else response
        if url.endswith("/robots.txt"):
            return FakeResponse(404, "")
        raise AssertionError(f"unexpected request: {url} {params}")

    def api_calls(self):
        return [c for c in self.calls if not c["url"].endswith("/robots.txt")]


def _online(monkeypatch, router):
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")
    monkeypatch.setattr(netfetch, "_http_get", router)


def _raw(run, source):
    return records.source_file(run, ROOM, source).read_text(encoding="utf-8")


def _assert_no_author_fields(raw):
    for rec in (json.loads(line) for line in raw.splitlines() if line.strip()):
        assert set(rec) == set(records.RECORD_FIELDS)
        for k in AUTHOR_KEYS:
            assert k not in rec["meta"], k
    for name in AUTHOR_NAMES:
        assert name not in raw, name


def _events(run):
    return common.read_jsonl(run / "runlog.jsonl")


# --------------------------------------------------------------------------- config/sources.md enforcement
def test_real_sources_md_parses(run):
    info = sources.parse_sources_md()
    assert {r["adapter"] for r in info["rows"]} >= {"stackexchange", "hackernews", "reddit", "youtube", "apple_reviews", "web", "discourse"}
    assert all(r["status"] and common.is_date(r["checked"]) for r in info["rows"])
    assert len(info["decisions"]) >= 1 and all(common.is_date(d["date"]) and d["status"] for d in info["decisions"])
    assert sources.api_source_check("apple")["source"] == "Apple App Store reviews feed"  # `apple` finds the apple_reviews row


def test_unallowed_statuses_are_refused_and_logged(froot, run):
    write_sources_md(froot, statuses={"stackexchange": "blocked-by-network", "reddit": "skip", "youtube": "unchecked"})
    se = sources.api_source_check("stackexchange")
    assert se["ok"] is False and se["status"] == "blocked-by-network" and "not a terms decision" in se["problem"]
    assert "funnel source-decision" in se["problem"]
    assert sources.api_source_check("reddit")["ok"] is False and sources.api_source_check("reddit")["status"] == "skip"
    assert sources.api_source_check("hackernews")["ok"] is True
    with pytest.raises(sources.SourceNotAllowed) as e:
        sources.ensure_allowed(run, "youtube")
    assert e.value.code == 1 and "config/sources.md" in str(e.value) and "`unchecked`" in str(e.value)
    assert any(ev["kind"] == "skip" and ev["source"] == "youtube" and ev["domain"] == "www.googleapis.com" for ev in _events(run))
    assert sources.api_source_check("nosuch")["ok"] is False and "no table row" in sources.api_source_check("nosuch")["problem"]
    d = sources.domain_decision_check("forum.example.org")
    assert d["ok"] is False and "no decision-log line for the domain forum.example.org" in d["problem"]
    with pytest.raises(sources.SourceNotAllowed):
        sources.ensure_allowed(run, "web", domain="forum.example.org")


def test_decisions_expire_after_90_days_and_latest_domain_line_wins(froot, run):
    write_sources_md(froot, checked="2026-07-01")  # 87 days before FUNNEL_TODAY
    assert sources.api_source_check("stackexchange")["ok"] is True
    write_sources_md(froot, checked="2026-06-27")  # 91 days
    chk = sources.api_source_check("stackexchange")
    assert chk["ok"] is False and "91 days ago" in chk["problem"]
    write_sources_md(froot, statuses={"hackernews": "allowed-with-limits", "youtube": "unchecked"})
    assert sources.api_source_check("hackernews")["ok"] is True
    assert sources.api_source_check("youtube")["ok"] is False
    write_sources_md(froot, decisions=[
        "- 2026-09-01 | forum.test | allowed | terms allow reading | https://forum.test/tos",
        "- 2026-09-20 | forum.test | skip | terms changed | https://forum.test/tos",
        "- 2026-06-01 | old.test | allowed | fine | https://old.test/tos",
        "- 2026-09-25 | www.blog.test | allowed-with-limits | one page a second | https://blog.test/tos",
    ])
    assert sources.domain_decision_check("forum.test")["ok"] is False
    assert "`skip`" in sources.domain_decision_check("forum.test")["problem"]
    assert "days ago" in sources.domain_decision_check("old.test")["problem"]
    assert sources.domain_decision_check("blog.test")["ok"] is True  # www. is ignored
    assert sources.domain_decision_check("https://blog.test/page")["ok"] is True


def test_cli_fetch_refused_by_sources_md_exits_1(froot, run, cli):
    write_sources_md(froot, statuses={"stackexchange": "blocked-by-network"})
    r = cli("fetch", "stackexchange", "--room", ROOM, "--site", "academia", "--query", "GRE", "--run", RUN)
    assert r.returncode == 1, r.stderr
    assert "1. config/sources.md" in r.stderr and "Stack Exchange API" in r.stderr
    r = cli("fetch", "--help")
    assert r.returncode == 0 and all(a in r.stdout for a in sources.ADAPTERS)


# --------------------------------------------------------------------------- Stack Exchange
def _se_router():
    q1 = {"question_id": 101, "title": "Is GRE coaching worth &quot;the money&quot;?",
          "body": "<p>I am Zubin Mistry and I paid <b>15,000</b> rupees.</p><p>Still stuck.</p>",
          "link": "https://academia.stackexchange.com/questions/101/is-gre-coaching-worth-the-money",
          "creation_date": NEW_EPOCH, "answer_count": 1, "score": 3,
          "owner": {"display_name": "Zubin Mistry", "user_id": 5, "reputation": 10,
                    "link": "https://academia.stackexchange.com/users/5/zubin-mistry", "profile_image": "https://i.test/5.png"}}
    q_old = {"question_id": 102, "title": "Old question about GRE", "body": "<p>old body</p>",
             "link": "https://academia.stackexchange.com/questions/102/old", "creation_date": OLD_EPOCH,
             "answer_count": 0, "owner": {"display_name": "Ann Lee", "user_id": 6}}
    q3 = {"question_id": 103, "title": "GRE coaching fees in Hyderabad", "body": "<p>Quoted 40k for two months.</p>",
          "link": "https://academia.stackexchange.com/questions/103/gre-coaching-fees", "creation_date": NEWER_EPOCH,
          "answer_count": 0, "owner": {"display_name": "gre_thrower", "user_id": 7}}
    a1 = {"answer_id": 201, "question_id": 101, "body": "<p>Coaching is a waste. Self study works.</p>",
          "creation_date": NEW_EPOCH + 86400, "is_accepted": True, "score": 2,
          "link": "https://academia.stackexchange.com/questions/101/is-gre-coaching-worth-the-money/201#201",
          "owner": {"display_name": "Ann Lee", "user_id": 6}}
    r = Router()
    r.add(lambda u, p: u.endswith("/search/advanced") and p.get("page") == 1,
          _json({"items": [q1, q_old], "has_more": True, "quota_max": 10000, "quota_remaining": 9990, "backoff": 3}))
    r.add(lambda u, p: u.endswith("/search/advanced") and p.get("page") == 2,
          _json({"items": [q3], "has_more": False, "quota_max": 10000, "quota_remaining": 9989}))
    r.add(lambda u, p: u.endswith("/questions/101/answers"),
          _json({"items": [a1], "has_more": False, "quota_max": 10000, "quota_remaining": 9988}))
    return r


def test_stackexchange_records_lookback_backoff_answers_and_rerun(froot, run, monkeypatch):
    write_sources_md(froot)
    router = _se_router()
    _online(monkeypatch, router)
    sleeps = []
    monkeypatch.setattr(netfetch, "_sleep", lambda s: sleeps.append(s))
    s = sources.fetch_stackexchange(run, ROOM, "academia", "GRE coaching", answers=True)
    assert s["records_new"] == 3 and s["duplicates"] == 0 and s["dropped_old"] == 1
    assert s["questions_seen"] == 3 and s["answers_seen"] == 1 and s["requests"] == 3 and s["from_cache"] == 0
    assert s["quota_remaining"] == 9988 and s["backoff_seconds"] == 3.0 and s["key_used"] is False
    assert sleeps == [3.0]
    first = router.api_calls()[0]
    assert first["url"] == "https://api.stackexchange.com/2.3/search/advanced"
    assert first["params"]["fromdate"] == CUTOFF_EPOCH and first["params"]["filter"] == "withbody"
    assert first["params"]["site"] == "academia" and first["params"]["q"] == "GRE coaching" and "key" not in first["params"]
    assert router.api_calls()[2]["params"]["site"] == "academia" and "fromdate" not in router.api_calls()[2]["params"]

    recs = records.load_records(run, ROOM)
    by_url = {r["url"]: r for r in recs}
    q = by_url["https://academia.stackexchange.com/questions/101/is-gre-coaching-worth-the-money"]
    assert q["text"] == 'Is GRE coaching worth "the money"?\n\nI am [name] and I paid 15,000 rupees.\nStill stuck.'
    assert q["date"] == "2025-01-01" and q["source"] == "stackexchange"
    assert q["meta"]["kind"] == "question" and q["meta"]["date_from"] == "api" and q["meta"]["site"] == "academia"
    assert q["meta"]["order"] == [1, 0, 1] and q["meta"]["round"] == 1 and q["meta"]["fetched_at"] == RUN
    assert q["meta"]["domain"] == "academia.stackexchange.com"
    a = by_url["https://academia.stackexchange.com/questions/101/is-gre-coaching-worth-the-money/201#201"]
    assert a["text"] == "Coaching is a waste. Self study works." and a["meta"]["kind"] == "answer" and a["meta"]["is_accepted"] is True
    assert a["meta"]["order"] == [1, 0, 3]
    assert all(r["record_id"] == common.record_id(r["url"], r["text"]) for r in recs)
    raw = _raw(run, "stackexchange")
    _assert_no_author_fields(raw)
    assert "users/5" not in raw

    # the same call again: everything from the cache, no waiting, byte-identical file
    before = records.source_file(run, ROOM, "stackexchange").read_bytes()
    s2 = sources.fetch_stackexchange(run, ROOM, "academia", "GRE coaching", answers=True)
    assert s2["records_new"] == 0 and s2["duplicates"] == 3 and s2["from_cache"] == 3
    assert sleeps == [3.0]
    assert records.source_file(run, ROOM, "stackexchange").read_bytes() == before
    ev = [e for e in _events(run) if e["kind"] == "source"]
    assert ev == []  # the source event is written by the command, not the function


def test_stackexchange_optional_key_is_sent_but_never_stored(froot, run, monkeypatch):
    write_sources_md(froot)
    monkeypatch.setenv("STACKEXCHANGE_KEY", "SE-SECRET-KEY")
    router = _se_router()
    _online(monkeypatch, router)
    monkeypatch.setattr(netfetch, "_sleep", lambda s: None)
    s = sources.fetch_stackexchange(run, ROOM, "academia", "GRE coaching", tagged="gre", max_records=2)
    assert s["key_used"] is True and s["records_new"] == 2 and s["collected"] == 2
    assert router.api_calls()[0]["params"]["key"] == "SE-SECRET-KEY" and router.api_calls()[0]["params"]["tagged"] == "gre"
    everything = "".join(p.read_text(encoding="utf-8") for p in froot.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".txt"))
    assert "SE-SECRET-KEY" not in everything


def test_stackexchange_stops_when_quota_is_used_up(froot, run, monkeypatch):
    write_sources_md(froot)
    router = Router().add(lambda u, p: p.get("page") == 1, _json({
        "items": [{"question_id": 1, "title": "GRE quant tips needed", "body": "<p>Help with quant please</p>",
                   "link": "https://academia.stackexchange.com/questions/1/gre", "creation_date": NEW_EPOCH, "answer_count": 0}],
        "has_more": True, "quota_remaining": 0}))
    _online(monkeypatch, router)
    s = sources.fetch_stackexchange(run, ROOM, "academia", "GRE")
    assert s["records_new"] == 1 and s["stopped"] and "quota" in s["stopped"] and len(router.api_calls()) == 1


# --------------------------------------------------------------------------- Hacker News
def test_hackernews_stories_and_comments(froot, run, monkeypatch, capsys):
    write_sources_md(froot)
    story = {"objectID": "41000001", "title": "Ask HN: Is GRE coaching a scam?", "story_text": "<p>Paid $500.</p><p>Nothing.</p>",
             "url": None, "author": "throwaway_gre", "points": 12, "created_at": "2025-02-01T10:00:00.000Z",
             "created_at_i": NEWER_EPOCH, "story_id": 41000001, "_tags": ["story", "author_throwaway_gre", "story_41000001"]}
    comment = {"objectID": "41000002", "title": None, "comment_text": "I wasted money too.<p>Twice.", "author": "gre_thrower",
               "created_at": "2025-02-01T10:10:00.000Z", "created_at_i": NEWER_EPOCH + 600, "story_id": 41000001,
               "parent_id": 41000001, "_tags": ["comment", "author_gre_thrower", "story_41000001"]}
    old = {"objectID": "30000000", "title": "Old GRE story", "story_text": None, "author": "pg", "created_at_i": OLD_EPOCH,
           "_tags": ["story", "author_pg", "story_30000000"]}
    router = Router()
    router.add(lambda u, p: p.get("page") == 0, _json({"hits": [story, comment], "nbHits": 3, "page": 0, "nbPages": 2, "hitsPerPage": 100}))
    router.add(lambda u, p: p.get("page") == 1, _json({"hits": [old], "nbHits": 3, "page": 1, "nbPages": 2, "hitsPerPage": 100}))
    _online(monkeypatch, router)
    rc = funnel.main(["fetch", "hackernews", "--room", ROOM, "--query", "GRE coaching", "--run", RUN])
    assert rc == 0
    out = capsys.readouterr().out
    assert "Records new: 2" in out and "1 older than 2024-09-26 dropped" in out
    first = router.api_calls()[0]
    assert first["url"] == "https://hn.algolia.com/api/v1/search_by_date"
    assert first["params"]["numericFilters"] == f"created_at_i>{CUTOFF_EPOCH}" and first["params"]["tags"] == "(story,comment)"
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    st = recs["https://news.ycombinator.com/item?id=41000001"]
    assert st["text"] == "Ask HN: Is GRE coaching a scam?\n\nPaid $500.\nNothing." and st["meta"]["kind"] == "story"
    assert st["date"] == "2025-02-01"
    cm = recs["https://news.ycombinator.com/item?id=41000002"]
    assert cm["text"] == "I wasted money too.\nTwice." and cm["meta"]["kind"] == "comment" and cm["meta"]["story_id"] == 41000001
    _assert_no_author_fields(_raw(run, "hackernews"))
    ev = [e for e in _events(run) if e["kind"] == "source" and e["command"] == "fetch"]
    assert len(ev) == 1 and ev[0]["records_new"] == 2 and ev[0]["domain"] == "hn.algolia.com" and ev[0]["adapter"] == "hackernews"


# --------------------------------------------------------------------------- Reddit
def _reddit_env(monkeypatch, **overrides):
    values = {"REDDIT_CLIENT_ID": "cid-SECRET", "REDDIT_CLIENT_SECRET": "csec-SECRET", "REDDIT_USER_AGENT": "funnel-test/0.1"}
    values.update(overrides)
    for k, v in values.items():
        if v is None:
            monkeypatch.delenv(k, raising=False)
        else:
            monkeypatch.setenv(k, v)


def test_reddit_missing_keys_exit_3_names_the_variables(froot, run, monkeypatch, cli):
    write_sources_md(froot)
    _reddit_env(monkeypatch, REDDIT_CLIENT_ID=None, REDDIT_CLIENT_SECRET=None, REDDIT_USER_AGENT=None)
    with pytest.raises(sources.MissingKey) as e:
        sources.fetch_reddit(run, ROOM, "GRE")
    assert e.value.code == 3 and isinstance(e.value, common.Blocked)
    assert "set the environment variable REDDIT_CLIENT_ID" in str(e.value)
    assert "REDDIT_CLIENT_SECRET" in str(e.value) and "REDDIT_USER_AGENT" in str(e.value)
    blocked = [ev for ev in _events(run) if ev["kind"] == "blocked"]
    assert blocked and blocked[-1]["key_names"] == ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]
    _reddit_env(monkeypatch, REDDIT_USER_AGENT=None)
    with pytest.raises(sources.MissingKey) as e:
        sources.fetch_reddit(run, ROOM, "GRE")
    assert e.value.names == ["REDDIT_USER_AGENT"] and "cid-SECRET" not in str(e.value)
    r = cli("fetch", "reddit", "--room", ROOM, "--subreddit", "GRE", "--run", RUN)
    assert r.returncode == 3, r.stderr
    assert "Blocked" in r.stderr and "REDDIT_USER_AGENT" in r.stderr and "SECRET" not in r.stderr + r.stdout


def test_reddit_posts_and_top_level_comments_with_token_never_stored(froot, run, monkeypatch):
    write_sources_md(froot)
    _reddit_env(monkeypatch)
    posts_seen = []

    def fake_post(url, data=None, headers=None, auth=None, timeout=30):
        posts_seen.append({"url": url, "data": data, "headers": headers, "auth": auth})
        return _json({"access_token": "TOKEN-SECRET-123", "token_type": "bearer", "expires_in": 86400, "scope": "*"})

    monkeypatch.setattr(sources, "_http_post", fake_post)
    post = {"kind": "t3", "data": {"id": "abc123", "title": "Wasted 30k on GRE coaching", "selftext": "Faculty kept changing.\n\nNo refund.",
                                   "permalink": "/r/GRE/comments/abc123/wasted_30k_on_gre_coaching/", "created_utc": NEW_EPOCH + 0.0,
                                   "author": "gre_thrower", "author_fullname": "t2_xyz", "num_comments": 2, "score": 40, "subreddit": "GRE"}}
    removed = {"kind": "t3", "data": {"id": "def456", "title": "Best coaching in Pune?", "selftext": "[removed]",
                                      "permalink": "/r/GRE/comments/def456/best_coaching_in_pune/", "created_utc": NEW_EPOCH + 10.0,
                                      "author": "throwaway_gre", "num_comments": 0}}
    old = {"kind": "t3", "data": {"id": "old001", "title": "Old post", "selftext": "", "permalink": "/r/GRE/comments/old001/old/",
                                  "created_utc": OLD_EPOCH + 0.0, "author": "pg", "num_comments": 5}}
    comments = [
        {"kind": "t1", "data": {"id": "c1", "body": "Same here, 25k gone.", "permalink": "/r/GRE/comments/abc123/wasted_30k_on_gre_coaching/c1/",
                                "created_utc": NEW_EPOCH + 100.0, "author": "throwaway_gre"}},
        {"kind": "t1", "data": {"id": "c2", "body": "[deleted]", "permalink": "/r/GRE/comments/abc123/x/c2/", "created_utc": NEW_EPOCH + 200.0, "author": "[deleted]"}},
        {"kind": "more", "data": {"count": 3, "children": ["c3"]}},
    ]
    router = Router()
    router.add(lambda u, p: u.endswith("/r/GRE/search"),
               _json({"kind": "Listing", "data": {"after": "t3_zzz", "children": [post, removed, old]}}))
    router.add(lambda u, p: u.endswith("/comments/abc123"),
               _json([{"kind": "Listing", "data": {"children": [post]}}, {"kind": "Listing", "data": {"children": comments}}]))
    _online(monkeypatch, router)
    s = sources.fetch_reddit(run, ROOM, "r/GRE", query="coaching refund")
    assert s["records_new"] == 3 and s["posts_seen"] == 3 and s["comments_seen"] == 2 and s["dropped_old"] == 1
    assert s["requests"] == 2  # the old post stopped the paging even though `after` was set
    assert posts_seen[0]["url"] == "https://www.reddit.com/api/v1/access_token" and posts_seen[0]["auth"] == ("cid-SECRET", "csec-SECRET")
    assert posts_seen[0]["data"] == {"grant_type": "client_credentials"} and posts_seen[0]["headers"]["User-Agent"] == "funnel-test/0.1"
    calls = router.api_calls()
    assert calls[0]["url"] == "https://oauth.reddit.com/r/GRE/search"
    assert calls[0]["params"]["q"] == "coaching refund" and calls[0]["params"]["restrict_sr"] == 1 and calls[0]["params"]["sort"] == "new"
    assert all(c["headers"]["Authorization"] == "bearer TOKEN-SECRET-123" and c["headers"]["User-Agent"] == "funnel-test/0.1" for c in calls)
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    p = recs["https://www.reddit.com/r/GRE/comments/abc123/wasted_30k_on_gre_coaching/"]
    assert p["text"] == "Wasted 30k on GRE coaching\n\nFaculty kept changing.\n\nNo refund." and p["meta"]["kind"] == "post"
    assert p["date"] == "2025-01-01" and p["meta"]["subreddit"] == "GRE"
    assert recs["https://www.reddit.com/r/GRE/comments/def456/best_coaching_in_pune/"]["text"] == "Best coaching in Pune?"
    c = recs["https://www.reddit.com/r/GRE/comments/abc123/wasted_30k_on_gre_coaching/c1/"]
    assert c["text"] == "Same here, 25k gone." and c["meta"]["kind"] == "comment" and c["meta"]["post_id"] == "abc123"
    raw = _raw(run, "reddit")
    _assert_no_author_fields(raw)
    everything = "".join(p.read_text(encoding="utf-8") for p in froot.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".txt", ".md"))
    assert "TOKEN-SECRET-123" not in everything and "cid-SECRET" not in everything and "csec-SECRET" not in everything


def test_reddit_refused_credentials_exit_3(froot, run, monkeypatch):
    write_sources_md(froot)
    _reddit_env(monkeypatch)
    monkeypatch.setattr(sources, "_http_post", lambda *a, **k: _json({"error": 401}, status=401))
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")
    with pytest.raises(common.Blocked) as e:
        sources.fetch_reddit(run, ROOM, "GRE")
    assert e.value.code == 3 and "www.reddit.com refused the API credentials" in str(e.value)


def test_rate_gate_allows_60_a_minute_then_waits(monkeypatch):
    clock = {"t": 1000.0}
    sleeps = []
    monkeypatch.setattr(sources, "_now", lambda: clock["t"])
    monkeypatch.setattr(netfetch, "_sleep", lambda s: sleeps.append(s))
    gate = sources.RateGate(3)
    assert [gate.wait() for _ in range(3)] == [0.0, 0.0, 0.0]
    clock["t"] = 1010.0
    assert gate.wait() == 50.0 and sleeps == [50.0]
    clock["t"] = 1070.0
    assert gate.wait() == 0.0 and sleeps == [50.0]
    assert sources._REDDIT_GATE.per_minute == 60


# --------------------------------------------------------------------------- YouTube
def _yt_comment(cid, text, published, author="Ravi Kulkarni"):
    return {"kind": "youtube#commentThread", "id": cid,
            "snippet": {"videoId": "x", "topLevelComment": {"kind": "youtube#comment", "id": cid, "snippet": {
                "textDisplay": text.replace("\n", "<br>"), "textOriginal": text, "authorDisplayName": author,
                "authorProfileImageUrl": "https://yt3.test/a.jpg", "authorChannelUrl": "http://www.youtube.com/@ravi",
                "likeCount": 4, "publishedAt": published, "updatedAt": published}}, "totalReplyCount": 0}}


def test_youtube_missing_key_and_fetch_with_search(froot, run, monkeypatch, cli):
    write_sources_md(froot)
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    with pytest.raises(sources.MissingKey) as e:
        sources.fetch_youtube(run, ROOM, videos=["dQw4w9WgXcQ"])
    assert "set the environment variable YOUTUBE_API_KEY" in str(e.value) and e.value.code == 3
    r = cli("fetch", "youtube", "--room", ROOM, "--video", "dQw4w9WgXcQ", "--run", RUN)
    assert r.returncode == 3 and "YOUTUBE_API_KEY" in r.stderr
    assert any(ev["kind"] == "blocked" and ev["key_names"] == ["YOUTUBE_API_KEY"] for ev in _events(run))

    monkeypatch.setenv("YOUTUBE_API_KEY", "YT-SECRET")
    router = Router()
    router.add(lambda u, p: u.endswith("/youtube/v3/search"),
               _json({"items": [{"id": {"kind": "youtube#video", "videoId": "dQw4w9WgXcQ"}, "snippet": {"title": "GRE prep review"}}],
                      "pageInfo": {"totalResults": 1}}))
    router.add(lambda u, p: u.endswith("/commentThreads") and p.get("videoId") == "abcdefghijk" and not p.get("pageToken"),
               _json({"items": [_yt_comment("Ug1", "I am Ravi Kulkarni and I paid 20k for this course, useless", "2025-03-01T10:00:00Z")],
                      "nextPageToken": "P2"}))
    router.add(lambda u, p: u.endswith("/commentThreads") and p.get("videoId") == "abcdefghijk" and p.get("pageToken") == "P2",
               _json({"items": [_yt_comment("Ug2", "Refund took 3 months", "2025-02-01T10:00:00Z")]}))
    router.add(lambda u, p: u.endswith("/commentThreads") and p.get("videoId") == "dQw4w9WgXcQ",
               _json({"items": [_yt_comment("Ug3", "Best free resource, thanks", "2025-04-01T10:00:00Z"),
                                _yt_comment("Ug4", "old comment here", "2023-01-01T10:00:00Z")], "nextPageToken": "NEVER"}))
    _online(monkeypatch, router)
    s = sources.fetch_youtube(run, ROOM, videos=["https://youtu.be/abcdefghijk"], search="GRE coaching review", videos_k=3)
    assert s["records_new"] == 3 and s["dropped_old"] == 1 and s["quota_units"] == 103 and s["refused"] == []
    assert s["videos"] == ["abcdefghijk", "dQw4w9WgXcQ"] and s["videos_from_search"] == 1
    calls = router.api_calls()
    assert calls[0]["params"]["publishedAfter"] == "2024-09-26T00:00:00Z" and calls[0]["params"]["maxResults"] == 3
    assert calls[0]["params"]["type"] == "video" and calls[0]["params"]["key"] == "YT-SECRET"
    assert calls[1]["params"]["textFormat"] == "plainText" and calls[1]["params"]["part"] == "snippet"
    assert len(calls) == 4  # the "NEVER" page token was not followed: older comments stop the paging
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    c = recs["https://www.youtube.com/watch?v=abcdefghijk&lc=Ug1"]
    assert c["text"] == "I am [name] and I paid 20k for this course, useless" and c["date"] == "2025-03-01"
    assert c["meta"] == {"kind": "comment", "video_id": "abcdefghijk", "comment_id": "Ug1", "search": "GRE coaching review",
                         "like_count": 4, "date_from": "api", "domain": "youtube.com", "round": 1, "order": [1, 0, 1], "fetched_at": RUN}
    assert "https://www.youtube.com/watch?v=dQw4w9WgXcQ&lc=Ug3" in recs
    raw = _raw(run, "youtube")
    _assert_no_author_fields(raw)
    everything = "".join(p.read_text(encoding="utf-8") for p in froot.rglob("*") if p.is_file() and p.suffix in (".json", ".jsonl", ".txt"))
    assert "YT-SECRET" not in everything
    cost = [ev for ev in _events(run) if ev["kind"] == "cost"]
    assert cost and cost[-1]["units"] == 103 and cost[-1]["tag"] == "measured"
    with pytest.raises(common.ValidationErrors):
        sources.youtube_video_id("https://example.test/not-a-video")


def test_youtube_every_video_refused_is_blocked(froot, run, monkeypatch):
    write_sources_md(froot)
    monkeypatch.setenv("YOUTUBE_API_KEY", "YT-SECRET")
    router = Router().add(lambda u, p: u.endswith("/commentThreads"), _json({"error": {"code": 403, "message": "quotaExceeded"}}, status=403))
    _online(monkeypatch, router)
    with pytest.raises(common.Blocked) as e:
        sources.fetch_youtube(run, ROOM, videos=["dQw4w9WgXcQ"])
    assert e.value.code == 3 and "www.googleapis.com" in str(e.value) and "YOUTUBE_API_KEY" in str(e.value)
    assert "YT-SECRET" not in str(e.value)


# --------------------------------------------------------------------------- Apple
def test_apple_reviews_feed(froot, run, monkeypatch):
    write_sources_md(froot)

    def review(rid, title, content, rating, updated, author="AppFan99"):
        return {"author": {"uri": {"label": f"https://itunes.apple.com/in/reviews/id{rid}"}, "name": {"label": author}, "label": ""},
                "updated": {"label": updated}, "im:rating": {"label": str(rating)}, "im:version": {"label": "4.2"},
                "id": {"label": str(rid)}, "title": {"label": title}, "content": {"label": content, "attributes": {"type": "text"}},
                "link": {"attributes": {"rel": "related", "href": "https://itunes.apple.com/in/review?id=1&type=Purple%20Software"}},
                "im:voteSum": {"label": "0"}, "im:contentType": {"attributes": {"term": "Application", "label": "Application"}}, "im:voteCount": {"label": "0"}}

    app_entry = {"im:name": {"label": "GRE Prep App"}, "im:artist": {"label": "Some Studio"}, "id": {"label": "https://apps.apple.com/in/app/id123456"}}
    page1 = {"feed": {"entry": [app_entry, review(9001, "Waste of money", "Paid 999 and the app crashes on every quant set.", 1, "2025-05-06T10:00:00-07:00"),
                                review(9002, "Decent", "Verbal section is good, quant explanations are thin.", 3, "2025-04-01T00:30:00-07:00")]}}
    page2 = {"feed": {"entry": review(9003, "Old review", "It was fine back then.", 4, "2023-01-01T10:00:00-07:00")}}
    router = Router()
    router.add(lambda u, p: "page=1/" in u, _json(page1))
    router.add(lambda u, p: "page=2/" in u, _json(page2))
    _online(monkeypatch, router)
    s = sources.fetch_apple(run, ROOM, "id123456", country="IN")
    assert s["records_new"] == 2 and s["dropped_old"] == 1 and s["pages"] == 2 and s["seen"] == 3
    assert router.api_calls()[0]["url"] == "https://itunes.apple.com/in/rss/customerreviews/page=1/id=123456/sortby=mostrecent/json"
    assert len(router.api_calls()) == 2  # page 3 was never asked for
    recs = records.load_records(run, ROOM)
    assert all(r["url"] == "https://apps.apple.com/in/app/id123456?see-all=reviews" for r in recs)
    one = {r["meta"]["review_id"]: r for r in recs}["9001"]
    assert one["text"] == "Waste of money\n\nPaid 999 and the app crashes on every quant set." and one["date"] == "2025-05-06"
    assert one["meta"]["rating"] == 1 and one["meta"]["version"] == "4.2" and one["meta"]["kind"] == "review" and one["meta"]["country"] == "in"
    _assert_no_author_fields(_raw(run, "apple"))
    with pytest.raises(common.ValidationErrors):
        sources.fetch_apple(run, ROOM, "not-a-number")


# --------------------------------------------------------------------------- Discourse
def _discourse_router():
    def post(pid, number, cooked, created, post_type=1, name="Zubin Mistry"):
        return {"id": pid, "name": name, "username": "zubin", "avatar_template": "/user_avatar/forum.test/zubin/{size}/1_2.png",
                "created_at": created, "cooked": cooked, "post_number": number, "post_type": post_type, "topic_id": 55,
                "user_id": 12, "reads": 3, "score": 1.5}

    search = {"posts": [{"id": 900, "name": "Zubin Mistry", "username": "zubin", "avatar_template": "/x/{size}.png",
                         "blurb": "Paid 20k, no result.", "topic_id": 55, "post_number": 1, "created_at": "2025-03-01T10:00:00.000Z"}],
              "topics": [{"id": 55, "title": "GRE coaching worth it?", "slug": "gre-coaching-worth-it", "posts_count": 4}],
              "users": [{"id": 12, "username": "zubin", "name": "Zubin Mistry", "avatar_template": "/x/{size}.png"}],
              "grouped_search_result": {"more_full_page_results": None, "term": "GRE coaching after:2024-09-26"}}
    topic55 = {"id": 55, "title": "GRE coaching worth it?", "slug": "gre-coaching-worth-it", "posts_count": 4,
               "details": {"created_by": {"username": "zubin", "name": "Zubin Mistry"}},
               "post_stream": {"posts": [post(900, 1, "<p>Paid 20k, no result. I am Zubin Mistry.</p>", "2025-03-01T10:00:00.000Z"),
                                         post(901, 2, "<p>Same here.</p><p>Refund refused.</p>", "2025-03-02T10:00:00.000Z", name="Ann Lee"),
                                         post(902, 3, "<p>joined the topic</p>", "2025-03-03T10:00:00.000Z", post_type=3)],
                               "stream": [900, 901, 902, 903]}}
    more = {"post_stream": {"posts": [post(903, 4, "<p>Very old post.</p>", "2023-05-01T10:00:00.000Z")]}}
    topic56 = {"id": 56, "title": "Refund from Jamboree", "slug": "refund-from-jamboree",
               "post_stream": {"posts": [post(950, 1, "<p>Took four months to get the refund.</p>", "2025-06-01T10:00:00.000Z")], "stream": [950]}}
    r = Router()
    r.add(lambda u, p: u == "https://forum.test/search.json", _json(search))
    r.add(lambda u, p: u == "https://forum.test/t/55.json", _json(topic55))
    r.add(lambda u, p: u.startswith("https://forum.test/t/55/posts.json?post_ids[]=903"), _json(more))
    r.add(lambda u, p: u == "https://forum.test/t/56.json", _json(topic56))
    r.add(lambda u, p: u == "https://closed.test/robots.txt", FakeResponse(200, "User-agent: *\nDisallow: /search\nDisallow: /u/\n"))
    r.add(lambda u, p: u == "https://closed.test/t/7.json", _json(topic56))
    return r


def test_discourse_needs_domain_decision_then_honours_robots(froot, run, monkeypatch, cli):
    write_sources_md(froot)
    router = _discourse_router()
    _online(monkeypatch, router)
    with pytest.raises(sources.SourceNotAllowed) as e:
        sources.fetch_discourse(run, ROOM, "https://forum.test", query="GRE coaching")
    assert "no decision-log line for the domain forum.test" in str(e.value) and router.calls == []
    write_sources_md(froot, decisions=["- 2026-09-20 | forum.test | allowed | terms allow reading public posts | https://forum.test/tos",
                                       "- 2026-09-20 | closed.test | allowed | terms allow reading | https://closed.test/tos"])
    # robots.txt on closed.test forbids /search: the search is refused (exit 1) and logged as skipped
    with pytest.raises(common.ValidationErrors) as e:
        sources.fetch_discourse(run, ROOM, "closed.test", query="GRE")
    assert "robots.txt on closed.test does not allow" in str(e.value) and e.value.code == 1
    assert any(ev["kind"] == "skip" and ev["domain"] == "closed.test" for ev in _events(run))
    # but a topic given by URL on that forum is allowed by robots.txt
    s = sources.fetch_discourse(run, ROOM, "https://closed.test/", topics=["https://closed.test/t/refund/7"])
    assert s["records_new"] == 1 and s["topics"] == 1

    s = sources.fetch_discourse(run, ROOM, "https://forum.test", query="GRE coaching", topics=["https://forum.test/t/refund-from-jamboree/56/1"])
    assert s["records_new"] == 3 and s["topics"] == 2 and s["dropped_old"] == 1 and s["search_pages"] == 1
    search_call = [c for c in router.api_calls() if c["url"] == "https://forum.test/search.json"][0]
    assert search_call["params"] == {"q": "GRE coaching after:2024-09-26", "page": 1}
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    first = recs["https://forum.test/t/gre-coaching-worth-it/55/1"]
    assert first["text"] == "GRE coaching worth it?\n\nPaid 20k, no result. I am [name]." and first["date"] == "2025-03-01"
    assert first["meta"]["kind"] == "post" and first["meta"]["forum"] == "forum.test" and first["meta"]["topic_id"] == 55
    assert recs["https://forum.test/t/gre-coaching-worth-it/55/2"]["text"] == "Same here.\nRefund refused."
    assert "https://forum.test/t/gre-coaching-worth-it/55/3" not in recs  # a small action, not a post
    assert recs["https://forum.test/t/refund-from-jamboree/56/1"]["text"].startswith("Refund from Jamboree\n\n")
    _assert_no_author_fields(_raw(run, "discourse"))
    with pytest.raises(common.ValidationErrors):
        sources.fetch_discourse(run, ROOM, "https://forum.test")


# --------------------------------------------------------------------------- web
def test_web_page_record_cap_and_content_type(froot, run, monkeypatch):
    write_sources_md(froot)
    body = "<p>" + "GRE coaching fees are rising every year. " * 700 + "</p>"
    html = ('<html><head><title>Fees 2025</title><meta property="article:published_time" content="2025-05-06T10:00:00Z">'
            '<script>var x=1;</script></head><body><h1>Coaching fees</h1>' + body + "</body></html>")
    router = Router()
    router.add(lambda u, p: u == "https://blog.test/fees", FakeResponse(200, html, {"Content-Type": "text/html; charset=utf-8"}))
    router.add(lambda u, p: u == "https://blog.test/brochure.pdf", FakeResponse(200, "%PDF-1.4 binary", {"Content-Type": "application/pdf"}))
    router.add(lambda u, p: u == "https://blog.test/notes.txt", FakeResponse(200, "plain notes about fees\nline two", {"Content-Type": "text/plain"}))
    _online(monkeypatch, router)
    with pytest.raises(sources.SourceNotAllowed):
        sources.fetch_web(run, ROOM, ["https://blog.test/fees"])
    assert router.calls == []
    write_sources_md(froot, decisions=["- 2026-09-25 | blog.test | allowed-with-limits | one page a second | https://blog.test/terms"])
    s = sources.fetch_web(run, ROOM, ["https://blog.test/fees", "https://blog.test/notes.txt"])
    assert s["records_new"] == 2 and s["truncated"] == 1 and s["pages"] == ["https://blog.test/fees", "https://blog.test/notes.txt"]
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    page = recs["https://blog.test/fees"]
    assert len(page["text"]) == sources.WEB_TEXT_CAP and page["text"].startswith("Fees 2025\nCoaching fees\nGRE coaching fees")
    assert "var x" not in page["text"] and page["date"] == "2025-05-06" and page["meta"]["date_from"] == "page"
    assert page["meta"]["truncated"] is True and page["meta"]["chars"] > sources.WEB_TEXT_CAP and page["meta"]["kind"] == "page"
    assert recs["https://blog.test/notes.txt"]["text"] == "plain notes about fees\nline two" and recs["https://blog.test/notes.txt"]["date"] is None
    with pytest.raises(common.ValidationErrors) as e:
        sources.fetch_web(run, ROOM, ["https://blog.test/brochure.pdf"])
    assert "not a text or HTML page" in str(e.value)
    with pytest.raises(common.ValidationErrors):
        sources.fetch_web(run, ROOM, ["ftp://blog.test/x"])


# --------------------------------------------------------------------------- blocked network
def test_network_blocked_exits_3_naming_the_domain(froot, run, cli):
    write_sources_md(froot)
    with pytest.raises(netfetch.NetworkBlocked) as e:
        sources.fetch_hackernews(run, ROOM, "GRE coaching")
    assert e.value.domain == "hn.algolia.com" and e.value.code == 3
    assert any(ev["kind"] == "blocked" and ev["domain"] == "hn.algolia.com" and ev["source"] == "hackernews" for ev in _events(run))
    r = cli("fetch", "hackernews", "--room", ROOM, "--query", "GRE coaching", "--run", RUN)
    assert r.returncode == 3, r.stderr
    assert "Blocked" in r.stderr and "hn.algolia.com" in r.stderr
    r = cli("fetch", "apple", "--room", ROOM, "--app", "123", "--country", "in", "--run", RUN)
    assert r.returncode == 3 and "itunes.apple.com" in r.stderr
    monkey_free = cli("fetch", "web", "--room", ROOM, "--url", "https://blog.test/x", "--run", RUN)
    assert monkey_free.returncode == 1 and "no decision-log line for the domain blog.test" in monkey_free.stderr


def test_partial_results_are_kept_when_a_later_page_is_blocked(froot, run, monkeypatch):
    write_sources_md(froot)
    import requests

    def fake_get(url, params=None, headers=None, timeout=30):
        if params.get("page") == 0:
            return _json({"hits": [{"objectID": "1", "title": "Ask HN: GRE coaching fees", "story_text": "", "created_at_i": NEW_EPOCH, "_tags": ["story"]}],
                          "nbPages": 3, "page": 0})
        raise requests.exceptions.ProxyError("Tunnel connection failed: 403 Forbidden")

    monkeypatch.setenv("FUNNEL_OFFLINE", "0")
    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    with pytest.raises(netfetch.NetworkBlocked):
        sources.fetch_hackernews(run, ROOM, "GRE coaching")
    assert len(records.load_records(run, ROOM)) == 1
    notes = [ev for ev in _events(run) if ev["kind"] == "note" and "before the source failed" in ev.get("note", "")]
    assert len(notes) == 1


# --------------------------------------------------------------------------- Discourse quote headers (rule 5)
QUOTED_COOKED = ('<aside class="quote no-group" data-username="priya_s" data-post="3" data-topic="55">'
                 '<div class="title"><div class="quote-controls"></div><img class="avatar" src="/u/a.png"> priya_s:</div>'
                 '<blockquote><p>I paid 40k and still scored 300</p></blockquote></aside>'
                 '<p>Same here, <a class="mention" href="/u/rahul_v">@rahul_v</a> told me the same.</p>')


def test_discourse_quote_headers_never_keep_the_quoted_username(froot, run, monkeypatch):
    html, users = sources.strip_quote_headers(QUOTED_COOKED)
    assert users == ["priya_s"] and "priya_s" not in html and '<div class="title">[user]:</div>' in html
    text = anonymize(netfetch.html_to_text(html), known_names=users)
    assert text == "[user]:\nI paid 40k and still scored 300\nSame here, [user] told me the same."
    assert sources.strip_quote_headers(None) == ("", []) and sources.strip_quote_headers("<p>plain</p>") == ("<p>plain</p>", [])
    # through the adapter: the quoted member's username reaches neither the text nor the meta
    write_sources_md(froot, decisions=["- 2026-09-20 | forum.test | allowed | terms allow reading public posts | https://forum.test/tos"])
    topic = {"id": 77, "title": "Quoted reply", "slug": "quoted-reply",
             "post_stream": {"posts": [
                 {"id": 970, "name": "Ann Lee", "username": "ann_lee", "created_at": "2025-04-01T10:00:00.000Z", "cooked": QUOTED_COOKED,
                  "post_number": 1, "post_type": 1, "topic_id": 77, "user_id": 3},
                 {"id": 971, "name": "Priya S", "username": "priya_s", "created_at": "2025-04-02T10:00:00.000Z",
                  "cooked": "<p>priya_s here again, I got a refund.</p>", "post_number": 2, "post_type": 1, "topic_id": 77, "user_id": 4}],
                 "stream": [970, 971]}}
    router = Router().add(lambda u, p: u == "https://forum.test/t/77.json", _json(topic))
    _online(monkeypatch, router)
    s = sources.fetch_discourse(run, ROOM, "https://forum.test", topics=["https://forum.test/t/quoted-reply/77"])
    assert s["records_new"] == 2
    recs = {r["url"]: r for r in records.load_records(run, ROOM)}
    assert recs["https://forum.test/t/quoted-reply/77/1"]["text"] == \
        "Quoted reply\n\n[user]:\nI paid 40k and still scored 300\nSame here, [user] told me the same."
    assert recs["https://forum.test/t/quoted-reply/77/2"]["text"] == "[name] here again, I got a refund."
    raw = _raw(run, "discourse")
    for needle in ("priya_s", "rahul_v", "Priya S", "Ann Lee", "ann_lee", "data-username"):
        assert needle not in raw, needle
    _assert_no_author_fields(raw)
