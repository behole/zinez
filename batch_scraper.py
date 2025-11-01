#!/usr/bin/env python3
"""
Batch Scraper for Punk Zines
Runs configured searches from scraper_config.json
"""

import json
import sys
from pathlib import Path
from archive_scraper import PunkZineScraper
import time


class BatchScraper:
    """Runs batch scraping operations based on config file"""

    def __init__(self, config_path: str = "scraper_config.json"):
        self.config_path = config_path
        self.config = self.load_config()
        self.scraper = PunkZineScraper()
        self.stats = {
            "searches_run": 0,
            "zines_found": 0,
            "images_downloaded": 0,
            "errors": 0
        }

    def load_config(self) -> dict:
        """Load configuration file"""
        if not Path(self.config_path).exists():
            print(f"⚠️  Config file not found: {self.config_path}")
            print("Using default settings")
            return {}

        with open(self.config_path, 'r') as f:
            return json.load(f)

    def run_priority_searches(self):
        """Run all enabled priority searches from config"""
        priority_searches = self.config.get('priority_searches', [])
        settings = self.config.get('scraper_settings', {})

        max_results = settings.get('max_results_per_query', 30)
        rate_limit = settings.get('rate_limit_seconds', 2)

        print("=" * 70)
        print("🎸 BATCH PUNK ZINE SCRAPER")
        print("=" * 70)
        print(f"\nLoaded {len(priority_searches)} search configurations")

        enabled_searches = [s for s in priority_searches if s.get('enabled', True)]
        print(f"Running {len(enabled_searches)} enabled searches\n")

        initial_count = len(self.scraper.database.get('zines', []))

        for i, search_config in enumerate(enabled_searches, 1):
            if not search_config.get('enabled', True):
                continue

            name = search_config.get('name', 'Unnamed Search')
            query = search_config.get('query', '')
            collection = search_config.get('collection')
            search_max = search_config.get('max_results', max_results)

            print(f"\n{'=' * 70}")
            print(f"Search {i}/{len(enabled_searches)}: {name}")
            print(f"{'=' * 70}")
            print(f"Query: {query}")
            if collection:
                print(f"Collection: {collection}")
            print(f"Max results: {search_max}")

            try:
                before = len(self.scraper.database.get('zines', []))
                new_zines = self.scraper.search_collection(
                    query=query,
                    collection=collection,
                    max_results=search_max
                )

                if new_zines:
                    self.scraper.database.setdefault('zines', []).extend(new_zines)
                    self.scraper.save_database()
                    after = len(self.scraper.database.get('zines', []))
                    added = after - before

                    print(f"\n✅ Search complete: {added} new zines added")
                    self.stats['zines_found'] += added
                else:
                    print(f"\n⚠️  No new zines found for this search")

                self.stats['searches_run'] += 1

                # Rate limiting
                if i < len(enabled_searches):
                    print(f"\n⏳ Waiting {rate_limit} seconds before next search...")
                    time.sleep(rate_limit)

            except Exception as e:
                print(f"\n❌ Error in search: {e}")
                self.stats['errors'] += 1
                continue

        final_count = len(self.scraper.database.get('zines', []))
        total_added = final_count - initial_count

        # Print summary
        print("\n" + "=" * 70)
        print("📊 BATCH SCRAPING SUMMARY")
        print("=" * 70)
        print(f"Searches completed: {self.stats['searches_run']}")
        print(f"Searches failed: {self.stats['errors']}")
        print(f"Total new zines: {total_added}")
        print(f"Total zines in database: {final_count}")
        print("=" * 70)

    def run_single_search(self, search_name: str):
        """Run a single named search from config"""
        priority_searches = self.config.get('priority_searches', [])

        search_config = next(
            (s for s in priority_searches if s.get('name') == search_name),
            None
        )

        if not search_config:
            print(f"❌ Search not found: {search_name}")
            print("\nAvailable searches:")
            for s in priority_searches:
                status = "✅" if s.get('enabled', True) else "⏸️"
                print(f"  {status} {s.get('name')}")
            return

        print(f"🔍 Running search: {search_name}\n")

        query = search_config.get('query', '')
        collection = search_config.get('collection')
        max_results = search_config.get('max_results', 30)

        before = len(self.scraper.database.get('zines', []))
        new_zines = self.scraper.search_collection(
            query=query,
            collection=collection,
            max_results=max_results
        )

        if new_zines:
            self.scraper.database.setdefault('zines', []).extend(new_zines)
            self.scraper.save_database()
            after = len(self.scraper.database.get('zines', []))
            print(f"\n✅ Added {after - before} new zines")
        else:
            print("\n⚠️  No new zines found")

    def list_searches(self):
        """List all configured searches"""
        priority_searches = self.config.get('priority_searches', [])

        print("\n📋 Configured Priority Searches:")
        print("=" * 70)

        for i, search in enumerate(priority_searches, 1):
            status = "✅ Enabled" if search.get('enabled', True) else "⏸️  Disabled"
            name = search.get('name', 'Unnamed')
            query = search.get('query', '')
            max_results = search.get('max_results', 30)

            print(f"\n{i}. {name} [{status}]")
            print(f"   Query: {query}")
            print(f"   Max results: {max_results}")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "--list":
            scraper = BatchScraper()
            scraper.list_searches()

        elif command == "--search":
            if len(sys.argv) > 2:
                search_name = ' '.join(sys.argv[2:])
                scraper = BatchScraper()
                scraper.run_single_search(search_name)
            else:
                print("Usage: python batch_scraper.py --search <search name>")

        elif command == "--help":
            print("""
Batch Punk Zine Scraper

Usage:
  python batch_scraper.py                    # Run all enabled searches
  python batch_scraper.py --list             # List configured searches
  python batch_scraper.py --search <name>    # Run specific search
  python batch_scraper.py --help             # Show this help

Examples:
  python batch_scraper.py --search "Riot Grrrl Zines"
  python batch_scraper.py --search "UK First Wave Punk"
  python batch_scraper.py --list
""")
        else:
            print(f"Unknown command: {command}")
            print("Use --help for usage information")

    else:
        # Run all enabled searches
        scraper = BatchScraper()
        scraper.run_priority_searches()


if __name__ == "__main__":
    main()
