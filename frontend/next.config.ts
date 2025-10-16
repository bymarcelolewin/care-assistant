import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  output: 'export',

  // Disable features that require server-side rendering
  images: {
    unoptimized: true,
  },

  // Rewrites only work in development mode, not in static export
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ]
  },
};

export default nextConfig;
