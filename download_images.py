#!/usr/bin/env python3
"""
Punk Zine Image Downloader
Downloads cover images from Internet Archive and other sources
"""

import os
import requests
import json
from urllib.parse import urlparse, parse_qs
import time

# Configuration
IMAGE_DIR = "./images"
DATABASE_FILE = "punk_zines_database.json"

def ensure_directories():
    """Create image directories if they don't exist"""
    dirs = [
        "images/sniffin_glue",
        "images/maximum_rocknroll", 
        "images/punk_planet",
        "images/flipside",
        "images/riot_grrrl",
        "images/uk_punk",
        "images/us_hardcore",
        "images/international",
        "images/anarcho",
        "images/queercore"
    ]
    for dir in dirs:
        os.makedirs(dir, exist_ok=True)
        print(f"✓ Directory ready: {dir}")

def get_archive_thumbnail(archive_url):
    """Extract Internet Archive item ID and construct thumbnail URL"""
    if "archive.org/details/" in archive_url:
        # Extract item ID
        parts = archive_url.split("/details/")
        if len(parts) > 1:
            item_id = parts[1].split("/")[0].split("?")[0]
            # Construct thumbnail URL
            thumb_url = f"https://archive.org/services/img/{item_id}"
            return thumb_url, item_id
    return None, None

def download_image(url, filepath):
    """Download image from URL to filepath"""
    try:
        print(f"  Downloading: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  ✓ Saved: {filepath}")
            return True
        else:
            print(f"  ✗ Failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"  ✗ Error: {str(e)}")
        return False

def process_database():
    """Process the zine database and download missing images"""
    # Load database
    with open(DATABASE_FILE, 'r') as f:
        data = json.load(f)
    
    zines = data['zines']
    downloaded = 0
    skipped = 0
    failed = 0
    
    print(f"\nProcessing {len(zines)} zines...")
    print("=" * 50)
    
    for zine in zines:
        zine_id = zine['id']
        name = zine['zine_name']
        issue = zine.get('issue_number', '')
        
        print(f"\n{zine_id}: {name} #{issue}")
        
        # Determine subdirectory based on tags
        tags = zine.get('tags', [])
        subdir = "images/"
        
        if 'riot grrrl' in [t.lower() for t in tags]:
            subdir += "riot_grrrl/"
        elif 'anarcho' in [t.lower() for t in tags]:
            subdir += "anarcho/"
        elif 'UK' in tags:
            subdir += "uk_punk/"
        elif 'hardcore' in [t.lower() for t in tags]:
            subdir += "us_hardcore/"
        elif name.lower() == "sniffin' glue":
            subdir += "sniffin_glue/"
        elif name.lower() == "maximum rocknroll":
            subdir += "maximum_rocknroll/"
        elif name.lower() == "punk planet":
            subdir += "punk_planet/"
        else:
            subdir += "international/"
        
        # Create filename
        filename = f"{zine_id.lower()}_{name.lower().replace(' ', '_').replace('/', '_')}"
        if issue and issue != 'Various':
            filename += f"_{issue}"
        filename += ".jpg"
        filepath = os.path.join(subdir, filename)
        
        # Check if already downloaded
        if os.path.exists(filepath):
            print(f"  → Already exists: {filepath}")
            skipped += 1
            continue
        
        # Try to get image URL
        image_url = zine.get('image_url', '')
        
        if image_url and 'archive.org' in image_url:
            # Get Internet Archive thumbnail
            thumb_url, item_id = get_archive_thumbnail(image_url)
            if thumb_url:
                if download_image(thumb_url, filepath):
                    downloaded += 1
                else:
                    failed += 1
            else:
                print(f"  ✗ Could not extract Archive ID")
                failed += 1
        elif image_url and image_url.startswith('http'):
            # Try direct download for other URLs
            if download_image(image_url, filepath):
                downloaded += 1
            else:
                failed += 1
        else:
            print(f"  → No downloadable URL")
            failed += 1
        
        # Be nice to servers
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print(f"COMPLETE!")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped (existing): {skipped}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(zines)}")

def create_image_index():
    """Create an index of all downloaded images"""
    index = {}
    
    for root, dirs, files in os.walk(IMAGE_DIR):
        for file in files:
            if file.endswith(('.jpg', '.jpeg', '.png', '.gif')):
                # Extract zine ID from filename
                zine_id = file.split('_')[0].upper()
                filepath = os.path.join(root, file)
                relative_path = filepath.replace("\\", "/")
                index[zine_id] = relative_path
    
    # Save index
    with open('image_index.json', 'w') as f:
        json.dump(index, f, indent=2)
    
    print(f"\nImage index created with {len(index)} entries")
    return index

def main():
    print("=" * 50)
    print("PUNK ZINE IMAGE DOWNLOADER")
    print("=" * 50)
    
    # Setup directories
    print("\n1. Setting up directories...")
    ensure_directories()
    
    # Download images
    print("\n2. Downloading images from archives...")
    process_database()
    
    # Create index
    print("\n3. Creating image index...")
    index = create_image_index()
    
    print("\n" + "=" * 50)
    print("Done! Check the ./images directory")
    print("=" * 50)

if __name__ == "__main__":
    main()