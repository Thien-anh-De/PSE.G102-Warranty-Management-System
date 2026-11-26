const nextConfig = {
  output: "export",
  trailingSlash: true,
  poweredByHeader: false,
  devIndicators: false,
  experimental: { cpus: 2 },
};

if (process.env.NODE_ENV === "development") {
  nextConfig.rewrites = async () => [
    {
      source: "/api/:path*",
      destination: `${process.env.PORTAL_API_ORIGIN || "http://127.0.0.1:8008"}/api/:path*`,
    },
  ];
}

export default nextConfig;
