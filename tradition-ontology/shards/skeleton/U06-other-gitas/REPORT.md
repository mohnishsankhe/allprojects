# U06-other-gitas — skeleton sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map A3 (the Uddhava and Kapila Gītās, the other Gītās, the Yoga Vāsiṣṭha full and Laghu, and the Adhyātma Rāmāyaṇa), plus every other Gītā known.
U06 owns no lineage, so it writes no lineage entries and no ult: views.
It references existing lineage ids: lin:puranic, lin:advaita-vedanta, lin:sakta, lin:pasupata, lin:ramanandi, lin:epic-teaching, lin:datta-sampradaya, lin:varkari and others.

**Counts:** sources 78 · teachers 54 · teachings 301 · terms 95 · concepts 34 · practices 39 · obstacles 18 · phenomenology 16 · paths 3 · disputes 4 · borrowings 8 · interpretation_log 18.
**Validator:** 0 errors.

**Method note.** Most verse refs were checked against local corpora in sources_raw/:
- the Bhāgavata e-text (raw_etexts mAdhva-app)
- the 1915 Gītāsaṅgraha (Aṣṭāvakra, Avadhūta, Kapila, Devī, Śiva, Gaṇeśa, Rāma, Sūrya, Yama, Haṃsa, Pāṇḍava, Brahma Gītās)
- the Gita Press Adhyātma Rāmāyaṇa
- the GRETIL Mokṣopāya critical text
- the Kūrma, Viṣṇu, Agni and Narasiṃha Purāṇa e-texts
- the Mahābhārata critical edition (DharmicData)
- the Ganeshpuri Guru Gītā
- the Rāmcaritmānas

All entries remain at level `skeleton`; each checked ref says so in its `notes`.
`original` fields were copied from those editions (Devanāgarī converted to IAST by script). Three half-verses were completed from memory, and each is flagged in its note.

## Corrections to the task's list
- **24 teachers:** exactly as listed, verified at BhP 11.7.33-34. The maiden's bangles are conch-shell bangles (śaṅkha; called kaṅkaṇa at 11.9.10).
- **The avadhūta's name:** the Bhāgavata calls him only "an avadhūta brāhmaṇa" (11.7.25). The identification with Dattātreya is the tradition's (cf. BhP 2.7.4).
- **Uddhava Gītā:** Uddhava's plea is 11.6.40-49; the teaching runs 11.7.1-11.29.49; the avadhūta section is 11.7.24-11.9.33.
- **Haṃsa Gītā:** a section, BhP 11.13.15-42, not a whole chapter. A different Haṃsa Gītā is at Mahābhārata 12.288.
- **Bhikṣu Gītā:** BhP 11.23 (story 6-41, song 42-57). There is also an embedded **Aila Gītā** at 11.26.
- **Kapila Gītā:** 9 chapters (3.25-33), about 397 verses. The embryo's prayer is 3.31.12-21. Verses 3.28.37-38 recur as 11.13.36-37.
- **Aṣṭāvakra Gītā:** 20 chapters, 298 verses. Some editions append a 6-verse saṅkhyākrama as a "21st". It is distinct from the Mahābhārata's Aṣṭāvakrīya (3.132-134), which an 1896 collection also prints as an "Aṣṭāvakra Gītā".
- **Avadhūta Gītā:** 8 chapters, about 289 verses. Verses 8.2-4 reproduce BhP 11.11.29-31.
- **Īśvara Gītā:** Kūrma Purāṇa uparivibhāga 2.1-11 (verified). The **Vyāsa Gītā** follows from 2.12.
- **Devī Gītā:** DBhP 7.31-40, with the teaching proper at 7.32-40.
- **Śiva Gītā:** its own colophons place it in the Padma Purāṇa "uparibhāga"; 16 chapters, titles verified.
- **Gaṇeśa Gītā:** 11 chapters, titles verified; Gaṇeśa Purāṇa uttarakhaṇḍa, a dialogue of Gajānana and Vareṇya.
- **Rāma Gītā:** Adhyātma Rāmāyaṇa Uttarakāṇḍa 5, 62 verses. A longer Rāma Gītā in the Tattvasārāyaṇa is recalled with low confidence.
- **Guru Gītā:** exists in several recensions of different lengths.
- **Brahma Gītā:** there are two, one in the Sūta Saṃhitā (12 chapters) and one in the Yoga Vāsiṣṭha.
- **Yama Gītā:** there are three: Viṣṇu Purāṇa 3.7, Narasiṃha Purāṇa 8 and Agni Purāṇa 381.
- **Vibhīṣaṇa Gītā:** it comes from the Rāmcaritmānas (Laṅkākāṇḍa, before dohā 80), not from Vālmīki.
- **Spellings and story names:**
  - "Dāsūra" should read **Dāśūra**.
  - The Mokṣopāya names the Karkaṭī story Sūcy-upākhyāna, the Śukra story Bhārgavopākhyāna and the stone story Pāṣāṇopākhyāna.
  - It names Book 5 Upaśānti.
- **Yoga Vāsiṣṭha:**
  - At 2.17.6 the text calls itself the Mokṣopāya saṃhitā of 32,000 verses.
  - The seven stages (3.118.5-6) and the four gatekeepers (2.11.59) are verified in the Mokṣopāya.
- **Numbering:** Mokṣopāya sarga numbers differ from the vulgate's.
  - Book 1 is offset by about 1 and Book 4 by about 18; the vulgate splits Book 6 into two halves.
  - So verse-level teachings are anchored on src:moksopaya.
  - Four chapter-level anchors on src:yoga-vasistha carry cross-refs to them.

## 1. Checklist
| item | ids |
|---|---|
| Uddhava Gītā | src:uddhava-gita; 88 teachings (tea:uddhava-gita:11.7.6-9 … 11.29.12-19); tch:krsna, tch:uddhava |
| — the 24 teachers (each has its own teaching) | cpt:twenty-four-teachers-of-the-avadhuta; tea:uddhava-gita:11.7.37 … 11.9.22-23, 11.9.25-30, 11.9.31; prc:learning-from-all-beings; tch:dattatreya, tch:yadu, tch:pingala |
| — Bhikṣu Gītā | src:bhiksu-gita; tea:uddhava-gita:11.23.* (7 teachings); cpt:mind-as-cause-of-samsara; obs:fifteen-evils-of-wealth |
| — Haṃsa Gītā | src:hamsa-gita-bhagavata; tea:uddhava-gita:11.13.16-21 … 11.13.38-40; tch:hamsa-avatara, tch:sanaka |
| — Aila Gītā | src:aila-gita; tea:uddhava-gita:11.26.4-24, 11.26.26-34; tch:pururavas |
| — bhakti and jñāna teachings | 11.11-11.29 teachings; cpt:three-yogas-by-disposition-bhagavata; pth:uddhava-gita-three-yogas; cpt:eighteen-siddhis-bhagavata; cpt:twelve-yamas-twelve-niyamas-bhagavata; cpt:redefined-virtues-bhagavata; cpt:tattva-counts-reconciled-bhagavata; dsp:number-of-tattvas |
| Kapila Gītā | src:kapila-gita; 26 teachings; tch:kapila, tch:devahuti; cpt:kapila-gita-principles, cpt:bhakti-by-the-gunas, cpt:five-kinds-of-liberation, cpt:embryo-remembrance-and-prayer, cpt:paths-of-smoke-and-light-kapila, cpt:kapila-gita-death-and-hells; pth:kapila-gita-bhakti-sequence |
| Aṣṭāvakra Gītā | src:astavakra-gita; 15 teachings; tch:astavakra, tch:janaka; prc:saksi-bhava-astavakra, prc:laya-astavakra, prc:sarva-vismarana |
| Avadhūta Gītā | src:avadhuta-gita; 8 teachings; cpt:avadhuta; trm:avadhuta |
| Ṛbhu Gītā | src:rbhu-gita (+src:siva-rahasya); 2 teachings; tea:visnu-purana:2.15-16; tch:rbhu, tch:nidagha |
| Īśvara Gītā | src:isvara-gita; 7 teachings; cpt:pati-pasu-pasa; prc:pasupata-yoga-isvara-gita; phn:siva-dance-vision |
| Devī Gītā | src:devi-gita; 14 teachings; tch:devi, tch:himavat; cpt:ten-yamas-ten-niyamas-devi-gita, cpt:three-paths-devi-gita; prc:devi-gita-kundalini-dhyana (restricted), prc:antaryaga, prc:nyasa, prc:bhuta-suddhi, prc:tirthatana |
| Śiva Gītā | src:siva-gita; 6 chapter-level teachings; prc:viraja-diksa |
| Gaṇeśa Gītā | src:ganesa-gita, src:ganesa-gita-tika-nilakantha, src:ganesa-purana; 5 teachings; tch:ganesa, tch:varenya |
| Rāma Gītā | src:rama-gita; 11 teachings; pth:rama-gita-sequence; prc:pranava-laya-rama-gita, prc:mahavakya-vicara; dsp:jnana-karma-samuccaya |
| Guru Gītā | src:guru-gita; 6 teachings; cpt:guru-principle; prc:guru-seva, prc:guru-dhyana, prc:guru-gita-recitation |
| Uttara, Pāṇḍava, Vyāsa, Sūta Gītās | src:uttara-gita (2 teachings, low), src:pandava-gita (1), src:vyasa-gita (1), src:suta-gita (+src:suta-samhita; no teaching) |
| Brahma Gītā | src:brahma-gita-suta-samhita (2 teachings), src:brahma-gita-yoga-vasistha |
| Yama Gītā | src:yama-gita-visnu-purana, src:yama-gita-narasimha-purana, src:yama-gita-agni-purana (1 teaching each) |
| Piṅgalā Gītā | src:pingala-gita (2 teachings) |
| Vibhīṣaṇa Gītā | src:vibhisana-gita (1 teaching) |
| other Gītās added | **Bhāgavata:** rudra-, gopi-, venu-, yugala-, bhramara-, sruti-, bhu-gita-bhagavata. **Mahābhārata:** manki-, bodhya-, samyaka-, vicakhnu-, harita-, vrtra-, parasara-, hamsa-gita-mahabharata, sadja-, utathya-, vamadeva-, rsabha-, kama-, vyadha-, sarasvati-, kasyapa-, saunaka-gita, ajagara-carita, astavakriya-mahabharata, brahmana-gita. **Others:** bhu-gita-visnu-purana, gita-sara-agni-purana, surya-gita, rama-gita-tattvasarayana, bhagavati-gita, jivanmukta-gita, siddha-gita, vasistha-gita, laksmana-gita, eknathi-bhagavata |
| Yoga Vāsiṣṭha: six books, size, dating (tradition vs scholarly), Mokṣopāya as scholarly metadata | src:yoga-vasistha, src:moksopaya, src:moksopaya-tika-bhaskarakantha, src:yoga-vasistha-tatparyaprakasa; tea:moksopaya:2.17.6-11 |
| — Laghu Yoga Vāsiṣṭha | src:laghu-yoga-vasistha; tch:abhinanda; src:vasistha-candrika (low); src:yoga-vasistha-sara (low) |
| — the seven bhūmikās | cpt:seven-stages-of-knowledge; trm:subheccha … trm:turyaga, trm:turyatita; tea:moksopaya:3.118.1-7, 3.118.8-15, 3.118.16-26, 6.140-156; tea:yoga-vasistha:3.118; references pth:yoga-vasistha-seven-bhumikas (owned by U51) |
| — seven stages of ignorance (added) | cpt:seven-stages-of-ignorance; tea:moksopaya:3.117.11-24 |
| — the four gatekeepers | cpt:four-gatekeepers-of-liberation; trm:moksa-dvarapala, trm:sama, trm:vicara, trm:santosa, trm:satsanga; tea:moksopaya:2.11.56-61, 2.13.48-53, 2.14, 2.15, 2.16; prc:four-gatekeepers-practice |
| — stories (all tea:moksopaya:) | Līlā 3.15-60; Karkaṭī 3.68-83; Aindava/Ahalyā 3.86-90; the child's tale 3.101; Lavaṇa 3.104-109; Śukra 3.127-138; Dāma-Vyāla-Kaṭa 4.7-16; Dāśūra 4.30-37; Kaca 4.40 and 6.115; Janaka 5.9-10 (+tea:siddha-gita:5.8); Puṇya-Pāvana 5.19-20; Bali 5.22-29; Prahlāda 5.30-43; Gādhi 5.44-49; Uddālaka 5.51-56; Suraghu 5.58-63; Bhāsa-Vilāsa 5.65-70; Vītahavya 5.82-88; Bhuśuṇḍa 6.14-27, 6.26; Deva-pūjā 6.31-46; Arjuna 6.56-62; Cūḍālā 6.82-83, 6.84-86, 6.88-96, 6.97-114; the illusory man 6.116-117; Bhṛṅgīśa 6.119.9-20; Maṅki 6.180-183; the stone 6.221-252 |
| — mind; effort vs fate; vāsanās; prāṇa and mind; jīvanmukti | cpt:world-as-projection-of-mind, cpt:paurusa-and-daiva, dsp:daiva-or-paurusa, cpt:two-seeds-of-the-mind, cpt:three-spaces-yoga-vasistha, cpt:jivanmukti, cpt:three-great-vows-of-bhrngisa; trm:paurusa, trm:daiva, trm:vasana, trm:vasana-ksaya, trm:mano-nasa, trm:prana-spanda; prc:vasana-ksaya-practice, prc:prana-cinta-bhusunda, prc:prana-nirodha-yoga-vasistha, prc:vicara-yoga-vasistha, prc:brahmabhyasa, prc:sarva-tyaga |
| Adhyātma Rāmāyaṇa: Brahmāṇḍa placement, structure | src:adhyatma-ramayana (7 kāṇḍas, 65 sargas; Māhātmya colophon "brahmāṇḍapurāṇe uttarakhaṇḍe" verified) |
| — Rāma-hṛdaya | src:rama-hrdaya; tea:adhyatma-ramayana:1.1.32-43, 1.1.44-52; tea:rama-hrdaya:1.1.44-52; cpt:threefold-consciousness-rama-hrdaya |
| — Advaitic reading of the Rāma story | tea:adhyatma-ramayana:1.1.13-24, 3.4.*, 3.10.*; cpt:two-powers-of-maya; cpt:navadha-bhakti-adhyatma-ramayana; brw:adhyatma-ramayana-to-ramcaritmanas |
| Disputes | own: dsp:daiva-or-paurusa, dsp:jnana-karma-samuccaya, dsp:bhakti-jnana-precedence, dsp:number-of-tattvas. Teachings also link to U50's dsp:works-knowledge-grace, dsp:saguna-nirguna, dsp:women-caste-liberation, dsp:sudden-or-gradual |
| One truth, many names | cpt:one-ultimate-many-names; tea:uddhava-gita:11.9.31, 11.22.1-9; tea:moksopaya:3.5.3-7, 3.66.10-14, 6.195.1-4; tea:ganesa-gita:1.21-24 |
| Borrowings | 8 brw: entries (Bodhya→24 teachers; Bhāgavata→Avadhūta 8.2-4; Bhagavad Gītā as model for later Gītās; Yoga Vāsiṣṭha bhūmikās in minor Upaniṣads; Mokṣopāya and Kashmir Śaiva vocabulary; Yoga Vāsiṣṭha and Buddhist idealism; Adhyātma Rāmāyaṇa→Rāmcaritmānas; Uddhava Gītā→Vārkarī) |

## 2. Least sure (check first)
- **Ṛbhu Gītā:** location in Śivarahasya aṃśa 6, the chapter and verse counts, and both "passim" teachings.
- **Uttara Gītā:** the structure, both teachings, and the commentary ascribed to Gauḍapāda.
- **Texts known only by recall:** src:jivanmukta-gita, src:bhagavati-gita, src:rama-gita-tattvasarayana, src:vasistha-candrika (with tch:atmasukha), src:yoga-vasistha-sara, and the 8-chapter count of src:suta-gita.
- **Śiva Gītā:** chapter titles are verified, but chapter content, including the Virajā rite, is from memory.
- **Mokṣopāya stories:** locations are verified by colophons, but the narrative details are from memory. This covers Śukra, Dāma-Vyāla-Kaṭa, Dāśūra, Gādhi, Uddālaka, Suraghu, Vītahavya, Cūḍālā's powers and parables, Mithyāpuruṣa, Maṅki, 6.140-156 and 6.26.
- **Vulgate Yoga Vāsiṣṭha refs** given in notes (e.g. Cūḍālā at about 6.1.77-110) are approximate.
- **Scholarly dates** for the Īśvara, Devī and Guru Gītās, the Laghu Yoga Vāsiṣṭha and the Adhyātma Rāmāyaṇa are estimates.
- **Mahābhārata Gītā names:** "Ṣaḍja Gītā" and "Hārīta Gītā" come from the vulgate; the passages themselves are verified.
- **Epic side of dsp:daiva-or-paurusa:** the Anuśāsana 13.6 reference is recalled with low confidence.
- **Twelve niyamas:** how commentators reach twelve for the Bhāgavata list is recalled.
- **Borrowing claim:** that the Varāha, Akṣi and Mahā Upaniṣads contain the bhūmikās (U04 should verify).

## 3. Gaps
- **Laghu Yoga Vāsiṣṭha:** no teachings, because the text is not local.
- **Pañcadaśagītā items not located:** the Nahuṣa, Yudhiṣṭhira, Baka and Śrī-Kṛṣṇa Gītās could not be placed in the Mahābhārata.
- **Too vague to create:** the Agastya Gītā, and a Devī Gītā in Kūrma Purāṇa 1.12.
- **Seen in the corpus but not created:** a Jain "Adhyātma Gītā", the modern "Gāndhī Gītā"s and the "Arūpa Gītā".
- **No owning unit:** no unit owns lin:ganapatya (referenced by the slug rule) or a Saura lineage; please assign.
- **Vulgate numbering:** the vulgate Yoga Vāsiṣṭha is not local, so its Book 1, 4 and 6 numbering still needs mapping to the Mokṣopāya.
- **Left to U07/U16:** Śrīdhara's Bhāvārthadīpikā.
- **Depends on U03:** the cross-ref tea:mundaka-upanisad:2.2.4.

## 4. Out of reach
- **Not in the local corpora:** critical texts of the Ṛbhu Gītā, Uttara Gītā, Sūta Saṃhitā and Laghu Yoga Vāsiṣṭha; the web sites that carry them are blocked.
- **Oral lore:** Datta and Nāth traditions about the Avadhūta Gītā (e.g. the disciples Svāmī and Kārttika), and the Guru Gītā chanting tradition.
- **Restricted:** the Devī Gītā's kuṇḍalinī yoga and Cūḍālā's powers are recorded as summaries only; prc:devi-gita-kundalini-dhyana is marked restricted.
