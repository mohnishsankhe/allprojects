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


## P1 refresh (2026-09-29): newly verified texts

_Written by onto-analyst. Only `layers/practices.json` was changed (30 entries added and 5 repaired). `layers/diagnosis.json` was read, not edited._

### Result
- There are now 84 entries (54 before).
- 69 are usable by `insight.ontology.practices()` (35 before).
- 45 are **gentle and usable** (19 before). By lens:
  - vedic-yogic: 7 → 21;
  - ascetic-buddhist: 6 → 12;
  - ascetic-jain: 6 → 12.
- Every new entry is loaded by `practices()`. The loader drops no cite and no warning from any new or changed entry.

### Added
**Vedic-yogic, gentle (10).**
- Vijñāna Bhairava (lineage `lin:trika`):
  - `px:vbt-sound-to-its-end-41`
  - `px:vbt-middle-between-two-61-62`
  - `px:vbt-watching-a-desire-arise-96`
  - `px:vbt-unstirred-amid-the-passions-101`
  - `px:vbt-neither-attachment-nor-aversion-125-126`
  - `px:vbt-wherever-the-mind-goes-116` (verses 116–117)
  - `px:vbt-letting-go-where-the-mind-goes-129`
- Yoga Sūtra: `px:vitaraga-citta-ys-1-37`, `px:yathabhimata-dhyana-ys-1-39`.
- Gītā: `px:speech-that-does-not-agitate-bg-17-15`.

**Vedic-yogic, not gentle (6).**
- needs-teacher:
  - `px:vbt-desire-as-the-self-97-98`
  - `px:vbt-fixed-gaze-76-80-84`
  - `px:pranava-japa-ys-1-27-29`
  - `px:nadanusandhana-hyp-4-65-102`
- never-recommend:
  - `px:vbt-body-burnt-by-the-fire-of-time-52-53`
  - `px:vbt-looking-down-into-a-well-115`

**Ascetic-buddhist, gentle (6).**
- Dhammapada:
  - `px:appamada-dhp-21-27`
  - `px:guarding-the-mind-dhp-33-36`
  - `px:not-harbouring-the-grievance-dhp-3-5`
  - `px:restraint-of-body-speech-mind-dhp-231-234` (it also uses Dhp 222–223)
  - `px:own-deeds-not-others-faults-dhp-50-252`
- Visuddhimagga: `px:recalling-the-good-in-one-who-wronged-vism-9` (IX p.296–301).

**Ascetic-jain, gentle (6).** All from the Tattvārtha Sūtra:
- `px:anitya-anupreksa-ts-9-7`
- `px:asrava-samvara-anupreksa-ts-9-7`
- `px:supports-of-truthful-speech-ts-7-5`
- `px:letting-go-of-liking-and-disliking-ts-7-8`
- `px:seeing-harm-in-the-faults-ts-7-9-10`
- `px:noticing-sorrowful-dwelling-ts-9-30-34`

**Ascetic-jain, not gentle (2).**
- `px:asarana-samsara-anupreksa-ts-9-7` (needs-teacher).
- `px:asuci-anupreksa-ts-9-7` (never-recommend).

**How the entries were built.**
- Targets are existing dx ids. I chose them by reading each dx entry's markers and matching them to what the practice's own verse names. For example:
  - VBT 126 names rāga and dveṣa;
  - Dhp 3–5 is the text quoted in the markers of `dx:nivarana-byapada` and `dx:root-dosa`;
  - TS 7.5 names anger, greed, fear and laughter, which the markers of `dx:kasaya-krodha`, `dx:kasaya-lobha` and `dx:jain-nokasaya` cite.
- `diagnosis.json` has no `paired_practices` pointing to the new ids, because I could not edit it. The pathway still finds the new entries through `targets`.
- Steps contain only what the verse says, plus neutral framing ("Sit comfortably", "Close gently").
- Duration is the product default of 5–10 minutes, labelled as such. Practices that run through the day (speech, anger, others' faults) say that the text applies them to all speech or conduct.
- Where a text gives no caution of its own, the warning is the nearest caution from the same text family:
  - YS 1.14 (practice is long and not quick);
  - Dhp 239 ("little by little, moment by moment");
  - TS 9.30–9.33 (reflection must not turn into ārta brooding).
- For the Vijñāna Bhairava, the tantra's own rule of transmission (VBT 157–159) is shown on every entry. VBT 146 (meditation is not the imagining of a form) is added where relevant.
- No gentle entry contains the no-diet trigger words (food, eating, posture, āsana and the rest). All new gentle entries stay eligible under `continue_no_diet`.

### Repairs to existing entries
- **YB 2.1 is restricted** because it glosses tapas, so it cannot be cited. That made four gentle YS entries unusable. The fixes:
  - `px:ekatattva-abhyasa-ys-1-32`, `px:maitri-bhavana-ys-1-33` and `px:pratipaksa-bhavana-ys-2-33`: the "nearest general caution" citing YB 2.1 is replaced by the sūtra's own condition on practice, YS 1.14.
  - `px:abhyasa-vairagya-ys-1-12`: the YB 2.1 caution is dropped, because the entry already carried YS 1.14.
  - `px:abhyasa-vairagya-ys-1-12`: the note citing YB 1.14 (restricted) is also dropped. It said "Vyāsa lists austerity and celibacy among what makes practice firm". The steps never included those supports.
  - All four entries are now usable.
- **`px:anupreksa-ts-9-7` (fidelity).** One step said "the self is other than the body (TS 9.7)". The sūtra gives only the names. The teaching's own note says that reading of anyatva comes from the commentaries (recalled; not in the local segments).
  - The step and summary now say the commentaries read it so.
  - I did not check the commentaries against a local text; none is verified.

### Tier calls (the stricter option where unsure)
1. **The Vijñāna Bhairava's plain attention verses are gentle, with the tantra's secrecy verses as a caution.**
   - VBT 157 says the teaching is "never to be revealed to anyone". VBT 158–159 say it is to be given only to devotees and to the teacher's circle, not to one without devotion to the teacher.
   - No verified verse requires initiation (dīkṣā). So I followed the brief and kept the seven plain verses gentle, with the rule shown verbatim.
   - The alternative is to make every VBT entry needs-teacher. That is a one-field change per entry and needs a decision in DECISIONS.md.
2. **The VBT is placed in the vedic-yogic lens with `tradition: lin:trika`.** It is a Śaiva tantra, not a Vedic text. The product has only three lenses, and the tradition field keeps the distinction.
   - The 116–117 entry states plainly where it differs from the Gītā. The Gītā says to bring the wandering mind back (BhG 6.26); the tantra sees Śiva wherever it goes.
3. **VBT 97–98 are needs-teacher.** Verse 98 asks that an arisen desire be taken as the self; verse 97 rests on the same non-dual doctrine. Out of the tantra's teaching, 98 can be heard as licence to follow desire. VBT 96 is the gentle desire practice.
4. **VBT 52–53 are never-recommend.** They ask one to picture one's own body burnt by the fire of time. This is placed with the death and foulness contemplations.
5. **VBT 115 is never-recommend.** It involves standing over a well or pit and looking down, so there is a risk of falling.
6. **VBT 76, 80 and 84 are needs-teacher.** They are fixed or unbroken gazes, at sunlit space or the open sky in 76 and 84.
7. **YS 1.27–1.29 (repetition of Oṃ) is needs-teacher.** This keeps the layer's existing rule that mantra practice is left to a teacher (Oṃ in the Māṇḍūkya; the note on YS 1.32). The text gives no danger.
8. **HYP nādānusandhāna is needs-teacher.** It uses the śāmbhavī seal and closes the ears with the hands (4.67, 4.82). It also sits in the haṭha stage sequence of piercing the knots (4.69–4.70). HYP 4.68 is restricted and not cited. No HYP entry is gentle.
9. **TS 9.7: impermanence and inflow/stopping are gentle, each as its own short sitting.**
   - No refuge and the round of births are needs-teacher. The sūtra gives only the names; the tradition reads "no refuge" as helplessness before death; the commentaries are unverified.
   - Impurity is never-recommend, as a repulsiveness contemplation. This matches kāyagatāsati and asubha.
   - Aloneness, otherness, shedding, universe, rarity of enlightenment and well-taught dharma get no separate entries. The sūtra gives only their names. Aloneness, otherness and the last two are already in the combined `px:anupreksa-ts-9-7`. Shedding is tied to tapas (TS 9.3, restricted). The universe needs the cosmology of TS 3–4, which is not verified.
10. **Dharma-dhyāna (TS 9.36) stays needs-teacher.** TS 9.27 ties dhyāna to the best bodily frame. The reflection side is covered by the gentle TS 7.9–7.10 and ārta-noticing entries, which do not claim to be dhyāna.
11. **The Dhp 3–5 grievance entry and the Vism IX recalling-the-good entry are gentle.** Their tier_reason says they are not advice to stay in ongoing harm. A reading that mentions abuse is stopped by the safety screen before any practice is chosen (SAFETY.md).

### Left out, and why
- **VBT 71 and 73 (resting in a moment of joy; savouring song).**
  - No dx marker in the layer is answered by them.
  - Two verified texts of the same lens treat savouring the other way: GK 3.45 counts relishing the happiness as an obstacle, and BhG 18.38 calls happiness born of sense-contact rājasic.
  - Presenting them needs a decision on how to show that difference.
- **VBT 72 (eating and drinking)** is left out as the brief says. It is also not named in any entry, so no entry picks up a no-diet trigger.
- **VBT 74** ("wherever the mind finds satisfaction") could be heard as licence for any pleasure.
- **VBT 38** (the inner unstruck sound) is left for a teacher, as with HYP nāda. It is only mentioned in a warning on VBT 41.
- **Restricted VBT verses** (26–31, 36, 64, 66–70, 77, 89, 93, 111, 113–114) are not cited anywhere.
- **YS 2.32 and 2.42 (contentment).** YS 2.32 and Vyāsa's definition of contentment are restricted because they gloss tapas. Only 2.42 is citable, which is too thin for steps.
- **The Visuddhimagga's breath-counting (VIII p.278–280).** The text has this subject learned from a teacher in five links (p.277–278). The existing gentle ānāpānasati entry already covers knowing the natural breath.
- **Careful walking (īryā-samiti) and control of mind (mano-gupti).** TS 7.4 and 9.4–9.5 give only the names.
- **Dhp 379–380** was not used. Its "rebuke yourself" could tilt toward guilt.
- **BhG 16.21** was not used. Its "gate of hell" imagery goes against the tone guide's no-fear rule.

### Verified by code
The script `refresh_p1.py` checked:
- every cite in the 30 new and 5 changed entries passes `citable()`, including every warning cite;
- `practices()` loads all 30 new entries;
- every target exists in `diagnosis.json` (re-checked after writing);
- every `ontology_refs` id exists in `data/practices.json` and is not restricted;
- every tradition exists in `data/lineages.json`;
- field order;
- gentle entries have 3–6 steps;
- non-gentle entries have no steps;
- the dangerous-technique words of `tests/test_schema_layers.py` do not appear in name, summary or steps;
- `claims.scan` finds nothing in name, summary, steps, warnings or tier_reason. One hit ("treats") was reworded.

`scripts/check_layers.py` reports practices: 84 entries, 69 user-facing and 45 gentle.

Test suite results:
- **First run: 298 passed and 1 failed.** The failure was `tests/test_engine.py::test_model_engine_end_to_end`:
  - It expected "No practice could be matched safely" for the fake mapper's `dx:klesa-raga`.
  - `dx:klesa-raga` now has usable gentle practices: the repaired `px:pratipaksa-bhavana-ys-2-33`, plus the new VBT 96, VBT 125–126 and YS 1.37 entries.
- **The test was then changed by someone else, not by me.** It now stubs `pathway.select`, so it no longer depends on the practice layer.
- **Final run: 299 passed.**

### What I could not check
- The steps have not been through a fidelity checker.
- The Tattvārtha commentaries' readings, used in two tier_reasons and in the repaired anuprekṣā step, are not verified locally.
- `layers/_gen/practices/build.py` rebuilds `practices.json` from `entries.py` and the `diagnosis.json` pairings. Re-running it would drop these 30 entries and undo the repairs.
  - The additions live only in the session script `refresh_p1.py` (see the final reply).
  - Either port them into `entries.py`, or retire `build.py`.
- There are no prc: entries for:
  - Dhp 3–5 (non-enmity);
  - Dhp 231–234 (restraint of body, speech and mind);
  - Dhp 50 and 252 (one's own deeds, not others' faults);
  - TS 9.30–9.34 (ārta as something to give up).

  Their `ontology_refs` are empty. These are candidates for the gap hunter.

## Judge fixes (P6)
Source: the P5 practice-safety judge (`eval/judge/practice_safety.jsonl`, `PRACTICE_SAFETY.md`; gate FAIL with 14 pass, 20 fix and 4 demote). The fixes are applied by `layers/_gen/practices/judge_fixes.py`, which is idempotent, edits entries by px id and gives a one-line reason per fix. `build.py` runs it after the second `overrides.py`. A full rebuild reproduces the fixed layer byte for byte (same md5), and a second run changes nothing.
- **Demoted to needs-teacher** (steps [], summary-only duration). Each gets a tier_reason and a cited warning giving the text's own teacher statement:
  - `inward-turned-gaze-ku-2-1-1` (KU 1.2.8–9). Its stage is now advanced, as data/ tags KU 2.1.1.
  - `anapanasati-first-tetrad` (Vism VIII p.277/2, p.278).
  - `metta-bhavana-vism-9` (Vism IX p.295; III p.89/3, p.97/3, p.98/2). The summary now keeps the "taken the subject" condition.
  - `recalling-the-good-in-one-who-wronged-vism-9` (same cites). W2 (bodily harm) is deleted and cite IX p.300 (hells) dropped.
- **Excluded:** the four `uttama-*-ts-9-6` entries now have user_facing false and manual_exclusion "their only real step rests on the Daśavaikālika 8.36–38 entry, still skeleton". Re-running `overrides.py` leaves them excluded (checked). Their ārta caution now cites TS 9.30, 9.31, 9.32 and 9.33. For śauca, the unsourced "commentaries' reading" is removed from W1 and from the summary.
- **Editorial:**
  - Product notes are out of the warnings. Deleted: pratipakṣa W2 (its note kept in tier_reason) and guarding-the-mind W2. Moved to tier_reason: ekatattva W3, citta W3, vītarāga W1, speech W3, anitya W2, āsrava-saṃvara W2 and seeing-harm W3. Anuprekṣā W2 is removed, since its tier_reason already says the same.
  - Misstated warnings corrected: KU 1.3.14 (the razor's-edge line only), TS 7.11 (the four pairings) and BhG 6.35 (reworded to 6.35–6.36).
  - Steps corrected:
    - YS 1.12 S4 (cite YB 1.11 dropped);
    - ekatattva S2 and S4;
    - yathābhimata S2 (no fixed gaze, nothing craved); W1's inferred clause is dropped and YS 1.15 added to cites;
    - bearing-the-surge S3 (limited to the surge);
    - speech S5 (daily recitation) deleted, with tier_reason updated.
  - Anuprekṣā S3 and summary no longer carry the commentary gloss; W1 cites TS 9.30–9.33 separately.
- **Beyond the judge's list (same rule: a warning is the texts' own caution only):**
  - TS 7.11 W2's clause "the vows themselves are not taken through the product" is moved to tier_reason.
  - Dhp 3–5 W2 (the Vism IX p.298 mettā advice) is removed, following the judge's note to revisit it if mettā is demoted.
  - BhG 6.35 W3 says "can be attained" (6.36 *śakyaḥ*), where the judge's text had "is attained".
- **Checked by code:**
  - Only these 25 entries changed.
  - Every cite in them passes `ontology.citable()`, except the Daśavaikālika skeleton cite in the four excluded entries. Each keeps at least one warning with a citable cite.
  - All 216 cites of the 30 loaded gentle entries are citable.
  - `claims.scan_fields` finds 0 hits, and the clinical-word and danger-word checks are clean.
- **Result:**
  - Usable practices went from 69 to 65, and gentle usable from 38 to 30 (vedic-yogic 13, Buddhist 9, Jain 8).
  - `scripts/check_layers.py`: 84 entries, 65 user-facing, 30 gentle.
  - `pytest`: 299 passed.
- **Open:**
  - The uttama W1 notes ("the steps are recollection ...") still read as product notes. They are not shown now; move them before the entries are re-enabled.
  - Śauca's only method practises contentment, not śauca (judge).
  - 11 entries this pass did not touch (all non-gentle or excluded) have no citable warning, as before.
  - The judge re-checks the entries that failed.
