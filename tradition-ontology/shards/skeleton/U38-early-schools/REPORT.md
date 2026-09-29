# REPORT — U38-early-schools (Phase B skeleton)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


The generators are in `shards/skeleton/U38-early-schools/_gen/` (`common.py`, `texts.py`, parts 1–11). Run them in order from `tradition-ontology/`. Part 10 patches the saved entries, so run it after parts 1–9.

Local texts read (data only):
- GRETIL Abhidharmakośakārikā (597 kārikās; the e-text lacks 2.32) and Abhidharmakośabhāṣya (Pradhan page markers).
- Yaśomitra's Sphuṭārthā.
- Mahāvastu (Senart ed., vol.page).
- Kathāvatthu (bilara-data).
- Headers of the Udānavarga, Patna Dharmapada, the Prātimokṣas and the MSV vastus.

Final validator result: 0 errors. The only warning is that REPORT.md is missing.

## 1. Coverage checklist (scope I1 and the unit brief), with ids

**Owned lineages**
- lin:sarvastivada, lin:sautrantika, lin:mahasanghika, lin:lokottaravada, lin:pudgalavada, lin:dharmaguptaka, lin:mulasarvastivada, lin:mahisasaka.
- Added lineages:
  - Grouping: lin:sthavira.
  - Sarvāstivāda currents: lin:vaibhasika, lin:darstantika.
  - Other Sthavira branches: lin:haimavata, lin:kasyapiya, lin:vibhajyavada.
  - Pudgalavāda branches: lin:vatsiputriya, lin:sammitiya, lin:dharmottariya, lin:bhadrayaniya, lin:sannagarika.
  - Mahāsāṃghika branches: lin:ekavyavaharika, lin:kaukkutika, lin:bahusrutiya, lin:prajnaptivada, lin:caitika, lin:purvasaila, lin:aparasaila, lin:andhaka.
  - East Asian continuations: lin:lu-zong, lin:ritsu-shu, lin:jushe-zong, lin:chengshi-zong.
- Eight ult views: ult:sarvastivada, ult:sautrantika, ult:mahasanghika, ult:lokottaravada, ult:pudgalavada, ult:dharmaguptaka, ult:mulasarvastivada, ult:mahisasaka. Each has a caveat, and each sets tradition_denies_single_ultimate: true.

**Schisms and lists of the eighteen schools**
- Concepts: cpt:eighteen-schools, cpt:first-schism, cpt:councils, cpt:four-nikayas, cpt:ten-points-of-vaisali, cpt:five-points-of-mahadeva.
- Sources: src:samayabhedoparacanacakra (T2031/2032/2033, D4138), src:nikayabhedavibhangavyakhyana (Bhavya, D4139), src:samayabhedoparacanacakre-nikayabhedopadesanasamgraha (Vinītadeva, D4140), src:dipavamsa, src:mahavamsa, src:kathavatthu-atthakatha, src:sariputrapariprccha, src:nanhai-jigui-neifa-zhuan, src:xiyu-ji, src:gyagar-chojung-taranatha.
- Teachings: tea:samayabhedoparacanacakra:1–9, tea:dipavamsa:5, tea:cullavagga:12, tea:mahavibhasa:fasc.99, tea:sariputrapariprccha:schism, tea:nanhai-jigui-neifa-zhuan:intro, tea:samayabhedoparacanacakre-nikayabhedopadesanasamgraha:list.
- Dispute: dsp:cause-of-the-first-schism (queued).
- Teachers: tch:mahadeva, tch:yasa-kakandakaputta.

**Sarvāstivāda**
- The seven books: src:jnanaprasthana plus src:prakaranapada, src:vijnanakaya, src:dharmaskandha, src:prajnaptisastra, src:dhatukaya, src:sangitiparyaya. Covered by cpt:seven-abhidharma-books, with Yaśomitra's list checked locally.
- src:mahavibhasa (T1545, 200 fascicles, Xuanzang 656–659), plus src:vibhasa-buddhavarman and src:vibhasa-sitapani.
- The four masters: cpt:four-masters-on-three-times; tea:abhidharmakosa:5.26 and tea:abhidharmakosabhasya:5.26. Teachers tch:dharmatrata, tch:ghosaka, tch:vasumitra, tch:buddhadeva.
- The 75 dharmas: cpt:seventy-five-dharmas and cpt:forty-six-caittas.
- Prāpti: cpt:prapti, trm:prapti.
- Four characteristics of the conditioned: cpt:four-characteristics-of-the-conditioned.
- Avijñapti: cpt:avijnapti-rupa.
- The path:
  - pth:abhidharmakosa-path and pth:abhidharmakosa-four-fruits.
  - cpt:four-nirvedhabhagiyas, cpt:sixteen-moments-of-realization, cpt:noble-persons-abhidharma, cpt:six-kinds-of-arhat.
- Saṅghabhadra: tch:sanghabhadra, src:nyayanusara, src:abhidharmasamayapradipika.
- Manuals: src:abhidharmahrdaya, src:abhidharmahrdaya-upasanta, src:samyuktabhidharmahrdaya, src:abhidharmamrtarasa, src:abhidharmavatara, src:abhidharmadipa.

**Abhidharmakośa (owned: src:abhidharmakosa, plus src:abhidharmakosabhasya)**
- All eight chapters have kārikā teachings, 138 in total (tea:abhidharmakosa:1.1 … 8.41-43).
- Chapter 9 is covered by tea:abhidharmakosabhasya:9.p461, 9.p461/2, 9.p461/3, 9.p462, 9.p469 and 9.p477.
- Commentaries: src:sphutartha-abhidharmakosavyakhya, src:upayika-samathadeva.

**Sautrāntika**
- Critiques in the bhāṣya: tea:abhidharmakosabhasya:1.42, 2.36, 2.40, 2.46, 2.55, 4.2-3, 4.3-4, 5.2, 5.27, 6.58.
- Concepts: cpt:sautrantika-seed-theory, cpt:causeless-destruction, cpt:sutra-as-authority.
- Teachers: tch:kumaralata (src:kalpanamanditika), tch:srilata, tch:harivarman (src:satyasiddhisastra).
- Representationalism: dsp:direct-or-representational-perception (low confidence).

**Mahāsāṃghika and Lokottaravāda**
- Concepts: cpt:supramundane-buddha, cpt:lokanuvartana, cpt:luminous-mind, cpt:mulavijnana.
- Mahāvastu (src:mahavastu): teachings at 1.1, 1.2, 1.76, 1.158-159, 1.167-168, 1.168-169, 3.331-333 and 3.335.
- Path maps: pth:mahavastu-ten-bhumis, pth:mahavastu-four-caryas.
- Branch schools: Caitika, Bahuśrutīya, Prajñaptivāda (lineages above).
- Texts: src:lokanuvartana-sutra; the Lokottaravāda Prātimokṣa, Bhikṣuṇī-Vinaya and Abhisamācārikā.

**Pudgalavāda**
- cpt:pudgala-doctrine, cpt:five-knowables; trm:pudgala, trm:avaktavya, trm:upadaya-prajnapti, trm:bharahara.
- Texts: src:sammitiyanikaya-sastra (T1649), src:tridharmaka-sastra, src:vinaya-dvavimsati-prasannartha-sastra.
- **dsp:pudgala**: sides for the Pudgalavāda, Sautrāntika/Vasubandhu, Sarvāstivāda and Theravāda; queued. Rests on tea:kathavatthu:1.1 and tea:abhidharmakosabhasya:9.*.

**Vinayas**
- The five Vinayas: src:dharmaguptaka-vinaya (T1428), src:mulasarvastivada-vinaya (with src:vinayavastu and src:sanghabhedavastu), src:mahisasaka-vinaya, src:mahasamghika-vinaya, src:sarvastivada-vinaya.
- Prātimokṣa and related texts: the five src:pratimoksa-sutra-* entries, src:kasyapiya-pratimoksa, src:dharmaguptaka-pratimoksa, src:vinayasutra-gunaprabha.
- Rule counts: cpt:vinaya-rule-counts.
- Related concepts: cpt:bhiksuni-ordination-lineages, cpt:tibetan-vinaya-lineages, cpt:preceptor-and-teacher-vinaya.
- Practices: prc:posadha, prc:pravarana, prc:varsavasa, prc:upasampada, prc:pravrajya, prc:apatti-desana, prc:parivasa-manatva, prc:kathina, prc:dhutagunas.
- dsp:bhiksuni-ordination-revival (flagged recent).

**Chinese Āgamas**
- Sources: src:dirghagama (T1), src:madhyamagama (T26), src:samyuktagama (T99), src:samyuktagama-t100, src:samyuktagama-t101, src:ekottarikagama (T125).
- Sanskrit Āgama texts: src:dirghagama-sanskrit, src:nidanasamyukta, src:mahaparinirvanasutra-sanskrit, src:mahavadanasutra, src:catusparisatsutra, src:arthapada-sutra, src:faju-jing.
- cpt:four-agamas.
- 29 textual-parallel borrowings (brw:*-agama-parallel), including MN 10 ↔ MĀ 98 and SN 56.11 ↔ SĀ 379. Both were confirmed from memory at high confidence; they were not checked against a local text.

**Manuscripts**
- src:gandhari-manuscripts, src:british-library-kharosthi-fragments, src:senior-collection, src:bajaur-collection, src:schoyen-collection, src:gandhari-dharmapada (Khotan), src:gandhari-rhinoceros-sutra, src:gilgit-manuscripts, src:turfan-manuscripts, src:udanavarga, src:patna-dharmapada.
- Concepts: cpt:dharmapada-recensions, cpt:gandhari-buddhist-literature, cpt:languages-of-the-early-canons.

**Disputes**
- dsp:existence-in-three-times, dsp:intermediate-existence, dsp:arhat-retrogression, dsp:gradual-or-single-realization, dsp:pudgala, dsp:nature-of-the-buddha, dsp:five-points-of-mahadeva, dsp:original-purity-of-mind, dsp:reality-of-prapti, dsp:reality-of-avijnapti, dsp:reality-of-the-unconditioned, dsp:cause-of-destruction, dsp:abhidharma-as-buddhavacana, dsp:what-sees, dsp:merit-of-gifts-buddha-or-sangha.
- Plus the three already listed (dsp:cause-of-the-first-schism, dsp:bhiksuni-ordination-revival, dsp:direct-or-representational-perception).

**Section D, per lineage (mainly Sarvāstivāda through the Kośa)**
- Ultimate: ult:*.
- Mind: caittas, dissociated formations, cpt:twenty-two-indriyas.
- Self: cpt:pudgala-doctrine; tea:abhidharmakosa:3.18.
- Body and matter: tea:abhidharmakosa:1.9, 1.11, 1.12.
- Obstacles: 15 obs:*.
- Ethics: cpt:eight-pratimoksas; prc:upavasa, prc:saranagamana.
- Karma: cpt:karma-as-volition, cpt:six-causes-four-conditions-five-results.
- Stages: 5 pth:*.
- Powers: cpt:six-abhinnas and cpt:prohibition-of-displaying-powers, both with warnings.
- Teacher and transmission: cpt:preceptor-and-teacher-vinaya, cpt:sarvastivada-succession-of-masters.
- Cosmology: cpt:abhidharmakosa-cosmology, cpt:kalpa-cycle-abhidharmakosa.
- Language: nāmakāya; cpt:four-ways-of-answering-questions.
- Death: cpt:antarabhava; phn:place-of-death-of-mind.
- Decline of the Dharma: cpt:decline-of-the-dharma.

**Corrections to the MUST-COVER list**
- Vasumitra (in Xuanzang's version) counts 20 groups (9 Mahāsāṃghika and 11 Sthavira), not eighteen.
- The seven books' authors differ between Yaśomitra and the Chinese tradition. For example, Dharmaskandha is Śāriputra in Yaśomitra but Maudgalyāyana in the Chinese sources; Dhātukāya is Pūrṇa vs Vasumitra; Saṅgītiparyāya is Mahākauṣṭhila vs Śāriputra.
- The Kośa has about 600 kārikās (597 in the e-text). The ninth chapter is prose and belongs to the bhāṣya.
- The Mahāvastu's second bhūmi reads "baddhamānā" in Senart's text.
- The "five points of Mahādeva" are reported only by the Sarvāstivāda and Theravāda. No Mahāsāṃghika source presents them as its own.
- The Satyasiddhiśāstra survives in Chinese. The Sanskrit text is Aiyaswami Sastri's modern reconstruction.
- Prātimokṣa counts: only the Dharmaguptaka (250/348) and Theravāda (227/311) counts are given with confidence.

## 2. Least-sure items (check first)
- **Doxographic tenets** of the Mahīśāsaka, Dharmaguptaka, Kāśyapīya, Bahuśrutīya, Prajñaptivāda, Kaukkuṭika, Ekavyavahārika and Haimavata. This includes the "nine asaṃskṛtas" of the Mahāsāṃghika and Mahīśāsaka, and tea:samayabhedoparacanacakra:4, 6, 7, 9.
- **Bhavya's three lists** (not detailed) and **Vinītadeva's four-group membership**.
- **Rule counts**: Mahīśāsaka 251, Sarvāstivāda 263, MSV 258 (Tibetan tradition: 253), Mahāsāṃghika 218; the śaikṣa counts.
- **Āgama numbers**: SĀ 810 for MN 118 (low); SĀ 34, SĀ 197, SĀ 470, SĀ 962 and MĀ 106 (moderate); EĀ 43.7, 40.10 and 44.6.
- **Mahāvibhāṣā fascicle refs** (fasc. 77, 99, 27). The Mahāvibhāṣā account of the Vibhajyavādins' luminous mind is also uncertain.
- **Pudgalavāda details:**
  - Śrīlāta's "anudhātu".
  - The three designations in the Saṃmitīyanikāya-śāstra.
  - The Tridharmaka-śāstra's attribution (Vasubhadra, Saṅghasena).
  - The Patna Dharmapada's verse count and Saṃmitīya affiliation.
- **Manuscript collections**: the Senior, Bajaur and Schøyen contents, and the British Library fragment count (29).
- **Other attributions**:
  - The Lokānuvartana-sūtra's Pūrvaśaila affiliation.
  - The Mahāsāṃghika mūlavijñāna, which rests on Asaṅga's report only.
  - T100's Kāśyapīya affiliation.
- **Dates** for Skandhila, Yaśomitra, Guṇaprabha, Vinītadeva, Śrīlāta and Lachen Gongpa Rabsal. Also the Tibetan "upper/lower Vinaya" narrative.
- **dsp:gradual-or-single-realization**: the Theravāda and Mahāsāṃghika "single moment" sides.
- **dsp:bhiksuni-ordination-revival**: the 2007 Hamburg congress details.
- **Aśubhā warning**: that the suicide story appears in every school's Vinaya.
- **Sutta ids referenced by slug rule** that U36 may not create: src:ariyapariyesana-sutta, src:culamalunkya-sutta, src:alagaddupama-sutta, src:kaccanagotta-sutta, src:phenapindupama-sutta, src:nagara-sutta, src:culasunnata-sutta, src:culavedalla-sutta, src:mahapadana-sutta, src:singalaka-sutta, src:culakammavibhanga-sutta.

## 3. Gaps (belong here, not created responsibly)
- **Key texts not extracted:**
  - Teachings from the Jñānaprasthāna, the six pādas, the Mahāvibhāṣā (beyond three fascicle-level items), the Nyāyānusāra and the Śāriputrābhidharma: no local text.
  - Individual Āgama sūtras as separate sources.
  - The Pudgalavāda texts T1649, T1506 and T1505 beyond work-level summaries.
  - Each Mahāvastu bhūmi's contents; the Dīpaṅkaravastu; the Mahāvastu Sahasravarga; the jātakas.
- **Doxography and commentary:**
  - Bhavya's three lists and Tāranātha's lists in detail.
  - The Kathāvatthu commentary's attribution for each kathā.
  - Kośa commentaries: Sthiramati (Tattvārthā), Pūrṇavardhana, Puguang, Fabao.
  - Vasubandhu's Vyākhyāyukti.
  - Śāntarakṣita's Tattvasaṃgraha section on the Vātsīputrīya self (only noted in dsp:pudgala notes).
- **Minor schools not created as separate lineages**: the Uttarāpathakas, Rājagirikas, Siddhārthikas, Vetulyakas, Uttaraśaila, Kaurukullaka, Āvantaka, Jetavanīya and Abhayagirivāsin. Only the Pali-commentary group lin:andhaka exists.
- **Gāndhārī texts not given separate entries**: the Anavatapta-gāthā, the Gāndhārī Ekottarika-type sūtras, the Saṃgīti commentary, the Library of Congress scroll and the Split collection Prajñāpāramitā.
- **Tibetan grub mtha' Sautrāntika subdivisions** ("following scripture / following reasoning"). These are left to U41/U47.
- **Cross-unit ids referenced but not owned here** (to confirm at merge): cpt:bardo, cpt:five-paths, cpt:no-self, cpt:seven-abhidhamma-books, cpt:storehouse-consciousness, cpt:ten-bhumis, trm:alayavijnana, prc:satipatthana. Also dsp:isvara and dsp:is-there-a-self (U50).
- **Dedupe or merge candidates:**
  - My cross-school disputes versus U37's dsp:kv-puggala, dsp:kv-arahant-falling-away, dsp:kv-sabbam-atthi, dsp:kv-arahant-imperfections, dsp:kv-gradual-penetration, dsp:kv-antarabhava, dsp:kv-buddha-in-human-world, dsp:kv-unconditioned-dhammas, dsp:luminous-citta-reading and dsp:authority-of-abhidhamma. Each pair is noted on my entry.
  - Sanskrit-form terms linked to the Pali-form terms (trm:khandha, trm:paticcasamuppada, trm:nibbana …) as exact equivalents: 50 lines logged.
  - Shared ids I contribute to: cpt:three-doors-of-liberation, cpt:six-abhinnas, cpt:dependent-origination, cpt:five-aggregates, cpt:four-noble-truths, prc:nirodha-samapatti; plus trm:asubha and other Sanskrit/Pali slugs that happen to coincide.
- **Recommendation**: add lin:sthavira to merge.py's UMBRELLAS. Member schools keep lin:early-buddhism as parent so that each counts as its own root.

## 4. Out of reach
- CBETA in sources_raw holds only T08, T12, T47 and T48. The following Taishō volumes are missing, so everything drawn from them is from memory:
  - T01–02: the Āgamas.
  - T22–24: the Vinayas.
  - T26–29: Sarvāstivāda Abhidharma and the Kośa translations.
  - T32: the Satyasiddhi.
  - T49: Vasumitra's doxography.
- Derge D4138–4140 (the doxographies) exist locally in Tibetan but were not read in this phase.
- The Gāndhārī critical editions (Gandhāran Buddhist Texts series) are not local.
- Restricted material: none in this unit. The Vinaya's sexual-offence rules appear only as a one-line summary within obs:four-parajikas.
