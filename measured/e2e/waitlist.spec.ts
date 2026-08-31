import { expect, test } from '@playwright/test'

/** Criterion 5: the round trip, and an error state that does not lie. */

test.describe('waitlist', () => {
  test('sends variant, utm and sku, then confirms', async ({ page }) => {
    let payload: Record<string, unknown> | null = null

    await page.route('**/api/waitlist', async (route) => {
      payload = JSON.parse(route.request().postData() ?? '{}')
      await route.fulfill({ json: { ok: true, contactType: 'email' } })
    })

    await page.goto('/?v=hope&utm_source=meta&utm_campaign=cold-1')
    await page.locator('[data-section="line"] a', { hasText: 'Waitlist this' }).first().click()
    await page.locator('[data-testid="waitlist-form"] input[type="email"]').fill('reader@example.com')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()

    await expect(page.locator('[data-testid="waitlist-success"]')).toBeVisible()
    await expect(page.locator('[data-testid="waitlist-success"]')).toContainText('the panel protocol')

    expect(payload).toMatchObject({
      email: 'reader@example.com',
      sku: 'date',
      utm: { utm_source: 'meta', utm_campaign: 'cold-1' },
    })
  })

  test('accepts a WhatsApp number instead of an email', async ({ page }) => {
    let payload: Record<string, unknown> | null = null
    await page.route('**/api/waitlist', async (route) => {
      payload = JSON.parse(route.request().postData() ?? '{}')
      await route.fulfill({ json: { ok: true, contactType: 'phone' } })
    })

    await page.goto('/?v=proof')
    await page.locator('[data-testid="waitlist-form"] input[type="tel"]').fill('+91 98765 43210')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()
    await expect(page.locator('[data-testid="waitlist-success"]')).toBeVisible()
    expect(payload).toMatchObject({ phone: '+91 98765 43210' })
  })

  test('validates before it sends', async ({ page }) => {
    let called = false
    await page.route('**/api/waitlist', async (route) => {
      called = true
      await route.fulfill({ json: { ok: true } })
    })

    await page.goto('/?v=proof')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()
    await expect(page.locator('[data-testid="waitlist-error"]')).toContainText('email address or a WhatsApp')

    await page.locator('[data-testid="waitlist-form"] input[type="email"]').fill('not-an-email')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()
    await expect(page.locator('[data-testid="waitlist-error"]')).toContainText('does not look right')

    expect(called, 'no request should reach the server for invalid input').toBe(false)
  })

  test('fails honestly when the webhook is down', async ({ page }) => {
    await page.route('**/api/waitlist', (route) => route.fulfill({ status: 502, json: { ok: false, error: 'generic' } }))

    await page.goto('/?v=proof')
    await page.locator('[data-testid="waitlist-form"] input[type="email"]').fill('reader@example.com')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()

    // It must not claim success, and it must say nothing was saved.
    await expect(page.locator('[data-testid="waitlist-error"]')).toContainText('Nothing was saved')
    await expect(page.locator('[data-testid="waitlist-success"]')).toHaveCount(0)
  })

  test('says so plainly when the waitlist is not connected', async ({ page }) => {
    await page.route('**/api/waitlist', (route) =>
      route.fulfill({ status: 503, json: { ok: false, error: 'notConfigured' } }),
    )
    await page.goto('/?v=proof')
    await page.locator('[data-testid="waitlist-form"] input[type="email"]').fill('reader@example.com')
    await page.locator('[data-testid="waitlist-form"] button[type="submit"]').click()
    await expect(page.locator('[data-testid="waitlist-error"]')).toContainText('not connected yet')
  })

  test('shows the proof and hope headings on the same form', async ({ page }) => {
    await page.goto('/?v=proof')
    await expect(page.locator('#waitlist-heading')).toContainText('Be one of the first 1,000 noses.')
    await page.goto('/?v=hope')
    await expect(page.locator('#waitlist-heading')).toContainText('Get early access.')
  })
})
