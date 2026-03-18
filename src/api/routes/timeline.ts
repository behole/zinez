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
