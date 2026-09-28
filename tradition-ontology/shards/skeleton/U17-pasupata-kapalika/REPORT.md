# U17-pasupata-kapalika — skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: A7 (Pāśupata; Lākula, Kāpālika, Kālāmukha) and I2 (the Atimārga as a division). Owned lineages: lin:atimarga, lin:pasupata, lin:lakula, lin:kapalika, lin:kalamukha.
Counts: sources 28, teachers 28, teachings 130, terms 131, concepts 43, practices 40, obstacles 12, paths 1, phenomenology 11, disputes 8, borrowings 7, lineages 5, ultimate 5, interpretation_log 13. Validator: 0 errors.
Generators: `_gen/part1…part9*.py` (run from `tradition-ontology/`).

The Pāśupata core was checked against local e-texts in `sources_raw`. Those files are:
- GRETIL Pāśupata Sūtra (Sagar 1987) and the Sūtra with Kauṇḍinya's Pañcārthabhāṣya (Sastri 1940).
- Muktabodha M00508: the Gaṇakārikā with Ratnaṭīkā, plus its appendices (SDS ch. 6, Guṇaratna, Rājaśekhara, Kāravaṇa-māhātmya).
- Āgamaprāmāṇya (M00001), Śaṅkara on BS 2.2.37, Bhāmatī, Svacchanda Tantra, Kiraṇavṛtti.
- Liṅga, Kūrma, Śiva and Skanda Purāṇas; MBh 12.337 (critical edition); Atharvaśiras.
- Mattavilāsa, Mālatīmādhava, Sattasaī, and the Harṣacarita (DCS).

All entries stay at level `skeleton`. Notes say where a passage was checked.

## 1. Coverage checklist
- **Atimārga as a division (I2).** lin:atimarga, cpt:atimarga-mantramarga-division, cpt:five-streams-nisvasa, cpt:atimarga-divisions, cpt:atimarga-goal-levels. Teachings: svacchanda-tantra:11.182-185, 11.189-190, 11.71-72, 10.1169-1171; nisvasamukha:4 and 4/2; kurma-purana:2.37.140-146; siva-purana:7.2.31.173.
- **Mantramārga.** Referenced as lin:mantramarga (owned by U08).
- **Lakulīśa: the tradition's accounts.**
  - Entries: tch:lakulisa, cpt:lakulisa-incarnation, cpt:twenty-eight-yogacaryas.
  - Liṅga P. 1.24.126-134 (entering a corpse; Kāyāvatāra; four disciples).
  - Kūrma P. 1.51.9-10 and 1.51.26.
  - Kauṇḍinya on PS 1.1: pancarthabhasya:1.1/2.
  - Kāravaṇa-māhātmya 1, 3, 4.
  - Liṅga 1.76.38-39 (his image).
- **Lakulīśa: scholarly dating.** c. 2nd c. CE, labelled; based on src:mathura-pillar-inscription and tch:uditacarya.
- **The four disciples.** tch:kusika, tch:garga-pasupata, tch:mitra-pasupata, tch:kaurusya.
- **The eighteen tīrthakaras.** 12 further tch entries and cpt:pasupata-tirthakaras.
- **Pāśupata Sūtra.** src:pasupata-sutra plus 41 teachings covering the whole text.
- **Kauṇḍinya and the five categories.**
  - Sources and teacher: src:pancarthabhasya (21 teachings), tch:kaundinya.
  - Categories: cpt:pancartha-five-categories, cpt:pasupata-karya, cpt:pasupata-karana, cpt:pasupata-yoga, cpt:pasupata-vidhi, cpt:duhkhanta.
  - Soul, bonds and knowledge: cpt:pasu-bound-soul-pasupata, cpt:pasupata-kalas, cpt:pasupata-vidya, cpt:pasupata-three-pramanas.
- **Gaṇakārikā and Ratnaṭīkā.**
  - Sources: src:ganakarika (8 verse teachings), src:ratnatika (5), tch:bhasarvajna, tch:haradatta-pasupata, cpt:eight-pentads-ganakarika.
  - The pentads, one concept each: stages, places, impurities, gains, means, purifications, strengths, initiation factors.
  - The triad of livelihoods: cpt:pasupata-three-livelihoods.
- **Five stages.** pth:pasupata-five-stages (bands B2, B2, B3, B6, B7, logged), cpt:pasupata-five-stages, trm:vyaktavastha … trm:nisthavastha.
- **Practices.**
  - Ash: prc:bhasmasnana, prc:bhasmasayana, prc:anusnana.
  - The six-limbed offering: prc:pasupata-upahara, prc:hasita, prc:gita-upahara, prc:nrtta-upahara, prc:dundunkara, prc:namaskara-upahara.
  - Mantra: prc:pancabrahma-japa, prc:raudri-gayatri-japa.
  - Other first-stage acts: prc:pradaksina, prc:atmapradana, prc:nirmalya-dharana, prc:ayatana-vasa, prc:ekavasa-avasa, prc:pasupata-diksa.
  - Later stages: prc:omkara-dhyana-hrd, prc:rudra-anusmarana, prc:sunyagara-guha-vasa, prc:smasana-vasa, prc:pasupata-vrtti.
- **Courting dishonour.**
  - The six "doors": prc:krathana, prc:spandana, prc:mantana, prc:srngarana, prc:avitatkarana, prc:avitadbhasana.
  - Related practices: prc:courting-dishonour, prc:pretacarana, prc:unmatta-carana, prc:gudha-vrata, prc:indriya-dvara-pidhana.
  - Concepts: cpt:six-doors-dvara, cpt:courting-dishonour.
  - Kauṇḍinya's own safeguards are stored as warnings.
- **Goal and powers.**
  - The goal: cpt:duhkhanta, trm:sayujya, trm:rudrasamipa.
  - The powers: cpt:pasupata-powers and phn:pasupata-* (8 items).
- **Īśvara's independence from karma.** cpt:isvara-independence-from-karma, pancarthabhasya:2.6, sarvadarsanasangraha:6/4, and dsp:pasupata-isvara-karma (queued).
- **Brahma Sūtra 2.2.37ff critique.** dsp:lord-only-efficient-cause (queued), with teachings brahma-sutra:2.2.37, brahma-sutra:2.1.34, brahma-sutra-bhasya-sankara:2.2.37, bhamati:2.2.37, sribhasya:2.2.35.
- **Lākula and the mahāvrata.** lin:lakula, ult:lakula, cpt:mahavrata-skull-observance, prc:mahavrata-kapala (restricted), trm:lokatita, trm:kapalavrata. All low confidence.
- **Kāpālika.**
  - Lineage and myth: lin:kapalika, cpt:bhairava-brahmahatya-myth (Kūrma 2.31.104-106), trm:kapala, trm:khatvanga, trm:somasiddhanta.
  - The six insignia: cpt:kapalika-six-insignia.
  - Opponents' reports, all tagged reported_by_opponent:
    - Yāmuna and Rāmānuja.
    - Mattavilāsa 6-7; Mālatīmādhava 1, 5, 5.1-2; Prabodhacandrodaya 3 and 3/2.
    - Yaśastilaka (source entry only); Sattasaī 408 (not tagged as an opponent: it is a poem, not a polemic).
    - Śaṅkaradigvijaya 11 and 15; Xuanzang juan 2.
    - Guṇaratna and Rājaśekhara.
  - Dispute: dsp:kapalika-path-validity.
  - Borrowing: brw:kapalika-to-vajrayana (disputed).
- **Kālāmukha.**
  - Lineage and institutions: lin:kalamukha, cpt:kalamukha-institutions, src:balligave-kalamukha-inscriptions.
  - Pontiffs: tch:kedarasakti, tch:vamasakti, tch:kriyasakti.
  - Śakti- and Siṃha-pariṣad; Kedāreśvara at Balligāve; Śrīśaila.
  - Opponents' reports: agamapramanya mahesvara-tantra/2, and prc:kalamukha-skull-ash-practices and prc:surakumbha-worship (the former restricted).
  - Relation to Vīraśaivism: brw:kalamukha-to-virasaiva (direction "disputed"). It records the scholarly continuity hypothesis, the Vīraśaivas' own origin accounts, and a caution.
- **Other disputes.**
  - dsp:pasupata-vedic-status (queued).
  - dsp:atimarga-liberation-rank (partially reconciled under P4-stage; the Pāśupata objection is recorded).
  - dsp:atimarga-initiation-eligibility (queued).
  - dsp:liberated-soul-qualities (queued).
  - dsp:duhkhanta-cessation-or-lordship (queued).
- **Other borrowings.** brw:pasupata-to-mantramarga, brw:pasupata-nyaya, brw:atharvasiras-pasupata-sutra, brw:vedic-pancabrahma-to-pasupata, brw:dharmasastra-penance-to-kapalika.

### Corrections to the must-cover list
1. **The "ḍuṃḍuṃ" sound.** Kauṇḍinya reads *ḍuṇḍuṅkāra*: a holy sound like a bull's bellow, made by touching the tongue-tip to the palate. The Sagar text has *dunduṃkāra*, and the SDS and Ratnaṭīkā have *huḍukkāra*.
2. **"Eight pentads".** The Gaṇakārikā has eight pentads plus one triad (the livelihoods), which make its "nine groups" (gaṇa).
   - The SDS quotes the verses as Haradattācārya's. Dalal ascribes them to Bhāsarvajña, who wrote the Ratnaṭīkā.
   - Kauṇḍinya's own lists of the pentads (PABh on 5.29) differ from the Gaṇakārikā's.
3. **The feigned behaviours.** Confirmed as krāthana (feigned sleep with snoring), spandana, maṇṭana (SDS: *mandana*), śṛṅgāraṇa, avitatkaraṇa and avitadbhāṣaṇa (Ratnaṭīkā: *apitat-*).
   - The last two names come from the SDS; the sūtra says only "api tat kuryāt / api tad bhāṣet".
   - Kauṇḍinya sets conditions: knowledge already gained, the teacher's leave, and no breach of the yamas. The amorous gestures are only feigned.
4. **Kauṇḍinya's account of the founder.** He never names Lakulīśa. He says the Lord took a brahmin's body, descended at Kāyāvataraṇa, and taught Kuśika at Ujjayinī. The place name also appears as Kāyāvatāra, Kāyārohaṇa and Kāyāvarohaṇa.
5. **The four disciples.** Liṅga P. 1.24.131 reads Kuśika, Garga, Mitra, Kauruṣya. Kūrma 1.51.26 reads "Mitraka" and "Ṛṣya"; the Jain lists read Gārgya, Maitrya, Kauruṣa.
6. **The five stages.** They are vyakta, avyakta, jaya, cheda and niṣṭhā (Gaṇakārikā 5). The Ratnaṭīkā rejects a "stage of the perfected" as the fifth.
7. **Sūtra numbering.** The Pāśupata Sūtra has 5 adhyāyas and 168 sūtras in the Sagar numbering (167 in Sastri's). Numbering in adhyāya 5 differs between the two after 5.28; the notes say which is used.
8. **What Brahma Sūtra 2.2.37ff attacks.** Its main target is the Māheśvara view that the Lord is only the efficient cause; Śaṅkara quotes the five categories. The karma question comes up inside his argument, and BS 2.1.34 gives the Vedāntin position on it. In Rāmānuja's numbering the sūtra is 2.2.35.
9. **Rāmānuja's source.** His report on the Kāpālikas and Kālāmukhas follows Yāmuna's Āgamaprāmāṇya, which I verified. Vācaspati's four Māheśvaras are Śaivas, Pāśupatas, Kāruṇika-siddhāntins and Kāpālikas; he does not name the Kālāmukhas.
10. **Additions not in the list.**
    - Kūrma 2.37.146 names "Soma" (Somasiddhānta) with Pāśupata and Lākula as non-Vedic.
    - Svacchanda 11.71-72 names further groups (Mausula, Kāruka, Vaimala, Pramāṇa).
    - Rāmakaṇṭha rejects three accounts of liberation: saṅkrānti (transfer), āveśa (possession) and samutpatti (production).

## 2. Least sure (check first)
- Niśvāsamukha: chapter 4 location and the atyāśrama/lokātīta wording (not in the local corpus).
- Kālāmukha pontiffs Kedāraśakti, Vāmaśakti and Kriyāśakti (Kriyāśakti's affiliation especially); the pariṣad structure; Śrīśaila's role.
- The Cintra praśasti (1287), the Ekaliṅgajī inscription (971) and the Prabhāsa inscription (1169, Bhāva Bṛhaspati): dates and contents.
- The Mathurā inscription's wording, including the teachers Kapila and Upamita.
- Prabodhacandrodaya act 3 (verse numbers; the power boasts, especially 3/2); the Yaśastilaka's Kāpālika and Kaula passages.
- Xuanzang juan 2; Śaṅkaradigvijaya cantos 11 and 15; the details of the Harṣacarita ch. 3 rite.
- Uddyotakara as "Pāśupatācārya"; Bhāsarvajña's date.
- The Guṇaratna attribution: the appendix heading says Haribhadra.
- Scholarly dates for Lakulīśa, Kauṇḍinya and the Sattasaī.
- The Nyāya Sūtra 4.1.19-21 side in dsp:pasupata-isvara-karma.
- The Swami Kripalvananda revival note (recent).

## 3. Gaps (not created)
- **Lost or unknown texts.** Lākula scriptures and doctrine; any Kāpālika or Somasiddhānta scripture; the Rāśīkara-bhāṣya, Ādarśa and Pañcārthabhāṣyadīpikā (entered as lost or unknown).
- **Unchecked Purāṇic material.** The Vāyu Purāṇa's Pāśupata-yoga chapters and its ch. 23 list; other Purāṇic Bhairava/Kapālamocana versions (Śiva P., Matsya, Skanda Kāśīkhaṇḍa).
- **Unchecked verse numbers.** Dharmaśāstra brahmahatyā penance verses (Manu, Yājñavalkya); the Hevajra six-mudrā verse.
- **Unentered detail.** Individual Kālāmukha inscriptions (Epigraphia Carnatica numbers) and sites beyond Balligāve; Pāśupata evidence from Nepal and Cambodia; Kauṇḍinya's expiation (prāyaścitta) rules.
- **Cross-unit.** Kāpālika references in Tamil sources (Maṇimēkalai, Tēvāram); Kāpālika–Aghora continuity (U21).
- **Ids referenced but owned elsewhere (confirm at merge):** cpt:kaivalya, cpt:yama-niyama, obs:anava-mala, trm:isvara, trm:jiva, trm:moksa, trm:apavarga, trm:lila, trm:jnanasakti, src:nisvasatattvasamhita, src:nyayasara, src:saddarsanasamuccaya-haribhadra.

## 4. Out of reach
- Oral and initiatory instruction of these extinct orders.
- Undigitized inscriptions.
- Texts not in this run's corpus: the Niśvāsamukha (Kafle 2020), Prabodhacandrodaya, Yaśastilaka, Śrībhāṣya, Vāyu Purāṇa.
- Restricted content kept to summary only: the bhagāsana meditation, corpse-ash practices, and the skull vow.
