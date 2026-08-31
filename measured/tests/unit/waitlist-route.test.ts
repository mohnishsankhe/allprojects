import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { RATE_LIMIT, resetRateLimit } from '@/lib/rate-limit'

const WEBHOOK = 'https://hooks.example.test/waitlist'

vi.mock('@/brand.config', async (importOriginal) => {
  const actual = await importOriginal<typeof import('@/brand.config')>()
  return { ...actual, env: { ...actual.env, waitlistWebhookUrl: WEBHOOK } }
})

const { NextRequest } = await import('next/server')
const { POST, GET } = await import('@/app/api/waitlist/route')

function post(body: unknown, headers: Record<string, string> = {}) {
  return new NextRequest('https://measured.test/api/waitlist', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-forwarded-for': '10.0.0.1', ...headers },
    body: JSON.stringify(body),
  })
}

let fetchMock: ReturnType<typeof vi.fn>

beforeEach(() => {
  resetRateLimit()
  fetchMock = vi.fn(async () => new Response('{"ok":true}', { status: 200 }))
  vi.stubGlobal('fetch', fetchMock)
})

afterEach(() => {
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

describe('POST /api/waitlist', () => {
  it('forwards a valid signup to the webhook', async () => {
    const res = await POST(post({ email: 'Reader@Example.com' }))
    expect(res.status).toBe(200)
    await expect(res.json()).resolves.toMatchObject({ ok: true, contactType: 'email' })
    expect(fetchMock).toHaveBeenCalledTimes(1)

    const [url, init] = fetchMock.mock.calls[0]!
    expect(url).toBe(WEBHOOK)
    const sent = JSON.parse((init as RequestInit).body as string)
    expect(sent.email).toBe('reader@example.com')
    expect(sent.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T/)
  })

  it('carries variant, utm and sku through to the webhook', async () => {
    await POST(
      post(
        {
          email: 'a@b.com',
          sku: 'shaadi',
          utm: { utm_source: 'meta', utm_campaign: 'cold-1', ignored: 'x' },
          referrer: 'https://instagram.com/',
        },
        { cookie: 'variant=hope' },
      ),
    )
    const sent = JSON.parse(fetchMock.mock.calls[0]![1]!.body as string)
    expect(sent.variant).toBe('hope')
    expect(sent.sku).toBe('shaadi')
    expect(sent.utm).toEqual({ utm_source: 'meta', utm_campaign: 'cold-1' })
    expect(sent.referrer).toBe('https://instagram.com/')
  })

  it('takes the variant from the cookie, not the request body', async () => {
    await POST(post({ email: 'a@b.com', variant: 'proof' }, { cookie: 'variant=hope' }))
    const sent = JSON.parse(fetchMock.mock.calls[0]![1]!.body as string)
    expect(sent.variant).toBe('hope')
  })

  it('defaults the variant when no cookie is present', async () => {
    await POST(post({ email: 'a@b.com' }))
    const sent = JSON.parse(fetchMock.mock.calls[0]![1]!.body as string)
    expect(sent.variant).toBe('proof')
  })

  it('rejects a signup with no contact method', async () => {
    const res = await POST(post({}))
    expect(res.status).toBe(400)
    await expect(res.json()).resolves.toMatchObject({ error: 'contactRequired' })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('rejects a malformed email and a non-Indian mobile', async () => {
    await expect((await POST(post({ email: 'nope' }))).json()).resolves.toMatchObject({ error: 'email' })
    await expect((await POST(post({ phone: '12345' }))).json()).resolves.toMatchObject({ error: 'phone' })
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('swallows a honeypot hit without storing anything', async () => {
    const res = await POST(post({ email: 'a@b.com', company: 'Acme Corp' }))
    expect(res.status).toBe(200)
    expect(fetchMock).not.toHaveBeenCalled()
  })

  it('rejects invalid JSON', async () => {
    const bad = new NextRequest('https://measured.test/api/waitlist', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: 'not json',
    })
    expect((await POST(bad)).status).toBe(400)
  })

  it('rate limits a hammering client', async () => {
    for (let i = 0; i < RATE_LIMIT.max; i += 1) {
      expect((await POST(post({ email: `a${i}@b.com` }))).status).toBe(200)
    }
    const blocked = await POST(post({ email: 'over@b.com' }))
    expect(blocked.status).toBe(429)
    expect(blocked.headers.get('Retry-After')).toBeTruthy()
    await expect(blocked.json()).resolves.toMatchObject({ error: 'rateLimited' })
  })

  it('reports a webhook failure instead of claiming success', async () => {
    fetchMock.mockResolvedValueOnce(new Response('nope', { status: 500 }))
    const res = await POST(post({ email: 'a@b.com' }))
    expect(res.status).toBe(502)
    await expect(res.json()).resolves.toMatchObject({ ok: false, error: 'generic' })
  })

  it('reports a network failure instead of claiming success', async () => {
    fetchMock.mockRejectedValueOnce(new Error('ECONNRESET'))
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const res = await POST(post({ email: 'a@b.com' }))
    expect(res.status).toBe(502)
  })

  it('refuses GET', async () => {
    expect((await GET()).status).toBe(405)
  })
})
