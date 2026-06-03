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