#!/usr/bin/env python3
"""
Database Schema Updater
Add new fields to existing database entries for bidirectional IA workflow

This script:
1. Adds source_type field to all entries
2. Adds IA attribution URLs for existing IA-sourced zines
3. Identifies entries that need source_type classification
4. Creates backup before updating
"""

import json
import os
from datetime import datetime
from pathlib import Path
import shutil


def create_backup(database_path: str) -> str:
    """Create timestamped backup of database"""
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"punk_zines_database_backup_{timestamp}.json"

    shutil.copy2(database_path, backup_path)
    print(f"✅ Backup created: {backup_path}")

    return str(backup_path)


def classify_source_type(zine: dict) -> str:
    """Classify the source type of a zine entry"""
    archive_source = zine.get('archive_source', '').lower()

    # Check if it's from Internet Archive
    if 'internet archive' in archive_source or 'archive.org' in archive_source:
        return 'internet_archive'

    # Check image URL for clues
    image_url = zine.get('image_url', '').lower()
    if 'archive.org' in image_url:
        return 'internet_archive'

    # Check if it has local image (potential contribution candidate)
    if image_url and not image_url.startswith('http'):
        return 'local_collection'

    # Check for other specific sources
    if 'flickr' in archive_source:
        return 'flickr'
    elif 'museum' in archive_source or 'library' in archive_source:
        return 'institutional_archive'
    elif archive_source and archive_source != 'unknown':
        return 'other_archive'

    # Unknown/undefined
    return 'uncategorized'


def extract_ia_identifier(zine: dict) -> str:
    """Extract Internet Archive identifier from existing data"""
    # Check ia_metadata first
    if 'ia_metadata' in zine and 'identifier' in zine['ia_metadata']:
        return zine['ia_metadata']['identifier']

    # Try to extract from archive_source
    archive_source = zine.get('archive_source', '')
    if 'Internet Archive:' in archive_source:
        # Format: "Internet Archive: identifier_here"
        parts = archive_source.split(':', 1)
        if len(parts) > 1:
            return parts[1].strip()

    return None


def update_database_schema(database_path: str = "punk_zines_database.json"):
    """Update all entries with new schema fields"""
    print("=" * 70)
    print("🔧 DATABASE SCHEMA UPDATER")
    print("=" * 70)

    # Create backup first
    backup_path = create_backup(database_path)

    # Load database
    with open(database_path, 'r', encoding='utf-8') as f:
        database = json.load(f)

    zines = database.get('zines', [])
    print(f"\n📊 Processing {len(zines)} zines...")

    # Statistics
    stats = {
        'total': len(zines),
        'updated': 0,
        'already_current': 0,
        'source_types': {},
        'ia_urls_added': 0,
        'errors': 0
    }

    # Process each zine
    for i, zine in enumerate(zines, 1):
        try:
            updated = False

            # Add source_type if missing
            if 'source_type' not in zine:
                source_type = classify_source_type(zine)
                zine['source_type'] = source_type
                updated = True

                # Track source type distribution
                stats['source_types'][source_type] = stats['source_types'].get(source_type, 0) + 1
            else:
                stats['source_types'][zine['source_type']] = stats['source_types'].get(zine['source_type'], 0) + 1

            # Add IA URLs if it's from Internet Archive
            if zine.get('source_type') == 'internet_archive':
                ia_identifier = extract_ia_identifier(zine)

                if ia_identifier:
                    # Add IA item URL if missing
                    if 'ia_item_url' not in zine:
                        zine['ia_item_url'] = f"https://archive.org/details/{ia_identifier}"
                        stats['ia_urls_added'] += 1
                        updated = True

                    # Add IA download URL if missing
                    if 'ia_download_url' not in zine:
                        zine['ia_download_url'] = f"https://archive.org/download/{ia_identifier}"
                        updated = True

                    # Add attribution if missing
                    if 'attribution' not in zine:
                        zine['attribution'] = f"Sourced from Internet Archive (archive.org/details/{ia_identifier})"
                        updated = True

                    # Ensure ia_metadata has identifier
                    if 'ia_metadata' not in zine:
                        zine['ia_metadata'] = {}
                    if 'identifier' not in zine['ia_metadata']:
                        zine['ia_metadata']['identifier'] = ia_identifier
                        updated = True

            if updated:
                stats['updated'] += 1
            else:
                stats['already_current'] += 1

            # Progress indicator
            if i % 100 == 0:
                print(f"   Processed {i}/{len(zines)} zines...")

        except Exception as e:
            print(f"   ⚠️  Error processing zine {zine.get('id', 'unknown')}: {e}")
            stats['errors'] += 1

    # Update database metadata
    if 'database_info' in database:
        database['database_info']['last_updated'] = datetime.now().strftime("%Y-%m-%d")
        database['database_info']['schema_version'] = '2.0'
        database['database_info']['schema_updated'] = datetime.now().isoformat()

    # Save updated database
    with open(database_path, 'w', encoding='utf-8') as f:
        json.dump(database, f, indent=2, ensure_ascii=False)

    # Print statistics
    print("\n" + "=" * 70)
    print("✅ DATABASE SCHEMA UPDATE COMPLETE")
    print("=" * 70)
    print(f"\nTotal zines: {stats['total']}")
    print(f"Updated: {stats['updated']}")
    print(f"Already current: {stats['already_current']}")
    print(f"Errors: {stats['errors']}")

    print(f"\n📊 Source Type Distribution:")
    for source_type, count in sorted(stats['source_types'].items(), key=lambda x: x[1], reverse=True):
        percentage = (count / stats['total'] * 100) if stats['total'] > 0 else 0
        print(f"   {source_type}: {count} ({percentage:.1f}%)")

    print(f"\n🔗 IA Attribution URLs added: {stats['ia_urls_added']}")

    print(f"\n💾 Backup saved at: {backup_path}")
    print("=" * 70)

    # Show zines that need source classification
    uncategorized = [z for z in zines if z.get('source_type') == 'uncategorized']
    if uncategorized:
        print(f"\n⚠️  {len(uncategorized)} zines need manual source classification:")
        for zine in uncategorized[:10]:  # Show first 10
            print(f"   - {zine['id']}: {zine.get('zine_name', 'Unknown')}")
            print(f"     Archive source: {zine.get('archive_source', 'none')}")
        if len(uncategorized) > 10:
            print(f"   ... and {len(uncategorized) - 10} more")


def main():
    """Main entry point"""
    print("🎸 Punk Zines Database Schema Updater\n")

    database_path = "punk_zines_database.json"

    if not os.path.exists(database_path):
        print(f"❌ Database not found: {database_path}")
        return

    # Confirm before updating
    print("This will update the database schema with:")
    print("  - source_type field for all entries")
    print("  - IA attribution URLs for Internet Archive sources")
    print("  - Enhanced metadata tracking")
    print("\nA backup will be created automatically.")

    response = input("\nProceed with update? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        update_database_schema(database_path)
    else:
        print("Update cancelled.")


if __name__ == "__main__":
    main()
