#!/bin/bash
# Master upload script for all prepared punk zines
# Generated: 2025-10-30 08:42:28
# Total zines: 83

echo '========================================='
echo '🎸 Uploading Punk Zines to Internet Archive'
echo 'Total zines to upload: 83'
echo '========================================='

# Check if internetarchive is configured
if ! ia configure --help &> /dev/null; then
    echo 'Error: internetarchive not configured'
    echo 'Run: ia configure'
    exit 1
fi

UPLOAD_COUNT=0
ERROR_COUNT=0

# Upload 1/83: Sniffin' Glue
echo ''
echo 'Uploading 1/83: Sniffin' Glue'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue3-1976.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 2/83: Sniffin' Glue
echo ''
echo 'Uploading 2/83: Sniffin' Glue'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue4-1976.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 3/83: Sniffin' Glue
echo ''
echo 'Uploading 3/83: Sniffin' Glue'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue5-1976.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 4/83: Sniffin' Glue
echo ''
echo 'Uploading 4/83: Sniffin' Glue'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue9-1977.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 5/83: Sniffin' Glue
echo ''
echo 'Uploading 5/83: Sniffin' Glue'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sniffin-glue-issue12-1977.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 6/83: Punk Magazine
echo ''
echo 'Uploading 6/83: Punk Magazine'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-punk-magazine-issue1-1976.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 7/83: Maximum Rocknroll
echo ''
echo 'Uploading 7/83: Maximum Rocknroll'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-maximum-rocknroll-issue13-1984.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 8/83: Maximum Rocknroll
echo ''
echo 'Uploading 8/83: Maximum Rocknroll'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-maximum-rocknroll-issue432-2019.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 9/83: Slash
echo ''
echo 'Uploading 9/83: Slash'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-slash-issueVarious-1977-1980.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 10/83: Search & Destroy
echo ''
echo 'Uploading 10/83: Search & Destroy'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-search--destroy-issueVarious-1977.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 11/83: Ripped & Torn
echo ''
echo 'Uploading 11/83: Ripped & Torn'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-ripped--torn-issueVarious-1976-1979.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 12/83: Sideburns
echo ''
echo 'Uploading 12/83: Sideburns'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-sideburns-issue1-1977.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 13/83: Bikini Kill
echo ''
echo 'Uploading 13/83: Bikini Kill'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-bikini-kill-issue1-1991.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 14/83: Bikini Kill
echo ''
echo 'Uploading 14/83: Bikini Kill'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-bikini-kill-issue2-1991.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 15/83: Jigsaw
echo ''
echo 'Uploading 15/83: Jigsaw'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-jigsaw-issueVarious-1988-1995.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 16/83: Girl Germs
echo ''
echo 'Uploading 16/83: Girl Germs'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-girl-germs-issueVarious-1990-1991.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 17/83: Profane Existence
echo ''
echo 'Uploading 17/83: Profane Existence'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-profane-existence-issueVarious-1989-present.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 18/83: Jet Lag
echo ''
echo 'Uploading 18/83: Jet Lag'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-jet-lag-issueVarious-1980-1981.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 19/83: We Got Power
echo ''
echo 'Uploading 19/83: We Got Power'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-we-got-power-issueVarious-Early 1980s.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 20/83: Suburban Voice
echo ''
echo 'Uploading 20/83: Suburban Voice'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-suburban-voice-issueVarious-1980s-1990s.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 21/83: Kill Your Pet Puppy
echo ''
echo 'Uploading 21/83: Kill Your Pet Puppy'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-kill-your-pet-puppy-issueVarious-1980-1984.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 22/83: 48 Thrills
echo ''
echo 'Uploading 22/83: 48 Thrills'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-48-thrills-issue1-1976.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 23/83: Chainsaw
echo ''
echo 'Uploading 23/83: Chainsaw'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-chainsaw-issueVarious-1977-1978.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 24/83: Flickr zine cover
echo ''
echo 'Uploading 24/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 25/83: Flickr zine cover
echo ''
echo 'Uploading 25/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 26/83: Flickr zine cover
echo ''
echo 'Uploading 26/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 27/83: Flickr zine cover
echo ''
echo 'Uploading 27/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 28/83: Flickr zine cover
echo ''
echo 'Uploading 28/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 29/83: Flickr zine cover
echo ''
echo 'Uploading 29/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 30/83: Flickr zine cover
echo ''
echo 'Uploading 30/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 31/83: Flickr zine cover
echo ''
echo 'Uploading 31/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 32/83: Flickr zine cover
echo ''
echo 'Uploading 32/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 33/83: Flickr zine cover
echo ''
echo 'Uploading 33/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 34/83: Flickr zine cover
echo ''
echo 'Uploading 34/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 35/83: Flickr zine cover
echo ''
echo 'Uploading 35/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 36/83: Flickr zine cover
echo ''
echo 'Uploading 36/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 37/83: Flickr zine cover
echo ''
echo 'Uploading 37/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 38/83: Flickr zine cover
echo ''
echo 'Uploading 38/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 39/83: Flickr zine cover
echo ''
echo 'Uploading 39/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 40/83: Flickr zine cover
echo ''
echo 'Uploading 40/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 41/83: Flickr zine cover
echo ''
echo 'Uploading 41/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 42/83: Flickr zine cover
echo ''
echo 'Uploading 42/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 43/83: Flickr zine cover
echo ''
echo 'Uploading 43/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 44/83: Flickr zine cover
echo ''
echo 'Uploading 44/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 45/83: Flickr zine cover
echo ''
echo 'Uploading 45/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 46/83: Flickr zine cover
echo ''
echo 'Uploading 46/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 47/83: Flickr zine cover
echo ''
echo 'Uploading 47/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 48/83: Flickr zine cover
echo ''
echo 'Uploading 48/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 49/83: Flickr zine cover
echo ''
echo 'Uploading 49/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 50/83: Flickr zine cover
echo ''
echo 'Uploading 50/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 51/83: Flickr zine cover
echo ''
echo 'Uploading 51/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 52/83: Flickr zine cover
echo ''
echo 'Uploading 52/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 53/83: Flickr zine cover
echo ''
echo 'Uploading 53/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 54/83: Flickr zine cover
echo ''
echo 'Uploading 54/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 55/83: Flickr zine cover
echo ''
echo 'Uploading 55/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 56/83: Flickr zine cover
echo ''
echo 'Uploading 56/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 57/83: Flickr zine cover
echo ''
echo 'Uploading 57/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 58/83: Flickr zine cover
echo ''
echo 'Uploading 58/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 59/83: Flickr zine cover
echo ''
echo 'Uploading 59/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 60/83: Flickr zine cover
echo ''
echo 'Uploading 60/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 61/83: Flickr zine cover
echo ''
echo 'Uploading 61/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 62/83: Flickr zine cover
echo ''
echo 'Uploading 62/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 63/83: Flickr zine cover
echo ''
echo 'Uploading 63/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 64/83: Flickr zine cover
echo ''
echo 'Uploading 64/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 65/83: Flickr zine cover
echo ''
echo 'Uploading 65/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 66/83: Flickr zine cover
echo ''
echo 'Uploading 66/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 67/83: Flickr zine cover
echo ''
echo 'Uploading 67/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 68/83: Flickr zine cover
echo ''
echo 'Uploading 68/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 69/83: Flickr zine cover
echo ''
echo 'Uploading 69/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 70/83: Flickr zine cover
echo ''
echo 'Uploading 70/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 71/83: Flickr zine cover
echo ''
echo 'Uploading 71/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 72/83: Flickr zine cover
echo ''
echo 'Uploading 72/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 73/83: Flickr zine cover
echo ''
echo 'Uploading 73/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 74/83: Flickr zine cover
echo ''
echo 'Uploading 74/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 75/83: Flickr zine cover
echo ''
echo 'Uploading 75/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 76/83: Flickr zine cover
echo ''
echo 'Uploading 76/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 77/83: Flickr zine cover
echo ''
echo 'Uploading 77/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 78/83: Flickr zine cover
echo ''
echo 'Uploading 78/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 79/83: Flickr zine cover
echo ''
echo 'Uploading 79/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 80/83: Flickr zine cover
echo ''
echo 'Uploading 80/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 81/83: Flickr zine cover
echo ''
echo 'Uploading 81/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 82/83: Flickr zine cover
echo ''
echo 'Uploading 82/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

# Upload 83/83: Flickr zine cover
echo ''
echo 'Uploading 83/83: Flickr zine cover'
if bash 'ia_contributions/batch_scripts/upload_punk-zine-flickr-zine-cover.sh'; then
    UPLOAD_COUNT=$((UPLOAD_COUNT + 1))
    echo '✅ Success!'
else
    ERROR_COUNT=$((ERROR_COUNT + 1))
    echo '❌ Failed'
fi

# Rate limiting - be nice to IA servers
sleep 5

echo ''
echo '========================================='
echo '📊 Upload Summary'
echo "Successful: $UPLOAD_COUNT"
echo "Failed: $ERROR_COUNT"
echo '========================================='