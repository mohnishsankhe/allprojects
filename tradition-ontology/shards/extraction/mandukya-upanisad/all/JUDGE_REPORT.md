# Judge report (Role J): Māṇḍūkya Upaniṣad and Gauḍapāda's Kārikā (protocol insight-p1-single+spot)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**What was written**
- `shards/extraction/mandukya-upanisad/all/final/`: the same six files as single/.
- `shards/extraction/mandukya-karika/all/final/`: the same nine files as single/.
- `…/all/fidelity.jsonl` in each folder:
  - one line per teaching: 13 for the Upaniṣad and 219 for the Kārikā;
  - plus entity-check lines: 9 for the Upaniṣad and 46 for the Kārikā.
- My scripts are outside the project, in the session scratchpad.

## Step 1: originals, checked by code
- Every `original.text` equals its segment's `iast`: 12 of 12 in the Upaniṣad and 214 of 214 in the Kārikā. There are 0 mismatches and no commentary excerpts.
- The summary entries (Upaniṣad thesis; Kārikā ch1–ch4 and thesis) have no original. I checked their cited refs against the segments instead.
- No teaching links a restricted practice. I checked this against the `restricted` flag in data/practices.json, which marks 130 ids.
- Every linked id resolves, in data/ or in the shards, both before and after the fixes.

## Step 2: sample (seed 20260929, `random.Random`)
**Upaniṣad**
- 13 teachings, split in file order into 5 strata with one pick per stratum.
- Picked: MU 2, 5, 8, 10, 11. There are no low-confidence entries.

**Kārikā**
- 10% of 219 is 22 (above the minimum of 20). I stratified by prakaraṇa with proportional allocation: 3, 4, 5 and 10. The ch entries sit in their own prakaraṇa; the thesis sits outside the strata.
- Picked:
  - prakaraṇa 1: 1.13, 1.17, 1.24;
  - prakaraṇa 2: 2.10, 2.19, 2.29, 2.31;
  - prakaraṇa 3: 3.5, 3.16, 3.24, 3.31, 3.39;
  - prakaraṇa 4: 4.2, 4.40, 4.55, 4.57, 4.58, 4.59, 4.65, 4.75, 4.76, 4.87.
- I added all 20 low-confidence entries. 2.29 is in both sets.

**What I checked in each entry**
- Is the paraphrase faithful to the Sanskrit?
- Is any Śaṅkara, Ānandagiri or other commentator's reading given as plain sense?
- Does it give a verdict on the Buddhist-sounding vocabulary?
- Does it use modern psychology?
- Are the tags, types and `reported_by_opponent` flag right?
- Do the linked ids have the right sense?

## Step 3: acceptance
The random samples were below 95% in both texts, so every entry was checked individually and all are promoted in mode "individually-checked".

| | Upaniṣad | Kārikā |
|---|---|---|
| Random sample faithful as written | 3/5 (60%) | 16/22 (72.7%) |
| Random-sample failures | MU 10, 11 | 1.24, 2.31, 3.16, 3.24, 4.40, 4.87 |
| All teachings faithful as written | 8 | 165 |
| All teachings fixed | 5 | 54 |
| Low-confidence entries | none | 11 faithful, 9 fixed |

- In the Upaniṣad, MU 5 got a J note only.
- The 9 fixed low-confidence entries are 1.6, 1.18, 2.8, 2.34, 4.15, 4.24, 4.43, 4.78 and 4.82.
- In the Kārikā, 34 of the 54 fixes change the paraphrase; the rest change notes, tags, flags or a link.

Every change is logged in the entry's `correction_log` (field, old, new, reason, by J, date), and in the `fix` field of fidelity.jsonl.

## Fixes by kind
1. **A commentators' reading given as plain sense.** In most cases the extractor's own note already said it was the commentators' reading.
   - pravivikta as "subtle": MU 4; Kārikā 1.3 and 1.4.
   - ubhayatva as "in-between": MU 10; Kārikā 1.20; the Upaniṣad thesis.
   - "[the self]" supplied as the object at 1.18.
   - "he [who so holds]" at 3.1.
   - Worship narrowed to "the lower and middle" at 3.16 (note and stage tag), ch3 and the Kārikā thesis.
   - "[real]" at 3.18.
   - "[seen as]" at 4.29.
   - "for the knower" in the 3.43 note.
   - At 3.36 the misprint "anindram" was given as the Sanskrit and "sleepless" labelled a commentators' reading. It is the evident text ("anidram", as at 1.16 and 4.81).
2. **Grammatical misconstruals.**
   - 1.18: the masculine "kalpitaḥ" agrees with "vikalpaḥ", not with a supplied "[duality]".
   - 2.1: "svapne" is a locative ("in dream").
   - 2.8: "sthānidharmaḥ" is a nominative compound.
   - 2.31: "svapnamāye" is a dual, giving three images, not one.
   - 2.34.
   - 3.3: "saṃghātaiḥ" parallels "jīvaiḥ".
   - 4.23: "anādeḥ" is an ablative.
   - 4.24.
   - 4.40: "sad asaddhetukam" completes the four combinations of real and unreal.
   - 4.45: the "-ābhāsam" words agree with "vijñānam".
   - 4.82: "bhagavān asau" is the nominative subject of the passive verbs, and sukham/duḥkham are adverbs.
   - 4.94: the wretched are persons, not doctrines.
   - 4.98.
3. **Additions not in the verse.**
   - 1.24: "think of nothing else" (the verse says "not think of anything at all").
   - 3.24: "by māyā alone".
   - The Upaniṣad thesis: "Oṃ is the means of seeing this", and "turīya", a word the Upaniṣad does not use.
   - 4.83: the tetralemma formula "neither exists nor does not exist" for "nāsti nāsti".
   - 4.87: "purely worldly" for śuddha laukika, which inverts the grade.
   - ch4 and the Kārikā thesis: "both or neither" and "fourfold denial" at 4.22.
4. **A construal chosen silently, or against the context.**
   - 1.6: "Some are certain", `reported_by_opponent` true and standpoint polemical. The verse does not mark itself as others' view; 1.7 then opens with "tv anye" ("but others").
   - 1.27: the paraphrase chose "immediately" although its note said it kept the neutral wording.
   - 4.42: I restored the skeleton's single-sentence reading and recorded the extractor's two-statement split as an alternative. Confidence goes from high to moderate.
   - 4.43.
   - 4.67: the edition's word division reverses the sense and was not flagged. Confidence goes from moderate to low.
   - 4.78: "buddhvā 'nimittatāṃ" (the absence of a basis). "Signhood as true" contradicts the verse's own second clause.
   - 3.26: the note misdescribed what the paraphrase does.
5. **Tags, flags and links.**
   - Level ultimate → conventional for means and instructions: MU 9–11; Kārikā 1.24 and 3.40–3.45. This follows principles.md, where conventional covers "the path itself", and the DECISIONS convention that a means and its result are conventional.
   - `reported_by_opponent` true → false where the verse is the author's own argument: 1.6, 3.17, 4.11–4.18 and 4.20.
   - 3.16: stage → all.
   - 1.6: standpoint → cosmic.
   - trm:catuskoti-gk removed from 4.22.
6. **Summaries.** ch1 (1.6), ch2 (2.6 had been inverted), ch3, ch4 and both theses.

## Entities
- Levels are not raised. Every entity got a `verification.checks` record (phase J).
- **Upaniṣad, 31 entities:** 23 confirmed, 5 corrected, 3 partially-confirmed (their rename is not confirmed).
- **Kārikā, 160 entities:** 132 confirmed, 16 corrected, 12 partially-confirmed. A further 3 of the corrected entities are also unconfirmed renames.
- **Corrections:**
  - "subtle" in cpt:three-states-and-turiya, trm:taijasa and trm:praviviktabhuj, in both texts;
  - "in-between" in cpt:omkara-matras and trm:matra;
  - cpt:ajativada (the 4.22 wording);
  - "residue" in cpt:manonigraha-obstacles;
  - cpt:gk-fourfold-denial and trm:catuskoti-gk (4.22 is not the four-corner list of 4.83–4.84; 4.22 removed from `rests_on`);
  - cpt:gk-three-grades-of-knowing;
  - trm:vikalpa, trm:krpana-gk, trm:upasana-gk, trm:kosa, trm:aja-gk;
  - dsp:gk-creation-theories (1.6 moved out of the unnamed side);
  - in the Upaniṣad, trm:prajna-mandukya and trm:antaryamin, which stated the commentators' referent of MU 6 as fact.

## The -gk/-mu renames and obstacle senses
**Confirmed (13):**
- trm:kasaya-gk, alata-gk, sanirvana-gk, samkalpa-gk, prapanca-gk, ksanti-gk, avatara-gk, abhasa-gk, asrama-gk, upacara-gk, prajna-gk, prc:omkara-dhyana-mandukya and phn:gk-the-fourth.
- Caveat on trm:prajna-gk: data trm:prajna mixes prājña and prajñā.
- Caveat on trm:kasaya-gk: data trm:kasaya has a lin:advaita-vedanta definition ("Latent attachment", a commentators' gloss) that rests on tea:mandukya-karika:3.44. It should move to trm:kasaya-gk at merge, or the Kārikā's kaṣāya will have two ids.

**Not confirmed (18).** Each has the right sense, but the base id in data/ already has a lineage definition with that sense:
- trm:vaisvanara-mu and cpt:vaisvanara-mu: the base entries already cite MāU 3.
- trm:aksara-mu: the base entry already cites MāU 1.
- cpt:pranava-gk.
- cpt:maya-gk: the base lin:advaita-vedanta definition rests on Kārikā 1.17.
- trm:akasa-gk, svabhava-gk, citta-gk, manas-gk, buddhi-gk, paramartha-gk, jnana-gk, aja-gk, upasana-gk, upaya-gk, krpana-gk, nirvikalpa-gk, tattva-gk.

In several cases the extractor's report named only a non-matching lineage as the reason (BhG 15.14 for vaiśvānara, Yogācāra for paramārtha, the she-goat for aja). I left these ids unchanged in final/, where they resolve. The merger should fold them into the base ids as lineage contributions.

**Obstacles.** obs:laya, obs:viksepa, obs:kasaya, obs:rasasvada and obs:four-obstacles-to-samadhi are the Gauḍapāda referents: the data entries already rest on Kārikā 3.44–3.45. But the data names and descriptions carry commentators' or Vedāntasāra glosses ("latent attachment", "dullness", "savikalpa", "nirvikalpa samādhi"). The shard contributions avoid them and should be the Kārikā's line at merge.

## Skeleton decisions
- Copied to final/. Every `replaced_by` exists in the final teachings: 9 in the Upaniṣad and 33 in the Kārikā. Every data teaching of both sources has a decision.
- Kārikā 4.42 changed from "correct" to "upgrade", with a `j_note` explaining why.
- The extractor's report says 23 upgrade and 10 correct, but its file has 25 upgrade and 8 correct. After my change it is 26 and 7.

## Validation
`scripts/validate_shard.py` on both final/ folders: 0 errors and 1 warning each (REPORT.md missing; this report comes back as text instead).

## Could not check, and open points
- **Commentators' claims in notes.** I could not verify the "commentators read …" statements: the ontology has no Śaṅkara or Ānandagiri entries for these verses apart from one skeleton entry (4.99). They are labelled as commentators', as the rule requires. I removed one unverifiable claim (1.6).
- **Verse 2.22 has no ref.** Segment 2.23 holds 2.22 and 2.23 together, so a citation of Kārikā 2.22 will not resolve. This is a segmentation or citation-resolution task.
- **nimitta.** 4.75 and 4.77 keep "signless", which is lexically possible. "Without basis" fits 4.25–4.27 and 4.76 better; worth a consistency pass.
- **Level tags.** I changed only verses that are clearly instructions or means. Mixed verses (1.22, 1.25, 1.27, 1.28) keep "ultimate". If the orchestrator rejects the means-and-result convention, the level changes can be found by their `tags.level` entries in `correction_log`.
- **Edition misprints.** These are noted and left in the originals, by design: MU 5 evāndamayo; Kārikā 1.10 devās, 1.29 netāro, 3.5 ghāṭ-, 3.36 anindram, 4.33 kāyasyānta, 4.72 cittaspandikam; and 1.5, 1.21, 2.16, 4.15, which the extractor already noted.
- **Shared scratchpad.** The session scratchpad is shared with another agent that was running at the same time. It overwrote my sample.json; I regenerated it identically in a private subfolder. My early scratch files with generic names (show.py, rng.py, links.py, sample.py, ents.py) may have overwritten that agent's files of the same names. Nothing inside the project was affected.
