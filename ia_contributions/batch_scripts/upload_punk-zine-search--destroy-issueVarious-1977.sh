#!/bin/bash
# Upload script for Internet Archive
# Zine: Search & Destroy
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-search--destroy-issueVarious-1977
ia upload \
  "punk-zine-search--destroy-issueVarious-1977" \
  --metadata="title:Search & Destroy" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:San Francisco punk zine, later became RE/Search

Punk zine from San Francisco, USA
Published: 1977

Featured bands: Dead Kennedys, Crime, The Avengers

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:SF punk; California; 1970s; punk; art" \
  --metadata="creator:V. Vale" \
  --metadata="date:1977" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:San Francisco, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-search--destroy-issueVarious-1977"