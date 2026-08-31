import { expect, test, type Page } from '@playwright/test'

/** Every analytics event must carry the variant, or the experiment cannot be read. */

type Captured = { name: string; props?: Record<string, unknown> }

async function captureEvents(page: Page): Promise<() => Promise<Captured[]>> {
  await page.addInitScript(() => {
    const w = window as unknown as { __events: Captured[]; plausible: unknown }
    w.__events = []
    w.plausible = (name: string, options?: { props?: Record<string, unknown> }) => {
      w.__events.push({ name, props: options?.props })
    }
  })
  return async () => page.evaluate(() => (window as unknown as { __events: Captured[] }).__events)
}

test.describe('analytics', () => {
  test('fires hero_view tagged with the variant', async ({ page }) => {
    const events = await captureEvents(page)
    await page.goto('/?v=hope')
    await expect.poll(async () => (await events()).some((e) => e.name === 'hero_view')).toBe(true)

    const hero = (await events()).find((e) => e.name === 'hero_view')
    expect(hero?.props?.variant).toBe('hope')
  })

  test('tags every emitted event with the variant', async ({ page }) => {
    const events = await captureEvents(page)
    await page.goto('/?v=proof')

    await page.locator('[data-section="hero"] a').first().click()
    await page.locator('summary').first().click()
    await page.mouse.wheel(0, 40_000)
    await page.waitForTimeout(600)

    const all = await events()
    expect(all.length).toBeGreaterThan(2)
    for (const event of all) {
      expect(event.props?.variant, `${event.name} is missing its variant`).toBe('proof')
    }
  })

  test('fires the CTA, FAQ and scroll events', async ({ page }) => {
    const events = await captureEvents(page)
    await page.goto('/?v=proof')

    await page.locator('[data-section="hero"] a').first().click()
    await expect.poll(async () => (await events()).map((e) => e.name)).toContain('cta_hero_click')

    await page.locator('summary').first().click()
    const faq = (await events()).find((e) => e.name === 'faq_open')
    expect(faq?.props?.q).toBeTruthy()

    await page.mouse.wheel(0, 60_000)
    await expect
      .poll(async () => (await events()).map((e) => e.name))
      .toEqual(expect.arrayContaining(['scroll_50', 'scroll_90']))
  })

  test('fires cta_sku_click with the sku and pre-tags the form', async ({ page }) => {
    const events = await captureEvents(page)
    await page.goto('/?v=proof')

    await page.locator('[data-section="line"] a', { hasText: 'Waitlist this' }).nth(2).click()
    const click = (await events()).find((e) => e.name === 'cta_sku_click')
    expect(click?.props?.sku).toBe('shaadi')
    await expect(page.locator('[data-testid="waitlist-form"] select')).toHaveValue('shaadi')
  })

  test('fires receipts_view and empty_reviews_view', async ({ page }) => {
    const events = await captureEvents(page)
    await page.goto('/?v=proof')
    await page.locator('[data-testid="empty-reviews"]').scrollIntoViewIfNeeded()
    await expect
      .poll(async () => (await events()).map((e) => e.name))
      .toEqual(expect.arrayContaining(['receipts_view', 'empty_reviews_view']))
  })
})
