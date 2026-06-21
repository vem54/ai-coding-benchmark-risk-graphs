#!/usr/bin/env bash
# Fetch the IBM Plex fonts used by the charts into render/fonts/.
# IBM Plex is licensed under the SIL Open Font License 1.1 (redistributable).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p fonts
base="https://github.com/IBM/plex/raw/master/packages"

for w in Regular Medium SemiBold Bold; do
  curl -fsSL -o "fonts/IBMPlexSans-$w.ttf" \
    "$base/plex-sans/fonts/complete/ttf/IBMPlexSans-$w.ttf"
done
for w in Regular Medium; do
  curl -fsSL -o "fonts/IBMPlexMono-$w.ttf" \
    "$base/plex-mono/fonts/complete/ttf/IBMPlexMono-$w.ttf"
done

echo "Fonts installed in render/fonts/:"
ls -1 fonts/
