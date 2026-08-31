/**
 * A fixed-window limiter held in process memory.
 *
 * Honest about what this is: it protects a single Node instance and nothing
 * more. Behind several serverless instances it is best-effort. The real
 * defences against abuse are the honeypot field, the submit-timing check, and
 * whatever limits the receiving webhook enforces — this just stops one script
 * from hammering one box.
 */
type Bucket = { count: number; resetAt: number }

const buckets = new Map<string, Bucket>()

export const RATE_LIMIT = { max: 5, windowMs: 10 * 60 * 1000 }

export function rateLimit(
  key: string,
  now: number = Date.now(),
  config = RATE_LIMIT,
): { allowed: boolean; remaining: number; resetAt: number } {
  const existing = buckets.get(key)

  if (!existing || now >= existing.resetAt) {
    const bucket = { count: 1, resetAt: now + config.windowMs }
    buckets.set(key, bucket)
    return { allowed: true, remaining: config.max - 1, resetAt: bucket.resetAt }
  }

  existing.count += 1
  const allowed = existing.count <= config.max
  return { allowed, remaining: Math.max(0, config.max - existing.count), resetAt: existing.resetAt }
}

/** Test seam, and a way to keep the map from growing without bound. */
export function resetRateLimit(key?: string): void {
  if (key) buckets.delete(key)
  else buckets.clear()
}

export function pruneRateLimit(now: number = Date.now()): void {
  for (const [key, bucket] of buckets) {
    if (now >= bucket.resetAt) buckets.delete(key)
  }
}
