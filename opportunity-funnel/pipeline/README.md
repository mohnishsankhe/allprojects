# Pipeline: design and command reference

All code for the funnel. The model does judgment; these scripts do everything with a right answer (rule 2).
File formats are in `config/formats.md`. Kill rules are in `config/kill_rules.yaml`.

- Python 3.10+. Dependencies: `requests`, `PyYAML` (see `requirements.txt`); tests use `pytest`. Everything else is the standard library.
- Entry point: `python3 pipeline/funnel.py <command> [--run RUN] ...`. It finds the funnel root from its own location (`Path(__file__).resolve().parent.parent`), so it works from any working directory.
- `--run` accepts `runs/2026-09-26`, `2026-09-26` or a loop run name. The default is `runs/<today>`.
- Global flag `--dry-run`: count ranges (40–60 rooms, lens balance) become warnings, not errors. Used for one-room dry runs.
- Exit codes: 0 ok; 1 validation errors the model must fix (printed as a numbered list, one line each, saying file, item and fix); 2 missing inputs; 3 blocked (network or key), with the exact domain or key name.
- Every command appends events to `RUN/runlog.jsonl` (`{"ts", "stage", "command", "kind": "ran|count|source|skip|blocked|error|note|cost", ...}`) so `runlog` can build `RUNLOG.md`.
- Idempotent: rerunning a command with the same inputs gives byte-identical outputs (timestamps only in `runlog.jsonl`). Graveyard lines are never duplicated. Randomness is seeded from the run name.
- Never print or store API keys. Keys come from environment variables first, then `.env`. Cache keys and cached URLs must have keys stripped.
- Plain English in every message and rendered file.

## Modules

| Module | Job |
|---|---|
| `funnel.py` | CLI. Imports each module in `MODULES` and calls its `register(subparsers)`. A missing module is skipped with a warning, so modules can be built separately. |
| `common.py` | Paths (`FUNNEL_ROOT`, `run_dir()`), config loading (`load_kill_rules()`, `load_ledger()` which parses the fenced yaml block in `config/ledger.md`, `load_walls()` which parses W-IDs from `config/walls.md`), JSON/JSONL read/write (sorted keys, UTF-8, trailing newline), `normalize_ws()`, `record_id()`, slug checks, judgment validation (`check_judgment(obj, where)` → list of errors), number and price validation, graveyard read/append, runlog events, env/key loading, `ValidationErrors` exception. |
| `anonymize.py` | `anonymize(text, known_names=())` → text. Idempotent. See Privacy below. |
| `netfetch.py` | Polite HTTP: per-host rate limit, disk cache in `cache/http/`, robots.txt check (cache in `cache/robots/`), retries on 429/5xx honoring `Retry-After`, no retry on 401/403, `NetworkBlocked(domain)` when the egress proxy refuses the tunnel, `RobotsDisallowed`, `FetchError`. User agent: `OpportunityFunnel/0.1 (market research; low rate)`. `html_to_text()` with the stdlib `html.parser` (drops script, style, nav, header, footer, forms). `extract_date()` from meta tags, JSON-LD `datePublished` and `<time datetime>`. |
| `records.py` | `store_records(run, room, source, iterable)`: anonymize, compute record_id, drop empty, dedupe against the file, append to `RUN/03_listen/raw/<room>/<source-file>.jsonl`. `load_records(run, room)`. `make_batches(...)`. |
| `sources.py` | Source adapters and `ingest-inbox` (chat export parsers). Each adapter first checks `config/sources.md` (API sources: status `allowed` or `allowed-with-limits`, checked within 90 days; web and Discourse: a logged decision for that domain plus robots.txt). |
| `quote_check.py` | The quote checker (rule 1). |
| `counts.py` | Label validation and counting. |
| `prices.py` | Price checker: is the cited price really on the cited page? |
| `stage1.py` | `rooms` |
| `stage2.py` | `mask` |
| `stage3.py` | `pains` |
| `stage45.py` | `walks`, `pairs` |
| `stage6.py` | `numbers` |
| `outputs.py` | `audit-packet`, `shortlist`, `review`, `runlog`, `status`, `commit-message`, `compare`, `audit-status` |
| `admin.py` | `init`, `preflight`, `ledger-check`, `loop-init`, `rooms-known`, `graveyard`, `log`, `source-decision`, `robots`, `purge-expired`, `show`, `excerpt`, `listen-status` |

## Commands

### Setup and admin
- `init`: create `inbox/closed_groups`, `inbox/customers`, `inbox/audit_results`, `runs/`, `cache/`. Report ledger status and age.
- `ledger-check`: parse the ledger yaml block. Check the required keys, unique ids, walls W17–W29 in supply, supply `rooms` that name existing reach ids or `any`, `via` pointing to partner ids, numeric constraints, currency. Warn if `confirmed` is empty or older than 90 days.
- `preflight [--network-only]`: create `RUN`, copy `config/*` to `RUN/config_snapshot/`, run `ledger-check` (exit 2 if there's no ledger or it's unconfirmed), report which API keys are set (names only), and probe each source domain in `config/sources.md` (one light request each). Classify each as reachable, blocked by network policy or error. Log blocked domains as `kind: blocked` events and print the exact list to allow.
- `loop-init --room <slug>`: create `runs/<today>-loop-<slug>/`. Copy the room's entry from the latest run whose `02_mask.json` kept it into `01_rooms.json` and `02_mask.json` (marked `copied_from`). Snapshot config. Refuse (exit 2) if no run kept the room, or if it is in the graveyard with no revival line.
- `rooms-known`: list rooms kept by any run, with the run date.
- `graveyard`: print dead items (with revival status).
- `log --stage N (--error TEXT | --note TEXT | --cost TEXT)`: append a manual event.
- `source-decision --source NAME --status allowed|allowed-with-limits|skip --reason TEXT --url URL`: append `- YYYY-MM-DD | NAME | status | reason | URL` to the decision log in `config/sources.md`. If NAME matches a table row, update that row's Status, Checked and Decision cells. If NAME looks like a domain, the decision covers that domain for `web`/`discourse`.
- `robots URL`: print allowed/disallowed for our user agent.
- `purge-expired --source youtube --days 30`: delete raw records of that source older than N days by fetch time (for sources whose terms limit storage).
- `show --room R --ids a,b` prints records in full. `show --pain P [--limit 15]` prints the pain entry from `pains.json` plus its quotes and a sample of supporting records.
- `excerpt --room R --id X --start "first words" --end "last words"`: print the exact original substring from the first match of `start` to the end of the next match of `end`. Matching is whitespace-normalized; the output is the original stored characters.
- `listen-status --room R`: records per source, date range, undated count.

### Stage 3 collection (in `sources.py`)
- `fetch stackexchange --room R --site S --query Q [--tagged T] [--max N] [--answers]`: API 2.3 `/search/advanced` with `filter=withbody`, `fromdate` = run date minus lookback, paging, honoring `backoff` and `quota_remaining`. One record per question: `title + "\n\n" + body text`; with `--answers`, also one record per answer. URL = question or answer link. Optional key `STACKEXCHANGE_KEY`.
- `fetch hackernews --room R --query Q [--max N]`: Algolia `search_by_date`, `tags=(story,comment)`, `numericFilters=created_at_i>X`. URL = `https://news.ycombinator.com/item?id=<id>`.
- `fetch reddit --room R --subreddit S [--query Q] [--max N]`: official OAuth (client credentials) with `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`, `REDDIT_USER_AGENT`; at most 60 requests per minute. Posts (title + selftext) and top-level comments. URL = `https://www.reddit.com` + permalink. Exit 3 if keys are missing.
- `fetch youtube --room R (--video ID_OR_URL ... | --search Q --videos K) [--max N]`: Data API v3 `commentThreads.list` (`textFormat=plainText`); `search.list` costs 100 quota units, so it is used sparingly. URL = `https://www.youtube.com/watch?v=<id>&lc=<commentId>`. `meta.fetched_at` supports `purge-expired`. Exit 3 without `YOUTUBE_API_KEY`.
- `fetch apple --room R --app ID --country CC [--max N]`: `https://itunes.apple.com/<cc>/rss/customerreviews/page=<p>/id=<id>/sortby=mostrecent/json`, pages 1–10. URL = `https://apps.apple.com/<cc>/app/id<id>?see-all=reviews`; the review id goes in meta.
- `fetch discourse --room R --forum BASE --query Q [--max N]`: `/search.json`, then `/t/<id>.json`. One record per post. URL = `BASE/t/<slug>/<id>/<post_number>`. Never store `username`, `name` or `avatar` fields.
- `fetch web --room R --url URL`: one public page as one record (text capped at 20,000 characters), date from `extract_date()` or null.
- `ingest-inbox --room R [--customers]`: read `inbox/closed_groups/R/` (or `inbox/customers/R/`), parse, anonymize, store. Source = `inbox:closed_groups` or `inbox:customers`. Never print raw text.
  - WhatsApp `.txt`, both iOS `[dd/mm/yyyy, hh:mm:ss] Name: msg` and Android `dd/mm/yyyy, hh:mm - Name: msg`; multi-line messages continue until the next header. Day/month order is detected per file (a first field > 12 means day-first, a second field > 12 means month-first; otherwise day-first) and logged.
  - Telegram `result.json` (`messages[]`, `text` as a string or a list of entities).
  - `.csv` with `date` and `text` columns; `.txt`/`.md` otherwise, one record per paragraph, undated.
  - Drop system lines (encryption notice, `<Media omitted>`, joined, left, added, deleted). Drop messages under 3 words.
  - Sender names are never stored. All sender names from the file (full names and each name part of 3 or more letters) are passed to `anonymize()` as `known_names`.
  - URL = `inbox://<closed_groups|customers>/<room>/<file>#<line or msg id>`.
- `batches --room R [--size 60] [--chars 1500]`: load the room's records; drop records older than the lookback (from the run date) and undated ones (unless `include_undated_records`); drop normalized-text duplicates (keep the earliest); cap at `max_records_per_room` by round-robin across sources, newest first. Write `_batches/batch_NNN.md` under `raw/<room>/`: for each record a header `### <record_id> | <source> | <date>` then the text (cut at `--chars`, marked `[…cut]`) and a `money_hint: yes/no` line from a regex (currency symbols, codes, amounts, pay/paid/fee/cost/price/refund). Write `rooms/<room>/batches.json`: the batch → record_ids manifest and the filter counts (in, too old, undated, duplicates, capped, out).

### Stage 3 analysis
- `count --room R`: see counts.py below.
- `quote-check [--room R]`: check the quotes in `pains_draft.json` for one room (self-check, prints pass/fail per quote) without changing files.
- `pains`: see stage3.py below.

## The two core checks

### Quote checker (`quote_check.py`)
- `normalize_ws(s)`: Unicode NFC, then every run of whitespace (Python `\s`, which includes non-breaking and thin spaces) becomes one space, then strip. Nothing else changes: case, punctuation, curly vs straight quotes and dashes all must match exactly.
- A quote **passes** only if: its record_id exists among the stored records of that room; `normalize_ws(quote.text)` is a substring of `normalize_ws(record.text)`; and it has at least `quote_min_words` words.
- If the quote's `url` or `date` differs from the stored record, the checker replaces them with the stored values and notes `citation corrected`. The record is the source of truth.
- Output rows for `quote_check.csv`: `pain_id, record_id, status (pass|fail), reason (ok|record_missing|not_substring|too_short|empty), citation_corrected (yes|no), url, date, quote`.
- `apply(pains)`: delete failed quotes, keep at most `quotes_per_pain_max` passing ones (in the model's order), and report which pains have fewer than `min_verified_quotes`.

### Counters (`counts.py`)
- Inputs: `rooms/<room>/batches.json` (the record_ids that went to labeling), `taxonomy.json`, `labels/batch_*.jsonl`.
- Errors (exit 1): label for an unknown record_id; record in the manifest with no label; the same record labeled twice with different content; unknown pain key; more than 2 pain keys; `money` or `failed_spend` not boolean; missing `reasoning` or `confidence`. `failed_spend: true` with `money: false` is corrected to `money: true`, since paying is a money mention, and noted.
- For each pain key: `record_count`, `money_mentions`, `failed_spend_mentions` and the sorted record_ids behind each. A record with two keys counts once for each key.
- Totals: records labeled, off-topic (no key), per source.
- Writes `rooms/<room>/counts.json` and prints a table.

## Stage scripts

### `rooms` (stage1.py)
`--merge-parts` first concatenates `RUN/01_rooms.parts/*.json` into `01_rooms.json`. Then it validates every room (formats.md Stage 1; geography codes inside the ledger's `geography`; size tagged; judgment fields). It removes rooms dead in the graveyard (matched by slug or normalized name) unless revived, removes exact duplicates (same slug or same normalized name) and rooms with `duplicate_of`. It lists near-duplicates (name token Jaccard ≥ 0.6, or a shared `where` URL) without removing them. It checks 40–60 rooms and at least `min_rooms_per_lens` per lens. It writes `01_rooms.json` (normalized, `status` per room) and `01_rooms.md`.

### `mask` (stage2.py)
`--merge-parts` first concatenates `RUN/02_mask.parts/*.json`. It runs the price checker on every spend item. For each room it applies the five tests: reach (valid ledger reach id), depth (valid depth id, or a partner id whose `judges_domains` is non-empty), spend (at least one item with URL and `price_text` whose price check is not `not_found`), ladder (at least `min_ladder_steps` steps), supply (`blocked` is false), plus exclusions (`is_excluded` false). Survivors are ranked by ladder steps, verified spend points, spend points, then slug. It keeps `max_rooms` (or `--max-rooms`). Every killed or cut room goes to the graveyard with all its failed tests. If fewer than `warn_below_rooms` survive, it records a review note listing rooms that failed only on depth and/or supply. It writes `02_mask.json` and `02_mask.md` (a table of rooms × tests).

### `price-check --stage 2|3|6` (prices.py)
For each cited price (Stage 2 spend, Stage 3 alternatives, Stage 6 anchors) it fetches the URL through `netfetch` (cached, robots-checked) and looks for `price_text` in the page text (whitespace-normalized, case-insensitive), then for the amount in common formats (`15000`, `15,000`, `15 000`, `1,50,000`, with or without decimals). Status: `verified` | `amount_found` | `not_found` | `unreachable` | `blocked_by_network` | `robots_disallowed`. It writes or updates `RUN/price_check.csv` (key: stage, item, url). Tags used downstream: `verified`/`amount_found` → `[measured]`; `unreachable`/`blocked_by_network`/`robots_disallowed` → `[measured, page not checked: <status>]`; `not_found` → the claim is not counted as measured and shows as `[not found on cited page]`.

### `pains` (stage3.py)
For every room with `pains_draft.json`: join each drafted pain with its counts (a pain key with no counts is an error). Build `pain_id`. Run the quote checker and write `quote_check.csv`. Apply Stage 3 rules in this order: fewer than `min_verified_quotes` verified quotes → drop; money 0 and failed spend 0 and urgency `none` → drop; fewer than `thin_below_records` records → tag `[thin]`. Rank the rest by failed spend, money mentions, urgency (order from the kill rules), record count, then pain_id. Keep `max_pains_total`. Everything dropped or cut gets a graveyard line. A pain with fewer than `quotes_per_pain_min` verified quotes is flagged, not dropped. Alternatives are tagged via `price_check.csv`. `needs_calls` rooms are collected for REVIEW. Writes `pains.json` (kept and dropped, with `status`, `drop_reason`, `rank`, `tags`) and `pains.md`.

### `walks` (stage45.py)
`--check P` validates one walk file and exits (used by the walker). Without `--check`, for each kept pain: validate `04_walks/<pain_id>.json` (all W-IDs exist; `forward_12m` covers every wall in `today`; valid statuses; judgments complete). A missing or invalid walk is an error (the pain is marked `error`, not killed). `outcome_reached_today.value == true` → kill ("their own AI already gets them to the outcome today"). `unsure` counts as `melts`. If every wall melts → `lane_hint: trade`. Render `04_walks/<pain_id>.md`. Write `04_walks/_stage4.json`.

### `pairs` (stage45.py)
For each Stage 4 survivor, check the pair mechanically:
- entry: at least `min_entry_walls` distinct machine walls (W1–W16), all on the `today` path, adjacent (the steps where they first appear span at most `len(entry) + adjacency_slack_steps` steps);
- hold: one human wall (W17–W29) on the path, within `adjacency_slack_steps` steps of the entry span, with `forward_12m` status `persists`.
Lane, in this order:
- **business** if the hold is valid and `hold_supply_id` names a ledger `supply.can_be` entry with the same wall whose `rooms` include the room's reach id (from `02_mask.json`) or `any`;
- **partner** if the hold is valid and there is a `partner_id` (a ledger partner that supplies the wall, or a `can_rent` entry for the wall) or a non-empty `partner_kind`;
- **trade** if there is no valid hold and `trade` meets every trade condition (build weeks ≤ max, payment upfront, no subscription, a valid exit date);
- otherwise **kill** ("no pair, no clean trade, no plausible partner", listing the failed checks).
A Stage 4 `lane_hint: trade` pain can only be trade or killed. Writes `05_pairs.json` and `05_pairs.md`.

### `numbers` (stage6.py)
`--check P` validates one inputs file and exits. Otherwise, for each Stage 5 survivor, compute from `06_inputs/<pain_id>.json` and the ledger (hour value `h`, currency):
- `price_total` = amount × months (monthly) or amount (one-off)
- `delivery_cost` = my_hours × h + cash_cost
- `margin` = price_total − delivery_cost
- `cac_low` = touches.low × (minutes.low / 60 × h + cash_per_touch.low); `cac_high` uses the highs
- `cash30` = amount if `payment_days_after_sale` ≤ 30, else 0 (monthly: the first month's amount under the same rule)
- `cash30_to_cac_low` and `cash30_to_cac_high` ratios
- `horizon_months` = min of boredom and melt months (ignoring nulls)
- `days_to_first_payment` = days_to_first_conversation + days_to_close + build_days
- `cohort_hours_per_week` = first_cohort × my_hours / delivery_weeks + first_cohort × touches.high × minutes.high / 60 / (test.days / 7)
- `guarantee_exposure` = first_cohort × refund_per_customer (0 if no guarantee)
- `anchor_ratio` = amount / anchor amount (a reference only; units may differ)
The numbers work only if all of these hold: margin > `min_margin_after_my_hours`; cash30 ≥ cac_low (or cac_high if configured); days_to_first_payment ≤ min(`max_days_to_first_payment`, runway_months × 30); cohort_hours_per_week ≤ ledger hours_per_week; guarantee_exposure ≤ guarantee_reserve. Otherwise kill (graveyard, listing the failed checks).
Rank the survivors by opens_ladder (position ≤ `opens_ladder_max_position`) first, then fewest days to first payment, then evidence strength (failed spend, money mentions, verified quotes, records). Keep `max_survivors`; the rest are cut with a graveyard line.
For each kept survivor, build the hypothesis: "At least 1 of {n} {who}, reached {how}, will pay {price} for {offer} within {days} days." Build the kill rule: "Kill it if fewer than 1 of the {n} pays {price} within {days} days of the first message. Decide on day {days}. No extensions." Write `06_numbers.csv` (one row per pain, with status), `06_numbers.md` (per survivor: a table of every number with its tag and formula, the stated assumptions, and a plain-English reading) and `06_survivors.json`.

### Outputs (outputs.py)
- `audit-packet`: `07_audit_packet/AUDIT_PROMPT.md` is a self-contained prompt for a different AI with deep research. Its one job is the strongest case against each survivor, with sources: competitors already doing it; past attempts that failed and why; reasons the pain isn't actually paid for; legal or platform risks. It embeds each survivor's one-liner, hypothesis, room, pain, pair and price, demands a URL for every claim, forbids invented sources, and fixes an output format. `evidence.md` holds each survivor's key evidence: verified quotes with links, counts, urgency, alternatives with prices, walk summary, pair, numbers.
- `shortlist`: `SHORTLIST.md`, one page per survivor (pages separated by `---`), in this order: 1 hypothesis; 2 room, pain, lane, one-liner; 3 evidence (3 verified quotes with links, counts, urgency, who pays, alternatives and prices); 4 walk summary (today and 12 months forward, walls that persist); 5 pair (entry walls and holding wall, with names); 6 numbers table; 7 ladder position and time to first payment; 8 the crux and the test's kill rule; 9 open questions and confidence; 10 case against (from `case_against.json`, if present; order and rank changes applied, each change explained in one line). If there are no survivors, say so plainly and point to the graveyard lines of this run.
- `review`: `REVIEW.md` with only what needs the founder: 1 is the ledger still true (its confirmed date, age, a short summary); 2 three quotes chosen at random (seeded by the run name) from verified quotes of kept pains, with links, "open it and check the meaning was read correctly"; 3 the credibility question for each survivor; 4 rooms that need 5 short calls; 5 other items only when present (fewer than 5 rooms at Stage 2 with depth/supply near-misses, blocked domains or missing keys).
- `runlog`: `RUNLOG.md` from `runlog.jsonl`: what ran (in order); counts in and out of every stage; sources used and skipped with reasons; blocked domains, with the exact list to allow; errors; approximate cost (API quota used; free APIs cost 0; model cost from `cost` events, tagged `[estimate]`).
- `status`: expected files per stage: present, missing, or missing with a logged reason.
- `commit-message`: `funnel: run YYYY-MM-DD: N rooms, M pains, K survivors` (rooms kept at Stage 2, pains kept at Stage 3, survivors kept at Stage 6).
- `compare --with latest`: for loop runs, compare with the latest earlier run containing the room; append a "What changed" section to `RUNLOG.md`.
- `audit-status`: print the run, its survivors and the files in `inbox/audit_results/`.

## Privacy (`anonymize.py`)
In this order, idempotently:
1. Emails → `[email]`.
2. Profile links → `[profile link]`: reddit `/user/` `/u/`, twitter.com / x.com handles, instagram, facebook profiles, linkedin `/in/`, youtube `/@` `/channel/` `/c/` `/user/`, tiktok `/@`, medium `/@`, quora `/profile/`, stackoverflow/stackexchange `/users/`, HN `user?id=`, github.com/<user> (a single path segment), `t.me/<user>`, `wa.me/<number>`. Other URLs stay.
3. Phone numbers → `[phone]`: 9–15 digits with optional `+`, spaces, dashes, dots or brackets. Never touch prices (currency before the number, or comma grouping like `15,000` / `1,50,000`), years, dates, times, percentages, test scores, or numbers glued to units.
4. Usernames → `[user]`: `u/name`, `/u/name`, `@handle` (not inside emails).
5. Names → `[name]`: honorific + capitalized name(s) (Mr, Mrs, Ms, Miss, Dr, Prof, Sir, Madam, Shri, Smt, Sri); a greeting or sign-off plus a name (`Hi Priya`, `Thanks, John`, `Regards,\nAmit`); `my name is X`; every `known_names` entry (whole word, case-insensitive).
Known limit (log it): names in running text without such a cue may survive. Rendered outputs use short quotes, and REVIEW asks the founder to open three of them.

## Tests (`tests/`)
`pytest -q opportunity-funnel/tests`. Tests never touch the network (fetches are mocked) and never write outside a temporary directory (`FUNNEL_ROOT` is overridable through the env var `FUNNEL_ROOT_OVERRIDE`, which tests set to a tmp copy).
Must cover: the quote checker (exact, whitespace, NBSP, case, punctuation, curly quotes, missing record, too short, citation correction, idempotency); the counters (counts, multi-key, every error type, failed-spend implies money); batches (24-month boundary, undated, text duplicates, cap, deterministic); anonymizer (each rule, prices and dates untouched, idempotent); inbox parsers; Stage 3 kills and ranking; walks and pairs lanes and adjacency; numbers arithmetic, kills and ranking; and an end-to-end synthetic run through the CLI, run twice to prove identical outputs.
