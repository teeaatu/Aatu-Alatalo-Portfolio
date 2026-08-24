import fs from 'node:fs';
import path from 'node:path';
import { exec } from 'node:child_process';
import { promisify } from 'node:util';
import { readYaml, writeYaml, restoreLatestBackup, getAvailableBackups } from './creative-yaml.js';

const execAsync = promisify(exec);

export function creativeDevPlugin() {
  return {
    name: 'creative-dev-plugin',
    configureServer(server) {
      server.middlewares.use(async (req, res, next) => {
        if (!req.url?.startsWith('/api/creative/')) {
          return next();
        }

        const url = new URL(req.url, 'http://localhost');
        const pathname = url.pathname;

        const sendJson = (statusCode, data) => {
          res.statusCode = statusCode;
          res.setHeader('Content-Type', 'application/json');
          res.end(JSON.stringify(data));
        };

        const readBody = () => new Promise((resolve, reject) => {
          let data = '';
          req.on('data', chunk => { data += chunk; });
          req.on('end', () => {
            try {
              resolve(data ? JSON.parse(data) : {});
            } catch (e) {
              resolve({});
            }
          });
          req.on('error', reject);
        });

        try {
          if (pathname === '/api/creative/save-order' && req.method === 'POST') {
            const body = await readBody();
            const { category, order } = body;
            if (!category || !Array.isArray(order)) {
              return sendJson(400, { error: 'Virheelliset parametrit: category ja order vaaditaan.' });
            }
            const currentData = readYaml(category);
            if (!currentData || !Array.isArray(currentData)) {
              return sendJson(404, { error: `Kategorian dataa ei löytynyt: ${category}` });
            }
            const getItemKey = (item) => {
              if (item.kuva) return item.kuva;
              if (item.layout === 'diptych' && item.images && item.images[0]?.kuva) {
                return item.images.map(i => i.kuva).join('|');
              }
              if (item.otsikko) return `text_${item.otsikko}`;
              return JSON.stringify(item);
            };
            const itemMap = new Map();
            currentData.forEach(item => {
              itemMap.set(getItemKey(item), item);
            });
            const reorderedData = [];
            const usedKeys = new Set();
            for (const key of order) {
              if (itemMap.has(key)) {
                reorderedData.push(itemMap.get(key));
                usedKeys.add(key);
              }
            }
            currentData.forEach(item => {
              const key = getItemKey(item);
              if (!usedKeys.has(key)) reorderedData.push(item);
            });
            writeYaml(category, reorderedData);
            return sendJson(200, { success: true, count: reorderedData.length });
          }

          if (pathname === '/api/creative/save-categories' && req.method === 'POST') {
            const body = await readBody();
            const { categoryOrder } = body;
            if (!Array.isArray(categoryOrder)) {
              return sendJson(400, { error: 'Virheellinen parametri: categoryOrder vaaditaan listana.' });
            }
            const currentCategories = readYaml('categories');
            if (!currentCategories || !Array.isArray(currentCategories)) {
              return sendJson(404, { error: 'categories.yml ei löytynyt.' });
            }
            const catMap = new Map();
            currentCategories.forEach(cat => catMap.set(cat.id, cat));
            const reordered = [];
            const usedIds = new Set();
            for (const id of categoryOrder) {
              if (catMap.has(id)) {
                reordered.push(catMap.get(id));
                usedIds.add(id);
              }
            }
            currentCategories.forEach(cat => {
              if (!usedIds.has(cat.id)) reordered.push(cat);
            });
            writeYaml('categories', reordered);
            return sendJson(200, { success: true, count: reordered.length });
          }

          if (pathname === '/api/creative/delete-image' && req.method === 'POST') {
            const body = await readBody();
            const { category, imageKey } = body;
            if (!category || !imageKey) {
              return sendJson(400, { error: 'Virheelliset parametrit: category ja imageKey vaaditaan.' });
            }
            const currentData = readYaml(category);
            if (!currentData || !Array.isArray(currentData)) {
              return sendJson(404, { error: `Kategoriaa ei löytynyt: ${category}` });
            }
            const getItemKey = (item) => {
              if (item.kuva) return item.kuva;
              if (item.layout === 'diptych' && item.images && item.images[0]?.kuva) {
                return item.images.map(i => i.kuva).join('|');
              }
              if (item.otsikko) return `text_${item.otsikko}`;
              return JSON.stringify(item);
            };
            const initialLength = currentData.length;
            const filteredData = currentData.filter(item => getItemKey(item) !== imageKey);
            if (filteredData.length === initialLength) {
              return sendJson(404, { error: 'Poistettavaa kuvaa ei löytynyt.' });
            }
            writeYaml(category, filteredData);
            return sendJson(200, { success: true, remaining: filteredData.length });
          }

          if (pathname === '/api/creative/restore-backup' && req.method === 'POST') {
            const body = await readBody();
            const { category } = body;
            const restored = restoreLatestBackup(category);
            if (!restored) {
              return sendJson(404, { error: 'Ei löytynyt varmuuskopiota palautettavaksi.' });
            }
            return sendJson(200, { success: true, message: `Varmuuskopio palautettu kategorialle: ${category}` });
          }

          if (pathname === '/api/creative/upload-image' && req.method === 'POST') {
            const body = await readBody();
            const { category, kuva, otsikko, paikka, alt_text, position, width, height, series } = body;
            if (!category || !kuva) {
              return sendJson(400, { error: 'Kategoria ja kuva (URL) ovat pakollisia.' });
            }
            const currentData = readYaml(category) || [];
            const newEntry = {
              kuva,
              width: Number(width) || 2000,
              height: Number(height) || 1500,
              alt_text: alt_text || ''
            };
            if (otsikko) newEntry.otsikko = otsikko;
            if (paikka) newEntry.paikka = paikka;
            if (series) newEntry.series = series;

            if (typeof position === 'number') {
              const pos = Math.max(0, Math.min(position, currentData.length));
              currentData.splice(pos, 0, newEntry);
            } else if (position === 'start') {
              currentData.unshift(newEntry);
            } else {
              currentData.push(newEntry);
            }

            writeYaml(category, currentData);
            return sendJson(200, { success: true, item: newEntry, count: currentData.length });
          }

          if (pathname === '/api/creative/publish' && req.method === 'POST') {
            const body = await readBody();
            const commitMsg = body.message || 'Creative Mode: Päivitetty kuvat ja järjestys';
            await execAsync('npm run build', { cwd: process.cwd() });
            await execAsync('git add src/data/', { cwd: process.cwd() });
            const { stdout: statusOut } = await execAsync('git status --porcelain src/data/', { cwd: process.cwd() });
            if (statusOut.trim().length > 0) {
              await execAsync(`git commit -m "${commitMsg.replace(/"/g, '\\"')}"`, { cwd: process.cwd() });
            }
            let pushOutput = '';
            try {
              const { stdout: pushOut, stderr: pushErr } = await execAsync('git push', { cwd: process.cwd() });
              pushOutput = pushOut + (pushErr ? `\n${pushErr}` : '');
            } catch (pushError) {
              pushOutput = `Git push huomautus: ${pushError?.message || pushError}`;
            }
            return sendJson(200, { success: true, message: 'Julkaistu onnistuneesti!', details: pushOutput });
          }

          return next();
        } catch (err) {
          return sendJson(500, { error: err?.message || 'Palvelinvirhe' });
        }
      });
    }
  };
}
