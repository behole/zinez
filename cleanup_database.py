#!/usr/bin/env python3
"""
Database Cleanup Tool
Identifies and removes false positives from the punk zines database
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path


class DatabaseCleaner:
    """Clean up false positives from the database"""

    def __init__(self, database_path: str = "punk_zines_database.json"):
        self.database_path = database_path
        self.backup_dir = Path("backups")
        self.backup_dir.mkdir(exist_ok=True)

        # False positive indicators
        self.false_positive_keywords = [
            # Audiobooks and classic literature
            "librivox",
            "audiobook",
            "audio book",

            # Classic literature titles
            "alice in wonderland",
            "moby dick",
            "tom sawyer",
            "sherlock holmes",
            "huckleberry finn",
            "dracula",
            "frankenstein",
            "treasure island",
            "swiss family robinson",
            "great expectations",
            "heart of darkness",
            "wuthering heights",
            "gulliver's travels",
            "uncle tom's cabin",
            "grimm",
            "sense and sensibility",

            # Radio shows
            "gunsmoke",
            "dragnet",
            "suspense",
            "richard diamond",
            "philip marlowe",

            # Other non-zine content
            "software library",
            "software capsule",
            "martin luther king",
            "i have a dream",
            "art of war",
            "game of life",
            "anthem",
            "time machine",
            "call of the wild",
            "secret garden",
            "princess of mars",
            "gods of mars",
            "science of getting rich",

            # Scientific journals
            "swenska wetenskaps",
            "paxton's magazine of botany",
            "icones plantarum",

            # Foreign language non-zine
            "expédition dans",

            # Academic archaeology
            "archaeology of crete",
        ]

        # Known good zine names (keep these even if they might match keywords)
        self.known_good_zines = [
            "maximum rocknroll",
            "punk planet",
            "profane existence",
            "sniffin' glue",
            "flipside",
            "heartattack",
            "bikini kill",
            "cometbus",
            "book your own fuckin' life",
            "riot grrrl",
            "slug & lettuce",
            "your flesh",
            "girl germs",
            "touch and go",
            "forced exposure",
            "clit rocket",
        ]

    def create_backup(self):
        """Create timestamped backup of database"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"punk_zines_database_backup_{timestamp}.json"

        shutil.copy2(self.database_path, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return backup_path

    def load_database(self):
        """Load database"""
        with open(self.database_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_database(self, database):
        """Save cleaned database"""
        with open(self.database_path, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
        print(f"✅ Database saved")

    def is_known_good_zine(self, zine_name: str) -> bool:
        """Check if zine is in known good list"""
        name_lower = zine_name.lower()
        return any(good in name_lower for good in self.known_good_zines)

    def is_false_positive(self, zine: dict) -> tuple[bool, str]:
        """
        Determine if entry is a false positive
        Returns: (is_false_positive, reason)
        """
        zine_name = zine.get('zine_name', '').lower()
        description = zine.get('description', '').lower()
        archive_source = zine.get('archive_source', '').lower()
        ia_metadata = zine.get('ia_metadata', {})
        mediatype = ia_metadata.get('mediatype', '')

        # Skip known good zines
        if self.is_known_good_zine(zine_name):
            return False, ""

        # Check for audiobook mediatype
        if mediatype == 'audio':
            return True, "Audio content (not a zine)"

        # Check for software/collection mediatype
        if mediatype in ['software', 'collection']:
            # Unless it's a zine collection
            if 'zine' not in description and 'punk' not in description:
                return True, f"Non-zine {mediatype}"

        # Check name and description for false positive keywords
        combined_text = f"{zine_name} {description}"

        for keyword in self.false_positive_keywords:
            if keyword in combined_text:
                return True, f"Matched keyword: {keyword}"

        return False, ""

    def analyze_database(self):
        """Analyze database and identify false positives"""
        print("\n" + "=" * 70)
        print("🔍 ANALYZING DATABASE FOR FALSE POSITIVES")
        print("=" * 70)

        database = self.load_database()
        zines = database.get('zines', [])

        false_positives = []
        legitimate = []

        for zine in zines:
            is_fp, reason = self.is_false_positive(zine)
            if is_fp:
                false_positives.append({
                    'zine': zine,
                    'reason': reason
                })
            else:
                legitimate.append(zine)

        # Print analysis
        print(f"\n📊 Analysis Results:")
        print(f"   Total entries: {len(zines)}")
        print(f"   Legitimate zines: {len(legitimate)} ({len(legitimate)/len(zines)*100:.1f}%)")
        print(f"   False positives: {len(false_positives)} ({len(false_positives)/len(zines)*100:.1f}%)")

        if false_positives:
            print(f"\n🚫 False Positives Identified:\n")
            for i, fp in enumerate(false_positives[:20], 1):  # Show first 20
                zine = fp['zine']
                print(f"{i}. {zine['zine_name']}")
                print(f"   ID: {zine['id']}")
                print(f"   Reason: {fp['reason']}")
                print(f"   Mediatype: {zine.get('ia_metadata', {}).get('mediatype', 'N/A')}")
                print()

            if len(false_positives) > 20:
                print(f"   ... and {len(false_positives) - 20} more\n")

        return legitimate, false_positives

    def clean_database(self, auto_confirm: bool = False):
        """Clean database by removing false positives"""
        print("\n" + "=" * 70)
        print("🧹 DATABASE CLEANUP")
        print("=" * 70)

        # Create backup first
        self.create_backup()

        # Analyze
        legitimate, false_positives = self.analyze_database()

        if not false_positives:
            print("\n✅ No false positives found! Database is clean.")
            return

        # Confirm removal
        if not auto_confirm:
            print(f"\n⚠️  Ready to remove {len(false_positives)} false positive entries")
            response = input("Proceed with cleanup? (yes/no): ").strip().lower()
            if response not in ['yes', 'y']:
                print("❌ Cleanup cancelled")
                return

        # Load and clean database
        database = self.load_database()
        database['zines'] = legitimate

        # Update metadata
        if 'database_info' in database:
            database['database_info']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
            database['database_info']['total_entries'] = len(legitimate)

        # Save
        self.save_database(database)

        # Delete images for removed entries
        images_removed = 0
        for fp in false_positives:
            zine = fp['zine']
            image_url = zine.get('image_url', '')
            if image_url.startswith('images/'):
                image_path = Path(image_url)
                if image_path.exists():
                    image_path.unlink()
                    images_removed += 1

        print(f"\n✅ CLEANUP COMPLETE!")
        print(f"   Removed: {len(false_positives)} false positive entries")
        print(f"   Deleted: {images_removed} associated images")
        print(f"   Remaining: {len(legitimate)} legitimate zines")

        # Save removed entries log
        log_path = self.backup_dir / f"removed_entries_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(false_positives, f, indent=2, ensure_ascii=False)
        print(f"   Log saved: {log_path}")


def main():
    import sys

    cleaner = DatabaseCleaner()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--analyze":
            cleaner.analyze_database()
        elif sys.argv[1] == "--clean":
            auto_confirm = "--yes" in sys.argv
            cleaner.clean_database(auto_confirm=auto_confirm)
        elif sys.argv[1] == "--help":
            print("""
Database Cleanup Tool

Usage:
  python cleanup_database.py --analyze          # Analyze without changes
  python cleanup_database.py --clean            # Clean with confirmation
  python cleanup_database.py --clean --yes      # Clean without confirmation
  python cleanup_database.py --help             # Show this help

What it does:
- Creates backup before any changes
- Identifies false positives (audiobooks, classic literature, etc.)
- Preserves known good zines (MRR, Punk Planet, etc.)
- Removes false positive entries and their images
- Logs all removed entries for review
""")
        else:
            print("Unknown option. Use --help for usage information.")
    else:
        # Default: analyze only
        print("Running analysis (use --clean to remove false positives)\n")
        cleaner.analyze_database()


if __name__ == "__main__":
    main()
