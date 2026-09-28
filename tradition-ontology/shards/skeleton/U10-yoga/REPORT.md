# U10-yoga — Phase B skeleton report (Pātañjala Yoga, coverage map A5)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Owner of `lin:patanjala-yoga` and `ult:patanjala-yoga`. Generators in `_gen/` (`part1` … `part12`, shared `common.py`, sūtra text in `ys_text.py`); re-run in order from `tradition-ontology/`.

**Counts:** lineages 1 · sources 19 · teachers 18 · teachings 335 (Yoga Sūtra 195 = every sūtra; Yogabhāṣya 120; later commentaries 20) · terms 204 · concepts 72 · practices 34 (2 restricted) · obstacles 27 · path maps 6 · phenomenology 61 · disputes 9 · borrowings 16 · ultimate view 1 · interpretation_log 22.
**Validator:** 0 errors; the only warning is that this REPORT.md is missing.

**Method note.** This is still a skeleton. But I checked the sūtra numbering and wording, and every Vyāsa passage used, against the local GRETIL e-text of the Ānandāśrama edition (`sources_raw/dcs/corpus/GRETIL/sa_pataJjali-yogasUtra-with-bhASya.txt`). I also read the passages cited from the Rājamārtaṇḍa, Yogavārttika, Yogamaṇiprabhā, Nāgeśa, Padacandrikā, Yogasiddhāntacandrikā, Sūtrārthabodhinī and Bhāvāgaṇeśa in `sources_raw/raw_etexts`. Because the ref and wording of each sūtra were checked, the sūtra teachings carry `original` (IAST, with edition and licence) and `confidence: high`. All paraphrases are mine and have not been fidelity-checked. Every entry stays at level `skeleton`.

## Corrections to the task's MUST-COVER list
- **Sūtra count.** The vulgate (Ānandāśrama ed. and all nine local commentary e-texts) has **195 sūtras = 51 + 55 + 55 + 34**. Some editions reach **196** because they count "etena śabdādy antardhānam uktam" as sūtra 3.22; in the Ānandāśrama text this line is bhāṣya on 3.21. This unit uses the 195 numbering; the variant is recorded on `src:yoga-sutra`, `tea:yoga-sutra:3.21` and `tea:yoga-bhasya:3.21`.
- **YS 4.16 is absent from Bhoja's Rājamārtaṇḍa.** The local e-text has an editorial note to this effect, recorded in `tea:yoga-sutra:4.16` and `tea:rajamartanda:4.16`.
- **Anantadeva's commentary is titled *Padacandrikā*.** The colophon reads "kṛteyaṃ padacandrikā" and the opening "sūtrārthacandrikā", not just "Candrikā". Id: `src:padacandrika-anantadeva`.
- **Rāmānanda Sarasvatī's work is the *Yogamaṇiprabhā*.** The colophon names him a pupil of Govindānanda.
- **"Nāgojī Bhaṭṭa" = Nāgeśa Bhaṭṭa.** Id `tch:nagesa-bhatta`, to match the grammarian (U31).
- **"Sadāśivendra" = Sadāśiva Brahmendra.** Id `tch:sadasiva-brahmendra`.
- **Source of the Hiraṇyagarbha verse.** Vijñānabhikṣu (YV 1.1, checked locally) attributes "hiraṇyagarbho yogasya vaktā nānyaḥ purātanaḥ" to the **Yoga-Yājñavalkya**. I recall Vācaspati ascribing it to the Yājñavalkya-smṛti (TV 1.1, not checked).
- **Kinds of karma (4.7).** The sūtra says "neither white nor black for the yogin, threefold for others"; the four named classes (catuṣpadī karmajāti) are Vyāsa's.

## (1) Checklist — coverage-map A5 (Yoga) and task items → ids
- **Texts**
  - Yoga Sūtra, four pādas: `src:yoga-sutra`, `tea:yoga-sutra:1.1` … `4.34` (all 195).
  - Vyāsa's bhāṣya: `src:yoga-bhasya`, 120 `tea:yoga-bhasya:*`. The Pātañjalayogaśāstra hypothesis (Maas; Bronkhorst) is recorded as `attribution.scholarly` on both sources.
  - Commentaries:
    - `src:tattvavaisaradi` (+`tea:tattvavaisaradi:1.1`)
    - `src:rajamartanda` (+5 teachings)
    - `src:yogavarttika` (+5)
    - `src:yogasarasangraha`
    - `src:yoga-sutra-bhasya-vivarana` (ascription to Śaṅkara disputed)
    - `src:yogasutravrtti-nagesa` (+2)
    - `src:yogamaniprabha` (+1)
    - `src:padacandrika-anantadeva` (+1)
    - `src:yogasudhakara`
  - Other works added: `src:yogasiddhantacandrika` and `src:sutrarthabodhini` (Nārāyaṇatīrtha), `src:yogasutradipika-bhavaganesa`, `src:bhasvati` (recent), `src:patanjala-rahasya`, `src:yogavalli` (recent), `src:dharma-patanjala` (Old Javanese).
  - Arabic translation: `src:kitab-patanjal`, dated c. 1017–1030, translator `tch:al-biruni`.
- **Teachers**
  - Founder `tch:hiranyagarbha`; `tch:patanjali`, `tch:vyasa`, `tch:vacaspati-misra`, `tch:bhoja`, `tch:vijnanabhiksu`.
  - `tch:sankara`: Yoga contribution only.
  - `tch:nagesa-bhatta`, `tch:ramananda-sarasvati`, `tch:anantadeva-padacandrika`, `tch:sadasiva-brahmendra`, `tch:narayanatirtha`, `tch:bhavaganesa`, `tch:hariharananda-aranya` (recent), `tch:raghavananda-sarasvati`.
  - Figures named in the bhāṣya: `tch:jaigisavya`, `tch:avatya`.
- **Lineage and ultimate:** `lin:patanjala-yoga`, `ult:patanjala-yoga` (`tradition_denies_single_ultimate: true`, with caveat).
- **Mind**
  - citta and its five vṛttis (pramāṇa, viparyaya, vikalpa, nidrā, smṛti): `cpt:citta`, `cpt:five-vrttis`, `cpt:pramana`, `cpt:deep-sleep`; terms `trm:vrtti`, `trm:pramana`, `trm:viparyaya`, `trm:vikalpa`, `trm:nidra`, `trm:smrti`; YS 1.5–11.
  - abhyāsa and vairāgya (lower and higher): `cpt:abhyasa-vairagya`, `cpt:vairagya`, `prc:abhyasa`, `prc:vairagya`, `pth:vacaspati-four-stages-of-vairagya`; YS 1.12–16.
  - Vyāsa's five bhūmis of citta: `cpt:citta-bhumis`, `trm:ksipta` … `trm:niruddha`, `obs:ksipta-mudha-viksipta`, `tea:yoga-bhasya:1.1`.
  - Saṃskāra and vāsanā: `cpt:samskara`, `cpt:vasana` (1.5, 1.50, 3.9, 4.8–11).
- **Īśvara and Oṃ**
  - Īśvara as special puruṣa (1.24–26): `cpt:isvara`, `trm:isvara`, `trm:purusa-visesa`.
  - Oṃ (1.27–28): `cpt:pranava`, `prc:pranava-japa`.
  - Devotion to Īśvara: `prc:isvara-pranidhana`.
- **Obstacles and remedies**
  - The nine obstacles (1.30): `obs:nine-antarayas` plus one obs: entry and one term each.
  - The five accompaniments (1.31): `obs:viksepa-sahabhuva`.
  - The four attitudes (1.33): `cpt:four-attitudes`, `prc:four-attitudes`.
  - Other methods (1.34–39): `prc:pracchardana-vidharana`, `prc:visayavati-pravrtti`, `prc:visoka-jyotismati`, `prc:vitaraga-visaya-citta`, `prc:svapna-nidra-jnana-alambana`, `prc:yathabhimata-dhyana`, `prc:ekatattva-abhyasa`.
- **Samādhi**
  - Samāpattis (1.41–44): `cpt:samapatti`, `trm:savitarka`, `trm:nirvitarka`, `trm:savicara`, `trm:nirvicara`.
  - Ṛtambharā prajñā: `cpt:rtambhara-prajna`.
  - Samprajñāta and asamprajñāta: `cpt:samprajnata-samadhi`, `cpt:asamprajnata-samadhi`.
  - Sabīja and nirbīja: `cpt:sabija-nirbija`.
  - Ladders: `pth:rajamartanda-samadhi-ladder`; `pth:yoga-sutra-samadhi-ladder` is referenced only (U51 owns it).
  - Upāya- and bhava-pratyaya: `cpt:upaya-bhava-pratyaya`, `cpt:videha-prakrtilaya`.
  - Graded practitioners: `cpt:grades-of-practitioners`.
  - Five means (1.20): `cpt:sraddha-virya-smrti-samadhi-prajna`, `pth:yoga-sutra-five-means`.
- **Afflictions and karma**
  - Kriyā-yoga (2.1): `cpt:kriya-yoga`, `prc:kriya-yoga`, `prc:tapas` (restricted), `prc:svadhyaya`.
  - Five kleśas (2.3–9) and their states (2.4, plus Vyāsa's "burnt seed"): `cpt:five-klesas`, `cpt:four-states-of-klesas`, `obs:five-klesas`, `obs:avidya`, `obs:asmita`, `obs:raga`, `obs:dvesa`, `obs:abhinivesa`; terms `trm:prasupta`, `trm:tanu`, `trm:vicchinna`, `trm:udara`, `trm:dagdha-bija`.
  - Karmāśaya: `cpt:karmasaya`, `cpt:vipaka-jati-ayus-bhoga`.
  - Four kinds of karma (4.7): `cpt:four-kinds-of-karma`, `trm:asuklakrsna`.
  - Everything as suffering for the discerning (2.15): `cpt:duhkha-for-the-discerning`.
  - Heya / heya-hetu / hāna / hānopāya: `cpt:caturvyuha`.
  - Seer and seen: `cpt:seer-and-seen`, `cpt:purusa`, `cpt:prakrti`, `cpt:three-gunas`, `cpt:guna-parvan`, `cpt:samyoga`, `cpt:plurality-of-purusas`, `cpt:purpose-of-prakrti`, `cpt:witness`, `cpt:asmita`.
  - Discrimination: `cpt:viveka-khyati`, `cpt:sevenfold-prajna`, `pth:yoga-sutra-sevenfold-prajna`.
- **The eight limbs (2.29–3.3)**
  - `cpt:astanga-yoga`; the path map `pth:yoga-sutra-eight-limbs` is referenced only (U51 owns it).
  - Yamas: `cpt:yamas`, `prc:yama`, `prc:ahimsa`, `prc:satya`, `prc:asteya`, `prc:brahmacarya`, `prc:aparigraha`.
  - Niyamas: `cpt:niyamas`, `prc:niyama`, `prc:sauca`, `prc:santosa`, `prc:tapas`, `prc:svadhyaya`, `prc:isvara-pranidhana`.
  - Fruits of each (2.35–45): `cpt:signs-of-yama-niyama` and ten phn: signs.
  - Pratipakṣa-bhāvana (2.33–34): `cpt:pratipaksa-bhavana`, `prc:pratipaksa-bhavana`, `obs:vitarka-himsadi`, `obs:lobha-krodha-moha`.
  - Āsana (2.46–48): `prc:asana`, with Vyāsa's list.
  - Prāṇāyāma (2.49–53): `prc:pranayama`, `prc:caturtha-pranayama` (restricted).
  - Pratyāhāra (2.54–55): `prc:pratyahara`.
  - Dhāraṇā, dhyāna, samādhi: `prc:dharana`, `prc:dhyana`, `prc:samadhi`.
- **Saṃyama and transformations**
  - Saṃyama (3.4–6): `cpt:samyama`, `prc:samyama`; inner and outer limbs: `cpt:antaranga-bahiranga`.
  - Three transformations (3.9–12): `cpt:three-parinamas-of-citta`.
  - 3.13 (dharma, lakṣaṇa, avasthā): `cpt:dharma-laksana-avastha-parinama`, `cpt:dharma-dharmin`.
  - Time: `cpt:ksana-krama`, `cpt:existence-of-past-and-future`.
- **Powers**
  - Every power of pāda 3 has a phn: entry (35) plus its sūtra teaching; overview in `cpt:vibhutis`.
  - Also `cpt:anima-adi-siddhis`, `cpt:omniscience-in-yoga`, `cpt:nirmana-citta`.
  - Warnings (3.37, 3.51): `cpt:siddhis-as-obstacles`, `obs:siddhis-as-upasarga`, `obs:sanga-smaya`, `phn:ys-celestial-invitation`, `tea:yoga-bhasya:3.51`, `pth:vyasa-four-yogins`.
  - Five sources of powers (4.1): `cpt:five-sources-of-siddhis`.
- **Culmination**
  - Cloud of dharma (4.29): `cpt:dharmamegha-samadhi`.
  - Kaivalya (3.55, 4.34): `cpt:kaivalya`, `cpt:jivanmukti` (YBh 4.30), `pth:yoga-sutra-kaivalya-sequence`.
- **Other D-checklist items for this lineage**
  - Body and energy: `cpt:prana-vayus-yoga`, `cpt:bodily-loci-of-samyama`.
  - Cosmology: `cpt:yoga-cosmology-vyasa`.
  - Sound and language: `cpt:word-meaning-cognition`, `cpt:pranava`.
  - Death: `cpt:death-in-yoga` (abhiniveśa, omens, utkrānti).
  - Teacher and transmission: `cpt:isvara-as-first-teacher` (YBh 3.6 "yoga itself is the teacher").
  - Mind as not self-luminous; objects not mind-dependent: `cpt:citta-not-self-luminous`, `cpt:object-independent-of-mind`.
- **Disputes**
  - `dsp:isvara` (U50) is referenced; the narrower `dsp:yoga-samkhya-isvara` is partially reconciled (P3/P5, with objections recorded).
  - Commentators' differences, both queued: `dsp:reflection-single-or-mutual` (Vācaspati vs Vijñānabhikṣu, YV 1.7) and `dsp:objects-of-samprajnata` (Vācaspati vs Bhoja vs Vijñānabhikṣu).
  - `dsp:vedanta-on-yoga-smrti` (BS 2.1.3): partially reconciled, P3.
  - Anti-Buddhist debates of the bhāṣya, all queued: `dsp:object-independent-of-mind`, `dsp:is-mind-self-luminous`, `dsp:citta-momentary-or-enduring`.
  - Debates internal to the bhāṣya: `dsp:size-of-citta` (queued) and `dsp:mastery-of-the-senses` (reconciled, P4).
  - Also referenced (U50 owns them): `dsp:number-of-pramanas`, `dsp:causation`, `dsp:souls-one-or-distinct`, `dsp:is-there-a-self`.
- **Borrowings with Buddhism.** The kleśa theory, the four attitudes, the samāpatti vocabulary and dharmamegha are all recorded (`brw:buddhism-yoga-*`, `brw:mahayana-yoga-dharmamegha`). I also added:
  - the four inversions of 2.5;
  - the five faculties of 1.20;
  - Sarvāstivāda time theory;
  - the cosmology's deva classes;
  - verse parallels (YBh 1.47 ≈ Dhp 28; YBh 2.42 ≈ Udāna 2.2);
  - question types (YBh 4.33 ≈ AN 4.42);
  - the medical fourfold scheme.

  Each is marked `scholarly-hypothesis` / `disputed` where appropriate.
- **Other borrowings:** `brw:samkhya-to-yoga`, `brw:upanisadic-to-yoga`, `brw:epic-to-yoga`, `brw:yoga-to-hatha`, `brw:yoga-to-jainism`, `brw:yoga-to-advaita`.

## (2) Least sure — check these first
- **Recalled, not checked locally**
  - `tea:tattvavaisaradi:1.1` and every Vācaspati position quoted in the disputes. Only TV 4.1 is in the local corpus; his side of `dsp:reflection-single-or-mutual` rests partly on Vijñānabhikṣu's report.
  - `pth:vacaspati-four-stages-of-vairagya`, the stage names from TV 1.15 (confidence low).
- **Sources and teachers**
  - `src:patanjala-rahasya` / `tch:raghavananda-sarasvati` (low).
  - `src:dharma-patanjala`: the manuscript date of 1467 and the details (low).
  - `src:kitab-patanjal`: Arabic title, the Istanbul manuscript, Ritter 1956.
  - `src:yoga-sutra-bhasya-vivarana`: the scholars named and the 1952 first edition.
  - `src:yogasarasangraha`: contents not recalled.
  - Dates for Rāmānanda Sarasvatī, Nārāyaṇatīrtha, Bhāvāgaṇeśa and Sadāśiva Brahmendra (all low). Also Sadāśiva's teacher and other works, and whether Nārāyaṇatīrtha is the Kṛṣṇalīlātaraṅgiṇī composer (flagged in notes).
  - Nāgeśa's "Bṛhatī / Laghvī" vṛttis.
- **References recalled from memory**
  - Mahābhārata: Nārāyaṇīya c. 12.337 (Hiraṇyagarbha); the Sāṃkhya–Yoga contest c. 12.289 (CE).
  - Sāṃkhya Sūtra 1.92 and 5.2–12; Sāṃkhya Kārikā 57.
  - Buddhist refs in disputes and borrowings: Viṃśatikā 1–7, Pramāṇasamuccaya 1.9–12, AKBh 4.2–3, AKBh 5.25–26, AKBh on 6.3 (the eyeball simile), AN 4.49, AN 4.42.
  - HYP 1.1–2 and 4.3–4.
  - Jain details: Haribhadra naming Patañjali; Yaśovijaya's work on selected sūtras.
  - The attribution of the YBh 4.13 verse to the Ṣaṣṭitantra / Vārṣagaṇya.
- **Summaries of long passages** (faithful in outline, compressed): YBh 2.23 (eight views on adarśana), 2.24 (the paṇḍaka story), 3.17 (word as a unit), 3.26 (cosmology) and 3.51.
- **YSC intro. v.4.** The compound "svātantrya-satyatva-sukham" is ambiguous; the paraphrase is flagged.
- **Tags.** `level`, `standpoint` and `stage` are interpretive. Rule used: practice, ethics and cosmology are conventional; analysis of the seen is unmarked; the puruṣa's own form and kaivalya are ultimate.
- **Framing choice.** `obs:prakrtilaya-short-of-kaivalya` (confidence moderate): the sūtra only gives the cause of that state.

## (3) Gaps — belong here but not responsibly creatable
- The Vivaraṇa, the Tattvavaiśāradī (except 1.1), the Yogasārasaṅgraha, the Bhāsvatī, the Pātañjalarahasya, the Kitāb Pātanǧal and the Dharma Pātañjala have source entries but no teachings; they are not local or not recalled verse-exactly.
- Author and date of the Yogavallī (local e-text, Samādhipāda only).
- Other YS commentaries I could not name with confidence, so I created none.
- Who "the ācārya" and "the others" are in YBh 4.10; who the unnamed authorities quoted in the bhāṣya are (the commentators' Pañcaśikha attributions are only noted).
- Successors at the Kāpil Maṭh after Hariharānanda (recent).
- Persian or Mughal-era renderings of the YS: unknown.
- Kashmir Śaiva critique and adaptation of aṣṭāṅga yoga (Tantrāloka), for U19 / U49.
- **Ids owned or likely held by other units, referenced by slug guess:**
  - path maps `pth:yoga-sutra-eight-limbs`, `pth:yoga-sutra-samadhi-ladder` (U51);
  - equivalence targets `trm:atman`, `trm:ahamkara`, `trm:antahkarana`, `trm:moksa`, `trm:om`, `cpt:four-immeasurables`, `cpt:five-spiritual-faculties`, `cpt:jhana`, `prc:bhakti`, `prc:brahmavihara-bhavana`, `obs:klesa`, `obs:three-poisons`;
  - `tch:kapila`, `tch:asuri`, `tch:govindananda`;
  - `lin:pramana-buddhist`, `lin:yogacara`, `lin:sautrantika`, `lin:sarvastivada`, `lin:vedanta`.

  The merge or dedupe step should check these.
- **Scalar conflicts to expect at merge.** Shared teacher entries (`tch:sankara`, `tch:vyasa`, `tch:vacaspati-misra`, `tch:vijnanabhiksu`) carry only this unit's Yoga contribution. Their `summary` will conflict with the owning units' summaries at merge.

## (4) Out of reach
- The oral instruction of living Sāṃkhya-Yoga lineages (Kāpil Maṭh) and of modern yoga lineages.
- Undigitized manuscripts of minor YS commentaries.
- Copyrighted critical editions and translations (Maas 2006; Harimoto 2014; Leggett; Rukmani): references only.
- **Restricted (summary and the texts' own warnings only):**
  - `prc:tapas`: the fasting vows are named, not described.
  - `prc:caturtha-pranayama`: breath suspension, no method.
  - YBh 2.50's measurement "by number" is summarized without counts.

## Decisions taken (DECISIONS.md is outside this unit's write scope)
- **195-sūtra numbering** (Ānandāśrama). Refs follow it throughout.
- **U51 path maps and U50's `dsp:isvara`: referenced, not written.** New Yoga-specific maps and disputes use new ids.
- **Lineage `status: "living"`.** The commentarial school continues (Kāpil Maṭh; modern teaching).
- **`tch:al-biruni` is filed under `lin:patanjala-yoga`** only because the schema requires a lineage. His summary states he was not a member.
