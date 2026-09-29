# Bhagavad Gītā ch. 16–18: fidelity check (role F), 2026-09-29
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Counts
- **Teachings checked: 137.** That is every entry, as for the earlier dual-extracted chunks.
  - 130 verses (ch. 16 has 24, ch. 17 has 28, ch. 18 has 78; chapters 16–18 have the same numbering in the 700-verse text).
  - 3 chapter entries.
  - 3 sentence entries: 16.1-3, 17.5-6 and 18.51-53.
  - `tea:bhagavad-gita:thesis`.
- **Results: 126 passed, 11 fixed, 0 failed.**
  - All 137 are in `final/teachings.jsonl` at text-verified, each with a fidelity block (checked_by F, 2026-09-29).
  - The 11 fixed entries each carry `correction_log` items.
- **fidelity.jsonl** has one line per teaching. Each line holds id, status, verdict (pass/fail as submitted), per-criterion results, fix, evidence (segment line and quote, merged line, old text) and a note.
- **Checked by code:**
  - Every `original` matches its segment character for character. Each sentence entry is its segments joined by line breaks.
  - The speaker follows the segment's heading or speaker field. Arjuna speaks 17.1, 18.1 and 18.73; Sañjaya speaks 18.74–78; Kṛṣṇa speaks the rest. Every verse paraphrase begins with its speaker.
  - All 130 verses are present.
  - 1602 link references resolve in data/, the other Gītā finals or this chunk. This includes the Upaniṣad cross-references ChU 3.14.1, BĀU 4.4.5, BĀU 3.7.3-23, Kaṭha 1.2.18-19 and ŚvetU 6.22–23.
  - Citta and cetas are rendered "thought" throughout. "Mind" is used only for manas. "Ego" does not occur.
  - No commentator is named outside notes. Every note that names one is marked "recalled".
- **Entities: 214** (35 concepts, 2 disputes, 27 obstacles, 1 path, 5 phenomenology, 21 practices, 5 teachers, 117 terms, 1 ultimate).
  - 6 were corrected. Each carries a `correction_log` item and an interpretation_log line.
  - No level was raised. Each entity got one `verification.checks` record (phase D, method text, result confirmed or corrected, evidence = the teachings it rests on).
- **skeleton_decisions.jsonl: 61** (51 upgrade, 10 correct, 0 retire).
  - Every `replaced_by` exists, and all 61 of data/'s unverified ch16–18 teachings have a decision. The file is copied unchanged.
  - Two decisions confirm my fixes: 18.74-78 says `cpt:divine-eye` is not carried, and 18.33-35 construes avyabhicāriṇyā with dhṛti.
- **final/interpretation_log.jsonl: 19 text-correction lines** (11 for teachings, 8 for entities).
- **Edition errata**, confirmed in the Devanāgarī and kept as printed:
  - śrṛṇu at 16.6, 17.2, 17.7, 18.4, 18.29, 18.36, 18.64 and 18.71;
  - niśicatāḥ (16.11), niśicataṃ (18.6), kaśicanme (18.69);
  - tatitravidhaṃ (17.17), syātitrabhir (18.40), bhakitaṃ (18.68);
  - asurīṃ (16.20);
  - no oṃ in 17.23 (तत्सदिति), and 17.25 truncated to mokṣakāṅkṣi;
  - speaker headings fused into the verse at 17.1, 17.2, 18.73 and 18.74, and printed inside the verse at 16.1 and 18.2;
  - the verse number included in the text at 18.78.

  These go to the post-ch18 correction pass.

## The 11 teaching fixes
1. **18.64 (paraphrase).** "…the most secret of all: you are dearly loved by me, therefore…" made the endearment read as the supreme word itself. In the Sanskrit, "iṣṭo 'si me dṛḍham iti … tataḥ" is the reason, and the word follows in 18.65–66. It now has a full stop: "…the most secret of all (sarva-guhyatama). You are dearly loved by me; therefore I shall tell you what is for your good (hita)."
2. **Thesis (paraphrase, one clause).** Mark 5 said the praise and blame passages "are not counted as separate doctrines". That decides the P7-arthavāda question for 18.68–71 and 18.78, which the entry's own notes list as "not decided". It now reads: "as marks of purport these urge the teaching; whether particular verses are praise only (P7-arthavāda) is not decided here (see notes)."
3. **18.75 (concepts).** `cpt:divine-eye` was linked. The verse says only "by Vyāsa's grace", and the entry's own notes and the 18.74-78 skeleton decision both say it is not linked. Removed.
4. **16.1-3, 17.5-6 and 18.51-53 (cross_refs).** Each sentence entry listed its own id. Removed.
5. **18.12 (notes).** "Here saṃnyāsin stands for the one who has relinquished the fruit" stated one reading as the verse's meaning, against the commentators' division recorded in the same notes and in `trm:samnyasin`. It now states only the contrast with atyāgin.
6. **18.14 (notes).** "'daiva' here is not the Sāṃkhya 'adhiṣṭhāna' of SK 17" named the wrong factor. The SK 17 homonym is adhiṣṭhāna, the seat, which is why `trm:adhisthana` is not linked.
7. **18.16 (notes).** The notes quoted the paraphrase as "the self alone"; the paraphrase reads "one's self (ātman) alone". Aligned.
8. **18.20 (notes).** "Hence level 'ultimate'" contradicted the level tag, which is unmarked. It now says "hence the type 'ultimate'".
9. **18.33 (notes).** "avyabhicāriṇyā may qualify dhṛti or yoga; commentators differ" is not possible: the word is feminine, so it agrees with dhṛtyā and not with the masculine yogena. Corrected. The paraphrase already construed it this way.

## Entity fixes
- **`phn:bhagavad-gita-three-kinds-of-happiness`, `trm:prasada` and `trm:sukha`.**
  - All three read 18.37 as "born of the clarity of the self's understanding". That is one analysis of ātma-buddhi-prasāda-ja, which the teaching leaves open and the 18.36-39 skeleton decision corrects.
  - The phenomenology entry and `trm:sukha` also had "deludes the self" at 18.39; the teaching has "deludes one's self".
  - All are aligned with the teaching.
- **`cpt:divine-grace`.** It listed 18.75 (Vyāsa's grace) in rests_on for the Lord's grace. Removed; `trm:prasada` keeps it for the word.
- **`obs:dambha`.** The epic-teaching name copied data/'s haṭha title "Hypocrisy of the unrealised". It is now "Hypocrisy, ostentation (dambha)".
- **`cpt:maya`.** The epic-teaching name copied data/'s title "Māyā in the principal Upaniṣads". It is now "Māyā (the Lord's māyā, BhG 18.61)".
- The shared top-level names of both entries are left for S5.

## Restricted content
- The restricted items are 17.5, 17.6, 17.5-6 (terrible austerity outside scripture, which torments the body and "me within the body") and 17.19 (self-tormenting austerity, classed tāmasic).
- These, together with `prc:tapas`, `prc:threefold-tapas` and `cpt:threefold-austerity`, record only a summary and the text's own verdict, quoted as warnings. There is no method, duration or practice.
- There is no fasting content. "Eating lightly" (laghv-āśin) at 18.52 is moderation.
- The food verses (17.8–10) and `prc:sattvic-diet` report the text's own statements about effects. Their notes say the text enjoins no diet, and no health claim is added.

## Thesis
- I checked every cited verse across chs. 1–18 against the segments. Each mark is cited correctly, including:
  - 2.7–11 against 18.59, 18.66 and 18.72–73;
  - the grading of 18.63 and 18.64;
  - 4.3, 9.1–2, 11.47, 15.20;
  - 18.65a = 9.34a and 18.47a = 3.35a.
- It states the purport in the text's words, gives the order of 18.45–55 and 18.56, and says the marks do not settle "abandoning all dharmas" or which means is final.
- The traditions (Advaita, Viśiṣṭādvaita, Dvaita, Abhinavagupta, Bhāskara, Gauḍīya, and Tilak marked as recent) appear only in notes marked as recalled.
- It chooses no tradition's thesis. The one fix is listed above.

## Passed after a close check
- **Open construals kept:**
  - aparaspara-sambhūta (16.8), naṣṭātman (16.9);
  - sattva at 16.1, 17.3 and 17.8;
  - sāṃkhye kṛtānte (18.13);
  - ātmānaṃ kevalaṃ (18.16), ātma-buddhi-prasāda (18.37);
  - niṣṭhā jñānasya yā parā (18.50);
  - "[me]" supplied in brackets at 18.55;
  - tad-arthīya (17.27), kuśala/akuśala (18.10).
- **Supplements** marked in brackets and justified in notes: "[Oṃ]" at 17.23; the instrumental read into the truncated word at 17.25.
- **Homonyms and senses:**
  - `trm:isvara` at 16.14 is the demonic's own claim, and the definition records that sense.
  - `obs:manitva` is not the Buddhist fetter.
  - `trm:vijnana` at 18.42 is in the jñāna–vijñāna sense (7.2, 9.1), and vijñāna is left untranslated.
  - `trm:ksanti`, `trm:mada`, `trm:mardava`, `trm:nistha`, `trm:para-bhakti`, `trm:svabhava`, `trm:siddhi` and `trm:bhava` each give their Gītā sense in the chunk's definition.
  - Prapatti ids are deliberately not linked at 18.66, and `trm:hari` is not linked at 18.77.
- **Cross-references to ch. 13** use this edition's numbering: 13.8-12, 13.11, 13.17 and 13.18, all checked.

## What the next wave should revisit
1. **data/ holds only one other school's definition** for these terms, which are linked here in their ordinary sense. S5 should add a general or epic sense:
   - `trm:punya` (18.71) has only the Jain definition;
   - `trm:artha` (18.34) has only the Arthaśāstra definition;
   - `trm:acara` (16.7) has only the Kaula and Dharmaśāstra definitions;
   - `trm:paurusa` (18.25) has only the Yoga Vāsiṣṭha definition.

   Also, data/'s `trm:bhava` mixes bhāva with Buddhist bhava, and data/'s `trm:soka` is labelled Pali.
2. **Term links where the verse lacks the word** (the idea is present; I left them):
   - `trm:ahankara` at 16.14;
   - `trm:karma` at 18.17;
   - `trm:svabhava` at 18.59 (the verse has prakṛti);
   - `trm:samsaya` at 18.73 (the verse has sandeha);
   - `trm:daivi-sampad` and `trm:asuri-sampad` at 16.6.

   A Gītā-wide rule is needed.
3. **"The self" for a reflexive ātman in entities**, left as ch13-15 did because it is within the verse's sense: `obs:three-gates-of-hell` and `trm:kama` at 16.21–22, and `cpt:non-agency-of-the-self`, `trm:buddhi`, `trm:kartr` and `obs:sense-of-doership` at 18.16.
4. **Shared top-level names for S5:**
   - `cpt:maya` ("…in the principal Upaniṣads");
   - `obs:dambha` ("…of the unrealised");
   - `prc:dhyana-yoga-gita` and `prc:buddhi-yoga`, whose names carry chapter-6 and chapter-2 verse ranges.
5. **Leftovers from code-combined merging** (cosmetic, not changed):
   - duplicated items in `prc:dhyana-yoga-gita` signs_of_progress, `prc:gita-study` prerequisites and `obs:asuri-sampad` antidotes;
   - repeated sentences in the notes of 18.13, 18.42, 18.49, 18.55, 18.75 and others.
6. **Commentators' views are recalled, not checked against the bhāṣyas.** This covers all notes marked "recalled", the thesis notes and both disputes. Check them in Wave 2.
7. **Level-tag policy, still open:**
   - "unmarked" is used at 17.23, 18.20, 18.54, 18.55, 18.61 and the thesis;
   - "bridging" only at 18.17.
8. **The path map's bands** (B1–B7 for 18.45–56) are an interpretive alignment, as its notes say. They are for the reconciliation auditor.

## Files
- /home/user/allprojects/tradition-ontology/shards/extraction/bhagavad-gita/ch16-18/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/bhagavad-gita/ch16-18/final/ (the 11 merged files plus interpretation_log.jsonl)
- Scratch (session scratchpad, not in the project): /tmp/claude-0/-home-user-allprojects/2c0e32b7-c920-5af7-bfe1-3ee59e322221/scratchpad/F-bg1618/ (build_final.py, notes_f.py)
