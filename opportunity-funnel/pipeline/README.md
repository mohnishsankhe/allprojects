# Pipeline: design and command reference

All code for the funnel. The model does judgment; these scripts do everything with a right answer (rule 2).
File formats: `config/formats.md`. Thresholds: `config/kill_rules.yaml`. Ledger: `config/ledger.yaml` (transcribed from `config/ledger.md`).

- Python 3.10+. Dependencies: `requests`, `PyYAML`; tests use `pytest`. Everything else is the standard library.
- Entry point: `python3 pipeline/funnel.py <command> [--run RUN] ...`. It finds the funnel root from its own location, so it works from any working directory. `FUNNEL_ROOT_OVERRIDE` (env) points it at another root (tests).
- `--run` accepts `runs/2026-09-26`, `2026-09-26` or a loop run name. The default is `runs/<today>`.
- Global flag `--dry-run`: count ranges (80–120 rooms, lens balance, 500 records) become warnings, not errors.
- Exit codes: 0 ok; 1 validation errors the model must fix (numbered list, one line each: file, item, fix); 2 missing inputs; 3 blocked (network or key), naming the exact domain or key.
- Every command appends events to `RUN/runlog.jsonl` (`{"ts", "stage", "command", "kind": "ran|count|source|skip|blocked|error|note|cost|check", ...}`) so `runlog` can build `RUNLOG.md`.
- Idempotent: the same inputs give byte-identical outputs (timestamps only in `runlog.jsonl`). Graveyard lines are never duplicated. Randomness is seeded from the run name. JSON is written with `sort_keys=True, indent=2, ensure_ascii=False` and a trailing newline.
- Never print or store API keys. Keys come from environment variables first, then `.env`. Cache keys and cached URLs have keys stripped.
- `FUNNEL_OFFLINE=1` (env) makes every network call fail fast as "blocked" (tests and offline runs).
- Plain English in every message and rendered file.

## Modules

| Module | Job |
|---|---|
| `funnel.py` | CLI. Imports each module in `MODULES` and calls its `register(subparsers)`. A missing module is skipped with a warning. |
| `common.py` | Paths (`FUNNEL_ROOT`, `run_dir()`, `run_date()`), `load_kill_rules()`, `load_ledger()` (parses `config/ledger.yaml`), `load_walls()` (W-IDs from `config/walls.md`), JSON/JSONL I/O, `normalize_ws()`, `record_id()`, slug checks (also refuse path traversal), `check_judgment()`, `check_number()`, `check_price()`, graveyard helpers, `log_event()`, `get_key()`, FX helpers (`load_fx(run)`, `to_usd(amount, currency, fx)`), `ValidationErrors`, `fail(errors, code)`. |
| `anonymize.py` | `anonymize(text, known_names=())`. Idempotent. See Privacy. |
| `netfetch.py` | Polite HTTP (rate limit, cache in `cache/http/`, robots.txt in `cache/robots/`, retries on 429/5xx with `Retry-After`, none on 401/403), `NetworkBlocked(domain)`, `RobotsDisallowed`, `FetchError`, `html_to_text()`, `extract_date()`, offline switch. |
| `records.py` | `store_records()`, `load_records()`, `make_batches()`, command `batches`. |
| `harvest.py` | Command `harvest-search`: web-search results from session transcripts → records. |
| `sources.py` | Commands `fetch <adapter>` and `ingest-inbox` (full-text adapters and chat-export parsers). |
| `quote_check.py` | The quote checker; command `quote-check`. |
| `counts.py` | Label validation, counting, saturation; commands `count`, `saturation`. |
| `prices.py` | Price checker; command `price-check`. |
| `stage1.py` | Command `rooms`. |
| `stage2.py` | Commands `fx`, `mask`. |
| `stage3.py` | Command `pains`. |
| `stage45.py` | Commands `walks`, `pairs`. |
| `stage6.py` | Command `numbers`. |
| `outputs.py` | Commands `redteam`, `audit-packet`, `shortlist`, `review`, `runlog`, `progress`, `status`, `commit-message`, `compare`, `audit-status`. |
| `admin.py` | Commands `init`, `preflight`, `ledger-check`, `loop-init`, `rooms-known`, `graveyard`, `log`, `source-decision`, `robots`, `purge-expired`, `show`, `excerpt`, `listen-status`. |

## Setup and admin commands
- `init`: create `inbox/closed_groups`, `inbox/customers`, `inbox/audit_results`, `runs/`, `cache/`. Print ledger status.
- `ledger-check`: load `config/ledger.yaml`; check required sections, unique ids, wall IDs (W17–W29 in supply), numeric constraints; check that every `text` field appears word for word in `config/ledger.md` (after `normalize_ws`); list every line of `ledger.md` containing `[assumed` (these go to REVIEW). Exit 1 on mismatch.
- `preflight [--network-only]`: create `RUN`; copy `config/*` into `RUN/config_snapshot/`; run the ledger check; report API keys set (names only); probe each domain in the `config/sources.md` table (one light request) and classify reachable / blocked_by_network / error; log `blocked` events; print the exact list of domains to allow.
- `loop-init --room <slug>`: create `runs/<today>-loop-<slug>/`; copy the room's entries from the latest run whose `02_mask.json` kept it; snapshot config. Refuse if no run kept it or it is dead in the graveyard.
- `rooms-known`, `graveyard`, `log --stage N (--error|--note|--cost TEXT) [--review]` (`--review` marks a note for REVIEW.md), `robots URL`, `purge-expired --source S --days N` (by `meta.fetched_at`).
- `source-decision --source NAME --status S --reason TEXT --url URL`: append to the decision log in `config/sources.md`; update the matching table row's Status, Checked and Decision cells without breaking the table.
- `show --room R --ids a,b` (records in full); `show --pain P [--limit 15]` (pain entry, quotes and a sample of member records); `excerpt --room R --id X --start "..." --end "..."` (exact original substring; matching is whitespace-normalized); `listen-status --room R` (records per source, per round, dated/undated).

## Stage 3 collection
### `harvest-search --room R [--transcripts DIR]` (harvest.py)
The only collection path that works when the network blocks direct fetching. The model never types record text; the script reads the search tool's own output from the session transcripts.
1. Read `RUN/03_listen/rooms/R/queries.jsonl` (`{"round", "query", "kind"}`).
2. Scan every `*.jsonl` under the transcripts dir (default `~/.claude/projects/`, recursive; env `FUNNEL_TRANSCRIPTS_DIR` overrides). Recognize a web-search result in either form:
   - a line whose `toolUseResult` is a dict with `query` and `results` (a list whose dict items have `content: [{title, url}, ...]`);
   - a `tool_result` content string that starts with `Web search results for query: "<query>"` followed by `Links: [ ...JSON array... ]` (parse the array with `json.JSONDecoder().raw_decode`).
3. Keep results whose query equals (after `strip()`) a query in `queries.jsonl`. Ignore the tool's written summary entirely.
4. For each link, in order: skip if the title is empty, is a bare domain or URL, or has fewer than 3 words. Otherwise build a record: `source: "websearch"`, `url`, `text: title`, `date` from the URL (`/YYYY/MM/DD/`, `/YYYY/MM/`, `YYYY-MM-DD` in the path) or null, `meta: {kind: "search_title", query, query_kind, round, order: [round, query_index, rank], domain, date_from: "url"|"none"}`.
5. One record per URL per room (the first sighting wins). Store through `records.store_records` (anonymizes first).
6. Print and log: queries matched, queries with no transcript result (listed), links seen, records new, duplicates, skipped junk titles.

### Full-text adapters (sources.py)
`fetch stackexchange|hackernews|reddit|youtube|apple|discourse|web ...` and `ingest-inbox --room R [--customers]` exactly as in the earlier design: official APIs only, `config/sources.md` status must be `allowed`/`allowed-with-limits` (checked within 90 days; for `web`/`discourse` a per-domain decision plus robots.txt allow), missing key → exit 3 naming the env var, `NetworkBlocked` → exit 3 naming the domain, never store author fields, chat exports parsed (WhatsApp iOS/Android, Telegram JSON, CSV, text), anonymized with sender names as `known_names`, never printed.

### `batches --room R [--size 80] [--chars 1500]` (records.py)
Load the room's records. Drop records whose date is older than the lookback; keep undated ones if `include_undated_records` (tag them); drop normalized-text duplicates (keep the first in collection order). Order by `meta.order` when present, else newest first. Assign each record to a batch by its round: batch files are `raw/<room>/_batches/batch_r<round>_<NNN>.md`, so a new round never changes earlier batches. Each record: header `### <record_id> | <source> | <date or undated> | <domain>`, the text (cut at `--chars`, marked `[…cut]`), and `money_hint: yes/no` (regex: currency symbols and codes, amounts, pay/paid/fee/cost/price/refund/₹/lakh/k). Write the manifest `rooms/<room>/batches.json` (batch → record_ids, filter counts). Rerunning deletes stale batch files first.

## Core checks
### Quote checker (quote_check.py)
- `normalize_ws(s)`: Unicode NFC, every whitespace run (Python `\s`) → one space, strip. Nothing else changes: case, punctuation, curly vs straight quotes, dashes all must match.
- A quote **passes** only if its record_id exists among the room's stored records, `normalize_ws(quote)` is a substring of `normalize_ws(record.text)`, and it has at least `quote_min_words` words. A quote may be the whole record (a title).
- If the quote's `url` or `date` differs from the record, the stored values replace them (`citation corrected`).
- `quote_check.csv` columns: `pain_id, record_id, status, reason (ok|record_missing|not_substring|too_short|empty), citation_corrected, url, date, quote`.
- `quote-check --room R` self-checks a room's draft without changing files.

### Counters and saturation (counts.py)
- `count --room R`: inputs `batches.json`, `taxonomy.json`, `labels/*.jsonl`. Errors (exit 1): unknown record_id; a manifest record with no label; conflicting duplicate labels; unknown pain key; more than 2 keys; bad `voice`; non-boolean flags; missing reasoning/confidence. `failed_spend: true` forces `money: true` (noted). Per pain key: member `record_count`, `money_mentions`, `failed_spend_mentions` (sorted ids each), `seller_records`, `media_records`. Totals by voice and by source kind. Writes `counts.json`.
- `saturation --room R [--final --stop-reason saturated|exhausted|max_rounds]`: order labeled records by collection order (`meta.order`, then record_id). Let N = number of records, W = `saturation_window`. If N < W + 1: not evaluable → `saturated: false`. Otherwise compare pains from member records among the first N−W records with those among all N: `new_pains` = keys with member records in the last W but none before; rank = competition rank by (failed_spend, money, record_count) descending; `rank_changes` = keys present in both whose rank differs. `saturated` = no new pains and no rank changes. Append (or, on rerun of the same round, replace) a round entry in `saturation.json` with N, new records this round, new_pains, rank_changes and saturated. With `--final`, record `stop_reason` (it must be `saturated` only if the last entry is saturated). Print a one-line verdict.

## Stage scripts
### `rooms [--merge-parts]` (stage1.py)
Merge `RUN/01_rooms.parts/*.json` (lens and gap parts) into `01_rooms.json`. Validate each room (formats.md; six lenses; `origin`; size tagged; ladder; judgment fields; `venture_overlap` ids exist in the ledger). Geography is never checked against anything. Remove rooms dead in the graveyard (slug or normalized name) unless revived; remove exact duplicates (same slug or normalized name; keep the first by lens order then origin order generated > gap_pass > external) and rooms with `duplicate_of`; list near-duplicates (name token Jaccard ≥ 0.6 or a shared `where` URL). Check 80–120 rooms and at least `min_rooms_per_lens` per lens. Write `01_rooms.json` (with `status`) and `01_rooms.md`.

### `fx` (stage2.py)
Validate `RUN/fx_rates.json` (positive `per_usd`, URL, reasoning) and print the table. Every later stage converts through it; a currency missing from it is an error naming the currency.

### `mask [--merge-parts] [--max-rooms N]` (stage2.py)
Merge `RUN/02_mask.parts/*.json`. Run the price checker on every spend item (offline → `blocked_by_network`, kept as `[measured, page not checked]`). Tests, all must pass:
- **reach:** `kind == warm` with a valid warm id, or `kind == search` with ledger id `s1` and an `evidence_url`;
- **depth:** a valid ledger depth id;
- **spend:** at least one item with URL and `price_text` whose price check is not `not_found`;
- **ladder:** at least `min_ladder_steps` steps in `01_rooms.json`;
- **supply:** `blocked` false;
- **exclusions:** `is_excluded` false.
Rank survivors by ladder steps, verified spend points, spend points, warm before search, then slug; keep `max_rooms` (or `--max-rooms`). Every killed or cut room → graveyard with all failed tests. Record in `02_mask.json`: `reach_kind`, `trust_flag` (search reach and trust needed), `venture_overlap`, `employer_overlap` (warm id `w2`/`w4` or exclusion `x2` mentioned). Fewer than `warn_below_rooms` survivors → a review note listing rooms that failed only on depth and/or supply. Write `02_mask.json` and `02_mask.md`.

### `pains` (stage3.py)
For every room with `pains_draft.json`: join each pain with `counts.json` (missing key → error). Build `pain_id`. Run the quote checker; write `quote_check.csv`. Rules in order: fewer than `min_verified_quotes` verified quotes → drop; money 0 and failed spend 0 and urgency `none` → drop; fewer than `thin_below_records` member records → `[thin]`. Spend check: count distinct domains across `spend_evidence` (a record's domain comes from its URL); fewer than `spend_sources_min` → tag `[spend: 1 source]`. Tag `[titles only]` when all supporting records come from `websearch`, `[undated share: X%]` always. Rank by failed spend, money, urgency order, record count, then pain_id; keep `max_pains_total`; graveyard every drop and cut. Collect `needs_calls` rooms and each room's `saturation.json` verdict. Write `pains.json` and `pains.md`.

### `walks [--check PAIN_ID]` (stage45.py)
For each kept pain: validate `.a.json`, `.b.json` and the merged `<pain-id>.json` (W-IDs exist; `forward_12m` covers every wall in `today`; statuses; judgments). Re-derive the conservative merge from `.a`/`.b`: outcome reached = a OR b; a wall persists only if both say persists (unsure = melts); `walls_both` must only hold walls both put on the path, allowing the comparator's `reconciled_ids`. Reject a merged file that is less conservative than this (exit 1 with the exact field). Kill if the merged outcome is reached today. If every wall in the merged walk melts → `lane_hint: trade`. Render `04_walks/<pain-id>.md` (persona; today table; outcome; 12-month table; where walkers disagreed). Write `04_walks/_stage4.json`. `--check` validates one pain (walker files alone if the merged file is missing) and exits.

### `pairs` (stage45.py)
For each Stage 4 survivor, validate every alternative in `pairs`:
- entry: at least `min_entry_walls` distinct machine walls (W1–W16), all in `walls_both`, adjacent (first-appearance steps span at most `len(entry) + adjacency_slack_steps`);
- hold: one human wall (W17–W29) in `walls_both`, within `adjacency_slack_steps` steps of the entry span, `persists` in the merged `forward_12m`;
- lane: **business** if the hold is valid and `hold_supply_id` is a ledger `can_be` entry with the same wall whose `rooms` include `any` (for `c2` Judgment, only if the room's Stage 2 depth id has strength `strong`); **partner** if the hold is valid and `partner_id` is a ledger `can_rent` entry for that wall, or `partner_kind` is non-empty and the wall is not in the ledger's `cannot` list; **trade** if there is no valid hold and `trade` meets every trade condition; otherwise invalid. A wall in `cannot` can never be a hold. A `lane_hint: trade` pain can only be trade.
Keep the strongest valid alternative (lane order from the kill rules, then `rank`). No valid alternative → kill ("no pair, no clean trade, no plausible partner", listing each alternative's failed checks). Write `05_pairs.json` and `05_pairs.md` (every alternative, which checks passed, which one was kept and why).

### `numbers [--check PAIN_ID]` (stage6.py)
For each Stage 5 survivor, from `06_inputs/<pain-id>.json`, the ledger and `fx_rates.json`. Let `h` = hour value (INR) and `fx(c)` = units of `c` per USD.
Cases: **low** = price.low, conversion.low, minutes_per_reach.high, cash_per_reach.high; **base** = all base; **high** = price.high, conversion.high, minutes_per_reach.low, cash_per_reach.low.
Per case, in the room's currency `c` (founder time valued at `h` converted to `c` via USD):
- `price_total` = price × months (monthly) or price (one-off)
- `reaches_per_sale` = 1 / conversion
- `acq_hours` = reaches_per_sale × minutes_per_reach / 60
- `acq_cash` = reaches_per_sale × cash_per_reach
- `acquisition_cost` = acq_cash + acq_hours × h_c
- `net_cash` = price_total − delivery cash cost − acq_cash
- `founder_hours` = delivery hours + acq_hours
- `usd_per_hour` = (net_cash / founder_hours) / fx(c)
- `cash30` = price if `payment_days_after_sale` ≤ 30 else 0
Also: `horizon_months` = min(boredom, melt) ignoring nulls; `days_to_first_payment` = the three parts summed; `cohort_hours_per_week` = first_cohort × delivery hours / delivery_weeks + first_cohort × acq_hours(base) / (test.days / 7); `guarantee_exposure` (INR) = first_cohort × refund, converted; `anchor_ratio` = base price / anchor amount (both converted to USD).
Numbers work only if, in the **base** case: `usd_per_hour` ≥ h in USD × `min_usd_per_hour_vs_hour_value`; `cash30` ≥ `acquisition_cost`; `days_to_first_payment` ≤ `max_days_to_first_payment` (and ≤ runway × 30 when the ledger has a runway); `cohort_hours_per_week` ≤ the ledger's `hours_per_week.use`; `guarantee_exposure` ≤ the reserve; live delivery fits the evening/weekend window. Otherwise kill (graveyard lists each failed check).
Evidence strength: **strong** if failed spend ≥ 3, member records ≥ 30 and spend sources ≥ 2; **moderate** if (failed spend ≥ 1 or money ≥ 3) and member records ≥ 15; else **weak**.
Rank survivors by opens_ladder (position ≤ `opens_ladder_max_position`), then fewest days to first payment, then highest base `usd_per_hour`, then evidence strength (then failed spend, money, verified quotes, records). Keep `max_survivors`; cut the rest with a graveyard line.
Hypothesis: "At least 1 of {n} {who}, reached {how}, will pay {price} for {offer} within {days} days." (`price` = base price in the room's currency with the USD value in brackets). Kill rule: "Kill it if fewer than 1 of the {n} pays {price} within {days} days of the first message. Decide on day {days}. No extensions."
Write `06_numbers.csv` (one row per pain × case, with status), `06_numbers.md` (per survivor: every number, its formula, its tag, low/base/high side by side, in local currency and USD, and a plain-English reading) and `06_survivors.json`.

### Outputs (outputs.py)
- `redteam`: validate `07_red_team/*.json` (one per survivor; kinds; URLs present on every point) and print a summary. `case_against.json` is then written by a judge (model) and applied by `shortlist`.
- `audit-packet`: `07_audit_packet/AUDIT_PROMPT.md` (self-contained prompt for an outside AI with deep research: the strongest case against each survivor, with sources; four angles; a URL for every claim; "no evidence found" instead of inventing; a fixed output format keyed by pain_id; each survivor's summary embedded) and `evidence.md` (key evidence per survivor).
- `shortlist`: `SHORTLIST.md`, one section per survivor in the final order (after `case_against.json` if present): 1 hypothesis; 2 room, pain, lane, one-liner; 3 evidence (3 verified quotes with links, counts, urgency, who pays, alternatives and prices, tags); 4 walk summary (today, 12 months, persisting walls, walker disagreements); 5 pair (entry and holding walls with names; alternatives considered); 6 numbers table (low/base/high, local and USD); 7 ladder position and time to first payment; 8 crux and test kill rule; 9 open questions and confidence; 10 case against (sources, severity, rank change in one line). With no survivors: say so plainly, then the five closest candidates (latest-stage kills first, then by evidence) and exactly what killed each.
- `review`: `REVIEW.md` with only what needs the founder: 1 every `[assumed]` ledger item and every default or gap the run relied on (ledger gaps, kill-rule defaults used, conservative choices logged as `kind: note` events with `review: true`); 2 three quotes chosen at random (seeded by the run name) from verified quotes of kept pains, with links; 3 the credibility question for each survivor; 4 rooms that need calls; 5 skipped and blocked sources, each with what it would add (from `sources.json` and `config/sources.md`); 6 search-reach rooms whose product needs trust; 7 overlaps with existing ventures or the founder's job.
- `runlog`: `RUNLOG.md` from `runlog.jsonl`: what ran; counts in and out of every stage; records per room and per source; saturation per room; sources used and skipped with reasons; domains to allow; errors; approximate cost (API calls; model cost from `cost` events, `[estimate]`); build and test results (from `kind: check` events).
- `progress`: regenerate the block between `<!-- auto:status -->` and `<!-- /auto:status -->` in `PROGRESS.md` from the run folder (which stages have outputs; per room in Stage 3: rounds, records, saturation verdict, draft and quote-check state). The hand-written parts of the file are left untouched. Safe to run from parallel agents (same inputs, same output).
- `status`, `commit-message` (`funnel: run YYYY-MM-DD: N rooms, M pains, K survivors`), `compare --with latest`, `audit-status`.

## Privacy (anonymize.py)
In order, idempotently: emails → `[email]` (also `name at domain dot com` forms); profile links → `[profile link]` (reddit `/user/` `/u/`, twitter.com / x.com handles, instagram, facebook profiles, linkedin `/in/`, youtube `/@` `/channel/` `/c/` `/user/`, tiktok `/@`, medium `/@`, quora `/profile/`, stackoverflow/stackexchange `/users/`, HN `user?id=`, github.com/<user>, `t.me/<user>`, `wa.me/<number>`); phone numbers → `[phone]` (9–15 digits with `+`, spaces, dashes, dots, brackets; never prices, years, dates, times, percentages, scores, or numbers glued to units); usernames → `[user]` (`u/name`, `/u/name`, `@handle` outside emails); names → `[name]` (honorific + capitalized names; greeting or sign-off + name; `my name is X`; every `known_names` entry). Known limit: names in running text without a cue may survive; logged.

## Tests (`tests/`)
`cd opportunity-funnel && python3 -m pytest -q`. No network (mocked; `FUNNEL_OFFLINE=1`), no writes outside a temp copy (`FUNNEL_ROOT_OVERRIDE`). Cover: quote checker; counters and saturation; batches (lookback, undated, duplicates, rounds, determinism); harvest-search (both transcript forms, query matching, junk titles, URL dates, dedupe, no summary text stored); anonymizer; inbox parsers; ledger-check (text drift detection, assumed items); Stage 1–6 rules, the conservative walk merge, alternative pairs, every Stage 6 formula and kill; outputs; docs–CLI sync (every `funnel <command> --flag` in `.claude/` files exists); and an end-to-end synthetic run through the CLI run twice with byte-identical outputs.
