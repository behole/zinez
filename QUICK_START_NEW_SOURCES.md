# Quick Start: Adding Zines from New Sources

## 1. Flickr (Easiest - Start Here!)

### Search for punk zine covers:
```bash
export FLICKR_API_KEY=your_key_here  # Get from flickr.com/services/api/

python tools/flickr_api_harvester.py search \
  --text "punk zine" --pages 3 --per-page 200 --download

python tools/flickr_api_harvester.py search \
  --text "punk fanzine cover" --pages 3 --per-page 200 --download
```

## 2. Wikimedia Commons (Manual - High Quality!)

### Browse and download:
1. Visit: https://commons.wikimedia.org/wiki/Category:Fanzines
2. Visit: https://commons.wikimedia.org/wiki/Category:Punk
3. Download full-resolution images
4. Add manually to database or use external_sources_scraper.py

## 3. IIIF Collections (Best Quality - Needs Research!)

### Find manifests:
```bash
# Example: Search a digital collection page for IIIF manifests
python tools/find_iiif.py "https://digitalcollections.example.edu/browse"

# Once you have manifests, add to iiif_seeds.txt then:
python tools/iiif_harvester.py --file iiif_seeds.txt --download
```

### Institutions to contact:
- Barnard: archives@barnard.edu
- Pratt Institute
- UCLA Special Collections
- University of Maryland

## 4. Current Progress

**Database:** 3,636 zines (+26 today!)
**Scrapers running:** Multiple IA searches in progress

See ADDITIONAL_SOURCES_RESEARCH.md for complete details!
