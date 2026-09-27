# Progress

Read this first when resuming ("continue"). Never redo a step marked done.
Current run folder: `runs/2026-09-26/`

## Done
- Step 0 — Permissions: the session runs in auto mode, so no permission change was needed. The web-search cap (default 200 per session) was raised to 20000 with `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` in the repo-root `.claude/settings.json` (a project-settings change the founder authorized in Step 0). (2026-09-27)
- Step C — `config/ledger.md` written exactly as given; `config/ledger.yaml` is its transcription. (2026-09-26)
- Step B — new rules made permanent (commit c1eae44).
- Step A (part) — core, sources, admin, prices, stage1, stage2 built; 130 core tests pass.
- Stage 1 (part) — six lens files and four gap files written; FX rates in `runs/2026-09-26/fx_rates.json` (read from the npm-hosted currency-api dataset, dated 2026-09-26, because FX sites are blocked).

## In progress (workflows; resume with the Workflow tool and `resumeFromRunId` if interrupted)
- Step A finish — `funnel-build-finish` (run `wf_51b992ab-f05`): finish stage3/stage45/stage6/outputs → integration → 4 reviews → fixes.
- Stage 1 grounding A — `funnel-stage1-ground-a` (run `wf_e87b0e72-48a`): re-ground and top up business_type, identity_community, obligation, transition.
- Stage 1 grounding B — `funnel-stage1-ground-b` (run `wf_a0f83bc8-726`): re-ground gap files, redo gap_profession, add gap_identity_community.
- Why: the first Stage 1 pass hit the 200-search cap; later agents reused sibling URLs instead of searching. Nothing was invented, but the rooms were thin.

## Next
1. Record build test results in the run's RUNLOG.md (`funnel log`), commit.
2. `funnel rooms --merge-parts` (80–120 rooms), resolve near-duplicates → checkpoint.
3. Stage 2 mask (≤15 rooms) → checkpoint.
4. Stage 3 listen to saturation, one listener per room → checkpoint per room → `funnel pains` → checkpoint.
5. Stages 4–6, red team, audit packet, outputs → final commit, push, pull request.
6. Step E — final output in chat.

## Known blockers
- The environment's network policy blocks every data source except web search (see `config/sources.md`). Stage 3 evidence = search-result titles and URLs captured verbatim from the session transcripts. Logged as a limit for REVIEW.md.

<!-- auto:status -->
<!-- /auto:status -->
