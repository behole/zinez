#!/usr/bin/env python3
"""
Find IIIF manifest URLs on a given webpage.

Heuristics:
- Look for absolute URLs containing 'manifest' and 'iiif'
- Parse JSON-LD blocks for Presentation API markers
- Scan attributes used by Universal Viewer (data-uri, data-config)

Usage:
  python tools/find_iiif.py "https://example.org/item/123"
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable, List

import requests
from bs4 import BeautifulSoup  # type: ignore


def find_candidates(html: str, base_url: str) -> List[str]:
    cands = set()
    # Raw regex: absolute URLs ending with 'manifest' or containing manifest.json
    for m in re.finditer(r"https?://[^\s\"']+manifest[^\s\"']+", html, re.I):
        cands.add(m.group(0))
    # JSON-LD blocks
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            text = tag.string or tag.text or ""
            for m in re.finditer(r"https?://[^\s\"']+manifest[^\s\"']+", text, re.I):
                cands.add(m.group(0))
        except Exception:
            continue
    # Universal Viewer config
    for tag in soup.find_all(attrs={"data-uri": True}):
        url = tag.get("data-uri")
        if isinstance(url, str) and "manifest" in url:
            cands.add(url)
    for tag in soup.find_all(attrs={"data-config": True}):
        cfg = tag.get("data-config")
        if isinstance(cfg, str) and "manifest" in cfg:
            for m in re.finditer(r"https?://[^\s\"']+manifest[^\s\"']+", cfg, re.I):
                cands.add(m.group(0))

    return sorted(cands)


def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/find_iiif.py <page_url>")
        sys.exit(1)
    url = sys.argv[1]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    r = requests.get(url, headers=headers, timeout=25)
    r.raise_for_status()
    cands = find_candidates(r.text, url)
    if not cands:
        print("No IIIF manifest references found.")
        sys.exit(0)
    print("Found manifest candidates:")
    for c in cands:
        print(c)


if __name__ == "__main__":
    main()

