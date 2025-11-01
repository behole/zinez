# Bidirectional Internet Archive Workflow
## Two-Way Integration: Scraping FROM and Contributing TO Internet Archive

Created: October 29, 2025

---

## Overview

This project now has a **bidirectional workflow** with Internet Archive:

1. **📥 FROM Internet Archive**: Scrape punk zines, properly attribute sources, link back
2. **📤 TO Internet Archive**: Contribute non-IA zines back to expand the public archive

This establishes a sustainable cycle of preservation and sharing for punk zine culture.

---

## 📥 Part 1: Scraping FROM Internet Archive

### Enhanced Attribution System

All zines scraped from Internet Archive now include:

#### New Database Fields

```json
{
  "id": "MRR001",
  "zine_name": "Maximum Rocknroll",
  "source_type": "internet_archive",
  "ia_item_url": "https://archive.org/details/maximumrnr_001",
  "ia_download_url": "https://archive.org/download/maximumrnr_001",
  "attribution": "Sourced from Internet Archive (archive.org/details/maximumrnr_001)",
  "license": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
  "ia_metadata": {
    "identifier": "maximumrnr_001",
    "mediatype": "texts",
    "downloads": 1234,
    "collection": ["zines", "maximumrnr"]
  }
}
```

#### Source Types

The database now classifies all entries by source:

- **`internet_archive`** - Scraped from IA (97.6% of collection)
- **`local_collection`** - From physical collections or local files
- **`other_archive`** - From Flickr, institutional archives, etc.
- **`flickr`** - Specifically from Flickr collections
- **`institutional_archive`** - From museums, libraries, universities
- **`uncategorized`** - Needs manual classification

### Using the Enhanced Scraper

```bash
# Search with automatic attribution
python archive_scraper.py --search "riot grrrl"

# All new entries will include:
# - Direct IA item URLs
# - Attribution text
# - License information
# - Collection tracking
```

### Current Statistics

After schema update (October 29, 2025):

```
Total zines: 1,055
├─ From Internet Archive: 1,030 (97.6%)
├─ From local collections: 21 (2.0%)
├─ From other archives: 2 (0.2%)
├─ From Flickr: 1 (0.1%)
└─ From institutional archives: 1 (0.1%)

IA Attribution URLs added: 1,022
```

---

## 📤 Part 2: Contributing TO Internet Archive

### Identifying Contribution Candidates

The system automatically identifies zines that should be contributed:

```bash
# Show database statistics
python ia_contributor.py --stats

# Output:
# 📥 From Internet Archive: 1,030
# 📤 Contributed TO Internet Archive: 0
# 📦 From other sources: 25
```

### Preparing Contribution Packages

```bash
# Prepare all non-IA zines for upload
python ia_contributor.py --prepare
```

This creates:

1. **Individual upload scripts** for each zine
2. **Master batch script** to upload all
3. **Manifest file** tracking all packages
4. **Proper IA metadata** for each item

### Generated Files Structure

```
ia_contributions/
├── contribution_manifest.json
└── batch_scripts/
    ├── upload_all_zines.sh (master script)
    ├── upload_punk-zine-sniffin-glue-issue3-1976.sh
    ├── upload_punk-zine-bikini-kill-issue1-1991.sh
    └── ... (one script per zine)
```

### What Gets Created

#### 1. Individual Upload Script

Each zine gets a complete upload script:

```bash
#!/bin/bash
# Upload script for Internet Archive
# Zine: Sniffin' Glue

ia upload \
  "punk-zine-sniffin-glue-issue3-1976" \
  --metadata="title:Sniffin' Glue" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Issue 3 with interviews...
Contributed by the Punk Zines Research Project" \
  --metadata="subject:punk; DIY; UK; 1976" \
  --metadata="creator:Mark Perry, Danny Baker" \
  --metadata="date:1976" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/"

echo "View at: https://archive.org/details/punk-zine-sniffin-glue-issue3-1976"
```

#### 2. Master Upload Script

Uploads all zines sequentially with:
- Progress tracking
- Error handling
- Rate limiting (5 second delay between uploads)
- Summary statistics

#### 3. Contribution Manifest

JSON file tracking all prepared packages:

```json
{
  "created": "2025-10-29T09:36:26",
  "total_packages": 23,
  "packages": [
    {
      "zine_id": "SG003",
      "zine_name": "Sniffin' Glue",
      "ia_identifier": "punk-zine-sniffin-glue-issue3-1976",
      "status": "prepared",
      "upload_script": "ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue3-1976.sh"
    }
  ]
}
```

---

## 🔄 Complete Workflow

### Step-by-Step Process

#### Phase 1: Scraping FROM IA

1. **Search for zines**
   ```bash
   python archive_scraper.py --search "hardcore punk 1980s"
   ```

2. **Automatic processing**
   - Scraper finds items on IA
   - Downloads cover images locally
   - Extracts metadata
   - Creates database entries with full attribution
   - Adds direct IA URLs

3. **Result**: Entries in database with `source_type: "internet_archive"`

#### Phase 2: Adding From Other Sources

1. **Manual addition** (or from other archives)
   - Add entries to database from physical collections
   - Include local image files
   - Mark as `source_type: "local_collection"`

2. **Example entry**:
   ```json
   {
     "id": "SG003",
     "zine_name": "Sniffin' Glue",
     "issue_number": "3",
     "year": "1976",
     "image_url": "images/sg003.jpg",
     "archive_source": "Academic archive",
     "source_type": "local_collection"
   }
   ```

#### Phase 3: Contributing TO IA

1. **Prepare packages**
   ```bash
   python ia_contributor.py --prepare
   ```

2. **Review packages**
   - Check generated scripts in `ia_contributions/batch_scripts/`
   - Review metadata in `contribution_manifest.json`
   - Verify image files exist

3. **Configure IA CLI** (one-time setup)
   ```bash
   ia configure
   # Enter your IA email and password
   ```

4. **Upload to Internet Archive**

   Option A: Upload all at once
   ```bash
   bash ia_contributions/batch_scripts/upload_all_zines.sh
   ```

   Option B: Upload individually
   ```bash
   bash ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue3-1976.sh
   ```

5. **Track contributions**
   - Each upload creates a new item on IA
   - Items are viewable at: `https://archive.org/details/{identifier}`
   - Database can be updated with `mark_as_contributed()` function

---

## 📊 Current Collection Status

### By Source Type (Post-Schema Update)

| Source Type | Count | Percentage |
|-------------|-------|------------|
| Internet Archive | 1,030 | 97.6% |
| Local Collection | 21 | 2.0% |
| Other Archives | 2 | 0.2% |
| Flickr | 1 | 0.1% |
| Institutional | 1 | 0.1% |
| **Total** | **1,055** | **100%** |

### Contribution Candidates

**23 zines ready to contribute to IA**, including:

- **5 Sniffin' Glue issues** (1976-1977)
- **2 Bikini Kill issues** (1991)
- **2 Maximum Rocknroll issues** (1984, 2019)
- **1 Punk Magazine issue** (1976)
- **Historical zines**: Slash, Search & Destroy, Ripped & Torn, Sideburns
- **Riot Grrrl**: Jigsaw, Girl Germs
- **Regional**: We Got Power, Suburban Voice, Jet Lag
- **UK**: 48 Thrills, Chainsaw, Kill Your Pet Puppy

---

## 🛠️ Technical Details

### Database Schema v2.0

New fields added to all entries:

```
source_type         - Classification of where zine came from
ia_item_url         - Direct link to IA item page (if applicable)
ia_download_url     - Direct download link (if applicable)
attribution         - Attribution text for sourcing
license             - License URL (if known)
ia_metadata         - Enhanced with collection field
```

### IA Identifier Generation

Format: `punk-zine-{name}-issue{number}-{year}`

Examples:
- `punk-zine-sniffin-glue-issue3-1976`
- `punk-zine-maximum-rocknroll-issue1-1982`
- `punk-zine-bikini-kill-issue2-1991`

### Metadata Mapping

| Database Field | IA Metadata Field |
|----------------|-------------------|
| zine_name | title |
| description | description |
| tags | subject |
| creators | creator |
| year | date |
| location | coverage |
| issue_number | volume |

### License Policy

All contributions default to: **CC BY-NC-SA 4.0**
(Creative Commons Attribution-NonCommercial-ShareAlike)

This allows:
- ✅ Sharing and redistribution
- ✅ Adaptation and remixing
- ✅ Attribution required
- ❌ No commercial use
- ✅ Share-alike (derivatives must use same license)

---

## 🎯 Best Practices

### When Scraping FROM IA

1. **Always include attribution**
   - Use the auto-generated attribution text
   - Link back to original IA items
   - Respect existing licenses

2. **Download responsibly**
   - Use rate limiting (built into scraper)
   - Don't overwhelm IA servers
   - Cache images locally

3. **Verify metadata**
   - Check extracted year/location for accuracy
   - Review tags and subjects
   - Correct obvious errors

### When Contributing TO IA

1. **Verify you have rights**
   - Only upload if you have permission
   - Respect copyright (even for old zines)
   - Use appropriate Creative Commons license

2. **Provide good metadata**
   - Complete descriptions
   - Accurate dates and locations
   - Relevant tags and subjects

3. **Check for duplicates**
   - Search IA first to avoid duplicates
   - Our scraper checks automatically
   - When in doubt, don't upload

4. **Quality over quantity**
   - Better to upload fewer high-quality items
   - Include proper documentation
   - Scan at good resolution if possible

---

## 🚀 Future Enhancements

### Planned Features

1. **Automatic duplicate checking**
   - Query IA before upload to prevent duplicates
   - Cross-reference by title, year, issue

2. **Contribution tracking**
   - Update database after successful uploads
   - Mark as `contributed_to_ia`
   - Track IA identifiers in database

3. **Batch status monitoring**
   - Check upload status
   - Retry failed uploads
   - Generate success reports

4. **Enhanced metadata extraction**
   - OCR from cover images
   - Extract band names from descriptions
   - Infer tags from content

5. **Web interface**
   - Browse database by source
   - See contribution candidates
   - Generate upload scripts from UI

---

## 📚 Related Documentation

- **[SCRAPER_GUIDE.md](SCRAPER_GUIDE.md)** - How to use the scraper
- **[INTERNET_ARCHIVE_GUIDE.md](INTERNET_ARCHIVE_GUIDE.md)** - IA upload basics
- **[ADD_MORE_ZINES.md](ADD_MORE_ZINES.md)** - Manual addition guide
- **[PUNK_ZINES_MASTER_LIST.md](PUNK_ZINES_MASTER_LIST.md)** - Historical catalog

---

## 🤝 Contributing to the Project

This bidirectional workflow helps preserve punk culture by:

1. **Documenting**: Cataloging what's already on IA
2. **Expanding**: Adding new zines from other sources
3. **Sharing**: Contributing back to the public archive
4. **Attributing**: Properly crediting all sources

Together, we're creating a comprehensive, properly-sourced archive of punk zine culture!

---

## 📞 Support

### Common Issues

**Q: Can I upload without IA account?**
A: No, you need an Internet Archive account. Create one at https://archive.org/account/signup

**Q: What if the upload fails?**
A: Check the error message. Common issues:
- Not configured: Run `ia configure`
- Duplicate identifier: Change the name
- File not found: Check image path

**Q: How do I know what's already on IA?**
A: Run `python ia_contributor.py --stats` to see the breakdown

**Q: Can I edit metadata after upload?**
A: Yes, log into IA and edit the item page

---

## 🎸 Philosophy

> "Punk is musical freedom. It's saying, doing and playing what you want."
> — Kurt Cobain

These zines were created to be **shared, copied, and distributed**. By establishing a bidirectional workflow with Internet Archive, we honor that spirit while ensuring proper attribution and preservation.

**We scrape FROM the commons and contribute BACK to the commons.**

---

*Last updated: October 29, 2025*
*Database v2.0 with bidirectional IA integration*
