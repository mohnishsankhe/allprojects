import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'

/**
 * The signature move: a review module, fully designed, deliberately empty.
 *
 * There is no rating markup here and none anywhere in the output — the build
 * check in scripts/check-no-review-schema.mjs enforces it. The stars are
 * decorative outlines with aria-hidden, so no assistive technology announces a
 * rating that does not exist.
 */
function HollowStar() {
  return (
    <svg viewBox="0 0 24 24" fill="none" className="size-5 sm:size-6" aria-hidden="true">
      <path
        d="M12 3.4l2.6 5.65 6.15.72-4.55 4.2 1.23 6.08L12 17.02 6.57 20.05l1.23-6.08-4.55-4.2 6.15-.72L12 3.4z"
        stroke="currentColor"
        strokeWidth="1.1"
        strokeLinejoin="round"
      />
    </svg>
  )
}

export function EmptyReviews() {
  const { emptyReviews } = COPY.receipts

  return (
    <div
      data-testid="empty-reviews"
      className="flex h-full flex-col border border-ink-line bg-paper p-6 sm:p-8"
    >
      <p className="label text-ink-soft">{emptyReviews.heading}</p>

      <div className="mt-8 flex items-center justify-center gap-2 text-ink-decor" aria-hidden="true">
        <HollowStar />
        <HollowStar />
        <HollowStar />
        <HollowStar />
        <HollowStar />
      </div>

      {/* Empty quote lines: the shape of a testimonial with nothing written in it. */}
      <div className="mx-auto mt-8 flex w-full max-w-xs flex-col items-center gap-4" aria-hidden="true">
        <div className="h-px w-full bg-ink-line" />
        <div className="h-px w-full bg-ink-line" />
        <div className="h-px w-3/5 bg-ink-line" />
      </div>

      <p className="mt-10 text-balance text-center text-[0.9375rem] leading-relaxed text-ink-muted">
        {t(emptyReviews.body)}
      </p>

      <p className="mt-6 text-center text-[0.75rem] uppercase tracking-[0.16em] text-ink-soft">
        {t(emptyReviews.caption)}
      </p>
    </div>
  )
}
