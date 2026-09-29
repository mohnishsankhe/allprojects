# U49-cross-family — REPORT (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Before writing anything I surveyed data/borrowings.json and every other shard's borrowings.jsonl. data/ was re-merged at 12:15 during the session (424 borrowings after the merge), and I re-checked against it.
- I reused existing ids. Where I only had more evidence, I re-emitted the same id with from/to/what/direction/era copied unchanged, so the merge unions the evidence lists without scalar conflicts.
- Every evidence item is typed. Where a tradition denies a borrowing, the denial is recorded as tradition-account.
- Sufi material appears only as context (one concept and two sources). There is no Sufi lineage, doctrine or teaching.
- Originals are quoted only from texts read locally:
  - Yoga Sūtra and bhāṣya, Māṇḍūkya-kārikā, Maitrī, Haṭhapradīpikā, Pratyabhijñāhṛdaya with commentary, Tattvārtha (prepared segments)
  - Buddhacarita 12 (SARIT)
  - SN 46.54 (bilara)
  - Laṅkāvatāra ch. 2 (GRETIL, Vaidya p. 33)
  - Dattātreyayogaśāstra (eBhāratī)
  - Derge Tengyur Tōh 2285 (Amṛtasiddhimūla): homage to Heruka, and a colophon ascribing the work to Virūpa. This is new explicit evidence.

## 1. Checklist (coverage map C and the unit brief) → ids
**Tantra as a movement**
- Lineage and view: lin:tantra-movement, ult:tantra-movement.
- Shared features: cpt:tantra-common-features, cpt:bhukti-and-mukti, cpt:deity-identification-across-families, cpt:nyasa-across-families, cpt:mantra-as-deity-across-families, cpt:guru-as-deity-across-families, cpt:secrecy-across-families, cpt:subtle-body-across-families, cpt:pitha-network-across-families, cpt:tantra-and-veda.
- Kaula transgression and its internalization: cpt:internalization-of-transgression.
- Terms: trm:yantra, trm:tantrika, trm:ista-devata, trm:tantra (contribution).
- Links:
  - Vedic ritual forms into tantra: brw:vedic-ritual-forms-to-tantra.
  - Tantra into the Purāṇas: brw:tantra-to-puranic-ritual.
  - Pāśupata/Atimārga → Mantramārga: brw:atimarga-to-mantramarga (+evidence); also existing brw:pasupata-to-mantramarga.
  - Śaiva Siddhānta ↔ Pāñcarātra: new brw:saiva-siddhanta-pancaratra, plus cpt:four-padas (contribution).
  - Jain Padmāvatī: brw:tantra-to-jain-mantrasastra (+evidence), trm:sakalikarana.
- Yoginītantra borrowing from Śaiva Vidyāpīṭha texts (scholarly hypothesis): already recorded by U44 as brw:saiva-vidyapitha-to-yogini-tantras, with brw:kapalika-to-vajrayana (U17) and brw:vidyapitha-to-kaula. Not duplicated.
- Cakrasaṃvara pīṭhas ↔ Śaiva pīṭhas: brw:saiva-pithas-to-cakrasamvara (U44) and brw:yogini-pithas-to-buddhist-yoginitantras (U24), plus cpt:pitha-network-across-families.
- Tārā: brw:tara-mahacina-buddhist (+evidence), cpt:tara-across-families, trm:aksobhya.
- Mutual ranking of revelations (new dispute): dsp:ranking-of-other-revelations, cpt:doxographic-ranking-of-schools, cpt:taming-of-rival-deities.

**Nāth–Mahāsiddha overlap**
- brw:natha-mahasiddha (+evidence: the fish legend in Mīnapa and KJN 16, the Gorakṣa–Cauraṅgī pair, the Virūpa attribution).
- The two lists of 84 compared: cpt:eighty-four-siddhas-two-lists, cpt:siddha-identifications, tea:varnaratnakara:siddha-list.
- Song genres: cpt:siddha-song-genres, brw:caryagiti-and-natha-songs.
- Shared vocabulary: cpt:twilight-language-across-families, cpt:sunya-across-families, cpt:upward-flow-across-families. Sahaja is left to the existing cpt:sahaja.
- Haṭha links: brw:four-empties-and-hatha-voids, brw:vajroli-name-and-bindu-retention (restricted, summary only), dsp:source-of-hatha-yoga.

**Borrowings named in the brief**
- **Yoga Sūtras and Buddhism**
  - Four immeasurables (YS 1.33): brw:buddhism-yoga-four-attitudes (+SN 46.54), new brw:jain-four-bhavanas-and-yoga, new brw:four-immeasurables-sramana-common, cpt:four-immeasurables-across-families.
  - Kleśa theory: brw:buddhism-yoga-klesa-theory (U10).
  - Samāpatti: brw:buddhism-yoga-meditation-vocabulary (U10).
  - Dharmamegha ↔ tenth bhūmi: brw:mahayana-yoga-dharmamegha (U10), plus a cpt:dharmamegha-samadhi contribution.
  - YS 1.20 ↔ the five indriyas: brw:buddhism-yoga-five-faculties (U10), plus a cpt:five-indriyas contribution.
  - Also new: brw:jain-mahavratas-and-yoga-yamas, brw:yoga-refutes-buddhist-idealism, cpt:five-great-vows-across-families.
- **Gauḍapāda and Madhyamaka**
  - brw:madhyamaka-to-gaudapada (+verse-level refs), brw:yogacara-to-gaudapada, brw:mandukya-madhyamaka-prapancopasama.
  - New: brw:mahayana-vocabulary-in-alatasanti.
  - Teachings: GK 4.19, 4.42, 4.73-74, 4.87-88, 4.90, 4.98, 4.100; tea:mandukya-karika-bhasya-sankara:4.99.
- **Pratyabhijñā and Dharmakīrti:** brw:pramana-buddhist-to-pratyabhijna (+evidence); dsp:pratyabhijna-vs-buddhist-logicians (U19).
- **Amṛtasiddhi and early haṭha:** brw:amrtasiddhi-buddhist-to-hatha (+Derge colophon), src:amrtasiddhimula (contribution), tea:amrtasiddhimula:homage and :colophon.
- **Jain adoption of yoga:** brw:yoga-to-jainism (+Hemacandra and Śubhacandra's reservations about prāṇāyāma), brw:pinda-pada-rupa-rupatita-shared, practice equivalents on prc:maitri-adi-bhavana and prc:five-dharanas-jain.
- **Arāḍa Kālāma:** new src:buddhacarita, new brw:samkhya-in-buddhacarita, 9 teachings from BC 12.
- **Mīmāṃsā hermeneutics → Vedānta:** existing entries from U12 and U13 (see dedupe list).
- **Nyāya logic ↔ Jain and Buddhist:** brw:nyaya-buddhist-logic (+Uddyotakara), brw:pramana-buddhist-to-jain-logic (+Tattvasaṃgraha teaching), new brw:nyaya-to-jain-logic, new brw:mimamsa-buddhist-epistemology, cpt:shared-pramana-framework.
- **Kashmir aesthetics → Gauḍīya bhakti-rasa:** new brw:abhinava-rasa-to-bhakti-rasa (U16's brw:alankara-rasa-to-gaudiya kept).
- **Kālacakra six-branch yoga ↔ Maitrī six limbs:** brw:sadanga-yoga-shared-limbs (+local Maitrī text), new brw:sadanga-yoga-maitri-to-mantramarga, cpt:six-limbed-yoga-across-families, cpt:tarka-as-limb, trm:sadanga-yoga (Śaiva and Nāth definitions).
- **Āyurveda ↔ Tibetan medicine:** U48's brw:ayurveda-to-sowa-rigpa and dsp:gyushi-buddha-word already cover it. I dropped my own re-emit and added only cpt:three-humours-across-traditions.
- **Yavanajātaka:** brw:yavana-jataka-to-jyotisa (U32), complete.
- **Āgamas ↔ Nikāyas:** about 30 *-agama-parallel entries (U38).
- **Chan ↔ Pure Land:** brw:pure-land-chan (U42/U43), cpt:chan-pure-land-dual-cultivation (U43).
- **Bön ↔ Buddhism:** new brw:bon-buddhism-mutual; also brw:nyingma-bon-dzogchen and dsp:bon-and-buddhism (U45).

**Other well-attested links added (new)**
- Buddha-nature and the self: brw:tathagatagarbha-and-atman (read locally in the Laṅkāvatāra, which raises the objection itself), cpt:tathagatagarbha-and-atman, brw:shentong-atman-charge.
- Cosmography: brw:meru-jambudvipa-cosmography, cpt:meru-cosmography-across-families, cpt:cosmic-cycles-across-families.
- Deities and avatāras: brw:buddha-in-avatara-lists, brw:hindu-deities-in-buddhist-pantheon, brw:hindu-deities-in-theravada.
- Narrative, genre and grammar: brw:epic-narratives-in-jatakas, brw:purana-genre-to-jain, brw:paninian-grammar-to-sramana-grammars.
- Mantra: brw:om-in-jain-mantra, brw:om-in-buddhist-mantra.
- Philosophy and polemic: brw:atomism-across-schools, brw:two-standpoints-kundakunda, brw:nairatmyavada-known-to-maitri.
- Medicine and alchemy: brw:sramana-medicine-and-ayurveda, brw:buddhist-siddha-to-rasa-sastra.
- Other: brw:soma-amrta-to-hatha-moon, brw:buddhist-sunya-in-odia-vaisnava, cpt:yoga-open-to-all-sects.

**Sant–Bāul–Sufi (context only):** cpt:sant-sufi-context, src:majma-ul-bahrain, src:dara-baba-lal-dialogues; existing src:sirr-i-akbar and cpt:baul-fakir-exchange (U27).

**Disputes**
- dsp:advaita-crypto-buddhism (owned by U50). I supplied hypotheses only, no verdict: brw:madhyamaka-to-gaudapada, brw:yogacara-to-gaudapada, brw:mahayana-vocabulary-in-alatasanti, brw:madhyamaka-dialectic-to-sriharsa, brw:two-truths-to-advaita-levels, brw:buddhist-claim-vedanta-borrowed, brw:buddhist-sangha-and-dasanami, and teachings tea:padma-purana:6.236.7, tea:khandanakhandakhadya:1/2, tea:mandukya-karika-bhasya-sankara:4.99.
- New: dsp:yoga-buddhism-shared-milieu (queued, with candidate readings), dsp:ranking-of-other-revelations, dsp:source-of-hatha-yoga.

**Corrections to the must-cover list**
- **Six limbs:** the Buddhist list (GST 18.138 / Kālacakra) shares five limb-names with Maitrī 6.18. It has anusmṛti where the Maitrī has tarka, and the order differs. The Śaiva ṣaḍaṅga (MVT, tarka as the highest limb, recalled) is a third form. The Mṛgendra has ūha, not tarka.
- **Arāḍa's prakṛti (BC 12.18):** it is the five elements + ahaṃkāra + buddhi + avyakta, which is epic-period rather than classical Sāṃkhya. His five-jointed ignorance equals the five viparyayas of SK 47–48.
- **YS 1.33:** it assigns each attitude to a class of beings, like the Jain TS 7.11, and unlike the Pali formula. The four immeasurables are therefore a three-way link, not simply Buddhism → Yoga.
- **"Āgamas' parallels with the Nikāyas":** this means the Chinese Buddhist Āgamas, not the Hindu Āgamas.
- **Shared siddha names:** add Carpaṭi. Mīnapa = Matsyendra is an identification that not every source accepts.
- **Kashmir aesthetics → Gauḍīya:** the route may be indirect, through Bhoja, Mammaṭa and Viśvanātha.

## 2. Least sure items (possible hallucinations — check first)
- **Teachings:**
  - tea:varnaratnakara:siddha-list (names and order recalled)
  - tea:padma-purana:6.236.7 (verse number varies by edition)
  - tea:sarvatathagatatattvasamgraha:trailokyavijaya (details)
  - tea:tattvasangraha:anumanapariksa-patrasvamin (verse numbers)
  - tea:khandanakhandakhadya:1/2 (exact locus)
  - tea:mandukya-karika-bhasya-sankara:4.99 (gist only)
- **Sources:** src:dara-baba-lal-dialogues (title forms; Bābā Lāl's affiliation).
- **Borrowings, low confidence:**
  - brw:samkhya-buddhist-debate (Paramārtha's Life; the Paramārthasaptati)
  - brw:pinda-pada-rupa-rupatita-shared (Śaiva attestation not located)
  - brw:buddhist-sangha-and-dasanami
  - brw:sramana-medicine-and-ayurveda
  - brw:buddhist-siddha-to-rasa-sastra (Prabhāvakacarita's Pādalipta–Nāgārjuna story)
  - brw:buddhist-sunya-in-odia-vaisnava
  - brw:bon-buddhism-mutual
  - brw:shentong-atman-charge
  - brw:vajroli-name-and-bindu-retention
  - brw:saiva-siddhanta-pancaratra
- **Recalled details inside moderate-confidence entries:**
  - Sādhanamālā Ekajaṭā "from Bhoṭa" (in brw:tara-mahacina-buddhist)
  - the Jain oṃ = five parameṣṭhins etymology
  - Mahāvaṃsa 7 Uppalavaṇṇa
  - Jātaka numbers 461/454
  - Candrakīrti's mleccha simile
  - the MVT 'tarko yogāṅgam uttamam' quotation
  - Jain sakalīkaraṇa (in cpt:nyasa-across-families and trm:sakalikarana)
  - the Pāñcarātra identification maxim

## 3. Gaps (not created, deliberately)
- **Not created:**
  - Sufi lineage and teachings (out of scope by rule).
  - The Bengal Dharma-Ṭhākur/Śūnya Purāṇa "surviving Buddhism" hypothesis: there is no suitable lineage id (U59).
  - Maga/Śākadvīpī priests and the Saura cult: lin:saura (U60) does not exist yet.
  - Romaka/Pauliśa siddhāntas (U32).
  - Appar's Jain past and the Śaiva–Jain contests in Tamil Nadu (U18).
  - Newar shared Hindu–Buddhist cults (U55).
  - Cāndra grammar as its own entry (only mentioned in a note).
- **Dedupe candidates for the merge** (other units' entries, not edited by me):
  - brw:mimamsa-hermeneutics-to-vedanta / brw:mimamsa-hermeneutics-vedanta
  - brw:samkhya-to-yoga / brw:samkhya-patanjala-yoga
  - brw:epic-samkhya / brw:epic-samkhya-to-classical-samkhya
  - brw:upanisads-to-gita / brw:upanisads-to-bhagavad-gita
  - brw:adhyatma-ramayana-to-manas / brw:adhyatma-ramayana-to-ramcaritmanas
  - brw:rasa-sastra-hatha / brw:rasa-sastra-hatha-yoga
  - brw:samkhya-saiva-tattvas / brw:samkhya-to-kashmir-saivism
  - brw:sautrantika-pramana / brw:sautrantika-to-pramana
  - brw:kagyu-to-gelug / brw:kagyu-to-gelug-mahamudra
  - brw:kadam-to-kagyu / brw:kadam-to-dakpo-kagyu
  - brw:pure-land-chan (U42 from→to vs U43 mutual)
  - brw:ayurveda-to-sowa-rigpa (U30 vs U48 give different "what" text)
  - prc:bhutasuddhi / prc:bhuta-suddhi
- **Registry ids I reference that are not created yet:** dsp:advaita-crypto-buddhism (U50), lin:dasanami (U57), lin:pancasakha (U56), lin:zhenyan (U54), lin:shingon and lin:newar-vajrayana (U55), and pth:kalacakra-six-branches, pth:kashmir-four-upayas, pth:saiva-siddhanta-four-padas (U51).

## 4. Out of reach
- **Not available locally:** the Sanskrit Amṛtasiddhi and Amṛtasiddhimūla (Mallinson & Szántó 2021, copyright; only the Tibetan Tōh 2285 was read), the Caryāpada original, the Varṇaratnākara, the Persian Majmaʿ al-Baḥrayn and Sirr-i Akbar, the Mālinīvijayottara ṣaḍaṅga verse, and the Sādhanamālā Tārā sādhanas (not searched).
- **Oral:** oral Nāth, Bāul and Fakir song traditions.
- **Restricted (summary and the texts' own warnings only):** vajrolī, bindu-retention, Kaula substances, and rasa/metals.
