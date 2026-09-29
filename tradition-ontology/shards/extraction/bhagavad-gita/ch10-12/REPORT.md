# Bhagavad Gītā ch. 10–12 — fidelity check (role F), 2026-09-29
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the subagent — subagents cannot write report files in this harness.)_

## Counts
- **Teachings checked: 125.** That is 117 verses, 3 chapter entries (ch10, ch11, ch12) and 5 sentence spans (10.4-5, 12.3-4, 12.6-7, 12.13-14, 12.18-19).
- **Results: 121 passed, 4 fixed, 0 failed.** All 125 are in `final/teachings.jsonl` at level `text-verified`. Each has a fidelity block (checked_by "F", date 2026-09-29), and each fixed entry has `correction_log` items.
- **Original text:** `original` matches the segment character for character for every verse. Each span is exactly its two segments joined with a newline. The glitches listed in DECISIONS.md are kept as given.
- **Speakers:** every speaker and addressee matches the segments' speaker fields and headings. Every paraphrase begins with the right speaker ("Kṛṣṇa:", "Arjuna:", "Sañjaya:").
- **Entities: 204 entries** (20 concepts, 13 practices, 14 obstacles, 8 phenomenology, 1 dispute, 1 path, 24 teachers, 123 terms).
  - All were checked against the Sanskrit of the verses they cite.
  - 10 were corrected: 7 text corrections, 1 path corrected in two ways (notes rewritten and a duplicate source removed), and 2 concepts de-duplicated.
  - Following the DECISIONS.md policy, no entity level was raised. Each entity got a `verification.checks` record instead (phase D, method text, result confirmed or corrected).
- **skeleton_decisions.jsonl:** 36 decisions (33 upgrade, 3 correct, 0 retire). Every `replaced_by` exists.
  - The reasons for 10.6 and 10.10-11 quoted the merged wording that this check changed, so an "[F, 2026-09-29: …]" note was appended to each. Nothing else was changed.
- **interpretation_log.jsonl:** 15 lines — 12 text-corrections (4 teachings, 8 entities) and 3 dedupes.
- **Linked ids:** all of them exist in data/, in other extraction chunks or in this chunk, except the 7 later-Gītā refs listed below. Homonyms were checked:
  - These are correctly not linked: trm:nimitta, trm:nidhana, tch:rama, and trm:om only by way of 8.13.
  - These words are linked in their ordinary sense, and each term's definition says so: kleśa at 12.5, cetanā at 10.22, māhātmya at 11.2 and siddhi at 12.10.

## The 4 teaching fixes
- **10.11:** "abiding in the self's own state" read the reflexive *ātma-bhāva-stha* as "the self" — the pattern DECISIONS.md flags. It now reads "abiding in their own being or in my own", which leaves open whose, as the notes say.
  - Aligned in `cpt:divine-grace`, `cpt:lord-in-the-heart` and `trm:ajnana`.
- **10.6:** "the seven great seers of old, and the four, and the Manus" matched neither of the two groupings the notes record. The paraphrase now gives both: "the seven great seers of old and the four Manus — or the seven great seers, the four of old, and the Manus".
- **ch10:** the summary said 10.1 is spoken "because he delights in hearing". The verse says only *prīyamāṇāya*, "to you who take delight"; the object and the "because" are the commentators', and the 10.1 entry leaves them open. It now says "to him who takes delight (prīyamāṇa)". The purpose sentence cites 10.18 (Arjuna's own "I have no satiety hearing") for the hearing. The 10.6 groups were aligned too.
- **11.19:** the link `tea:mundaka-upanisad:2.1.4` did not exist. It was repointed to `tea:mundaka-upanisad:2.1.3-9`, which contains 2.1.4 (sun and moon his eyes).

## Entity-only fixes
- **"Born of mind" (10.6):** `cpt:isvara`, `trm:manu` and `trm:rsi` said the seers and Manus of 10.6 were "born from his / the Lord's mind". The verse says only *mānasā jātāḥ*, "born of mind", and does not say whose. They now read "sharing his being (mad-bhāva), were born of mind". `trm:manu` also gets both groupings.
- **`prc:abhyasa`:** 8.8's *cetasā nānyagāminā* was rendered "the mind not going to anything else", which flattens cetas into "mind". It now reads "thought (cetas)", as ch07-09 has it.
- **`pth:gita-devotion-ladder`:**
  - The notes held two versions of the same text, which are now merged into one.
  - "Commentators commonly read 12.12 as praise" is now attributed to Śaṅkara (recalled).
  - A duplicate source ("12.8-12" / "12.8–12") was removed.
- **Duplicate members removed:**
  - `cpt:qualities-of-the-devotee`: B's 31 unglossed items each repeated one of A's 31 glossed items.
  - `cpt:vibhutis`: 16 of B's items repeated A's list for 10.20–38. They included glosses the verses do not give ("the lion", "spring").

## Passed after a close check
- Every "of X I am Y" verse (10.20–39) keeps only what the verse names. Kubera, spring, the lion, the churning of the ocean, Kapila's Sāṃkhya and oṃ at 10.25 appear only in notes and are labelled.
- Both construals are kept in the paraphrase or notes at 11.15, 11.37, 11.46/11.50, 11.54 (the scope of *tattvena* and the sense of *praveṣṭum*), 12.1–5 (what the akṣara is) and 12.11–13.
- The cross-references to ch. 13 were checked against the segments; they use this edition's numbering: 13.1 (the extra verse), 13.3 (vulgate 13.2) and 13.13 (vulgate 13.12).

## What the next wave should revisit
1. **Links to later Gītā verses not yet extracted:** 13.1, 13.3, 13.13, 14.24, 14.25, 15.16 and 18.57. They resolve when chs. 13–18 are merged. ch13-15 is under way.
2. **cetas and citta renderings.** Chs. 10–12 render cetas as "awareness (cetas)" (11.51, 12.5, 12.7; `trm:cetas`) and citta as "thought (citta)" (10.9, 12.9). Chs. 4–9 render cetas as "thought". Neither is flattened to "mind", but a Gītā-wide pass should fix one rendering.
3. **The level tag.** 'ultimate' is used for Arjuna's praise of the Lord as paraṃ brahma and similar (10.12, 10.15, 11.18, 11.37, 11.38) and for 12.3. Comparable descriptions (10.20, 10.39, 11.40) are 'unmarked', and the merger's stated rule is "descriptions of the Lord are unmarked". I accepted these as plausible; one policy is needed, together with the 'bridging' question from ch07-09.
4. **Shared-entity names that go beyond the verse** (shared ids, so not edited here):
   - `prc:kirtana` ("Devotional singing …") is linked at 10.9 ("speaking of me") and 11.36 (*prakīrti*). Its chunk notes say the verses do not mention singing.
   - `tch:bhrgu` is named "Bhṛgu Vāruṇi", but 10.25 says only "Bhṛgu, among great seers". The identity is traditional, not stated.
   - `tch:kapila` is the founder of Sāṃkhya; 10.26 says only "the sage Kapila".
   - `tch:brhaspati`'s data summary is the Lokāyata attribution.
5. **Commentators' views that are recalled, not checked.** Śaṅkara's and Rāmānuja's positions appear in `dsp:bhagavad-gita-lord-or-unmanifest` and in the notes of 10.2, 11.55, 12.1, 12.4, 12.12 and 12.13. Check them against the bhāṣyas in Wave 2.
   - The 11.54 note about the critical text (MBh 6.33.54: 'śakya aham … draṣṭuṃ') comes from the skeleton and was not checked here.
6. **Errata for the post-ch18 pass** (as DECISIONS.md already lists), plus:
   - 11.54 'śakyam aham': is it a variant or a glitch? The vulgate prints 'śakya aham'. Decide in the errata pass.
   - Fused speaker headings also occur at 13.2 and 18.73 in later chunks.
7. **Open items from the merger:** `prc:vandana` ≈ `prc:namaskara` dedupe; whether fixing manas and buddhi on the Lord is its own practice or part of `prc:smarana`; `lin:bhagavata-early` as the lineage of `pth:gita-devotion-ladder` (from data).
8. **Minor, left for the misreading hunter:**
   - `cpt:lord-in-the-heart` at 10.11 rests on one of the two readings of the reflexive; its definition now says the reflexive is open.
   - The `obs:vyatha` antidote `prc:ananya-bhakti` is an inference from 12.16 (*gatavyatha*).
   - 12.4's "they too reach me indeed" renders the contrast of *ye tu … mām eva*; I accepted it.
   - 11.15 has "O God" where 11.44–45 have "O god".
