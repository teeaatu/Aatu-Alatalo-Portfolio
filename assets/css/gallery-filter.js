function initGalleryFilter() {
    const filterLinks = document.querySelectorAll(".filter-link");
    const imageSections = document.querySelectorAll(".image-section");
    const subSeriesIntros = document.querySelectorAll(".sub-series-intro");

    if (!filterLinks.length || !imageSections.length) return;
    
    // Estetään tuplalataus
    if (document.body.dataset.filterInit === "true") return;
    document.body.dataset.filterInit = "true";

    filterLinks.forEach(link => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            
            // Päivitetään aktiivinen linkki
            filterLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");

            const filter = link.getAttribute("data-filter");

            // Toggle Sub-series Intros
            subSeriesIntros.forEach(intro => {
                if (intro.getAttribute("data-intro-series") === filter) {
                    intro.classList.remove("hidden");
                } else {
                    intro.classList.add("hidden");
                }
            });

            imageSections.forEach(section => {
                if (filter === "all" || section.getAttribute("data-series") === filter) {
                    section.classList.remove("hidden");
                } else {
                    section.classList.add("hidden");
                }
            });
        });
    });
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initGalleryFilter);
} else {
    initGalleryFilter();
}