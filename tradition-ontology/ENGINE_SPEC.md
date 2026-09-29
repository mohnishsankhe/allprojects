# Ontology Insight Generator — engine specification (v1)

This is the design contract for the product. The rule files it points to (`rules/`) are the detail, and the code follows
them. When the code and this file disagree, the code is wrong. The ontology (`data/`, `layers/`) is read-only to the app.

## 1. What the product does, and what it never does
- **Person map.** A person answers up to 15 plain questions, writes freely, or pastes a dialogue. The engine:
  - finds the patterns the traditional texts describe in the person's own words;
  - reads them through two lenses, Vedic/yogic and ascetic (Buddhist and Jain);
  - shows where the two readings agree and where they differ, under the one-truth principle (`config/principles.md`);
  - suggests a short, gentle practice pathway drawn only from the texts;
  - produces a report in Markdown and HTML.
- **Content engine.** It drafts posts per audience bucket and account voice that connect an everyday problem to a cited
  teaching. Every draft goes to a human review queue. Nothing is ever posted by the app.
- **Never:**
  - modern research, psychology or science;
  - diagnosis, cure, treatment or health claims;
  - predictions, astrology or kundali;
  - content from skeleton (unchecked) ontology entries;
  - a recommendation of a restricted practice;
  - a reading for anyone under 18, or without consent.

## 2. Pipeline (person map)
```
consent + age gate ─► intake (build own-words units) ─► SAFETY SCREEN ─┬─ stop_crisis / decline_minor / stop_unavailable → stop message, nothing else
                                                                      └─ continue (+ notes) ─► reading gate (≥25 own words)
      ─► mapper (rules | model | merged; validators V1–V13) ─► synthesizer (two lenses + reconciliation)
      ─► pathway (rules first; model may only reword "why") ─► finalize (specificity, claims scan, citation resolution)
      ─► report object ─► Markdown / HTML ─► encrypted store
```
- Code: `insight/engine.py` `run_reading()`. Every step records its model cost in a `Ledger`.
- A model failure never raises to the user:
  - a failed **safety** model call fails closed with `stop_unavailable`;
  - any other failed step falls back to the rules engine for that step and adds a notice.

## 3. Engines and model routing
- `ONTO_ENGINE`:
  - `rules`: deterministic and offline;
  - `model`: Claude API;
  - `auto`: model if `ANTHROPIC_API_KEY` is set, else rules.
- Every engine passes the **same validators**.
- `config/model_routing.json` sets the model and effort per step:

  | Step | Model | Effort |
  |---|---|---|
  | safety screen | Opus 5.5 | high |
  | intake parsing and candidate mapping | Sonnet 5.5 | high |
  | synthesis and report | Opus 5.5 | high (xhigh as a premium setting) |
  | pathway | rules first, then Sonnet 5.5 | high |
  | content drafts | Sonnet 5.5 | medium |
  | content check | Opus 5.5 | high |

- Every call:
  - structured JSON output (`output_config.format`) and explicit `output_config.effort`;
  - timeout 90 s, 3 SDK retries with backoff, and server-side fallbacks (beta header in `model_routing.json`);
  - refusal and truncation are errors.
- The API base URL comes only from `ONTO_ANTHROPIC_BASE_URL` (default `https://api.anthropic.com`), never from the
  environment of a host tool.
- **Code decides; the model proposes.** A model never sets confidence, citations, the safety tier, the practice
  choice or the route. Its output is data that the validators accept or drop.

## 4. Inputs and intake
- **Intake:** `rules/intake.json` holds at most 15 questions. Each has an id, the plain question, its purpose (what it
  lets the texts' markers notice), `optional: true`, and whether its answer is evidence. Only free-text answers are
  evidence. Scale or option picks are never quoted as the person's words.
- **Free text:** paragraphs over 120 words are split into chunks of 60+ words, and at most 3 free-text units count per entry.
- **Dialogue:** the person names their own speaker label, and only those lines are evidence. The other lines are context only.
  With no speaker label, the dialogue is not used and nothing is guessed from content.
- **Collect only what the reading needs:** answers, age (a number, 18 or over), and a consent timestamp. No name, email,
  location or date of birth. Details the person volunteers anyway (email, phone, URL) are never quoted (V4).
- **Injection:** all user text is wrapped as `<user_input>` data with angle brackets neutralised. Instructions inside it are
  ignored, and injection sentences are excluded from evidence. Requests for a diagnosis, a prediction or a horoscope get
  the standing notice and are not answered.

## 5. Safety screen (runs first, always)
- **Files:** `rules/safety_rules.json` (regex screen, precedence) and `rules/safety_messages.json` (wording and resources).
  Code: `insight/safety.py`.
- **Rules first.** An under-18 signal declines before any model call. The model screen (model engine only) can **add** flags,
  never remove them. A refusal from the screen counts as a crisis flag.
- **Routes, in precedence:**
  - `decline_minor`;
  - `stop_crisis` (suicidal thoughts, self-harm, abuse, psychosis signs, medical emergency). It stops the reading and shows warm
    words plus Tele-MANAS 14416, 988, Samaritans 116 123 and findahelpline.com;
  - `stop_unavailable` (the model screen failed in model mode);
  - `continue_no_diet` (disordered eating). No guidance on diet, fasting or exercise. Practices whose steps or warnings
    touch food or exercise are excluded, and food sentences are never evidence;
  - `continue_medical_note` (a medical condition). The note reads "This is not medical advice; continue your
    treatment". The condition is never interpreted, and the flagged sentences are never evidence;
  - `continue`.

## 6. Mapping
- **Files:** `rules/mapping_rules.json` (machine) and `rules/MAPPING_RULES.md` (human). Code: `insight/mapper.py`. Summary:
  - **Evidence** is an exact substring of the person's own words: 3–35 words, one sentence, sliced from the source by code.
    Exclusions run in a fixed order, each with a reason code: hypothetical; someone else as subject or
    attribution; sarcasm; past and resolved; negation; generic; clinical words; body and health.
  - **Strength:** direct 1.0, indirect 0.6, suggestive 0.3, lowered by caps.
  - **Confidence:** `E_net = E − 0.5·C`. Map only if E_net ≥ 1.0 AND (a direct, specific quote OR 2+ units).
    Moderate is ≥ 1.6 with 2+ units; high is ≥ 2.2 with direct items in 2+ units and C = 0. The numbers are audit only and never shown.
  - **Kinds:** sheath, vital-current and state-of-consciousness are never mapped, and neither is the denylist
    (attainments, what is true of everyone not yet free, bodily entries). Guṇa and temperament top out at moderate.
    Of the YS 2.4 states, only `udāra` may be attached.
  - **Limits per reading:** at most 5 equivalence groups and 8 entries.
- **Rules engine.** It matches the cues of the diagnosis layer's markers (`layers/diagnosis.json`): exact cue, cue window,
  partial or one-stem. Cues only help noticing; the marker, which carries the texts' description and citations, is what is
  matched. The rules engine has no blind recheck, so its indirect items come only from partial lexical matches.
- **Model engine** (candidate step). The model proposes candidates (entry, marker, exact quotes, rationale). Anything
  weaker than direct goes to a blind recheck, then to the same validators. **Merged** pools both engines.
- **Mapping record** as the report shows it:
  - `dx_id`, `name`, `kind`, `lens`, `lens_label`, `group_id`, `confidence`;
  - `evidence[{qid, unit, quote, strength, specificity, engines}]`, `counter_evidence[…]`;
  - `why` (the rationale: ≤ 45 words, no clinical, modern, diagnostic, predictive, universal or certainty words);
  - `cites` (copied by code from the markers used), `state` (null or udāra), `audit` (never rendered).

## 7. Two-lens synthesis and reconciliation
- **Files:** `rules/synthesis_rules.json` plus the tables in `layers/tables/` (one-truth, path-map correspondence, obstacle
  correspondence). Code: `insight/synthesizer.py`.
- **Lenses.** The *Vedic/yogic* lens reads the mapped vedic-yogic entries; the *ascetic* lens reads the Buddhist and Jain
  entries. A lens also reads an entry of the other lens **through the equivalence table**, but only where the diagnosis
  layer lists an equivalence with a cited note. Evidence never transfers: the point states the equivalence and its grade,
  and quotes the words that mapped the original entry.
- **Every lens point** is one or two plain sentences with `cites` (the entry's definition or marker citations) and
  `evidence_refs` (qids of this person's quotes). A point without evidence is dropped (specificity rule).
- **Both lenses, always.** If only one lens has a direct mapping, the other lens speaks through a cited equivalence. If
  there is none, the report says plainly that this lens's texts, as held in the ontology, describe it differently or not
  at all. It never pads.
- **Reconciliation** (one-truth principle, principles.md). Each point names its basis, one of:
  - *level*: the same pattern described at a different depth (e.g. kleśa as root, hindrance as what blocks the settling mind);
  - *standpoint*: the same experience, with a different account of who or what undergoes it (self vs. no-self vs. jīva);
  - *path*: the same obstacle met at a different place on each tradition's path map;
  - *stage*: the practice that answers it belongs to a different stage in each tradition.
  Each point cites both sides. In v1, the rules engine takes reconciliation points only from user-facing rows of
  `obstacle_correspondence.json`. All of those rows are related under P2-standpoint, so a v1 reading's basis is
  standpoint, and each point says the match is partial, not an identity. The model engine may use level, path or
  stage only with cites from the packet. Rows whose shared word has different senses are held out
  (`rules/synthesis_rules.json`).
- **Differences** are stated plainly, never smoothed over: different accounts of bondage, of the self, of what liberation is.
  An `exact` equivalence is never claimed where the table grades it `partial`.
- **Model synthesis** (optional). The model writes the lens points from a packet of mapped entries, definitions,
  equivalences and quotes. Each point must carry `cites` from the packet and `evidence_refs` from the quotes; anything
  else is dropped. The rules template is the fallback.

## 8. Pathway
- **Code:** `insight/pathway.py`.
- **Choice.** 2–4 practices, chosen **only** from the gentle tier of `layers/practices.json`: those that target a mapped
  entry or are paired with it, ranked by confidence, with one of each lens where possible.
- **Excluded:**
  - needs-teacher and never-recommend practices;
  - restricted practices;
  - practices whose warnings have lost a citation;
  - under no-diet, anything touching food or exercise.
- **Each practice shows** why it was chosen (quoting the person), the steps, the length (product default where the text
  gives none, labelled), the texts' warnings verbatim with citations, and its citations.
- **14-day sequence.** Start with one practice, add one on days 4, 8 and 11, and keep sessions short in week 1.
- **Daily check-in prompt.** The model may only reword "why", and only if the new wording quotes the person and passes the
  claims scan.

## 9. Specificity (the anti-horoscope rule)
Every insight must depend on something **this** person said. The rules and the tests that enforce it:
- **Evidence references.** Every insight (lens point, reconciliation point, pathway "why") carries ≥ 1 `evidence_refs`
  to a kept quote of this person, or it is removed (`rules/specificity.json`).
- **Generic statements.** Wording that would fit anyone ("everyone feels…", "in today's world…", "you are on a
  journey") is removed.
- **Mapping specificity.** A mapping needs a quote with a frequency, detail or consequence feature, or evidence from 2+ units (§6).
- **Swap test** (evaluation). A judge shows report A's insights beside person B's input. At least 90% of the insights must
  stop fitting.

## 10. Finalize (the last line of defence, every reading)
In order:
1. specificity filter;
2. claims scan on every free-text field (sentences with a forbidden claim are removed);
3. every `cites` list reduced to citable ids (sourced or text-verified, not restricted, not unverified);
4. citations resolved into `citations{id: {title, ref, original, paraphrase, level}}`;
5. `claim_hits` recorded for audit. They must be empty; the evaluation fails any report with a hit.

## 11. Tone
- **Guide:** `rules/tone.md`. Plain, warm, exact.
- **Language:** short sentences and everyday words. Sanskrit, Pali or Prakrit terms appear once, with the plain meaning
  beside them.
- **Standing:** the person is never told what they "are". The report says what they wrote and what the texts say about
  patterns like it.
- **Never:** hype, promises, "you will", fear, flattery, or moral judgement.
- **Standing notice** at the top of every report: not a diagnosis, not medical or psychological advice, no predictions.

## 12. Report object
```
{engine, created, safety{route, categories, model_checked, injection}, notices[], stopped? | insufficient?,
 summary, mappings[§6], groups[], lenses{vedic{points[]}, ascetic{points[]}},
 reconciliation{points[{text, basis, cites, evidence_refs}], differences[{text, cites, evidence_refs}]},
 pathway{practices[], sequence[14], checkin_prompt, tier_rule}, citations{}, claim_hits[], cost{}}
```
- The schema lives in `insight/schemas.py`, and the tests validate every report against it.
- The renderer (`insight/report.py`) adds only fixed headings and the standing notice.

## 13. Data, privacy and cost
- **Consent** (`rules/consent.json`) is recorded with its version before any processing. Adults only: under 18 declines.
- **Storage.** Personal data (inputs, reports, check-ins) is encrypted at rest with Fernet in SQLite. The key comes from
  `ONTO_DATA_KEY` or a 0600 key file.
- **Retention and deletion.** Retention is 90 days by default (`ONTO_RETENTION_DAYS`), enforced by `purge_expired()`.
  The person can view, export and delete their data; delete removes all rows and vacuums.
- **Logs** hold ids, routes, step names, costs and error kinds only, never text. Posts and evaluations never use personal data.
- **Cost.** Every model call's tokens and cost go to the ledger and to the `costs` table. The admin view sums them by step.
  `COSTS.md` reports measured numbers from real runs only.

## 14. Content engine (see `rules/content/`)
- **Buckets:**
  - work pressure and burnout;
  - anxiety and overthinking;
  - sleep;
  - loneliness;
  - meaning and identity.
  Each bucket's account has its own voice guide (`rules/voices/<bucket>.md`).
- **Formats:** X post, X thread, Instagram carousel script, short-video script, long-video outline (`rules/content/formats.json`).
- **Idea.** Each post "connects the unrelated": an everyday scene from the bucket, joined to one cited teaching (a verse
  or passage that is sourced or text-verified). The link must be the teaching's own point, not a stretch.
- **Pipeline:**
  - Pick a teaching from the bucket's allowed pool (`rules/content/buckets.json`), never a restricted one.
  - Draft (Sonnet, medium; or the rules template offline).
  - Check (Opus, high; or the rules checks offline): citation faithful, claims scan clean, not a near-duplicate
    (character 5-gram Jaccard < 0.5 against every queued or approved post, and the same teaching at most once per account
    in 30 days), idea-specific (the scene and the teaching both named).
  - Only then does the draft join the review queue (`pending`). A human approves, edits or rejects.
  - The app has no posting API.
- **Platform rules.** Each account publishes its own original material. There is no cross-account amplification. Each
  platform's AI-content policy is followed, and AI-assisted media is labelled where required (the queue shows a label
  reminder per format).
- **Calendar.** 30 days per bucket, drawn from the approved and pending queue. It is a plan, not a schedule the app executes.

## 15. Interfaces
- **Web** (FastAPI, `insight/api.py`, one page `web/index.html`): consent and age gate, intake, reading, report, check-in,
  my data (view, export, delete), review queue, admin costs.
- **CLI** (`python -m insight.cli`): the same actions.
- **Admin routes** need `ONTO_ADMIN_TOKEN`. Person routes use an opaque person id held by the client.

## 16. Evaluation hooks
- `eval/` holds the synthetic sets: 30 personas, 12 safety cases, 10 adversarial cases. They are written only by the
  evaluation analyst and never read by builders.
- `scripts/run_eval.py` runs the sets through the chosen engine and stores every report.
- The judge scores each gate from the stored outputs.
- A gate that needs live model calls is reported **not run** when no API key is present.
