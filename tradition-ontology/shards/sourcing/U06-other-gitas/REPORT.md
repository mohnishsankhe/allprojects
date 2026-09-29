# U06-other-gitas — Phase C hallucination sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

**Scope:** every source (78), teacher (54), teaching (301), concept (34), practice (39), obstacle (18), phenomenology item (16), path (3), dispute (4) and borrowing (8), plus the one low-confidence term.
- The interpretation log is outside the brief and was not checked.
- The unit's "least sure" list was checked first.

**Result: 556 checked · 522 confirmed · 13 partially confirmed · 20 corrected · 1 not found.** The validator reports 0 errors.

| | confirmed | partial | corrected | not found |
|---|---|---|---|---|
| sources | 59 | 5 | 14 | 0 |
| teachers | 53 | 1 | 0 | 0 |
| teachings | 288 | 6 | 6 | 1 |
| concepts, practices, obstacles, phenomenology, paths, disputes, borrowings, term | 122 | 1 | 0 | 0 |

## How the checks were made
**Local texts (all read-only).** A loader in `_gen/lib.py` reads each text by verse, and each teaching was printed beside its text and read:
- **Bhāgavata:** the mAdhva e-text, plus the 1915 Gītāsaṅgraha for vulgate numbering.
- **1915 Gītāsaṅgraha (eBhāratī 6673):** the Aṣṭāvakra, Avadhūta, Devī, Kapila, Śiva, Gaṇeśa, Rāma, Sūrya, three Yama, Haṃsa, Pāṇḍava and two Brahma Gītās. Chapters were split by their colophons.
- **Mokṣopāya:** the GRETIL text, with sarga colophons and its concordance to the vulgate.
- **Yoga Vāsiṣṭha vulgate:** the Nirṇaya Sāgara edition with the Tātparyaprakāśa (Muktabodha M00335–339, M00345). The unit's report said this was not local; it is.
- **Laghu Yoga Vāsiṣṭha:** with the Vāsiṣṭhacandrikā (Muktabodha M00351), and an eBhāratī copy.
- **Rāmāyaṇa texts:** the Gita Press Adhyātma Rāmāyaṇa and the Rāmcaritmānas.
- **Purāṇas:** the Kūrma and Viṣṇu Purāṇas (mAdhva e-texts), the GRETIL Agni and Narasiṃha Purāṇas, and the GRETIL Devīgītā (Devī Bhāgavata 7.31–40).
- **Mahābhārata:** the BORI critical edition (DharmicData), plus the Gita Press vulgate's chapter colophons, which name the Gītās.
- **Others:** the Ganeshpuri Guru Gītā, the 108-Upaniṣad e-text, and the Varāha Upaniṣad (Muktabodha).

**Also used:** `catalog.py` for existence checks, and WebSearch for authors, dates, recensions and the texts that are not local (Ṛbhu, Uttara, Jīvanmukta, Bhagavatī, Tattvasārāyaṇa Gītās, Sūta Gītā).

**Originals.** All 45 `original` fields were compared with the local edition:
- 33 match character for character.
- 3 Mahābhārata ones match letter for letter; only the half-verse separator and the anusvāra sign (ṁ/ṃ) differ.
- 6 were corrected to the edition's exact string (listed below).
- The other 3 are covered by notes (the Kapila Gītā numbering note, the Adhyātma Rāmāyaṇa note, and the Aṣṭāvakra 1.11 reading).
- The two half-verses the unit completed from memory (Bhāgavata 11.23.42 and 3.33.7) turn out to be letter-perfect.

## Not found (possible hallucination)
- **`tea:uttara-gita:1`.** The text is not local, and three searches did not tie either statement to the Uttara Gītā:
  - the verse "jñānāmṛtena tṛptasya kṛtakṛtyasya yoginaḥ …" turned up only in other texts, such as the Sāṃkhyaparibhāṣā;
  - the husk simile is Amṛtabindu Upaniṣad 18.
  - The attribution may still be right, but it is unconfirmed; the merge should flag it [unverified].

## Corrected
**Generator default (dating).** Thirteen Mahābhārata Gītās outside the Mokṣadharma carried a copied scholarly date note ending "the Śāntiparvan's Mokṣadharma belongs to the later layers". The note is replaced with the right section; the tradition's account is unchanged.
- Āraṇyakaparvan: `src:vyadha-gita`, `src:sarasvati-gita`, `src:kasyapa-gita`, `src:saunaka-gita`, `src:astavakriya-mahabharata`.
- Āśvamedhikaparvan: `src:kama-gita`, `src:brahmana-gita`.
- Rājadharma: `src:utathya-gita`, `src:vamadeva-gita`, `src:rsabha-gita`.
- Āpaddharma: `src:sadja-gita`.

**Other source corrections**
- **`src:rsabha-gita`.** In the critical edition the Sumitra–Ṛṣabha story runs 12.125.8–12.126.52.
  - CE 12.127 is the Gautama–Yama dialogue, and 12.128 is on kings in distress.
  - The range 125–128 is the Gita Press vulgate's (its colophons read "ṛṣabhagītāsu").
  - The passage is in the Rājadharma, not the Mokṣadharma: part_of is now U05's `src:rajadharma`.
- **`src:sadja-gita`.** The vulgate colophon reads "āpaddharmaparvaṇi ṣaḍjagītāyām", so part_of is now `src:apaddharma` (not the Mokṣadharma).
- **`src:surya-gita`.** The frame was wrong.
  - Brahmā questions his teacher Dakṣiṇāmūrti, not the Sun.
  - Dakṣiṇāmūrti then relates the Sun's teaching to his charioteer Aruṇa ("aruṇa uvāca" / "sūrya uvāca").
  - Its 5 chapters and its place in the Tattvasārāyaṇa's Karmakāṇḍa are confirmed.
- **`src:devi-gita` (dating).** C. Mackenzie Brown finds it hard to place the text before the 13th c.; it may be as late as the 16th (often given as the 15th). The entry said 11th–13th c.
- **`src:yoga-vasistha-tatparyaprakasa`.** A date was added. The commentary's closing verse gives "ṛturasaturagamahī 1766 śaka", c. 1844 CE, which fits Dasgupta's 19th c.

**Teaching `original` corrections** (to the edition's exact text)
- `tea:uddhava-gita:11.20.6-8`, `11.23.42-45` and `tea:kapila-gita:3.33.6-7`: word spacing had been added.
- `tea:moksopaya:1.1.2`: the Kashmiri sandhi had been normalized ("aham baddho vimuktas … nātajjñas").
- `tea:astavakra-gita:1.3-6`: the Gītāsaṅgraha misprints "deha", so the original is now the GRETIL reading "dehaṃ", with its edition label.
- `tea:laksmana-gita:2.92-93`: a space before the daṇḍa was removed.

## Partially confirmed
**Teachings**
- **`tea:uddhava-gita:11.20.9-11`.** The last clause (the gods desire a human birth) is 11.20.12.
- **`tea:bhramara-gita:10.47.12-21`.** Uddhava's wish to be a creeper touched by the gopīs' feet is 10.47.61.
- **`tea:devi-gita:7.40/2`.** The restriction is confirmed (7.40.34), but inner worship is ranked above outer at Devī Bhāgavata 7.39.43–46, not in 7.40. The same applies to `prc:antaryaga`.
- **`tea:rsabha-gita:12.125-128`.** See the critical-edition range above.
- **`tea:rbhu-gita:passim`.** The refrains are confirmed by descriptions of the text; no verse was located. (`passim/2`, on ash, rudrākṣa and Śiva worship, is confirmed.)
- **`tea:uttara-gita:2`.** The nāḍī teaching is confirmed in the text; the chapter is not.

**Sources and teacher**
- **`src:rbhu-gita`.** Confirmed: sixth aṃśa of the 12-part Śivarahasya, about 2,000 verses, the Sanskrit online. Unconfirmed: the chapter count and the 44-chapter Tamil version.
- **`src:vyasa-gita`.** Kūrma 2.12–2.33 fits: the tīrthas start at 2.34. The local colophons do not carry the name.
- **`src:rama-gita-tattvasarayana`.** 18 chapters, about 1,000 verses, in the Upāsanākāṇḍa: confirmed. The Rāma-to-Hanumān frame is not confirmed.
- **`src:laghu-yoga-vasistha`.** Confirmed locally:
  - six prakaraṇas (3+1+9+5+10+18 sargas), about 6,000 verses;
  - the final colophon names "gauḍamaṇḍalālaṅkāra … abhinanda", and some colophons use the title "Yogavāsiṣṭhasāra".
  - The 10th-c. identification and date are disputed by Slaje (see also `tch:abhinanda`).
- **`src:mahabhagavata-purana`.** The date is disputed: 10th–11th c. (Hazra, per Wikipedia) against 13th–14th c. (Banglapedia).

## Least-sure items resolved
**Sources**
- **Ṛbhu Gītā:** sixth aṃśa confirmed. The Śaiva-observance teaching is confirmed; the chapter count stays open.
- **Uttara Gītā:** confirmed:
  - 3 chapters, with its traditional claim to the Aśvamedhikaparvan;
  - absent from the critical edition;
  - 5 of 8 commentary manuscripts ascribed to Gauḍapāda.
- **Other recalled texts:**
  - Jīvanmukta Gītā: exists, about 24 verses, attributed to Dattātreya.
  - Bhagavatī Gītā: Mahābhāgavata chs. 15–19 (the recalled numbers are right).
  - Vāsiṣṭhacandrikā: local, by Ātmasukha, pupil of Uttamasukha (per its colophon).
  - Yogavāsiṣṭhasāra: 10 chapters, about 230 verses.
  - Sūta Gītā: the 8 chapters after the Brahma Gītā's 12 (Tilak).
  - Tattvasārāyaṇa: three kāṇḍas, ascribed to Vasiṣṭha.

**Śiva Gītā.** Content verified for chs. 1, 3, 7, 8–11, 13–16:
- Agastya gives the teaching to Rāma (1.39);
- the Virajā initiation, Pāśupata vow and ash (3.15–33);
- the five sheaths (14.6–25).

**Mokṣopāya stories.** Every story range checked out by colophon, and key details were spot-checked in the text:
- King Padma and Jñapti Sarasvatī; Karkaṭī among the Kirātas; Indradyumna's Ahalyā; the three unborn princes;
- Śukra's celestial woman; Śambara; Dāśūra's kadamba; Kaca's song (4.40.5, verbatim);
- Bali and Virocana; the Pāñcajanya waking Prahlāda; Gādhi in the water; Uddālaka's Oṃ and sattāsāmānya; Suraghu of the Kirātas;
- Vītahavya's mud; Madanikā; the well-space of the illusory man; the Maṅki desert road; Śiva and Bhṛṅgīśa;
- the waking/dream/sleep correlation of the stages (6.148.9, 6.153.3–8, 6.154.8).

Corrections and precisions to the unit's notes:
- The Śukra story runs to 3.140, not 3.138.
- The Bhuśuṇḍa story closes at 6.28.
- Rāma is "ūnaṣoḍaśa" (not yet sixteen) at 1.4.1 and 1.7.2.

**Vulgate numbers.** All the approximate vulgate references in the notes are confirmed by the local vulgate or by the Mokṣopāya concordance:
- Śukra 4.5; Dāma 4.25; Dāśūra 4.48; Kaca 4.58;
- Bhuśuṇḍa 6.1.14; Deva-pūjā from about 6.1.27; Arjuna 6.1.52; Cūḍālā 6.1.77–110;
- Book 2 has the same numbering as the Mokṣopāya;
- vulgate structure: 33, 20, 122, 62, 93, and 128+216 = 674 sargas.

**Scholarly dates**
- Aṣṭāvakra Gītā (Brockington: 8th or 14th c.), Avadhūta Gītā (9th–10th c.), Adhyātma Rāmāyaṇa (13th–15th c., per Wikipedia) and Īśvara Gītā (Kūrma core c. 8th c.): consistent with the entries.
- Devī Gītā: corrected, as above.
- Gaṇeśa Purāṇa: 1100–1400; the Gaṇeśa Gītā is Krīḍākhaṇḍa chs. 138–148 (the low-confidence chapter numbers are right).

**Mahābhārata Gītā names.** The vulgate colophons name the Ṣaḍja (Āpaddharma), Hārīta, Śampāka (CE "Śamyāka"), Maṅki, Bodhya, Vicakhnu, Vṛtra, Parāśara, Haṃsa, Utathya, Vāmadeva, Ṛṣabha and Brāhmaṇa Gītās. The critical text of 12.269 does not name Hārīta.

**Daiva/pauruṣa dispute, epic side.** Confirmed at Mahābhārata critical edition 13.6.7–8 (seed and field). The Ājīvika report is at DN 2 (dn2:20.6).

**Twelve niyamas.** The Bhāgavata verse lists eleven; the vedabase (BBT) translation reaches twelve by taking śauca as outer and inner. Śrīdhara's own gloss was not retrieved.

**Borrowing into minor Upaniṣads (for U04).** Verified locally:
- The Mahā Upaniṣad (ch. 5) and Varāha Upaniṣad (ch. 4) carry the seven stages under the Mokṣopāya 3.118 names.
- The Akṣi Upaniṣad reproduces Mokṣopāya 6.140–141 almost word for word, not 3.118; there the third stage is called "asaṃsaṅga".

**Teachers.** All confirmed in their texts or by web sources, including:
- Nidāgha (son of Pulastya, at Vīranagara on the Devikā; Viṣṇu Purāṇa 2.15.4–6);
- Vareṇya (Gajānana was born his son);
- Ātmasukha (local colophon);
- Ānandabodhendra (19th c.; Śaka 1766 colophon).

Only Abhinanda remains partial.

**Restricted practices.** `prc:devi-gita-kundalini-dhyana` stays summary-only, with no procedures, counts or retentions, and its warning is the text's own (7.40.34). The Cūḍālā powers and the Bhuśuṇḍa breath entries record no technique.

## Minor notes for the merge or Phase D
- **Availability:** could be set to digitized-original for `src:rbhu-gita`, `src:laghu-yoga-vasistha`, `src:vasistha-candrika` and `src:siva-rahasya`; `src:eknathi-bhagavata` is also digitized (archive.org). These are left as notes, not corrections.
- **`src:brahma-gita-yoga-vasistha`:** the vulgate colophons with "brahmagītāsu" are at Nirvāṇa uttarārdha 6.2.128 and 6.2.173–181. The Gītāsaṅgraha text ends with 6.2.181 (gauryāśramavarṇana) as its 9th sarga.
- **Kapila Gītā numbering:** the local mAdhva e-text skips the number 3.25.33, so its 3.25 numbers run one high from there. The teachings rightly use vulgate numbers (checked in the Gītāsaṅgraha).
- **Pāṇḍava Gītā 1–3:** three speakers (the Pāṇḍavas, Lomaharṣaṇa, Brahmā); the paraphrase merges them.
- **`cpt:pati-pasu-pasa`:** its "he is bondage, binder, noose and bound" clause is Kūrma 2.7.32, just outside the cited teaching.
- **Gap report:** the Laghu Yoga Vāsiṣṭha and the vulgate are now known to be local, so Phase D can extract Laghu teachings and map vulgate numbers directly.
- **Registry ids:** U05's `src:rajadharma` and `src:apaddharma` are now referenced by U06 corrections.

## Could not be checked
- The Uttara Gītā and Ṛbhu Gītā texts themselves (not local; web pages cannot be fetched), so no verse-level refs for them.
- The Rāma-to-Hanumān frame of the Tattvasārāyaṇa Rāma Gītā.
- Śrīdhara's gloss on the twelve niyamas.
- The name "Vyāsa Gītā" for Kūrma 2.12 onward.
- Bhāskara's samuccaya position in his own text.
- The cave in the Vītahavya story and the peacock-feather wand in the Lavaṇa story (the colophons and other details were verified).
- The exact chapter count of the Ṛbhu Gītā and of its Tamil rendering.
