#!/bin/bash
# Upload script for Internet Archive
# Zine: Maximum Rocknroll
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-maximum-rocknroll-issue432-2019
ia upload \
  "punk-zine-maximum-rocknroll-issue432-2019" \
  --metadata="title:Maximum Rocknroll" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Final print issue with cover by Martin Sprouse

Punk zine from San Francisco, USA
Published: 2019

Featured bands: Various

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:final issue; punk; end of era; hardcore" \
  --metadata="creator:MRR collective" \
  --metadata="date:2019" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:San Francisco, USA" \
  --metadata="volume:432"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-maximum-rocknroll-issue432-2019"