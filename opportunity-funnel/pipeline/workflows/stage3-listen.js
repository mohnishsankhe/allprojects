export const meta = {
  name: 'funnel-stage3-listen',
  description: 'Stage 3: listen to saturation, one listener per room (plan -> harvest -> label rounds, then synthesize, then checkpoint)',
  phases: [{ title: 'Listen', detail: 'per room: rounds until saturated, exhausted or max rounds' }],
}
const F = '/home/user/allprojects/opportunity-funnel'
const RUNREL = 'runs/2026-09-26'
const MIN_RECORDS = 500, EXHAUSTED = 50, MAX_ROUNDS = 8, CHUNK = 25

const PLAN = { type: 'object', properties: {
  round: { type: 'integer' }, queries: { type: 'array', items: { type: 'string' } },
  kinds_covered: { type: 'array', items: { type: 'string' } }, notes: { type: 'string' } },
  required: ['round', 'queries', 'kinds_covered', 'notes'] }
const LABEL = { type: 'object', properties: {
  records_total: { type: 'integer' }, new_records: { type: 'integer' }, member_records: { type: 'integer' },
  pains: { type: 'integer' }, saturated: { type: 'boolean' }, new_pains: { type: 'array', items: { type: 'string' } },
  rank_changes: { type: 'array', items: { type: 'string' } }, unmatched_queries: { type: 'integer' }, notes: { type: 'string' } },
  required: ['records_total', 'new_records', 'member_records', 'pains', 'saturated', 'new_pains', 'rank_changes', 'unmatched_queries', 'notes'] }
const SYN = { type: 'object', properties: {
  pains_drafted: { type: 'integer' }, quotes_passing: { type: 'integer' }, records_by_kind: { type: 'string' },
  thin: { type: 'array', items: { type: 'string' } }, spend_gaps: { type: 'array', items: { type: 'string' } },
  needs_calls: { type: 'boolean' }, summary: { type: 'string' } },
  required: ['pains_drafted', 'quotes_passing', 'records_by_kind', 'thin', 'spend_gaps', 'needs_calls', 'summary'] }

const base = (slug) => `Opportunity Funnel, Stage 3. RUN = ${RUNREL} (folder ${F}/${RUNREL}). Room slug: ${slug}. Follow your agent instructions (funnel-listener) exactly. Commands: python3 ${F}/pipeline/funnel.py --run ${RUNREL} <command> ...`

// Round 1 keeps its original prompt and model so completed round-1 harvests replay from the workflow cache.
// Later rounds batch the searches (10 parallel WebSearch calls per message) on a cheaper model: harvesting is
// mechanical (no judgment), and batching avoids re-reading a growing context once per search.
function harvestPrompt(qs, round) {
  if (round === 1) {
    return `Run each of the web searches below with the WebSearch tool, in order, one WebSearch call per line.
Copy each query string EXACTLY as written (same words, quotes, site: operators, capitalization, spacing). Do not rephrase, fix, merge or skip any.
Use no other tool. Do not analyse or summarise the results. When all are done, reply only: DONE <number of searches you ran>.

${qs.map((q, i) => `${i + 1}. ${q}`).join('\n')}`
  }
  return `Run every web search below with the WebSearch tool.
Send them in parallel: put 10 WebSearch tool calls in a single message, wait for those results, then send the next 10, until all are done.
Copy each query string EXACTLY as written (same words, quotes, site: operators, capitalization, spacing). Do not rephrase, fix, merge or skip any.
Use no other tool. Do not analyse or summarise the results. When all are done, reply only: DONE <number of searches you ran>.

${qs.map((q, i) => `${i + 1}. ${q}`).join('\n')}`
}
const harvestModel = (round) => (round === 1 ? 'sonnet' : 'haiku')

async function listen(slug) {
  let round = 1, stop = null
  const history = []
  while (true) {
    const plan = await agent(`${base(slug)}\nMODE: plan. ROUND: ${round}. ${round > 1 ? `Earlier rounds so far: ${JSON.stringify(history)}. Aim new queries at what is missing (source kinds, pains, money and failed-spend language, deadlines).` : ''}\nAppend this round's queries to queries.jsonl and return them in the queries field exactly as written there.`,
      { agentType: 'funnel-listener', model: 'fable', schema: PLAN, label: `plan:${slug}:r${round}`, phase: 'Listen' })
    if (!plan || !plan.queries || plan.queries.length === 0) { stop = 'exhausted'; break }
    const chunks = []
    const size = round === 1 ? CHUNK : 50
    for (let i = 0; i < plan.queries.length; i += size) chunks.push(plan.queries.slice(i, i + size))
    await parallel(chunks.map((qs, ci) => () => agent(harvestPrompt(qs, round), { model: harvestModel(round), label: `harvest:${slug}:r${round}:${ci}`, phase: 'Listen' })))
    const lab = await agent(`${base(slug)}\nMODE: label. ROUND: ${round}. Run harvest-search, batches, label every new batch (relabel all batches if the taxonomy changed), then count and saturation. Report the numbers exactly as the scripts printed them.`,
      { agentType: 'funnel-listener', model: 'fable', schema: LABEL, label: `label:${slug}:r${round}`, phase: 'Listen' })
    if (!lab) { stop = 'error'; break }
    history.push({ round, queries: plan.queries.length, kinds: plan.kinds_covered, records_total: lab.records_total, new_records: lab.new_records, member_records: lab.member_records, pains: lab.pains, saturated: lab.saturated, new_pains: lab.new_pains, rank_changes: lab.rank_changes.length, unmatched: lab.unmatched_queries })
    log(`${slug} r${round}: ${lab.records_total} records (+${lab.new_records}), ${lab.pains} pains, saturated=${lab.saturated}`)
    if (lab.saturated && lab.records_total >= MIN_RECORDS) { stop = 'saturated'; break }
    if (round > 1 && lab.new_records < EXHAUSTED) { stop = 'exhausted'; break }
    if (round >= MAX_ROUNDS) { stop = 'max_rounds'; break }
    round++
  }
  const syn = await agent(`${base(slug)}\nMODE: synthesize. STOP REASON: ${stop} (use it in funnel saturation --final --stop-reason; if the script refuses 'saturated', use what it accepts and say so). Rounds: ${JSON.stringify(history)}.`,
    { agentType: 'funnel-listener', model: 'fable', schema: SYN, label: `synth:${slug}`, phase: 'Listen' })
  const cp = await agent(`Run exactly this shell command once and reply with its output only:\nbash ${F}/pipeline/checkpoint.sh ${RUNREL} "Stage 3 room ${slug} (${stop}, ${history.length} rounds)"`,
    { model: 'haiku', label: `checkpoint:${slug}`, phase: 'Listen' })
  return { slug, stop, rounds: history.length, history, synth: syn, checkpoint: cp }
}

return await parallel(args.rooms.map(s => () => listen(s)))
