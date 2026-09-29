# Practice-safety gate (P5): the gentle practices

Judge: onto-judge (claude-opus-5-5), 2026-09-29. Scope: every entry of `insight.ontology.gentle_practices()` (38 entries). Per-entry verdicts, criteria and evidence (file and line, verse quotes): `eval/judge/practice_safety.jsonl`.

**Gate result: FAIL.** 4 entries must be demoted and 4 need a substantive fix. The gate passes only if every entry passes or its fix is purely editorial.

## Counts
- pass 14; fix-needed 20 (16 editorial, 4 substantive); demote 4.
- Checked by code:
  - `claims.scan_fields` on the raw and loaded entries: 0 hits.
  - Cite resolution: 244 cites. 240 are citable (233 text-verified, 7 sourced). Not citable: tea:dasavaikalika-sutra:8.36-38 (skeleton, dropped silently by the loader).
  - Duration: 38/38 are labelled as a product default where the text gives no length.

## Demote to needs-teacher (the text's own statement that a teacher is needed)
- `inward-turned-gaze-ku-2-1-1`: The entry's own warning cites KU 1.2.8-9 ('unless taught by another there is no way to it'). The ontology tags KU 2.1.1 as advanced. The layer already puts the MāU Oṃ entry (same caution) and KU 1.3.13 in needs-teacher.
- `anapanasati-first-tetrad`: Vism VIII p.278 (text-verified) has this subject learned from a teacher in five links, and p.277/2 names the first tetrad as the beginner's subject. The layer excluded breath-counting on the same ground. Exception: if DECISIONS.md rules that only the root sutta counts, keep it gentle, add the p.278 caution with its cite and reword W2.
- `metta-bhavana-vism-9`: Vism IX p.295, which the entry cites, requires that the beginner has 'taken the subject'. Vism III p.89/3, p.97/3 and p.98/2 say the subject is received from a good friend and name loving-kindness. Friendliness stays open to users through YS 1.33 and TS 7.11.
- `recalling-the-good-in-one-who-wronged-vism-9`: It is a step within the same Vism IX mettā development. Also, W2 brings body-cutting and body-parts content into the cautions, and cite p.300 carries 'in a few days he will be filling the eight great hells'.

## Substantive fixes (they block the gate)
- `uttama-ksama`, `uttama-mardava`, `uttama-arjava`, `uttama-sauca` (TS 9.6):
  - S4, the only actionable step, rests only on `tea:dasavaikalika-sutra:8.36-38`, which is skeleton, has no original and is not citable. The step still shows it to the user.
  - The fix: text-verify that teaching, or set `user_facing:false` until it is verified. Also cite TS 9.30, 9.31, 9.32 and 9.33 in place of the skeleton range 9.30-33.
  - For śauca, also delete or source 'the commentaries' reading'.

## Editorial fixes
- **Product notes shown as "The texts' caution:" (`insight/report.py`): move them to tier_reason.**
  - Warnings that are not the texts' own caution: `ekatattva` W3, `citta-contemplation` W3, `vitaraga` W1, `speech` W3, `anupreksa` W2, `anitya` W2, `asrava-samvara` W2, `seeing-harm` W3.
  - Delete outright, because they bring hell or death imagery: `pratipaksa` W2 (YB 2.34 hells) and `guarding-the-mind` W2 (Dhp 41).
- `abhyasa-vairagya-ys-1-12`: S4 carries YS 2.47 (said of posture) over to the mind's effort; reword to 'Return to the effort toward stability, without strain (YS 1.13); keep the posture easy, with effort relaxed (YS 2.47).' Drop cite YB 1.11.
- `ekatattva-abhyasa-ys-1-32`: S2 must bound the open object ('hold it in mind; it is not a fixed gaze and not a mantra'). S4: remove 'Keep the effort light'.
- `yathabhimata-dhyana-ys-1-39`: S2 adds 'not something you crave, and not a fixed gaze at a light or the sun'. W1: drop the inferred last clause.
- `abhyasa-vairagya-bg-6-35` W3: 'over time, not at once' is not in 6.35-6.36. Add the cite BhG 6.25 or reword.
- `bearing-the-surge-bg-5-23` S3: limit 'endure them' to the surge, so that it cannot be read as enduring bodily pain.
- `sreyas-preyas-viveka-ku-1-2-2` W1: KU 1.3.14 does not say 'approaching the excellent ones' (the verified reading is 'having obtained the boons'). Reword it to the razor's-edge line only.
- `maitri-pramoda-karunya-madhyastha-ts-7-11` W1: TS 7.11 gives friendliness toward all beings, and says nothing of argument. Restate the four pairings exactly.
- `anupreksa-ts-9-7`: S3: delete the unverified commentary gloss on otherness. W1: cite TS 9.30, 9.31, 9.32 and 9.33.
- `speech-that-does-not-agitate-bg-17-15` S5: delete the daily 'reciting a text you hold sacred', or make it information only. It widens svādhyāya and sits on the layer's own teacher line for recitation.

## Notes and limits
- Criterion 2 rule applied: a warning passes if it is the texts' caution or condition, correctly given and supported by its displayed cite. A product note fails, because the report prints every warning as the texts' caution.
- `insight/pathway.py` EXCLUDE_IF_NO_DIET does not match 'taste'. `letting-go-of-liking-and-disliking-ts-7-8` (S2 and S3 name taste) survives `continue_no_diet`.
- `not-harbouring-the-grievance-dhp-3-5` W2 points to the Vism mettā method. Revisit it if mettā is demoted.
- Not judged: 5 raw gentle entries that the loader already excludes for uncitable warning cites (`aloka-sanna-dn2-68`, `brahmavihara-bhavana-vism-9`, `six-recollections-vism-7`, `upasamanussati-vism-8`, `tattvartha-sraddhana-ts-1-2`). Re-judge them if they become loadable.
- Could not check: Daśavaikālika wording (no local text); Tattvārtha commentaries (not verified in data/). Readings rest on the ontology's verified originals and paraphrases, not on fresh fetches.
