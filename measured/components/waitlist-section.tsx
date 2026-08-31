import { SKUS } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { Section } from '@/components/section'
import { WaitlistForm } from '@/components/waitlist-form'
import { WAITLIST_ANCHOR } from '@/lib/anchors'
import type { Variant } from '@/lib/variant'

/**
 * Resolves the copy on the server — including the variant-specific heading,
 * which is the second half of the experiment — and hands the form plain
 * strings.
 */
export function WaitlistSection({ variant }: { variant: Variant }) {
  const { waitlist } = COPY

  return (
    <Section
      id={WAITLIST_ANCHOR}
      labelledBy={`${WAITLIST_ANCHOR}-heading`}
      className="border-t border-ink-line py-20 sm:py-28"
    >
      <WaitlistForm
        copy={{
          heading: t(waitlist.h2[variant]),
          sub: t(waitlist.sub),
          emailLabel: waitlist.emailLabel,
          phoneLabel: waitlist.phoneLabel,
          emailPlaceholder: waitlist.emailPlaceholder,
          phonePlaceholder: waitlist.phonePlaceholder,
          skuLabel: waitlist.skuLabel,
          skuNone: waitlist.skuNone,
          button: waitlist.button,
          buttonBusy: waitlist.buttonBusy,
          success: t(waitlist.success),
          errors: { ...waitlist.errors },
        }}
        skus={SKUS.map((s) => ({ id: s.id, name: s.name }))}
      />
    </Section>
  )
}
