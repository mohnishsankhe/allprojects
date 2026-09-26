---
name: funnel-run
description: Opportunity Funnel full run. Stages 1–6 plus the audit packet, ending with SHORTLIST.md, REVIEW.md and RUNLOG.md in runs/YYYY-MM-DD/. Runs to the end without stopping; needs a confirmed ledger from /funnel-setup.
argument-hint: "[--rooms N] [--run YYYY-MM-DD] [--only-room <slug>] (optional: limit the number of rooms, reuse a run folder, dry-run one room)"
disable-model-invocation: true
---

# /funnel-run: Stages 1–6 and the audit packet

Arguments: `$ARGUMENTS` (may be empty).
- `--rooms N` caps the rooms kept at Stage 2 (below the kill rules' limit), for small runs.
- `--run YYYY-MM-DD` reuses that run folder (to resume or rerun). The default is today.
- `--only-room <slug>` is a dry run: Stages 3–6 for that one room only.

`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py`. Pass `--run RUN` to every command. `RUN` is `runs/YYYY-MM-DD`.
Everything happens inside `opportunity-funnel/` (rule 11). Do not stop to ask the founder anything. Put anything that needs them in `REVIEW.md` (the scripts do this from the files). Give short progress notes between stages.
Every stage is rerunnable. If a step fails, fix its input and rerun the step. Record each error with `funnel log --stage <n> --error "<what broke>"`.

## Stage 0 check
1. `funnel preflight`. It creates `RUN`, snapshots `config/`, checks that the ledger is confirmed (stop only if there is no ledger: tell the founder to run `/funnel-setup`), checks API keys (names only, never values), and tests each source domain. In a cloud session, blocked domains are logged. Keep going with what is reachable.

## Stage 1: Rooms
2. Read `graveyard.md` (`funnel graveyard`).
3. Spawn **4 agents in parallel** (general-purpose), one per lens: `life_stage`, `profession`, `transition`, `obligation`. Give each: the path to `config/ledger.md` (geography, languages, exclusions), `config/definitions.md`, the Stage 1 part of `config/formats.md`, the graveyard list, and the instruction to write 12–15 rooms to `RUN/01_rooms.parts/<lens>.json`. For each room: name, who is in it, where they gather (named communities, platforms and sites, with URLs), who pays, rough size (`measured` with URL, or `estimate` with reasoning), its ladder (the paid problems, in order), and geography. Rooms must sit inside the ledger's geographies. Use WebSearch to ground places and sizes. Invent nothing.
4. If `config/rooms_external.md` exists, spawn one agent to convert it into `RUN/01_rooms.parts/external.json` with `"origin": "external"`, filling gaps by research.
5. `funnel rooms --merge-parts`. It merges the parts, removes exact duplicates and graveyard rooms, lists near-duplicates, checks the 40–60 range and the lens balance, and writes `01_rooms.json` and `01_rooms.md`. For each near-duplicate it lists, set `"duplicate_of": "<slug>"` in `01_rooms.json` when they really are the same room, then run `funnel rooms` again. If the count is out of range, add or cut rooms and rerun.

## Stage 2: Room mask
6. Split the rooms into groups of about 8. Spawn one agent per group (in parallel). Each writes `RUN/02_mask.parts/<n>.json` in the Stage 2 format. For every room it:
   - matches reach to a ledger reach id (or null);
   - matches depth to a ledger depth id or a partner id (or null);
   - finds at least one concrete price people in this room already pay for a problem of this kind, by web search, with `price_text` copied exactly and the URL;
   - checks supply (does the room's core pain obviously need a licence, physical work or capital the ledger lacks?);
   - checks the ledger's exclusions.
   Judgment only. The script applies the rules.
7. `funnel mask --merge-parts` (add `--max-rooms N` if given). It checks prices on their pages, applies the mask mechanically, keeps at most 10, writes `02_mask.json` and `02_mask.md`, sends kills to the graveyard, and notes in `REVIEW.md` if fewer than 5 survive.

## Stage 3: Listen
8. For each kept room (or only `--only-room`), spawn one **`funnel-listener`** agent, mode `full`, with `RUN` and the room slug. Run them in parallel. One room per agent, never more.
9. `funnel pains`. It merges the rooms' drafts with the code counts, runs the quote checker (writes `quote_check.csv`, deletes failed quotes), applies the Stage 3 kill rules, tags `[thin]`, ranks, keeps at most 15, writes `pains.json` and `pains.md`, and sends kills to the graveyard.

## Stages 4 and 5: Walk and pair
10. For each kept pain, spawn one **`funnel-walker`** agent, mode `walk`, with `RUN` and the `pain_id`. Run them in parallel.
11. `funnel walks` (Stage 4 kills, lane hints, renders each walk), then `funnel pairs` (lanes, Stage 5 kills, `05_pairs.md`, credibility questions).

## Stage 6: Numbers
12. For each pain that survived Stage 5, spawn one **`funnel-walker`** agent, mode `numbers`. Run them in parallel.
13. `funnel price-check --stage 6`, then `funnel numbers`. It does all the arithmetic, kills survivors whose numbers don't work inside the ledger, ranks the rest, keeps at most 3, and writes `06_numbers.csv`, `06_numbers.md` and `06_survivors.json`.

## Audit packet and outputs
14. `funnel audit-packet`. It writes `07_audit_packet/AUDIT_PROMPT.md` and `evidence.md`. Do not run the audit yourself.
15. `funnel shortlist`, `funnel review`, `funnel runlog`.
16. Check: `funnel status`. Every stage file should exist or have a logged reason for being missing.
17. **Commit** only this folder: `git add -- <repo>/opportunity-funnel` then `git commit -m "$(funnel commit-message)"`. In a cloud session, push to the session's branch and, at the end of the session, open a pull request that changes only files inside `opportunity-funnel/` (plus the repo-root `funnel-*` pointer files).
18. **Tell the founder, in five lines:** rooms in; rooms kept; pains found; survivors; the top hypothesis. Then list any blocked domains or missing keys.
