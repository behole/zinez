#!/bin/bash
# Upload script for Internet Archive
# Zine: Suburban Voice
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-suburban-voice-issueVarious-1980s-1990s
ia upload \
  "punk-zine-suburban-voice-issueVarious-1980s-1990s" \
  --metadata="title:Suburban Voice" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Boston area hardcore zine

Punk zine from Boston, USA
Published: 1980s-1990s

Featured bands: Boston hardcore bands, SSD, DYS

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:Boston; hardcore; straight edge; punk; East Coast" \
  --metadata="creator:Al Quint" \
  --metadata="date:1980s-1990s" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Boston, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-suburban-voice-issueVarious-1980s-1990s"