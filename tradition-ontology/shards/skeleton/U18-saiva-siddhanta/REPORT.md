# U18 Śaiva Siddhānta: skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Counts:** 3 lineages, 61 sources, 100 teachers, 138 teachings, 90 terms, 37 concepts, 29 practices, 9 obstacles, 7 disputes, 11 phenomenology entries, 5 borrowings, 1 path map, 3 ult views, 12 interpretation_log lines. Validator: 0 errors.

**Decision:** I created two sub-lineages that are not in the registry. This keeps the Sanskrit and Tamil positions apart (for example śivasāmya against the Tamil advaita of inseparability).
- `lin:tamil-saiva-siddhanta` (the Meykaṇṭa school)
- `lin:nayanmar` (the Tirumuṟai bhakti stream)

Both have parent `lin:saiva-siddhanta`, which has parent `lin:mantramarga`. There are three ult views: `ult:saiva-siddhanta`, `ult:tamil-saiva-siddhanta` and `ult:nayanmar`.

**Reused ids:**
- **From U08:** `src:kirana-tantra`, `src:matangaparamesvara`, `src:mrgendra-tantra`, `src:somasambhupaddhati`, `src:kriyakramadyotika`, `src:mrgendravrtti`, `src:kiranavrtti`, `src:matangavrtti`, `src:siddhantasaravali`, `src:saivasiddhantaparibhasa`, `src:pauskarabhasya`, and U08's diksa/saktipata concepts and terms.
- **From U19:** `cpt:thirty-six-tattvas`, `cpt:five-acts-of-siva`, `cpt:three-malas`, and the malas under `trm:` and `obs:`.
- **Disputes I added sides to:** U19's `dsp:liberation-identity-or-equality-with-siva` and `dsp:mala-substance-or-ignorance`, and U08's `dsp:does-diksa-liberate` and `dsp:cause-of-saktipata`. I added Sanskrit-exegete and Tamil-school sides.

## 1. Checklist (coverage map A7 Siddhānta and I2 Tirukkuṟaḷ)

**Sanskrit authors and works**
- **Sadyojyoti** (`tch:sadyojyoti`), with teacher `tch:ugrajyoti`. Works:
  - `src:naresvarapariksa`
  - `src:moksakarika`
  - `src:paramoksanirasakarika`
  - `src:tattvasangraha-sadyojyoti`
  - `src:tattvatrayanirnaya`
  - `src:bhogakarika`
- **Bṛhaspati:** `tch:brhaspati-saiddhantika`.
- **Rāmakaṇṭha:** `tch:ramakantha`, with `src:naresvarapariksaprakasa`, `src:moksakarikavrtti` and `src:paramoksanirasakarikavrtti`, plus U08's Kiraṇa and Mataṅga commentaries.
- **Nārāyaṇakaṇṭha:** `tch:narayanakantha` (Mṛgendravṛtti).
- **Aghoraśiva:** `tch:aghorasiva`, with `src:astaprakarana`, `src:mahotsavavidhi`, `src:pancavaranastava` and the Kriyākramadyotikā.
- **Others:**
  - Somaśambhu (`tch:somasambhu`)
  - Bhoja, with `src:tattvaprakasa-bhoja`
  - Trilocanaśiva, with `src:prayascittasamuccaya-trilocanasiva`
  - Śrīkaṇṭha: `tch:srikantha-saiddhantika` with `src:ratnatraya-srikantha`
  - `src:nadakarika`
  - `src:tatparyadipika-srikumara`
  - Śivāgrayogin, with `src:sivajnanabodha`

**Tamil texts**
- **Tirumuṟai:** `src:tirumurai`, with all 12 books described.
- **Tēvāram and Tirumuṟai 8–10:** `src:tevaram`, `src:tiruvacakam`, `src:tirukkovaiyar`, `src:tiruvicaippa`, `src:tiruppallantu`, `src:tirumantiram` (nine tantras).
- **Book 11:** `src:patinonram-tirumurai`, and 7 of its works as separate entries.
- **Periya Purāṇam:** `src:periya-puranam`.
- **Meykaṇṭa Śāstras:** `src:meykanta-sastras`, with all 14 listed and each given its own id. Among them:
  - `src:sivananabodham` (12 sūtras, one teaching each)
  - `src:sivananasiddhiyar`
  - `src:irupa-irupatu`
  - Umāpati's 8 works, including `src:tiruvarutpayan` and `src:civappirakacam`
- **Later works:** `src:civanana-mapatiyam`, `src:civanana-potac-cirrurai`, and the purāṇas of Umāpati and Parañcōti.

**Tamil teachers**
- The 63 Nāyaṉmārs each have a `tch:` entry with the tradition's account, and the full roster is in `cpt:sixty-three-nayanmars`.
- Also covered: Kāraikkāl Ammaiyār, Kaṇṇappar, Nantaṉār, Māṇikkavācakar, Cēkkiḻār, Nampi Āṇṭār Nampi, Meykaṇṭār, Aruṇanti, `tch:marainana-campantar`, Umāpati and `tch:civanana-munivar`.
- Recent (flagged `recent: true`): Ārumuka Nāvalar and Maṟaimalai Aṭikaḷ.

**Concepts**

| Topic | Ids |
|---|---|
| Pati, paśu, pāśa | `cpt:pati-pasu-pasa` |
| Three and five malas | `cpt:three-malas`, `cpt:five-malas`, and `obs:*` |
| Three classes of souls | `cpt:three-classes-of-souls` |
| 36 tattvas (Siddhānta form) | `cpt:thirty-six-tattvas` |
| Five acts | `cpt:five-acts-of-siva` |
| Four pādas and four liberations | `cpt:four-padas`, `cpt:four-kinds-of-mukti`, `cpt:four-margas` |
| Dīkṣā | `cpt:kinds-of-diksa`, `cpt:grades-of-initiates`; practices for samaya, viśeṣa, nirvāṇa and ābhiṣeka |
| Śaktipāta and malaparipāka | `cpt:saktipata`, `cpt:malaparipaka` |
| Iruviṉaiyoppu | `cpt:iruvinaiyoppu` |
| Śivasāmya and Tamil advaita (both recorded) | `cpt:sivasamya`, `cpt:siddhanta-advaita` |
| Grace | `cpt:grace-anugraha`, `trm:arul` |
| Naṭarāja and Chidambaram | `cpt:dance-of-nataraja`, `trm:cidambara` |
| Other | three causes, bindu and māyā, Vidyeśvaras, mantra-body, pañcākṣara, the ten kāryas, navabheda, eṇkuṇam, lineages of teachers, avasthās, sadasat |

**Tirukkuṟaḷ**
- Structure: 3 books, 133 chapters, 1,330 couplets.
- Dating: tradition's and scholarly accounts kept apart.
- Affiliation: 33 couplet teachings, and the dispute `dsp:affiliation-of-tirukkural` with Jain, Śaiva, Vaiṣṇava, Buddhist and non-sectarian sides. It is **queued**.

**Path map**
- U51 owns `pth:saiva-siddhanta-four-padas`, which I only referenced. Proposed bands for U51: caryā B1–B2, kriyā B2, yoga B3–B4, jñāna B5–B7, with sālokya, sāmīpya and sārūpya counted as station-liberations.
- New map: `pth:saiva-siddhanta-ten-karyas`.

**Disputes**
- New: `dsp:is-siva-the-material-cause`, `dsp:tamil-saiva-and-jain-contests` (historical debates at Madurai, Appar's trials, and the Buddhists at Chidambaram) and `dsp:affiliation-of-tirukkural`.
- U50's disputes are referenced: `world-real-or-appearance`, `souls-one-or-distinct`, `isvara`, `is-there-a-self`, `causation`, `works-knowledge-grace`, `women-caste-liberation` and `status-of-veda`.

**Corrections to the brief**
- "Rāmakaṇṭha II" and "Bhaṭṭa Rāmakaṇṭha" are the same person. He is distinct from Rājānaka Rāmakaṇṭha of the Spanda/Gītā commentaries.
- Aghoraśiva commented on 6 of the 8 Aṣṭaprakaraṇa treatises, not all 8. Rāmakaṇṭha commented on the Mokṣakārikā and Paramokṣanirāsakārikā.
- The Śrīkaṇṭha of the Ratnatraya is not the Śrīkaṇṭha of the Brahmasūtra bhāṣya. His id is `tch:srikantha-saiddhantika`.
- Māṇikkavācakar is not one of the 63.

## 2. Least sure (possible hallucinations — check first)
- **Verse numbers:**
  - Tirumantiram 63, 85, 724, 1823, 2104, 2397
  - Tēvāram 2.66.1, 2.85.1, 3.54.1, 6.95.10
  - Tiruvācakam 35 (Accappattu)
  - Uṇmai Viḷakkam 36
  - Kuṟaḷ 81, 267, 1103
- **Teachings summarized at section level (reconstructed):** the Sanskrit treatises, with placeholder locators like "1-150"; `tea:nadakarika`, `tea:tattvatrayanirnaya` (which triad it treats is uncertain), `tea:bhogakarika`, `tea:matangavrtti` and `tea:kriyakramadyotika:diksa`.
- **Lists given from memory:**
  - the seven modes of dīkṣā in the Cittiyār
  - Umāpati's nine refuted views
  - the 14 schools of the Parapakkam
  - the Tiruvicaippā poets
  - the 40 works and 12 authors of book 11
  - the nine tokai aṭiyār groups
  - the 35/25/3/2/1 placement of the avasthās
  - the navabheda and the four circles of schools
- **Other details:**
  - the alias Kheṭapāla for Sadyojyoti
  - the Śivatanu title for Bṛhaspati
  - Somaśambhu and the Golagī maṭha; Aghoraśiva and the Āmardaka lineage
  - Trilocanaśiva's works
  - Śrīkumāra and the Tātparyadīpikā
  - the Kuñcitāṅghristava, Cēkkiḻār Purāṇam and Tiruttoṇṭar Purāṇa Cāram
  - the Nīlakēci commentary calling the Kuṟaḷ "our scripture"
  - the Pariyaṅka yōkam section, recorded restricted with summary only
- **Low-confidence Nāyaṉmār stories:** Cōmāci Māṟar, Ciṟappuli, Kaṇanātar, Kūṟṟuvar, Pukaḻccōḻar's ending, Kalikkampar, Cattiyār, Kāri, Vāyilār, Muṉaiyaṭuvār, Kaḻaṟciṅkar, Iṭaṅkaḻiyār, Ceruttuṇaiyār, Pukaḻttuṇaiyār, Kōṭpuliyār, Nēcar and Perumiḻalaikkuṟumpar.
- **Ids guessed from the slug rule or registry (not yet in any shard):** `lin:mahayana` for the Buddhist Kuṟaḷ claim (approximate) and `obs:three-poisons`.

## 3. Gaps (not created responsibly)
- Sadyojyoti's Raurava commentary.
- Vidyākaṇṭha and other later Kashmirian Saiddhāntikas.
- Hṛdayaśiva's and Jñānaśambhu's doctrine, and the Nirmalamaṇi commentary.
- The Tamil Kantapurāṇam.
- The ātīṉam founders (Namaccivāya Mūrttikaḷ, Guru Ñāṉacampantar) and Kumarakuruparar.
- The six Cittiyār commentators.
- Verse-level teachings from the Civappirakācam, Neñcuviṭu Tūtu, Poṟṟippahṟoṭai and Viṉāveṇpā.
- Tēvāram hymn counts and the tradition's numbers of lost hymns.
- The exact 96-tattva list (left to U22).
- The Periya Purāṇam verse count.

## 4. Out of reach
- Oral initiatory instruction (upadeśa) of dīkṣā.
- Ōtuvār performance traditions (paṇ).
- Ātīṉam oral lineages.
- Many Siddhānta paddhatis that exist only in manuscript (IFP, Nepal).

**Needs RQ ids in RECONCILE_QUEUE.md:** `dsp:affiliation-of-tirukkural`, `dsp:tamil-saiva-and-jain-contests` and `dsp:is-siva-the-material-cause`.
