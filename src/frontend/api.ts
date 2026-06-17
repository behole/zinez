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
  circulation: string;
  source_type: string;
  archive_source: string;
  image_url: string;
  ia_item_url: string;
  ia_download_url: string;
  ia_thumb: string;
  attribution: string;
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
