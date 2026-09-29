# Evaluation sets (synthetic only)

- **Author.** The evaluation analyst (onto-analyst) writes these sets in P5.
- **Builders.** Builder agents never read this folder (brief, section 7).
- **Data.** No personal data is used; every persona is synthetic.
- **Files:**
  - `personas.jsonl`: 30 synthetic personas;
  - `safety.jsonl`: 12 safety cases;
  - `adversarial.jsonl`: 10 adversarial cases.
- **Case shape:** `{"id", "inputs": {"age", "answers": {qid: text}, "free_text", "dialogue", "dialogue_speaker"}, "expected": {"route", "must_show": [...], "must_not": [regex...]}, "attack"?}`.
- **Outputs:** `scripts/run_eval.py` writes to `results/<engine>/`, and the judge packets go to `judge/<engine>/`.
