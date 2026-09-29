# Product layers — schema (read-only to the app)

These layers are built from the ontology (data/) for the Insight Generator. The app reads them; it never writes them.
Every `cites` item is a teaching id (`tea:<slug>:<ref>`). The build check (`scripts/check_layers.py`) enforces:
- every cited teaching resolves in data/;
- every cited teaching is `sourced` or `text-verified`. An entry that cites a skeleton teaching is excluded from
  user-facing use until it is verified; it stays in the file with `"user_facing": false`.

## layers/diagnosis.json — list of objects
```
{ "id": "dx:<slug>",                       # e.g. dx:klesa-raga, dx:nivarana-thina-middha, dx:kasaya-krodha
  "name": "Rāga (attachment)",
  "kind": "affliction|hindrance|fetter|passion|guna|mind-activity|sheath|vital-current|state-of-consciousness|obstacle|state|temperament",
  "group": "the five kleśas (YS 2.3)",      # the list it belongs to, as the text gives it
  "lens": "vedic-yogic|ascetic-buddhist|ascetic-jain",
  "ontology_refs": ["obs:…","cpt:…","trm:…"],
  "definitions": [ {"tradition": "lin:…", "text": "…", "cites": ["tea:…"]} ],
  "markers": [ {"marker": "how it shows itself, as the text describes it (plain words)",
                "cues": ["short phrases a person might use that would fit this description"],
                "cites": ["tea:…"]} ],
  "states": [ {"name": "prasupta (dormant)", "text": "…", "cites": ["tea:yoga-sutra:2.4"]} ],   # optional
  "equivalences": [ {"id": "dx:…", "grade": "exact|partial|same-under-standpoint", "note": "…", "cites": ["tea:…"]} ],
  "paired_practices": [ {"practice": "px:…", "cites": ["tea:…"]} ],
  "not_to_be_read_as": "a plain statement of what this is NOT (never a diagnosis or a medical condition)",
  "user_facing": true }
```
Markers come from the texts' own descriptions (e.g. YS 1.31 on the companions of distraction; the Pali similes for the
hindrances; the Visuddhimagga's temperaments), never from modern psychology. Cues are plain-language paraphrases of
those descriptions, used only to help the mapper notice them. A cue never licenses a mapping on its own: the mapper
must still quote the person's words and cite the entry.

## layers/practices.json — list of objects
```
{ "id": "px:<slug>", "name": "…", "lens": "…", "ontology_refs": ["prc:…"], "tradition": "lin:…",
  "summary": "what the practice is, as the text states it (for gentle-tier practices, enough to do it)",
  "steps": ["…"],                         # gentle tier only; others get [] (summary only)
  "targets": ["dx:…"], "stage": "beginner|intermediate|advanced|all",
  "duration": {"minutes_per_session": [5, 10], "sessions_per_day": 1,
               "basis": "product default for a beginner; the text gives no length" | "text: …"},
  "warnings": [ {"text": "…", "cites": ["tea:…"]} ],   # the texts' own warnings, verbatim or closely paraphrased
  "safety_tier": "gentle|needs-teacher|never-recommend",
  "tier_reason": "…",
  "cites": ["tea:…"],
  "user_facing": true }
```
Only `gentle` practices can ever be recommended. Anything involving breath retention, forceful breathing, fasting, diet
rules, bodily cleansing (ṣaṭkarma), sexual practices, metals or mercury, cutting, inversions or strong postures, or
visualisation of death or decay is never gentle. Such practices are `needs-teacher` or `never-recommend`, with the
reason given.

## layers/tables/*.json
- `one_truth.json`: the one-truth table. Rows pair each lineage's name for the ultimate with its standpoint, what it
  denies, and the reconciliation principle (P1–P8) that relates it to the others, with citations. RV 1.164.46 is the
  first principle.
- `path_map_correspondence.json`: stages of the main path maps aligned by band (B0–B8), with citations and the
  traditions' own objections to alignment.
- `obstacle_correspondence.json`: rows of corresponding obstacles across the lenses (e.g. rāga ↔ kāmacchanda ↔ lobha),
  graded exact / partial / same-under-standpoint, with what differs, citations, and the principle used.
