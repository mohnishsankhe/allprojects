# Fidelity check — Bhagavad Gītā (src:bhagavad-gita), chunk ch04-06 (chapters 4–6)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Role F, fresh context, 2026-09-29. Inputs used: only `merged/` (teachings, entity files, skeleton_decisions) and `sources_raw/prepared/bhagavad-gita/segments.jsonl` + `META.json`.

## Counts
| | count |
|---|---|
| Teachings checked | 124 (118 verses, 3 chapter entries ch4/ch5/ch6, 3 sentence spans 5.8-9, 5.27-28, 6.20-23) |
| passed | 109 |
| fixed | 15 (4.21, 4.23, 4.34, 4.35, 4.40, 5.13, 5.14, 5.15, 5.17, ch6, 6.7, 6.10, 6.12, 6.20-23, 6.29) |
| failed | 0 |
| Entity entries copied | 225 (terms 128, concepts 29, obstacles 19, practices 34, phenomenology 9, paths 1, disputes 1, teachers 5) |
| Entity entries corrected | 22 (18 text corrections, 6 dedupes; 2 entries had both) |
| Skeleton decisions copied | 67 (63 upgrade, 4 correct); 1 reason corrected (5.14-15) |
| interpretation_log.jsonl lines | 43 (37 text-correction, 6 dedupe) |

Final teachings all carry `fidelity {status, checked_by: "F", date: "2026-09-29", note}` and `verification.level: "text-verified"`. Fixed teachings carry `correction_log` items `{field, old, new, reason, by, date}`.

## What was checked, and what was already right
- **Originals.** Checked by script. Every verse's `original.text` is exactly the segment IAST, and every span's is the segments joined with `\n`. The known edition slips are kept exactly as given and noted in each entry: 4.29 'prāṇa', 4.31 stray nukta 'kuto़'nyaḥ', 4.39 'śraddhāvā~l', 5.1 'suniśicatam', 5.8 'śrṛṇavan', 6.32 'saḥ yogī', 6.35 'calaṃ', 6.40 'kaśicad'. The 'śrī bhagavān uvāca' headings in the segments are also kept.
- **Speakers.** Arjuna → Kṛṣṇa at exactly 4.4, 5.1, 6.33, 6.34, 6.37, 6.38, 6.39 (matching the segments' 'arjuna uvāca' markers). All other verses are Kṛṣṇa → Arjuna.
- **Avatāra.** 4.5–9 use the text's own verbs: saṃbhavāmi = "I come into being", sṛjāmi = "I send myself forth". The word avatāra is absent from every paraphrase. The `cpt:avatara` definition itself states that the word does not occur.
- **Imported vocabulary.** No psychology terms anywhere (ego, energy, psyche, consciousness, etc.), in teachings or entities. No capital-S "Self".
- **Commentarial readings.** Śaṅkara/Rāmānuja readings are confined to `notes`, not paraphrases: vikarma, madbhāva, prakṛti/māyā in 4.6, varṇa by birth or by conduct, the scope of 5.2's "superior", 5.14–15 prabhu/vibhu, 6.31 ekatva, and so on.
- **Links.** All term, concept, practice, obstacle, path, teacher and dispute ids resolve: either in merged/, in canonical data, or in the registry (`dsp:works-knowledge-grace`). The forward refs `tea:bhagavad-gita:7.1` and `18.41` belong to chunks not yet final.

## Examples of fixes
- **4.40.** Old: "the doubting self (saṃśayātman) perish". New: "the one of doubting mind (saṃśayātman) perish". A reflexive/mental ātman had been read as "the self", which would make the self perish, against the Gītā's own teaching. Note added on the singular verb.
- **6.7.** Old: "the supreme self (paramātman) is composed". This picked one construal even though the entry's own note said it did not decide. New: both construals — "either the supreme self (paramātman) is established (samāhita), or, taking 'param' adverbially, his self is supremely composed". jitātman is now reflexive. The ch6 chapter entry had the same problem and was fixed too.
- **5.17.** Old: "whose self is That (tad-ātman)", which reads identity into the compound. New: "whose self is set on That", with both readings in notes (identity with That / mind fixed on That).
- **5.15.** Old: "the all-pervading one (vibhu)". New: "the pervading, mighty one (vibhu)"; note updated.
- **5.14 and 5.15.** Only the self-reading was linked (`cpt:non-agency-of-the-self`). `cpt:isvara`, which already rests on both verses, is now linked as well.
- **Term flattening.** "mind" is kept for manas. citta/cetas are now marked where they had been flattened:
  - 4.21 and 6.10 yatacittātmā → "restrained in thought (citta) and in himself" (ātman here = oneself; commentators say the body);
  - 4.23 cetas;
  - 6.12, where manas and citta had both been rendered "mind";
  - 6.20-23 span: citta, buddhi and cetas markers;
  - ch6 summary: sama-buddhi had been "equal mind", now "even in intellect (sama-buddhi)"; citta/cetas at 6.14, 6.18, 6.20, 6.23 marked.
- **Notes only.**
  - 4.35: the reflexive reading "in yourself" of ātmani is recorded.
  - 6.29: the reflexive reading of ātmānam … ātmani is recorded, with the commentators' readings listed neutrally (one self in all / all selves alike in nature / the Lord in all).
- **Dangling cross-refs.** Repointed to the existing canonical span entries:
  - 4.35 and 6.29: `tea:isa-upanisad:6` → `6-7`;
  - 4.34: `tea:mundaka-upanisad:1.2.12` → `1.2.12-13`;
  - 5.13: `tea:svetasvatara-upanisad:3.18` → `3.16-19`.
- **Entities.**
  - `trm:citta`: said citta is "made one-pointed" in 6.12; there it is the manas.
  - `trm:svadhyaya` literal "self-study" → "one's own recitation; (Vedic) study"; `prc:svadhyaya` name "Self-study" → "Recitation and study (svādhyāya)".
  - `trm:samsaya` / `obs:samsaya`: "the doubting self" corrected.
  - `trm:apunaravrtti`, `trm:atman`, `trm:nirasih`, `trm:niruddha`, `trm:yoga`, `trm:yukta`, `cpt:the-self`, `cpt:non-agency-of-the-self`, `prc:dhyana-yoga-gita`, `prc:brahmacarya`, both `phn` entries, and `pth:gita-ascent-in-yoga`: aligned with the teaching fixes above.
  - Duplicates left by the union of the A and B entity lists were removed from `cpt:yajna-reinterpreted` (members), `obs:ajnana`, `obs:samsaya`, `obs:restless-mind`, `prc:dhyana-yoga-gita` and `prc:karma-yoga`.
- **Skeleton decision 5.14-15.** Its reason cited a merged entry "5.14-15" that does not exist; it now points to 5.14 and 5.15, and the vibhu gloss is aligned.

## Decisions taken
- **Entity verification levels are unchanged.** Each entity got a `verification.checks` record instead: phase D, method text, result confirmed/corrected. Many ids are shared across units (e.g. `trm:atman`, `cpt:brahman`, `tch:krsna`). Raising them to text-verified would make the merged entry show other units' skeleton definitions as verified. Teachings are raised to text-verified as the brief requires.
- **No teaching failed.** Every problem could be fixed from the Sanskrit.

## For the next wave to revisit
1. **Entity levels.** Set a project-wide policy on whether chunk-derived entity contributions become text-verified (the per-lineage definition vs the whole entity).
2. **Cross-refs.** When Īśā, Muṇḍaka and Śvetāśvatara are extracted verse by verse, repoint 4.34, 4.35, 5.13 and 6.29 to the verse ids. Confirm `tea:bhagavad-gita:18.41` and `7.1` once those chunks are final.
3. **Other chunks.** Check ch01-03 and ch07-09 for the same citta/cetas → "mind" flattening and reflexive-ātman → "the self" pattern. Consider one text-wide convention: here verse entries use "mind (citta)", while overviews and entities sometimes use "thought (citta)"; all are marked.
4. **Names worded from other chapters.** `cpt:non-agency-of-the-self` ("…the guṇas act") and `prc:guna-witnessing` are linked from 5.8–9/5.14, where the text says the senses or svabhāva act. Their notes say so, but the misreading hunter should check the names after the merge.
5. **Merge conflicts.** `prc:svadhyaya`'s name change may conflict with Yoga-Sūtra units at merge (scalar `name`).
6. **Debatable tags and fields (plausible, not changed).**
   - level `bridging` on 4.6, 4.13, 4.18, 4.20, 4.24, 5.8–9, 5.13–16, 5.18–19;
   - standpoint `absolute` on 4.20;
   - level `ultimate` on 4.35, 5.24, 6.29;
   - `stage_native` descriptors ("nitya-saṃnyāsin", "yukta", "yuktatama") that are not stage labels;
   - concept categories: `cpt:bhakti` = ethics, `cpt:yajna-reinterpreted` = karma-rebirth, `cpt:internalized-sacrifice` = stages-maps.
7. **Paraphrase and links left as they are.** 4.9 takes divyam predicatively (same sense either way). `obs:kalmasa` is used for kilbiṣa, vṛjina and pāpa (these are named in the entry). `trm:yati` is linked from 6.37 ayati as a contrast.
8. **Reconciliation auditor.** In `dsp:renunciation-or-action-gita`, side 2 is marked `reported_by_opponent` (the views are known only through the Gītā's denials), and a P4/P3 partial reconciliation is recorded. `dsp:works-knowledge-grace` exists only in the registry so far.
9. **`cpt:avatara`.** Its name, "The Lord's descent (avatāra / prādurbhāva)", is an interpretation-layer label for a word the text does not use; the definition says so. Revisit if concept names should avoid words absent from the texts they index.
