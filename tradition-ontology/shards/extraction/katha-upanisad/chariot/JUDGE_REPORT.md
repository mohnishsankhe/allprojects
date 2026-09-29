# Role J: judge spot-check and promotion (2026-09-29)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Units:**
- tattvartha-sutra/karma-passions
- taittiriya-upanisad/kosa
- katha-upanisad/chariot
- prajnaparamita-hrdaya/all
- prajnaparamita-hrdaya-sanskrit-short/all

**Files written, nothing else:**
- `/home/user/allprojects/tradition-ontology/shards/extraction/<unit>/fidelity.jsonl`: one line per teaching and per entity, with id, kind, sample_role, criteria, verdict (pass or fail), status, fix and evidence. Evidence cites the file and line in single/ and quotes the segment.
- `/home/user/allprojects/tradition-ontology/shards/extraction/<unit>/final/`: the same files as single/.

I ran all scripts inline and saved none. I did not run git.

## Method
1. **Originals, by code.** Every `original.text` in all 5 units equals its segment, or is an exact substring for the Taittirīya `/2` and `/3` sub-teachings. There were 0 mismatches. Tattvārtha 8.16 maps to segment "8.116"; I confirmed that the file contains no "8.16" segment.
2. **Sample.** Seed 20260929. Sample size is max(5, ceil(10%)), stratified as one entry drawn at random from each equal slice of the file order. On top of the sample I checked:
   - every low-confidence entry: TS 6.19 and 8.24, TU 2.9.1, KU 1.3.2, and Heart 1.1 and ch1;
   - TS 8.9, as the orchestrator asked;
   - two keyword hits, TS 7.7 (celibacy vow) and TU 3.7.1 (food vow). Neither is a restricted practice.
   
   The random samples were:

   | Unit | Sample | Faithful as written |
   |---|---|---|
   | Tattvārtha | 2.7, 6.11, 6.16, ch6, 7.5, 8.6, 8.12, ch8 | 6/8 |
   | Taittirīya | 2.2.1, 2.6.1, ch2, 3.9.1, 3.10.2 | 3/5 |
   | Kaṭha | 1.3.4, 1.3.7, 1.3.10, 1.3.14, ch1.3 | 3/5 |
   | Heart, Chinese | 2.1, 2.4, 2.6, ch1, thesis | 4/5 |
   | Heart, Sanskrit-short | s2, s5, s7, s10, thesis-sanskrit-short | 3/5 |
3. **Acceptance.** Overall 19 of 28 were faithful (67.9%). Every unit was below 95%, so I checked every entry: 155 teachings and 97 entities.
4. **Promotion.**
   - Teachings are now at level text-verified, with protocol insight-p1-single+spot and fidelity {status, checked_by "J", date 2026-09-29, mode "individually-checked", note}.
   - Each fixed teaching has a correction_log (field, old, new, reason, by J, date).
   - Entities stay at level sourced and each has a verification.checks record (phase J, method text).
   - Every skeleton_decisions `replaced_by` exists in final/, and every skeleton_id exists in data/teachings. I found no undecided skeleton ids in any unit's range.
5. **Links, by code.** After the fixes, every linked id in final/ resolves to data/ or to one of the five final/ folders. By code, no final/ file still references obs:kasaya, trm:maya, trm:pratyakhyana, trm:ajiva, trm:amanaska or trm:mahas.

## Results

| Unit | Teachings passed | Teachings fixed | Entities checked | Entities fixed |
|---|---|---|---|---|
| Tattvārtha | 57 | 19 | 58 | 6 |
| Taittirīya | 26 | 11 | 20 | 3 |
| Kaṭha | 13 | 5 | 9 | 0 |
| Heart, Chinese | 10 | 2 | 6 | 0 |
| Heart, Sanskrit-short | 9 | 3 | 4 | 0 |
| **Total** | **115** | **40** | **97** | **9** |

None failed without a fix.

## Fixes

### Tattvārtha
**Wrong-sense links (homonyms):**
- The 9 teachings linking **obs:kasaya** (2.6, 6.4, 6.5, 6.8, 6.14, 6.16, 8.1, 8.2, 8.9) now point to obs:four-kasayas. In data, obs:kasaya is the Advaita/Gauḍīya meditation fault "latent attachment" (Māṇḍūkya-kārikā 3.44), not the Jain passions.
- **trm:maya → trm:maya-kasaya** in 6.16 and 8.9.
- **trm:pratyakhyana → trm:pratyakhyanavarana** in 8.9. In data, trm:pratyakhyana means the formal resolve of renunciation.
- **trm:ajiva → trm:ajiva-jain** in 6.7 and 6.9. In data, trm:ajiva is the Pali ājīva, "livelihood".
- Reused trm:anantanubandhin and trm:apratyakhyanavarana are the right sense.

**Commentarial glosses presented as the sūtra's words:**
- 6.4, 6.5 and ch6 called the two kinds of inflow "lasting" and "transient". They now use the sūtra's own words, sāmparāyika and īryāpatha, and the glosses are labelled as the commentators'.
- 6.15 and 6.17 said "violent undertaking". "violent" is removed and labelled, and the trm:himsa link on 6.15 is removed.
- 6.24 said "affection for the scripture's community"; it now reads "affection for the teaching (pravacana-vatsalatva)".
- 7.8 had "one for each sense" unlabelled; it is now labelled as the commentaries' reading.

**Other teaching fixes:**
- ch6 misdescribed the structure of 6.6–6.9.
- 6.10 narrowed "tat" to knowledge only.
- 6.19 supplied a noun that its own note said it left open.
- 7.11 misquoted "avineya"; the segment reads "avinaya".
- 8.9 omitted that conduct-deluding karma has two kinds. It glossed saṃjvalana as "smouldering" while calling the glosses literal.

**Sarvārthasiddhi reading in 8.9:** it stays labelled as the commentators' reading. I added a label that it comes from the extractor's recollection and could not be checked, because the commentary is not in the prepared segments.

**Entities:**
- trm:maya renamed to trm:maya-kasaya.
- trm:pratyakhyana renamed to trm:pratyakhyanavarana.
- trm:asrava and cpt:asrava reworded to the sūtra's terms.
- The shard's obs:kasaya entry is removed and folded into obs:four-kasayas (description and rests_on).

### Taittirīya
- **Refrain "tasyaiṣa eva śārīra ātmā yaḥ pūrvasya"** (2.3.1, 2.4.1, 2.5.1, 2.6.1): each had been given one construal without a flag. It is now kept literal, and a note records the ambiguity.
- **sat/tyat** (2.6.1, 2.6.1/2): the gloss "the manifest and the beyond" is replaced by the literal sense and the gloss is labelled.
- **2.1.1/2:** the note presented the commentarial term lakṣaṇa as the text's framing.
- **2.8.1:** trm:abhaya was linked to a verse about fear (bhīṣā); link removed.
- **2.9.1 (low confidence):** the paraphrase split the double object "ete ātmānaṃ spṛṇute" across two clauses. The trm:punya link is removed because the text says sādhu.
- **3.10.2:** "ya evaṃ veda" closes 3.10.1, but the paraphrase made it the subject of the following list.
- **3.10.3:** trm:mahas does not exist, so the link is removed. The referent "(brahman)" is now marked as supplied. The ambiguity of mānavān is flagged.
- **3.10.6:** "suvarṇa" misquoted the e-text, which reads "suvarna" (suvar na).
- **Entities:** cpt:five-sheaths, trm:annamaya and prc:brahma-upasana-3-10 are aligned with these fixes.

### Kaṭha
- **1.3.2 (low confidence):** the paraphrase supplied "to know" as the unstated complement of śakemahi.
- **1.3.7:** the trm:amanaska link is removed. The data entry holds only the samādhi sense, which the entry's own note rejects, and no right-sense id exists.
- **1.3.14:** "understand them" added an object; "them" is removed.
- **1.3.16:** the speaker was Yama, but the verse refers to the story as "told by Death" in the third person. The speaker is now the narrator.
- **1.3.17:** "(fruit)" was a commentator's gloss, and the causative śrāvayet was blurred.

### Heart Sūtra, Chinese
- **1.1 (low confidence):**
  - The paraphrase omitted the preface's own claim that the Buddha taught the nature-principle of the three bonds and five constants (三綱五常).
  - The trm:skandha link is removed; the preface talks about the six sense-appearances, not the aggregates.
- **thesis:** "empty of … own mark" is replaced by the text's wording, "the mark of emptiness" (是諸法空相).

### Heart Sūtra, Sanskrit-short
- **s2:** the note made an outside claim, "the standard translator's homage of the Sanskrit canon", which the text does not support. Removed.
- **s8:** the paraphrase silently corrected the e-text's "viharati cittāvaraṇaḥ" to the negative sense. Now flagged.
- **thesis-sanskrit-short:** it had imported the Chinese causal clause 以無所得故, which this e-text lacks, and misdescribed the reasoning steps.

## Open points for the orchestrator
1. **Problems in data/ (outside my scope):**
   - trm:anna is labelled "aññā" and mixes the Pali aññā with the Upaniṣadic anna ("food").
   - trm:bhava mixes bhava ("becoming") with bhāva.
   - The definitions of trm:anantanubandhin, trm:apratyakhyanavarana, trm:pratyakhyanavarana, trm:samjvalana and cpt:four-kasayas-sixteen give the commentarial reading but cite "TS 8.9", as if the sūtra said it. They should be relabelled as the Sarvārthasiddhi reading. On merge they will sit beside the shard's "not defined in the sūtra" definitions.
2. **Links I kept, although data has no definition for this lineage.** Same word, compatible sense:
   - trm:kriya (TS 6.5)
   - trm:bhava (TS 2.1–2.7)
   - trm:anubhava (TS 8.21)
   - trm:rasa (TU 2.7.1): no Upaniṣadic sense in data
   - trm:prapti (Heart 2.4 and s7): data has only the Sarvāstivāda "possession" sense
   
   These need lineage definitions or sense-specific ids.
3. **Kaṭha amanaska** has no right-sense id. Adding a Kaṭha-sense definition is an option.
4. **Segmentation:**
   - Prepared Tattvārtha 8.16 is labelled "8.116".
   - Taittirīya segments begin with the closing words or verse of the previous section. TU 3.10.2 is the clearest case.
5. **Sanskrit-short s8:** check the e-text reading "viharati cittāvaraṇaḥ" against Vaidya's printed edition.
6. **tch:sariputra** is created only in the Chinese unit's final/, but the Sanskrit-short final/ links it. Merge the two finals together.
7. **Heart Sūtra skeleton entries long.1 and long.2** are still undecided because they have no segment.
8. **original.licence** carries the full sentence from META rather than a short form. It is cosmetic and I left it unchanged.
9. **For future single extractions:** the sample failure rate (32%) came mostly from two sources. The extractor reused existing ids without checking their sense, and commentarial glosses went into paraphrases unlabelled. A mandatory check of the data sense of every reused id would help.

## Not checked
- The commentaries (Sarvārthasiddhi, Śaṅkara), because they are not in local segments. Nothing was judged against them.
- The Śvetāmbara recension of the Tattvārtha.
- The printed editions behind the e-texts.
- The historicity or authorship of the two Chinese prefaces.
