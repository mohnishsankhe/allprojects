# Brief: fidelity check of the ontology layer (quality gate)

You are an independent checker. You did not write any of this. Your job is to find where the layer says more, less or
other than the passages it cites. Follow `CLAUDE.md` in `tradition-ontology/` and read `ontology_layer/SCHEMA.md`.

## Input
`ontology_layer/_inputs/JUDGE_SAMPLE.jsonl`: one entry per line (a why or a result), with its `cited_passages`
(id, verification level, paraphrase) attached. The sample is stratified by unit and basis.

## For each entry, decide one verdict
- `pass`: the statement says what the cited passages say. Plain-English rewording is fine.
- `overreach`: it adds a cause, effect, step, benefit, duration or condition the passages do not state.
- `misread`: it reverses, distorts or confuses what the passages say (wrong subject, wrong direction, wrong term).
- `wrong-cite`: the cited passages do not contain the claim at all (it may be true elsewhere).
- `wrong-link` (results only): the `rests_on` why does not explain how the result works.
- `wrong-layer`: the engine-layer tags are clearly wrong by SCHEMA.md's table (e.g. a centre tagged as a cause, L3 used
  for a mood, W combined with another tag).
- `restricted-breach`: a restricted practice is given with steps, counts or durations, or without `restricted: true`.
- `modern`: it imports modern psychology, medicine or science, or makes a health claim of its own.
For `outline` entries (no passage cited), judge only whether the claim is a fair statement of the named text at the
`ref_hint` given, from your own knowledge, and say how sure you are.

## Output
Write `ontology_layer/_inputs/JUDGE_VERDICTS.jsonl`: `{"id", "verdict", "reason", "fix"}` per entry. `reason` is one
sentence quoting the words at issue. `fix` is the corrected statement (or corrected tags), or empty for `pass`.
Write only that file. Do not edit the layer. Your final message: the counts per verdict, and the three patterns of
error you saw most, in at most eight lines.
