# Costs

## Measured costs: NOT RUN
This session had no Anthropic API key, so no model call was made, and there are **no measured costs**. The gate
"measured cost (COSTS.md from real runs)" is therefore **not run**.

**Offline:** the rules engine makes no model calls and costs nothing per reading.

**To measure:** set `ANTHROPIC_API_KEY`, then run `python3 scripts/run_eval.py --engine model` and
`python3 scripts/build_content_queue.py --engine model`. Every call's tokens and cost are recorded:
- per step, in each report's `cost` field;
- in the admin view (`GET /api/admin/costs`, `python3 -m insight.cli costs`).

Replace the estimates below with those numbers.

## Estimates (not measurements)
- **Prices** come from `config/pricing.json` (per million tokens):
  - Opus 5.5: $4 in, $20 out.
  - Sonnet 5.5: $2 in, $10 out.
  - Cache reads cost $0.20. The cache-write price is an assumption; check it before relying on it.
- **Token counts** are rough assumptions and include thinking tokens in the output.
- **Model and effort per step** follow `config/model_routing.json`.

### One person map (model engine)
| Step | Model, effort | Assumed tokens in / out | Est. USD |
|---|---|---|---|
| Safety screen | Opus 5.5, high | 1,500 / 800 | 0.022 |
| Candidate mapping (the catalogue of mappable markers is most of the input) | Sonnet 5.5, high | 30,000 / 3,000 | 0.090 |
| Blind rechecks (0–40 per reading, about 10 assumed) | Sonnet 5.5, high | 10 × (800 / 400) | 0.056 |
| Two-lens synthesis | Opus 5.5, high | 6,000 / 3,000 | 0.084 |
| Pathway wording (the rules choose the practices) | Sonnet 5.5, high | 2,000 / 800 | 0.012 |
| **Total per reading** | | | **≈ 0.26** |
| With premium synthesis (xhigh; assume 6,000 out) | | | ≈ 0.32 |

A reading that stops at the safety screen costs about 0.02. A daily check-in is screened only, at about 0.013.

### Content engine
| Step | Model, effort | Assumed tokens in / out | Est. USD |
|---|---|---|---|
| Draft (voice guide, tone guide, format and teaching) | Sonnet 5.5, medium | 4,000 / 700 | 0.015 |
| Check (faithfulness, claims, idea) | Opus 5.5, high | 1,500 / 800 | 0.022 |
| **Per queued post** | | | **≈ 0.037** |
| 50 posts (10 per bucket) | | | ≈ 1.85 |

## Ways to cut cost (not done in v1)
- **Prompt caching.** Put the stable catalogue of mappable markers in a cached system block. This could cut
  candidate-mapping input cost by roughly 90% for repeat readings within the cache window. `insight/llm.py` does not
  set `cache_control` yet.
- **Fewer rechecks.** Cap blind rechecks lower than 40, or batch several items into one recheck call.
- **Cheaper synthesis.** Keep synthesis at high effort and not xhigh, unless the premium setting is chosen.
