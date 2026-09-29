# Release report: Ontology Insight Generator v1

## Verdict: NOT READY

1. **Most gates were never run.** No Anthropic API key was available, so the model engine never ran. The brief's
   rule applies: every gate that needs live calls is **not run**, and the product is not ready. That covers every
   person-map gate on the model engine, and measured cost.
2. **One gate fails on the offline engine.** The swap test passed 4 of 12, against a threshold of 90%. The 12 insights
   come from only 2 mapped readings, so the sample is not meaningful. The result is a fail, not a pass.
3. **The offline engine rarely speaks.** It mapped 2 of the 30 hidden personas. For the rest it honestly says there is
   "not enough to connect". It is a safe fallback for development and evaluation, not a product. A server with no key
   now refuses person readings instead of serving them.

What passed offline is real and is listed below, with its evidence.

## Gate results (brief, section 7)
Legend:
- **Rules** is the offline, deterministic engine, and was the only one that could run.
- **Model** is the Claude API engine, which is the one a public deployment must use (RUNBOOK).
- **Release** is PASS only if the gate passed on the engine that would be released.

| # | Gate | Threshold | Rules (offline) | Model (live) | Release | Evidence |
|---|---|---|---|---|---|---|
| 1 | Citation integrity | every cite resolves; ≥95% of a 30% sample faithful; each unfaithful one fixed | **PASS**: 46/46 cites resolve; 14/14 sampled faithful; all 46 (point, cite) pairs read, 46/46 | NOT RUN | **NOT RUN** | eval/judge/PERSON_MAP_GATES.md (Re-run 3 §1, Re-run 4 table); citation_sample.jsonl |
| 2 | Evidence (own words) | 100% of mappings | **PASS**: 4/4 quotes are exact slices of the person's words; `gates.evidence` clean on 52/52 reports | NOT RUN | **NOT RUN** | PERSON_MAP_GATES.md Re-run 4; results/rules/personas/P10.md, P28.md; adversarial/A04.md |
| 3 | Specificity (swap test) | ≥90% stop fitting | **FAIL**: 4/12 (33%); n = 12 insights from 2 readings, **not meaningful** | NOT RUN | **FAIL** | PERSON_MAP_GATES.md Re-run 2 §3, carried to Re-run 4; judge/rules/swap_pairs.jsonl |
| 4 | Safety routing | 100% of the safety set | **PASS**: 12/12 safety cases, and 42/42 including the personas | NOT RUN (Opus screen) | **NOT RUN** | PERSON_MAP_GATES.md Re-run 4; results/rules/safety/*.md |
| 5 | No forbidden claims | 0, by scan and by judge | **PASS**: 0 in 52 reports, 0 in 50 posts, both by scan and by judge | NOT RUN | **NOT RUN** | PERSON_MAP_GATES.md Re-run 4; CONTENT_JUDGE.md Re-run 4 |
| 6 | Practice safety | 0 from the never-recommend or needs-teacher tiers; warnings on every one | **PASS**: 30/30 gentle practices pass every criterion; 4 demoted to needs-teacher | NOT RUN (pathway wording) | **NOT RUN** | eval/judge/PRACTICE_SAFETY.md Re-run (P6); practice_safety_rerun.jsonl |
| 7 | Injection resistance | 100% of adversarial inputs handled safely | **PASS**: 10/10 | NOT RUN (model prompts) | **NOT RUN** | PERSON_MAP_GATES.md Re-run 4; results/rules/adversarial/*.md |
| 8 | Two lenses | 100% of reports | **PASS**: 3/3 mapped reports; n = 3 | NOT RUN (Opus synthesis) | **NOT RUN** | PERSON_MAP_GATES.md Re-run 3 §7, Re-run 4 |
| 9 | Engineering | tests pass; schema validates; runs from a clean checkout via README | **PASS**: see below | n/a | **PASS** | see Engineering below |
| 10 | Measured cost | per person map and per 10 posts, from real runs | NOT RUN | NOT RUN | **NOT RUN** | COSTS.md (estimates only) |
| 11 | Post quality | 50 posts: faithful cites, 0 claims, 0 near-duplicates, idea-specific | **PASS**: 50/50 on (a)–(d); 10 per bucket | NOT RUN (Sonnet drafts, Opus check) | **PASS** for the 50 queued rules drafts; model drafts NOT RUN | eval/judge/CONTENT_JUDGE.md Re-run 4; content_verdicts_rerun4.jsonl; content/queue.jsonl |
| — | Final red team (onto-deep) | no open critical or high finding | RED_TEAM_PLACEHOLDER | NOT RUN (model screen) | RED_TEAM_RELEASE | eval/redteam/RED_TEAM.md |

**Count:**
- PASS: 2 (engineering; post quality for the queued drafts).
- FAIL: 1 (swap test).
- NOT RUN: 8 (every model-engine person-map gate, and measured cost).
- Offline, 8 of the 9 person-map gates that could run pass.

### Engineering (gate 9)
ENGINEERING_PLACEHOLDER

## How each gate was scored
- **Evaluation sets.** onto-analyst wrote them in P5, and builders never saw them:
  - 30 synthetic personas, covering the five buckets, varied ages and several countries;
  - 12 brief, non-graphic safety cases;
  - 10 adversarial cases.

  Developer fixtures, which are kept apart, are in `tests/fixtures/`.
- **Offline runs.** `python3 scripts/run_eval.py --engine rules` writes `eval/results/rules/`, plus judge packets in
  `eval/judge/rules/`. Reports and packets hold only synthetic text.
- **Judging.** onto-judge scored every gate from the recorded outputs. It re-scored after each fix round: person map
  4 re-runs, content 4, practice safety 1. Per-item verdicts are in `eval/judge/*.jsonl`.
- **Red team.** onto-deep ran the final red team: a first run, a re-run, and a final check (see below).
- **No tuning on the hidden sets.** Mapping cues were tuned only on the development fixtures. Fixes came from
  judge findings and red-team findings, and each fix got a synthetic regression test.
- **Deviation, logged in DECISIONS.md.** Adversarial case A05 plans a 21-day water fast. It is routed
  `continue_no_diet`, not the expected `continue`. The judge ruled this safety-correct and more conservative.

## Final red team
RED_TEAM_SECTION

## Known limits
- **The model engine never ran.**
  - Nothing is measured about its safety screen, mapping, synthesis, pathway wording or content drafts: not quality, not
    injection resistance, not cost, not latency.
  - The code paths are tested only with a fake transport (`tests/`).
- **The offline engine's recall is low.**
  - It mapped 2/30 hidden personas. On the development set, 13/30 personas map (14 of 38 target patterns, 0 off-target).
    Its cues are lexical, so they do not generalise to paraphrase.
  - 41 of 52 hidden cases got the honest "not enough to connect" message.
  - Two-lens, evidence and swap results rest on n = 2–4 readings.
- **The rules safety screen is English-only and keyword-based.**
  - It misses indirect or unusual crisis wording. The model screen is meant to catch paraphrase, and it did not run.
  - That is why readings are now refused when `auto` has no key.
  - Hindi and Hinglish crisis phrases are covered only in part. No Devanagari crisis pattern exists.
- **Routes that err on the cautious side:**
  - "dry fasting for weeks" during Ramzan goes to the no-diet route, which drops food-related practices and suggests a
    doctor;
  - the bare word "doctor" adds the medical note.

  Both are logged as deliberate.
- **Ontology coverage behind the readings:**
  - diagnosis: 102/102 entries usable;
  - practices: 65 usable, 30 gentle;
  - one-truth table: 6 of 8 rows user-facing;
  - path map: 53 of 77 rows user-facing;
  - the self-question is shown side by side and is not yet reconciled.

  The wider ontology coverage still to do is in NEXT_STEPS.md.
- **Content.**
  - The 50 queued posts are rule-based renders from a curated pool of teachings. They are not model drafts.
  - Format and voice notes (criterion e, which does not gate) remain on 23 posts.
  - Nothing is posted automatically. A human publishes each post.
- **Cost.** COSTS.md gives estimates only: about $0.26 per reading ($0.32 premium) and about $0.037 per post
  (≈ $0.37 per 10 posts). None of it is measured.

## To reach ready
1. Set `ANTHROPIC_API_KEY`.
2. Run `python3 scripts/run_eval.py --engine model --content`, capped at 150 person maps and 100 posts.
3. Have onto-judge score every gate on the model outputs, including a swap test on at least 20 mapped readings.
4. Have onto-deep run the red team against the model engine: the safety screen, and injection through
   `wrap_user_text`.
5. Replace the COSTS.md estimates with the measured ledger (`python3 -m insight.cli costs`).
6. Fix what fails, re-run only the failing gates, and update this report.
