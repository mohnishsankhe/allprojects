"""Shared pytest fixtures for the pipeline tests.

Fixtures
--------
    froot   a temporary funnel root: a copy of the REAL config/ (ledger.md, ledger.yaml, ...),
            an empty graveyard.md and PROGRESS.md, empty runs/, cache/ and inbox/.
            FUNNEL_ROOT_OVERRIDE points at it, FUNNEL_TODAY is 2026-09-26, the pipeline modules
            are reloaded. Returns the root Path.
    run     froot/runs/2026-09-26 with fx_rates.json (INR 88.0, AED 3.6725, SGD 1.29, GBP 0.75, EUR 0.86).
    cli     cli(*args) runs `python3 pipeline/funnel.py <args>` in a subprocess with the override
            environment and returns the CompletedProcess (stdout, stderr, returncode).
    h       helper functions: h.make_record(...), h.store(...), h.label(...), h.write_labels(...),
            h.set_rule(...), h.read(...).
    (autouse) FUNNEL_OFFLINE=1 and every real HTTP path patched to fail loudly.

Modules under pipeline/ are importable directly (`import common`).
"""
from __future__ import annotations

import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REAL_ROOT = Path(__file__).resolve().parent.parent
PIPELINE = REAL_ROOT / "pipeline"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
TRANSCRIPTS = FIXTURES / "transcripts"
RUN_NAME = "2026-09-26"
FX_RATES = {"INR": 88.0, "AED": 3.6725, "SGD": 1.29, "GBP": 0.75, "EUR": 0.86}

if str(PIPELINE) not in sys.path:
    sys.path.insert(0, str(PIPELINE))


def reload_pipeline() -> None:
    """Reload every loaded pipeline module, common first, so FUNNEL_ROOT follows the environment."""
    names = ["common"] + sorted(
        n for n, m in list(sys.modules.items())
        if n != "common" and getattr(m, "__file__", None) and str(Path(m.__file__).resolve().parent) == str(PIPELINE)
    )
    for name in names:
        mod = sys.modules.get(name)
        if mod is not None:
            importlib.reload(mod)


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    """Offline for every test; any real HTTP attempt fails loudly."""
    monkeypatch.setenv("FUNNEL_OFFLINE", "1")

    def boom(*args, **kwargs):
        raise AssertionError(f"A test tried to use the real network: {args[:2]!r}")

    monkeypatch.setattr("requests.Session.request", boom)
    monkeypatch.setattr("requests.adapters.HTTPAdapter.send", boom)
    monkeypatch.setattr("urllib.request.urlopen", boom)
    monkeypatch.setattr("http.client.HTTPConnection.connect", boom)
    yield


@pytest.fixture
def froot(tmp_path, monkeypatch):
    root = tmp_path / "funnel"
    shutil.copytree(REAL_ROOT / "config", root / "config")
    (root / "graveyard.md").write_text(
        "# Graveyard\n\nEverything the funnel killed, one line each: `- date | stage | item | reason`.\n",
        encoding="utf-8",
    )
    (root / "PROGRESS.md").write_text(
        "# Progress\n\n<!-- auto:status -->\n<!-- /auto:status -->\n\n## Done\n\n## Next\n", encoding="utf-8"
    )
    for d in ("runs", "cache", "inbox/closed_groups", "inbox/customers", "inbox/audit_results"):
        (root / d).mkdir(parents=True)
    monkeypatch.setenv("FUNNEL_ROOT_OVERRIDE", str(root))
    monkeypatch.setenv("FUNNEL_TODAY", RUN_NAME)
    monkeypatch.setenv("FUNNEL_TRANSCRIPTS_DIR", str(TRANSCRIPTS))
    monkeypatch.setenv("FUNNEL_MIN_INTERVAL", "0")
    monkeypatch.setenv("FUNNEL_RETRY_BASE_SECONDS", "0")
    monkeypatch.delenv("FUNNEL_DRY_RUN", raising=False)
    reload_pipeline()
    yield root
    monkeypatch.delenv("FUNNEL_ROOT_OVERRIDE", raising=False)
    reload_pipeline()


@pytest.fixture
def run(froot):
    import common

    rd = froot / "runs" / RUN_NAME
    rd.mkdir(parents=True, exist_ok=True)
    rates = {
        code: {"per_usd": v, "url": "https://example.test/fx", "seen_via": "search",
               "reasoning": "test rate", "confidence": "moderate"}
        for code, v in FX_RATES.items()
    }
    common.write_json(rd / "fx_rates.json", {"base": "USD", "as_of": RUN_NAME, "rates": rates})
    return rd


@pytest.fixture
def cli(froot, tmp_path):
    def _cli(*args, env=None, cwd=None):
        e = dict(os.environ)
        e.update(env or {})
        cmd = [sys.executable, str(PIPELINE / "funnel.py"), *[str(a) for a in args]]
        return subprocess.run(cmd, capture_output=True, text=True, env=e, cwd=str(cwd or tmp_path))

    return _cli


class Helpers:
    """Small builders shared by the test files."""

    @staticmethod
    def make_record(url, text, date=None, round=1, qi=1, rank=1, kind="forum", query="q"):
        return {
            "url": url, "text": text, "date": date,
            "meta": {"kind": "search_title", "query": query, "query_kind": kind, "round": round,
                     "order": [round, qi, rank], "domain": url.split("/")[2] if "//" in url else "",
                     "date_from": "url" if date else "none"},
        }

    @staticmethod
    def store(run, room, recs, source="websearch"):
        import records

        return records.store_records(run, room, source, recs)

    @staticmethod
    def label(rid, voice="member", keys=(), money=False, failed=False, reasoning="test label", confidence="high"):
        return {"record_id": rid, "voice": voice, "pain_keys": list(keys), "money": money,
                "failed_spend": failed, "reasoning": reasoning, "confidence": confidence}

    @staticmethod
    def write_labels(run, room, batch_name, rows):
        import common

        common.write_jsonl(common.room_dir(run, room) / "labels" / f"{batch_name}.jsonl", rows)

    @staticmethod
    def write_taxonomy(run, room, keys):
        import common

        common.write_json(common.room_dir(run, room) / "taxonomy.json",
                          {"pains": [{"key": k, "label": k, "definition": k, "added_round": 1} for k in keys]})

    @staticmethod
    def set_rule(froot, stage, key, value):
        p = froot / "config" / "kill_rules.yaml"
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        data[stage][key] = value
        p.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True), encoding="utf-8")

    @staticmethod
    def read(path):
        return Path(path).read_text(encoding="utf-8")


@pytest.fixture
def h():
    return Helpers
