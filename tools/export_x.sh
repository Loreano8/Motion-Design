#!/usr/bin/env bash
# Export compatible X : H.264 High, yuv420p, 60 fps, AAC 192k, faststart.
# Usage : tools/export_x.sh film.mp4 [film_x.mp4]
set -euo pipefail
in="${1:?usage: tools/export_x.sh film.mp4 [out]}"
out="${2:-${in%.mp4}_x.mp4}"
ffmpeg -y -hide_banner -i "$in" -c:v libx264 -profile:v high -pix_fmt yuv420p -r 60 -crf 18 \
  -c:a aac -b:a 192k -movflags +faststart "$out"
echo "$out"
