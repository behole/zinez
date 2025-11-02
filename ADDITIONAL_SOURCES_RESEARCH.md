# Additional Punk Zine Sources Research
**Research Date:** November 1, 2025

## Overview
This document catalogs potential sources for expanding the punk zines database beyond Internet Archive, with focus on IIIF-enabled collections and Creative Commons licensed materials.

---

## 🏛️ University & Institutional Collections

### Barnard College
**Barnard Zine Library**
- URL: https://zines.barnard.edu/
- Digital Collections: https://digitalcollections.barnard.edu/
- **Focus**: Zines by women, nonbinary people, and trans men
- **Emphasis**: Women of color creators
- **Platform**: Islandora (Drupal/Fedora/Solr based)
- **IIIF Status**: Unknown - may need to contact archives@barnard.edu
- **Physical Location**: 2nd floor, Milstein Center
- **Note**: Planning to digitize print collection with author permission

### Pratt Institute
**Pratt Libraries Zine Collection**
- Digital Zines: https://libguides.pratt.edu/zines/digitalzines
- Punk Zines: https://libguides.pratt.edu/zines/punk
- **Focus**: Locally-produced titles, artistic and literary content
- **Access**: Special Collections, non-circulating
- **Status**: Some digitization available through LibGuides
- **IIIF Status**: Unknown

### University of Maryland
**Punk Fanzine Collections**
- Archives: https://archives.lib.umd.edu/subjects/1785
- DC Punk Archive: https://digdc.dclibrary.org/do/5a4fb481-be26-44bb-8bc4-077f3b28dfb3
- **Ian MacKaye Digital Collection**: 1978-2020 materials
- **DC Punk Archive Zine Library**: Mid-1970s to present (mostly 1980s)
- **IIIF Status**: Unknown

### UCLA Library
**Punk Zines and Ephemera Collection**
- Finding Aid: https://oac.cdlib.org/findaid/ark:/13030/c8542t4x/
- **Coverage**: California punk scene, primarily Los Angeles
- **Date Range**: 1977-2018
- **License**: Finding aid metadata under CC0 1.0
- **Access**: Special Collections

### Other Notable Collections
- **University of Virginia**: Digital zine collections
- **University of San Francisco**: Gleeson Zine Library
- **University of Miami**: 5,000+ zine items (South Florida focus)
- **University of Iowa**: 700+ digitized sci-fi zines (Hevelin Collection)

---

## 🎨 IIIF Resources & Tools

### What We Have
- `tools/iiif_harvester.py` - IIIF Presentation API harvester (v2 & v3)
- `tools/find_iiif.py` - Find IIIF manifests on web pages
- `iiif_seeds.txt` - Placeholder for manifest URLs

### How to Use IIIF Tools

```bash
# Single manifest
python tools/iiif_harvester.py --manifest "https://example.org/iiif/manifest.json" --download

# Text file with manifest URLs
python tools/iiif_harvester.py --file iiif_seeds.txt --download

# IIIF Collection (recursive)
python tools/iiif_harvester.py --collection "https://example.org/iiif/collection.json" \
  --max-items 200 --download

# Find manifests on a page
python tools/find_iiif.py "https://digitalcollections.example.edu/item/123"
```

### Museums Using IIIF
While these don't specifically have punk zines, they demonstrate IIIF infrastructure:
- Harvard Art Museums: https://iiif.harvard.edu/
- Smithsonian: https://siarchives.si.edu/blog/some-iiif-y-collections
- Victoria & Albert Museum
- J. Paul Getty Trust
- Yale Center for British Art
- National Gallery of Art
- Cooper Hewitt Smithsonian Design Museum

### Action Items for IIIF
1. Contact Barnard Archives (archives@barnard.edu) about IIIF manifests
2. Check if Pratt has IIIF endpoints
3. Explore UCLA and UMD digital collections for manifests
4. Use `find_iiif.py` on digital collection pages
5. Build `iiif_seeds.txt` with discovered manifests

---

## 📸 Flickr Resources

### Key Flickr Albums
**1970s Fanzines Album**
- URL: https://www.flickr.com/photos/stillunusual/albums/72157657899141379/
- **Content**: Scans of 1970s punk fanzine front covers
- **License**: Check individual photos for CC licensing

### Using Existing Flickr Harvester

```bash
# Set API key (if you have one)
export FLICKR_API_KEY=<your_api_key>

# Search Flickr for punk zines
python tools/flickr_api_harvester.py search \
  --text "punk zine" --pages 3 --per-page 200 --download

# Search for fanzine covers
python tools/flickr_api_harvester.py search \
  --text "punk fanzine cover" --pages 5 --per-page 200 --download

# Harvest from groups (if any exist)
python tools/flickr_api_harvester.py group \
  --url "https://www.flickr.com/groups/punkfanzines/pool/" \
  --pages 5 --per-page 200 --download
```

### Search Terms to Try
- "punk zine"
- "punk fanzine"
- "hardcore fanzine"
- "riot grrrl zine"
- "1970s punk"
- "anarcho punk"
- "maximum rocknroll"
- "sniffin glue"

---

## 🌐 Wikimedia Commons

### Relevant Categories
**Direct Categories**
- Category:Fanzines: https://commons.wikimedia.org/wiki/Category:Fanzines
  - Notable: "A Selection of UK Punk Fanzines.jpg"
- Category:Punk: https://commons.wikimedia.org/wiki/Category:Punk
  - "SF punk zines at Prelinger Library.jpg"
- Category:Punk rock: https://commons.wikimedia.org/wiki/Category:Punk_rock
  - "Fanzines de Tucumán 2022.jpg"
- Category:Anarcho-punk: https://commons.wikimedia.org/wiki/Category:Anarcho-punk

### How to Harvest from Wikimedia Commons
1. Browse categories manually
2. Download high-res images (all CC-licensed)
3. Extract metadata from image descriptions
4. Add to database with proper attribution
5. Consider using Wikimedia API for bulk downloads

### Advantages
- All content is Creative Commons licensed
- High-quality scans often available
- Rich metadata in image descriptions
- Stable, reliable hosting
- Easy attribution requirements

---

## 🔧 Other Digital Archives

### Digital Fanzine Preservation Society (DFPS)
- Type: Blogspot collection
- Years: 2009-2011
- Focus: Hardcore and punk music fanzines
- Status: Check if still active/accessible

### Punk Planet Archive
- Internet Archive: 56+ GB of PDFs
- Already in our IA scraper coverage
- Collection ID: `punkplanet`

### Additional Scraping Targets
Consider adding scrapers for:
- HathiTrust Digital Library (if punk zines present)
- Archive-It collections (punk/zine collections)
- Library of Congress web archives
- European digital libraries (Europeana)

---

## 📊 Recommended Priorities

### High Priority (Immediate)
1. **Flickr API harvest** - Likely 100-500 new images
   - Run searches for major zine names
   - Target "punk zine" and "fanzine" tags

2. **Wikimedia Commons** - High-quality, CC-licensed
   - Manually browse and download from categories
   - Focus on cover scans

3. **IIIF Discovery** - Future-proof, high-res access
   - Contact Barnard, Pratt, UCLA, UMD
   - Use `find_iiif.py` on digital collection pages
   - Build manifest list in `iiif_seeds.txt`

### Medium Priority (Next Phase)
4. **University Digital Collections**
   - Systematic check of each library's digital collections
   - Look for downloadable images or APIs

5. **DC Punk Archive**
   - Explore https://digdc.dclibrary.org/
   - Check for bulk download options

### Lower Priority (Research Needed)
6. **Digital Fanzine Preservation Society**
   - Verify accessibility
   - Assess quality and coverage

7. **International Collections**
   - UK libraries (British Library, V&A)
   - European Punk Archives
   - Japanese zine collections

---

## 🎯 Next Steps

### Immediate Actions
1. Run Flickr searches with existing harvester
2. Download notable images from Wikimedia Commons categories
3. Contact institutions about IIIF access
4. Create `iiif_seeds.txt` starter list

### Research Tasks
1. Check if Barnard Digital Collections has IIIF
2. Explore Pratt digital collections for accessible content
3. Test UCLA finding aid for downloadable content
4. Survey other university digital libraries for punk content

### Development Tasks
1. Consider adding Wikimedia Commons API harvester
2. Enhance IIIF tools for batch processing
3. Add institution-specific scrapers as needed
4. Document licensing for each source

---

## 📝 Notes

### Licensing Considerations
- **Internet Archive**: Generally public domain or CC-licensed
- **IIIF Collections**: Varies by institution - always check
- **Flickr**: Individual photo licensing (look for CC)
- **Wikimedia Commons**: All CC or public domain
- **University Collections**: Often educational/research use; verify

### Attribution Requirements
Track for each source:
- `source_type`: iiif, flickr, wikimedia_commons, institutional_archive
- `attribution`: Required attribution text
- `license`: Specific license (CC-BY, CC0, etc.)
- `archive_source`: Original collection URL

### Technical Considerations
- IIIF provides highest quality and most metadata
- Wikimedia Commons is most reliable for long-term access
- Flickr API has rate limits (3600 requests/hour)
- University collections may require special access

---

## 🔗 Tools Summary

### Current Tools
- ✅ `archive_scraper.py` - Internet Archive
- ✅ `tools/iiif_harvester.py` - IIIF manifests
- ✅ `tools/find_iiif.py` - Discover IIIF on pages
- ✅ `tools/flickr_api_harvester.py` - Flickr API
- ✅ `external_sources_scraper.py` - Generic HTML pages

### Potential New Tools
- ⚠️ Wikimedia Commons API harvester
- ⚠️ HathiTrust scraper
- ⚠️ Library of Congress web archives
- ⚠️ Europeana API integration

---

**Last Updated**: November 1, 2025
**Researcher**: AI Assistant
**Status**: Active research, ready for implementation
