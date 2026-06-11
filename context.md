# Project Context
# Projektin muutoshistoria - Kesäkuu 2026

## Project Overview
Jekyll-based portfolio website hosted on GitHub Pages with Cloudflare proxy.

## Current State
The repository incorporates a robust Vanilla JS Masonry grid with CSS transitions for a flicker-free layout. Core Web Vitals are optimized, featuring `loading="eager"` on above-the-fold content for instant LCP. External media integration is fully supported via HTTPS URLs natively in YAML. Recent content curation updates are complete, with key works pinned correctly. The site maintains a clean separation of FI and EN localization logic.

## Core Development Rules
- Always keep FI and EN localization logic strictly separated.
- Always run and verify changes locally via `bundle exec jekyll serve` before any staging.
- Use atomic, small commits for individual working fixes.

## Future Roadmap
Future steps include professional video/media streaming architecture (via Cloudflare R2 object storage) and gallery scalability planning.

## History
* **[2026-06-10] Masonry Grid, HTTPS Support, LCP Optimization & Content Curation**
    * **Layout Architecture:** Implemented a robust Vanilla JS Masonry grid (`overview-grid.html` & `default.html`) to dynamically position images without breaking the critical `pin_priority` left-to-right sorting. Added CSS transitions (`transition: left 0.4s, top 0.4s`) for a smooth, flicker-free layout rendering.
    * **Performance (LCP):** Upgraded the image loading logic to force `loading="eager"` on the first 6 items of any gallery grid automatically, ensuring instantaneous rendering of above-the-fold content even on slow connections.
    * **External Media Integration:** Modified Liquid templates across all individual gallery pages (`elaimet.html`, `raw.html`, `luonto-ja-ymparisto.html`, etc.) and the main grid to natively support absolute external HTTPS URLs in the `kuva` YAML field using a `{% if item.kuva contains 'http' %}` check. Created an automated python script for rolling out this support.
    * **Content Curation:** Added new external `webp` assets (e.g., *Hevoset ja ponit pellolla*, *Unto Välikatto*). Updated the `pinned: true` status across multiple datasets (`raw.yml`, `vari-ja-muoto.yml`, `mustavalkoinen-sarja.yml`) to elevate key works like *Mysteeri*, *Leila Palmu*, *Kaksi naista selin*, *Betoni-ihme*, and *Ronja pellolla*.

* **[2026-06-09] Mobile Typography, Portrait Optimization, and Alt-Text Automation**
    * **Typography:** Fixed "MUSTAVALKOINEN" mobile overflow orphans. Implemented language-aware hyphenation (`hyphens: auto`) and word-break controls for long titles ("Kuvaprojekti ajasta", "Kiehtovat rakennukset", "Monochrome") on desktop.
    * **UX/Layout:** Optimized portrait image display with a `85vh` max-height constraint. Refactored `.image-wrapper` to use `width: fit-content`, ensuring project metadata aligns perfectly with image edges across all aspect ratios.
    * **Transitions:** Stabilized gallery filtering (e.g., Utajärvi sub-series) by switching to `display: none !important` for hidden elements, eliminating layout jumps.
    * **Accessibility:** Standardized `alt` text logic across all gallery pages. The system now prioritizes the YAML `alt_text` field and provides an automated fallback that generates readable text from filenames (e.g., `DSC_001.jpg` -> `Dsc 001`).
    * **Cleanup:** Removed redundant image tags in `raw.html` and fixed YAML syntax errors in data files.

* **[2026-06-08] Sub-series Filtering Architecture & Utajärvi Integration**
    * **Architecture:** Implemented a scalable sub-series filtering system within the "Väri ja muoto / Color & Form" gallery. This allows a single gallery page to be divided into granular, thematically-linked projects.
    * **Data Model:** Introduced a `series` key in the YAML data files (e.g., `series: "utajarvi"` in `_data/vari-ja-muoto.yml`) to programmatically associate images with a specific sub-series. Images without this key default to a "general" category. Metadata for titles and locations was updated to a bilingual `EN / FI` format.
    * **UI/UX:** Developed a minimalist, text-based filter navigation bar that is fully bilingual and responsive. The UI uses slashes as separators (`KAIKKI / UTAJÄRVI / YKSITTÄISET TEOKSET`) and an elegant `opacity: 0.5` state for inactive links to provide clear visual focus. A mobile-specific CSS media query was added to prevent awkward text wrapping on smaller screens.
    * **Dynamic Content:** Created dynamic introduction text blocks (`<div class="sub-series-intro">`) that are toggled via JavaScript. These blocks provide narrative context for a sub-series and are only visible when the corresponding filter is active, remaining hidden in the "All" view.
    * **JavaScript & CSS:** Implemented a lightweight, vanilla JavaScript solution (embedded directly in the HTML for robustness) to handle the filtering logic. The script toggles a `.hidden` CSS class (`opacity: 0`, `height: 0`) on image sections and intro blocks, creating a smooth fade-in/out transition.
    * **Bilingual Sync:** The entire feature was deployed symmetrically across both the Finnish (`vari-ja-muoto.html`) and English (`en/color-and-form.html`) pages. The core automation script (`scripts/replace_loops.py`) was also updated to correctly parse the new bilingual `otsikko` and `paikka` fields.

* **[2026-06-07] Core Web Vitals & UX Refactor: Pure CSS Grid, Advanced Pinning, and Splash Screen Removal**
    * **Architecture:** Replaced the JavaScript-driven masonry layout with a pure CSS Grid solution (`display: grid`, `align-items: start`). This completely eliminated Cumulative Layout Shift (CLS=0) by allowing the browser to calculate layout space before images load, while respecting their natural aspect ratios.
    * **Curation:** Implemented an advanced `pin_priority` system in YAML, allowing specific images to be forced to the absolute top of the grid, overriding the standard `pinned: true` logic for ultimate editorial control.
    * **UX/Features:** Developed a flexible external link feature. By adding `link_url` to an item's YAML data, it transforms from a standard gallery image into a clickable link to an external site. This was used for the Hasselblad badge, which now includes a custom hover effect (grayscale + SVG icon) and a configurable text overlay.
    * **Data Isolation:** Created a dedicated `etusivu.yml` data file to house homepage-specific items (like the badge), preventing them from appearing in categorized portfolio galleries.
    * **Performance:** Completely removed the initial splash screen/intro animation. All related HTML, CSS (`@keyframes`), and JavaScript (`sessionStorage` checks, timed sequences) were purged to eliminate render-blocking resources, significantly improving First Contentful Paint (FCP) and Largest Contentful Paint (LCP).

* **[2026-06-07] Homepage Grid Layout & Pinning Refactor**
    * Implemented a `pinned: true` flag in YAML data files to allow manual curation of top portfolio images.
    * Updated `_includes/overview-grid.html` to separate images into a `pinned_images` array (stable order) and a `shuffled_pool` array (randomized at build time).
    * Replaced the CSS `column-count` layout, which caused vertical stacking of pinned items, with a custom JavaScript masonry solution.
    * The new JS logic in `_layouts/default.html` calculates and applies absolute positions, ensuring a natural left-to-right, row-by-row flow for all grid items.
    * The JS solution is responsive (adapting from 3 to 2 columns) and integrated with BFCache `pageshow` events to prevent layout bugs on iOS back-swipe gestures.
    * Removed `column-count` and related properties from `assets/css/style.css` to support the new JS-driven layout.

* **[2026-06-06] Home Page Grid Architecture Refactor**
    * Centralized duplicated homepage grid logic from `index.html` and `en/index.html` into a single reusable `_includes/overview-grid.html` file.
    * The new include aggregates images from all category YAML files, supporting both local assets and absolute external URLs.
    * Improved internationalization by using the `page.lang` variable for robust language-specific `alt` text rendering.
    * Simplified `index.html` and `en/index.html` to a single `{% include %}` tag, significantly improving maintainability and scalability.

* **[2026-06-04] Repository Cleanup & Architecture Optimization**
    * Purged 6,534 untracked macOS metadata ghost files (`._*`) that were causing severe performance degradation across development tools.
    * Updated `.gitignore` to strictly block future system file pollution, specifically targeting `._*` and `.DS_Store` patterns.
    * Cleaned up the root directory by isolating scattered, single use Python automation scripts into a central `scripts/` folder.

* **[2026-06-04] Implemented Session-Gated Cinematic Loader**
    * Integrated a zero-flicker sessionStorage check at the top of document layout to append a .skip-intro state.
    * Reduced subpage and gallery navigation delay to 0 seconds, matching instant-loading static portfolio standards.
    * Preserved the 4.4s typography intro and 2.5s fade sequence exclusively for first-time session arrivals.
    * Cleaned up and extracted all remaining inline styles into centralized CSS classes inside style.css.

* **[2026-06-03] Style Architecture & AI Safeguards**
    * Moved all hardcoded colors, fonts, and style values from the main stylesheet into global CSS variables within the :root block to enable easier future theme management.
    * Created the .cursorrules file in the root directory to enforce strict AI boundaries, banning inline styles (style="...") and mandating the use of centralized CSS variables for all visual adjustments.