# U15-dvaita — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Unit: U15-dvaita (coverage map A6 Dvaita; owns lin:dvaita).
- Generators: _gen/part1…part8*.py, run from tradition-ontology/; common.py holds the shared helpers.
- Validator: 0 errors; the only warning is the missing REPORT.md.

Counts: lineages 5 (lin:dvaita and 4 maṭha sub-lineages); sources 98; teachers 37; teachings 107 (96 high, 10 moderate, 1 low confidence; 12 with `original`); terms 107; concepts 56; practices 19 (1 restricted); obstacles 10; path maps 3; phenomenology 9; disputes 6; ultimate views 5; borrowings 6; interpretation_log 48 lines.

## Method
Everything is at skeleton level.

The local corpus sources_raw/raw_etexts/vedAntam/dvaitam (github.com/sanskrit/raw_etexts, about 650 Devanāgarī files) holds most of Madhva's works and the main commentaries. I used it to check wording, verse numbers, titles, authorship colophons and structure.
- Entries checked this way have confidence "high" and a note saying so.
- `original` text is given only where I read it in the e-text; the IAST transliteration is mine.
- Numbering follows the raw_etexts copy. Other editions differ: for example, the bhakti verse is MBTN 1.85 there but is often cited as 1.86, and the Nyāyasudhā e-text numbers Anuvyākhyāna 4.2.46 as "4,2.43".
- Prose works have no standard numbering, so their refs are section labels or chapter (pariccheda) numbers.

## Corrections to the task's MUST-COVER list
1. The full title of "Mithyātvānumānakhaṇḍana" is Prapañca-mithyātvānumāna-khaṇḍana.
2. The 37 works (Sarvamūla), as counted here:
   - Brahmasūtra works: BSB, Anuvyākhyāna, Nyāyavivaraṇa, Aṇubhāṣya.
   - Gītā works: Gītābhāṣya, Gītātātparyanirṇaya.
   - Ten Upaniṣad bhāṣyas.
   - Ṛgbhāṣya, covering ṚV 1.1–1.40 (40 sūktas, checked).
   - The ten prakaraṇas.
   - MBTN, Bhāgavatatātparyanirṇaya, Yamakabhārata.
   - Dvādaśastotra, Narasiṃhanakhastuti, Kṛṣṇāmṛtamahārṇava, Tantrasārasaṅgraha, Sadācārasmṛti, Yatipraṇavakalpa (colophon "Praṇavakalpa"), Jayantīnirṇaya (colophon "Jayantīkalpa").
   - Outside the 37 but ascribed to Madhva: Kandukastuti; Tithinirṇaya (doubtful); Sannyāsapaddhati (its colophon names Pūrṇaprajña).
3. The ten prakaraṇas are correctly listed. The local edition numbers Tattvasaṅkhyāna 6th, Tattvaviveka 7th and Tattvoddyota 8th; Upādhikhaṇḍana and Māyāvādakhaṇḍana swap 3rd/4th between copies.
4. The Aṇubhāṣya is often said to have 32 verses; the local copy numbers 30 (7+7+7+9).
5. "Madhva as the third avatāra of Vāyu" is Madhva's own claim, not only later tradition. He states it in MBTN 32.162 and 32.166 and at the close of the Anuvyākhyāna (4.4.15), reading ṚV 1.141 (quoted at MBTN 32.163).
6. Madhva's dates, kept as labelled accounts:
   - Tradition, one reading: MBTN 32.120 dates Bhīma's rebirth to Kali 4300, about 1199 CE; with the traditional 79 years this gives 1199–1278.
   - Tradition, another reading used by the maṭhas: 1238–1317.
   - Scholarly: about 1238–1317 (B. N. K. Sharma, from Narahari Tīrtha's inscriptions).
7. The five differences appear in MBTN 1.68–71 as a quoted scripture, not as Madhva's own verse. The same passage says internal difference within Viṣṇu is unreal and that gradation holds "always".
8. MBTN 1.86–90 gives a variant of the three classes of souls:
   - gods and the best humans are fit for liberation;
   - middling humans are fit only for transmigration;
   - the lowest humans go to hell (niraya) and dānavas to darkness (tamas).
   Tattvasaṅkhyāna 6 instead places the lowest humans among those fit for darkness. Both schemes are recorded.
9. Jayatīrtha's commentary on the Pramāṇalakṣaṇa is titled Nyāyakalpalatā.
10. The Nyāyāmṛta has four chapters that follow the four chapters of the Brahmasūtras. They argue in turn:
    - the world is real — the five Advaita definitions of falsity are refuted;
    - the Upaniṣads have no "impartite" meaning, and Brahman is different from souls;
    - on the means of liberation, against the Vivaraṇa view;
    - liberation is not mere removal of ignorance, and the liberated are graded.
11. The twofold ignorance (one covering the soul's own qualities, one covering the Supreme) is confirmed in the Bhāgavatatātparya on 10.87.14.
12. Tattvaviveka 10–12 accepts difference-and-identity for a thing's temporary properties and no difference for its lasting ones. This qualifies the usual summary that Dvaita simply denies difference-and-identity.
13. Satyadharma Tīrtha is included at low confidence only; none of his works were verified, so none were created.

## (1) Coverage checklist
**Lineage and institutions**
- lin:dvaita, with sub-lineages lin:uttaradi-matha, lin:raghavendra-matha, lin:vyasaraja-matha and lin:udupi-asta-matha.
- The eight Uḍupi maṭhas and their rotation of Kṛṣṇa worship: prc:paryaya-puja, trm:paryaya, trm:asta-matha.
- Haridāsas (owned by U56) are only referenced: lin:haridasa-karnataka, brw:dvaita-to-haridasa, tch:purandara-dasa, tch:kanaka-dasa, src:harikathamrtasara.

**Madhva**
- tch:madhva, with tradition's and scholarly dating and the tradition's realization account.
- src:sumadhvavijaya, with teachings 4.32-33, 5.1-2 and 16.57-58; also src:anumadhvavijaya.

**The 37 works**
- src:brahma-sutra-bhasya-madhva, src:anuvyakhyana, src:nyayavivarana, src:anubhasya-madhva
- src:gita-bhasya-madhva, src:gita-tatparya-nirnaya
- src:{isa,kena,katha,mundaka,prasna,mandukya,taittiriya,aitareya,chandogya,brhadaranyaka}-upanisad-bhasya-madhva
- src:rgbhasya-madhva
- The ten prakaraṇas:
  - src:pramanalaksana-madhva, src:kathalaksana, src:upadhikhandana, src:mayavadakhandana, src:prapancamithyatvanumanakhandana
  - src:tattvasankhyana, src:tattvaviveka, src:tattvoddyota, src:karmanirnaya, src:visnutattvavinirnaya
- src:mahabharata-tatparya-nirnaya, src:bhagavata-tatparya-nirnaya, src:yamakabharata
- src:dvadasastotra, src:narasimhanakhastuti, src:krsnamrtamaharnava, src:tantrasarasangraha-madhva, src:sadacarasmrti-madhva, src:yatipranavakalpa, src:jayantinirnaya
- Outside the 37: src:kandukastuti, src:tithinirnaya-madhva, src:sannyasapaddhati-madhva

**Later teachers**
- Padmanābha Tīrtha: src:sattarkadipavali.
- Trivikrama Paṇḍitācārya: src:tattvapradipa-trivikrama, src:vayustuti.
- Nārāyaṇa Paṇḍitācārya: src:sumadhvavijaya, src:manimanjari, src:yogadipika-narayana-pandita.
- Jayatīrtha:
  - src:nyayasudha, src:tattvaprakasika, src:pramanapaddhati, src:vadavali
  - src:prameyadipika, src:nyayadipika-jayatirtha, src:nyayakalpalata-jayatirtha, src:rgbhasya-tika-jayatirtha
  - nine prakaraṇa commentaries (src:*-tika-jayatirtha)
- Vyāsatīrtha: src:nyayamrta, src:tarkatandava, src:tatparyacandrika, src:bhedojjivana, src:mandaramanjari.
- Vādirāja: src:yuktimallika, src:tirthaprabandha, src:rukminisavijaya, src:laksalankara.
- Vijayīndra: src:nyayamrta-amoda, src:madhvatantramukhabhusana, src:appayyakapolacapetika.
- Rāghavendra: nine works, including src:nyayasudha-parimala, src:tattvaprakasika-bhavadipa, src:nyayamuktavali-raghavendra, src:gitavivrti, src:bhattasangraha.
- Satyadharma: tch:satyadharma-tirtha only (low confidence).
- Other teachers:
  - Madhva's direct disciples, including the eight founders of the Uḍupi maṭhas.
  - Narahari, Mādhava and Akṣobhya Tīrtha.
  - Śrīpādarāja, Brahmaṇya, Surendra, Sudhīndra, Raghūttama, Vijayadhvaja, Satyanātha.
  - Satyadhyāna and Viśveśa, both marked recent.
  - Rāmācārya.
  - Brahmānanda Sarasvatī (an Advaita opponent).

**Concepts from the task list**

| Concept | Main ids |
|---|---|
| Five differences | cpt:pancabheda; tea:mahabharata-tatparya-nirnaya:1.68-71 |
| Independent and dependent reality | cpt:svatantra-paratantra; tea:tattvasankhyana:1; tea:tattvaviveka:1-3 and 13 |
| Gradation of souls and the three classes | cpt:taratamya, cpt:jiva-traividhya, cpt:andhatamas, cpt:svarupa-yogyata |
| Eternal distinction in liberation | cpt:difference-in-liberation |
| Graded bliss in liberation | cpt:ananda-taratamya |
| The witness (sākṣin) | cpt:saksin; Anuvyākhyāna 1.4.95-103 |
| Viśeṣa | cpt:visesa-dvaita, cpt:bheda-svarupa |
| Soul as God's reflection (bimba–pratibimba) | cpt:bimba-pratibimba-dvaita, prc:bimba-pratibimba-dhyana |
| Hari supreme, Vāyu highest soul | cpt:hari-sarvottamatva, cpt:vayu-jivottamatva, cpt:vayu-three-avataras |
| Bhakti with knowledge of God's greatness | cpt:bhakti; MBTN 1.85 and 1.104-105 |
| God's grace | cpt:grace, cpt:grace-through-hierarchy, cpt:three-grades-of-prasada |
| Three means of knowledge | cpt:kevala-anupramana |
| Reality of the world | cpt:jagat-satyatva |
| Critique of māyā | cpt:mayavada-khandana, cpt:atat-tvam-asi |

**Section D checklist**

| Item | Main ids |
|---|---|
| The ultimate | ult:dvaita |
| States of consciousness | cpt:four-states-as-forms-of-visnu, cpt:dream-dvaita, cpt:deep-sleep-dvaita |
| Self | cpt:jiva |
| Mind | cpt:antahkarana-dvaita |
| Body and energy anatomy | cpt:nadis-dvaita |
| Matter | cpt:prakrti, cpt:tattva-division-dvaita, cpt:kala |
| Obstacles | 10 obstacle entries; cpt:avidya |
| Ethics | cpt:god-as-true-agent, cpt:adhikara-three-grades |
| Karma and liberation | cpt:karma-dvaita, cpt:moksa |
| Stages | cpt:sravana-manana-nididhyasana, cpt:aparoksa-jnana; the path maps |
| Signs, powers, warnings | cpt:yogyata-limited-vision; phenomenology entries |
| Teacher and transmission | cpt:guru-dvaita, prc:diksa-dvaita |
| Cosmology | cpt:srsti-dvaita, cpt:asta-kartrtva, cpt:ksara-aksara-purusottama |
| Sound and language | cpt:sarvasabdavacyatva, cpt:pranava-eightfold, cpt:matrka-fifty-forms, cpt:threefold-meaning-mahabharata, cpt:sadagama, cpt:apauruseyatva, cpt:sadlinga-tatparya |
| Death | cpt:utkranti-dvaita, cpt:krama-mukti-with-brahma |

**Section E (practices)**
There are 19. Tapta-mudrā-dhāraṇa (heated branding) is restricted: summary only, no procedure.

**Section F (path maps)**
pth:dvaita-sadhana-krama, pth:dvaita-moksa-krama and pth:yogadipika-graded-disciplines. Their stage bands are logged as interpretation.

**Section G (debates)**
- Disputes owned by U50 are only referenced; Dvaita's side is supplied as teachings:
  - dsp:souls-one-or-distinct and dsp:world-real-or-appearance
  - dsp:advaita-crypto-buddhism, from Anuvyākhyāna 2.2.241-242 and 4.2.40-48 and the Nyāyasudhā on 4.2.46
  - dsp:works-knowledge-grace, dsp:number-of-pramanas, dsp:status-of-veda, dsp:isvara
  - dsp:saguna-nirguna, dsp:women-caste-liberation, dsp:causation
- Six disputes are owned here. Each records both sides first, then candidate readings, then both traditions' objections:
  - dsp:nyayamrta-advaitasiddhi: Vyāsatīrtha → Madhusūdana → Rāmācārya's Taraṅgiṇī → Brahmānanda's Laghucandrikā
  - dsp:tat-tvam-asi, which includes the Akṣobhya–Vidyāraṇya debate
  - dsp:gradation-in-liberation
  - dsp:can-every-soul-be-liberated
  - dsp:appayya-vijayindra-controversy
  - dsp:madhva-sources-authenticity
- All six are queued as "not yet reconciled". Dvaita's rejection of any reconciliation that dissolves difference is recorded in the objections and in the ult:dvaita caveat.

## (2) Least sure — check these first
- **Recalled titles.** Sampradāyapaddhati, Nyāyaratnāvalī (Padmanābha), what the Mandāramañjarī covers, Madhvatantramukhabhūṣaṇa, Appayyakapolacapeṭikā.
- **Attributions.** The Nyāyāmṛta-āmoda is attributed to Vijayīndra only on the strength of a file name. Also uncertain: Abhinavāmṛta, Vāgvajra, Mantrārthamañjarī, Lakṣālaṅkāra, and Aṇumadhvavijaya as Nārāyaṇa Paṇḍita's work.
- **Maṭha history.**
  - Which founder heads which Uḍupi maṭha, and how the maṭhas are paired.
  - The change of the rotation to two years credited to Vādirāja (1522).
  - Pontificate dates, the splits after Vidyādhirāja, and where Jayatīrtha's tomb-shrine is.
- **Hagiographic details** (all labelled as the tradition's account):
  - Jayatīrtha's earlier life.
  - Narahari's Kaliṅga episode and the Yakṣagāna claim.
  - Vyāsatīrtha's kuhu-yoga episode and the 732 Hanumān images.
  - Rāghavendra's "700 years".
  - Vādirāja as a future Vāyu.
  - Madhva vanishing while teaching the Aitareya.
  - The gopīcandana origin of the Uḍupi Kṛṣṇa image.
- **Other people.** Satyadharma, Satyadhyāna, Appaṇṇācārya, and "Nārāyaṇācārya" as author of the Sadācāradīpikā.
- **The other schools' sides in the disputes** are from general knowledge with chapter-level refs, including Śrībhāṣya 4.4.17-21 on equality in liberation.
- **Readings and refs.**
  - The reading "ajāt" in Anuvyākhyāna 4.4.13 may be a misreading.
  - The middle component names of the eightfold praṇava are recalled, not checked.
  - The Gauḍīya affiliation details are low confidence.
  - The Anuvyākhyāna chapter headings for verses 88–106 come from an e-text that is incomplete in 2.4 and 3.1.

## (3) Gaps
**Works not given entries**
- Most of Vijayīndra's reputed 104 works.
- Vādirāja's Kannada works.
- Rāghavendra's minor works.
- Raghūttama's other Bhāvabodhas and Satyadharma's glosses.
- Further Nyāyāmṛta commentaries and replies: Śrīnivāsa Tīrtha's Prakāśa, Vanamālī Miśra, Ānanda Bhaṭṭāraka.
- Chalāri Śeṣācārya.
- Several texts that are in the local corpus but not yet entered:
  - commentaries by Viśvapati Tīrtha and Sumatīndra Tīrtha;
  - the Muktimuktāvalī;
  - Dvaitadyumaṇi, Sattattvaratnamālā and Haribhaktisudhākara, whose authors were not identified.

**Lineage names not given**
- The Haṃsa succession before Acyutaprekṣa.
- Full pontiff lists of the maṭhas.
- The Gauḍa Sārasvata Mādhva maṭhas (Kāśī, Gokarṇa-Partagāḷī), plus the Śrīpādarāja, Subrahmaṇya, Bhīmanakaṭṭe and Bhaṇḍārakeri maṭhas.

**Teachings not written**
- Upaniṣad commentaries other than the Māṇḍūkya and Chāndogya.
- The Gītā commentaries verse by verse.
- Most of the Bhāgavatatātparya.
- The Tarkatāṇḍava, Tātparyacandrikā and Yuktimallikā.
- The Dvādaśastotra and Vāyustuti beyond their opening verses.
- The three guṇas as presided over by Śrī, Bhū and Durgā.
- The creation account of MBTN chapter 3.
- The three kinds of karma.

**Warnings not found**
None was found in the texts about powers (siddhis) as obstacles, or about exemptions from the Ekādaśī fast.

**Not recorded**
- 20th-century continuations of the debates.
- Cāturmāsya vows (not verified).

## (4) Out of reach
- Oral learning of the maṭhas (recitation and vākyārtha disputation).
- Initiation mantras (deliberately not recorded).
- The tapta-mudrā procedure (restricted).
- Undigitized Tuḷu-script and Kannada manuscripts, such as the Palimaru Sarvamūla.
- Inscriptions, which were not consulted.
- Copyrighted modern editions and translations, which appear only as labelled scholarly metadata.

## Decisions taken
**Sub-lineages**
- The four maṭha sub-lineages are created under lin:dvaita. Each has a minimal ultimate view pointing to ult:dvaita.

**Id disambiguation**
- src:anubhasya-madhva, because src:anubhasya is Vallabha's work (owned by U16).
- Also disambiguated: src:pramanalaksana-madhva, src:tantrasarasangraha-madhva, src:sadacarasmrti-madhva, src:tithinirnaya-madhva, src:nyayadipika-jayatirtha, src:nyayaratnavali-padmanabha.
- For teachers: tch:visnu-tirtha-sode, tch:rama-tirtha-kaniyur, tch:narasimha-tirtha-adamaru.

**Shared ids**
- Shared terms and concepts (brahman, bhakti, sākṣin, jīva, avidyā, māyā, karma, manas, nāḍī, dīkṣā, guru, and cpt:bhakti, grace, saksin, moksa, jiva, prakrti, kala, avidya, avatara) carry only Dvaita's own definition, for the merge to combine.
- Practices specific to Dvaita get Dvaita ids. Only śravaṇa, manana and nididhyāsana reuse generic ids.

**Disputes**
- Disputes owned by U50 are referenced, not written.
- The Akṣobhya–Vidyāraṇya debate is placed under dsp:tat-tvam-asi.

**Advaita texts**
- The Advaita texts at the centre of the controversies are entered as sources with Advaita as their lineage: Madhvatantramukhamardana, Laghucandrikā, Sarvadarśanasaṅgraha. No Advaita teachings were written; U13 should supply them.
