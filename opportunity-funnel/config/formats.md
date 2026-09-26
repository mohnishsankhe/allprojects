# File formats

Every stage talks to the next through files. This page is the contract.
**M** = the model writes it (judgment). **S** = a script in `pipeline/` writes it (code). Never hand-edit an S file; rerun its script.

All paths are relative to `opportunity-funnel/`. `RUN` means `runs/YYYY-MM-DD/` (a loop run is `runs/YYYY-MM-DD-loop-<room-slug>/`).
Run any script with `python3 pipeline/funnel.py <command>`; it finds the folder by itself, from any working directory.

## Shared rules

- **Judgment objects.** Every object the model writes as a judgment carries `"reasoning"` (one or two sentences) and `"confidence"` (`"high"`, `"moderate"` or `"low"`). The scripts reject files that lack them.
- **Numbers.** Every number the model supplies is an object: `{"value": 120, "tag": "measured", "url": "https://..."}` or `{"value": 120, "tag": "estimate", "reasoning": "..."}`. A `measured` number needs a URL or a list of `record_ids`.
- **Prices.** `{"what": "...", "price_text": "$49/month", "amount": 49, "currency": "USD", "unit": "month", "url": "https://..."}`. `price_text` must be copied exactly as the page shows it. The price checker looks for it on the page.
- **Slugs.** Lowercase letters, digits and hyphens. Room slug example: `us-masters-engineers`. Pain ID = `<room-slug>--<pain-key>`.
- **Walls.** Always IDs `W1`–`W29` from `config/walls.md`.
- **Dates.** `YYYY-MM-DD`.

## Ledger: `config/ledger.md` (M, Stage 0)

Readable prose, plus one fenced `yaml` block that the scripts parse:

```yaml
confirmed: 2026-09-26          # date the founder last confirmed it
currency: INR
reach:                         # rooms I can enter warmly within 14 days
  - id: r1
    name: "..."
    path: "person / group / network that gets me in"
    covers: "which kinds of people this reaches"
depth:                         # domains where I can tell a good answer from a bad one
  - id: d1
    domain: "..."
partners:                      # people who could judge a domain or supply a wall for me
  - id: p1
    kind: "..."
    judges_domains: ["..."]
    supplies_walls: [W18]
supply:
  can_be:                      # human walls I can credibly be today
    - id: s1
      wall: W20
      rooms: [r1, r2]          # reach ids, or [any]
  can_rent:                    # human walls I could rent through a partner
    - id: s2
      wall: W18
      via: p1
constraints:
  hours_per_week: 10
  runway_months: 6
  guarantee_reserve: 50000     # cash I could hold for guarantees/refunds
  hour_value: 1500             # value of one of my hours, in `currency`
geography: [IN]
languages: [en, hi]
exclusions: ["..."]
year_four: ["..."]
```

## Graveyard: `graveyard.md` (S appends; M may add revival notes)

One line per kill:
`- 2026-09-26 | stage 2 | room:us-masters-engineers | no reach entry matches`
To revive an item, add an indented line directly under it:
`  - new evidence 2026-12-01: <what changed, with a URL or record_id>`
The scripts skip dead items unless such a line exists.

## Stage 1

`RUN/01_rooms.json` (M):
```json
{"rooms": [{
  "slug": "us-masters-engineers",
  "name": "Engineers applying for a US master's",
  "lens": "transition",
  "origin": "generated",
  "who": "Final-year and working engineers applying to US MS programs",
  "where": [{"name": "r/gradadmissions", "url": "https://www.reddit.com/r/gradadmissions/"}],
  "who_pays": "The applicant, often with parents' money",
  "size": {"value": 100000, "unit": "applicants per year", "tag": "estimate", "reasoning": "..."},
  "ladder": [
    {"step": 1, "problem": "Exam prep (GRE, IELTS)", "price_text": "...", "url": "..."},
    {"step": 2, "problem": "Shortlisting and applications"}
  ],
  "geography": ["IN"],
  "duplicate_of": null,
  "reasoning": "...", "confidence": "moderate"
}]}
```
`lens`: `life_stage` | `profession` | `transition` | `obligation`. `origin`: `generated` | `external` (from `config/rooms_external.md`).
`python3 pipeline/funnel.py rooms` validates it, removes duplicates and graveyard rooms, and writes `RUN/01_rooms.md`.

## Stage 2

`RUN/02_mask_input.json` (M): one entry per room.
```json
{"rooms": [{
  "slug": "us-masters-engineers",
  "reach":  {"ledger_id": "r1", "reasoning": "...", "confidence": "high"},
  "depth":  {"ledger_id": "d1", "partner_id": null, "reasoning": "...", "confidence": "moderate"},
  "spend":  [{"what": "...", "price_text": "...", "amount": 0, "currency": "INR", "unit": "one-off", "url": "https://..."}],
  "supply": {"blocked": false, "needs": [], "reasoning": "...", "confidence": "moderate"},
  "excluded": {"is_excluded": false, "reasoning": "...", "confidence": "high"}
}]}
```
`reach.ledger_id` must be a reach id from the ledger, or `null`. `depth` needs a depth id or a partner id whose `judges_domains` fits.
`supply.needs` lists what the core pains obviously need that the ledger says the founder lacks: `license`, `physical_work` or `capital`.
Scripts: `price-check --stage 2`, then `mask`. They write `RUN/02_mask.json` and `RUN/02_mask.md`.

## Stage 3

Records (S): `RUN/03_listen/raw/<room>/<source>.jsonl`, one JSON object per line:
```json
{"record_id": "9f2c...", "source": "stackexchange:expatriates", "url": "https://...", "date": "2025-03-14",
 "text": "anonymized text", "meta": {"kind": "question", "title": "...", "room": "..."}}
```
`record_id` = first 16 hex characters of SHA-256 over `url + "\n" + text` (whitespace normalized). Text is anonymized before it is written. Author fields are never stored.

Per room, in `RUN/03_listen/rooms/<room>/`:
- `sources.json` (M): `{"used": [{"source": "...", "query": "...", "records": 0}], "skipped": [{"source": "...", "reason": "..."}], "needs_calls": {"value": false, "reasoning": "...", "confidence": "moderate"}}`. Set `needs_calls` to true when the room is older, offline or businesses, so public text under-represents it.
- `taxonomy.json` (M): `{"pains": [{"key": "visa-slot-panic", "label": "in the room's words", "definition": "..."}]}`.
- `labels/batch_NNN.jsonl` (M): one labels file for each batch file `RUN/03_listen/raw/<room>/_batches/batch_NNN.md`, one line per record: `{"record_id": "...", "pain_keys": ["visa-slot-panic"], "money": true, "failed_spend": false, "reasoning": "...", "confidence": "high"}`. `pain_keys` may be empty (off-topic) or hold up to 2 keys. `money` = mentions money or a price. `failed_spend` = says they paid for something that did not solve the problem. (Batches hold raw text, so they live under `raw/` and are git-ignored. Labels hold no raw text, so they are committed.)
- `counts.json` (S): per pain key, from the labels: `record_count`, `money_mentions`, `failed_spend_mentions` and the record_ids of each.
- `pains_draft.json` (M): one entry per pain key worth keeping:
```json
{"pains": [{
  "pain_key": "visa-slot-panic",
  "description": "in the room's words",
  "urgency": {"type": "deadline_or_rule", "evidence": "...", "record_ids": ["..."], "reasoning": "...", "confidence": "high"},
  "who_pays": {"text": "...", "reasoning": "...", "confidence": "moderate"},
  "alternatives": [{"what": "...", "price_text": "...", "amount": 0, "currency": "...", "unit": "...", "url": "..."}],
  "sellers": [{"name": "...", "url": "...", "complaints": ["..."], "complaint_record_ids": ["..."]}],
  "quotes": [{"record_id": "...", "url": "...", "date": "...", "text": "exact words copied from the record"}]
}]}
```
Global (S): `RUN/03_listen/pains.json`, `RUN/03_listen/pains.md`, `RUN/03_listen/quote_check.csv`, written by `pains`.

## Stages 4 and 5

`RUN/04_walks/<pain-id>.json` (M, one `funnel-walker` per pain):
```json
{"pain_id": "...",
 "persona": {"description": "...", "record_ids": ["..."]},
 "outcome": "the result they want (not the answer)",
 "today": [{"step": 1, "does": "...", "drops_out": false, "why": "...", "walls": ["W1"], "reasoning": "...", "confidence": "moderate"}],
 "outcome_reached_today": {"value": false, "reasoning": "...", "confidence": "high"},
 "forward_12m": [{"wall": "W1", "status": "melts", "reasoning": "...", "confidence": "low"}],
 "pair": {
   "entry_walls": ["W2", "W4", "W9"],
   "hold_wall": "W20",
   "hold_supply_id": "s1",
   "partner_id": null,
   "partner_kind": null,
   "trade": null,
   "one_liner": "For [room], [promise] in [time], because [machine walls], held by [human wall].",
   "crux": "...",
   "credibility_question": "Will this room accept the founder as ...?",
   "ladder_position": 1,
   "reasoning": "...", "confidence": "moderate"
 }}
```
`forward_12m` must list every wall that appears in `today`. `trade`, when used: `{"build_weeks": 1, "payment_upfront": true, "subscription": false, "exit_date": "2027-03-31"}`.
Scripts: `walks` (Stage 4 kills, renders `RUN/04_walks/<pain-id>.md`), then `pairs` (lanes, Stage 5 kills, writes `RUN/05_pairs.json` and `RUN/05_pairs.md`).

## Stage 6

`RUN/06_inputs/<pain-id>.json` (M, one `funnel-walker` in numbers mode per surviving pain):
```json
{"pain_id": "...",
 "price_anchor": {"what": "Private IELTS tutor, 10 hours", "price_text": "...", "amount": 0, "currency": "INR", "unit": "package", "url": "https://...", "reasoning": "...", "confidence": "moderate"},
 "proposed_price": {"amount": 0, "billing": "one_off", "months": 1, "payment_days_after_sale": 0, "reasoning": "...", "confidence": "low"},
 "delivery": {"my_hours_per_customer": {"value": 3, "tag": "estimate", "reasoning": "..."},
              "cash_cost_per_customer": {"value": 0, "tag": "estimate", "reasoning": "..."},
              "delivery_weeks": {"value": 2, "tag": "estimate", "reasoning": "..."}},
 "channel": {"name": "...", "where": "...", "trust": "high", "reasoning": "...", "confidence": "moderate"},
 "acquisition": {
   "touches_per_sale": {"low": 5, "high": 20, "reasoning": "..."},
   "minutes_per_touch": {"low": 5, "high": 15, "reasoning": "..."},
   "cash_per_touch": {"low": 0, "high": 0, "reasoning": "..."}},
 "revenue_horizon": {"boredom_months": {"value": 6, "tag": "estimate", "reasoning": "..."},
                     "melt_months": {"value": null, "tag": "estimate", "reasoning": "hold wall persists"}},
 "ladder_test": {"position": 1, "urgent": true, "provable_outcome": {"value": true, "how": "...", "reasoning": "...", "confidence": "moderate"}},
 "time_to_first_payment": {"days_to_first_conversation": 3, "days_to_close": 7, "build_days": 2, "reasoning": "..."},
 "guarantee": {"offered": false, "refund_per_customer": 0},
 "test": {"n": 20, "who": "room members", "how": "reached how", "offer": "...", "days": 14}}
```
`billing`: `one_off` or `monthly` (`months` = expected months paid). `payment_days_after_sale`: 0 = paid upfront. `trust`: `high` (warm one-to-one), `medium` (teaching content), `low` (cold ads).
The script computes every derived number: delivery cost, margin, acquisition cost range, first-30-day cash, revenue horizon, days to first payment, hours per week for the first cohort, guarantee exposure.
Scripts: `price-check --stage 6`, then `numbers`. They write `RUN/06_numbers.csv`, `RUN/06_numbers.md` and `RUN/06_survivors.json`.

## Stage 7 prep and audit

`audit-packet` (S) writes `RUN/07_audit_packet/AUDIT_PROMPT.md` and `RUN/07_audit_packet/evidence.md`.
After the founder drops the outside auditor's findings in `inbox/audit_results/`, `/funnel-audit` writes
`RUN/07_audit_packet/case_against.json` (M):
```json
{"survivors": [{"pain_id": "...",
  "points": [{"kind": "competitor", "claim": "...", "url": "https://...", "severity": "high"}],
  "new_rank": 1, "rank_change_reason": "one line",
  "reasoning": "...", "confidence": "moderate"}]}
```
`kind`: `competitor` | `failed_attempt` | `not_paid_for` | `legal_or_platform`. Then `shortlist` re-renders `RUN/SHORTLIST.md`.

## Final outputs (S)

`shortlist` writes `RUN/SHORTLIST.md`. `review` writes `RUN/REVIEW.md`. `runlog` writes `RUN/RUNLOG.md` from `RUN/runlog.jsonl`, the event log every script appends to.
