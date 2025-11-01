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

# Upload punk-zine-sniffin-glue-issue9-1977
ia upload \
  "punk-zine-sniffin-glue-issue9-1977" \
  --metadata="title:Sniffin' Glue" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:April 1977 issue featuring Billy Idol

Punk zine from London, UK
Published: 1977

Featured bands: Billy Idol, The Clash, The Damned, Ramones, Cortinas

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:punk; Billy Idol; The Clash; The Damned; Ramones; Cortinas" \
  --metadata="creator:Mark Perry" \
  --metadata="date:1977" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:London, UK" \
  --metadata="volume:9"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-sniffin-glue-issue9-1977"