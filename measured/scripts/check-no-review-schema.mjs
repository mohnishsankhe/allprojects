#!/usr/bin/env node
/**
 * Acceptance criterion 4: zero review/rating schema in the output HTML.
 *
 * The empty-reviews module is the site's signature move; this check is what
 * makes it true rather than decorative. It scans served HTML rather than
 * .next output because every page route is dynamically rendered (the variant
 * is decided per request), so no static .html is ever emitted.
 *
 * Set BASE_URL to check an already-running server; otherwise this boots
 * `next start` on a free port and shuts it down afterwards.
 */
import { spawn } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import { setTimeout as delay } from 'node:timers/promises'

const ROOT = fileURLToPath(new URL('..', import.meta.url))

const FORBIDDEN = [
  { name: 'aggregateRating', re: /aggregateRating/i },
  { name: 'AggregateRating type', re: /"@type"\s*:\s*"AggregateRating"/i },
  { name: 'Review type', re: /"@type"\s*:\s*"Review"/i },
  { name: 'ratingValue', re: /ratingValue/i },
  { name: 'reviewCount', re: /reviewCount/i },
  { name: 'ratingCount', re: /ratingCount/i },
  { name: 'bestRating', re: /bestRating/i },
  { name: 'worstRating', re: /worstRating/i },
  { name: 'schema.org/Review', re: /schema\.org\/(Review|AggregateRating)/i },
  { name: 'rating microdata', re: /itemprop\s*=\s*["'](?:ratingValue|reviewRating|aggregateRating)/i },
  // Product schema is also barred: a Product node is what search engines
  // attach star ratings to, and the brief rules it out along with reviews.
  { name: 'Product type', re: /"@type"\s*:\s*"Product"/i },
]

const ROUTES = ['/?v=proof', '/?v=hope', '/receipts', '/llms.txt', '/robots.txt', '/sitemap.xml']

const PORT = process.env.CHECK_PORT ?? '3123'
const BASE = process.env.BASE_URL ?? `http://127.0.0.1:${PORT}`
const shouldBoot = !process.env.BASE_URL

let server
if (shouldBoot) {
  server = spawn('npx', ['next', 'start', '--port', PORT], {
    cwd: ROOT,
    stdio: ['ignore', 'pipe', 'pipe'],
    env: { ...process.env, NODE_ENV: 'production' },
  })
  server.stderr.on('data', (d) => process.stderr.write(`[next] ${d}`))
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
  throw new Error(`Server did not become ready at ${BASE} within ${timeoutMs}ms`)
}

function shutdown() {
  if (server && !server.killed) server.kill('SIGTERM')
}

let exitCode = 0
try {
  await waitForServer()
  const failures = []

  for (const route of ROUTES) {
    const res = await fetch(`${BASE}${route}`)
    const body = await res.text()
    if (res.status >= 400) {
      failures.push({ route, name: `HTTP ${res.status}`, excerpt: 'route did not render' })
      continue
    }
    for (const { name, re } of FORBIDDEN) {
      const m = body.match(re)
      if (!m) continue
      const at = body.indexOf(m[0])
      failures.push({ route, name, excerpt: body.slice(Math.max(0, at - 60), at + 60).replace(/\s+/g, ' ') })
    }
  }

  if (failures.length) {
    console.error(`\nschema-check FAILED — review/rating markup found in ${failures.length} place(s):\n`)
    for (const f of failures) {
      console.error(`  ${f.route}  [${f.name}]`)
      console.error(`    …${f.excerpt}…`)
    }
    console.error(
      '\nThis site publishes no ratings until it has earned them. Remove the markup\n' +
        'rather than relaxing this check.\n',
    )
    exitCode = 1
  } else {
    console.log(`schema-check OK — ${ROUTES.length} routes, no review, rating or Product schema.`)
  }
} catch (err) {
  console.error(`schema-check ERROR: ${err.message}`)
  exitCode = 1
} finally {
  shutdown()
}

process.exit(exitCode)
