# U07-puranas — Phase C hallucination sweep report
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the unit's sweep subagent — subagents cannot write report files in this harness — and saved by the orchestrator.)_

**Scope:** every entry in `shards/skeleton/U07-puranas`:
- 58 sources, 1 lineage, 1 view of the ultimate, 45 teachers
- 208 teachings: every ref located, every `original` compared with the e-text
- 8 disputes, 10 borrowings, 8 paths, 17 phenomenology entries, 13 obstacles, 35 practices, 65 concepts
- the one low-confidence term

The "least sure" list was done first.

**Result: 470 checked · 453 confirmed · 11 partially confirmed · 6 corrected · 0 not found.**
- Methods: 404 text-locate, 40 catalog+websearch, 23 websearch, 3 catalog.
- Validator: 0 errors.

## How the checks were made
**Local e-texts (read-only).** A small loader (`_gen/etext.py`) maps every verse marker to its ref, and each ref was printed and read.
- GRETIL/Sansknet: Mārkaṇḍeya 1–93, Garuḍa (Venkateshwara ed.), Agni (R. Mitra), Brahmāṇḍa, Nārada, Brahma (Schreiner & Söhnen), Śiva books 1 and 7.
- raw_etexts:
  - Bhāgavata: the Gita Press-type wiki text, with the mAdhva-app text used for variant readings.
  - Viṣṇu (with the Viṣṇucittīya and Ātmaprakāśa), Liṅga, Kūrma, Matsya 1–176.
  - Kāśī Khaṇḍa files; the Bhāgavata-māhātmya; the Gita Press Durgā Saptaśatī.
- Local texts the unit said did not exist, which settled several low-confidence items:
  - Padma: peterFreund I–III and eBhārati.
  - Devī Bhāgavata: eBhārati, 1927 edition.
  - Full Matsya, 291 chapters: peterFreund.
  - Full Mārkaṇḍeya: peterFreund.
  - Early Skandapurāṇa: sarit, and skanda-purANam/8_ambikA-khaNDaH.
  - Upapurāṇas: Kapila, Parāśara, Sāmba, Nīlamata, Viṣṇudharma, Kalki, Bṛhaddharma, Śivadharma (Muktabodha).
- Comparing `original`s: each was compared character by character after normalisation, and against a second edition where one exists. "Matches" below means identical apart from sandhi and word division.

**Also used:**
- `catalog.py` for existence.
- WebSearch (Wikipedia, wisdomlib/Hazra, university pages) for dates, recensions, authors and the texts with no local copy.

## Corrected (6)
- **`src:brahma-purana`** (structure). Schreiner & Söhnen did not publish a critical edition. Their *Sanskrit Indices and Text of the Brahmapurāṇa* (1987) supplies the 246-chapter text behind the GRETIL file.
- **`src:padma-purana`** (attribution, dating).
  - The six-khaṇḍa recension is traced to western India, not "South Indian".
  - Scholarly estimates run from the 4th to the 15th c. CE; the entry had 8th–15th.
  - The tradition's account is kept separate.
- **`tea:visnu-purana:3.8.9`** (original). The last pāda "nānyat tattoṣakāraṇam" is the form quoted in Gauḍīya works. Four local VP editions read "nānyas tattoṣakārakaḥ".
- **`tea:siva-purana:1.5.10-13`** (speaker). 1.5.9–10 is the Sūta, reporting Śiva's words as heard from his teacher; Nandikeśvara begins only at 1.5.19.
- **`tea:narada-purana:1.92-109`** (speaker).
  - The index of the eighteen Purāṇas is given by Sanātana (1.92.13–14), relaying Brahmā's account to Marīci, not by Sanandana.
  - The paraphrase still says "Sanandana" and needs fixing in Phase D.
  - Range confirmed: 1.92 (Brāhma) to 1.109 (Brahmāṇḍa), with the Vāyu fourth (1.95).
- **`dsp:which-bhagavata-is-the-mahapurana`** (historical_debates). The pamphlet war is 17th–18th c., not "18th–19th, not checked":
  - Rāmāśrama (Bhānuji Dīkṣita, son of Bhaṭṭoji Dīkṣita) wrote the Durjanamukhacapeṭikā.
  - Kāśīnātha Bhaṭṭa of Vārāṇasī answered with the Śākta Durjanamukhamahācapeṭikā.
  - Mitra Miśra's Vīramitrodaya also backed the Viṣṇu-Bhāgavata.

## Partially confirmed (11) — possible misreadings for Phase D
- **`tea:garuda-purana:1.142`** — the chapter's colophon says "daśāvatāra", but its content does not match the paraphrase:
  - It names Matsya, Kūrma, Dhanvantari, Mohinī, Varāha, Narasiṃha, Paraśurāma and Rāma with his brothers.
  - It then tells the story of a leper's faithful wife who stopped the sunrise (resolved by Anasūyā).
  - No Vāmana, Kṛṣṇa, Buddha or Kalki appear.
  - **`cpt:avatara-lists`** is partial for the same reason: it should not cite GP 1.142 for the standard ten.
- **`tea:garuda-purana:2.49`** — dispassion, good company and self-knowledge from the teacher are confirmed. "Devotion to Viṣṇu as the way" is not in the chapter's teaching.
- **`tea:agni-purana:376-379`** — "the self is Brahman" is confirmed (376.1–7; the 377 litany; 379 retells Jaḍa Bharata). "The world is superimposed" was not located.
- **`tea:siva-purana:4`** and **`prc:sivaratri-vrata`** — there is no local Koṭirudra Saṃhitā. The web places the jyotirliṅgas in chs. 14–33 and the hunter Gurudruha in ch. 40. Both stay at saṃhitā level.
- **`tea:padma-purana:nama-aparadha`** — located at Brahmakhaṇḍa 25.15–18, spoken by Sanatkumāra, and a locator was added. But this edition's second offence reads "śubhasya śrīviṣṇoḥ" where the Gauḍīya citation (which the paraphrase follows) has "śivasya". A parallel list is at Nārada 1.82.22–24.
- **`tch:sanatkumara`** — "eldest of the Kumāras" is unsupported: BhP 3.12.4 lists him last, VP 1.7.9 and KūP 1.10.13 put Sanandana/Sananda first.
- **`src:devi-purana`** — exists (Hazra: 128 chapters, Vindhyavāsinī). Its date was not confirmed and no digitized text was found.
- **`src:sanatkumara-purana`** — the Upapurāṇa table on Wikipedia reports a published 19-chapter text. The entry's "survival uncertain" may be too cautious.
- **`prc:jivac-chraddha`** — only the chapter titles are confirmed: LiP 2.45 "jīvacchrāddhavidhi" and GP 2.8 "ātmaśrāddha".

## Least-sure items resolved
- **Padma 6.236.18–21.** Found at Uttarakhaṇḍa ch. 236, vv. 18–21 (Rudra to Pārvatī) in the local peterFreund text. The six-per-guṇa list matches exactly. `dsp:guna-ranking-of-puranas` and `cpt:guna-classification-of-puranas` now rest on a located text.
- **Devī Bhāgavata.** All four teachings located in the local text:
  - 1.3.2–12: the "madvayaṃ bhadvayaṃ" list, counting the Vāyu; 1.3.16 lists "bhāgavatam" among the Upapurāṇas.
  - 3.3: the gods turned into women. The name "Maṇidvīpa" is not used in these chapters.
  - 3.26: the Navarātra vow with worship of young girls.
  - 12.10–12: Maṇidvīpa.
- **Kāśī Khaṇḍa tāraka teaching.** Found at 4.1.25.72–73, also 4.1.5.26–28 and 4.1.30.13–14. A locator was added.
- **Matsya 274–289.** Exact: the colophons run from 274 "tulāpuruṣa-dāna" to 289, closing the great-gifts section.
- **Garuḍa title-only chapters.**
  - 2.11: the eight upper openings.
  - 2.12: "only dharma follows the dead", at 2.12.25.
  - 2.22: Bhīṣma speaks from 2.22.20.
  - 2.38.5: the verse spans 2.38.5–6.
- **Agni title-only chapters.**
  - 370 opens with the same dying-process verse as MkP 10.48, a third witness to that shared block.
  - 381: the Yamagītā told to Naciketas.
- **Sāroddhāra compiler.** Naunidhirāma (Navanidhirāma of Jhunjhunu); Wood & Subrahmanyam, *Sacred Books of the Hindus* 9, 1911.
- **tch:visnucitta.** c. 12th c., a pupil of Piḷḷāṉ; a dating was supplied.
- **Speaker Kavi for BhP 11.2.** Confirmed: 11.2.33 to 11.2.43.
- **VP 2.15–16 (Ṛbhu).** Confirmed; Nidāgha is Pulastya's son (2.15.4).
- **Order of the oceans in `cpt:bhu-mandala`.** Matches VP 2.4. The Bhāgavata swaps two: Krauñca is ringed by milk (5.20.18) and Śāka by curd (5.20.24).
- **MkP 39.1–35.** The Sansknet file has a gap: chapter 39 restarts at verse 27. The peterFreund text supplies 39.1–26 (prāṇāyāma and its four states).
- **Scholarly dates.** All Mahāpurāṇa and Upapurāṇa dates fall within the ranges given by Wikipedia and Hazra, except the Padma, which was corrected.
- **Minor Upapurāṇas.**
  - Kapila (local): opens on the holy places of Utkala.
  - Parāśara (local): Śaiva in orientation, with Śuka questioning Parāśara.
  - Āditya: known from quotations in later digests.

## Generator-default strings found
- **Availability "digitized-original".** Used for 56 of 58 sources. It is not contradicted anywhere, but no digitized text was found for the Devī Purāṇa, Mudgala, Gaṇeśa, Saura, Vāyu or Bhaviṣya (printed scans probably exist).
- **Tradition dating "Vyāsa, end of Dvāpara" (from −3102).** Copied into 18 sources. It is the tradition's own general claim (Matsya 53.8–11; BhP 1.4.14), so it is not an error.
- **`original.edition` "as recited/printed; checked against the local e-text where noted".** Set on all 58 originals. It is misleading for VP 3.8.9, which is now corrected.
- **Sweep language in skeleton text.**
  - "dating not checked in this sweep" (`tch:visnucitta`) and "no surviving text confirmed in this sweep" (`src:sanatkumara-purana`) were written before any sweep ran.
  - The note on `tea:bhagavata-purana:1.17.38-39` ("1.17.39-41 in the checked e-text") contradicts the e-text; the ref as given is right.

## Minor notes for Phase D
- BhP variant readings (the `original`s follow the other editions, which is acceptable):
  - 1.2.6: the wiki reads "samprasīdati"; the mAdhva-app has "suprasīdati".
  - 2.9.32: the wiki reads "evāsam eko 'gre"; others have "evāsam evāgre".
  - VP 6.7.31 "tasyā" vs "tasya" is also a variant.
- BhP 10.33 is numbered one higher in the wiki text than in the mAdhva-app text (29–30 and 39).
- GP 2.5.85–86: the traveller covers 247 yojanas a day over 86,000; the paraphrase's "about two hundred" condenses this.
- LiP 1.8.2 places yoga a span below the throat, below the navel and between the brows; the paraphrase says "navel region".
- The warning in `prc:hrt-padma-dhyana` softens BhP 11.14.29, which names "women and those attached to women".
- The name "Śrīkaṇṭha" in `prc:saiva-dhyana` was not found in ŚiP 7.2.39.
- A variant of "harer nāma …" stands at Nārada 1.41.115 (relevant to `src:brhannaradiya-purana`).
- The claim of extra Madhva-edition verses after BhP 2.2.24 was not confirmed.
- Restricted practices (`prc:utkranti-yoga`, `prc:prayopavesa`, prāṇāyāma detail) are summary-only, as required.

## Could not be checked
- The Koṭirudra Saṃhitā text (no local copy); covered by web only.
- The Vāyu, Bhaviṣya, Mahābhāgavata, Mudgala, Gaṇeśa, Saura, Sūta Saṃhitā, Śivadharmottara, Bhāvārthadīpikā and Guptavatī: checked by web only, with no local e-text.
- The "78–90 in some editions" numbering of the Devī Māhātmya, and the "35-chapter" Pretakhaṇḍa of other editions.
- ŚvetU 2.13 (U03's text), and the Gauḍīya and Buddhist sides of the disputes, beyond each school's known stance.
- The Mārkaṇḍeya manvantara chapters beyond 93; the local e-text ends there.
