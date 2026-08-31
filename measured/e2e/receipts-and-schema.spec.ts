import { expect, test } from '@playwright/test'

/** Criteria 4 and 6: no rating schema anywhere, and the empty module at 360px. */

const FORBIDDEN = [
  'aggregateRating',
  'ratingValue',
  'reviewCount',
  'bestRating',
  'worstRating',
  '"@type":"Review"',
  '"@type":"AggregateRating"',
  '"@type":"Product"',
]

test.describe('no review or rating markup', () => {
  for (const path of ['/?v=proof', '/?v=hope', '/receipts']) {
    test(`${path} emits none of it`, async ({ page }) => {
      await page.goto(path)
      const html = await page.content()
      for (const needle of FORBIDDEN) {
        expect(html, `${path} contains ${needle}`).not.toContain(needle)
      }
    })
  }

  test('the JSON-LD carries only the intended node types', async ({ page }) => {
    await page.goto('/?v=proof')
    const blocks = await page.locator('script[type="application/ld+json"]').allTextContents()
    expect(blocks.length).toBeGreaterThan(0)

    const types = new Set<string>()
    for (const block of blocks) {
      JSON.stringify(JSON.parse(block), (key, value) => {
        if (key === '@type' && typeof value === 'string') types.add(value)
        return value
      })
    }
    expect(types).toContain('Organization')
    expect(types).toContain('WebSite')
    expect(types).toContain('FAQPage')
    expect(types).not.toContain('Review')
    expect(types).not.toContain('AggregateRating')
    expect(types).not.toContain('Product')
    // The street test is not planned, so it is not announced.
    expect(types).not.toContain('Event')
  })
})

test.describe('the deliberately empty reviews module', () => {
  test('renders without overflow at 360px', async ({ page }, testInfo) => {
    test.skip(testInfo.project.name !== 'mobile', 'layout floor is asserted on the mobile project')

    await page.goto('/?v=proof')
    const module = page.locator('[data-testid="empty-reviews"]')
    await module.scrollIntoViewIfNeeded()
    await expect(module).toBeVisible()

    const overflow = await page.evaluate(() => ({
      scroll: document.documentElement.scrollWidth,
      client: document.documentElement.clientWidth,
    }))
    expect(overflow.scroll, 'the page must not scroll sideways').toBe(overflow.client)

    const box = await module.boundingBox()
    expect(box!.width).toBeLessThanOrEqual(360)

    await expect(module).toContainText('This section is intentionally empty.')
    await expect(module).toContainText('Screenshot this. Check back. Hold us to it.')
    await expect(module.locator('svg')).toHaveCount(5)
    await expect(module).toHaveScreenshot('empty-reviews-360.png', { maxDiffPixelRatio: 0.01 })
  })
})

test.describe('receipts page', () => {
  test('renders one anchored row per live claim', async ({ page }) => {
    await page.goto('/receipts')
    for (const id of ['oil-20', 'climate-test', 'panel', 'invoice', 'guarantee', 'names', 'catalog']) {
      await expect(page.locator(`#${id}`)).toHaveCount(1)
    }
    // Conditional and disabled: it must not appear at all.
    await expect(page.locator('#street-test')).toHaveCount(0)
  })

  test('publishes the sources the invoice footnote promises', async ({ page }) => {
    await page.goto('/receipts#sources')
    await expect(page.locator('#sources')).toContainText('Sources & math')
    await expect(page.locator('#sources')).toContainText('category illustration')
  })

  test('a status chip links to its manifest row', async ({ page }) => {
    await page.goto('/?v=proof')
    await page.locator('a[href="/receipts#guarantee"]').first().click()
    await expect(page).toHaveURL(/\/receipts#guarantee$/)
    await expect(page.locator('#guarantee')).toBeVisible()
  })
})

test.describe('answer-engine surface', () => {
  test('llms.txt names the receipts page as canonical', async ({ request }) => {
    const res = await request.get('/llms.txt')
    expect(res.status()).toBe(200)
    const body = await res.text()
    expect(body).toContain('MEASURED')
    expect(body).toContain('/receipts')
    expect(body).not.toMatch(/\{[a-zA-Z]+\}/)
  })
})
