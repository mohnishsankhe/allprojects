import { ImageResponse } from 'next/og'
import { BRAND } from '@/brand.config'

export const alt = `${BRAND.name} — ${BRAND.descriptor}`
export const size = { width: 1200, height: 630 }
export const contentType = 'image/png'

/**
 * Black ground, the wordmark and its dot, the tagline beneath. Everything is
 * drawn from config, so a brand rename repaints the card with the build.
 *
 * No font file is fetched: a build that reaches out to a font CDN fails in any
 * network-restricted CI, and the card is strong enough on the built-in face.
 */
export default function OpengraphImage() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          background: '#0A0A0A',
          padding: '88px 96px',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'flex-end' }}>
          <div
            style={{
              fontSize: 132,
              letterSpacing: '-0.045em',
              color: '#FAF9F6',
              lineHeight: 1,
              fontWeight: 600,
            }}
          >
            {BRAND.name}
          </div>
          <div
            style={{
              width: 30,
              height: 30,
              borderRadius: 999,
              background: '#0B3BEC',
              marginLeft: 20,
              marginBottom: 16,
            }}
          />
        </div>

        <div style={{ display: 'flex', width: 132, height: 1, background: '#3A3A3A', margin: '44px 0' }} />

        <div style={{ fontSize: 46, color: '#FAF9F6', letterSpacing: '-0.02em' }}>{BRAND.tagline}</div>
        <div style={{ fontSize: 26, color: '#8A8A8A', marginTop: 22, letterSpacing: '0.16em' }}>
          {`${BRAND.descriptor.toUpperCase()} · ${BRAND.city.toUpperCase()}`}
        </div>
      </div>
    ),
    size,
  )
}
