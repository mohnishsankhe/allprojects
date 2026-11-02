# Brief: Read unit (the results)

You are building one unit of the **ontology layer**: the results that the Read texts of the Vedic and ascetic
traditions give (what to do, the signs and the warnings), each tied to the Study "why" it rests on. The whys are
already built. Read `ontology_layer/SCHEMA.md` first: it defines every field. Follow `CLAUDE.md` in `tradition-ontology/`.

## Your inputs
- `ontology_layer/_inputs/<unit>/rows.json`: your catalog rows. For each: `text`, `what`, `why_this_tier`,
  `why_lives_in` (**the Study family or text where the catalog says this row's why lives**: start your search there),
  `feeds_layer`, `also_feeds`, `scope_note`, `passages_tiered_differently`, `teaching_count`.
- `ontology_layer/_inputs/<unit>/teachings.jsonl`: every teaching in your rows' scope: `row`, `id`, `ref`, `level`,
  `types`, `paraphrase`, and linked ids. **The paraphrase is your evidence.** Read the whole file, in chunks.
- `ontology_layer/_inputs/<unit>/vocab.jsonl`: names of linked ids. Grep it; do not read it all.
- `ontology_layer/_inputs/WHY_INDEX.tsv`: every why the Study units wrote, one per line:
  `id`, `family`, `layers`, `relation`, `subject`, `object`, `statement`. **Grep it** by family (`^why:hatha:`), by node id,
  or by keyword. The full records are in `shards/ontology_layer/S*/whys.jsonl` if you need a why's cites.

## What to write (in `shards/ontology_layer/<unit>/`)
1. `results.jsonl`: the results of every row in your unit.
2. `whys.jsonl`: **only** when a Read text states a working of its own that the index lacks (check first). Use your
   own families. Keep these few.
3. `nodes.jsonl`: only for things with no id in `data/` yet.
4. `REPORT.md`: see the end.

## How to work, row by row
1. Read the row's fields, then its teachings.
2. Write one result per **distinct** teaching about what to do (or a sign, or a warning). Merge repeats into one result
   and cite every teaching that states it.
   - `kind`: `method`, `conduct`, `counsel`, `devotion`, `mantra`, `ritual`, `regimen`, `sign`, `warning`.
   - `for`: the condition or aim it works on, in plain words. This is what the engine matches a person against, so make
     it concrete ("anger that flares at an insult", "a mind that scatters at the start of a task").
   - `suits` / `not_for`: who the text says the result is for, and who should not do it or when not to: the seeker's
     stage, temperament, constitution (doṣa), strength or capacity (adhikāra). Examples: BhG 6.3 (action is the means for
     one still climbing, calm for one who has arrived); HYP 2.21 (the cleansing acts only for one with excess fat or
     phlegm; one whose humours are balanced should not do them). Fill these only when a cited passage says so, with its
     cites; otherwise leave them empty. They are the conditions the engine routes people by, and they are where the texts
     settle what looks like disagreement between traditions.
3. Tie each result to the why it rests on (`rests_on`):
   - `same-text`: this text itself states the reason (cite it in the result);
   - `same-tradition`: a Study why of the same tradition explains it (start with `why_lives_in`);
   - `other-tradition`: only when the text itself borrows that frame, or `why_lives_in` names that family.
   - Pick the why that actually explains how the result works, not one that merely shares a word. One to three links
     is normal.
   - **If no why fits, leave `rests_on` empty and fill `why_gap`** with what the missing why would have to explain.
     Gaps are useful; a forced link is a failure.
4. Append lines as you finish each row. Run the checker every few rows:
   `python3 scripts/ontology_layer_check.py shards/ontology_layer/<unit>`.

**How many.** A big row (100 or more teachings): 30–100 results, putting first what bears on a person's state and action.
A medium row (20–100): 8–30. A small row (under 20): 2–10. A row with **no teachings**: 2–5 results at
`basis: outline`, from your knowledge of the text, each with a `ref_hint` and an honest confidence. Never pad.
Teachings that are only story, praise or narrative get no result.

## Fidelity rules
- **Say only what the cited passages say.** No added steps, durations, benefits or reasons.
- **The traditions' own terms**, in plain English with the native term in brackets. No modern psychology, medicine or
  science, and no health claims of your own. Regimen and body claims are what the tradition says; word them so.
- **Never invent a locator** in `ref_hint`; chapter level is fine. Reconstructing rather than recalling: `confidence: low`.
- **Restricted practices** (CLAUDE.md rule 11: body-cutting, metals or mercury, extreme breath retention, sexual rites,
  prolonged fasting, and the advanced energy practices such as khecarī and vajrolī): `restricted: true`, a summary only,
  never steps, counts or durations, and the texts' own warnings in `warnings`.
- **Teacher or initiation**: if the text says a practice needs a guru or initiation (dīkṣā), record it in `warnings`.
- **Mantra**: record which mantra or kind of mantra the text gives, what it is for, and how the text says to use it
  (repetition, meditation on its meaning, the conditions it sets). Note any initiation requirement.
- **Signs and tests**: when the text says how to tell a practice is working, put it in `test`.

## Ids and families
`res:<family>:<slug>` (and `why:` / `nd:` for the rare new ones). The slug is lowercase ASCII with hyphens, at most 60
characters. Your unit's families are given in your task. Ids must be unique in your unit.

## Rules
- Write only inside `shards/ontology_layer/<unit>/`. Never write to `data/` or anywhere else. Do not commit.
- Never ask questions or wait. If something is ambiguous, take the conservative reading and note it in `REPORT.md`.
- Budget about two hours of work. If you run long, finish the rows whose `feeds_layer` is not "World model only" first.
- Finish with the checker at zero errors.

## `REPORT.md`
- A table: row number, text, results, how many have `rests_on`, how many have a `why_gap`.
- The why gaps, grouped: what kinds of whys the Study layer is missing.
- Rows done only at outline level. Passages the ontology lacks (text and locator).
- Anything you doubted, and the reading you took.
- Your final message: five lines at most, with the counts and the checker result.
