# U05-gita-epic — Phase B skeleton report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Scope: coverage map A3 (Bhagavad Gītā, the Mahābhārata's teaching sections, the Rāmāyaṇa's teaching), plus the D/E/F/G items for the two lineages this unit owns: `lin:epic-teaching` and `lin:bhagavata-early`.

**Counts:** sources 98 · teachers 102 · teachings 487 (Gītā 325; Mokṣadharma 45; other Mahābhārata 32; Nārāyaṇīya 18; Rāmāyaṇa 17; Yakṣapraśna 10; Viduranīti 7; Anugītā 6; Sanatsujātīya 6; Vyādha Gītā 6; Rājadharma 5; others 13) · terms 184 · concepts 62 · practices 41 · obstacles 20 · path maps 4 · disputes 12 · phenomenology 17 · borrowings 10 · ultimate views 2 · lineages 2 · interpretation-log lines 29. Validator: 0 errors.

**Method.** All entries come from model knowledge and stay at skeleton level. Verse numbers and wording were spot-checked against the local corpora in `sources_raw/`:
- the critical Mahābhārata text (DharmicData, ODbL);
- gita/gita (Unlicense);
- the southern-vulgate Rāmāyaṇa (DharmicData).

The generators (`_gen/_common.py`, `_gen/_tools.py`) letter-checked all 91 `original` texts and dropped any that did not match. Where a ref was checked, the entry's `notes` says so; a chapter-level ref means the passage was summarised from memory.

**Numbering:**
- Gītā: 700-verse numbering (= the critical edition).
- Mahābhārata: Critical Edition, book.chapter.verse.
- Rāmāyaṇa: southern vulgate (the numbering of the local text).
- Yakṣapraśna verses found only in the vulgate use ids of the form `vulg-3.313/n`.

## 1. Coverage checklist

**Bhagavad Gītā**
- Location, 18 chapters with traditional titles, verse count, Kashmir recension, the 745-verse "Gītāmāna" note, dating by tradition vs scholars: all in `src:bhagavad-gita`.
- Teachings per chapter: ch.1 5 · 2 46 · 3 22 · 4 25 · 5 17 · 6 25 · 7 14 · 8 15 · 9 17 · 10 12 · 11 12 · 12 12 · 13 18 · 14 13 · 15 11 · 16 9 · 17 13 · 18 39.
- Every ref on the MUST-COVER list has a `tea:bhagavad-gita:<ref>` entry. Where the id differs from the listed ref:
  - 6.5 → 6.5-6
  - 7.16 → 7.16-18
  - 8.24–26 → 8.23-26
  - 15.1 → 15.1-2
  - 18.20–40 → six sub-ranges plus 18.40
  - 18.65 and 18.66 are separate entries

**Gītā themes**
- Paths of action, knowledge, devotion and meditation: `cpt:four-yogas-of-the-gita`, the `trm:*-yoga` terms, `prc:karma-yoga`, `prc:dhyana-yoga-gita`.
- Niṣkāma karma: `cpt:niskama-karma`, `trm:karmaphala-tyaga`, `obs:attachment-to-fruits`.
- Svadharma: `cpt:svadharma`, `trm:svadharma`, `trm:paradharma`.
- Sthitaprajña: `cpt:sthitaprajna`; tea 2.54-72 plus eleven individual verses; `phn:awake-in-the-night-of-beings`.
- Kṣetra–kṣetrajña, prakṛti–puruṣa: `cpt:ksetra-ksetrajna`; tea 13.1-2, 13.5-6, 13.19-23 (plus 13.19-20, 13.21, 13.22, 13.23), 13.31-33, 13.34.
- The three guṇas: `cpt:three-gunas`, `cpt:guna-typology-of-gita-18`, `obs:guna-bondage`, `phn:guna-signs`, `phn:marks-of-gunatita`.
- The Lord's two natures: `cpt:two-natures-of-the-lord`.
- Avatāra: `cpt:avatara`, `trm:pradurbhava`, `tea:narayaniya:12.326.72-94`.
- Universal form: `cpt:visvarupa`, `phn:visvarupa-vision`, `cpt:divine-eye`.
- Yajña reinterpreted: `cpt:yajna-reinterpreted`, `prc:yajna`, `prc:inner-sacrifice-anugita`.
- Tyāga vs saṃnyāsa: `cpt:tyaga-and-samnyasa`; tea 18.1–18.11; `dsp:renunciation-or-action-gita`.
- Ch. 17 (faith, food, austerity, giving; oṃ tat sat): the four `cpt:three-kinds-*` / `cpt:threefold-austerity` concepts, `trm:om-tat-sat`.
- Ch. 16 (divine and demonic): `cpt:divine-and-demonic-endowments`; teaching 16.8 is flagged `reported_by_opponent`.
- Ch. 15: `cpt:asvattha-tree`, `cpt:three-purusas`.
- Death: `cpt:last-thought-at-death`, `cpt:two-paths-after-death`, `cpt:yogic-death`, `prc:antakala-smarana`.

**Commentators (sources, with teacher entries carrying U05's contribution only)**
- Śaṅkara, Rāmānuja, Madhva (×2), Abhinavagupta, Jñāneśvarī, Madhusūdana, Śrīdhara (`src:subodhini-sridhara`), Nīlakaṇṭha (`src:bharatabhavadipa`).
- Vallabha (`src:tattvartha-dipa-nibandha`) and the Nimbārka school (`src:tattvaprakasika-kesava-kasmiri`).
- Yāmuna, Deśika (×2), Jayatīrtha (×2), Bhāskara, Viśvanātha, Baladeva, Ānandagiri, Dhanapati, Rājānaka Rāmakaṇṭha.
- Recent (flagged `recent: true`): Tilak, Gandhi, Aurobindo.

**Mahābhārata**
- Structure: `src:mahabharata` has the 18 parvans with CE chapter counts, the 100 upaparvans, the 24,000-verse Bhārata (1.1.61) and the three starting points (1.1.50). Each of the 18 parvans has its own source entry, and the Harivaṃśa is entered as `src:harivamsa` (khila).
- Mokṣadharma: `src:moksadharma` plus sources for about twenty dialogues, including Bhṛgu–Bharadvāja, Vasiṣṭha–Karāla Janaka, Yājñavalkya–Janaka, Sulabhā–Janaka, Pañcaśikha–Janadeva, Śuka (2), Piṅgalā, Maṅki, Ajagara, Jāpaka, Tulādhāra, Kapila–Syūmaraśmi, Vṛtra, Parāśara and Haṃsa.
- The 24/25/26 principles: `cpt:twenty-four-principles-epic`, `cpt:twenty-fifth-and-twenty-sixth`.
- Anugītā: `src:anugita`, 6 teachings.
- Sanatsujātīya: `src:sanatsujatiya`, 6 teachings.
- Viduranīti: `src:viduraniti`, 7 teachings.
- Yakṣapraśna: `src:yaksaprasna`, 5 critical-text teachings plus 5 vulgate-only teachings.
- Vyādha Gītā: `src:vyadha-gita`, 6 teachings.
- Nārāyaṇīya: `src:narayaniya`, 18 teachings; `cpt:vyuhas`, `cpt:ekantika-dharma`, `cpt:svetadvipa`, `cpt:five-systems-of-knowledge`.
- Viṣṇu Sahasranāma: `src:visnu-sahasranama` plus two commentaries.
- Bhīṣma's instruction: `src:rajadharma` (with the 12.7–36 debate), `src:apaddharma`, and Anuśāsana teachings 13.1, 13.6.7, 13.114.8, 13.116, 13.154.5.

**Rāmāyaṇa**
- `src:ramayana`, the 7 kāṇḍa sources and `src:aditya-hrdaya`; 17 teachings; `cpt:rama-embodied-dharma`.
- References `src:adhyatma-ramayana` and `src:yoga-vasistha`, which U06 owns.

**Disputes, ultimate views, practices, path maps**
- Disputes (12): `dsp:gita-primary-teaching` (references `dsp:works-knowledge-grace`), renunciation-or-action-gita, renounce-or-rule, sulabha-janaka, samkhya-or-yoga-epic, one-or-many-purusas-epic, fate-or-effort, jabali-rama, varna-by-birth-or-conduct-epic, siva-or-visnu-epic, violence-and-svadharma, animal-sacrifice-epic. Teachings also link the registry disputes.
- Ultimate views: `ult:epic-teaching`, `ult:bhagavata-early`.
- D checklist: covered for both owned lineages through the concepts above.
- Practices: 41; `prc:mahaprasthana` is marked `restricted`.
- Path maps: `pth:gita-svadharma-to-entering-the-lord`, `pth:gita-devotion-ladder`, `pth:gita-ascent-in-yoga`, `pth:narayaniya-vyuha-ascent`, with bands logged.

## Corrections to the brief's MUST-COVER list
- The Gītā is Bhīṣmaparvan 23–40 in the Critical Edition (25–42 in the vulgate), 700 verses in both. Some printed editions add an opening verse to ch. 13, making 701; in those, 13.1–2 and 13.19–23 appear as 13.2–3 and 13.20–24.
- The two-paths passage begins at 8.23 (8.23–26), not 8.24.
- The Yakṣapraśna is CE 3.297–298 (vulgate 3.311–313). These famous questions are not in the critical text and are recorded as vulgate-only:
  - "the greatest wonder"
  - "dharma's truth is hidden in a cave"
  - "time cooks beings"
  - "who is happy"
  - "is a brāhmaṇa made by birth or by conduct"
  The critical text's verse saying conduct makes a brāhmaṇa is Nahuṣa's, at 3.177.16.
- Critical Edition locations of the other teaching sections:

  | Section | CE location | Vulgate |
  |---|---|---|
  | Viṣṇu Sahasranāma | 13.135 | 13.149 |
  | Sanatsujātīya | 5.41–45 | — |
  | Viduranīti | 5.33–40 | — |
  | Anugītā | 14.16–50 | — |
  | Mokṣadharma | 12.168–353 | — |
  | Nārāyaṇīya | 12.321–339 | — |

- The vulgate Nārāyaṇīya's compact avatāra list ending in Kalki is not in the critical text; CE 12.326 does not name Kalki.
- "Avatāra" and "niṣkāma karma" are not Gītā words.
- MBh 12.337.60 calls Hiraṇyagarbha the *knower* (vettā) of Yoga, not its proclaimer.
- Where the critical text differs from the vulgate, I adopted the critical reading:
  - BhG 13.20: kāryakāraṇa-
  - BhG 18.68: ya idaṃ
  - MBh 13.114.8: saṃdadyāt
  - MBh 12.171.25: bhaviṣyati

## 2. Least-certain items (check these first)
- **Sources (low confidence):** gita-bhasya-bhaskara, tattvaprakasika-kesava-kasmiri, sarvatobhadra-ramakantha, jnanadipika-devabodha, gitarthasangraha-raksa, bhasyotkarsadipika (title), tattvartha-dipa-nibandha (its Gītā section), gita-mahatmya (location), manu-brhaspati-samvada (12.194–199), unchavrtti-upakhyana; the Harivaṃśa chapter count; the Āditya Hṛdaya's status in the critical edition.
- **Teachers (low confidence):** kesava-kasmiri, dhanapati-suri, ramakantha-rajanaka, devabodha, vallabha (for the Gītā section), bhaskara (for the Gītā commentary); several commentators' dates.
- **Chapter-level summaries from memory:** MBh 12.194–199, 12.279–287, 12.289 (the yoga images), 12.298–306 beyond the checked verses, 12.308 (the course of the argument), 12.312–313, 12.318–320, 12.340–353, 3.28–33, 3.148, 3.200–202, 13.14–17, 13.126–134, 3.38–41.
- `tea:ramayana:6.18.33` is famous, but I could not find it in the local vulgate file, whose Yuddhakāṇḍa numbering is offset.
- Commentators' glosses cited in `notes` (Śaṅkara on 6.13 and 13.4; Rāmānuja on 13.4 and 18.66; the readings of 9.32), and the positions I attributed to Abhinavagupta and Bhāskara in `dsp:gita-primary-teaching`.
- Borrowings marked low confidence (Buddhist meditation vocabulary, Jain narratives, the colour doctrines).
- The inscriptional dating metadata in `lin:bhagavata-early`.

## 3. Gaps
- Not entered because title or authorship is unconfirmed: the Puṣṭimārga Gītā commentary under Vallabha's name, Puruṣottama's Gītā commentary, Hanumat, Śaṅkarānanda, Arjunamiśra and Vādirāja.
- Not found in the critical text by name, so not entered: the Śampāka, Bodhya and Hārīta Gītās, and Yayāti's teaching ("na jātu kāmaḥ").
- Covered only selectively: the Rājadharma, Āpaddharma and Anuśāsana (gifts, fasts, śrāddha). The Harivaṃśa teachings and the tīrtha lists are not itemised.
- Prāyopaveśa (fasting unto death) is not recorded; if added, it must be a restricted, summary-only entry.
- No Baroda critical-edition refs for the Rāmāyaṇa.
- The Kashmir recension's variant readings are not itemised.
- The epic layer has essentially no energy anatomy (channels, centres); nothing was invented to fill that slot.

## 4. Out of reach
- Oral recitation and exposition lineages, such as Gītā chanting and Vārkarī kīrtan on the Jñāneśvarī.
- Lost or only partly surviving commentaries.
- Undigitized manuscripts.
- The copyrighted apparatus of the critical editions (used here only for refs).

## Process notes
- The `_gen/` helpers read only `sources_raw/` and write only inside this folder.
- One read-only `git remote -v` was run in two `sources_raw/` clones; nothing was modified.
- Two ids are referenced but left undefined on purpose: `trm:jivanmukta` and `trm:nirvana`, which belong to other units.
