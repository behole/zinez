#!/usr/bin/env python3
"""
Wikimedia Commons Scraper for Punk Zines
Downloads images from Wikimedia Commons categories and adds them to the database.

No API key required! All content is Creative Commons licensed.

Usage:
  python wikimedia_scraper.py --category "Fanzines" --download
  python wikimedia_scraper.py --category "Punk" --download
  python wikimedia_scraper.py --categories "Fanzines,Punk,Punk_rock" --download
"""

import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import requests

# Paths
ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "punk_zines_database.json"
IMG_DIR = ROOT / "images" / "wikimedia"

# Wikimedia Commons API endpoint
API_URL = "https://commons.wikimedia.org/w/api.php"


class WikimediaCommonsScraper:
    """Scraper for Wikimedia Commons images"""

    def __init__(self):
        self.database = self.load_database()
        self.existing_ids = set(z["id"] for z in self.database.get("zines", []))
        self.existing_sources = set(z.get("archive_source") for z in self.database.get("zines", []))
        IMG_DIR.mkdir(parents=True, exist_ok=True)

    def load_database(self) -> Dict:
        """Load existing database"""
        if DB_PATH.exists():
            return json.loads(DB_PATH.read_text())
        return {"database_info": {}, "zines": []}

    def save_database(self):
        """Save database to file"""
        info = self.database.setdefault("database_info", {})
        info["last_updated"] = datetime.now().strftime("%Y-%m-%d")
        info["total_entries"] = len(self.database.get("zines", []))

        with open(DB_PATH, "w", encoding="utf-8") as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)

        print(f"✅ Database saved: {len(self.database.get('zines', []))} entries")

    def generate_id(self, title: str) -> str:
        """Generate unique ID for zine"""
        # Extract initials or abbreviation
        words = title.upper().split()
        if len(words) == 1:
            prefix = words[0][:3]
        else:
            prefix = "".join(word[0] for word in words[:3] if word)

        # Clean prefix
        prefix = re.sub(r"[^A-Z]", "", prefix)[:3] or "WMC"

        # Find next available number
        existing_with_prefix = [zid for zid in self.existing_ids if zid.startswith(prefix)]
        if existing_with_prefix:
            numbers = [int(re.search(r"\d+", zid).group()) for zid in existing_with_prefix if re.search(r"\d+", zid)]
            next_num = max(numbers) + 1 if numbers else 1
        else:
            next_num = 1

        new_id = f"{prefix}{next_num:03d}"
        self.existing_ids.add(new_id)
        return new_id

    def get_category_members(self, category: str, limit: int = 500) -> List[Dict]:
        """Get all files in a Wikimedia Commons category"""
        print(f"\n🔍 Fetching images from Category:{category}")

        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": f"Category:{category}",
            "cmlimit": min(limit, 500),  # Max 500 per request
            "cmtype": "file",  # Only files (images)
            "format": "json"
        }

        headers = {
            "User-Agent": "PunkZinesArchive/1.0 (https://github.com/behole/zinez; research project)"
        }

        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            members = data.get("query", {}).get("categorymembers", [])
            print(f"   Found {len(members)} images in category")
            return members

        except Exception as e:
            print(f"❌ Error fetching category: {e}")
            return []

    def get_image_info(self, filename: str) -> Optional[Dict]:
        """Get detailed information about an image"""
        params = {
            "action": "query",
            "titles": filename,
            "prop": "imageinfo",
            "iiprop": "url|size|metadata|extmetadata|timestamp",
            "format": "json"
        }

        headers = {
            "User-Agent": "PunkZinesArchive/1.0 (https://github.com/behole/zinez; research project)"
        }

        try:
            response = requests.get(API_URL, params=params, headers=headers, timeout=30)
            response.raise_for_status()
            data = response.json()

            pages = data.get("query", {}).get("pages", {})
            if not pages:
                return None

            # Get first (and only) page
            page = list(pages.values())[0]
            imageinfo = page.get("imageinfo", [{}])[0]

            return {
                "title": page.get("title", ""),
                "pageid": page.get("pageid"),
                "url": imageinfo.get("url"),
                "descriptionurl": imageinfo.get("descriptionurl"),
                "width": imageinfo.get("width"),
                "height": imageinfo.get("height"),
                "size": imageinfo.get("size"),
                "timestamp": imageinfo.get("timestamp"),
                "metadata": imageinfo.get("extmetadata", {})
            }

        except Exception as e:
            print(f"   ⚠️  Error getting image info: {e}")
            return None

    def extract_metadata(self, info: Dict) -> Dict:
        """Extract useful metadata from image info"""
        metadata = info.get("metadata", {})

        # Extract description
        desc = metadata.get("ImageDescription", {}).get("value", "")
        if not desc:
            desc = metadata.get("ObjectName", {}).get("value", "")

        # Clean HTML from description
        desc = re.sub(r"<[^>]+>", "", desc)
        desc = desc.strip()

        # Extract license
        license_info = metadata.get("LicenseShortName", {}).get("value", "CC-BY-SA")

        # Extract artist/creator
        artist = metadata.get("Artist", {}).get("value", "")
        artist = re.sub(r"<[^>]+>", "", artist).strip()

        # Extract date (try multiple fields)
        date_created = metadata.get("DateTimeOriginal", {}).get("value", "")
        if not date_created:
            date_created = metadata.get("DateTime", {}).get("value", "")

        # Try to extract year
        year = None
        if date_created:
            year_match = re.search(r"(19\d{2}|20\d{2})", date_created)
            if year_match:
                year = year_match.group(1)

        return {
            "description": desc[:500] if desc else "From Wikimedia Commons",
            "license": license_info,
            "artist": artist or "Unknown",
            "year": year,
            "date_created": date_created
        }

    def download_image(self, url: str, filename: str) -> Optional[str]:
        """Download image from URL"""
        headers = {
            "User-Agent": "PunkZinesArchive/1.0 (https://github.com/behole/zinez; research project)"
        }

        try:
            response = requests.get(url, headers=headers, timeout=60)
            response.raise_for_status()

            # Save to wikimedia directory
            filepath = IMG_DIR / filename
            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"   ✅ Downloaded: {filename}")
            return str(filepath)

        except Exception as e:
            print(f"   ⚠️  Download failed: {e}")
            return None

    def is_punk_related(self, title: str, description: str) -> bool:
        """Check if image is punk/zine related"""
        text = f"{title} {description}".lower()

        punk_keywords = [
            "punk", "zine", "fanzine", "hardcore", "anarcho",
            "riot grrrl", "diy", "underground", "subculture",
            "sniffin", "maximum", "flipside", "profane", "slash"
        ]

        return any(keyword in text for keyword in punk_keywords)

    def process_image(self, member: Dict, download: bool = True) -> int:
        """Process a single image from category"""
        filename = member.get("title", "")
        if not filename:
            return 0

        print(f"\n📄 Processing: {filename}")

        # Get detailed image info
        info = self.get_image_info(filename)
        if not info:
            print("   ⚠️  Could not get image info")
            return 0

        # Extract metadata
        meta = self.extract_metadata(info)

        # Check if already in database
        page_url = info.get("descriptionurl", "")
        if page_url in self.existing_sources:
            print("   → Already in database")
            return 0

        # Filter for punk-related content
        if not self.is_punk_related(filename, meta["description"]):
            print("   → Not punk/zine related, skipping")
            return 0

        # Download image if requested
        local_image = None
        if download and info.get("url"):
            # Create safe filename
            safe_name = re.sub(r"[^a-z0-9_-]", "_", filename.lower())[:100]
            safe_name = f"{safe_name}.jpg"
            local_image = self.download_image(info["url"], safe_name)

        # Generate database entry
        zine_id = self.generate_id(filename.replace("File:", "").replace(".jpg", "").replace(".png", ""))

        entry = {
            "id": zine_id,
            "zine_name": filename.replace("File:", "").replace(".jpg", "").replace(".png", ""),
            "issue_number": None,
            "year": meta["year"],
            "location": None,
            "image_url": local_image or info.get("url"),
            "archive_source": page_url,
            "description": meta["description"],
            "tags": ["punk", "zine", "wikimedia"],
            "bands_featured": [],
            "circulation": None,
            "creators": meta["artist"],
            "source_type": "wikimedia_commons",
            "attribution": f"From Wikimedia Commons: {page_url}",
            "license": meta["license"]
        }

        self.database.setdefault("zines", []).append(entry)
        self.save_database()
        print(f"   ✓ Added to database as {zine_id}")
        return 1

    def scrape_category(self, category: str, limit: int = 500, download: bool = True):
        """Scrape all images from a category"""
        members = self.get_category_members(category, limit)

        added = 0
        for i, member in enumerate(members, 1):
            print(f"\n[{i}/{len(members)}]", end=" ")
            added += self.process_image(member, download)

            # Rate limiting - be nice to Wikimedia
            time.sleep(1)

        print(f"\n\n✅ Category complete: {added} new zines added from {len(members)} images")
        return added


def main():
    parser = argparse.ArgumentParser(description="Wikimedia Commons Punk Zines Scraper")
    parser.add_argument("--category", help="Single category to scrape (e.g., 'Fanzines')")
    parser.add_argument("--categories", help="Comma-separated list of categories")
    parser.add_argument("--limit", type=int, default=500, help="Max images per category")
    parser.add_argument("--download", action="store_true", help="Download images locally")
    parser.add_argument("--no-download", dest="download", action="store_false", help="Don't download, just link to Wikimedia")
    parser.set_defaults(download=True)

    args = parser.parse_args()

    if not args.category and not args.categories:
        print("❌ Please specify --category or --categories")
        print("\nRecommended categories:")
        print("  --category Fanzines")
        print("  --category Punk")
        print("  --categories 'Fanzines,Punk,Punk_rock,Anarcho-punk'")
        return

    scraper = WikimediaCommonsScraper()

    # Get list of categories to scrape
    categories = []
    if args.category:
        categories = [args.category]
    elif args.categories:
        categories = [c.strip() for c in args.categories.split(",")]

    # Scrape each category
    total_added = 0
    for category in categories:
        added = scraper.scrape_category(category, args.limit, args.download)
        total_added += added
        time.sleep(2)  # Pause between categories

    print(f"\n{'='*60}")
    print(f"✅ SCRAPING COMPLETE")
    print(f"   New zines added: {total_added}")
    print(f"   Total in database: {len(scraper.database.get('zines', []))}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
