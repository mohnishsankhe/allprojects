# Bhagavad Gītā ch. 13–15 — fidelity check (role F), 2026-09-29
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_

_(Returned as text by the subagent — subagents cannot write report files in this harness.)_

## Counts
- **Teachings checked: 88.**
  - 82 verses (ch. 13 has 35 in this edition, ch. 14 has 27, ch. 15 has 20).
  - 3 chapter entries.
  - 3 sentence spans: 13.6-7, 13.8-12 and 14.23-25.
- **Results: 86 passed, 2 fixed, 0 failed.**
  - All 88 are in `final/teachings.jsonl` at level text-verified.
  - Each has a fidelity block (checked_by F, 2026-09-29). The two fixed entries each have `correction_log` items.
- **Original text.** Every `original` matches its segment character for character, and each span is its segments joined with a newline. These edition glitches are kept as printed and noted:
  - śrṛṇu (13.4), viniśicataiḥ (13.5), asakitar (13.10), bhakitar (13.11), liṃgais (14.21), bhakitayogena (14.26), parimārgitavya (15.4).
  - Speaker headings fused into the verse at 13.2, 14.1, 14.21, 14.22 and 15.1.
  - Words split across the pāda break at 15.3 and 15.5.
  - A scan of the segments found no further errata.
- **Conventions**, all checked by script:
  - Every paraphrase begins with the speaker. Arjuna speaks 13.1 and 14.21; Kṛṣṇa speaks the rest.
  - All 38 ch. 13 entries give the correct 700-verse number in their notes; 13.1 is marked as having no vulgate number.
  - Cross-references to ch. 13 from ch. 14–15 use this edition's numbering: 13.9, 13.11, 13.13, 13.18, 13.23, 13.30 and 13.35.
  - Sentence entries appear only where allowed.
  - Commentators' readings appear only in notes, labelled as recalled.
  - The reflexive ātman is left open: 13.8, 13.25, 13.29, 13.30, 14.24 and 15.11.
- **Entities: 216.** That is 33 concepts, 17 practices, 17 obstacles, 4 phenomenology, 3 disputes, 2 teachers and 140 terms.
  - 10 were corrected: 4 concepts and 6 terms.
  - No level was raised. Each entity got a `verification.checks` record (phase D, method text, result confirmed or corrected).
- **skeleton_decisions.jsonl: 42** (23 upgrade, 19 correct, 0 retire).
  - Every `replaced_by` exists.
  - `skeleton_id_edition` and `id_collision` are kept unchanged.
  - One "[F, 2026-09-29: …]" note is appended to 13.3-4, because its reason depends on the corrected wording of 13.5.
- **final/interpretation_log.jsonl: 13 text-correction lines.** 3 are for teachings (13.5 paraphrase; 15.11 paraphrase and notes) and 10 are for entities.
- **Linked ids: 411 references.** All exist in data/, in other Gītā chunks or in this chunk, except:
  - 5 references to later Gītā verses, listed below;
  - the 11 skeleton ids in skeleton_decisions, which use the 700-verse ch. 13 numbering. This is expected: the merge shifts them.

## The 2 teaching fixes
- **15.11.** acetas was rendered "without awareness", and the notes said cetas is rendered "awareness", following the ch10-12 merge.
  - The convention is citta/cetas → "thought (…)", and this chunk's own trm:cetas already gives "lack thought (acetas)" for this verse.
  - It now reads "without thought (acetas)", and the notes are aligned.
- **13.5.** "in the words of the brahmasūtras, which give reasons … and are decisive" made the compound plural and let the adjectives attach to it.
  - That is close to the "words of the Brahma-sūtra" wording (Rāmānuja's gloss) that the skeleton decision on 13.3-4 corrects. Yet the notes claim the compound is left untranslated.
  - It now reads "in the brahmasūtra words (brahmasūtra-pada), which give reasons (hetumat) and are decisive (viniścita)". The adjectives now agree with -pada, as in the Sanskrit.

## Entity fixes
- **trm:kartrtva and trm:prakrti.** Both had "the agency regarding effects and instruments (kārya-kāraṇa)". That renders the variant kārya-karaṇa. This edition reads kārya-kāraṇa, "effect and cause", as teaching 13.21, cpt:prakrti and the skeleton decisions have it. Both now say "effect and cause".
- **cpt:ksetra-ksetrajna.** It dropped the verse's "also" (api) at 13.3, the word dsp:bhagavad-gita-ksetrajna-and-the-lord turns on. Restored.
- **cpt:gunatita.** "from which the body arises" picked one analysis of deha-samudbhava. It now reads "bound up with the body's arising", as in 14.20.
- **cpt:non-agency-of-the-self.** 14.19 was cited without "and knows what is higher than the guṇas", although the result depends on both. Restored.
- **cpt:lord-in-the-heart.** It glossed apohana as "the removal of doubt", unattributed. It now gives the readings recorded at 15.15: "their loss, as most commentators take it, or reasoning that excludes".
- **trm:jiva.** "seen only by those with the eye of knowledge" added "only" and left out the striving yogins of 15.11. Corrected.
- **Same word, different sense in data/.** These three now state their sense in the definition, as ch10-12 did for kleśa:
  - trm:svastha: data/ holds only the Āyurvedic "healthy"; the definition had given no sense;
  - trm:arambha: data/ holds only the stage of yoga, ārambha;
  - trm:pratistha: data/ holds only the Āgamic installation of images.

## Passed after a close check
- **Homonyms.** These are correctly not linked: trm:mahesvara (māheśvara) at 13.23, trm:asakti (aśakti) at 13.10, trm:dvara at 14.11, cpt:nine-gated-city at 14.11 and cpt:real-and-unreal at 13.13. trm:asakta covers asakti (13.10) and asaktam (13.15).
- **Linked in their ordinary sense, with the definition giving that sense:** trm:yoni (data/ holds only the Śākta sense), trm:prakasa, trm:sruti and trm:linga. trm:apohana is the right sense: Utpaladeva's triad of cognition, memory and exclusion goes back to this very verse.
- **Terms not flattened:**
  - upadraṣṭṛ is rendered "onlooker", not "witness";
  - kṣetrin is "possessor of the field";
  - cetanā is "sentience", listed on the side of the field;
  - anahaṅkāra is "absence of the sense of I", not "ego".
- **Sanskrit left as the verse has it:** "great brahman" at 14.3 (not "prakṛti"), soma at 15.13 (not "the moon") and the tree at 15.1 (not "saṃsāra").
- **Open construals kept, with both readings:**
  - anādimat paraṃ / anādi mat-paraṃ (13.13);
  - sarvendriya-guṇābhāsa (13.15);
  - bhūta-prakṛti-mokṣa (13.35);
  - tṛṣṇā-saṅga-samudbhava (14.7);
  - sādharmya (14.2);
  - 14.22 as its own sentence;
  - amṛta and avyaya at 14.27, either in apposition to brahman or as further items;
  - aṃśa (15.7);
  - apohana and vedānta-kṛt (15.15);
  - akṣara (15.16).
- **Upaniṣadic parallels checked:** ŚU 3.16–17, 4.18, 3.8, 3.13, 1.8–10 and 6.14; Īśa 3 and 5; Kaṭha 2.2.13, 2.2.15, 2.3.1 and 2.3.17; MuU 2.1.2, 2.2.9 and 2.2.10; BĀU 4.4.16 and 5.9.1; BS 2.3.43.

## What the next wave should revisit
1. **Links to later Gītā verses not yet extracted:** 16.1, 16.2 and 16.3 (from 13.8 and 13.8-12), 18.53 (from 14.26) and 18.64 (from 15.20). They resolve when ch16-18 is final.
2. **U50's registry disputes are now in data/.**
   - dsp:saguna-nirguna's epic side rests on tea:bhagavad-gita:15.16-18. That is a skeleton span; this chunk records it verse by verse as 15.16–15.18. Repoint it in the merge or in S5.
   - dsp:souls-one-or-distinct's epic-teaching side has no rests_on. The loci are 13.3, 13.23 and 15.7 (see the three Gītā disputes).
   - The teachings still link only the three Gītā disputes, as the merger decided.
3. **cetas rendering, Gītā-wide.** Chs. 13–15 now use "thought" throughout (13.10, 15.11, trm:cetas). ch10-12's final still has "awareness (cetas)" at 11.51, 12.5 and 12.7 and in its trm:cetas definition. The convention is now decided, so align them in the consistency pass.
4. **Shared-entity names beyond the verse.** These are shared ids, so I did not edit them; for S5:
   - cpt:twenty-virtues-called-knowledge is named "(BhG 13.7–11)", which is the 700-verse numbering; in this edition it is 13.8–12.
   - cpt:asvattha-tree is named "… of saṃsāra", but the verses do not use that word (its definition says so).
   - cpt:equanimity is named "Evenness of mind", but the Gītā's word at 13.10 is sama-cittatva, "evenness of thought".
   - cpt:vaisvanara is named "The self common to all men", but 15.14 describes the digestive fire.
   - data/ lists trm:lobha's language as "Pali"; this chunk has Sanskrit, so the merge will see a conflict.
   - The merger's cpt:liberation rename is pending.
5. **Commentators' views recalled, not checked against the bhāṣyas:**
   - notes of 13.3, 13.4, 13.5, 13.7, 13.8, 13.12, 13.13, 13.21, 13.23, 13.25, 13.35, 14.2, 14.3, 14.7, 14.27, 15.7, 15.15 and 15.16;
   - trm:sadharmya's notes;
   - all sides of dsp:bhagavad-gita-ksetrajna-and-the-lord, dsp:bhagavad-gita-jiva-as-amsa and dsp:bhagavad-gita-aksara-purusa, all at low confidence. The Madhva sides are the weakest.
   - Check them in Wave 2.
6. **Level-tag policy**, continuing the ch10-12 item.
   - "ultimate" is used at 13.13, 13.14, 13.16, 13.18, 14.27, 15.6, 15.15, 15.17 and 15.18.
   - "bridging" is used at 13.15, 13.17, 13.23, 13.28, 13.30–34 and 14.19.
   - Comparable descriptions of the Lord (15.12–14) are "unmarked".
   - I accepted these as plausible; one Gītā-wide rule is still needed.
7. **Minor points for the misreading hunter:**
   - Several entities render 13.30 as "oneself as not the doer" (cpt:the-self, prc:guna-witnessing, prc:discerning-field-and-knower, obs:sense-of-doership). The teaching has "one's self", which covers both readings. The reflexive reading is within the verse's sense, so I left them.
   - cpt:gita-transmission calls 14.1's knowledge "the knowledge of the guṇas". That rests on the chapter's context, not on 14.1's words.
   - 15.7 says "draws to itself" for karṣati.
   - 13.26 is tagged stage beginner, which rests on "not knowing in this way".
8. **Praise-reading candidates for the thesis:** 13.24 (sarvathā vartamāno 'pi, also at 6.31) and 13.26. These are recorded in notes, not decided.
