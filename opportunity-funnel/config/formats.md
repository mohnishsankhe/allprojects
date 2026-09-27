# File formats

Every stage talks to the next through files. This page is the contract.
**M** = the model writes it (judgment). **S** = a script in `pipeline/` writes it (code). Never hand-edit an S file; rerun its script.

Paths are relative to `opportunity-funnel/`. `RUN` = `runs/YYYY-MM-DD/` (a loop run is `runs/YYYY-MM-DD-loop-<room-slug>/`).
Run any script with `python3 pipeline/funnel.py <command> --run RUN`; it finds the folder by itself, from any working directory.

## Shared rules
- **Judgment objects** carry `"reasoning"` (one or two sentences) and `"confidence"` (`"high"`, `"moderate"` or `"low"`). Scripts reject files that lack them.
- **Numbers** the model supplies are objects: `{"value": 120, "tag": "measured", "url": "https://..."}` or `{"value": 120, "tag": "estimate", "reasoning": "..."}`. A `measured` number needs a URL or `record_ids`.
- **Prices:** `{"what": "...", "price_text": "$49/month", "amount": 49, "currency": "USD", "unit": "month", "url": "https://...", "seen_via": "page|search"}`. `price_text` is copied exactly as the source shows it. `seen_via: "search"` means the price was read in a web-search result, not on a page the script could open; it is shown as `[measured, page not checked]`. A `seen_via: "page"` price is `[measured]` only when the script opened the page and found the price text; a page the network blocks is also shown as `[measured, page not checked]`, and a page opened without the price as `[not found on page]`. Stage 3 stores the checker's status and tag on each alternative in pains.json.
- **Currencies:** ISO codes (`USD`, `INR`, `AED`, `SGD`...). The script converts to USD with `RUN/fx_rates.json`.
- **Slugs:** lowercase letters, digits, hyphens. Pain ID = `<room-slug>--<pain-key>`.
- **Walls:** IDs `W1`–`W29` from `config/walls.md`.
- **Dates:** `YYYY-MM-DD`.

## Ledger
`config/ledger.md` is the founder's text. `config/ledger.yaml` is its transcription (ids, walls, numbers) and the only ledger file the scripts read. `ledger-check` verifies that every `text` field in the yaml appears word for word in `ledger.md`, and lists every `[assumed]` item for REVIEW.

## Graveyard: `graveyard.md` (S appends; M may add revival notes)
`- 2026-09-26 | stage 2 | room:us-masters-engineers | no reach entry matches`
Revive with an indented line directly under it: `  - new evidence 2026-12-01: <what changed, with a URL or record_id>`.
A revival note revives only the line it sits under: a later kill line for the same item kills it again unless a new note is written under that later line. A stage's lines dated on the run's own date always say what its latest run killed, so a rerun that keeps an item removes its earlier same-date line; `rooms` and `pains` ignore lines dated on the run's own date (this run's later kills), so reruns are idempotent.

## FX rates: `RUN/fx_rates.json` (M, before Stage 2)
```json
{"base": "USD", "as_of": "2026-09-26",
 "rates": {"INR": {"per_usd": 88.1, "url": "https://...", "seen_via": "search", "reasoning": "...", "confidence": "moderate"}}}
```
`per_usd` = units of that currency per 1 US dollar. `USD` is implicit (1.0).

## Stage 1
`RUN/01_rooms.parts/<lens>.json` and `RUN/01_rooms.parts/gap_<lens>.json` (M), merged by `rooms --merge-parts` into `RUN/01_rooms.json`:
```json
{"rooms": [{
  "slug": "gre-engineers-india",
  "name": "Indian engineers preparing for the GRE",
  "lens": "transition",
  "origin": "generated",
  "who": "...",
  "where": [{"name": "r/GRE", "url": "https://www.reddit.com/r/GRE/"}],
  "who_pays": "...",
  "size": {"value": 100000, "unit": "test takers per year", "tag": "estimate", "reasoning": "..."},
  "ladder": [{"step": 1, "problem": "GRE prep", "price_text": "...", "url": "..."}, {"step": 2, "problem": "..."}],
  "geography": ["IN"],
  "venture_overlap": ["v1"],
  "duplicate_of": null,
  "reasoning": "...", "confidence": "moderate"
}]}
```
`lens`: `life_stage` | `profession` | `transition` | `obligation` | `business_type` | `identity_community`. `origin`: `generated` | `gap_pass` | `external`. `geography` is descriptive only (ISO country codes or `GLOBAL`); it never filters. `venture_overlap` lists ledger venture ids the room touches.

## Stage 2
`RUN/02_mask.parts/<n>.json` (M), merged by `mask --merge-parts` into `RUN/02_mask_input.json`:
```json
{"rooms": [{
  "slug": "...",
  "reach": {"kind": "warm", "ledger_id": "w1", "evidence_url": null, "reasoning": "...", "confidence": "high"},
  "depth": {"ledger_id": "d1", "reasoning": "...", "confidence": "high"},
  "spend": [{"what": "...", "price_text": "...", "amount": 0, "currency": "INR", "unit": "one-off", "url": "https://...", "seen_via": "search"}],
  "supply": {"blocked": false, "needs": [], "reasoning": "...", "confidence": "moderate"},
  "excluded": {"is_excluded": false, "exclusion_id": null, "reasoning": "...", "confidence": "high"},
  "trust_needed": {"value": true, "reasoning": "...", "confidence": "moderate"}
}]}
```
- `reach.kind`: `warm` (then `ledger_id` is a warm id `w1`–`w5`), `search` (then `ledger_id` is `s1` and `evidence_url` shows people in this room buying this kind of product through search, an app store or a public marketplace), or `null`.
- `depth.ledger_id`: a ledger depth id, or `null`.
- `supply.needs`: what the room's core pains obviously need that the ledger says the founder lacks and cannot rent: `license_not_rentable`, `large_capital`, `ritual`, `licensed_advocacy`.
- `trust_needed`: does the likely product need trust? Search reach plus trust needed is flagged in REVIEW (search reach suits self-serve products).
Scripts write `RUN/02_mask.json` and `RUN/02_mask.md`.

## Stage 3
Records (S): `RUN/03_listen/raw/<room>/<source>.jsonl`, one per line:
```json
{"record_id": "9f2c...", "source": "websearch", "url": "https://...", "date": null,
 "text": "anonymized text", "meta": {"kind": "search_title", "query": "...", "domain": "reddit.com", "date_from": "url|page|api|none"}}
```
`record_id` = first 16 hex characters of SHA-256 over `url + "\n" + text` (whitespace normalized). An inbox message's URL is `inbox://<kind>/<room>/file_<12 hex>#<fragment>` (a content-free file label; the label → file map lives in the gitignored `RUN/03_listen/raw/<room>/_inbox_index.json`).

Per room, in `RUN/03_listen/rooms/<room>/`:
- `queries.jsonl` (M): one line per web search the harvesters ran: `{"round": 1, "query": "...", "kind": "forum|video|reviews|qa|blog|pricing|jobs|official|phrasing"}`. `harvest-search` matches these queries against the session transcripts and stores their results as records.
- `sources.json` (M): `{"used": [...], "skipped": [{"source": "...", "reason": "...", "would_add": "..."}], "needs_calls": {"value": false, "reasoning": "...", "confidence": "moderate"}}`.
- `taxonomy.json` (M): `{"pains": [{"key": "...", "label": "in the room's words", "definition": "...", "added_round": 1}]}`.
- `labels/batch_NNN.jsonl` (M), one per batch file `RUN/03_listen/raw/<room>/_batches/batch_NNN.md`:
  `{"record_id": "...", "voice": "member", "pain_keys": ["..."], "money": true, "failed_spend": false, "reasoning": "...", "confidence": "high"}`.
  `voice`: `member` | `seller` | `media` | `other`. `pain_keys`: 0–2 keys. `money` = mentions money or a price. `failed_spend` = the writer paid for something that did not solve the problem.
- `counts.json` (S): per pain key: member `record_count`, `money_mentions`, `failed_spend_mentions` (with record_ids), plus `seller_records` and `media_records`.
- `saturation.json` (S): per round: records in, new pains in the last window, rank changes in the last window, `saturated` true/false, and why the room stopped (`saturated`, `exhausted`, `max_rounds`).
- `pains_draft.json` (M):
```json
{"pains": [{
  "pain_key": "...",
  "description": "in the room's words",
  "urgency": {"type": "deadline_or_rule", "evidence": "...", "record_ids": ["..."], "reasoning": "...", "confidence": "high"},
  "who_pays": {"text": "...", "reasoning": "...", "confidence": "moderate"},
  "alternatives": [{"what": "...", "price_text": "...", "amount": 0, "currency": "...", "unit": "...", "url": "...", "seen_via": "search"}],
  "sellers": [{"name": "...", "url": "...", "complaints": ["..."], "complaint_record_ids": ["..."]}],
  "spend_evidence": [{"kind": "record", "record_id": "..."}, {"kind": "price", "url": "https://..."}, {"kind": "job_posting", "record_id": "..."}],
  "ladder_position": 1,
  "quotes": [{"record_id": "...", "url": "...", "date": null, "text": "exact words copied from the record"}]
}]}
```
The script checks that `spend_evidence` spans at least `spend_sources_min` distinct domains; otherwise the pain is tagged `[spend: N source(s)]` with the real count (`[spend: 1 source]`, `[spend: 0 sources]`). quote_check.csv reason values: ok, record_missing, not_substring, too_short, empty, duplicate (the same words, or a part of them, already quoted from the same record; one piece of evidence counts once).
Global (S): `RUN/03_listen/pains.json`, `pains.md`, `quote_check.csv`.

## Stage 4 (two walkers and a comparator per pain)
- `RUN/04_walks/<pain-id>.a.json` and `.b.json` (M, one independent `funnel-walker` each, mode `walk`):
```json
{"pain_id": "...", "walker": "a",
 "persona": {"description": "...", "record_ids": ["..."]},
 "outcome": "the result they want (not the answer)",
 "today": [{"step": 1, "does": "...", "drops_out": false, "why": "...", "walls": ["W1"], "reasoning": "...", "confidence": "moderate"}],
 "outcome_reached_today": {"value": false, "reasoning": "...", "confidence": "high"},
 "forward_12m": [{"wall": "W1", "status": "melts", "reasoning": "...", "confidence": "low"}]}
```
- `RUN/04_walks/<pain-id>.json` (M, the comparator, mode `compare`): the merged walk in the same shape, plus:
```json
{"agreement": {"outcome": "agree|disagree", "walls_both": ["W2", "W4"], "walls_one": ["W9"], "reconciled_ids": [{"a": "W10", "b": "W9", "as": "W9", "reasoning": "..."}]},
 "disagreements": ["one line each"],
 "pairs": [ PAIR, PAIR, PAIR ]}
```
`forward_12m` must list exactly the walls on that file's today path; `agreement.walls_one` must list exactly the walls only one walker met; a kept pain's comparator file must hold 2 to 3 alternative pairs (`funnel walks --check` and `funnel pairs` reject it otherwise). Walkers check their own file with `funnel walks --check <pain_id> --walker <a|b>`.
The merge must follow the conservative rule: outcome reached if either walker says so; a wall `persists` only if both say `persists`; a wall is in `walls_both` only if both walkers put it (or a reconciled equivalent) on the path. `walks` re-derives these from the `.a`/`.b` files and rejects a merged file that is less conservative.

## Stage 5: pairs (inside the comparator's file)
Each `PAIR`:
```json
{"rank": 1,
 "entry_walls": ["W2", "W4", "W9"], "hold_wall": "W20",
 "hold_supply_id": "c1", "partner_id": null, "partner_kind": null,
 "trade": null,
 "one_liner": "For [room], [promise] in [time], because [machine walls], held by [human wall].",
 "crux": "...", "credibility_question": "Will this room accept the founder as ...?",
 "reasoning": "...", "confidence": "moderate"}
```
`hold_supply_id` = a ledger `supply.can_be` id; `partner_id` = a ledger `supply.can_rent` id. `trade`: `{"build_weeks": 1, "payment_upfront": true, "subscription": false, "exit_date": "2027-03-31"}`.
`pairs` validates every alternative mechanically and keeps the strongest valid one (lane order from the kill rules, then the comparator's `rank`). Writes `RUN/05_pairs.json` and `RUN/05_pairs.md`.

## Stage 6
`RUN/06_inputs/<pain-id>.json` (M, a `funnel-walker` in mode `numbers`):
```json
{"pain_id": "...", "currency": "INR",
 "price_anchor": {"what": "Private GRE tutor, 20 hours", "price_text": "...", "amount": 0, "currency": "INR", "unit": "package", "url": "https://...", "seen_via": "search", "reasoning": "...", "confidence": "moderate"},
 "offer": "one line: what the customer gets",
 "price": {"low": 0, "base": 0, "high": 0, "billing": "one_off", "months": 1, "payment_days_after_sale": 0, "reasoning": "..."},
 "conversion_rate": {"low": 0.02, "base": 0.05, "high": 0.10, "reasoning": "share of people reached who buy"},
 "acquisition": {"minutes_per_reach": {"low": 2, "base": 5, "high": 10, "reasoning": "..."},
                 "cash_per_reach": {"low": 0, "base": 0, "high": 0, "reasoning": "..."}},
 "delivery": {"my_hours_per_customer": {"value": 3, "tag": "estimate", "reasoning": "..."},
              "cash_cost_per_customer": {"value": 0, "tag": "estimate", "reasoning": "..."},
              "delivery_weeks": {"value": 2, "tag": "estimate", "reasoning": "..."},
              "live": {"value": true, "fits_evenings_weekends_ist": true, "reasoning": "..."}},
 "channel": {"name": "...", "where": "...", "reach_kind": "warm", "trust": "high", "reasoning": "...", "confidence": "moderate"},
 "revenue_horizon": {"boredom_months": {"value": 6, "tag": "estimate", "reasoning": "..."},
                     "melt_months": {"value": null, "tag": "estimate", "reasoning": "hold wall persists"}},
 "ladder_test": {"position": 1, "urgent": true, "provable_outcome": {"value": true, "how": "...", "reasoning": "...", "confidence": "moderate"}},
 "time_to_first_payment": {"days_to_first_conversation": 3, "days_to_close": 7, "build_days": 2, "reasoning": "..."},
 "guarantee": {"offered": false, "refund_per_customer": 0},
 "test": {"n": 20, "who": "room members", "how": "reached how", "days": 14},
 "open_questions": ["..."], "confidence": "moderate"}
```
Cases: `low` = low price, low conversion, high acquisition cost; `base` = base values; `high` = high price, high conversion, low acquisition cost.
The script computes everything else (see `pipeline/README.md`), in the room's currency and in USD, and writes `RUN/06_numbers.csv`, `RUN/06_numbers.md` and `RUN/06_survivors.json`.

## Red team and audit
- `RUN/07_red_team/<pain-id>.json` (M, a fresh subagent per survivor that has not seen earlier reasoning):
```json
{"pain_id": "...",
 "points": [{"kind": "competitor", "claim": "...", "url": "https://...", "severity": "high", "reasoning": "..."}],
 "verdict": {"new_rank_hint": "keep|down|kill", "reasoning": "...", "confidence": "moderate"}}
```
`kind`: `competitor` | `failed_attempt` | `not_paid_for` | `legal_or_platform`. `redteam` writes `RUN/07_red_team/_redteam.json`; `compare` writes `RUN/compare.json`. case_against.json points may carry `origin` (`red_team` | `outside_audit`), shown in the shortlist as e.g. `competitor (high; red_team)`.
- `RUN/07_audit_packet/case_against.json` (M, written after reading the red-team files or, later, `inbox/audit_results/`): `{"survivors": [{"pain_id": "...", "points": [...], "new_rank": 1, "rank_change_reason": "one line", "reasoning": "...", "confidence": "moderate"}]}`. `new_rank: null` kills the survivor (graveyard).
- `audit-packet` (S) writes `RUN/07_audit_packet/AUDIT_PROMPT.md` and `evidence.md`.

## Final outputs (S)
`shortlist` → `RUN/SHORTLIST.md`; `review` → `RUN/REVIEW.md`; `runlog` → `RUN/RUNLOG.md` (from `RUN/runlog.jsonl`).
