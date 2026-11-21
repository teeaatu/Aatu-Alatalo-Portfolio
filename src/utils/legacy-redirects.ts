import type { APIRoute } from 'astro';

const redirects = {
  '/recent.html': '/recent/',
  '/work1.html': '/work1/',
  '/work2.html': '/work2/',
  '/work3.html': '/work2/',
  '/tapahtumat.html': '/tapahtumat/',
  '/vari-ja-muoto.html': '/vari-ja-muoto/',
  '/kirjaston-ihmeet.html': '/vari-ja-muoto/',
  '/raw.html': '/raw/',
  '/mustavalkoinen-sarja.html': '/mustavalkoinen-sarja/',
  '/sisatilan-valo.html': '/sisatilan-valo/',
  '/kiehtovat-rakennukset.html': '/kiehtovat-rakennukset/',
  '/luonto-ja-ymparisto.html': '/luonto-ja-ymparisto/',
  '/still-life.html': '/still-life/',
  '/elaimet.html': '/elaimet/',
  '/masters-2026.html': '/masters-2026/',
  '/kuvaprojekti-ajasta-v365.html': '/kuvaprojekti-ajasta-v365/',
  '/about.html': '/recent/#jd-about-panel',
  '/en/about.html': '/en/#jd-about-panel',
  '/en/animals.html': '/en/animals/',
  '/en/black-and-white-series.html': '/en/black-and-white-series/',
  '/en/buildings.html': '/en/buildings/',
  '/en/color-and-form.html': '/en/color-and-form/',
  '/en/events.html': '/en/events/',
  '/en/interior-light.html': '/en/interior-light/',
  '/en/kirjaston-ihmeet.html': '/en/color-and-form/',
  '/en/masters-2026.html': '/en/masters-2026/',
  '/en/nature.html': '/en/nature/',
  '/en/photo-project-time-v365.html': '/en/photo-project-time-v365/',
  '/en/raw.html': '/en/raw/',
  '/en/recent.html': '/en/',
  '/en/still-life.html': '/en/still-life/'
};

export function legacyPaths(language: 'fi' | 'en') {
  return Object.entries(redirects)
    .filter(([oldPath]) => oldPath.startsWith('/en/') === (language === 'en'))
    .map(([oldPath, destination]) => ({
      params: { legacy: oldPath.split('/').pop()!.slice(0, -'.html'.length) },
      props: { destination, language },
    }));
}

// GitHub Pages serves static files. An immediate meta refresh also works
// without JavaScript and is treated as a permanent redirect by Google.
export const legacyRedirect: APIRoute = ({ props }) => {
  const { destination, language } = props;
  const label = language === 'fi' ? 'Sivu on siirtynyt' : 'This page has moved';
  return new Response(`<!doctype html>
<html lang="${language}">
<head>
  <meta charset="utf-8">
  <meta http-equiv="refresh" content="0; url=${destination}">
  <title>${label}</title>
</head>
<body><a href="${destination}">${label}</a></body>
</html>
`, { headers: { 'Content-Type': 'text/html; charset=utf-8' } });
};
