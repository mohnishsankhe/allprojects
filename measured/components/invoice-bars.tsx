import Link from 'next/link'
import { INVOICE_BENCHMARK, INVOICE_COMMITMENT } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { StatusChip } from '@/components/status-chip'
import { SectionLabel } from '@/components/section'
import { InView } from '@/components/in-view'

type Segment = { id: string; label: string; pct: number; highlight?: boolean; floor?: boolean }

/**
 * Two stacked bars, filled on scroll.
 *
 * Widths are inline styles present in the server HTML, so with JavaScript off
 * the bars are already correct and to scale. The collapsed starting state
 * lives in CSS behind the `js` class, and InView only flips one attribute — so
 * the whole graphic is server-rendered and costs nothing at LCP.
 */
function Bar({ segments }: { segments: readonly Segment[] }) {
  return (
    <>
      <div className="flex h-11 w-full overflow-hidden rounded-sm border border-ink-line">
        {segments.map((seg) => (
          <div
            key={seg.id}
            style={{ width: `${seg.pct}%` }}
            className={`bar-seg h-full border-r border-paper/70 last:border-r-0 ${
              seg.highlight ? 'bg-accent' : 'bg-ink-line'
            }`}
            aria-hidden="true"
          />
        ))}
      </div>
      <dl className="mt-4 grid grid-cols-1 gap-x-6 gap-y-2 sm:grid-cols-2 lg:grid-cols-3">
        {segments.map((seg) => (
          <div key={seg.id} className="flex items-baseline gap-1.5">
            <span
              aria-hidden="true"
              className={`size-2 shrink-0 translate-y-[-0.1em] rounded-[1px] ${
                seg.highlight ? 'bg-accent' : 'bg-ink-line'
              }`}
            />
            <dt className="text-[0.8125rem] text-ink-muted">{seg.label}</dt>
            <dd className={`num text-[0.8125rem] font-medium ${seg.highlight ? 'text-accent' : 'text-ink'}`}>
              {seg.floor ? '≥' : '~'}
              {seg.pct}%
            </dd>
          </div>
        ))}
      </dl>
    </>
  )
}

export function InvoiceBars() {
  const { invoice } = COPY

  return (
    <section
      id="invoice"
      data-section="invoice"
      aria-labelledby="invoice-heading"
      className="scroll-mt-16 px-5 py-20 sm:px-8 sm:py-28 lg:px-12"
    >
      <InView>
        <SectionLabel>{invoice.label}</SectionLabel>
        <h2
          id="invoice-heading"
          className="num mt-5 max-w-3xl text-[length:var(--text-section)] font-medium leading-[1.04] tracking-[-0.03em]"
        >
          {t(invoice.heading)}
        </h2>

        <div className="mt-12 space-y-12 sm:mt-14 sm:space-y-14">
          <div>
            <p className="label mb-3.5 text-ink-soft">{t(invoice.categoryLabel)}</p>
            <Bar segments={INVOICE_BENCHMARK.segments} />
            <p className="mt-4 max-w-xl text-[0.8125rem] leading-relaxed text-ink-soft">
              {t(invoice.categoryFootnote)}{' '}
              <Link href="/receipts#sources" className="dotted-underline hover:text-ink">
                {t(invoice.categoryFootnoteLink)}
              </Link>
            </p>
          </div>

          <div>
            <p className="label mb-3.5 text-ink-soft">{t(invoice.commitmentLabel)}</p>
            <Bar segments={INVOICE_COMMITMENT.segments} />
            <p className="mt-4 flex flex-wrap items-center gap-x-3 gap-y-2 text-[0.8125rem] leading-relaxed text-ink-soft">
              <span className="max-w-xl">{t(invoice.commitmentFootnote)}</span>
              <StatusChip claimId={invoice.commitmentClaimId} />
            </p>
          </div>
        </div>
      </InView>
    </section>
  )
}
