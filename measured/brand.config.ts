/**
 * The one place any number, name, price or date lives.
 *
 * Hard rule from the brief: "Prices, concentrations, and dates render from
 * config, never hardcoded in copy." `content/copy.ts` therefore holds prose
 * with {tokens} only, and `scripts/check-claims.mjs` fails the build if a
 * claim-shaped number appears anywhere outside this file and the manifest.
 *
 * Swapping `name` below repaints the wordmark, <title>, meta description, OG
 * image, llms.txt and every copy token. That is acceptance criterion 7.
 */

export const BRAND = {
  name: 'MEASURED', // alternates: "PRAMANA", "PROBABLY"
  descriptor: 'Proven Perfumery',
  tagline: 'Measured, not promised.',
  founderName: 'Mohnish',
  city: 'Bombay',
  launchWindow: 'Early 2027',
  currency: '₹',
  heroPrice: 1499,
  kitPrice: 299,
  waitlistGoalCopy: 'the first 1,000 noses',
} as const

/** Where longevity and projection get measured. Bombay in October, not Paris in spring. */
export const CLIMATE = {
  tempC: 34,
  rh: 75,
} as const

/** The Compliments Guarantee window, in days from launch purchase. */
export const GUARANTEE_DAYS = 30

/**
 * Numbers inside the founder's manifesto (§4.3). These are narrative and
 * illustrative, not product claims — they describe a personal wardrobe and a
 * category-typical price, so they carry no manifest id. They live here anyway
 * so that copy.ts stays free of literals.
 */
export const MANIFESTO_FIGURES = {
  bottlesOwned: 100,
  bottlesWorn: 10,
  bottlesUnworn: 90,
  /** A category-typical D2C bottle price, used to follow the rupee. */
  categoryBottlePrice: 1500,
  /** Typical juice cost inside that bottle. */
  categoryJuiceCost: 100,
  /** The price point above which "chemical-free" marketing does not stop. */
  luxuryComparisonPrice: 40000,
} as const

export type SkuId = 'date' | 'office' | 'shaadi' | 'kit'

export type Sku = {
  id: SkuId
  index: string
  name: string
  /** Which BRAND price this SKU is sold at. */
  priceKey: 'heroPrice' | 'kitPrice'
  sizeMl?: number
  /** Fragrance-oil concentration, disclosed per SKU. */
  oilPct?: number
  vialCount?: number
  vialMl?: number
  /** Provisional thresholds the lab is allowed to overrule. See claim `names`. */
  renameAboveHours?: number
  reformulateBelowHours?: number
  /** Engineered projection spine, in hours. Provisional until measured. */
  spineHours?: number
}

export const SKUS: readonly Sku[] = [
  {
    id: 'date',
    index: 'No. 01',
    name: 'THE 8-HOUR DATE',
    priceKey: 'heroPrice',
    sizeMl: 50,
    oilPct: 20,
    renameAboveHours: 10,
    reformulateBelowHours: 6,
  },
  { id: 'office', index: 'No. 02', name: 'THE 9-TO-9 OFFICE', priceKey: 'heroPrice', sizeMl: 50, oilPct: 18, spineHours: 12 },
  { id: 'shaadi', index: 'No. 03', name: 'THE THREE-DAY SHAADI', priceKey: 'heroPrice', sizeMl: 50, oilPct: 22 },
  { id: 'kit', index: 'No. 04', name: 'THE FIRST BOTTLE KIT', priceKey: 'kitPrice', vialCount: 3, vialMl: 2 },
] as const

/**
 * §4.4, bar 1. A representative industry cost structure — NOT a measurement of
 * any specific competitor. `source` is required and is republished on
 * /receipts, because the on-page footnote promises "Sources & math on the
 * receipts page" and the site does not make promises it does not keep.
 */
export const INVOICE_BENCHMARK = {
  source:
    'Indicative structure assembled from public D2C beauty and fragrance unit-economics ' +
    'commentary: marketplace take rates, performance-marketing CAC as a share of MRP, and ' +
    'packaging-to-juice ratios widely reported in the category. It is a category illustration ' +
    'with wide variance, not an audit of any single brand, and not a measurement of ours.',
  segments: [
    { id: 'marketing', label: 'Marketing & influencers', pct: 35 },
    { id: 'platform', label: 'Platform fees', pct: 28 },
    { id: 'packaging', label: 'Box & bottle', pct: 15 },
    { id: 'logistics', label: 'Logistics', pct: 10 },
    { id: 'juice', label: 'Juice', pct: 7, highlight: true },
    { id: 'margin', label: 'Margin remainder', pct: 5 },
  ],
} as const

/**
 * §4.4, bar 2. Forward-looking commitment, tagged PLANNED on the page.
 *
 * Only the juice floor is a manifest-backed commitment (claim `invoice`:
 * "juice >= 25% of MRP cost base"). The testing reserve is a committed line
 * item whose final size is not yet fixed, and everything else is deliberately
 * left as one undivided remainder rather than invented in detail — the full
 * invoice publishes at launch.
 */
export const INVOICE_COMMITMENT = {
  segments: [
    { id: 'juice', label: 'Juice', pct: 25, floor: true, highlight: true },
    { id: 'testing', label: 'Testing & guarantee reserve', pct: 10 },
    { id: 'rest', label: 'Everything else — itemised at launch', pct: 65 },
  ],
} as const

/**
 * §4.7 is announced only if it is genuinely planned. It is not, so the section
 * renders nothing, contributes no Event schema, and its manifest row is hidden.
 * Flipping this to true (and setting a real eventWindow) turns all three on.
 */
export const streetTestPlanned = false
export const eventWindow = ''

/** Panel size for the street test. Unused while streetTestPlanned is false. */
export const STREET_TEST = {
  venue: 'BASTIAN',
  neighbourhood: 'BANDRA',
  panelSize: 234,
} as const

/**
 * Answer-engine targets. The price band appears in FAQ copy as the example
 * query a shopper would actually type, so it lives in config like every other
 * number on the site.
 */
export const AEO = {
  queryPriceBand: 2000,
} as const

export const env = {
  siteUrl: process.env.NEXT_PUBLIC_SITE_URL ?? 'https://measured.in',
  plausibleDomain: process.env.PLAUSIBLE_DOMAIN ?? '',
  instagramUrl: process.env.INSTAGRAM_URL ?? '',
  waitlistWebhookUrl: process.env.WAITLIST_WEBHOOK_URL ?? '',
}
