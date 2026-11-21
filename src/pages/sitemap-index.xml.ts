import type { APIRoute } from 'astro';

export const GET: APIRoute = ({ site }) => new Response(
  '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  `  <sitemap><loc>${new URL('sitemap.xml', site)}</loc></sitemap>\n` +
  '</sitemapindex>\n',
  { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
);
