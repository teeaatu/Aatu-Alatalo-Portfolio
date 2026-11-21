import type { APIRoute } from 'astro';

// These filenames serve error pages, redirects or copies of the home galleries.
const excludedPages = new Set(['404', 'recent', 'work3', 'work4']);
const paths = Object.keys(import.meta.glob('./**/*.astro'))
  .map(file => file.slice(2, -'.astro'.length))
  .filter(page => !excludedPages.has(page.split('/').pop()!))
  .map(page => '/' + page.replace(/(^|\/)index$/, '$1').replace(/([^/])$/, '$1/'))
  .sort();

export const GET: APIRoute = ({ site }) => new Response(
  '<?xml version="1.0" encoding="UTF-8"?>\n' +
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
  paths.map(path => `  <url><loc>${new URL(path, site)}</loc></url>\n`).join('') +
  '</urlset>\n',
  { headers: { 'Content-Type': 'application/xml; charset=utf-8' } },
);
