# Report: HYP single extraction (Role S), chunk `all`
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Output is in `/home/user/allprojects/tradition-ontology/shards/extraction/hatha-yoga-pradipika/all/single/`. Scripts are in `.../all/_gen/S/`: `common.py` (reused), `ch1.py` to `ch4.py`, `ents.py`, `build.py`. The earlier `ch1.py` draft is kept as `_gen/S/old/ch1_draft.py`.

## What I did
- I reused `common.py` after checking it. I rewrote `ch1.py` because the earlier draft linked many unverified or invented ids.
- I read all 387 segments in full. I wrote every teaching by hand from the Sanskrit, and `build.py` produced the files.
- `original.text` is copied by code from the segment. `build.py` asserts that every segment has one whole-segment teaching with an identical original and that every other original is an exact substring.
- Every teaching is tagged `extraction` single/S and `verification` sourced with `protocol` insight-p1-single+spot.

## Mechanical checks (by code)
- **Completeness:** every one of the 387 segments has a whole-segment original.
- **Ids:** no duplicate teaching ids.
- **Links:** every linked id resolves, either to my own entity files or to an id in `data/`.
- **Entity `rests_on`:** all resolve to my teaching ids.
- **Decisions:** every `replaced_by` exists.
- **Restricted scan:** no digits or duration or count words in restricted paraphrases. Verse refs are excluded from the scan, and the ordinal "second" is allowed.
- **Validator:** `validate_shard.py` gives 0 errors.

## Not checked
- Fidelity of paraphrases is my own reading only. The judge should do the spot-check.
- The Jyotsnā commentary file was not touched and not used. The segment contains no translation. Text-critical questions (variants, corrupt readings) are recorded in notes, not resolved.

## Segment irregularities of the prepared text
- There is no segment 2.20 (the numbering jumps from 2.19 to 2.21).
- Verse 2.51 is embedded inside segment 2.52, marked "|| | 51 ||". It is handled in 2.52's paraphrase and notes.
- Segment 1.17 contains a bracketed list of ten yamas and ten niyamas, which reads as an insertion. I recorded it as `1.17/2` with the original taken as a substring. The list is inconsistent with 1.38, which puts moderate eating among the yamas and non-harming among the niyamas.
- Segment 4.20 begins with a prose gloss on 4.19 ("Vāyuḥ iti | yasmāt paricitaḥ …"). It is labelled in the notes as an embedded gloss, whose commentator the segment does not name. It is kept out of the paraphrase, which covers only the verse's last line.
- The e-text carries inline headings ("atha padmāsanam", "dvitīyopadeśaḥ", etc.) inside segments. They are mentioned in notes, not treated as verse content.
- Verse 1.26 has the reading "śrīmatyanāthoditam", which is probably corrupt. Recorded at low confidence.
- Verse 4.58 has a vocative "Rāma", and the source is not stated in the segment. Noted only.

## Restricted handling
- 240 teachings are `restricted: true`. This covers:
  - all breath-control, retention and diet verses;
  - the ṣaṭkarmas;
  - all ten mudrās (mahāmudrā, bandhas, mahāvedha, khecarī with its tongue-cutting preparation, viparītakaraṇī, vajrolī, sahajolī, amarolī, śakticālana);
  - the strained or inverted postures (kūrma, kukkuṭa, uttānakūrma, dhanura, matsyendra, paścimatāna, māyūra);
  - the mercury verses 4.26, 4.27 and 4.96;
  - the khecarī of 4.43–4.53;
  - śāmbhavī 4.35–4.39.
- Verse 3.47 (a riddle about eating cow-flesh) is summarised with the text's own gloss at 3.48 that "cow" means the tongue.
- The gentle seated postures are `restricted: false`: svastika, gomukha, vīra, siddha, padma (1.44, 1.45, 1.47), siṃha (1.50, 1.51), bhadra, and śavāsana.
- Also `restricted: false` are the doctrinal and conditions verses, nāda-attention (4.65–4.99 except 4.68 and 4.96), the samādhi verses, and the yama/niyama list.
- Judgement calls, all conservative. The judge may prefer to reverse some.
  - 4.39 (fixing the mind on light) is restricted only because it mentions a bodily brow movement.
  - The mind-breath doctrine verses 2.2 and 2.3 are restricted because they lead into breath restraint.

## Product-relevant entries (warnings and general conditions)
- Conditions: 1.11–1.16, 1.64–1.66, `cpt:hyp-conditions-for-practice`, `obs:hyp-six-destroyers` (1.15), `cpt:hyp-six-furtherers-of-yoga` (1.16), `prc:hyp-yoga-hut` (1.12–1.14).
- Warnings: `cpt:hyp-warnings-on-breath`, the `warnings[]` of the `prc:hyp-*-summary` entries, 4.114 (`cpt:hyp-warnings-on-boasting`), and 1.65/1.66/4.40 (`cpt:hyp-practice-not-talk`).
- Health claims are always phrased "the text says …" or "the text claims …" and never as fact.

## Entity notes for the orchestrator and merge
- **Sense-specific new ids:** `trm:samadhi-hyp`, `trm:laya-hyp`, `trm:sunya-hyp`, `trm:bandha-hyp`, `tch:sabara-hyp`, `tch:pujyapada-hyp`, `tch:nityanatha-hyp`, `tch:kakacandisvara-hyp` and the other adept ids.
- **Homonyms not linked:** the existing `trm:samadhi`, `trm:laya`, `trm:sunya` and `cpt:bandha` carry other lineages' senses. `cpt:satkarma` is a Kālīkula sense, so I linked `cpt:satkarma-doctrine` and `trm:satkarma` instead. `prc:mahabandha-mahavedha` is Yogatattva-based, so I made `prc:mahavedha-hyp` for 3.26–3.31.
- **Contributions to existing ids:** I emitted lineage contributions with my sourced text to existing ids, all read before linking, so merge will union them:
  - terms such as `trm:hatha`, `trm:raja-yoga`, `trm:nada`, `trm:susumna`, `trm:kundalini`;
  - concepts such as `cpt:hatha-raja-interdependence` and `cpt:guru-in-hatha`;
  - practices for the asanas, bandhas, mudrās, dhauti, `prc:nadanusandhana` and `prc:hatha-yama-niyama`;
  - phenomenology `phn:hyp-*`;
  - `pth:hyp-nada-four-stages`;
  - the disputes `dsp:necessity-of-satkarma`, `dsp:jalandhara-in-mahabandha` and a new `dsp:hyp-is-laya-liberation`;
  - the teachers `tch:adinatha`, `tch:matsyendranatha`, `tch:goraksanatha`, `tch:caurangi`, `tch:svatmarama`.
- **Check the merge for restricted entries:** the existing skeleton entries for the restricted asanas, bandhas, mudrās and dhauti carry step-level `method_summary` text. My contributions are summary-only with `restricted: true`. The merge should keep the higher-verified summary and the restricted flag.
- **`dsp:hatha-vs-raja` not re-emitted:** the HYP gives only one side, and the schema needs two. The teachings still link to it (`rests_on` for it lives in `cpt:hatha-raja-interdependence`).
- **`prc:mahamudra` linked:** it is the mahāmudrā of HYP 3.10–18 (lineages incl. hatha-yoga), so I reused it.
- **`pth:hyp-nada-four-stages`:** bands are marked low confidence, because the text says "liberation or not" at 4.78.
- **`dsp:hyp-is-laya-liberation` side 2:** it has no `lineage` field, because the other school is unnamed.
- **Phenomenology:** `phn:hyp-nadi-suddhi-signs` now carries only the two signs that 2.19 actually names.

## Skeleton decisions (229)
- 81 upgrade, 148 correct, 0 retire.
- Single-verse skeleton entries that the text confirms are upgraded. Restricted single-verse entries are upgraded only where the skeleton carried no steps.
- Range entries, and restricted entries that carried steps, measures or claims, are "correct": they are replaced by verse-level ids, listed in `replaced_by_all` when there are several.
- Specific corrections:
  - `1.10`: the skeleton says "supporting tortoise", but the text says maṭha (hut) in both lines.
  - `4.41`: "(the two breaths)" is a gloss, not in the verse.
  - `4.74-75`: "(between the brows)" is not in the verse.
  - `2.19-20`: the e-text has no 2.20, and the extra signs in the skeleton are not in 2.19.
- Overlapping skeleton ranges, such as `1.4-9` with `1.5-9`, `1.12` with `1.12-13`, and `3.32-54` with `3.33-36`, are all folded into the verse-level ids.

## Open points for the judge
1. All 39 low-confidence entries, and the 240 restricted ones.
2. The adept lists at 1.5–1.8: the compounds are divisible in more than one way. The judge should confirm that only the clear proper names got teacher entries, all as `-hyp` ids, with no identification beyond the name.
3. Whether the "restricted" boundary for 4.35–4.39, 4.43–4.53 and the mercury verses matches the orchestrator's intent.
4. The `thesis` entry: the ref lists per mark are my selection.

Files:
- `/home/user/allprojects/tradition-ontology/shards/extraction/hatha-yoga-pradipika/all/single/` (`teachings.jsonl`, `skeleton_decisions.jsonl` and the entity `.jsonl` files)
- `/home/user/allprojects/tradition-ontology/shards/extraction/hatha-yoga-pradipika/all/_gen/S/` (`build.py`, `ch1.py` to `ch4.py`, `ents.py`, `common.py`, `old/ch1_draft.py`)
