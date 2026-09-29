# U03-principal-upanisads — Phase C hallucination sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's sweep subagent, since subagents cannot write report files in this harness; saved by the orchestrator.)_

Output file: `shards/sourcing/U03-principal-upanisads/checks.jsonl` (736 lines). Validation with `scripts/validate_shard.py` gives 0 errors.
Generator scripts and drafts are in `shards/sourcing/U03-principal-upanisads/_gen/`: `lib.py` and `refs.py` locate refs, `b_src`, `b_tch`, `b_tea` and `b_rest` build the checks, `assemble.py` writes the file, and the `*_view.txt` files are the review views.

## 1. Numbers

| type | checked | confirmed | partially | corrected | not-found |
|---|---|---|---|---|---|
| src | 17 | 11 | 1 | 5 | 0 |
| lin | 1 | 1 | 0 | 0 | 0 |
| tch | 85 | 84 | 1 | 0 | 0 |
| tea | 446 | 446 | 0 | 0 | 0 |
| ult | 1 | 1 | 0 | 0 | 0 |
| cpt | 72 | 72 | 0 | 0 | 0 |
| prc | 57 | 57 | 0 | 0 | 0 |
| obs | 14 | 14 | 0 | 0 | 0 |
| phn | 26 | 26 | 0 | 0 | 0 |
| pth | 5 | 5 | 0 | 0 | 0 |
| dsp | 5 | 5 | 0 | 0 | 0 |
| brw | 7 | 7 | 0 | 0 | 0 |
| **total** | **736** | **729** | **2** | **5** | **0** |

By method:
- **text-locate:** 708
- **text-locate+websearch:** 11
- **catalog+websearch:** 8
- **catalog+text-locate+websearch:** 6
- **websearch:** 3

No terms were checked: none has low confidence (154 high, 11 moderate). The interpretation log is outside the scope.

## 2. Method

**Teachings.** Every ref of all 446 teachings was found in `sources_raw/prepared/<slug>/segments.jsonl`, using each edition's own numbering:
- Advaita-Śāradā mūla for 11 texts
- GRETIL for the Māṇḍūkya
- eBhāratī Ebharati-9566 (Cowell numbering) for the Maitrī
- Advaita-Śāradā numbering for the Kauṣītaki

Each passage was read against its paraphrase. The 73 `original` quotations were also matched by fuzzy n-grams; all match apart from sandhi differences and the numbering cases in §5.

**Other entries.** Every inline Upaniṣad ref and every `rests_on` teaching in the concepts, practices, obstacles, phenomenology, paths, disputes, borrowings, lineage and ultimate entries was checked automatically: all refs exist, and every `rests_on` teaching is one confirmed here. Claims that point outside the Upaniṣads were checked locally:
- ŚB 10.6.1 and 10.6.3 (GRETIL)
- TB 3.11.8 (raw_etexts Kāṭhaka)
- VSM 11.1-5 (DCS)
- JUB 4.18-21 (DCS)
- nine Ṛgveda verses (DCS)
- BhG 2.19-20, 8.11, 13.x and 15.1
- the MMK dedicatory verse
- YS 2.29
- Brahma Sūtra 1.1.28, 1.4.1 and 2.1.17 (Advaita-Śāradā)

**Teachers.** All 85 were located by name at the passages they cite.

**Web.** Web searches covered texts, dates, placements and scholarly points.

## 3. Not-found (possible hallucinations)

None. Every text, teacher, verse ref and named list could be located. The closest cases to fabrication are the default edition string on five sources (§4) and the unsupported Uṣasti = Uṣasta identity (§6).

## 4. Corrections (in `corrections`, in the entry's own schema)

**`src:maitri-upanisad` → `editions`.** The first "original" edition, "Sanskrit text with Śaṅkara's bhāṣya (Advaita-Śāradā e-text)", does not exist: there is no Śaṅkara commentary and no Advaita-Śāradā file for the Maitrī.
- It is replaced by eBhāratī Ebharati-9566, which is Cowell's recension with Rāmatīrtha's Dīpikā.
- Hume and Cowell (Bibliotheca Indica, 1870, archive.org) are kept.

**`src:baskala-upanisad`, `src:chagaleya-upanisad`, `src:arseya-upanisad`, `src:saunaka-upanisad` → `editions`.** All four carried the same wrong "Śaṅkara's bhāṣya, Advaita-Śāradā" edition, a generator default. They are replaced by:
- S. K. Belvalkar, *Four Unpublished Upaniṣadic Texts* (1925), confirmed on Google Books, for all four;
- the sanskritdocuments.org e-text, added for the Chāgaleya;
- eBhāratī Ebharati-9441 (Deccan College), added for the Ārṣeya.

Other facts confirmed for these four:
- **Bāṣkala:** 25 verses; Indra as a ram and Medhātithi; part of the Persian Oupnek'hat collection.
- **Ārṣeya:** Viśvāmitra's brahmodya opening, followed by Jamadagni, Bharadvāja, Gautama and Vasiṣṭha (local e-text).
- **All four:** manuscripts described in Schrader's 1908 Adyar catalogue.

## 5. Numbering and text notes (refs confirmed, recorded in the notes)

- **MuU 2.2.7–2.2.11** are cited in the common numbering. The Advaita-Śāradā text splits 2.2.7, so it is one higher from 2.2.8 on. The Śarvānanda edition in eBhāratī numbers "bhidyate hṛdayagranthiḥ" 2.2.8, which confirms the common numbering. Concept and obstacle entries citing MuU 2.2.8 or 2.2.10 use the same numbering.
- **BĀU 5.1.1:** "pūrṇam adaḥ" is missing from the Advaita-Śāradā segment, which prints it only as an invocation, but GRETIL (with Śaṅkara's commentary) has it at 5.1.1.
- **BĀU 5.15.1-4:** the e-text prints the four verses as one segment.
- **BĀU 3.7.1 and 3.3.1:** the Advaita-Śāradā text reads "Patañjala Kāpya"; GRETIL reads "Patañcala Kāpya", as the entries do.
- **TU 3.8–3.9:** missing from the prepared TU segments because they have no verse marks, but present in the raw `mUla/Taitiriya.md`. Worth fixing in `sources_raw/prepared/taittiriya-upanisad`.
- **KauU:** the refs follow the Advaita-Śāradā numbering (2.5, 2.15, 3.9 as the skeleton says). The landmark names in 1.3 are confirmed in both reading sets: Virajā, Tilya, Sāyujya (Śāradā) and Vijarā, Ilya, Sālajya (web translation).
- **MaiU 6.34:** the mind verses are in the Cowell text. "mana eva manuṣyāṇāṃ …" follows them in the same e-text but is not in the prepared root segment. No U03 entry cites that verse.
- **ChU 4.10.4:** "prāṇo brahma kaṃ brahma khaṃ brahma" is at 4.10.4, as the skeleton report's correction says.
- **Gītā parallel:** ŚU 3.16-17 ≈ BhG 13.13-14 holds in the 34-verse numbering; the prepared Gītā has them as 13.14-15.

## 6. Partially confirmed

- **`tch:usasti-cakrayana`:** both Uṣasta Cākrāyaṇa (BĀU 3.4) and Uṣasti Cākrāyaṇa (ChU 1.10-11) are located. No outside source identifies them as one person; the identity rests only on the shared patronymic, as the entry says.
- **`src:kausitaki-upanisad`:** placement (KĀ 3-6), structure, readings and dating are confirmed. Two things were not checked: that Cowell's section numbering matches the Advaita-Śāradā numbering, and whether the commentary in `kst.md`, headed as Śaṅkara's, is actually his.

## 7. "Least sure" list: outcomes

**Confirmed from the texts:**
- KauU 1.3–1.5 landmarks
- BĀU 4.3.33 levels, in order: fathers → gandharvas → karma-gods → gods by birth → Prajāpati → brahman
- ChU 3.13 pairings
- ChU 4.5–9 quarter names: prakāśavān, anantavān, jyotiṣmān, āyatanavān
- MaiU 3.5 lists
- MaiU 6.1-2
- MaiU 6.29 wording and section number
- all 24 MaiU refs, in Cowell numbering

**Confirmed by an outside source or a second local text:**
- TB 3.11.8 as the older Naciketas story
- ŚU 2.1-5 = VSM 11.1-5
- the Muktikā places the Maitrī (no. 24) under the Sāmaveda
- Madhva's school (and Rāmānuja) treat the Āgama-prakaraṇa as śruti (Wikipedia, Gauḍapāda)
- TU 1.10, Kena 4.6 (tadvana) and MuU 3.2.10 (śirovrata) are located
- Belvalkar 1925

**Teachers:**
- **tch:vajasravasa:** KU 1.1.10-11 and TB 3.11.8 are confirmed; his identity with Uddālaka is rightly left open.
- **tch:ayasya-angirasa** (low confidence): confirmed; he also appears in the BĀU lineage lists (2.6.3, 4.6.3).
- **tch:kapila** (low confidence): confirmed; both readings of ŚU 5.2 are attested on the web.

**brw:mandukya-madhyamaka-prapancopasama** (low confidence): the phrase is confirmed in MāU 7 and 12 and in the MMK dedication; no direction of borrowing is asserted.

**Scholarly dates:** all consistent with Olivelle's chronology as reported on the web; none clearly contradicted.

## 8. Fidelity notes for Phase D (not existence errors; left as `confirmed`)

- **tea:brhadaranyaka-upanisad:4.3.33:** the clause about the learned brahmin untouched by desire applies only from the gods-by-birth level upward, not to every level.
- **tea:chandogya-upanisad:5.2.4-8:** consecration is on the new-moon day and the rite on the full-moon night; the paraphrase puts the rite on the new moon.
- **tea:maitri-upanisad:3.5 / obs:tamas-rajas-marks-maitri:** "hatred, deceit" are loose renderings, and some list items are omitted.
- **cpt:sixteen-parts:** "fifteen depend on food" is an interpretation of ChU 6.7, not its wording.
- **tch:narada:** the epithet "devarṣi" is later; ChU 7 does not use it.
- **cpt:bhakti:** Max Müller's view that ŚU 6.23 may be a later insertion could be noted.
- **tea:katha-upanisad:1.1.1-4 / tch:vajasravasa:** "Viśvajit" comes from Śaṅkara's gloss, not the text.

## 9. Could not be checked

- The contents of the Śaunaka Upaniṣad.
- The Ṛgveda/Bāṣkala-śākhā affiliation of the Bāṣkala.
- The Veda affiliation of the Chāgaleya and Ārṣeya.
- The Chāgaleya's chariot image: consistent with a web retelling (Kavaṣa Ailūṣa and the Vālakhilyas) that does not name the Upaniṣad.
- The Kauthuma–Rāṇāyanīya detail for the ChU; web results name only the Tāṇḍya school.
- Cowell's own edition of the KauU.
- The historicity of the Upaniṣadic figures beyond their textual attestation.
