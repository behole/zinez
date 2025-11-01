#!/bin/bash
# Upload script for Internet Archive
# Zine: We Got Power
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-we-got-power-issueVarious-Early 1980s
ia upload \
  "punk-zine-we-got-power-issueVarious-Early 1980s" \
  --metadata="title:We Got Power" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:LA hardcore scene documentation

Punk zine from Los Angeles, USA
Published: Early 1980s

Featured bands: Black Flag, Minutemen, LA hardcore bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:LA hardcore; California; 1980s; punk; SST" \
  --metadata="creator:David Markey, Jordan Schwartz" \
  --metadata="date:Early 1980s" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Los Angeles, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-we-got-power-issueVarious-Early 1980s"