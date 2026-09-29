# U04-minor-upanisads — Phase C hallucination sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's sweep subagent, since subagents cannot write report files in this harness; saved by the orchestrator.)_

Output: `shards/sourcing/U04-minor-upanisads/checks.jsonl` (915 lines). `scripts/validate_shard.py` gives 0 errors.

Scripts are in `_gen/`:
- `lib.py` splits the local e-text into texts, chapters and verses.
- `muktika_list.py` holds the Muktikā order and Veda lists as read from the e-text.
- `view_tea.py` builds `tea_view.json`/`.txt`, the reviewed passages.
- `tea_judg.txt` holds the hand judgments.
- `assemble.py` writes `checks.jsonl`.

## 1. Numbers

| type | checked | confirmed | partially | corrected | not-found |
|---|---|---|---|---|---|
| src | 115 | 16 | 4 | 95 | 0 |
| lin | 1 | 1 | 0 | 0 | 0 |
| tch | 57 | 55 | 2 | 0 | 0 |
| tea | 524 | 488 | 13 | 23 | 0 |
| ult | 1 | 1 | 0 | 0 | 0 |
| cpt | 80 | 79 | 0 | 1 | 0 |
| prc | 51 | 51 | 0 | 0 | 0 |
| obs | 14 | 13 | 0 | 1 | 0 |
| phn | 30 | 27 | 0 | 3 | 0 |
| pth | 19 | 19 | 0 | 0 | 0 |
| dsp | 9 | 9 | 0 | 0 | 0 |
| brw | 12 | 11 | 1 | 0 | 0 |
| trm (low only) | 2 | 2 | 0 | 0 | 0 |
| **total** | **915** | **772** | **20** | **123** | **0** |

By method:
- text-locate: 788
- catalog+websearch: 110
- websearch: 10
- catalog: 4
- text-locate+websearch: 2
- catalog+text-locate: 1

Only the 2 low-confidence terms were checked, as the brief asks. The interpretation log is out of scope.

## 2. Method

**E-text.** The local 120-Upaniṣad e-text (`sources_raw/raw_etexts/vedaH/misc/upaniShat/mixedPF/108_Upanishads.md`) was transliterated to IAST. It was split by the collection-number headings (nos. 1-120) and the chapter colophons ("iti …upaniṣatsu …adhyāyaḥ/khaṇḍaḥ/brāhmaṇam"), and each verse or section marker was indexed.

**Teachings.** For every one of the 524 teachings, the passage at the cited ref was pulled out and read against the paraphrase.
- Where the automatic slice failed, the passage was found by hand with keyword search. This happened for chapter-level refs, unnumbered prose, and markers the e-text misnumbers (e.g. Yogakuṇḍalī 1.59 printed as "51", Yogaśikhā 6.79 printed as "71").
- All 17 `original` quotations match the e-text (5-gram score 1.00 after folding sandhi).

**Canon.** Muktikā number and Veda were checked for all 95 sources against the e-text Muktikā: the list of the 108 in 1.30-39, and the prose Veda lists with their peace-chants. All 95 match, as do the 108 entries of `src:muktika-upanisad` `canon.list`.

**Groups.** Editorial groups were checked against the local group lists (`raw_etexts/…/sAmAnyA|saMnyAsI|shaivI|yaugikI/intro-*.md`) and against Wikipedia for the Vaiṣṇava and Śākta groups. All 98 group assignments match (the 95 here plus Śvetāśvatara, Kauṣītaki and Maitrāyaṇī in U03).

**Other local witnesses.**
- Muktabodha: the Adyar 1920 Yoga Upaniṣads with commentary (20 texts) and the Adyar 1929 Saṃnyāsa Upaniṣads.
- eBhāratī: Tantrik Texts XI (1922); Jacob's Atharvaṇopaniṣadaḥ (1916); Kaṭhaśruti, Maṭhāmnāya, Nīlarudra, Allā and Caitanya e-texts.
- GRETIL: Brahmasūtrabhāṣya 3.4.17/3.4.20; Vivekacūḍāmaṇi.
- DCS: Haṭhayogapradīpikā 2.15.
- raw_etexts: Vājasaneyi Saṃhitā 34.1-6, Manusmṛti 6.35-37, Pañcadaśī Tṛptidīpa, Aparokṣānubhūti.

**Teachers.** All 47 mythic or textual teachers were found by name in the texts they are said to appear in. The 10 historical or problematic ones were checked on the web or in the catalogue.

**Other entities.** In concepts, practices, obstacles, paths, phenomenology, disputes and borrowings, every `tea:` reference resolves. The inline refs were read in the e-text. External parallels were checked locally where possible.

**Restricted practices.** All 14 restricted teachings and 7 restricted practices are summary-only, as required.

## 3. Not-found (possible hallucinations)

None. Every text, teacher and teaching could be located. What comes closest to fabrication:
- **Invented or overlong verse ranges.** These refs run past the end of the e-text:
  - Sarasvatīrahasya "11-60": the second series has only 33 verses.
  - Pañcabrahma "11-40": there are 36 verses.
  - Sītā "4-10": there are 8 sections.
  - Kṛṣṇa "3-26": there are 25 verses.
  - Sarvasāra "1-20": there are 4 sections.

  Two texts are numbered in a way that matches no edition:
  - Haṃsa "3"/"4": the e-text has vv. 1-3 plus prose sections 1-2; Adyar has 21 sections.
  - Mahāvākya "1-2/3-4/5": the e-text is unnumbered; Adyar has 12 sections.

  In every case the content exists, so these are "corrected" (with a `location` fix), not "not-found".
- **The Adyar edition default** on all 95 Muktikā sources (§4).
- **`cpt:cakras`**: "nine cakras, sixteen ādhāras" for the Maṇḍalabrāhmaṇa conflates two texts.

## 4. Corrections (in `corrections`, in the entry's own schema)

**Sources: `editions` on all 95 Muktikā texts.** This is a generator default, like the one U03 found. Every text carried the same string: "Adyar Library Upaniṣad series (Schrader, Minor Upaniṣads vol. 1: Saṃnyāsa, 1912; A. Mahadeva Sastri: Yoga 1920 … Śākta 1925) with Upaniṣad Brahmayogin's commentary".
- What is wrong: Schrader 1912 is a critical edition of twenty Saṃnyāsa texts with Schrader's own ṭippaṇī, not Brahmayogin's commentary. The Saṃnyāsa volume with Brahmayogin's commentary is Adyar 1929, ed. T. R. Chintamani Dikshit (Muktabodha M00334 metadata; archive.org).
- What was confirmed: the other years (1920, 1921, 1923, 1925, 1925) and A. Mahadeva Sastri as editor.
- Fix: each text now gets the e-text edition (unchanged) and the Adyar volume for its own group. For the 16 Saṃnyāsa texts that are among Schrader's twenty (per the archive.org contents), Schrader 1912 is added as its own entry. Kaṭharudra was not in the list of Schrader's contents returned by the search, so it gets no Schrader entry.
- Ten sources also get a `notes` correction: Haṃsa, Mahāvākya, Kālāgnirudra, Akṣamālikā, Gaṇapati, Jābāli, Bhāvanā, Bahvṛca, Vāsudeva and Pāśupatabrahma. Their refs do not follow e-text numbering, contrary to the default note.

**Teachings: `location.ref` (23).**
- Haṃsa ×8: refs changed to "1-3", "prose 1" and "prose 2".
- Mahāvākya ×3: changed to Adyar "1-5", "6" and "7".
- Amṛtanāda 27 → 28.
- Śāṇḍilya 1.60-68 → the prose after 1.68 that closes khaṇḍa 7.
- Varāha 4.2-3 (the praṇava mapping) → the opening prose of ch. 4.
- Dakṣiṇāmūrti 4-6 → 15-20.
- Pañcabrahma 11-40 → 11-36.
- Sītā 4-10 → 3-8.
- Sarasvatīrahasya 11-60 → 11-43 (the e-text numbers these 1-33).
- Kṛṣṇa 3-26 → 3-25.
- Garbha 2 → 3 and Garbha 3 → 3.
- Sarvasāra 1-20 → 1-4.
- Gaṇeśatāpanī "pūrva 1" → "uttara 1": "omityekākṣaram … gaṇeśo'yam ātmā" opens the Gaṇeśottaratāpinī.

**Other entities.**
- `cpt:cakras` (definitions): the Maṇḍalabrāhmaṇa 4.1 has nine cakras and six ādhāras; the sixteen ādhāras are Yogacūḍāmaṇi 3.
- `obs:amrtanada-faults` (description): Amṛtanāda 27 → 28.
- `phn:hamsa-ten-sounds` and `phn:hamsa-sound-effects` (ref): → "prose 2".
- `phn:sandilya-samyama-powers` (ref): → 1.68-69 (the prose closing khaṇḍa 7).

## 5. Partially confirmed (20)

**Teachings in unnumbered e-text prose (13).** The content is located, but the section numbers come from another edition and could not be checked locally:
- Kālāgnirudra ×3
- Akṣamālikā
- Gaṇapati ×2 (the refs appear to follow the usual Atharvaśīrṣa sections)
- Jābāli ×2
- Bhāvanā
- Bahvṛca ×2
- Vāsudeva ×2

**Sources and teachers.**
- `tch:sanatsujata`: the e-text Haṃsa reads "sanatsujāta uvāca", but the Adyar 1920 text and Brahmayogin's commentary read Sanatkumāra. The entry already hedges ("in this recension").
- `src:yatidharmasamuccaya`: the entry says c. 11th c., but the SUNY 1995 description of Olivelle's edition calls it a twelfth-century text. It was left uncorrected because the sources disagree; a reviewer should consider c. 11th-12th c.
- `src:yatidharmaprakasa`: the dating is unchecked.
- `src:mathamnaya-upanisad`: the dating is unchecked.
- `src:narayana-dipika` and `tch:narayana-dipikakara`: existence is confirmed; the "Colebrooke's list of 52" claim is unchecked.
- `brw:yoga-yajnavalkya-darsana`: there is no local Yoga-Yājñavalkya and the web gave no confirmation.

## 6. Least-sure items from the skeleton report — resolved

- **Haṃsa teacher:** e-text Sanatsujāta, Adyar Sanatkumāra (see §5).
- **Yogakuṇḍalī 1.59-61:** located. The e-text prints v. 59 as "51". Obstacles 8-9 read "viṣama" and "anākhya", so the uncertainty flagged in the entry is real.
- **Sannyāsa 2.101 ("cat" and "monkey"):** located (pravṛttir dvividhā … mārjārī … vānarī). The construal is still interpretive.
- **Upaniṣad Brahmayogin:** confirmed. His initiation name was Rāmacandrendra Sarasvatī (the "(?)" can go); he was based at Kāñcīpuram; he dates to the mid-18th c. and completed his Muktikā commentary in 1751; he commented on all 108.
- **Śaṅkarānanda:** c. 13th-14th c.; guru of Sāyaṇa and, in tradition, of Vidyāraṇya. Compatible with the entry.
- **Nārāyaṇa:** his date is unknown (Jacob).
- **Adyar years:** confirmed, with the Saṃnyāsa error corrected (§4). Olivelle's dating is confirmed at group level via Wikipedia, and Bouy's via reviews.
- **Outside the Muktikā:**
  - Allā: Mughal-era apocryphal text.
  - Caitanya: first printed 1887 by Bhaktivinoda.
  - Kālikā: extant in Tantrik Texts XI.
  - Kaula: Tantrik Texts XI with Bhāskararāya's commentary.
  - Maṭhāmnāya: eBhāratī e-text.

  All are confirmed.
- **Lineage attributions (Gauḍīya, Rāmānandī, Buddhist Vajrasūcī):** the Vajrasūcī is Taishō T1642, ascribed in Chinese to Dharmakīrti and in Sanskrit to Aśvaghoṣa, so the attribution is confirmed. The Gauḍīya and Rāmānandī use claims are plausible and were not checked separately.
- **Low-confidence paths:** `pth:sannyasa-six-renunciant-grades` is grounded in Nāradaparivrājaka 5, which ranks the kinds by the worlds they reach. `pth:yogatattva-four-yogas` is grounded in Yogaśikhā 1.129 ("antarbhūmikāḥ kramāt").
- **Text-corrections the skeleton logged:** confirmed in the e-text, e.g. "haṭhāvasthā" at Yogatattva 65-66 and "mahānārāyaṇāhvayam" at Muktikā 1.34. The same e-text's Nāradaparivrājaka opening reads "mahānārāyaṇādvayam", which supports the emended count of 108.
- **Veda colophons:** the Atharvan colophons are confirmed for Jābāla, Haṃsa, Āruṇika, Brahmabindu and Kaivalya, as the skeleton said. Kṣurikā and Sarvasāra also have Atharvan colophons, which the skeleton did not mention.

## 7. Notes for extraction and review (not corrections)

- **`tea:yogatattva-upanisad:12-13` and `obs:yogatattva-twenty-dosas`:** the Yogatattva says the freed jīva is "kevala". Only Yogaśikhā 1.11 says "śiva ucyate".
- **`tea:amrtanada-upanisad:2-3`:** the text says the seeker is "seeking the Brahma-world, devoted to Rudra", not that he goes to Rudra's world.
- **`ult:sannyasa`:** it cites "Avadhūta 1" for "the jīva is Śiva", but that passage is in Maitreya 2.1 and Skanda 6-10.
- **Editions and fields that could be added:**
  - `src:kathasruti-upanisad` and `src:kalika-upanisad` have no editions. Possible additions are Schrader 1912 and the eBhāratī text for the Kaṭhaśruti, and Tantrik Texts XI for the Kālikā.
  - `src:asrama-upanisad` has no dating; Olivelle gives 3rd c. CE.
  - `src:jivanmuktiviveka` has no authors field (Vidyāraṇya).
- **E-text edition entry:** the title Īśādiviṃśottaraśatopaniṣadaḥ is confirmed in the e-text itself and on archive.org. The publisher (Nirṇayasāgara) was not independently confirmed.

## 8. Could not be checked

- Section numbers of the texts that are unnumbered in the e-text (§5).
- The Yoga-Yājñavalkya parallel.
- Text-by-text scholarly dates for the Śaiva, Vaiṣṇava and Sāmānya groups; their group-level statements are generic.
- The Khecarīvidyā and Gorakṣaśataka parallels claimed in `brw:hatha-to-yoga-upanisads`. Only Śāṇḍilya 1.23 ≈ HYP 2.15 was confirmed locally.

## 9. Main web sources

- Adyar editions: archive.org in.ernet.dli.2015.345354, in.gov.ignca.7941, in.gov.ignca.7940, wg206, in.ernet.dli.2015.383591 and in.ernet.dli.2015.553699; Schrader 1912 at archive.org in.ernet.dli.2015.283511 and WorldCat 6590364.
- Wikipedia: Sannyasa Upanishads; Upanishad Brahmayogin; Vaishnava and Shakta Upanishads; Allopanishad; Sirr-i-Akbar; Bhaskararaya.
- Other: Lubin's Nīlarudra edition (academia.edu); Bhaktivinoda Institute (Caitanya Upaniṣad); wisdomlib (Śaṅkarānanda, Jīvanmuktiviveka); the BSOAS review of Bouy 1994; Olivelle's editions (SUNY 1995; Vienna 1976-77).
