import { streetTestPlanned, eventWindow } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { StatusChip } from '@/components/status-chip'
import { HeroCta } from '@/components/cta-button'

/**
 * Announced only if it is genuinely planned. While the flag is off this
 * renders nothing at all — no section, no Event schema, and the matching
 * manifest row is hidden from /receipts too. Announcing an event that has not
 * been booked would be exactly the kind of claim this brand exists to refuse.
 */
export function StreetTest() {
  if (!streetTestPlanned || !eventWindow) return null

  const { streetTest } = COPY

  return (
    <section
      id="street-test"
      data-section="street-test"
      aria-labelledby="street-test-heading"
      className="macro-glass border-y border-ink-line bg-ink px-5 py-20 text-paper sm:px-8 sm:py-28 lg:px-12"
    >
      <div className="mx-auto w-full max-w-6xl">
        <h2
          id="street-test-heading"
          className="max-w-3xl text-[length:var(--text-section)] font-medium leading-[1.05] tracking-[-0.03em]"
        >
          {t(streetTest.heading)}
        </h2>
        <p className="mt-7 max-w-2xl text-[1.0625rem] leading-relaxed text-paper/75">{t(streetTest.body)}</p>
        <div className="mt-9 flex flex-wrap items-center gap-4">
          <HeroCta variantStyle="ghost">{t(streetTest.cta)}</HeroCta>
          <StatusChip claimId={streetTest.claimId} className="bg-paper/10" />
        </div>
      </div>
    </section>
  )
}
