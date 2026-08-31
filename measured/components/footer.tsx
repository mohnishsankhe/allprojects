import Link from 'next/link'
import { BRAND, env } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { Wordmark } from '@/components/wordmark'

export function Footer() {
  return (
    <footer className="border-t border-ink-line px-5 py-12 sm:px-8 sm:py-14 lg:px-12">
      <div className="mx-auto w-full max-w-6xl">
        <div className="flex flex-wrap items-center gap-x-6 gap-y-3 text-[0.875rem]">
          <Wordmark />
          <span className="text-ink-soft">{BRAND.city}</span>
          <Link href="/receipts" className="text-ink-muted transition-colors hover:text-ink">
            {COPY.nav.receipts}
          </Link>
          {env.instagramUrl ? (
            <a
              href={env.instagramUrl}
              rel="noopener noreferrer"
              target="_blank"
              className="text-ink-muted transition-colors hover:text-ink"
            >
              {COPY.footer.instagram}
            </a>
          ) : null}
        </div>

        <p className="mt-8 max-w-2xl text-[0.8125rem] leading-relaxed text-ink-soft">
          {t(COPY.footer.manifestNote)}
        </p>
        <p className="mt-3 max-w-2xl text-[0.8125rem] leading-relaxed text-ink-soft">
          {t(COPY.footer.privacy)}
        </p>
      </div>
    </footer>
  )
}
