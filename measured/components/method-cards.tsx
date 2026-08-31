import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { Section, SectionLabel } from '@/components/section'
import { StatusChip } from '@/components/status-chip'

export function MethodCards() {
  const { method } = COPY

  return (
    <Section id="method" labelledBy="method-heading" className="py-20 sm:py-28">
      <SectionLabel>{method.label}</SectionLabel>
      <h2 id="method-heading" className="sr-only">
        {method.label}
      </h2>
      <ul className="mt-8 grid gap-px overflow-hidden rounded-sm border border-ink-line bg-ink-line sm:grid-cols-3">
        {method.cards.map((card) => (
          <li key={card.title} className="flex flex-col gap-4 bg-paper p-6 sm:p-7">
            <h3 className="label text-ink">{card.title}</h3>
            <p className="flex-1 text-[0.9375rem] leading-relaxed text-ink-muted">{t(card.body)}</p>
            <div>
              <StatusChip claimId={card.claimId} note={card.chipNote} />
            </div>
          </li>
        ))}
      </ul>
    </Section>
  )
}
