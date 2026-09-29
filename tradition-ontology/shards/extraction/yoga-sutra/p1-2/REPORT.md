# Role S single extraction: Yoga Sūtra + Vyāsa bhāṣya, pādas 1–2 (1.1–2.55)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## What was done
- All 106 segments were read in the original. Every sūtra `original.text` is the segment's `iast` field, copied by code. Every bhāṣya `original.text` is an exact substring of `commentary_iast`.
- A code check found 0 mismatches over all 213 verse-level entries.
- Ids follow the brief: `tea:yoga-sutra:<ref>` and `tea:yoga-bhasya:<ref>` (source `src:yoga-bhasya`). Each sūtra entry cross-refs its bhāṣya entry, and each bhāṣya entry has `commentary_on`.
- Metadata: `extraction` is `{"method":"single","extractors":["S"]}`, and `verification` is `sourced` with `protocol` `insight-p1-single+spot`.
- Chapter entries `tea:yoga-sutra:ch1` and `ch2` are included.
- No `thesis` entry: the text is not complete in this chunk.
- The earlier draft (`_gen/S/t1.py`, refs 1.1–1.16) was reused. I found its bhāṣya anchors mismatched or untested in several places (1.1, 1.2, 1.5, 1.7, 1.8, 1.9, 1.10, 1.11, 1.16), so I re-anchored them so each `original` covers what its paraphrase states.
- `lib.py` was reused and extended (`ALL` anchor, `/2` and `/3` suffixes, slug normalisation, a fix so `pth` reaches the paths field).
- Scripts, in `_gen/S/`: `t1.py`–`t7.py`, `chapters.py`, `gloss.txt`, `build.py`, `fin.py`, `ent1.py`, `ent2.py`, `skel.py`. Run in that order: build, fin, ent1, ent2, skel.

## Diagnostic layer (the parts the Insight Generator will use)
- **Vṛttis 1.5–1.11:** each has its own sūtra and bhāṣya entry. Vyāsa's descriptions of how sleep shows itself on waking (1.10) and his bridge from the five activities to pleasure, pain and delusion and then to rāga, dveṣa and moha (1.11) are recorded. Entities: `cpt:five-vrttis`, `phn:ys-sleep-recollection`.
- **Antarāyas and companions 1.30–1.31:** the nine obstacles each have an obstacle entry with Vyāsa's gloss, plus `obs:nine-antarayas` and `obs:viksepa-sahabhuva`. The three kinds of pain, dejection, trembling of the limbs, and inhalation and exhalation are in `phn:ys-viksepa-sahabhu-shows`. "Illness" is recorded as Vyāsa's definition, not as a medical statement.
- **The four attitudes 1.33:** `prc:four-attitudes`, `cpt:four-attitudes`.
- **Kleśas and their states 2.3–2.11:**
  - Obstacle entries for the five, `cpt:four-states-of-klesas`, and one phenomenology entry per state (dormant, attenuated, interrupted, active), plus Vyāsa's fifth, burnt-seed state.
  - Vyāsa's own descriptions of how each shows itself (avidyā, rāga, dveṣa, abhiniveśa) are in `phn:ys-*-shows`.
  - The gross and subtle activities and their abandonment (2.10–2.11) are covered.
- **Duḥkha 2.15–2.16:** 2.15 is split into three bhāṣya entries: the three sufferings plus the eyeball simile; the guṇa-vṛtti conflict; the fourfold scheme (heya, heya-hetu, hāna, hānopāya). Entities: `cpt:duhkha-for-the-discerning`, `cpt:caturvyuha`, three `phn:ys-duhkha-shows-*`.
- **Eight limbs 2.28–2.55:** `pth:yoga-sutra-eight-limbs` (stages 6–8 are named only, since they belong to pāda 3), the yama and niyama practice entries, and an entry for each sign of establishment (2.35–2.45).
- **Warnings quoted verbatim:** Vyāsa's own warning on austerity (YBh 2.1, "without harming the clarity of the mind", on `prc:tapas` and `prc:kriya-yoga`), on truthfulness (YBh 2.30), and on harmful thoughts (YBh 2.34). These are exact substrings of the source, produced by code. No warning text exists in this range for prāṇāyāma; that is stated, not invented.

## Restricted material
- Marked `restricted: true`, summary only, with no counts, steps or durations: 1.34 (expulsion and retention of breath), 2.49–2.51 (prāṇāyāma), and 2.32 (the fasting-type vows kṛcchra, cāndrāyaṇa and sāṃtapana, named only).
- The three prāṇāyāma practice entries and `prc:tapas` are flagged `restricted`. `prc:brahmacarya` records only Vyāsa's definition.
- The text gives no figures in these passages, and none were added.

## Skeleton decisions
- 3 corrections:
  - YBh 1.11: the skeleton's gloss of the dream/waking memory contrast was wrong.
  - YBh 1.14: the skeleton said "devotion" where the text says satkāra.
  - 2.49-51: the skeleton bundled three segments.
- Everything else is confirmed by the text and marked upgrade.
- The skeleton sūtra paraphrases were compared only by their opening words. The bhāṣya paraphrases were read in full.

## Uncertain (for the judge)
- **Low confidence:** YBh 1.43 (the whole, avayavin, compressed; the edition has a stray `.uparaktā`), YBh 2.23 (the views on what non-seeing is), YBh 2.24 (the impotent-husband objection and the partial-teacher's reading).
- **Moderate confidence, worth checking first:** 1.5, 1.7, 1.9, 1.11 (compressed), 1.24–1.25 (Vyāsa's argument for Īśvara), 1.32 (polemic against an unnamed opponent), 1.35–1.36 (experience descriptions), 1.42–1.45, 2.4, 2.5, 2.13 (long), 2.15/2–3, 2.17–2.20, 2.27, 2.28, 2.51, 2.55.
- **YBh 2.13:** only the first part is paraphrased; the rest of the bhāṣya is described in the note.
- **YBh 1.20:** the paraphrase mentions the nine kinds of yogin, which fall just past the end of the excerpt. This is noted in the entry.
- **Ids from the notes:** entries for the `phn:ys-*` ids named in the notes exist, except one deliberate wildcard (`phn:ys-klesa-state-*`) whose concrete ids also exist.
- **Terms:** 65 candidate term tokens I had generated (mostly compound phrases) were dropped because they were neither in `data/terms.json` nor glossed; the list is in `_gen/S/dropped_terms.txt`. The 248 new terms have short definitions and were not double-checked against a standard glossary.
- **Not checked:** no external translation was consulted (`translation_basis` says so), and cross-refs to ch3 ids (3.1, 3.2, 3.3, 3.50) resolve only after the merge. Not checked further: whether the existing skeleton concept and term ids are the right homonyms.

## Paths
`/home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p1-2/single/` (teachings.jsonl, terms.jsonl, concepts.jsonl, obstacles.jsonl, practices.jsonl, phenomenology.jsonl, disputes.jsonl, paths.jsonl, skeleton_decisions.jsonl). Scripts are in `/home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p1-2/_gen/S/`.
