#!/bin/bash
# The globe's map data, end to end. Run from anywhere.
set -e
cd "$(dirname "$0")/.."   # the pipeline folder
MAPS=../site/maps; WORK="${ATLAS_WORK:-../work}"; mkdir -p "$WORK"
python3 mapfix.py                     # survey maps 1400-2010 with corrected owners -> site/maps
mapshaper -i $WORK/land_src.json -o format=geojson $WORK/land.geojson 2>/dev/null || mapshaper -i $MAPS/land.json -o format=geojson $WORK/land.geojson
python3 g2/landfix.py                # cut land at the 180th meridian for the planar steps
python3 g2/despike.py                 # spikes and misplaced regional names
python3 g2/gapfill.py                 # close coastal gaps and slivers
python3 g2/fillblank.py               # fill blank land from neighbouring surveys or regional peoples
python3 g2/despike.py
for y in 1400 1500 1530 1600 1650 1700 1715 1783 1800 1815 1880 1900 1914 1920 1930 1938 1945 1960 1994 2000 2010; do  # shared edges, so borders draw once
  mapshaper -i $MAPS/w$y.json -filter "!!NAME" -clean snap-interval=0.002 gap-width=2km -o format=topojson precision=0.0001 force $MAPS/w$y.json 2>/dev/null
done
node g2/hb_props.js                   # label points and areas
mapshaper -i $MAPS/land.json -simplify 25% weighted keep-shapes -o format=topojson precision=0.01 $MAPS/landlo.json
node g2/cs_build.js                   # dated borders 1886-2019 and their ledger
python3 g2/cities.py                  # historical cities
python3 g2/physbuild.py               # mountains, deserts, rivers, lakes, seas
python3 g2/islands.py                 # who held the islands before 1886
python3 g2/assemble.py                # dated transfers 1400-1885 and the full ledger
python3 g2/csgaps.py                  # land the 1886-2019 record leaves empty, with its holder
# g2/transfers.py and the dating files (g2/dated_0*.json) are inputs; rerunning transfers.py renumbers pieces and needs fresh dating.
python3 g2/atoms.py                   # survey periods cut into atoms with their ruler year by year
python3 g2/coastdist.py               # distance to coast for the engraved water lines
