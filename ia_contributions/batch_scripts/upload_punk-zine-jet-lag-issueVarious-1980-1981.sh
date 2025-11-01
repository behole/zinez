#!/bin/bash
# Upload script for Internet Archive
# Zine: Jet Lag
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-jet-lag-issueVarious-1980-1981
ia upload \
  "punk-zine-jet-lag-issueVarious-1980-1981" \
  --metadata="title:Jet Lag" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:St. Louis punk scene coverage

Punk zine from St. Louis, USA
Published: 1980-1981

Featured bands: St. Louis punk bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:St. Louis; punk; regional; 1980s; Midwest" \
  --metadata="creator:Unknown" \
  --metadata="date:1980-1981" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:St. Louis, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-jet-lag-issueVarious-1980-1981"