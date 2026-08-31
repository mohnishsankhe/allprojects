import { describe, expect, it } from 'vitest'
import { eventSchema, faqSchema, jsonLdForLanding, organizationSchema, websiteSchema } from '@/lib/seo'
import { COPY } from '@/content/copy'
import { streetTestPlanned } from '@/brand.config'

describe('structured data', () => {
  it('publishes Organization, WebSite and FAQPage', () => {
    expect(organizationSchema()['@type']).toBe('Organization')
    expect(websiteSchema()['@type']).toBe('WebSite')
    expect(faqSchema()['@type']).toBe('FAQPage')
  })

  it('includes every FAQ item, with tokens resolved', () => {
    const schema = faqSchema()
    expect(schema.mainEntity).toHaveLength(COPY.faq.items.length)
    for (const entry of schema.mainEntity) {
      expect(entry.name).not.toMatch(/\{[a-zA-Z]+\}/)
      expect(entry.acceptedAnswer.text).not.toMatch(/\{[a-zA-Z]+\}/)
    }
  })

  it('omits Event schema while the street test is not planned', () => {
    expect(streetTestPlanned).toBe(false)
    expect(eventSchema()).toBeNull()
    expect(JSON.stringify(jsonLdForLanding())).not.toContain('"Event"')
  })

  it('emits no review, rating or Product node anywhere', () => {
    const serialized = JSON.stringify(jsonLdForLanding())
    for (const forbidden of [
      'aggregateRating',
      'ratingValue',
      'reviewCount',
      'bestRating',
      '"Review"',
      '"Product"',
      '"AggregateRating"',
    ]) {
      expect(serialized, forbidden).not.toContain(forbidden)
    }
  })
})
