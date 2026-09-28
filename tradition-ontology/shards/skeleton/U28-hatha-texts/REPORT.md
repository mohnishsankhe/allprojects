# U28-hatha-texts — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Unit scope: coverage map A10 — the haṭha, tantric and Nāth yoga **texts** and their **concepts**. U28 owns `lin:hatha-yoga` and `ult:hatha-yoga`.
Generators are in `_gen/` (common, part1–part9), and all of them can be re-run.

**Method.** Everything is from model knowledge (skeleton level). For the texts that exist in `sources_raw/`, verse numbers were checked read-only against the local e-texts:
- Haṭhapradīpikā: prepared vulgate plus the Muktabodha Jyotsnā e-text M00243.
- Gheraṇḍa Saṃhitā: Thomi edition, GRETIL.
- Śiva Saṃhitā: Muktabodha M00082.
- Dattātreyayogaśāstra: the 154-verse vulgate (sanskritdocuments / eBhāratī).
- Gorakṣaśataka: GRETIL (Kuvalayananda–Shukla).
- Haṭhatattvakaumudī: Lonavla edition, chapter colophons.
- Yogacintāmaṇi: Muktabodha M00536, colophons.

Where the wording was taken from those e-texts it is quoted in `original` with the edition named. Each teaching's `notes` says which edition's numbering it follows. For the Śiva Saṃhitā and the Dattātreyayogaśāstra, the numbering of Mallinson's editions differs from the numbering used here.

## 1. Checklist (coverage-map A10 and the unit brief's MUST-COVER)

### Texts
| item | id(s) |
|---|---|
| Amṛtasiddhi — the earliest text; Buddhist–Śaiva setting; bindu; mahāmudrā, mahābandha, mahāvedha | `src:amrtasiddhi`; `tea:amrtasiddhi:topic.{bindu,sun-moon,madhyama,three-mudras,avasthas}`; `src:amrtasiddhimula`; `brw:amrtasiddhi-buddhist-to-hatha` |
| Dattātreyayogaśāstra — the four yogas; Yājñavalkya's eight limbs and Kapila's haṭha | `src:dattatreyayogasastra`; 25 teachings: `tea:dattatreyayogasastra:9-10`, `11-13`, `14-24`, `25-29`, `37-38`, `119-120` and others |
| Vasiṣṭha Saṃhitā | `src:vasistha-samhita`; `tea:vasistha-samhita:topic.kundalini`, `topic.pratyahara-marmas` |
| Vivekamārtaṇḍa | `src:vivekamartanda`; 3 teachings |
| Gorakṣaśataka (the several texts of that name) | the source entries are U21's (`src:goraksasataka`, `-briggs`, `-mallinson`, `src:goraksa-paddhati`); U28 added 16 teachings `tea:goraksasataka:*` in GRETIL numbering |
| Yogabīja | `src:yogabija`; 4 teachings |
| Amaraughaprabodha | U21 owns `src:amaraugha-prabodha`; referenced in the lineage; U28 wrote no teachings for it |
| Yoga section of the Śārṅgadhara Paddhati | `src:sarngadhara-paddhati`; `tea:sarngadhara-paddhati:topic.two-hathas` |
| Khecarīvidyā (restricted) | `src:khecarividya` (restricted); 4 teachings, 3 flagged restricted; `src:brhatkhecariprakasa` |
| Śiva Saṃhitā (five paṭalas) | `src:siva-samhita`; 29 teachings |
| Haṭhapradīpikā (four upadeśas; Svātmārāma; lineage list 1.5–9) | `src:hatha-yoga-pradipika`; 127 teachings; `tea:hatha-yoga-pradipika:1.5-9`; `cpt:hyp-mahasiddha-list`; `tch:svatmarama` |
| Gheraṇḍa Saṃhitā (seven limbs; 32 postures; 25 mudrās) | `src:gheranda-samhita`; 38 teachings; `tea:gheranda-samhita:1.9-11`, `2.3-6`, `3.1-3`; `cpt:ghatastha-seven-sadhanas`, `cpt:thirty-two-asanas-gheranda`, `cpt:twenty-five-mudras-gheranda` |
| Haṭharatnāvalī (Śrīnivāsa) | `src:hatharatnavali`; `tch:srinivasa-hatharatnavali`; 3 teachings |
| Jogapradīpikā (Jayatarāma) | `src:jogapradipika`; `tch:jayatarama` |
| Yoga Yājñavalkya (Gārgī and Yājñavalkya) | `src:yoga-yajnavalkya`; `tch:gargi-yoga-yajnavalkya`; 4 teachings; `pth:yoga-yajnavalkya-eight-limbs` |
| Yogatārāvalī (attributed to Śaṅkara) | `src:yogataravali`; 3 teachings |
| Amanaska | `src:amanaska`; 4 teachings; `dsp:amanaska-critique-of-hatha` |
| Haṭhābhyāsapaddhati | `src:hathabhyasapaddhati`; `tch:kapalakurantaka` |
| Śiva Svarodaya | `src:siva-svarodaya`; 4 teachings; `cpt:svara-science`, `cpt:five-tattvas-in-breath` |
| Pūrṇānanda's Ṣaṭcakranirūpaṇa and the Pādukāpañcaka | `src:sat-cakra-nirupana`, `src:sritattvacintamani`, `src:padukapancaka`; `tch:purnananda`, `tch:kalicarana`; 7 teachings; `pth:satcakra-ascent` |
| Haṭhapradīpikā-Jyotsnā (Brahmānanda) | `src:hatha-yoga-pradipika-jyotsna`; `tch:brahmananda-jyotsna`, `tch:merusastrin`; `tea:…-jyotsna:1.1`, `1.11` (checked) |
| Haṭhatattvakaumudī (Sundaradeva) | `src:hathatattvakaumudi` (56 udyotas, checked); `src:hathasanketacandrika`; `tch:sundaradeva`; 5 teachings |
| Yuktabhavadeva | `src:yuktabhavadeva`; `tch:bhavadeva-misra` |
| Yogacintāmaṇi | `src:yogacintamani-sivananda`; `tch:sivananda-yogacintamani`, `tch:ramacandra-sadananda-sarasvati` |
| Śrītattvanidhi (recent) | `src:sritattvanidhi`; `tch:mummadi-krsnaraja-wodeyar` (both marked recent) |
| Further texts | `src:kumbhakapaddhati` (restricted), `src:satkarmasangraha`; a contribution to `src:sivayoga-pradipika` |
| The Yoga Upaniṣads (A2) | referenced, not recreated (owned by U04): `brw:hatha-to-yoga-upanisads`, `dsp:yoga-or-knowledge-for-liberation`, and the lineage's transmissions_given |

### Concepts
| item | id(s) |
|---|---|
| bindu and its preservation | `cpt:bindu`, `cpt:bindu-natha`, `trm:bindu`, `trm:rajas-hatha`, `obs:bindu-pata` |
| the sun and moon channels, suṣumnā | `cpt:sun-moon-fire`, `cpt:susumna-central-channel`, `trm:ida`, `trm:pingala`, `trm:susumna`, `trm:citrini`, `trm:vajrini`, `trm:brahma-nadi` |
| amṛta and the moon at the palate | `cpt:amrta-natha`, `trm:amrta`, `trm:soma`, `trm:candra`, `trm:surya` |
| kuṇḍalinī and the three knots | `cpt:kundalini`, `cpt:three-granthis`, and the three granthi terms |
| the four yogas; rājayoga as the goal (HYP 1.1–2) | `cpt:four-yogas`, `cpt:rajayoga-goal`, `cpt:hatha-raja-interdependence`, `cpt:mahayoga-unity`, `cpt:meaning-of-hatha` |
| the four stages of practice | `cpt:four-avasthas-of-yoga`, `pth:hyp-nada-four-stages`; teachings for U51's `pth:hatha-four-stages` |
| the nāḍīs (72,000; ten or fourteen principal) | `cpt:nadis` |
| the ten vāyus | `cpt:ten-vayus` and ten terms |
| the cakra systems | `cpt:cakras` (lin:hatha-yoga and lin:sakta definitions), `cpt:sixteen-adharas`, `cpt:three-laksyas`, `cpt:vyoma-pancaka`; relation to U21's `cpt:nava-cakra-ssp` |
| laya, nāda, manonmanī / unmanī | `cpt:laya-natha`, `cpt:nada`, `cpt:ten-inner-sounds`, `cpt:unmani` |
| the samādhi synonyms (HYP 4.3–4) | members of `cpt:rajayoga-goal`; `tea:hatha-yoga-pradipika:4.3-4` |
| sahaja | `cpt:sahaja` |
| Further concepts | `cpt:mind-breath-bond`, `cpt:kala-vancana`, `cpt:kaya-siddhi`, `cpt:utkranti`, `cpt:pinda-brahmanda`, `cpt:jiva-paramatma-union-hatha`, `cpt:karma-in-hatha`, `cpt:internalized-kaula-transgression`, `cpt:rasa-mind-analogy`, `cpt:eight-kumbhakas`, `cpt:ten-mudras-hyp`, `cpt:satkarma-doctrine`, `cpt:eighty-four-asanas`, `cpt:three-dhyanas-gheranda`, `cpt:six-samadhis-gheranda`, `cpt:four-grades-of-aspirant`, `cpt:eligibility-for-hatha` |

### Warnings recorded as teachings
| item | id(s) |
|---|---|
| Disorders from improper prāṇāyāma | `tea:hatha-yoga-pradipika:2.15`, `2.16-17`, `2.18`; `tea:goraksasataka:51`; `obs:improper-pranayama`; `cpt:dangers-of-forcing` |
| What destroys and what promotes yoga | `tea:hatha-yoga-pradipika:1.15`, `1.16`; `obs:six-destroyers-of-yoga` and its six members |
| Moderate diet | `tea:hatha-yoga-pradipika:1.58`; `prc:mitahara`; `cpt:mitahara` |
| The guru | `cpt:guru-in-hatha`; HYP 1.14, 3.2-3, 3.77-79, 3.128-130, 4.8-9; SS 3.11-14; GS 7.1 |
| Secrecy | `cpt:secrecy-and-testing`; HYP 1.11, 3.8-9 |
| Powers as obstacles | `tea:dattatreyayogasastra:91-95`; `obs:siddhis-as-obstacles` |
| The place and hut | `tea:hatha-yoga-pradipika:1.12`, `1.13`; GS 5.3–9; `cpt:yoga-matha`; `obs:yoga-faults-wrong-place` |
| The dangers of forcing | `cpt:dangers-of-forcing`; HYP 3.80-81; GS 5.8-9 |

### Phenomenology
| item | id(s) |
|---|---|
| Signs of success (HYP 2.78) | `phn:hyp-hatha-siddhi-signs` |
| Signs of nāḍī purification | `phn:hyp-nadi-suddhi-signs`, `phn:dys-nadi-suddhi-signs` |
| The sounds of the nāda stages | `phn:hyp-nada-{arambha,ghata,paricaya,nispatti}`, `phn:hyp-inner-sounds-sequence` |
| Other experiences | 18 more: kuṇḍalinī awakening, the samādhi state, the signs of breath-mastery in the Śiva Saṃhitā, Gheraṇḍa and DYŚ, the powers in the DYŚ, the Śiva Saṃhitā's paricaya vision, and others |

### Path maps
- Referenced, owned by U51, with the teachings they rest on:
  - `pth:hatha-four-stages`: HYP 4.69–77; DYŚ 9–10, 81–83, 97–99, 145–147; SS 3.29–31, 3.60–67; Amṛtasiddhi topic.avasthas.
  - `pth:dattatreya-four-yogas`: DYŚ 9–29; SS 5.9–14.
  - `pth:gheranda-seven-limbs`: GS 1.9–11.
- New and banded: `pth:hyp-nada-four-stages`, `pth:hyp-practice-sequence`, `pth:yoga-yajnavalkya-eight-limbs`, `pth:gheranda-six-samadhis` (parallel routes, not a sequence), `pth:satcakra-ascent` (restricted).

### Disputes
- `dsp:hatha-vs-raja`: partially reconciled under P4-stage and P3-path, with the Amanaska's objection recorded.
- `dsp:amanaska-critique-of-hatha`: partially reconciled under P4-stage.
- `dsp:necessity-of-satkarma`: reconciled under P4-stage; the objection of the 'some teachers' of HYP 2.37 is recorded.
- Effort or grace in awakening kuṇḍalinī: `dsp:kundalini-effort-grace` is referenced, not written (U50 owns it). Evidence teachings for U50: HYP 3.2-3, 3.5, 3.66-69, 3.105-108, 3.109-110, 3.111, 4.8-9, 4.10-12; GS 7.1; SS 4.14; Amanaska 2.topic.effortless; ṢCN 50-54.
- Also referenced: `dsp:yoga-or-knowledge-for-liberation` (U04), `dsp:siddhis-sign-or-obstacle` (U04), `dsp:women-caste-liberation` (U50).

### Ultimate
`ult:hatha-yoga`. Its caveat records that the metaphysics is borrowed (Advaita, Śaiva, Vaiṣṇava, and Buddhist in the Amṛtasiddhi).

### Corrections to the MUST-COVER list
1. The Gorakṣaśataka source entries belong to U21. The GRETIL text labelled "Kuvalayananda–Shukla" is the six-limbed Vivekamārtaṇḍa-family text.
2. GS 2.1–2: Śiva taught 8,400,000 postures. Of these, 84 are distinguished — "a hundred less sixteen" (ṣaḍdaśonaṃ śatam) — and 32 are auspicious for mortals.
3. The ha = sun / ṭha = moon verse: the Jyotsnā cites it as from the Siddhasiddhāntapaddhati, but modern scholarship places it in the Yogabīja.
4. DYŚ 42 in the vulgate reads *kṛpaiva kāraṇaṃ siddheḥ* ("grace is the cause of success"). The parallel HYP 1.66 reads *kriyaiva* ("practice"). This is recorded in notes as not yet reconciled at the text level.
5. The vulgate HYP prints ten yamas and ten niyamas with 1.17, as an interpolation. They are recorded separately as `tea:…:1.17/2`.
6. The "12" in "cakra systems (6 + sahasrāra; 9; 12; …)" was not identified in any text. The only twelve U28 found is the GS's twelve-petalled lotus inside the sahasrāra (6.9–14).

### Id alignment with other units
- To avoid duplicates, U28 used U21's existing ids: `cpt:rajayoga-goal`, `cpt:kala-vancana`, `cpt:kaya-siddhi`, `cpt:sun-moon-fire`, `cpt:amrta-natha`, `cpt:bindu-natha`, `cpt:laya-natha`, `cpt:sunya-natha`, `cpt:sahaja`, `cpt:samarasa`, `cpt:secrecy-and-testing`, `obs:dambha`, `obs:bindu-pata`.
- U28 also used U04's `cpt:four-yogas`, `cpt:four-avasthas-of-yoga`, `cpt:kundalini`, `cpt:three-granthis`, `cpt:nadis`, `cpt:ten-vayus`, `cpt:cakras`, `cpt:unmani`, `cpt:nada` and others.
- Flagged for the merge: `cpt:vyoma-pancaka` (U04) and `cpt:five-vyomas` (U21) are the same list under two ids. `cpt:three-laksyas` has different categories in U04 and U21.
- Practice ids for U29 follow the slug rule, for example `prc:viparitakarani` and `prc:sanmukhi-mudra`. U21 has `prc:viparita-karani` and U04 has `prc:shanmukhi-mudra`, which will need de-duplicating. The 27 prc ids referenced but not yet defined are all in U29's catalogue: postures, retentions, bandhas, cleansing acts and mudrās.
- `trm:candali` and `trm:bodhicitta` are referenced as analogues (logged). The Buddhist units will create them.

## 2. Least sure — possible hallucinations to check first
- **Amṛtasiddhi:** the chapter count (36 vivekas), the attribution to Virūpākṣa/Virūpa, and the term "madhyamā". All its teachings use topic-level refs. Also `src:amrtasiddhimula` (existence recalled only from the 2021 edition's title).
- **Vasiṣṭha Saṃhitā:** the interlocutor Śakti (`tch:sakti-vasisthaputra`), the chapter structure and the dating.
- **Yoga Yājñavalkya:** 12 chapters, and the chapter-to-limb mapping in `pth:yoga-yajnavalkya-eight-limbs`. The provision for women and śūdras (`tea:yoga-yajnavalkya:topic.women-sudras`) is low confidence.
- **Śārṅgadhara Paddhati:** the two kinds of haṭha (Gorakṣa's, and that of "the son of Mṛkaṇḍu").
- **Yogabīja:** the wording of all four topic teachings. **Yogatārāvalī:** the verse number 2.
- **Amanaska:** the Īśvara–Vāmadeva frame (`tch:vamadeva-amanaska`), the dating of the two chapters, and the list of methods it criticizes.
- **Haṭharatnāvalī:** the author's name forms, 17th c. and Andhra origin, the list of the eight acts, and "mahāyoga".
- **Jogapradīpikā:** 1737, about 960 verses, 24 mudrās, Rāmānandī affiliation.
- **Haṭhābhyāsapaddhati:** the author Kapālakuruṇṭaka, about 112 postures, 18th c. **Śrītattvanidhi:** about 122 postures, and its dependence on the Haṭhābhyāsapaddhati.
- **Śiva Svarodaya:** all content is recalled; it has topic-level refs only.
- **Ṣaṭcakranirūpaṇa:** the verse ranges (1-2, 4-13, 14-39, 40-49, 50-54, 55). **Pādukāpañcaka:** details.
- **Kumbhakapaddhati** (Raghuvīra), **Ṣaṭkarmasaṅgraha** (Cidghanānanda), **Haṭhasaṅketacandrikā**, **Bṛhatkhecarīprakāśa** (Ballāla), **Yuktabhavadeva** (1623): existence and attribution recalled only.
- **Śivayogapradīpikā:** U28's contribution (Sadāśivayogīśvara, c. 15th c.) is low confidence.
- **GS 7.7–16 sub-refs** in `pth:gheranda-six-samadhis`, and the "two arms, white garments" detail of GS 6.11–13.
- **Identities:** `tch:gargi-yoga-yajnavalkya` versus the Upaniṣadic Gārgī; `tch:virupa` = Virūpākṣa; Allama = Allama Prabhu in HYP 1.8.
- **Path bandings** (B3 / B4 / B7) are U28's interpretation. They are logged, and they omit B5–B6 on purpose.

## 3. Gaps — belong here but not created responsibly
- Verse-level refs (and `original` wording) for every text not available locally: Amṛtasiddhi, Vivekamārtaṇḍa, Yogabīja, Khecarīvidyā, Yoga Yājñavalkya, Vasiṣṭha Saṃhitā, Yogatārāvalī, Amanaska, Haṭharatnāvalī, Jogapradīpikā, Haṭhābhyāsapaddhati, Śiva Svarodaya, Ṣaṭcakranirūpaṇa, Pādukāpañcaka, Yuktabhavadeva.
- A concordance of the Muktabodha / vulgate numbering with Mallinson's editions for the Śiva Saṃhitā and the Dattātreyayogaśāstra.
- The "12" cakra system named in the brief; the actual lists of the sixteen ādhāras, three lakṣyas and five vyomas (Siddhasiddhāntapaddhati / Haṭhatattvakaumudī — partly U21's).
- The Mahākālayogaśāstra, which the Jyotsnā cites for Ādinātha teaching Girijā: not identified.
- Teachings from the Amaraughaprabodha (the source is U21's).
- Other late haṭha compendia recalled too vaguely to enter: Yogakarṇikā, Haṭhayogamañjarī, Yogamārgaprakāśikā, commentaries on the HYP other than the Jyotsnā, and a separate entry for the 10-chapter HYP recension (noted only under editions).
- Persian and Arabic transmissions of haṭha (the Amṛtakuṇḍa / Baḥr al-Ḥayāt). Sufism is outside scope; noted for U49 as context only.
- A possible debate on householder versus renouncer eligibility (SS 5.186–212 against HYP 1.12, 1.57). It was not found as an explicit recorded debate, so no dispute was created.

## 4. Out of reach (restricted, undigitized or oral)
- **Restricted (summary and warnings only, by rule):**
  - khecarī's tongue procedure (HYP 3.33–36; Khecarīvidyā paṭala 1) and its herbal recipes (paṭala 4);
  - vajrolī, amarolī and sahajolī (HYP 3.83–103; DYŚ 137–143);
  - counts, ratios and schedules of retention (HYP 2.11; GS 5.49–57; DYŚ 58–61; GŚ 47–49; the whole Kumbhakapaddhati);
  - the method of śakticālana (HYP 3.112–120), the utkrānti breath (Haṭhatattvakaumudī), and the ṢCN's method of raising kuṇḍalinī;
  - the durations of the element-concentrations.
- **Undigitized or copyright:**
  - modern critical editions of the Amṛtasiddhi, Khecarīvidyā, Amanaska, Haṭharatnāvalī and Jogapradīpikā, and the critical Dattātreyayogaśāstra;
  - manuscripts only: Haṭhasaṅketacandrikā, Bṛhatkhecarīprakāśa.
- **Oral:** the living haṭha lineages of Nāth, Daśanāmī and Rāmānandī ascetics (U21 and U57).
