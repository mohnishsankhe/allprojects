'use client'

import { useEffect, useId, useRef, useState } from 'react'
import { useTrack } from '@/components/variant-provider'
import { UTM_KEYS, isValidEmail, isValidPhone } from '@/lib/validation'
import { WAITLIST_ANCHOR } from '@/lib/anchors'

type Status = 'idle' | 'busy' | 'done'

/**
 * Every string and every SKU arrives as a prop, already interpolated on the
 * server. That keeps the copy tree and brand config out of the client bundle —
 * this component ships form behaviour, not content.
 */
export type WaitlistCopy = {
  heading: string
  sub: string
  emailLabel: string
  phoneLabel: string
  emailPlaceholder: string
  phonePlaceholder: string
  skuLabel: string
  skuNone: string
  button: string
  buttonBusy: string
  success: string
  errors: Record<string, string>
}

export type WaitlistSku = { id: string; name: string }

type ErrorKey = string

function readUtm(): Record<string, string> {
  if (typeof window === 'undefined') return {}
  const params = new URLSearchParams(window.location.search)
  const out: Record<string, string> = {}
  for (const key of UTM_KEYS) {
    const value = params.get(key)
    if (value) out[key] = value
  }
  return out
}

export function WaitlistForm({ copy, skus }: { copy: WaitlistCopy; skus: readonly WaitlistSku[] }) {
  const track = useTrack()
  const ids = useId()

  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [sku, setSku] = useState('')
  const [status, setStatus] = useState<Status>('idle')
  const [error, setError] = useState<ErrorKey | null>(null)
  const mountedAt = useRef(0)
  const honeypot = useRef<HTMLInputElement>(null)

  useEffect(() => {
    mountedAt.current = Date.now()
    const onPrefill = (e: Event) => {
      const detail = (e as CustomEvent<string>).detail
      if (skus.some((s) => s.id === detail)) setSku(detail)
    }
    window.addEventListener('measured:prefill-sku', onPrefill)
    return () => window.removeEventListener('measured:prefill-sku', onPrefill)
  }, [skus])

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    if (status === 'busy') return

    const hasEmail = email.trim() !== ''
    const hasPhone = phone.trim() !== ''

    if (!hasEmail && !hasPhone) return setError('contactRequired')
    if (hasEmail && !isValidEmail(email)) return setError('email')
    if (hasPhone && !isValidPhone(phone)) return setError('phone')

    setError(null)
    setStatus('busy')

    try {
      const res = await fetch('/api/waitlist', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({
          email: hasEmail ? email : undefined,
          phone: hasPhone ? phone : undefined,
          sku: sku || undefined,
          company: honeypot.current?.value ?? '',
          utm: readUtm(),
          referrer: typeof document !== 'undefined' ? document.referrer : undefined,
          // A form completed in under a second was not completed by a person.
          elapsedMs: Date.now() - mountedAt.current,
        }),
      })

      const data = (await res.json().catch(() => ({}))) as { ok?: boolean; error?: ErrorKey }

      if (!res.ok || !data.ok) {
        setError(data.error && data.error in copy.errors ? data.error : 'generic')
        setStatus('idle')
        return
      }

      track({
        name: 'waitlist_submit',
        props: { sku: sku || undefined, contact_type: hasEmail ? 'email' : 'phone' },
      })
      setStatus('done')
    } catch {
      setError('generic')
      setStatus('idle')
    }
  }

  if (status === 'done') {
    return (
      <div
        role="status"
        aria-live="polite"
        className="border border-accent/30 bg-accent/[0.05] p-7 sm:p-9"
        data-testid="waitlist-success"
      >
        <p className="max-w-xl text-[1.0625rem] leading-relaxed">{copy.success}</p>
      </div>
    )
  }

  return (
    <form onSubmit={onSubmit} noValidate className="max-w-xl" data-testid="waitlist-form">
      <h2 id={`${WAITLIST_ANCHOR}-heading`} className="text-[length:var(--text-section)] font-medium leading-[1.05] tracking-[-0.03em]">
        {copy.heading}
      </h2>
      <p className="mt-5 text-[0.9375rem] leading-relaxed text-ink-muted">{copy.sub}</p>

      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <label className="flex flex-col gap-2">
          <span className="label text-ink-soft">{copy.emailLabel}</span>
          <input
            id={`${ids}-email`}
            type="email"
            inputMode="email"
            autoComplete="email"
            value={email}
            placeholder={copy.emailPlaceholder}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full border border-ink-line bg-paper px-3.5 py-3 text-[0.9375rem] placeholder:text-ink-soft focus:border-ink focus:outline-none"
          />
        </label>

        <label className="flex flex-col gap-2">
          <span className="label text-ink-soft">{copy.phoneLabel}</span>
          <input
            id={`${ids}-phone`}
            type="tel"
            inputMode="tel"
            autoComplete="tel"
            value={phone}
            placeholder={copy.phonePlaceholder}
            onChange={(e) => setPhone(e.target.value)}
            className="num w-full border border-ink-line bg-paper px-3.5 py-3 text-[0.9375rem] placeholder:text-ink-soft focus:border-ink focus:outline-none"
          />
        </label>
      </div>

      <label className="mt-4 flex flex-col gap-2">
        <span className="label text-ink-soft">{copy.skuLabel}</span>
        <select
          id={`${ids}-sku`}
          value={sku}
          onChange={(e) => setSku(e.target.value)}
          className="w-full border border-ink-line bg-paper px-3.5 py-3 text-[0.9375rem] focus:border-ink focus:outline-none"
        >
          <option value="">{copy.skuNone}</option>
          {skus.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name}
            </option>
          ))}
        </select>
      </label>

      {/* Bot trap. Hidden from people and from assistive technology alike. */}
      <div aria-hidden="true" className="absolute left-[-9999px] h-0 w-0 overflow-hidden">
        <label>
          Company
          <input ref={honeypot} type="text" name="company" tabIndex={-1} autoComplete="off" />
        </label>
      </div>

      <button
        type="submit"
        disabled={status === 'busy'}
        className="mt-7 inline-flex items-center justify-center rounded-full bg-ink px-8 py-3.5 text-[0.9375rem] font-medium text-paper transition-colors hover:bg-accent disabled:opacity-60"
      >
        {status === 'busy' ? copy.buttonBusy : copy.button}
      </button>

      {error ? (
        <p role="alert" data-testid="waitlist-error" className="mt-4 text-[0.875rem] text-status-planned">
          {copy.errors[error]}
        </p>
      ) : null}
    </form>
  )
}
