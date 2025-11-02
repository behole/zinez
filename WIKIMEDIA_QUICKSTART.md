# Wikimedia Commons Scraper - Quick Start

## ✅ What You Get

- **NO API key needed** - Works immediately!
- **All Creative Commons licensed** - Legally free to use
- **High quality images** - Often better than other sources
- **Automatic filtering** - Only downloads punk/zine related content
- **Full metadata** - License, creator, description all tracked

## 🚀 Usage

### Basic Commands

```bash
# Scrape single category
python wikimedia_scraper.py --category "Fanzines" --download

# Scrape multiple categories
python wikimedia_scraper.py --categories "Fanzines,Punk,Punk_rock" --download

# Scrape without downloading (just link to Wikimedia)
python wikimedia_scraper.py --category "Punk" --no-download

# Limit results per category
python wikimedia_scraper.py --category "Fanzines" --limit 100 --download
```

### Recommended Categories

**Best for punk zines:**
- `Fanzines` - Main fanzine category
- `Punk` - General punk culture
- `Punk_rock` - Music focused
- `Anarcho-punk` - Political punk content

**Also worth checking:**
- `Magazine_covers` - Some punk magazines
- `Music_magazines` - Broader music coverage
- `1970s_in_music` - Early punk era
- `1980s_in_music` - Hardcore era

## 📊 What It Does

1. **Fetches** images from Wikimedia Commons categories
2. **Filters** for punk/zine related content (keywords: punk, zine, fanzine, hardcore, riot grrrl, etc.)
3. **Downloads** images to `images/wikimedia/`
4. **Extracts** metadata (title, description, license, creator, year)
5. **Adds** to database with proper attribution
6. **Skips** duplicates automatically

## 🎯 Current Run

**Running now:**
```bash
python wikimedia_scraper.py --categories "Fanzines,Punk,Punk_rock" --download
```

This will scrape all three categories and add punk-related images to your database!

## 📁 Output

**Images saved to:**
```
images/wikimedia/
```

**Database entries include:**
- `source_type`: "wikimedia_commons"
- `license`: CC-BY-SA, CC0, etc.
- `attribution`: Full Wikimedia Commons URL
- `archive_source`: Link to original page

## 💡 Tips

1. **Be patient** - Scraper waits 1 second between images (Wikimedia rate limiting)
2. **Check results** - It filters for punk content, but may need manual review
3. **Run multiple times** - Safe to re-run, it skips duplicates
4. **Browse first** - Visit https://commons.wikimedia.org/wiki/Category:Fanzines to see what's available

## 🔗 Manual Browsing

If you want to browse visually first:
1. Visit: https://commons.wikimedia.org/wiki/Category:Fanzines
2. Click images to see full resolution
3. Download manually if you prefer

Then run scraper on specific categories that look good!

## 📈 What to Expect

Typical results per category:
- **Fanzines**: 10-50 punk-related images
- **Punk**: 20-100 general punk images
- **Punk_rock**: 10-30 music-focused images

Not all will be zine covers, so manual filtering may help!

---

**Created:** November 1, 2025
**No API key required!** 🎸
