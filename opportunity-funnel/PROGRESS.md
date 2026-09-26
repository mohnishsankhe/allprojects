# Progress

Read this first when resuming ("continue"). Never redo a step marked done.
Current run folder: `runs/2026-09-26/`

## Done
- Step 0 — Permissions: the session runs in auto mode, so no settings change was needed. (2026-09-26)
- Step C — `config/ledger.md` written exactly as the founder gave it; `config/ledger.yaml` is its machine-readable transcription. (2026-09-26)
- Step B — new rules made permanent: `CLAUDE.md`, `config/kill_rules.yaml`, `config/formats.md`, `config/definitions.md`, `config/sources.md`, the four skills, both subagents, `pipeline/README.md`. (commit c1eae44)

## In progress
- Step A — pipeline build workflow `funnel-build-pipeline-v2` (run id `wf_4a614d5e-c00`): core → 4 parallel modules → integration → 4 reviews → fixes. If interrupted, resume it with the Workflow tool (`resumeFromRunId`); finished agents are cached.
- Stage 1 — rooms workflow `funnel-stage1-rooms` (run id `wf_b92d470f-599`): six lens agents → six gap-pass agents, plus FX rates. Outputs: `runs/2026-09-26/01_rooms.parts/*.json`, `runs/2026-09-26/fx_rates.json`. Merge with `funnel rooms --merge-parts` once the build lands.

## Next
1. Record build test results in the run's RUNLOG.md; commit.
2. Stage 1 merge and dedupe (80–120 rooms) → checkpoint.
3. Stage 2 mask (≤15 rooms) → checkpoint.
4. Stage 3 listen to saturation, one listener per room, rooms in parallel → checkpoint after each room → `funnel pains` → checkpoint.
5. Stage 4 (two walkers + comparator per pain) → Stage 5 pairs → Stage 6 numbers → red team → audit packet → outputs → final commit, push, pull request.
6. Step E — final output in chat.

## Known blockers
- The environment's network policy blocks every data source except web search (see `config/sources.md`). Stage 3 evidence = search-result titles and URLs captured verbatim from the session transcripts. Logged as a limit for REVIEW.md.

<!-- auto:status -->
<!-- /auto:status -->
