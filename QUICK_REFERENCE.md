# Punk Zines Database - Quick Reference Card
## Version 2.0 - Bidirectional IA Integration

---

## 🚀 Quick Commands

### Scraping FROM Internet Archive
```bash
# Search for specific zines
python archive_scraper.py --search "riot grrrl"
python archive_scraper.py --search "maximum rocknroll"
python archive_scraper.py --search "hardcore punk 1980s"

# Run batch searches
python batch_scraper.py

# Run aggressive expansion
python aggressive_expansion.py

# Full sweep across configured IA collections (no per-query cap)
python archive_scraper.py --full
```

### Contributing TO Internet Archive
```bash
# Check statistics
python ia_contributor.py --stats

# Prepare contribution packages
python ia_contributor.py --prepare

# Configure IA CLI (one-time)
ia configure

# Upload all zines
bash ia_contributions/batch_scripts/upload_all_zines.sh

# Upload single zine
bash ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue3-1976.sh
```

### Database Maintenance
```bash
# Update schema (already done, but repeatable)
python update_database_schema.py

# Clean false positives
python cleanup_database.py
```

---

## 📊 Current Stats (November 1, 2025)

```
Total Zines:              3,565
Cover Images:             3,987
IA Attribution Links:     3,542+
Contribution Ready:       23
Time Period:              1976-2019 (43 years)
Countries:                20+
Database Version:         2.1
```

---

## 📁 Key Files

### Database
- `punk_zines_database.json` - Main database (3,565 entries)
- `punk_zines_database.csv` - CSV export

### Tools
- `archive_scraper.py` - Scrape FROM IA (enhanced v2.0)
- `ia_contributor.py` - Contribute TO IA (new!)
- `batch_scraper.py` - Batch processing
- `cleanup_database.py` - Quality control
- `external_sources_scraper.py` - Harvest from non-IA pages (Flickr/generic)
- `tools/generate_data_js.py` - Build `viewer/data.js` for offline viewer
- `tools/flickr_api_harvester.py` - Harvest from Flickr via API (search/group)

### Contribution Packages
- `ia_contributions/contribution_manifest.json` - All packages
- `ia_contributions/batch_scripts/upload_all_zines.sh` - Master upload
- `ia_contributions/batch_scripts/upload_*.sh` - Individual uploads (23)

---

## 📖 Documentation

### Start Here
- `README.md` - Project overview
- `BIDIRECTIONAL_WORKFLOW.md` - Complete v2.0 guide (34 pages)
- `QUICK_REFERENCE.md` - This file

### Guides
- `SCRAPER_GUIDE.md` - How to use the scraper
- `INTERNET_ARCHIVE_GUIDE.md` - IA upload procedures
- `ADD_MORE_ZINES.md` - Manual additions

### Reports
- `PROJECT_STATUS_V2.md` - Current status (comprehensive)
- `BIDIRECTIONAL_UPDATE_SUMMARY.md` - What changed in v2.0
- `MEGA_EXPANSION_REPORT.md` - Expansion achievements

---

## 🔄 The Bidirectional Workflow

```
1. SCRAPE FROM IA
   python archive_scraper.py --search "your query"
   ↓
2. CHECK SOURCES
   python ia_contributor.py --stats
   ↓
3. PREPARE TO CONTRIBUTE
   python ia_contributor.py --prepare
   ↓
4. UPLOAD TO IA
   ia configure
   bash ia_contributions/batch_scripts/upload_all_zines.sh
   ↓
5. EXPAND THE COMMONS!
```

---

## 🖼️ Static Viewer (Offline)

```bash
# Generate viewer/data.js from the JSON database
python tools/generate_data_js.py

# Open the viewer (macOS)
open viewer/index.html
```

---

## 🌐 External Sources (non‑IA)

```bash
# Harvest from a Flickr album page (records URLs + attribution)
python external_sources_scraper.py flickr_album "<flickr_album_url>"

# Harvest from a generic HTML page with images
python external_sources_scraper.py generic_page "<page_url>"

# Optional: also download images locally
python external_sources_scraper.py flickr_album "<album_url>" --download

# Flickr API (recommended for groups/search)
export FLICKR_API_KEY=<your_api_key>

# Search Flickr for zine covers
python tools/flickr_api_harvester.py search --text "punk zine" --pages 3 --per-page 200 --download

# Harvest a group pool (use URL or known group_id)
python tools/flickr_api_harvester.py group --url "https://www.flickr.com/groups/punkfanzines/pool/" --pages 5 --per-page 200 --download

# IIIF Manifests (Pratt, Barnard, etc.)
# Single manifest
python tools/iiif_harvester.py --manifest "<iiif_manifest_url>" --download

# Text file of manifests (see iiif_seeds.txt)
python tools/iiif_harvester.py --file iiif_seeds.txt --download

# IIIF Collection: pull first N manifests
python tools/iiif_harvester.py --collection "<iiif_collection_url>" --max-items 200 --download
```

Tip: After large imports, run `python cleanup_database.py`.

## 🎯 Source Types

| Type | Count | % | Example |
|------|-------|---|---------|
| internet_archive | 3,542+ | 99.4% | Most entries |
| local_collection | 21 | 0.6% | Physical zines |
| other_archive | 2 | 0.1% | eBay refs |
| flickr | <1% | <0.1% | Photo collections |
| institutional_archive | <1% | <0.1% | Museums |

---

## 📦 Ready to Contribute (23 Zines)

### First Wave Punk
- 5× Sniffin' Glue (1976-1977)
- 1× Punk Magazine (1976)
- Slash, Search & Destroy, Ripped & Torn

### Riot Grrrl
- 2× Bikini Kill (1991)
- Jigsaw, Girl Germs

### Hardcore
- 2× Maximum Rocknroll (1984, 2019)
- We Got Power, Suburban Voice, Jet Lag

### UK Scene
- 48 Thrills, Chainsaw, Kill Your Pet Puppy

---

## 💡 Tips

### Best Practices
1. Always run cleanup after bulk scraping
2. Back up database before major changes
3. Use rate limiting (built into scraper)
4. Review metadata before uploading to IA
5. Check for duplicates on IA first

### Common Tasks

**Add new zines from IA:**
```bash
python archive_scraper.py --search "your zine name"
```

**Check what's ready to contribute:**
```bash
python ia_contributor.py --stats
```

**Prepare new contributions:**
```bash
python ia_contributor.py --prepare
```

**View a sample database entry:**
```bash
cat punk_zines_database.json | jq '.zines[0]' | head -30
```

---

## 🆘 Troubleshooting

### Error: "internetarchive library not installed"
```bash
pip install internetarchive
```

### Error: "IA not configured"
```bash
ia configure
# Enter your archive.org email and password
```

### Error: "Duplicate identifier"
Change the zine name slightly or add more specific info

### Database looks corrupted
Check `backups/` folder for recent backup:
```bash
ls -lh backups/
```

---

## 📞 Quick Links

### Documentation
- [Complete Workflow Guide](BIDIRECTIONAL_WORKFLOW.md)
- [Project Status](PROJECT_STATUS_V2.md)
- [Scraper Guide](SCRAPER_GUIDE.md)

### External Resources
- [Internet Archive Zines](https://archive.org/details/zines)
- [Maximum Rocknroll Archive](https://archive.org/details/maximumrnr)
- [Punk Planet Archive](https://archive.org/details/punkplanet)

---

## 🎸 Remember

> "These zines were created to be shared, copied, and distributed."

**We scrape FROM the commons and contribute BACK to the commons.**

This is punk rock archiving: DIY, collaborative, and free for all. 🤘

---

*Last updated: November 1, 2025*
*Version: 2.1*
