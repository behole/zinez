#!/bin/bash
# Upload script for Internet Archive
# Zine: Kill Your Pet Puppy
# Generated: 2025-10-30 08:42:28

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

# Upload punk-zine-kill-your-pet-puppy-issueVarious-1980-1984
ia upload \
  "punk-zine-kill-your-pet-puppy-issueVarious-1980-1984" \
  --metadata="title:Kill Your Pet Puppy" \
  --metadata="mediatype:texts" \
  --metadata="collection:opensource" \
  --metadata="description:UK anarcho-punk zine

Punk zine from UK
Published: 1980-1984

Featured bands: Crass, Poison Girls, anarcho-punk bands

---
Contributed by the Punk Zines Research Project
Part of documenting underground punk culture and DIY publishing" \
  --metadata="subject:anarcho-punk; UK; 1980s; Crass; political" \
  --metadata="creator:Tony Drayton (later)" \
  --metadata="date:1980-1984" \
  --metadata="language:eng" \
  --metadata="licenseurl:http://creativecommons.org/licenses/by-nc-sa/4.0/" \
  --metadata="coverage:UK" \
  --metadata="volume:Various"

echo "Upload complete!"
echo "View at: https://archive.org/details/punk-zine-kill-your-pet-puppy-issueVarious-1980-1984"