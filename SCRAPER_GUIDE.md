# Internet Archive Punk Zine Scraper
## Automated Collection Expansion Tool

Created: October 28, 2025

---

## 🎯 Overview

This scraper automatically searches the Internet Archive for punk zines, downloads cover images, extracts metadata, and adds entries to the punk zines database. It's designed to rapidly expand the collection while maintaining data quality.

## 📁 Files

- **archive_scraper.py** - Core scraper with search and download functionality
- **batch_scraper.py** - Batch processor for multiple configured searches
- **scraper_config.json** - Configuration file with priority searches
- **images/** - Downloaded cover images (auto-created)

## 🚀 Quick Start

### Installation

```bash
# Install required library
pip install internetarchive

# Make scripts executable
chmod +x archive_scraper.py batch_scraper.py
```

### Basic Usage

```bash
# Single search (quick test)
python archive_scraper.py --search "Maximum Rocknroll"

# Run all configured priority searches
python batch_scraper.py

# Run specific priority search
python batch_scraper.py --search "Riot Grrrl Zines"

# List all configured searches
python batch_scraper.py --list
```

## 🔍 How It Works

### Archive Scraper (archive_scraper.py)

**Core Features:**
1. Searches Internet Archive using the `internetarchive` Python library
2. Queries multiple collections (zines, misczinespunk, punkplanet, etc.)
3. Extracts metadata (title, year, creator, location, tags)
4. Downloads cover images as JPG thumbnails
5. Generates unique IDs for each zine
6. Updates punk_zines_database.json automatically
7. Avoids duplicates by checking existing entries

**Search Examples:**
```bash
# Specific zine
python archive_scraper.py --search "Flipside fanzine"

# Movement
python archive_scraper.py --search "riot grrrl"

# Time period
python archive_scraper.py --search "punk 1976 1977 UK"

# Band
python archive_scraper.py --search "Black Flag Maximum Rocknroll"

# Multiple keywords
python archive_scraper.py --search "hardcore Boston 1980s"
```

### Batch Scraper (batch_scraper.py)

Runs multiple searches from scraper_config.json in sequence.

**Priority Searches Included:**
1. Maximum Rocknroll Collection (100 results)
2. Punk Planet Archive (50 results)
3. Riot Grrrl Zines (50 results)
4. UK First Wave Punk (30 results)
5. US Hardcore Zines (40 results)
6. Anarcho Punk (30 results)
7. Queercore/Homocore (25 results)
8. International Punk Zines (30 results)
9. Regional US Scenes (30 results)
10. Cometbus & Personal Zines (20 results)

**Total Potential:** ~355 new zines per full run

**Commands:**
```bash
# Run all enabled searches
python batch_scraper.py

# Run single search by name
python batch_scraper.py --search "UK First Wave Punk"

# List available searches
python batch_scraper.py --list
```

## ⚙️ Configuration (scraper_config.json)

### Scraper Settings

```json
"scraper_settings": {
  "max_results_per_query": 30,      // Default max results
  "rate_limit_seconds": 2,           // Delay between searches
  "download_images": true,           // Auto-download covers
  "update_existing": false,          // Skip existing entries
  "skip_duplicates": true            // Avoid duplicates
}
```

### Adding Custom Searches

Edit `scraper_config.json` and add to `priority_searches`:

```json
{
  "name": "Your Search Name",
  "query": "search terms",
  "collection": "optional_collection_name",
  "max_results": 50,
  "enabled": true
}
```

**Search Query Syntax:**
- `AND` - All terms must match: `punk AND 1976 AND UK`
- `OR` - Any term matches: `flipside OR maximum rocknroll`
- `()` - Group terms: `(boston OR chicago) AND hardcore`
- `collection:` - Filter by collection: `punk AND collection:zines`

### Internet Archive Collections

Configured collections:
- **zines** - General zine collection (60,000+ items)
- **misczinespunk** - Punk-specific zines
- **punkplanet** - Punk Planet magazine archive
- **maximumrnr** - Maximum Rocknroll collection
- **riot_grrrl_collection** - Riot Grrrl materials

## 📊 Data Structure

Each scraped zine creates an entry with:

```json
{
  "id": "MRR001",
  "zine_name": "Maximum Rocknroll",
  "issue_number": "1",
  "year": "1982",
  "location": "San Francisco, CA",
  "image_url": "images/mrr001.jpg",
  "archive_source": "Internet Archive: maximumrnr",
  "description": "First issue of MRR...",
  "tags": ["punk", "hardcore", "DIY", "SF"],
  "bands_featured": [],
  "circulation": null,
  "creators": "Tim Yohannan",
  "ia_metadata": {
    "identifier": "maximumrnr_001",
    "mediatype": "texts",
    "downloads": 150
  }
}
```

## 🎨 ID Generation

The scraper auto-generates unique IDs:

**Format:** `PREFIX###`

**Prefix Logic:**
- 3-letter abbreviation from zine name
- Examples:
  - "Maximum Rocknroll" → MRR
  - "Bikini Kill" → BK
  - "Sniffin' Glue" → SG
  - "The Riot Grrrl Collection" → TRG

**Number:** Sequential starting from 001

## 🖼️ Image Handling

**Download Process:**
1. Attempts to fetch item thumbnail from Internet Archive
2. Falls back to first image file in item if thumbnail fails
3. Saves as `{id_lowercase}.jpg` in `images/` folder
4. Updates database with local path: `images/xyz001.jpg`

**Image Specs:**
- Format: JPG
- Typical size: 5-25KB (thumbnails)
- Fallback: Links to archive.org if download fails

## 🔧 Metadata Extraction

### Automatic Extraction

**Year:**
- Checks: `year`, `date`, `publicdate`, `addeddate` fields
- Extracts: 4-digit year (1975-2025)

**Location:**
- Searches description and subjects for city/country names
- Recognizes: Major punk cities (NYC, LA, SF, London, etc.)

**Tags:**
- Includes all relevant subjects from Internet Archive
- Adds keywords from description
- Filters: Keeps only punk-related tags

**Creators:**
- Extracts from `creator` field
- Handles multiple creators with semicolon separator

## 📈 Usage Tips

### Best Practices

1. **Start Small:**
   ```bash
   # Test with specific search first
   python archive_scraper.py --search "Flipside"
   ```

2. **Run Priority Searches:**
   ```bash
   # High-value targeted searches
   python batch_scraper.py
   ```

3. **Monitor Results:**
   - Check `punk_zines_database.json` for new entries
   - Verify images in `images/` folder
   - Review console output for errors

4. **Refine Searches:**
   - Adjust queries in `scraper_config.json`
   - Use boolean operators for precision
   - Test new queries individually first

### Rate Limiting

**Built-in Delays:**
- 1 second between individual items
- 2 seconds between searches (configurable)

**Be Respectful:**
- Internet Archive is a non-profit
- Don't run massive concurrent searches
- Use during off-peak hours for large batches

## 🐛 Troubleshooting

### Common Issues

**"internetarchive library not installed"**
```bash
pip install internetarchive
```

**"No new zines found"**
- Zines may already exist in database
- Try different search terms
- Check if collection exists on archive.org

**Image download failures**
- Some items may not have images
- Scraper will use archive.org link as fallback
- Check console for specific error messages

**Duplicate entries**
- Scraper checks existing IDs automatically
- Uses archive source to detect duplicates
- Safe to run multiple times

## 📋 Recommended Search Strategy

### Phase 1: Major Archives (High Yield)
```bash
python batch_scraper.py --search "Maximum Rocknroll Collection"
python batch_scraper.py --search "Punk Planet Archive"
```

### Phase 2: Movements (Quality)
```bash
python batch_scraper.py --search "Riot Grrrl Zines"
python batch_scraper.py --search "Anarcho Punk"
python batch_scraper.py --search "Queercore/Homocore"
```

### Phase 3: Regional Scenes (Depth)
```bash
python batch_scraper.py --search "UK First Wave Punk"
python batch_scraper.py --search "US Hardcore Zines"
python batch_scraper.py --search "Regional US Scenes"
```

### Phase 4: International (Breadth)
```bash
python batch_scraper.py --search "International Punk Zines"
```

### Phase 5: Personal/Underground (Rare)
```bash
python batch_scraper.py --search "Cometbus & Personal Zines"
```

## 🎯 Custom Search Ideas

Add these to `scraper_config.json`:

**By Band:**
```json
{
  "name": "Dead Kennedys Coverage",
  "query": "dead kennedys AND (zine OR fanzine)",
  "max_results": 20
}
```

**By Label:**
```json
{
  "name": "Dischord Records",
  "query": "dischord AND (punk OR hardcore)",
  "max_results": 25
}
```

**By City:**
```json
{
  "name": "Detroit Punk",
  "query": "detroit AND (punk zine OR hardcore fanzine)",
  "max_results": 20
}
```

**By Year:**
```json
{
  "name": "1977 First Wave",
  "query": "punk fanzine AND 1977",
  "max_results": 30
}
```

## 📊 Expected Results

### Performance Metrics (Initial Tests)

**Single Search ("Maximum Rocknroll 1982"):**
- Runtime: ~45 seconds
- Results: 17 new zines
- Images: 17 downloaded
- Success rate: 100%

**Full Batch Run (10 priority searches):**
- Estimated runtime: 15-30 minutes
- Expected results: 200-350 new zines
- Storage: ~5-10 MB images

## 🔄 Maintenance

### Regular Tasks

1. **Weekly:** Run priority searches to catch new uploads
   ```bash
   python batch_scraper.py
   ```

2. **Monthly:** Review and refine search queries
   - Check `scraper_config.json`
   - Add new priority searches
   - Disable completed searches

3. **As Needed:** Manual specific searches
   ```bash
   python archive_scraper.py --search "specific zine name"
   ```

## 📝 Output Files

**Modified Files:**
- `punk_zines_database.json` - Updated with new entries
- `images/*.jpg` - Downloaded cover images

**Console Output:**
```
🔍 Searching: Maximum Rocknroll
📄 Found: Maximum Rocknroll 001 (1982)
  ✅ Downloaded image: mrr001.jpg
✅ Database saved: 52 entries
✅ Added 17 new zines
```

## 🤝 Contributing

To improve the scraper:

1. **Add Search Queries:** Edit `scraper_config.json`
2. **Enhance Extraction:** Modify `archive_scraper.py`
3. **Report Issues:** Document any problems/edge cases

## 📚 Resources

- [Internet Archive Search](https://archive.org/advancedsearch.php)
- [internetarchive Python Docs](https://internetarchive.readthedocs.io/)
- [Internet Archive Zines Collection](https://archive.org/details/zines)
- [Advanced Search Syntax](https://archive.org/help/aboutsearch.htm)

---

**Remember:** This tool is for research and preservation. Respect Internet Archive's resources and the original zine creators' work.

*"Copy and distribute freely" - The punk ethos*
