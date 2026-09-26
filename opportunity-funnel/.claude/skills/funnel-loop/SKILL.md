---
name: funnel-loop
description: Opportunity Funnel loop mode. Reruns Stages 3–6 inside ONE room already kept by an earlier run, adding the founder's customer messages from inbox/customers/<room>/ as Listen input. Use once you have customers in a room.
argument-hint: "<room-slug>"
arguments: [room]
disable-model-invocation: true
---

# /funnel-loop <room>: Stages 3–6 inside one room

Room slug: `$ARGUMENTS`. If it is empty, run `funnel rooms-known` to list rooms from earlier runs, and stop with that list.

`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py`. Stay inside `opportunity-funnel/`. Do not stop to ask the founder anything.

1. `funnel loop-init --room <slug>`. It creates `runs/YYYY-MM-DD-loop-<slug>/`. It copies this room's entries from the latest run that kept it (`01_rooms.json`, `02_mask.json`), snapshots `config/` and checks the ledger. It prints the new `RUN` path. Use it for every command below. If the room was never kept, or is in the graveyard with no new evidence, it stops and says why.
2. Spawn one **`funnel-listener`** agent, mode `full`, `customers: yes`, with `RUN` and the slug. It also runs `funnel ingest-inbox --room <slug> --customers`, which anonymizes `inbox/customers/<slug>/` before anything reads it. Customer messages count as Listen input like any other source (`source` = `inbox:customers`).
3. `funnel pains`.
4. One **`funnel-walker`** per kept pain, mode `walk`, in parallel. Then `funnel walks` and `funnel pairs`.
5. One **`funnel-walker`** per pair survivor, mode `numbers`, in parallel. Then `funnel price-check --stage 6` and `funnel numbers`.
6. `funnel audit-packet`, `funnel shortlist`, `funnel review`, `funnel runlog`.
7. `funnel compare --with latest`. It writes a short "what changed since the last run in this room" section into `RUNLOG.md`: pains added or dropped, count changes, and survivor rank changes.
8. Commit only this folder, with the message from `funnel commit-message`.
9. Tell the founder in five lines: records in (customer messages among them), pains found, survivors, the top hypothesis, and the biggest change since the last run.
