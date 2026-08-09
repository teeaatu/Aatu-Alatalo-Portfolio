import etusivu from '../data/etusivu.yml';
import variJaMuoto from '../data/vari-ja-muoto.yml';
import luonto from '../data/luonto-ja-ymparisto.yml';
import masters from '../data/masters-2026.yml';
import mustavalkoinen from '../data/mustavalkoinen-sarja.yml';
import raw from '../data/raw.yml';
import sisatilanValo from '../data/sisatilan-valo.yml';
import elaimet from '../data/elaimet.yml';
import rakennukset from '../data/kiehtovat-rakennukset.yml';
import stillLife from '../data/still-life.yml';
import v365 from '../data/kuvaprojekti_ajasta_v365.yml';
import tapahtumat from '../data/tapahtumat.yml';
import lqipData from '../data/lqip.json';

export function getOverviewImages() {
  const datasets = [
    etusivu, variJaMuoto, luonto, masters, mustavalkoinen, raw, 
    sisatilanValo, elaimet, rakennukset, stillLife, v365, tapahtumat
  ];

  let priorityPinned = [];
  let pinned = [];
  let standard = [];

  datasets.forEach(dataset => {
    if (!dataset) return;
    dataset.forEach((item, index) => {
      if (item.tyyppi === 'teksti') return;

      const processItem = (imgData, isDiptych, dIndex) => {
        const pinPriority = item.pin_priority || 999;
        const alt = imgData.alt_text || 'EMPTY_ALT';
        const title = item.otsikko || 'EMPTY_OTSIKKO';
        const orientation = imgData.orientation || (item.orientation || 'unknown');
        const itemType = item.item_type || 'image';
        const linkUrl = item.link_url || 'none';
        const linkTextFi = item.link_text_fi || 'Siirry sivustolle';
        const linkTextEn = item.link_text_en || 'Visit website';
        const isPinned = item.pinned === true || item.pinned === 'true';
        const width = imgData.width || item.width || '';
        const height = imgData.height || item.height || '';
        const kuva = imgData.kuva || item.kuva;

        const obj = {
          pinPriority, kuva, alt, title, 
          type: isDiptych ? 'diptych' : 'normal',
          index: dIndex, orientation, itemType, linkUrl, linkTextFi, linkTextEn, 
          isPinned, width, height, originalIndex: index
        };

        if (pinPriority !== 999) {
          priorityPinned.push(obj);
        } else if (isPinned) {
          pinned.push(obj);
        } else {
          standard.push(obj);
        }
      };

      if (item.layout === 'diptych' && item.images) {
        item.images.forEach((img, idx) => processItem(img, true, idx + 1));
      } else {
        processItem(item, false, 0);
      }
    });
  });

  priorityPinned.sort((a, b) => a.pinPriority - b.pinPriority);
  
  // Shuffle standard pool
  for (let i = standard.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [standard[i], standard[j]] = [standard[j], standard[i]];
  }

  return [...priorityPinned, ...pinned, ...standard].map(item => {
    const filenameNoExt = item.kuva.split('/').pop().split('.')[0];
    const thumbMobile = `${filenameNoExt}_mobile.webp`;
    const thumbDesktop = `${filenameNoExt}_desktop.webp`;
    const lqipB64 = lqipData[filenameNoExt] || '';
    
    let pThumbMobile, pThumbDesktop, fullImgUrl;
    if (item.kuva.includes('http')) {
      const filenameWithExt = item.kuva.split('/').pop();
      const basePath = item.kuva.replace(filenameWithExt, '');
      pThumbMobile = `${basePath}thumbs/${thumbMobile}`;
      pThumbDesktop = `${basePath}thumbs/${thumbDesktop}`;
      fullImgUrl = item.kuva;
    } else {
      pThumbMobile = `/images/thumbnails/${thumbMobile}`;
      pThumbDesktop = `/images/thumbnails/${thumbDesktop}`;
      fullImgUrl = `/images/${item.kuva}`;
    }
    
    return { ...item, pThumbMobile, pThumbDesktop, fullImgUrl, lqipB64 };
  });
}
