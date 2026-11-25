import t from '../data/t.yml';
import recent from '../data/recent.yml';
import work1 from '../data/work1.yml';
import work2 from '../data/work2.yml';
import tapahtumat from '../data/tapahtumat.yml';
import variJaMuoto from '../data/vari-ja-muoto.yml';
import raw from '../data/raw.yml';
import mustavalkoinenSarja from '../data/mustavalkoinen-sarja.yml';
import sisatilanValo from '../data/sisatilan-valo.yml';
import kiehtovatRakennukset from '../data/kiehtovat-rakennukset.yml';
import luontoJaYmparisto from '../data/luonto-ja-ymparisto.yml';
import stillLife from '../data/still-life.yml';
import elaimet from '../data/elaimet.yml';
import masters from '../data/masters-2026.yml';
import v365 from '../data/kuvaprojekti_ajasta_v365.yml';

export type Lang = 'fi' | 'en';

export interface CategoryConfig {
  key: string;
  enSlug: string;
  group: 'primary' | 'category' | 'project';
  data: any[];
  label: (lang: Lang) => string;
}

export const CATEGORIES: CategoryConfig[] = [
  { key: 'recent', enSlug: 'recent', group: 'primary', data: recent, label: l => l === 'fi' ? 'Uusimmat' : 'Recent' },
  { key: 'masters-2026', enSlug: 'masters-2026', group: 'primary', data: masters, label: () => 'Hasselblad Masters 2026' },
  { key: 'work1', enSlug: 'work1', group: 'primary', data: work1, label: l => l === 'fi' ? 'Työ I' : 'Work I' },
  { key: 'work2', enSlug: 'work2', group: 'primary', data: work2, label: l => l === 'fi' ? 'Työ II' : 'Work II' },
  { key: 'tapahtumat', enSlug: 'events', group: 'category', data: tapahtumat, label: l => t.events[l] },
  { key: 'vari-ja-muoto', enSlug: 'color-and-form', group: 'category', data: variJaMuoto, label: l => t.color_and_form[l] },
  { key: 'raw', enSlug: 'raw', group: 'category', data: raw, label: l => t.portraits[l] },
  { key: 'mustavalkoinen-sarja', enSlug: 'black-and-white-series', group: 'category', data: mustavalkoinenSarja, label: l => t.monochrome[l] },
  { key: 'sisatilan-valo', enSlug: 'interior-light', group: 'category', data: sisatilanValo, label: l => t.interior[l] },
  { key: 'kiehtovat-rakennukset', enSlug: 'buildings', group: 'category', data: kiehtovatRakennukset, label: l => t.buildings[l] },
  { key: 'luonto-ja-ymparisto', enSlug: 'nature', group: 'category', data: luontoJaYmparisto, label: l => t.nature[l] },
  { key: 'still-life', enSlug: 'still-life', group: 'category', data: stillLife, label: l => t.still_life[l] },
  { key: 'elaimet', enSlug: 'animals', group: 'category', data: elaimet, label: l => t.animals[l] },
  { key: 'kuvaprojekti-ajasta-v365', enSlug: 'photo-project-time-v365', group: 'project', data: v365, label: l => t.v365[l] },
];

const CATEGORY_BY_KEY = new Map(CATEGORIES.map(cat => [cat.key, cat]));

// Older R2 uploads that do not have a _desktop.avif variant; omitting them prevents 404 console errors.
const MISSING_R2_AVIF = new Set(['lohi_norja', 'mersu', 'sinisethousut']);

export function getCategoryUrl(key: string, lang: Lang): string {
  const cat = CATEGORY_BY_KEY.get(key);
  const slug = lang === 'en' ? (cat?.enSlug || key) : key;
  return lang === 'en' ? `/en/${slug}/` : `/${slug}/`;
}

export function getCategoryLabel(key: string, lang: Lang, fallback = ''): string {
  const cat = CATEGORY_BY_KEY.get(key);
  return cat ? cat.label(lang) : (fallback || key);
}

export function parseLocalizedField(val: unknown, lang: Lang): string {
  if (val === undefined || val === null || val === '') return '';
  const str = String(val);
  if (str.includes(' / ')) {
    const parts = str.split(' / ');
    return lang === 'fi'
      ? (parts[1]?.trim() || parts[0]?.trim() || '')
      : (parts[0]?.trim() || parts[1]?.trim() || '');
  }
  return str;
}

export function resolveImagePaths(kuva: string) {
  const queryIdx = kuva.search(/[?#]/);
  const cleanUrl = queryIdx >= 0 ? kuva.slice(0, queryIdx) : kuva;
  const querySuffix = queryIdx >= 0 ? kuva.slice(queryIdx) : '';
  const fileName = cleanUrl.split('/').pop() || '';
  const dotIdx = fileName.lastIndexOf('.');
  const stem = dotIdx > 0 ? fileName.slice(0, dotIdx) : fileName;

  const mob = `${stem}_mobile.webp`;
  const dsk = `${stem}_desktop.webp`;

  if (cleanUrl.startsWith('http://') || cleanUrl.startsWith('https://')) {
    const baseDir = cleanUrl.slice(0, cleanUrl.length - fileName.length);
    return {
      src: `${baseDir}thumbs/${dsk}${querySuffix}`,
      srcAvif: MISSING_R2_AVIF.has(stem) ? null : `${baseDir}thumbs/${stem}_desktop.avif${querySuffix}`,
      srcMob: `${baseDir}thumbs/${mob}${querySuffix}`,
      full: kuva,
    };
  }

  return {
    src: `/assets/thumbnails/${dsk}`,
    srcAvif: null,
    srcMob: `/assets/thumbnails/${mob}`,
    full: `/assets/images/${kuva}`,
  };
}

export function canonicalPath(path: string): string {
  const withSlash = path.endsWith('/') ? path : `${path}/`;
  if (withSlash === '/recent/') return '/';
  if (withSlash === '/en/recent/') return '/en/';
  return withSlash;
}
