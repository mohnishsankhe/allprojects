export const meta = {
  name: 'funnel-stage6-numbers',
  description: 'Stage 6: one funnel-walker in mode numbers per Stage 5 survivor (low/base/high inputs, price anchor from the human substitute)',
  phases: [{ title: 'Numbers', detail: 'one walker per survivor, in parallel' }],
}
// args = { run: 'runs/YYYY-MM-DD', pains: ['<room-slug>--<pain-key>', ...] }
const F = '/home/user/allprojects/opportunity-funnel'
const RUNREL = args.run
// Model policy (founder, 2026-09-27): Claude Opus 5.5 at max effort for every agent.
const OPUS = { model: 'claude-opus-5-5', effort: 'max' }

const NUM = { type: 'object', properties: {
  pain_id: { type: 'string' }, offer: { type: 'string' }, currency: { type: 'string' },
  price_base: { type: 'number' }, anchor_price_text: { type: 'string' }, anchor_url: { type: 'string' },
  channel: { type: 'string' }, check_passed: { type: 'boolean' }, confidence: { type: 'string' }, notes: { type: 'string' } },
  required: ['pain_id', 'offer', 'currency', 'price_base', 'anchor_price_text', 'anchor_url', 'channel', 'check_passed', 'confidence', 'notes'] }

const run = (pain) => agent(
  `Opportunity Funnel, Stage 6. RUN = ${RUNREL} (folder ${F}/${RUNREL}). pain_id: ${pain}. MODE: numbers. Follow your agent instructions (funnel-walker) exactly. Commands: python3 ${F}/pipeline/funnel.py --run ${RUNREL} <command> ...\nWrite ${RUNREL}/06_inputs/${pain}.json and check it with: numbers --check ${pain}. Return check_passed = true only when that check printed no errors.`,
  { agentType: 'funnel-walker', ...OPUS, schema: NUM, label: `numbers:${pain}`, phase: 'Numbers' })

return await parallel(args.pains.map(p => () => run(p)))
