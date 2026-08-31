import { beforeEach, describe, expect, it } from 'vitest'
import { RATE_LIMIT, pruneRateLimit, rateLimit, resetRateLimit } from '@/lib/rate-limit'

describe('rate limit', () => {
  beforeEach(() => resetRateLimit())

  it('allows up to the cap inside one window', () => {
    for (let i = 0; i < RATE_LIMIT.max; i += 1) {
      expect(rateLimit('1.2.3.4', 1_000).allowed, `attempt ${i + 1}`).toBe(true)
    }
    expect(rateLimit('1.2.3.4', 1_000).allowed).toBe(false)
  })

  it('counts each client separately', () => {
    for (let i = 0; i < RATE_LIMIT.max + 1; i += 1) rateLimit('1.1.1.1', 1_000)
    expect(rateLimit('1.1.1.1', 1_000).allowed).toBe(false)
    expect(rateLimit('2.2.2.2', 1_000).allowed).toBe(true)
  })

  it('opens a fresh window once the old one expires', () => {
    for (let i = 0; i < RATE_LIMIT.max + 1; i += 1) rateLimit('9.9.9.9', 1_000)
    expect(rateLimit('9.9.9.9', 1_000).allowed).toBe(false)
    expect(rateLimit('9.9.9.9', 1_000 + RATE_LIMIT.windowMs + 1).allowed).toBe(true)
  })

  it('reports how many attempts are left', () => {
    expect(rateLimit('3.3.3.3', 1_000).remaining).toBe(RATE_LIMIT.max - 1)
    expect(rateLimit('3.3.3.3', 1_000).remaining).toBe(RATE_LIMIT.max - 2)
  })

  it('prunes expired buckets so the map cannot grow without bound', () => {
    rateLimit('4.4.4.4', 1_000)
    pruneRateLimit(1_000 + RATE_LIMIT.windowMs + 1)
    // A pruned bucket starts over at full allowance.
    expect(rateLimit('4.4.4.4', 2_000_000).remaining).toBe(RATE_LIMIT.max - 1)
  })
})
