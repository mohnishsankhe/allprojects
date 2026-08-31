import type { Metadata } from 'next'
import Link from 'next/link'
import { BRAND, INVOICE_BENCHMARK } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { STATUS_ORDER, resolveTarget, visibleClaims, type ClaimStatus } from '@/content/manifest'
import { Nav } from '@/components/nav'
import { Footer } from '@/components/footer'
import { ClaimStatusBadge } from '@/components/claim-status-badge'
import { EmptyReviews } from '@/components/empty-reviews'
import { CONTENT_ANCHOR } from '@/lib/anchors'

export const metadata: Metadata = {
  title: `${COPY.receipts.pageTitle} — ${BRAND.name}`,
  description: t(COPY.receipts.pageIntro),
  alternates: { canonical: '/receipts' },
}

export default function ReceiptsPage() {
  const claims = visibleClaims()
  const legend = COPY.receipts.statusLegend

  return (
    <>
      <Nav />
      <main id={CONTENT_ANCHOR} className="px-5 py-16 sm:px-8 sm:py-24 lg:px-12">
        <div className="mx-auto w-full max-w-6xl">
          <h1 className="text-[length:var(--text-section)] font-medium leading-[1.05] tracking-[-0.03em]">
            {COPY.receipts.pageTitle}
          </h1>
          <p className="mt-6 max-w-2xl text-[1.0625rem] leading-relaxed text-ink-muted">
            {t(COPY.receipts.pageIntro)}
          </p>

          <dl className="mt-10 grid gap-4 sm:grid-cols-3">
            {STATUS_ORDER.map((status: ClaimStatus) => (
              <div key={status} className="border border-ink-line p-4">
                <dt>
                  <ClaimStatusBadge status={status} />
                </dt>
                <dd className="mt-3 text-[0.8125rem] leading-relaxed text-ink-muted">{legend[status]}</dd>
              </div>
            ))}
          </dl>

          <ul className="mt-14 border-t border-ink-line">
            {claims.map((entry) => {
              const target = resolveTarget(entry)
              return (
                <li key={entry.id} id={entry.id} className="scroll-mt-24 border-b border-ink-line py-7">
                  <div className="grid gap-4 sm:grid-cols-[10rem_1fr] sm:gap-8">
                    <div className="flex flex-col gap-2">
                      <ClaimStatusBadge status={entry.status} className="self-start" />
                      <code className="num text-[0.75rem] text-ink-soft">#{entry.id}</code>
                    </div>
                    <div>
                      <p className="text-[1.0625rem] leading-snug">{entry.claim}</p>
                      {entry.note ? (
                        <p className="mt-2.5 text-[0.875rem] leading-relaxed text-ink-soft">{entry.note}</p>
                      ) : null}
                      {target ? (
                        <p className="num mt-2.5 text-[0.8125rem] text-ink-soft">
                          <span className="label text-ink-soft">Target</span> {target}
                        </p>
                      ) : null}
                    </div>
                  </div>
                </li>
              )
            })}
          </ul>

          {/*
            The invoice graphic footnote promises "Sources & math on the
            receipts page", so the source lives here. A promise the site does
            not keep would undo the entire positioning.
          */}
          <section id="sources" className="mt-16 scroll-mt-24 border border-ink-line p-6 sm:p-8">
            <h2 className="label text-ink-soft">{COPY.receipts.sourcesHeading}</h2>
            <p className="mt-4 max-w-3xl text-[0.9375rem] leading-relaxed text-ink-muted">
              {INVOICE_BENCHMARK.source}
            </p>
            <ul className="mt-6 grid gap-2 sm:grid-cols-2">
              {INVOICE_BENCHMARK.segments.map((seg) => (
                <li key={seg.id} className="flex items-baseline justify-between gap-4 border-b border-ink-wash py-2">
                  <span className="text-[0.875rem] text-ink-muted">{seg.label}</span>
                  <span className="num text-[0.875rem]">~{seg.pct}%</span>
                </li>
              ))}
            </ul>
          </section>

          <div className="mt-16 max-w-xl">
            <EmptyReviews />
          </div>

          <Link href="/" className="mt-12 inline-block text-[0.875rem] text-ink transition-colors hover:text-accent">
            ← {BRAND.name}
          </Link>
        </div>
      </main>
      <Footer />
    </>
  )
}
