/** @type {import('next').NextConfig} */
const nextConfig = {
  // 🚀 CI / Docker friendly
  output: 'standalone',

  // ⚡ Faster builds
  swcMinify: true,
  poweredByHeader: false,

  // 🧠 Caching & memory
  experimental: {
    turbo: {
      rules: {
        '*.ts': ['swc'],
        '*.tsx': ['swc'],
      },
    },
    optimizePackageImports: [
      'lucide-react',
      '@radix-ui/react-dialog',
      '@radix-ui/react-dropdown-menu',
      '@radix-ui/react-select',
      '@radix-ui/react-tabs',
      '@radix-ui/react-toast',
      '@tanstack/react-query',
      'date-fns',
    ],
  },

  // 🧹 Ignore lint & type errors in CI (handled separately)
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },

  // 🖼 Image optimisation
  images: {
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60 * 60 * 24 * 30, // 30 days
  },

  // 🌐 Headers caching
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' },
        ],
      },
    ];
  },
};

module.exports = nextConfig;