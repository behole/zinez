#!/bin/bash
# Upload script for Internet Archive
# Zine: Ripped & Torn
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-ripped--torn-issueVarious-1976-1979
ia upload \
  "punk-zine-ripped--torn-issueVarious-1976-1979" \
  --metadata="title:Ripped & Torn" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:First Scottish punk zine, 'Loudest Punk Fanzine in the UK'

Punk zine from Glasgow/Cumbernauld, Scotland
Published: 1976-1979

Featured bands: Sex Pistols, The Clash, Scottish bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:Scottish punk; UK; 1970s; DIY" \
  --metadata="creator:Tony Drayton" \
  --metadata="date:1976-1979" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Glasgow/Cumbernauld, Scotland" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-ripped--torn-issueVarious-1976-1979"