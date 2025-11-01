#!/bin/bash
# Upload script for Internet Archive
# Zine: Sideburns
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-sideburns-issue1-1977
ia upload \
  "punk-zine-sideburns-issue1-1977" \
  --metadata="title:Sideburns" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Featured famous 'three chords' drawing

Punk zine from UK
Published: 1977

Featured bands: Various

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:punk; UK; DIY; iconic; three chords" \
  --metadata="creator:Tony Moon" \
  --metadata="date:1977" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:UK" \
  --metadata="volume:1"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-sideburns-issue1-1977"