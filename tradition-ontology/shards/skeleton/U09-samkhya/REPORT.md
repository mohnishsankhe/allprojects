# U09-samkhya — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Method.** Entries come from model knowledge. Verse and sūtra numbers and wording were checked read-only against the local e-texts in `sources_raw/`: the SK (Ruzsa's edition with variants; Gauḍapāda; Māṭhara; Jayamaṅgalā; Yuktidīpikā), the Sāṃkhya Sūtra (Sansknet e-text), the Tattvasamāsa and its commentaries, the Tattvakaumudī (DCS, SK 1–15 only), the Yoga Bhāṣya fragments, the Sāṃkhyasāra, and the BS with Śaṅkara. `original` is given only where the wording was checked. Everything stays at level `skeleton`.

## Corrections to the task's list
1. **SK 1** says only "the three sufferings". The names ādhyātmika, ādhibhautika and ādhidaivika come from the commentaries.
2. **The fifty categories of the creation of cognitions are SK 46–51, not 44–51.** SK 44–45 give the results of the eight dispositions (bhāvas).
3. **SK 23** calls the eight "forms" (rūpa) of buddhi: four sāttvika and their tāmasa reverse. The word bhāva appears in SK 40, 43, 52 and 63.
4. **Closing verses and verse count:**
   - SK 69 is about the supreme sage; 70–71 give the lineage; 72 is about the Ṣaṣṭitantra.
   - The vulgate has 72 verses. Gauḍapāda comments only on 1–69.
   - Paramārtha's Chinese version lacks v.63, and its commentary says v.72 is not original.
   - A v.73 appears only in the Māṭhara Vṛtti and V1.
5. **Jaigīṣavya** is attested through the Yoga Bhāṣya (on YS 2.55 and 3.18) and the Mahābhārata, not in the SK commentaries' teacher lists. He is recorded under both Sāṃkhya and Yoga.
6. **BS 2.2.1–10** use Śaṅkara's division. The bare GRETIL BS text merges 2.2.1–2 and shifts the later numbers.
7. **Sāṃkhya Sūtra refs** follow the Sansknet e-text (526 sūtras). The Veda sūtra there is 5.45, not 5.46.
8. **Attributions:**
   - The Jayamaṅgalā's colophon ascribes it to Śaṅkara, pupil of Govinda. Recorded as doubtful under tch:sankara.
   - The Yuktidīpikā's colophon names Vācaspati. Recorded as doubtful.
9. **Gauḍapāda:** I used the registry id tch:gaudapada with attribution "disputed", as the registry requires. I suggest splitting it as tch:gaudapada-samkhya if the merge keeps the two persons apart.
10. **Paramārtha's translation** is filed as src:jin-qishi-lun under the pinyin rule. "Suvarṇasaptati" is recorded as a reconstructed alt title.

## 1. Coverage checklist (A5 Sāṃkhya)

**Teachers**
- Kapila: tch:kapila
- Āsuri: tch:asuri
- Pañcaśikha: tch:pancasikha
- Vārṣagaṇya: tch:varsaganya
- Vindhyavāsin: tch:vindhyavasin
- Jaigīṣavya: tch:jaigisavya
- Īśvarakṛṣṇa: tch:isvarakrsna
- Gauḍapāda: tch:gaudapada
- Māṭhara: tch:mathara
- Vācaspati Miśra: tch:vacaspati-misra
- Aniruddha: tch:aniruddha-samkhya
- Vijñānabhikṣu: tch:vijnanabhiksu
- Mahādeva Vedāntin: tch:mahadeva-vedantin
- Paramārtha: tch:paramartha, src:jin-qishi-lun
- Added from the texts: Pañcādhikaraṇa, Paurika, the Sāṃkhya Patañjali, Hārīta, Vāddhali, Kairāta, Ṛṣabheśvara, Kauṇḍinya, Mūka, Bhārgava, Ulūka, Vālmīki, Devala, Voḍhu, Sanandana, Buddhamitra, Bhāvāgaṇeśa and the later authors
- Recent: Hariharānanda Āraṇya, Dharmamegha Āraṇya

**Texts**
- SK: src:samkhya-karika, with 73 verse teachings tea:samkhya-karika:1–73
- Commentaries on the SK: src:samkhya-karika-bhasya-gaudapada, src:mathara-vrtti, src:yuktidipika, src:jayamangala, src:tattvakaumudi, src:samkhya-saptati-vrtti (V1), src:samkhya-vrtti (V2)
- Sāṃkhya Sūtra: src:samkhya-sutra. Its attribution is recorded as the tradition's account (Kapila) against the scholarly date (14th–15th c.).
- Commentaries on the SS: src:samkhya-sutra-vrtti-aniruddha, src:samkhya-pravacana-bhasya, src:samkhya-sutra-vrttisara
- Tattvasamāsa and its commentaries: src:tattvasamasa and five commentaries
- Ṣaṣṭitantra (lost) and its sixty topics: src:sastitantra, cpt:sastitantra-sixty-topics
- Also: src:samkhyasara, src:pancasikha-sutra, src:rajavarttika-samkhya

**The 25 principles and the order of emergence:** cpt:twenty-five-tattvas (members listed), cpt:samkhya-order-of-emergence. Terms exist for every principle: trm:purusa, trm:prakrti, trm:mahat / trm:buddhi, trm:ahamkara, trm:manas, trm:buddhindriya, trm:karmendriya, trm:tanmatra, trm:mahabhuta.

**SK teachings asked for:** all verses 1–72 (+73) are tea:samkhya-karika:N.

**Concepts**
- Satkāryavāda: cpt:satkaryavada
- The guṇas: cpt:three-gunas
- The three sufferings: cpt:three-kinds-of-suffering
- Viveka-khyāti: cpt:viveka-khyati
- Plurality of puruṣas: cpt:plurality-of-purusas
- Īśvara, classical vs theistic: cpt:isvara, cpt:theistic-samkhya
- Liṅga-śarīra: cpt:linga-sarira
- The eight bhāvas: cpt:eight-bhavas
- Kaivalya: cpt:kaivalya
- Early Sāṃkhya (points to U05 and U30): cpt:early-samkhya
- Section-D items: cpt:pramana, cpt:thirteen-instruments, cpt:antahkarana, cpt:five-vayus, cpt:pratyaya-sarga, cpt:prakrtilaya, cpt:jivanmukti, cpt:videhamukti, cpt:death-in-samkhya, cpt:samkhya-on-sound-and-veda, cpt:dharma-in-samkhya, cpt:teacher-in-samkhya, cpt:reflection-of-purusa-in-buddhi, cpt:states-of-consciousness-samkhya, cpt:aisvarya-eight-powers

**Disputes**
- Referenced, owned by U50: dsp:causation, dsp:isvara, dsp:number-of-pramanas, dsp:status-of-veda, dsp:works-knowledge-grace, dsp:world-real-or-appearance, dsp:is-there-a-self
- New, owned here:
  - Sāṃkhya vs Vedānta: dsp:is-pradhana-taught-in-sruti (BS 1.1.5, 1.4.1, 1.4.11, 2.1.1) and dsp:can-unconscious-pradhana-create (BS 2.2.1–10)
  - Sāṃkhya vs Buddhists: dsp:existence-of-pradhana (includes the Vindhyavāsa–Buddhamitra debate) and dsp:are-things-momentary
  - Sāṃkhya vs Advaita: dsp:one-or-many-purusas (partially reconciled under P2 via SS 1.154)
  - Sāṃkhya vs Mīmāṃsā: dsp:does-sacrificial-killing-incur-demerit
  - Sāṃkhya vs Nyāya: dsp:are-the-senses-elemental
  - Sāṃkhya vs Cārvāka: dsp:consciousness-from-elements
  - Against rival schools generally: dsp:khyativada, dsp:nature-of-liberation
  - Debates among Sāṃkhya teachers: dsp:number-of-instruments-samkhya, dsp:is-there-a-subtle-body, dsp:one-prakrti-or-many, dsp:cause-of-purusa-prakrti-relation, dsp:isvara-within-samkhya

**Ultimate:** ult:samkhya, with tradition_denies_single_ultimate = true.

**Path maps:** pth:samkhya-karika-path, pth:samkhya-sutra-path.

## 2. Least sure — check these first
- **Recalled titles and authors:** src:laghu-samkhya-sutra-vrtti (Nāgeśa), src:samkhyataruvasanta (Muḍumba Narasiṃhasvāmin), src:vidvattosini (Bālarāma Udāsīna), src:samkhyacandrika (Nārāyaṇa Tīrtha), tch:dharmamegha-aranya, and the Kāpil Maṭh details under tch:hariharananda-aranya.
- **Tattvakaumudī beyond SK 15 (from memory):** tea:tattvakaumudi:51 (the order of the siddhis; dāna read as purification) and tea:tattvakaumudi:72 (the Rājavārttika quotation).
- **Vijñānabhikṣu:** his reading of SS 1.92 as a concessive argument (prauḍhivāda), and his mutual-reflection theory.
- **Aniruddha:** his non-theistic stance.
- **Other recalled details:**
  - Kumārila's report on Vindhyavāsin.
  - The Chinese Life of Vasubandhu's details (Ayodhyā, Buddhamitra, the Paramārthasaptati).
  - Jin qishi lun as T2137 in three fascicles.
  - Ahirbudhnya Saṃhitā ch.12.
  - The Mahābhārata chapter refs.
  - Śabara on MS 1.1.2.
  - NS 1.1.22 and TS 10.5 as cited in disputes.
- **Other entries:** the Chinese and Tibetan cross-language forms, the lineage assigned to tch:buddhamitra, and the reading of tch:vaddhali's name.
- **External ids I referenced:** src:tattvasangraha-santaraksita is not in the registry. I also referenced cpt:thirty-six-tattvas, cpt:three-bodies, cpt:vivartavada, cpt:asatkaryavada, obs:five-klesas, prc:sravana, prc:manana, prc:nididhyasana and trm:klesa, expecting other units to create them. Please check they exist after the merge.

## 3. Gaps — not created responsibly
- **No teaching entries for passages owned by other units:**
  - Early Sāṃkhya passages in the Mahābhārata (U05), Caraka and Suśruta Śārīrasthāna 1 (U30), and the Upaniṣads (U03).
  - The Buddhacarita 12 report of Arāḍa's teaching (no owner for src:buddhacarita).
  - The Yoga Bhāṣya fragments of Pañcaśikha, Vārṣagaṇya and Jaigīṣavya (U10's source).
- **Buddhist and Jain critiques are only sketched:** Madhyamakahṛdaya ch.6, Tattvasaṅgraha ch.1, Dignāga's critique of Vārṣagaṇya's definition of perception, the Nayacakra fragments, Guṇaratna's list of Sāṃkhya works.
- **Vācaspati's sequence of the siddhis** is not made into a path map, because it is unverified.
- **Kāpil Maṭh** is not a separate lineage; it is covered through its teachers only.
- **Not available locally:** the full Tattvakaumudī, the Sāṃkhyapravacanabhāṣya, Aniruddha's vṛtti, and the Chinese text of the Jin qishi lun.

## 4. Out of reach
- **Lost works:** the Ṣaṣṭitantra, the Rājavārttika, the works of Vārṣagaṇya, Vindhyavāsin, Pañcādhikaraṇa and Paurika (known only through quotations and reports), and Vasubandhu's Paramārthasaptati.
- **Oral teaching:** the oral instruction of the Kāpil Maṭh.
