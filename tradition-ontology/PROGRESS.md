# Ontology Insight Generator — build to release-ready (supersedes the earlier ontology-build plan)

Budget: 12 working hours. Phase budgets: P0 0:00–0:30 · P1 0:30–3:30 · P2 3:30–5:00 · P3 5:00–8:30 · P4 8:30–9:30 · P5 9:30–10:30 · P6 10:30–11:30 · P7 11:30–12:00.

## Work blocks (TZ=Asia/Kolkata)
| block | start | end | phases | elapsed at end |
|---|---|---|---|---|
| 1 | 2026-09-29 18:27 IST | 2026-09-29 18:40 IST (session usage limit: all 9 running agents failed with HTTP 429) | P0 done; P1 started | 0:13 |
| 2 | 2026-09-29 21:30 IST | | P1– | |

## Phase status
| phase | status | notes |
|---|---|---|
| P0 Audit | done (2026-09-29 18:39 IST) | AUDIT.md: ascetic lens has no user-facing entries yet; person-layer kleśa/hindrance/fetter/kaṣāya/vṛtti ids all skeleton; 20 spot-checks: 17 faithful, 3 partly; restricted-flag gaps listed |
| P1 Ontology sufficiency | running (since 18:36 IST) | ALL core texts text-verified and merged (2,833+ teachings): Gītā (all 736), YS + Vyāsa, Māṇḍūkya + Kārikā, VBT, Satipaṭṭhāna/Mahāsatipaṭṭhāna/Ānāpānasati, Heart Sūtra ×2, HYP, Dhammapada, Visuddhimagga selections, Tattvārtha (karma/passions; ch9–10), TaittU sheaths, KU chariot. Diagnosis 102/102 usable; practices 35 usable, 19 gentle; tables rebuilt (obstacle 16/16, one-truth 6/8, path-map 53/77). Restricted practices/teachings redacted to summary-only in merged data. Running: practice-layer refresh, onto-deep self-question. |
| P2 Engine design | started early, in parallel (22:45 IST) | ENGINE_SPEC.md; mapping rules (onto-deep); intake.json; tone.md; synthesis_rules.json; content design running (onto-analyst) |
| P3 Build | started early, in parallel | written: llm, store, safety, claims, specificity, ontology, report, engine, pathway, synthesizer, schemas, service, cli, content, gates, run_eval. Builders running: mapper; api + web + tests |
| P4 Content engine | drafts done early (23:20 IST), rules engine | 50 posts (10 per bucket, 5 formats) in the review queue, all passing rules checks; 30-day calendar per bucket (content/calendars/); export content/queue.jsonl. Model-engine drafts and the Opus content check: not run (no API key). |
| P5 Evaluation | queued | |
| P6 Fix loop | queued | |
| P7 Release | queued | |

---

# Progress

Resume point for "continue". Update after every lineage (unit) and every text.

## Phase A — Frame
- [x] folder, CLAUDE.md, .gitignore, config/principles.md, config/data_model.md, config/coverage_map.md (A–H verbatim + I verbatim), config/registry.md, config/briefs/skeleton.md
- [x] scripts/validate_shard.py, scripts/shardlib.py
- [ ] scripts/merge.py, scripts/build_atlas.py, scripts/stats.py
- [ ] data files (empty), ultimate node, glossary seed (U53)

## Phase B — Skeleton sweep (59 units)
(status per unit: queued / running / done / merged)

| unit | status | counts | note |
|---|---|---|---|
| U01-vedic-samhitas | done | 70 src · 91 tch · 290 tea (65 originals) · 232 trm · 68 cpt · 43 prc · 13 dsp | report saved |
| U02-brahmana-vedanga | done | 164 src · 89 tch · 288 tea (~190 spot-checked) · 157 trm · 89 cpt · 47 prc · 11 dsp | report saved |
| U03-principal-upanisads | done | 17 src · 85 tch · 446 tea (345 ref-spot-checked) · 165 trm · 72 cpt · 57 prc · 5 dsp | report saved |
| U04-minor-upanisads | done | 115 src (all 95 non-principal Muktikā texts) · 57 tch · 524 tea · 156 trm · 80 cpt · 51 prc · 19 pth · 9 dsp | report saved |
| U05-gita-epic | done | 98 src · 102 tch · 487 tea (325 Gītā, all 18 ch.; 91 originals letter-checked) · 184 trm · 62 cpt · 41 prc · 12 dsp · 4 pth | report saved |
| U06-other-gitas | done | 78 src · 54 tch · 301 tea · 95 trm · 34 cpt · 39 prc · 3 pth · 4 dsp | report saved |
| U07-puranas | done | 58 src · 45 tch · 208 tea · 173 trm · 65 cpt · 35 prc · 13 obs · 8 pth · 8 dsp | report saved |
| U08-agama-catalogue | done | 125 src · 33 tch · 65 tea · 116 trm · 52 cpt · 29 prc · 7 dsp; +5 sub-lineages | report saved |
| U09-samkhya | done | 31 src · 41 tch · 218 tea (all 72+1 kārikās) · 142 trm · 49 cpt · 15 dsp · 2 pth | report saved |
| U10-yoga | done | 19 src · 18 tch · 335 tea (all 195 sūtras + 120 bhāṣya) · 204 trm · 72 cpt · 34 prc · 27 obs · 6 pth · 9 dsp | report saved |
| U11-nyaya-vaisesika | done | 58 src · 40 tch · 259 tea · 226 trm · 76 cpt · 19 new dsp · 2 pth | report saved |
| U12-mimamsa | done | 57 src · 49 tch · 146 tea (99 originals) · 154 trm · 64 cpt · 16 dsp · 3 pth | report saved |
| U13-advaita | done | 109 src · 67 tch · 302 tea · 171 trm · 86 cpt · 29 prc · 18 dsp · 4 pth | report saved |
| U14-visistadvaita | done | 3 lin · 93 src · 53 tch · 118 tea · 142 trm · 61 cpt · 18 prc · 12 dsp | report saved; id note: src:tatparyacandrika clash (U05 vs U15) |
| U15-dvaita | done | 98 src · 37 tch · 107 tea (96 checked in e-texts) · 107 trm · 56 cpt · 19 prc · 6 dsp | report saved |
| U16-bhedabheda | done | 121 src · 80 tch · 155 tea · 128 trm · 75 cpt · 25 prc · 14 dsp · 4 pth | report saved |
| U17-pasupata-kapalika | done | 5 lin · 28 src · 28 tch · 130 tea · 131 trm · 43 cpt · 40 prc · 8 dsp | report saved |
| U18-saiva-siddhanta | done | 3 lin · 61 src · 100 tch (all 63 Nāyaṉmārs) · 138 tea · 90 trm · 37 cpt · 29 prc · 7 dsp | report saved |
| U19-kashmir-saivism | done | 89 src · 45 tch · 352 tea (all 77 ŚS, 20 PH, 112 VBT dhāraṇās) · 144 trm · 46 cpt · 137 prc · 6 dsp | report saved |
| U20-virasaiva | done | 75 src · 78 tch · 157 tea (57 with exact SSM verse) · 119 trm · 43 cpt · 23 prc · 10 dsp | report saved |
| U21-natha-aghora | done | 4 lin · 42 src · 38 tch · 171 tea (115 ref-checked, 104 originals) · 115 trm · 83 cpt · 36 prc (11 restricted) · 7 dsp | report saved |
| U22-tamil-siddha | done | 2 lin · 47 src · 37 tch · 157 tea (124 with originals from local e-texts) · 98 trm · 60 cpt · 26 prc · 6 dsp | report saved |
| U23-sakta-srividya | done | 4 lin · 63 src · 47 tch · 157 tea (127 high) · 136 trm · 74 cpt · 34 prc · 6 dsp | report saved; tch:laksmidhara homonym remapped |
| U24-kali-kaula | done | 4 lin · 54 src · 20 tch · 116 tea (82 verse-checked) · 120 trm · 81 cpt · 27 prc (10 restricted) · 6 dsp | report saved |
| U25-alvar-bhakti-theory | done | 2 lin (new lin:bhakti-sastra) · 41 src · 28 tch (12 Āḻvārs) · 149 tea · 98 trm · 40 cpt · 26 prc · 4 dsp | report saved |
| U26-regional-bhakti | done | 14 lin · 102 src · 109 tch · 182 tea (61 originals) · 93 trm · 69 cpt · 34 prc · 9 dsp | report saved |
| U27-sant-baul | done | 21 lin · 63 src · 94 tch (49 recent) · 166 tea · 122 trm · 67 cpt · 32 prc (5 restricted) · 7 dsp | report saved |
| U28-hatha-texts | done | 31 src · 35 tch · 288 tea (96 HYP with originals) · 122 trm · 65 cpt · 12 prc · 27 phn · 3 dsp | report saved |
| U29-hatha-practices | done | 141 prc (19 restricted) · 354 tea (57 originals) · 42 trm · 15 phn · 1 dsp | report saved; 107 tea ids shared with U28 (union at merge) |
| U30-ayurveda-rasa | done | 5 lin · 69 src · 97 tch · 259 tea (71 originals) · 181 trm · 112 cpt · 32 prc · 15 dsp · 68 restricted | report saved |
| U31-sound-arts | done | 4 lin · 76 src · 81 tch · 148 tea · 119 trm · 38 cpt · 19 prc · 12 dsp | report saved |
| U32-jyotisa | done | 5 lin · 92 src · 78 tch · 125 tea (116 spot-checked) · 164 trm · 83 cpt · 23 prc · 11 dsp | report saved |
| U33-sramana | done | 4 lin · 66 src · 28 tch · 180 tea (opponents' reports flagged) · 106 trm · 66 cpt · 9 prc · 10 dsp | report saved |
| U34-jain-canon | done | 24 lin · 141 src · 163 tch (all 24 Tīrthaṅkaras) · 168 tea · 105 trm · 75 cpt · 32 prc · 16 dsp | report saved |
| U35-jain-philosophy | done | 1 lin · 128 src · 65 tch · 427 tea (256 Tattvārtha, sūtra wording local) · 406 trm · 97 cpt · 54 prc (7 restricted) · 7 dsp | report saved |
| U36-pali-suttas | done | 2 lin · 200 src · 117 tch · 447 tea (all segment-checked, 96 Pali originals) · 303 trm · 153 cpt · 74 prc · 11 dsp | report saved |
| U37-abhidhamma-visuddhimagga | done | 16 lin · 80 src · 53 tch · 222 tea (109 Pali originals read locally) · 190 trm · 58 cpt · 81 prc · 20 dsp | report saved |
| U38-early-schools | done | 31 lin · 85 src · 47 tch · 197 tea (114 AK kārikās quoted) · 181 trm · 62 cpt · 25 prc · 18 dsp · 50 brw | report saved |
| U39-mahayana-sutras | done | 2 lin · 98 src · 53 tch · 265 tea (171 located locally, 91 originals) · 139 trm · 87 cpt · 38 prc · 8 dsp | report saved |
| U40-madhyamaka | done | 4 lin · 70 src · 30 tch · 228 tea (105 MMK with GRETIL originals; 159 originals) · 124 trm · 76 cpt · 21 prc · 7 dsp | report saved |
| U41-yogacara-pramana | done | 7 lin · 120 src · 51 tch · 177 tea (91 originals checked locally) · 198 trm · 71 cpt · 22 prc · 15 dsp | report saved |
| U42-chan-zen | done | 143 src · 228 tch · 244 tea (189 with verified CBETA original) · 11 dsp | REPORT.md; Japanese texts not local |
| U43-pure-land | done | 77 src · 89 tch · 193 tea (93 originals verified: CBETA 89, GRETIL 4) · 14 dsp | REPORT.md; Japanese texts not local |
| U44-indian-vajrayana | done | 100 src · 133 tch · 303 tea (244 originals read locally; 23 restricted) · 27 prc (9 restricted) · 6 dsp | REPORT.md; Hevajra/Saṃvara/Kālacakra Sanskrit not local |
| U45-nyingma-bon | done | 125 src · 82 tch · 101 tea (23 read in Derge) · 43 prc (8 restricted) · 5 dsp | REPORT.md; Seventeen Tantras, Longchenpa, Bön not local |
| U46-kagyu | done | 52 src · 74 tch · 147 tea (59 from local Derge with Wylie originals) · 45 prc (restricted six-yoga methods summary-only) · 3 dsp | REPORT.md; Tibetan-authored works not local |
| U47-sakya-kadam-gelug | done | 84 src · 84 tch · 251 tea (66 Wylie originals from Derge: Lamdre root Tōh 2284, Atiśa) · 12 dsp | REPORT.md; Tibetan-authored works recalled |
| U48-jonang-chod-medicine-rime | done | 51 src · 45 tch · 90 tea · 12 prc (5 restricted) · 3 dsp | REPORT.md; Four Tantras chapter refs low; Tibetan works not local |
| U49-cross-family | done | 53 brw (41 new + 12 evidence re-emits) · 36 cpt · 31 tea · 3 dsp; new explicit evidence: Tōh 2285 Amṛtasiddhimūla colophon (Virūpa) | REPORT.md; dedupe list for S5 |
| U50-debates | done | 15 dsp (8 partially reconciled, 7 queued) · 19 new tea (originals verified: BSBh, CBETA, eBhāratī) | REPORT.md |
| U51-path-maps | stopped by user (partial kept) | | |
| U52-recent-teachers | stopped by user (partial kept) | | |
| U53-glossary-ultimate | stopped by user (partial kept) | | |
| U54-chinese-schools | stopped by user (partial kept) | | |
| U55-japan-korea-vietnam-nepal | queued | | |
| U56-datta-haridasa-odisha | queued | | |
| U57-ascetic-orders | queued | | |
| U58-sacred-sciences-body-arts | queued | | |
| U59-folk-regional | queued | | |
| U60-ganapatya-saura-smarta | queued | | added to close gaps |

## PAUSED — 2026-09-29 18:18 IST: all running agents were stopped by the user
Nothing has been relaunched. The fallback check-in (trig_01TAWjatPpGAGwbxcCz6ynAP) is disabled, so no new agents start. On "continue", restart these items; restarting fresh is safest, and each agent's partial output is kept.

| item | state at stop | what is on disk |
|---|---|---|
| U51-path-maps (skeleton) | stopped mid-run | 37 paths, 15 teachings, 3 sources, 150 interpretation-log lines — valid (0 errors), no REPORT |
| U52-recent-teachers (skeleton) | stopped mid-run | 48 lines (lineages / ultimate views begun) — valid, no REPORT |
| U53-glossary-ultimate (skeleton) | stopped while surveying | nothing written |
| U54-chinese-schools (skeleton) | stopped at start | nothing written |
| C-U08, C-U09, C-U10, C-U11 (Phase C sweeps) | stopped | no checks written (drafts only in _gen/, if any) |
| Gītā ch16-18 merger M (+ thesis) | stopped at start | nothing written; A.jsonl (137) and B.jsonl (136) with notes are complete and waiting |
| lojong root reconstruction (Phase D prep) | stopped at start | nothing written |

## Phase C — Hallucination sweep
| unit | status |
|---|---|
| U05-gita-epic | done — 689 checked: 683 confirmed · 5 partial · 1 corrected · 0 not-found |
| U01-vedic-samhitas | done — 502 checked: 492 confirmed · 9 partial · 1 corrected (RV 10.88.15 srutī) · 0 not-found |
| U02-brahmana-vedanga | done — 723 checked: 689 confirmed · 17 partial · 17 corrected · 0 not-found (157 terms not in scope) |
| U03-principal-upanisads | done — 736 checked: 729 confirmed · 2 partial · 5 corrected (fabricated default edition strings) · 0 not-found |
| U04-minor-upanisads | done — 915 checked: 772 confirmed · 20 partial · 123 corrected (95 default Adyar edition strings; overlong verse ranges) · 0 not-found |
| U06-other-gitas | done — 556 checked: 522 confirmed · 13 partial · 20 corrected (13 copied Mokṣadharma dating defaults) · 1 not-found (tea:uttara-gita:1) |
| U07-puranas | done — 470 checked: 453 confirmed · 11 partial · 6 corrected · 0 not-found |
| U08-agama-catalogue | stopped by user — to restart |
| U09-samkhya | stopped by user — to restart |
| U10-yoga | stopped by user — to restart |
| U11-nyaya-vaisesika | stopped by user — to restart |
### Sweep follow-ups (for Phase D / S5 / later sweeps)
- C-U06:
  - Local but missed by the unit: the Yoga Vāsiṣṭha vulgate with the Tātparyaprakāśa (Muktabodha M00335–339, M00345) and the Laghu Yoga Vāsiṣṭha with the Vāsiṣṭhacandrikā (M00351). Phase D can extract from them.
  - The Akṣi Upaniṣad reproduces Mokṣopāya 6.140–141, not 3.118 (for U04).
  - The Pāṇḍava Gītā has three speakers that the paraphrase merges.
  - Devī Bhāgavata 7.39.43–46 (not 7.40) ranks inner worship above outer.
  - The local mAdhva Bhāgavata skips the number 3.25.33.
- U49 dedupe candidates for S5:
  - brw pairs: mimamsa-hermeneutics-to-vedanta / -vedanta; samkhya-to-yoga / samkhya-patanjala-yoga; epic-samkhya / epic-samkhya-to-classical-samkhya; upanisads-to-gita / -bhagavad-gita; adhyatma-ramayana-to-manas / -ramcaritmanas; rasa-sastra-hatha / -hatha-yoga; samkhya-saiva-tattvas / samkhya-to-kashmir-saivism; sautrantika-pramana / sautrantika-to-pramana; kagyu-to-gelug / -mahamudra; kadam-to-kagyu / kadam-to-dakpo-kagyu.
  - brw:pure-land-chan: U42 gives a direction (from→to); U43 gives mutual.
  - brw:ayurveda-to-sowa-rigpa: U30 and U48 give different 'what' text.
  - prc:bhutasuddhi / prc:bhuta-suddhi.
- C-U07:
  - tea:garuda-purana:1.142 and cpt:avatara-lists: GP 1.142 is titled daśāvatāra, but its list lacks Vāmana, Kṛṣṇa, Buddha and Kalki. Do not cite it for the standard ten.
  - tea:narada-purana:1.92-109: the paraphrase still names Sanandana; the speaker is Sanātana.
  - tea:padma-purana:nama-aparadha: the edition reads 'śubhasya śrīviṣṇoḥ', where the Gauḍīya citation has 'śivasya'.
  - tch:sanatkumara: 'eldest of the Kumāras' is unsupported.
  - tea:garuda-purana:2.49: 'devotion to Viṣṇu' is not in the chapter.
  - tea:agni-purana:376-379: 'the world is superimposed' was not located.
  - LiP 1.8.2 and the prc:hrt-padma-dhyana warning soften the text; 'Śrīkaṇṭha' is not in ŚiP 7.2.39.
  - Local texts the unit missed: Padma (peterFreund, eBhāratī), Devī Bhāgavata (eBhāratī), full Matsya and Mārkaṇḍeya (peterFreund), early Skanda (sarit), and upapurāṇas on Muktabodha.
- C-U04:
  - tea:yogatattva-upanisad:12-13 and obs:yogatattva-twenty-dosas: the text says the freed jīva is "kevala"; only Yogaśikhā 1.11 has "śiva ucyate".
  - tea:amrtanada-upanisad:2-3: the seeker is "devoted to Rudra", not going to Rudra's world.
  - ult:sannyasa: cites "Avadhūta 1" for "the jīva is Śiva"; the passage is at Maitreya 2.1 and Skanda 6-10.
  - Missing editions: Kaṭhaśruti (Schrader 1912; eBhāratī) and Kālikā (Tantrik Texts XI).
  - Āśrama Upaniṣad dating: Olivelle 3rd c. CE.
  - Jīvanmuktiviveka: author Vidyāraṇya.
  - Yatidharmasamuccaya dating: c. 11th–12th c.
- C-U05: tea:moksadharma:12.289 — the arrow-maker simile is at 12.171.61, not 12.289 (12.289.31 has an archer); fix in extraction. tch:hanuman summary says "four sciences" but MBh 3.149.31 says three (tisro vidyāḥ) — shared by U04/U06/U05, fix in S5. U13 sweep: check tch:sankara's dating framing (788–820 CE is the older scholarly convention, not "most maṭha traditions"; Kāñcī gives 509–477 BCE). tea:vyadha-gita:3.197 has ref "3.196-197".

- C-U01: tea:atharvaveda-saunaka:2.32 paraphrase imports 'visible and invisible' and 'with a stone' from AVŚ 2.31; trm:samana — no Saṃhitā occurrence found (BĀU 1.5.3 has it); src:jnanayajna 'c. 11th c.' and src:vedadipa 'c. 1589' unsupported; use GRETIL (not DharmicData) for RV verse text.
- S4 note: prc:mahamrtyunjaya-japa has method summaries from U01 (Vedic) and U32 (jyotiṣa remedy) — merge must keep both as per-lineage content, not let one replace the other. U32 kuja-dosa and kāla-sarpa entries have no classical verse located (recent/unsourced — sweep first).
- C/Phase D note (U37): the 'sixteen insight knowledges' are a later systematization (Vism has 9 within the 6th purification, Abhidhammatthasaṅgaha 10); the heart-base is commentarial (Paṭṭhāna names only 'the matter in dependence on which'). prc:nesajjikanga flagged restricted.
- S5 note (U39): tch:maitreya-bodhisattva = U36's tch:metteyya (same figure, Pali/Sanskrit ids; relate, do not merge ids blindly — tch:maitreya is the Upaniṣadic sage); trm:vyakarana-prediction ≠ trm:vyakarana (grammar).
- C-U03 fidelity notes for Upaniṣad extraction: BĀU 4.3.33 (learned brahmin clause applies from gods-by-birth up), ChU 5.2.4-8 (consecration new moon, rite full moon), MaiU 3.5 lists loose, 'Viśvajit' at KU 1.1.1 is Śaṅkara's gloss; tch:usasti-cakrayana identity (Uṣasti ChU = Uṣasta BĀU) unsupported. Prepared TU segments lacked 3.8–3.9 (no verse marks) — FIXED 09-29 (TU now 51 units; see DECISIONS). Generator default edition strings were fabricated in U03 — watch for the same in other units' sweeps.
- S5 dedupe candidates (reported by units): U04 prc:mahabandha-mahavedha → U29 prc:mahabandha + prc:mahavedha; U24 cpt:satkarma (tantric six acts) ≠ U28 cpt:satkarma-doctrine (haṭha six acts) — never merge; U28/U29 overlapping HYP/GS range teachings (≈53) — Phase D decides; U10's YBh 2.46 paraphrase may omit vīrāsana; cpt:vyoma-pancaka (U04) = cpt:five-vyomas (U21); cpt:three-laksyas categories differ U04/U21; prc:viparitakarani (U28/U29) vs prc:viparita-karani (U21); prc:sanmukhi-mudra vs prc:shanmukhi-mudra (U04); tea overlaps on U04's Śākta Upaniṣad range teachings vs U23's verse teachings (fidelity pass decides levels).

## Gap hunter (after C)
## Phase D — Verified core
| text | chunk | A | B | M | F | gates |
|---|---|---|---|---|---|---|
| bhagavad-gita | ch01-03 | done (165) | done (165) | done (165 tea, 554 disagreements; skeleton 72 up · 1 corr · 0 ret) | done: 151 passed · 14 fixed · 0 failed → text-verified | |
| bhagavad-gita | ch04-06 | done (123) | done (125) | done (124 tea, 534 disagreements; skeleton 63 up · 4 corr · 0 ret) | done: 109 passed · 15 fixed · 0 failed → text-verified | |
| bhagavad-gita | ch07-09 | done (95) | done (95) | done (97 tea, 449 disagreements; skeleton 40 up · 6 corr · 0 ret) | done: 68 passed · 29 fixed · 0 failed → text-verified | |
| bhagavad-gita | ch10-12 | done (120) | done (120) | done (125 tea, 498 disagreements; skeleton 33 up · 3 corr · 0 ret) | done: 121 passed · 4 fixed · 0 failed → text-verified | |
| bhagavad-gita | ch13-15 | done (85) | done (88) | done (88 tea, 545 disagreements; skeleton 23 up · 19 corr · 0 ret) | done: 86 passed · 2 fixed · 0 failed → text-verified | |
| bhagavad-gita | ch16-18 | done (137) | done (136) | stopped by user — to restart (+ thesis) | | |
| seven-point-mind-training + eight-verses | root reconstruction from OpenPecha lemmata (prep) — stopped by user, to restart | | | | | |

### Gītā text-level gates (after ch16-18)
- One consistency pass across all 18 chapters: citta/cetas → "thought (citta/cetas)" (ch. 6.18–23 still read "mind (citta)"), reflexive ātman, adhyātma gloss; one policy for the level tag 'bridging' vs 'unmarked'; resolve forward links to later chapters (13.x uses this edition's numbering); errata pass for the edition's glitches (DECISIONS 2026-09-28); then the quality gates (misreading hunter, hallucination hunter, reconciliation auditor, reviewer 5%) and the thesis entry by the ch16-18 merger.
- From ch13-15 F:
  - cetas is now 'thought' in ch13-15; align ch10-12 final (11.51, 12.5, 12.7, trm:cetas).
  - Repoint dsp:saguna-nirguna's skeleton span 15.16-18 to the verse entries.
  - Give dsp:souls-one-or-distinct's epic side rests_on (13.3, 13.23, 15.7).
  - Fix the vulgate numbering in cpt:twenty-virtues-called-knowledge's name (13.8–12 here).
  - Names that go beyond the verse: cpt:asvattha-tree ('of saṃsāra'), cpt:vaisvanara.
  - trm:lobha's language conflict.
  - One policy for the 'ultimate' and 'bridging' level tags.
- From ch10-12 F:
  - cetas is rendered "awareness (cetas)" in ch10-12 but "thought (cetas)" in ch04-09 — fix one rendering;
  - the 'ultimate' level tag is used for praise of the Lord as paraṃ brahma (10.12, 10.15, 11.18, 11.37, 11.38, 12.3), while similar descriptions are 'unmarked' — one policy;
  - shared-entity names that go beyond the verse: prc:kirtana ("singing") at 10.9 and 11.36; tch:bhrgu "Vāruṇi"; tch:kapila as founder of Sāṃkhya; tch:brhaspati as Lokāyata;
  - 11.54 śakyam/śakya aham — variant or glitch;
  - dedupe prc:vandana ≈ prc:namaskara;
  - check the commentators' positions recalled in the 12.1–5 and 12.12 notes against the bhāṣyas in Wave 2.

Prepared verse-level segments (sources_raw/prepared/, git-ignored) as of 2026-09-28 04:51 IST:
- [x] bhagavad-gita (701 verses; gita/gita vulgate) — 6 chunks of 3 chapters
- [x] yoga-sutra (195 sūtras + Vyāsa bhāṣya; GRETIL, Āgāśe ed.) — 4 chunks (pādas)
- [x] principal Upaniṣads (Advaita Śāradā mūla, traditional numbering): īśa 18, kena 35, kaṭha 120, praśna 67, muṇḍaka 65, taittirīya 51 units (1.12, 3.8, 3.9 recovered 09-29), aitareya 33, chāndogya 629, bṛhadāraṇyaka 441, śvetāśvatara 113, kauṣītaki 51; māṇḍūkya 12 (GRETIL); maitrī 73 (below)
- [x] Pali (bilara-data, CC0 with Sujato): DN 22 (22 sections), MN 10 (41), MN 118 (43), SN 56.11 (14), Dhammapada (423 verses)
- [x] sāṃkhya-kārikā (72; GRETIL/Jayamaṅgalā ed.), māṇḍūkya-kārikā (214; GRETIL), vijñāna-bhairava (162), śiva-sūtra (75 in Bhāskara's recension = 77 in Kṣemarāja's; refs to be given in Kṣemarāja's numbering), spanda-kārikā (53)
- [x] haṭha-yoga-pradīpikā (387 verses), platform sūtra (CBETA T2008 162 sections; Dunhuang T2007 86), heart (T251 9; Sanskrit short 10), diamond (CBETA T235 127)
- [x] mūlamadhyamakakārikā (448 verses, GRETIL Devanāgarī mirror, 4 chunks), aṣṭāvakra gītā (298 verses, GRETIL, 2 chunks), pratyabhijñāhṛdayam (20 sūtras + Kṣemarāja's commentary + intro, GRETIL), avadhūta gītā (275 verses of the 1917 Khemrāj ed., 8 chapters; 5 refs to recover by hand — see META known_gaps)
- [x] tattvārtha-sūtra (357 sūtras, Digambara recension, nikkyjain Jain DB), Tilopa's Gaṅgā Mahāmudrā (Tōh 2303, 29 stanzas + title/colophon, Tibetan + Wylie), Saraha's People/King/Queen Dohās (Tōh 2224: 136 st.; 2263; 2264)
- [x] maitrī (73 sections in 7 prapāṭhakas, Cowell/Rāmatīrtha recension, eBhāratī)
- [x] lojong sources located (not prepared as segments): Seven Points root = lemmata in Blo sbyong legs bshad kun 'dus (OpenPecha P000258); confirmations P000209, P000200; Eight Verses + Chekawa's commentary P000222 — see GAPS/DECISIONS

## Morning report (07:00 IST)
## Waves 1–5
