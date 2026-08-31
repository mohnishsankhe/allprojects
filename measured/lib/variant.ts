/**
 * The A/B system. `proof` is the hypothesis, `hope` is the control.
 *
 * Assignment happens once, in proxy.ts, and reaches the page as a request
 * header. Nothing downstream re-derives it, so a visitor sees exactly one
 * variant and every analytics event carries the same value the page rendered.
 */

export const VARIANTS = ['proof', 'hope'] as const
export type Variant = (typeof VARIANTS)[number]

export const DEFAULT_VARIANT: Variant = 'proof'

export const VARIANT_COOKIE = 'variant'
export const VARIANT_HEADER = 'x-measured-variant'
export const VARIANT_PARAM = 'v'

/** 180 days: long enough that a returning visitor stays in their arm. */
export const VARIANT_COOKIE_MAX_AGE = 60 * 60 * 24 * 180

export function isVariant(value: unknown): value is Variant {
  return typeof value === 'string' && (VARIANTS as readonly string[]).includes(value)
}

/** Narrows an untrusted value, falling back to the default rather than throwing. */
export function parseVariant(value: string | null | undefined): Variant {
  return isVariant(value) ? value : DEFAULT_VARIANT
}

/**
 * Resolution order: an explicit ?v= wins (so a campaign or a QA link can force
 * an arm), then the existing cookie, then a fresh 50/50 draw.
 *
 * `random` is injected so the split is testable without stubbing globals.
 */
export function resolveVariant(
  param: string | null | undefined,
  cookie: string | null | undefined,
  random: () => number = Math.random,
): { variant: Variant; assigned: boolean } {
  if (isVariant(param)) return { variant: param, assigned: true }
  if (isVariant(cookie)) return { variant: cookie, assigned: false }
  return { variant: random() < 0.5 ? 'proof' : 'hope', assigned: true }
}

export const variantCookieOptions = {
  path: '/',
  maxAge: VARIANT_COOKIE_MAX_AGE,
  sameSite: 'lax',
  httpOnly: true,
} as const
