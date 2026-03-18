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
