import { NextResponse, type NextRequest } from 'next/server'
import { SKUS, env } from '@/brand.config'
import { parseWaitlist, pickUtm, type UtmParams } from '@/lib/validation'
import { pruneRateLimit, rateLimit } from '@/lib/rate-limit'
import { VARIANT_COOKIE, parseVariant } from '@/lib/variant'

export const runtime = 'nodejs'
export const dynamic = 'force-dynamic'

const ALLOWED_SKUS = SKUS.map((s) => s.id)

/** Trust order matches how this is likely to be deployed: proxy first, then socket. */
function clientIp(request: NextRequest): string {
  const forwarded = request.headers.get('x-forwarded-for')
  if (forwarded) return forwarded.split(',')[0]!.trim()
  return request.headers.get('x-real-ip') ?? 'unknown'
}

type Payload = {
  email: string | null
  phone: string | null
  sku: string | null
  contactType: 'email' | 'phone'
  variant: string
  utm: UtmParams
  referrer: string | null
  timestamp: string
}

export async function POST(request: NextRequest) {
  let body: unknown
  try {
    body = await request.json()
  } catch {
    return NextResponse.json({ ok: false, error: 'generic' }, { status: 400 })
  }

  const input = (body ?? {}) as Record<string, unknown>
  const parsed = parseWaitlist(input, ALLOWED_SKUS)

  if (!parsed.ok) {
    // A honeypot hit is a bot. Return the shape of success so it stops
    // probing, but store nothing.
    if (parsed.error === 'honeypot') return NextResponse.json({ ok: true })
    return NextResponse.json({ ok: false, error: parsed.error }, { status: 400 })
  }

  pruneRateLimit()
  const limit = rateLimit(clientIp(request))
  if (!limit.allowed) {
    return NextResponse.json(
      { ok: false, error: 'rateLimited' },
      { status: 429, headers: { 'Retry-After': String(Math.ceil((limit.resetAt - Date.now()) / 1000)) } },
    )
  }

  // The variant comes from the cookie, not the request body, so a submission
  // cannot be attributed to the wrong arm by a client that lies about it.
  const variant = parseVariant(request.cookies.get(VARIANT_COOKIE)?.value)

  const utmFromBody = typeof input.utm === 'object' && input.utm ? (input.utm as Record<string, string>) : {}

  const payload: Payload = {
    ...parsed.value,
    contactType: parsed.value.contactType,
    variant,
    utm: pickUtm(utmFromBody),
    referrer: typeof input.referrer === 'string' ? input.referrer.slice(0, 500) : null,
    timestamp: new Date().toISOString(),
  }

  if (!env.waitlistWebhookUrl) {
    console.warn('[waitlist] WAITLIST_WEBHOOK_URL is not set; signup was not stored.')
    return NextResponse.json({ ok: false, error: 'notConfigured' }, { status: 503 })
  }

  try {
    const res = await fetch(env.waitlistWebhookUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/json', accept: 'application/json' },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(8000),
    })
    if (!res.ok) {
      console.error(`[waitlist] webhook responded ${res.status}`)
      return NextResponse.json({ ok: false, error: 'generic' }, { status: 502 })
    }
  } catch (err) {
    console.error('[waitlist] webhook request failed', err)
    return NextResponse.json({ ok: false, error: 'generic' }, { status: 502 })
  }

  return NextResponse.json({ ok: true, contactType: payload.contactType, sku: payload.sku })
}

export async function GET() {
  return NextResponse.json({ ok: false, error: 'generic' }, { status: 405 })
}
