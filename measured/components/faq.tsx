import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { SectionLabel } from '@/components/section'
import { FaqTracker } from '@/components/faq-tracker'

/**
 * Native <details>, so the accordion works with zero JavaScript and needs no
 * open-state hydration.
 *
 * The questions and answers are server-rendered — they never enter the client
 * bundle. FaqTracker wraps them purely to attach one delegated listener for
 * the faq_open event.
 */
export function Faq() {
  return (
    <section
      id="faq"
      data-section="faq"
      aria-labelledby="faq-heading"
      className="scroll-mt-16 px-5 py-20 sm:px-8 sm:py-28 lg:px-12"
    >
      <div className="mx-auto w-full max-w-6xl">
        <SectionLabel>{COPY.faq.label}</SectionLabel>
        <h2 id="faq-heading" className="sr-only">
          {COPY.faq.label}
        </h2>
        <FaqTracker>
          {COPY.faq.items.map((item) => (
            <details key={item.q} name="faq" className="group border-b border-ink-line">
              <summary className="flex cursor-pointer list-none items-start justify-between gap-6 py-5 text-[0.9375rem] font-medium leading-snug marker:content-none">
                {t(item.q)}
                <span
                  aria-hidden="true"
                  className="mt-0.5 shrink-0 text-ink-decor transition-transform group-open:rotate-45"
                >
                  +
                </span>
              </summary>
              <p className="max-w-2xl pb-6 text-[0.9375rem] leading-relaxed text-ink-muted">{t(item.a)}</p>
            </details>
          ))}
        </FaqTracker>
      </div>
    </section>
  )
}
