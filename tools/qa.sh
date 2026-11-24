#!/usr/bin/env bash
# QA mouvement d'un MP4 : détection des freezes, puis loudness si piste audio.
# Usage : tools/qa.sh film.mp4
set -euo pipefail
f="${1:?usage: tools/qa.sh film.mp4}"

echo "== Freezes (>= 0.5 s sans changement) =="
ffmpeg -hide_banner -i "$f" -vf freezedetect=n=-60dB:d=0.5 -map 0:v:0 -f null - 2>&1 \
  | grep -E 'freeze_(start|end|duration)' || echo "aucun freeze"

if ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "$f" | grep -q .; then
  echo "== Loudness (cible -14 LUFS, true peak <= -2 dBTP) =="
  ffmpeg -hide_banner -i "$f" -af ebur128=peak=true -f null - 2>&1 | grep -A12 'Summary:'
fi
