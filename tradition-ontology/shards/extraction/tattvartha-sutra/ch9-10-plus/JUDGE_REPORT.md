# Role J: judge spot-check and promotion — Tattvārtha Sūtra ch.9–10 plus 5.16 and 5.30 (2026-09-29)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Written (nothing else):**
- `/home/user/allprojects/tradition-ontology/shards/extraction/tattvartha-sutra/ch9-10-plus/fidelity.jsonl` — 107 lines. Each line has id, kind, sample_role, criteria, failed_criteria, verdict, status, fix (old, new, reason) and evidence (the single/ file and line, plus the quoted segment).
- `/home/user/allprojects/tradition-ontology/shards/extraction/tattvartha-sutra/ch9-10-plus/final/`:

  | File | Entries |
  |---|---|
  | teachings.jsonl | 60 |
  | terms.jsonl | 20 |
  | concepts.jsonl | 16 |
  | obstacles.jsonl | 1 |
  | practices.jsonl | 1 |
  | skeleton_decisions.jsonl | 49 |

- The promotion script is in the session scratchpad (`j910/promote.py`). I did not run git.

## Method
1. **Originals, by code.** Every `original.text` equals its segment's IAST exactly: 0 mismatches out of 60. Every ch9 and ch10 segment (47 + 9) has a teaching.
2. **Sample.** The population is the 60 teachings left after dropping the duplicates. Sample size is max(5, ceil(10%)) = 6, drawn with `random.Random("20260929")`, one per equal slice of the file order. The sample was 9.2, 9.11, 9.23, 9.40, 10.2 and 10.4.
   - I also checked:
     - the 3 low-confidence entries (9.26, 9.41, 10.3);
     - every restricted entry (9.8–9.17, 9.19);
     - the ch9 chapter entry;
     - the product range 9.28–9.36.
   - Everything was judged against the Digambara Sanskrit only; there is no translation.
3. **Acceptance.** 3 of 6 random-sample entries were faithful as written (50%, below 95%):
   - 9.11: a disputed construal was not flagged;
   - 9.23: "toward" was supplied, and the note called the nominative dvandva "genitive-like";
   - 9.40: the stage tag was "realized", although the holders with three yogas and one yoga are not kevalins.

   So I checked every teaching and every entity individually.
4. **Promotion.**
   - Teachings: `verification.level` text-verified, protocol insight-p1-single+spot, and fidelity {status, checked_by J, date 2026-09-29, mode individually-checked, note}. Every fix has a correction_log item (field, old, new, reason, by J, date).
   - Entities: level stays sourced. Each has a J record in `verification.checks`, and fixed entities also have a correction_log.
5. **Links, by code.** Every linked id in final/ resolves to data/, to this final/, or to karma-passions/final. No final/ file still references trm:bhava, trm:aloka, trm:siddhasila, trm:kayotsarga or prc:kayotsarga.
6. **Multi-sense ids.** dhyāna, dharma, tapas, vitarka, vīcāra, nidāna, yoga, jīva, siddha, mokṣa and loka all carry a lin:jainism definition in data, and each is linked in its Jain sense. I found no homonym linking errors among these; the homonym problems are in item 5 of "Fixes" below.

## Results
| | Passed | Fixed | Failed |
|---|---|---|---|
| Teachings | 33 | 27 | 0 |
| Terms | 16 | 4 | 0 |
| Concepts | 14 | 2 | 0 |
| Obstacles | 1 | 0 | 0 |
| Practices | 0 | 1 | 0 |

Checked groups:
- **Low-confidence:** 9.41 passed; 9.26 and 10.3 were fixed.
- **Restricted:** 9.8, 9.9, 9.12, 9.14, 9.15 and 9.16 passed; 9.10, 9.11, 9.13, 9.17 and 9.19 were fixed.
- **Chapter entries:** ch9 was fixed; ch10 passed.
- **Product range 9.28–9.36:** 9.29, 9.30, 9.31, 9.33 and 9.35 passed; 9.28, 9.32, 9.34 and 9.36 were fixed.

Failed criteria across the teachings:

| Criterion | Count |
|---|---|
| Commentary or unlabelled claim in notes | 15 |
| Paraphrase | 13 |
| Links or cross-refs | 5 |
| Tags | 4 |
| Types | 2 |

## Fixes
1. **Sectarian construal (9.11).** "can occur in the jina" becomes "assigns a number of the parīṣahas to the jina; the sūtra does not say in what sense". The Digambara and Śvetāmbara readings are recorded in a labelled note, as J's recollection, unchecked.
2. **Restricted leakage.**
   - 9.19 paraphrase: "the six outer austerities" → "the outer austerities".
   - 9.17 note: the quoted "one and so on" is removed.
   - cpt:twelve-tapas and prc:jain-external-austerities: the count "six" for the outer austerities is removed.
   - Every other restricted entry is summary-only with no counts, lists, durations or procedures (checked by code; the only remaining number words are not counts of the hardships).
3. **Product check, 9.28–9.36 (exact renderings).**
   - 9.28: śukla "(pure)" → "(white)"; the note says "pure" is the commentators' gloss.
   - 9.32: "pain" → "feeling (vedanā)"; "painful feeling" is labelled as the commentators' reading.
   - 9.36: apāya "(harm)" → "('going away', also 'ruin')"; both commentarial readings are recorded.
   - 9.34: the note equated avirata with the fourth guṇasthāna only; it is corrected and labelled.
   - Aligned entities: trm:arta-dhyana, trm:dharma-dhyana, and trm:sukla-dhyana (literal: "white (bright) meditation").
   - Final renderings: ārta "pained", raudra "fierce", dharmya "of dharma", śukla "white". No anxiety, rumination, stress or depression anywhere (checked by code).
4. **Commentary or tradition given as the text's plain sense.**
   - 9.18: "i.e. perfect" and "after a break" replaced by the literal senses. The chedopasthāpanā gloss attributed to the Digambara commentaries is the Śvetāmbara usage, and is now flagged as uncertain.
   - 9.20, 9.21 and ch9: "inner austerity" is not the sūtra's word (it says uttara); "inner" is labelled as the tradition's name.
   - 9.22: viveka "(discrimination)" → "(separation)". The recension note ("Śvetāmbara has ten") is flagged as doubtful.
   - 9.23: "toward" and "formal" are removed, and the note's grammar is corrected.
   - 9.45: "endless-binding passions" is bracketed as the tradition's expansion of "ananta".
   - 10.6: "its nature as such a motion" → "its taking the form of such a motion" (cpt:siddha-ascent-causes aligned).
   - 9.1, 9.10 and 9.37: unlabelled claims in notes are relabelled.
   - 10.3: the recalled supplied word ("abhāva") is flagged; J recalls "mokṣa". Neither is checked.
   - trm:samvara: the commentators' reading of "ca" in 9.3 had been given as the sūtra's teaching; it is now labelled.
5. **Links.**
   - 9.13 cross-ref: 8.9 (deluding karma) → 8.4 and 8.6 (knowledge-obscuring karma).
   - Removed links to words the sūtra does not use: 9.26 trm:kayotsarga and prc:kayotsarga; 10.3 trm:bhava (data has no Jain sense for it); 10.5 trm:siddhasila; 10.8 trm:aloka (see open point 1).
6. **Tags and types.**
   - 9.21: path meditation → general.
   - 9.27: stage advanced → unmarked (the definition covers ārta and raudra too).
   - 9.40: stage realized → advanced.
   - 9.45: stage advanced → all.
   - 5.16 and 5.30: "karma-liberation" removed from types.
7. **Skeleton decisions.**
   - Dropped: the decisions for 2.1 and 2.7.
   - Corrected (they had been marked upgrade although the skeleton wording was wrong or commentarial):
     - 9.3: "[as well as stopping]";
     - 9.27: "up to one muhūrta";
     - 10.9: "[only in retrospect]".
   - Reasons fixed on the other two:
     - 9.8: the templated reason "named hardships in detail" was false; the decision is now upgrade;
     - 9.11: the reason now names the disputed "[occur]".
   - Every `replaced_by` exists in final/. All 49 skeleton ids in range are decided. Now 35 upgrade and 14 correct.

## Open points for the orchestrator
1. **trm:aloka (data)** is headed "āloka" and holds the Guhyasamāja āloka ("light") beside the Jain aloka ("non-world"). That is two words under one id and needs a sense-specific id (trm:aloka-jain).
2. **trm:bhava (data)** still has no Jain definition (as the earlier judge also found). **trm:nidana** holds the Āyurveda and Jain senses under one id.
3. **Data renderings differ from the verified shard:**
   - trm:dhyana, trm:arta-dhyana and obs:arta-raudra-dhyana use "sorrowful", "brooding" and "cruel";
   - trm:dhyana and prc:sukla-dhyana use "pure";
   - trm:apaya-vicaya and prc:dharma-dhyana each state a single reading of apāya.

   Product text should use the final/ renderings. "Brooding" comes close to the forbidden psychology vocabulary.
4. **Restricted content in data:** cpt:twenty-two-parisahas, obs:twenty-two-parisahas, trm:parisaha, cpt:twelve-tapas, trm:tapas and trm:bahya-tapas list the hardships and outer austerities, with counts. The ids themselves contain counts. The merge will union these with the summary-only shard entries.
5. **trm:chedopasthapana (data)** has only the Śvetāmbara "great initiation" sense. The Digambara sense is uncertain (fix 4).
6. **Skeleton "upgrade" decisions left as they are**, although the skeletons' brackets or parentheses carry commentarial glosses: 9.6, 9.7, 9.22, 9.28, 9.35, 9.36, 10.1, 10.7 and 10.8. The substance is confirmed. Re-label them if strict bookkeeping is wanted.
7. **cpt:five-bhavas** in this shard rests only on 2.1 and 2.7. It duplicates the karma-passions contribution, but its links resolve through karma-passions/final.
8. **Segment typo** in 9.39: "kriryānivartīni". The original is kept as an exact copy.

## Not checked
- The commentaries (Sarvārthasiddhi, Rājavārttika) are not in the local segments. Every commentators' reading in the notes is recalled, by the extractor or by J, and labelled so.
- The Śvetāmbara recension.
- The printed edition behind the e-text.
