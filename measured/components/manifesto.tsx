import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { Section, SectionLabel } from '@/components/section'
import { StatusChip } from '@/components/status-chip'
import type { ClaimId } from '@/content/manifest'

/** The only place the serif runs. Generous whitespace, one idea per truth. */
export function Manifesto() {
  const { manifesto } = COPY

  return (
    <Section id="manifesto" labelledBy="manifesto-heading" className="py-20 sm:py-28">
      <SectionLabel>{manifesto.label}</SectionLabel>
      <h2
        id="manifesto-heading"
        className="mt-5 max-w-3xl font-display text-[length:var(--text-section)] font-normal leading-[1.06] tracking-[-0.02em]"
      >
        {t(manifesto.heading)}
      </h2>
      <p className="mt-7 max-w-2xl font-display text-[length:var(--text-serif-body)] leading-[1.55] text-ink-muted">
        {t(manifesto.intro)}
      </p>

      <ol className="mt-14 space-y-14 sm:mt-16 sm:space-y-16">
        {manifesto.truths.map((truth) => (
          <li key={truth.index} className="grid gap-5 sm:grid-cols-[4rem_1fr] sm:gap-8">
            <span className="num label pt-1.5 text-accent">{truth.index}</span>
            <div className="max-w-2xl">
              <h3 className="font-display text-[length:var(--text-serif-body)] leading-snug text-ink">
                {t(truth.lead)}
              </h3>
              <p className="mt-3.5 font-display text-[length:var(--text-serif-body)] leading-[1.6] text-ink-muted">
                {t(truth.body)}
              </p>
              {truth.claimId ? (
                <div className="mt-4">
                  <StatusChip claimId={truth.claimId as ClaimId} />
                </div>
              ) : null}
            </div>
          </li>
        ))}
      </ol>

      <p className="mt-14 max-w-2xl border-t border-ink-line pt-6 text-[0.9375rem] text-ink-soft sm:mt-16">
        {t(manifesto.signature)}
      </p>
    </Section>
  )
}
