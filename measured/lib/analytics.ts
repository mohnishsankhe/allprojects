import type { Variant } from './variant'

/**
 * Plausible custom events (§9). Every event carries `variant`, because the
 * experiment's success metric is waitlist_submit rate per variant per unique
 * visitor — an untagged event is a lost data point.
 */
export type AnalyticsEvent =
  | { name: 'hero_view' }
  | { name: 'scroll_50' }
  | { name: 'scroll_90' }
  | { name: 'cta_hero_click' }
  | { name: 'cta_sku_click'; props: { sku: string } }
  | { name: 'receipts_view' }
  | { name: 'empty_reviews_view' }
  | { name: 'faq_open'; props: { q: string } }
  | { name: 'waitlist_submit'; props: { sku?: string; contact_type: 'email' | 'phone' } }

type PlausibleFn = (event: string, options?: { props?: Record<string, string | number | boolean> }) => void

declare global {
  interface Window {
    plausible?: PlausibleFn & { q?: unknown[] }
  }
}

export function track(event: AnalyticsEvent, variant: Variant): void {
  if (typeof window === 'undefined') return
  const props: Record<string, string | number | boolean> = { variant }
  if ('props' in event) {
    for (const [k, v] of Object.entries(event.props)) {
      if (v !== undefined) props[k] = v
    }
  }
  // The inline stub in layout.tsx queues calls made before the script lands,
  // so an early hero_view is never dropped.
  window.plausible?.(event.name, { props })
}

/**
 * Queues events fired before plausible.js loads. Kept identical to the snippet
 * Plausible documents, so behaviour matches when the script arrives.
 */
/**
 * Marks that scripting is available, before first paint. CSS uses it to decide
 * whether an entrance animation should start from a hidden state — so a
 * visitor without JavaScript is never left looking at a collapsed graphic.
 */
export const JS_MARKER = "document.documentElement.classList.add('js')"

export const PLAUSIBLE_STUB =
  'window.plausible=window.plausible||function(){(window.plausible.q=window.plausible.q||[]).push(arguments)}'
