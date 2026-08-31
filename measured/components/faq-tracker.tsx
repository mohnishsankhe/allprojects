'use client'

import { useEffect, useRef, type ReactNode } from 'react'
import { useTrack } from '@/components/variant-provider'

/**
 * One delegated `toggle` listener over server-rendered <details> elements.
 * Holding the children as an RSC payload keeps the FAQ text out of the client
 * bundle entirely — this component ships a listener, not the content.
 */
export function FaqTracker({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null)
  const track = useTrack()

  useEffect(() => {
    const node = ref.current
    if (!node) return

    const onToggle = (event: Event) => {
      const target = event.target as HTMLDetailsElement
      if (target.tagName !== 'DETAILS' || !target.open) return
      const question = target.querySelector('summary')?.textContent?.replace(/\+$/, '').trim()
      if (question) track({ name: 'faq_open', props: { q: question } })
    }

    // `toggle` does not bubble, so it is captured instead of delegated.
    node.addEventListener('toggle', onToggle, true)
    return () => node.removeEventListener('toggle', onToggle, true)
  }, [track])

  return (
    <div ref={ref} className="mt-6 border-t border-ink-line">
      {children}
    </div>
  )
}
