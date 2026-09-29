# U40-madhyamaka — skeleton sweep report (Phase B)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map B4 (Madhyamaka), with its D/E/F/G/C items. Owned lineages: lin:madhyamaka, lin:prasangika, lin:svatantrika, lin:yogacara-madhyamaka.
The generators are in `shards/skeleton/U40-madhyamaka/_gen/` (common.py, part1 to part9). Part 9 rebuilds interpretation_log.jsonl from the current equivalents, relations, path bands and reconciliations.

Counts: lineages 4 · ultimate 4 · sources 70 · teachers 30 · teachings 228 · terms 124 · concepts 76 · practices 21 · obstacles 16 · paths 6 · phenomenology 8 · disputes 7 · borrowings 10 · interpretation_log 59.
Validator: 0 errors.

## 0. Corrections to the MUST-COVER list, and id decisions

**Corrections to the list:**
- **MMK dedicatory verses.** They are unnumbered in the GRETIL numbering (448 verses; chapter counts are in the source notes). They are recorded as `tea:mulamadhyamakakarika:0.1-2`, with the original read in the local Vaidya/Tripathi Prasannapadā.
- **MMK 24.18–19.** The identity of dependent origination, emptiness, dependent designation and the middle way is in 24.18 alone. 24.19 says instead that no dharma is non-empty because none is not dependently arisen.
- **MMK chapter titles.** Confirmed from the Prasannapadā colophons. Chapter 12 is Duḥkha-parīkṣā and chapter 16 is Bandhamokṣa-parīkṣā.
- **Vigrahavyāvartanī.** It has 70 verses plus a closing homage (given here as v.71). "No thesis" is v.29. The Chinese is T1631, confirmed in the local CBETA catalogue.
- **Ratnāvalī.** The local GRETIL Sanskrit covers 1.1–4.100 only; chapter 5 is not there. Only the chapter 4 title (rājavṛttopadeśa) is confirmed by a colophon.
- **Śataśāstra.** This is the Chinese Bai lun (T1569): verses ascribed to Āryadeva with Vasu's commentary. Its relation to the Catuḥśataka is uncertain.
- **Catuḥśataka.** Colophons in the local e-text confirm the titles of chapters 8, 9, 10, 13, 14 and 16. The work's own title is Bodhisattvayogācāra-catuḥśataka.
- **Bodhicaryāvatāra.** Chapter 8 contains both equalizing self and other (8.90–96) and exchanging them (8.120–136). The Sanskrit vulgate numbering (DCS) is one lower than the Tibetan in chapter 3.

**Id decisions:**
- **Haribhadra (Buddhist)** is `tch:haribhadra-buddhist`, because `tch:haribhadra` is the Jain Haribhadra Sūri.
- **Jayānanda** is `tch:jayananda-madhyamaka`, because `tch:jayananda` is already the Bengali Vaiṣṇava poet (U16).
- **Madhyamaka vs Nyāya on pramāṇa.** U11 had already created `dsp:establishment-of-pramanas`. I added Madhyamaka and Nyāya sides to it with VV rests_on and no reconciliation, rather than create a duplicate. The self-refutation part of the VV debate became a new id, `dsp:can-emptiness-be-asserted`.
- **Tattvasaṅgraha** is `src:tattvasangraha`, as U12 and U31 use it. U09 uses `src:tattvasangraha-santaraksita` for the same text, so the two need deduping.
- **Shared concepts reused rather than duplicated:** cpt:two-truths, cpt:six-paramitas, cpt:ten-paramitas, cpt:twenty-emptinesses, cpt:two-selflessnesses (U39), cpt:middle-way (U36), cpt:dependent-origination, cpt:tathagata-after-death. U36's cpt:middle-way has category "ethics" and mine "ultimate", so the merge will log a scalar conflict. cpt:bodhicitta is kept as the treatise-level concept, related to U39's cpt:bodhicitta-sutra.
- **Shared terms.** I contributed Madhyamaka definitions to the existing term ids rather than create new ones: pramāṇa, prapañca, vikalpa, avidyā, klesa, nirvāṇa, svabhāva, pratītyasamutpāda, satkāyadṛṣṭi, pāramitā, bodhisattva, pudgala, skandha, sunyata and others.
- **dsp:prasangika-svatantrika** is owned by U50. Both sides are supplied as teachings:
  - Buddhapālita (tea:buddhapalita-vrtti:1.1) and Bhāviveka's critique (tea:prajnapradipa:1.1), both as quoted in the Prasannapadā.
  - Bhāviveka's own syllogism (tea:prajnapradipa:1.1/2).
  - Candrakīrti's reply (tea:prasannapada:1.1) and CŚ 16.25.

## 1. Checklist (coverage map B4 Madhyamaka and the unit brief)

**Nāgārjuna**
- tch:nagarjuna: the tradition's accounts (Laṅkāvatāra prophecy, Kumārajīva's Life, Bu-ston and Tāranātha) and the scholarly account are kept apart.
- **Mūlamadhyamakakārikā** — src:mulamadhyamakakarika:
  - 105 teachings covering the dedication and every chapter 1–27, all with GRETIL originals.
  - Brief's key verses: 0.1-2 (eight negations), 1.1, 13.8, 18.5–9, 24.8–10, 24.14, 24.18–19, 25.19–20, 27.30.
  - Also 24.1–6 (the objection) and 24.7, 24.11–12, 24.15–16, 24.20, 24.32, 24.38, 24.40.
- **Vigrahavyāvartanī** — src:vigrahavyavartani, 11 teachings: vv.1, 5-6, 22, 23, 29, 30, 31-33, 34-39, 46-51, 70, 71.
- **Śūnyatāsaptati** — src:sunyatasaptati: vv.1, 64-65.
- **Yuktiṣaṣṭikā** — src:yuktisastika: vv.5-6, 35, 46-48, 50.
- **Vaidalyaprakaraṇa** — src:vaidalyaprakarana: source entry only (the 16 Nyāya categories).
- **Ratnāvalī** — src:ratnavali, five chapter titles: 1.3-4, 1.5, 1.8-10, 1.26, 1.28, 1.35, 1.36, 1.42, 1.61-62, 2.1, 3.12-13, 4.86, 4.94-96.
- **Suhṛllekha** — src:suhrllekha: v.29.
- **Catuḥstava** — src:catuhstava, plus src:dharmadhatustava.
- Other attributed works: src:bodhicittavivarana, src:pratityasamutpadahrdaya, src:sutrasamuccaya, src:mahayanavimsika, src:bhavasankranti, src:akutobhaya, src:vyavaharasiddhi, src:mahaprajnaparamitopadesa, src:dasabhumika-vibhasa (tea:…:9), src:bodhisambhara-sastra, src:ekaslokasastra.
- Chinese recensions: src:zhong-lun, src:shiermen-lun, src:longshu-pusa-zhuan.

**Āryadeva and Rāhulabhadra**
- tch:aryadeva; src:catuhsataka (16 chapter titles): teachings on ch.1, 8.15, 8.19, ch.10, 12.1, 12.23, 16.25.
- src:satasastra, src:hastavalaprakarana, src:jnanasarasamuccaya, src:tipo-pusa-zhuan.
- tch:rahulabhadra; src:prajnaparamitastotra.

**Buddhapālita**
- tch:buddhapalita, src:buddhapalita-vrtti, tea:buddhapalita-vrtti:1.1.

**Bhāviveka**
- tch:bhaviveka.
- Sources: src:prajnapradipa, src:madhyamakahrdaya (11 chapter titles), src:tarkajvala, src:karatalaratna, src:madhyamakarthasamgraha, src:madhyamakaratnapradipa.
- Teachings: PP 1.1, 1.1/2; MH 3.12, 5, 6, 8 (the Vedānta view, reported), 8/2, 9; TJ 3.26.
- Avalokitavrata: tch:avalokitavrata, src:prajnapradipa-tika.

**Candrakīrti**
- tch:candrakirti.
- Sources: src:prasannapada, src:madhyamakavatara, src:madhyamakavatara-bhasya, src:catuhsataka-tika, src:yuktisastika-vrtti, src:sunyatasaptati-vrtti, src:pancaskandhaprakarana-candrakirti.
- Prasannapadā teachings: 1.1, 13.8, 17.30, 18.7, 24.8 (three meanings of saṃvṛti), 24.18.
- Madhyamakāvatāra teachings: 1.1, 1.2, 1.3-4 (three kinds of compassion), 6.4-5, 6.8, 6.23, 6.28, 6.45-97, 6.80, 6.120, 6.151-160 (sevenfold chariot), 6.179-223.
- Ten grounds: pth:madhyamakavatara-ten-grounds.

**Śāntideva**
- tch:santideva (hagiography kept as the tradition's account).
- Bodhicaryāvatāra (src:bodhicaryavatara), ten chapter titles and 36 teachings:
  - ch.6 patience: 6.1-2, 6.10, 6.21.
  - ch.8 equalizing and exchanging self and other: 8.90-91, 8.95-96, 8.120, 8.129-131, 8.134-136.
  - ch.9 wisdom: 9.1, 9.2, 9.3, 9.15-17, 9.33-35, 9.41-44, 9.54-55, 9.56-57, 9.58-60, 9.73, 9.78, 9.119-126, 9.150-151.
  - Also 10.55-56.
- src:siksasamuccaya: kārikās 1, 2, 4, 20.
- src:bodhicaryavatara-panjika (Prajñākaramati).

**Svātantrika line**
- Jñānagarbha: src:satyadvayavibhanga (tea:…:8-12), src:satyadvayavibhanga-panjika.
- Śrīgupta: src:tattvavatara-vrtti.

**Śāntarakṣita**
- src:madhyamakalamkara: v.1 (neither one nor many), 16-17, 64, 92-93.
- src:madhyamakalamkara-vrtti.
- src:tattvasangraha with its critiques of the other schools: examinations of Īśvara, the self (including the Upaniṣadic view), the Lokāyata, and the seer of the supersensible.

**Kamalaśīla**
- src:bhavanakrama: I (three points; compassion as root; three wisdoms; six faults and eight remedies; nine stages), II, III (bhūtapratyavekṣā).
- src:tattvasangraha-panjika, src:madhyamakalamkara-panjika, src:madhyamakaloka, src:sarvadharmanihsvabhavasiddhi.

**Haribhadra and later Indian authors**
- Haribhadra: tch:haribhadra-buddhist, src:abhisamayalamkaraloka, src:abhisamayalamkara-vivrti.
- Vimuktisena: tch:vimuktisena.
- Atiśa (contribution only): src:satyadvayavatara, src:madhyamakopadesa.
- Jayānanda: src:madhyamakavatara-tika-jayananda, src:tarkamudgara.
- Also: Maitrīpa (src:tattvaratnavali), Ratnākaraśānti, Jitāri (src:sugatamatavibhanga), Abhayākaragupta (src:munimatalamkara), Sthiramati's MMK commentary (src:dasheng-zhongguan-shilun), Kumārajīva, Piṅgala.

**Concepts**

| Brief item | Ids |
|---|---|
| emptiness | cpt:sunyata, trm:sunyata |
| svabhāva / niḥsvabhāvatā | cpt:svabhava-and-nihsvabhavata, trm:svabhava, trm:nihsvabhavata |
| two truths | cpt:two-truths, trm:satyadvaya, trm:samvrti-satya, trm:paramartha-satya, cpt:conventional-truth-divisions, cpt:paryaya-paramartha |
| catuṣkoṭi | cpt:catuskoti, trm:catuskoti |
| prasaṅga vs svatantra | cpt:prasanga-method, cpt:svatantra-anumana, trm:prasanga, trm:svatantra-anumana, lin:prasangika, lin:svatantrika |
| dependent designation | cpt:upadaya-prajnapti |
| emptiness of emptiness | cpt:emptiness-of-emptiness |
| relative and ultimate bodhicitta; aspiration and engagement | cpt:relative-and-ultimate-bodhicitta, cpt:aspiring-and-engaging-bodhicitta |
| six and ten pāramitās | cpt:six-paramitas, cpt:ten-paramitas |
| exchanging and equalizing | cpt:exchanging-self-and-other, cpt:equalizing-self-and-other |
| three kinds of compassion | cpt:three-kinds-of-compassion |
| critiques of other schools | cpt:madhyamaka-critique-of-samkhya / -nyaya / -vedanta / -abhidharma / -yogacara / -mimamsa / -isvara |
| other additions | cpt:eight-negations, cpt:non-arising-four-alternatives, cpt:neither-one-nor-many, cpt:sevenfold-chariot-analysis, cpt:no-thesis, cpt:emptiness-not-a-view, cpt:madhyamaka-doxography |

**Section D, per owned lineage** (ult:madhyamaka, ult:prasangika, ult:svatantrika, ult:yogacara-madhyamaka; the madhyamaka caveat rejects any reading of emptiness as a positive entity):

| D item | Ids |
|---|---|
| consciousness and its states | cpt:nonconceptual-wisdom, cpt:bhutapratyaveksa, cpt:mere-non-thought, cpt:samatha-vipasyana-union |
| self | cpt:self-as-dependent-designation, cpt:fivefold-analysis, cpt:two-selflessnesses, cpt:identity-difference-analysis |
| mind | cpt:mind-in-madhyamaka, cpt:svasamvedana-critique, cpt:prapanca-and-its-pacification |
| body | cpt:body-in-madhyamaka (records that these sūtra-path texts teach no subtle body) |
| matter | cpt:elements-in-madhyamaka |
| obstacles | 16 obs entries, cpt:four-viparyasas |
| ethics | cpt:ten-virtuous-paths, cpt:abhyudaya-naihsreyasa, cpt:bodhisattva-training-siksasamuccaya, cpt:union-of-method-and-wisdom, cpt:two-accumulations, cpt:mahakaruna |
| karma and liberation | cpt:karma-without-svabhava, cpt:avipranasa, cpt:dependent-origination, cpt:twelve-links-in-madhyamaka, cpt:nirvana-in-madhyamaka, cpt:samsara-nirvana-nondifference, cpt:apratisthita-nirvana |
| signs and powers | cpt:fear-of-emptiness, cpt:bhumi-qualities, cpt:omniscience-madhyamaka, 8 phn entries; warnings sit on the practices |
| teacher and transmission | cpt:graded-teaching, cpt:qualified-student, cpt:madhyamaka-lineage-transmission, cpt:neyartha-nitartha-madhyamaka |
| cosmology and time | cpt:time-in-madhyamaka, cpt:cosmology-in-madhyamaka |
| sound and language | cpt:language-and-emptiness |
| death and dying | cpt:death-and-impermanence-madhyamaka, cpt:refutation-of-materialism, prc:contemplating-death-and-impermanence |

**Section E practices**
- Analytical meditation: prc:analytical-meditation-on-emptiness.
- The reasonings: prc:sevenfold-reasoning, prc:four-alternatives-reasoning, prc:neither-one-nor-many-reasoning, prc:dependent-origination-reasoning.
- Vows and devotion: prc:bodhisattva-vow, prc:generating-bodhicitta, prc:sevenfold-worship, prc:confession-of-faults, prc:dedication-of-merit.
- Mind and patience: prc:guarding-the-mind, prc:cultivating-patience, prc:equalizing-self-and-other, prc:exchanging-self-and-other (equivalent to prc:tonglen, graded partial).
- Meditation manuals: prc:samatha-bhavanakrama (nine stages), prc:compassion-meditation-bhavanakrama, prc:three-wisdoms, prc:solitude-and-body-contemplation.
- Restricted: prc:giving-body-enjoyments-merit, summary only, with the texts' own warnings from BCA 5.86–87 and ŚSK 5.
- Also prc:reliance-on-spiritual-friend.
- Obstacles for the brief's items: obs:svabhava-graha (grasping at inherent existence), obs:sunyata-drsti, obs:nihilistic-misreading-of-emptiness, obs:eternalism-annihilationism, obs:satkayadrsti (exact equivalent of obs:sakkaya-ditthi). The other obstacles cover afflictions and meditation faults.

**Section F path maps**
- pth:madhyamakavatara-ten-grounds (relates to U51's pth:ten-bhumis), pth:bodhicaryavatara-sequence, pth:bhavanakrama-stages, pth:ratnavali-two-goods, pth:catuhsataka-three-turnings, pth:madhyamakalamkara-ladder.
- Bands are logged in interpretation_log. The dedication stage and the MAL ladder are left unbanded.

**Section G and new disputes**

New disputes:
- dsp:madhyamaka-nihilism-charge: sides are the realist Buddhist of MMK 24, Śaṅkara, Kumārila, the Yogācāra, and the Madhyamaka. Partially reconciled under P1-level, with the traditions' objections recorded.
- dsp:can-emptiness-be-asserted: queued.
- dsp:madhyamaka-yogacara: partially reconciled under P1-level and P5-neyartha; Candrakīrti's and the Yogācāra objections recorded.
- dsp:svasamvedana: queued.
- dsp:sravaka-realization-of-emptiness: queued.
- dsp:mahayana-as-buddhavacana: queued.

Contributed to an existing dispute: dsp:establishment-of-pramanas (U11).

Supplied as teachings to disputes owned by others:
- dsp:prasangika-svatantrika.
- dsp:sudden-or-gradual (BhK III).
- dsp:is-there-a-self (MMK 9, 10.15-16, 16.2, 18.1, 18.6, 27.8; RĀ 1.28, 2.1; CŚ 10; MA 6.120, 6.151-160; BCA 9.58-60; TS).
- dsp:causation (MMK 1.1, 1.14, 12.1, 20.24; MH 6).
- dsp:isvara (BCA 9.119-126; TS).
- dsp:status-of-veda (MH 9; TS).
- dsp:debate-without-thesis and dsp:own-nature-of-things (both U11).
- dsp:pudgala (U38).

**Section C borrowings**
- Gauḍapāda and Madhyamaka: brw:madhyamaka-to-gaudapada, direction disputed; linked to U03's brw:mandukya-madhyamaka-prapancopasama and to dsp:advaita-crypto-buddhism.
- Also: brw:madhyamaka-to-sanlun, -to-tiantai, -to-pure-land, -to-chan; brw:prasangika-to-gelug; brw:yogacara-madhyamaka-to-nyingma; brw:yogacara-to-yogacara-madhyamaka; brw:pramana-buddhist-to-svatantrika; brw:pramana-buddhist-to-yogacara-madhyamaka.

## 2. Least sure — check these first for hallucination

**Verse numbers from memory, with no local text**
- VV 5-6, 22, 23, 34-39, 46-51, 71.
- ŚS 1, 64-65.
- YṢ 5-6, 35, 46-48, 50. The local Sanskrit agrees but is a back-translation.
- SL 29; RĀ 3.12-13.
- MA 1.2, 1.3-4, 6.4-5, 6.8, 6.28, 6.45-97, 6.80, 6.120, 6.151-160, 6.179-223. Only MA 6.23 is a well-known reference.
- MH 3.12; Tarkajvālā 3.26.
- MAL 16-17, 64, 92-93; SDV 8-12.

**Chapter-level summaries written from memory**
- CŚ ch.1 and ch.10.
- MH 5, 6, 8, 8/2, 9. MH 8/2's claim that the Vedāntins' good points derive from Buddhism is flagged in its notes.
- The four Tattvasaṅgraha examinations. Its "c. 3,600 verses in 26 examinations" is also from memory.
- BhK II (method and wisdom).
- DBV ch.9 "easy practice".

**Low-confidence teachers**
- tch:kamalabuddhi, tch:srigupta, tch:jitari, tch:bodhibhadra, tch:devasarman, tch:gunamati-madhyamaka-commentator, tch:vasu-satasastra, tch:ajitamitra, tch:parahita.
- Conflicting placements of tch:rahulabhadra, recorded as they stand.
- Dates of Prajñākaramati, Avalokitavrata and Jayānanda.

**Traditional accounts and hagiographies from memory**
- Xuanzang's story of Bhāviveka waiting for Maitreya.
- The Jayānanda–Chapa debate.
- Tāranātha's details on Buddhapālita and Haribhadra.
- Śāntideva's hagiography.
- Kamalaśīla's death.

**Low-confidence sources and attributions**
- src:vyavaharasiddhi, src:bhavasankranti, src:mahayanavimsika.
- src:hastavalaprakarana: is D3844 really the Hastavāla?
- src:jnanasarasamuccaya, src:madhyamakarthasamgraha, src:madhyamakaratnapradipa, src:sugatamatavibhanga, src:ekaslokasastra, src:pancaskandhaprakarana-candrakirti, src:tarkamudgara.
- T1664 is identified as Bhāvanākrama I only probably.
- The Madhyamakāvatāra's structure after chapter 10 and its verse total.
- The MH chapter list.

**Other uncertain content**
- cpt:bhumi-qualities and phn:bhumi-powers: the MA list of twelve hundreds is from memory.
- dsp:sravaka-realization-of-emptiness: location of the Svātantrika side.
- Non-Madhyamaka sides written by U40: BSBh 2.2.31, Ślokavārttika Śūnyavāda, Bodhisattvabhūmi Tattvārtha, Pramāṇasamuccaya on self-awareness.
- Tibetan and Chinese forms in cross_language are mostly from memory.

**Verified locally**
- Tengyur numbers (D-numbers) come from the local catalogue.
- The Chinese Taishō numbers (T1564, 1566–1571, 1573, 1575, 1576, 1578, 1509, 1521, 1631, 1635, 1636, 1654, 1656, 1660, 1662, 1672–1675, 2047, 2048) were confirmed in the extended CBETA catalogue.
- All 159 originals were copied from local e-texts. The BCA and Ratnāvalī originals were machine-checked against DCS and GRETIL. The CŚ 8.15 original keeps the e-text reading "paścāda yo".

## 3. Gaps — belong here but not responsibly created

- **Vaidalyaprakaraṇa:** no verse-anchored teachings (Tibetan only; sūtra numbering unknown).
- **Catuḥstava:** no teachings. The Acintyastava is in DCS and should be extracted in Phase D.
- **Ratnāvalī ch.5 and Suhṛllekha:** very thin, one teaching for SL.
- **Madhyamakāloka:** the GRETIL Sanskrit is local but was not mined.
- **Tattvasaṅgraha:** its 26 examinations are not itemized and there are no verse refs.
- **Āloka and Abhisamayālaṃkāra:** no teachings (AA is U41's).
- **Prajñāpradīpa, Tarkajvālā, Śūnyatāsaptati commentaries:** Tibetan only; need extraction.
- **Lost MMK commentaries:** Devaśarman, Guṇaśrī (no entry created), Guṇamati.
- **Teachers not created:** Candragomin (Candrakīrti's debate partner, likely U41), Mātṛceṭa, Nāgabodhi, Vidyākokila, Avadhūtipa.
- **Patsab Nyima Drak, Ngok Loden Sherab and later Tibetan Madhyamaka** (Chapa, Tsongkhapa, Gorampa, Mipham, rangtong/shentong) are left to U47/U48. Chinese Sanlun (Sengzhao, Jizang) is left to U54.
- **Dangling references to check at merge:** prc:tonglen is referenced but not yet defined anywhere (expected from U47). The Yogācāra and pramāṇa sources cited as dispute sides (src:vimsatika, src:trimsika, src:madhyantavibhaga, src:yogacarabhumi, src:pramanasamuccaya, src:pramanavarttika) are registry ids owned by U41.
- **Dedupe for the orchestrator:**
  - src:tattvasangraha (U12, U31, U40) vs src:tattvasangraha-santaraksita (U09).
  - cpt:bodhicitta (U40) is related to cpt:bodhicitta-sutra (U39).
  - cpt:middle-way category conflict (U36 "ethics" vs U40 "ultimate").

## 4. Out of reach

- The Sanskrit of the Madhyamakāvatāra root verses (recently edited manuscript) is not local. Buddhapālita's Sanskrit is lost except for quotations.
- The oral commentarial and debate traditions of Madhyamaka in Tibetan monasteries.
- Restricted content: the physical giving of the body is recorded as a summary with the texts' warnings only (prc:giving-body-enjoyments-merit, restricted: true).
