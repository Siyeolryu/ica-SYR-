/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'via.placeholder.com',
        pathname: '/**',
      },
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/**',
      },
    ],
    // 레거시 도메인 설정 (Next.js 14 이전 버전 호환)
    domains: ['via.placeholder.com', 'localhost'],
  },
}

module.exports = nextConfig




















