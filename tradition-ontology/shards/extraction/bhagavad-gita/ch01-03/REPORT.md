# Fidelity check — Bhagavad Gītā (src:bhagavad-gita), chunk ch01-03 (chapters 1–3)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Role F, fresh context, 2026-09-28. Inputs used: `merged/` only (teachings, entity files, skeleton_decisions) and `sources_raw/prepared/bhagavad-gita/segments.jsonl` + `META.json`. I did not read A/B, the notes files, disagreements or any skeleton shard.

## Counts
| | teachings |
|---|---|
| merged entries checked | 165 (162 verses 1.1–3.43 + ch1, ch2, ch3) |
| passed | 151 |
| fixed | 14 (7 change the meaning or links, 7 change only the notes) |
| failed | 0 |

- All passed and fixed entries are in `final/teachings.jsonl` with verification level `text-verified` and a `fidelity` block (checked by F, 2026-09-28). The `confidence` values are unchanged.
- Every fixed entry has `correction_log` items with the field, the old and new text, and the reason.
- `fidelity.jsonl` in the chunk directory has one line per teaching.

### Checks that were mechanical, and what they found
- **Original text:** for all 162 verses, `original.text` is byte-identical to the segment's IAST.
- **Ids and locations:** all consistent; no verse is missing.
- **Speakers:**
  - 1.21 and 1.28 each have two speakers: Sañjaya narrates the first half and Arjuna speaks the second. The segment's "arjuna uvāca" label applies only to the second half.
  - 1.25 has Kṛṣṇa's words quoted inside Sañjaya's narration.
  - 3.10–12 are Prajāpati's words quoted by Kṛṣṇa.
  - At 2.9, "parantapa" is printed as a vocative addressed to Dhṛtarāṣṭra (checked against the Devanāgarī परन्तप).
- **Terms kept apart:** buddhi ("understanding"), manas ("mind") and cetas stay distinct throughout. Dehin and śarīrin are kept as the text uses them in 2.11–30.

## Fixes that change the sense or the links (7)
- **2.16:** "of the unreal … no coming to be; of the real … no ceasing to be" became "of what is not (asat — the non-existent or unreal) there is no being (bhāva); of what is (sat — the existent or real) there is no non-being (abhāva)". The old wording chose one side of a division that the entry's own note records (existence or reality). ch2's summary and the entities cpt:real-and-unreal, trm:sat and trm:asat were aligned.
- **2.5:** "even though they are 'arthakāma' … only pleasures smeared with blood" became "having killed the gurus — 'arthakāmān' — I would enjoy, here in this very world (ihaiva), pleasures smeared with blood". The concessive reading settled a disputed construal. "Only" was not in the verse: *eva* goes with *iha*.
- **2.43:** "whose selves are made of desire (kāmātman)" became "full of desire (kāmātmānaḥ, 'whose nature is desire')". Here ātman is used reflexively; the old wording read it as the self the text teaches about.
- **2.55:** "content in the self by the self alone" became "content in the self alone, by the self". *Eva* restricts *ātmani*, not *ātmanā*.
- **3.42:** removed the link to trm:atman. The verse says only "he" (*saḥ*); identifying him with the self is the commentators' reading and stays in the note. trm:atman remains linked from 3.43.
- **ch3:** "only the ego-deluded thinks 'I am the doer'" became "only one deluded by the sense of 'I' (ahaṃkāra)". "Ego" is a modern psychological word.
- **ch2:** aligned with the new 2.16 wording.

## Fixes to the notes only (7)
- **1.29:** the note pointed to phn:bhagavad-gita-arjuna-visada-signs, which does not exist. It now points to phn:arjuna-despondency.
- **2.26:** the note claimed a "polemical" tag that the entry does not carry (the standpoint is "seeker"). The note now matches the tag.
- **3.3:** "original declarer" overstated *purā proktā mayā*. The same note allows *purā* to mean "earlier", i.e. at 2.39.
- **2.7, 3.25, 3.26, 3.29:** removed references to the pipeline ("the skeleton's note", "A's stage label").

## Entity files (checked and copied into final/)
- I read every entry: 143 terms, 32 concepts, 20 obstacles, 11 practices, 1 path, 11 phenomenology items, 3 disputes and 38 teachers.
- I made 29 changes, each logged in `final/interpretation_log.jsonl` (19 corrections against the text, 10 removals of duplicates). The main ones:
  - **prc:svadharma-anusthana:** removed the name "svanuṣṭhita dharma". This was a misreading of 3.35: *svanuṣṭhitāt* ("well performed") describes another's dharma (*paradharmāt*), not one's own.
  - **cpt:imperishable-embodied-self:** removed "ātman" from its names. 2.11–30 never uses the word; the commentators' identification stays as a partial equivalence on trm:dehin.
  - **trm:atman:** the definition no longer treats 3.42's *saḥ* as ātman as though the text said so.
  - **obs:asuya:** its name was linked to trm:mata; it now links to trm:asuya.
  - **cpt:gita-transmission:** 1.3 says Drupada's son *arrayed* the Pāṇḍava army, not that he *leads* it.
  - **cpt:three-gunas:** the reading of sattva at 2.45 is now given as one reading, not as fact.
  - **"Sāṃkhyas/Yogins" lower-cased** in the entries using them. At 3.3 these words name the followers of the two commitments, not the later schools.
  - **tch:krsna:** "original declarer" corrected, as at 3.3.
  - **prc:karma-yoga:** "prescribed action" became "allotted action (niyataṃ karma)".
  - **Duplicate list items removed.** The merge of A and B had left duplicates in the members, names, warnings and antidotes lists of 5 concepts, 5 practices and 2 obstacles.
- Phenomenology, disputes, paths and skeleton_decisions are copied unchanged: 72 upgrade and 1 correct decisions, and every `replaced_by` target exists.
- **Entity verification levels are left at `skeleton`.** The brief raises only teachings to text-verified. Most entity entries rest only on text-verified teachings of this chunk, so the merge or the next gate may raise them.

## For the next wave to revisit
1. **Encoding faults in the edition.** The Devanāgarī itself has old-font glitches, carried into the IAST:
   - 2.7 niśicataṃ (the Devanāgarī reads निश्िचतं)
   - 3.2 niśicatya
   - 3.5 kaśicat
   - 3.18 kaśicad
   - 3.25 saktaśicakīrṣur
   - 2.29 śrṛṇoti
   - 2.39 śrṛṇu
   - 1.34 ścaśurāḥ
   - 1.26 a stray nukta

   There are also speaker headings ("śrī bhagavān uvāca") inside the IAST at 2.2, 2.11, 2.55, 3.3 and 3.37, and the segment speaker label sits on the whole verse even when the speaker changes mid-verse (1.21, 1.28). All are kept as printed and noted, but chapters 4–18 will have the same faults. An errata list at source level is recommended.
2. **Pairs of ids to merge in the de-duplication pass:**
   - cpt:imperishable-embodied-self ↔ cpt:the-self
   - cpt:samatva ↔ cpt:equanimity
   - prc:indriya-samyama ↔ prc:indriya-nigraha
   - cpt:descent-from-sense-objects-to-ruin ↔ obs:chain-from-dwelling-on-objects
   - cpt:kama-as-the-enemy ↔ obs:kama-the-enemy
   - cpt:last-thought ↔ cpt:last-thought-at-death
   - cpt:real-and-unreal ↔ cpt:sat-and-asat (the note says these differ)
   - the three disputes against the old A/B ids given in their notes

   Two phenomenology ids lack the `bhagavad-gita-` prefix: phn:arjuna-despondency and phn:awake-in-the-night-of-beings.
3. **Dispute ids used but not defined in this chunk:** dsp:causation, dsp:souls-one-or-distinct, dsp:works-knowledge-grace and dsp:world-real-or-appearance. They are registry ids, so the merge must resolve them.
4. **Contested verses for the misreading hunter:** 2.16, 2.5 (arthakāmān), 2.45 (nityasattvastha), 2.46 (the well simile; confidence low), 3.15 (brahman/akṣara; confidence low), 3.17–19, 3.3 (purā), 3.26 (joṣayet), 1.10 and 2.12. At 2.26, the standpoint (seeker or polemical) is a judgement call.
5. **For the hallucination hunter:**
   - Cross-references to other texts: Kaṭha 1.2.7, 1.2.18, 1.2.19 and 1.3.10; Chāndogya 6.2.2 and 7.25.2; Muṇḍaka 3.1.4.
   - References in notes: Manusmṛti 3.76; Taittirīya 3.2 (marked "from memory"); BĀU 4.4.7; Kaṭha 2.3.14.
   - Check that the target teaching ids use the same ref format as the Upaniṣad extractions.
6. **Things the Gītā alone cannot verify:**
   - Epic identifications on teacher entries: Saubhadra = Abhimanyu, Saumadatti = Bhūriśravas, Yuyudhāna = Sātyaki, the ācārya = Droṇa, drupadaputra = Dhṛṣṭadyumna.
   - The lin:bhagavata-early lineage on Arjuna, Bhīṣma and Kṛṣṇa.

   These should stay labelled as epic context.
7. **Tagging conventions to keep the same across chunks:**
   - The frame verses 1.1–1.27 use standpoint "ethical-social" by convention, since no narrative standpoint exists.
   - "powers-experiences" is used for Arjuna's bodily signs at 1.29–30.
   - prc:isvararpana's id uses *īśvara*, a word that is not in 3.30.
