# U12-mimamsa — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Everything is at `verification.level: skeleton`. Wording and verse/sūtra numbers were checked against local e-texts in `sources_raw/raw_etexts` (GRETIL Śābarabhāṣya adhyāyas 1–7; ebhāratī Mīmāṃsā Sūtra, all 12 adhyāyas; the Benares 1910 OCR of MS with Śabara; Ślokavārttika with Nyāyaratnākara and with Kāśikā; Tantravārttika 1.2–3.8; Prakaraṇapañcikā; Śāstradīpikā tarkapāda; Arthasaṅgraha; Mīmāṃsānyāyaprakāśa; Nyāyamālāvistara 1–4; Bhāṭṭadīpikā with Prabhāvalī 1.2–3.3).
- The 99 `original` fields were copied by script (`_gen/originals_final.json`, transliterated by `_gen/translit.py`).
- Passages where the e-texts have typos or OCR damage were left without an original.
- Generators: `_gen/part1…part9`. Re-run from `tradition-ontology/`.

## 1. Coverage checklist (A5 Mīmāṃsā + D/E/F/G for my lineages)

**Lineages**
- lin:mimamsa; lin:bhatta-mimamsa; lin:prabhakara-mimamsa.
- lin:murari-mimamsa is a new sub-lineage for Murāri's "third path".
- Views of the ultimate: ult:mimamsa, ult:bhatta-mimamsa, ult:prabhakara-mimamsa, ult:murari-mimamsa. All set `tradition_denies_single_ultimate: true`, with the caveat that classical Mīmāṃsā posits no Vedāntic ultimate.

**Texts**
- Jaimini's MS: src:mimamsa-sutra (12 adhyāyas and 60 pādas; the twelve topics are in tea:jaiminiya-nyayamala:1.1.11-12).
- Saṅkarṣa-kāṇḍa: src:sankarsa-kanda; Devasvāmin's commentary: src:sankarsa-kanda-bhasya.
- Upavarṣa: tch:upavarsa, src:upavarsa-vrtti (lost). The Vṛttikāra: tch:vrttikara-mimamsa. Also tch:bhavadasa / src:bhavadasa-vrtti and tch:bhartrmitra.
- Śabara: src:sabara-bhasya.
- Kumārila: src:slokavarttika, src:tantravarttika, src:tuptika, src:brhattika (lost).
- Prabhākara: src:brhati (extant only to adhyāya 6), src:laghvi (lost).
- Maṇḍana: src:vidhiviveka, src:mimamsanukramani, src:bhavanaviveka, src:vibhramaviveka, src:sphotasiddhi.
- Śālikanātha: src:prakaranapancika, src:rjuvimala, src:dipasikha.
- Umbeka: src:tatparyatika-umbeka.
- Pārthasārathi: src:sastradipika, src:nyayaratnakara, src:nyayaratnamala, src:tantraratna.
- Someśvara: src:nyayasudha-somesvara (the Rāṇaka, a different work from Jayatīrtha's src:nyayasudha).
- Khaṇḍadeva: src:bhattadipika, src:mimamsa-kaustubha, src:bhattarahasya.
- Āpadeva: src:mimamsanyayaprakasa. Laugākṣi Bhāskara: src:arthasangraha.
- Murāri Miśra: src:tripadinitinayana, src:angatvanirukti.
- Others: Nyāyamālā, Nyāyakaṇikā, Tattvabindu, Kāśikā, Nayaviveka(+Dīpikā), Prābhākaravijaya, Tantrarahasya, Seśvaramīmāṃsā, Mīmāṃsāpādukā, Vidhirasāyana, Upakramaparākrama, Mānameyodaya, Mīmāṃsāparibhāṣā, Bhāṭṭacintāmaṇi, Mīmāṃsābālaprakāśa, Prabhāvalī, and others. Matching teachers exist for all.

**Concepts and teachings**
- MS 1.1.1: tea:mimamsa-sutra:1.1.1 and tea:sabara-bhasya:1.1.1.
- MS 1.1.2: tea:mimamsa-sutra:1.1.2 and tea:sabara-bhasya:1.1.2, 1.1.2/2 (Śyena), 1.1.2/3.
- MS 1.1.4–5: tea:mimamsa-sutra:1.1.4, 1.1.5; cpt:autpattika-sambandha.
- Eternality of words: 1.1.6-11, 1.1.12-17, 1.1.18, 1.1.19-23; cpt:eternality-of-sound.
- Authorlessness of the Veda: 1.1.27-28, 1.1.29, 1.1.30, 1.1.31; ŚV vakya.366; cpt:apauruseyatva.
- Intrinsic validity: ŚV codana.47, codana.53, codana.62; ŚD 1.1.2, 1.1.5; cpt:intrinsic-validity and cpt:validity-of-cognition.
- The five kinds of Vedic sentence: cpt:vedic-sentence-types; tea:arthasangraha:veda; tea:mimamsanyayaprakasa:veda.
- Kinds of injunction: cpt:kinds-of-vidhi and cpt:apurva-niyama-parisankhya (Arthasaṅgraha vidhi and niyama-parisankhya).
- Arthavāda and its types: MS 1.2.1, 1.2.7, 1.2.10, 4.3.1; tea:arthasangraha:arthavada.
- Apūrva: MS 2.1.5 with Śabara; cpt:apurva.
- Nitya / naimittika / kāmya acts: cpt:classification-of-acts; ŚV sambandhaksepaparihara.108-111; TV 1.3.24-29.
- Adhikaraṇa method: cpt:adhikarana-method; tea:jaiminiya-nyayamala:1.1.7-8.
- Six marks of purport: cpt:six-marks-of-purport (see the correction in §2).
- Six vs five means of knowledge: tea:sabara-bhasya:1.1.5 (the Vṛttikāra's list of six); ŚV abhava.1-4; tea:prakaranapancika:6; cpt:means-of-knowledge, cpt:arthapatti, cpt:anupalabdhi, cpt:kinds-of-absence.
- Abhihitānvaya vs anvitābhidhāna: tea:sabara-bhasya:1.1.25; ŚV vakya.342-343; tea:prakaranapancika:7.
- Akhyāti vs viparītakhyāti: tea:prakaranapancika:3, 6/2; tea:sastradipika:1.1.5/2.
- The self: Śabara 1.1.5/3; ŚV atmavada.148; PP 8; cpt:self.
- Liberation, with heaven as the earlier goal: MS 4.3.15; Śabara 6.1.1-2; ŚV sambandhaksepaparihara.102-104, 105-107, 108-111; ŚD 1.1.5/4-/8; PP 8/2-8/4; cpt:liberation, cpt:svarga.
- Deities: MS 9.1.6-8, 9.1.9 with Śabara; cpt:deity.
- No creator and no total dissolution: ŚV sambandhaksepaparihara.42-47, 52-55, 66-68, 113; PP 7/2; cpt:isvara, cpt:creation-and-dissolution.
- Critique of omniscience: ŚV codana.110-112, 117-118, 130; cpt:omniscience, cpt:yogic-perception.
- Also covered: eligibility (MS 6.1.x), subsidiarity (MS 3.3.14), sequence, transfer and cancellation, bhāvanā, niyoga, authority of smṛti and of Buddhist texts (TV 1.3.4, 1.3.4/2, 1.3.6), mantra, names of rites, theistic dedication (Arthasaṅgraha and MNP conclusions).

**Practices, obstacles, path maps, phenomenology**
- 14 prc (the Śyena and Agnīṣomīya entries are `restricted`, summary only). 7 obs.
- pth:mimamsa-vedic-dharma-life, pth:kumarila-moksa, pth:prabhakara-moksa.
- 3 phn.

**Disputes**
- New ids: dsp:siddha-or-sadhya, dsp:omniscience, dsp:eternality-of-sound, dsp:sphota, dsp:sentence-meaning, dsp:akhyati-or-viparitakhyati, dsp:meaning-of-injunction, dsp:how-cognition-is-known, dsp:self-known-as-object, dsp:creation-and-dissolution, dsp:purva-uttara-mimamsa-unity, dsp:nitya-karma-result, dsp:bliss-in-liberation, dsp:sacrificial-killing, dsp:external-objects, dsp:apoha. All are `queued` with candidate readings.
- The Bhāṭṭa–Prābhākara disputes are among these new ids.
- U50 disputes are referenced but not written: dsp:status-of-veda, dsp:works-knowledge-grace, dsp:is-there-a-self, dsp:isvara, dsp:number-of-pramanas, dsp:women-caste-liberation.

**Brahma Sūtra passages**
- The Vedānta side of these disputes needed text anchors, so I emitted teachings for BS 1.3.31, 3.2.40, 3.4.2, 3.4.8, 3.4.18, 4.3.12, 4.4.5 and BSBh 1.1.4, 3.3.53. These ids may overlap with U13's.

## 2. Corrections to the assigned list, and items least sure (check these first)

**Corrections**
- **Six marks of purport:** the versified list *upakramopasaṃhārāv…* is cited by Vedānta authors (Madhva at BSBh 1.1.4 ascribes it to a "Bṛhatsaṃhitā"). I did not find it as a list in the Mīmāṃsā texts consulted. Mīmāṃsā supplies the criteria (MS 1.2.7, 1.4.29, 2.2.2, 4.3.1; the Upakramaparākrama), and the concept is recorded that way.
- **Omniscience "against Buddha and Mahāvīra":** ŚV codanā 110–136 names only "the Buddha and others" (v. 130). I found no verse naming Mahāvīra; Jain authors reply to Kumārila.
- **"Periodic dissolution":** Kumārila rejects a total dissolution and a first creation ("creation and dissolution as today", ŚV 113). His Tantravārttika still speaks of Manus in every kalpa, so this is recorded as unresolved within his works. Śālikanātha (PP ch. 7) rejects them too.
- **Liberation as "cessation of the body":** this is the Prābhākara formulation (*dehoccheda*). The Bhāṭṭa one (Pārthasārathi) is the dissolution of the threefold bond, without bliss. The Śāstradīpikā also reports an opposing Bhāṭṭa view that release has bliss.
- **Six pramāṇas:** the list already appears in the Vṛttikāra passage quoted by Śabara, before Kumārila.
- **Śabara's six means of distinguishing rites:** a different word, repetition, number, quality, context (prakriyā) and name.
- **Adhikaraṇa members:** the Nyāyamālā's list is subject, doubt, connection (saṅgati), prima facie view and conclusion.
- **Titles:** Murāri's work is *Tripādīnītinayana*, and the Aṅgatvanirukti's attribution is disputed. Khaṇḍadeva's second work is titled *Mīmāṃsākaustubha* in the e-text. Āpadeva is Anantadeva's son. His MNP ends by dedicating dharma to Govinda; the Arthasaṅgraha repeats this with "Īśvara".
- **MS size:** c. 2,700 sūtras (one e-text yields c. 2,720).

**Least sure — possible hallucinations**
- Hagiography: Kumārila's fall and husk-fire, Prabhākara's title "Guru", the Śabara legends, Ubhaya-Bhāratī.
- Most later dates.
- Low-confidence sources and teachers: Śarkarikā/Jayamiśra, Ajitā/Paritoṣa, Tautātitamatatilaka/Bhavadeva, Dīpaśikhā, Mayūkhamālikā, Yuktisnehaprapūraṇī, Adhvaramīmāṃsākutūhalavṛtti, Bhāṭṭabhāṣāprakāśa/Nārāyaṇa Tīrtha, Saṅkarṣa authorship and state, Devasvāmin, the Mānameyodaya authorship, the Tuptīkā's extent.
- Doctrinal items: cpt:categories (low); the Kumārila side of dsp:self-known-as-object; the Prābhākara side of dsp:nitya-karma-result; the Bhāṭṭa and Sāṃkhya sides of dsp:sacrificial-killing; Maṇḍana's iṣṭasādhanatā (Vidhiviveka not read); Gaṅgeśa's report of Murāri's view; the "vyavahāre bhāṭṭanayaḥ" maxim.
- BS sūtra numbers (Śaṅkara's recension); the Śrībhāṣya Vṛttikāra quote (cited only in a dispute side).

## 3. Gaps (belong here but not responsibly created)
- MS adhyāyas 7–12 have only opening teachings; the sense of 6.1.3, 11.1.1 and 12.1.1 was not checked.
- Not read: Bṛhatī content, Ṭupṭīkā, Tantraratna, Rāṇaka, Vidhiviveka, Bhāvanāviveka, Vibhramaviveka, Tattvabindu, Mānameyodaya, Nayaviveka.
- The ŚV Ātmavāda doctrine that the self is the object of the I-notion needs checking.
- Bhāṭṭa subdivisions of apūrva are noted but not attached to a teaching.
- Many 16th–18th c. authors (Rāja Cūḍāmaṇi Dīkṣita, Veṅkaṭādhvarin, Kamalākara Bhaṭṭa, Devanātha Ṭhakkura, Halāyudha, and others) were not created.
- Post-1800 Mīmāṃsakas (e.g. A. Chinnaswami Sastri, Paṭṭābhirāma Śāstrī) were not created (`recent`).
- Kāśakṛtsna (possible Saṅkarṣa author) was not created.
- **For U50:** the Śaṅkara–Maṇḍana debate (Śaṅkaradigvijaya) belongs in dsp:works-knowledge-grace.historical_debates.
- **For the merge:** possible dedupe of shared concept ids (cpt:self, cpt:liberation, cpt:isvara, cpt:deity, cpt:karma, cpt:rebirth, cpt:mind, cpt:means-of-knowledge, cpt:omniscience, cpt:yogic-perception, cpt:categories, cpt:states-of-consciousness, cpt:six-marks-of-purport).
- Term ids that clash with other senses were given a `-mimamsa` suffix (trm:linga-mimamsa, trm:krama-mimamsa, trm:uha-mimamsa, trm:badha-mimamsa, trm:prasanga-mimamsa, trm:abhyasa-mimamsa, trm:tantra-mimamsa, and others).
- trm:apavarga (Nyāya) is referenced as an equivalence target but not created here.

## 4. Out of reach
- Undigitized manuscripts: most of the lost Bṛhaṭṭīkā and Laghvī, the Saṅkarṣa and its commentaries, and later Prābhākara works.
- The oral teaching lineages of traditional Mīmāṃsā pāṭhaśālās.
- GRETIL and ebhāratī were used only through the local GitHub mirror (`sanskrit/raw_etexts`).
