'use client'

import { createContext, useContext, type ReactNode } from 'react'
import { DEFAULT_VARIANT, type Variant } from '@/lib/variant'
import { track, type AnalyticsEvent } from '@/lib/analytics'

const VariantContext = createContext<Variant>(DEFAULT_VARIANT)

/**
 * Receives the variant as a prop from the server. The client never reads the
 * cookie, so what analytics reports and what the visitor saw cannot diverge.
 */
export function VariantProvider({ variant, children }: { variant: Variant; children: ReactNode }) {
  return <VariantContext.Provider value={variant}>{children}</VariantContext.Provider>
}

export function useVariant(): Variant {
  return useContext(VariantContext)
}

/** Every component that fires an event goes through here, so none can forget the variant tag. */
export function useTrack(): (event: AnalyticsEvent) => void {
  const variant = useVariant()
  return (event: AnalyticsEvent) => track(event, variant)
}
