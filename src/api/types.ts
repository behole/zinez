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
