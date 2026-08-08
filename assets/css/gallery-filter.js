/**
 * Gallery Filter — Velvet Drop Edition
 *
 * Käyttää CSS View Transitions API:a koreografioimaan
 * kategoriamuutokset. Kursorianimaatio hoidetaan JS:llä,
 * koska kursori ei kuulu View Transitions -snapshottiin.
 *
 * Koreografia:
 *   Exit  ~700ms cubic-bezier(0.76, 0, 0.24, 1): elementit laskeutuvat alas
 *   Enter ~600ms cubic-bezier(0.16, 1, 0.3, 1):  elementit nousevat ylhäältä
 *   Kursori: nousee -12px exitin alussa, palaa 0 enterin alussa
 */

/* ==========================================================================
   KURSORIANIMAATIO — hallitaan JS:llä koska kursori ei ole VT-snapshotissa
   ========================================================================== */

const VT_CURSOR_EASE_UP   = 'cubic-bezier(0.4, 0, 0.2, 1)';
const VT_CURSOR_EASE_DOWN = 'cubic-bezier(0.16, 1, 0.3, 1)';
const VT_ENTER_DELAY_MS   = 200;

/**
 * Animoi kursoria Velvet Drop -koreografian mukaisesti:
 * nousee ylös exitin alkaessa, palaa paikalleen enterin alkaessa.
 */
function animateCursorVelvetDrop() {
  // Haetaan kaikki elementit joihin cursor-style on asetettu
  // (native cursor, ei custom DOM-kursoria — natiivi kursori ei ole animoitavissa JS:llä suoraan)
  // Jos sivustolla on custom cursor -elementti, animoidaan sitä.
  const customCursor = document.querySelector(
    '.custom-cursor, [data-cursor], #custom-cursor, .cursor, .cursor-dot, .cursor-ring'
  );

  if (!customCursor) return; // Natiivi kursori — ohitetaan

  // Exit: kursori nousee ylös 12px
  customCursor.animate(
    [
      { transform: 'translateY(0px)',   offset: 0 },
      { transform: 'translateY(-12px)', offset: 1 },
    ],
    {
      duration: 300,
      easing: VT_CURSOR_EASE_UP,
      fill: 'forwards',
    }
  );

  // Enter: kursori palaa paikalleen viiveellä
  setTimeout(() => {
    customCursor.animate(
      [
        { transform: 'translateY(-12px)', offset: 0 },
        { transform: 'translateY(0px)',   offset: 1 },
      ],
      {
        duration: 500,
        easing: VT_CURSOR_EASE_DOWN,
        fill: 'forwards',
      }
    );
  }, VT_ENTER_DELAY_MS);
}

/* ==========================================================================
   DOM-MUUTOS — filter-logiikka
   ========================================================================== */

/**
 * Päivittää galleriafiltterin DOM-tilan (luokat) ilman animaatiologiikkaa.
 * Tämä funktion kutsu tapahtuu View Transition -callbackin sisällä,
 * joten selain ottaa snapshotteja ennen ja jälkeen muutoksen.
 */
function applyFilter(filterLinks, imageSections, subSeriesIntros, activeLink) {
  const filter = activeLink.getAttribute('data-filter');

  // Päivitä aktiivinen linkki
  filterLinks.forEach(l => l.classList.remove('active'));
  activeLink.classList.add('active');

  // Näytä/piilota sub-series intro -tekstit
  subSeriesIntros.forEach(intro => {
    if (intro.getAttribute('data-intro-series') === filter) {
      intro.classList.remove('hidden');
    } else {
      intro.classList.add('hidden');
    }
  });

  // Näytä/piilota kuvasektiot
  imageSections.forEach(section => {
    if (filter === 'all' || section.getAttribute('data-series') === filter) {
      section.classList.remove('hidden');
    } else {
      section.classList.add('hidden');
    }
  });
}

/* ==========================================================================
   PÄÄFUNKTIO
   ========================================================================== */

function initGalleryFilter() {
  const filterLinks     = document.querySelectorAll('.filter-link');
  const imageSections   = document.querySelectorAll('.image-section');
  const subSeriesIntros = document.querySelectorAll('.sub-series-intro');

  if (!filterLinks.length || !imageSections.length) return;

  // Estetään tuplalataus
  if (document.body.dataset.filterInit === 'true') return;
  document.body.dataset.filterInit = 'true';

  // Tarkistetaan View Transitions -tuki
  const supportsVT = 'startViewTransition' in document;

  filterLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();

      // Ohitetaan klikki jos jo aktiivinen
      if (link.classList.contains('active')) return;

      if (supportsVT) {
        // --- VELVET DROP VIEW TRANSITION ---
        // 1. Aloita kursorianimaatio heti
        animateCursorVelvetDrop();

        // 2. Käynnistä View Transition — selain ottaa snapshot ennen DOM-muutosta
        document.startViewTransition(() => {
          applyFilter(filterLinks, imageSections, subSeriesIntros, link);
        });

      } else {
        // --- FALLBACK: ei View Transitions -tukea ---
        applyFilter(filterLinks, imageSections, subSeriesIntros, link);
      }
    });
  });
}

/* ==========================================================================
   KÄYNNISTYS
   ========================================================================== */

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initGalleryFilter);
} else {
  initGalleryFilter();
}