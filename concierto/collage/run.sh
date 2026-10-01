#!/bin/bash
# Render the collage layers with headless Chromium and composite them over the final video.
# usage: run.sh <repo-sha> <master-url> [upload-url]
set -e
SHA=$1; MASTER=$2; UP=$3
BASE=https://raw.githubusercontent.com/Xelick/criterio-assets/$SHA/concierto/collage
mkdir -p /home/user/col/fonts /home/user/col/fr && cd /home/user/col
for f in index.html render.js composite.py noise.png fonts/Fraunces-SoftBlack.ttf fonts/PermanentMarker.ttf \
         fonts/MartianMonowght500.ttf fonts/NunitoSans-Black.ttf fonts/NunitoSanswght800.ttf; do
  curl -sfL -o $f $BASE/$f
done
[ -s v.mp4 ] || curl -sf -o v.mp4 "$MASTER"
export NODE_PATH=$(npm root -g)
for r in 0-159 160-319 320-479 480-639 640-799 800-959; do node render.js front fr $r & done
node render.js back fr 200-310 &
wait
echo "rendered $(ls fr | wc -l) frames"
python3 composite.py
ls -la out.mp4
if [ -n "$UP" ]; then
  curl -s -o /dev/null -w "PUT %{http_code}\n" -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --data-binary @out.mp4 "$UP"
fi
