# Ontology Insight Generator

This folder holds two things:

- **The ontology** (`data/`, `ATLAS/`) records what the Vedic and ascetic traditions of India teach, in their own
  terms. Every entry carries a verification level: skeleton, sourced or text-verified.
- **The Insight Generator** (`insight/`, `web/`) is a small product built on that ontology. It has two engines:
  - **Person map.** A person answers up to 15 plain questions, writes freely or pastes a dialogue. The reading:
    - finds the patterns the traditional texts describe, in the person's own words;
    - reads them through two lenses, Vedic/yogic and ascetic (Buddhist and Jain);
    - shows how the two readings fit together and where they differ (the one-truth principle);
    - suggests a short pathway of gentle practices, taken only from the texts, with the texts' own warnings.
  - **Content engine.** It drafts posts for five audience buckets, each joining an everyday scene to one cited teaching.
    Every draft goes to a human review queue. The app never posts anything.

What it never does:
- diagnose, treat, cure or make health claims;
- predict, or use astrology or kundali;
- use modern psychology or research;
- show unchecked (skeleton) entries;
- recommend a restricted practice;
- give a reading to anyone under 18 or without consent.

See SAFETY.md and PRIVACY.md.

## Quick start
```bash
cd tradition-ontology
python3 -m pip install -r requirements.txt           # Python 3.11+
python3 -m pytest -q                                 # all tests are offline (model calls are mocked)
python3 -m uvicorn insight.api:app --port 8000       # web app: http://127.0.0.1:8000
python3 -m insight.cli questions                     # the CLI mirrors the web app
```
**Engines.**
- `ONTO_ENGINE=rules` is deterministic and offline, and needs no key.
- `ONTO_ENGINE=model` uses the Claude API and needs `ANTHROPIC_API_KEY`.
- `auto` (the default) uses the model engine when a key is set. With no key it **refuses person readings and
  check-ins** (503), because the rules screen alone misses indirect crisis wording. Set `ONTO_ALLOW_RULES_ONLY=1`
  (development, evaluation) or `ONTO_ENGINE=rules` to allow rule-only readings; never on a public deployment.
- The public page offers no engine choice, and a caller can never step down from the model engine to rules (403).

**Other settings:** see RUNBOOK.md.

## Layout
| Path | What it is |
|---|---|
| `ENGINE_SPEC.md` | The design contract: pipeline, engines, safety, mapping, synthesis, pathway, report object, content engine |
| `insight/` | The app: `engine.py` (pipeline), `safety.py`, `mapper.py`, `synthesizer.py`, `pathway.py`, `report.py`, `content.py`, `store.py` (encrypted SQLite), `service.py` (the one service layer), `api.py` (FastAPI), `cli.py`, `llm.py` (Claude API client and cost ledger), `gates.py` (automated gate checks) |
| `web/` | The single-page UI: plain HTML, CSS and JS, no external resources |
| `rules/` | Product rules: safety, consent, intake, mapping, specificity, forbidden claims, tone, synthesis, content buckets, voices, formats |
| `layers/` | Product layers over the ontology: `diagnosis.json`, `practices.json`, `tables/` (obstacle correspondence, one-truth, path maps). The app only reads them |
| `config/model_routing.json` | Model and effort per step. `config/pricing.json` holds token prices |
| `eval/` | Synthetic evaluation sets and results. Builders never read the sets |
| `tests/` | The test suite (offline) |
| `RELEASE_REPORT.md` | Every release gate: pass, fail or not run, with evidence |

## Status
RELEASE_REPORT.md has the release status. Without an API key the live-model gates are **not run**, so the product is
**not ready** for release, even where every offline gate passes.
