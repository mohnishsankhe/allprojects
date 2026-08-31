import Link from 'next/link'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { HeroCta } from '@/components/cta-button'
import { Section } from '@/components/section'
import type { Variant } from '@/lib/variant'

/**
 * The hero is the experiment. Proof frames the brand as evidence; hope frames
 * it the way the category already does. Only one is ever in the DOM.
 */
export function Hero({ variant }: { variant: Variant }) {
  const copy = COPY.hero[variant]

  return (
    <Section id="hero" labelledBy="hero-heading" className="pb-14 pt-16 sm:pb-20 sm:pt-24">
      <p className="label text-ink-soft">{t(copy.eyebrow)}</p>
      <h1
        id="hero-heading"
        className="mt-6 max-w-4xl text-[length:var(--text-hero)] font-medium leading-[0.94] tracking-[-0.035em]"
      >
        {t(copy.h1)}
      </h1>
      <p className="mt-7 max-w-2xl text-[1.0625rem] leading-relaxed text-ink-muted sm:text-lg">{t(copy.sub)}</p>
      <div className="mt-9 flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
        <HeroCta>{t(copy.ctaPrimary)}</HeroCta>
        {copy.ctaSecondary ? (
          <Link
            href="/receipts"
            className="inline-flex items-center justify-center rounded-full border border-ink-line px-7 py-3.5 text-[0.9375rem] font-medium transition-colors hover:border-ink hover:bg-ink-wash"
          >
            {t(copy.ctaSecondary)}
          </Link>
        ) : null}
      </div>
    </Section>
  )
}
