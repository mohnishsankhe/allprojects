# Data model

All data is JSON / JSONL, UTF-8, cross-linked by id. Canonical data lives in `data/`. Subagents never write to `data/`
directly: they write **shards** (`shards/<phase>/<unit>/<entity>.jsonl`), which `scripts/merge.py` validates, de-duplicates
and merges into `data/`. This is what lets dozens of subagents work in parallel without clobbering each other.

```
tradition-ontology/
  CLAUDE.md  PROGRESS.md  RUNLOG.md  DECISIONS.md  GAPS.md  RECONCILE_QUEUE.md  MORNING_REPORT.md
  config/        principles.md  data_model.md  coverage_map.md  registry.md  briefs/*.md
  data/          sources.json lineages.json teachers.json terms.json ultimate.json concepts.json
                 obstacles.json practices.json paths.json phenomenology.json disputes.json
                 borrowings.json timeline.json interpretation_log.jsonl  teachings/<source-slug>.jsonl
  shards/        skeleton/<unit>/*.jsonl   sourcing/<unit>/checks.jsonl   extraction/<source-slug>/...
  scripts/       validate_shard.py merge.py build_atlas.py stats.py
  ATLAS/         INDEX.md + one page per entry
  sources_raw/   downloaded texts (git-ignored, never committed)
```

## 1. Ids

`<prefix>:<slug>`. Prefixes: `src` text · `lin` lineage · `tch` teacher · `tea` teaching · `trm` term · `cpt` concept ·
`prc` practice · `obs` obstacle · `pth` path map · `phn` phenomenology item · `dsp` dispute · `brw` borrowing ·
`ult` a tradition's view of the ultimate.

**Slug rule** (deterministic): take the IAST form, strip diacritics (ś ṣ → s, ṅ ñ ṇ → n, ṭ → t, ḍ → d, ṛ ṝ → r, ḷ → l,
ṃ → m, ḥ → h, long vowels → short), lowercase, every run of non-alphanumerics → `-`. Use IAST spellings, **not**
Anglicised ones: `upanisad` not `upanishad`; `sankara` not `shankara`; `siva` not `shiva`; `krsna` not `krishna`.
Tibetan names: standard phonetics (`longchenpa`, `tsongkhapa`, `lamrim-chenmo`). Chinese/Japanese: pinyin/Hepburn
without tone marks (`huineng`, `linji-lu`, `dogen`, `shobogenzo`). Pali: Pali form (`satipatthana-sutta`).
Disambiguate homonyms by appending the author or tradition: `src:yogasataka-haribhadra`, `src:gorakṣaśataka`→
`src:goraksasataka` (if several texts share the title add `-briggs` / `-nowotny` etc. only when you know the variant).

**Before inventing an id, check `config/registry.md`** — it fixes ids for all lineages, all units, and the most
cross-referenced texts and teachers. Reusing a registry id is mandatory. Referencing an id that another unit owns is
fine and expected (the merge resolves it); if you are unsure whether it exists, still reference it by the slug rule.

Teaching ids: `tea:<source-slug>:<ref>` where `<ref>` is the native locator with dots (`2.47`, `1.2.3`, `mn10`,
`4.3.21`). Ranges use `-` (`2.55-72`). Several teachings from one locator: append `/2`, `/3` (`tea:bhagavad-gita:2.47/2`).

## 2. Common envelope (every entry in every file)

```json
"verification": {
  "level": "skeleton | sourced | text-verified",
  "confidence": "high | moderate | low",
  "unverified": false,
  "checks": []
}
```
- `skeleton` = from model knowledge, unchecked. `sourced` = existence and basic facts (title, author, date, lineage)
  confirmed against an external source (a check entry records how). `text-verified` = extracted from the actual text
  and fidelity-checked.
- `confidence` = how sure the author of the entry is of its content. Be honest: obscure titles, verse numbers,
  teacher lists and dates are where invention happens. Use `low` whenever you are reconstructing rather than recalling.
- `unverified: true` is set by the hallucination sweep when external confirmation failed; the entry is kept and shown
  as `[unverified]`, never deleted.
- `checks[]` items: `{"phase":"C","date":"YYYY-MM-DD","method":"websearch|catalog|text","queries":[],"evidence":[],
  "result":"confirmed|partially-confirmed|not-found|corrected","note":""}`.

Optional on every entry: `"notes": "..."`, `"coverage": ["A6", "D", ...]` (coverage-map section codes it satisfies),
`"recent": true` (post-1800; section H or flagged items), `"restricted": true` (summary-only practice; see §6).
The merge adds `"provenance": {"units": [...], "first_phase": "B"}` — do not write it yourself.

Dates are always given as **two labeled accounts** where both exist:
```json
"dating": {"tradition": {"text": "3102 BCE onward (Kali-yuga reckoning)", "from": -3102, "to": null},
           "scholarly": {"text": "c. 2nd c. BCE – 2nd c. CE", "from": -200, "to": 200},
           "confidence": "moderate"}
```
`from`/`to` are integer years (negative = BCE), or null when unknown. Omit an account you do not know; never invent.

## 3. Files and schemas

Required fields are marked ★. Arrays may be empty. Unknown → omit the field (never fill with guesses).

### sources.json — every text
```json
{"id":"src:bhagavad-gita"★, "title":"Bhagavad Gītā"★, "title_original":"भगवद्गीता", "alt_titles":["Gītā"],
 "language":["Sanskrit"]★, "script":["Devanāgarī"], "family":"vedic|ascetic|shared"★, "lineages":["lin:..."]★,
 "genre":"gītā", "part_of":"src:mahabharata", "location_in_parent":"Bhīṣmaparvan 23–40",
 "commentary_on":"src:...", "authors":[{"teacher":"tch:...","role":"author|compiler|commentator|revealer|translator",
 "attribution":"accepted|traditional|disputed|doubtful"}],
 "attribution":{"tradition":"...","scholarly":"...","confidence":"high|moderate|low|disputed"},
 "dating":{...}, "structure":{"description":"18 chapters, 700 verses","chapters":18,"verses":700},
 "summary":"what the text teaches, 1–4 sentences"★, "key_teachings":["tea:..."],
 "editions":[{"kind":"original|translation","name":"...","licence":"...","url":"..."}],
 "availability":"digitized-original|digitized-translation|manuscript-only|lost|oral|partly-lost|unknown",
 "verification":{...}★}
```

### lineages.json — every lineage / school / order / sampradāya
```json
{"id":"lin:advaita-vedanta"★, "name":"Advaita Vedānta"★, "alt_names":[], "family":"vedic|ascetic|shared"★,
 "parent":"lin:vedanta", "sub_lineages":["lin:..."], "founders":["tch:..."], "key_teachers":["tch:..."],
 "texts":["src:..."], "regions":["..."], "dating":{...}, "status":"living|extinct|revived|absorbed|unknown",
 "transmissions_received":[{"from":"lin:...","what":"...","evidence":"..."}],
 "transmissions_given":[{"to":"lin:...","what":"..."}],
 "distinctive_positions":["..."]★, "ultimate":"ult:...", "path_maps":["pth:..."], "summary":"..."★,
 "verification":{...}★}
```

### teachers.json — every named teacher
```json
{"id":"tch:sankara"★, "name":"Śaṅkara"★, "alt_names":["Ādi Śaṅkarācārya"], "lineages":["lin:..."]★,
 "dating":{...}, "places":["..."], "teachers":["tch:..."], "students":["tch:..."],
 "works":[{"source":"src:...","attribution":"accepted|traditional|disputed|doubtful"}],
 "realization_account":{"text":"...","label":"the tradition's account","sources":["src:..."]},
 "historicity":"historical|semi-legendary|legendary|mythic|unknown", "gender":"male|female|unknown",
 "summary":"..."★, "verification":{...}★}
```

### teachings/<source-slug>.jsonl — THE TEXT LAYER (one line per teaching)
```json
{"id":"tea:bhagavad-gita:2.47"★, "source":"src:bhagavad-gita"★,
 "location":{"ref":"2.47"★,"chapter":"2","verse":"47","section":null},
 "original":{"text":"karmaṇy evādhikāras te mā phaleṣu kadācana ...","script":"IAST","edition":"...","licence":"..."},
 "paraphrase":"faithful paraphrase of what THIS passage says, nothing more"★,
 "speaker":"Kṛṣṇa", "addressee":"Arjuna",
 "tags":{"level":"conventional"★,"standpoint":"seeker"★,"naya":null,"path":["action"]★,"stage":"all"★,"stage_native":null},
 "types":["practice","ethics"]★,
 "terms":["trm:karma"], "concepts":["cpt:..."], "practices":["prc:..."], "obstacles":["obs:..."],
 "paths":["pth:..."], "teachers":["tch:..."], "disputes":["dsp:..."],
 "commentary_on":"tea:...", "differs_from":[{"target":"tea:...","note":"..."}], "cross_refs":["tea:..."],
 "reported_by_opponent":false, "ai_translated":false, "translation_basis":"...",
 "fidelity":{"status":"unchecked|passed|fixed|failed","checked_by":"...","date":"...","note":"..."},
 "extraction":{"method":"skeleton|single|double","extractors":[],"disagreements":[]},
 "correction_log":[], "verification":{...}★}
```
`types` values (the twelve): `ultimate`, `consciousness-mind`, `body-layers`, `practice`, `ethics`, `karma-liberation`,
`world-fate`, `powers-experiences`, `teacher-transmission`, `sound-language`, `death-dying`, `dispute`.
Tag vocabularies for `level`, `standpoint`, `naya`, `path`, `stage`: see `config/principles.md`.
**Skeleton teachings** (from memory) are allowed and useful — the famous verse-anchored teachings — but `original` must
be omitted unless you are certain of the wording, and the `ref` must be marked low confidence if you are not sure of it.

### terms.json — every technical term (glossary)
```json
{"id":"trm:atman"★, "term":"ātman"★, "language":"Sanskrit"★, "native":"आत्मन्", "literal":"self; breath",
 "definitions":[{"lineage":"lin:...","definition":"...","sources":["src:..."],"rests_on":["tea:..."]}]★,
 "cross_language":[{"language":"Pali|Prakrit|Tamil|Tibetan|Chinese|Japanese|Sanskrit|Apabhraṃśa|Hindi|Marathi|Bengali|Kannada",
                    "form":"attā","native":"","grade":"exact|partial|same-under-standpoint","standpoint":"","note":""}],
 "equivalents":[{"target":"trm:purusa","grade":"exact|partial|same-under-standpoint|analogous|contested",
                 "standpoint":"","note":"","rests_on":["tea:..."]}],
 "related":["trm:..."], "concepts":["cpt:..."], "verification":{...}★}
```

### ultimate.json — the one truth
```json
{"node":{"id":"ult:the-one","principle":"ekaṃ sad viprā bahudhā vadanti (Ṛgveda 1.164.46)", "...":"..."},
 "views":[{"id":"ult:advaita-vedanta"★, "lineage":"lin:advaita-vedanta"★, "names":[{"name":"Brahman","term":"trm:brahman"}]★,
   "descriptions":["sat-cit-ānanda ..."], "negations":["neti neti (BĀU 2.3.6)"], "relation_to_self":"...",
   "relation_to_world":"...", "personal_or_impersonal":"personal|impersonal|both|neither|not-posited",
   "tradition_denies_single_ultimate":false, "caveat":"what this tradition would reject in the one-truth reading",
   "rests_on":["tea:..."], "verification":{...}★}]}
```
(Shards write one `views` item per line in `ultimate.jsonl`.)

### concepts.json
```json
{"id":"cpt:five-sheaths"★, "name":"The five sheaths (pañca-kośa)"★,
 "category":"ultimate|consciousness-states|self|mind|body-energy|matter-qualities|obstacles|ethics|karma-rebirth|stages-maps|signs-powers|teacher-transmission|cosmology-time|sound-language|death-dying|disputes"★,
 "names":[{"lineage":"lin:...","name":"pañcakośa","term":"trm:..."}], "definitions":[{"lineage":"lin:...","definition":"...","rests_on":[]}]★,
 "members":["annamaya", "..."],
 "relations":[{"rel":"is-a|part-of|causes|obstructs|leads-to|same-as-under-standpoint|corresponds-to-in-map|contrasts-with|opposes",
               "target":"cpt:...","standpoint":"","note":"","rests_on":["tea:..."]}],
 "verification":{...}★}
```

### obstacles.json / practices.json / paths.json
Common: `id`★, `name`★, `names[]` (per lineage), `lineages[]`★ (lineages that teach it — used for the convergence
count), `sources[]` (`{"source":"src:...","ref":"...","rests_on":["tea:..."]}`), `equivalents[]`
(`{"target":"...","grade":"...","standpoint":"","note":"","rests_on":[]}`), `verification`★.
The merge computes `"convergence":{"count":N,"lineages":[...]}` = number of distinct *independent* lineage roots
teaching it (sub-lineages of one root count once). Do not write `convergence` yourself.

**obstacles**: `category` = `affliction|hindrance|fetter|passion|obstacle|poison|impurity|bond|dosa-imbalance|guna|karma-type|meditation-fault|other`;
`description`★; `antidotes`: `["prc:..."]` and/or text; `members` when it is a list (e.g. the five hindrances).

**practices**: `category` = `posture|breath|lock-seal|cleansing|sense-withdrawal-concentration|meditation|inquiry|mantra-sound|visualization-deity|energy|sleep-dream-death|devotion-service|ethics|mind-training|body-daily-rhythm|ritual`★;
`method_summary`★ (a summary — never step-by-step for restricted practices), `stage`, `prerequisites`, `duration`,
`signs_of_progress`, `warnings[]` (`{"text":"...","source":"src:...","ref":"..."}` — the texts' own warnings),
`sequences` (`["pth:..."]`), `restricted` (true for body-cutting, metals/mercury ingestion, extreme breath retention,
sexual rites, prolonged fasting, and advanced energy practices such as khecarī, vajrolī, dark retreat, tögal).

**paths** (path maps): `lineage`★, `stages[]`★ =
`{"order":1,"name":"yama","gloss":"restraints","description":"...","ref":"YS 2.30","band":"B1"}`.
`band` = the interpretive correspondence band used to align all maps (interpretation layer, cite `rests_on` when you can):
`B0` entry/turning/qualification/faith/refuge/preliminaries · `B1` ethical foundation & purification ·
`B2` preparatory discipline (posture, breath, study, devotional or ritual practice) · `B3` withdrawal & one-pointed
concentration · `B4` absorption with support (jhāna, savikalpa/samprajñāta samādhi, stable calm) · `B5` first direct
seeing / insight / recognition (path of seeing, stream-entry, kenshō, pratyabhijñā, darśana) · `B6` cultivation and
deepening after seeing (path of meditation, higher grounds, one taste, gradual cultivation) · `B7` final liberation
(kaivalya, nirvāṇa, arahatta, kevala-jñāna, mokṣa, buddhahood, non-meditation) · `B8` activity after liberation
(jīvanmukta life, bodhisattva activity, return to the marketplace, dharmamegha as culmination).

### phenomenology.json
```json
{"id":"phn:hyp-nada-four-stages"★, "lineage":"lin:..."★, "source":"src:...", "ref":"...", "stage":"...",
 "kind":"sign|vision|state|difficulty|power|sound|light|bodily"★, "description":"..."★, "rests_on":[], "verification":{...}★}
```

### disputes.json
```json
{"id":"dsp:is-there-a-self"★, "question":"Is there a self?"★, "coverage_ref":"G1",
 "sides":[{"lineage":"lin:nyaya","position":"...","arguments":["..."],"texts":[{"source":"src:...","ref":"..."}],"rests_on":[]}]★,
 "historical_debates":[{"name":"...","date":"...","participants":["tch:..."],"accounts":"...","outcome_by_tradition":"..."}],
 "reconciliation":{"status":"reconciled|partially-reconciled|queued","principles":["P2-standpoint"],"explanation":"one line",
                   "detail":"...","tradition_objections":"...","rests_on":[]},
 "queue_ref":"RQ-...", "verification":{...}★}
```
Record both sides first. Reconcile only where a principle genuinely applies; otherwise `status: "queued"` with
`candidate_readings[]`. Never call anything a contradiction.

### borrowings.json
```json
{"id":"brw:...","from":"lin:...","to":"lin:...","what":"...","direction":"from→to|mutual|disputed","era":"...",
 "evidence":[{"type":"explicit-citation|textual-parallel|shared-vocabulary|tradition-account|scholarly-hypothesis","detail":"...","refs":[]}],
 "verification":{...}}
```

### timeline.json — generated by `scripts/merge.py` from every `dating` field. Do not write by hand.

### interpretation_log.jsonl — one line per interpretive change
```json
{"ts":"...","kind":"equivalence|reconciliation|correspondence|convergence|text-correction|retire|dedupe|upgrade|sourcing-correction",
 "entity":"...","change":"...","reason":"...","principle":"P1-level","rests_on":[],"by":"unit or script"}
```

## 4. Shards (what a subagent writes)

`shards/<phase>/<unit>/<entity>.jsonl` where `<entity>` ∈ `sources lineages teachers teachings terms concepts
ultimate obstacles practices paths phenomenology disputes borrowings interpretation_log`, plus `REPORT.md`
(what was covered, what is uncertain, what is missing). One JSON object per line. Run
`python3 scripts/validate_shard.py shards/<phase>/<unit>` and fix every error before finishing.

Several units may emit the same id (e.g. `tch:sankara` from Advaita and from Yoga). That is expected: the merge unions
list fields, merges per-lineage definitions, keeps the higher-verified scalar value, and logs conflicts. So emit
shared entities with **your lineage's contribution** (your definition, your lineage's view), not a full rewrite.

## 5. Sourcing checks (Phase C) and extraction (Phase D)
- Phase C writes `shards/sourcing/<unit>/checks.jsonl`: `{"id":"src:...","result":"confirmed|partially-confirmed|not-found|corrected",
  "method":"websearch|catalog","queries":[],"evidence":["url or catalog ref"],"corrections":{"field":"value"},"note":""}`.
  The merge upgrades confirmed skeleton entries to `sourced`, sets `unverified:true` on `not-found`, and applies and logs corrections.
- Phase D writes `shards/extraction/<source-slug>/`: `A.jsonl`, `B.jsonl` (independent double extraction),
  `teachings.jsonl` (merged), `disagreements.jsonl`, entity shards, `fidelity.jsonl`, `REPORT.md`. See `config/briefs/extraction.md`.

## 6. Restricted content
For practices that involve cutting the body, ingesting metals or mercury, extreme breath retention, sexual rites, or
prolonged fasting (and advanced energy practices like khecarī, vajrolī, dark retreat, tögal): record only a summary
with the texts' own warnings (`restricted: true`). Never step-by-step instructions, quantities, durations of
retention, or recipes. The traditions' own safety teachings are recorded as teachings.
