# Complete Guide to Using IIIF for Punk Zines

## What is IIIF?

**IIIF** (International Image Interoperability Framework) is a set of standards for delivering high-quality, high-resolution images on the web. Think of it as a way to access museum/library-quality scans with zoom, pan, and metadata.

### Why IIIF is Perfect for Your Project

- ✅ **Highest resolution** - Museum-quality scans (often 3000-6000px+)
- ✅ **Standardized** - Works the same across all institutions
- ✅ **Rich metadata** - Title, date, creator, license info
- ✅ **Zoom/pan built-in** - Deep zoom capabilities
- ✅ **Free access** - Most institutions provide free access
- ✅ **Legal** - Proper attribution and licensing

---

## How IIIF Works

### The IIIF Manifest

A **manifest** is a JSON file that describes a digital object (like a zine). It contains:
- Links to high-resolution images
- Metadata (title, creator, date, description)
- Viewing instructions
- License information

**Example manifest URL:**
```
https://digital.library.example.edu/iiif/zine-collection/item-123/manifest.json
```

### What You Can Get

From a single manifest, you can:
1. Download cover images at any resolution
2. Extract all metadata
3. Get proper attribution text
4. Link to the original source

---

## Step 1: Finding IIIF Manifests

### Method 1: Search Digital Collections

Many universities have IIIF-enabled digital collections:

**Barnard College**
- Digital Collections: https://digitalcollections.barnard.edu/
- Look for zine items
- Check page source for manifest URLs

**How to find manifests:**
1. Visit the digital collection
2. Search for "zine" or "fanzine"
3. Open an item page
4. Use our tool to find the manifest

```bash
python tools/find_iiif.py "https://digitalcollections.barnard.edu/item/12345"
```

### Method 2: Contact Institutions Directly

**Best institutions for punk zines:**

1. **Barnard Zine Library**
   - Email: archives@barnard.edu or zines@barnard.edu
   - Ask: "Do you have IIIF manifests for your zine collection?"
   - Mention: Non-commercial research project

2. **Pratt Institute Libraries**
   - Contact via their LibGuides
   - https://libguides.pratt.edu/zines

3. **UCLA Library Special Collections**
   - Punk Zines and Ephemera Collection
   - Contact through their finding aid

4. **University of Maryland**
   - DC Punk Archive
   - archives@umd.edu

**Email template:**
```
Subject: IIIF Manifest Access for Punk Zine Research

Hello,

I'm working on a non-commercial research project archiving punk
zines and fanzines. I noticed your institution has [mention specific
collection]. Do you provide IIIF manifests for your zine collection?

If so, I would appreciate:
- A collection manifest URL, or
- Individual manifest URLs for punk/music zines

This is for educational research and all materials will be properly
attributed according to your license requirements.

Thank you!
```

### Method 3: Browse Known IIIF Collections

**Museums with IIIF (may have zine-related content):**
- Harvard Art Museums: https://iiif.harvard.edu/
- Smithsonian: Search their IIIF collections
- V&A Museum: https://www.vam.ac.uk/

**How to explore:**
1. Visit their IIIF collection page
2. Search for "zine", "fanzine", "punk", "music"
3. Copy manifest URLs

---

## Step 2: Using Your IIIF Tools

You already have two powerful tools ready to use!

### Tool 1: find_iiif.py - Discover Manifests

**What it does:** Scans a webpage and finds IIIF manifest URLs

**When to use:** When you find a digital collection item page

**Usage:**
```bash
# Find manifests on a page
python tools/find_iiif.py "https://digitalcollections.example.edu/item/123"

# Output will show all manifest URLs found:
# Found manifest candidates:
# https://digitalcollections.example.edu/iiif/item-123/manifest.json
```

**How it works:**
- Looks for URLs containing "manifest" and "iiif"
- Parses JSON-LD blocks
- Checks Universal Viewer data attributes
- Returns all candidates

### Tool 2: iiif_harvester.py - Download from Manifests

**What it does:** Downloads images and metadata from IIIF manifests

**When to use:** Once you have manifest URLs

**Usage:**

#### Single Manifest
```bash
python tools/iiif_harvester.py \
  --manifest "https://example.edu/iiif/zine-123/manifest.json" \
  --download
```

#### Multiple Manifests (from file)
```bash
# 1. Add manifests to iiif_seeds.txt (one per line)
echo "https://example.edu/iiif/zine-123/manifest.json" >> iiif_seeds.txt
echo "https://example.edu/iiif/zine-456/manifest.json" >> iiif_seeds.txt

# 2. Run harvester
python tools/iiif_harvester.py --file iiif_seeds.txt --download
```

#### Entire IIIF Collection
```bash
python tools/iiif_harvester.py \
  --collection "https://example.edu/iiif/punk-zines/collection.json" \
  --max-items 200 \
  --download
```

**What happens:**
1. Fetches the manifest (v2 or v3 compatible)
2. Extracts metadata (title, year, description, license)
3. Downloads cover image to `images/iiif/`
4. Adds entry to your database
5. Skips duplicates automatically

---

## Step 3: Practical Examples

### Example 1: Barnard Digital Collections

**Scenario:** You found a punk zine on Barnard's website

```bash
# 1. Find the manifest
python tools/find_iiif.py "https://digitalcollections.barnard.edu/item/zine-riot-grrrl-1991"

# Output: https://digitalcollections.barnard.edu/iiif/ark:/12345/abcde/manifest

# 2. Download it
python tools/iiif_harvester.py \
  --manifest "https://digitalcollections.barnard.edu/iiif/ark:/12345/abcde/manifest" \
  --download

# 3. Check result
ls images/iiif/
# riot_grrrl_zine_1991_1234567890.jpg
```

### Example 2: Bulk Harvest from University

**Scenario:** Barnard gave you a collection manifest

```bash
# Harvest first 100 items from collection
python tools/iiif_harvester.py \
  --collection "https://digitalcollections.barnard.edu/iiif/zines/collection" \
  --max-items 100 \
  --download

# Tool will:
# - Find all manifests in the collection
# - Download up to 100 items
# - Add each to your database
# - Save images to images/iiif/
```

### Example 3: Building a Manifest List

**Scenario:** You're manually collecting manifests

```bash
# 1. Create/edit iiif_seeds.txt
cat > iiif_seeds.txt << 'EOF'
# Barnard Riot Grrrl Collection
https://digitalcollections.barnard.edu/iiif/ark:/12345/bikini-kill-1/manifest
https://digitalcollections.barnard.edu/iiif/ark:/12345/bikini-kill-2/manifest
https://digitalcollections.barnard.edu/iiif/ark:/12345/jigsaw-zine/manifest

# Pratt Punk Collection
https://digitalcollections.pratt.edu/iiif/punk-zine-001/manifest
https://digitalcollections.pratt.edu/iiif/punk-zine-002/manifest
EOF

# 2. Harvest all at once
python tools/iiif_harvester.py --file iiif_seeds.txt --download
```

---

## Step 4: Understanding the Output

### Database Entry Created

When you harvest a IIIF manifest, this gets added to your database:

```json
{
  "id": "RG001",
  "zine_name": "Bikini Kill #2",
  "issue_number": "2",
  "year": "1991",
  "location": null,
  "image_url": "images/iiif/bikini_kill_2_1234567890.jpg",
  "archive_source": "https://digitalcollections.barnard.edu/item/bikini-kill-2",
  "description": "Second issue of influential riot grrrl zine from Olympia, WA",
  "tags": ["punk", "zine"],
  "source_type": "iiif",
  "attribution": "Imported via IIIF manifest",
  "license": "CC-BY-SA"
}
```

### Images Saved

```
images/iiif/
  ├── bikini_kill_2_1234567890.jpg
  ├── jigsaw_zine_1234567891.jpg
  └── sniffin_glue_1234567892.jpg
```

---

## Step 5: Common IIIF Patterns

### Pattern 1: Manifest URL from Item Page

Most institutions use predictable patterns:

**Item page:**
```
https://digital.library.example.edu/item/12345
```

**Manifest URL (common patterns):**
```
https://digital.library.example.edu/iiif/item/12345/manifest
https://digital.library.example.edu/iiif/manifest/12345
https://digital.library.example.edu/iiif/12345/manifest.json
```

**Try these variations if find_iiif.py doesn't find it!**

### Pattern 2: Collection Hierarchy

Collections often have nested structures:

```
Collection: All Zines
  ├── Subcollection: Riot Grrrl
  │   ├── Manifest: Bikini Kill #1
  │   ├── Manifest: Bikini Kill #2
  │   └── Manifest: Jigsaw
  └── Subcollection: First Wave Punk
      ├── Manifest: Sniffin' Glue #1
      └── Manifest: Punk Magazine
```

**Start with the top-level collection URL for bulk harvesting!**

---

## Step 6: Institutions to Target

### High Priority (Likely to Have IIIF)

**1. Barnard College** ⭐
- Reason: Modern digital collections platform
- Collection: Women/feminist zines (riot grrrl!)
- Contact: archives@barnard.edu, zines@barnard.edu
- URL: https://digitalcollections.barnard.edu/

**2. UCLA Library** ⭐
- Reason: Large punk zines collection
- Collection: California punk scene 1977-2018
- Finding Aid: https://oac.cdlib.org/findaid/ark:/13030/c8542t4x/

**3. University of Maryland** ⭐
- Reason: DC Punk Archive with digital access
- Collection: DC punk scene, Ian MacKaye collection
- URL: https://digdc.dclibrary.org/

### Medium Priority (May Have IIIF)

**4. Pratt Institute**
- Digital collections: Check their website
- Known to have punk zine materials

**5. Harvard Art Museums**
- Known IIIF infrastructure: https://iiif.harvard.edu/
- May have zine/ephemera collections

**6. Smithsonian**
- IIIF enabled: Yes
- Check American History museum collections

### Lower Priority (Worth Exploring)

- University of Virginia
- University of San Francisco (Gleeson Zine Library)
- Library of Congress (American Folklife Center)

---

## Step 7: Testing & Troubleshooting

### Test with a Known IIIF Source

**Harvard Art Museums** provides public IIIF manifests:

```bash
# Test your tools with Harvard's IIIF
python tools/find_iiif.py "https://harvardartmuseums.org/collections/object/299843"

# Try harvesting a test item
python tools/iiif_harvester.py \
  --manifest "https://iiif.harvardartmuseums.org/manifests/object/299843" \
  --download
```

### Common Issues

**Issue: "No manifest found"**
- Try manual URL patterns
- Check page source for hidden manifest links
- Contact institution directly

**Issue: "403 Forbidden"**
- Manifest may require authentication
- Contact institution for access
- Some require institutional login

**Issue: "No images in manifest"**
- Manifest may be metadata-only
- Check if they have separate image API
- Ask institution for image access

---

## Step 8: Best Practices

### 1. Start Small
```bash
# Test with 1-2 manifests first
python tools/iiif_harvester.py \
  --manifest "URL" \
  --download
```

### 2. Build Your List Gradually
```bash
# Add to iiif_seeds.txt as you find them
echo "manifest-url" >> iiif_seeds.txt
```

### 3. Respect Rate Limits
- The tool already has 1-second delays
- For large collections, run overnight
- Be a good API citizen!

### 4. Document Sources
Keep track of where manifests came from:
```bash
# Good practice in iiif_seeds.txt:
# Barnard Riot Grrrl Collection - Contact: archives@barnard.edu
https://digitalcollections.barnard.edu/iiif/manifest1

# UCLA Punk Collection - Contact: special@library.ucla.edu
https://digital.library.ucla.edu/iiif/manifest2
```

---

## Step 9: Immediate Action Plan

### Week 1: Contact Institutions

**Email template ready!** Send to:
- [ ] Barnard (archives@barnard.edu)
- [ ] UCLA Special Collections
- [ ] University of Maryland Archives
- [ ] Pratt Institute Libraries

### Week 2: Manual Discovery

While waiting for responses:
```bash
# Try find_iiif.py on known digital collections
python tools/find_iiif.py "https://digitalcollections.barnard.edu/"
python tools/find_iiif.py "https://digdc.dclibrary.org/"
```

### Week 3: Test Harvesting

Once you have 5-10 manifests:
```bash
# Add to iiif_seeds.txt
# Run harvester
python tools/iiif_harvester.py --file iiif_seeds.txt --download

# Check results
ls images/iiif/
jq '.zines[-10:] | .[] | select(.source_type=="iiif")' punk_zines_database.json
```

### Week 4: Scale Up

If successful:
- Request collection-level manifests
- Run bulk harvests
- Document and share findings

---

## Resources & Reference

### IIIF Documentation
- Spec: https://iiif.io/api/presentation/
- Examples: https://iiif.io/guides/finding_resources/
- Viewers: https://iiif.io/apps-demos/

### Your Tools
- `tools/find_iiif.py` - Find manifests on web pages
- `tools/iiif_harvester.py` - Download from manifests
- `iiif_seeds.txt` - Your manifest URL list

### Commands Cheat Sheet
```bash
# Find manifest
python tools/find_iiif.py "<page-url>"

# Single manifest
python tools/iiif_harvester.py --manifest "<manifest-url>" --download

# From file
python tools/iiif_harvester.py --file iiif_seeds.txt --download

# Collection
python tools/iiif_harvester.py --collection "<collection-url>" --max-items 100 --download
```

---

## What Makes IIIF Special

Compared to other sources:

| Feature | Internet Archive | Wikimedia Commons | IIIF |
|---------|-----------------|-------------------|------|
| Resolution | 3000px (BookReader) | Varies | Up to 6000px+ |
| Metadata | Good | Good | Excellent |
| Zoom Support | Yes | No | Built-in |
| Standard Format | No | No | Yes |
| Institution Quality | Archive | Community | Museum |
| Ease of Access | Easy (API) | Easy (API) | Medium (need manifests) |

**IIIF is worth the extra effort for the highest quality results!**

---

## Success Metrics

You'll know IIIF is working when:
- ✅ You get 3000px+ resolution images
- ✅ Metadata is complete and accurate
- ✅ Images have proper institutional attribution
- ✅ License information is clear
- ✅ You can zoom deeply in the viewer

---

## Next Steps

1. **Right now**: Email Barnard, UCLA, UMD
2. **This week**: Browse their digital collections
3. **When you get responses**: Add manifests to iiif_seeds.txt
4. **Then**: Run harvester and watch high-quality zines pour in!

Good luck! IIIF will give you the highest quality zine scans available. 🎸

---

**Created:** November 1, 2025
**Tools Ready:** ✅ find_iiif.py, iiif_harvester.py
**Status:** Ready to harvest - just need manifest URLs!
