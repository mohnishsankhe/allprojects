"""Shared test helpers. Every test runs with its own temporary ONTO_DATA_DIR and no network: model calls are faked."""
import json
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _env(tmp_path, monkeypatch):
    monkeypatch.setenv("ONTO_DATA_DIR", str(tmp_path / "data"))
    monkeypatch.delenv("ONTO_DATA_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.delenv("ONTO_ADMIN_TOKEN", raising=False)
    monkeypatch.setenv("ONTO_ENGINE", "rules")
    yield


def fake_response(data=None, stop_reason="end_turn", text=None, tokens=(100, 50)):
    body = text if text is not None else json.dumps(data)
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=body)], stop_reason=stop_reason, model="fake",
        usage=SimpleNamespace(input_tokens=tokens[0], output_tokens=tokens[1],
                              cache_read_input_tokens=0, cache_creation_input_tokens=0))


class FakeTransport:
    """transport(step=..., **kwargs). handlers: step -> dict (JSON to return), callable(kwargs) -> dict,
    an Exception instance (raised), or the string 'refusal'. Steps with no handler raise (a model failure)."""

    def __init__(self, handlers=None):
        self.handlers = dict(handlers or {})
        self.calls = []

    def __call__(self, step, **kwargs):
        self.calls.append((step, kwargs))
        h = self.handlers.get(step)
        if h is None:
            raise RuntimeError("no handler for " + step)
        if callable(h):
            h = h(kwargs)
        if isinstance(h, Exception):
            raise h
        if h == "refusal":
            return fake_response({}, stop_reason="refusal")
        return fake_response(h)


NO_FLAGS = {"flags": [], "injection_attempt": False, "asks_for_diagnosis_or_prediction": False}


def client_with(handlers):
    from insight.llm import ModelClient
    t = FakeTransport(handlers)
    return ModelClient(transport=t), t


QUOTE = "I remember how good it felt and I want it again, and I need whatever gets me that feeling"
BENIGN = ("Every night I scroll for hours and I keep wanting to go back to that feeling. " + QUOTE +
          ". As soon as one want is met, another takes its place. It happens most nights this month.")


def fake_map_person(inputs, scr=None, engine="rules", client=None, ledger=None, layer=None):
    """One valid mapping for dx:klesa-raga, quoting the input exactly (stands in for insight.mapper)."""
    from insight import ontology
    text = " ".join(str(v) for v in (inputs.get("answers") or {}).values()) + " " + (inputs.get("free_text") or "")
    if QUOTE not in text:
        return {"mappings": [], "groups": [], "audit": {"unmapped_reason": None}, "notice": None}
    entry = ontology.diagnosis()["dx:klesa-raga"]
    cites = [c for m in entry["markers"] for c in m["cites"]][:2]
    m = {"dx_id": "dx:klesa-raga", "name": entry["name"], "kind": entry["kind"], "lens": entry["lens"],
         "lens_label": "Vedic/yogic", "group_id": None, "confidence": "low",
         "evidence": [{"qid": "intake:q01#s1:78", "unit": "intake:q01", "quote": QUOTE, "strength": "direct",
                       "specificity": ["F2"], "engines": ["rules"]}],
         "counter_evidence": [], "cites": cites, "state": None,
         "why": f"You wrote “{QUOTE}”; the texts describe this as wanting a pleasure again because it is remembered.",
         "audit": {}}
    return {"mappings": [m], "groups": [], "audit": {"unmapped_reason": None}, "notice": None}


@pytest.fixture
def fake_mapper(monkeypatch):
    from insight import mapper
    monkeypatch.setattr(mapper, "map_person", fake_map_person)
    return fake_map_person


@pytest.fixture
def store():
    from insight.store import Store
    s = Store()
    yield s
    s.db.close()


@pytest.fixture
def svc(store):
    from insight.service import Service
    return Service(store=store)
