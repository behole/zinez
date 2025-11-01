#!/bin/bash
# Upload script for Internet Archive
# Zine: Profane Existence
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-profane-existence-issueVarious-1989-present
ia upload \
  "punk-zine-profane-existence-issueVarious-1989-present" \
  --metadata="title:Profane Existence" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:Anarchist punk zine

Punk zine from Minneapolis, USA
Published: 1989-present

Featured bands: Crust and anarcho-punk bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:anarchist; punk; political; Minneapolis; crust punk" \
  --metadata="creator:Collective" \
  --metadata="date:1989-present" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:Minneapolis, USA" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-profane-existence-issueVarious-1989-present"