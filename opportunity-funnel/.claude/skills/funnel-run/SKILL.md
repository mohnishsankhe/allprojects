---
name: funnel-run
description: Opportunity Funnel full run at maximum depth. Stages 1–6, red team and audit packet, ending with SHORTLIST.md, REVIEW.md and RUNLOG.md in runs/YYYY-MM-DD/. Never asks the founder anything; checkpoints to PROGRESS.md and git after every stage and every Stage 3 room.
argument-hint: "[--run YYYY-MM-DD] [--only-room <slug>] (resume a run folder; dry-run one room)"
disable-model-invocation: true
model: claude-opus-5-5
effort: max
---

# /funnel-run: Stages 1–6, red team, audit packet

Arguments: `$ARGUMENTS`. `--run` reuses a run folder (resume). `--only-room <slug>` is a dry run of Stages 3–6 on one room: it needs a run whose `01_rooms.json` and `02_mask.json` keep that room, it runs in its own folder `runs/<date>-dry-<slug>` (pass `--run <date>-dry-<slug>` to every command, plus `--dry-run`), and its outputs are never the real run (`rooms-known`, `compare` and `audit-status` skip such folders; `funnel status` marks them `(dry run)`).
`funnel` means `python3 <repo>/opportunity-funnel/pipeline/funnel.py --run RUN`. Stay inside `opportunity-funnel/`.

**Standing rules for the whole run**
- Never ask or wait for the founder. On ambiguity choose the conservative option and log it: `funnel log --stage N --note "<choice>" --review`.
- Depth over speed. Never shrink a sample to save time. Use Claude Opus 5.5 (`claude-opus-5-5`) at max effort for everything: this session, every subagent (listeners, walkers, search runners, commit helpers) and all bulk labeling. Pass model `claude-opus-5-5` and effort `max` to every subagent; never use Fable or a smaller model.
- Run independent units in parallel (rooms in Stage 3, pains in Stages 4–6).
- **Checkpoint** after every stage and after every Stage 3 room: run `funnel progress`, update the hand-written "Done / Next" lines of `PROGRESS.md`, then `git add -- <repo>/opportunity-funnel && git commit -m "funnel: checkpoint <what>" && git push` (on a git lock, wait a few seconds and retry).
- On resume ("continue"): read `PROGRESS.md` and `funnel status`; skip every finished step.

## 0. Preflight
`funnel preflight` and `funnel ledger-check`. Log blocked domains and missing keys (they go to REVIEW with what each would add). Read `graveyard.md` (`funnel graveyard`).

## Stage 1: Rooms (80–120, six lenses, gap pass)
1. In parallel, one agent per lens (`life_stage`, `profession`, `transition`, `obligation`, `business_type`, `identity_community`) writes `RUN/01_rooms.parts/<lens>.json`: 16–22 rooms worldwide, each with name, who, where they gather (named places with URLs), who pays, size (`measured` with URL or `estimate` with reasoning), ladder (paid problems in order, with prices where found), geography (descriptive only), `venture_overlap`. Ground places, sizes and prices with WebSearch. Invent nothing. Geography is never a filter. Skip graveyard rooms unless revived.
2. If `config/rooms_external.md` exists, one agent converts it into `RUN/01_rooms.parts/external.json` (`origin: external`).
3. `funnel rooms --merge-parts`. Then the **gap pass**: in parallel, one agent per lens reads `01_rooms.md` and asks "which rooms are missing from this lens?", writing `RUN/01_rooms.parts/gap_<lens>.json` (`origin: gap_pass`).
4. `funnel rooms --merge-parts` again. Resolve near-duplicates it lists by setting `duplicate_of`, rerun until it passes (80–120 rooms, lens balance). Checkpoint.

## Stage 2: Room mask (≤15 rooms)
1. FX: search the current exchange rate of every currency the rooms use against USD; write `RUN/fx_rates.json` (URL, date, `seen_via`). `funnel fx`.
2. In parallel, one agent per group of about 8 rooms writes `RUN/02_mask.parts/<n>.json`: reach kind (warm = a ledger warm id; search = the room already buys this kind of product via search, app stores or public marketplaces, with an evidence URL), depth id, spend (a concrete price people in the room pay, `price_text` exact, URL), supply, exclusions (licences the founder lacks; employer overlap), trust needed. Judgment only.
3. `funnel mask --merge-parts`. Checkpoint.

## Stage 3: Listen to saturation (one listener per room, rooms in parallel)
For each kept room, loop over rounds r = 1, 2, … until saturated, exhausted (a round adds fewer than `exhausted_round_new_records`) or `max_rounds`:
1. `funnel-listener`, mode `plan`, round r → new queries in `queries.jsonl`.
2. Harvest: split the round's queries into groups of about 50; one plain agent per group runs each query with WebSearch exactly as written, 10 in parallel per message (nothing else). Their results land in the session transcripts.
3. `funnel-listener`, mode `label-prep`, round r → `harvest-search`, `batches`, the taxonomy, the batches to label (`funnel label-todo`) and, when it added pains in a later round, packs of earlier member records to re-check (`funnel relabel-pack`).
4. One `funnel-listener` per listed batch, mode `label-batch`, and one per pack, mode `label-pack`, in parallel → `labels/<batch>.jsonl` (checked with `funnel count --room R --batch B`) and `labels/_patches/<pack>.jsonl` (checked with `funnel apply-patches --room R --check P`). Labelers never edit the taxonomy; they suggest missing pains.
5. `funnel-listener`, mode `label-finish`, round r → `apply-patches`, `count`, `saturation`. A round in which labelers suggested a pain is not saturated; the next `label-prep` decides on the suggestions.
Then `funnel-listener`, mode `synthesize` (with the stop reason) → `pains_draft.json`, `sources.json`, quotes checked. Checkpoint after each room. The workflow `pipeline/workflows/stage3-listen.js` runs all of this per room.
When all rooms are done: `funnel pains`. Checkpoint.

## Stage 4: Walk (two independent walkers + a comparator per pain)
For each kept pain, in parallel: two `funnel-walker` agents in mode `walk` (letters `a` and `b`, neither sees the other; each checks its own file with `funnel walks --check <pain_id> --walker <letter>`), then one in mode `compare` (merges conservatively and drafts 2–3 alternative pairs). Then `funnel walks`. Checkpoint.

## Stage 5: Pair
`funnel pairs` (keeps the strongest valid alternative per pain; kills pains with none). Checkpoint.

## Stage 6: Numbers
For each Stage 5 survivor, in parallel: `funnel-walker`, mode `numbers`. Then `funnel price-check --stage 6` and `funnel numbers`. Checkpoint.

## Red team
For each survivor, in parallel: a fresh agent that has not seen earlier reasoning. Give it only the survivor's room, offer, price, channel and hypothesis. It searches the web for the strongest case against: competitors already doing it, past attempts that failed and why, reasons the pain isn't actually paid for, legal or platform risks; every point with a URL. It writes `RUN/07_red_team/<pain_id>.json`. `funnel redteam`. Then one judge agent reads the red-team files and the survivors and writes `RUN/07_audit_packet/case_against.json` (re-rank only when a sourced point is material; one line per change). Checkpoint.

## Outputs
`funnel audit-packet` (files only; do not show it), `funnel shortlist`, `funnel review`, `funnel runlog`, `funnel status`, `funnel progress`. Commit with `funnel commit-message`, push. In a cloud session, open a pull request that changes only this folder (plus the pointer files).

## Final message to the founder
1. Summary: rooms generated, rooms kept, pains found, pains left after the walk, survivors; records per room; where saturation was reached; sources skipped and why.
2. Ranking table of survivors: hypothesis, lane, USD per hour (low / base / high), time to first payment, evidence strength, confidence.
3. The full `SHORTLIST.md`.
4. Recommendation: which survivor to test first (two sentences) and what evidence would change your mind.
5. If nothing survives, say so plainly; show the five closest candidates and exactly what killed each.
6. The `REVIEW.md` list.
