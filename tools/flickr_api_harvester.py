#!/usr/bin/env python3
"""
Flickr API Harvester for Zine Covers

Supports two modes:
  1) Search:   query Flickr for photos with zine-related keywords
  2) Group:    pull photos from a Flickr group pool (by URL or group_id)

Auth: Set environment variable FLICKR_API_KEY (and optionally FLICKR_API_SECRET).

Examples:
  # Search for punk zines (3 pages x 200 = 600 photos max)
  python tools/flickr_api_harvester.py search --text "punk zine" --per-page 200 --pages 3 --download

  # Harvest a group pool by URL
  python tools/flickr_api_harvester.py group --url "https://www.flickr.com/groups/punkfanzines/pool/" --per-page 200 --pages 5 --download
"""

from __future__ import annotations

import argparse
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import requests

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "punk_zines_database.json"
IMG_DIR = ROOT / "images" / "flickr"


def get_api_key() -> str:
    key = os.environ.get("FLICKR_API_KEY")
    if key:
        return key
    cfg = ROOT / "flickr_config.json"
    if cfg.exists():
        try:
            data = json.loads(cfg.read_text())
            if data.get("api_key"):
                return data["api_key"]
        except Exception:
            pass
    raise SystemExit("Missing Flickr API key. Set FLICKR_API_KEY env var or create flickr_config.json with {\"api_key\": \"...\"}.")


def flickr_call(method: str, params: Dict[str, str | int]) -> dict:
    api_key = get_api_key()
    base = "https://api.flickr.com/services/rest"
    q = {
        "method": method,
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": 1,
        **params,
    }
    r = requests.get(base, params=q, timeout=20)
    r.raise_for_status()
    data = r.json()
    if data.get("stat") != "ok":
        raise RuntimeError(f"Flickr API error: {data}")
    return data


def ensure_db() -> Dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {"database_info": {}, "zines": []}


def save_db(db: Dict) -> None:
    info = db.setdefault("database_info", {})
    info["last_updated"] = time.strftime("%Y-%m-%d")
    info["total_entries"] = len(db.get("zines", []))
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def build_photo_page(owner: str, photo_id: str) -> str:
    return f"https://www.flickr.com/photos/{owner}/{photo_id}"


def choose_image(p: dict) -> Optional[str]:
    # prefer medium/large
    for k in ("url_l", "url_c", "url_m", "url_z", "url_o", "url_s"):
        if p.get(k):
            return p[k]
    return None


def keyword_ok(title: str, tags: str, desc: str) -> bool:
    t = (title or "").lower()
    tg = (tags or "").lower()
    d = (desc or "").lower()
    hay = " ".join([t, tg, d])
    keys_any = ["zine", "fanzine"]
    keys_plus = ["punk", "riot grrrl", "hardcore", "queercore", "anarcho"]
    if any(k in hay for k in keys_any):
        return True
    # allow punk + zine split across fields
    return (any(k in hay for k in keys_plus) and ("zine" in hay or "fanzine" in hay))


def upsert_entries(db: Dict, photos: List[dict], download: bool) -> int:
    existing = db.get("zines", [])
    existing_srcs = {str(z.get("archive_source")) for z in existing}
    added = 0
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for p in photos:
        title = p.get("title") or "Flickr zine cover"
        owner = p.get("owner")
        pid = p.get("id")
        page = build_photo_page(owner, pid)
        if page in existing_srcs:
            continue
        img = choose_image(p)
        if not img:
            continue
        if not keyword_ok(title, p.get("tags", ""), p.get("description", {}).get("_content", "")):
            continue
        local_path = None
        if download:
            try:
                rr = requests.get(img, timeout=20)
                if rr.status_code == 200:
                    ext = ".jpg"
                    out = IMG_DIR / f"f_{pid}{ext}"
                    out.write_bytes(rr.content)
                    local_path = str(out)
            except Exception:
                local_path = None
        entry = {
            "id": f"F{pid}",
            "zine_name": title,
            "issue_number": None,
            "year": None,
            "location": None,
            "image_url": local_path or img,
            "archive_source": page,
            "description": (p.get("description", {}) or {}).get("_content", "Flickr import"),
            "tags": list(set((p.get("tags") or "").split())) or ["punk", "zine"],
            "bands_featured": [],
            "circulation": None,
            "creators": p.get("ownername") or owner,
            "source_type": "flickr",
            "attribution": f"Flickr photo by {p.get('ownername') or owner}",
            "license": None,
        }
        db.setdefault("zines", []).append(entry)
        existing_srcs.add(page)
        added += 1
    save_db(db)
    return added


def harvest_search(text: str, per_page: int, pages: int, download: bool) -> int:
    extras = "description,owner_name,tags,url_o,url_l,url_c,url_z,url_m,url_s"
    total_added = 0
    for page in range(1, pages + 1):
        data = flickr_call(
            "flickr.photos.search",
            {
                "text": text,
                "content_type": 1,  # photos only
                "safe_search": 1,
                "per_page": per_page,
                "page": page,
                "extras": extras,
                "sort": "relevance",
            },
        )
        photos = data.get("photos", {}).get("photo", [])
        if not photos:
            break
        added = upsert_entries(ensure_db(), photos, download)
        print(f"Page {page}: added {added} entries")
        total_added += added
        time.sleep(0.5)
    return total_added


def resolve_group_id(url: Optional[str], group_id: Optional[str]) -> str:
    if group_id:
        return group_id
    if not url:
        raise SystemExit("Provide --url or --group-id")
    data = flickr_call("flickr.urls.lookupGroup", {"url": url})
    gid = data.get("group", {}).get("id")
    if not gid:
        raise RuntimeError(f"Could not resolve group id from URL: {url}")
    return gid


def harvest_group(url: Optional[str], group_id: Optional[str], per_page: int, pages: int, download: bool) -> int:
    gid = resolve_group_id(url, group_id)
    extras = "description,owner_name,tags,url_o,url_l,url_c,url_z,url_m,url_s"
    total_added = 0
    for page in range(1, pages + 1):
        data = flickr_call(
            "flickr.groups.pools.getPhotos",
            {
                "group_id": gid,
                "per_page": per_page,
                "page": page,
                "extras": extras,
            },
        )
        photos = data.get("photos", {}).get("photo", [])
        if not photos:
            break
        added = upsert_entries(ensure_db(), photos, download)
        print(f"Page {page}: added {added} entries")
        total_added += added
        time.sleep(0.5)
    return total_added


def main():
    p = argparse.ArgumentParser(description="Flickr API harvester for zine covers")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("search", help="Search Flickr for zine photos")
    sp.add_argument("--text", default="punk zine", help="Search text")
    sp.add_argument("--per-page", type=int, default=200)
    sp.add_argument("--pages", type=int, default=3)
    sp.add_argument("--download", action="store_true")

    gp = sub.add_parser("group", help="Harvest a Flickr group pool")
    gp.add_argument("--url", help="Flickr group (pool) URL")
    gp.add_argument("--group-id", help="Flickr group_id (if you already know it)")
    gp.add_argument("--per-page", type=int, default=200)
    gp.add_argument("--pages", type=int, default=5)
    gp.add_argument("--download", action="store_true")

    args = p.parse_args()

    if args.cmd == "search":
        total = harvest_search(args.text, args.per_page, args.pages, args.download)
        print(f"\nDone. Total added: {total}")
    elif args.cmd == "group":
        total = harvest_group(args.url, args.group_id, args.per_page, args.pages, args.download)
        print(f"\nDone. Total added: {total}")


if __name__ == "__main__":
    main()

