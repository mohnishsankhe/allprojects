#!/usr/bin/env node
/**
 * Acceptance criterion 1: Lighthouse mobile >= 90 across the board, LCP < 2.0s
 * on simulated 4G.
 *
 * Runs against a production build with Lighthouse's default mobile preset
 * (Slow 4G throttling, 4x CPU slowdown) and exits non-zero if any category or
 * the LCP budget is missed, so it can gate CI rather than just report.
 */
import { spawn } from 'node:child_process'
import { existsSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { setTimeout as delay } from 'node:timers/promises'
import lighthouse from 'lighthouse'
import * as chromeLauncher from 'chrome-launcher'

const ROOT = fileURLToPath(new URL('..', import.meta.url))

const MIN_SCORE = Number(process.env.LH_MIN_SCORE ?? 90)
const MAX_LCP_MS = Number(process.env.LH_MAX_LCP_MS ?? 2000)
const PORT = process.env.LH_PORT ?? '3124'
const BASE = process.env.BASE_URL ?? `http://127.0.0.1:${PORT}`
const ROUTES = (process.env.LH_ROUTES ?? '/?v=proof,/?v=hope,/receipts').split(',')

/*
 * Two throttling methods, because they disagree and only one of them reflects
 * a browser.
 *
 *  - `simulate` (Lighthouse's default) runs the page unthrottled and then
 *    models what 4G would have done. The model is pessimistic and its output
 *    moves with the load on the machine running it.
 *  - `devtools` applies real 4G throttling — 1.6 Mbps, 150 ms RTT, 4x CPU —
 *    and measures what actually happened.
 *
 * Category scores are read from the simulated run, since that is what the
 * public Lighthouse score means. The LCP budget is judged on the observed run,
 * because that is the number a person on an Indian 4G connection experiences.
 * Both are printed, so the gap is never hidden.
 */
const METHODS = ['simulate', 'devtools']

function resolveChromium() {
  if (process.env.CHROME_PATH) return process.env.CHROME_PATH
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH ?? '/opt/pw-browsers'
  if (!existsSync(root)) return undefined
  for (const entry of readdirSync(root)) {
    if (!entry.startsWith('chromium-')) continue
    const candidate = join(root, entry, 'chrome-linux', 'chrome')
    if (existsSync(candidate)) return candidate
  }
  return undefined
}

const chromePath = resolveChromium()
if (chromePath) process.env.CHROME_PATH = chromePath

/*
 * A server already listening on this port would be measured silently, and a
 * stale build scoring well is worse than no measurement at all. Refuse to run.
 */
if (!process.env.BASE_URL) {
  try {
    await fetch(`${BASE}/`, { redirect: 'manual', signal: AbortSignal.timeout(1500) })
    console.error(
      `lighthouse ERROR: something is already serving ${BASE}.\n` +
        `Stop it first — measuring a stale build would report scores this build did not earn.`,
    )
    process.exit(1)
  } catch {
    /* nothing listening, which is what we want */
  }
}

let server
if (!process.env.BASE_URL) {
  server = spawn('npx', ['next', 'start', '--port', PORT], {
    cwd: ROOT,
    stdio: ['ignore', 'ignore', 'pipe'],
    env: { ...process.env, NODE_ENV: 'production' },
  })
  server.stderr.on('data', (d) => process.stderr.write(`[next] ${d}`))
  server.on('exit', (code) => {
    if (code && code !== 0) {
      console.error(`lighthouse ERROR: next start exited with code ${code}`)
      process.exit(1)
    }
  })
}

async function waitForServer(timeoutMs = 60_000) {
  const deadline = Date.now() + timeoutMs
  while (Date.now() < deadline) {
    try {
      const res = await fetch(`${BASE}/`, { redirect: 'manual' })
      if (res.status < 500) return
    } catch {
      /* not up yet */
    }
    await delay(500)
  }
  throw new Error(`Server never became ready at ${BASE}`)
}

const CATEGORIES = ['performance', 'accessibility', 'best-practices', 'seo']

let exitCode = 0
let chrome

try {
  await waitForServer()

  /*
   * Warm every route before measuring. A freshly started Node process pays a
   * one-off cost on its first render of each route, and charging that to the
   * first URL measured would report a number no real visitor experiences —
   * and would make the result depend on which route happened to run first.
   */
  for (const route of ROUTES) {
    for (let i = 0; i < 3; i += 1) {
      await fetch(`${BASE}${route}`).then((r) => r.text()).catch(() => {})
    }
  }

  chrome = await chromeLauncher.launch({
    chromeFlags: ['--headless=new', '--no-sandbox', '--disable-dev-shm-usage', '--disable-gpu'],
    chromePath,
  })

  mkdirSync(join(ROOT, '.lighthouse'), { recursive: true })
  const failures = []

  for (const route of ROUTES) {
    const url = `${BASE}${route}`
    const measured = {}

    for (const throttlingMethod of METHODS) {
      const result = await lighthouse(url, {
        port: chrome.port,
        output: 'json',
        logLevel: 'error',
        throttlingMethod,
      })
      const lhr = result.lhr
      const slug = route.replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '') || 'root'
      writeFileSync(join(ROOT, '.lighthouse', `${slug}.${throttlingMethod}.json`), JSON.stringify(lhr, null, 2))
      measured[throttlingMethod] = {
        scores: Object.fromEntries(
          CATEGORIES.map((c) => [c, Math.round((lhr.categories[c]?.score ?? 0) * 100)]),
        ),
        lcp: lhr.audits['largest-contentful-paint']?.numericValue ?? Infinity,
        fcp: lhr.audits['first-contentful-paint']?.numericValue ?? Infinity,
        cls: lhr.audits['cumulative-layout-shift']?.numericValue ?? Infinity,
      }
    }

    const { scores } = measured.simulate
    const observedLcp = measured.devtools.lcp

    console.log(
      `${route.padEnd(14)} ` +
        CATEGORIES.map((c) => `${c}=${scores[c]}`).join('  ') +
        `  LCP(observed)=${Math.round(observedLcp)}ms` +
        `  LCP(modelled)=${Math.round(measured.simulate.lcp)}ms` +
        `  CLS=${measured.devtools.cls}`,
    )

    for (const category of CATEGORIES) {
      if (scores[category] < MIN_SCORE) {
        failures.push(`${route}: ${category} scored ${scores[category]}, needs >= ${MIN_SCORE}`)
      }
    }
    if (observedLcp >= MAX_LCP_MS) {
      failures.push(`${route}: observed LCP ${Math.round(observedLcp)}ms, needs < ${MAX_LCP_MS}ms`)
    }
  }

  if (failures.length) {
    console.error(`\nlighthouse FAILED:\n${failures.map((f) => `  ${f}`).join('\n')}\n`)
    exitCode = 1
  } else {
    console.log(
      `\nlighthouse OK — every category >= ${MIN_SCORE} on the mobile preset, ` +
        `observed LCP < ${MAX_LCP_MS}ms under applied 4G throttling.`,
    )
  }
} catch (err) {
  console.error(`lighthouse ERROR: ${err.message}`)
  exitCode = 1
} finally {
  if (chrome) await chrome.kill()
  if (server && !server.killed) server.kill('SIGTERM')
}

process.exit(exitCode)
