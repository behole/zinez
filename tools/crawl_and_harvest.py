#!/usr/bin/env python3
"""
Lightweight crawler + harvester for external archives.

Given a start URL, crawls same-domain pages up to a specified depth/limit,
and applies GenericPageAdapter harvesting on each visited page.

Usage:
  python tools/crawl_and_harvest.py \
    --start https://archive.qzap.org/ \
    --max-pages 50 --depth 2 --download

  python tools/crawl_and_harvest.py \
    --start https://www.digitaltransgenderarchive.net/col/0g354f345 \
    --max-pages 60 --depth 2 --download
"""

from __future__ import annotations

import argparse
import time
from collections import deque
from urllib.parse import urlparse, urljoin

import sys
try:
    import requests
    from bs4 import BeautifulSoup  # type: ignore
    HAVE_DEPS = True
except Exception:
    HAVE_DEPS = False

ROOT = None
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from external_sources_scraper import GenericPageAdapter, load_db, upsert_entries


def crawl(start: str, max_pages: int, depth: int):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": start,
    }
    parsed = urlparse(start)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    q = deque([(start, 0)])
    seen = set([start])
    pages = []
    while q and len(pages) < max_pages:
        url, d = q.popleft()
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code >= 400:
                continue
            pages.append(url)
            if d >= depth:
                continue
            soup = BeautifulSoup(r.text, 'html.parser')
            for a in soup.find_all('a'):
                href = a.get('href')
                if not href:
                    continue
                href = urljoin(url, href)
                hp = urlparse(href)
                if hp.netloc != parsed.netloc:
                    continue
                if any(hp.path.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.gif', '.pdf', '.zip', '.dmg')):
                    continue
                if href not in seen and href.startswith(origin):
                    seen.add(href)
                    q.append((href, d+1))
        except Exception:
            continue
    return pages


def main():
    ap = argparse.ArgumentParser(description="Crawl site and harvest image covers")
    ap.add_argument("--start", required=True, help="Start URL to crawl")
    ap.add_argument("--max-pages", type=int, default=50)
    ap.add_argument("--depth", type=int, default=2)
    ap.add_argument("--download", action="store_true")
    args = ap.parse_args()

    if not HAVE_DEPS:
        print("Missing dependencies. Run: pip install requests beautifulsoup4")
        sys.exit(1)

    print(f"Discovering up to {args.max_pages} pages (depth {args.depth}) from {args.start}")
    pages = crawl(args.start, args.max_pages, args.depth)
    print(f"Found {len(pages)} pages to scan for covers")

    adapter = GenericPageAdapter()
    db = load_db()
    total = 0
    for i, url in enumerate(pages, 1):
        try:
            found = list(adapter.harvest(url))
            if found:
                added = upsert_entries(db, found, download=args.download)
                total += added
                print(f"[{i}/{len(pages)}] {url} -> +{added}")
            else:
                print(f"[{i}/{len(pages)}] {url} -> 0")
            time.sleep(0.2)
        except Exception as e:
            print(f"[{i}/{len(pages)}] {url} -> error: {e}")
            continue
    print(f"\nDone. Added {total} entries.")


if __name__ == "__main__":
    main()

