import raw from './claims-manifest.json'
import { streetTestPlanned, eventWindow } from '@/brand.config'

export type ClaimStatus = 'MEASURED' | 'PLANNED' | 'PROVISIONAL'

export type Claim = {
  id: string
  claim: string
  status: ClaimStatus
  note?: string
  target?: string
  /** Name of a brand.config flag that gates whether this claim is live at all. */
  conditional?: string
}

export const CLAIMS: readonly Claim[] = raw as readonly Claim[]

export const CLAIM_IDS = new Set(CLAIMS.map((c) => c.id))

/**
 * Every claim id, as a union. A typo in a claimId is a type error, not just a
 * lint failure.
 */
export type ClaimId =
  | 'oil-20'
  | 'climate-test'
  | 'panel'
  | 'street-test'
  | 'invoice'
  | 'guarantee'
  | 'names'
  | 'catalog'

const FLAGS: Record<string, boolean> = {
  streetTestPlanned,
}

/** A claim is live only if it has no conditional, or its flag is on. */
export function isLive(c: Claim): boolean {
  if (!c.conditional) return true
  return FLAGS[c.conditional] === true
}

/**
 * The claims the site is allowed to show today. A conditional claim whose flag
 * is off does not render anywhere — not on the landing page, not on /receipts.
 */
export function visibleClaims(): readonly Claim[] {
  return CLAIMS.filter(isLive)
}

/** Lookup that throws rather than silently rendering an empty status chip. */
export function claim(id: ClaimId): Claim {
  const found = CLAIMS.find((c) => c.id === id)
  if (!found) throw new Error(`Unknown claim id: ${id}. Every claim must exist in claims-manifest.json.`)
  return found
}

/**
 * Manifest targets may point at config rather than carry a literal date, so a
 * date never gets hardcoded into the manifest before it is known.
 */
export function resolveTarget(c: Claim): string | undefined {
  if (!c.target) return undefined
  if (c.target === 'config.eventWindow') return eventWindow || undefined
  return c.target
}

export const STATUS_ORDER: readonly ClaimStatus[] = ['MEASURED', 'PLANNED', 'PROVISIONAL']
