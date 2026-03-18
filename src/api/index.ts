import { Hono } from "hono";
import { cors } from "hono/cors";
import type { Env } from "./types";
import zines from "./routes/zines";
import stats from "./routes/stats";
import timeline from "./routes/timeline";

const app = new Hono<{ Bindings: Env }>();

app.use("/api/*", cors());

app.route("/api/zines", zines);
app.route("/api/stats", stats);
app.route("/api/timeline", timeline);

// Health check
app.get("/api/health", (c) => c.json({ status: "ok" }));

export default app;
