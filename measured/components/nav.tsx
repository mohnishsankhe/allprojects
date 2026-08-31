import Link from 'next/link'
import { Wordmark } from '@/components/wordmark'
import { NavCta } from '@/components/cta-button'
import { COPY } from '@/content/copy'
import { CONTENT_ANCHOR } from '@/lib/anchors'

export function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b border-ink-wash bg-paper/85 backdrop-blur-md">
      <a
        href={`#${CONTENT_ANCHOR}`}
        className="sr-only focus:not-sr-only focus:absolute focus:left-4 focus:top-3 focus:z-50 focus:rounded-full focus:bg-ink focus:px-4 focus:py-2 focus:text-paper"
      >
        {COPY.nav.skipToContent}
      </a>
      <nav
        aria-label="Primary"
        className="mx-auto flex w-full max-w-6xl items-center justify-between px-5 py-3.5 sm:px-8 lg:px-12"
      >
        <Link href="/" className="text-[0.9375rem]">
          <Wordmark />
          <span className="sr-only">home</span>
        </Link>
        <div className="flex items-center gap-4 sm:gap-6">
          <Link href="/receipts" className="text-[0.8125rem] text-ink-muted transition-colors hover:text-ink">
            {COPY.nav.receipts}
          </Link>
          <NavCta>{COPY.nav.waitlist}</NavCta>
        </div>
      </nav>
    </header>
  )
}
