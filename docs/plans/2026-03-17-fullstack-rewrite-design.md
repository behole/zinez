# Punk Zines Full-Stack Rewrite Design

Date: 2026-03-17

## Problem

The current viewer loads a 2.6MB data.js file and renders all 3,484 cards at once. Search filters the entire array on every keystroke. No API exists for programmatic access. The Python scraping tools work but have no pipeline into a proper database. The viewer barely functions on mobile.

## Solution

Full-stack TypeScript app on Cloudflare Workers + D1 with a vanilla TS frontend.

## Data Layer

D1 SQLite database with FTS5 full-text search. Schema:

- `zines` table: id, zine_name, issue_number, year, year_primary (computed int), location, description, tags (JSON text), bands_featured (JSON text), creators, source_type, archive_source, image_url, ia_item_url, ia_download_url, ia_thumb (computed), created_at, updated_at
- FTS5 virtual table indexing: zine_name, description, tags, bands_featured, creators, location

Import script (TypeScript/Bun) reads punk_zines_database.json and bulk-inserts into D1. Python scrapers stay as-is, writing to JSON. Import script syncs JSON to D1.

## API Layer

Hono on Cloudflare Workers. Endpoints:

- `GET /api/zines` — paginated list with search, filters, sorting
  - Params: q, decade, location, source_type, sort (year_asc/desc, name_asc/desc), page, limit (default 50)
  - Returns: { zines, total, page, pages }
- `GET /api/zines/:id` — single zine detail
- `GET /api/stats` — collection stats (total, by decade, by source)
- `GET /api/timeline` — year-count data for timeline chart

No auth for reads. Open CORS.

## Frontend

Vite + vanilla TypeScript. Key improvements:

- Virtual scrolling: render only visible cards (~20-30), not all 3,484
- Paginated API calls: fetch 50 at a time, infinite scroll
- Debounced search: 300ms debounce, API call instead of client-side filtering
- Lazy image loading: IntersectionObserver, IA thumbnails for grid, high-res on lightbox
- Mobile responsive
- Keeps current dark/punk aesthetic (black bg, hot pink accents, monospace touches)
- Adds: source type filter, location filter, sort dropdown
- Keeps: timeline chart, grid/list toggle, lightbox with zoom/pan

No framework. TypeScript modules, CSS custom properties, fetch calls.

## Project Structure

```
src/
  api/
    index.ts              # Worker entry, Hono routes
    routes/zines.ts       # /api/zines endpoints
    routes/stats.ts       # /api/stats
    routes/timeline.ts    # /api/timeline
    db/schema.sql         # D1 table definitions
    db/import.ts          # JSON -> D1 import script
  frontend/
    index.html
    main.ts
    api.ts                # Typed fetch wrapper
    grid.ts               # Virtual scroll grid
    lightbox.ts           # Lightbox with zoom/pan
    timeline.ts           # Canvas timeline
    filters.ts            # Search + filter UI
    style.css
wrangler.toml
package.json
tsconfig.json
vite.config.ts
```

## Deployment

- `wrangler deploy` pushes API worker + static frontend
- `bun run dev` starts Vite dev server + local D1
- `bun run import` syncs JSON to D1

## Data Update Flow

Python scrapers -> update JSON -> `bun run import` -> D1 synced

## Non-Goals

- No auth/write endpoints (future consideration)
- No React/Next.js
- Python scrapers not rewritten (they work fine)
- Existing docs/viewer stays as static fallback
