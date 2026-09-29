# Next steps

This lists what is left after the insight build of 2026-09-29. Items are ordered by what blocks release first.
RELEASE_REPORT.md has the gate status.

## 1. Blocking release
1. **Run every live-model gate with an API key.** None has been run, because this session had no key.
   - **Steps to exercise:**
     - the model safety screen, which runs first and fails closed;
     - candidate mapping and the blind recheck;
     - two-lens synthesis;
     - pathway wording;
     - content drafts and the Opus content check.
   - **Commands:**
     - `ANTHROPIC_API_KEY=… python3 scripts/run_eval.py --engine model`
     - `python3 scripts/build_content_queue.py --engine model --fresh --data-dir <new dir>`
   - **Then:**
     - judge the packets in `eval/judge/model/`;
     - write measured costs into COSTS.md;
     - re-run the red team against the model engine.
2. **Recall of the person map.** The offline rules engine maps only 2 of 30 hidden personas; both are genuine, and 28 get an honest "could not connect". Lexical cues do not generalise: 15/30 on the development set against 2/30 on the hidden set. The model engine's blind recheck is the designed path for paraphrase and must be measured, not assumed. Do not tune cues on the hidden set.
3. **Gates that could not be judged meaningfully offline.** The swap test and citation integrity rest on 2 mapped readings. Re-judge them on model-engine output with at least 20 mapped readings.

## 2. Product
- **Prompt caching.** Put the mappable-marker catalogue in a cached system block for candidate mapping (COSTS.md).
- **Practice layer:**
  - the four TS 9.6 "uttama" practices stay excluded until Daśavaikālika 8.36–38 is text-verified;
  - move their W1 product notes into tier_reason;
  - reframe śauca, or keep it excluded;
  - optional edits: YS 1.39 step 2 (name sexual imagery and intoxicants); the MN 118:26 quote in W2 of the four satipaṭṭhāna entries.
- **diagnosis.json paired_practices.** Align with the practice layer's targets, and review every pairing the texts do not make themselves (the pathway already says when the pairing is the reading's).
- **Entries:**
  - envy has no mappable entry of its own (it is only a named state inside dx:carita-dosa);
  - fear of losing someone falls outside every marker's described sense.
- **Content:**
  - pools under 30 items leave 4–8 calendar days per month with no suggestion;
  - redrafting an item after 30 days may trip the 0.5 similarity rule because scenes are fixed, so add scene variants;
  - check each platform's AI-content policy at posting time.
- **Safety screen:**
  - English only in v1 (Hindi and Hinglish crisis phrases are partly covered);
  - write a proper multilingual screen before any non-English launch;
  - check the crisis numbers before each release (RUNBOOK).
- **Red-team low findings:** see eval/redteam/RED_TEAM.md.
- **Deployment:**
  - TLS reverse proxy;
  - a secret store for ONTO_DATA_KEY and ONTO_ADMIN_TOKEN;
  - a daily purge job;
  - log retention;
  - `ONTO_ENGINE=model` in production. In `auto` mode with no key the model screen does not run.

## 3. Ontology (Tradition Ontology)
- **Skeleton citations the layers or tables still need:**
  - Daśavaikālika 8.36–38;
  - TS ch. 1–5 and the other sūtras, e.g. 10.1–2 context and 5.21;
  - Gommaṭasāra Jīvakāṇḍa 9–10 (guṇasthāna map);
  - MN 24 (seven purifications), Ud 8.3, Vism XVI, XVIII, XIX, XX (Theravāda one-truth row);
  - MMK 18.6;
  - DN 2 (sāmaññaphala 67–74);
  - Kārikā 2.22 (shares a segment with 2.23);
  - tea:yoga-bhasya:mangala.
- **Homonyms and mixed senses in data/terms.json:**
  - trm:samana (vital wind) vs trm:sramana;
  - trm:bhava, trm:dosa, trm:aloka, trm:nidana, trm:vicara, trm:kasaya (Gauḍapāda vs Jain);
  - the 18 -gk/-mu ids with the same sense as their base ids (fold them in);
  - entries holding only another school's sense: trm:punya, trm:artha, trm:acara, trm:paurusa;
  - Yoga-sense definitions for svarūpa, deśa, samaya, kṣetra, artha, bhūta, citi, prakāśa;
  - data/'s older ārta renderings ("sorrowful", "brooding"): align them with the verified shard ("pained").
- **Restricted content:**
  - merge.py now redacts restricted practices and unchecked restricted teachings mechanically;
  - sweep the remaining skeleton teachings and concepts by hand, e.g. the Jain parīṣaha and tapas concepts that list hardships with counts.
- **paths.json:**
  - dharmamegha is placed at B8 (YS 4.29 puts it before kaivalya);
  - the eight-limbs stages lost their rests_on;
  - the guṇasthāna bands run against the Jain order;
  - MN 118 step 12.
- **Hard reconciliation items (tables report):**
  - the B7 band;
  - negation across traditions (Heart Sūtra and neti neti);
  - Gītā inclusivism under P3;
  - bands against a tradition's own order;
  - RQ-U50-01, the self-question: side by side, not yet reconciled.
- **Gītā text-level gates:**
  - one consistency pass across all 18 chapters (citta/cetas; reflexive ātman; level tags "ultimate" vs "bridging" vs "unmarked");
  - duplicates left by the code-combined merge;
  - the commentators' views, recalled in notes, to be checked against the bhāṣyas.
- **Skeleton upgrades whose brackets carry commentarial glosses:** TS 9.6, 9.7, 9.22, 9.28, 9.35, 9.36, 10.1, 10.7, 10.8.
- **The earlier ontology plan, paused by the user at 18:18 IST:**
  - U51–U54 were stopped mid-run, with partial output kept;
  - U55–U60 are queued;
  - the Phase C sweeps C-U08–C-U11 were stopped;
  - lojong root reconstruction was stopped.
  - Nothing was relaunched, as the user chose.
