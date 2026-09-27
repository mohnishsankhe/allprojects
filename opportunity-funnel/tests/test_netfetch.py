import json
import os

import pytest
import requests

import common
import netfetch


class FakeResponse:
    def __init__(self, status=200, text="", headers=None):
        self.status_code = status
        self.text = text
        self.headers = headers or {}


def _online(monkeypatch):
    monkeypatch.setenv("FUNNEL_OFFLINE", "0")
    monkeypatch.setenv("FUNNEL_MIN_INTERVAL", "0")
    monkeypatch.setenv("FUNNEL_RETRY_BASE_SECONDS", "0")


def test_offline_raises_before_any_request(froot, monkeypatch):
    calls = []
    monkeypatch.setattr(netfetch, "_http_get", lambda *a, **k: calls.append(a) or FakeResponse())
    assert netfetch.offline() is True
    with pytest.raises(netfetch.NetworkBlocked) as e:
        netfetch.fetch("https://api.stackexchange.com/2.3/questions?key=SECRET")
    assert e.value.domain == "api.stackexchange.com"
    assert "api.stackexchange.com" in str(e.value)
    assert "SECRET" not in str(e.value)
    assert isinstance(e.value, common.Blocked) and e.value.code == 3
    with pytest.raises(netfetch.NetworkBlocked):
        netfetch.robots_allowed("https://example.org/page")
    assert netfetch.probe("example.org")["status"] == "blocked_by_network"
    assert calls == []


def test_blocked_exit_code_and_message(froot, capsys):
    with pytest.raises(SystemExit) as e:
        common.fail(netfetch.NetworkBlocked("hn.algolia.com"))
    assert e.value.code == 3
    err = capsys.readouterr().err
    assert "1. Network blocked: cannot reach hn.algolia.com." in err


def test_strip_key_params_and_cache_key():
    url = "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&key=SECRET&videoId=abc&access_token=T&token=x&api_key=y&client_secret=z"
    stripped = netfetch.strip_key_params(url)
    assert stripped == "https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId=abc"
    assert netfetch.cache_key(url) == netfetch.cache_key(stripped)
    assert netfetch.public_url("https://x.test/a", {"key": "S", "q": "1"}) == "https://x.test/a?q=1"
    assert netfetch.strip_key_params("https://x.test/a") == "https://x.test/a"


def test_fetch_caches_without_secrets(froot, monkeypatch):
    _online(monkeypatch)
    calls = []

    def fake_get(url, params=None, headers=None, timeout=30):
        calls.append((url, params))
        if url.endswith("/robots.txt"):
            return FakeResponse(404, "")
        return FakeResponse(200, "<html><body><p>hello</p></body></html>", {"Content-Type": "text/html"})

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    r1 = netfetch.fetch("https://example.test/page", params={"key": "SECRET", "q": "gre"})
    assert r1["from_cache"] is False and r1["status"] == 200
    assert r1["url"] == "https://example.test/page?q=gre"
    r2 = netfetch.fetch("https://example.test/page", params={"key": "SECRET", "q": "gre"})
    assert r2["from_cache"] is True and r2["text"] == r1["text"]
    assert len([c for c in calls if not c[0].endswith("robots.txt")]) == 1
    cache_files = list((froot / "cache" / "http").glob("*.json"))
    assert len(cache_files) == 1
    stored = json.loads(cache_files[0].read_text(encoding="utf-8"))
    assert "SECRET" not in cache_files[0].read_text(encoding="utf-8")
    assert stored["url"] == "https://example.test/page?q=gre"
    assert (froot / "cache" / "robots" / "example.test.txt").exists()
    # the real request still carried the key
    assert any(c[1] and c[1].get("key") == "SECRET" for c in calls)


def test_proxy_error_and_tunnel_403_become_network_blocked(froot, monkeypatch):
    _online(monkeypatch)

    def proxy_fail(url, params=None, headers=None, timeout=30):
        raise requests.exceptions.ProxyError("Tunnel connection failed: 403 Forbidden")

    monkeypatch.setattr(netfetch, "_http_get", proxy_fail)
    with pytest.raises(netfetch.NetworkBlocked) as e:
        netfetch.fetch("https://hn.algolia.com/api/v1/search", respect_robots=False)
    assert e.value.domain == "hn.algolia.com"
    assert netfetch.probe("hn.algolia.com")["status"] == "blocked_by_network"

    def conn_fail(url, params=None, headers=None, timeout=30):
        raise requests.exceptions.ConnectionError("HTTPSConnectionPool: Tunnel connection failed: 403 Forbidden")

    monkeypatch.setattr(netfetch, "_http_get", conn_fail)
    with pytest.raises(netfetch.NetworkBlocked):
        netfetch.fetch("https://itunes.apple.com/rss", respect_robots=False)


def test_retry_on_429_with_retry_after_and_no_retry_on_403(froot, monkeypatch):
    _online(monkeypatch)
    sleeps = []
    monkeypatch.setattr(netfetch, "_sleep", lambda s: sleeps.append(s))
    answers = [FakeResponse(429, "", {"Retry-After": "7"}), FakeResponse(503, ""), FakeResponse(200, "ok")]
    calls = []

    def fake_get(url, params=None, headers=None, timeout=30):
        calls.append(url)
        return answers.pop(0)

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    r = netfetch.fetch("https://api.example.test/x", respect_robots=False, use_cache=False)
    assert r["text"] == "ok" and len(calls) == 3
    assert sleeps[0] == 7.0

    calls.clear()
    monkeypatch.setattr(netfetch, "_http_get", lambda *a, **k: calls.append(1) or FakeResponse(403, "no"))
    with pytest.raises(netfetch.FetchError) as e:
        netfetch.fetch("https://api.example.test/y", respect_robots=False, use_cache=False)
    assert e.value.status == 403 and len(calls) == 1
    assert not isinstance(e.value, netfetch.NetworkBlocked)


def test_robots_disallow(froot, monkeypatch):
    _online(monkeypatch)

    def fake_get(url, params=None, headers=None, timeout=30):
        if url.endswith("/robots.txt"):
            return FakeResponse(200, "User-agent: *\nDisallow: /private/\n")
        return FakeResponse(200, "page")

    monkeypatch.setattr(netfetch, "_http_get", fake_get)
    assert netfetch.robots_allowed("https://forum.test/public/thread") is True
    assert netfetch.robots_allowed("https://forum.test/private/thread") is False
    with pytest.raises(netfetch.RobotsDisallowed) as e:
        netfetch.fetch("https://forum.test/private/thread")
    assert "forum.test" in str(e.value)
    assert netfetch.fetch("https://forum.test/public/thread")["text"] == "page"


def test_html_to_text_and_dates():
    html = ('<html><head><title>T</title><meta property="article:published_time" content="2025-03-04T10:00:00Z">'
            '<script>var x = 1;</script><style>p{}</style></head>'
            '<body><h1>Head</h1><p>One &amp; two</p><div>three</div></body></html>')
    text = netfetch.html_to_text(html)
    assert "var x" not in text and "p{}" not in text
    assert text.split("\n") == ["T", "Head", "One & two", "three"]
    assert netfetch.extract_date(html) == ("2025-03-04", "page")
    assert netfetch.extract_date("<p>no date</p>", "https://a.test/2024/05/06/post") == ("2024-05-06", "url")
    assert netfetch.extract_date("<p>no date</p>", "https://a.test/post") == (None, "none")


@pytest.mark.parametrize("url,expected", [
    ("https://universe.byu.edu/2002/05/13/experts-say-gre-prep-courses-a-waste", ("2002-05-13", "day")),
    ("https://www.thedp.com/article/2016/04/studyign-for-the-graduate-record-examination", ("2016-04-01", "month")),
    ("https://a.test/blog/2024-09-26-launch", ("2024-09-26", "day")),
    ("https://forums.studentdoctor.net/threads/are-gre-prep-courses-worth-it.968822/", (None, None)),
    ("https://a.test/2023/13/01/bad-month", (None, None)),
    ("https://a.test/2023/02/30/bad-day", (None, None)),
    ("https://a.test/p?d=2024/05/06", (None, None)),
])
def test_date_from_url(url, expected):
    assert netfetch.url_date_info(url) == expected
    assert netfetch.date_from_url(url) == expected[0]


# --------------------------------------------------------------------------- rate limits shared across processes
_RATE_SCRIPT = """
import json, sys
sys.path.insert(0, sys.argv[1])
import netfetch
sleeps = []
netfetch._sleep = lambda s: sleeps.append(s)
if sys.argv[2] == "domain":
    waited = netfetch._rate_limit("api.test")
else:
    waited = netfetch.shared_window_wait("reddit", 2)
print(json.dumps({"waited": waited, "sleeps": sleeps}))
"""


def test_rate_limit_and_reddit_window_are_shared_across_processes(froot, tmp_path):
    """Rule 4: the listeners run one process per room against the same APIs. The per-domain interval and the
    Reddit sliding window live in cache/ratelimit/ under a file lock, so a second process waits for the first."""
    import subprocess
    import sys
    from conftest import PIPELINE

    def run_once(mode, interval="3"):
        env = dict(os.environ, FUNNEL_ROOT_OVERRIDE=str(froot), FUNNEL_MIN_INTERVAL=interval, FUNNEL_OFFLINE="1")
        r = subprocess.run([sys.executable, "-c", _RATE_SCRIPT, str(PIPELINE), mode], capture_output=True, text=True, env=env, cwd=str(tmp_path))
        assert r.returncode == 0, r.stderr
        return json.loads(r.stdout)

    first = run_once("domain")
    second = run_once("domain")
    assert first["waited"] == 0.0 and first["sleeps"] == []
    assert 2.0 < second["waited"] <= 3.0 and second["sleeps"] == [second["waited"]]
    assert (froot / "cache" / "ratelimit" / "domain-api.test.json").exists()
    assert (froot / "cache" / "ratelimit" / "domain-api.test.lock").exists()
    # the Reddit window: 2 a minute for ALL processes together, so the third process waits close to 60 s
    w1, w2, w3 = run_once("window"), run_once("window"), run_once("window")
    assert w1["waited"] == 0.0 and w2["waited"] == 0.0
    assert 55.0 < w3["waited"] <= 60.0 and w3["sleeps"] == [w3["waited"]]
    state = json.loads((froot / "cache" / "ratelimit" / "window-reddit.json").read_text(encoding="utf-8"))
    assert state["per_minute"] == 2 and len(state["times"]) == 2
    # interval 0 (tests) keeps the fast path and never touches the file for a new domain
    assert run_once("domain", interval="0")["waited"] == 0.0
    import sources
    assert sources._REDDIT_GATE.name == "reddit" and sources._REDDIT_GATE.per_minute == 60
