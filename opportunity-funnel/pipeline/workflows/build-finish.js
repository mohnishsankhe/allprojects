export const meta = {
  name: 'funnel-build-finish',
  description: 'Finish the pipeline build: complete stages 3-6 and outputs, integrate, four reviews, fixes',
  phases: [
    { title: 'Modules', detail: 'finish stage3+stage45 and stage6+outputs (partial files exist)' },
    { title: 'Integrate', detail: 'end-to-end synthetic run twice, docs-CLI sync, full suite' },
    { title: 'Review', detail: 'spec, privacy, correctness, usability lenses' },
    { title: 'Fix', detail: 'verify each finding, fix real ones, final suite' },
  ],
}
const F = '/home/user/allprojects/opportunity-funnel'
const RULES = `
HARD RULES FOR THIS TASK
- Work only inside ${F}/. Never create, modify or delete anything else under /home/user/allprojects (never touch /home/user/allprojects/.claude/, README.md, or ${F}/PROGRESS.md, ${F}/CLAUDE.md, ${F}/config/*, ${F}/.claude/*, ${F}/runs/* — list needed edits to those in needed_changes_elsewhere instead).
- Do not run git commit, push, checkout, reset or stash. The orchestrator commits (an autosave loop may commit your files; that's fine).
- No real network calls. Tests mock HTTP and set FUNNEL_OFFLINE=1.
- First read: ${F}/pipeline/README.md (the design: follow it exactly), ${F}/config/formats.md, ${F}/config/kill_rules.yaml, ${F}/config/ledger.yaml, ${F}/config/ledger.md, ${F}/config/walls.md, ${F}/config/definitions.md, ${F}/config/sources.md, ${F}/CLAUDE.md, and the existing core modules (common.py, anonymize.py, netfetch.py, records.py, harvest.py, quote_check.py, counts.py, funnel.py, sources.py, admin.py, prices.py, stage1.py, stage2.py) and tests/conftest.py. Reuse their helpers.
- Python 3.11. Allowed deps: standard library, requests, PyYAML, pytest.
- Deterministic outputs (stable orders; json sort_keys, indent 2, ensure_ascii False, trailing newline; no timestamps except runlog.jsonl; randomness seeded from the run name).
- Plain English in every message and rendered file. Short sentences.
- Run tests with: cd ${F} && python3 -m pytest -q <files>.
- If the design is ambiguous, choose the option most faithful to the founder's rules (evidence by construction; code for all arithmetic, counting, dedupe, dates, currency; mechanical logged kills; honest tags; conservative choices) and list it in design_choices.
`
const REPORT = {
  type: 'object',
  properties: {
    summary: { type: 'string' }, files_written: { type: 'array', items: { type: 'string' } },
    test_command: { type: 'string' }, test_result: { type: 'string' },
    design_choices: { type: 'array', items: { type: 'string' } },
    needed_changes_elsewhere: { type: 'array', items: { type: 'string' } },
    open_issues: { type: 'array', items: { type: 'string' } },
  },
  required: ['summary', 'files_written', 'test_command', 'test_result', 'design_choices', 'needed_changes_elsewhere', 'open_issues'],
}
const FINDINGS = {
  type: 'object',
  properties: { findings: { type: 'array', items: { type: 'object', properties: {
    title: { type: 'string' }, file: { type: 'string' }, line: { type: 'integer' },
    severity: { type: 'string', enum: ['blocker', 'major', 'minor'] },
    description: { type: 'string' }, failure_scenario: { type: 'string' }, suggested_fix: { type: 'string' },
  }, required: ['title', 'file', 'severity', 'description', 'failure_scenario', 'suggested_fix'] } } },
  required: ['findings'],
}
const M = 'fable'

phase('Modules')
const JOBS = [
  { key: 'stages345', prompt: `Finish pipeline/stage3.py (command pains) and pipeline/stage45.py (commands walks [--check PAIN_ID] and pairs). PARTIAL VERSIONS ALREADY EXIST from an attempt that was cut off by a usage limit: read them first, keep what is right, complete and fix the rest (you own these two files and may rewrite them). Requirements, per the design: pains — drafts + counts join, quote checker + quote_check.csv, drop rules in order, [thin], spend-evidence distinct-domain check -> [spend: 1 source], [titles only], [undated share: X%], ranking, max 25 across rooms, graveyard every drop/cut, needs_calls and saturation verdicts collected, pains.json and a readable pains.md. walks — validate .a/.b/merged files, re-derive the conservative merge from .a/.b and reject a less-conservative merged file naming the field, reconciled_ids honored, kill on outcome reached, all-melt -> lane_hint trade, render each walk markdown incl. walker disagreements, _stage4.json. pairs — validate EVERY alternative mechanically (entry/hold/adjacency/persistence/walls_both; lanes business/partner/trade with the ledger's can_be — c2 Judgment only for strong-depth rooms via 02_mask.json depth id strength — can_rent, cannot list, trade conditions), keep the strongest valid one by lane order then rank, kill if none listing each alternative's failures; write 05_pairs.json and 05_pairs.md showing all alternatives. Write tests/test_stage3.py and tests/test_stage45.py covering every rule, the conservative-merge rejection cases and each lane.` },
  { key: 'stage6out', prompt: `Finish pipeline/stage6.py (command numbers [--check PAIN_ID]) — A PARTIAL VERSION EXISTS from an attempt cut off by a usage limit: read it, keep what is right, complete and fix the rest — and write pipeline/outputs.py (commands redteam, audit-packet, shortlist, review, runlog, progress, status, commit-message, compare --with latest, audit-status). Stage 6 per the design: three cases and every formula, room currency and USD via fx_rates.json (note: the real run's fx_rates.json may carry seen_via "page"), founder hour value from the ledger converted through USD, the six base-case kill checks, evidence labels from kill_rules, ranking opens_ladder > days_to_first_payment > usd_per_hour_base > evidence, keep max 5 with graveyard cuts, hypothesis and kill-rule sentences with the price in local currency and USD in brackets; 06_numbers.csv one row per pain x case; 06_numbers.md every number with formula and tag, low/base/high side by side; 06_survivors.json. Outputs per the design's Outputs section, including the no-survivor case (five closest candidates and what killed each), REVIEW.md sections 1-7 with [assumed] items (reuse admin's ledger-check logic), 'progress' regenerating only the auto:status block of PROGRESS.md, runlog with 'Domains to allow' and 'Approximate cost' and build/test 'check' events. Write tests/test_stage6.py (hand-computed values for every formula and case, each kill check, ranking, top-5 cut, sentences, --check errors) and tests/test_outputs.py.` },
]
const modules = await parallel(JOBS.map(j => () => agent(`${RULES}
Do NOT edit core or already-finished modules (common, anonymize, netfetch, records, harvest, quote_check, counts, funnel, sources, admin, prices, stage1, stage2); put needed changes in needed_changes_elsewhere and work around them. Only run your own test files (another agent works in parallel).

YOUR JOB: ${j.prompt}

Make all your tests pass. Put the final pytest output verbatim in test_result.`, { label: `module:${j.key}`, phase: 'Modules', schema: REPORT, model: M })))
const modReports = JOBS.map((j, i) => ({ key: j.key, report: modules[i] }))
log(`Modules: ${modReports.map(m => `${m.key}=${m.report ? 'ok' : 'FAILED'}`).join(', ')}`)

phase('Integrate')
const integ = await agent(`${RULES}
All modules exist now. YOUR JOB is integration. You may edit any file under ${F}/pipeline and ${F}/tests.
Module reports (apply or consciously reject their needed changes): ${JSON.stringify(modReports.map(m => ({ key: m.key, needed: m.report ? m.report.needed_changes_elsewhere : ['AGENT FAILED - finish this module per the design'], open: m.report ? m.report.open_issues : [] })), null, 1)}
Also note: sources.py, admin.py, prices.py, stage1.py and stage2.py were built by earlier agents whose reports you don't have — read them and their tests.
1. Run the full suite (cd ${F} && python3 -m pytest -q). Fix every failure at its root. Never skip, weaken or delete a test.
2. Write tests/test_e2e.py: a full synthetic run through the CLI in subprocesses (FUNNEL_ROOT_OVERRIDE to a tmp copy with the real config; FUNNEL_OFFLINE=1; FUNNEL_TRANSCRIPTS_DIR to a tmp dir holding synthetic transcript lines in both forms): preflight, rooms --merge-parts --dry-run (small parts incl. a gap part), fx, mask --merge-parts, then 2 rooms: queries.jsonl for 2 rounds -> harvest-search -> batches -> taxonomy + labels -> count -> saturation, then pains_draft files (some quotes exact, some altered) -> pains; walks with .a/.b/merged files exercising a kill, a trade hint, a rejected less-conservative merge (exit 1) then a corrected one, and business/partner alternatives; pairs; 06_inputs exercising a numbers kill and at least 2 survivors; redteam files + case_against.json re-ranking; audit-packet, shortlist, review, runlog, progress, status, commit-message. Assert key contents (quote_check statuses, graveyard lines, lanes, survivor order, SHORTLIST section order and 'Case against', REVIEW sections incl. [assumed] items, no raw emails/phones under runs/ outside raw/). Run the sequence a SECOND time on the same folder: every output except runlog.jsonl, RUNLOG.md and PROGRESS.md byte-identical; no duplicate graveyard lines.
3. Write tests/test_docs_cli_sync.py: parse ${F}/.claude/skills/*/SKILL.md and ${F}/.claude/agents/*.md for every 'funnel <command> [--flags]' usage and assert the CLI has that command and those flags. Fix the CLI when they disagree; list doc fixes in needed_changes_elsewhere.
4. Check 'python3 ${F}/pipeline/funnel.py --help' works from /tmp and from ${F}.
5. Full suite green. Final pytest output (verbatim, last 30 lines) in test_result.`, { label: 'integrate', phase: 'Integrate', schema: REPORT, model: M })
log(`Integration: ${integ ? integ.test_result.split('\n').filter(Boolean).slice(-1)[0] : 'FAILED'}`)

phase('Review')
const LENSES = [
  { key: 'spec', prompt: `SPEC COMPLIANCE. Compare the code's actual behavior with the founder's instructions below, rule by rule and stage by stage: kill rules and their order/comparisons, graveyard lines, output sections and order, arithmetic/currency only in code, [measured] only with URL or record ids, no quote reaching an output without passing the checker, no stage reading a later stage's file, idempotency, the conservative walk merge, all alternatives validated, Stage 6 cases and ranking, REVIEW.md items.\n\nFOUNDER'S INSTRUCTIONS (FINAL INSTRUCTIONS win on conflict):\n${args.brief}` },
  { key: 'privacy', prompt: `PRIVACY, SAFETY AND BOUNDARIES. Personal data surviving anonymization (run adversarial inputs), anonymizer false positives corrupting prices/dates/scores, raw text written where git would commit (check ${F}/.gitignore against every path the code writes: batches, caches, harvested records, logs), inbox read or printed before anonymization, API keys reaching logs/cache/errors, robots/rate limits bypassable, writes outside ${F}, path traversal via slugs or file names, the harvest storing the search tool's written summary or anything other than titles and URLs, the harvest ingesting non-search transcript text.` },
  { key: 'correctness', prompt: `CORRECTNESS AND DETERMINISM. Real bugs only: Stage 6 case arithmetic and USD conversion, 24-month lookback and 30/90-day windows, URL-date parsing, saturation (window, competition ranks, new pains), batches by round, division by zero, None handling, unstable sort orders, rerun byte differences, graveyard duplication, double counting, voice handling, conservative merge derivation, adjacency, lane precedence, ranking tie-breaks. Demonstrate each bug with a script or test before reporting it.` },
  { key: 'ux', prompt: `AGENT AND FOUNDER USABILITY. The CLI is driven by subagents following ${F}/.claude/skills/*/SKILL.md and ${F}/.claude/agents/*.md. Check each step there is doable with the CLI as built (commands, flags, paths, printed output), error messages say exactly what to fix, exit codes match the design, rendered markdown is plain English with short sentences and explains non-everyday terms, and a --dry-run one-room pass works end to end. Report doc problems in .claude files as findings.` },
]
const reviews = await parallel(LENSES.map(l => () => agent(`${RULES}
You are an independent reviewer. Do NOT edit any file (scratch files under /tmp only). Report only real, verified problems with a concrete failure scenario. No style nits.

LENS: ${l.prompt}`, { label: `review:${l.key}`, phase: 'Review', schema: FINDINGS, model: M })))
const all = []
reviews.forEach((r, i) => { if (r) r.findings.forEach(f => all.push({ lens: LENSES[i].key, ...f })) })
const seen = new Set()
const deduped = all.filter(f => { const k = `${f.file}|${f.title.toLowerCase().slice(0, 60)}`; if (seen.has(k)) return false; seen.add(k); return true })
log(`Review: ${deduped.length} findings (${deduped.filter(f => f.severity === 'blocker').length} blockers, ${deduped.filter(f => f.severity === 'major').length} major); reviewers ok: ${reviews.filter(Boolean).length}/4`)

phase('Fix')
const fix = await agent(`${RULES}
You may edit any file under ${F}/pipeline and ${F}/tests (not .claude/, config/, CLAUDE.md, PROGRESS.md, runs/: list needed edits there in needed_changes_elsewhere with exact new text).
Independent reviewers reported these findings. For EACH: verify first (reproduce with a test or script). If real, fix the root cause and add a regression test. If not real, reject it in one line. Never weaken or delete an existing test.
FINDINGS: ${JSON.stringify(deduped, null, 1)}
Integration open items: ${JSON.stringify(integ ? { needed: integ.needed_changes_elsewhere, open: integ.open_issues } : 'integration failed — run the full suite and fix everything', null, 1)}
Finish with the full suite green (cd ${F} && python3 -m pytest -q). In summary list each finding as 'FIXED: title' or 'REJECTED: title — reason'. Final pytest output (verbatim, last 30 lines) in test_result.`, { label: 'fix', phase: 'Fix', schema: REPORT, model: M })

return { modules: modReports, integrate: integ, findings: deduped, fix }
