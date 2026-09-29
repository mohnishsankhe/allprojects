# Bhagavad Gītā ch. 7–9 — fidelity check (role F), 2026-09-29
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Counts
- **Teachings checked: 97.** That is 92 verses, 3 chapter entries (ch7, ch8, ch9) and 2 sentence spans (8.9-10, 8.12-13).
- **Results: 68 passed, 29 fixed, 0 failed.** All 97 are written to `final/teachings.jsonl` at level `text-verified`. Each has a fidelity block (checked_by "F", date 2026-09-29). Each fixed entry has `correction_log` items.
- **Entities: 137 entries** (32 concepts, 15 practices, 9 obstacles, 3 phenomenology, 2 disputes, 2 teachers, 74 terms).
  - All were checked against the Sanskrit of the verses they cite.
  - 17 were corrected (15 text corrections and 2 duplicate-member removals).
  - Following the DECISIONS.md policy, no entity level was raised. Each entity got a `verification.checks` record instead (phase D, method text, result confirmed or corrected).
- **Skeleton decisions:** `skeleton_decisions.jsonl` copied unchanged (46: 40 upgrade, 6 correct, 0 retire). Every `replaced_by` id exists.
- **interpretation_log.jsonl:** 52 lines — 33 teaching text-corrections, 17 entity text-corrections, 2 dedupes.
- **Original text:** `original` is identical to the segments for every verse. The two spans are exactly their two segments joined. The known glitches in 7.3, 7.17, 7.24, 9.16, 9.21 and 9.25 are left as given.
- **Restricted practice:** `prc:utkranti-yoga` is still `restricted: true` and summary-only. No method, measures or warnings were added (the Gītā gives none).

## The 29 fixes
**Paraphrase fixes (9 entries)**
- **7.24:** the paraphrase silently chose one commentator's construal. It read "me, the unmanifest, as one who has come into manifestation", which takes *avyaktam* as what the Lord is. It now reads "think of me as unmanifest come into manifestation", in the Sanskrit order. The notes give both construals: *avyakta* as his true status, or as part of the mistaken view.
  - The same wording was aligned in the ch7 entry, `cpt:vyakta-and-avyakta`, `trm:avyakta`, `trm:vyakti` and dispute side 1 of `dsp:bhagavad-gita-the-lords-embodiment`.
- **7.18:** *yuktātmā* was "with self yoked", which reads the reflexive ātman as "the self". It is now "yoked in himself". "ātmaiva me matam" stays "my very self", with both readings (identity; as dear as his own self) in the notes.
- **7.30, 8.8, 8.14:** cetas had been flattened into "mind" (*yukta-cetasaḥ*, *cetasā*, *ananya-cetāḥ*). It is now "thought (cetas)"; "mind" is kept for manas (8.7, 8.10, 9.13).
  - Aligned in the ch8 entry, `prc:abhyasa`, `prc:ananya-bhakti`, `prc:smarana`, `trm:abhyasa-yoga` and `trm:antakala`.
- **8.4:** the adhidaivata was "the Person (puruṣa)". The capital P leans toward the supreme Person, which no reading takes it to be here. It is now puruṣa ('person'), with the readings (Hiraṇyagarbha, the enjoying self) in the notes.
  - Aligned in the ch8 entry, `cpt:adhidaiva-adhyatma-adhiyajna`, `trm:adhidaiva`, `trm:adhidaivata` and `trm:purusa`.
- **ch9:** the purpose statement said the chapter "resumes" the knowledge of 7.2. The chapter only repeats the phrase *jñānaṃ vijñāna-sahitam*; it does not say it resumes that teaching. The statement now says only that.

**Notes fixes**
- **7.19:** the note fixed "Vāsudeva" as a patronymic. It now says the verse gives no gloss of the name, and that commentators give both the patronymic and etymologies such as "the one who dwells in all".
- **8.1 and ch8:** the notes said the segment has no *arjuna uvāca* for 8.1. The segment's speaker field does have it.
- **8.17:** the note called the Manusmṛti numbering unchecked and cited a non-existent entry. Both are fixed; the note now matches the repointed link.

**Link fixes (18 entries, a recurring fault)**
- Links pointed to ids that do not exist in other texts. They were repointed to the existing span entry that contains the verse:
  - Chāndogya 6.1.3, 5.10.1–5
  - Bṛhadāraṇyaka 3.8.8, 3.8.11
  - Śvetāśvatara 3.3, 3.8, 3.19, 4.10
  - Praśna 3.10, 5.5
  - Kaṭha 1.2.15, 1.2.16
  - Muṇḍaka 1.2.7, 1.2.10
  - Manusmṛti 1.73 → `tea:manusmrti:1.68-72`, which contains 1.72. Manu 1.73 has no entry yet.

**Entity-only fixes**
- Reflexive ātman had been read as "the self" in `prc:isvararpana`, `trm:samnyasa` (9.28 *saṃnyāsa-yoga-yuktātmā*) and `prc:patram-puspam-offering` (a prerequisite read "a self that is pure", for 9.26 *prayatātman*). All three now read reflexively (in oneself).
- Duplicate members removed from `cpt:adhidaiva-adhyatma-adhiyajna` (6) and `cpt:two-natures-of-the-lord` (1).
- `cpt:gita-transmission`: added 7.2 to `rests_on`; its definition already cited that verse.

**Watched verses that passed as literal and neutral**
- 7.18 apart from the fix above, 8.3, 9.4-5, 9.15, 9.29 and 9.32. Where commentators divide (Advaita, Viśiṣṭādvaita, Dvaita, Gauḍīya), the readings appear only in the notes, labelled as the commentators'.
- The words vibhūti, avatāra, devayāna and pitṛyāna appear in no paraphrase. The 8.24 note mentions devayāna only to say the Gītā does not name it.

## What the next wave should revisit
1. **Links to later Gītā verses not yet extracted.** 18 of these resolve only when chs. 10–18 are merged: 10.39, 11.37, 11.53, 12.8, 12.9, 12.10, 12.14, 13.6, 13.13, 13.28, 14.3, 14.4, 14.23, 15.16, 16.6, 18.57, 18.64, 18.67. Check them at merge.
   - The 13.x ids use this edition's numbering, one higher than the 700-verse text. The notes at 7.4, 8.20 and 9.19 say so.
2. **The 'bridging' level tag** is used at 7.12, 7.24, 7.25, 8.3, 8.4, 9.4, 9.5, 9.6 and 9.11. I accepted it as plausible, but it stretches the definition ("explicitly relates two levels"). The misreading hunter or reconciliation auditor should set one policy for all Gītā chunks (bridging or unmarked).
3. **Links to ideas named by words the verse does not use.** These are kept, and each definition states the word does not occur:
   - `cpt:vibhutis` (7.8–11, 9.16–19, ch7), `cpt:avatara` (9.11, ch9), `cpt:istapurta-merit` (8.28), `dsp:destination-of-devayana` (8.24).
   - Term-to-term "related" links `trm:uttarayana`→`trm:devayana` and `trm:daksinayana`→`trm:pitryana`.
4. **Names of shared entities that go beyond the Gītā's words.** These belong to shared ids, so they were not edited here:
   - `cpt:maya` is named "Māyā in the principal Upaniṣads".
   - `prc:kirtana` is named "…nāma-saṅkīrtana", but 9.14 says only *kīrtayantaḥ*.
   - `obs:attachment-to-ritual-rewards` is named "(vedavāda)", a word from 2.42.
   - `cpt:omniscience` is named "(sarvajñatva)".
5. **One pass to make citta/cetas consistent across the whole Gītā.** Chs. 4–9 now use "thought (cetas/citta)", but ch. 6.18–23 in ch04-06/final still read "mind (citta)".
   - Reflexive ātman in the form "whose self(ves)…" (8.2, 9.26, 9.28) and the gloss of adhyātma as "what pertains to the self" (7.29, 8.1) were accepted, following ch01-06. A standard rendering could be set.
6. **Deduplication pairs the merger flagged remain** (S5): `cpt:last-thought`/`cpt:last-thought-at-death`, `cpt:two-paths-after-death`/`cpt:devayana-pitryana`, `cpt:surrender-to-the-lord`/`cpt:prapatti`, `prc:saranagati`/`prc:prapatti`.
7. **Segment glitches** are kept for the planned errata pass: 7.3 kaśicad, 7.17 ekabhakitar, 7.24 vyakitam, 9.16 maṃtro, 9.21 eva, 9.25 pitṛ़n. The line breaks inside sandhi at 8.9 and 9.20 are recorded in the notes.
8. **`lin:bhagavata-early`** appears, from the merged union, in the lineages of several practices and in both teachers. Reviewers should confirm this is intended before convergence counts are made.
