import { describe, expect, it, vi } from 'vitest'

/**
 * Acceptance criterion 7: swapping one config constant repaints the wordmark,
 * the title, the OG card and every copy token.
 *
 * The whole content layer is re-imported against a renamed brand, then the
 * rendered strings are checked for any surviving trace of the old name.
 */
const ALTERNATE = 'PRAMANA'

vi.mock('@/brand.config', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/brand.config')>()
  return { ...actual, BRAND: { ...actual.BRAND, name: ALTERNATE } }
})

const { COPY } = await import('@/content/copy')
const { t } = await import('@/content/tokens')
const { organizationSchema, websiteSchema } = await import('@/lib/seo')
const { BRAND } = await import('@/brand.config')

/**
 * The brand shares its name with one of its own status labels. MEASURED /
 * PLANNED / PROVISIONAL is the manifest's vocabulary and must survive a
 * rename, so a string that lists the statuses together is not a stale brand
 * reference.
 */
function isStatusVocabulary(text: string): boolean {
  return /\bPLANNED\b/i.test(text) && /\bPROVISIONAL\b/i.test(text)
}

function everyString(value: unknown, path = 'COPY'): Array<[string, string]> {
  if (typeof value === 'string') return [[path, value]]
  if (Array.isArray(value)) return value.flatMap((v, i) => everyString(v, `${path}[${i}]`))
  if (value && typeof value === 'object') {
    return Object.entries(value).flatMap(([k, v]) => everyString(v, `${path}.${k}`))
  }
  return []
}

describe('brand name swap', () => {
  it('takes effect through the config', () => {
    expect(BRAND.name).toBe(ALTERNATE)
  })

  it('repaints the page title and meta description', () => {
    expect(t(COPY.seo.title)).toContain(ALTERNATE)
    expect(t(COPY.seo.title)).not.toContain('MEASURED')
  })

  it('repaints the llms.txt summary', () => {
    const lines = COPY.seo.llms.map((line) => t(line))
    expect(lines.join('\n')).toContain(ALTERNATE)
    for (const line of lines) {
      if (isStatusVocabulary(line)) continue
      expect(line).not.toMatch(/\bMEASURED\b/)
    }
  })

  it('repaints structured data', () => {
    expect(organizationSchema().name).toBe(ALTERNATE)
    expect(websiteSchema().name).toBe(ALTERNATE)
    expect(JSON.stringify([organizationSchema(), websiteSchema()])).not.toContain('MEASURED')
  })

  it('leaves no rendered copy string carrying the old brand name', () => {
    for (const [path, text] of everyString(COPY)) {
      const rendered = t(text)
      if (isStatusVocabulary(rendered)) continue
      expect(rendered, `${path}: ${rendered}`).not.toMatch(/\bMEASURED\b/)
    }
  })
})
