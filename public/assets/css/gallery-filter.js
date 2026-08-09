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

function initGalleryFilter() {
  const filterLinks     = document.querySelectorAll('.filter-link');
  const imageSections   = document.querySelectorAll('.image-section');
  const subSeriesIntros = document.querySelectorAll('.sub-series-intro');

  if (!filterLinks.length || !imageSections.length) return;

  // Estetään tuplalataus
  if (document.body.dataset.filterInit === 'true') return;
  document.body.dataset.filterInit = 'true';

  filterLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();

      // Ohitetaan klikki jos jo aktiivinen
      if (link.classList.contains('active')) return;
      
      applyFilter(filterLinks, imageSections, subSeriesIntros, link);
    });
  });
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initGalleryFilter);
} else {
  initGalleryFilter();
}
leryFilter);
} else {
  initGalleryFilter();
}