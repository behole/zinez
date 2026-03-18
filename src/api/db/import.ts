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
