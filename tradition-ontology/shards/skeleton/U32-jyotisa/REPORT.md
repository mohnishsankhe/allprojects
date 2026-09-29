# U32-jyotisa — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Unit: U32-jyotisa. Scope: coverage map A13 (Jyotiṣa and sacred timing). Owned lineage: `lin:jyotisa`. I also created four sub-lineages: `lin:kerala-jyotisa`, `lin:tajika`, `lin:nadi-jyotisa` (recent) and `lin:yavana-jataka` (absorbed).

Counts: 92 sources, 78 teachers, 125 teachings, 164 terms, 83 concepts, 23 practices, 20 obstacles, 7 phenomenology, 11 disputes, 8 borrowings, 1 ult view, 16 interpretation-log lines. Validator: 0 errors.

**Method.** Entries are skeletons written from memory. For the text layer, I checked wording and locators against local e-texts in `sources_raw/`: Vedāṅga Jyotiṣa, Sūrya Siddhānta, Āryabhaṭīya (with Bhāskara I), Bṛhajjātaka (GRETIL 28-chapter numbering and the Trivandrum edition), Laghujātaka, Bṛhat Saṃhitā (Bhat/GRETIL numbering), Yogayātrā, BPHS (97-chapter e-text), Jaimini Sūtras, Muhūrtacintāmaṇi, Brāhmasphuṭasiddhānta, Golādhyāya, Yājñavalkya and Manu smṛtis, DN 1, Snp 4.14, Ja 49, Vinaya kd15, and the Uttarajjhayaṇa. 116 teachings carry a "Phase-B spot check" note, but every entry stays at `level: skeleton`.

## 1. Coverage checklist (A13 and the unit brief's MUST-COVER list)

**Texts**
- Vedāṅga Jyotiṣa (Ṛk and Yajus recensions; five-year yuga): `src:vedanga-jyotisa` is owned by U02. I added `tea:vedanga-jyotisa:r.25-28` (the asterism deities) and `r.29-30`. U02's `cpt:five-year-yuga` is linked from `cpt:samvatsara-cycle`.
- Sūrya Siddhānta (revealed by Sūrya to Maya; structure): `src:surya-siddhanta`, with 13 teachings from 1.1 to 14. `tch:surya` and `tch:maya-asura`.
- Āryabhaṭīya (four pādas; 499 CE): `src:aryabhatiya`, with 9 teachings. Also `tch:aryabhata`, `src:aryabhata-siddhanta`, `src:aryabhatiya-bhasya-bhaskara`.
- Varāhamihira:
  - Bṛhajjātaka: `src:brhat-jataka`, 22 teachings.
  - Bṛhat Saṃhitā: `src:brhat-samhita`, 25 teachings, covering omens (ch. 45), vāstu (52) and gems (79).
  - Pañcasiddhāntikā: `src:pancasiddhantika`, plus the five siddhāntas as lost sources.
  - Laghujātaka: `src:laghu-jataka`.
  - Yogayātrā: `src:yogayatra`, 3 teachings. Also `src:tikanika-yatra`, `src:vivahapatala`, `tch:varahamihira`, `tch:adityadasa`.
- BPHS (tradition vs scholarly, both labelled): `src:brhat-parasara-hora-sastra`, 22 teachings. `tch:parasara` (contribution), `tch:maitreya-puranic`.
- Jaimini Upadeśa Sūtras (cara-kārakas, rāśi-dṛṣṭi, cara-daśā): `src:jaimini-upadesa-sutra`, 5 teachings. Concepts `cpt:cara-karakas`, `cpt:rasi-drsti`, `cpt:cara-dasa`.
- Yavanajātaka (Greek transmission as a borrowing): `src:yavanajataka`, `tch:sphujidhvaja`, `tch:yavanesvara`, `brw:yavana-jataka-to-jyotisa`, `lin:yavana-jataka`.
- Sārāvalī: `src:saravali`, `tch:kalyanavarman`.
- Phaladīpikā: `src:phaladipika`, `tch:mantresvara`.
- Jātakapārijāta: `src:jataka-parijata`, `tch:vaidyanatha-diksita`.
- Muhūrtacintāmaṇi: `src:muhurta-cintamani` (5 teachings), `tch:rama-daivajna`, `src:piyusadhara`.
- Tājika texts: `src:tajika-nilakanthi`, `src:hayanaratna`, `src:tajikasastra-samarasimha`, `src:trailokyaprakasa`. `tch:nilakantha-daivajna`, `lin:tajika`, `cpt:tajika-system`.
- Praśna Mārga: `src:prasna-marga`, `tea:prasna-marga:1` and `:15`, `lin:kerala-jyotisa`.
- Brahmagupta: `tch:brahmagupta`, `src:brahmasphuta-siddhanta` (2 teachings), `src:khandakhadyaka`.
- Bhāskara II: `tch:bhaskara-ii`, `src:siddhanta-siromani` (2 teachings), `src:lilavati`, `src:karanakutuhala`.
- Nāḍī traditions (as the tradition's claims): `lin:nadi-jyotisa`, `src:nadi-granthas`, `src:bhrgu-samhita`, `src:candrakala-nadi`, `cpt:nadi-leaf-reading`, `phn:nadi-leaf-found`.
- Additional texts:
  - Siddhāntas and handbooks: Mahābhāskarīya, Laghubhāskarīya, Śiṣyadhīvṛddhida, Laghumānasa, Vaṭeśvarasiddhānta, Siddhāntaśekhara, Bhāsvatī, Grahalāghava, Siddhāntatattvaviveka, Gūḍhārthaprakāśa.
  - Kerala: Parahita (Grahacāranibandhana), Dṛggaṇita, Goladīpikā, Tantrasaṅgraha, Nīlakaṇṭha's Āryabhaṭīyabhāṣya, Yuktibhāṣā.
  - Omens and early saṃhitā: Adbhutasāgara, Vasantarāja Śākuna, Vṛddhagargasaṃhitā, Yugapurāṇa.
  - Horā: Horāsāra, Ṣaṭpañcāśikā, Laghupārāśarī, Uttarakālāmṛta, Jātakābharaṇa, Sarvārthacintāmaṇi, Kṛṣṇīyam, Daśādhyāyī, Rudra's Vivaraṇa.
  - Time and muhūrta: Kālamādhava, Jyotiṣaratnamālā.
  - Jain and Buddhist: Sūryaprajñapti, Candraprajñapti, Jyotiṣkaraṇḍaka, Aṅgavijjā, Gaṇitasārasaṅgraha, Śārdūlakarṇāvadāna, Daivajñakāmadhenu.
  - Recent: Siddhāntadarpaṇa, Gaṇakataraṅgiṇī, The Holy Science.

**Concepts**
- Nine grahas including Rāhu and Ketu: `cpt:navagraha`, `cpt:graha-significations`, `cpt:planetary-dignities`, `cpt:graha-drsti`, `cpt:graha-avatara`. Terms `trm:surya` … `trm:ketu`, `trm:chaya-graha`, `trm:upagraha`, `trm:gulika`.
- Twelve rāśis: `cpt:twelve-rasis`, `cpt:kalapurusa`, and 12 terms `trm:<name>-rasi`.
- Twelve bhāvas and their significations: `cpt:twelve-bhavas`, `cpt:house-groupings`, `trm:bhava-jyotisa`, `trm:kendra`, `trm:upacaya`, and related terms.
- 27/28 nakṣatras with their deities: `cpt:twenty-seven-naksatras` (list with deities), `cpt:naksatra-classes`, 28 terms `trm:<name>-naksatra`.
- Vargas: `cpt:vargas`, `trm:varga-jyotisa`, `trm:navamsa`, `trm:drekkana`, `trm:vargottama`.
- Daśā systems: `cpt:dasa-systems`, `cpt:vimsottari-dasa` (120 years; order and years checked against BPHS 46.12–15), `cpt:astottari-dasa`, `cpt:yogini-dasa`, `cpt:cara-dasa`.
- Yogas: `cpt:jyotisa-yogas`, `cpt:rajayoga-jyotisa`, `cpt:dhana-yogas`, `cpt:pancamahapurusa-yogas`, `cpt:candra-yogas` (includes Gajakesarī), `cpt:nabhasa-yogas`, `cpt:pravrajya-yogas`.
- Muhūrta and pañcāṅga: `cpt:muhurta-science`, `cpt:pancanga`, `cpt:tithi-classes`, `cpt:astakuta`, `cpt:gocara`. Terms `trm:tithi`, `trm:vara`, `trm:karana-jyotisa`, `trm:yoga-jyotisa`, `trm:muhurta`.
- Remedial measures: `cpt:remedial-measures`, `cpt:navagraha-correspondences`.
  - Practices: `prc:graha-santi`, `prc:navagraha-puja`, `prc:navagraha-mantra-japa`, `prc:mahamrtyunjaya-japa` (jyotiṣa use, BPHS 52), `prc:aditya-hrdaya`, `prc:graha-dana`, `prc:ratna-dharana`, `prc:graha-vrata`, `prc:janma-santi`, `prc:utpata-santi`.
- Horoscope as showing prārabdha karma: `cpt:horoscope-reveals-karma` (BJ 1.3 and LJ 1.3 checked verbatim; BPHS 2.3). Logged as `same-as-under-standpoint cpt:three-kinds-of-karma`.
- Eclipses and their rules: `cpt:eclipse-doctrine`, `cpt:eclipse-observances`, `prc:grahana-observance`, `obs:grahana-janma`, `dsp:eclipse-cause`.
- Calendar and festivals: `cpt:lunisolar-calendar`, `cpt:samvatsara-cycle`, `cpt:calendar-eras`, `cpt:festival-timing`, `cpt:ayanamsa-reckoning`, `cpt:kali-epoch`, `cpt:yuga-system-jyotisa`, `cpt:two-kinds-of-time`, `cpt:measures-of-time`.

**Section D checklist for lin:jyotisa**
- Ultimate: `ult:jyotisa`, `cpt:jyotisa-ultimate`, `cpt:sun-as-self-of-time`.
- Self and mind: `cpt:self-and-mind-in-jyotisa`, `cpt:jivamsa-paramatmamsa`.
- Body: `cpt:body-and-constitution-in-jyotisa`, `cpt:kalapurusa`.
- Matter and qualities: `cpt:gunas-of-planets` (contribution to `cpt:three-gunas`), `cpt:planets-and-elements`.
- Obstacles: 20 `obs:` entries.
- Ethics: `cpt:daivajna-qualifications`, `obs:kuhaka-daivajna`, `cpt:astakuta`.
- Karma, rebirth and liberation: `cpt:horoscope-reveals-karma`, `cpt:daiva-and-purusakara-jyotisa`, `cpt:moksa-in-the-chart`, `cpt:pravrajya-yogas`.
- Signs and powers: `cpt:utpata-portents`, `cpt:sakuna-augury`, 7 `phn:` entries.
- Teacher and transmission: `cpt:jyotisa-transmission`, `cpt:jyotisa-revelation`, `cpt:eighteen-promulgators`, `cpt:jyotisa-three-skandhas`, `cpt:jyotisa-as-eye-of-veda`.
- Cosmology and time: `cpt:siddhantic-cosmography`, `cpt:causes-of-planetary-motion`, `cpt:kurma-vibhaga`, `cpt:vastu-purusa`.
- Sound and language: `cpt:number-and-sound-in-jyotisa`, `cpt:naksatra-naming`, `trm:katapayadi`, `trm:bhutasankhya`, `trm:aryabhata-numerals`.
- Death and dying: `cpt:ayurdaya`, `cpt:niryana-and-next-world`, `obs:apamrtyu`, contribution to `cpt:death-omens`.
- Path maps: none. Jyotiṣa has no path to liberation of its own, so no `pth:` entry was made.

**Disputes**
- Fate vs effort: `dsp:jyotisa-fate-and-effort` (Varāhamihira, Yājñavalkya, Yoga Vāsiṣṭha, Nakkhatta Jātaka). It cross-refers to U06's `dsp:daiva-or-paurusa` and `tea:moksopaya:*`.
- Buddhist and Jain rejection of astrology for monastics: `dsp:astrology-for-renunciants`. Sides: DN 1.21–27 and 1.24, Snp 927, Vinaya Cv 5.33.2, Ja 49, Uttarādhyayana 15.7, and Manu 6.50 for the Vedic renouncer.
- Mīmāṃsā/Dharmaśāstra use of timing: `cpt:time-as-limb-of-rite`, `cpt:festival-timing`, `dsp:ekadasi-viddha`, `dsp:astrologer-at-sraddha` (Manu 3.162 vs BS 2.13).
- Other recorded debates:
  - `dsp:grahas-cause-or-sign`
  - `dsp:eclipse-cause` (reconciled by BS 5.14–15 itself)
  - `dsp:yuga-quarters` (Brahmagupta vs Āryabhaṭa, BSS 1.9)
  - `dsp:earth-rotation` (Āryabhaṭīya 4.9 vs BSS 11.17)
  - `dsp:sayana-nirayana`
  - `dsp:ayurdaya-methods` (BJ 7)
  - `dsp:exalted-malefics-rajayoga` (BJ 11.1)
- Queued: yuga-quarters, earth-rotation, sayana-nirayana, ayurdaya-methods, exalted-malefics. The orchestrator should add these five to RECONCILE_QUEUE.md under the ids `RQ-U32-*`.
- ult:jyotisa is present, with the caveat that jyotiṣa is a limb of the Veda, not a soteriology.

**Corrections to the unit brief's list**
- Āryabhaṭīya "499 CE": the text gives the author's age (23) at Kali 3600, not a composition date (Kālakriyā 10).
- DN 1 frames astrology as a "low art" by which some ascetics live by wrong livelihood (tiracchāna-vijjā, micchā-ājīva). It is not a general ban on laypeople. The Vedic Manu 6.50 imposes the same rule on renouncers, and Manu 3.162 excludes professional astrologers from śrāddha.
- The planet–gem table is not in the Bṛhat Saṃhitā. BS 79–82 judges gems by their own qualities. The table comes from later texts (usually cited as Phaladīpikā 2, not verified here).
- The Bṛhat Saṃhitā's "five great men" chapter is BS 68 in Bhat numbering (69 in some editions). BPHS has it at ch. 75.
- The Vedāṅga Jyotiṣa's asterism list starts from Kṛttikā, has 27 deities and has no Abhijit. Abhijit (Brahmā) appears in muhūrta texts.
- Renunciation yogas differ between BJ 15.1 and BPHS 79.2–3. Both are recorded, linked by `differs_from`.
- Bṛhajjātaka chapter numbers differ between editions: 28 chapters in GRETIL, 26 in the Trivandrum edition. I used GRETIL numbering.

## 2. Least-sure items (check these first for hallucination)
- **Teachings:**
  - `tea:surya-siddhanta:14`: the nine measures of time, from memory.
  - `tea:pancasiddhantika:1.4`: verse number and ranking from memory.
  - `tea:prasna-marga:1` and `:15`: chapter-level; ch. 15 is a guess.
  - `tea:aryabhatiya:4.50`: the wording is from memory.
  - `tea:aryabhatiya:1.5`: decoding of the alphabetic numerals.
  - `tea:brhat-jataka:15.2-4` and `:8.1`: dense verses, paraphrased.
  - `tea:yajnavalkyasmrti:1.295-306`, `1.307-308`, `1.349-351`: only the pāda locators were checked, not the full wording or the lists of materials.
  - `tea:mahabharata:1.17` and `tea:rgveda:5.40.5-9`: verse divisions not checked.
  - `tea:tattvartha-sutra:4.12-15`: numbering differs between recensions.
- **Concepts:**
  - `cpt:eighteen-promulgators`: the list is from memory.
  - `cpt:tajika-system`: the sixteen yoga names may be misspelled.
  - `cpt:astottari-dasa` and `cpt:yogini-dasa`: years and names from memory.
  - `cpt:nabhasa-yogas`: the 3 + 2 + 20 + 7 split.
  - `cpt:candra-yogas`: BJ 13 not checked.
  - `cpt:planetary-friendship`, `cpt:dhana-yogas`.
  - The Kerala six-limb list (ṣaḍaṅga) inside `cpt:jyotisa-three-skandhas`.
- **Sources and teachers with uncertain dates or attributions:**
  - Kalyāṇavarman (c. 800?), Mantreśvara (13th–16th c.?), Vaidyanātha Dīkṣita.
  - Govinda Bhaṭṭatiri and Daśādhyāyī; Rudra (Kerala).
  - Anavamadarśī and Daivajñakāmadhenu; Samarasiṃha (1274) and the title of his work.
  - Hemaprabha and Trailokyaprakāśa (1248); Balabhadra's works.
  - Muhūrtamārtaṇḍa (1571); `src:jagaccandrika` (commentary title).
  - The Praśna Mārga's chapter count (32) and author.
  - `tch:nc-lahiri` and the Calendar Reform Committee detail; `tch:bapudeva-sastri`.
- **Terms and obstacles:** `trm:rahukala`, `trm:dhanistha-pancaka`, `trm:kuja-dosa` and `obs:kuja-dosa` (no classical verse located), `obs:kala-sarpa-yoga` (recent; no classical source found), `obs:pitr-dosa`, `obs:sarpa-dosa`, and the member list of `obs:purvajanma-sapa`.
- **Disputes:**
  - `dsp:sayana-nirayana` (low): positions from memory, and the Sūrya Siddhānta's libration verses (SS 3) not checked.
  - `dsp:ekadasi-viddha` (low): Nirṇayasindhu and Haribhaktivilāsa locators are approximate.
  - `dsp:eclipse-cause`: the claim that Brahmagupta defended the Rāhu view is marked unverified.
- **Borrowings:** the Kālacakra, Jain-astronomy, Śārdūlakarṇāvadāna and Sri Lanka borrowings are all low confidence.

## 3. Gaps (belong here, but not created responsibly)
- **No teachings extracted** from the Sārāvalī, Phaladīpikā, Jātakapārijāta, Tājikanīlakaṇṭhī, Horāsāra, Ṣaṭpañcāśikā, Uttarakālāmṛta, Kālamādhava, Nirṇayasindhu (eclipse and tithi rules), Adbhutasāgara, or the Nārada/Vasiṣṭha saṃhitās. Their sources exist; verse-level teachings need Phase D. Local e-texts exist for several: Jātakapārijāta, Jaimini, Horāsāra, Kālamādhava, Adbhutasāgara, Ṣaṭpañcāśikā, Jyotirnibandha.
- **BPHS** chapters 3–5, 11–31, 33–45 and 66–78 are covered only at concept level: planet natures, house significations, ārūḍha, argalā, aṣṭakavarga, ṣaḍbala, Kālacakra daśā.
- **Jaimini:** the cara-daśā rules (adhyāya 2) were not spot-checked.
- **Bṛhajjātaka:** ch. 6, 13, 16–24, 26–27 have no teachings.
- **Bṛhat Saṃhitā:** chapters 3–4 and 6–44 (courses of individual planets, rain-forecasting, Agastya, the Seven Seers, comets, earthquakes, meteors, Indra's banner, nīrājana) and 46–51, 53–67, 69–96 lack teachings. Comets and earthquakes appear only as low-confidence `phn:` entries.
- **Perso-Arabic source of Tājika:** no borrowing entry, because no lineage id exists for Islamic astrology (outside scope). Recorded in `lin:tajika` instead.
- **Ramala (geomancy), Svapna-śāstra, Sāmudrika (physiognomy), Svarodaya:** not entered. Śiva Svarodaya is owned by U28 and already tagged lin:jyotisa there.
- **Purāṇic jyotiṣa sections** (Nārada Purāṇa's triskandha chapters, Agni Purāṇa, Viṣṇudharmottara's Paitāmaha): mentioned only in notes, because I could not verify the chapter numbers.
- **Tibetan kar-tsi and the Kālacakra's calendrics:** only a low-confidence borrowing. Belongs to U44/U48.
- **Other details not entered:** the Kumbha Melā's timing by Jupiter (U57 owns the event); the 27 pañcāṅga yogas as a verified list (named only in a term); the full list of the thirty muhūrtas of a day.
- **Ult views for sub-lineages:** I wrote only `ult:jyotisa`. The four sub-lineages I created share it and teach nothing distinct on the ultimate.
- **Shared ids emitted with jyotiṣa contributions:** these may produce scalar conflicts at merge.
  - Teachers: tch:parasara, jaimini, garga, brahma, vasistha, narada, bhrgu, agastya, maitreya-puranic, vidyaranya, sri-yukteswar.
  - Terms: trm:jyotisa, naksatra, yuga, kala, kalpa, mahayuga, manvantara, kali-yuga, samvatsara, uttarayana, muhurta, surya, candra, brhaspati, daiva, purusakara, prarabdha, santi, dana, vrata, guna, moksa, kaivalya.
  - Concepts: cpt:three-gunas, three-kinds-of-karma, ages-and-day-of-brahma, paurusa-and-daiva, time-for-sacrifice, kala, death-omens.
  - Practice: prc:mahamrtyunjaya-japa. Its method_summary differs from U01's; the jyotiṣa summary should be merged in, not allowed to replace U01's.

## 4. Out of reach
- **Nāḍī palm leaves:** unedited, privately held, read orally in Tamil. Only the tradition's claim is recorded (recent: true).
- **Bhṛgu Saṃhitā collections:** family-held manuscripts, not published.
- **Kerala praśna practice** (aṣṭamaṅgala, devaprāśna): oral and ritual in large part. The written Praśna Mārga was not locally available.
- **Early texts known only in manuscript or through citation:** Vṛddhagargasaṃhitā (manuscript-only), and the Paitāmaha, Vāsiṣṭha, Romaka and Pauliśa siddhāntas (lost; known through the Pañcasiddhāntikā). Āryabhaṭa's midnight siddhānta is lost.
- **Restricted material:** none in this unit met the restricted criteria. Eclipse and vrata fasts are short and not prolonged, which is noted on the entries. Practices carry the texts' own warnings (Yogayātrā 1.5–6; BS 2.15, 45.5, 79.1; BPHS 91.1).
