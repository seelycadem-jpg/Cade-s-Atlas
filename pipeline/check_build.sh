#!/bin/bash
# Safety check: the content pipeline still runs, and its output matches the stored
# Prototype 1 data (site/data.json and site/graph.json). Builds into a scratch copy so
# site/ is never touched. rules.json is not compared: its unused polities step differs.
set -e
cd "$(dirname "$0")/.."
T="${ATLAS_WORK:-work}/check"
rm -rf "$T"; mkdir -p "$T/site" "$T/scratch"
cp site/*.json "$T/site/"
ATLAS_SITE="$PWD/$T/site" ATLAS_WORK="$PWD/$T/scratch" bash pipeline/build.sh > "$T/build.log"
for f in data.json graph.json; do
  if cmp -s "$T/site/$f" "site/$f"; then echo "same   $f"; else echo "DIFFERS $f"; exit 1; fi
done
echo "pipeline check passed"
