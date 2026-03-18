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
