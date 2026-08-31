import { BRAND, env, streetTestPlanned, eventWindow, STREET_TEST } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'

/**
 * JSON-LD for the site. Deliberately absent: Product, Review and
 * aggregateRating. Those are what search engines hang star ratings on, and
 * this brand has not earned a rating yet. scripts/check-no-review-schema.mjs
 * fails the build if any of them reappear.
 */

export function organizationSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: BRAND.name,
    description: t(COPY.seo.description),
    url: env.siteUrl,
    slogan: BRAND.tagline,
    foundingLocation: {
      '@type': 'Place',
      address: { '@type': 'PostalAddress', addressLocality: BRAND.city, addressCountry: 'IN' },
    },
    founder: { '@type': 'Person', name: BRAND.founderName },
    ...(env.instagramUrl ? { sameAs: [env.instagramUrl] } : {}),
  }
}

export function websiteSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: BRAND.name,
    url: env.siteUrl,
    description: t(COPY.seo.description),
    publisher: { '@type': 'Organization', name: BRAND.name },
  }
}

export function faqSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: COPY.faq.items.map((item) => ({
      '@type': 'Question',
      name: t(item.q),
      acceptedAnswer: { '@type': 'Answer', text: t(item.a) },
    })),
  }
}

/** Only emitted when the event is genuinely planned. Otherwise: nothing. */
export function eventSchema() {
  if (!streetTestPlanned || !eventWindow) return null
  return {
    '@context': 'https://schema.org',
    '@type': 'Event',
    name: t(COPY.streetTest.heading),
    description: t(COPY.streetTest.body),
    eventStatus: 'https://schema.org/EventScheduled',
    eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
    location: {
      '@type': 'Place',
      name: STREET_TEST.venue,
      address: {
        '@type': 'PostalAddress',
        addressLocality: STREET_TEST.neighbourhood,
        addressRegion: BRAND.city,
        addressCountry: 'IN',
      },
    },
    organizer: { '@type': 'Organization', name: BRAND.name, url: env.siteUrl },
  }
}

export function jsonLdForLanding() {
  return [organizationSchema(), websiteSchema(), faqSchema(), eventSchema()].filter(Boolean)
}
