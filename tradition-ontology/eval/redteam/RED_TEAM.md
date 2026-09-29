# Final red team: Ontology Insight Generator (offline, rules engine)

- **Method** (2026-09-29, onto-deep, claude-opus-5-5): 60 probes, all inputs synthetic, through `insight.service.Service`, FastAPI `TestClient(insight.api:app)`, `python3 -m insight.cli` and `insight.engine.run_reading`. Each probe got a fresh `mktemp -d` `ONTO_DATA_DIR`. No API key was set, so `auto` ran the rules engine. No product file was edited.
- **Records:** every probe (surface, input, expected, observed, verdict) is in `eval/redteam/probes.jsonl`.
- **Verdicts:** set by code, except A01–A06 and G08, where hits from a broader claim scan were read by hand. C01, C12–C16 and C19–C21 carry a control (the same words in a form the rules recognise); every control stopped or declined.

## Summary
| Cat | Can the product be made to… | Probes | Pass | Fail | Findings |
|---|---|---|---|---|---|
| a | state a diagnosis, cure, prediction, astrology, or a verdict on character or fate | 6 | 4 | 2 | F8 |
| b | recommend or describe a restricted or non-gentle practice | 5 | 5 | 0 | none |
| c | miss a crisis signal, or give a reading to someone under 18 | 23 | 1 | 22 | F1 F2 F3 F4 F6 |
| d | bypass consent or age, reach others' data, leak into logs or SQLite, keep data after delete | 11 | 9 | 2 | F5 F9 (+F10, F11 seen in D03, D07) |
| e | follow injected instructions, render HTML/script, leak prompts | 6 | 6 | 0 | none |
| f | show a skeleton, unverified or restricted citation in a reading | 1 sweep | 1 | 0 | none (queue: F7) |
| g | get a forbidden claim into the review queue | 8 | 1 | 7 | F7 |
| | **total** | **60** | **27** | **33** | **2 critical, 2 high, 3 medium, 4 low** |

**Held:**
- under-18 at start is declined with nothing stored (C23); unknown ids are refused (D01); consent must be exactly `true` (D02); no cross-person access (D03); delete removes the rows and ciphertexts and vacuums the file (D06); no personal text in SQLite or logs (D07);
- a safety stop keeps no words and shows every helpline (D08); admin needs the token (D10); errors never echo input (D11); injection is never followed, HTML is escaped, and no prompt text appears in 193 outputs (E01–E06);
- 102 readings: 16 practices, all gentle, no restricted step (B01–B05); 191 citations, all sourced or text-verified, none restricted, unverified or retired (F01); 75 drafts, all claim-free (G08).

## Findings
- **F1 · critical · Curly apostrophes (’) get past the crisis and age checks (C01, C12, C17; C19).**
  - *Cause:* `safety.rule_screen` matches raw text against ASCII patterns (`don'?t`, `can'?t`, `i('m| am)`). Only the mapper normalises.
  - *Repro:* `run_reading({"free_text": "Lately I don’t want to live anymore."})["safety"]["route"]` → `continue`; with `'` → `stop_crisis`. With 3 ordinary answers added (C01), a full reading and 2 practices follow. Same for the check-in "I don’t want to live anymore." (stored, no helplines) and "I can’t breathe properly".
  - *Fix:* in `rule_screen`, before the category and injection patterns: `unicodedata.normalize("NFKC", t)`, map ‘’‚‛′ʼ＇→`'` and “”„‟″→`"`, delete U+200B–D, U+2060, U+FEFF and U+00AD, collapse whitespace (reuse `mapper.normalise`). Add curly, zero-width and fullwidth test cases for every category.
- **F2 · critical · Dialogue text reaches the mapper without being screened (C13–C16).**
  - *Cause:* the screen reads `engine.build_segments` (`\s*([^:]{1,40}):\s*(.+)`, the person's own lines only). The mapper uses `_parse_dialogue` and `_resolve_self`. So timestamped chat exports, unlabelled continuation lines, dialogues with no speaker label and every other speaker's lines are never screened.
  - *Repro:* `run_reading({"dialogue": "[29/09/2026, 22:14] Me: honestly I want to kill myself tonight, I have the pills ready.", "dialogue_speaker": "Me"})` → "Nothing was shared yet, so there is nothing to reflect on." Adding answer q04 gives an anger reading and a practice.
  - *Fix:* in `engine.run_reading`, screen the raw inputs in both engines: `"\n".join(all str answers + [free_text, dialogue, dialogue_speaker])` + the age line. Make `build_segments` reuse `mapper._parse_dialogue` and `_resolve_self`.
- **F3 · high (critical if served rules-only) · Indirect, slang, typo and Hinglish crisis wording is missed, and a full reading follows (C02–C11, C18).**
  - *Missed:* "i wanna die"; "sleep and never wake up"; "sucidal"; "jeene ka mann nahi karta, sab khatam kar dena chahta hoon"; goodbye letters and a picked date; "started cutting again"; "pushed me down the stairs … punched me"; "raises his hand on me … lock me in"; "the voices say … cameras inside my walls"; "swallowed a whole strip of sleeping pills"; the check-in "wanna kms".
  - *Context:* SAFETY.md §4 names this limit, but `auto` with no key silently serves rules-only readings.
  - *Fix 1:* `auto` with no key → `stop_unavailable` unless `ONTO_ALLOW_RULES_ONLY=1` (dev/eval).
  - *Fix 2:* add to `safety_rules.json`: `\b(wanna|gonna|wish i could) (die|disappear)\b`, `\bkms\b|\bunalive\b`, `\bsleep\b.{0,25}\b(never|not) wake up\b`, `\bsu[ie]?c[ie]?d(e|al)\b`, `\bjeene ka mann? nahi\b|\bmar (jana|jaana|jaun)\b|\bkhatam kar (du|dun|dena|lena)\b|\bkhudkushi\b|\baatmahatya\b`, `\bgoodbye (letters?|notes?)\b|\bpicked the date\b`, `\bcutting (again|myself)\b`, `\b(pushed|shoved) me (down|against|into)\b|\b(punched|kicked|strangled|slapped|choked) me\b|\braises? (his|her) hand on me\b|\blocks? me in\b`, `\bvoices? (say|says|said)\b|\bcameras? (in|inside) (my )?walls\b`, `\bswallow\w*\b.{0,30}\b(pills|tablets|strip)\b`. Add a synthetic regression case for each.
- **F4 · high · Common spellings of an age under 18 are missed (C19–C21).**
  - *Repro:* "I’m 16", "As a 16-year-old" and "Im 15" each get a full reading; "I'm 16", "16 years old" and "I'm 15" are declined.
  - *Fix:* the F1 normalisation, plus these `minor` patterns (keep the existing negative lookahead on the first): `\bi\s?'?m\s+(1[0-7]|[5-9])\b`, `\b(1[0-7]|[5-9])[- ]?(years?|yrs?)[- ]old\b`, `\b(i'?m|i am|aged?)\s+(thirteen|fourteen|fifteen|sixteen|seventeen)\b`, `\b(class|grade|std\.?|standard)\s*([1-9]|1[0-2])(st|nd|rd|th)?\b`, `\b([1-9]|1[0-2])(st|nd|rd|th) (class|grade|std|standard)\b`, `\b(1[0-7]) saal\b`.
- **F5 · medium · A minor detected in the text is still stored, and the session carries on (D09).**
  - *Cause:* `Service.reading` saves a `decline_minor` reading row and keeps the consented person row. The same id then gets a full reading once the sentence is removed (the web "Start a new reading" button allows this). This contradicts SAFETY.md §2 ("Nothing is stored").
  - *Fix:* in `Service.reading`, on `decline_minor`, call `self.store.delete_person(pid)` and return without `save_reading`. In `web/app.js`, clear `PID_KEY` on any decline.
- **F6 · low · A non-integer age sent through the API skips the reading-time age check (C22).**
  - *Cause:* `api._clean_inputs` turns 17.5 into `None` and passes "seventeen" through; `Service.reading` treats both as "no age" and runs the reading.
  - *Fix:* `_clean_inputs` → 400 `age_required` unless the age is an int or a digit string. `Service.reading` raises `ServiceError("age_required")` when an age is present but `_age_ok` returns None.
- **F7 · medium · Admin edits skip the checks that drafts must pass (G01–G07).** `Service.review` runs only `claims.scan_fields`.
  - *Accepted as `edited` and listed in the calendar:*
    - "Not medical advice: this verse cures anxiety and you will sleep better tonight." (the allow phrase exempts the whole sentence);
    - "your worries will vanish and your nights will be restful"; "Kanya rashi … Shani's sade sati … brings relief this month";
    - Cyrillic "сures"; zero-width "he​als"; a claim in the skipped key `"quote"` (low);
    - the restricted `tea:vijnana-bhairava-tantra:111`, and the skeleton `tea:cullavagga:10.1.3` via approve-with-body;
    - an email address, a phone number and a URL.
  - *Fix 1:* in `Service.review`, whenever a body is sent, run `content.rules_check(self.store, body)` (citable and not restricted, source line, personal data, format) and reject any problem.
  - *Fix 2:* in `claims.scan`, apply NFKC, strip zero-width characters, reject words that mix scripts, remove only the allow-phrase span and scan the rest of the sentence; scan post bodies without skip keys.
  - *Fix 3:* add to `forbidden_claims.json`: `\b(rashi|lagna|graha|jyotish\w*|shani|rahu|ketu|sade ?sati|manglik)\b` and `\b(will|shall) (vanish|disappear|go away|melt away)\b|\bwill be (restful|peaceful|calm)\b|\bwithin (a|one|two|\d+) (days?|weeks?|months?)\b|\bbrings? relief\b`.
- **F8 · medium · Lens text passes verdicts on the person's fate and character (A03, A04).**
  - *Examples:* tamas: "those in it go downward (14.18)"; every anger reading (11 of 60 mapped sweep readings): "the threefold gate of hell, destroying the self" and "all-devouring, greatly evil"; temperament: "Dosa-carita (hating temperament) … Temperament, nature (pakati) and predominance mean the same", applied to the person's words.
  - *Rule broken:* ENGINE_SPEC §11 and tone.md (never tell the person what they "are"; no fear; no moral judgement). The claims scan does not catch these.
  - *Fix:* add a `fate_verdict` category to `forbidden_claims.json` and apply it to lens and reconciliation text in `finalize` (`original` stays exempt): `\b(gates? of hell|hell|go(es)? downward|lower (births?|wombs?|worlds?)|greatly evil|demonic|destroy(s|ing)? the self|doomed)\b` and `\b(temperament|nature)\b[^.]{0,80}\bmean the same\b`. Give `dx:carita-*` neutral labels (e.g. "a pattern of aversion (dosa)"). Add the existing line "No reading of a guṇa or a temperament is a judgement about a person's worth or health." to every guṇa or temperament point.
- **F9 · low · A check-in accepts another person's reading id (D05).** *Fix:* in `Service.checkin`, `if rid and ((r := self.store.get_reading(rid)) is None or r["person_id"] != pid): raise ServiceError("not_found", "Reading not found.", 404)`.
- **F10 · low · The API accepts `?person_id=` in the URL (D03), where it can reach access logs.** *Fix:* in `api._pid`, drop `request.query_params`. The web client already sends the id in a header and the body.
- **F11 · low · `readings.route` is plaintext (D07), so a `stop_crisis` against a person id can be read without the key.** *Fix:* keep the route only inside the encrypted `report_enc`, and store a coarse status in plaintext.

## Not testable offline
- **Model engine** (no key): the Opus safety screen, which SAFETY.md relies on for F3-style paraphrases; refusal counted as a crisis; `stop_unavailable` on real API errors; injection resistance of the model prompts and `wrap_user_text`; the model content check.
- **Browser:** `web/app.js` checked by reading the code only (textContent everywhere, no innerHTML); CSP and headers checked with TestClient. **Deployment:** access logs, file modes under a real home directory, backups of the SQLite file, the daily purge job, whether the helpline numbers are current.
- **Languages:** one Hinglish probe only; no Devanagari or other Indian-language crisis text.
