# REPORT — U44-indian-vajrayana (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent, which cannot write report files in this harness; the orchestrator saves it.)_

## How the shard is built
- **Generators.** They are in `shards/skeleton/U44-indian-vajrayana/_gen/`:
  - `common.py` holds the local-text loaders and helpers.
  - `siddhas.py` holds the table of the 84 siddhas.
  - The data comes from `part1_lineages_ultimate.py` … `part11_crosslinks.py`.
- **Rebuilding.** `sh shards/skeleton/U44-indian-vajrayana/_gen/run_all.sh` rebuilds everything from scratch (it deletes the unit's `*.jsonl` first) and then runs the validator.
- **What part 11 does.**
  - It fills `key_teachings` on the sources.
  - It audits references: every id referenced here exists in this shard, in another unit's shard, or in the registry.
- **Validator result.** 0 errors. The only warning is the missing REPORT.md.

### Local texts read (data only)
- **Prepared Tibetan with Wylie.** Saraha's People Dohā (Tōh 2224, 136 stanzas), King Dohā (Tōh 2263, 40) and Queen Dohā (Tōh 2264, 83); Tilopa's Gaṅgā Mahāmudrā (Tōh 2303, 29).
  - Stanza refs are the preparer's 4-line stanzas.
  - Where a sense unit crosses stanzas, the quote is cut to the exact verse lines.
- **Derge Tengyur, converted to Wylie by the unit with pyewts.**
  - Read in full:
    - Tōh 2292, the realization songs of the 84 siddhas.
    - Tōh 2281, Tilopa's Dohākoṣa.
    - Tōh 2330, Tilopa's Ṣaḍdharmopadeśa.
  - Read in part:
    - Tōh 2293, Munidatta's Caryāgīti commentary: songs 1–2, the colophon and name searches for the poets.
    - The colophons of Tōh 2280, 2301, 2273 and 2287.
- **GRETIL/DSBC Sanskrit.**
  - Pañcakrama (Tripathi ed.), Sekoddeśa (Gnoli), Mañjuśrīnāmasaṃgīti, Sarvatathāgatatattvasaṃgraha (opening), Gurupañcāśikā, Cittaviśuddhiprakaraṇa.
  - Bodhipathapradīpa: this is a *restored* Sanskrit text, and the entries flag it.
- **Muktabodha.**
  - Guhyasamājatantra (Bhattacharya 1931). There are no verse numbers in the e-text, so the unit counted double daṇḍas.
  - Advayavajrasaṃgraha (Shastri 1927): the root downfalls, Tattvaratnāvalī, Caturmudrā, Amanasikārādhāra and Kudṛṣṭinirghātana.
- **Derge catalogue.** Tōhoku numbers marked "confirmed" were checked in `tibetan_canon_titles.json` / `catalog.py`. The others are marked "from memory".

## 1. Coverage checklist (coverage map B5 and the unit brief)

### Lineages and ultimate views
- **Owned lineages:** lin:vajrayana and lin:mahasiddha.
- **Sub-lineages created:**
  - lin:arya-guhyasamaja
  - lin:jnanapada-guhyasamaja
  - lin:cakrasamvara
  - lin:kalacakra (the Indian phase only; the Tibetan Jonang and Gelug phases belong to U48/U47)
- **Ult views:**
  - ult:vajrayana, ult:mahasiddha, ult:arya-guhyasamaja, ult:jnanapada-guhyasamaja, ult:cakrasamvara, ult:kalacakra.
  - Each has caveats. The Ādibuddha is marked "not a creator, not a self".

### Tantra classifications
- **Terms:**
  - trm:kriyatantra, trm:caryatantra, trm:yogatantra
  - trm:anuttarayogatantra (flagged as a Tibetan back-translation)
  - trm:yogottaratantra, trm:yoginitantra, trm:mahayogatantra
  - trm:pha-rgyud, trm:ma-rgyud, trm:gnyis-med-rgyud (father, mother and non-dual, labeled as later Tibetan categories)
- **Concepts:** cpt:tantra-classes.
- **Supporting terms:** trm:mantranaya, trm:paramitanaya, trm:vajrayana.

### Guhyasamāja
- **Root tantra:** src:guhyasamaja-tantra (17 chapters plus the ch. 18 uttaratantra).
  - Teachings: 1.1, 2.3, 2.3p, 5.3-9, 12, 18.138, 18.139-145, 18.146-149, 18.150-152, 18.152-155.
- **Explanatory tantras:** src:vajramala-tantra, src:sandhivyakarana-tantra.
- **Ārya school:**
  - Sources: src:pancakrama (21 teachings), src:pindikrama, src:caryamelapakapradipa, src:cittavisuddhiprakarana (3 teachings), src:svadhisthanakramaprabheda, src:pradipoddyotana.
  - Teacher homonyms are kept apart: tch:nagarjuna-siddha, tch:aryadeva-tantric, tch:candrakirti-tantric (versus tch:nagarjuna, tch:aryadeva, tch:candrakirti of U40). See cpt:homonymous-tantric-authors.
- **Jñānapāda school:**
  - Sources: src:dvikramatattvabhavana, src:samantabhadra-sadhana, src:guhyasamajamandalavidhi.
  - Teachers: tch:buddhajnanapada, tch:dipankarabhadra, tch:vitapada.
  - Other: trm:manjuvajra, cpt:guhyasamaja-two-schools.
- **Pañcakrama's five stages:** pth:pancakrama-five-stages, cpt:four-empties, cpt:eighty-natural-concepts, cpt:illusory-body, cpt:clear-light-vajrayana, cpt:yuganaddha.

### Hevajra
- **Root tantra:** src:hevajra-tantra (two books, 23 chapters). Teachings 1.1, 1.1.channels, 1.1.candali, 1.5, 1.6, 1.7, 1.8, 1.10, 2.2, 2.3, 2.4 — all from memory.
- **Commentaries and sādhanas:**
  - Kāṇha's src:yogaratnamala (Tōh 1183).
  - src:hevajrapindarthatika, src:muktavali, src:bhramahara-hevajrasadhana, src:vajrapanjara-tantra, src:samputa-tantra.
- **Concepts and terms:** cpt:four-joys, cpt:four-moments, cpt:sahaja-vajrayana, trm:sahaja, trm:sahajananda.

### Cakrasaṃvara
- **Tantras:** src:cakrasamvara-tantra (Laghuśaṃvara, 51 chapters), src:abhidhanottara-tantra, src:samvarodaya-tantra, src:vajradaka-tantra, src:dakarnava-tantra, src:yoginisamcarya.
- **Commentaries and sādhanas:** src:luipa-abhisamaya, src:sadhananidana-kambala, src:cakrasamvara-panjika-jayabhadra, src:cakrasamvara-vivrti-bhavabhatta, src:vasantatilaka.
- **The 24 sites:**
  - Teaching tea:cakrasamvara-tantra:pitha-list.
  - Concepts: cpt:twenty-four-pithas, cpt:body-as-pitha.
  - Borrowings: brw:saiva-pithas-to-cakrasamvara and brw:saiva-vidyapitha-to-yogini-tantras (U24's brw:yogini-pithas-to-buddhist-yoginitantras is cross-referenced).
- **Lineages and practice:** cpt:cakrasamvara-three-lineages, prc:body-mandala.

### Kālacakra
- **Texts:**
  - src:kalacakra-tantra (5 chapters; teachings 1, 2, 4, 5 from memory).
  - src:kalacakra-mulatantra.
  - src:sekoddesa (12 teachings, read locally).
  - src:vimalaprabha, src:paramarthaseva, src:sekoddesatika.
- **Concepts:** cpt:sambhala, cpt:outer-inner-other-kalacakra, cpt:kalacakra-calendar (epoch 1027), cpt:empty-form, cpt:aksara-sukha-kalacakra, cpt:ten-signs-kalacakra.
- **Six-branch yoga:** prc:sadanga-yoga. pth:kalacakra-six-branches is only referenced (U51 owns it). The Guhyasamāja version is written as pth:guhyasamaja-sadanga-yoga.

### Other tantras
- **Vajrayoginī cycles:** cpt:vajrayogini-cycles, src:guhyasamayasadhanamala.
- **Mañjuśrīnāmasaṃgīti:** src:manjusrinamasamgiti (teachings 28-29, 30, 100), src:namamantrarthavalokini.
- **Mahāvairocana:**
  - Sources: src:mahavairocana-sutra, with teachings 1 (the three phrases), 1.mind, 2 (the Womb maṇḍala) and a-syllable.
  - Concepts: cpt:three-phrases-mahavairocana, cpt:syllable-a, cpt:womb-and-vajra-mandalas.
  - Commentaries: src:mahavairocana-pindartha, src:mahavairocana-vrtti-buddhaguhya.
- **Vajraśekhara / Tattvasaṃgraha:**
  - Sources: src:sarvatathagatatattvasamgraha (the five abhisambodhis read locally), src:vajrasekhara-sutra.
  - Concepts: cpt:five-buddha-families, cpt:five-wisdoms, cpt:four-seals, cpt:five-abhisambodhis.
  - Commentaries: src:tantrarthavatara, src:kosalalamkara, src:tattvaloka-anandagarbha.
- **Also covered:** src:candamaharosana-tantra, src:buddhakapala-tantra, src:mahamaya-tantra, src:krsnayamari-tantra, src:raktayamari-tantra, src:vajrabhairava-tantra, src:catuspitha-tantra, src:sarvabuddhasamayoga, src:mayajala-tantra, src:sarvadurgatiparisodhana-tantra.
- **Kriyā and caryā tantras:** src:manjusrimulakalpa, src:susiddhikara-sutra, src:subahupariprccha-tantra, src:vajrapani-abhiseka-tantra.

### The eighty-four siddhas
- **All 84 are present as teachers,** in the order of Tōh 2292. Each has:
  - its song as tea:caturasiti-siddha-bodhihrdaya:1–84, with the Tibetan original read locally;
  - Abhayadatta's life, recalled from memory.
- **Ids shared with other units** (the unit adds only its contribution): tch:luipa, tch:virupa, tch:savaripa, tch:saraha, tch:tilopa, tch:naropa, tch:kanha, tch:goraksanatha, tch:caurangi, tch:jalandharanatha, tch:nagarjuna-siddha, tch:ratnakarasanti (= Śāntipa), tch:laksminkara, tch:indrabhuti.
- **Other named siddhas** have new ids: tch:dombipa, tch:minapa, tch:kukkuripa, tch:ghantapa, tch:kambala, tch:mekhala, tch:kanakhala, tch:manibhadra, tch:tantipa, tch:bhusuku, tch:darikapa, tch:aryadeva-tantric (Karṇaripa), and so on.
- **Not in the 84 but in scope:** tch:maitripa, tch:niguma, tch:sukhasiddhi.
- **Life episodes from memory:** tea:caturasiti-siddha-pravrtti:3, 6, 8, 12, 20, 22, 41, 65, 66, 82.
- **Concepts:** cpt:eighty-four-siddhas (related to U21's cpt:eighty-four-siddhas-natha).

### Songs
- **Saraha:**
  - src:dohakosa-saraha: 40 teachings.
  - src:dohakosa-king-saraha: 15.
  - src:dohakosa-queen-saraha: 19.
  - Also src:dohakosa-panjika, src:dohakosa-mahamudropadesa-saraha, src:kakhasya-doha.
- **Caryāgīti:**
  - Sources: src:caryagiti, src:caryagiti-munidatta.
  - Teachings 1 and 2 read in Tibetan; 5, 6, 10, 28 and 33 from memory; the colophon read.
  - Concept cpt:caryagiti-poets lists 23 poets. New poet ids: tch:catila, tch:dhendhanapa, tch:gundaripa, tch:mahidhara, tch:bhadepa, tch:tadaka, tch:jayanandi, tch:tantripa-caryagiti.
- **Tilopa:**
  - src:ganga-mahamudra: 23 teachings.
  - src:dohakosa-tilopa: 4.
  - src:saddharmopadesa-tilopa: 7. This is the Indian root of the six yogas: cpt:six-dharmas-tilopa, cpt:four-instruction-lineages-tilopa.
  - The "six words": cpt:tilopa-six-words (low confidence; Tibetan transmission).
- **Kāṇha:** src:dohakosa-kanha.
- **Also covered:** src:dohakosa-virupa, src:virupa-padacaturasiti, src:mahamudra-vajragiti-savaripa.

### Concepts
- **The two stages:** cpt:two-stages, cpt:generation-stage, cpt:completion-stage, pth:vajrayana-two-stages.
- **Deity yoga:** cpt:deity-yoga, prc:deity-yoga, cpt:divine-pride.
- **The bodies:** cpt:buddha-bodies-vajrayana, trm:svabhavikakaya, trm:mahasukhakaya.
- **Families and gnoses:** cpt:five-buddha-families, cpt:five-wisdoms, trm:pancajnana plus the five gnosis terms, cpt:purity-of-aggregates-and-elements.
- **Subtle body:** cpt:buddhist-subtle-body, cpt:four-cakras-vajrayana, cpt:winds-vajrayana, trm:avadhuti, trm:lalana, trm:rasana (logged as partial equivalents of suṣumṇā, iḍā and piṅgalā, resting on Sekoddeśa 46–50).
- **Inner heat:** cpt:candali, prc:candali (restricted).
- **Illusory body and clear light:** cpt:illusory-body, cpt:clear-light-vajrayana.
- **The four joys:** cpt:four-joys, phn:four-joys.
- **Sahaja and nature of mind:** cpt:sahaja-vajrayana, cpt:nature-of-mind-siddha, cpt:amanasikara.
- **Consecration:** cpt:abhiseka-four, cpt:abhiseka-kalacakra, and the four abhiṣeka terms.
- **Pledges:** cpt:samaya-vows, cpt:fourteen-root-downfalls (from the Advayavajrasaṃgraha, local), cpt:three-vows, obs:root-downfalls.
- **Karmamudrā:** cpt:karmamudra, prc:karmamudra (restricted, summary and the texts' warnings only).
- **Antinomian conduct:** cpt:vratacarya, prc:vratacarya.
- **Institutions:** cpt:tantric-monastic-centres.

### Practices, phenomenology and disputes
- **Practices:** 27; the list is in practices.jsonl.
- **Phenomenology:** 18 items, including the five signs (GST 18) and the ten signs (Sekoddeśa 26).
- **Disputes:**
  - dsp:legitimacy-of-tantra (queued)
  - dsp:literal-or-symbolic-tantric-conduct (partially reconciled under P5 and P4)
  - dsp:mantra-and-paramita-ways (partially reconciled under P3 and P4)
  - dsp:higher-consecrations-for-monastics (queued)
  - dsp:ritual-or-innate (reconciled under P1 and P4; rests on the Kudṛṣṭinirghātana)
  - dsp:acceptance-of-the-kalacakra (queued, low confidence)
- **Queue refs** for the RECONCILE_QUEUE: RQ-U44-legitimacy-of-tantra, RQ-U44-higher-consecrations-monastics, RQ-U44-acceptance-of-kalacakra.
- **Referenced but not written** (U50 owns it): dsp:sudden-or-gradual, via Queen Dohā v81–82 ("gradual and simultaneous entry").

### D checklist
Covered for each owned lineage through concepts, terms and ult views:
- the ultimate
- consciousness (the empties, clear light)
- the self (divine pride, adventitious stains)
- mind (the 80 conceptions)
- body (the subtle body)
- matter (aggregates and elements)
- obstacles
- ethics
- karma and liberation
- path maps
- signs and powers
- teacher and transmission
- cosmology (Śambhala)
- sound (the syllable A, sandhyābhāṣā)
- death (cpt:dissolution-at-death, cpt:antarabhava, cpt:funerary-rites-sarvadurgati)
- disputes

### Corrections to the brief's must-cover list
- **Guhyasamāja chapters.** It has 17 chapters plus an eighteenth "uttaratantra"; the brief's "18 chapters" counts that appendix.
- **Abhayadatta's lives are not in the local Derge Tengyur** (they are, as I recall, in the Peking/Narthang). The unit used Tōh 2292 instead. Its order follows Abhayadatta's almost exactly, but it names different siddhas at positions 36, 63, 64, 67, 74, 78 and 82. For example, Tōh 2292 has "Dhūmapa" where Abhayadatta has Carpaṭi, and "nI lak+Sha na" at 82 (taken as Lakṣmīṅkarā, low confidence). The notes on each entry say so.
- **Tilopa's "six words of advice" are not in the Tengyur texts of Tilopa read** (Tōh 2281, 2303, 2330). They are recorded as Tibetan transmission, low confidence.
- **Vajraśekhara and Tattvasaṃgraha are distinct Kangyur texts** (Tōh 480 and 479), but East Asian usage merges them. Both ids exist (registry src:vajrasekhara-sutra and src:sarvatathagatatattvasamgraha).
- **Six-branch order.** The Guhyasamāja ch. 18 order (pratyāhāra, dhyāna, prāṇāyāma, dhāraṇā, anusmṛti, samādhi) matches the order given for the Kālacakra; verified locally in GST 18.

## 2. Items least sure of (check first)
- **Abhayadatta's life stories** for most of the 84 (77 teachers are marked low). Weakest: positions 23–40, 48–63, 67–81. Also the Abhayadatta numbering of the tea:caturasiti-siddha-pravrtti:N ids.
- **Identifications of Tōh 2292 names with Abhayadatta's siddhas:**
  - 21 Śalipa: Tōh 2292 spells it "sha wa ri pa".
  - 28 Dhobīpa: spelled "Dom+bi pa".
  - 30 Kambala: spelled "ka ma la".
  - 33 Tandhepa, 36 Dhamupa, 39 Bhalaha.
  - 63 Kumaripa: spelled "kaM pa la".
  - 64 Dhūmapa.
  - 67 Kanakhalā: spelled "nA ga ka la ka".
  - 74 Sakara: spelled "pa ga ra".
  - 78 Putali: spelled "su ta ba".
  - 82 Lakṣmīṅkarā: spelled "nI lak+Sha na".
- **Song paraphrases the unit could not fully construe** (marked low or moderate): Tōh 2292 nos. 8, 31, 59, 65, 67, 71, 76, 83; King Dohā v12; People Dohā v108; Caryāgīti song 1 (Tibetan).
- **Hevajra refs are from memory:** 1.5, 1.8 (≈ I.8.36), 2.2 (≈ II.2.51), 2.4 (≈ II.4.69–70), 1.7 (the pīṭha classes with the ten grounds), 1.10 (the joys).
- **Other memory-based items:**
  - The Laghuśaṃvara 1.1 wording.
  - The 24-site list order.
  - All Kālacakra chapter summaries.
  - The Vimalaprabhā statements: the Ādibuddha as not a creator; monks as the best vajra masters.
  - The Caṇḍamahāroṣaṇa passage on women (≈ ch. 8).
  - Caryāgīti songs 5, 6, 10, 28, 33 and the poet counts.
- **Tōh numbers from memory:** 805, 1853, 1855, 2501, 2503, 2510, and the Yoginīsaṃcārya.
- **Attributions:**
  - The seven siddhi texts (the last three members).
  - tch:viraprabhasvara (the Sanskrit is reconstructed from dpa' bo 'od gsal).
  - The Dohākoṣapañjikā ascribed to Advayavajra.
  - The Caryāpa = Kāṇha identification.
  - Vitapāda, Durjayacandra, Tripiṭakamala.
- **Guhyasamāja verse numbers** are the unit's own count in Bhattacharya's e-text. They may not match Matsunaga's numbering.
- **Dates:** the Sādhanamālā (now "c. 12th c."); Śākyaśrībhadra; Kālacakrapāda (elder and younger).

## 3. Gaps (belong here but could not be created responsibly)
- **Missing Indian texts:**
  - Hevajra, Laghuśaṃvara and Kālacakra verses. They need a Sanskrit e-text (Snellgrove, Gray, Sarnath editions).
  - The Kālacakra's six-branch yoga at verse level.
  - The Vimalaprabhā's polemics (Īśvara, the barbarians).
- **Missing lineages and systems:**
  - The full Vajrayoginī sādhana lineages (Guhyasamayasādhanamālā not local).
  - Jñānapāda texts: nothing read; the Mañjuvajra maṇḍala count of 19 deities is from memory.
  - Ghaṇṭāpa's body-maṇḍala system, and Kṛṣṇācārya's Vasantatilakā.
- **Missing commentaries and treatises:**
  - Candrakīrti's Pradīpoddyotana (the seven ornaments and six alternatives, from memory only).
  - Indrabhūti's Jñānasiddhi apart from the one quoted gloss.
  - Munidatta's commentary beyond songs 1–2; the Apabhraṃśa and Old Bengali originals of the Dohās and the Caryāgīti.
- **Missing teachers:**
  - Other siddha lists: the Varṇaratnākara's 84, Tāranātha's Seven Instruction Lineages — only a source entry, not read.
  - Indian teachers of Marpa and Atiśa beyond the named ones (Avadhūtipa, Paiṇḍapātika, Prajñāraśmi …).
- **Missing debates:** the Indian debate on whether the Ādibuddha is an Īśvara, and the critique of theism in the Vimalaprabhā. These belong with U50's dsp:isvara and were not added.

## 4. Out of reach
- **Oral and restricted instructions:** caṇḍālī methods, retention in the six-branch yoga, karmamudrā, transference and the "cheating death" techniques. Only summaries and the texts' own warnings are recorded, all flagged restricted.
- **Not in the local corpora:** Abhayadatta's Caturaśītisiddhapravṛtti (Peking/Narthang Tengyur); the Newar manuscripts of the Guhyasamayasādhanamālā; the Sanskrit of many commentaries (Jayabhadra, Bhavabhaṭṭa, Muktāvalī, Sekoddeśaṭīkā).

## Decisions (for DECISIONS.md)
1. **Four Indian sub-lineages were created** (lin:arya-guhyasamaja, lin:jnanapada-guhyasamaja, lin:cakrasamvara, lin:kalacakra) so that definitions can be given per lineage. Each has an ult view. U48 may reference lin:kalacakra for the Tibetan phase.
2. **Tantric homonyms were given separate ids** (tch:aryadeva-tantric, tch:candrakirti-tantric), while U30's tch:nagarjuna-siddha is reused for the siddha and tantric author. The tradition's identification with the Madhyamaka masters is recorded in the notes.
3. **Tōh 2292 is the basis for the 84-siddha list**, because Abhayadatta's text is not local. The new source is src:caturasiti-siddha-bodhihrdaya. The registry's src:caturasiti-siddha-pravrtti is kept for the lives.
4. **Tibetan paraphrases are flagged.** Paraphrases made from Tibetan translations carry `ai_translated: true` and a `translation_basis` note. Originals are quoted in Wylie exactly as prepared, sliced to the verse lines of the sense unit. Misprints in the Sanskrit e-texts are kept and noted, not silently corrected.
5. **Shared ids got only this unit's contribution:** trm:mahamudra, trm:sahaja, trm:bindu, trm:svadhisthana (homonym noted), trm:prakrti (Ārya-school sense), trm:samvara, obs:three-poisons, cpt:antarabhava, and the shared teachers. The registry dispute dsp:sudden-or-gradual and the path maps pth:kalacakra-six-branches and pth:mahamudra-four-yogas are referenced but not written.
