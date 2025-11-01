#!/bin/bash
# Upload script for Internet Archive
# Zine: Chainsaw
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-chainsaw-issueVarious-1977-1978
ia upload \
  "punk-zine-chainsaw-issueVarious-1977-1978" \
  --metadata="title:Chainsaw" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:UK punk zine from first wave

Punk zine from London, UK
Published: 1977-1978

Featured bands: UK punk bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:UK punk; 1977; London; first wave; DIY" \
  --metadata="creator:Unknown" \
  --metadata="date:1977-1978" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:London, UK" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-chainsaw-issueVarious-1977-1978"