#!/bin/bash
# Upload script for Internet Archive
# Zine: Jigsaw
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-jigsaw-issueVarious-1988-1995
ia upload \
  "punk-zine-jigsaw-issueVarious-1988-1995" \
  --metadata="title:Jigsaw" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Tobi Vail's pre-Riot Grrrl zine

Punk zine from Olympia, Washington, USA
Published: 1988-1995

Featured bands: Various punk and indie bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:pre-riot grrrl; feminist; punk; Olympia; Tobi Vail" \
  --metadata="creator:Tobi Vail" \
  --metadata="date:1988-1995" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Olympia, Washington, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-jigsaw-issueVarious-1988-1995"