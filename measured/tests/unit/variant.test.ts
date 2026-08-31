import { describe, expect, it } from 'vitest'
import { DEFAULT_VARIANT, VARIANTS, isVariant, parseVariant, resolveVariant } from '@/lib/variant'

describe('variant resolution', () => {
  it('treats only the two arms as valid', () => {
    expect(VARIANTS).toEqual(['proof', 'hope'])
    expect(isVariant('proof')).toBe(true)
    expect(isVariant('hope')).toBe(true)
    expect(isVariant('control')).toBe(false)
    expect(isVariant(undefined)).toBe(false)
  })

  it('falls back to the default rather than throwing on junk', () => {
    expect(parseVariant(null)).toBe(DEFAULT_VARIANT)
    expect(parseVariant('nonsense')).toBe(DEFAULT_VARIANT)
    expect(parseVariant('hope')).toBe('hope')
  })

  it('lets an explicit ?v= override an existing cookie', () => {
    expect(resolveVariant('hope', 'proof')).toEqual({ variant: 'hope', assigned: true })
    expect(resolveVariant('proof', 'hope')).toEqual({ variant: 'proof', assigned: true })
  })

  it('keeps a returning visitor in their arm', () => {
    expect(resolveVariant(null, 'hope')).toEqual({ variant: 'hope', assigned: false })
    expect(resolveVariant(undefined, 'proof')).toEqual({ variant: 'proof', assigned: false })
  })

  it('ignores an invalid ?v= and honours the cookie instead', () => {
    expect(resolveVariant('banana', 'hope')).toEqual({ variant: 'hope', assigned: false })
  })

  it('assigns a fresh visitor from the draw', () => {
    expect(resolveVariant(null, null, () => 0.2)).toEqual({ variant: 'proof', assigned: true })
    expect(resolveVariant(null, null, () => 0.9)).toEqual({ variant: 'hope', assigned: true })
  })

  it('splits close to 50/50 over many draws', () => {
    let proof = 0
    const draws = 20_000
    for (let i = 0; i < draws; i += 1) {
      // Deterministic sweep across [0,1) rather than a random source, so the
      // assertion cannot flake.
      if (resolveVariant(null, null, () => i / draws).variant === 'proof') proof += 1
    }
    expect(proof / draws).toBeCloseTo(0.5, 2)
  })
})
