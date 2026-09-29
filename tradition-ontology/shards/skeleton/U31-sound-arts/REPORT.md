# U31-sound-arts — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


**Scope:** coverage map A12 (sound, language and the arts as paths), plus the D, E, F and G items that touch the four lineages this unit owns: lin:vyakarana, lin:alankara, lin:sangita and lin:mantrasastra.
**Generators:** `_gen/part1…part10*.py` (common helpers in `_gen/common.py`). `_gen/check_refs.py` lists every reference that is defined in no skeleton shard.
**Counts:** lineages 4 · ultimate 4 · sources 76 · teachers 81 · teachings 148 · terms 119 · concepts 38 · practices 19 · obstacles 5 · phenomenology 10 · paths 2 · disputes 12 · borrowings 11 · interpretation_log 36.
**Validator:** 0 errors.

**Local checking:** these texts were checked against local e-texts in sources_raw/:
- Nāṭyaśāstra ch. 1, 6 and 7
- Saṅgītaratnākara 1.1, 1.2, 1.3 and 3.24–26
- Bṛhaddeśī 13–25 and 280–281
- Sāhityadarpaṇa 1.3, 3.1–5 and 3.245–251 (GRETIL)
- Kāvyaprakāśa 1.1–1.3 and the ullāsa 4 bhāva kārikā
- Śāradātilaka 1.7–16 and 2.57–153, with the Padārthādarśa (Muktabodha M00077)

Entries checked this way say so in `notes`. They are still skeleton level, not fidelity-checked.

## 1. Coverage checklist

### A12 — philosophy of language
- **Vākyapadīya:** src:vakyapadiya (three kāṇḍas; the 14 samuddeśas of kāṇḍa 3 are listed in `structure`), src:vakyapadiya-vrtti, src:vakyapadiya-paddhati, src:vakyapadiya-tika-punyaraja, src:prakirnaprakasa, src:mahabhasya-dipika.
- **VP 1.1:** tea:vakyapadiya:1.1 (with original); also 1.2, 1.3, 1.4, 1.5.
- **Śabda-brahman:** cpt:sabda-brahman, trm:sabda-brahman, trm:sabdatattva, ult:vyakarana.
- **Sphoṭa:**
  - teachings: tea:vakyapadiya:1.44, 1/2, 1/3, 1.73; tea:mahabhasya:1.1.70; tea:sphotasiddhi:1-37; tea:vaiyakarana-bhusana-sara:sphotanirnaya; tea:laghumanjusa:sphota
  - concepts and terms: cpt:sphota, cpt:eight-sphotas, trm:sphota, trm:dhvani
- **Pratibhā:** tea:vakyapadiya:2.143-145, 2.146-152; cpt:pratibha-vyakarana; trm:pratibha; phn:pratibha-flash.
- **Levels of speech:**
  - teachings: tea:vakyapadiya:1.142, tea:vakyapadiya-vrtti:1.142, tea:laghumanjusa:sphota (Nāgeśa's four levels in the body)
  - concept and terms: cpt:levels-of-speech (U31 definitions added for VY, MS and SG), trm:vaikhari, trm:madhyama, trm:pasyanti, trm:para-vak
  - The parā level of the Kashmir Śaivas and Somānanda's critique are referenced to U19 through dsp:pasyanti-brahman (tea:sivadrsti:2.1, tea:isvarapratyabhijna-karika:1.5.13).
- **Mahābhāṣya:**
  - Purposes of grammar: U02's tea:mahabhasya:paspasa/2 is referenced.
  - Additions: tea:mahabhasya:paspasa/6 (siddhe śabdārthasambandhe), tea:mahabhasya:1.1.70 (sphoṭa/dhvani), tea:mahabhasya:1.2.64 (ākṛti vs dravya).
- **Commentators and later grammarians:**
  - Maṇḍana (src:sphotasiddhi, tch:mandana-misra), Bharata Miśra, the Gopālikā
  - Helārāja, Puṇyarāja, Vṛṣabhadeva, Kaiyaṭa (src:mahabhasya-pradipa, contribution), Nāgeśa's Uddyota
  - Bhaṭṭoji (src:vaiyakarana-siddhanta-karika)
  - Kauṇḍa Bhaṭṭa (src:vaiyakarana-bhusana, src:vaiyakarana-bhusana-sara)
  - Nāgeśa (src:vaiyakarana-siddhanta-manjusa, src:laghumanjusa, src:paramalaghumanjusa, src:sphotavada-nagesa)
  - Early names: tch:vyadi, tch:vajapyayana, tch:sphotayana, tch:audumbarayana, tch:candracarya, tch:vasurata
- **Mīmāṃsā's rejection of sphoṭa:** dsp:sphota (full record with both sides, referencing U12's tea:sabara-bhasya:1.1.5/4 and tea:slokavarttika:sphotavada.134-137), plus Śaṅkara's tea:brahma-sutra-bhasya-sankara:1.3.28.

### A12 — nāda
- **Āhata and anāhata nāda:** cpt:ahata-anahata, trm:ahata-nada, trm:anahata-nada.
- **Nāda–bindu–kalā:** cpt:nada-bindu-kala (ŚT 1.7–16) and cpt:nada-kalas-of-uccarana (U31 definition added).
- **Nāda in general:** cpt:nada (U31 definitions for SG and MS).
- **Haṃsa and Nādabindu ten sounds and stages:** linked, not duplicated. See the note on cpt:nada and prc:nadopasana, which point to U04's tea:hamsa-upanisad:4-ten-sounds and tea:nadabindu-upanisad:33-35, and to U28/U29's HYP 4.65–69 and pth:hyp-nada-four-stages.

### A12 — music
- **Saṅgītaratnākara:** src:sangita-ratnakara (seven adhyāyas).
  - Nāda and the body: tea:sangita-ratnakara:1.2.1-3, 1.2.4-7, 1.2.8-10, 1.2.11-12, 1.2.14-17
  - Centres: tea:sangita-ratnakara:1.2.120-139, 1.2.140-144; cpt:sangita-ratnakara-centres (a ten-centre system)
  - Music and liberation: tea:sangita-ratnakara:1.2.163-167
  - Nāda-brahman and nāda: 1.3.1-2, 1.3.3-5, 1.3.6
  - The 22 śrutis and 7 svaras: 1.3.7-10, 1.3.11-22, 1.3.23-25
  - Singers' faults: 3.24-26
  - Commentaries: src:sangita-ratnakara-kalanidhi, src:sangita-sudhakara
- **Other treatises:**
  - Bṛhaddeśī: src:brhaddesi (tea:brhaddesi:13, 16-19, 20-21, 22-25, 280-281)
  - Nāradīya Śikṣā: src:naradiya-siksa (contribution; U01's teachings referenced)
  - Dattila: src:dattilam, tch:dattila
  - Later treatises: Nānyadeva, Pārśvadeva, Someśvara III, Kumbhā, Rāmāmātya, Somanātha, Veṅkaṭamakhin, Govinda Dīkṣita, Ahobala, Dāmodara, Puṇḍarīka Viṭṭhala, the Saṅgītamakaranda
- **Music as a path:**
  - cpt:music-as-path, prc:nadopasana, cpt:nada-brahman, ult:sangita
  - tea:yajnavalkyasmrti:3.116 (U02's 3.115 is referenced)
  - Tyāgarāja (U26) is referenced: contribution to tch:tyagaraja, plus two low-confidence teachings on src:tyagaraja-krtis
  - Composers (contributions): tch:muttusvami-diksitar, tch:syama-sastri, tch:purandara-dasa, tch:svami-haridas, tch:tansen, tch:annamacarya
  - New composer entries: tch:ksetrayya, tch:svati-tirunal (recent)

### A12 — aesthetics
- **Nāṭyaśāstra:** src:natyasastra (structure recorded).
  - Teachings: tea:natyasastra:1.11-12, 1.14-16, 1.17, 1.106-107, 1.108-113, 1.114, 1.115-116, 3, 5, 6.15-16, 6.17, 6.18-21, 6.22, 6.31-prose (the rasa-sūtra), 6.32-33, 6.36-38, 6.39-41, 6.82-santa, 7.1-3, 28, 36
- **Rasa and bhāva:**
  - Concepts: cpt:rasa-sutra, cpt:bhava-theory, cpt:nine-rasas
  - Terms: trm:rasa, trm:bhava-alankara, trm:vibhava-alankara, trm:anubhava-alankara, trm:vyabhicari-bhava, trm:sthayibhava, trm:sattvika-bhava
- **Śānta debate:** dsp:santa-rasa, cpt:santa-rasa, trm:santa-rasa.
- **Lollaṭa, Śaṅkuka, Bhaṭṭa Nāyaka:**
  - Their views: tea:abhinavabharati:6.rasasutra.lollata, .sankuka, .bhatta-nayaka (reported_by_opponent)
  - Bhaṭṭa Nāyaka's powers: trm:bhavakatva, trm:bhojakatva
  - Tasting Brahman: trm:brahmasvada-sahodara
- **Abhinavagupta:**
  - Sources: src:abhinavabharati, src:dhvanyaloka-locana
  - Teachings: tea:abhinavabharati:6.rasasutra.abhinavagupta, .vighnas, .steps, 6.santa; tea:dhvanyaloka-locana:1.5
  - Camatkāra and the likeness to tasting Brahman: trm:camatkara, cpt:rasa-as-relish-of-consciousness, phn:rasa-camatkara
- **Ānandavardhana:** src:dhvanyaloka (tea:dhvanyaloka:1.1, 1.4, 1.5, 1.13, 3.26-vrtti, 4.5-vrtti), cpt:dhvani-theory.
- **Mammaṭa:** src:kavyaprakasa (tea:kavyaprakasa:1.1, 1.2, 1.3, 4.rasasutra, 4.bhava, 4.santa).
- **Viśvanātha:** src:sahityadarpana (tea:sahityadarpana:1.3, 3.1, 3.2-3, 3.3-vrtti, 3.4-5, 3.245-250, 3.251).
- **Also:**
  - Bhāmaha, Daṇḍin, Vāmana, Udbhaṭa, Rudraṭa, Kuntaka, Mahimabhaṭṭa
  - Dhanañjaya and Dhanika, Bhoja, Kṣemendra, Ruyyaka
  - Jagannātha, Rājaśekhara, the Nāṭyadarpaṇa, Hemacandra
  - Śāradātanaya, the Abhinayadarpaṇa, Bhavabhūti
- **Link to bhakti-rasa:** dsp:is-bhakti-a-rasa (U31 adds the alaṅkāra side with the KP 4 anchor). Concept relations go to cpt:bhakti-rasa-components and cpt:five-devotional-rasas (U16).

### A12 — mantra theory
- **Mātṛkā and its placement:**
  - Teaching: tea:saradatilaka:1.14
  - Concept, practice and term: cpt:matrka-and-malini (U31 definition), prc:matrka-nyasa, trm:matrka
  - Nyāsa contribution: prc:nyasa
- **Bīja of the centres and elements:** cpt:bija-of-centres-and-elements, prc:bija-mantras-of-centres-and-elements, trm:bija.
- **Oṃ:**
  - Practice: prc:pranava-japa, whose sources cover Māṇḍūkya 1 and 8–12, YS 1.27–29, Kaṭha 1.2.15–17, Praśna 5, Muṇḍaka 2.2.3–4, Taittirīya 1.8, Maitrī 6.22–23, BhG 8.13, MK 1.25 and Gopatha 1.1.16–30 (all teachings owned by other units)
  - Concept and term: cpt:pranava, trm:pranava
- **Gāyatrī:** prc:gayatri-japa (RV 3.62.10, VS 36.3, MDh 2.76–78, BĀU 5.14, ChU 3.12), trm:gayatri.
- **Mahāmṛtyuñjaya:** prc:mahamrtyunjaya-japa (RV 7.59.12, TS 1.8.6, VS 3.60), trm:tryambaka.
- **Kinds of japa:**
  - Teaching: tea:padarthadarsa:16/japa (Rāghavabhaṭṭa quoting the Vāyavīya Saṃhitā)
  - Practices: prc:japa, prc:vacika-japa, prc:upamsu-japa, prc:manasa-japa
- **Manuals:**
  - Śāradātilaka: src:saradatilaka (contribution); teachings 1.8-9, 1.10-11, 1.12-13, 1.14, 1.15-16, 2.57-59, 2.60-63, 2.64-70, 2.112-123, 2.141-144, 2.145-153
  - Other manuals: src:padarthadarsa, src:prapancasara (contribution), src:prapancasara-vivarana, src:mantramahodadhi, src:mantramaharnava
- **Defects and purifications:** obs:mantra-dosas (49 members, from the text), prc:mantra-samskara (summary only), trm:mantra-dosa, trm:mantra-samskara.
- **Initiation, testing and secrecy:**
  - cpt:mantra-diksa-and-secrecy, cpt:mantra-sodhana, prc:mantra-diksa
  - trm:gopana, trm:diksa
- **Also added:**
  - cpt:classes-of-mantras
  - cpt:six-rites-of-mantra (classification only; no procedures)
  - prc:purascarana (contribution), pth:purascarana-five-limbs
  - phn:mantra-awakening

### E — practices this unit owns
- Mantra repetition: prc:japa, plus its three modes (prc:vacika-japa, prc:upamsu-japa, prc:manasa-japa).
- Oṃ, Gāyatrī and Mahāmṛtyuñjaya: prc:pranava-japa, prc:gayatri-japa, prc:mahamrtyunjaya-japa.
- Seed syllables of the centres and elements: prc:bija-mantras-of-centres-and-elements.
- Devotional singing: prc:kirtana and prc:bhajana, with signs (phn:kirtana-ecstasy) and warnings (Śikṣāṣṭaka 3).
- Also: prc:nadopasana, prc:matrka-nyasa, prc:mantra-diksa, prc:mantra-samskara, prc:vyakarana-study, prc:ranga-puja, prc:purvaranga.
- Equivalences to the other units' ids are logged.

### D — concept checklist, by lineage
- **Vyākaraṇa:**
  - ultimate: ult:vyakarana, cpt:sabda-brahman
  - consciousness: cpt:word-permeated-cognition
  - self: trm:vagrupata
  - mind: cpt:pratibha-vyakarana
  - matter: cpt:jati-dravya
  - obstacles: obs:vang-mala
  - ethics: trm:sadhu-sabda, trm:apasabda
  - liberation: cpt:grammar-as-path
  - path map: pth:vyakarana-sabdapurva-yoga
  - signs: phn:seers-vision
  - transmission: tea:vakyapadiya:2/2, trm:agama
  - time and cosmology: cpt:kala-sakti, tea:vakyapadiya:1/6
  - sound: all of the above
  - disputes: see G
- **Alaṅkāra:**
  - ultimate: ult:alankara (with caveat)
  - consciousness: cpt:rasa-as-relish-of-consciousness
  - self: cpt:sadharanikarana
  - mind: cpt:bhava-theory
  - body: phn:sattvika-signs
  - obstacles: obs:rasa-vighnas, obs:kavya-dosas
  - ethics: cpt:purposes-of-poetry, cpt:natya-as-fifth-veda
  - liberation: cpt:santa-rasa
  - transmission: tea:natyasastra:1.*, tea:natyasastra:36
- **Saṅgīta:**
  - ultimate: ult:sangita, cpt:nada-brahman
  - self: tea:sangita-ratnakara:1.2.4-7 and 1.2.11-12
  - body: cpt:sangita-ratnakara-centres, phn:sr-petal-states
  - cosmology: tea:sangita-ratnakara:1.2.8-17
  - obstacles: obs:gayaka-dosas
  - liberation: cpt:music-as-path
  - signs: phn:sr-music-success-petals
  - transmission: tea:sangita-ratnakara:1.1.15-20
- **Mantraśāstra:**
  - ultimate: ult:mantrasastra
  - consciousness and self: tea:saradatilaka:1.12-13 and 1.14
  - body: cpt:bija-of-centres-and-elements
  - obstacles: obs:mantra-dosas
  - liberation: trm:bhukti-mukti (referenced)
  - signs: phn:mantra-awakening
  - transmission: cpt:mantra-diksa-and-secrecy
  - cosmology: cpt:nada-bindu-kala
  - powers: cpt:six-rites-of-mantra
- **Death and dying:** only indirect coverage: Oṃ at death (BhG 8.13, cited in prc:pranava-japa), the Mahāmṛtyuñjaya, and "death" among the 33 vyabhicāribhāvas. None of the four lineages has a death doctrine of its own in the texts used (see gaps).

### F — path maps
- pth:vyakarana-sabdapurva-yoga (low confidence; reconstructed).
- pth:purascarana-five-limbs (low confidence; a ritual sequence).
- The nāda stages (pth:hyp-nada-four-stages) are left to U29/U51.

### G — debates
- dsp:sphota, dsp:pasyanti-brahman, dsp:is-the-ultimate-speech, dsp:sentence-meaning and dsp:eternality-of-sound: queued, with candidate readings.
- dsp:jati-or-vyakti (P2), dsp:how-rasa-arises (P4, Abhinava's own "ladder"), dsp:santa-rasa (P2), dsp:dhvani-vyanjana (P2), dsp:one-rasa-or-many (P2), dsp:is-rasa-bliss (P2) and dsp:is-bhakti-a-rasa (P2): partially reconciled, with tradition_objections recorded.
- The orchestrator should add the five queued disputes to RECONCILE_QUEUE.md.

## 2. Corrections to the brief's MUST-COVER list
- **Levels of speech:** the fourth level (parā) was not added only by the Kashmir Śaivas. The mantra manuals have it, and so does the grammarian Nāgeśa, who locates parā, paśyantī, madhyamā and vaikharī in the root centre, navel, heart and throat. Bhartṛhari himself names three.
- **Nāṭyaśāstra's śānta passage:** it occurs only in some recensions; in the edition used, the same chapter still says "eight rasas" (6.15). The śānta passage is placed after 6.82, and scholars take it as an addition. The edition used has 36 chapters; others have 37.
- **"Twin of tasting Brahman":** the phrase brahmāsvāda-sahodara is Viśvanātha's (SD 3.2). Bhaṭṭa Nāyaka's comparison (as Abhinava reports it) is that the enjoyment is akin to tasting the supreme Brahman.
- **Puṇyarāja:** his authorship of the Vākyakāṇḍa commentary is disputed. It is recorded as such.
- **Kaṭha reference:** "Kaṭha 1.2.15–16" is anchored to U03's existing teaching tea:katha-upanisad:1.2.15-17.
- **Saṅgītaratnākara's centres:** the text has ten centres, not six. It adds lalanā, manas and soma. It also teaches that particular petals give or destroy success in music (1.2.140–144).

## 3. Least-sure items (check these first for hallucination)
- **Vākyapadīya verse numbers.** Numbering follows Iyer; Rau's edition differs in kāṇḍa 1. Low confidence: 1.9, 1.12, 1.23, 1.30, 1.37, 1.46, 1.142. Some verses are located by content only (ids 1/2–1/6 and 2/2). Samuddeśa-level refs: 3.3, 3.9. The Vṛtti's "śabdapūrva-yoga" location (tea:vakyapadiya-vrtti:1.14) is also uncertain.
- **Other alaṅkāra verse numbers:**
  - Vakroktijīvita 1.7
  - Daśarūpaka 4.35
  - Sarasvatīkaṇṭhābharaṇa 5.1 (Bhoja's "one rasa")
  - Aucityavicāracarcā 5
  - Abhinayadarpaṇa 37
  - Nāṭyadarpaṇa ch. 3
  - Dhvanyāloka 3.26 vṛtti
  - SD 3.3 vṛtti (Nārāyaṇa)
  - ABh "ladder" verse (tea:abhinavabharati:6.rasasutra.steps)
- **Tyāgarāja paraphrases** (Nāda tanum aniśam; Mokṣamu galadā): recalled from memory.
- **Low-confidence sources and teachers:**
  - Bharata Miśra's Sphoṭasiddhi; the Gopālikā and Ṛṣiputra Parameśvara
  - the Paddhati and Vṛṣabhadeva; Vasurāta; Candrācārya
  - Pārśvadeva's sect (recorded as Digambara, low confidence)
  - Saṅgītasudhā (ascription disputed)
  - Saṅgītamakaranda (date unknown)
  - Mantramahārṇava (compiler and date unknown)
  - Bodhendra Sarasvatī and Śrīdhara Ayyāvāḷ (dates are traditional)
- **Prabhācandra and the Prameyakamalamārtaṇḍa:** the śabdādvaita refutation is recorded at work level only.
- **Tattvasaṅgraha Śabdabrahma-parīkṣā:** the argument is summarized from memory.
- **Path maps:** the five-limb scheme of puraścaraṇa and its tenth-proportions, and the stage order of pth:vyakarana-sabdapurva-yoga.
- **Saṅgītaratnākara 3.24–26:** the adhyāya and verse locator is taken from the e-text's section numbering; glosses of some of the fault names are from memory.
- **Mahāmṛtyuñjaya seed-syllable forms:** deliberately not given.

## 4. Gaps (could not responsibly create)
- **Mantramahodadhi and Prapañcasāra:** no verse-level teachings. I don't reliably know the taraṅga and paṭala mapping (Mṛtyuñjaya section, the six rites, the general rules).
- **Verse-level anchors** are still needed for the Sphoṭasiddhi kārikās, the Mañjūṣā sections and the Kāvyaprakāśa rasa kārikās.
- **Tamil music theory** (paṇ; the Cilappatikāram and Aṭiyārkkunallār; paṇ in the Tēvāram): not created. Should be assigned to a Tamil unit.
- **South Indian nāma-bhajana tradition:** the works of Bodhendra and Śrīdhara Ayyāvāḷ (titles uncertain) and Marudanallur Sadguru Svāmī's bhajana-paddhati are not created.
- **Bhānudatta** (Rasataraṅgiṇī, Rasamañjarī), **Śiṅgabhūpāla's Rasārṇavasudhākara** and **Ramānanda Rāya's** use of rasa: not created.
- **Lost works:** Kohala's, the Candrikā on the Dhvanyāloka and Bhaṭṭa Tauta's work are listed as lost, or not created.
- **Bhartṛhari's Śabdadhātusamīkṣā:** its existence is uncertain, so it was omitted.
- **Death and dying** has no dedicated doctrine in the four lineages as far as I know. There may be specific death-bed rules for mantras; unverified.
- **Mantra manuals' own warnings** about the six rites, and ethical restrictions on them: not recorded.
- **Recent musicologists** (Bhātkhaṇḍe, Paluskar): not included. Flag for inclusion or exclusion.

## 5. Out of reach
- **Oral transmission:** the oral pedagogy of rāga and of mantra dīkṣā is secret by rule (ŚT 2.122–123), so the real content of mantra "purifications" and puraścaraṇa is transmitted orally.
- **Manuscript-only and damaged texts:** the Mahābhāṣyadīpikā (single damaged manuscript); parts of the Bṛhaddeśī and the Vakroktijīvita are lost.
- **Not digitized locally:** no Vākyapadīya e-text was available in sources_raw/ at this phase.
- **Restricted material:** none of the practices here fall under the restricted list. Kuṇḍalinī-related seed-syllable work carries the text's own warning (ŚCN 50–54). The six rites are recorded as a classification only.

## 6. Cross-unit notes for the merge
- **Duplicate ids, recommended merges** (each logged as an equivalence):
  - trm:sabdabrahman (U19) → trm:sabda-brahman
  - trm:om and trm:omkara → trm:pranava
  - cpt:om (U05) → cpt:pranava
  - trm:bhajan (U27) → trm:bhajana
  - prc:japa-kinds (U04) and prc:japa-three-kinds (U02) → prc:japa
  - prc:pranava-upasana, prc:pranava-dhyana and prc:omkara-dhyana → prc:pranava-japa
  - prc:bhuta-suddhi → prc:bhutasuddhi
- **Homonym collisions, disambiguated here:**
  - U16 uses trm:vibhava and trm:anubhava for the aesthetic vibhāva and anubhāva, but U08/U14 use trm:vibhava for Pāñcarātra vibhava, and U11/U20 use trm:anubhava for "experience". U31 created trm:vibhava-alankara and trm:anubhava-alankara; U16's aesthetic definitions should move to them.
  - Also disambiguated: trm:bhava-alankara, trm:raga-sangita (vs trm:raga = passion), trm:jati-sangita, trm:mela-raga (vs trm:mela = festival), and src:sarasvatikanthabharana-alankara (vs Bhoja's grammar of the same name).
- **Shared entities to which U31 contributed only its lineage's content:**
  - Sources: src:mahabhasya, src:mahabhasya-pradipa, src:naradiya-siksa, src:nandikesvara-kasika, src:saradatilaka, src:prapancasara, src:isanasivagurudevapaddhati, src:sarvadarsanasangraha, src:tattvasangraha
  - Teachers: tch:vyadi, tch:kaiyata, tch:mandana-misra, tch:bhattoji-diksita, tch:nagesa-bhatta, tch:abhinavagupta, tch:bhoja, tch:hemacandra, tch:narada, tch:nandikesvara, tch:bhatta-tauta, the composers, tch:laksmana-desika, tch:raghavabhatta, tch:mahidhara, tch:sankara
- **Registry ids referenced but not yet defined** (their owning units have not run): tch:santaraksita, lin:pramana-buddhist, lin:yogacara-madhyamaka, lin:dasanami, lin:smarta, lin:haridasa-karnataka, dsp:causation, dsp:world-real-or-appearance, dsp:number-of-pramanas, dsp:women-caste-liberation.
- **Teaching-id suffixes:** tea:mahabhasya:paspasa/6 continues U02's /2–/5 series. tea:nirukta:1.1/2 continues U02's tea:nirukta:1.1. tea:nandikesvara-kasika:1/2 repeats U02's verse 1 with its original text.
