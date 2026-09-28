# U01-vedic-samhitas — REPORT (Phase C hallucination sweep)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the sweep subagent. Subagents cannot write report files in this harness, so the orchestrator saves this verbatim.)_

Output: `shards/sourcing/U01-vedic-samhitas/checks.jsonl`, 502 lines. `validate_shard.py`: 0 errors (the only warning is the missing REPORT.md).

## 1. Numbers
| | checked | confirmed | partially | corrected | not-found |
|---|---|---|---|---|---|
| teachings (tea) | 290 | 287 | 2 | 1 | 0 |
| teachers (tch) | 91 | 90 | 1 | 0 | 0 |
| sources (src) | 70 | 67 | 3 | 0 | 0 |
| lineages (lin) | 18 | 18 | 0 | 0 | 0 |
| disputes (dsp) | 13 | 11 | 2 | 0 | 0 |
| practices / terms / borrowings / obstacles | 8 / 6 / 5 / 1 | 8 / 5 / 5 / 1 | 0 / 1 / 0 / 0 | 0 | 0 |
| **total** | **502** | **492** | **9** | **1** | **0** |

Coverage:
- Every source, teacher, lineage and teaching was checked.
- Every entry with confidence `low` was checked (sources, lineages, teachers, teachings, terms, practices, obstacles, borrowings, disputes).
- Every item on the Phase B "least sure" list was checked, including the dispute-side loci and the Rudra-japa multiples.
- Concepts, phenomenology, the path map and ultimate were not checked; none of them is marked low.

Methods: text-locate 403, websearch 55, text-locate+websearch 25, catalog+websearch 10, catalog+text-locate 6, catalog 3.

## 2. How the checks were made
Local texts did most of the work:
- **Ṛgveda:** GRETIL Van Nooten–Holland text for the verses (the DharmicData numbering is corrupted in long hymns), DharmicData Anukramaṇī headers for seer and deity, and Sāyaṇa's verse-by-verse bhāṣya JSON with Padapāṭha and ṛṣi/devatā attributes.
- **Atharvaveda:** GRETIL Roth–Whitney text (so "Whitney numbering" is now checkable) plus DharmicData headers.
- **Vājasaneyi Saṃhitā:** DharmicData. **Taittirīya Saṃhitā:** raw_etexts.
- **Nirukta:** the complete GRETIL text (Sarup edition), not just the DCS chapters 1–2.
- **Other texts:** Ṛgveda Khila, Padapāṭha, AV Pariśiṣṭa 49 (the Atharvaveda's Caraṇavyūha), Aitareya, Gopatha and Pañcaviṃśa Brāhmaṇas, Aṣṭādhyāyī, Mahābhāṣya, Upaniṣads, Bhāgavata and Viṣṇu Purāṇa, the two Śikṣās, and DCS Śabara, Suśruta, Caraka and Nāṭyaśāstra.

Web search covered what is not on disk: Bṛhaddevatā, Puṣpasūtra, Vikṛtivallī, the commentators' dates, śākhā regions, and recent authors.

All 172 Ṛgveda teachings were read against the Sanskrit. Every Anukramaṇī seer claim in the teacher entries was checked against the hymn headers. Every `original` quotation was compared automatically with the local text: only 10.88.15 differs in wording; the other differences are sandhi or orthography.

## 3. Correction
**tea:rgveda:10.88.15**
- **Problem:** `original.text` reads "dve sṛtī aśṛṇavaṃ…". The Ṛgveda reads "dve srutī aśṛṇavam" in GRETIL, DharmicData, and Sāyaṇa's text and Padapāṭha ("dve iti | srutī iti"). "sṛtī" is the reading of VS 19.47 and BĀU 6.2.2.
- **Fix:** only the text-layer quotation is corrected (`corrections.original`). Sāyaṇa glosses srutī as the two paths, so the paraphrase stands.

## 4. Partially confirmed (possible errors or unverifiable details)
- **tea:atharvaveda-saunaka:2.32:** the hymn and its topic are right (worm charm, seer Kaṇva, the sun slays the worms "in the cow"). But "visible and invisible" (dṛṣṭam adṛṣṭam) and "crushed with a stone" (dṛṣadā) come from AVŚ 2.31, not 2.32. For the extraction phase.
- **src:rgveda-padapatha:** the Padapāṭha's omission of 10.121.10 is confirmed (SBE 32; the GRETIL pada file carries it undivided). The omission of the Vālakhilya hymns is not confirmed, and the GRETIL Padapāṭha does give pada text for 8.49ff.
- **tea:rgveda-bhasya-sayana:upodghata:** the definition of the Veda is confirmed for the Taittirīya-Saṃhitā upodghāta. The Ṛgveda upodghāta is confirmed to argue authorlessness and self-validity. The exact wording inside the Ṛgveda upodghāta was not seen.
- **src:jnanayajna / tch:bhatta-bhaskara:** the work, its scope and its priority to Sāyaṇa are confirmed. "c. 11th century" was not found in any source.
- **src:vedadipa:** Mahīdhara, the 16th century and Vārāṇasī are confirmed. "c. 1589" is attested for his Mantramahodadhi (1588/89), not for the Vedadīpa itself.
- **trm:samana:** no occurrence of samāna as a breath was found in the local Śaunaka AV, VS or TS; it does occur in BĀU 1.5.3. The entry's Saṃhitā source is so far unsupported. (By contrast, udāna is found at AVŚ 11.8.4 and 11.8.26.)
- **dsp:nature-of-vedic-deities:** the Śabara locus can now be given as Mīmāṃsā Sūtra 9.1, devatādhikaraṇa ("na devatā prayojikā"). The full "gods are not embodied" argument was not seen.
- **dsp:rv-10-18-7-widow-reading:** "agre" is confirmed in the Padapāṭha. The "agneḥ" variant is reported only in secondary or popular sources; which digests cited it is still open.

## 5. Low-confidence or "from memory" items now confirmed
- **Nirukta:**
  - 13.9: the list of readings of the four quarters of speech is exact; in Sarup/GRETIL the passage is 13.8, with an embedded "(13,9)" marker from the older numbering.
  - 2.11 ("ṛṣir darśanāt, stomān dadarśety aupamanyavaḥ") confirmed.
  - 7.4: the wording recalled in the entry is exact.
  - 7.5 and 7.6–7 confirmed.
- **Bṛhaddevatā 2.82–84:** the brahmavādinī list and its verse numbers are confirmed.
- **Aitareya Brāhmaṇa 2.19:** the Kavaṣa episode is confirmed in the text.
- **TS 1.8.6:** the anuvāka number and "eka eva rudro na dvitīyāya tasthe" are confirmed.
- **Pāṇini:** 4.3.102 (Tittiri) confirmed; 4.3.104 lists Kaṭha among Vaiśampāyana's pupils (tch:katha).
- **Sri Sūkta and other khilas:** the Sri Sūkta is Khila 2.6, the Medhā Sūkta Khila 4.8 and the Śivasaṅkalpa Khila 4.11. The Khila has 5 adhyāyas and follows Scheftelowitz's 1906 edition.
- **AV Pariśiṣṭas:** 72 are named in AVPariś 49.4.9, and Pariśiṣṭa 49 is a Caraṇavyūha.
- **Caraṇavyūha:** Śaunaka's text lists five Ṛgveda śākhās. Note that the AV Caraṇavyūha lists seven (it adds sādhyāyana and audumbara).
- **Structural counts:**
  - Ṛgveda: 1,028 hymns, 10,552 verses.
  - Maṇḍala 9: 114 hymns.
  - Taittirīya Saṃhitā: 7 / 44 / 651.
  - Maitrāyaṇī Saṃhitā: 4 kāṇḍas, 54 prapāṭhakas (11 + 13 + 16 + 14).
  - Kāṭhaka Saṃhitā: 40 sthānakas.
  - Kāṇva Saṃhitā: 40 adhyāyas, 2,086 verses.
  - Sāmaveda (Kauthuma): 1,875 = 650 + 1,225. "Not in the Ṛgveda" is counted as 75 (Wikipedia) or 99 (Vedic Heritage Portal).
  - Atharvaveda Śaunaka: 731 sūktas and about 5,840 verses; book 15 has 18 paryāyas; 12.1 has 63 verses.
- **Commentators and dates:**
  - Skandasvāmin c. 625 CE, working with Nārāyaṇa and Udgītha; guru of Harisvāmin; wrote on the Nirukta with Maheśvara.
  - Veṅkaṭamādhava: 10th–12th century.
  - Uvaṭa: son of Vajraṭa, at Avantī under Bhoja.
  - Madhva's Ṛgbhāṣya covers 40 sūktas, with Jayatīrtha's ṭīkā and Rāghavendra's work on it.
  - Dayānanda: 1824–83; Ārya Samāj founded 1875; Ṛgvedādibhāṣyabhūmikā 1876–78.
  - Aurobindo's Arya writings on the Veda run 1914–20 (the "Secret of the Veda" series itself ran 1914–16).
- **Traditional legends:**
  - Dīrghatamas born blind.
  - Ghoṣā's skin disease.
  - Lopāmudrā and the hādi form of the Śrīvidyā.
  - Sāyaṇa on 3.53.21–24: the verses are against Vasiṣṭha and "the Vasiṣṭhas do not listen to them."
  - Sāyaṇa on 7.104.15: Vasiṣṭha's oath.
  - Sāyaṇa on the Vrātya (AVŚ 15.1.1).
- **Dispute and borrowing loci:**
  - Gopatha 1.2.24: the brahmán priest should be an Atharvavedin.
  - Pañcaviṃśa Brāhmaṇa 17.1–4: the vrātyastomas.
  - Mīmāṃsā Sūtra 1.2.31 and 1.1.27–32; Śabara on 1.1.2 (the śyena rite).
  - Suśruta Sū. 1.6 and Caraka Sū. 30.21.
  - Nāṭyaśāstra 1.17.
  - The Mahābhāṣya Paspaśāhnika cites RV 1.164.45 (with 4.58.3, 10.71.2 and 10.71.4).
  - The Rudra-japa multiples 11 / 121 / 1,331 / 14,641.
- **Śākhā regions:**
  - Kauṣītaki among the Nambūtiris; Śāṅkhāyana in Gujarat and Rajasthan.
  - Rāṇāyanīya in Karnataka and Maharashtra.
  - Jaiminīya in Kerala and Tamil Nadu.
  - Maitrāyaṇīya in Nashik.
  - Kāṇva and Śaunaka as described in the entries.
- **Upaniṣad cross-references in teaching notes:** checked locally and confirmed: BĀU 1.4.10, 2.5.19, 6.2.2, 5.1.1; Śvetāśvatara 2.4, 3.3, 3.8, 4.3, 4.6, 4.8, 4.19; Kaṭha 1.3.9 and 2.2.2; Aitareya 2.5.

## 6. Not-found (possible hallucinations)
None. No entry of U01 lacked an external or textual witness.

## 7. Could not be checked, or only partly
- **Not in the local corpora (web only):** the Bṛhaddevatā, Sarvānukramaṇī, Caraṇavyūha of Śaunaka, Puṣpasūtra, Vikṛtivallī, the gāna books and the Jaiminīya Saṃhitā.
- **Kātyāyana:** the alternative ascription of the Caraṇavyūha to Kātyāyana was not confirmed.
- **Minor claims not re-verified:**
  - the Ātmānanda commentary on 1.164;
  - the Aitareya Brāhmaṇa 7.13–18 Śunaḥśepa narrative;
  - the Maitrāyaṇīya presence in Gujarat;
  - Taittirīya Upaniṣad 2.7, Muṇḍaka 3.1.1, Brahma Sūtra 1.3.26–38, DN 27 and Sn 3.9 (all standard loci);
  - Sāyaṇa's stated reason for commenting on the Taittirīya Saṃhitā first.
- **TS anuvāka numbers:** segmenting the local TS by its "॥ [n]" markers is unreliable in prose-and-verse prapāṭhakas (it splits TS 1.8.5 in two). The TS 1.8.6 number was therefore confirmed by web search.

## 8. Notes for later sessions
- **DharmicData Ṛgveda:**
  - verse markers from 35 onward are malformed ("॥४॥५॥" for 45);
  - the headers for 1.191 and 10.151 are wrong or garbled;
  - 10.121.10 and 10.123 are incomplete.
  - Use the GRETIL mandala files for verse text; use DharmicData only for headers, cross-checked with Sāyaṇa's attributes.
- **Atharvaveda numbering:** the GRETIL text carries both numberings, e.g. "AVŚ_11,4[6]" means Whitney 11.4 = 11.6 in the other edition.
- **Nirukta pariśiṣṭa:** cite it as Sarup 13.8(–9).
- **lin:arya-samaj:** the facts are confirmed. Whether to include it is a registry decision, not a factual one.
