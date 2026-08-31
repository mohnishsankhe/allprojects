import { NextResponse, type NextRequest } from 'next/server'
import {
  VARIANT_COOKIE,
  VARIANT_HEADER,
  VARIANT_PARAM,
  resolveVariant,
  variantCookieOptions,
} from '@/lib/variant'

/**
 * Next 16 renamed `middleware.ts` to `proxy.ts` (Node runtime only). Assigns
 * the A/B arm once per visitor and hands it to the render.
 *
 * The variant is written twice on purpose:
 *
 *   1. onto the REQUEST, as a header, because on a first visit the cookie only
 *      exists on the response — `await cookies()` inside the page would not see
 *      it on that same request, and the visitor would get the default arm while
 *      their cookie said otherwise;
 *   2. onto the RESPONSE, as a cookie, so the arm survives the next visit.
 *
 * The cookie is httpOnly: the client never reads it. The server passes the
 * variant down as a prop, so there is exactly one source of truth and the
 * client cannot drift from what was rendered.
 *
 * ?v= is deliberately not stripped by a redirect — a redirect would cost a
 * round trip on cold 4G traffic and mangle UTM-tagged ad URLs. A canonical
 * link tag keeps search engines from splitting on the param instead.
 */
export function proxy(request: NextRequest) {
  const param = request.nextUrl.searchParams.get(VARIANT_PARAM)
  const cookie = request.cookies.get(VARIANT_COOKIE)?.value
  const { variant, assigned } = resolveVariant(param, cookie)

  const headers = new Headers(request.headers)
  headers.set(VARIANT_HEADER, variant)

  const response = NextResponse.next({ request: { headers } })

  if (assigned || cookie !== variant) {
    response.cookies.set(VARIANT_COOKIE, variant, variantCookieOptions)
  }

  // The HTML is now visitor-specific. A shared cache serving one visitor's arm
  // to everyone would silently destroy the experiment while the site still
  // looked fine, so the document is never stored by a shared or private cache.
  response.headers.set('Cache-Control', 'private, no-store, must-revalidate')

  return response
}

export const config = {
  matcher: [
    /*
     * Everything except static assets and the files that must stay cacheable.
     * Assets are variant-independent and are served with immutable caching, so
     * keeping them out of the proxy is what protects the LCP budget.
     */
    '/((?!_next/static|_next/image|favicon.ico|icon.svg|opengraph-image|robots.txt|sitemap.xml|llms.txt).*)',
  ],
}
