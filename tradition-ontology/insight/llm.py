"""Model access for the runtime steps in config/model_routing.json.

- The client never inherits the Claude Code harness's ANTHROPIC_BASE_URL: the base URL comes from
  ONTO_ANTHROPIC_BASE_URL (default https://api.anthropic.com), the key from ANTHROPIC_API_KEY.
- Every call asks for JSON against a schema (structured outputs) and records tokens and cost.
- User text is always passed as data inside <user_input> tags, never as instructions.
- A refusal or an error never becomes content: callers get an LLMError and fall back safely.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from . import config


class LLMError(Exception):
    """Model step failed (no key, refusal, network, invalid output). Callers must fail safe."""

    def __init__(self, step: str, kind: str, detail: str = ""):
        super().__init__(f"{step}: {kind} {detail}".strip())
        self.step, self.kind, self.detail = step, kind, detail


@dataclass
class Usage:
    step: str
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    seconds: float = 0.0

    @property
    def cost_usd(self) -> float:
        p = config.pricing().get(self.model) or {}
        return round((self.input_tokens * p.get("input", 0) + self.output_tokens * p.get("output", 0)
                      + self.cache_read_tokens * p.get("cache_read", 0)
                      + self.cache_write_tokens * p.get("cache_write_5m", 0)) / 1e6, 6)

    def as_dict(self) -> dict:
        d = dict(self.__dict__)
        d["cost_usd"] = self.cost_usd
        return d


@dataclass
class CallResult:
    data: Any
    usage: Usage
    served_by: str = ""


@dataclass
class Ledger:
    """Collects usage for one person map or one batch of posts (no personal data, only counts)."""
    items: list = field(default_factory=list)

    def add(self, u: Usage) -> None:
        self.items.append(u)

    def totals(self) -> dict:
        t = {"calls": len(self.items), "input_tokens": 0, "output_tokens": 0, "cache_read_tokens": 0,
             "cache_write_tokens": 0, "cost_usd": 0.0, "by_step": {}}
        for u in self.items:
            for k in ("input_tokens", "output_tokens", "cache_read_tokens", "cache_write_tokens"):
                t[k] += getattr(u, k)
            t["cost_usd"] = round(t["cost_usd"] + u.cost_usd, 6)
            s = t["by_step"].setdefault(u.step, {"calls": 0, "cost_usd": 0.0, "model": u.model})
            s["calls"] += 1
            s["cost_usd"] = round(s["cost_usd"] + u.cost_usd, 6)
        return t


def wrap_user_text(text: str) -> str:
    """User content is data. Neutralise tag look-alikes so it cannot close the wrapper."""
    safe = text.replace("<", "‹").replace(">", "›")
    return f"<user_input>\n{safe}\n</user_input>"


class ModelClient:
    """Thin wrapper over the Anthropic SDK. `transport` can be injected (tests) to avoid network calls."""

    def __init__(self, transport: Optional[Callable[..., Any]] = None, premium: bool = False):
        self.cfg = config.routing()
        self.premium = premium
        self._transport = transport
        self._client = None

    def available(self) -> bool:
        return self._transport is not None or bool(os.environ.get(self.cfg["api_key_env"]))

    def _sdk(self):
        if self._client is None:
            key = os.environ.get(self.cfg["api_key_env"])
            if not key:
                raise LLMError("client", "no-api-key", f"set {self.cfg['api_key_env']} in the environment or .env")
            import anthropic  # imported lazily so the rules engine works without the SDK
            self._client = anthropic.Anthropic(
                api_key=key,
                base_url=os.environ.get(self.cfg["base_url_env"], self.cfg["default_base_url"]),
                timeout=float(self.cfg.get("timeout_seconds", 90)),
                max_retries=int(self.cfg.get("max_retries", 3)),
            )
        return self._client

    def call_json(self, step: str, system: str, user: str, schema: dict, ledger: Optional[Ledger] = None) -> CallResult:
        sc = self.cfg["steps"][step]
        effort = sc.get("premium_effort") if (self.premium and sc.get("premium_effort")) else sc["effort"]
        kwargs = dict(
            model=sc["model"], max_tokens=int(sc.get("max_tokens", 4000)), system=system,
            messages=[{"role": "user", "content": user}],
            output_config={"effort": effort, "format": {"type": "json_schema", "schema": schema}},
        )
        fb = self.cfg.get("fallbacks") or {}
        t0 = time.time()
        try:
            if self._transport is not None:
                resp = self._transport(step=step, **kwargs)
            else:
                client = self._sdk()
                if fb.get("enabled"):
                    resp = client.beta.messages.create(betas=[fb["beta"]], fallbacks=fb.get("mode", "default"), **kwargs)
                else:
                    resp = client.messages.create(**kwargs)
        except LLMError:
            raise
        except Exception as e:  # SDK already retried with backoff; surface a typed, non-personal error
            raise LLMError(step, "api-error", type(e).__name__) from None
        u = getattr(resp, "usage", None)
        usage = Usage(step=step, model=getattr(resp, "model", sc["model"]) or sc["model"],
                      input_tokens=int(getattr(u, "input_tokens", 0) or 0),
                      output_tokens=int(getattr(u, "output_tokens", 0) or 0),
                      cache_read_tokens=int(getattr(u, "cache_read_input_tokens", 0) or 0),
                      cache_write_tokens=int(getattr(u, "cache_creation_input_tokens", 0) or 0),
                      seconds=round(time.time() - t0, 2))
        if ledger is not None:
            ledger.add(usage)
        if getattr(resp, "stop_reason", None) == "refusal":
            raise LLMError(step, "refusal")
        if getattr(resp, "stop_reason", None) == "max_tokens":
            raise LLMError(step, "truncated")
        text = next((b.text for b in resp.content if getattr(b, "type", "") == "text"), None)
        if text is None:
            raise LLMError(step, "no-text")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            raise LLMError(step, "invalid-json") from None
        return CallResult(data=data, usage=usage, served_by=usage.model)
