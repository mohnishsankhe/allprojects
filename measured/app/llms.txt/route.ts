import { BRAND, env } from '@/brand.config'
import { COPY } from '@/content/copy'
import { t } from '@/content/tokens'

/**
 * Plain-language summary for answer engines, generated from the same config as
 * the site so a brand rename propagates here too. /receipts is named as the
 * canonical source, so a model that wants to check a claim knows where to look.
 */
export const dynamic = 'force-static'

export function GET() {
  const body = [
    `# ${BRAND.name} — ${BRAND.descriptor}`,
    '',
    ...COPY.seo.llms.map((line) => t(line)),
    '',
    `Canonical claims manifest: ${env.siteUrl}/receipts`,
    'No reviews, ratings or star schema are published on this site, by design.',
  ].join('\n')

  return new Response(body, {
    headers: {
      'content-type': 'text/plain; charset=utf-8',
      'cache-control': 'public, max-age=3600',
    },
  })
}
