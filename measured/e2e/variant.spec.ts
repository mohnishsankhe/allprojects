import { expect, test, type Page } from '@playwright/test'

/** Acceptance criterion 2: variant copy, section order, cookie persistence, events. */

const PROOF_H1 = 'Measured, not promised.'
const HOPE_H1 = 'Smell unforgettable.'

async function sectionOrder(page: Page): Promise<string[]> {
  return page.locator('main [data-section]').evaluateAll((nodes) =>
    nodes.map((n) => n.getAttribute('data-section') ?? ''),
  )
}

test.describe('A/B variant', () => {
  test('?v=proof renders the proof hero and the written section order', async ({ page }) => {
    await page.goto('/?v=proof')
    await expect(page.locator('h1')).toHaveText(PROOF_H1)
    await expect(page.locator('h1')).toHaveCount(1)
    await expect(page.locator('main')).toHaveAttribute('data-variant', 'proof')

    const order = await sectionOrder(page)
    expect(order).toEqual([
      'hero',
      'manifesto',
      'invoice',
      'method',
      'line',
      'receipts',
      'faq',
      'waitlist',
    ])
    // The proof arm leads with the argument, not the product.
    expect(order.indexOf('manifesto')).toBeLessThan(order.indexOf('line'))
  })

  test('?v=hope renders the hope hero and moves the SKUs above the manifesto', async ({ page }) => {
    await page.goto('/?v=hope')
    await expect(page.locator('h1')).toHaveText(HOPE_H1)
    await expect(page.locator('h1')).toHaveCount(1)
    await expect(page.locator('main')).toHaveAttribute('data-variant', 'hope')

    const order = await sectionOrder(page)
    expect(order.indexOf('line')).toBeLessThan(order.indexOf('manifesto'))
    expect(order.indexOf('line')).toBeLessThan(order.indexOf('invoice'))
    expect(order.indexOf('line')).toBeLessThan(order.indexOf('method'))
  })

  test('only one variant is ever in the DOM', async ({ page }) => {
    await page.goto('/?v=proof')
    await expect(page.locator('main')).not.toContainText(HOPE_H1)

    await page.goto('/?v=hope')
    await expect(page.locator('main')).not.toContainText(PROOF_H1)
  })

  test('the hope arm shows no secondary CTA', async ({ page }) => {
    await page.goto('/?v=hope')
    await expect(page.locator('[data-section="hero"] a', { hasText: 'Read the receipts' })).toHaveCount(0)

    await page.goto('/?v=proof')
    await expect(page.locator('[data-section="hero"] a', { hasText: 'Read the receipts' })).toHaveCount(1)
  })

  test('the arm persists in a cookie across a param-less visit', async ({ page, context }) => {
    await page.goto('/?v=hope')
    const cookie = (await context.cookies()).find((c) => c.name === 'variant')
    expect(cookie?.value).toBe('hope')
    expect(cookie?.httpOnly).toBe(true)

    await page.goto('/')
    await expect(page.locator('h1')).toHaveText(HOPE_H1)

    await page.reload()
    await expect(page.locator('h1')).toHaveText(HOPE_H1)
  })

  test('a first-time visitor is assigned one of the two arms', async ({ page, context }) => {
    await context.clearCookies()
    await page.goto('/')
    const cookie = (await context.cookies()).find((c) => c.name === 'variant')
    expect(['proof', 'hope']).toContain(cookie?.value)
    await expect(page.locator('h1')).toHaveText(cookie?.value === 'hope' ? HOPE_H1 : PROOF_H1)
  })

  test('the document is never stored by a shared cache', async ({ page }) => {
    const response = await page.goto('/?v=proof')
    // A CDN caching one visitor's arm and serving it to everyone would destroy
    // the experiment silently, so this header is load-bearing.
    expect(response?.headers()['cache-control']).toContain('no-store')
  })
})
