import Link from 'next/link'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { resolveTarget, visibleClaims } from '@/content/manifest'
import { Section, SectionLabel } from '@/components/section'
import { EmptyReviews } from '@/components/empty-reviews'
import { ClaimStatusBadge } from '@/components/claim-status-badge'

/** The receipts table and the empty reviews module, side by side. */
export function ReceiptsPreview() {
  const claims = visibleClaims()

  return (
    <Section id="receipts" labelledBy="receipts-heading" className="py-20 sm:py-28">
      <div className="grid gap-10 lg:grid-cols-2 lg:gap-12">
        <div>
          <SectionLabel>{COPY.receipts.previewHeading}</SectionLabel>
          <h2 id="receipts-heading" className="sr-only">
            {COPY.receipts.previewHeading}
          </h2>

          <ul className="mt-6 border-t border-ink-line">
            {claims.map((entry) => {
              const target = resolveTarget(entry)
              return (
                <li key={entry.id} className="border-b border-ink-line py-4">
                  <Link href={`/receipts#${entry.id}`} className="group flex flex-col gap-2.5">
                    <span className="text-[0.9375rem] leading-snug text-ink-muted transition-colors group-hover:text-ink">
                      {entry.claim}
                    </span>
                    <span className="flex flex-wrap items-center gap-2.5">
                      <ClaimStatusBadge status={entry.status} />
                      {target ? <span className="num text-[0.75rem] text-ink-soft">{target}</span> : null}
                    </span>
                  </Link>
                </li>
              )
            })}
          </ul>

          <Link
            href="/receipts"
            className="mt-6 inline-block text-[0.875rem] text-ink transition-colors hover:text-accent"
          >
            {t(COPY.receipts.fullManifestLink)}
          </Link>
        </div>

        <EmptyReviews />
      </div>
    </Section>
  )
}
