#!/bin/sh
# Bump the build stamp in index.html. Open copies of the app compare this stamp with the live site and reload when it changes.
# Run before every commit that should reach people who already have the app open:  sh tools/stamp.sh
set -e
cd "$(dirname "$0")/.."
v="$(date -u +%Y-%m-%d.%H%M%S)"
sed -i.bak "0,/<meta name=\"build\" content=\"[^\"]*\"/s//<meta name=\"build\" content=\"$v\"/" index.html && rm -f index.html.bak
echo "build $v"
# The offline worker (sw.js) lists every file to keep on the device and gets a new version when any of them changes.
python3 tools/sw-build.py
