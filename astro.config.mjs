// @ts-check
import { defineConfig } from 'astro/config';
import yaml from '@rollup/plugin-yaml';
import { creativeDevPlugin } from './src/utils/creative-dev-server.js';

// https://astro.build/config
export default defineConfig({
  site: 'https://aatualatalo.com',
  prefetch: {
    defaultStrategy: 'hover'
  },
  server: {
    host: true
  },
  devToolbar: { enabled: false },
  vite: {
    plugins: [yaml(), creativeDevPlugin()]
  }
});
