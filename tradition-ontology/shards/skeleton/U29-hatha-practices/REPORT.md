# U29-hatha-practices — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Scope:** coverage-map section E. The practice catalogue of the haṭha texts and Yoga Upaniṣads: postures, breath, locks and seals, cleansing, sense-withdrawal and concentration, inner sound, and the main ritual hand-gestures.

This unit owns no lineage, so it writes no ult view. The practices reference the lineages of the texts that teach them:
- lin:hatha-yoga (U28)
- lin:natha (U21)
- lin:upanisadic (U04)
- lin:patanjala-yoga (U10)
- lin:mantrasastra and lin:kerala-tantra (the Śāradātilaka), plus lin:mantramarga and lin:pancaratra.

**Method.** Entries are skeleton knowledge, but verse numbers and wording were checked against local e-texts (read only, as data):
- Haṭhapradīpikā: vulgate segments in sources_raw/prepared, plus the Jyotsnā (Muktabodha M00243).
- Gheraṇḍasaṃhitā: eBhāratī Tirupati e-text. Upadeśa 4 comes from the Vasu e-text, because the Tirupati e-text lacks it.
- Śivasaṃhitā: Muktabodha M00082.
- Dattātreyayogaśāstra: the vulgate of 154 verses.
- Gorakṣaśataka: GRETIL (Kuvalayananda–Shukla edition) and the Briggs recension (Muktabodha M00522).
- Nādānusandhāna: Muktabodha M00526 and eBhāratī.
- Śāradātilaka with Rāghavabhaṭṭa's commentary: Muktabodha M00077.

Every teaching's notes name the edition its numbering follows.

**Restricted material.** No breath counts, ratios, retention times or measurements are given for any practice, restricted or not. Doctrinal numbers are kept: 84 lakh postures, 21,600 breaths a day, and the Gheraṇḍa's breath-lengths.

The following have `restricted: true` and carry only a summary plus the texts' own warnings:
- khecarī
- vajrolī / amarolī / sahajolī
- śakticālana
- sarasvatīcālana
- sūryabhedana, because the texts set an extreme limit for its retention
- mūrcchā
- sahita and kevala kumbhaka (kept consistent with U04)
- the Kumbhakapaddhati retentions
- bahiṣkṛta-dhauti
- tongue-lengthening (jihvā-śodhana)

## 1. Checklist of the coverage items in scope

### Postures (46 prc; ids are prc:<name>asana)

**Haṭhapradīpikā — all 15:**
svastikasana, gomukhasana, virasana, kurmasana, kukkutasana, uttanakurmasana, dhanurasana, matsyendrasana, pascimatanasana, mayurasana, savasana, siddhasana, padmasana, simhasana, bhadrasana.

**Gheraṇḍasaṃhitā — all 32** (GS 2.3-6; each posture has a teaching at GS 2.7-45). The 17 not already in the HYP list above:
muktasana, vajrasana, guptasana, matsyasana, goraksasana, utkatasana, sankatasana, uttanamandukasana, vrksasana, mandukasana, garudasana, vrsasana, salabhasana, makarasana, ustrasana, bhujangasana, yogasana.
- Mṛtāsana is recorded as a name of savasana.
- Paścimottāna is recorded as a name of pascimatanasana.

**Śivasaṃhitā — 4 (ŚS 3.84-97):**
- siddha → prc:siddhasana
- padma → prc:padmasana
- ugra → prc:pascimatanasana (ŚS 3.92 itself identifies ugrāsana with paścimottāna)
- svastika → prc:svastikasana (ŚS 3.97 calls it sukhāsana)
- The mention of 84 postures is in tea:siva-samhita:3.84 and U28's cpt:eighty-four-asanas.

**Seated meditation postures:**
siddhasana, padmasana, baddhapadmasana, svastikasana, bhadrasana, virasana, sukhasana, vajrasana, muktasana, guptasana, yogasana.

**Postures listed in the Yoga-bhāṣya on YS 2.46:**
dandasana, sopasrayasana, paryankasana, krauncanisadanasana, hastinisadanasana, ustranisadanasana, samasamsthanasana, sthirasukhasana, yathasukhasana, plus padma, vīra, bhadra and svastika.

**Later lists (group entries, low confidence):**
- prc:hathabhyasapaddhati-asanas (about 112 postures, with the Śrītattvanidhi)
- prc:hatharatnavali-asanas (84)
- prc:jogapradipika-asanas (84)

**Yoga Upaniṣad lists:** the posture entries point to U04's teachings (Triśikhi 34-52, Darśana 3.1-13, Dhyānabindu 41-43, Yogatattva 28-29, Amṛtanāda 18-19).

### Breath
- **Haṭhapradīpikā's eight retentions:** surya-bhedana*, ujjayi, sitkari, sitali, bhastrika, bhramari, murccha*, plavini. The list itself is U28's cpt:eight-kumbhakas.
- **Other retentions and preparation:** nadi-sodhana, sahita-kumbhaka*, kevala-kumbhaka*, pranayama (the haṭha contribution).
- **Gheraṇḍa's eight retentions:** sahita, sūryabheda, ujjāyī, śītalī, bhastrikā, bhrāmarī, mūrcchā, kevalī (GS 5.47). These are covered by the same practice entries, plus teachings at GS 5.47-99.
- **Crow-beak and serpent breathings, drinking the breath:** kaki-mudra, bhujangini-mudra, vayu-pana.
- **Svara yoga (Śiva Svarodaya):** svara-sadhana, svara-tattva-pariksa.
- **Ajapā (the haṃsa / so'ham breath-mantra):** prc:ajapa-japa. The haṭha contribution adds GS 5.86-94 and Gorakṣaśataka (Briggs) 42-46, both of which give the 21,600 daily breaths.
- **Kumbhakapaddhati:** kumbhakapaddhati-retentions* (group entry).
- **Owned by other units, not duplicated:** ānāpānasati and the sixteen steps (U36); Tibetan vase breathing and the nine-round purification (U45/U46).

### Locks and seals
- **Three locks and the great lock:** mula-bandha, uddiyana-bandha, jalandhara-bandha, bandha-traya, mahabandha.
- **Haṭhapradīpikā's ten mudrās:** mahamudra, mahabandha, mahavedha, khecari-mudra*, uddiyana-bandha, mula-bandha, jalandhara-bandha, viparita-karani, vajroli-amaroli*, sakticalana*. The list is U28's cpt:ten-mudras-hyp.
- **Gheraṇḍa's 25 (GS 3.1-3):** the ones above, plus nabhomudra, yoni-mudra, vajroli-gheranda, tadagi-mudra, manduki-mudra, sambhavi-mudra, the five dhāraṇās (parthivi-, ambhasi-, agneyi-, vayavi-, akasi-dharana), asvini-mudra, pasini-mudra, kaki-mudra, matangini-mudra, bhujangini-mudra.
- **Śāmbhavī and ṣaṇmukhī:** sambhavi-mudra, sanmukhi-mudra.
- **Also:** sarasvati-calana*.
- **Ritual hand-gestures:** ritual-mudras (a contribution to U08's entry), avahanadi-mudras (āvāhanī and the rest), dhenu-mudra, mahamudra-hasta, ankusa-mudra, sankha-mudra, garuda-mudra, jnana-mudra, yoni-hasta-mudra, anjali-mudra, abhaya-varada-mudras.

### Cleansing
- **The six acts:** dhauti, vastra-dhauti, basti, neti, trataka, nauli (laulikī), kapalabhati.
- **Gheraṇḍa variants:**
  - vatasara-dhauti, varisara-dhauti, agnisara-dhauti, bahiskrta-dhauti*
  - dantamula-dhauti, jihva-sodhana*, karna-dhauti, kapalarandhra-dhauti
  - danda-dhauti, vamana-dhauti, mulasodhana
  - suska-basti
  - vamakrama-, vyutkrama-, sitkrama-kapalabhati
- **Others:** gajakarani, cakri-karma (the Haṭharatnāvalī's eight acts), matangini-mudra, satkarmasangraha-cleansings (group entry).

### Sense-withdrawal and concentration
- pratyahara (the haṭha forms), five-pratyaharas, and marmasthana-dharana (the Vasiṣṭha Saṃhitā / Yoga Yājñavalkya marma method, resting on U28's topic teachings).
- element-dharanas plus the five individual dhāraṇās.
- trataka.
- bhrumadhya-drsti, nasagra-drsti.
- laya-sanketa (same id as U28's).
- pratikopasana (same id as U28's).
- laksya-traya (a contribution to U04's entry).

### Inner sound
- **nadanusandhana:** HYP 4.65-102, GS 5.79-83 and 7.10-11, ŚS 5.22-30, the Nādānusandhāna tract.
- **HYP's four stages:** teachings tea:hatha-yoga-pradipika:4.69 to 4.76-77; path U28's pth:hyp-nada-four-stages.
- **Haṃsa Upaniṣad's ten sounds:** U04's tea:hamsa-upanisad:4-ten-sounds (referenced).
- **Nādabindu sounds:** U04's tea:nadabindu-upanisad:33-35 (referenced).
- **New source:** src:nadanusandhana, which gives a different list of ten sounds.

### Supports of practice
yoga-matha, mitahara (same id as U28/U04), gatramardana.

### Obstacles, signs, maps, debates
- **New obstacles:** obs:apathya-ahara, obs:kayaklesa, obs:sun-swallows-nectar, obs:practice-without-guru.
- **Existing obstacles reused:** obs:improper-pranayama, obs:six-destroyers-of-yoga, obs:malas-in-nadis, obs:kapha-medas-excess, obs:dys-obstacles, obs:siva-samhita-three-obstacles, obs:dambha, obs:bindu-pata, obs:siddhis-as-obstacles, obs:yoga-faults-wrong-place.
- **Phenomenology:** 15 new items, e.g. phn:gheranda-bhramari-sounds-light, phn:ss-sanmukhi-light, phn:nadanusandhana-ten-sounds, phn:hyp-mahavedha-death-like. U28's items (nāḍī-śuddhi signs, the three grades, the four nāda stages and others) are referenced, not repeated.
- **Path map:** pth:siva-samhita-four-avasthas, banded B2/B3/B4/B7.
- **Dispute:** dsp:jalandhara-in-mahabandha (HYP 3.22), status queued with candidate readings.
- **Borrowing:** brw:hatha-mudra-to-mantrasastra.
- **Concepts:** cpt:four-preliminaries-of-pranayama, cpt:eighteen-marmas.

### Corrections to the unit brief's list
- The Śivasaṃhitā's four postures are siddha, padma, ugra (= paścimottāna) and svastika (= sukhāsana).
- The Gheraṇḍa's eight retentions include sahita and kevalī. They do not include sītkārī or plāvinī.
- The Gheraṇḍa's 25 mudrās count the five dhāraṇās as five.
- The Gheraṇḍa's vajrolī (GS 3.45-48) is an arm-supported lift of legs and head, not the Haṭhapradīpikā practice. It is a separate, unrestricted entry (prc:vajroli-gheranda).
- "Ṣaṇmukhī (yoni) mudrā" is only a partial equation. The Gheraṇḍa's yoni mudrā contains the closing of the six openings, but the Śivasaṃhitā's yoni mudrā (4.1-11) is a perineal contraction. HYP 4.68 does not name ṣaṇmukhī; the name comes from the Jyotsnā (recalled, not checked).
- On the HYP's nāda: the stages are 4.69-77 and the sound lists 4.84-86.
- The texts' trāṭaka is gazing at "a small target". The candle flame is later usage.
- The Muktabodha Śivasaṃhitā lists vajrolī in 4.15 but has no vajrolī section. Other editions have one.

## 2. Least-sure items (check these first)

**Low-confidence group entries and methods:**
- prc:cakri-karma: the method is recalled.
- prc:sarasvati-calana: kept deliberately minimal.
- The three posture group entries (Haṭhābhyāsapaddhati, Haṭharatnāvalī, Jogapradīpikā).
- prc:kumbhakapaddhati-retentions, prc:satkarmasangraha-cleansings.

**Ritual hand-gestures (Śāradātilaka):**
- ŚT 23.106-114 is verified in the local e-text.
- The chapter locations for the aṅkuśa, śaṅkha, garuḍa and jñāna mudrās are moderate: they are in Rāghavabhaṭṭa's commentary.
- prc:yoni-hasta-mudra is low. The lineage assignments for all these gestures are interpretive.

**Other low or recalled items:**
- The Nādānusandhāna's correlations of sounds with elements (tea:nadanusandhana:7-13): low, the e-text is corrupt.
- The Śiva Svarodaya entries rest on U28's topic-level teachings; no verse numbers.
- Yoga Yājñavalkya ch. 3 as describing 8 postures: recalled, low, in notes only.
- Brahmānanda naming 4.68 ṣaṇmukhī: recalled.
- ŚS 5.2-8, the "obstacles in the form of knowledge": the e-text is obscure.
- GS 1.46 (a tube in basti): the e-text is corrupt.

**Interpretive links that are mine:**
- kevala-kumbhaka is "analogous" to YS 2.51's fourth prāṇāyāma.
- śāmbhavī is "exact" with vaiṣṇavī.
- The "contested" name-equivalences for siddhāsana (vajrāsana, muktāsana, guptāsana), bhadrāsana (gorakṣāsana) and svastika (sukhāsana).

**Cross-unit issues noticed:**
- U10's paraphrase of Yoga-bhāṣya 2.46 omits vīrāsana, which I believe is in the list.
- U28's phn:dys-ghata-signs (DYŚ 69-76) belong to the ārambha stage by DYŚ 81.
- U04's prc:shanmukhi-mudra breaks the slug rule; it should merge into prc:sanmukhi-mudra (logged as a dedupe).
- U04's prc:mahabandha-mahavedha is split here into prc:mahabandha and prc:mahavedha (logged).
- U24's cpt:satkarma is the tantric six magical acts. The haṭha six acts are U28's cpt:satkarma-doctrine; the two must not be merged.

**Text-layer overlap with U28:**
- 107 teaching ids are the same as U28's; the merge will combine the paraphrases.
- About 53 of my teachings overlap U28's ranges with different spans, for example HYP 2.4-6 / 2.7-10 against U28's 2.4-5 / 2.6-10, HYP 3.32-3.54 in fine segments against U28's 3.32-54, and HYP 4.100 / 4.101-102 against 4.100-102.
- GS 4 is numbered after the Vasu edition, while U28 uses Thomi.
- These need dedupe at merge or in Phase D.

## 3. Gaps (belong here, but not responsibly created)
- The names of the Haṭhābhyāsapaddhati's postures (about 112) and the Śrītattvanidhi's (about 122).
- The names of the Haṭharatnāvalī's 84 postures and the Jogapradīpikā's 84 postures and 24 mudrās.
- The practice lists of the Yuktabhavadeva, Haṭhasaṅketacandrikā and Yogacintāmaṇi, and of the Haṭhatattvakaumudī (its e-text is local, so it is a good Phase D target).
- The individual retentions of the Kumbhakapaddhati (names only would be allowed) and the cleansing variants of the Ṣaṭkarmasaṅgraha.
- The list and distances of the eighteen marmas.
- Verse references for the Yoga Yājñavalkya and the Vasiṣṭha Saṃhitā's postures, prāṇāyāma and pratyāhāra; the Vasiṣṭha Saṃhitā's posture list.
- Śiva Svarodaya verse numbers and its methods of changing the nostril flow.
- The Amṛtasiddhi's own descriptions of mahāmudrā, mahābandha and mahāvedha (only U28's topic-level teaching exists).
- The "original" Gorakṣaśataka (Mallinson): its retentions and sarasvatīcālana. It is not available locally.
- The postures of the Ahirbudhnya Saṃhitā, the Vaikhānasa texts and the Tirumantiram.
- Āgamic lists of hand-gestures (Somaśambhupaddhati, Jayākhya ch. 8).
- Brahmānanda's Jyotsnā glosses on most practices. The e-text is local; only two glosses were checked.
- Practices owned by other units:
  - the Vijñāna Bhairava dhāraṇās (U19)
  - mantra and japa (U31)
  - the ten Śrīvidyā mudrās (U23)
  - Buddhist hand-mudrās (U44)
  - dance hastas (U31)
  - nyāsa and bhūtaśuddhi (U08/U23)
- Recent teachers' forms, which belong to U52 if they are wanted: Satyananda's yoga-nidrā, candle trāṭaka, śaṅkhaprakṣālana, kuñjala and jala-neti; the postures of Krishnamacharya, Iyengar and Sivananda.

## 4. Out of reach
- **Oral or guru-only instruction:** the khecarī mantra (melaka) and the practical preparation for khecarī; the actual methods of vajrolī, śakticālana and sarasvatīcālana. The texts themselves say these are to be learned from the guru's mouth. They are restricted in any case.
- **Critical editions under copyright:** the Haṭhābhyāsapaddhati (Birch and colleagues), the Haṭharatnāvalī and Jogapradīpikā (Lonavla), and Mallinson's Dattātreyayogaśāstra and Gorakṣaśataka.
- **Images:** the Śrītattvanidhi's illustrations.
