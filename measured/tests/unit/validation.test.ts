import { describe, expect, it } from 'vitest'
import {
  isValidEmail,
  isValidPhone,
  normalizePhone,
  parseWaitlist,
  pickUtm,
} from '@/lib/validation'

const SKUS = ['date', 'office', 'shaadi', 'kit']

describe('email', () => {
  it('accepts ordinary addresses', () => {
    expect(isValidEmail('mohnish@example.com')).toBe(true)
    expect(isValidEmail(' Someone@Example.co.in ')).toBe(true)
  })

  it('rejects malformed addresses', () => {
    for (const bad of ['', 'nope', 'a@b', 'a b@c.com', '@example.com', 'a@.com']) {
      expect(isValidEmail(bad), bad).toBe(false)
    }
  })
})

describe('Indian mobile numbers', () => {
  it('accepts the formats people actually type', () => {
    for (const good of [
      '9876543210',
      '+919876543210',
      '+91 98765 43210',
      '09876543210',
      '98765-43210',
      '(+91) 6123456789',
    ]) {
      expect(isValidPhone(good), good).toBe(true)
    }
  })

  it('rejects numbers that are not Indian mobiles', () => {
    for (const bad of ['1234567890', '5876543210', '98765432', '98765432101', '', '+1 415 555 0100']) {
      expect(isValidPhone(bad), bad).toBe(false)
    }
  })

  it('normalizes everything to E.164 so stored numbers match', () => {
    expect(normalizePhone('+91 98765 43210')).toBe('+919876543210')
    expect(normalizePhone('09876543210')).toBe('+919876543210')
    expect(normalizePhone('9876543210')).toBe('+919876543210')
    expect(normalizePhone('nope')).toBeNull()
  })
})

describe('parseWaitlist', () => {
  it('requires at least one contact method', () => {
    expect(parseWaitlist({}, SKUS)).toEqual({ ok: false, error: 'contactRequired' })
  })

  it('accepts email only', () => {
    const result = parseWaitlist({ email: 'A@Example.com' }, SKUS)
    expect(result).toEqual({
      ok: true,
      value: { email: 'a@example.com', phone: null, sku: null, contactType: 'email' },
    })
  })

  it('accepts phone only', () => {
    const result = parseWaitlist({ phone: '98765 43210' }, SKUS)
    expect(result.ok && result.value.phone).toBe('+919876543210')
    expect(result.ok && result.value.contactType).toBe('phone')
  })

  it('prefers email as the identifier when both are given', () => {
    const result = parseWaitlist({ email: 'a@b.com', phone: '9876543210' }, SKUS)
    expect(result.ok && result.value.contactType).toBe('email')
    expect(result.ok && result.value.phone).toBe('+919876543210')
  })

  it('reports which field is wrong', () => {
    expect(parseWaitlist({ email: 'bad' }, SKUS)).toEqual({ ok: false, error: 'email' })
    expect(parseWaitlist({ phone: '123' }, SKUS)).toEqual({ ok: false, error: 'phone' })
  })

  it('drops an unknown sku rather than storing it', () => {
    const result = parseWaitlist({ email: 'a@b.com', sku: '../../etc/passwd' }, SKUS)
    expect(result.ok && result.value.sku).toBeNull()
  })

  it('keeps a known sku', () => {
    const result = parseWaitlist({ email: 'a@b.com', sku: 'shaadi' }, SKUS)
    expect(result.ok && result.value.sku).toBe('shaadi')
  })

  it('treats a filled honeypot as a bot', () => {
    expect(parseWaitlist({ email: 'a@b.com', company: 'Acme' }, SKUS)).toEqual({
      ok: false,
      error: 'honeypot',
    })
  })
})

describe('utm', () => {
  it('picks only the five utm keys', () => {
    const params = new URLSearchParams('utm_source=meta&utm_medium=cpc&other=x&utm_campaign=launch')
    expect(pickUtm(params)).toEqual({ utm_source: 'meta', utm_medium: 'cpc', utm_campaign: 'launch' })
  })

  it('accepts a plain object and truncates long values', () => {
    expect(pickUtm({ utm_term: 'x'.repeat(400) }).utm_term).toHaveLength(200)
  })
})
