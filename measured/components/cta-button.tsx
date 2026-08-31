'use client'

import type { ReactNode } from 'react'
import { useTrack } from '@/components/variant-provider'
import { WAITLIST_ANCHOR } from '@/lib/anchors'

/**
 * The only reason these are client components: they fire the analytics event
 * and scroll to the single conversion point. Everything around them stays a
 * server component.
 */
export function HeroCta({
  children,
  variantStyle = 'solid',
}: {
  children: ReactNode
  variantStyle?: 'solid' | 'ghost'
}) {
  const track = useTrack()
  const base =
    'inline-flex items-center justify-center rounded-full px-7 py-3.5 text-[0.9375rem] font-medium transition-colors'
  const style =
    variantStyle === 'solid'
      ? 'bg-ink text-paper hover:bg-accent'
      : 'border border-ink-line text-ink hover:border-ink hover:bg-ink-wash'

  return (
    <a
      href={`#${WAITLIST_ANCHOR}`}
      className={`${base} ${style}`}
      onClick={() => track({ name: 'cta_hero_click' })}
    >
      {children}
    </a>
  )
}

export function SkuCta({ sku, children }: { sku: string; children: ReactNode }) {
  const track = useTrack()
  return (
    <a
      href={`#${WAITLIST_ANCHOR}?sku=${encodeURIComponent(sku)}`}
      className="label inline-flex items-center gap-2 text-ink transition-colors hover:text-accent"
      onClick={(e) => {
        e.preventDefault()
        track({ name: 'cta_sku_click', props: { sku } })
        // Pre-tag the form, then bring the visitor to it.
        window.dispatchEvent(new CustomEvent('measured:prefill-sku', { detail: sku }))
        document.getElementById(WAITLIST_ANCHOR)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      }}
    >
      {children}
      <span aria-hidden="true">→</span>
    </a>
  )
}

export function NavCta({ children }: { children: ReactNode }) {
  const track = useTrack()
  return (
    <a
      href={`#${WAITLIST_ANCHOR}`}
      className="rounded-full bg-ink px-4 py-2 text-[0.8125rem] font-medium text-paper transition-colors hover:bg-accent"
      onClick={() => track({ name: 'cta_hero_click' })}
    >
      {children}
    </a>
  )
}
