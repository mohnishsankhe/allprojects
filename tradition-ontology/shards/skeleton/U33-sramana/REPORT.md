# U33-sramana — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Method.** All entries are skeleton level and come from model knowledge. Where a local e-text existed in `sources_raw/`, it was read to check refs and wording; `original` is given only for wording checked there, or for a few famous verses whose edition note says "from memory".
- **Texts checked locally:**
  - SuttaCentral bilara (Mahāsaṅgīti Pali with Sujato's English): DN 1, 2, 8, 16, 23; MN 12, 26, 36, 57, 60, 71, 76, 77, 101; SN 2.30, 3.1, 12.35, 22.60, 24.5–8, 44.9, 46.56; AN 1.319, 3.61, 3.137, 6.38, 6.57; Snp 3.6; Dhp 70/142/184/265/388; Thig 13.3; Ja 543 and 545; Mil 2; Vinaya kd1 and kd15.
  - GRETIL: Suyagaḍa Book 1, Uttarajjhaya, Isibhāsiyāiṃ, Tattvopaplavasiṃha (incomplete manuscript), Maṇimēkalai, Mahābhāṣya.
  - SARIT: Tattvasaṅgraha with Pañjikā, Nyāyamañjarī.
  - eBhāratī: Śaṅkara's Brahmasūtrabhāṣya, Arthaśāstra.
  - Others: the Mahābhārata (DharmicData); the Abhidhāna-rājendra, for Jain gāthās quoted from the commentaries.
- **Refs:** Pali section refs follow SuttaCentral segmentation, and each entry says so. Bṛhaspati Sūtra fragment labels (`fr-…`) are this unit's own labels, not an editor's numbering.
- **Opponents' reports:** every doctrinal statement of the Ājīvikas, the six teachers, the Cārvākas and the Ajñānikas is `reported_by_opponent: true`, with the reporting source named in `notes`.
  - Exception: Jayarāśi's Tattvopaplavasiṃha is a Lokāyata author's own work, so its teachings are not flagged.
  - Exception: the Isibhāsiyāiṃ 11 saying is flagged as reported, although the Jain text calls Maṅkhaliputta an arhat seer.

## Corrections to the task's MUST-COVER list
1. **Six classes (abhijāti).** DN 2 names "six classes" inside Makkhali's doctrine. The detailed list (black … supremely white, with Nanda Vaccha, Kisa Saṅkicca and Makkhali as supremely white) is ascribed to **Pūraṇa Kassapa** in AN 6.57. Both are recorded as given.
2. **"No cause" (ahetu).** The doctrine that there is no cause for defilement or purification is Makkhali's in DN 2 but **Pūraṇa's** in SN 22.60 and SN 46.56. SN 46.56 applies it to knowing and seeing.
3. **Great aeons.** The number is 8,400,000 (cullāsīti mahākappino satasahassāni), checked in DN 2 §20.7.
4. **Fourfold restraint.** DN 2's cātuyāma-saṃvara is the Buddhist report. The Jain canon assigns the four restraints (cāujjāma) to **Pārśva** and the five vows to Mahāvīra (Utt 23.12–13, checked). The Buddhist and Jain accounts are cross-linked with `differs_from`.
5. **The count of 363 views is not in the Sūtrakṛtāṅga text.** The text (1.12.1) names only the four "samosaraṇas". The numbers 180/84/67/32 come from the gāthā quoted by the commentators and the combinatorial derivation in Śīlāṅka (both checked as quoted in the Abhidhāna-rājendra).
6. **Five elements, not four.** Sūtr 1.1.1.7 counts five great elements, with space as the fifth. The later Lokāyata fragments count four.
7. **Tattvopaplavasiṃha.** It quotes "the venerable Bṛhaspati" (§4.25a) and the sūtra's list of elements, saying the list is stated only "to reflect" (pratibimbana) worldly belief (§0.2). It is sceptical, as the brief said.
8. **Mahābhārata 12.39.** The Cārvāka there is a rākṣasa disguised as a Sāṃkhya mendicant. He teaches no doctrine (checked).
9. **Sañjaya in the Vinaya.** Mv 1.23–24 names Sāriputta's teacher only as "Sañjaya the wanderer". The identification with Sañjaya Belaṭṭhiputta is the commentaries'.
10. **The Tamil Ājīvika teacher is Pūraṇa.** Maṇimēkalai 27.108–165 (checked) has "Pūraṇaṉ, who knows the Ājīvaka texts", expounding "the Maṟkali text": life plus four kinds of atom, six births ending in release in the supremely white birth, and all fixed in the womb. This canto is available locally, so it is not only a U55 reference.
11. **Things the list did not mention that belong in scope:**
    - the materialist Pāyāsi (DN 23);
    - King Paesi (Rājapraśnīya);
    - the Isibhāsiyāiṃ's Maṅkhaliputta chapter (11) and its five "ukkalas" of materialism (20);
    - the Mahānāradakassapa Jātaka, whose naked ascetic Guṇa merges Gosāla's destiny with Pakudha's seven bodies;
    - the Vinaya episode of the sandalwood bowl, where all six teachers claim to be arahants with powers.

## 1. Coverage checklist (B1 and the unit brief)

**Lineages**
- lin:sramana. Jainism and Buddhism are deliberately **not** listed as sub-lineages, so the merge does not count them as one root.
- lin:ajivika (parent lin:sramana)
- lin:carvaka
- lin:ajnana (parent lin:sramana)

**Ultimate views**
- ult:sramana, ult:carvaka and ult:ajnana set `tradition_denies_single_ultimate: true`.
- ult:ajivika treats niyati as a governing order, not a ground of being. Its caveat says the sources are hostile.

**The six teachers of DN 2**
- The teachers, by teaching:
  - Pūraṇa: tea:samannaphala-sutta:17
  - Makkhali: :20 and :20.7 (the enumerations)
  - Ajita: :23
  - Pakudha: :26
  - Nigaṇṭha: :29
  - Sañjaya: :32
  - The king's verdict: :33
  - The ministers' praise of all six: :2-7
- Teacher entries:
  - tch:purana-kassapa, tch:makkhali-gosala, tch:ajita-kesakambali, tch:pakudha-kaccayana, tch:sanjaya-belatthiputta
  - U33 contribution to tch:mahavira
- The six as a group:
  - cpt:six-teachers
  - tea:dahara-sutta:2
  - tea:kutuhalasala-sutta:2-4
  - tea:sabhiya-sutta:2-3
  - tea:mahaparinibbana-sutta:5.26-27
  - tea:mahasaccaka-sutta:48
  - tea:mahasakuludayi-sutta:6
  - tea:nanatitthiyasavaka-sutta:2-14
  - tea:vinaya-pitaka:cv.5.8
  - tea:milindapanha:2.7, 2.8
- The same doctrines unnamed:
  - tea:sandaka-sutta:7-19
  - tea:apannaka-sutta:5-12, 13-20, 21-28
  - tea:ditthi-samyutta:24.5–24.8
- Named reports:
  - tea:kesakambala-sutta:1-3
  - tea:anguttara-nikaya:1.319
  - tea:mahali-sutta-sn22-60:2
  - tea:abhaya-sutta-sn46-56:1
  - tea:chalabhijati-sutta:1-9 and 10-17
- Doctrine concepts:
  - cpt:akiriyavada
  - cpt:niyativada, cpt:samsara-suddhi, cpt:ball-of-thread
  - cpt:six-abhijatis
  - cpt:mahakappa-ajivika, cpt:ajivika-cosmology
  - cpt:ucchedavada, cpt:natthikavada
  - cpt:seven-bodies-pakudha
  - cpt:fourfold-restraint
  - cpt:amaravikkhepa, cpt:four-questions-sanjaya

**Chinese Āgama parallel**
- src:shamenguo-jing (DĀ 27) and src:jizhi-guo-jing (T 22) are recorded as sources only (see Gaps).

**Jain reports of rival views**
- src:sutrakrtanga teachings, all checked:
  - 1.1.1.7-8, 9-10, 11-12, 13-14, 15-16, 17-18, 19-27
  - 1.1.2.1-5, 14-23, 24-29
  - 1.1.3.5-10, 11-12
  - 1.12.1, 1.12.2, 1.12.3, 1.12.4-8, 1.12.9-10, 1.12.11-22
- src:sutrakrtanga teachings from memory: 2.1, 2.6, 2.6/2, 2.6/3.
- Commentaries and other Jain works:
  - tea:sutrakrtanga-niryukti:1.12
  - tea:sutrakrtanga-vrtti-silanka:1.12
  - tea:sthananga-sutra:4 and 4/2
  - tea:sarvarthasiddhi:8.1
  - tea:tattvartha-rajavarttika:8.1
  - tea:sanmati-tarka:3.53
  - tea:isibhasiyaim:11, 20, 20/2
  - tea:rajaprasniya:paesi and paesi/2
- Concepts: cpt:jain-report-rival-views, cpt:four-vada-classes, cpt:363-views, cpt:ajnanavada, cpt:vainayikavada, cpt:five-causes-jain, cpt:ukkala-five.

**Ājīvikas**
- Gosāla's life in Bhagavatī 15: tea:bhagavati-sutra:15, 15/2 to 15/8.
- Uvāsagadasāo: tea:uvasagadasao:6, 7, 7/2.
- Other Ājīvika figures: tch:nanda-vaccha, tch:kisa-sankicca, tch:upaka-ajivaka, tch:halahala, tch:saddalaputta, tch:ayampula, tch:guna-kassapa.
- Buddhist reports:
  - tea:tevijjavacchagotta-sutta:14-15
  - tea:mahasaccaka-sutta:5-6
  - tea:sandaka-sutta:53
  - tea:ariyapariyesana-sutta:25
  - tea:therigatha:13.3
  - tea:mahanaradakassapa-jataka:34-45
- Concepts: cpt:reanimation-ajivika, cpt:tejolesya, cpt:mahanimitta, cpt:eight-finalities, cpt:ajivika-disacaras, cpt:ajivika-three-leaders, cpt:ajivika-austerities, cpt:gosala-in-isibhasiyaim, cpt:ajivika-atoms.
- Barābar caves and Aśoka's donations (scholarly metadata):
  - src:barabar-cave-inscriptions, src:nagarjuni-cave-inscriptions
  - src:asokan-edicts, with tea:asokan-edicts:pe7, re12, re13
  - tch:asoka
- Arthaśāstra fine for feeding Ājīvakas: tea:arthasastra:3.20.16.
- Later South Indian Ājīvikas:
  - tea:manimekalai:27.108-165 (checked)
  - tea:nilakesi:acivaka-vatam (low)
  - tea:sivananasiddhiyar:parapakkam.acivaka (low)
- Extinction: recorded in lin:ajivika `status: extinct`, dating and notes.
- Legends: tea:divyavadana:28 (Puṇḍravardhana) and tea:divyavadana:12.
- Path maps: pth:ajivika-samsara-suddhi and pth:ajivika-eight-purisabhumi.

**Cārvāka / Lokāyata**
- Bṛhaspati Sūtra fragments: src:brhaspati-sutra, with tea:brhaspati-sutra:fr-atha, fr-tattvani, fr-samudaye, fr-caitanya, fr-purusa, fr-paraloka.
- Jayarāśi:
  - src:tattvopaplavasimha
  - tea:tattvopaplavasimha:0.1, 0.2, 0.3, 1, 2-4, 4.25a, 5, end
  - tch:jayarasi-bhatta
- Purandara: tch:purandara-carvaka, tea:tattvasangraha-panjika:1481-1482.
- Kambalāśvatara: tch:kambalasvatara, tea:tattvasangraha:1857-1864, tea:tattvasangraha-panjika:1864.
- Aviddhakarṇa and Bhaṭṭodbhaṭa: tch:aviddhakarna, tch:bhattodbhata (both low).
- Founders: tch:brhaspati (U33 contribution), tch:carvaka.
- The epic figure: tch:carvaka-raksasa, tea:mahabharata:12.39.22-47.
- Sarvadarśanasaṅgraha ch. 1: tea:sarvadarsanasangraha:1 and 1/2 to 1/9.
- Śaṅkara:
  - tea:brahma-sutra-bhasya-sankara:3.3.53/2 and 3.3.54 (checked)
  - existing U13 teaching tea:vedantasara:refutation (the four Cārvāka self-views) is cross-referenced
- Jain reports:
  - tea:saddarsanasamuccaya-haribhadra:80, 81, 82, 83-85
  - tea:tarkarahasyadipika:80
- Buddhist reports:
  - tea:tattvasangraha:1456, 1857-1864, 1865-1964
  - tea:prasannapada:18.6
- Nyāya reports: tea:nyayamanjari:1.pramana-sankhya, 1.carvaka-dhurta, 7.susiksita-carvaka (checked).
- Other reports:
  - tea:sarvasiddhantasangraha:2
  - tea:prabodhacandrodaya:2
  - tea:arthasastra:1.2.4-5 (checked)
  - tea:manimekalai:27.80-81 and 27.263-286 (checked)
  - tea:nilakesi:puta-vatam
  - tea:sivananasiddhiyar:parapakkam.lokayata
- Positions, as concepts:
  - perception as the only pramāṇa: cpt:pratyaksa-only, cpt:critique-of-inference, cpt:purandara-worldly-inference
  - four elements: cpt:carvaka-four-elements
  - consciousness like fermentation: cpt:bhuta-caitanya, cpt:madasakti-simile
  - self as body: cpt:dehatmavada, cpt:tajjiva-taccharira
  - denial of rebirth and karma: cpt:paraloka-denial, cpt:svabhavavada
  - critique of ritual and priests: cpt:critique-of-sacrifice, cpt:barhaspatya-arthasastra
  - pleasure, heaven, hell and release: cpt:carvaka-hedonism, cpt:carvaka-heaven-hell-liberation
  - kinds of Cārvāka: cpt:susiksita-carvaka, cpt:tattvopaplava, cpt:loka-vyavahara-carvaka
  - the wolf's footprint: cpt:vrkapada-parable
- The verses opponents attribute to them are in the SDS 1/8 and 1/9 teachings (two with `original`), the Nyāyamañjarī variant (checked), and Haribhadra 81–82.
- Materialists in the narratives: tea:payasi-sutta:2, 6-12, 14-20, 29-30; tch:payasi; tch:paesi; tch:kumara-kassapa; cpt:carvaka-experiments.
- Existing cross-references (not duplicated):
  - tea:maitri-upanisad:7.9-10
  - tea:visnu-purana:3.17-18
  - tea:ramayana:2.108.1-18 and dsp:jabali-rama (U05)
  - tea:nyaya-sutra:2.1.58-59
  - tea:arthasastra:1.2.10-12
  - tea:brhadaranyaka-upanisad:2.4.12 (quoted by the SDS)
  - dsp:consciousness-from-elements (U09)
  - dsp:validity-of-inference (U11)

**Ajñāna and the view catalogues**
- Ajñāna: lin:ajnana, cpt:amaravikkhepa, cpt:ajnanavada, prc:amaravikkhepa-suspension.
- Brahmajāla views:
  - cpt:sixty-two-views, with 10 class concepts: sassata, ekacca-sassata, antānantika, amarāvikkhepa, adhicca, saññī, asaññī, nevasaññī, uccheda, diṭṭhadhammanibbāna
  - tea:brahmajala-sutta:1.30-1.37, 2.1-2.15, 2.16-2.22, 2.23-2.29, 2.30-2.36, 2.38-2.39, 3.1-3.4, 3.5-3.8, 3.9-3.18, 3.19-3.28, 3.29-3.31, 3.32-3.71
  - The net simile is U36's tea:brahmajala-sutta:3.72-3.73.
- Other catalogues: cpt:three-sectarian-tenets, cpt:four-negations-of-holy-life, cpt:four-unreliable-holy-lives, cpt:apannaka-wager.

**Śramaṇa–brāhmaṇa contrast**
- cpt:sramana-brahmana-contrast
- Buddhist: tea:dhammapada:142, 184, 265, 388; tea:bhuridatta-jataka:158-160, 161-173; tea:mahabhasya:2.4.12 (checked); tea:asokan-edicts:re12, re13.
- Jain: tea:uttaradhyayana-sutra:25.31-33 (checked).
- Existing cross-references: tea:taittiriya-aranyaka:2.7.1 and tea:brhadaranyaka-upanisad:4.3.22.
- Practices: prc:sramana-pabbajja, prc:sramana-vada, cpt:sramana-debate-culture.

**Disputes**
- New, all queued with candidate readings; please add RQ-U33-1 to 6 to RECONCILE_QUEUE.md:
  - dsp:niyati-or-effort (RQ-U33-1). The candidate is P2, the Jain five-cause synthesis in Sanmati 3.53; the Ājīvika and Buddhist objections are recorded.
  - dsp:is-there-fruit-of-action (RQ-U33-2)
  - dsp:materialism-and-the-other-world (RQ-U33-3). Candidates are P1, P2 (the suśikṣita partial concession) and P6 (the Maitrī Up. 7.9 account).
  - dsp:tajjiva-taccharira (RQ-U33-4)
  - dsp:suspension-of-judgment (RQ-U33-5)
  - dsp:gosala-mahavira (RQ-U33-6, a historical debate)
- Contributions, with sides only and no reconciliation, since U50 owns them: dsp:number-of-pramanas, dsp:status-of-veda, dsp:is-there-a-self, dsp:isvara.

**Other entities**
- **Practices** (restricted ones are summary-only, with the texts' own warnings):
  - prc:acelaka-vata (restricted)
  - prc:ajivika-tapas (restricted)
  - prc:tejolesya-sadhana (restricted; no steps or durations)
  - prc:mahanimitta
  - prc:kukkuravata-govata
  - prc:vainayika-veneration
  - prc:amaravikkhepa-suspension
  - prc:sramana-pabbajja
  - prc:sramana-vada
- **Obstacles:** obs:ditthi-jala, obs:niyata-micchaditthi, obs:uccheda-ditthi, obs:sassata-ditthi, obs:amaravikkhepa, obs:bala-tapa, obs:attakilamathanuyoga, obs:mithyatva, obs:dhurta-vancana.
- **Phenomenology:**
  - DN 1 meditative grounds of views: past-life recollection, first perception, the finite world, jhāna taken for nibbāna.
  - Gosāla (Jain report): tejoleśyā, reanimation, deathbed state, prognostication.
  - The six teachers' claims to powers; Upaka's sign.
- **Borrowings** (8):
  - Sañjaya's disciples to Buddhism
  - Pūraṇa and the Ājīvikas
  - Pakudha's bodies in the Ājīvika doctrine
  - Ajita to the Lokāyata
  - Mahānimitta from the Pūrvas
  - abhijāti and leśyā
  - the Bārhaspatya Arthaśāstra and the Lokāyata
  - Sañjaya's formula and syādvāda (scholarly hypothesis; the Jain objection is recorded)

## 2. Least sure — check first (possible hallucinations)
- **Bhagavatī 15** (not local), in particular:
  - the six disācaras' names in cpt:ajivika-disacaras (low);
  - the two burnt monks (Savvāṇubhūi, Sunakkhatta);
  - the list of eight finalities;
  - Udāyi Kuṇḍiyāyaṇa;
  - the future birth as Daḍhapaiṇṇa;
  - the Revatī and Sīha episode;
  - Ayampula;
  - Gosāla's birthplace Saravaṇa and the brāhmaṇa Gobahula.
- **Uvāsagadasāo 6–7 details:** the wife Aggimittā and the epithets of Mahāvīra (7/2, low).
- **Sthānāṅga 4:** the fourfold Ājīvika austerity (low).
- **Sūtrakṛtāṅga Book 2 (2.1, 2.6):** the contents of the lotus parable and Ārdraka's debates, from memory.
- **Rājapraśnīya:** the order and content of Paesi's experiments and Kesi's similes.
- **Buddhist legends and commentaries:**
  - Divyāvadāna 12 and 28, including the chapter numbers and the Ājīvika vs Nirgrantha versions of the Puṇḍravardhana story;
  - Dhammapada-aṭṭhakathā 14.2 (Pūraṇa's drowning);
  - the Sumaṅgalavilāsinī's name etymologies and the eight purisabhūmi names (the whole of pth:ajivika-eight-purisabhumi is low).
- **Jain doxographies and commentaries:**
  - Haribhadra ṢDS verse numbers 80–85, and the content of 83–85;
  - Guṇaratna (tea:tarkarahasyadipika:80);
  - Sanmati "3.53" (the wording was checked, the number was not);
  - Rājavārttika 8.1.
- **Other doxographies:**
  - the Sarvasiddhāntasaṅgraha chapter (2) and its attribution;
  - Nīlakēci chapter names and "Pūraṇa as Ājīvika teacher" there;
  - the Śivajñānasiddhiyār Parapakkam sections.
- **Cārvāka authors:** Aviddhakarṇa's Cārvāka affiliation (Kamalaśīla's citations checked do not show it) and Bhaṭṭodbhaṭa.
- **Inscriptions and edicts:** the paraphrases of Aśokan RE 12, RE 13 and PE 7 (from memory), and the Nāgārjunī cave names.
- **Single refs:** the Arthaśāstra section number 3.20.16 (wording checked); the Prasannapadā kārikā 18.6 (located in an OCR-damaged e-text); and the commentarial term niyata-micchādiṭṭhi.
- **The Tattvopaplavasiṃha closing sentence** ("avicāritaramaṇīyāḥ…"). The local manuscript is incomplete.
- **SDS ch. 1:** the whole chapter is from memory (the local DCS extract has only the Raseśvara chapter). Moderate confidence overall.
- **Lineage dating:** the Ājīvika end date (the "ācīvakak-kācu" tax into the Cōḻa period) and the Lokāyata date range are low.

## 3. Gaps (belong here, not responsibly creatable)
- **Chinese Āgama parallel.** CBETA T01 is not in sources_raw, so which doctrines DĀ 27, T 22 and EĀ 43.7 assign to which teacher could not be verified; the source entries are made but no teachings. The Sanskrit Śrāmaṇyaphala-sūtra of the Saṅghabhedavastu is also missing (U38?).
- **Ājīvika religious fasting to death.** It is reported in modern studies, but this unit could not tie it to a primary passage, so no entry was made.
- **The four drinkables and non-drinkables (Bhagavatī 15)** are not itemised.
- **Akalaṅka's names for the teachers of the 363 views.**
- **The Jain Nandī and Anuyogadvāra list of "false scriptures" that includes Logāyata.**
- **The Viśeṣāvaśyakabhāṣya Gaṇadharavāda** (the gaṇadharas' doubts on soul and body) — for U34/U35.
- **The Pali "lokāyata" as a brāhmaṇical art forbidden to monks.** An existing teaching, tea:vinaya-pitaka:cv.5.33.2, may cover it (not linked here).
- **Mahāvaṃsa 10** (a dwelling for Ājīvakas at Anurādhapura) and **Bṛhajjātaka 15.1** (Ājīvika among the ascetic types by planet): recalled but not created.
- **Sources not made:** Dharmakīrti's Pramāṇavārttika refutation of materialism is referenced only in a dispute side (PV ch. 2), and Kumārila's Ātmavāda is not linked either — both lack verse refs.
- **Guṇaratna's remark on Kāpālika nāstikas** — not made.
- **The Vimānavatthu story of Pāyāsi's afterlife** — not made.
- **The fragments of Udbhaṭa's commentary** — not made.

## 4. Out of reach
- No Ājīvika, Ajñānika or early Lokāyata text survives. Every doctrine except Jayarāśi's is known only from opponents.
- The Bṛhaspati Sūtra and the commentaries of Kambalāśvatara, Purandara, Aviddhakarṇa and Udbhaṭa are lost.
- Not available locally: Bhagavatī, Uvāsagadasāo, Sthānāṅga, Rājapraśnīya, Sūtrakṛtāṅga Book 2, Nīlakēci, Śivajñānasiddhiyār, and the Cārvāka chapter of the SDS.
- Restricted material appears as summaries plus the texts' own warnings only: the method of gaining tejoleśyā, the naked ascetics' fasting regimes, and the Ājīvika austerities. No steps, quantities or durations are given.
