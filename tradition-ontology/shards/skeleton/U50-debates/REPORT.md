# U50-debates — REPORT (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Counts and validation
- 15 disputes (all registry ids), 19 new teachings, 1 new source (src:dinakari), 29 interpretation_log lines.
- `python3 scripts/validate_shard.py shards/skeleton/U50-debates`: 0 errors, 1 warning (REPORT.md missing; this is the report).
- `_gen/check_refs.py`: every tea/src/lin/tch/dsp/brw id the shard references exists in data/ or the skeleton shards.
- `_gen/verify.py` checks each `original` against a local file before saving.
- A dry run of merge.py's merge_entity (no files written) confirms the U50 entries become primary for the four disputes U33 had also written. U33's sides are included verbatim, so they merge without duplicates.
- Only the question text differs, and the merge logs that as a scalar conflict.

## New teachings (text layer)
- **Brahmasūtra and Śaṅkara's bhāṣya:**
  - tea:brahma-sutra:2.2.25 and :1.3.29
  - tea:brahma-sutra-bhasya-sankara:2.2.25 (memory/recognition against momentariness), :2.2.28 (against the vijñānavādin; the witness), :2.2.31 (śūnyavāda dismissed), :1.1.12 (the twofold Brahman), :1.1.3 and :1.3.29 (the Veda's source and eternity)
- **Other Advaita and Vedānta texts:**
  - tea:mandukya-karika-bhasya-sankara:4.99 ("this was not spoken by the Buddha")
  - tea:vedantasara:apavada (the vikāra/vivarta verse, as quoted in the Śabdakalpadruma)
- **The "Buddhism in disguise" charge:**
  - tea:padma-purana:uttara-khanda.mayavada (text verified as quoted by Jīva)
  - tea:paramatma-sandarbha:71
  - tea:satadusani:opening (as quoted in a modern editor's introduction)
  - tea:samkhya-pravacana-bhasya:intro (low confidence, no original)
- **Number of pramāṇas:** tea:dinakari:pramana-sankhya (verifies the "Paurāṇikas count 8" doxography)
- **Kashmir Śaivism:** tea:pratyabhijnahrdayam:8/2 (Kṣemarāja: every doctrine is a role of the one Self)
- **Chan:**
  - tea:chanyuan-zhuquanji-duxu:402a10 and :408a02 (Zongmi)
  - tea:dasheng-wusheng-fangbian-men:1273c01 (the Northern school in its own words)

## (1) Coverage checklist (coverage map G; unit brief MUST-COVER)

**G1 dsp:is-there-a-self** — queued, RQ-U50-01.
- Nyāya, with the memory and recognition arguments: NS 1.1.10 and 3.1.x; NBh 1.1.2; NV 3.1.1; Ātmatattvaviveka
- Vaiśeṣika
- Mīmāṃsā: Śabara, Ślokavārttika, Prakaraṇapañcikā
- Sāṃkhya: SK 17-18. Yoga: YS 2.20, 4.19; YBh 4.21
- Advaita witness-self: BSBh 1.1.1/2; Dṛg-dṛśya-viveka 1; new BSBh 2.2.25, 2.2.28, 2.2.31
- Viśiṣṭādvaita; Jain jīva (TS 2.8; Bhagavatī 7.2; gaṇadharavāda); Śaiva Siddhānta; Pratyabhijñā
- Buddhists:
  - Anattalakkhaṇa
  - The chariot: SN 5.10, Milinda, Visuddhimagga 18
  - The "bundle": Vajirā's "heap of mere formations"
  - Momentariness: dsp:momentariness; Ratnakīrti
  - Vasubandhu AKBh 9; Dharmakīrti PV
  - Madhyamaka
- Pudgalavāda: dsp:pudgala; tathāgatagarbha "true self"
- U33's Cārvāka, Ajñāna and Pakudha sides
- Historical debates: Kathāvatthu 1.1; Mahāvīra and Indrabhūti; Nāgasena and Milinda; the Nyāya–Buddhist textual exchange

**G2 dsp:causation** — partially reconciled under P1 and P2.
- Satkārya (Sāṃkhya, Yoga)
- Asatkārya / ārambha (Nyāya, Vaiśeṣika)
- Vivarta (Advaita; the Vedāntasāra verse; Bhartṛhari)
- Ābhāsa (IPK 1.5.1, 2.4.1; PH 1-2)
- Avikṛta-pariṇāma (Vallabha's Anubhāṣya 1.4.26)
- Real pariṇāma (Rāmānuja, Bhāskara, Nimbārka); Dvaita; Śaiva Siddhānta
- Pratītyasamutpāda, and MMK 1.1 with Buddhapālita
- Jain anekānta: TS 5.30; ĀM 14; Sanmati 3.53

**G3 dsp:world-real-or-appearance** — queued, RQ-U50-03.
- Rāmānuja's seven untenables (Śrībhāṣya 1.1.1/7)
- Mithyātva definitions: Advaitasiddhi 1; Citsukha
- Nyāyāmṛta and its Dvaita companions
- Advaita vs Kashmir Śaivism: vivarta vs ābhāsa; māyā as Śakti (Paramārthasāra 15; PH 8/2)
- Śākta, Śaiva Siddhānta, Sāṃkhya, Jain, Nyāya and Madhyamaka sides
- Historical debates: the Nyāyāmṛta–Advaitasiddhi exchange; Rāmānuja and Yajñamūrti; the digvijaya

**G4 dsp:souls-one-or-distinct** — queued, RQ-U50-04.
- Pañca-bheda (MBhTN 1.68-71)
- Tat tvam asi vs "atat tvam asi" (Madhva's Chāndogya-bhāṣya 6.8.7)
- Viśiṣṭādvaita; Bhāskara, Nimbārka and the Gauḍīyas; BS 1.4.20-22; Śaiva Siddhānta; Kashmir Śaivism; the many-puruṣa schools

**G5 dsp:advaita-crypto-buddhism** — queued, RQ-U50-05.
- The charge: Bhāskara, Madhva/Jayatīrtha, the Padma verse, Jīva Gosvāmī, Vedānta Deśika, Vijñānabhikṣu
- The Advaita replies: BSBh 2.2.25-32; MK-bhāṣya 4.99
- The historical borrowing evidence is kept separate in `doctrinal_vs_historical`: brw:madhyamaka-to-gaudapada, brw:yogacara-to-gaudapada, brw:mandukya-madhyamaka-prapancopasama

**G6 dsp:sudden-or-gradual** — partially reconciled under P4 and P1.
- Samye: the Tibetan and Dunhuang accounts are both recorded
- Shenhui and Huatai vs the Northern school's own text
- Zongmi's classification; Jinul's synthesis; Seongcheol (recent)
- Kathāvatthu 2.9 vs Sarvāstivāda; Laṅkāvatāra; Sakya Paṇḍita; Ājñāsamyakpramāṇa; the Varāha Upaniṣad analogue

**G7 dsp:rangtong-shentong** — partially reconciled under P4 and P3.
- Dolpopa, Tāranātha, Tsongkhapa/Khedrup, Gorampa, Rangjung Dorje, Mipham, Kongtrul, and the Indian scriptural ground

**G8 dsp:prasangika-svatantrika** — partially reconciled under P4 and P6.
- Buddhapālita, Bhāviveka, Candrakīrti; Śāntarakṣita; Tsongkhapa; Gorampa; Mipham
- The Tibetan construction of the categories is recorded as metadata:
  - a historical_debates entry marked `metadata`
  - a `tibetan_classification` label on each Indian side
- Also: Gelug monastic debate; Mipham's exchanges with Gelug scholars

**G9 dsp:works-knowledge-grace** — partially reconciled under P3 and P4.
- Mīmāṃsā, both Bhāṭṭa and Prābhākara
- Advaita (knowledge alone); jñāna-karma-samuccaya (Bhāskara, Bhartṛprapañca)
- Viśiṣṭādvaita; the Vaḍakalai "monkey" and Teṅkalai "cat" positions; Dvaita grace
- The bhakti sūtras and Bhāgavata; the Gītā; the Upaniṣads
- Trika; Śaiva Siddhānta; Jain; Pure Land
- Historical debates: Śaṅkara–Maṇḍana (tradition's account); the Vaḍakalai–Teṅkalai division; Hōnen at Ōhara

**G10 dsp:isvara** — queued, RQ-U50-10.
- Nyāya's proofs; Vaiśeṣika
- Yoga's special puruṣa; Sāṃkhya
- Mīmāṃsā
- Advaita and Viśiṣṭādvaita (known from scripture alone); Dvaita; Śaiva Siddhānta
- Dharmakīrti, Śāntarakṣita, Ratnakīrti, Vasubandhu; Theravāda
- The Jains, including Haribhadra's reinterpretation; the Upaniṣads; U33's sides

**G11 dsp:status-of-veda** — queued, RQ-U50-11.
- Authorless: Mīmāṃsā, Vedānta, Dvaita
- Authored by Īśvara: Nyāya, Vaiśeṣika
- Neither eternal nor authored: Sāṃkhya
- Relativized: the Gītā
- Rejected: the Buddhists, Jains and Cārvākas (U33)
- Veda and Āgama together: Tantra; the Sant critiques

**G12 dsp:women-caste-liberation** — queued, RQ-U50-12.
- The orthodox positions, stated faithfully, including Śaṅkara's BSBh 1.3.38 and the Manīṣāpañcaka
- Digambara vs Śvetāmbara vs Yāpanīya
- The Buddhist and Mahāyāna positions
- Critiques from the Gītā, bhakti, Āḻvār, Vīraśaiva, Sant, Siddha, Kaula and Śaiva Siddhānta (Kiraṇa) traditions; haṭha

**G13 dsp:saguna-nirguna** — partially reconciled under P3, P1 and P2.
- Advaita (new BSBh 1.1.12); Rāmānuja; Madhva; the Gauḍīyas; Vallabha
- Gītā ch. 12; the Sants (Kabīr); Tulsīdās; the Trika; Śrīvidyā; the Śvetāśvatara Upaniṣad

**G14 dsp:kundalini-effort-grace** — partially reconciled under P4 and P3.
- Haṭha (HYP 3.2 "guru's grace" with 3.5 "every effort"); the Nāth texts; the Amanaska
- Trika śaktipāta and the upāyas; Kaula; the Siddhānta's view of when grace descends; Yoga Sūtra
- The Siddha Yoga claim is recent and left to U52

**G15 dsp:number-of-pramanas** — partially reconciled under P2 (the schools' own inclusion arguments).
- All counts are recorded with texts in `count_summary`

**Corrections to the unit brief's MUST-COVER list:**
- G15: the Jains count two kinds (direct and indirect: TS 1.9-12; Nyāyāvatāra 1), not 3. Viśiṣṭādvaita, Dvaita and the Pāśupatas count 3; Caraka counts 4 (with yukti). The Paurāṇika count of 8 is confirmed from the Dinakarī doxography, which also groups the Bhāṭṭas with the Vedāntins at 6.
- G5: I could not verify that Yāmuna or Rāmānuja use the label "pracchanna-bauddha", so it is not asserted. Vedānta Deśika's Śatadūṣaṇī (verified as quoted) and Jīva Gosvāmī are added instead. Two readings of the Padma verse are recorded.
- G6: the Northern school's own text uses the language of sudden transcendence (頓超佛地). "Gradual" is the Southern school's characterization and is recorded as such.
- G2: Bhartṛhari's vivarta is added, as the earliest technical use of the term.

## (2) Least sure (check first)
- tea:samkhya-pravacana-bhasya:intro — from memory; the text is not local.
- The Padma verse's locator (commonly cited as Uttarakhaṇḍa 236.7-8; unverified).
- The attribution of the starred commentary layer in the 1899 print to the Dinakarī (Mahādeva/Dinakara).
- tea:satadusani:opening — where the verse stands among the opening verses.
- dsp:rangtong-shentong historical entry: the 17th-century Jonang suppression details.
- dsp:prasangika-svatantrika historical entries:
  - that Pa tshab Nyi ma grags originated the labels
  - the description of the Gelug debate curriculum
- The order of the later Nyāyāmṛta/Advaitasiddhi rejoinders.
- The Samye date (c. 792–794).
- Gorampa's position on the Prāsaṅgika/Svātantrika difference is summarized from other units' teachings (taway-shenje), not from a passage specific to that difference.
- The "cat/monkey" labels are treated as the traditions' mnemonic.
- These other-unit teachings are low confidence and U50's sides depend on them: brahma-sutra-bhasya-bhaskara:1.4.25, sheja-kunkhyab:tenets, sastravartasamuccaya:stabaka-3, tirumantiram:2397.

## (3) Gaps
- G13: the Śaiva Siddhānta view (Śiva with form, formless, and form-and-formless) has no teaching yet.
- Not in the local corpus, so not quoted:
  - Vedāntaparibhāṣā's definitions of pariṇāma and vivarta
  - Vedāntasāra (checked only via a dictionary's quotation)
  - Bhāskara's bhāṣya
  - Sāṃkhyapravacanabhāṣya
  - the Padma Purāṇa itself
- Advaitasiddhi and Nyāyāmṛta are local (eBhāratī) but were not quoted; this is a Phase D extraction target.
- Where exactly Madhva reads "atat tvam asi" (in his own bhāṣya or later) is unverified.
- Tibetan narrative sources for Samye (sBa bzhed, Bu ston) and for the Jonang history were not checked locally.
- G14 and G15 have no historical_debates entries.

## (4) Out of reach
- The oral Tibetan courtyard debate tradition and oral ascetic lineages: only textual or tradition's-account entries are recorded.
- Restricted kuṇḍalinī, khecarī and śakticālana methods: summary only, per the rules.
- The recent Siddha Yoga śaktipāta claim: deferred to U52.
