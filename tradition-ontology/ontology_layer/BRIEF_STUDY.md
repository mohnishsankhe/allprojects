# Brief: Study unit (the whys)

You are building one unit of the **ontology layer**: the workings ("whys") that the Study texts of the Vedic and
ascetic traditions state, written as cited cause-and-effect links. Read `ontology_layer/SCHEMA.md` first: it defines
every field, the relations, the engine layers and the families. Follow `CLAUDE.md` in `tradition-ontology/`.

## Your inputs (in `ontology_layer/_inputs/<unit>/`)
- `rows.json`: your catalog rows. For each: `text`, `what` (what it talks about), `why_this_tier` (the why the catalog
  says this text holds), `feeds_layer` and `also_feeds` (the engine layers the catalog tagged), `scope_note`,
  `passages_tiered_differently`, `teaching_count`. Rows with `extra_why_passages_only: true` are Read rows where only the
  flagged passages are Study: write whys for those passages only.
- `teachings.jsonl`: every teaching in your rows' scope, one per line: `row`, `id`, `ref`, `level`
  (text-verified / sourced / skeleton), `types`, `paraphrase`, and the `concepts`, `terms`, `obstacles`, `practices` ids
  it links to. **The paraphrase is your evidence.** Read the whole file, in chunks.
- `vocab.jsonl`: names and one-line glosses of the ids those teachings link to. Search it with grep; do not read it all.
  For anything else, grep `data/concepts.json`, `data/terms.json`, `data/obstacles.json`, `data/practices.json`.

## What to write (in `shards/ontology_layer/<unit>/`)
1. `whys.jsonl`: the workings each Study row states.
2. `results.jsonl`: the results (methods, conduct, counsel, devotion, mantra, regimen, signs, warnings) that the **same
   Study texts** give, each tied to the why in your unit that explains it. Many Study texts hold both: the Yoga Sūtra's
   eight limbs rest on its account of the afflictions; Caraka's daily regimen rests on its doṣa theory.
3. `nodes.jsonl`: only the things your whys connect that have no id in `data/` yet.
4. `REPORT.md`: see the end.

## How to work, row by row
1. Read the row's fields, then its teachings.
2. Write its whys, in this order of priority:
   - first, what `why_this_tier` names;
   - then every link that bears on a person's state and action (layers `L0` to `L7` and `M`);
   - then the world-model links (`W`): how the world arises, what exists, cosmology, theology.
3. Write the results the row itself gives, with `rests_on` pointing to your whys (`link: same-text` when this text states
   the why; `same-tradition` when another of your rows does).
4. Append the lines to the files as you finish each row, so partial work survives. Run the checker every few rows:
   `python3 scripts/ontology_layer_check.py shards/ontology_layer/<unit>`.

**How many.** A big systematic text (100 or more teachings in scope): 25–80 whys. A medium one (20–100): 8–30. A small one
(under 20): 3–12. A row with **no teachings** in the ontology: 3–8 whys at `basis: outline`, written from your knowledge
of the text, each with a `ref_hint` and an honest confidence. Never pad: a why must carry a real working.

## Fidelity rules (these are the job)
- **Say only what the cited passage says.** The statement restates a link the paraphrase states. If you need two passages
  to get the link, use `basis: inferred` and say how in `notes`. Do not put a commentary's reading into a root text's
  why unless you cite the commentary's own teaching.
- **One link per why.** A chain is several whys. Do not split a list into one why per item unless each item has its own
  stated working; a list that carries a working is one `part-of` or `composed-of` why plus the whys of its working.
- **The traditions' own terms.** Plain English with the native term in brackets: "heaviness (tamas)", not "low energy".
  No modern psychology, medicine or science, and no health claims of your own. Body and cosmos claims (`claim: body`,
  `cosmos`) are what the tradition says; word them so ("Caraka holds that…").
- **Never invent a locator.** In `ref_hint`, give only what you are sure of; chapter level is fine. If you are reconstructing
  rather than recalling, set `confidence: low`.
- **Nodes.** Use an existing `data/` id for `subject`, `object` and `targets` whenever one fits (grep `vocab.jsonl` first,
  then `data/`). Make an `nd:` node only when none fits, and keep each tradition's node its own: the Yoga Sūtra's
  `saṃskāra` and the Abhidharma's `saṅkhāra` are different nodes unless the data already merges them.
- **Layers.** Tag the layer the why explains, using SCHEMA.md's table. `L3` (centres, channels, vital points) is a place,
  never a cause: a why may say a wind moves in a channel (`seated-in`), not that a centre causes a mood. `W` stands alone.
- **`shows_as`** (for `L1`–`L7` whys): how the condition shows in a person, **only as the text describes it**, with cites.
  These become intake signals later, so they matter. **`test`**: the tradition's own test in experience, when it gives one.
- **Restricted practices** (CLAUDE.md rule 11) in results: `restricted: true`, a summary only, and the texts' own warnings.
  If a text says a practice needs a teacher or initiation, put that in `warnings`.
- **`corresponds`**: only to other whys in your own unit for now. Cross-tradition links are a later pass.

## Ids and families
`why:<family>:<slug>`, `res:<family>:<slug>`, `nd:<family>:<slug>`. The slug is lowercase ASCII with hyphens, at most
60 characters, and says the link ("vata-provoked-by-grief", "avidya-field-of-the-afflictions"). Your unit's families
are given in your task. Ids must be unique in your unit.

## Rules
- Write only inside `shards/ontology_layer/<unit>/`. Never write to `data/` or anywhere else. Do not commit.
- Never ask questions or wait. If something is ambiguous, take the conservative reading and note it in `REPORT.md`.
- Budget about two hours of work. If you run long, finish the rows whose `feeds_layer` is not "World model only" first.
- Finish with the checker at zero errors.

## `REPORT.md`
- A table: row number, text, whys, results, and the basis mix (stated / inferred / outline).
- Rows done only at outline level, and why.
- **Passages the ontology lacks**: for each, the text and locator and why it matters. These feed the extraction queue.
- Anything you doubted, and the reading you took.
- Your final message: five lines at most, with the counts and the checker result.
