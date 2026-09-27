# Progress

Read this first when resuming ("continue"). Never redo a step marked done.
Current run folder: `runs/2026-09-26/`

## Model policy (founder, 2026-09-27 08:16 UTC)
Claude Opus 5.5 (`claude-opus-5-5`) at max effort for everything: this session, every subagent, all bulk labeling. Never Fable or a smaller model. Pinned in: `CLAUDE.md` rule 13, both agent definitions and all four skills (frontmatter `model: claude-opus-5-5`, `effort: max`), the repo-root pointer files, `pipeline/workflows/*.js` (`{ model: 'claude-opus-5-5', effort: 'max' }` on every agent), and the repo-root `.claude/settings.json` (`model`, `CLAUDE_CODE_EFFORT_LEVEL=max`; `CLAUDE_CODE_SUBAGENT_MODEL` is ignored by this host-managed session, so every agent call names the model). Every new workflow agent call must pass `model: 'claude-opus-5-5', effort: 'max'`.

## Done
- Step 0 — Permissions: the session runs in auto mode, so no permission change was needed. The web-search cap (default 200 per session) was raised to 20000 with `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` in the repo-root `.claude/settings.json` (a project-settings change the founder authorized in Step 0). (2026-09-27)
- Step C — `config/ledger.md` written exactly as given; `config/ledger.yaml` is its transcription. (2026-09-26)
- Step B — new rules made permanent (commit c1eae44).
- Step A — DONE: 17 modules built; four independent reviews found 22 problems (15 major, 0 blockers), all fixed with regression tests; 426 tests pass, logged in the run log (2026-09-27).
- Stage 1 — DONE: 123 rooms generated (six lenses + gap pass, all re-grounded with fresh searches), 12 true duplicates removed → 111 rooms in `runs/2026-09-26/01_rooms.json` / `01_rooms.md` (life_stage 10, profession 22, transition 20, obligation 19, business_type 19, identity_community 21). FX rates in `runs/2026-09-26/fx_rates.json`. (2026-09-27)
- Stage 2 — DONE: 111 in → 36 killed (35 on depth), 75 passed, 15 kept, 60 cut. After an equal-effort ladder audit of all 75 survivors and a priced-ladder-steps tie-break, the kept rooms are: small-industrial-property-investors, gre-engineers-india, active-retail-options-traders, small-business-owners-reddit-community, bpo-contact-centre-operators-india-philippines, outbound-lead-gen-appointment-setting-agencies, business-brokers-ma-boutiques, indie-perfumers-launching-brands, startup-founders-409a-83b-deadlines, lender-insurer-telesales-floors-india, cfa-candidates-community, d2c-brands-scaling-past-launch, dubai-real-estate-brokerages-telesales, gre-preppers-worldwide-online, salon-spa-owners-india-global. Graveyard consistent (revival notes for re-kept rooms). (2026-09-27)

## In progress
- Stage 3 — listening to saturation on Opus 5.5 at max effort, script `pipeline/workflows/stage3-listen.js`. Per room and round: plan → search runners (50 queries each, 10 in parallel per message) → `label-prep` (harvest-search, batches, taxonomy, `funnel label-todo`) → one `label-batch` labeler per batch in parallel → `label-finish` (count, saturation). Stops when saturated (from round 2, ≥500 records, no labeler-suggested pains), exhausted (a round after round 1 adds <50 new records) or at 8 rounds; then synthesize; then `pipeline/checkpoint.sh`. `args` = `{rooms, r1}`; `r1` (all 15 rooms) = round 1 already planned and searched, so those rooms start at `label-prep`. Build `r1` from each room's `queries.jsonl` (round-1 query count and distinct `kind` values).
- 2026-09-27 ~09:55 UTC the weekly usage limit stopped the five workflows launched at ~08:44. State then: round 1 labeled in 9 rooms (5 of them with round-2 queries planned, not yet searched), partly labeled in active-retail, salon-spa and startup-founders, not labeled in d2c and outbound. Relaunched with per-batch labeling after the founder's "Try again" (~10:05 UTC):
  - `wf_46876e4c-15e`: small-industrial-property-investors, gre-engineers-india, active-retail-options-traders
  - `wf_8d9d92d1-ffe`: small-business-owners-reddit-community, bpo-contact-centre-operators-india-philippines, outbound-lead-gen-appointment-setting-agencies
  - `wf_d5941d3f-ab9`: business-brokers-ma-boutiques, indie-perfumers-launching-brands, startup-founders-409a-83b-deadlines
  - `wf_4e83b9b5-cf2`: lender-insurer-telesales-floors-india, cfa-candidates-community, d2c-brands-scaling-past-launch
  - `wf_fc5f1a47-cc6`: dubai-real-estate-brokerages-telesales, gre-preppers-worldwide-online, salon-spa-owners-india-global
- Resume after an interruption: launch the same script with the same `args` (a fresh run is fine: `label-prep` finds finished labels with `label-todo`, planners return round queries that already exist, and a failed step leaves the room at `error` without synthesis). Never resume the pre-switch workflows (`wf_4757764b-c75`, `wf_460fc963-f08`, `wf_79dc2b15-1cc`, `wf_32011f32-94e`, `wf_f82b6e84-e08`).
- A room is finished when `runs/2026-09-26/03_listen/rooms/<slug>/pains_draft.json` and `sources.json` exist and `funnel quote-check --room <slug>` passes; the auto-status block below shows it.

## Next
1. Stage 3 to saturation in every room → checkpoint per room → `funnel pains` → checkpoint.
2. Stage 4 (two walkers + comparator per pain) → `funnel walks`, `funnel pairs` → checkpoint.
3. Stage 6 numbers → `funnel price-check --stage 6`, `funnel numbers` → checkpoint.
4. Red team, audit packet, outputs (SHORTLIST.md, REVIEW.md, RUNLOG.md) → final commit, push, pull request.
5. Step E — final output in chat.

## Known blockers
- The environment's network policy blocks every data source except web search (see `config/sources.md`). Stage 3 evidence = search-result titles and URLs captured verbatim from the session transcripts. Logged as a limit for REVIEW.md.

<!-- auto:status -->
Run folder: `runs/2026-09-26` (regenerated by `funnel progress`; do not edit by hand).

| Stage | Output | State |
|---|---|---|
| 0 | preflight (`preflight.json`) | missing |
| 1 | rooms (`01_rooms.json`) | done |
| 2 | fx (`fx_rates.json`) | done |
| 2 | mask (`02_mask.json`) | done |
| 3 | pains (`03_listen/pains.json`) | missing |
| 4 | walks (`04_walks/_stage4.json`) | missing |
| 5 | pairs (`05_pairs.json`) | missing |
| 6 | numbers (`06_survivors.json`) | missing |
| 7 | redteam (`07_red_team/_redteam.json`) | missing |
| 7 | case against (`07_audit_packet/case_against.json`) | missing |
| 7 | audit-packet (`07_audit_packet/AUDIT_PROMPT.md`) | missing |
| 7 | shortlist (`SHORTLIST.md`) | missing |
| 7 | review (`REVIEW.md`) | missing |
| 7 | runlog (`RUNLOG.md`) | missing |
| 7 | red team files (`07_red_team/*.json`) | missing |

Stage 3 per room:

| Room | Rounds | Records | Labeled | Saturation | Draft | Quote check |
|---|---|---|---|---|---|---|
| active-retail-options-traders | 1 | 1150 | 1086 | round 1: 1086 records, not saturated | no | not checked |
| bpo-contact-centre-operators-india-philippines | 1 | 1283 | 1243 | round 1: 1243 records, not saturated | no | not checked |
| business-brokers-ma-boutiques | 2 | 1005 | 979 | round 1: 896 records, not saturated | no | not checked |
| cfa-candidates-community | 2 | 927 | 805 | round 1: 805 records, not saturated | no | not checked |
| d2c-brands-scaling-past-launch | 1 | 1032 | 560 | not evaluated | no | not checked |
| dubai-real-estate-brokerages-telesales | 1 | 912 | 882 | round 1: 882 records, not saturated | no | not checked |
| gre-engineers-india | 1 | 923 | 900 | round 1: 900 records, not saturated | no | not checked |
| gre-preppers-worldwide-online | 2 | 979 | 924 | round 1: 924 records, not saturated | no | not checked |
| indie-perfumers-launching-brands | 2 | 1794 | 845 | round 1: 845 records, not saturated | no | not checked |
| lender-insurer-telesales-floors-india | 1 | 858 | 835 | round 1: 835 records, not saturated | no | not checked |
| outbound-lead-gen-appointment-setting-agencies | 1 | 1022 | 240 | not evaluated | no | not checked |
| salon-spa-owners-india-global | 1 | 1380 | 1280 | not evaluated | no | not checked |
| small-business-owners-reddit-community | 1 | 926 | 896 | round 1: 896 records, not saturated | no | not checked |
| small-industrial-property-investors | 2 | 1784 | 948 | round 1: 948 records, not saturated | no | not checked |
| startup-founders-409a-83b-deadlines | 1 | 870 | 813 | round 1: 813 records, not saturated | no | not checked |

Rooms kept: 15. Pains kept: 0. Stage 6 kept: 0. Survivors (final): 0.
<!-- /auto:status -->
