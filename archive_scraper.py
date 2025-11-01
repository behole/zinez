#!/usr/bin/env python3
"""
Internet Archive Punk Zine Scraper
Automatically scrapes punk zine metadata and images from archive.org

Features:
- Searches multiple punk zine collections on Internet Archive
- Extracts metadata (title, year, creator, location, etc.)
- Downloads cover images
- Integrates with existing punk_zines_database.json
- Supports batch processing and filtering
"""

import json
import os
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import time

# Check for required libraries
try:
    from internetarchive import search_items, get_item
    IA_AVAILABLE = True
except ImportError:
    print("⚠️  internetarchive library not installed")
    print("Run: pip install internetarchive")
    IA_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("⚠️  requests library not installed")
    print("Run: pip install requests")
    REQUESTS_AVAILABLE = False


class PunkZineScraper:
    """Scraper for punk zines from Internet Archive"""

    def __init__(self, database_path: str = "punk_zines_database.json"):
        self.database_path = database_path
        self.database = self.load_database()
        self.existing_ids = set(zine['id'] for zine in self.database.get('zines', []))
        self.images_dir = Path("images")
        self.images_dir.mkdir(exist_ok=True)

        # Track IA identifiers already present in DB to avoid duplicates
        self.seen_ia_ids = set()
        for z in self.database.get('zines', []):
            iid = None
            # Prefer explicit metadata
            meta = z.get('ia_metadata') or {}
            if isinstance(meta, dict):
                iid = meta.get('identifier')
            # Fallback: parse ia_item_url
            if not iid and z.get('ia_item_url'):
                parts = str(z['ia_item_url']).split('/details/')
                if len(parts) > 1:
                    iid = parts[1].split('/')[0].split('?')[0]
            # Fallback: parse archive_source suffix
            if not iid and isinstance(z.get('archive_source'), str) and 'Internet Archive:' in z['archive_source']:
                iid = z['archive_source'].split('Internet Archive:')[-1].strip()
            if iid:
                self.seen_ia_ids.add(iid)

        # Internet Archive collections to search
        self.collections = [
            "zines",
            "misczinespunk",
            "punkplanet",
            "maximumrnr",
            "riot_grrrl_collection"
        ]

        # Search queries for punk zines
        self.search_queries = [
            "punk fanzine",
            "punk zine",
            "hardcore fanzine",
            "riot grrrl",
            "anarcho punk",
            "DIY punk",
            "punk magazine"
        ]

    def load_database(self) -> Dict:
        """Load existing database"""
        if os.path.exists(self.database_path):
            with open(self.database_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"database_info": {}, "zines": []}

    def save_database(self):
        """Save database to file"""
        # Update metadata
        if "database_info" in self.database:
            self.database["database_info"]["last_updated"] = datetime.now().strftime("%Y-%m-%d")
            self.database["database_info"]["total_entries"] = len(self.database.get("zines", []))

        with open(self.database_path, 'w', encoding='utf-8') as f:
            json.dump(self.database, f, indent=2, ensure_ascii=False)

        print(f"✅ Database saved: {len(self.database.get('zines', []))} entries")

    def generate_id(self, zine_name: str, issue: Optional[str] = None) -> str:
        """Generate unique ID for zine"""
        # Extract initials or abbreviation
        words = zine_name.upper().split()
        if len(words) == 1:
            prefix = words[0][:3]
        else:
            prefix = ''.join(word[0] for word in words[:3] if word)

        # Clean prefix
        prefix = re.sub(r'[^A-Z]', '', prefix)[:3]

        # Find next available number
        existing_with_prefix = [zid for zid in self.existing_ids if zid.startswith(prefix)]
        if existing_with_prefix:
            numbers = [int(re.search(r'\d+', zid).group()) for zid in existing_with_prefix if re.search(r'\d+', zid)]
            next_num = max(numbers) + 1 if numbers else 1
        else:
            next_num = 1

        new_id = f"{prefix}{next_num:03d}"
        self.existing_ids.add(new_id)
        return new_id

    def extract_year(self, item_metadata: Dict) -> Optional[str]:
        """Extract publication year from metadata"""
        # Try multiple fields
        for field in ['year', 'date', 'publicdate', 'addeddate']:
            if field in item_metadata:
                year_str = str(item_metadata[field])
                # Extract 4-digit year
                match = re.search(r'(19\d{2}|20\d{2})', year_str)
                if match:
                    return match.group(1)
        return None

    def extract_location(self, item_metadata: Dict) -> Optional[str]:
        """Extract location from metadata"""
        # Check description and subject fields
        location_indicators = {
            'UK': ['London', 'UK', 'Britain', 'England', 'Scotland'],
            'USA': ['New York', 'NYC', 'Los Angeles', 'LA', 'San Francisco',
                    'SF', 'Boston', 'Chicago', 'Washington', 'DC'],
            'Canada': ['Toronto', 'Montreal', 'Vancouver', 'Canada'],
            'Japan': ['Tokyo', 'Japan', 'Osaka'],
        }

        description = item_metadata.get('description', '')
        subject = ' '.join(item_metadata.get('subject', []))
        text = f"{description} {subject}".lower()

        for country, cities in location_indicators.items():
            for city in cities:
                if city.lower() in text:
                    return city if city not in ['UK', 'USA', 'Canada', 'Japan'] else country

        return None

    def extract_tags(self, item_metadata: Dict) -> List[str]:
        """Extract relevant tags from metadata"""
        tags = set(['punk', 'DIY', 'zine'])

        # Add subjects as tags
        subjects = item_metadata.get('subject', [])
        if isinstance(subjects, list):
            for subject in subjects:
                # Clean and add relevant subjects
                subject_lower = subject.lower()
                if any(keyword in subject_lower for keyword in
                       ['punk', 'hardcore', 'riot', 'anarcho', 'zine', 'fanzine']):
                    tags.add(subject.lower())

        # Extract from description
        description = item_metadata.get('description', '').lower()
        keywords = ['hardcore', 'riot grrrl', 'anarcho', 'first wave', 'queercore',
                   'straight edge', 'crust', 'peace punk']
        for keyword in keywords:
            if keyword in description:
                tags.add(keyword)

        return sorted(list(tags))

    def download_cover_image(self, item_id: str, save_path: Path) -> bool:
        """Download cover/thumbnail image for item"""
        if not REQUESTS_AVAILABLE:
            return False

        try:
            # Try to get item thumbnail
            thumb_url = f"https://archive.org/services/img/{item_id}"
            response = requests.get(thumb_url, timeout=30)

            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                print(f"  ✅ Downloaded image: {save_path.name}")
                return True
            else:
                # Try alternative: direct metadata image
                item = get_item(item_id)
                metadata = item.metadata

                # Look for image files in the item
                if 'files' in item.item_metadata:
                    for file_info in item.item_metadata['files']:
                        filename = file_info.get('name', '')
                        if any(ext in filename.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                            # Download first image found
                            image_url = f"https://archive.org/download/{item_id}/{filename}"
                            response = requests.get(image_url, timeout=30)
                            if response.status_code == 200:
                                with open(save_path, 'wb') as f:
                                    f.write(response.content)
                                print(f"  ✅ Downloaded image: {save_path.name}")
                                return True
                            break

        except Exception as e:
            print(f"  ⚠️  Error downloading image: {e}")

        return False

    def search_collection(self, query: str, collection: Optional[str] = None,
                         max_results: Optional[int] = 50) -> List[Dict]:
        """Search Internet Archive for punk zines"""
        if not IA_AVAILABLE:
            print("❌ internetarchive library not available")
            return []

        new_zines = []
        # When running uncapped, flush results to disk periodically to retain progress
        commit_every = 50 if max_results is None else 0
        search_query = query

        if collection:
            search_query = f"{query} AND collection:{collection}"

        print(f"\n🔍 Searching: {search_query}")

        try:
            results = search_items(
                search_query,
                fields=['identifier', 'title', 'creator', 'year', 'date',
                       'description', 'subject', 'mediatype'],
                sorts=['downloads desc']
            )

            count = 0
            session_seen = set()
            for result in results:
                if max_results is not None and count >= max_results:
                    break

                item_id = result.get('identifier')
                title = result.get('title', 'Unknown')

                # Skip duplicates by IA identifier
                if not item_id or item_id in self.seen_ia_ids or item_id in session_seen:
                    continue

                # Keep only textual items (zines are usually texts) and allow images
                mt_raw = result.get('mediatype')
                if isinstance(mt_raw, list):
                    mtypes = {str(m).lower() for m in mt_raw if isinstance(m, (str, bytes))}
                else:
                    mtypes = {str(mt_raw).lower()} if mt_raw else set()
                if mtypes and not (mtypes & {"texts", "text", "image", "images"}):
                    continue

                print(f"\n📄 Found: {title}")
                print(f"   ID: {item_id}")

                # Get full metadata
                try:
                    item = get_item(item_id)
                    metadata = item.metadata

                    # Extract information
                    year = self.extract_year(metadata)
                    location = self.extract_location(metadata)
                    tags = self.extract_tags(metadata)
                    creators = metadata.get('creator', 'Unknown')
                    if isinstance(creators, list):
                        creators = '; '.join(creators)

                    # Generate ID
                    zine_id = self.generate_id(title)

                    # Download image
                    image_filename = f"{zine_id.lower()}.jpg"
                    image_path = self.images_dir / image_filename
                    image_downloaded = self.download_cover_image(item_id, image_path)

                    # Create zine entry with enhanced IA attribution
                    zine_entry = {
                        "id": zine_id,
                        "zine_name": title,
                        "issue_number": None,
                        "year": year,
                        "location": location,
                        "image_url": f"images/{image_filename}" if image_downloaded else f"https://archive.org/details/{item_id}",
                        "archive_source": f"Internet Archive: {item_id}",
                        "description": metadata.get('description', '')[:500],  # Truncate long descriptions
                        "tags": tags,
                        "bands_featured": [],
                        "circulation": None,
                        "creators": creators,
                        "source_type": "internet_archive",  # NEW: Track source type
                        "ia_item_url": f"https://archive.org/details/{item_id}",  # NEW: Direct link to IA item
                        "ia_download_url": f"https://archive.org/download/{item_id}",  # NEW: Direct download link
                        "ia_metadata": {
                            "identifier": item_id,
                            "mediatype": metadata.get('mediatype'),
                            "downloads": metadata.get('downloads', 0),
                            "collection": metadata.get('collection', [])  # NEW: Track which IA collections
                        },
                        "attribution": f"Sourced from Internet Archive (archive.org/details/{item_id})",  # NEW: Attribution text
                        "license": metadata.get('licenseurl') or metadata.get('license')  # NEW: Track license if available
                    }

                    new_zines.append(zine_entry)
                    session_seen.add(item_id)
                    count += 1

                    # Periodic commit to database to avoid losing progress on long queries
                    if commit_every and (len(new_zines) % commit_every == 0):
                        self.database.setdefault('zines', []).extend(new_zines)
                        self.save_database()
                        # Promote session_seen into global seen set for dedupe across queries
                        self.seen_ia_ids.update(session_seen)
                        print(f"   ↳ Committed {commit_every} items (running total this query: {count})")
                        new_zines.clear()

                    # Rate limiting
                    time.sleep(1)

                except Exception as e:
                    print(f"  ⚠️  Error processing item: {e}")
                    continue

        except Exception as e:
            print(f"❌ Search error: {e}")

        # Final commit for any leftovers collected during this search
        if new_zines:
            self.database.setdefault('zines', []).extend(new_zines)
            self.save_database()
            self.seen_ia_ids.update(session_seen)
            print(f"   ↳ Committed final {len(new_zines)} items for this query")
        return []

    def scrape_all_collections(self, max_per_query: Optional[int] = 20):
        """Scrape all configured collections"""
        print("=" * 60)
        print("🎸 PUNK ZINE SCRAPER - Internet Archive")
        print("=" * 60)

        if not IA_AVAILABLE:
            print("\n❌ Cannot proceed without internetarchive library")
            print("Install with: pip install internetarchive")
            return

        total_added = 0

        # Search each collection with each query
        for collection in self.collections:
            for query in self.search_queries:
                new_zines = self.search_collection(query, collection, max_per_query)
                print(f"\n📊 Found {len(new_zines)} new zines")

                if new_zines:
                    self.database.setdefault('zines', []).extend(new_zines)
                    self.save_database()  # incremental save to preserve progress
                    total_added += len(new_zines)

                # Be nice to the servers
                time.sleep(2)

        # Summary
        print("\n" + "=" * 60)
        print(f"✅ SCRAPING COMPLETE")
        print(f"   New zines added: {total_added}")
        print(f"   Total zines in database: {len(self.database.get('zines', []))}")
        print("=" * 60)

    def search_specific(self, query: str, max_results: Optional[int] = 50):
        """Search for specific zines"""
        new_zines = self.search_collection(query, max_results=max_results)

        if new_zines:
            self.database.setdefault('zines', []).extend(new_zines)
            self.save_database()
            print(f"\n✅ Added {len(new_zines)} new zines")
        else:
            print("\n⚠️  No new zines found")


def main():
    """Main entry point"""
    print("🎸 Punk Zine Scraper for Internet Archive\n")

    # Check dependencies
    if not IA_AVAILABLE or not REQUESTS_AVAILABLE:
        print("❌ Missing required libraries. Please install:")
        if not IA_AVAILABLE:
            print("   pip install internetarchive")
        if not REQUESTS_AVAILABLE:
            print("   pip install requests")
        sys.exit(1)

    scraper = PunkZineScraper()

    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--search":
            if len(sys.argv) > 2:
                query = ' '.join(sys.argv[2:])
                scraper.search_specific(query)
            else:
                print("Usage: python archive_scraper.py --search <query>")
        elif sys.argv[1] == "--full":
            # Full sweep across configured collections with no per-query cap
            scraper.scrape_all_collections(max_per_query=None)
        elif sys.argv[1] == "--help":
            print("""
Usage:
  python archive_scraper.py              # Run full scrape
  python archive_scraper.py --search <query>   # Search specific term
  python archive_scraper.py --full             # Sweep all collections (no cap)
  python archive_scraper.py --help       # Show this help

Examples:
  python archive_scraper.py --search "Maximum Rocknroll"
  python archive_scraper.py --search "riot grrrl"
  python archive_scraper.py --search "hardcore punk 1980s"
""")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        # Run full scrape
        scraper.scrape_all_collections(max_per_query=10)


if __name__ == "__main__":
    main()
