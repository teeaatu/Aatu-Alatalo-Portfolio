// @ts-check
import { defineConfig } from 'astro/config';
import yaml from '@rollup/plugin-yaml';
import { creativeDevPlugin } from './src/utils/creative-dev-server.js';

// https://astro.build/config
export default defineConfig({
  site: 'https://aatualatalo.com',
  redirects: {
    '/recent.html': '/recent',
    '/work1.html': '/work1',
    '/work2.html': '/work2',
    '/work3.html': '/work3',
    '/tapahtumat.html': '/tapahtumat',
    '/vari-ja-muoto.html': '/vari-ja-muoto',
    '/raw.html': '/raw',
    '/mustavalkoinen-sarja.html': '/mustavalkoinen-sarja',
    '/sisatilan-valo.html': '/sisatilan-valo',
    '/kiehtovat-rakennukset.html': '/kiehtovat-rakennukset',
    '/luonto-ja-ymparisto.html': '/luonto-ja-ymparisto',
    '/still-life.html': '/still-life',
    '/elaimet.html': '/elaimet',
    '/masters-2026.html': '/masters-2026',
    '/kuvaprojekti-ajasta-v365.html': '/kuvaprojekti-ajasta-v365'
  },
  prefetch: {
    defaultStrategy: 'hover'
  },
  devToolbar: { enabled: false },
  vite: {
    plugins: [yaml(), creativeDevPlugin()]
  }
});
