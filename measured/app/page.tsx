import { headers } from 'next/headers'
import type { ReactNode } from 'react'

import { Nav } from '@/components/nav'
import { Hero } from '@/components/hero'
import { StatsStrip } from '@/components/stats-strip'
import { Manifesto } from '@/components/manifesto'
import { InvoiceBars } from '@/components/invoice-bars'
import { MethodCards } from '@/components/method-cards'
import { TheLine } from '@/components/sku-card'
import { StreetTest } from '@/components/street-test'
import { ReceiptsPreview } from '@/components/receipts-preview'
import { Faq } from '@/components/faq'
import { WaitlistSection } from '@/components/waitlist-section'
import { Footer } from '@/components/footer'
import { Analytics } from '@/components/analytics'
import { CONTENT_ANCHOR } from '@/lib/anchors'
import { jsonLdForLanding } from '@/lib/seo'
import { VARIANT_HEADER, parseVariant, type Variant } from '@/lib/variant'

// The variant is read per request, so the page is never statically rendered
// and — critically — never shared between visitors by a cache. See proxy.ts.
export const dynamic = 'force-dynamic'

type SectionKey =
  | 'hero'
  | 'stats'
  | 'manifesto'
  | 'invoice'
  | 'method'
  | 'line'
  | 'streetTest'
  | 'receipts'
  | 'faq'
  | 'waitlist'

/**
 * Section order is the second half of the experiment: hope leads with product,
 * proof leads with the argument.
 *
 * This reorders the DOM rather than using CSS `order`, so crawlers and screen
 * readers get the same narrative the eye does.
 */
const ORDER: Record<Variant, readonly SectionKey[]> = {
  proof: ['hero', 'stats', 'manifesto', 'invoice', 'method', 'line', 'streetTest', 'receipts', 'faq', 'waitlist'],
  hope: ['hero', 'stats', 'line', 'manifesto', 'invoice', 'method', 'streetTest', 'receipts', 'faq', 'waitlist'],
}

export default async function LandingPage() {
  const variant = parseVariant((await headers()).get(VARIANT_HEADER))

  const sections: Record<SectionKey, ReactNode> = {
    hero: <Hero variant={variant} />,
    stats: <StatsStrip />,
    manifesto: <Manifesto />,
    invoice: <InvoiceBars />,
    method: <MethodCards />,
    line: <TheLine />,
    streetTest: <StreetTest />,
    receipts: <ReceiptsPreview />,
    faq: <Faq />,
    waitlist: <WaitlistSection variant={variant} />,
  }

  return (
    <>
      <script
        type="application/ld+json"
        // Built from the manifest and config; contains no Review, rating or
        // Product node, and the build fails if one ever appears.
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdForLanding()) }}
      />
      <Nav />
      <main id={CONTENT_ANCHOR} data-variant={variant}>
        {ORDER[variant].map((key) => (
          <div key={key}>{sections[key]}</div>
        ))}
      </main>
      <Footer />
      <Analytics />
    </>
  )
}
