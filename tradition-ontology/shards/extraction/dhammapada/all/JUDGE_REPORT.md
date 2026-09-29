# Dhammapada, chunk "all": Role J (judge spot-check and promotion)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Step 1: original.text against the segments (by code)
- All 423 verse teachings have original.text equal to segments.jsonl `pali`: 0 mismatches.
- The 26 chapter entries and the thesis have no original.
- Each segment has exactly one teaching. The vagga for each verse matches the standard ranges (1-20 … 383-423).

## Step 2: sample
- **Random sample:** 43 verse teachings (10% of 423 is 42.3, minimum 43), seed 20260929.
  - Allocation is proportional with at least 1 per vagga: vagga 24 has 3, vagga 26 has 4, the others 1-2.
  - Refs: 13 17 32 37 46 58 63 73 81 85 97 102 108 116 138 142 153 164 175 183 193 208 209 223 248 250 260 261 281 283 304 305 308 333 334 338 350 374 377 395 401 406 412.
- **Low-confidence:** all 15 (6 72 97 209 218 240 294 295 302 339 341 370 384 385 389).
- **Restricted-practice:** 70 (a fool eating from a kusa-grass tip month after month), 141 (nakedness, fasting, squatting) and 308 (iron-ball image).
- **Chapter and thesis:** ch7, ch14 and ch15 (same RNG), plus the thesis.
- 62 entries in all. Each was read against the Pali, with Sujato's English as a check.
- Linked ids: existence was checked by code. Sense was checked against data/ definitions, including the 7 reused ids the extractor flagged and all 38 "-pali" ids.

## Step 3: acceptance
- The random sample was 40/43 faithful as written (93.0%), which is below 95%, so every entry was checked individually.
- Every final teaching has mode "individually-checked".
- Random-sample failures:
  - **97:** the commentators' praise senses ("knower of the unmade", "cutter of links") were in the paraphrase, although the entry's own note says they are the commentators'.
  - **138:** jāniṁ ("loss"), one of the ten states, was dropped.
  - **142:** linked trm:samana, which is a homonym (see below).

## Result
- 450 teachings: 412 passed, 38 fixed, 0 failed.
- In final/, all 450 are `text-verified` with protocol `insight-p1-single+spot` and fidelity {status, checked_by "J", date 2026-09-29, mode "individually-checked", note}.
- Every fixed entry has correction_log items (field, old, new, reason, by J, date).
- fidelity.jsonl has one line per teaching: id, sample, criterion, verdict, fix, evidence (quoted Pali, file and line), reason.

## Fixes (38 teachings)
- **Commentarial reading given as plain sense, or an unlabelled commentary gloss:**
  - 6: yamāmase, "we are coming to an end".
  - 79: dhammapīti, "drinker of the Dhamma".
  - 97: as above.
  - 146: "(the world) is burning".
  - 167: lokavaḍḍhana gloss in the note.
  - 266: vissa taken as "corrupt"; now left untranslated, with the readings in the note.
- **Wrong construal, omission or addition:**
  - 138: jāni restored.
  - 171: cittaṁ ("adorned") restored.
  - 218: manasā phuṭo is "suffused by mind", not "whose mind is suffused (with it)".
  - 295: veyagghapañcamaṁ is "the tiger as the fifth".
  - 313: the verse has paribbāja, not paribbājaka.
  - 389: the greater shame falls on the one who retaliates (yassa = yo assa, matching the verse's own second line), not on the striker.
  - 136: "does not awaken" becomes "does not realise it".
  - 157: "at least one" becomes "one" of the three watches.
- **Homonym links:**
  - 142, 184, 254, 255, 264, 265, 388: trm:samana (headword samāna, the vital wind) re-pointed to trm:sramana (śramaṇa; its early-buddhism definition matches Dhp 265, and the skeleton itself used this id).
  - 332: wrong-sense trm:samanna link removed. Here sāmaññatā means service of samaṇas, not the ascetic life.
- **Tags:**
  - 294, 295: standpoint "apophatic" becomes "ethical-social". These are riddles, not statements by negation. Type karma-liberation added.
  - 89, 92, 93, 95: level "ultimate" becomes "conventional", since they speak of persons, like 90, 91, 94 and 96.
  - 154, 179, 180, 353: level "bridging" becomes "conventional", since they relate no two levels explicitly.
  - ch7: stage becomes "realized" and types become karma-liberation and ultimate, as in its own verses.
- **Chapter entries:**
  - ch5: ñatta now keeps both readings.
  - ch6: "drinking the Dhamma" and "without fear" removed.
  - ch11: "all is burning" becomes "constant burning".
  - ch22: the kusa-grass image, which had been garbled, corrected.
  - ch26: "not by a rag-robe alone" inverted 395, which praises the rag-robed meditator; corrected.
- **Thesis:**
  - Verses 1-2 have mano (not citta) and dhammā, and the thesis no longer narrows dhammā to "what one says and does".
  - 279 has "all dhammas" not-self, not "formations".
  - The refrain "him I call a brāhmaṇa" is in most verses of 385-423, not all: by code, 387-390 and 392-394 lack it.

## Entities (level not raised; each has a verification.checks record from J)
By code:
- every rests_on teaching exists and links the entity;
- every "as used in Dhp …" list matches its rests_on;
- no practice is restricted or carries warnings.

Corrected:
- trm:samanna: 332 removed from its rests_on and its "as used in" list.
- trm:dhammapiti: now "joy in the Dhamma" (205), with the "drinker" reading labelled as the commentators'.
- trm:akatannu and trm:sandhiccheda: ordinary sense first; praise readings labelled as the commentators', consistent with the fix to 97.
- trm:sota-stream: "(of craving…)" and "339-347" removed.
- obs:kodha: 407 is not about kodha.

All 38 "-pali" ids have a base data/ entry without any early-buddhism or Theravāda sense, which is consistent with the extractor's rule.

## Skeleton decisions
- 22 decisions: 17 upgrade and 5 correct. The extractor's own summary line said 16 upgrades; the actual count is 17.
- Every replaced_by exists in final/, and every skeleton teaching in data/teachings/dhammapada.jsonl has a decision.

## Validation
- `python3 scripts/validate_shard.py shards/extraction/dhammapada/all/final` gives 0 errors and 1 warning ("REPORT.md missing").
- Every linked id resolves in data/ or the shard.

## Open points for the orchestrator
1. **data/ trm:samana** has a misfiled early-buddhism samaṇa definition under the headword samāna (the vital wind). It should move to trm:sramana.
2. **Conflated data/ headwords still linked:**
   - trm:bhava: headword "bhāva", with the early-buddhism "becoming" sense inside (348, 351, 415, 416).
   - trm:dosa: headword "doṣa", mixing the Āyurveda humour with the Buddhist sense of hatred (8 verses).
   - Their Buddhist-lineage definitions match the verses, so the links were kept. But a user-facing display of the headword would be wrong.
3. **Right word, but data/ holds only a later-school definition:**
   - trm:kayagatasati (Visuddhimagga: the 32 parts; used on 293, 299)
   - trm:kalyanamitta (Visuddhimagga: meditation teacher; 78, 376)
   - trm:gantha (the four ties; 90, 211)
   - trm:sasana (the five disappearances)
   - prc:asubha-bhavana (a Sarvāstivāda skeleton method; 8, 350)
   - prc:metta-bhavana (Visuddhimagga order; 368)
   - The paraphrases do not import these senses. These entries need an early-buddhism definition before user-facing use.
4. **trm:tapa-pali duplicates data/ trm:tapas.** trm:tapas has early-buddhism definitions citing Dhp 184 and 70, but it also carries the self-mortification sense. Decide whether to merge the two or record them as equivalents.
5. **trm:bandhana** reuses an existing data/ id (Sanskrit, Pātañjala-only). merge.py will union the definitions; the sense "bond" is the same, but the language field may flip.
6. **Frame text in originals.** original.text includes the commentarial story-titles and vagga colophons, because it must equal the segment. Segment 416 carries the verse twice, and 423 carries the edition's closing tables. User-facing quotes should strip these.
7. **Tagging conventions to align across texts:**
   - The type "ultimate" is used on 28 arahant, Buddha and nibbāna entries. I kept this as consistent with ult:early-buddhism.
   - Some text-layer notes label verses "arthavāda" (30, 70, 106, 178, 196, 354, 387). That is a reconciliation-layer category, so the interpretation layer may be the better place for it.
8. **Rendering choices left as the extractor made them:** 263 vantadosa as "hatred" (it could be "fault"); 334 hurāhuraṁ as "existence to existence"; 355 "as if he were another". All are defensible.

## Not checked, or limited
- The Dhammapada-aṭṭhakathā is not among the prepared sources. My attribution of readings to the commentators (6, 79, 146, 167, 266) rests on my own knowledge of the commentary and on the extractor's labels, not on a resolved commentary text.
- fidelity.jsonl itself is not covered by the validator.
- Beyond the flagged ids, data/ entries were read only for the ids linked from this shard.
