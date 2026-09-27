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
- Stage 3 — listening to saturation on Opus 5.5 at max effort, script `pipeline/workflows/stage3-listen.js`. Per room and round: plan → search runners (50 queries each, 10 in parallel per message) → `label-prep` (harvest-search, batches, taxonomy, `funnel label-todo`) → one `label-batch` labeler per new batch and one `label-pack` re-checker per pack of earlier member records (when pains were added), in parallel → `label-finish` (apply-patches, count, saturation). Stops when saturated (from round 2, ≥500 records, no labeler-suggested pains), exhausted (a round after round 1 adds <50 new records) or at 8 rounds; then synthesize; then `pipeline/checkpoint.sh`. `args` = `{rooms, r1}`; `r1` (all 15 rooms) = round 1 already planned and searched, so those rooms start at `label-prep`. Build `r1` from each room's `queries.jsonl` (round-1 query count and distinct `kind` values).
- History: ~09:55 UTC the weekly usage limit stopped the first Opus workflows; ~10:05 relaunched with per-batch labeling; ~12:22 relaunched with member re-check packs; ~13:30-14:10 the session limit (reset 14:50 UTC) stopped all five; 14:55 relaunched (13 rooms at round 2, business-brokers and outbound at round 1 because 87 and 151 of their round-2 queries were never searched). `relabel-pack` now leaves out packs that already have a valid patch, and label-prep records `reviewed_rounds` in taxonomy.json so a relaunch does not review the same round twice. Current workflows:
  - `wf_a4972a08-72a`: small-industrial-property-investors, gre-engineers-india, active-retail-options-traders
  - `wf_f0b19ebd-3ee`: small-business-owners-reddit-community, bpo-contact-centre-operators-india-philippines, outbound-lead-gen-appointment-setting-agencies
  - `wf_79705356-864`: business-brokers-ma-boutiques, indie-perfumers-launching-brands, startup-founders-409a-83b-deadlines
  - `wf_590d35e6-416`: lender-insurer-telesales-floors-india, cfa-candidates-community, d2c-brands-scaling-past-launch
  - `wf_dc5d1723-22e`: dubai-real-estate-brokerages-telesales, gre-preppers-worldwide-online, salon-spa-owners-india-global
- Resume after an interruption: launch the same script with `args` = `{rooms, searched}`, where `searched[slug]` = `{round, queries, kinds}` for the last round whose queries were all planned and searched (check with `funnel harvest-search --room <slug>`: every query matched). That room starts at that round's `label-prep`; `label-todo` finds finished labels, so nothing done is redone. A room whose last round was only partly searched starts one round earlier (its planner returns the round's existing queries and the runners search them). A room may stop as saturated only from round 2, with no unmatched queries and no labeler-suggested pains. A failed step leaves the room at `error` without synthesis. Never resume the pre-switch workflows (`wf_4757764b-c75`, `wf_460fc963-f08`, `wf_79dc2b15-1cc`, `wf_32011f32-94e`, `wf_f82b6e84-e08`).
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
| active-retail-options-traders | 2 | 2309 | 2216 | round 1: 1086 records, not saturated | no | not checked |
| bpo-contact-centre-operators-india-philippines | 3 | 3272 | 2130 | round 2: 2130 records, not saturated | no | not checked |
| business-brokers-ma-boutiques | 2 | 1646 | 1603 | round 2: 1603 records, not saturated | no | not checked |
| cfa-candidates-community | 3 | 2542 | 2071 | round 2: 1751 records, not saturated | no | not checked |
| d2c-brands-scaling-past-launch | 2 | 1884 | 1827 | round 2: 1827 records, not saturated | no | not checked |
| dubai-real-estate-brokerages-telesales | 2 | 1516 | 1472 | round 2: 1472 records, not saturated, stopped: exhausted | yes | 17 pass / 0 fail (self-check) |
| gre-engineers-india | 2 | 1762 | 1726 | round 1: 900 records, not saturated | no | not checked |
| gre-preppers-worldwide-online | 3 | 2997 | 2456 | round 2: 1896 records, not saturated | no | not checked |
| indie-perfumers-launching-brands | 3 | 2740 | 2128 | round 2: 1728 records, not saturated | no | not checked |
| lender-insurer-telesales-floors-india | 2 | 1721 | 1684 | round 2: 1684 records, not saturated, stopped: exhausted | yes | 0 pass / 0 fail (self-check) |
| outbound-lead-gen-appointment-setting-agencies | 2 | 2090 | 1464 | round 1: 984 records, not saturated | no | not checked |
| salon-spa-owners-india-global | 2 | 2302 | 2255 | round 2: 2255 records, not saturated | no | not checked |
| small-business-owners-reddit-community | 3 | 3505 | 2180 | round 2: 2180 records, not saturated | no | not checked |
| small-industrial-property-investors | 2 | 1784 | 1748 | round 1: 948 records, not saturated | no | not checked |
| startup-founders-409a-83b-deadlines | 3 | 2614 | 1636 | round 2: 1636 records, not saturated | no | not checked |

Rooms kept: 15. Pains kept: 0. Stage 6 kept: 0. Survivors (final): 0.
<!-- /auto:status -->
