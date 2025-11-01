#!/bin/bash
# Upload script for Internet Archive
# Zine: Maximum Rocknroll
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-maximum-rocknroll-issue13-1984
ia upload \
  "punk-zine-maximum-rocknroll-issue13-1984" \
  --metadata="title:Maximum Rocknroll" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Classic mid-80s issue

Punk zine from San Francisco, USA
Published: 1984

Featured bands: Various hardcore bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:hardcore; punk; political; anarchist mantras" \
  --metadata="creator:Tim Yohannan and collective" \
  --metadata="date:1984" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:San Francisco, USA" \
  --metadata="volume:13"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-maximum-rocknroll-issue13-1984"