# U04 — Minor Upaniṣads (the Muktikā canon) — skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Method
- Written from own knowledge, then checked against a local e-text of the Nirṇayasāgara-type collection *Īśādiviṃśottaraśatopaniṣadaḥ* (120 Upaniṣads, South Indian recension, with Upaniṣad Brahmayogin's opening verses; github.com/sanskrit/raw_etexts, 108_Upanishads.md).
- All verse and section refs follow that e-text. Adyar, Schrader and northern editions number differently.
- All entries are at verification level "skeleton". Confidence is high or moderate where the passage was read in the e-text, and low where it was reconstructed.
- 17 teachings carry an `original`. Each was read in the e-text before being included.
- Generator scripts are in `_gen/`. `run_all.sh` rebuilds everything and `part11_finalize.py` checks cross-references: every tea:, cpt:, prc:, obs:, pth:, trm: and dsp: reference resolves.

## Coverage checklist (A2 and the rest of the brief)
- **Muktikā canon:** `src:muktika-upanisad` holds `canon.list`, all 108 in order with Veda and group. It points to U03's ids for the 13 texts U03 owns (10 principal + Śvetāśvatara, Maitrāyaṇī/`src:maitri-upanisad`, Kauṣītaki).
  - All 95 other texts are sources `src:<name>-upanisad`. Each has a `canon` field (number, Veda per the Muktikā, peace-chant, editorial group), both dating accounts, a summary, uncertainty notes, and editions (the e-text and the Adyar series).
  - Concepts: `cpt:muktika-canon`, `cpt:minor-upanisad-groups`. Path map: `pth:muktika-path`, the graded study Māṇḍūkya → 10 → 32 → 108.
  - The Muktikā's teaching on four kinds of liberation vs kaivalya, and on jīvanmukti through destroying vāsanā, dissolving mind and knowing truth, is under `tea:muktika-upanisad:*`.
- **The 20 Yoga Upaniṣads (240 teachings):** Haṃsa, Amṛtabindu, Amṛtanāda, Kṣurikā, Tejobindu, Nādabindu, Dhyānabindu, Brahmavidyā, Yogatattva, Triśikhibrāhmaṇa, Yogacūḍāmaṇi, Maṇḍalabrāhmaṇa, Advayatāraka, Mahāvākya, Yogakuṇḍalī, Darśana, Śāṇḍilya, Varāha, Yogaśikhā, Pāśupatabrahma.
  - Concepts: nāda, bindu, kuṇḍalinī, cakras, nāḍīs, ten vāyus, three granthis, three lakṣyas, five vyomas, tāraka/amanaska, unmanī, five states, ten sounds, measures of Oṃ, levels of speech, ajapā/haṃsa, four yogas, four avasthās, seven bhūmikās, ten yamas and ten niyamas, limbs redefined as knowledge, siddhis, death omens.
  - 13 path maps, including the six-, eight- and fifteen-limbed schemes, `pth:varaha-seven-bhumikas`, `pth:hamsa-ten-nadas` and `pth:nadabindu-nada-stages`.
  - 30 phenomenology entries.
- **The Saṃnyāsa Upaniṣads (129 teachings), 17 texts plus Āśrama, Kaṭhaśruti and Mahānārāyaṇa (TA 10):**
  - `lin:sannyasa` is worked through the section-D checklist. `ult:sannyasa` is the lineage's ultimate view.
  - Four kinds of renunciation: `cpt:four-kinds-of-sannyasa`. Four or six kinds of renouncer with their marks, food, bathing, worship and worlds: `cpt:six-kinds-of-renunciant`, `pth:sannyasa-six-renunciant-grades`.
  - Rite: `cpt:sannyasa-rite`, `pth:sannyasa-rite-sequence`. Also covered: vidvat/vividiṣā and ātura/krama renunciation, inner topknot and thread, five kinds of alms, causes of a renouncer's fall, avadhūta, ativarṇāśramin, svecchācāra.
- **Śaiva (13 texts):** Kaivalya, Atharvaśiras (pāśupata vow), Atharvaśikhā, Bṛhajjābāla, Kālāgnirudra (tripuṇḍra), Dakṣiṇāmūrti, Śarabha, Akṣamālikā, Rudrahṛdaya, Bhasmajābāla, Rudrākṣajābāla, Gaṇapati, Pañcabrahma, Jābāli. Śvetāśvatara belongs to U03.
- **Śākta (8):** Sītā, Tripurātāpanī, Devī, Tripurā, Bhāvanā, Saubhāgyalakṣmī, Sarasvatīrahasya, Bahvṛca.
- **Vaiṣṇava (14):** includes the Kalisantaraṇa. The Hare Kṛṣṇa mantra has a verified original, `cpt:hare-krsna-mahamantra` and `prc:hare-krsna-mahamantra-japa`. Also Gopālatāpanī (bhakti definition, original verified) and Rāmatāpanī (1.7 "forms for worshippers", original verified).
- **Sāmānya-Vedānta (22 in this unit):** includes the Vajrasūci caste critique (5 teachings, `dsp:who-is-a-brahmana`), Nirālamba, Mahā ("vasudhaiva kuṭumbakam", original verified), Garbha embryology, Subāla antaryāmin, Muktikā.
- **Outside the Muktikā:** Mahānārāyaṇa (TA 10), Āśrama, Kaṭhaśruti, Maṭhāmnāya, Nīlarudra, Kaula, Kālikā, Piṇḍa, Gopīcandana, Gaṇeśatāpanī, Śivasaṅkalpa, Allā, Caitanya (recent), Sirr-i Akbar (1657), Oupnek'hat (recent). Renunciation digests: Yatidharmasamuccaya, Yatidharmaprakāśa. Commentaries: Upaniṣad Brahmayogin, Nārāyaṇa's Dīpikās.
  - Bāṣkala, Chāgaleya, Ārṣeya and Śaunaka are left to U03, which already emits them.
- **Disputes (9):** when to renounce, who may renounce (queued), ekadaṇḍa vs tridaṇḍa marks, yoga vs knowledge, siddhis as sign or obstacle, images vs inner worship, which deity is supreme, whether the renouncer acts for the world's good, who is a brāhmaṇa. Each has both sides, rests_on, a named principle or a queue with candidate readings, and tradition_objections.
- **Borrowings (12):** haṭha → Yoga Upaniṣads; Yoga Vāsiṣṭha; Aparokṣānubhūti ↔ Tejobindu; Vivekacūḍāmaṇi ↔ Adhyātma; Pañcadaśī ↔ Avadhūta; the Buddhist Vajrasūcī; Kalisantaraṇa → Gauḍīya; Saṃnyāsa → Daśanāmī and → Śrīvaiṣṇava tridaṇḍin; Śrīvidyā ↔ Śākta Upaniṣads; Pāñcarātra vyūhas; Yoga-Yājñavalkya ↔ Darśana.

## Corrections to the coordinator's list
1. The Sannyāsa group has 17 texts. Parabrahma was missing.
2. Mudgala and Mahā are Sāmānya-Vedānta in the Adyar scheme, although their content is Vaiṣṇava. The Vaiṣṇava group therefore has 14.
3. The Śaiva group (15) includes Śvetāśvatara. The Sāmānya group (24) includes Kauṣītaki and Maitrāyaṇī. All three belong to U03.
4. The groups are editorial, from the Adyar series. The Muktikā lists the 108 by Veda only.
5. The Muktikā's "Mahānārāyaṇa" is the Atharvan Tripādvibhūti-Mahānārāyaṇa, not Taittirīya Āraṇyaka 10.
6. Kalisantaraṇa gives the "hare rāma" half first; Gauḍīya use puts "hare kṛṣṇa" first.
7. The Jābāla does not list the kinds of renouncer. The four kinds are in the Bhikṣuka, Āśrama and Śāṭyāyanīya; the six are in Nāradaparivrājaka 5 and Sannyāsa 2.
8. In the Varāha, Varāha teaches Ṛbhu (ch. 1–3) and Ṛbhu teaches Nidāgha (ch. 4–5).
9. In this recension of the Haṃsa, Gautama asks Sanatsujāta.
10. In the Pāśupatabrahma the questioner is Vaiśravaṇa (a Vālakhilya).
11. In the Pañcabrahma, Paippalāda asks and Maheśa answers; later verses are addressed to Śākala.
12. Gaṇapati Upaniṣad = the Gaṇapati Atharvaśīrṣa.
13. Kaṭhaśruti ≈ Sannyāsa Upaniṣad ch. 1. It is not the Kaṭharudra.
14. Amṛtabindu is titled Brahmabindu in the e-text.
15. Darśana = Jābāladarśana, and the Tārasāra is headed "Tāraka". Āruṇi is also called Āruṇika or Āruṇeya; Yogakuṇḍalī is also called Yogakuṇḍalinī.
16. Nirṇayasāgara colophons assign Jābāla, Kaivalya, Haṃsa, Āruṇika and Brahmabindu to the Atharvaveda, which differs from the Muktikā.
17. E-text readings. These are logged as text-corrections; the text layer itself is untouched:
    - "brahmajābāla" is taken as Bhasmajābāla.
    - "mahānārāyaṇāhvayam" at Muktikā 1.34; other editions read "…ādvayam".
    - "haṭhāvasthā" at Yogatattva 65 is taken as ghaṭāvasthā.

## Least sure
- The Haṃsa teacher (Sanatsujāta) may differ in other editions.
- Yogakuṇḍalī 1.59–61, obstacles 8–9: the readings are uncertain.
- Sannyāsa 2.101 (the "cat" and "monkey" ways): the construal is uncertain.
- Upaniṣad Brahmayogin: his alternative names and dates. Nārāyaṇa and Śaṅkarānanda: their dates.
- Adyar volume years. Olivelle 1992 and Bouy 1994 dating summaries are from memory, and every scholarly `from`/`to` is left null.
- Outside-Muktikā items: Allā, Caitanya, Kālikā, Kaula, Maṭhāmnāya.
- Lineage attributions: Gopālatāpanī to Gauḍīya and Nimbārkī (Dvaitādvaita) use; Rāmatāpanī to the Rāmānandīs; the Buddhist Vajrasūcī placed under lin:early-buddhism.
- Band assignments in all path maps are interpretive, and each map is logged. `pth:sannyasa-six-renunciant-grades` and `pth:yogatattva-four-yogas` are low confidence.
- The Śākta, Vaiṣṇava and Śaiva mantra texts (Tripurātāpanī, Hayagrīva, Dattātreya, Gāruḍa, Avyakta, Tripādvibhūti) are summary-level.

## Gaps
- Not consulted: the Adyar or other critical editions, Schrader's apparatus, northern recensions and their numbering, Olivelle's translations.
- The commentaries of Upaniṣad Brahmayogin, Nārāyaṇa and Śaṅkarānanda were not extracted.
- The long "I am" litanies and the Yoga Vāsiṣṭha-shared verse blocks (Mahā 2–5, Annapūrṇā, Sannyāsa 2.13–58, Adhyātma) are at summary level only.
- The Praṇava Upaniṣad (Oupnek'hat) and the other Atharvan-list Upaniṣads (Colebrooke's 52) are not itemized.

## Out of reach / restricted (summary only, `restricted: true`, with the texts' own warnings)
- Khecarī bodily procedures, which must be learnt from a guru (Yogakuṇḍalī 2).
- Vajrolī, amarolī, sahajolī.
- Kevala- and sahita-kumbhaka methods, and all retention counts and schedules.
- Kṣurikā "cutting", śakticālana and sarasvatī-cālana.
- The mercury analogy (Varāha 2.78–79).
- The renouncer's permitted modes of death and yogic exit at death.
- The lunar fast (cāndrāyaṇa).
- The Tripurā's Kaula-offering verse.
- Oral initiatory mantras (melana) and the mantra texts of the Rāma, Gopāla, Hayagrīva and Dattātreya Upaniṣads are named, not reproduced.
