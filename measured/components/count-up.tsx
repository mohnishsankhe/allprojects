'use client'

import { useEffect, useRef, type ReactNode } from 'react'

const DURATION_MS = 900
const FIRST_NUMBER = /\d[\d,]*/

/**
 * Counts the first number in each `[data-countup]` up from zero when the strip
 * scrolls into view.
 *
 * It reads the final text out of the DOM rather than receiving it as a prop,
 * so the measurements stay server-rendered and never enter the client bundle.
 * That also means the true value is on screen before this runs, with no layout
 * shift and nothing to see if JavaScript never arrives.
 */
export function CountUp({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const root = ref.current
    if (!root) return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return

    const targets = [...root.querySelectorAll<HTMLElement>('[data-countup]')]
      .map((node) => {
        const finalText = node.textContent ?? ''
        const match = finalText.match(FIRST_NUMBER)
        if (!match) return null
        const value = Number(match[0].replace(/,/g, ''))
        return Number.isFinite(value) && value > 0 ? { node, finalText, value } : null
      })
      .filter((x): x is { node: HTMLElement; finalText: string; value: number } => x !== null)

    if (!targets.length) return

    let raf = 0
    let start = 0

    const step = (now: number) => {
      if (!start) start = now
      const progress = Math.min(1, (now - start) / DURATION_MS)
      // Ease-out cubic: fast arrival, no bounce. Restrained, per the brief.
      const eased = 1 - Math.pow(1 - progress, 3)
      for (const { node, finalText, value } of targets) {
        node.textContent =
          progress < 1 ? finalText.replace(FIRST_NUMBER, String(Math.round(value * eased))) : finalText
      }
      if (progress < 1) raf = requestAnimationFrame(step)
    }

    const observer = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return
        observer.disconnect()
        raf = requestAnimationFrame(step)
      },
      { threshold: 0.6 },
    )

    observer.observe(root)
    return () => {
      observer.disconnect()
      cancelAnimationFrame(raf)
    }
  }, [])

  return <div ref={ref}>{children}</div>
}
