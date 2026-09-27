# Brief — interpretation-layer synthesis across the whole skeleton (end of Phase B, and after every wave)

These passes read the MERGED data (`data/*.json`, `data/teachings/*.jsonl`, `data/reports/dangling.json`) and write
interpretation-layer shards to `shards/synthesis/<PASS>/` (same schemas; `scripts/merge.py` merges them in). They
never edit text-layer teachings. Every interpretive link carries `rests_on` teaching ids and a line in
`interpretation_log.jsonl` (use `scripts/shardlib.py`: `Shard("synthesis", "<PASS>")`, `sh.log(...)`).
Read first: `CLAUDE.md`, `config/principles.md`, `config/data_model.md`. Never touch anything outside
`tradition-ontology/`; never run git. Validate with `python3 scripts/validate_shard.py shards/synthesis/<PASS>`.
Final reply ≤5 lines.

## S1 — The ultimate (`ult:*`, `cpt:the-ultimate`)
1. Make sure every lineage in `data/lineages.json` that teaches about the ultimate has a view (`ult:<lineage-slug>`);
   write missing views from the lineage's own texts (skeleton level, honest confidence), including traditions that
   deny a single ultimate (say so in `tradition_denies_single_ultimate` and `caveat`).
2. Write `cpt:the-ultimate` (category `ultimate`) with `names` per lineage and `relations` of kind
   `same-as-under-standpoint` between views ONLY where a principle genuinely applies (P1 level, P2 standpoint, …),
   each with `standpoint`, a one-line `note` naming the principle, `rests_on`, and the objection of each tradition
   that rejects the identification. Where no principle applies, write a dispute with `status: "queued"`.

## S2 — Obstacles (`obs:*`)
Align kleśas, hindrances, fetters, passions, guṇas as obstacles, doṣa imbalances, malas, kaṣāyas, the nine
antarāyas, the five hindrances, the ten fetters, the three poisons, distraction and dullness, the Tibetan five
faults, Zen sickness, and every other named obstacle. Add `equivalents` (graded exact / partial /
same-under-standpoint / analogous / contested) between obstacles of different lineages, each with `rests_on` and a
note on what differs. Add a concept `cpt:obstacle-families` whose `members` are the families you use (e.g.
ignorance/misapprehension; craving/attachment; aversion; I-making/pride; doubt; dullness/torpor; agitation/
distraction; wrong view; clinging to life/fear; impurity of action; bodily imbalance) and relate each obstacle to its
family by a `relations` entry (`corresponds-to-in-map`). Never force an equivalence a tradition would refuse.

## S3 — Path maps (`pth:*`, `cpt:path-map-correspondence`)
Check every path map's stages and bands for consistency across maps; fix bands (logged) where a map is banded
inconsistently with its own texts; add `equivalents` between maps' stages where the traditions themselves draw the
correspondence (e.g. Haribhadra's eight views ↔ Patañjali's limbs; Kālacakra six branches ↔ Maitrī six limbs) and
where a principle genuinely supports it. Record every map whose tradition rejects stage-alignment (sudden schools,
Dzogchen, Dōgen) in the concept's notes.

## S4 — Practices (`prc:*`)
Add `equivalents` between practices of different lineages that teach the same method (e.g. breath-awareness,
mantra repetition, the four immeasurables, death contemplation, sense withdrawal, inner-sound listening, deity
visualization, witness practice / self-inquiry, confession), graded, with notes on what differs, `rests_on`, and the
texts' warnings preserved. This makes cluster convergence counts possible.

## S5 — Terms and concepts
Find duplicate or near-duplicate ids (e.g. `trm:dhyana` / `trm:jhana` created separately; `cpt:self` vs `cpt:the-self`)
and link them (`equivalents` for terms; `relations` `same-as-under-standpoint` or `is-a` for concepts) — never merge ids
yourself. Complete cross-language forms for the central ~300 terms. Resolve the most-referenced dangling ids in
`data/reports/dangling.json` by writing the missing entries (skeleton level, honest confidence) or noting the
correct existing id in `shards/synthesis/S5-terms/aliases.md`.

## S6 — Reconciliation pass
Go through every dispute whose status is `queued` and every pair of teachings flagged `differs_from`; reconcile
where one of P1–P8 genuinely applies (one-line explanation naming the principle; the traditions' objections
recorded), otherwise leave queued and improve the candidate readings. Never call anything a contradiction.
