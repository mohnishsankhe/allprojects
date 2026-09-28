# U08-agama-catalogue — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Scope:** coverage map A4 (Āgamas and tantras) and I2 (the Mantramārga as a division; Kerala tantra).
**Owned lineages:** lin:mantramarga, lin:pancaratra, lin:vaikhanasa, lin:kerala-tantra.
**New sub-lineages** (not in the registry; all with parent lin:mantramarga): lin:mantrapitha, lin:vidyapitha, lin:vama-srotas, lin:garuda-tantra, lin:bhuta-tantra.
**Counts:** lineages 9 · ultimate views 6 · sources 125 · teachers 33 · teachings 65 · terms 116 · concepts 52 · practices 29 · obstacles 7 · path maps 1 · phenomenology 3 · disputes 7 · borrowings 8 · interpretation-log lines 28.
**Validator:** 0 errors.

**Method.** Every entry is level `skeleton`, but the key catalogue passages were read in the local corpora under `sources_raw/`:
- Śaiva: Kāmika Pūrvabhāga, Kiraṇa vidyāpāda, Tantrāloka with Jayaratha's Viveka, Mṛgendra.
- Pāñcarātra: Ahirbudhnya, Lakṣmī Tantra, Jayākhya, Pādma, Āgamaprāmāṇya.
- Vaikhānasa: Kriyādhikāra, Bhṛgusaṃhitā, Daśavidhahetunirūpaṇa.
- Kerala and Śākta: Śāradātilaka, Nityāṣoḍaśikārṇava with the Setubandha, Saundaryalaharī with Lakṣmīdhara's commentary.
- The Muktabodha catalogue metadata.

Each entry that rests on one of these readings names the file in its `notes`. Devanāgarī `original` text is given only for verses copied from these e-texts.

## 1. Coverage checklist
- **28 Siddhānta Āgamas, one source each:**
  - Śivabheda: src:kamika-agama, yogaja-agama, cintya-agama, karana-agama, ajita-agama, dipta-agama, suksma-agama, sahasra-agama, amsumat-agama, suprabheda-agama.
  - Rudrabheda: src:vijaya-agama, nisvasatattvasamhita, svayambhuva-agama, agneya-agama, vira-agama, raurava-agama, makuta-agama, vimala-agama, candrajnana-agama, mukhabimba-agama, prodgita-agama, lalita-agama, siddha-agama, santana-agama, sarvokta-agama, paramesvara-agama, kirana-tantra, vatula-agama.
  - Also: cpt:twenty-eight-saiva-agamas; tea:kamika-agama:purva.1.30-92, tea:kirana-tantra:10.3-27, tea:tantraloka-viveka:1.18.
  - Each Āgama's first recipients, upabhedas (in `structure.upabhedas_kamika`) and the Kiraṇa/Śrīkaṇṭhīya variants are recorded.
- **Upāgamas and survivals:**
  - Concept: cpt:upagamas.
  - Upāgamas and related scriptures: src:mrgendra-tantra, matangaparamesvara, pauskara-agama, sarvajnanottara, kalottara, sardhatrisatikalottara, devikalottara-agama, nisvasakarika, diksottara, pingalamata.
  - Early scriptures outside the list: svayambhuvasutrasangraha, rauravasutrasangraha, parakhya-tantra.
  - Commentaries: mrgendravrtti, mrgendravrttidipika, kiranavrtti, matangavrtti, sardhatrisatikalottaravrtti, sarvajnanottaravrtti, svayambhuvasutrasangraha-vrtti, pauskarabhasya, pauskaravrtti.
  - Siddhānta paddhatis: somasambhupaddhati, kriyakramadyotika and 9 others.
- **Four pādas:** cpt:four-padas-of-agama, trm:pada-agama; tea:kamika-agama:purva.1.107-108, tea:kirana-tantra:1.12-13.
- **Niśvāsa (earliest surviving Śaiva tantra, with scholarly dating and the 2015 edition):** src:nisvasatattvasamhita plus its books nisvasamukha, nisvasa-mulasutra, -uttarasutra, -nayasutra, -guhyasutra.
- **Mantramārga vs Atimārga, as the texts draw it:** cpt:mantramarga-atimarga-division, cpt:fivefold-hierarchy-of-religion; tea:kamika-agama:purva.1.17-19, tea:nisvasamukha:1-4; brw:atimarga-to-mantramarga (lin:atimarga is referenced).
- **Streams and the Mantrapīṭha/Vidyāpīṭha division:** cpt:five-streams-of-revelation, cpt:mantrapitha-vidyapitha; trm:srotas, mantrapitha, vidyapitha, yamala, garuda-tantra, bhuta-tantra, vama-tantra; tea:kamika-agama:purva.1.20-27, tea:tantraloka-viveka:1.18/3.
- **64 Bhairava tantras:**
  - cpt:sixty-four-bhairava-tantras gives all members as quoted; also tea:tantraloka-viveka:1.18/2, tea:tantraloka:1.18 and src:srikanthiya-samhita.
  - Surviving members: src:svacchanda-tantra, brahmayamala, jayadrathayamala.
  - Related: src:netra-tantra, siddhayogesvarimata, tantrasadbhava, malinivijayottara-tantra, vinasikha-tantra, kriyakalagunottara.
- **Pāñcarātra saṃhitās (24 sources):**
  - The three gems: satvata-samhita, pauskara-samhita, jayakhya-samhita.
  - Others: ahirbudhnya-samhita, laksmi-tantra, paramesvara-samhita, isvara-samhita, padma-samhita, parama-samhita, visvaksena-samhita, sriprasna-samhita, naradiya-samhita, aniruddha-samhita, hayasirsa-pancaratra, visnu-samhita and others.
  - Three gems and the count of 108: cpt:ratnatraya-pancaratra, cpt:pancaratra-108-samhitas; tea:jayakhya-samhita:1.adhika.1-14.
- **Pāñcarātra theology:**
  - Concepts: cpt:five-forms-of-god-pancaratra, four-vyuhas, thirty-nine-vibhavas, six-gunas-of-bhagavan, laksmi-as-sakti, five-acts-pancaratra, pure-and-impure-creation.
  - Teachings: tea:ahirbudhnya-samhita:2.53-62, 5.16-19, 5.50-59; tea:laksmi-tantra:2.34-37, 12.12-14; tea:jayakhya-samhita:2.73-75.
- **Pāñcarātra practice:** prc:diksa, puja, pancakala, pancasamskara, saranagati; tea:ahirbudhnya-samhita:37.25-29, tea:laksmi-tantra:17.56-62.
- **Āgamaprāmāṇya (dispute record):**
  - src:agamapramanya; tea:agamapramanya:purvapaksa and :siddhanta; dsp:validity-of-pancaratra.
  - Related teachings: tea:brahma-sutra:2.2.42-45, brahma-sutra-bhasya-sankara:2.2.42-45, sribhasya:2.2.42-45, tantravarttika:1.3.4.
  - Also src:pancaratraraksa.
- **Vaikhānasa:**
  - Vikhanas and the four ṛṣis: tch:vikhanas, marici, atri, kasyapa, bhrgu; tea:kriyadhikara:1.1.
  - Sources (13): vaikhanasa-smartasutra, -dharmasutra, -srautasutra, -mantraprasna, vimanarcanakalpa, samurtarcanadhikarana, kasyapa-jnanakanda, kriyadhikara, khiladhikara, prakirnadhikara, bhrgu-samhita-vaikhanasa, dasavidhahetunirupana, tatparyacintamani.
  - Vedic character of the worship: cpt:niskala-sakala-vaikhanasa, vaikhanasa-five-forms, pancabera, garbha-vaisnava; prc:samurtarcana, visnubali; tea:kriyadhikara:11.147-152, bhrgu-samhita-vaikhanasa:13.1, dasavidhahetunirupana:p2.1-12 and p2.14-23.
  - Relation to Pāñcarātra: dsp:vaikhanasa-pancaratra.
- **Śākta catalogues:** cpt:sixty-four-sakta-tantras, subhagama-pancaka, three-krantas (low); tea:vamakesvara-tantra:1.13-22, saundarya-lahari:31, laksmidhara:31; src:laksmidhara; dsp:authority-of-sixty-four-tantras.
- **Kerala tantra:**
  - Sources: src:tantrasamuccaya, tantrasamuccaya-vimarsini, sesasamuccaya, isanasivagurudevapaddhati, kulikkattu-pacca.
  - Teachers: tch:cennas-narayanan, isanasiva-gurudeva.
  - Concepts: cpt:tantri-and-santi, seven-deities-of-tantrasamuccaya.
  - Practices: prc:kerala-daily-worship, sribhutabali, kalasabhiseka.
  - Terms: trm:tantri, santi, siveli, astabandha.
- **Prapañcasāra and Śāradātilaka:** src:prapancasara, prapancasara-vivarana, saradatilaka, padarthadarsa; tea:saradatilaka:1.7; prc:purascarana.
- **Āgama concepts:** cpt:kinds-of-diksa, grades-of-initiates, saktipata, signs-of-saktipata, grace-anugraha, temple-as-body (low), pratistha-concept, agamas-as-body-of-sadasiva, six-adhvans, five-kalas-saiva, atmartha-parartha-puja, five-purifications, kinds-of-linga, bhukti-and-mukti; tea:kirana-tantra:5.1-8 through 6.20-23; tea:ahirbudhnya-samhita:14.28-34.
- **Practices:** prc:puja, nyasa, bhutasuddhi, antaryaga, agnikarya, pratistha, temple-building-rites, jirnoddhara, mahotsava, pavitrarohana, prayascitta, ritual-mudras, mrgendra-yoga, saiva-antyesti, vidyapitha-observance (restricted).
- **Path map:** pth:mrgendra-yoga-limbs (Mṛgendra yogapāda 3: seven limbs, with yoga itself as the eighth).
- **Disputes:**
  - dsp:agama-veda-authority — queued.
  - dsp:validity-of-pancaratra — queued.
  - dsp:vaikhanasa-pancaratra — queued.
  - dsp:cause-of-saktipata — partially reconciled under P2; the Trika's objection is recorded.
  - dsp:does-diksa-liberate — queued.
  - dsp:rank-of-siddhanta-and-bhairava-tantras — queued.
  - dsp:authority-of-sixty-four-tantras — queued.

### Corrections to the task's list
1. **The 28 Āgamas.** The task's list matches the Kāmika's order (pūrva 1.30–92).
   - The Kāmika spells *Makuṭa/Mukuṭa* and *Śarvokta*.
   - The Kiraṇa (10.3–27) uses other names for five of the same slots: Nārasiṃha for Sarvokta, Bhadra for Vimala, Candrabhāsa for Candrajñāna, Vīraja for Vīra, Saurabheya for Vātula.
   - The Śrīkaṇṭhīya (quoted by Jayaratha on TĀ 1.18) puts Maukuṭa among the Śivabhedas. Its Rudrabhedas include Madgīta, Nārasiṃha, Candrāṃśu, Vīrabhadra, Visara and Saurabheya, with no Sarvokta or Vātula. Its Śivabheda list is lacunose.
2. **Upāgamas.**
   - The counts the Kāmika gives total 206; tradition usually says 207.
   - The Kāmika's own upabhedas of the Kāmika are Vaktra, Bhairavottara and Nārasiṃha, so the Mṛgendra's classification under the Kāmika is recorded as tradition only.
   - Mataṅga and Puṣkara are confirmed as upāgamas of the Pārameśvara.
   - The Niśvāsa's upabhedas match the books of the Niśvāsatattvasaṃhitā.
3. **The 64 Bhairava tantras.**
   - Three slots are unnamed or unclear in the quoted text: the 5th Yāmala, the 4th Mata and the 3rd Maṅgala.
   - The heading verse and the enumeration give the groups in different orders.
   - "Śiraścheda" is the Kashmirian name of the Jayadrathayāmala; in the Khmer inscription it is probably a Vāma text.
4. **Three gems.** The passage naming them, with their expansions, temple assignments and the count of 108, is an *adhika-pāṭha* (additional passage) in the Jayākhya edition, not part of its constituted text.
5. **Saundaryalaharī 31** reads *abhisandhāya*, not *atisandhāya*.
6. **Āgamaprāmāṇya.** The Ekāyana argument is not in the local Āgamaprāmāṇya; it is in Vedānta Deśika's Pāñcarātrarakṣā and is attributed there.
7. **Etymology of Pāñcarātra.** The Pādma (jñānapāda 1.72–75) derives the name from the five other śāstras "becoming night" before it. This is recorded alongside Śatapatha 13.6.1.1.
8. **Śaktipāta** is also Pāñcarātra. Ahirbudhnya 14.28–34 uses the term for Viṣṇu's grace and links it to karmasāmya, as Kiraṇa 5 does.

## 2. Least-sure items
- **Kerala:**
  - The Tantrasamuccaya's 12 paṭalas, 15th-c. date and TSS/Vimarśinī edition details, and the locus of its seven-deity list (tea:tantrasamuccaya:1 is a chapter-level ref).
  - src:sesasamuccaya, tantrasamuccaya-vimarsini (author) and kulikkattu-pacca.
  - The pūjā names in prc:kerala-daily-worship; prc:sribhutabali; trm:astabandha.
  - The date and region of tch:isanasiva-gurudeva.
  - Tantri families: Taraṇanallūr and Tāḻaman were deliberately not entered.
- **Pāñcarātra:**
  - Chapter counts and editions for the Sātvata, Pauṣkara and Parama.
  - src:kapinjala-samhita, bharadvaja-samhita, kasyapa-samhita-pancaratra, sanatkumara-samhita, prakasa-samhita, agastya-samhita.
  - The Lakṣmī Tantra's scholarly dating.
- **Vaikhānasa:**
  - The Smārtasūtra's 10-praśna structure.
  - src:kasyapa-jnanakanda, khiladhikara, prakirnadhikara.
  - cpt:vaikhanasa-four-liberations and cpt:amurta-samurta.
  - The month given for the viṣṇubali.
- **Śaiva:**
  - Minor paddhati authors known from catalogue metadata only: tch:varunasiva, jnanasiva, hrdayasiva, jnanaprakasa, sivagrayogin, trilocanasiva.
  - src:kriyakalagunottara (classification); the Brahmayāmala's date and size.
  - tch:hiranyadama; Sadyojyoti's dates.
- **Teachings paraphrased from memory:** tea:brahma-sutra-bhasya-sankara:2.2.42-45, sribhasya:2.2.42-45, tantravarttika:1.3.4 (locus uncertain), satapatha-brahmana:13.6.1.1, nisvasamukha:1-4.
- **Concepts without a verse anchor:** temple-as-body, six-adhvans, five-kalas-saiva, grades-of-initiates, three-krantas, five-forms-of-god-pancaratra.
- **Dispute sides given at chapter level from memory:** the Trika sides (TĀ 13) and the Saiddhāntika side of dsp:rank-of-siddhanta-and-bhairava-tantras.

## 3. Gaps
- No separate sources for the ~200 upāgamas or the lost Bhairava tantras; they are named in `structure` fields and concept members only.
- The Śivadharma corpus (lay Śaivism) is assigned to no unit and was not created.
- Not transcribed: the Pāñcarātra title lists (Pādma, Kapiñjala, Hayaśīrṣa) and the traditional Vaikhānasa corpus counts.
- No verse anchors for the temple as body, *nirbīja*, the initiate grades, the adhvans and kalās, or *viśeṣa-dīkṣā*.
- Not extracted: Pāñcarātra yoga (AS 31–32; JS 33) and the Śaiva ṣaḍaṅga-yoga with tarka (left to U19).
- Other Gāruḍa, Bhūta and Vāma texts (Tvaritā, Nayottara, Sammoha) were not entered; the Vāma stream has no ultimate view.
- Kerala: the Prapañcasāra's chapter count, the Tantrasamuccaya text (not local), Malayalam manuals, viṣa-vaidya texts and the full list of tantri families.
- The Guhyasūtra's content and the Niśvāsamukha verse loci (the Niśvāsa is not in the local corpora).

## 4. Out of reach
- The oral instruction that accompanies dīkṣā.
- The oral and Malayalam-manuscript traditions of Kerala tantri families.
- Undigitized IFP transcripts and NGMCP manuscripts.
- Restricted Vidyāpīṭha/Kaula rites: summary only (prc:vidyapitha-observance, `restricted: true`).
- Modern Vaikhānasa/Pāñcarātra temple litigation.

## Id notes for the merge
- **Suffixes.** The mūlāgamas use `src:<name>-agama`; the Kiraṇa and Mṛgendra use `-tantra`.
- **Homonyms kept apart:**
  - src:pauskara-agama and src:pauskara-samhita.
  - src:paramesvara-agama and src:paramesvara-samhita.
  - src:satvata-samhita and src:satvata-tantra.
  - src:bhrgu-samhita-vaikhanasa (not the astrological Bhṛgu Saṃhitā).
  - src:kasyapa-jnanakanda and src:kasyapa-samhita-pancaratra.
  - trm:pancakala (Pāñcarātra five periods) and trm:pancakala-saiva (five kalās).
  - trm:nyasa (placing) and trm:nyasa-surrender.
  - trm:ratnatraya-pancaratra.
- **Catalogue-only contributions to ids owned by other units:**
  - Sources: src:svacchanda-tantra, netra-tantra, siddhayogesvarimata, malinivijayottara-tantra.
  - Teachers: tch:sadyojyoti, ramakantha, aghorasiva, bhoja, umapati-sivacarya, jayaratha, yamuna, vedanta-desika, narada, sandilya, atri, bhrgu, kasyapa, marici.
  - Teachings: tea:tantraloka:1.18, brahma-sutra:2.2.42-45, saundarya-lahari:31, vamakesvara-tantra:1.13-22.
  - Terms: trm:mantra, nada, bindu, svadhyaya, pasu.
- **Generators:** the scripts are in `shards/skeleton/U08-agama-catalogue/_gen/` (part1–part11 plus `_common.py`); each part can be re-run safely.
