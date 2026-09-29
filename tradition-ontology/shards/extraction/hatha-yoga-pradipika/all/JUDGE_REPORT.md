# Role J report: Haṭha Yoga Pradīpikā, chunk `all` (insight-p1-single+spot)
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


Judge: J (onto-judge), 2026-09-29. Inputs: `single/` (393 teachings, 115 entities, 229 skeleton decisions), `sources_raw/prepared/hatha-yoga-pradipika/segments.jsonl` (Sanskrit only), and the extractor's REPORT.md. No translation and no Jyotsnā were used.

## 1. Originals (by code)
- All 393 teachings were checked:
  - 387 whole-segment originals equal the segment IAST exactly.
  - 1.17/2 is an exact substring of segment 1.17.
  - ch1–ch4 and the thesis carry no original.
- No segment lacks a whole-segment teaching, and there are no duplicate ids.
- Result: 0 mismatches, nothing to fix.
- Recheck on `final/`: originals are unchanged and still equal the segments.

## 2. Sample and acceptance
- **How the sample was drawn:**
  - `random.Random("20260929").sample` per upadeśa stratum, k = ceil(10%).
  - Chapter entries are counted in their upadeśa and the thesis in upadeśa 4.
  - Strata: 7, 8, 14 and 12 entries, 41 in total.
- **Result:** 38 of 41 faithful as written (92.7%), below 95%.
  - 1.12: the bow-length was misread as the size of the place.
  - 3.52: the paraphrase claimed the verse "describes how" the flow is held; it gives no description.
  - 3.99: "under a yogin" is imported; the e-text's "sāpi yoginā" is unclear.
- **Consequence:** every teaching was read individually against the Sanskrit (all 39 low-confidence and all 240 restricted included).
  - Every entry has `fidelity {status passed|fixed, checked_by J, date 2026-09-29, mode individually-checked}`.
  - Every entry has `verification.level` text-verified and `protocol` insight-p1-single+spot.
  - Confidence values are left as the extractor set them.
- **Totals:** 353 passed, 40 fixed, 0 failed.

## 3. Fixes (40 teachings, each with a `correction_log` item citing the Sanskrit)
- **Construal errors in the paraphrase (24):**
  - 1.10: "ādhārakamaṭhaḥ" can be divided as hut or as tortoise; both are recorded, and the paraphrase keeps only "support".
  - 1.12: the bow-length.
  - 1.28: "later named" is wrong; the verse names the posture itself.
  - 1.40: the result (niṣpatti) was not named.
  - 1.41: the kevala-kumbhaka condition had been dropped, which changed the sense.
  - 1.56: the order of practice was listed and then said to be withheld, and the note wrongly called "atha nādānusandhanam" a heading.
  - 3.31: the caution "svalpaṃ prathamasādhanam" (the first practice is small) had been lost.
  - 3.37: which thing the text calls vyomacakra.
  - 3.43: "yonimaṇḍala" had been rendered "its place".
  - 3.52: as above.
  - 3.79: sun and moon were reversed; the verse puts the sun above and the moon below.
  - 3.99: as above.
  - 3.106: parameśvarī is "Goddess", not "Lord".
  - 3.113: the verse does not say kuṇḍalī is wrapped as in a cloth.
  - 3.125: "parā" had been translated twice.
  - 4.16: sadbheda means piercing, not "difference".
  - 4.33: the natural reading is "where the gaze is, there is laya".
  - 4.39: the object of "saṃyojya" is unstated.
  - 4.40: "tāraka" had been rendered "liberating light".
  - 4.43: an interpretation had been put into the paraphrase; it is now a labelled note.
  - 4.44: "anilam" is the object, not the subject.
  - 4.73: "atiśūnya" had been flattened into the "great void".
  - 4.96: "manaḥpārada" (the mind as mercury) is the subject.
  - 4.104: "kalpalatikā" is the wish-fulfilling creeper, not "creeper, as it were".
- **Health, longevity or power claims stated as fact, now framed as the text's (6):** 1.9, 3.3, 4.71, 4.103, 4.108, 4.113.
- **Restricted safety (4):**
  - 1.46, 2.49 and 4.68 gave a step-level method; each is now a summary.
  - 1.44 flag set to `restricted: true`: the bound lotus is a strained posture by the extractor's own criterion.
- **Notes and speaker (6):**
  - 1.8: "allamaḥ prabhudevaśca" may be one name or two.
  - 2.37: the note put the verse in the wrong position.
  - 3.9: the note called its quote "verbatim", but it did not match the segment.
  - 2.7 and 3.21: "yathāśakti" added as the text's own limit.
  - 4.58: the speaker is now "Svātmārāma, quoting an unnamed source addressed to Rāma".

## 4. Restricted safety (all 240 original restricted entries, plus 1.44)
- **By code** (scripted scan over the restricted entries, text in the scratch folder listed below): digits, number words, durations, measures, step words and body-procedure words. Every remaining hit was read. They are all harmless:
  - verse refs or the "|| 51 ||" marker;
  - "not reproduced" wording;
  - names of lists ("the eight kumbhakas", "three bandhas");
  - the text's own cautions.
- **By reading:** every restricted entry is summary-only after the three trims above. There are:
  - no counts, schedules, durations or measures;
  - no tongue-cutting details (3.33–3.36);
  - no sexual-rite or bodily-fluid method (3.83–3.103);
  - no mercury method (4.26, 4.27, 4.96).
- **The text's own cautions are quoted verbatim:**
  - 1.15, where the original is the whole verse;
  - 1.61 'prātaḥ snānopavāsādi kāyakleśavidhiṃ tathā';
  - 2.9;
  - 2.15 'anyathā hanti sādhakam';
  - 2.16 'ayuktābhyāsayogena sarvarogasamudbhavaḥ';
  - 2.17 'bhavanti vividhā rogāḥ pavanasya prakopataḥ';
  - 2.21, 3.13, 3.18, 3.78, 3.95, 3.121;
  - 3.81 'alpāhāro yadi bhavedagnirdahati tatkṣaṇāt';
  - newly added: 2.7, 3.21 and 3.31.
- **Health claims:** a code scan of all 393 paraphrases shows every remaining health or death wording is framed as the text's, or is not a health claim (4.2 epithet, 4.13 salutation, 2.59 "sin").
- **Unrestricted postures and nāda verses:** read in full.
  - Postures: 1.19–21, 1.32, 1.34–39, 1.45, 1.47, 1.50–51, 1.53–54.
  - Nāda: 4.65–99 except 4.68 and 4.96.
  - I found no breath retention, strain or inversion, except the bound lotus 1.44, now restricted.
  - Siddhāsana 1.35 (chin on chest) was kept unrestricted as a standard seated posture. That is a judgement call.
  - 4.41, 4.42 and 4.112 describe states, not instructions, and were kept unrestricted.

## 5. Links, entities, decisions
- **Linked ids:** all 118 linked ids resolve (by code): 51 are the extractor's own, 53 are the extractor's own and also in data/, and 14 are data-only.
  - Every reused data/ id carries a hatha-yoga or nātha definition matching the HYP sense (read). Homonyms use -hyp ids (trm:samadhi-hyp, trm:laya-hyp, trm:sunya-hyp, trm:bandha-hyp, tch:*-hyp).
  - trm:satkarma carries both a hatha-yoga and a Kālīkula definition. It is linked in its hatha-yoga sense, which is acceptable for a multi-lineage term.
- **Entities:** 115, levels not raised. Each got a `verification.checks` J record; `rests_on` all resolve (by code). 7 were corrected, with `correction_log`:
  - cpt:hyp-practice-not-talk (4.40);
  - cpt:hyp-warnings-on-breath (3.13 quote made exact; yathāśakti and svalpaṃ prathamasādhanam added);
  - pth:hyp-nada-four-stages stage 2 and phn:hyp-nada-ghata (atiśūnya);
  - phn:hyp-samadhi-state (4.113 wording and framing);
  - tch:allama-hyp and tch:prabhudeva-hyp (division note).
  - Restricted practices were checked summary-only with verbatim warnings.
- **Skeleton decisions:** 229 copied (81 upgrade, 148 correct, 0 retire). Every `replaced_by` and `replaced_by_all` exists (by code). The 1.10 reason was corrected (the tortoise division is valid Sanskrit), with a `correction_log`.

## 6. Open points for the orchestrator
1. **Merge safety:** several restricted practices' existing entries in data/ carry step-level `method_summary` text. Examples: prc:mahamudra, prc:mahabandha, prc:mula-bandha, prc:padmasana (bound form), prc:dhauti, prc:siddhasana. The merge must keep the summary-only restricted text and the restricted flag.
2. **Unresolved text-critical readings** (the only source was the Sanskrit e-text, with nothing to compare against):
   - 3.99 "sāpi yoginā";
   - 1.26 "śrīmatyanātha";
   - 2.51 is embedded in 2.52, and there is no 2.20;
   - 4.20 carries an embedded gloss.
3. **-hyp teacher ids:** tch:mina-hyp, and Allama/Prabhudeva (one person or two), are provisional. Identification is a merge decision.
4. **Missing lineage:** dsp:hyp-is-laya-liberation side 2 has no lineage (the other school is unnamed).
5. **No interpretation_log written:** `final/` mirrors `single/`, so I wrote no interpretation_log.jsonl. The 40 `correction_log` items are the source if text-correction lines are wanted at merge.
6. **Thin restricted summaries:** they omit non-dangerous claims by design (for example 3.100's "nāda becomes bindu"). They are faithful but not complete.

## Files
- /home/user/allprojects/tradition-ontology/shards/extraction/hatha-yoga-pradipika/all/fidelity.jsonl: 508 lines. That is 393 teachings (353 pass, 40 fail then fixed) and 115 entities (108 pass, 7 fail then fixed). Each line has id, sample membership, seed, criterion, verdict, fix, reason, and evidence with file:line and a Sanskrit incipit.
- /home/user/allprojects/tradition-ontology/shards/extraction/hatha-yoga-pradipika/all/final/: teachings, concepts, disputes, obstacles, paths, phenomenology, practices, teachers, terms and skeleton_decisions `.jsonl`. `validate_shard.py` gives 0 errors and 1 warning (REPORT.md missing).
- Scratch folder: /tmp/claude-0/-home-user-allprojects/2c0e32b7-c920-5af7-bfe1-3ee59e322221/scratchpad/judge-hyp/. It holds the per-entry verdicts (V.py), the sample (sample.json), build_final.py, and the scan scripts (rscan.py, cautions.py, quotes.py).
- I ran no git and wrote nothing else in the project.
