import { SKUS, type Sku, type SkuId } from '@/brand.config'
import { COPY } from '@/content/copy'
import { skuPrice, t } from '@/content/tokens'
import { Section, SectionLabel } from '@/components/section'
import { StatusChip } from '@/components/status-chip'
import { SkuCta } from '@/components/cta-button'
import type { ClaimId } from '@/content/manifest'

type CardCopy = {
  promise: string
  body: string
  small: string | null
  claimId: ClaimId | null
}

/** Specimen label, not a product shot: index number, thin rules, small caps. */
function SkuCard({ sku, copy }: { sku: Sku; copy: CardCopy }) {
  const spec = [
    sku.sizeMl ? `${sku.sizeMl}ml EDP` : null,
    sku.oilPct ? `${sku.oilPct}% oil` : null,
    sku.vialCount && sku.vialMl ? `${sku.vialCount} × ${sku.vialMl}ml` : null,
  ].filter(Boolean)

  return (
    <li className="specimen flex flex-col border border-ink-line p-6 sm:p-7">
      <div className="flex items-baseline justify-between gap-4">
        <span className="num label text-accent">{sku.index}</span>
        <span className="num label text-ink-soft">{skuPrice(sku)}</span>
      </div>

      <h3 className="mt-5 text-[1.0625rem] font-medium leading-snug tracking-tight">{sku.name}</h3>
      <p className="num mt-2 text-[0.8125rem] text-ink-soft">{spec.join(' · ')}</p>

      <p className="mt-5 border-t border-ink-line pt-5 font-display text-[1.0625rem] leading-snug">
        {t(copy.promise)}
      </p>
      <p className="mt-3.5 flex-1 text-[0.9375rem] leading-relaxed text-ink-muted">{t(copy.body)}</p>

      {copy.small ? (
        <p className="mt-5 text-[0.8125rem] leading-relaxed text-ink-soft">{t(copy.small)}</p>
      ) : null}

      <div className="mt-6 flex flex-wrap items-center justify-between gap-3 border-t border-ink-line pt-5">
        <SkuCta sku={sku.id}>{COPY.line.cta}</SkuCta>
        {copy.claimId ? <StatusChip claimId={copy.claimId} /> : null}
      </div>
    </li>
  )
}

export function TheLine() {
  const { line } = COPY
  const cards = line.cards as Record<SkuId, CardCopy>

  return (
    <Section id="line" labelledBy="line-heading" className="py-20 sm:py-28">
      <div className="flex flex-wrap items-center gap-3">
        <SectionLabel>{t(line.label)}</SectionLabel>
        <StatusChip claimId={line.labelClaimId} />
      </div>
      <h2 id="line-heading" className="sr-only">
        {t(line.label)}
      </h2>
      <p className="mt-5 max-w-2xl font-display text-[length:var(--text-serif-body)] leading-[1.55] text-ink-muted">
        {t(line.intro)}
      </p>
      <ul className="mt-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {SKUS.map((sku) => (
          <SkuCard key={sku.id} sku={sku} copy={cards[sku.id]} />
        ))}
      </ul>
    </Section>
  )
}
