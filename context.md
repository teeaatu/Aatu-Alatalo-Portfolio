# Project Context

## Project Overview
Jekyll-based portfolio website hosted on GitHub Pages with Cloudflare proxy.

## Current State
The repository is currently clean at a stable commit (`5bfe70a`). Image lazy-loading optimizations were safely reverted, and the Finnish language gallery titles (e.g., "Väri ja muoto") have been fixed to display only Finnish text.

## Core Development Rules
- Always keep FI and EN localization logic strictly separated.
- Always run and verify changes locally via `bundle exec jekyll serve` before any staging.
- Use atomic, small commits for individual working fixes.

## Future Roadmap
Future steps include professional video/media streaming architecture (via Cloudflare R2 object storage) and gallery scalability planning.

## History
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