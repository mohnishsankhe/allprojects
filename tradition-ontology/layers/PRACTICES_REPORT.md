# Practice layer: layers/practices.json
_(Returned as text by the unit's subagent — subagents cannot write report files in this harness — and saved verbatim by the orchestrator.)_


## Files (all written inside layers/)
- `/home/user/allprojects/tradition-ontology/layers/practices.json`: a JSON list, UTF-8, indent 1, 54 entries. Fields are in the SCHEMA order.
- `/home/user/allprojects/tradition-ontology/layers/_gen/practices/entries.py`: all entry content, with the cite helpers.
- `/home/user/allprojects/tradition-ontology/layers/_gen/practices/build.py`: builds the file and validates it. It exits non-zero on any error.
- `/home/user/allprojects/tradition-ontology/layers/_gen/practices/build_report.json`: counts, tiers, user_facing reasons, cite status, ontology_ref levels, errors and warnings.
- `/home/user/allprojects/tradition-ontology/layers/_gen/practices/fetch.py` and `find_prc.py`: helpers that fetch passages and search prc: entries.

I removed a `__pycache__` that my imports had created in `layers/_gen/diagnosis`. Nothing was written outside layers/. I did not run git.

## How entries were built
- **Targets** are not written by hand. `build.py` reads them from the `paired_practices` in `diagnosis.json`, and they match exactly (checked).
- **Summaries** state the practice as the cited text does. I read each passage by code:
  - Yoga Sūtra with Vyāsa (`commentary_iast`), Gītā, Kaṭha, Taittirīya, Māṇḍūkya and Gauḍapāda from `sources_raw/prepared`;
  - MN10, DN22, MN118 and Dhp 5 in Pāli with the Sujato translation;
  - DN2:67–68 from the local bilara root and translation;
  - TS in IAST;
  - Visuddhimagga pages from the GRETIL e-text through `layers/_gen/diagnosis/vism.py`.
- **Cite forms** follow `diagnosis.json`: `tea:yoga-bhasya:<v>` for Vyāsa, `tea:visuddhimagga:<ch>.p<PTS page>`, and the existing id `tea:samannaphala-sutta:67-74` for DN2.
- **Steps** are given only for gentle entries, 3–6 each, made only of the text's own instructions plus "sit comfortably" and a gentle close.
- **Omissions from steps.** Where the text contains something outside the gentle tier, the steps leave it out and a warning says so:
  - Vyāsa's "austerity and celibacy" (YB 1.14);
  - the fourth ānāpānasati step, "stilling the bodily process", so that it is never read as holding the breath;
  - the Visuddhimagga's undertaking "not to eat without giving" in recollecting generosity (VII p.223);
  - the TS 9.7 reflections on impurity of the body and on helplessness;
  - equanimity, which Vism III p.114 says is not for beginners;
  - the Visuddhimagga's graphic example for compassion (IX p.314).
- **Warnings.**
  - Every gentle entry has at least one cited caution or condition.
  - Where the pairing text gives none, I cite the nearest general caution in the same family and say so in the wording:
    - Vyāsa on 2.1 (discipline must not disturb the mind's clarity);
    - MN118:26 (no development of mindfulness for one who is unmindful and lacks awareness);
    - KU 1.2.8–9 (the understanding must be taught by another; reasoning does not reach it), for Oṃ;
    - TS 9.30–33 (reflection must not turn into ārta brooding).
  - Other textual cautions used:
    - Gītā 6.16–17 (moderation) and 6.23 (an undejected mind);
    - BhG 2.59 (the restraint is of the senses, not a fast) and 2.60;
    - BhG 3.8 (the guṇa-witnessing does not cancel action);
    - Vism IX p.296 (whom not to begin mettā with);
    - Vism IX p.298 (what to do when resentment arises);
    - Vism IX p.318–319 (the failures and the near and far enemies);
    - Vism VII p.227 and VIII p.294 (these succeed fully only in noble disciples; an ordinary person may attend to them);
    - GK 3.39, 3.41 and 3.45;
    - KU 1.3.14 and 2.3.11.
  - I did not use HYP 2.15–16. No gentle practice involves breath regulation, and it would be a citation from another text family.
- **Duration.**
  - Gentle entries use 5–10 minutes once a day, basis "product default for a beginner; the text gives no length". The sampajañña entry adds that the text applies it to all activities.
  - Non-gentle entries have null minutes, with the basis "summary only".
  - Dharmya-dhyāna notes that TS 9.27 limits dhyāna to within one muhūrta.

## Tier calls worth reviewing (all chosen as the stricter option where unsure)
- **Needs-teacher even though not dangerous:**
  - bhakti-yoga (BhG 14.26): a whole-life devotion that cannot be set up in steps; 12.9–11 is the text's own graded path.
  - approach-a-teacher (BhG 4.34): the practice is the teacher relationship itself.
  - ātma-anātma viveka (BhG 2.11–30): it answers grief over death on a battlefield, and the argument leads on to the duty to fight (2.31). As a self-guided exercise it could be heard as "do not grieve for your dead".
  - Oṃ meditation (MāU 8–12).
  - Gauḍapāda's manonigraha and GK 3.43, which sit within asparśa-yoga (3.39: "yogins fear it").
  - KU 1.3.13 (graded withdrawal toward "the highest state").
  - MN10:38 aggregates and MN10:44 truths (analytic insight; DN22's exposition of the truths dwells on old age and death).
  - YS 3.51 (advanced, and set in the context of siddhis).
- **Vrata (TS 7.1) is never-recommend** rather than needs-teacher, because the great vow includes total celibacy.
- **Kāyagatāsati (the 32 parts) is never-recommend.** It is a repulsiveness (paṭikūla) contemplation, and Vism VIII p.241 has it learned from a teacher.
- **Gentle but thin:**
  - The four TS 9.6 virtues. The sūtra gives only the names. Their steps are recollection of the sūtra's words plus the one explicit pairing I found, in the Daśavaikālika (skeleton teaching `tea:dasavaikalika-sutra:8.36-38`, "conquer anger by calm, pride by gentleness, deceit by straightforwardness, greed by contentment").
  - I could not check the Daśavaikālika wording against a local text; there is none.
  - For śauca, a warning notes that its pairing with greed is the commentaries' reading, and that the Daśavaikālika names contentment against greed, not śauca.
- **Ānāpānasati first tetrad is gentle** because it is knowing the natural breath. I mention the Visuddhimagga's statement that this subject is weighty (VIII p.284) in `tier_reason` text rather than in `cites`, so that it does not block user-facing use of the verified MN118 grounding. Tell me if you want it moved into `cites`; that would make the entry non-user-facing.

## user_facing rule applied
- SCHEMA says an entry that cites any teaching that is not sourced or text-verified stays in the file with `user_facing: false`.
- I computed this with the app's own `insight.ontology.citable`, which includes the range-covering resolution. So `user_facing` is true only when every cite, including every warning cite, is citable.
- 20 entries are true. The app's loader, run on the written file, loads 20 practices and 13 gentle ones.
- **This is stricter than `diagnosis.json`.** That file sets all 102 entries to true even though it cites 79 skeleton teachings and 82 that are not in data; the app then filters per cite. Please decide which convention both layers should follow.

## What I checked by code (`build.py`, then a separate re-check of the written file)
- Every px id in `diagnosis.json` is present; there are no extras or duplicates, and targets equal the pairings.
- Tier, stage, lens and field order are valid, and every tradition exists in `data/lineages.json`.
- Every gentle entry has 3–6 steps, a duration and at least one warning with cites. Non-gentle entries have `steps: []`. Every warning has cites.
- A scan of gentle steps for danger words (retention, fasting, corpse, death, repulsive, celibacy, inversion and similar) found none.
- The clinical and health word scan covered the requested list (cure, heal, treat, therapy, symptom, anxiety, depression, stress relief, lowers, reduces) and more (diagnosis, disorder, patient, medical, health, wellness). The final file has 0 hits; two earlier hits ("anxiety" and "treated") were reworded.
- Every one of the 185 distinct cites resolves:
  - 75 are text-verified in data, 3 sourced, 53 skeleton;
  - 54 are not in data but their ref exists in the local source: Visuddhimagga pages, some Vyāsa and GK verses, and TS 9.30.
- All 69 ontology_refs exist in `data/practices.json`: 49 skeleton, 20 sourced.

## What I could not check
- The Daśavaikālika 8.36–38 wording (skeleton only; no local text).
- The Visuddhimagga renderings are my own reading of the Pāli e-text; no verified teaching entries exist for them.
- The steps have not been through a fidelity checker. That quality gate is still due before any user-facing use.
- `scripts/check_layers.py`, which SCHEMA names, does not exist yet, so its rule that every cite must resolve in data was not run. Under that rule the 54 cites that are not in data would fail, the same as in `diagnosis.json`.

## For the orchestrator (for DECISIONS.md, not written by me)
1. Decide one `user_facing` convention for both layers: strict per entry, as I applied it here, or per cite, as `diagnosis.json` does.
2. Priority for verification. Extracting or text-verifying these would unlock 14 more gentle entries:
   - Yoga Sūtra and Vyāsa 1.12–15, 1.32–33, 2.1, 2.33–34, 2.46–47;
   - Visuddhimagga III p.114–115, VII p.197–198 and 227, VIII p.293–294, IX p.295–298 and 314–319;
   - TS 1.2–4, 9.2, 9.6–7, 9.30–33;
   - Daśavaikālika 8.36–38.
3. Record the tier calls listed above, especially vrata as never-recommend, kāyagatāsati as never-recommend, and ātma-anātma viveka as needs-teacher.
4. There are no prc: entries for śreyas–preyas viveka, the TS 9.6 virtues, tattvārtha-śraddhāna, maggāmagga, YS 3.51 or BhG 2.11–30. These are candidates for the gap hunter.
