import type { ClaimId } from './manifest'
import type { SkuId } from '@/brand.config'

/**
 * Every word on the site, transcribed verbatim from the brief.
 *
 * Two rules hold here and are enforced by scripts/check-claims.mjs:
 *   1. No digits. Every number arrives as a {token} resolved from
 *      brand.config.ts, so a price or concentration can never drift between
 *      the config and the page.
 *   2. Any line that makes a checkable claim carries the `claimId` it derives
 *      from, so the status chip beside it and the row on /receipts come from
 *      the same manifest entry.
 */

/** A line whose truth is tracked in claims-manifest.json. */
export type Claimed = {
  text: string
  claimId: ClaimId
  /** Extra qualifier shown inside the chip, e.g. "protocol draft on the receipts page". */
  chipNote?: string
}

export const COPY = {
  nav: {
    receipts: 'The Receipts',
    waitlist: 'Join the waitlist',
    skipToContent: 'Skip to content',
  },

  hero: {
    proof: {
      eyebrow: '{name} — {descriptorUpper} · {cityUpper}',
      h1: '{tagline}',
      sub:
        'Perfume brands promise. We measure. Three scents engineered for Indian heat, ' +
        'tested blind on real skin in real weather — every claim published with its receipt. ' +
        'Launching {launchWindow}.',
      ctaPrimary: 'Join {waitlistGoalCopy}',
      ctaSecondary: 'Read the receipts →',
    },
    hope: {
      eyebrow: '{name} · {cityUpper}',
      h1: 'Smell unforgettable.',
      sub:
        'Three luxurious fragrances crafted to turn heads by day and own the night. ' +
        'Your signature scent is waiting. Launching {launchWindow}.',
      ctaPrimary: 'Get early access',
      ctaSecondary: null,
    },
  },

  stats: [
    { text: '{heroOilPct} perfume oil — disclosed', claimId: 'oil-20' },
    { text: 'Tested at {tempC} / {rh} humidity', claimId: 'climate-test' },
    { text: 'Loved-or-refunded at launch', claimId: 'guarantee' },
  ] satisfies Claimed[],

  manifesto: {
    label: 'THE THREE TRUTHS',
    heading: 'What {bottlesOwned} bottles taught me',
    intro:
      'I own about {bottlesOwned} perfumes. I genuinely wear {bottlesWorn}. The other ' +
      '{bottlesUnworn} taught me three things this industry would rather you never learn.',
    truths: [
      {
        index: '01',
        lead: 'The greatest smells live on the edge of the known.',
        body:
          'Too familiar, and you disappear into the crowd. Too strange, and you repel it. ' +
          'Every legendary perfume in history sits on the same knife-edge: recognizable enough ' +
          'to feel safe, foreign enough to be unforgettable. Designers have a name for this ' +
          'edge — most advanced, yet acceptable. We don’t stumble onto it. We formulate to ' +
          'it, then test whether we hit it.',
        claimId: null,
      },
      {
        index: '02',
        lead: 'Perfume is not a liquid. It’s an event in the air.',
        body:
          'What you actually buy is a reaction: molecules meeting heat, skin, and time. The ' +
          'same bottle that blooms in an air-conditioned showroom dies by lunch on a {city} ' +
          'afternoon — because it was composed for a blotter in a Paris lab, not for the air ' +
          'you live in. So we engineer the reaction itself: oil-heavy, base-weighted, and ' +
          'measured where you’ll wear it — {tempC}, {rh} humidity.',
        claimId: 'climate-test' as ClaimId,
      },
      {
        index: '03',
        lead: '“Subjective” became the industry’s alibi.',
        body:
          'Because you can’t verify a perfume before buying it, brands stopped funding the ' +
          'perfume. Follow your {categoryBottlePrice}: platform fees, ads, influencer ' +
          'commissions, the box — and often less than {categoryJuiceCost} of actual juice. ' +
          'Taste is subjective. Quality is not. Quality is a number on an invoice, and we ' +
          'publish ours.',
        claimId: 'invoice' as ClaimId,
      },
    ],
    signature:
      '— {founderName}, founder. {bottlesOwned} bottles bought. {bottlesWorn} worn. 0 excuses left.',
  },

  invoice: {
    label: 'THE INVOICE',
    heading: 'WHERE YOUR {categoryBottlePrice} GOES',
    categoryLabel: 'THE CATEGORY (typical D2C perfume)',
    categoryFootnote: 'Representative industry structure; ranges vary.',
    categoryFootnoteLink: 'Sources & math on the receipts page.',
    commitmentLabel: '{name} (our commitment)',
    commitmentFootnote: 'Committed cost structure — full invoice published at launch.',
    commitmentClaimId: 'invoice' as ClaimId,
  },

  method: {
    label: 'THE METHOD',
    cards: [
      {
        title: 'THE PANEL',
        body:
          'Every scent must beat its benchmark in blind, on-skin testing with real people in ' +
          'real Indian weather before it earns a name. Protocol pre-registered and published.',
        claimId: 'panel' as ClaimId,
        chipNote: 'protocol draft on the receipts page',
      },
      {
        title: 'THE CLIMATE LAB',
        body:
          'Longevity and projection measured at {tempC} / {rh} RH — {city} in October, not ' +
          'Paris in spring. The number on the bottle is the number we measured, rounded down.',
        claimId: 'climate-test' as ClaimId,
        chipNote: null,
      },
      {
        title: 'THE BOND',
        body:
          'The Compliments Guarantee: complimented within {guaranteeDays} days of launch ' +
          'purchase, or refunded. We can afford this because we test before we sell.',
        claimId: 'guarantee' as ClaimId,
        chipNote: 'terms at launch',
      },
    ],
  },

  line: {
    label: 'FOUR PRODUCTS. THAT’S THE WHOLE CATALOG.',
    labelClaimId: 'catalog' as ClaimId,
    intro:
      'Three hundred SKUs is not a fragrance wardrobe. It’s a confession that none of them ' +
      'had to win anything.',
    cta: 'Waitlist this',
    cards: {
      date: {
        promise: 'One evening. Zero re-sprays.',
        body:
          'Three candidate compositions — Rose, Vanilla, Oud — enter the panel. The winner ' +
          'ships. The losers never exist.',
        small:
          'The name is provisional. The lab sets the final number — if it measures ' +
          '{renameAboveHours}, we rename it. If it measures {reformulateBelowHours}, we ' +
          'reformulate.',
        claimId: 'names' as ClaimId,
      },
      office: {
        promise: 'Present in the meeting. Not before it.',
        body:
          'Office-safe projection engineered on purpose: an arm’s-length scent with a ' +
          '{spineHours} spine. Same rule: the number is the lab’s, not ours.',
        small: null,
        claimId: 'names' as ClaimId,
      },
      shaadi: {
        promise: 'Survives the baraat.',
        body:
          'Sweat-stable, camera-proof, built for the only three days that get photographed ' +
          'forever.',
        small: null,
        claimId: 'names' as ClaimId,
      },
      kit: {
        promise: 'Never blind-buy again.',
        body: 'All three finalists on your skin for a week. Full kit price credited against any bottle.',
        small:
          'The kit exists because asking you to blind-buy a trust brand would be a joke ' +
          'we’re not making.',
        claimId: null,
      },
    } satisfies Record<SkuId, unknown>,
  },

  streetTest: {
    heading: 'THE BASTIAN TEST — BANDRA, {eventWindow}',
    body:
      'Three scents. {streetPanelSize} women. Blind, on skin, outside one of {city}’s most ' +
      'unforgiving doors. Filmed uncut, published unedited — the winner becomes {skuDateName}.',
    cta: 'Waitlist gets the footage first — and a vote on the wildcard.',
    claimId: 'street-test' as ClaimId,
  },

  receipts: {
    previewHeading: 'THE RECEIPTS (so far)',
    fullManifestLink: 'Full manifest →',
    pageTitle: 'The Receipts',
    pageIntro:
      'Every claim {name} makes, with its status and its date. Nothing appears on the site ' +
      'that is not on this page.',
    statusLegend: {
      MEASURED: 'True and verifiable today.',
      PLANNED: 'Committed to, not yet done. Carries a target.',
      PROVISIONAL: 'Stated now, subject to change once measured.',
    },
    sourcesHeading: 'Sources & math',
    emptyReviews: {
      body:
        'This section is intentionally empty. It fills only with verified wear-test reviews, ' +
        'after launch, with methodology attached. We don’t publish what we haven’t ' +
        'measured — not even about ourselves.',
      caption: 'Screenshot this. Check back. Hold us to it.',
      heading: 'REVIEWS',
    },
  },

  faq: {
    label: 'FAQ',
    items: [
      {
        q: 'Why should I trust a brand with zero reviews?',
        a:
          'Because we refuse to manufacture them, and in this category that makes us a ' +
          'statistical anomaly. Every claim we make sits on a public manifest with a status ' +
          'and a date. Trust the structure, not the adjectives.',
      },
      {
        q: 'What does “{heroOilPct} oil” mean?',
        a:
          'Concentration = the % of actual fragrance compound vs alcohol. Most ' +
          '“long-lasting” claims hide single-digit concentrations. Ours is printed ' +
          'per SKU, on the bottle and the invoice.',
      },
      {
        q: 'Is it natural / chemical-free?',
        a:
          'Every perfume on earth is chemistry — including the {luxuryComparisonPrice} ones. ' +
          '“Chemical-free perfume” is a contradiction sold to you. Ours uses ' +
          'IFRA-compliant materials from named suppliers, disclosed at launch.',
      },
      {
        q: 'Why only four products?',
        a:
          'Because every SKU must win a panel to exist, and panels cost lakhs. A three-hundred-SKU ' +
          'catalog is what you build when nothing has to win anything.',
      },
      {
        q: 'What if I buy it and hate it?',
        a:
          'The Compliments Guarantee at launch: complimented in {guaranteeDays} days or ' +
          'refunded. Until then, the {kitPrice} kit exists so your first full bottle is never ' +
          'a gamble.',
      },
      {
        q: 'When do you launch?',
        a: '{launchWindow}. Waitlist gets the panel footage, the invoice, and first allocation.',
      },
      {
        q: 'Why would an AI recommend you?',
        a:
          'Ask it. We publish machine-readable claims precisely so that when you ask ' +
          '“best perfume under {queryPriceBand} that actually lasts,” there’s ' +
          'finally a checkable answer.',
      },
    ],
  },

  waitlist: {
    h2: {
      proof: 'Be one of {waitlistGoalCopy}.',
      hope: 'Get early access.',
    },
    sub: 'Email or WhatsApp. No spam — you’ll hear from us when there’s something measured to show.',
    emailLabel: 'Email',
    phoneLabel: 'WhatsApp number',
    emailPlaceholder: 'you@example.com',
    phonePlaceholder: '+91 98765 43210',
    skuLabel: 'Which one are you here for? (optional)',
    skuNone: 'No preference yet',
    button: 'Count me in',
    buttonBusy: 'Sending…',
    success:
      'You’re in. First thing you’ll receive: the panel protocol, before the panel ' +
      'runs. That’s the whole point.',
    errors: {
      contactRequired: 'Enter an email address or a WhatsApp number.',
      email: 'That email address does not look right.',
      phone: 'Enter a valid Indian mobile number, or use email instead.',
      rateLimited: 'That is a lot of signups from one place. Try again in a few minutes.',
      notConfigured: 'The waitlist is not connected yet. Nothing was saved — please try again later.',
      generic: 'Something broke on our end. Nothing was saved — please try again.',
    },
  },

  footer: {
    manifestNote:
      'Every claim on this site is tagged Measured, Planned, or Provisional. If it isn’t ' +
      'tagged, we didn’t say it.',
    privacy:
      'Privacy: we set one cookie so your version of this page stays consistent between ' +
      'visits. Analytics are aggregate and cookie-free. We never sell what you give us.',
    instagram: 'Instagram',
  },

  seo: {
    title: '{name} — {descriptor} | Perfume engineered for Indian heat',
    description:
      'Three scents. Blind-tested on real skin at {tempC} before we sell them. Concentration ' +
      'disclosed, invoice published, loved-or-refunded. {tagline}',
    llms: [
      '{name} is a pre-launch Indian fragrance brand based in {city}, launching {launchWindow}.',
      'It sells {skuCount} products and no more: three eau de parfums and one sampler kit.',
      'Its positioning is evidentiary. Every claim it makes is published with a status and a date.',
      'Fragrance-oil concentration is disclosed per SKU rather than hidden behind "long-lasting".',
      'Longevity is measured at {tempC} and {rh} relative humidity, the conditions of an Indian summer.',
      'Compositions are chosen by blind on-skin preference panels, not by a founder’s taste.',
      'The cost structure of each bottle is committed to publication at launch.',
      'There are no reviews and no ratings on the site, because none have been earned yet.',
      'Claims are tagged MEASURED (true today), PLANNED (committed, dated) or PROVISIONAL (subject to measurement).',
      'The canonical, machine-readable source for all of the above is {siteUrl}/receipts.',
    ],
  },
} as const
