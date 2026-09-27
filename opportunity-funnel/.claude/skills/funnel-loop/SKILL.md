---
name: funnel-loop
description: Opportunity Funnel loop mode. Reruns Stages 3–6 (plus red team) inside ONE room already kept by an earlier run, adding the founder's customer messages from inbox/customers/<room>/ as Listen input. Use once you have customers in a room.
argument-hint: "<room-slug>"
arguments: [room]
disable-model-invocation: true
model: claude-opus-5-5
effort: max
---

# /funnel-loop <room>: Stages 3–6 inside one room

Room slug: `$ARGUMENTS`. If empty, run `funnel rooms-known`, show the list and stop.
`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py --run RUN`. Stay inside `opportunity-funnel/`. Never ask the founder anything; follow the standing rules of `/funnel-run` (conservative choices logged, Claude Opus 5.5 at max effort for everything, checkpoints, resume from `PROGRESS.md`).

1. `funnel loop-init --room <slug>` → prints the new `RUN` (`runs/YYYY-MM-DD-loop-<slug>/`) with the room's Stage 1–2 entries copied from the latest run that kept it. Copy that run's `fx_rates.json` if it is less than 7 days old; otherwise refresh the rates.
2. `funnel ingest-inbox --room <slug> --customers` (anonymizes `inbox/customers/<slug>/` before anything reads it; source `inbox:customers`). Also `funnel ingest-inbox --room <slug>` for closed-group exports.
3. Stage 3 exactly as in `/funnel-run` for this one room (plan → harvest → label rounds until saturated, then synthesize), then `funnel pains`.
4. Stages 4–6, red team and outputs exactly as in `/funnel-run`.
5. `funnel compare --with latest` adds "What changed since the last run in this room" to `RUNLOG.md`.
6. Commit with `funnel commit-message`, push.
7. Tell the founder in five lines: records in (customer messages among them), pains found, survivors, the top hypothesis, the biggest change since the last run.
