'use client'

import { useEffect } from 'react'
import { useTrack } from '@/components/variant-provider'

/**
 * Fires the view and scroll events (§9). No UI, so it costs nothing visually
 * and nothing at LCP. Each observer disconnects after its one event, because
 * the experiment counts visitors, not impressions.
 */
export function Analytics() {
  const track = useTrack()

  useEffect(() => {
    const cleanups: Array<() => void> = []

    const onceInView = (selector: string, fire: () => void) => {
      const node = document.querySelector(selector)
      if (!node) return
      const observer = new IntersectionObserver(
        (entries) => {
          if (!entries.some((e) => e.isIntersecting)) return
          observer.disconnect()
          fire()
        },
        { threshold: 0.35 },
      )
      observer.observe(node)
      cleanups.push(() => observer.disconnect())
    }

    onceInView('[data-section="hero"]', () => track({ name: 'hero_view' }))
    onceInView('[data-section="receipts"]', () => track({ name: 'receipts_view' }))
    onceInView('[data-testid="empty-reviews"]', () => track({ name: 'empty_reviews_view' }))

    let fired50 = false
    let fired90 = false
    let ticking = false

    const onScroll = () => {
      if (ticking) return
      ticking = true
      requestAnimationFrame(() => {
        ticking = false
        const scrollable = document.documentElement.scrollHeight - window.innerHeight
        if (scrollable <= 0) return
        const depth = (window.scrollY / scrollable) * 100
        if (!fired50 && depth >= 50) {
          fired50 = true
          track({ name: 'scroll_50' })
        }
        if (!fired90 && depth >= 90) {
          fired90 = true
          track({ name: 'scroll_90' })
          window.removeEventListener('scroll', onScroll)
        }
      })
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    cleanups.push(() => window.removeEventListener('scroll', onScroll))

    return () => cleanups.forEach((fn) => fn())
  }, [track])

  return null
}
