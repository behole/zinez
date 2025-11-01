#!/usr/bin/env python3
"""
Harvest all matching albums from a Flickr user's albums page.

Example:
  python tools/harvest_flickr_albums.py \
    "https://www.flickr.com/photos/stillunusual/albums" \
    --filter "zine,fanzine" --download
"""

from __future__ import annotations

import argparse
import sys
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup  # type: ignore
except Exception:
    print("Missing dependencies. Run: pip install requests beautifulsoup4")
    sys.exit(1)

# Make project root importable
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from external_sources_scraper import (
    FlickrAlbumAdapter,
    upsert_entries,
    load_db,
)


def find_album_links(albums_url: str):
    r = requests.get(albums_url, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    seen = set()
    for a in soup.find_all("a"):
        href = a.get("href") or ""
        if "/albums/" in href and "/photos/" in href:
            url = urljoin("https://www.flickr.com", href)
            title = (a.get_text(strip=True) or "").strip()
            if url in seen:
                continue
            seen.add(url)
            yield url, title


def main():
    p = argparse.ArgumentParser(description="Harvest all albums from a Flickr user's albums page")
    p.add_argument("albums_url", help="Flickr albums URL, e.g. https://www.flickr.com/photos/<user>/albums")
    p.add_argument("--filter", default="", help="Comma-separated keywords to require in album title (case-insensitive)")
    p.add_argument("--download", action="store_true", help="Also download images locally")
    args = p.parse_args()

    filters = [t.strip().lower() for t in args.filter.split(",") if t.strip()]
    albums = list(find_album_links(args.albums_url))
    if filters:
        albums = [(u,t) for (u,t) in albums if any(f in (t or "").lower() for f in filters)]

    print(f"Discovered {len(albums)} album(s) matching filters: {filters or '[none]'}")
    if not albums:
        return

    adapter = FlickrAlbumAdapter()
    total_added = 0
    for url, title in albums:
        print(f"\n→ Harvesting album: {title or url}\n  {url}")
        found = list(adapter.harvest(url))
        print(f"  Found {len(found)} images")
        if not found:
            continue
        db = load_db()
        added = upsert_entries(db, found, download=args.download)
        print(f"  ✅ Added {added} entries")
        total_added += added
    print(f"\nAll done. Total added: {total_added}")


if __name__ == "__main__":
    main()
