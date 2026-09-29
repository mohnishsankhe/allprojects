# U41-yogacara-pramana — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map B4 (Yogācāra; the five Maitreya texts; Buddhist logic and epistemology). U41 owns `lin:yogacara` and `lin:pramana-buddhist`, and adds `lin:satyakaravada`, `lin:alikakaravada`, `lin:dilun`, `lin:shelun` and `lin:hosso` (none of these five is in the registry, so please register them).

- **Generators:** `_gen/part1…part8*.py`. `_gen/run_all.py` does a clean rebuild; `_gen/check_refs.py` checks references; `_gen/dcs_text.py` reads DCS files.
- **Final counts:** 7 lineages · 120 sources · 51 teachers · 177 teachings · 198 terms · 71 concepts · 22 practices · 12 obstacles · 4 path maps · 7 phenomenology items · 15 disputes · 10 borrowings · 2 ultimate views · 26 interpretation-log lines. Validator: 0 errors.

## 0. How the verse numbers were checked
Wording and numbering were checked against local e-texts for these works:
- Triṃśikā — all 30 verses; DSBC text.
- Viṃśatikā — DCS text, 22 verses.
- Trisvabhāvanirdeśa — GRETIL Devanāgarī text, transliterated.
- Madhyāntavibhāga — DSBC text.
- Mahāyānasūtrālaṃkāra — Lévi's edition via GRETIL.
- Abhisamayālaṃkāra — DSBC text, `asa_` numbering.
- Śrāvakabhūmi — Shukla's edition.
- Bodhisattvabhūmi — GRETIL Devanāgarī text.
- Yogācārabhūmi opening list of stages — Bhattacharya's edition.
- Abhidharmasamuccaya — DSBC text.
- Nyāyabindu — DCS text.
- Pramāṇavārttika — DSBC text.
- Kṣaṇabhaṅgasiddhi, Tarkabhāṣā — DSBC texts.
- Ratnakīrti's collected works (Apohasiddhi, Santānāntaradūṣaṇa) — SARIT text.
- Tattvasaṃgrahapañjikā — SARIT text.
- Laṅkāvatāra 10.256–258 — as quoted in the Bhāvanākrama.

**Pramāṇavārttika numbering.** Teaching ids for the Pramāṇavārttika use the **e-text's own numbering**, and the e-text orders the chapters differently from the usual citation:

| e-text chapter | content | usual (Tibetan / Miyasaka) citation |
|---|---|---|
| 1 | Pramāṇasiddhi (the two maṅgala verses counted as 1.1–2) | PV 2.(n−2) |
| 2 | Pratyakṣa | PV 3.n |
| 3 | Svārthānumāna | PV 1.n |
| 4 | Parārthānumāna | PV 4.n |

Each PV teaching gives its usual citation in `notes`.

**Ālambanaparīkṣā.** The local Sanskrit is a modern back-translation, so no original is quoted for it.

## 1. Coverage checklist (brief MUST-COVER, B4 and section D) with ids

### Maitreya texts
- Five Maitreya texts (Tibetan list): `src:abhisamayalamkara`, `src:mahayanasutralamkara`, `src:madhyantavibhaga`, `src:dharmadharmatavibhaga`; `src:ratnagotravibhaga` is U39's and is referenced. The fact that Chinese tradition attributes them differently is noted in each source's `notes`.
- Commentaries:
  - `src:mahayanasutralamkarabhasya`, `src:sutralamkaravrttibhasya`, `src:mahayanasutralamkaratika`
  - `src:madhyantavibhagabhasya`, `src:madhyantavibhagatika`
  - `src:dharmadharmatavibhagavrtti`
  - `src:abhisamayalamkaravrtti-vimuktisena`, `src:abhisamayalamkaraloka`, `src:sphutartha`

### Asaṅga
- Yogācārabhūmi: `src:yogacarabhumi`. Its seventeen stages are in `cpt:seventeen-bhumis` and `tea:yogacarabhumi:0.uddana`.
- Parts of the Yogācārabhūmi: `src:sravakabhumi` (the meditation manual), `src:bodhisattvabhumi`, `src:viniscayasamgrahani`, `src:vastusamgrahani`.
- `src:mahayanasamgraha` with `src:mahayanasamgrahabhasya` and `src:mahayanasamgrahopanibandhana`.
- `src:abhidharmasamuccaya` with `src:abhidharmasamuccayabhasya` and `src:abhidharmasamuccayavyakhya`.
- `src:xianyang-shengjiao-lun`, `src:vivrtaguhyarthapindavyakhya`.
- Teacher entries: `tch:asanga`, `tch:maitreyanatha`.

### Vasubandhu
- `src:vimsatika` (+ `src:vimsatikavrtti`), `src:trimsika`, `src:trisvabhavanirdesa`.
- `src:pancaskandhaprakarana` and `src:karmasiddhiprakarana` (U38's ids; U41 adds its contribution).
- `src:vyakhyayukti`, `src:baifa-mingmen-lun`, `src:dasabhumika-vyakhyana` (shared with U39).
- The "two Vasubandhus" question is recorded as scholarly metadata in `tch:vasubandhu` → `dating.scholarly`.

### Sthiramati, Dharmapāla, Paramārtha and the Chinese line
- Sthiramati: `tch:sthiramati`, `src:trimsikabhasya`, `src:madhyantavibhagatika`, `src:pancaskandhavibhasa`.
- Dharmapāla: `tch:dharmapala`, `src:cheng-weishi-lun`, `src:cheng-weishi-baosheng-lun`, `src:guan-suoyuan-lun-shi`.
- Paramārtha and the ninth consciousness: `tch:paramartha`, `trm:amalavijnana`, `lin:shelun`, `src:zhuanshi-lun`, `src:jueding-zang-lun`, `dsp:number-of-consciousnesses`.
- Chinese lineage: `tch:xuanzang`, `tch:kuiji`, `tch:woncheuk`, `tch:silabhadra`, `tch:dosho`, `lin:dilun`, `lin:hosso`. U54 (Faxiang) is referenced.

### Dignāga
- `src:pramanasamuccaya` (six chapters), `src:pramanasamuccayavrtti`, `src:visalamalavati`.
- `src:alambanapariksa` (+ vṛtti, ṭīkā), `src:nyayamukha`, `src:hetucakra`, `src:trikalapariksa`.
- `src:nyayapravesa`, which is Śaṅkarasvāmin's, not Dignāga's.
- Doctrines:
  - two means of knowledge: `cpt:two-pramanas`
  - exclusion: `cpt:apoha`, `trm:apoha`
  - three characteristics of a valid reason: `cpt:trairupya`
  - reflexive awareness: `cpt:svasamvedana`
  - wheel of reasons: `cpt:hetucakra`

### Dharmakīrti
- The seven treatises: `src:pramanavarttika` (+ `src:pramanavarttikasvavrtti`), `src:pramanaviniscaya`, `src:nyayabindu`, `src:hetubindu`, `src:sambandhapariksa`, `src:vadanyaya`, `src:santanantarasiddhi`.
- The Pramāṇasiddhi chapter:
  - the Buddha as authoritative: `tea:pramanavarttika:1.9`, `1.34-35`, `1.147-149`; `cpt:buddha-as-pramana`
  - rebirth: `tea:pramanavarttika:1.36-37`, `cpt:proof-of-rebirth-dharmakirti`, `dsp:mind-body-rebirth`

### Later logicians
- `tch:devendrabuddhi`, `tch:sakyabuddhi`, `tch:dharmottara` (+ 4 of his works), `tch:prajnakaragupta` (`src:pramanavarttikalankara`).
- `tch:jnanasrimitra` (`src:jnanasrimitra-nibandhavali`, `src:sakarasiddhisastra`).
- `tch:ratnakirti`: `src:ksanabhangasiddhi-ratnakirti`, `src:isvarasadhanadusana`, `src:apohasiddhi`, `src:santanantaradusana` and others.
- `tch:ratnakarasanti`: `lin:alikakaravada`, `src:antarvyaptisamarthana`, `src:prajnaparamitopadesa-ratnakarasanti`.
- `tch:moksakaragupta`: `src:tarkabhasa-moksakaragupta`.
- Also: `tch:jinendrabuddhi`, `tch:vinitadeva`, `tch:arcata`, `tch:durvekamisra`, `tch:karnakagomin`, `tch:manorathanandin`, `tch:jitari`, `tch:sankaranandana`, `tch:subhagupta`, `tch:isvarasena`, `tch:sankarasvamin`.
- Tibetan reception: `src:tshad-ma-rigs-gter`, `src:rnam-grel-thar-lam-gsal-byed`, `src:bsdus-grwa`, `prc:tshad-ma-debate`.

### Concepts named in the brief
- Eight consciousnesses: `cpt:eight-consciousnesses`, `cpt:alaya-vijnana`, `cpt:klista-manas`, `cpt:three-transformations-of-consciousness`.
- Seeds and imprints: `cpt:bija-vasana`, `cpt:six-characteristics-of-seeds`, `dsp:seeds-innate-or-perfumed`.
- Three natures and three naturelessnesses: `cpt:three-natures`, `cpt:three-naturelessnesses` (both shared with U39), plus `trm:parikalpita-svabhava` and its sibling terms.
- Mind-only / cognition-only: `cpt:vijnaptimatrata`, `trm:vijnaptimatra`, `trm:cittamatra`.
- Transformation of the basis: `cpt:asraya-paravrtti`.
- Four wisdoms and how they map to the consciousnesses: `cpt:four-wisdoms`, `tea:cheng-weishi-lun:10`, `tea:mahayanasutralamkara:9.67-76`.
- Five paths and ten grounds: teachings that feed U51's `pth:five-paths` and `pth:ten-bhumis`, plus `cpt:five-paths-yogacara` and `tea:abhidharmasamuccaya:2.1.five-paths`.
- Lineage (gotra) theory: `cpt:gotra-theory` (related to U39's `cpt:five-gotras`).
- Pramāṇa doctrines:
  - `cpt:svalaksana-samanyalaksana`
  - `cpt:momentariness-arguments`
  - `cpt:sakara-nirakara`, `dsp:sakara-nirakara`, `trm:satyakara`, `trm:alikakara`
- Yogācāra meditation path:
  - `pth:yogacara-entry-into-mind-only` (Mahāyānasūtrālaṃkāra 14)
  - `cpt:four-yogic-stages`, `prc:four-yogic-stages-lankavatara`
  - `prc:entry-into-cognition-only`
  - the nine stages: `cpt:nine-stages-calm-yogacara`, `prc:nine-mental-abidings`
  - five faults and eight remedies: `obs:five-faults-of-samatha`, `prc:eight-antidotal-formations`
  - `pth:sravakabhumi-seven-attentions`
  - `pth:bodhisattvabhumi-thirteen-viharas`
  - `pth:cheng-weishi-lun-five-stages`

### Disputes
- **Yogācāra vs Madhyamaka:** `dsp:yogacara-madhyamaka` (partially reconciled under P4-stage/P1-level, with both schools' objections recorded). U40 had no dispute on this yet — please link.
- **Registry disputes:** `dsp:isvara`, `dsp:status-of-veda`, `dsp:is-there-a-self` and `dsp:number-of-pramanas` are referenced from teachings only; U50 owns them.
- **New disputes:** `dsp:existence-of-alaya`, `dsp:number-of-consciousnesses`, `dsp:seeds-innate-or-perfumed`, `dsp:sakara-nirakara`, `dsp:other-minds-buddhist`, `dsp:mind-body-rebirth`, `dsp:is-perception-non-conceptual`.
- **Sides added to other units' disputes:** `dsp:external-objects`, `dsp:apoha`, `dsp:momentariness`, `dsp:self-awareness-of-cognition`, `dsp:omniscience`, `dsp:svatah-paratah-pramanya`, `dsp:mahayana-buddhavacana`.
- **Pratyabhijñā's engagement with Dharmakīrti:** `brw:pramana-buddhist-to-pratyabhijna` (added to U19's id); `dsp:pratyabhijna-vs-buddhist-logicians` is linked from teachings.

### Ultimate views
- `ult:yogacara`: the perfected nature / suchness / dharmadhātu. The caveat records that it is not a self, not a creator and not a cosmic mind, and that the school teaches different lineages.
- `ult:pramana-buddhist`: `tradition_denies_single_ultimate: true` (a plurality of momentary particulars, and non-dual cognition).

### Section D checklist, per lineage
**Yogācāra**
- Consciousness and its states: `cpt:states-without-mind-consciousness`, `cpt:non-conceptual-wisdom`, `cpt:luminous-mind`.
- Self: `cpt:klista-manas`, `cpt:two-selflessnesses`.
- Mind: `cpt:fifty-one-mental-factors`.
- Body: `obs:dausthulya`, `trm:prasrabdhi`, `phn:msa-pliancy-body-melting`. The lineage teaches no channel or centre anatomy.
- Matter: `trm:paramanu`, `cpt:receptacle-world-yogacara`.
- Ethics: `cpt:three-kinds-of-bodhisattva-discipline`, `prc:bodhisattva-vow-yogacara`, `cpt:ten-paramitas`.
- Karma and rebirth: `cpt:yogacara-rebirth`, `cpt:mental-karma-primacy`.
- Liberation: `cpt:apratisthita-nirvana`, `cpt:three-bodies-yogacara`.
- Signs and powers: `cpt:abhijna-yogacara`, plus the `phn:*` items.
- Teacher and transmission: `cpt:maitreya-transmission`, `cpt:ten-masters-cheng-weishi-lun`, `cpt:three-turnings`, `cpt:five-sciences`.
- Sound and language: `cpt:inexpressible-nature`, `cpt:mental-speech-and-names`.
- Death: `cpt:yogacara-death` (low confidence).

**Pramāṇa school**
- Perception: `cpt:perception-buddhist`, `cpt:yogic-perception`, `prc:bhutartha-bhavana`.
- Mind: `cpt:pramana-phala-identity`, `cpt:other-minds`.
- Self: `obs:self-grasping-pramana`.
- Practice: `prc:cultivation-of-compassion-pramana`, `prc:nairatmya-bhavana-pramana`.
- Testing the teacher: `cpt:testing-the-teacher-pramana`, `tea:tattvasangraha-panjika:1-6.gold-test` (the "test my word like gold" verse, checked in the local text).
- Debate: `cpt:debate-ethics-buddhist`.
- Language: `trm:apauruseya`, `trm:sabda`, `trm:aptavada`.
- The school has no path map of its own; it relies on the five paths.

### Corrections to the unit brief
- **"Four yogic stages of the Laṅkāvatāra/Madhyāntavibhāga."** The four-stage verses are Laṅkāvatāra 10.256–258 (Nanjio numbering, recalled; wording checked as quoted in the Bhāvanākrama). The Madhyāntavibhāga has no such four-stage list. The comparable Maitreya passages are Madhyāntavibhāga 1.6–8 (apprehension becoming non-apprehension) and Mahāyānasūtrālaṃkāra 14.23–28 (the four stages of the path of preparation read as mind-only).
- **"Hetucakra."** The Tibetan title is Hetucakraḍamaru (also called Hetucakranirṇaya).
- **Nyāyapraveśa.** It is Śaṅkarasvāmin's, not Dignāga's. The Tibetan translation (from Chinese) credits Dignāga, and this is recorded as a doubtful attribution.
- **Pramāṇavārttika chapter order.** Editions differ; see §0.

### Notes for merge and dedupe
- U41's own teachings on Saṃdhinirmocana chapters 5–8 and the Laṅkāvatāra's ocean-and-waves and five-lineages passages were **removed**. They duplicate U39's `tea:samdhinirmocana-sutra:5/6/7/7-2/8` and `tea:lankavatara-sutra:2.p20/2.p27`, which U41 now cites. `tea:lankavatara-sutra:10.256-258` is U41's own.
- `dsp:are-things-momentary` (U09) duplicates `dsp:momentariness` (U11).
- `dsp:object-independent-of-mind` (U10) overlaps `dsp:external-objects`.
- U11's Buddhist side in `dsp:svatah-paratah-pramanya` gives only the doxographic formula ("invalidity intrinsic, validity extrinsic"). U41 added Dharmakīrti's and Śāntarakṣita's own positions to that dispute.
- New disambiguated ids:
  - `tch:haribhadra-buddhist` (the Abhisamayālaṃkāra commentator, not the Jain `tch:haribhadra`)
  - `tch:dharmapala` (the Yogācāra master, not the Pāli commentator)
  - `tch:nanda-yogacara`
  - `src:tarkabhasa-moksakaragupta`
- Shared ids U41 contributed to:
  - teachers: `tch:vasubandhu`, `tch:paramartha`, `tch:xuanzang`, `tch:santaraksita`, `tch:kamalasila`, `tch:sakya-pandita`, `tch:gyaltsab-je`, `tch:ngok-loden-sherab`, `tch:maitripa`, `tch:tsongkhapa`
  - concepts: `cpt:luminous-mind`, `cpt:ten-paramitas`
  - obstacles: `obs:laya`, `obs:viksepa`, `obs:two-obscurations`, `obs:nine-samyojanas`
  - practices: `prc:asubha-bhavana`, `prc:four-immeasurables`
  - sources: `src:tattvasangraha`, `src:tattvasangraha-panjika`
- Modern labels ("realist", "idealist") were replaced by the traditions' own terms: proponents of external objects, proponents of cognition-only.

## 2. Least-sure items (check these first for hallucination)
- **Low-confidence teachings (7):**
  - `tea:dharmadharmatavibhaga:2` (the ten headings of the transformation of the basis)
  - `tea:sravakabhumi:3.prasrabdhi` (the passage was not located in the e-text)
  - `tea:viniscayasamgrahani:1.alaya-proofs` (the eight proofs of the ālaya)
  - `tea:vyakhyayukti:4`
  - `tea:tarkabhasa-moksakaragupta:3.tenets`
  - `tea:prajnaparamitopadesa-ratnakarasanti:1`
  - `tea:bahyarthasiddhikarika:1`
- **Mahāyānasaṃgraha teachings** (chs. 1, 2, 3, 8, 9, 10): chapter-level only, from memory. The six characteristics of seeds and the four investigations are recalled.
- **Cheng weishi lun teachings:** fascicle numbers are recalled (the four parts of cognition in juan 2; five stages in juan 9–10; four wisdoms in juan 10). So are the ten masters' names and the view each is said to hold (Candrapāla / Nanda / Dharmapāla on seeds; Nanda / Sthiramati on the parts of cognition).
- **Taishō numbers** throughout are recalled (CBETA volumes T30–31 and T44 are not local), e.g. T1579, T1585, T1586, T1590, T1593/1594, T1602, T1604–1606, T1609, T1612, T1614, T1624/1625, T1628–1630, T1830, T1840, T1861, T1587, T1584, T1591.
- **Tengyur attributions recalled rather than checked** (the titles themselves were checked):
  - D4033 → Jñānagarbha
  - D4053 → Jinaputra
  - D4071 → Sumatiśīla
  - D4208 identified as the Nyāyapraveśa
  - D4243–4247 → Śubhagupta ("dge srung" = Kalyāṇarakṣita)
  - D4248–4253 → Dharmottara
  - D4256–4257 → Śaṅkaranandana
  - D4259 → Ratnākaraśānti (doubtful)
  - Also D3993 for Vasubandhu's Daśabhūmika commentary.
- **Teachers with low confidence or uncertain dates:** Guṇamati, Jinaputra, Sumatiśīla, Nanda, Ārya Vimuktisena, Jitāri, Śaṅkaranandana, Śubhagupta. Many dates are marked low.
- **Tradition's accounts recalled from Bu ston, Tāranātha and Xuanzang:**
  - Dignāga's cave and Mañjuśrī
  - Dharmakīrti serving in Kumārila's household
  - Sthiramati as a pigeon in a former life
  - Śīlabhadra's dream
  - Bhāviveka waiting for Maitreya
  - the Candragomin–Candrakīrti debate
  - Maitrīpa's rediscovery of two Maitreya texts
- **Other doubtful items:**
  - `cpt:yogacara-death`: the "last to leave, first to come" account and the direction of cooling are recalled, not located.
  - `cpt:four-tenet-systems` as a closing section of the Tarkabhāṣā.
  - The Tibetan classification of Pramāṇavārttika commentators into lines (soft-pedalled in the teacher summaries).
  - `src:tshad-ma-yid-kyi-mun-sel` (title and role).
  - The Buddhist-logic sides' citations of opponents in disputes, all marked "recalled": Uddyotakara on exclusion, Tattvārtha Sūtra 5.30, Brahmasūtrabhāṣya 2.2.25, Vākyapadīya 1.123/1.131, Madhyamakāvatāra 6.72–76, Bodhicaryāvatāra 9.17–25, Madhyamakālaṃkāra 91–93.
- **Path bands:** the band assignments on the four path maps are U41's interpretation (logged). The pairing of the Bodhisattvabhūmi abodes 3–12 with grounds 1–10 is recalled.

## 3. Gaps (belong here, not created responsibly)
- **Yogācārabhūmi:** the remaining bhūmis (manobhūmi, samāhitā-bhūmi, śrutamayī and others) have no teachings; the other compendia are thin.
- **Indian commentaries without teachings:**
  - Pratyekabuddhabhūmi
  - Guṇaprabha's Bodhisattvabhūmi commentary
  - Sāgaramegha's Bodhisattvabhūmivyākhyā (D4047)
  - Bandhuprabha's Buddhabhūmyupadeśa (on the four wisdoms, T1530)
  - Dharmapāla's commentary on the Catuḥśataka (T1571)
- **Pramāṇa commentaries not created:**
  - Ravigupta, Yamāri, Jayānanta, Jina (the Pramāṇavārttikālaṅkāra commentaries, D4222–4226)
  - Kamalaśīla's Nyāyabindupūrvapakṣasaṃkṣipta (D4232), Jinamitra's piṇḍārtha (D4233)
  - Śaṅkaranandana's Pramāṇavārttika commentary
  - Jitāri's Jātinirākṛti
  - Jñānaśrībhadra's Pramāṇaviniścaya commentary
  - Durvekamiśra's Hetubinduṭīkāloka
- **Individual works:** the separate works inside Jñānaśrīmitra's and Ratnakīrti's collected works (e.g. Vyāpticarcā, Yoginirṇaya, Pramāṇāntarbhāva) have no entries of their own.
- **Tibetan and Chinese reception:**
  - Tibetan: Tsongkhapa's and Gyaltsab's Abhisamayālaṃkāra commentaries, Khedrup's Tshad ma sde bdun rgyan, Go Rampa and Śākya Chokden on Yogācāra, Dolpopa's reading of the Maitreya texts (U48 owns Jonang).
  - Chinese: Xuanzang's Verses on the Eight Consciousnesses; the Japanese Hossō works.
- **Phenomenology:** the Śrāvakabhūmi's accounts of the absorptions, and the signs of the paths of preparation beyond the Mahāyānasūtrālaṃkāra, were not extracted.
- **No subtle-body teaching:** this lineage has no channels, centres or energy practices. That is recorded as absence, not as an omission.

## 4. Out of reach
- No Sanskrit survives for the Mahāyānasaṃgraha, the Karmasiddhi, the Vyākhyāyukti (Tibetan only), or the complete Dharmadharmatāvibhāga (only fragments).
- For Dignāga's Pramāṇasamuccaya, only ch. 1 is reconstructed; Jinendrabuddhi's commentary is being edited and is not local.
- The Pramāṇaviniścaya ch. 3 Sanskrit is not local.
- The Nyāyamukha exists in Chinese only.
- The Chinese Yogācāra corpus (T30–31, T43–44) is not in `sources_raw/cbeta` (only T08, T12, T47, T48 are present), so T numbers and fascicle references could not be checked.
- Tibetan oral commentarial traditions (tshad ma debate lore, the Maitreya-text transmission lineages) are documented only in secondary Tibetan histories.
