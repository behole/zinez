#!/usr/bin/env python3
"""
Aggressive Expansion Mode
Get ALL remaining punk zines from Internet Archive
"""

import json
import time
from archive_scraper import PunkZineScraper


def aggressive_mrr_expansion():
    """Get ALL remaining Maximum Rocknroll issues"""
    print("=" * 70)
    print("🔥 AGGRESSIVE MRR EXPANSION - GET THEM ALL!")
    print("=" * 70)

    scraper = PunkZineScraper()

    # Search strategies for MRR
    searches = [
        ("Maximum Rocknroll 004", 50),  # Early 80s
        ("Maximum Rocknroll 005", 50),
        ("Maximum Rocknroll 007", 50),
        ("Maximum Rocknroll 008", 50),
        ("Maximum Rocknroll 009", 50),
        ("Maximum Rocknroll 010", 50),
        ("Maximum Rocknroll 011", 50),
        ("Maximum Rocknroll 012", 50),
        ("Maximum Rocknroll 014", 50),
        ("Maximum Rocknroll 015", 50),
        ("Maximum Rocknroll 016", 50),
        ("Maximum Rocknroll 017", 50),
        ("Maximum Rocknroll 018", 50),
        ("Maximum Rocknroll 020", 50),  # More 80s
        ("Maximum Rocknroll 021", 50),
        ("Maximum Rocknroll 022", 50),
        ("Maximum Rocknroll 023", 50),
        ("Maximum Rocknroll 024", 50),
        ("Maximum Rocknroll 025", 50),
        ("Maximum Rocknroll 026", 50),
        ("Maximum Rocknroll 027", 50),
        ("Maximum Rocknroll 028", 50),
        ("Maximum Rocknroll 029", 50),
        ("Maximum Rocknroll 030", 50),
    ]

    initial_count = len(scraper.database.get('zines', []))
    total_added = 0

    for query, max_results in searches:
        print(f"\n🔍 Searching: {query}")
        new_zines = scraper.search_collection(query, "maximumrnr", max_results)

        if new_zines:
            scraper.database.setdefault('zines', []).extend(new_zines)
            scraper.save_database()
            total_added += len(new_zines)
            print(f"   ✅ Added {len(new_zines)} zines")
        else:
            print(f"   ⏭️  No new zines")

        time.sleep(1)  # Rate limiting

    final_count = len(scraper.database.get('zines', []))
    print(f"\n" + "=" * 70)
    print(f"✅ AGGRESSIVE MRR COMPLETE")
    print(f"   Started with: {initial_count}")
    print(f"   Ended with: {final_count}")
    print(f"   Added: {total_added}")
    print("=" * 70)


def search_rare_zines():
    """Search for rare and underground zines"""
    print("\n" + "=" * 70)
    print("💎 RARE ZINE HUNTING")
    print("=" * 70)

    scraper = PunkZineScraper()

    rare_searches = [
        "Cometbus",
        "Ben is Dead",
        "Slug and Lettuce",
        "Your Flesh",
        "Motorbooty",
        "Scam zine",
        "Temp Slave",
        "Dishwasher Pete",
        "Doris zine",
        "Chainsaw zine",
        "Kill Your Pet Puppy",
        "Desperate Times",
        "Ripper zine",
        "Guillotine fanzine",
        "No Mag",
        "Forced Exposure",
        "Op Magazine",
        "Jamming fanzine UK",
        "Ripped and Torn",
        "48 Thrills",
        "Sideburns fanzine",
    ]

    initial_count = len(scraper.database.get('zines', []))

    for query in rare_searches:
        print(f"\n🔍 Hunting: {query}")
        new_zines = scraper.search_collection(query, max_results=20)

        if new_zines:
            scraper.database.setdefault('zines', []).extend(new_zines)
            scraper.save_database()
            print(f"   ✅ Found {len(new_zines)} zines!")
        else:
            print(f"   ⏭️  Nothing found")

        time.sleep(1)

    final_count = len(scraper.database.get('zines', []))
    print(f"\n✅ Rare zine hunt complete: +{final_count - initial_count} zines")


def search_movements():
    """Target specific punk movements"""
    print("\n" + "=" * 70)
    print("🎸 MOVEMENT-SPECIFIC EXPANSION")
    print("=" * 70)

    scraper = PunkZineScraper()

    movement_searches = [
        ("straight edge zine OR sXe fanzine", 30),
        ("emo zine OR emocore fanzine", 20),
        ("crust punk zine", 20),
        ("d-beat zine", 15),
        ("powerviolence zine", 15),
        ("fastcore zine", 15),
        ("grindcore zine OR grind fanzine", 20),
        ("screamo zine", 15),
        ("youth crew zine", 15),
        ("peace punk zine", 20),
        ("street punk zine OR Oi! fanzine", 20),
        ("ska punk zine", 15),
        ("folk punk zine", 15),
        ("garage punk zine", 15),
    ]

    initial_count = len(scraper.database.get('zines', []))

    for query, max_results in movement_searches:
        print(f"\n🔍 Searching: {query}")
        new_zines = scraper.search_collection(query, max_results=max_results)

        if new_zines:
            scraper.database.setdefault('zines', []).extend(new_zines)
            scraper.save_database()
            print(f"   ✅ Added {len(new_zines)} zines")
        else:
            print(f"   ⏭️  Nothing new")

        time.sleep(1)

    final_count = len(scraper.database.get('zines', []))
    print(f"\n✅ Movement expansion complete: +{final_count - initial_count} zines")


def search_international():
    """Expand international coverage"""
    print("\n" + "=" * 70)
    print("🌍 INTERNATIONAL EXPANSION")
    print("=" * 70)

    scraper = PunkZineScraper()

    international_searches = [
        ("punk zine japan OR japanese punk fanzine", 30),
        ("punk zine brazil OR brazilian punk", 20),
        ("punk zine germany OR german punk fanzine", 25),
        ("punk zine france OR french punk fanzine", 20),
        ("punk zine australia OR aussie punk", 20),
        ("punk zine mexico OR mexican punk", 20),
        ("punk zine spain OR spanish punk fanzine", 15),
        ("punk zine italy OR italian punk", 15),
        ("punk zine sweden OR swedish punk", 15),
        ("punk zine finland OR finnish punk", 15),
        ("punk zine netherlands OR dutch punk", 15),
        ("punk zine poland OR polish punk", 15),
        ("punk zine argentina", 15),
        ("punk zine chile", 15),
    ]

    initial_count = len(scraper.database.get('zines', []))

    for query, max_results in international_searches:
        print(f"\n🔍 Searching: {query}")
        new_zines = scraper.search_collection(query, max_results=max_results)

        if new_zines:
            scraper.database.setdefault('zines', []).extend(new_zines)
            scraper.save_database()
            print(f"   ✅ Added {len(new_zines)} zines")
        else:
            print(f"   ⏭️  Nothing new")

        time.sleep(1)

    final_count = len(scraper.database.get('zines', []))
    print(f"\n✅ International expansion complete: +{final_count - initial_count} zines")


def search_regional_us():
    """Deep dive into US regional scenes"""
    print("\n" + "=" * 70)
    print("🗺️ US REGIONAL DEEP DIVE")
    print("=" * 70)

    scraper = PunkZineScraper()

    regional_searches = [
        ("Detroit punk zine OR Michigan punk fanzine", 20),
        ("Minneapolis punk zine OR Minnesota punk", 20),
        ("Seattle punk zine OR Pacific Northwest punk", 20),
        ("Portland punk zine OR Oregon punk", 20),
        ("Austin punk zine OR Texas punk", 20),
        ("Philadelphia punk zine OR Philly punk", 20),
        ("Cleveland punk zine OR Ohio punk", 15),
        ("Pittsburgh punk zine", 15),
        ("Denver punk zine OR Colorado punk", 15),
        ("Phoenix punk zine OR Arizona punk", 15),
        ("Atlanta punk zine OR Georgia punk", 15),
        ("New Orleans punk zine", 15),
        ("Richmond punk zine OR Virginia punk", 20),
        ("Baltimore punk zine OR Maryland punk", 15),
        ("Long Island punk zine", 15),
        ("New Jersey punk zine", 20),
    ]

    initial_count = len(scraper.database.get('zines', []))

    for query, max_results in regional_searches:
        print(f"\n🔍 Searching: {query}")
        new_zines = scraper.search_collection(query, max_results=max_results)

        if new_zines:
            scraper.database.setdefault('zines', []).extend(new_zines)
            scraper.save_database()
            print(f"   ✅ Added {len(new_zines)} zines")
        else:
            print(f"   ⏭️  Nothing new")

        time.sleep(1)

    final_count = len(scraper.database.get('zines', []))
    print(f"\n✅ Regional expansion complete: +{final_count - initial_count} zines")


def run_aggressive_expansion():
    """Run all expansion strategies"""
    print("\n" + "=" * 70)
    print("🔥🔥🔥 AGGRESSIVE EXPANSION MODE - CATCH THEM ALL! 🔥🔥🔥")
    print("=" * 70)

    scraper = PunkZineScraper()
    initial_count = len(scraper.database.get('zines', []))

    print(f"\nStarting with: {initial_count} zines\n")

    # Phase 1: MRR expansion
    print("\n" + "▼" * 35)
    print("PHASE 1: MAXIMUM ROCKNROLL EXPANSION")
    print("▼" * 35)
    aggressive_mrr_expansion()

    # Phase 2: Rare zines
    print("\n" + "▼" * 35)
    print("PHASE 2: RARE ZINES")
    print("▼" * 35)
    search_rare_zines()

    # Phase 3: Movements
    print("\n" + "▼" * 35)
    print("PHASE 3: MOVEMENT-SPECIFIC")
    print("▼" * 35)
    search_movements()

    # Phase 4: International
    print("\n" + "▼" * 35)
    print("PHASE 4: INTERNATIONAL")
    print("▼" * 35)
    search_international()

    # Phase 5: Regional US
    print("\n" + "▼" * 35)
    print("PHASE 5: US REGIONAL SCENES")
    print("▼" * 35)
    search_regional_us()

    # Final stats
    scraper = PunkZineScraper()
    final_count = len(scraper.database.get('zines', []))
    total_added = final_count - initial_count

    print("\n\n" + "=" * 70)
    print("🎉 AGGRESSIVE EXPANSION COMPLETE!")
    print("=" * 70)
    print(f"\n   Started with:  {initial_count} zines")
    print(f"   Ended with:    {final_count} zines")
    print(f"   Total added:   {total_added} zines")
    print(f"   Growth:        {total_added/initial_count*100:.1f}%")
    print("\n" + "=" * 70)
    print("🎸 GOTTA CATCH 'EM ALL! 🎸")
    print("=" * 70)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        phase = sys.argv[1]
        if phase == "mrr":
            aggressive_mrr_expansion()
        elif phase == "rare":
            search_rare_zines()
        elif phase == "movements":
            search_movements()
        elif phase == "international":
            search_international()
        elif phase == "regional":
            search_regional_us()
        else:
            print("Unknown phase. Options: mrr, rare, movements, international, regional")
    else:
        # Run everything!
        run_aggressive_expansion()
