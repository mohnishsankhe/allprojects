"""The report object's schema (ENGINE_SPEC.md §12), as pydantic models.

validate_report(r) raises pydantic.ValidationError if a report is malformed. Extra keys are allowed on the inner
records (audit fields), but every field the renderer or the gates rely on must be present and well-typed.
"""
from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Confidence = Literal["low", "moderate", "high"]


class _M(BaseModel):
    model_config = ConfigDict(extra="allow")


class Evidence(_M):
    qid: str
    quote: str = Field(min_length=1)
    unit: str
    strength: Literal["direct", "indirect", "suggestive"]


class Mapping(_M):
    dx_id: str
    name: str
    kind: str
    lens: Literal["vedic-yogic", "ascetic-buddhist", "ascetic-jain"]
    lens_label: str
    confidence: Confidence
    evidence: list[Evidence] = Field(min_length=1)
    why: str
    cites: list[str] = Field(min_length=1)
    state: Optional[dict] = None


class Point(_M):
    text: str = Field(min_length=1)
    cites: list[str] = Field(min_length=1)
    evidence_refs: list[str] = Field(min_length=1)


class RecPoint(Point):
    basis: Literal["level", "standpoint", "path", "stage"]


class Lens(_M):
    points: list[Point] = []
    note: Optional[str] = None


class Reconciliation(_M):
    points: list[RecPoint] = []
    differences: list[Point] = []


class Warning_(_M):
    text: str
    cites: list[str] = Field(min_length=1)


class PathwayPractice(_M):
    px_id: str
    name: str
    lens: Optional[str] = None
    why: str
    steps: list[str] = Field(min_length=1)
    duration: dict
    warnings: list[Warning_] = Field(min_length=1)
    cites: list[str] = Field(min_length=1)


class Day(_M):
    day: int = Field(ge=1, le=14)
    plan: str


class Pathway(_M):
    practices: list[PathwayPractice] = Field(max_length=4)
    sequence: list[Day] = []
    checkin_prompt: str
    tier_rule: str


class Citation(_M):
    id: str
    title: str
    ref: Optional[str] = None
    original: Optional[str] = None
    paraphrase: str = ""
    level: Literal["sourced", "text-verified"]


class Safety(_M):
    route: str
    categories: list[str] = []
    model_checked: bool = False
    injection: bool = False


class Report(_M):
    engine: str
    created: float
    safety: Safety
    notices: list[str] = []
    stopped: Optional[dict] = None
    insufficient: Optional[str] = None
    summary: Optional[str] = None
    mappings: list[Mapping] = []
    groups: list[dict] = []
    lenses: dict[Literal["vedic", "ascetic"], Lens] = {}
    reconciliation: Reconciliation = Reconciliation()
    pathway: Optional[Pathway] = None
    citations: dict[str, Citation] = {}
    claim_hits: list[dict] = []
    cost: dict = {}


def validate_report(r: dict) -> Report:
    rep = Report.model_validate(r)
    # cross-field rules the models cannot express
    if rep.stopped is None and rep.insufficient is None and rep.mappings:
        quotes = {e.qid for m in rep.mappings for e in m.evidence}
        for lens in rep.lenses.values():
            for p in lens.points:
                if not set(p.evidence_refs) <= quotes:
                    raise ValueError(f"lens point refers to an unknown quote: {p.evidence_refs}")
        for p in rep.reconciliation.points + rep.reconciliation.differences:
            if not set(p.evidence_refs) <= quotes:
                raise ValueError(f"reconciliation point refers to an unknown quote: {p.evidence_refs}")
        shown = set()
        for m in rep.mappings:
            shown |= set(m.cites)
        for c in shown:
            if c not in rep.citations:
                raise ValueError(f"cited id not resolved in citations: {c}")
    return rep
