import type { Metadata, Viewport } from 'next'
import { Fraunces, Inter } from 'next/font/google'
import Script from 'next/script'
import { headers } from 'next/headers'
import './globals.css'

import { BRAND, env } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'
import { JS_MARKER, PLAUSIBLE_STUB } from '@/lib/analytics'
import { VARIANT_HEADER, parseVariant } from '@/lib/variant'
import { VariantProvider } from '@/components/variant-provider'

/*
 * Both faces are self-hosted at build time by next/font, so there is no
 * third-party connection on the critical path.
 *
 * Static weights, not variable fonts. A variable Fraunces carrying its SOFT,
 * WONK and opsz axes costs over 100 KB on its own, and on the 4G connection
 * most of this traffic arrives on, font bytes are the LCP. Two fixed weights
 * per family cover every style the site actually uses.
 *
 * The LCP element is the hero headline, set in the grotesk rather than the
 * serif — the brief only asks for serif in the manifesto — so Inter is
 * preloaded and Fraunces, which first appears below the fold, is not.
 */
const inter = Inter({
  subsets: ['latin'],
  weight: ['400', '500'],
  display: 'swap',
  variable: '--font-inter',
  adjustFontFallback: true,
  preload: true,
})

const fraunces = Fraunces({
  subsets: ['latin'],
  weight: ['400'],
  // `optional` rather than `swap`: the serif first appears below the fold, so
  // it must never compete for bandwidth with the text that decides LCP, and it
  // must never repaint the page after the fact. A first-time visitor on a slow
  // connection reads the manifesto in the metric-matched fallback; from the
  // second view on, it is Fraunces.
  display: 'optional',
  variable: '--font-fraunces',
  adjustFontFallback: true,
  preload: false,
})

export const metadata: Metadata = {
  metadataBase: new URL(env.siteUrl),
  title: t(COPY.seo.title),
  description: t(COPY.seo.description),
  applicationName: BRAND.name,
  alternates: { canonical: '/' },
  openGraph: {
    type: 'website',
    siteName: BRAND.name,
    title: t(COPY.seo.title),
    description: t(COPY.seo.description),
    url: '/',
    locale: 'en_IN',
  },
  twitter: {
    card: 'summary_large_image',
    title: t(COPY.seo.title),
    description: t(COPY.seo.description),
  },
  robots: { index: true, follow: true },
}

export const viewport: Viewport = {
  themeColor: '#faf9f6',
  width: 'device-width',
  initialScale: 1,
}

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const variant = parseVariant((await headers()).get(VARIANT_HEADER))

  return (
    <html lang="en-IN" className={`${inter.variable} ${fraunces.variable}`}>
      <head>
        {/* Two statements, inline and synchronous: mark that scripting is on
            before first paint, and queue analytics fired before the script
            lands. Inlining beats next/script here — the loader would cost more
            than the snippet. */}
        <script dangerouslySetInnerHTML={{ __html: `${JS_MARKER};${PLAUSIBLE_STUB}` }} />
      </head>
      <body className="min-h-dvh antialiased">
        {env.plausibleDomain ? (
          <Script
            id="plausible"
            strategy="afterInteractive"
            defer
            data-domain={env.plausibleDomain}
            src="https://plausible.io/js/script.manual.tagged-events.js"
          />
        ) : null}
        <VariantProvider variant={variant}>{children}</VariantProvider>
      </body>
    </html>
  )
}
