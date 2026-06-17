# Open Issues

## Active

### Lightbox: old image lingers when switching zines
When clicking a new zine while the lightbox is open, the previous image
remains visible for several seconds before the new one loads. The
shimmer animation shows but the old decoded frame persists in the
browser compositor.

Attempted fixes (not working):
- `removeAttribute("src")` — GPU doesn't evict texture
- Transparent data URL + double-RAF — progressive breakage, lightbox stops opening

Current approach: `display:none` on img during load. Under test.

### Lightbox: progressive breakage
After several open/close cycles, the lightbox stops opening entirely.
Likely caused by accumulating RAF callbacks or event listeners.

## Backlog

### High-res image swap causes visual flicker
When the high-res IA page image finishes preloading, the thumb dims
and shimmer re-appears during the swap. Should crossfade instead.

### No touch zoom (pinch)
Lightbox supports single-finger pan but not two-finger pinch-to-zoom.

### Keyboard arrow navigation in lightbox
Arrow keys work but aren't documented. Could show tip in footer.

### Grid images for non-IA entries
~240 entries have external image_url (Flickr, library archives) but
no ia_item_url. These may 404 in production since the URLs are often
page URLs, not direct image URLs.

### D1 ia_thumb column never populated
The import script computes ia_thumb from ia_item_url, but the database
was never re-imported after the column was added. All rows have empty
string. Worked around in frontend with getThumbUrl().
