import Link from 'next/link'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { claim } from '@/content/manifest'
import { CountUp } from '@/components/count-up'

/**
 * Server-rendered: the final measurements are in the HTML, so they are correct
 * before any JavaScript runs and correct without it. CountUp adds the
 * scroll-triggered animation on top without shipping this copy to the client.
 */
export function StatsStrip() {
  return (
    <div className="border-y border-ink-wash bg-ink-wash/40">
      <CountUp>
        <ul className="mx-auto grid w-full max-w-6xl gap-px px-5 sm:grid-cols-3 sm:px-8 lg:px-12">
          {COPY.stats.map((stat) => {
            const entry = claim(stat.claimId)
            return (
              <li key={stat.claimId} className="py-4 sm:py-5">
                <Link
                  href={`/receipts#${entry.id}`}
                  className="dotted-underline block text-[0.9375rem] text-ink-muted transition-colors hover:text-ink"
                >
                  <span className="num" data-countup>
                    {t(stat.text)}
                  </span>
                </Link>
              </li>
            )
          })}
        </ul>
      </CountUp>
    </div>
  )
}
