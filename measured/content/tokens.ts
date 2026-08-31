import {
  AEO,
  BRAND,
  CLIMATE,
  STREET_TEST,
  GUARANTEE_DAYS,
  MANIFESTO_FIGURES,
  SKUS,
  env,
  eventWindow,
  type Sku,
} from '@/brand.config'

const inr = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 })

/** Indian digit grouping, with the currency symbol from config. */
export function price(amount: number): string {
  return `${BRAND.currency}${inr.format(amount)}`
}

export function skuPrice(sku: Sku): string {
  return price(BRAND[sku.priceKey])
}

/**
 * Every token that copy.ts is allowed to interpolate. Adding a token here is
 * the only way to get a number or a brand fact into a copy string.
 */
function tokenMap(): Record<string, string> {
  return {
    name: BRAND.name,
    descriptor: BRAND.descriptor,
    descriptorUpper: BRAND.descriptor.toUpperCase(),
    cityUpper: BRAND.city.toUpperCase(),
    tagline: BRAND.tagline,
    founderName: BRAND.founderName,
    city: BRAND.city,
    launchWindow: BRAND.launchWindow,
    waitlistGoalCopy: BRAND.waitlistGoalCopy,
    heroPrice: price(BRAND.heroPrice),
    kitPrice: price(BRAND.kitPrice),
    tempC: `${CLIMATE.tempC}°C`,
    rh: `${CLIMATE.rh}%`,
    guaranteeDays: String(GUARANTEE_DAYS),
    bottlesOwned: String(MANIFESTO_FIGURES.bottlesOwned),
    bottlesWorn: String(MANIFESTO_FIGURES.bottlesWorn),
    bottlesUnworn: String(MANIFESTO_FIGURES.bottlesUnworn),
    categoryBottlePrice: price(MANIFESTO_FIGURES.categoryBottlePrice),
    categoryJuiceCost: price(MANIFESTO_FIGURES.categoryJuiceCost),
    luxuryComparisonPrice: price(MANIFESTO_FIGURES.luxuryComparisonPrice),
    skuCount: String(SKUS.length),
    heroOilPct: `${SKUS[0].oilPct}%`,
    renameAboveHours: `${SKUS[0].renameAboveHours} hours`,
    reformulateBelowHours: String(SKUS[0].reformulateBelowHours),
    spineHours: `${SKUS[1].spineHours}-hour`,
    queryPriceBand: price(AEO.queryPriceBand),
    streetPanelSize: String(STREET_TEST.panelSize),
    skuDateName: SKUS[0].name,
    siteUrl: env.siteUrl,
    eventWindow,
  }
}

const TOKEN_RE = /\{(\w+)\}/g

/**
 * Interpolates {tokens} in a copy string. An unknown token throws rather than
 * rendering a literal "{launchWindow}" to a visitor — a silent failure here
 * would put a placeholder on a live page.
 */
export function t(input: string): string {
  const map = tokenMap()
  return input.replace(TOKEN_RE, (_match, key: string) => {
    const value = map[key]
    if (value === undefined) {
      throw new Error(`Unknown copy token {${key}}. Add it to tokenMap() in content/tokens.ts.`)
    }
    return value
  })
}

/** Token names, for tests that walk the whole copy tree. */
export function knownTokens(): string[] {
  return Object.keys(tokenMap())
}
