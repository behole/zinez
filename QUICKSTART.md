# Quick Start Guide - Punk Zine Scraper

## 🚀 Get Started in 60 Seconds

### 1. Install Required Library
```bash
pip install internetarchive
```

### 2. Run Your First Search
```bash
# Search for a specific zine
python archive_scraper.py --search "Maximum Rocknroll"
```

### 3. Check Your Results
```bash
# View downloaded images
ls images/

# Check how many zines you now have
grep -c "\"id\":" punk_zines_database.json
```

## 🎯 Common Tasks

### Search for Specific Zines
```bash
# By zine name
python archive_scraper.py --search "Flipside"
python archive_scraper.py --search "Sniffin Glue"

# By movement
python archive_scraper.py --search "riot grrrl"
python archive_scraper.py --search "anarcho punk"

# By location
python archive_scraper.py --search "UK punk 1977"
python archive_scraper.py --search "San Francisco hardcore"
```

### Run Batch Searches

```bash
# List all configured searches
python batch_scraper.py --list

# Run a specific priority search
python batch_scraper.py --search "Riot Grrrl Zines"

# Run ALL priority searches (takes 15-30 minutes)
python batch_scraper.py
```

## 📊 What You'll Get

After running `python batch_scraper.py`:
- ✅ 200-350 new zine entries
- ✅ Cover images auto-downloaded
- ✅ Metadata extracted (year, location, creators, tags)
- ✅ Database automatically updated
- ✅ No duplicates (smart checking)

## 🎨 Priority Search Targets

Pre-configured in `scraper_config.json`:

| Search | Expected Zines | Focus |
|--------|---------------|-------|
| Maximum Rocknroll Collection | 100 | SF hardcore, interviews |
| Punk Planet Archive | 50 | 90s-2000s indie/punk |
| Riot Grrrl Zines | 50 | Feminist punk movement |
| UK First Wave Punk | 30 | 1976-78 originals |
| US Hardcore Zines | 40 | 80s hardcore scene |
| Anarcho Punk | 30 | Political punk |
| Queercore/Homocore | 25 | LGBTQ+ punk |
| International | 30 | Japan, Germany, Brazil, etc. |
| Regional US | 30 | Boston, Detroit, Chicago, etc. |
| Personal Zines | 20 | Cometbus, underground |

## ⚡ Quick Commands Reference

```bash
# SEARCH
python archive_scraper.py --search "query"        # Single search
python archive_scraper.py --help                  # Show help

# BATCH
python batch_scraper.py                           # Run all searches
python batch_scraper.py --list                    # List searches
python batch_scraper.py --search "search name"    # Run one search
python batch_scraper.py --help                    # Show help

# VERIFY
ls images/                                        # Check images
head -30 punk_zines_database.json                # Check database
tail -50 punk_zines_database.json                # See newest entries
```

## 🔧 Customize Searches

Edit `scraper_config.json` to add your own searches:

```json
{
  "name": "Your Search Name",
  "query": "your search terms",
  "max_results": 30,
  "enabled": true
}
```

Search tips:
- Use `AND` for all terms: `punk AND hardcore AND 1983`
- Use `OR` for any term: `flipside OR maximum rocknroll`
- Use `()` to group: `(london OR manchester) AND punk 1977`

## 📚 Learn More

- **Full Documentation:** [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md)
- **Database Info:** [README.md](README.md)
- **Manual Additions:** [ADD_MORE_ZINES.md](ADD_MORE_ZINES.md)
- **Zine History:** [PUNK_ZINES_MASTER_LIST.md](PUNK_ZINES_MASTER_LIST.md)

## 🎸 Example Session

```bash
# Day 1: Test the scraper
pip install internetarchive
python archive_scraper.py --search "Maximum Rocknroll"
# Result: 17 new zines, ~45 seconds

# Day 2: Run priority searches
python batch_scraper.py
# Result: 200+ new zines, ~20 minutes
# Now you have 250+ zines total!

# Check your collection
ls images/ | wc -l        # Count images
# Review in browser
open zine_archive_viewer.html
```

## ⚠️ Important Notes

1. **Rate Limiting:** Built-in delays respect Internet Archive servers
2. **Duplicates:** Automatically skipped - safe to run multiple times
3. **Storage:** ~5-10MB per 100 zines (thumbnails)
4. **Time:** ~2-3 zines per minute average
5. **Quality:** Some results may not be actual zines (e.g., podcasts, videos)

## 🤝 Need Help?

- Check the console output for errors
- Read [SCRAPER_GUIDE.md](SCRAPER_GUIDE.md) for troubleshooting
- Verify library installed: `pip list | grep internetarchive`
- Test with a simple search first before batch runs

---

**Ready?** Start with:
```bash
python archive_scraper.py --search "punk zine"
```

🎸 Happy scraping! 🎸
