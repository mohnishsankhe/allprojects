# Ontology layer: schema

The ontology layer is built only from the 604 **Study** and **Read** rows of the tier catalog
(`catalog/text-tiers-described.csv`). It sits on top of the ontology in `data/` and never changes it.

- **Study texts** state the workings: how things work and why (the *whys*).
- **Read texts** state the results: what to do, the signs and the warnings. Every result is tied to the why it rests on.

It is an interpretation layer (CLAUDE.md rule 9). Every link cites the teachings in `data/teachings/` it rests on.
Skim and Index texts are left out.

## Files

| File | What it holds | Written by |
|---|---|---|
| `register/texts.jsonl` | The 604 rows: tier, role, engine-layer tags, the texts each row maps to, its passage scope, the teachings in scope | `scripts/ontology_layer_register.py` |
| `register/units.json` | Which work unit handles which rows | same |
| `whys.jsonl` | The workings: one cause-and-effect or structural link per line | merged from `shards/ontology_layer/S*/` |
| `results.jsonl` | The results: what the texts teach to do, each with the why it rests on | merged from `shards/ontology_layer/*/` |
| `nodes.jsonl` | Things the whys connect that `data/` has no entry for yet | merged |
| `gaps.jsonl` | Results with no why found; whys the ontology has no passage for | merged |
| `graph/nodes.csv`, `graph/edges.csv` | The whole layer as a graph, for Neo4j or Gephi | `scripts/ontology_layer_merge.py` |
| `COVERAGE.md`, `QUEUE.md` | How much is verified, and what to extract next | `scripts/ontology_layer_report.py` |

## Engine layers (from the Map, Part A v2)

| Tag | Layer | What belongs here |
|---|---|---|
| `L0` | Gate | What makes it unsafe to read or advise: the texts' own warnings, illness as an obstacle, wrong practice causing harm |
| `L1` | Body | The food sheath; in Āyurveda the doṣas, tissues, digestive fire and wastes; pain, injury, sleep, appetite, bowels, energy |
| `L2` | Breath and the capacity to act | The breath sheath: the vital winds with the organs of action; breath, voice, movement, elimination, the drive to start |
| `L3` | Map | Places the other layers point to: centres (cakra), channels (nāḍī), vital points (marma). **A place, never a cause.** |
| `L4` | Mind | The mind sheath: the mind's activities and states, distraction and its companions, the obstacles, the mind's climate |
| `L5` | Drives and seeds | The afflictions (kleśa), latent impressions and tendencies (saṃskāra, vāsanā, anuśaya), the karmic store, triggers |
| `L6` | Resolve and action | The intellect sheath: decision, determination, steadiness, zeal; the agent, the factors of action, duty |
| `L7` | Knower and readiness | The witness or self; who one takes oneself to be; the seeker's readiness and capacity (adhikāra) |
| `M` | Method | How change happens: practice, dispassion, cultivating the opposite, the stages and order of practice |
| `W` | World model only | Cosmology, theology, metaphysics, ritual or law that shapes the picture of the world but not a reading of a person |

A why or result can carry several tags. `W` is used alone.

## Domains

`exists` (categories of reality) · `arising` (how the world arises) · `mind` · `consciousness` (consciousness and world) ·
`body` · `karma` (action and its results) · `suffering` (suffering and its end) · `transformation` (stages, what changes) ·
`cosmology` · `living` (conduct, values, the aims of life)

## Why: `whys.jsonl`

One link per line. A chain is several whys (A causes B; B causes C).

```json
{"id": "why:yoga-sutra:avidya-field-of-the-afflictions",
 "statement": "Not-seeing (avidyā) is the field in which the other four afflictions grow, whether dormant, thin, interrupted or active.",
 "subject": ["trm:avidya"], "relation": "conditions", "object": ["cpt:five-klesas"],
 "condition": "",
 "layers": ["L5"], "domain": ["mind", "suffering"], "claim": "inner",
 "shows_as": [{"text": "...", "cites": ["tea:..."]}],
 "test": {"text": "...", "cites": ["tea:..."]},
 "cites": ["tea:yoga-sutra:2.4", "tea:yoga-bhasya:2.4"],
 "basis": "stated", "ref_hint": "",
 "rows": [268], "tradition": "lin:yoga", "confidence": "high",
 "corresponds": [{"why": "why:pali:...", "grade": "partial", "note": "..."}],
 "notes": ""}
```

| Field | Required | Values |
|---|---|---|
| `id` | yes | `why:<family>:<slug>`; slug is lowercase ASCII with hyphens, at most 60 characters |
| `statement` | yes | One plain sentence saying the link as the text states it. Native terms in brackets. |
| `subject`, `object` | yes | Lists of node ids: an existing `cpt:`, `trm:`, `obs:` or `prc:` id from `data/`, or a new `nd:` id defined in `nodes.jsonl` |
| `relation` | yes | One of the relations below |
| `condition` | no | When the link holds |
| `layers` | yes | `L0`–`L7`, `M`, or `W` alone |
| `domain` | yes | One or more domains |
| `claim` | yes | `inner` (mind, experience, liberation), `body`, `cosmos`, `social`, `ultimate`. Body and cosmos claims are the tradition's claims, never presented as fact |
| `shows_as` | no | How the condition shows in a person, **as the text describes it**, with cites. These become intake signals later |
| `test` | no | The tradition's own test in experience, with cites |
| `cites` | yes for `stated` and `inferred` | Teaching ids that exist in `data/teachings/` |
| `basis` | yes | `stated`: the cited passage says this link. `inferred`: two or more cited passages together entail it (say how in `notes`). `outline`: the ontology has no teaching for it yet, so it is written from knowledge of the text; `ref_hint` is required and `cites` may be empty |
| `ref_hint` | for `outline` | The passage locator, as precise as you are sure of (e.g. `Caraka Sū 1.57`; chapter level if unsure) |
| `rows` | yes | Catalog row numbers the why comes from |
| `tradition` | no | A `lin:` id |
| `confidence` | yes | `high`, `moderate` or `low` |
| `corresponds` | no | Links to whys of other traditions that say the same thing: `exact`, `partial` or `analogous` |

**Relations**

| Relation | Meaning |
|---|---|
| `causes` | X brings Y about |
| `conditions` | Y needs X: X is its ground, support or necessary condition |
| `increases`, `decreases` | X raises or lowers Y (e.g. like increases like) |
| `obstructs` | X blocks or veils Y |
| `removes` | X ends or destroys Y |
| `opposes` | X is Y's contrary; cultivating X counters Y |
| `evolves-into` | X manifests or emanates as Y (Sāṃkhya, Pāñcarātra and Śaiva emanation) |
| `transforms-into` | X becomes Y |
| `leads-to` | Y follows X in a sequence the text gives (stages, links of a chain) |
| `sustains` | X keeps Y going |
| `seated-in` | X resides in or works from Y |
| `part-of`, `composed-of`, `is-a` | Structure |
| `has-quality` | X has quality Y |
| `sign-of` | X shows that Y is present |
| `known-by` | X is known through Y |

## Result: `results.jsonl`

```json
{"id": "res:gita:act-without-claim-to-the-fruit",
 "row": 152, "kind": "conduct",
 "statement": "Act, but never claim the fruit as yours, and do not cling to not acting either (2.47).",
 "for": "Anxiety over outcomes that stops or distorts action",
 "targets": ["nd:gita:attachment-to-fruit"],
 "rests_on": [{"why": "why:gita:attachment-to-fruit-binds", "link": "same-text", "note": ""}],
 "why_gap": "",
 "layers": ["L6"], "cites": ["tea:bhagavad-gita:2.47"], "basis": "stated", "ref_hint": "",
 "restricted": false, "warnings": [], "test": {"text": "...", "cites": []},
 "confidence": "high", "tradition": "lin:..."}
```

| Field | Required | Values |
|---|---|---|
| `id` | yes | `res:<family>:<slug>` |
| `row` | yes | The catalog row it comes from |
| `kind` | yes | `method` (a practice), `conduct` (how to live and act), `counsel` (how to see a situation), `devotion`, `mantra`, `ritual`, `regimen` (food, sleep, season, daily routine), `sign` (a sign of progress or of a condition), `warning` |
| `statement` | yes | What the text says to do, or the sign or warning it gives, plainly, with native terms in brackets |
| `for` | yes | The condition or aim it works on, in plain words |
| `targets` | no | Node ids of that condition |
| `rests_on` | yes, unless `why_gap` | `[{why, link, note}]`. `link`: `same-text` (this text states the why), `same-tradition`, or `other-tradition` (only when the text borrows that frame, or the row's `why_lives_in` names it) |
| `why_gap` | when no why fits | What the missing why would have to explain |
| `layers`, `cites`, `basis`, `ref_hint`, `confidence`, `tradition` | as for whys | |
| `restricted` | yes | `true` for body-cutting, metals or mercury, extreme breath retention, sexual rites, prolonged fasting and the advanced energy practices (CLAUDE.md rule 11). Then `statement` is a summary only and `warnings` carries the texts' own warnings |
| `warnings` | no | The texts' own warnings, with cites |
| `test` | no | The sign that it is working, as the text gives it |

## Node: `nodes.jsonl` (new nodes only)

```json
{"id": "nd:ayurveda:vata-provocation", "name": "Provocation of the wind principle (vāta-prakopa)",
 "native": "vātaprakopa", "kind": "process", "gloss": "...", "same_as": ["trm:vata"], "family": "ayurveda"}
```
`kind`: `quality`, `faculty`, `substance`, `tissue`, `channel`, `wind`, `place`, `state`, `affliction`, `latent-tendency`,
`process`, `principle`, `being`, `practice`, `other`. Use an existing `data/` id whenever one fits; make a node only when none does.

## Verification

Computed at merge from the cited teachings, never written by hand:
`text-verified` when every cited teaching is text-verified; `sourced` when every one is at least sourced;
`skeleton` when any is skeleton; `outline` when `basis` is `outline`. The engine may use only entries at
`sourced` or above for anything a person sees (layers/SCHEMA.md applies the same rule).

## Families (id prefixes)

`vedic`, `upanisad`, `brahmana`, `vedanga`, `mantra-nada`, `gita`, `epic`, `purana`, `ramayana`, `yoga-vasistha`, `dharma`,
`samkhya`, `yoga-sutra`, `nyaya-vaisesika`, `mimamsa`, `carvaka`, `surveys`, `vedanta`, `advaita`, `visistadvaita`,
`dvaita`, `bhedabheda`, `vallabha`, `pancaratra`, `bhagavata`, `gaudiya`, `alvar`, `varkari`, `mahanubhava`, `sant`,
`bhakti`, `pasupata`, `saiva-siddhanta`, `tamil-saiva`, `trika`, `spanda`, `pratyabhijna`, `krama`, `kaula`,
`virasaiva`, `sakta`, `srividya`, `hatha`, `ayurveda`, `rasa-sastra`, `aesthetics`, `music`, `jyotisa`, `vastu`,
`jain`, `pali`, `abhidharma`, `madhyamaka`, `yogacara`, `buddha-nature`, `mahayana`, `buddhist-logic`, `vajrayana`,
`siddha`, `tibetan`, `zen`, `tamil`, `later`
