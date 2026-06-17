import { Hono } from "hono";
import type { Env, ZineRow, ZineResponse } from "../types";

const zines = new Hono<{ Bindings: Env }>();

export function rowToResponse(row: ZineRow): ZineResponse {
  return {
    ...row,
    tags: safeParseArray(row.tags),
    bands_featured: safeParseArray(row.bands_featured),
  };
}

export function safeParseArray(s: string): string[] {
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
