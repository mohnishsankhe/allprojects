import { describe, expect, it } from 'vitest'
import { BRAND, SKUS, streetTestPlanned } from '@/brand.config'
import { COPY } from '@/content/copy'
import { knownTokens, price, t } from '@/content/tokens'
import { CLAIMS, CLAIM_IDS, claim, isLive, visibleClaims } from '@/content/manifest'

/** Walks the whole copy tree so no string escapes the token check. */
function everyString(value: unknown, path = 'COPY'): Array<[string, string]> {
  if (typeof value === 'string') return [[path, value]]
  if (Array.isArray(value)) return value.flatMap((v, i) => everyString(v, `${path}[${i}]`))
  if (value && typeof value === 'object') {
    return Object.entries(value).flatMap(([k, v]) => everyString(v, `${path}.${k}`))
  }
  return []
}

describe('copy tokens', () => {
  it('resolves every token used anywhere in the copy tree', () => {
    for (const [path, text] of everyString(COPY)) {
      expect(() => t(text), `${path}: ${text}`).not.toThrow()
    }
  })

  it('throws on an unknown token rather than shipping a placeholder', () => {
    expect(() => t('Launching {nonsense}.')).toThrow(/Unknown copy token/)
  })

  it('formats prices with Indian digit grouping', () => {
    expect(price(1499)).toBe('₹1,499')
    expect(price(299)).toBe('₹299')
    expect(price(40000)).toBe('₹40,000')
  })

  it('leaves no unresolved braces after interpolation', () => {
    for (const [path, text] of everyString(COPY)) {
      expect(t(text), path).not.toMatch(/\{[a-zA-Z]+\}/)
    }
  })

  it('exposes a token for every brand fact the copy needs', () => {
    expect(knownTokens()).toEqual(expect.arrayContaining(['name', 'launchWindow', 'heroPrice', 'kitPrice']))
  })
})

describe('copy holds no bare numbers', () => {
  // The site's numbers all live in brand.config.ts. This is the unit-level
  // mirror of scripts/check-claims.mjs.
  const CLAIM_SHAPE = /\d+\s*%|\d+\s*°\s*C|₹\s*\d|\d+\s*ml\b|\d+[\s-]*hours?\b|\d+[\s-]*days?\b/i

  it('contains no claim-shaped literal', () => {
    for (const [path, text] of everyString(COPY)) {
      expect(CLAIM_SHAPE.test(text), `${path}: ${text}`).toBe(false)
    }
  })
})

describe('claims manifest', () => {
  it('has the eight entries the brief specifies', () => {
    expect(CLAIMS).toHaveLength(8)
    expect([...CLAIM_IDS]).toEqual([
      'oil-20',
      'climate-test',
      'panel',
      'street-test',
      'invoice',
      'guarantee',
      'names',
      'catalog',
    ])
  })

  it('gives every claim a valid status', () => {
    for (const c of CLAIMS) {
      expect(['MEASURED', 'PLANNED', 'PROVISIONAL']).toContain(c.status)
    }
  })

  it('gives every PLANNED claim a target', () => {
    for (const c of CLAIMS.filter((x) => x.status === 'PLANNED')) {
      expect(c.target, c.id).toBeTruthy()
    }
  })

  it('hides the conditional street-test claim while the flag is off', () => {
    expect(streetTestPlanned).toBe(false)
    expect(isLive(claim('street-test'))).toBe(false)
    expect(visibleClaims().map((c) => c.id)).not.toContain('street-test')
    expect(visibleClaims()).toHaveLength(7)
  })

  it('throws on an unknown claim id rather than rendering an empty chip', () => {
    // @ts-expect-error deliberately outside the ClaimId union
    expect(() => claim('does-not-exist')).toThrow(/Unknown claim id/)
  })
})

describe('catalog', () => {
  it('is capped at four SKUs, which is what the `catalog` claim asserts', () => {
    expect(SKUS).toHaveLength(4)
    expect(claim('catalog').status).toBe('MEASURED')
  })

  it('discloses a concentration for each full-size SKU', () => {
    for (const sku of SKUS.filter((s) => s.sizeMl)) {
      expect(sku.oilPct, sku.id).toBeGreaterThan(0)
    }
  })

  it('keeps every concentration inside the 18-22% band the manifest states', () => {
    for (const sku of SKUS.filter((s) => s.oilPct)) {
      expect(sku.oilPct!).toBeGreaterThanOrEqual(18)
      expect(sku.oilPct!).toBeLessThanOrEqual(22)
    }
  })

  it('names the brand consistently', () => {
    expect(BRAND.name).toBe('MEASURED')
  })
})
