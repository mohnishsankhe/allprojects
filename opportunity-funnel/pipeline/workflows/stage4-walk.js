export const meta = {
  name: 'funnel-stage4-walk',
  description: 'Stage 4: two independent walkers per pain, then a comparator that merges conservatively and drafts 2-3 alternative pairs',
  phases: [{ title: 'Walk', detail: 'walkers a and b per pain, in parallel' }, { title: 'Compare', detail: 'one comparator per pain after both walks' }],
}
// args = { run: 'runs/YYYY-MM-DD', pains: ['<room-slug>--<pain-key>', ...] }
const F = '/home/user/allprojects/opportunity-funnel'
const RUNREL = args.run
// Model policy (founder, 2026-09-27): Claude Opus 5.5 at max effort for every agent.
const OPUS = { model: 'claude-opus-5-5', effort: 'max' }

const WALK = { type: 'object', properties: {
  pain_id: { type: 'string' }, walker: { type: 'string' },
  outcome_reached_today: { type: 'boolean' }, walls_on_path: { type: 'array', items: { type: 'string' } },
  check_passed: { type: 'boolean' }, notes: { type: 'string' } },
  required: ['pain_id', 'walker', 'outcome_reached_today', 'walls_on_path', 'check_passed', 'notes'] }
const COMPARE = { type: 'object', properties: {
  pain_id: { type: 'string' }, outcome_reached_today: { type: 'boolean' },
  walls_both: { type: 'array', items: { type: 'string' } }, walls_one: { type: 'array', items: { type: 'string' } },
  disagreements: { type: 'integer' }, pairs: { type: 'integer' }, best_pair: { type: 'string' },
  check_passed: { type: 'boolean' }, notes: { type: 'string' } },
  required: ['pain_id', 'outcome_reached_today', 'walls_both', 'walls_one', 'disagreements', 'pairs', 'best_pair', 'check_passed', 'notes'] }

const base = (pain) => `Opportunity Funnel, Stage 4. RUN = ${RUNREL} (folder ${F}/${RUNREL}). pain_id: ${pain}. Follow your agent instructions (funnel-walker) exactly. Commands: python3 ${F}/pipeline/funnel.py --run ${RUNREL} <command> ...`

async function walkOne(pain) {
  const walks = await parallel(['a', 'b'].map(w => () => agent(
    `${base(pain)}\nMODE: walk. WALKER: ${w}. You are one of two independent walkers: never open ${RUNREL}/04_walks/${pain}.${w === 'a' ? 'b' : 'a'}.json or the merged file. Check only your own file with: walks --check ${pain} --walker ${w}. Return check_passed = true only when that check printed no errors.`,
    { agentType: 'funnel-walker', ...OPUS, schema: WALK, label: `walk:${pain}:${w}`, phase: 'Walk' })))
  if (walks.some(x => !x || !x.check_passed)) {
    log(`${pain}: a walk failed its check; comparator not run`)
    return { pain, walks, compare: null }
  }
  const cmp = await agent(
    `${base(pain)}\nMODE: compare. Both walker files exist: ${RUNREL}/04_walks/${pain}.a.json and .b.json. Merge them conservatively into ${RUNREL}/04_walks/${pain}.json and, unless the merged outcome is reached today, draft 2 to 3 alternative pairs. Check with: walks --check ${pain}. Return check_passed = true only when that check printed no errors.`,
    { agentType: 'funnel-walker', ...OPUS, schema: COMPARE, label: `compare:${pain}`, phase: 'Compare' })
  if (cmp) log(`${pain}: outcome today=${cmp.outcome_reached_today}, both=${cmp.walls_both.join(',')}, pairs=${cmp.pairs}`)
  return { pain, walks, compare: cmp }
}

return await parallel(args.pains.map(p => () => walkOne(p)))
