# U19-kashmir-saivism — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map A7 (Kashmir Śaivism, incl. the 112 dhāraṇās of the Vijñāna Bhairava as practices) and I2 (the Mata alongside Kula, Krama and Trika). Owned lineages: lin:kashmir-saivism, lin:spanda, lin:pratyabhijna, lin:trika, lin:krama, lin:mata.

Counts: lineages 6 · ultimate 6 · sources 89 · teachers 45 · teachings 352 · terms 144 · concepts 46 · practices 137 (112 dhāraṇās + 25) · obstacles 15 · phenomenology 17 · disputes 6 · borrowings 11 · interpretation_log 17. Validator: 0 errors. Generators: _gen/part1…part9*.py, run from tradition-ontology/. common.py holds the helpers and the dispute cross-reference map; check_refs.py lists ids that are referenced but not defined.

Method: every entry is at skeleton level. Wording, verse numbers and structures were spot-checked against the GRETIL, Muktabodha and DCS mirrors in sources_raw/. These cover:
- Vijñāna Bhairava in 3 recensions
- Śiva Sūtra in the recensions of Kṣemarāja and Bhāskara
- Spandakārikā, Pratyabhijñāhṛdaya, Īśvarapratyabhijñākārikā
- Śivadṛṣṭi chapters 2 and 7
- Mālinīvijayottara, Parātrīśikā, Paramārthasāra
- Tantrāloka chapters 1, 4, 5, 13 and 29, plus the chapter colophons
- Tantrasāra, Kramastotra, Bhairavastava, Bodhapañcadaśikā, Śivastotrāvalī
- Lalleśvarīvākyāni, Netra 7.1, Vātūlanāthasūtra

Checked entries say so in their notes. Nothing has been fidelity-checked yet. The `original` field is filled only where copied from these e-texts, or for the Śiva Sūtra and PH, where the wording is certain.

## 1. Checklist — coverage-map items and the ids that cover them

**Lineages and ult views:** lin/ult:kashmir-saivism, spanda, pratyabhijna, trika, krama, mata; also cpt:mata-system. Kula is referenced as lin:kaula (U24).

**Scriptural base:**
- src:malinivijayottara-tantra, src:svacchanda-tantra, src:netra-tantra
- src:vijnana-bhairava-tantra — 163 verses in the KSTS 8 numbering. Frame and Rudrayāmala claim: tea:vijnana-bhairava-tantra:1 and :161-163.
- src:paratrisika — also claims to be the Rudrayāmala (v. 35)
- src:siddhayogesvarimata, src:jayadrathayamala
- also src:tantrasadbhava, src:trisirobhairava, src:devyayamala, src:kalasankarsinimata, src:kalikulapancasataka, src:kramasadbhava

**Spanda:**
- src:siva-sutra — all 77 sūtras as teachings, tea:siva-sutra:1.1 … 3.45 (key: 1.1, 1.2, 1.5, 3.9)
- src:spanda-karika — 24 teachings; authorship dispute in dsp:spanda-karika-authorship
- Kallaṭa: src:spanda-vrtti and the lost src:tattvarthacintamani
- Kṣemarāja: src:siva-sutra-vimarsini, src:spanda-nirnaya, src:spanda-sandoha
- Bhāskara: src:siva-sutra-varttika-bhaskara, with his lineage account at tea:…:1.3-9
- Rāmakaṇṭha: src:spanda-vivrti
- also src:spanda-pradipika, src:siva-sutra-varttika-varadaraja, src:siva-sutra-vrtti-sahib-kaul

**Pratyabhijñā:**
- src:sivadrsti — paśyantī critique at tea:sivadrsti:2.1 and :2, dispute dsp:pasyanti-brahman; also src:sivadrsti-vrtti
- src:isvarapratyabhijna-karika — 190 kārikās, 26 teachings — with its -vrtti and -vivrti
- src:sivastotravali and its -vivrti
- src:siddhitrayi, with src:ajadapramatrsiddhi, src:isvarasiddhi, src:sambandhasiddhi
- src:isvarapratyabhijna-vimarsini, src:isvarapratyabhijna-vivrti-vimarsini
- src:pratyabhijnahrdayam — all 20 sūtras as teachings
- src:bhaskari, src:isvarapratyabhijna-kaumudi

**Trika:**
- src:tantraloka — 37 āhnikas, chapter topics in `structure`, 22 teachings; src:tantraloka-viveka
- src:tantrasara, src:tantravatadhanika, src:paratrisika-vivarana, src:paratrisika-laghuvrtti
- src:paramarthasara and src:paramarthasara-vivrti; src:malinislokavarttika, src:purvapancika, src:gitarthasangraha
- Short works of Abhinavagupta: src:bodhapancadasika, src:anuttarastika, src:bhairavastava, src:kramastotra-abhinavagupta, src:dehasthadevatacakrastotra, src:paryantapancasika, src:mahopadesavimsatika, src:anubhavanivedana
- Aesthetics (U31), referenced only: src:abhinavabharati, src:dhvanyaloka-locana
- Vijñāna Bhairava commentaries: src:vijnana-bhairava-vivrti-sivopadhyaya, src:vijnana-kaumudi, src:vijnana-bhairava-uddyota
- Kṣemarāja: src:svacchandoddyota, src:netroddyota, src:parapravesika, src:stavacintamani(-vrtti), src:bhairavanukaranastotra

**Krama:**
- Twelve Kālīs: cpt:twelve-kalis, cpt:krama-phases-of-cognition, tea:tantraloka:4.148-172 and :4.173, tea:kramastotra-abhinavagupta:15-27, practice prc:krama-twelve-kalis-contemplation
- Pañcavāha: cpt:pancavaha
- src:maharthamanjari (+ -parimala), src:mahanayaprakasa-sitikantha, src:mahanayaprakasa, src:vatulanatha-sutra, src:chummasanketaprakasa, src:cidgaganacandrika

**Mata:** tea:tantraloka:4.262-263, :4.268-270, :13.300-301; cpt:scriptural-hierarchy.

**Later Kashmir:**
- tch:lal-ded and src:lalla-vakyani — 6 vākhs, in Bhāskara's numbering
- tch:rupa-bhavani and src:rupa-bhavani-vakhs
- tch:sahib-kaul and src:devinamavilasa
- Lakshmanjoo is referenced only (U52)

**Concepts:**
- 36 tattvas listed in full: cpt:thirty-six-tattvas, plus terms trm:siva-tattva … trm:purusa-kashmir
- Kañcukas: cpt:five-kancukas and obs:five-kancukas
- cpt:prakasa-vimarsa, cpt:spanda-doctrine, cpt:abhasavada, cpt:svatantrya, cpt:five-acts-of-siva
- Three malas: cpt:three-malas and obs:three-malas, plus one obstacle per mala
- Four upāyas: cpt:four-upayas and cpt:anupaya, with practices prc:anupaya-realization, prc:sambhava-samavesa, prc:sattarka, prc:uccara-prana, prc:karana-anava, prc:dhyana-anava, prc:varna-anava, prc:sthana-kalpana
- Powers: cpt:three-saktis (+ cpt:five-saktis for cit and ānanda)
- cpt:matrka-and-malini, cpt:pratyabhijna-recognition (+ prc:pratyabhijna-recognition), cpt:hrdaya-heart
- Madhya: cpt:madhya-centre and prc:madhya-vikasa, plus the PH 18 methods prc:vikalpa-ksaya, prc:sakti-sankoca, prc:sakti-vikasa, prc:vahaccheda, prc:adyantakoti-nibhalana
- cpt:seven-pramatrs, cpt:kinds-of-saktipata, cpt:jivanmukti-kashmir
- Kula ritual as read by Abhinavagupta: cpt:kaula-ritual-abhinava and prc:kula-yaga (restricted)
- cpt:levels-of-speech
- D-checklist extras: cpt:four-states-and-turya, cpt:self-as-consciousness, cpt:three-coverings, cpt:five-pranas-kashmir, cpt:subtle-body-netra, cpt:six-adhvans, cpt:cosmology-kashmir, cpt:karma-and-rebirth-kashmir, cpt:death-and-dying-kashmir, cpt:ethics-kashmir, cpt:siddhis-kashmir, cpt:guru-and-transmission, cpt:five-signs-of-samavesa, cpt:seven-anandas, cpt:trika-triad, cpt:kula-akula

**112 dhāraṇās:** prc:vbt-dharana-1…112, each with its verse range and a teaching tea:vijnana-bhairava-tantra:&lt;range&gt;. Verse numbers follow KSTS 8 / GRETIL.

Mapping: dhāraṇā n = verse n+23 for n=1–20 (verses 24–43). Then 21 = 44-45. Then n = verse n+24 for 22–59 (verses 46–83). Then 60 = 84-85. Then n = verse n+25 for 61–87 (verses 86–112). Then 88 = 113-114. Then n = verse n+26 for 89–112 (verses 115–138).

Grouping rule: the text itself counts 112 (v. 139) in vv. 24–138, which is 115 verses. The three verses joined to a neighbour (45, 84, 114) are exactly the three the Kaumudī recension (KSTS 9) does not have as separate verses: 45 is merged with 44 there, and its editor reports 84 and 114 as extra verses found in one manuscript. That recension therefore has exactly 112 verses in its dhāraṇā section, and Ānandabhaṭṭa's explicit ordinals for dhāraṇās 1–20 match this numbering.

Restricted (summary plus the text's secrecy rule, VBT 157–159): dhāraṇās 44–46 (sexual bliss), 53 (the five mudrās — a precaution because one is named khecarī) and 68 (piercing the body).

**Other practices:** prc:spanda-awareness, prc:nityodita-samadhi, prc:ajapa-japa, prc:inner-worship-trika, prc:saiva-stotra-devotion, prc:diksa-trika, prc:sadyahsamutkranti (restricted), prc:antyesti-trika.

**Obstacles:** obs:vikalpa, obs:sankoca, obs:vyamoha-sakti, obs:ksobha, obs:glani, obs:moha, obs:siddhi-attachment, obs:susupta-like-absorption, obs:sadripu, obs:sanka.

**Phenomenology:** 17 phn: items (from VBT, MVT, TĀ, SK, ŚS, PH and Lal Ded).

**Path map:** pth:kashmir-four-upayas is owned by U51. This unit contributes teachings tagged with `paths` and `stage_native`: ŚS sections, PH 13 and 17–19, MVT 2.21-23, TĀ 1.168-170, TĀ 2–5, Śivadṛṣṭi 7.5-6.

**Disputes:**
- With Advaita: references dsp:world-real-or-appearance and dsp:causation (from PH 1-2, ĪPK 1.5.1 and 2.4.1, PS 11-13, 15 and 27-29, VBT 102 and 133), and dsp:saguna-nirguna (from VBT 7-13).
- With the Buddhist logicians: dsp:pratyabhijna-vs-buddhist-logicians (+ dsp:is-there-a-self) and borrowing brw:pramana-buddhist-to-pratyabhijna.
- With the Śaiva Siddhānta: dsp:mala-substance-or-ignorance and dsp:liberation-identity-or-equality-with-siva (+ dsp:souls-one-or-distinct, dsp:works-knowledge-grace).
- Also dsp:pasyanti-brahman, dsp:spanda-karika-authorship, and dsp:purity-impurity-kaula (partially reconciled under P4/P1). The other five disputes are queued.

**Borrowings:** 11 entries, e.g. Kaula→Trika, Krama→Trika, Vyākaraṇa→Pratyabhijñā, Sāṃkhya→Kashmir Śaivism, Kashmir Śaivism→Śrīvidyā, Trika→Alaṅkāra.

## 2. Corrections to the MUST-COVER list (checked against the texts)
- **Vijñāna Bhairava:** "163 verses" is true only in the KSTS 8 numbering, which has a v. 155b on the haṃsa-japa. The GRETIL e-text numbers 162. The Rudrayāmala claim is in v. 1 and vv. 161–162; the Parātrīśikā makes the same claim.
- **Śiva Sūtra:** Kṣemarāja's recension has exactly 77 sūtras (22+10+45). Bhāskara's has 79 (23+10+46): he splits 1.16, adds 3.15, reorders 3.22-23, and calls the sections prakāśa.
- **Spandakārikā authorship:** Bhāskara (Vārttika 1.5: Kallaṭa's "own Spanda-sūtras") is on the Kallaṭa side, with Rāmakaṇṭha and Bhagavadutpala. Kṣemarāja's recension has 53 verses (25+7+19+2).
- **New ids to avoid clashes with registry ids:**
  - The Spandavivṛti's Rāmakaṇṭha is not tch:ramakantha (the Siddhānta Rāmakaṇṭha II) → tch:rajanaka-ramakantha
  - Bhāskara is not tch:bhaskara (the Vedāntin) → tch:bhaskara-kashmir
  - Utpaladeva's Siddhitrayī is not src:siddhitraya (Yāmuna) → src:siddhitrayi
- **MVT 2.15:** the third sign of śaktipāta is sarvasattvavaśitva (control of all beings), not sarvatattva.
- **Tantrāloka colophons:** chapter 16 is titled prameya and chapter 17 vikṣiptadīkṣā.
- **"Kālīkrama":** no text of that title could be confirmed, so it is covered as the Krama sequence of Kālīs. The Pañcavāha is entered only as a concept.
- **Twelve Kālīs:** TĀ 4.148-172 names phases rather than giving a list. Names 1–6 are confirmed; names 7–12 are reconstructed.
- **Mata:** its texts, deities and teachers cannot be identified. Its place in the scriptural hierarchy differs between two sources: before Kula in Jayaratha's quotation on TĀ 13.301, after Kula in the Parātrīśikāvivaraṇa's quotation.
- **Śivastotrāvalī:** per Kṣemarāja, the hymns were compiled by Rāma and Ādityarāja and arranged into 20 by Viśvāvarta.
- **Lal Ded:** her vākhs are numbered 60 in Bhāskara's collection and 109 in Grierson–Barnett. Sāhib Kaul also wrote Śrīvidyā works.

## 3. Least-sure items (check first in Phase C)
- **VBT:** the dhāraṇā grouping compared with Jaideva Singh's and Lakshmanjoo's.
- **Krama:**
  - cpt:pancavaha correlations; Kālī names 7–12
  - tch:jnananetra and his disciples; tch:niskriyanandanatha and src:chummasanketaprakasa
  - src:kalikulapancasataka, src:kramasadbhava, src:kalasankarsinimata
- **Mata:** all of lin:mata, ult:mata and cpt:mata-system.
- **Spanda:** src:siva-sutra-varttika-varadaraja.
- **Attributions and existence:** src:tantravatadhanika, src:dehasthadevatacakrastotra, src:mahopadesavimsatika, src:anubhavanivedana, src:paratrisika-laghuvrtti, src:isvarapratyabhijna-kaumudi.
- **Counts and structure:**
  - Netra: 22 chapters, and the content of its ch. 8
  - Svacchanda: 15 paṭalas
  - Mahārthamañjarī: 70 gāthās
  - Tantrāloka: c. 5,800 verses
  - the nine-grade śaktipāta scheme
- **Teachers and dates:**
  - tch:bhutiraja, tch:sumatinatha
  - dates of Ānandabhaṭṭa, Lakṣmīrāma, Śitikaṇṭha, Vāmadeva, Vāmanadatta
  - whether Bhāskarakaṇṭha is the translator of Lal Ded
  - the Abhinavagupta cave legend and TĀ 37 ancestry
  - Rūpa Bhavānī's dates and works
- **Other:**
  - tea:maharthamanjari:summary
  - the Siddhānta, grammarian and Dharmaśāstra sides of the disputes, which have work-level refs only; src:naresvarapariksa is a guessed id
  - edition details for the Siddhayogeśvarīmata and Jayadrathayāmala
  - the mālinī letter order

## 4. Gaps
- **Texts not identified or not available:**
  - Mata scriptures and teachers
  - Krama root tantras and its lineage
  - Jayadrathayāmala contents by ṣaṭka
  - Abhinavagupta's lost works
  - Kṣemarāja's full oeuvre
  - Utpaladeva's Vivṛti fragments
- **Anchors still thin:** verse-level teachings for most Tantrāloka chapters (only 22 anchors), and for the TS, PTV, IPV, IPVV, MŚV, Svacchanda and Netra.
- **Not entered:** Kashmiri ritual manuals in Muktabodha (Dīkṣāpaddhati, Agnikāryapaddhati, Ānandeśvarapaddhati, Nirvāṇapaddhati, Devīrahasya).
- **Recent, for U52:** Govinda Kaul, Mānasārāma's Svātantryadīpikā, Swami Ram, Mahtab Kak.
- **Not reproduced (copyright):** modern translators' classifications of the dhāraṇās by upāya.
- **Cross-unit ids assumed by the slug rule, to reconcile at merge:**
  - obs:three-bonds, cpt:twenty-five-tattvas, cpt:vivarta, cpt:jivanmukti, cpt:three-states-and-the-fourth
  - trm:brahman, trm:turiya
  - prc:antaryaga, prc:atma-vicara, prc:nadanusandhana, prc:sanmukhi-mudra
  - src:dhvanyaloka-locana, src:mrgendra-tantra, src:naresvarapariksa
  - tch:induraja, tch:bhatta-tauta
  - U49 may have its own id for brw:pramana-buddhist-to-pratyabhijna, which would need deduplicating

## 5. Out of reach
- Oral and initiatory instruction: the mudrās of VBT 77 and TĀ 32, the Kula rite of TĀ 29, the Krama chummā code-words (restricted and oral).
- Unpublished manuscripts of the Krama, Mata and Kālīkula scriptures.
- The living oral lineage through Swami Lakshmanjoo (U52).
