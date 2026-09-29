# Runbook

## Configuration (environment or `.env`; `.env` is git-ignored)
| Variable | Default | Meaning |
|---|---|---|
| `ANTHROPIC_API_KEY` | none | Needed for the model engine. Without it, `auto` refuses person readings and check-ins (503) |
| `ONTO_ANTHROPIC_BASE_URL` | `https://api.anthropic.com` | The API base URL. The app never reads `ANTHROPIC_BASE_URL` |
| `ONTO_ENGINE` | `auto` | `rules`, `model` or `auto`. **Any public deployment must run `model` with a key.** With `auto` and no key, person readings and check-ins are refused (503). `rules` is for development and evaluation only; every rule-only reading says it was made offline. A request can never step down from the model engine to rules (403). |
| `ONTO_ALLOW_RULES_ONLY` | unset | `1` lets `auto` with no key serve rule-only readings (development, evaluation). Never set it on a public deployment |
| `ONTO_DATA_DIR` | `~/.onto-insight` | Where the encrypted database and key file live (mode 0700). Keep it outside the repository |
| `ONTO_DATA_KEY` | a key file in the data directory | A Fernet key (urlsafe base64). Set it in production and keep it in a secret store |
| `ONTO_RETENTION_DAYS` | `90` | How long personal data is kept |
| `ONTO_ADMIN_TOKEN` | none | Needed for the admin routes (review queue, drafts, costs, purge). If unset, admin is disabled |

Model and effort per step are in `config/model_routing.json`. Prices are in `config/pricing.json`; check them against
the published price list before relying on COSTS.md.

## Run
- Web: `python3 -m uvicorn insight.api:app --host 127.0.0.1 --port 8000`. Put a TLS-terminating reverse proxy in front.
  The app itself sets CSP, nosniff and no-referrer headers.
- CLI: `python3 -m insight.cli --help`.

## Daily
- **Retention purge:** `python3 -m insight.cli purge`, or `POST /api/admin/purge` with the admin token. Schedule it daily.
- **Review queue:** the Admin tab in the web page, or `python3 -m insight.cli posts --status pending`, then
  `review --post ID --action approve|edit|reject`.
  - Edited text is scanned for forbidden claims before it is saved.
  - Nothing is ever posted by the app. Publish by hand, one account per bucket, and label AI-assisted media where the
    platform requires it.

## Content
- Draft posts: `python3 -m insight.cli draft --bucket work --format x_post --n 10`.
- Plan a month: `python3 -m insight.cli calendar --bucket work`.

## Before each release
1. `python3 -m pytest -q`: every test passes.
2. `python3 scripts/check_layers.py`: layer entries whose citations resolve.
3. Check the crisis numbers in `rules/safety_messages.json`: Tele-MANAS 14416 / 1-800-891-4416, 112, 988, 911,
   Samaritans 116 123, 999, findahelpline.com, Women Helpline 181, Childline 0800 1111.
4. `python3 scripts/run_eval.py --engine rules`, and with a key `--engine model`. Then the judge scores the packets in
   `eval/judge/`, and the results go into RELEASE_REPORT.md.

## Incidents
- **Model outage.** Readings in model mode stop with `stop_unavailable`, because the safety screen fails closed. Do **not**
  switch a public deployment to `ONTO_ENGINE=rules` to keep serving: the rules screen alone misses indirect crisis
  wording that the model screen is there to catch. Wait for the API to recover.
- **Deletion request.** The person uses "Delete my data" in the page, or the operator runs
  `python3 -m insight.cli delete --person ID`.
- **Suspected key leak.** Rotate `ONTO_DATA_KEY`. Old records cannot be decrypted with the new key, so export and
  re-encrypt first, or purge.
- **Logs** hold ids, routes and error kinds only. If text ever appears in a log, treat it as a privacy incident: rotate
  and delete the logs, and fix the code path.
