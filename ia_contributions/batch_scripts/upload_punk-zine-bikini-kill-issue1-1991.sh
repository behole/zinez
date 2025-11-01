#!/bin/bash
# Upload script for Internet Archive
# Zine: Bikini Kill
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-bikini-kill-issue1-1991
ia upload \
  "punk-zine-bikini-kill-issue1-1991" \
  --metadata="title:Bikini Kill" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:First issue of influential Riot Grrrl zine

Punk zine from Olympia, Washington, USA
Published: 1991

Featured bands: Bikini Kill, Bratmobile

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:riot grrrl; feminist; punk; DIY; Olympia" \
  --metadata="creator:Kathleen Hanna, Tobi Vail" \
  --metadata="date:1991" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Olympia, Washington, USA" \
  --metadata="volume:1"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-bikini-kill-issue1-1991"