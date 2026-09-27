export const meta = {
  name: 'funnel-stage3-listen',
  description: 'Stage 3: listen to saturation, one listener per room (plan -> harvest -> label-prep -> one labeler per batch -> label-finish rounds, then synthesize, then checkpoint)',
  phases: [{ title: 'Listen', detail: 'per room: rounds until saturated, exhausted or max rounds' }],
}
// args = { rooms: [slug, ...], searched: { <slug>: { round: N, queries: Q, kinds: [...] } } }
//   (older form: r1: { <slug>: { queries: Q, kinds: [...] } } = searched with round 1)
const F = '/home/user/allprojects/opportunity-funnel'
const RUNREL = 'runs/2026-09-26'
const MIN_RECORDS = 500, EXHAUSTED = 50, MAX_ROUNDS = 8, CHUNK = 50

// Model policy (founder, 2026-09-27): Claude Opus 5.5 at max effort for every agent, including search runners,
// bulk labeling and helpers. Nothing uses Fable or a smaller model.
const OPUS = { model: 'claude-opus-5-5', effort: 'max' }
// args.searched lists, per room, the last round whose queries were all planned (queries.jsonl) and searched (results in
// the session transcripts) by an earlier run. That room starts at that round's label step: harvest-search reads the
// earlier searches, so no plan or search agent runs again for it. The workflow cache is not relied on for this.
const SEARCHED = Object.assign({}, ...Object.entries(args.r1 || {}).map(([k, v]) => ({ [k]: { round: 1, ...v } })), args.searched || {})

const PLAN = { type: 'object', properties: {
  round: { type: 'integer' }, queries: { type: 'array', items: { type: 'string' } },
  kinds_covered: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['round', 'queries', 'kinds_covered', 'notes'] }
const LABEL = { type: 'object', properties: {
  records_total: { type: 'integer' }, new_records: { type: 'integer' }, member_records: { type: 'integer' },
  pains: { type: 'integer' }, saturated: { type: 'boolean' }, new_pains: { type: 'array', items: { type: 'string' } },
  rank_changes: { type: 'array', items: { type: 'string' } }, unmatched_queries: { type: 'integer' }, notes: { type: 'string' } },
  required: ['records_total', 'new_records', 'member_records', 'pains', 'saturated', 'new_pains', 'rank_changes', 'unmatched_queries', 'notes'] }
const PREP = { type: 'object', properties: {
  records_total: { type: 'integer' }, new_records: { type: 'integer' }, unmatched_queries: { type: 'integer' },
  batches_to_label: { type: 'array', items: { type: 'string' } }, packs_to_check: { type: 'array', items: { type: 'string' } },
  taxonomy_changed: { type: 'boolean' }, pains: { type: 'integer' }, added_pains: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['records_total', 'new_records', 'unmatched_queries', 'batches_to_label', 'packs_to_check', 'taxonomy_changed', 'pains', 'added_pains', 'notes'] }
const LPACK = { type: 'object', properties: {
  pack: { type: 'string' }, records: { type: 'integer' }, changed: { type: 'integer' }, check_passed: { type: 'boolean' }, notes: { type: 'string' } },
  required: ['pack', 'records', 'changed', 'check_passed', 'notes'] }
const LBATCH = { type: 'object', properties: {
  batch: { type: 'string' }, records: { type: 'integer' }, labels: { type: 'integer' }, member_records: { type: 'integer' },
  check_passed: { type: 'boolean' }, suggested_pains: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['batch', 'records', 'labels', 'member_records', 'check_passed', 'suggested_pains', 'notes'] }
const SYN = { type: 'object', properties: {
  pains_drafted: { type: 'integer' }, quotes_passing: { type: 'integer' }, records_by_kind: { type: 'string' },
  thin: { type: 'array', items: { type: 'string' } }, spend_gaps: { type: 'array', items: { type: 'string' } },
  needs_calls: { type: 'boolean' }, summary: { type: 'string' } },
  required: ['pains_drafted', 'quotes_passing', 'records_by_kind', 'thin', 'spend_gaps', 'needs_calls', 'summary'] }

const base = (slug) => `Opportunity Funnel, Stage 3. RUN = ${RUNREL} (folder ${F}/${RUNREL}). Room slug: ${slug}. Follow your agent instructions (funnel-listener) exactly. Commands: python3 ${F}/pipeline/funnel.py --run ${RUNREL} <command> ...`

// Harvesting is mechanical: batching 10 parallel searches per message avoids re-reading a growing context once per search.
function harvestPrompt(qs) {
  return `Run every web search below with the WebSearch tool.
Send them in parallel: put 10 WebSearch tool calls in a single message, wait for those results, then send the next 10, until all are done.
Copy each query string EXACTLY as written (same words, quotes, site: operators, capitalization, spacing). Do not rephrase, fix, merge or skip any.
Use no other tool. Do not analyse or summarise the results. When all are done, reply only: DONE <number of searches you ran>.

${qs.map((q, i) => `${i + 1}. ${q}`).join('\n')}`
}

// One round of labeling: label-prep (scripts + taxonomy + which batches need labels), one labeler per new batch and
// one re-check labeler per pack of earlier member records (when pains were added) in parallel, each with a small fresh
// context, then label-finish (apply the re-check patches, count, saturation). Labelers never edit the taxonomy:
// they suggest missing pains, and the next round's label-prep decides.
async function labelRound(slug, round, suggestions) {
  const prep = await agent(`${base(slug)}\nMODE: label-prep. ROUND: ${round}. PACKS: yes.${suggestions.length ? ` Pains the labelers suggested last round: ${JSON.stringify(suggestions)}.` : ''}`,
    { agentType: 'funnel-listener', ...OPUS, schema: PREP, label: `prep:${slug}:r${round}`, phase: 'Listen' })
  if (!prep) return null
  const todo = (prep.batches_to_label || []).filter(b => /^batch_r\d+_\d+$/.test(b))
  const packs = (prep.packs_to_check || []).filter(b => /^pack_r\d+_\d+$/.test(b))
  const kind = prep.taxonomy_changed && packs.length === 0 ? 'relabel' : 'label'
  const jobs = [
    ...todo.map(b => () => agent(`${base(slug)}\nMODE: label-batch. ROUND: ${round}. BATCH: ${b}.`,
      { agentType: 'funnel-listener', ...OPUS, schema: LBATCH, label: `${kind}:${slug}:r${round}:${b}`, phase: 'Listen' })),
    ...packs.map(k => () => agent(`${base(slug)}\nMODE: label-pack. ROUND: ${round}. PACK: ${k}.`,
      { agentType: 'funnel-listener', ...OPUS, schema: LPACK, label: `recheck:${slug}:r${round}:${k}`, phase: 'Listen' })),
  ]
  const results = await parallel(jobs)
  const done = results.slice(0, todo.length), checked = results.slice(todo.length)
  const failed = [...todo.filter((b, i) => !done[i] || !done[i].check_passed), ...packs.filter((k, i) => !checked[i] || !checked[i].check_passed)]
  const suggested = [...new Set(done.filter(Boolean).flatMap(x => x.suggested_pains || []))]
  const lab = await agent(`${base(slug)}\nMODE: label-finish. ROUND: ${round}.${failed.length ? ` These batches or packs have no checked labels or patch (their labeler failed); do them first: ${failed.join(', ')}.` : ''}`,
    { agentType: 'funnel-listener', ...OPUS, schema: LABEL, label: `finish:${slug}:r${round}`, phase: 'Listen' })
  if (!lab) return null
  return { prep, lab, labeled: todo.length, rechecked: packs.length, failed, suggested }
}

async function listen(slug) {
  const pre = SEARCHED[slug] || null
  const first = pre ? pre.round : 1
  let round = first, stop = null, suggestions = []
  const history = []
  while (true) {
    let nq, kinds
    if (pre && round === first) {
      nq = pre.queries; kinds = pre.kinds
      log(`${slug} r${round}: planned and searched by an earlier run (${nq} queries); labeling on Opus`)
    } else {
      const plan = await agent(`${base(slug)}\nMODE: plan. ROUND: ${round}. ${round > 1 ? `Earlier rounds so far: ${JSON.stringify(history)}. Aim new queries at what is missing (source kinds, pains, money and failed-spend language, deadlines).` : ''}\nAppend this round's queries to queries.jsonl and return them in the queries field exactly as written there.`,
        { agentType: 'funnel-listener', ...OPUS, schema: PLAN, label: `plan:${slug}:r${round}`, phase: 'Listen' })
      if (!plan) { stop = 'error'; break }
      if (!plan.queries || plan.queries.length === 0) { stop = 'exhausted'; break }
      nq = plan.queries.length; kinds = plan.kinds_covered
      const chunks = []
      for (let i = 0; i < plan.queries.length; i += CHUNK) chunks.push(plan.queries.slice(i, i + CHUNK))
      await parallel(chunks.map((qs, ci) => () => agent(harvestPrompt(qs), { ...OPUS, label: `harvest:${slug}:r${round}:${ci}`, phase: 'Listen' })))
    }
    const lr = await labelRound(slug, round, suggestions)
    if (!lr) { stop = 'error'; break }
    const lab = lr.lab
    suggestions = lr.suggested
    history.push({ round, queries: nq, kinds, records_total: lab.records_total, new_records: lab.new_records, member_records: lab.member_records, pains: lab.pains, saturated: lab.saturated, new_pains: lab.new_pains, rank_changes: lab.rank_changes.length, unmatched: lab.unmatched_queries, batches_labeled: lr.labeled, packs_rechecked: lr.rechecked, taxonomy_changed: lr.prep.taxonomy_changed, suggested_pains: suggestions.length })
    log(`${slug} r${round}: ${lab.records_total} records (+${lab.new_records}), ${lab.pains} pains, ${lr.labeled} batches labeled, saturated=${lab.saturated}, suggested pains=${suggestions.length}`)
    // Saturated only from round 2, with every planned query searched (an interrupted harvest leaves unmatched queries),
    // and with no pain a labeler suggested (the latest records may hold a pain the taxonomy lacks).
    if (lab.saturated && lab.records_total >= MIN_RECORDS && round >= 2 && lab.unmatched_queries === 0 && suggestions.length === 0) { stop = 'saturated'; break }
    if (round > 1 && lab.new_records < EXHAUSTED) { stop = 'exhausted'; break }
    if (round >= MAX_ROUNDS) { stop = 'max_rounds'; break }
    round++
  }
  // A failed step is not a finished room: skip the synthesis so the room can be resumed from where it stopped.
  const syn = stop === 'error' ? null : await agent(`${base(slug)}\nMODE: synthesize. STOP REASON: ${stop} (use it in funnel saturation --final --stop-reason; if the script refuses 'saturated', use what it accepts and say so). Rounds: ${JSON.stringify(history)}.${suggestions.length ? ` Pains the labelers suggested in the last round that the taxonomy does not have: ${JSON.stringify(suggestions)}. List them in sources.json under "suggested_pains_not_added", one line each, so the founder sees them.` : ''}`,
    { agentType: 'funnel-listener', ...OPUS, schema: SYN, label: `synth:${slug}`, phase: 'Listen' })
  const cp = await agent(`Run exactly this shell command once and reply with its output only:\nbash ${F}/pipeline/checkpoint.sh ${RUNREL} "Stage 3 room ${slug} (${stop}, ${history.length} rounds)"`,
    { ...OPUS, label: `checkpoint:${slug}`, phase: 'Listen' })
  return { slug, stop, rounds: history.length, history, synth: syn, checkpoint: cp }
}

return await parallel(args.rooms.map(s => () => listen(s)))
