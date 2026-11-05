#!/bin/bash
set -e
cd "$(dirname "$0")"   # the pipeline folder; scripts take their paths from paths.py
python3 make_json.py >/dev/null
python3 arcs_build.py >/dev/null
python3 refine.py | grep -v "^WARN backwards: Summer Palace"
python3 tiers.py
python3 deepen.py
python3 analysis.py
python3 briefcheck.py
python3 links.py
python3 map_rules.py
python3 polities.py
python3 motifs.py
python3 figs.py
python3 graph_build.py
