# Role J (judge spot-check and promotion): Yoga Sūtra + Vyāsa, p1-2 and p3-4 single extractions
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## What was checked
**1. Originals (by code).** Every sūtra `original.text` equals its segment's `iast`, and every bhāṣya excerpt is an exact substring of `commentary_iast` that starts and ends on a word boundary.
- p1-2: 213 of 213 match. There is no bhāṣya entry for 1.6 because the edition has no commentary there.
- p3-4: 186 of 186 match.
- No original was changed.

**2. Sample.**
- Seed "20260929:<chunk>", 10% of teachings, stratified by pāda × sūtra/bhāṣya.
  - p1-2: 22 entries (5/5/6/6).
  - p3-4: 19 entries (6/6/4/3).
- On top of that: every low-confidence entry (3 per chunk) and every entry flagged restricted or touching a restricted practice.
  - "Touching" was found by code: a restricted flag, a link to a restricted practice, or keywords such as prāṇāyāma, retention, kṛcchra/cāndrāyaṇa, tapas, rasāyana, herbs.
  - p1-2: 24 entries (10 flagged). p3-4: 7 entries.
- Each entry was read against the Sanskrit for paraphrase, speaker, tags, types and linked ids (right sense, homonyms).

**3. Acceptance.** "Faithful as written" was scored strictly: a wrong-sense link or a wrong type counts as a fail.
- p1-2: 16/22 = 72.7%.
- p3-4: 18/19 = 94.7%, below the ≥95% bar.
- Both chunks were therefore checked entry by entry: 215 + 189 = 404, all with fidelity mode "individually-checked".

**4. By-code screens across everything.**
- All top-level and nested link ids resolve against data/ and the two shards.
- A homonym screen flagged 106 linked data/ ids that have no Yoga or Sāṃkhya sense. J judged each one, which produced a removal/replacement table:
  - 43 term ids removed.
  - 2 concept ids removed: `cpt:kaya-siddhi`, `cpt:sattva-ksetrajna-distinction`.
  - Replacements:
    - `trm:bhuta` → `trm:mahabhuta`
    - `tch:nandisvara` (the Prābhākara author) → `tch:nandisvara-bhasya-example`
    - `cpt:five-niyamas` (Theravāda) → `cpt:niyamas`
    - Jain `cpt:four-bhavanas-maitri` / `prc:maitri-adi-bhavana` → `cpt:four-attitudes` / `prc:four-attitudes`
    - `prc:indriya-samyama` → `prc:samyama`
- A wording scan for modern-psychology, medical and prediction terms.
- Every quoted warning checked as verbatim in its cited segment: 11 of 11.
- A scan for process notes left in the data found one (YS 3.53).

## Results
**p1-2** (215 teachings): 153 passed, 62 fixed.
- 16 paraphrase/notes fixes:
  - 1.22: the "[the means]" bracket contradicted Vyāsa's grading.
  - YBh 1.24: "tatsaṃbandha" is connection with the bonds, not with the liberated.
  - YBh 1.36: the whole twofold activity is jyotiṣmatī.
  - YBh 1.44: the negation "anavacchinna" was dropped.
  - YBh 2.5: the YS 2.15 quote was attributed to Vyāsa; "deceived by praise" was not in the text, and the "viparyāsa" conclusion was omitted.
  - YBh 2.13: the second half of the bhāṣya was added.
  - YS/YBh 2.15: "his contrary nature" was a misattribution; tṛpti is satisfaction, not craving.
  - YBh 2.18: pradhāna here means "the predominant guṇa".
  - YBh 2.23 (low): the omitted view "arthavattā guṇānām" was added.
  - YBh 2.24 (low): the ācāryadeśīya is answering the objector.
  - YBh 2.42 and 2.52: arthavāda labels removed from text-layer notes.
  - YBh 2.43: note overgeneralised 3.37.
  - YBh 2.50: restricted content reduced to summary level.
  - YBh 2.54: "queen bee" restored to the text's king of the bees (madhukara-rāja).
- 45 link-only fixes, including wrong-context links (1.31, 1.32 `cpt:five-vrttis`; 1.33 `cpt:pratipaksa-bhavana`; 2.43 `cpt:siddhis-as-obstacles`).
- 1 type fix: YS 2.55 was typed "dispute".
- 71 link operations in total.

**p3-4** (189 teachings): 136 passed, 53 fixed.
- 12 paraphrase/notes fixes:
  - ch3 and thesis: 3.37 had been generalised to all powers; Vyāsa limits it to the 3.36 perceptions.
  - YBh 3.10: vyutthāna-dharmin is a bahuvrīhi.
  - YBh 3.17: speech organ functions only in producing sounds; the result clause was missing.
  - YS 3.21: the locative absolute had been read as a second object of saṃyama.
  - YBh 3.52/2: the moment is vastupatita (real), and the omitted clause "what yogins call time" was restored.
  - YS 3.53: a note addressed to the judge was removed.
  - YBh 3.53 (low): who is distracted was reversed, and the bhāṣya's own solution was missing.
  - YBh 3.53/2 (low): Vyāsa's rejoinder had been given to the "apare".
  - YBh 4.14: the idealist's argument had been presented as Vyāsa's own.
  - YS 4.15: cause and consequence were reversed.
  - YBh 4.23: "the unconscious" changed to sentient/insentient.
- 37 link-only fixes, including the YS 3.18 teacher links to Jaigīṣavya and Āvaṭya, who appear only in the bhāṣya.
- 4 type fixes: 4.10, and 4.33 ×3 (classification of questions, not a debate).
- 52 link operations in total.

**One judgement retracted by J.** I first proposed a fix at YBh 2.17 ("anyasvarūpeṇa pratilabdhātmakam"), then withdrew it. Vyāsa uses the same idiom at 2.21 and 2.22, so the extractor's literal rendering stands.

**Restricted material.**
- Summary-only everywhere, with no counts, steps or durations: 1.34, 2.49–2.53, the 2.32 fasting vows (named only), tapas, and rasāyana/herbs at 3.51 and 4.1.
- Vyāsa's own warnings are quoted verbatim (2.1 tapas, 2.30 truthfulness, 2.34, 3.51).

**Entities.** 484 entities (366 in p1-2, 118 in p3-4) were copied with a J `verification.checks` record; no level was raised. 10 were corrected, each with a `correction_log`:
- "anxiety" → "torment" for tāpa, in 4 entities.
- "queen bee" → king of the bees, in `prc:pratyahara` and `trm:madhukara-raja`.
- `dsp:nature-of-adarsana`: the list of views aligned with YBh 2.23.
- `dsp:is-liberation-cessation-of-mind`: the lineage moved from the objector to the ācāryadeśīya; the objector is now marked reported_by_opponent.
- `cpt:vibhutis` and `prc:samadhi`: the 3.37 scope corrected.

**Skeleton decisions.** 178 + 136 copied unchanged. Every `replaced_by` exists; none points to the other chunk, so there was nothing cross-chunk to resolve.

**Validation.** `scripts/validate_shard.py` on both `final/` folders: 0 errors. The only warning in each is "REPORT.md missing", which is expected.

## What could not be checked
- No published translation was consulted; Woods (HOS 17) is not available offline. Edition readings were taken as they stand, including ".uparaktā" at 1.43 and "īśravasya" at 1.27.
- Entity definitions were not read line by line. Their sense was checked only through the teachings J read, except the restricted practices and the entries corrected above, which were read in full. That includes the 248 p1-2 and 68 p3-4 terms.

## Open points for the orchestrator
1. **`tea:yoga-bhasya:mangala` has no decision.** The bhāṣya's opening verse is not in the prepared segments, which start at 1.1, so it needs either that source line or an explicit decision.
2. **Systemic data issue behind the links.** Many data/terms.json entries carry only another tradition's meaning (svarūpa, deśa, samaya, kṣetra, artha, bhūta, citi, prakāśa and others). Future extractions will repeat these mis-links unless:
   - Yoga-sense definitions are added, and
   - the extraction brief requires checking the lineage of any data/ term before linking it.
   Some borderline links were kept because a shared plain sense applies: `trm:mala`, `trm:avarana`, `trm:ayus`, `trm:dosa`/`trm:dhatu` (Vyāsa's own list at 3.29), `trm:punya`, `trm:samyag-jnana`, `trm:adhyasa`, `trm:avayavin`, `trm:viparyasa`, `trm:manojavitva`, `trm:darsana`, `trm:vidya`. These are for the term/reconciliation auditor.
3. **Suggested entries for DECISIONS.md** (J did not edit it):
   - tāpa is rendered "torment", not Woods's "anxiety".
   - cetana/acetana is rendered "sentient/insentient".
   - arthavāda labels are kept out of text-layer notes (P7 belongs to the interpretation layer).
   - YS 3.37 is recorded as applying to the perceptions of 3.36.
   - The wrong-sense link table as a whole (the full list and reason for each removal is in the fix fields of fidelity.jsonl).
4. **Possible refinements, not errors:**
   - "kāryā vimukti" is rendered "accomplished" (YBh 2.27).
   - vṛṣadaṃśa is left untranslated (YBh 4.9/2).
   - YBh 2.13 and 3.53 now paraphrase beyond their key-sentence excerpt, as the brief allows.
5. **How the verdicts were recorded.**
   - All scripts ran inline; no helper files were written.
   - `fidelity.jsonl` was rewritten at the end as one consolidated line per teaching: id, chunk, sample membership, criterion, verdict, machine-applicable fix list, evidence.

## Files
- /home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p1-2/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p1-2/final/ (9 files)
- /home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p3-4/fidelity.jsonl
- /home/user/allprojects/tradition-ontology/shards/extraction/yoga-sutra/p3-4/final/ (10 files)
