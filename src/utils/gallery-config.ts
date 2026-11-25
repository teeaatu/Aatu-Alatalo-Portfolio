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
  description: Record<Lang, string>;
}

export const CATEGORIES: CategoryConfig[] = [
  {
    key: 'recent',
    enSlug: 'recent',
    group: 'primary',
    data: recent,
    label: l => l === 'fi' ? 'Uusimmat' : 'Recent',
    description: {
      fi: 'Aatu Alatalon tuoreimmat valokuvat Oulusta ja muualta Suomesta. Hasselblad Masters 2026 -finalisti (Project//21).',
      en: 'Recent photographs by Aatu Alatalo from Oulu and across Finland. Hasselblad Masters 2026 finalist (Project//21).',
    },
  },
  {
    key: 'masters-2026',
    enSlug: 'masters-2026',
    group: 'primary',
    data: masters,
    label: () => 'Hasselblad Masters 2026',
    description: {
      fi: 'Aatu Alatalon Hasselblad Masters 2026 -kilpailun Project//21-kategorian finalistisarja.',
      en: 'Aatu Alatalo’s finalist series in the Hasselblad Masters 2026 competition (Project//21 category).',
    },
  },
  {
    key: 'work1',
    enSlug: 'work1',
    group: 'primary',
    data: work1,
    label: l => l === 'fi' ? 'Työ I' : 'Work I',
    description: {
      fi: 'Työ I — Aatu Alatalon dokumentaarinen ja tunnelmallinen kuvasarja Suomesta.',
      en: 'Work I — A documentary and atmospheric photography series from Finland by Aatu Alatalo.',
    },
  },
  {
    key: 'work2',
    enSlug: 'work2',
    group: 'primary',
    data: work2,
    label: l => l === 'fi' ? 'Työ II' : 'Work II',
    description: {
      fi: 'Työ II — Aatu Alatalon urbaaneja havaintoja valosta, varjoista ja kaupunkitilasta.',
      en: 'Work II — Urban observations of light, shadow, and city space by photographer Aatu Alatalo.',
    },
  },
  {
    key: 'tapahtumat',
    enSlug: 'events',
    group: 'category',
    data: tapahtumat,
    label: l => t.events[l],
    description: {
      fi: 'Tapahtuma- ja festivaalivalokuvia, mukana muun muassa Qstock Oulussa — Aatu Alatalo.',
      en: 'Event and festival photography, including Qstock Festival in Oulu, Finland — Aatu Alatalo.',
    },
  },
  {
    key: 'vari-ja-muoto',
    enSlug: 'color-and-form',
    group: 'category',
    data: variJaMuoto,
    label: l => t.color_and_form[l],
    description: {
      fi: 'Väri ja muoto — visuaalisia tutkielmia väreistä, rytmistä ja sommittelusta — Aatu Alatalo.',
      en: 'Color & Form — visual studies of color, rhythm, and composition by photographer Aatu Alatalo.',
    },
  },
  {
    key: 'raw',
    enSlug: 'raw',
    group: 'category',
    data: raw,
    label: l => t.portraits[l],
    description: {
      fi: 'Muotokuvia ihmisistä luonnonvalossa ja studiossa — valokuvaaja Aatu Alatalo, Oulu.',
      en: 'Portraits photographed in natural light and studio settings by Aatu Alatalo in Oulu, Finland.',
    },
  },
  {
    key: 'mustavalkoinen-sarja',
    enSlug: 'black-and-white-series',
    group: 'category',
    data: mustavalkoinenSarja,
    label: l => t.monochrome[l],
    description: {
      fi: 'Mustavalkoinen sarja — ajattomia sävyjä, katunäkymiä ja henkilökuvia — Aatu Alatalo.',
      en: 'Monochrome — timeless black and white street scenes and portraits by Aatu Alatalo.',
    },
  },
  {
    key: 'sisatilan-valo',
    enSlug: 'interior-light',
    group: 'category',
    data: sisatilanValo,
    label: l => t.interior[l],
    description: {
      fi: 'Valo sisällä — hiljaisia sisätiloja ja luonnonvalon leikkiä — Aatu Alatalo.',
      en: 'Available Light — quiet interiors and natural light studies by photographer Aatu Alatalo.',
    },
  },
  {
    key: 'kiehtovat-rakennukset',
    enSlug: 'buildings',
    group: 'category',
    data: kiehtovatRakennukset,
    label: l => t.buildings[l],
    description: {
      fi: 'Arkkitehtuuri — rakennusten muotoja, pintoja ja tiloja Suomesta — Aatu Alatalo.',
      en: 'Architecture — studies of buildings, surfaces, and spaces in Finland by Aatu Alatalo.',
    },
  },
  {
    key: 'luonto-ja-ymparisto',
    enSlug: 'nature',
    group: 'category',
    data: luontoJaYmparisto,
    label: l => t.nature[l],
    description: {
      fi: 'Maisema — pohjoisia maisemia, luontoa ja vuodenajoista muuttuvia näkymiä — Aatu Alatalo.',
      en: 'Landscape — Nordic landscapes, nature, and seasonal views by photographer Aatu Alatalo.',
    },
  },
  {
    key: 'still-life',
    enSlug: 'still-life',
    group: 'category',
    data: stillLife,
    label: l => t.still_life[l],
    description: {
      fi: 'Asetelmat — pelkistettyjä asetelmakuvia ja yksityiskohtia luonnonvalossa — Aatu Alatalo.',
      en: 'Still Life — minimal still-life compositions and natural-light details by Aatu Alatalo.',
    },
  },
  {
    key: 'elaimet',
    enSlug: 'animals',
    group: 'category',
    data: elaimet,
    label: l => t.animals[l],
    description: {
      fi: 'Eläimet — tunnelmallisia hetkiä eläimistä luonnossa ja arjessa — Aatu Alatalo.',
      en: 'Animals — candid moments with animals in nature and everyday life by Aatu Alatalo.',
    },
  },
  {
    key: 'kuvaprojekti-ajasta-v365',
    enSlug: 'photo-project-time-v365',
    group: 'project',
    data: v365,
    label: l => t.v365[l],
    description: {
      fi: 'Kuvaprojekti ajasta v.365 — visuaalinen projekti ajankulusta ja arjen havainnoista — Aatu Alatalo.',
      en: 'V365 — a personal photography project exploring time and everyday observations by Aatu Alatalo.',
    },
  },
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

export function getCategoryDescription(key: string, lang: Lang): string {
  const cat = CATEGORY_BY_KEY.get(key);
  if (cat) return cat.description[lang];
  return lang === 'fi'
    ? 'Aatu Alatalo (s. 25. tammikuuta 2005, Tyrnävä) on Oulussa asuva valokuvaaja ja Hasselblad Masters 2026 -finalisti.'
    : 'Aatu Alatalo is a photographer from Tyrnävä, based in Oulu, Finland, and a Hasselblad Masters 2026 finalist.';
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
