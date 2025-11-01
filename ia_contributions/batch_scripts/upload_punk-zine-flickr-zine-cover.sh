#!/bin/bash
# Upload script for Internet Archive
# Zine: Flickr zine cover
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-flickr-zine-cover
ia upload \
  "punk-zine-flickr-zine-cover" \
  --metadata="title:Flickr zine cover" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Imported from external source; needs curation

Punk zine from None

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:punk; zine" \
  --metadata="creator:None" \
  --metadata="date:None" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-flickr-zine-cover"