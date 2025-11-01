#!/bin/bash
# Upload script for Internet Archive
# Zine: 48 Thrills
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-48-thrills-issue1-1976
ia upload \
  "punk-zine-48-thrills-issue1-1976" \
  --metadata="title:48 Thrills" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Early UK punk zine with Sex Pistols and Clash coverage

Punk zine from London, UK
Published: 1976

Featured bands: Sex Pistols, The Clash

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:UK punk; 1976; Sex Pistols; The Clash; first wave" \
  --metadata="creator:Unknown" \
  --metadata="date:1976" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:London, UK" \
  --metadata="volume:1"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-48-thrills-issue1-1976"