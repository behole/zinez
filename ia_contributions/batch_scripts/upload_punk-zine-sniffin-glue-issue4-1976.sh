#!/bin/bash
# Upload script for Internet Archive
# Zine: Sniffin' Glue
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-sniffin-glue-issue4-1976
ia upload \
  "punk-zine-sniffin-glue-issue4-1976" \
  --metadata="title:Sniffin' Glue" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:The Clash on the cover

Punk zine from London, UK
Published: 1976

Featured bands: The Clash

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:punk; The Clash; UK; 1976" \
  --metadata="creator:Mark Perry" \
  --metadata="date:1976" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:London, UK" \
  --metadata="volume:4"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-sniffin-glue-issue4-1976"