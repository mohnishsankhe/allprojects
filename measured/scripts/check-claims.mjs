#!/usr/bin/env node
/**
 * Acceptance criterion 3: "no untagged number claims in JSX".
 *
 * The rule this enforces is stricter and simpler than a grep for tagged
 * strings: a claim-shaped number may appear ONLY in brand.config.ts and
 * claims-manifest.json. Everywhere else — copy.ts, components, app routes —
 * numbers arrive as {tokens} or as config reads, so a price can never drift
 * between the config and the page, and a stray "20%" typed into a component
 * fails the build.
 *
 * It also checks the manifest wiring in both directions: every claimId the
 * site references must exist, and every manifest entry must actually be
 * referenced (or be conditional-and-disabled), so a claim cannot rot unused.
 */
import { readFileSync, readdirSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = fileURLToPath(new URL('..', import.meta.url))

/** Files allowed to contain raw claim numbers. These are the sources of truth. */
const NUMBER_SOURCES = new Set(['brand.config.ts', 'content/claims-manifest.json'])

const SCAN_DIRS = ['app', 'components', 'content', 'lib']
const SCAN_EXT = /\.(ts|tsx)$/

/**
 * Claim shapes. Anything a visitor would read as a measurement, a price, a
 * concentration or a duration.
 */
const CLAIM_PATTERNS = [
  { name: 'percentage', re: /\d+\s*%/g },
  { name: 'temperature', re: /\d+\s*°\s*C/g },
  { name: 'humidity', re: /\d+\s*%?\s*RH\b/g },
  { name: 'price', re: /₹\s*\d/g },
  { name: 'volume', re: /\d+\s*ml\b/gi },
  { name: 'duration-hours', re: /\d+[\s-]*hours?\b/gi },
  { name: 'duration-days', re: /\d+[\s-]*days?\b/gi },
]

const PRAGMA = /claims-lint-ok:\s*(.+)$/

/** Comment-only lines are never rendered, so they are not visitor-facing text. */
const COMMENT_LINE = /^\s*(\/\/|\/\*|\*\/|\*)/

/**
 * CSS values are not claims. `width: '100%'` in a style object is layout, not
 * a measurement a visitor reads as a fact about the product.
 */
const CSS_CONTEXT =
  /\b(width|height|top|left|right|bottom|inset|margin|padding|flex|flexBasis|basis|gap|transform|translate|scale|opacity|size|lineHeight|fontSize|letterSpacing|borderRadius|maxWidth|minWidth|maxHeight|minHeight)\s*:/

function walk(dir, out = []) {
  let entries
  try {
    entries = readdirSync(dir)
  } catch {
    return out
  }
  for (const entry of entries) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) walk(full, out)
    else if (SCAN_EXT.test(entry)) out.push(full)
  }
  return out
}

const failures = []
const allowed = []

for (const dir of SCAN_DIRS) {
  for (const file of walk(join(ROOT, dir))) {
    const rel = relative(ROOT, file).replaceAll('\\', '/')
    if (NUMBER_SOURCES.has(rel)) continue
    const lines = readFileSync(file, 'utf8').split('\n')
    lines.forEach((line, i) => {
      if (COMMENT_LINE.test(line)) return
      if (CSS_CONTEXT.test(line)) return
      const pragma = line.match(PRAGMA)
      for (const { name, re } of CLAIM_PATTERNS) {
        re.lastIndex = 0
        const hits = line.match(re)
        if (!hits) continue
        if (pragma) {
          allowed.push(`${rel}:${i + 1}  ${hits.join(', ')}  — ${pragma[1].trim()}`)
          continue
        }
        failures.push({ file: rel, line: i + 1, kind: name, match: hits.join(', '), text: line.trim() })
      }
    })
  }
}

// brand.config.ts is the only place numbers live, so confirm it actually does.
const configText = readFileSync(join(ROOT, 'brand.config.ts'), 'utf8')
if (!/heroPrice:\s*\d+/.test(configText)) {
  failures.push({
    file: 'brand.config.ts',
    line: 0,
    kind: 'config',
    match: 'heroPrice',
    text: 'brand.config.ts must define the prices the site renders.',
  })
}

// Manifest wiring, both directions.
const manifest = JSON.parse(readFileSync(join(ROOT, 'content/claims-manifest.json'), 'utf8'))
const manifestIds = new Set(manifest.map((c) => c.id))
const VALID_STATUS = new Set(['MEASURED', 'PLANNED', 'PROVISIONAL'])

for (const entry of manifest) {
  if (!VALID_STATUS.has(entry.status)) {
    failures.push({
      file: 'content/claims-manifest.json',
      line: 0,
      kind: 'status',
      match: entry.status,
      text: `Claim "${entry.id}" has status ${entry.status}; must be MEASURED, PLANNED or PROVISIONAL.`,
    })
  }
}

const referenced = new Set()
// Matches claimId:'x', labelClaimId:'x', commitmentClaimId:'x', claim('x'), claimId={'x'}
const CLAIM_REF = /[A-Za-z]*[Cc]laimId[:=]\s*\{?'([^']+)'|\bclaim\('([^']+)'\)/g
for (const dir of SCAN_DIRS) {
  for (const file of walk(join(ROOT, dir))) {
    const text = readFileSync(file, 'utf8')
    let m
    CLAIM_REF.lastIndex = 0
    while ((m = CLAIM_REF.exec(text))) {
      const id = m[1] ?? m[2]
      if (!id) continue
      referenced.add(id)
      if (!manifestIds.has(id)) {
        failures.push({
          file: relative(ROOT, file).replaceAll('\\', '/'),
          line: 0,
          kind: 'unknown-claim',
          match: id,
          text: `References claimId "${id}", which is not in claims-manifest.json.`,
        })
      }
    }
  }
}

const conditionalOff = new Set(
  manifest.filter((c) => c.conditional && !isFlagOn(c.conditional)).map((c) => c.id),
)

function isFlagOn(flag) {
  const m = configText.match(new RegExp(`export const ${flag}\\s*=\\s*(true|false)`))
  return m ? m[1] === 'true' : false
}

for (const entry of manifest) {
  if (referenced.has(entry.id)) continue
  if (conditionalOff.has(entry.id)) continue
  failures.push({
    file: 'content/claims-manifest.json',
    line: 0,
    kind: 'orphan-claim',
    match: entry.id,
    text: `Claim "${entry.id}" is in the manifest but nothing on the site references it.`,
  })
}

if (allowed.length) {
  console.log(`claims-lint: ${allowed.length} explicitly allowed literal(s):`)
  for (const a of allowed) console.log(`  ${a}`)
}

if (failures.length) {
  console.error(`\nclaims-lint FAILED — ${failures.length} problem(s):\n`)
  for (const f of failures) {
    console.error(`  ${f.file}:${f.line}  [${f.kind}]  ${f.match}`)
    console.error(`    ${f.text}`)
  }
  console.error(
    '\nEvery number a visitor reads must come from brand.config.ts via a {token}.\n' +
      'If a literal is genuinely not a claim, annotate the line with:  // claims-lint-ok: <reason>\n',
  )
  process.exit(1)
}

console.log(
  `claims-lint OK — ${manifest.length} manifest claims, ${referenced.size} referenced, ` +
    `${conditionalOff.size} conditional and disabled, 0 stray literals.`,
)
