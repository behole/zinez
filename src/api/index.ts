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
