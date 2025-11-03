#!/usr/bin/env python3
"""
Cleanup script to remove non-punk false positives from the database
"""

import json
import sys
from pathlib import Path

# Navigate to project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = PROJECT_ROOT / "punk_zines_database.json"

def load_database():
    """Load the database"""
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_database(db):
    """Save the database"""
    db["database_info"]["total_entries"] = len(db.get("zines", []))
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    print(f"✅ Database saved: {len(db.get('zines', []))} entries")

def cleanup_bad_entries(db, dry_run=True):
    """Remove entries that don't belong"""

    # Criteria for removal
    exclude_keywords = [
        'newspaper', 'enterprise', 'times', 'gazette', 'herald', 'tribune',
        'diary of', 'columbine', 'massacre', 'suicide', 'lynch letter',
        'botany', 'botanical', 'horticulture', 'flora', 'plantarum',
        'pharmacopoeia', 'toxicology', 'anatomy', 'physiology',
        'paxton', 'swenska wetenskaps', 'expédition dans',
        'telegraph', 'chronicle', 'blairmore', 'wimpy kid'
    ]

    removed = []
    kept = []

    for zine in db.get('zines', []):
        remove = False
        reason = None

        # Check year
        year = zine.get('year')
        if year:
            try:
                year_int = int(year)
                if year_int < 1974 or year_int > 2025:
                    remove = True
                    reason = f"Year {year} out of range (proto-punk era: 1974-2025)"
            except (ValueError, TypeError):
                pass

        # Check title for exclusions
        title_lower = zine.get('zine_name', '').lower()
        for keyword in exclude_keywords:
            if keyword in title_lower:
                remove = True
                reason = f"Excluded keyword '{keyword}' in title"
                break

        # Check if it has any punk-related content
        if not remove:
            desc = zine.get('description', '').lower()
            tags = ' '.join(zine.get('tags', [])).lower()
            combined = f"{title_lower} {desc} {tags}"

            punk_keywords = ['punk', 'zine', 'fanzine', 'hardcore', 'riot grrrl', 'anarcho', 'diy']
            if not any(keyword in combined for keyword in punk_keywords):
                remove = True
                reason = "No punk/zine keywords found"

        if remove:
            removed.append({
                'id': zine['id'],
                'name': zine['zine_name'],
                'year': zine.get('year'),
                'reason': reason
            })
        else:
            kept.append(zine)

    print("\n" + "="*70)
    print(f"CLEANUP RESULTS ({'DRY RUN' if dry_run else 'EXECUTING'})")
    print("="*70)
    print(f"Total entries: {len(db['zines'])}")
    print(f"Entries to keep: {len(kept)}")
    print(f"Entries to remove: {len(removed)}")
    print()

    if removed:
        print("ENTRIES TO BE REMOVED:")
        print("-"*70)
        for entry in removed[:20]:  # Show first 20
            print(f"  {entry['id']}: {entry['name'][:60]}")
            print(f"    Year: {entry['year']} | Reason: {entry['reason']}")

        if len(removed) > 20:
            print(f"  ... and {len(removed) - 20} more")

    if not dry_run:
        db['zines'] = kept
        save_database(db)
        print(f"\n✅ Removed {len(removed)} entries")
    else:
        print("\nRun with --execute to actually remove these entries")

    return removed

def main():
    dry_run = '--execute' not in sys.argv

    print("🧹 Cleanup Script for Punk Zines Database\n")

    db = load_database()
    print(f"Loaded database with {len(db.get('zines', []))} entries")

    removed = cleanup_bad_entries(db, dry_run=dry_run)

    if removed and dry_run:
        print("\n💡 To actually remove these entries, run:")
        print("   python tools/cleanup_bad_entries.py --execute")

if __name__ == "__main__":
    main()
