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
- Stage 3 — listening to saturation, workflow script `pipeline/workflows/stage3-listen.js` (one listener per room: plan → search runners run the queries verbatim → label → count → saturation; stops when saturated with ≥500 records, exhausted, or 8 rounds; then synthesize; then `pipeline/checkpoint.sh`). Five workflows (rooms passed as `args.rooms`):
  - `wf_4757764b-c75`: small-industrial-property-investors, gre-engineers-india, active-retail-options-traders
  - `wf_460fc963-f08`: small-business-owners-reddit-community, bpo-contact-centre-operators-india-philippines, outbound-lead-gen-appointment-setting-agencies
  - `wf_79dc2b15-1cc`: business-brokers-ma-boutiques, indie-perfumers-launching-brands, startup-founders-409a-83b-deadlines
  - `wf_32011f32-94e`: lender-insurer-telesales-floors-india, cfa-candidates-community, d2c-brands-scaling-past-launch
  - `wf_f82b6e84-e08`: dubai-real-estate-brokerages-telesales, gre-preppers-worldwide-online, salon-spa-owners-india-global
- Switch-over to Opus 5.5 (in progress): the five workflows were launched before the model switch and are left to finish, as the founder asked. Under rule 13 their Fable labelers stop themselves without labeling. When a workflow ends: (1) read its `journal.jsonl` (`~/.claude/projects/-home-user-allprojects/<session>/subagents/workflows/<run id>/`); (2) put in `args.legacy` the labels of finished agents to keep: every `plan:*:r1` and `harvest:*:r1:*` that finished normally, plus any `label:*` that finished normally and was already running at 08:16 UTC; (3) remove taxonomy drafts and partial labels left by Fable labelers that did not finish (git history keeps them); (4) resume with the Workflow tool (`scriptPath` = `pipeline/workflows/stage3-listen.js`, `resumeFromRunId` = the run id, `args` = `{rooms, legacy}`). Legacy agents replay from cache; everything else runs on Opus 5.5 at max effort.
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
| active-retail-options-traders | 0 | 0 | 0 | not evaluated | no | not checked |
| bpo-contact-centre-operators-india-philippines | 1 | 1211 | 480 | not evaluated | no | not checked |
| business-brokers-ma-boutiques | 1 | 922 | 0 | not evaluated | no | not checked |
| cfa-candidates-community | 1 | 850 | 0 | not evaluated | no | not checked |
| d2c-brands-scaling-past-launch | 0 | 0 | 0 | not evaluated | no | not checked |
| dubai-real-estate-brokerages-telesales | 1 | 912 | 80 | not evaluated | no | not checked |
| gre-engineers-india | 1 | 920 | 0 | not evaluated | no | not checked |
| gre-preppers-worldwide-online | 1 | 948 | 0 | not evaluated | no | not checked |
| indie-perfumers-launching-brands | 1 | 871 | 0 | not evaluated | no | not checked |
| lender-insurer-telesales-floors-india | 1 | 858 | 560 | not evaluated | no | not checked |
| outbound-lead-gen-appointment-setting-agencies | 0 | 0 | 0 | not evaluated | no | not checked |
| salon-spa-owners-india-global | 0 | 0 | 0 | not evaluated | no | not checked |
| small-business-owners-reddit-community | 1 | 926 | 0 | not evaluated | no | not checked |
| small-industrial-property-investors | 1 | 978 | 0 | not evaluated | no | not checked |
| startup-founders-409a-83b-deadlines | 1 | 870 | 160 | not evaluated | no | not checked |

Rooms kept: 15. Pains kept: 0. Stage 6 kept: 0. Survivors (final): 0.
<!-- /auto:status -->
