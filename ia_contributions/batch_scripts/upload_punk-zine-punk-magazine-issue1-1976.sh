#!/bin/bash
# Upload script for Internet Archive
# Zine: Punk Magazine
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-punk-magazine-issue1-1976
ia upload \
  "punk-zine-punk-magazine-issue1-1976" \
  --metadata="title:Punk Magazine" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:First issue with Lou Reed on cover

Punk zine from New York City, USA
Published: 1976

Featured bands: Lou Reed

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:punk; NYC; Lou Reed; founding zine; USA" \
  --metadata="creator:John Holmstrom, Ged Dunn, Legs McNeil" \
  --metadata="date:1976" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:New York City, USA" \
  --metadata="volume:1"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-punk-magazine-issue1-1976"