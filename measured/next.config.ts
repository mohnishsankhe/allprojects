import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  reactStrictMode: true,
  poweredByHeader: false,
  compress: true,
  experimental: {
    /*
     * The stylesheet is small but render-blocking, and on a high-latency
     * mobile connection that round trip is the single largest slice of first
     * paint. Inlining it into the document removes the request entirely.
     */
    inlineCss: true,
  },
}

export default nextConfig
