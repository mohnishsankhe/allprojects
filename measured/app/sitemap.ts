import type { MetadataRoute } from 'next'
import { env } from '@/brand.config'

export const dynamic = 'force-static'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${env.siteUrl}/`, changeFrequency: 'weekly', priority: 1 },
    { url: `${env.siteUrl}/receipts`, changeFrequency: 'weekly', priority: 0.8 },
  ]
}
