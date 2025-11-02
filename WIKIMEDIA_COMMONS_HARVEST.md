# Harvesting Punk Zines from Wikimedia Commons

## Why Wikimedia Commons is Perfect

✅ **No API key required** - Can start immediately
✅ **All content is Creative Commons** - Legally free to use
✅ **High quality scans** - Often better than Flickr
✅ **Stable hosting** - Won't disappear
✅ **Easy attribution** - Built into metadata

## Quick Start (No Setup Required!)

### 1. Manual Download (Easiest - Start Now!)

Visit these categories and download images:
- https://commons.wikimedia.org/wiki/Category:Fanzines
- https://commons.wikimedia.org/wiki/Category:Punk
- https://commons.wikimedia.org/wiki/Category:Punk_rock
- https://commons.wikimedia.org/wiki/Category:Anarcho-punk

For each image:
1. Click the image
2. Click "Download" or view full resolution
3. Save to `images/wikimedia/`
4. Note the attribution info from the page

### 2. Using Wikimedia API (Also Free - No Key!)

The Wikimedia API doesn't require authentication for reading:

```bash
# Search for punk zine images
curl "https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:Fanzines&cmlimit=500&format=json" > fanzines.json

# Get image details
curl "https://commons.wikimedia.org/w/api.php?action=query&titles=File:A_Selection_of_UK_Punk_Fanzines.jpg&prop=imageinfo&iiprop=url|size|metadata&format=json"
```

### 3. Bulk Download Script

Create a simple Python script to download from Wikimedia:

```python
import requests
import json

def get_category_images(category, limit=100):
    url = "https://commons.wikimedia.org/w/api.php"
    params = {
        'action': 'query',
        'list': 'categorymembers',
        'cmtitle': f'Category:{category}',
        'cmlimit': limit,
        'cmtype': 'file',
        'format': 'json'
    }
    response = requests.get(url, params=params)
    return response.json()

# Get all fanzine images
images = get_category_images('Fanzines', 500)
print(json.dumps(images, indent=2))
```

## Recommended Categories for Punk Zines

1. **Category:Fanzines** - Main category
2. **Category:Punk** - General punk culture
3. **Category:Punk_rock** - Music focused
4. **Category:Anarcho-punk** - Political punk
5. **Category:Magazine_covers** - Some punk mags

## Next Steps

1. Visit https://commons.wikimedia.org/wiki/Category:Fanzines
2. Download any punk zine covers you find
3. Save to `images/wikimedia/`
4. Add to database manually or with a script

No API key needed - you can start RIGHT NOW! 🎸
