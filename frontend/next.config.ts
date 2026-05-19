import type { NextConfig } from 'next'

const nextConfig: NextConfig = {
  cacheComponents: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'shikimori.io',
        pathname: '/uploads/**',
      },
    ],
  },
}

export default nextConfig
