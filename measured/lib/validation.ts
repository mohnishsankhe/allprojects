/**
 * Waitlist input rules. Shared by the form and the route handler so the client
 * and the server never disagree about what is acceptable.
 */

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i

/** Indian mobile numbers: ten digits starting 6–9, with the usual prefixes. */
const PHONE_CLEAN = /[\s()\-.]/g
const PHONE_RE = /^(?:\+?91|0)?([6-9]\d{9})$/

export type ContactType = 'email' | 'phone'

export function isValidEmail(value: string): boolean {
  const v = value.trim()
  return v.length <= 254 && EMAIL_RE.test(v)
}

export function normalizeEmail(value: string): string {
  return value.trim().toLowerCase()
}

export function isValidPhone(value: string): boolean {
  return PHONE_RE.test(value.replace(PHONE_CLEAN, ''))
}

/** Returns E.164, so every stored number looks the same. */
export function normalizePhone(value: string): string | null {
  const match = value.replace(PHONE_CLEAN, '').match(PHONE_RE)
  return match ? `+91${match[1]}` : null
}

export type WaitlistInput = {
  email?: unknown
  phone?: unknown
  sku?: unknown
  /** Bot trap. A real person never fills this in — it is visually hidden. */
  company?: unknown
}

export type WaitlistParsed = {
  email: string | null
  phone: string | null
  sku: string | null
  contactType: ContactType
}

export type WaitlistError =
  | 'contactRequired'
  | 'email'
  | 'phone'
  | 'honeypot'

export type WaitlistResult =
  | { ok: true; value: WaitlistParsed }
  | { ok: false; error: WaitlistError }

const str = (v: unknown): string => (typeof v === 'string' ? v : '')

export function parseWaitlist(input: WaitlistInput, allowedSkus: readonly string[]): WaitlistResult {
  if (str(input.company).trim() !== '') return { ok: false, error: 'honeypot' }

  const rawEmail = str(input.email).trim()
  const rawPhone = str(input.phone).trim()

  if (!rawEmail && !rawPhone) return { ok: false, error: 'contactRequired' }
  if (rawEmail && !isValidEmail(rawEmail)) return { ok: false, error: 'email' }
  if (rawPhone && !isValidPhone(rawPhone)) return { ok: false, error: 'phone' }

  const sku = str(input.sku).trim()

  return {
    ok: true,
    value: {
      email: rawEmail ? normalizeEmail(rawEmail) : null,
      phone: rawPhone ? normalizePhone(rawPhone) : null,
      sku: allowedSkus.includes(sku) ? sku : null,
      // Email is the durable identifier, so it wins when both are given.
      contactType: rawEmail ? 'email' : 'phone',
    },
  }
}

export const UTM_KEYS = [
  'utm_source',
  'utm_medium',
  'utm_campaign',
  'utm_term',
  'utm_content',
] as const

export type UtmParams = Partial<Record<(typeof UTM_KEYS)[number], string>>

export function pickUtm(params: URLSearchParams | Record<string, string | undefined>): UtmParams {
  const get = (k: string) =>
    params instanceof URLSearchParams ? (params.get(k) ?? undefined) : params[k]
  const out: UtmParams = {}
  for (const key of UTM_KEYS) {
    const value = get(key)
    if (value) out[key] = value.slice(0, 200)
  }
  return out
}
