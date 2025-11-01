#!/usr/bin/env python3
"""
External Sources Harvester (non-IA)

Goal: Amass additional zine covers from public web sources to later
contribute to Internet Archive. This script provides a small, pluggable
adapter interface and a couple of basic adapters:

- FlickrAlbumAdapter: scrapes a Flickr album page for image URLs
- GenericPageAdapter: pulls <img> tags from any HTML page (best-effort)

Notes:
- This is conservative: it records source URLs + attribution and does not
  download images by default. Use --download to save thumbnails locally.
- Downstream IA contribution remains manual/curated (ia_contributor.py).
"""

from __future__ import annotations

import argparse
import json
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import sys
try:
    import requests
    from bs4 import BeautifulSoup  # type: ignore
    HAVE_DEPS = True
except Exception:
    HAVE_DEPS = False

DB_PATH = Path("punk_zines_database.json")
IMG_DIR = Path("images/external")


def load_db() -> Dict:
    if DB_PATH.exists():
        return json.loads(DB_PATH.read_text())
    return {"database_info": {}, "zines": []}


def save_db(db: Dict) -> None:
    info = db.setdefault("database_info", {})
    info["last_updated"] = time.strftime("%Y-%m-%d")
    info["total_entries"] = len(db.get("zines", []))
    DB_PATH.write_text(json.dumps(db, indent=2, ensure_ascii=False))


def generate_id(existing_ids: set, zine_name: str) -> str:
    words = [w for w in re.sub(r"[^A-Za-z0-9\s]", "", zine_name).split() if w]
    if not words:
        prefix = "ZN"
    elif len(words) == 1:
        prefix = words[0][:3].upper()
    else:
        prefix = (words[0][0] + (words[1][0] if len(words) > 1 else "")).upper()
        if len(words) > 2:
            prefix += words[2][0].upper()
    prefix = re.sub(r"[^A-Z]", "", prefix)[:3] or "ZN"
    i = 1
    while f"{prefix}{i:03d}" in existing_ids:
        i += 1
    new_id = f"{prefix}{i:03d}"
    existing_ids.add(new_id)
    return new_id


@dataclass
class FoundImage:
    title: str
    image_url: str
    page_url: str
    source_type: str


class BaseAdapter:
    def harvest(self, url: str) -> Iterable[FoundImage]:  # pragma: no cover (simple IO)
        raise NotImplementedError


class FlickrAlbumAdapter(BaseAdapter):
    def harvest(self, url: str) -> Iterable[FoundImage]:
        if not HAVE_DEPS:
            raise RuntimeError("requests + beautifulsoup4 required. pip install requests bs4")
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        # Flickr albums often contain <img src> with thumbs; use the largest available in src/srcset
        for img in soup.find_all("img"):
            srcset = img.get("srcset") or ""
            src = img.get("src") or ""
            best = None
            if srcset:
                parts = [p.strip().split(" ")[0] for p in srcset.split(",") if p.strip()]
                best = parts[-1] if parts else None
            if not best:
                best = src
            if not best or "staticflickr" not in best:
                continue
            alt = (img.get("alt") or "Flickr zine cover").strip()
            yield FoundImage(title=alt, image_url=best, page_url=url, source_type="flickr")


class GenericPageAdapter(BaseAdapter):
    def harvest(self, url: str) -> Iterable[FoundImage]:
        if not HAVE_DEPS:
            raise RuntimeError("requests + beautifulsoup4 required. pip install requests bs4")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }
        try:
            r = requests.get(url, timeout=20, headers=headers)
        except requests.exceptions.SSLError:
            # Fallback: try http if https cert is misconfigured (e.g., zinewiki)
            if url.startswith("https://"):
                alt = "http://" + url[len("https://"):]
                r = requests.get(alt, timeout=20, headers=headers)
            else:
                raise
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        domain = requests.utils.urlparse(url).netloc
        whitelist = {
            "digitaltransgenderarchive.net",
            "www.digitaltransgenderarchive.net",
            "sherwoodforestzinelibrary.org",
            "www.sherwoodforestzinelibrary.org",
            "austinfanzineproject.org",
            "www.austinfanzineproject.org",
            "digdc.dclibrary.org",
            "dclibrary.org",
            "microcosmpublishing.com",
            "www.microcosmpublishing.com",
            "quimbys.com",
            "www.quimbys.com",
            "zinewiki.com",
            "www.zinewiki.com",
        }
        for img in soup.find_all("img"):
            src = img.get("src") or ""
            if not src.startswith("http"):
                continue
            alt = (img.get("alt") or "").strip()
            # Prefer real photos over UI assets
            bad_alt_tokens = {"logo", "icon", "sprite", "button", "arrow", "avatar"}
            if any(tok in alt.lower() for tok in bad_alt_tokens):
                continue
            # Flickr-focused heuristics
            domain_ok = ("staticflickr" in src) or ("flickr.com" in src) or ("qzap" in src)
            # Also accept if page domain is a known archive
            page_domain_ok = domain in whitelist
            alt_ok = any(k in alt.lower() for k in ["zine", "fanzine", "punk", "riot grrrl", "queercore"]) or domain_ok or page_domain_ok
            if not alt_ok:
                continue
            # Try to link back to the nearest anchor
            a = img.find_parent("a")
            page_url = a.get("href") if a and a.get("href") else url
            if page_url and page_url.startswith("/"):
                from urllib.parse import urljoin as _urljoin
                page_url = _urljoin(url, page_url)
            title = alt or "Zine cover"
            yield FoundImage(title=title, image_url=src, page_url=page_url, source_type="other_archive")


ADAPTERS = {
    "flickr_album": FlickrAlbumAdapter(),
    "generic_page": GenericPageAdapter(),
}


def upsert_entries(db: Dict, found: List[FoundImage], download: bool = False) -> int:
    existing_ids = {z["id"] for z in db.get("zines", [])}
    added = 0
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for f in found:
        # Try to use alt/title as the zine name; this will be refined during quality pass
        name = f.title or "Untitled Zine"
        zid = generate_id(existing_ids, name)
        local_path = None
        if download:
            try:
                resp = requests.get(f.image_url, timeout=20)
                if resp.status_code == 200:
                    ext = ".jpg"
                    p = IMG_DIR / f"{zid.lower()}{ext}"
                    p.write_bytes(resp.content)
                    local_path = str(p)
            except Exception:
                local_path = None
        entry = {
            "id": zid,
            "zine_name": name,
            "issue_number": None,
            "year": None,
            "location": None,
            "image_url": local_path or f.image_url,
            "archive_source": f.page_url,
            "description": "Imported from external source; needs curation",
            "tags": ["punk", "zine"],
            "bands_featured": [],
            "circulation": None,
            "creators": None,
            "source_type": f.source_type,
            "attribution": f"Sourced from {f.source_type}: {f.page_url}",
            "license": None,
        }
        db.setdefault("zines", []).append(entry)
        added += 1
    save_db(db)
    return added


def main():
    parser = argparse.ArgumentParser(description="Harvest zine covers from external sources")
    parser.add_argument("adapter", choices=sorted(ADAPTERS.keys()), help="Which adapter to use")
    parser.add_argument("url", help="Source page URL (album, list, etc.)")
    parser.add_argument("--download", action="store_true", help="Also download images locally")
    args = parser.parse_args()

    if not HAVE_DEPS:
        print("Missing dependencies. Run: pip install requests beautifulsoup4")
        sys.exit(1)

    adapter = ADAPTERS[args.adapter]
    found = list(adapter.harvest(args.url))
    print(f"Found {len(found)} potential covers")
    if not found:
        return
    db = load_db()
    added = upsert_entries(db, found, download=args.download)
    print(f"✅ Added {added} entries to database")


if __name__ == "__main__":
    main()
