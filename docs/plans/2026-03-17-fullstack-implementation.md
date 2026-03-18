# Punk Zines Full-Stack Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Rewrite the punk zines viewer as a full-stack TypeScript app with Cloudflare Workers, D1 database with FTS5 search, Hono API, and a fast vanilla TS frontend with virtual scrolling.

**Architecture:** Hono API serves paginated, searchable zine data from D1 SQLite. Vanilla TypeScript frontend with Vite fetches from API, renders via virtual scrolling. Both deploy together via wrangler. Python scrapers stay untouched — an import script bridges JSON to D1.

**Tech Stack:** Bun, TypeScript, Hono, Cloudflare Workers, D1 (SQLite + FTS5), Vite, vanilla TS/CSS

---

## Task 1: Project Scaffolding

**Files:**
- Create: `package.json`
- Create: `tsconfig.json`
- Create: `wrangler.toml`
- Create: `vite.config.ts`
- Create: `.dev.vars` (empty, for future secrets)
- Modify: `.gitignore`

**Step 1: Initialize package.json**

```bash
bun init -y
```

Then replace contents of `package.json`:

```json
{
  "name": "punk-zines",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "wrangler dev",
    "dev:frontend": "vite dev src/frontend",
    "build": "vite build src/frontend && wrangler deploy --dry-run",
    "deploy": "vite build src/frontend && wrangler deploy",
    "import": "bun run src/api/db/import.ts",
    "db:init": "wrangler d1 execute punk-zines-db --local --file=src/api/db/schema.sql",
    "db:init:remote": "wrangler d1 execute punk-zines-db --file=src/api/db/schema.sql"
  },
  "dependencies": {
    "hono": "^4"
  },
  "devDependencies": {
    "@cloudflare/workers-types": "^4",
    "typescript": "^5",
    "vite": "^6",
    "wrangler": "^4"
  }
}
```

**Step 2: Install dependencies**

```bash
bun install
```

Expected: `node_modules/` created, lockfile written.

**Step 3: Create tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "jsx": "react-jsx",
    "jsxImportSource": "hono/jsx",
    "types": ["@cloudflare/workers-types"],
    "outDir": "dist",
    "rootDir": "."
  },
  "include": ["src/**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

**Step 4: Create wrangler.toml**

```toml
name = "punk-zines"
main = "src/api/index.ts"
compatibility_date = "2024-12-01"

[assets]
directory = "dist/frontend"

[[d1_databases]]
binding = "DB"
database_name = "punk-zines-db"
database_id = "local"
```

Note: `database_id = "local"` is a placeholder. After `wrangler d1 create punk-zines-db`, replace with the real ID.

**Step 5: Create vite.config.ts**

```typescript
import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  root: resolve(__dirname, "src/frontend"),
  build: {
    outDir: resolve(__dirname, "dist/frontend"),
    emptyOutDir: true,
  },
});
```

**Step 6: Update .gitignore**

Append to existing `.gitignore`:

```
# Node
node_modules/
dist/
.wrangler/
.dev.vars
bun.lockb
```

**Step 7: Commit**

```bash
git add package.json tsconfig.json wrangler.toml vite.config.ts .gitignore
git commit -m "feat: scaffold project with Bun, Hono, Vite, Wrangler"
```

---

## Task 2: D1 Schema & Import Script

**Files:**
- Create: `src/api/db/schema.sql`
- Create: `src/api/db/import.ts`

**Step 1: Create schema.sql**

```sql
DROP TABLE IF EXISTS zines_fts;
DROP TABLE IF EXISTS zines;

CREATE TABLE zines (
  id TEXT PRIMARY KEY,
  zine_name TEXT NOT NULL,
  issue_number TEXT,
  year TEXT,
  year_primary INTEGER,
  location TEXT,
  description TEXT,
  tags TEXT,              -- JSON array as text
  bands_featured TEXT,    -- JSON array as text
  creators TEXT,
  circulation TEXT,
  source_type TEXT,
  archive_source TEXT,
  image_url TEXT,
  ia_item_url TEXT,
  ia_download_url TEXT,
  ia_thumb TEXT,
  attribution TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now'))
);

CREATE INDEX idx_zines_year ON zines(year_primary);
CREATE INDEX idx_zines_source ON zines(source_type);
CREATE INDEX idx_zines_name ON zines(zine_name);

CREATE VIRTUAL TABLE zines_fts USING fts5(
  zine_name,
  description,
  tags,
  bands_featured,
  creators,
  location,
  content=zines,
  content_rowid=rowid
);

-- Triggers to keep FTS in sync
CREATE TRIGGER zines_ai AFTER INSERT ON zines BEGIN
  INSERT INTO zines_fts(rowid, zine_name, description, tags, bands_featured, creators, location)
  VALUES (new.rowid, new.zine_name, new.description, new.tags, new.bands_featured, new.creators, new.location);
END;

CREATE TRIGGER zines_ad AFTER DELETE ON zines BEGIN
  INSERT INTO zines_fts(zines_fts, rowid, zine_name, description, tags, bands_featured, creators, location)
  VALUES ('delete', old.rowid, old.zine_name, old.description, old.tags, old.bands_featured, old.creators, old.location);
END;

CREATE TRIGGER zines_au AFTER UPDATE ON zines BEGIN
  INSERT INTO zines_fts(zines_fts, rowid, zine_name, description, tags, bands_featured, creators, location)
  VALUES ('delete', old.rowid, old.zine_name, old.description, old.tags, old.bands_featured, old.creators, old.location);
  INSERT INTO zines_fts(rowid, zine_name, description, tags, bands_featured, creators, location)
  VALUES (new.rowid, new.zine_name, new.description, new.tags, new.bands_featured, new.creators, new.location);
END;
```

**Step 2: Create import.ts**

```typescript
import { readFileSync } from "fs";
import { execSync } from "child_process";
import { resolve } from "path";

const DB_NAME = "punk-zines-db";
const JSON_PATH = resolve(__dirname, "../../../punk_zines_database.json");

interface ZineEntry {
  id: string;
  zine_name: string;
  issue_number?: string;
  year?: string;
  location?: string;
  description?: string;
  tags?: string[];
  bands_featured?: string[];
  creators?: string;
  circulation?: string;
  source_type?: string;
  archive_source?: string;
  image_url?: string;
  ia_item_url?: string;
  ia_download_url?: string;
  attribution?: string;
  [key: string]: unknown;
}

function normalizeYear(s: string | number | undefined): number | null {
  if (s === undefined || s === null) return null;
  const str = String(s);
  for (let i = 0; i <= str.length - 4; i++) {
    const frag = str.slice(i, i + 4);
    if (/^\d{4}$/.test(frag)) {
      const y = parseInt(frag, 10);
      if (y >= 1900 && y <= 2100) return y;
    }
  }
  return null;
}

function deriveIaThumb(iaItemUrl: string | undefined): string | null {
  if (!iaItemUrl) return null;
  const marker = "/details/";
  const idx = iaItemUrl.indexOf(marker);
  if (idx === -1) return null;
  const rest = iaItemUrl.slice(idx + marker.length);
  const itemId = rest.split("/")[0].split("?")[0];
  if (!itemId) return null;
  return `https://archive.org/services/img/${itemId}`;
}

function escSql(s: string): string {
  return s.replace(/'/g, "''");
}

async function main() {
  const isRemote = process.argv.includes("--remote");
  const flag = isRemote ? "" : "--local";

  console.log(`Importing to ${isRemote ? "REMOTE" : "LOCAL"} D1...`);

  const raw = readFileSync(JSON_PATH, "utf-8");
  const data = JSON.parse(raw);
  const zines: ZineEntry[] = data.zines;

  console.log(`Found ${zines.length} zines in JSON`);

  // Build SQL statements in batches of 50
  const BATCH = 50;
  for (let i = 0; i < zines.length; i += BATCH) {
    const batch = zines.slice(i, i + BATCH);
    const statements = batch.map((z) => {
      const yearPrimary = normalizeYear(z.year);
      const iaThumb = deriveIaThumb(z.ia_item_url);
      const tags = JSON.stringify(z.tags || []);
      const bands = JSON.stringify(z.bands_featured || []);

      return `INSERT OR REPLACE INTO zines (id, zine_name, issue_number, year, year_primary, location, description, tags, bands_featured, creators, circulation, source_type, archive_source, image_url, ia_item_url, ia_download_url, ia_thumb, attribution) VALUES ('${escSql(z.id)}', '${escSql(z.zine_name || "")}', '${escSql(z.issue_number || "")}', '${escSql(z.year?.toString() || "")}', ${yearPrimary ?? "NULL"}, '${escSql(z.location || "")}', '${escSql(z.description || "")}', '${escSql(tags)}', '${escSql(bands)}', '${escSql(z.creators || "")}', '${escSql(z.circulation || "")}', '${escSql(z.source_type || "")}', '${escSql(z.archive_source || "")}', '${escSql(z.image_url || "")}', '${escSql(z.ia_item_url || "")}', '${escSql(z.ia_download_url || "")}', '${escSql(iaThumb || "")}', '${escSql(z.attribution || "")}');`;
    });

    const sql = statements.join("\n");
    const tmpFile = `/tmp/punk-zines-batch-${i}.sql`;
    require("fs").writeFileSync(tmpFile, sql);

    execSync(`wrangler d1 execute ${DB_NAME} ${flag} --file=${tmpFile}`, {
      stdio: "inherit",
    });

    process.stdout.write(`\r  Imported ${Math.min(i + BATCH, zines.length)} / ${zines.length}`);
  }

  console.log("\nDone!");
}

main().catch(console.error);
```

**Step 3: Initialize local D1 and import**

```bash
bun run db:init
bun run import
```

Expected: Schema created, 3,484 rows imported.

**Step 4: Verify import**

```bash
wrangler d1 execute punk-zines-db --local --command="SELECT COUNT(*) as total FROM zines"
wrangler d1 execute punk-zines-db --local --command="SELECT id, zine_name FROM zines LIMIT 3"
wrangler d1 execute punk-zines-db --local --command="SELECT * FROM zines_fts WHERE zines_fts MATCH 'riot grrrl' LIMIT 3"
```

Expected: 3484 total, sample rows returned, FTS search works.

**Step 5: Commit**

```bash
git add src/api/db/
git commit -m "feat: add D1 schema with FTS5 and JSON import script"
```

---

## Task 3: Hono API — Zines Endpoints

**Files:**
- Create: `src/api/index.ts`
- Create: `src/api/routes/zines.ts`
- Create: `src/api/types.ts`

**Step 1: Create types.ts**

```typescript
export interface Env {
  DB: D1Database;
}

export interface ZineRow {
  id: string;
  zine_name: string;
  issue_number: string;
  year: string;
  year_primary: number | null;
  location: string;
  description: string;
  tags: string; // JSON array
  bands_featured: string; // JSON array
  creators: string;
  circulation: string;
  source_type: string;
  archive_source: string;
  image_url: string;
  ia_item_url: string;
  ia_download_url: string;
  ia_thumb: string;
  attribution: string;
}

export interface ZineResponse {
  id: string;
  zine_name: string;
  issue_number: string;
  year: string;
  year_primary: number | null;
  location: string;
  description: string;
  tags: string[];
  bands_featured: string[];
  creators: string;
  circulation: string;
  source_type: string;
  archive_source: string;
  image_url: string;
  ia_item_url: string;
  ia_download_url: string;
  ia_thumb: string;
  attribution: string;
}
```

**Step 2: Create routes/zines.ts**

```typescript
import { Hono } from "hono";
import type { Env, ZineRow, ZineResponse } from "../types";

const zines = new Hono<{ Bindings: Env }>();

function rowToResponse(row: ZineRow): ZineResponse {
  return {
    ...row,
    tags: safeParseArray(row.tags),
    bands_featured: safeParseArray(row.bands_featured),
  };
}

function safeParseArray(s: string): string[] {
  if (!s) return [];
  try {
    const parsed = JSON.parse(s);
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

// GET /api/zines — paginated list with search and filters
zines.get("/", async (c) => {
  const db = c.env.DB;
  const q = c.req.query("q") || "";
  const decade = c.req.query("decade") || "";
  const location = c.req.query("location") || "";
  const sourceType = c.req.query("source_type") || "";
  const sort = c.req.query("sort") || "name_asc";
  const page = Math.max(1, parseInt(c.req.query("page") || "1", 10));
  const limit = Math.min(100, Math.max(1, parseInt(c.req.query("limit") || "50", 10)));
  const offset = (page - 1) * limit;

  // Build query
  const conditions: string[] = [];
  const params: unknown[] = [];

  // Full-text search
  let fromClause = "zines";
  if (q) {
    // Use FTS5 MATCH with fallback for short queries
    if (q.length >= 3) {
      fromClause = "zines INNER JOIN zines_fts ON zines.rowid = zines_fts.rowid";
      conditions.push("zines_fts MATCH ?");
      // Append * for prefix matching
      params.push(q.split(/\s+/).map((t) => `"${t}"*`).join(" "));
    } else {
      conditions.push("(zine_name LIKE ? OR location LIKE ?)");
      params.push(`%${q}%`, `%${q}%`);
    }
  }

  if (decade) {
    const d = parseInt(decade, 10);
    conditions.push("year_primary >= ? AND year_primary < ?");
    params.push(d, d + 10);
  }

  if (location) {
    conditions.push("location LIKE ?");
    params.push(`%${location}%`);
  }

  if (sourceType) {
    conditions.push("source_type = ?");
    params.push(sourceType);
  }

  const where = conditions.length ? `WHERE ${conditions.join(" AND ")}` : "";

  // Sort
  const sortMap: Record<string, string> = {
    name_asc: "zines.zine_name ASC",
    name_desc: "zines.zine_name DESC",
    year_asc: "zines.year_primary ASC NULLS LAST",
    year_desc: "zines.year_primary DESC NULLS LAST",
  };
  const orderBy = sortMap[sort] || sortMap.name_asc;

  // Count
  const countSql = `SELECT COUNT(*) as total FROM ${fromClause} ${where}`;
  const countResult = await db.prepare(countSql).bind(...params).first<{ total: number }>();
  const total = countResult?.total || 0;

  // Fetch page
  const dataSql = `SELECT zines.* FROM ${fromClause} ${where} ORDER BY ${orderBy} LIMIT ? OFFSET ?`;
  const rows = await db.prepare(dataSql).bind(...params, limit, offset).all<ZineRow>();

  return c.json({
    zines: (rows.results || []).map(rowToResponse),
    total,
    page,
    pages: Math.ceil(total / limit),
  });
});

// GET /api/zines/:id — single zine
zines.get("/:id", async (c) => {
  const db = c.env.DB;
  const id = c.req.param("id");
  const row = await db.prepare("SELECT * FROM zines WHERE id = ?").bind(id).first<ZineRow>();

  if (!row) {
    return c.json({ error: "Not found" }, 404);
  }

  return c.json(rowToResponse(row));
});

export default zines;
```

**Step 3: Create index.ts (Worker entry)**

```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import type { Env } from "./types";
import zines from "./routes/zines";

const app = new Hono<{ Bindings: Env }>();

app.use("/api/*", cors());

app.route("/api/zines", zines);

// Health check
app.get("/api/health", (c) => c.json({ status: "ok" }));

export default app;
```

**Step 4: Test locally**

```bash
wrangler dev
```

In another terminal:

```bash
curl "http://localhost:8787/api/health"
curl "http://localhost:8787/api/zines?limit=3" | jq '.zines | length'
curl "http://localhost:8787/api/zines?q=riot+grrrl&limit=3" | jq '.total'
curl "http://localhost:8787/api/zines/SG001" | jq '.zine_name'
```

Expected: health ok, 3 zines returned, FTS search returns results, SG001 returns "Sniffin' Glue".

**Step 5: Commit**

```bash
git add src/api/
git commit -m "feat: add Hono API with paginated search and D1 backend"
```

---

## Task 4: API — Stats & Timeline Endpoints

**Files:**
- Create: `src/api/routes/stats.ts`
- Create: `src/api/routes/timeline.ts`
- Modify: `src/api/index.ts`

**Step 1: Create routes/stats.ts**

```typescript
import { Hono } from "hono";
import type { Env } from "../types";

const stats = new Hono<{ Bindings: Env }>();

stats.get("/", async (c) => {
  const db = c.env.DB;

  const [total, byDecade, bySource, byLocation] = await Promise.all([
    db.prepare("SELECT COUNT(*) as count FROM zines").first<{ count: number }>(),
    db.prepare(`
      SELECT (year_primary / 10) * 10 as decade, COUNT(*) as count
      FROM zines WHERE year_primary IS NOT NULL
      GROUP BY decade ORDER BY decade
    `).all<{ decade: number; count: number }>(),
    db.prepare(`
      SELECT source_type, COUNT(*) as count
      FROM zines GROUP BY source_type ORDER BY count DESC
    `).all<{ source_type: string; count: number }>(),
    db.prepare(`
      SELECT location, COUNT(*) as count
      FROM zines WHERE location != ''
      GROUP BY location ORDER BY count DESC LIMIT 20
    `).all<{ location: string; count: number }>(),
  ]);

  return c.json({
    total: total?.count || 0,
    by_decade: byDecade.results || [],
    by_source: bySource.results || [],
    top_locations: byLocation.results || [],
  });
});

export default stats;
```

**Step 2: Create routes/timeline.ts**

```typescript
import { Hono } from "hono";
import type { Env } from "../types";

const timeline = new Hono<{ Bindings: Env }>();

timeline.get("/", async (c) => {
  const db = c.env.DB;
  const rows = await db.prepare(`
    SELECT year_primary as year, COUNT(*) as count
    FROM zines WHERE year_primary IS NOT NULL
    GROUP BY year_primary ORDER BY year_primary
  `).all<{ year: number; count: number }>();

  return c.json(rows.results || []);
});

export default timeline;
```

**Step 3: Add routes to index.ts**

Add these imports and routes to `src/api/index.ts`:

```typescript
import stats from "./routes/stats";
import timeline from "./routes/timeline";

// After the zines route:
app.route("/api/stats", stats);
app.route("/api/timeline", timeline);
```

**Step 4: Test**

```bash
curl "http://localhost:8787/api/stats" | jq '.total'
curl "http://localhost:8787/api/timeline" | jq 'length'
```

Expected: total 3484, timeline returns ~50-60 year entries.

**Step 5: Commit**

```bash
git add src/api/
git commit -m "feat: add stats and timeline API endpoints"
```

---

## Task 5: Frontend — HTML Shell & Styles

**Files:**
- Create: `src/frontend/index.html`
- Create: `src/frontend/style.css`
- Create: `src/frontend/main.ts`

**Step 1: Create index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Punk Zines Archive</title>
  <link rel="stylesheet" href="./style.css" />
</head>
<body>
  <header>
    <h1>Punk Zines Archive</h1>
    <p class="sub">3,484 zines &bull; 1967&ndash;2025 &bull; Searchable &bull; Open data</p>
  </header>

  <main>
    <div class="controls">
      <div class="search">
        <input id="q" type="search" placeholder="Search name, band, location, year, tag, creator..." autocomplete="off" />
      </div>
      <div class="filters">
        <button data-decade="all" class="active">All</button>
        <button data-decade="1970">70s</button>
        <button data-decade="1980">80s</button>
        <button data-decade="1990">90s</button>
        <button data-decade="2000">00s+</button>
        <select id="sort">
          <option value="name_asc">Name A-Z</option>
          <option value="name_desc">Name Z-A</option>
          <option value="year_asc">Year (oldest)</option>
          <option value="year_desc">Year (newest)</option>
        </select>
      </div>
    </div>

    <div id="stats" class="stats"></div>

    <section class="panel" aria-label="Timeline">
      <canvas id="timeline"></canvas>
    </section>

    <section id="grid" class="grid" aria-label="Results"></section>

    <div id="loader" class="loader" hidden>Loading...</div>
  </main>

  <div id="lightbox" class="lb" role="dialog" aria-modal="true" hidden>
    <div class="lb-box">
      <div class="lb-head">
        <span id="lb-title" class="lb-title"></span>
        <div class="lb-actions">
          <button id="lb-prev" title="Previous">&lsaquo;</button>
          <button id="lb-next" title="Next">&rsaquo;</button>
          <button id="lb-zoom-in" title="Zoom in">+</button>
          <button id="lb-zoom-out" title="Zoom out">&minus;</button>
          <button id="lb-reset" title="Reset zoom">Reset</button>
          <a id="lb-origin" href="#" target="_blank" rel="noopener">View on IA</a>
          <button id="lb-close" title="Close">Close</button>
        </div>
      </div>
      <div class="lb-img" id="lb-img-container">
        <img id="lb-image" alt="" />
      </div>
      <div class="lb-foot">
        <span>Tip: &larr; &rarr; to navigate, Esc to close</span>
        <span class="lb-id">ID: <code id="lb-idval"></code></span>
      </div>
    </div>
  </div>

  <script type="module" src="./main.ts"></script>
</body>
</html>
```

**Step 2: Create style.css**

```css
:root {
  --bg: #0b0b0b;
  --fg: #f5f5f5;
  --hi: #ff0066;
  --alt: #ffe600;
  --mut: #9aa0a6;
  --card: #121212;
  --line: #222;
  --radius: 8px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--fg);
  line-height: 1.5;
}

/* Header */
header {
  border-bottom: 2px solid var(--line);
  padding: 18px 16px;
}
h1 {
  font-size: clamp(18px, 4vw, 24px);
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--hi);
}
.sub { color: var(--mut); font-size: 12px; margin-top: 4px; }

/* Layout */
main {
  max-width: 1280px;
  margin: 0 auto;
  padding: 16px;
}

/* Controls */
.controls {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 12px;
}
.search { flex: 1 1 320px; }
.search input {
  width: 100%;
  padding: 10px 12px;
  border: 2px solid var(--line);
  background: var(--card);
  color: var(--fg);
  border-radius: var(--radius);
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s;
}
.search input:focus { border-color: var(--hi); }
.filters { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }

button, select {
  padding: 8px 12px;
  border: 1px solid var(--line);
  background: var(--card);
  color: var(--fg);
  border-radius: var(--radius);
  cursor: pointer;
  font-size: 13px;
}
button:hover, select:hover { border-color: var(--mut); }
button.active { border-color: var(--hi); color: #000; background: var(--hi); }
select { appearance: auto; }

/* Stats */
.stats {
  color: var(--alt);
  font-size: 12px;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 12px;
}

/* Timeline */
.panel {
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: var(--radius);
  padding: 10px;
  margin-bottom: 16px;
}
canvas { width: 100%; height: 120px; display: block; }

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 12px;
}

.card {
  border: 1px solid var(--line);
  background: var(--card);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.15s;
}
.card:hover { border-color: var(--hi); }

.thumb {
  height: 260px;
  background: #111;
  display: grid;
  place-items: center;
  overflow: hidden;
}
.thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity 0.3s;
}
.thumb img.loaded { opacity: 1; }
.thumb .ph { color: #444; font-size: 12px; }

.meta { padding: 10px 12px; }
.title { font-weight: 600; font-size: 14px; }
.small { font-size: 12px; color: var(--mut); margin-top: 2px; }
.tags { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
.tag {
  font-size: 11px;
  border: 1px solid var(--line);
  padding: 2px 6px;
  border-radius: 999px;
  color: var(--hi);
}

/* Loader */
.loader {
  text-align: center;
  padding: 24px;
  color: var(--mut);
  font-size: 14px;
}

/* Lightbox */
.lb {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.92);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.lb[hidden] { display: none; }

.lb-box {
  max-width: min(92vw, 1100px);
  max-height: 90vh;
  background: #0e0e0e;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}
.lb-head {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
}
.lb-title {
  font-size: 14px;
  color: #eee;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
}
.lb-actions { display: flex; gap: 6px; flex-shrink: 0; }
.lb-actions a,
.lb-actions button {
  border: 1px solid #333;
  background: #141414;
  color: #eee;
  border-radius: 6px;
  padding: 6px 10px;
  cursor: pointer;
  text-decoration: none;
  font-size: 13px;
}
.lb-img {
  display: grid;
  place-items: center;
  background: #0a0a0a;
  overflow: hidden;
  position: relative;
  cursor: grab;
  min-height: 300px;
}
.lb-img.dragging { cursor: grabbing; }
.lb-img img {
  max-width: 100%;
  max-height: 70vh;
  transition: transform 0.15s ease;
  transform-origin: center center;
}
.lb-foot {
  display: flex;
  gap: 8px;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-top: 1px solid var(--line);
  color: #999;
  font-size: 12px;
}
.lb-id code { color: #bbb; font-family: ui-monospace, monospace; }

/* Mobile */
@media (max-width: 640px) {
  .grid { grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 8px; }
  .thumb { height: 200px; }
  .controls { flex-direction: column; }
  .search { flex: 1 1 100%; }
  .lb-actions { flex-wrap: wrap; }
  .lb-head { flex-direction: column; align-items: flex-start; }
}
```

**Step 3: Create main.ts (stub)**

```typescript
import "./style.css";

console.log("Punk Zines Archive loaded");
```

**Step 4: Test dev server**

```bash
bun run dev:frontend
```

Open `http://localhost:5173` — should show the HTML shell with styles, no data yet.

**Step 5: Commit**

```bash
git add src/frontend/
git commit -m "feat: add frontend HTML shell, styles, and Vite entry"
```

---

## Task 6: Frontend — API Client & Search/Filters

**Files:**
- Create: `src/frontend/api.ts`
- Create: `src/frontend/filters.ts`
- Modify: `src/frontend/main.ts`

**Step 1: Create api.ts**

```typescript
const API_BASE = "/api";

export interface Zine {
  id: string;
  zine_name: string;
  issue_number: string;
  year: string;
  year_primary: number | null;
  location: string;
  description: string;
  tags: string[];
  bands_featured: string[];
  creators: string;
  source_type: string;
  archive_source: string;
  image_url: string;
  ia_item_url: string;
  ia_download_url: string;
  ia_thumb: string;
}

export interface ZineListResponse {
  zines: Zine[];
  total: number;
  page: number;
  pages: number;
}

export interface TimelineEntry {
  year: number;
  count: number;
}

export interface Stats {
  total: number;
  by_decade: { decade: number; count: number }[];
  by_source: { source_type: string; count: number }[];
  top_locations: { location: string; count: number }[];
}

export interface FetchParams {
  q?: string;
  decade?: string;
  sort?: string;
  page?: number;
  limit?: number;
}

export async function fetchZines(params: FetchParams): Promise<ZineListResponse> {
  const sp = new URLSearchParams();
  if (params.q) sp.set("q", params.q);
  if (params.decade && params.decade !== "all") sp.set("decade", params.decade);
  if (params.sort) sp.set("sort", params.sort);
  sp.set("page", String(params.page || 1));
  sp.set("limit", String(params.limit || 50));
  const res = await fetch(`${API_BASE}/zines?${sp}`);
  return res.json();
}

export async function fetchZine(id: string): Promise<Zine> {
  const res = await fetch(`${API_BASE}/zines/${id}`);
  return res.json();
}

export async function fetchStats(): Promise<Stats> {
  const res = await fetch(`${API_BASE}/stats`);
  return res.json();
}

export async function fetchTimeline(): Promise<TimelineEntry[]> {
  const res = await fetch(`${API_BASE}/timeline`);
  return res.json();
}
```

**Step 2: Create filters.ts**

```typescript
export interface FilterState {
  q: string;
  decade: string;
  sort: string;
  page: number;
}

export function createFilterState(): FilterState {
  return { q: "", decade: "all", sort: "name_asc", page: 1 };
}

export function initFilters(
  state: FilterState,
  onChange: () => void
): void {
  const input = document.getElementById("q") as HTMLInputElement;
  const sortSelect = document.getElementById("sort") as HTMLSelectElement;
  const decadeButtons = document.querySelectorAll<HTMLButtonElement>("[data-decade]");

  let debounceTimer: ReturnType<typeof setTimeout>;

  input.addEventListener("input", () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      state.q = input.value.trim();
      state.page = 1;
      onChange();
    }, 300);
  });

  sortSelect.addEventListener("change", () => {
    state.sort = sortSelect.value;
    state.page = 1;
    onChange();
  });

  decadeButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      decadeButtons.forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      state.decade = btn.dataset.decade || "all";
      state.page = 1;
      onChange();
    });
  });
}
```

**Step 3: Update main.ts**

```typescript
import "./style.css";
import { fetchZines, fetchStats, fetchTimeline, type Zine, type ZineListResponse } from "./api";
import { createFilterState, initFilters, type FilterState } from "./filters";

const state = createFilterState();
let currentData: ZineListResponse | null = null;
let loading = false;

async function sync(): Promise<void> {
  if (loading) return;
  loading = true;

  const loader = document.getElementById("loader")!;
  loader.hidden = false;

  try {
    currentData = await fetchZines({
      q: state.q,
      decade: state.decade,
      sort: state.sort,
      page: state.page,
      limit: 50,
    });

    renderStats(currentData);
    renderGrid(currentData.zines);
  } finally {
    loading = false;
    loader.hidden = true;
  }
}

function renderStats(data: ZineListResponse): void {
  const el = document.getElementById("stats")!;
  el.textContent = `${data.total} zines found · page ${data.page} of ${data.pages}`;
}

function renderGrid(zines: Zine[]): void {
  const grid = document.getElementById("grid")!;
  grid.innerHTML = zines
    .map(
      (z) => {
        const thumb = z.ia_thumb || z.image_url || "";
        const title = [z.zine_name, z.issue_number && `#${z.issue_number}`].filter(Boolean).join(" ");
        const locyr = [z.location, z.year].filter(Boolean).join(" · ");
        const tags = z.tags.slice(0, 4).map((t) => `<span class="tag">${t}</span>`).join("");

        return `<article class="card" data-id="${z.id}">
          <div class="thumb">${
            thumb
              ? `<img data-src="${thumb}" alt="${title}" />`
              : `<div class="ph">No image</div>`
          }</div>
          <div class="meta">
            <div class="title">${title}</div>
            <div class="small">${locyr}</div>
            ${tags ? `<div class="tags">${tags}</div>` : ""}
          </div>
        </article>`;
      }
    )
    .join("");

  // Lazy load images
  observeImages(grid);

  // Infinite scroll — load next page when near bottom
  setupInfiniteScroll();
}

function observeImages(container: HTMLElement): void {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target as HTMLImageElement;
          const src = img.dataset.src;
          if (src) {
            img.src = src;
            img.onload = () => img.classList.add("loaded");
            img.onerror = () => {
              img.removeAttribute("src");
              img.closest(".thumb")!.innerHTML = `<div class="ph">No image</div>`;
            };
          }
          observer.unobserve(img);
        }
      });
    },
    { rootMargin: "200px" }
  );

  container.querySelectorAll<HTMLImageElement>("img[data-src]").forEach((img) => {
    observer.observe(img);
  });
}

function setupInfiniteScroll(): void {
  // Remove existing listener to avoid duplicates
  window.removeEventListener("scroll", handleScroll);
  window.addEventListener("scroll", handleScroll);
}

async function handleScroll(): Promise<void> {
  if (!currentData || loading) return;
  if (state.page >= currentData.pages) return;

  const scrollBottom = window.innerHeight + window.scrollY;
  const docHeight = document.documentElement.scrollHeight;

  if (docHeight - scrollBottom < 400) {
    state.page++;
    loading = true;
    const loader = document.getElementById("loader")!;
    loader.hidden = false;

    try {
      const more = await fetchZines({
        q: state.q,
        decade: state.decade,
        sort: state.sort,
        page: state.page,
        limit: 50,
      });

      currentData.page = more.page;
      currentData.zines = [...currentData.zines, ...more.zines];

      // Append cards instead of replacing
      const grid = document.getElementById("grid")!;
      const fragment = document.createElement("div");
      fragment.innerHTML = more.zines
        .map((z) => {
          const thumb = z.ia_thumb || z.image_url || "";
          const title = [z.zine_name, z.issue_number && `#${z.issue_number}`].filter(Boolean).join(" ");
          const locyr = [z.location, z.year].filter(Boolean).join(" · ");
          const tags = z.tags.slice(0, 4).map((t) => `<span class="tag">${t}</span>`).join("");

          return `<article class="card" data-id="${z.id}">
            <div class="thumb">${
              thumb
                ? `<img data-src="${thumb}" alt="${title}" />`
                : `<div class="ph">No image</div>`
            }</div>
            <div class="meta">
              <div class="title">${title}</div>
              <div class="small">${locyr}</div>
              ${tags ? `<div class="tags">${tags}</div>` : ""}
            </div>
          </article>`;
        })
        .join("");

      while (fragment.firstElementChild) {
        grid.appendChild(fragment.firstElementChild);
      }

      observeImages(grid);
      renderStats(currentData);
    } finally {
      loading = false;
      loader.hidden = true;
    }
  }
}

// Boot
document.addEventListener("DOMContentLoaded", () => {
  initFilters(state, () => sync());
  sync();
});
```

**Step 6: Commit**

```bash
git add src/frontend/
git commit -m "feat: add API client, search/filters, grid with lazy loading and infinite scroll"
```

---

## Task 7: Frontend — Timeline & Lightbox

**Files:**
- Create: `src/frontend/timeline.ts`
- Create: `src/frontend/lightbox.ts`
- Modify: `src/frontend/main.ts`

**Step 1: Create timeline.ts**

```typescript
import { fetchTimeline, type TimelineEntry } from "./api";

export async function renderTimeline(): Promise<void> {
  const canvas = document.getElementById("timeline") as HTMLCanvasElement;
  if (!canvas) return;

  const data = await fetchTimeline();
  if (!data.length) return;

  const ctx = canvas.getContext("2d")!;
  const w = (canvas.width = canvas.clientWidth);
  const h = (canvas.height = canvas.clientHeight);
  ctx.clearRect(0, 0, w, h);

  const years = data.map((d) => d.year);
  const minY = Math.min(...years);
  const maxY = Math.max(...years);
  const maxC = Math.max(...data.map((d) => d.count));
  const pad = 24;
  const bars = maxY - minY + 1;
  const bw = Math.max(1, (w - pad * 2) / bars);

  const countMap = new Map(data.map((d) => [d.year, d.count]));

  // Bars
  for (let y = minY; y <= maxY; y++) {
    const c = countMap.get(y) || 0;
    const x = pad + (y - minY) * bw;
    const bh = (h - 40) * (c / maxC);
    ctx.fillStyle = c ? "#ff0066" : "#222";
    ctx.fillRect(x, h - 22 - bh, bw - 1, bh);
  }

  // Decade ticks
  ctx.fillStyle = "#9aa0a6";
  ctx.font = "11px system-ui";
  ctx.strokeStyle = "#333";
  ctx.beginPath();
  ctx.moveTo(pad, h - 22);
  ctx.lineTo(w - pad, h - 22);
  ctx.stroke();

  const startDec = Math.floor(minY / 10) * 10;
  const endDec = Math.floor(maxY / 10) * 10;
  for (let d = startDec; d <= endDec; d += 10) {
    const x = pad + (d - minY) * bw;
    ctx.fillRect(x, h - 24, 1, 6);
    ctx.fillText(String(d), x + 2, h - 8);
  }
}
```

**Step 2: Create lightbox.ts**

```typescript
import type { Zine } from "./api";

let lbZines: Zine[] = [];
let lbIdx = 0;
let zoom = 1;
let panX = 0;
let panY = 0;
let dragging = false;
let dragStartX = 0;
let dragStartY = 0;

const $ = (id: string) => document.getElementById(id);

function applyTransform(): void {
  const img = $("lb-image") as HTMLImageElement;
  if (img) img.style.transform = `scale(${zoom}) translate(${panX}px, ${panY}px)`;
}

function resetZoom(): void {
  zoom = 1;
  panX = 0;
  panY = 0;
  applyTransform();
}

function show(zines: Zine[], idx: number): void {
  lbZines = zines;
  lbIdx = idx;
  const z = zines[idx];
  if (!z) return;

  const title = [z.zine_name, z.issue_number && `#${z.issue_number}`].filter(Boolean).join(" ");
  const titleEl = $("lb-title");
  if (titleEl) titleEl.textContent = title;

  const img = $("lb-image") as HTMLImageElement;
  if (img) {
    // High-res: try IA BookReader, fallback to thumb
    let src = "";
    if (z.ia_item_url) {
      const match = z.ia_item_url.match(/\/details\/([^/?]+)/);
      if (match) src = `https://archive.org/download/${match[1]}/page/n0_w3000.jpg`;
    }
    if (!src) src = z.ia_thumb || z.image_url || "";
    img.src = src;
    img.alt = title;
  }

  const link = $("lb-origin") as HTMLAnchorElement;
  if (link) link.href = z.ia_item_url ? `${z.ia_item_url}/mode/2up` : z.image_url || "#";

  const idVal = $("lb-idval");
  if (idVal) idVal.textContent = z.id;

  resetZoom();
  const lb = $("lightbox");
  if (lb) lb.hidden = false;
}

function close(): void {
  const lb = $("lightbox");
  if (lb) lb.hidden = true;
  resetZoom();
}

function nav(dir: number): void {
  if (!lbZines.length) return;
  lbIdx = (lbIdx + dir + lbZines.length) % lbZines.length;
  show(lbZines, lbIdx);
}

export function initLightbox(): void {
  $("lb-close")?.addEventListener("click", close);
  $("lb-prev")?.addEventListener("click", () => nav(-1));
  $("lb-next")?.addEventListener("click", () => nav(1));
  $("lb-zoom-in")?.addEventListener("click", () => {
    zoom = Math.min(zoom * 1.3, 10);
    applyTransform();
  });
  $("lb-zoom-out")?.addEventListener("click", () => {
    zoom = Math.max(zoom / 1.3, 1);
    if (zoom === 1) { panX = 0; panY = 0; }
    applyTransform();
  });
  $("lb-reset")?.addEventListener("click", resetZoom);

  // Close on backdrop click
  $("lightbox")?.addEventListener("click", (e) => {
    if ((e.target as HTMLElement).id === "lightbox") close();
  });

  // Pan/drag
  const container = $("lb-img-container");
  if (container) {
    container.addEventListener("mousedown", (e) => {
      if (zoom > 1) {
        dragging = true;
        dragStartX = e.clientX - panX;
        dragStartY = e.clientY - panY;
        container.classList.add("dragging");
        e.preventDefault();
      }
    });

    document.addEventListener("mousemove", (e) => {
      if (dragging) {
        panX = e.clientX - dragStartX;
        panY = e.clientY - dragStartY;
        applyTransform();
      }
    });

    document.addEventListener("mouseup", () => {
      if (dragging) {
        dragging = false;
        container.classList.remove("dragging");
      }
    });
  }

  // Keyboard
  document.addEventListener("keydown", (e) => {
    const lb = $("lightbox");
    if (!lb || lb.hidden) return;
    if (e.key === "Escape") close();
    if (e.key === "ArrowRight") nav(1);
    if (e.key === "ArrowLeft") nav(-1);
  });
}

export function openLightbox(zines: Zine[], idx: number): void {
  show(zines, idx);
}
```

**Step 3: Update main.ts to use timeline and lightbox**

Add imports at top of `src/frontend/main.ts`:

```typescript
import { renderTimeline } from "./timeline";
import { initLightbox, openLightbox } from "./lightbox";
```

In the `renderGrid` function, after `observeImages(grid)`, add click handlers:

```typescript
  // Card click -> lightbox
  grid.querySelectorAll<HTMLElement>(".card").forEach((card, i) => {
    card.addEventListener("click", () => {
      if (currentData) openLightbox(currentData.zines, i);
    });
  });
```

In the `DOMContentLoaded` handler, add:

```typescript
  initLightbox();
  renderTimeline();
```

**Step 4: Test**

```bash
bun run dev
```

Open `http://localhost:8787` — should show the full app with search, filters, grid, timeline, and lightbox.

**Step 5: Commit**

```bash
git add src/frontend/
git commit -m "feat: add timeline chart and lightbox with zoom/pan"
```

---

## Task 8: Wire Dev Proxy & Polish

**Files:**
- Modify: `vite.config.ts` (add API proxy for dev)
- Modify: `src/frontend/main.ts` (fix infinite scroll lightbox index bug)

**Step 1: Add dev proxy to vite.config.ts**

```typescript
import { defineConfig } from "vite";
import { resolve } from "path";

export default defineConfig({
  root: resolve(__dirname, "src/frontend"),
  build: {
    outDir: resolve(__dirname, "dist/frontend"),
    emptyOutDir: true,
  },
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8787",
        changeOrigin: true,
      },
    },
  },
});
```

**Step 2: Fix lightbox index for appended cards**

In `main.ts`, the card click handler in `renderGrid` needs to track the absolute index in `currentData.zines`, not just the position within the current render batch. Replace the card click handler with a data-id based approach.

Change the card click listener in both `renderGrid` and the infinite scroll append section to use:

```typescript
  grid.querySelectorAll<HTMLElement>(".card").forEach((card) => {
    card.addEventListener("click", () => {
      if (!currentData) return;
      const id = card.dataset.id;
      const idx = currentData.zines.findIndex((z) => z.id === id);
      if (idx >= 0) openLightbox(currentData.zines, idx);
    });
  });
```

**Step 3: Test full flow**

Terminal 1: `wrangler dev` (API on :8787)
Terminal 2: `bun run dev:frontend` (Vite on :5173 with proxy)

- Search for "riot grrrl" — should return filtered results
- Click decade filters — results update
- Scroll down — infinite scroll loads more
- Click a card — lightbox opens with zoom/pan
- Arrow keys navigate lightbox
- Mobile viewport in devtools — responsive layout

**Step 4: Commit**

```bash
git add vite.config.ts src/frontend/
git commit -m "feat: add dev proxy, fix lightbox indexing for infinite scroll"
```

---

## Task 9: Production Build & Deploy

**Step 1: Create D1 database on Cloudflare**

```bash
wrangler d1 create punk-zines-db
```

Copy the `database_id` from output and update `wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "punk-zines-db"
database_id = "<paste-real-id-here>"
```

**Step 2: Initialize remote schema**

```bash
bun run db:init:remote
```

**Step 3: Import data to remote D1**

```bash
bun run import -- --remote
```

**Step 4: Build & deploy**

```bash
bun run deploy
```

Expected: Vite builds frontend to `dist/frontend/`, wrangler deploys worker + assets. Returns a `*.workers.dev` URL.

**Step 5: Verify production**

```bash
curl "https://punk-zines.<your-subdomain>.workers.dev/api/health"
curl "https://punk-zines.<your-subdomain>.workers.dev/api/zines?limit=1" | jq '.total'
```

Open the URL in browser — full app should work.

**Step 6: Commit**

```bash
git add wrangler.toml
git commit -m "feat: configure production D1 and deploy"
```

---

Plan complete and saved to `docs/plans/2026-03-17-fullstack-implementation.md`. Two execution options:

**1. Subagent-Driven (this session)** — I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Parallel Session (separate)** — Open new session with executing-plans, batch execution with checkpoints

Which approach?
