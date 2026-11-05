# Meanwhile Atlas: the province map and its review (2026-10-30)

The user asked for an EU4/EU5-style province map, filled everywhere, estimated where unclear and never hand-drawn. The globe is now built on that model.

Province map: 10,902 provinces made once from Natural Earth admin-1 regions (g4/prov.py): small regions merged within a country, large ones split into parts of even size (about 5,000 km2 in old dense cores, 20,000 elsewhere, up to 80,000 in desert and tundra), cut lines roughened (g4/topo.py). Files: maps/prov_p.json and maps/prov_e.json (loaded by the map's worker), maps/prov_meta.json (areas, centres, neighbours), maps/prov.json (topology, loaded only when a state is clicked).

Owners: maps/own.json gives each province its owner for every year 1400-2019 (g4/owners.py, then g4/estimate.py). Order of layers:
1. the corrected Cliopatria period maps (1400-1885) and CShapes 2.0 with gaps (1886-2019), by sample points;
2. clean-up: peoples labels carrying a state's name merged into it; duplicate names merged; stray far-flung pieces of a polity cleared; holes and short flicker removed (record artefacts of 3 years between states, 8 years involving peoples, 15 years of no record); Iberian Union keeps Portugal's colonies Portuguese;
3. islands join the nearest owner within 4 degrees;
4. estimates: about 2,250 researched polities (review/gaz/*.json, 10 regional lists with seats, dated extents and sources) take open land (no state, peoples, or lumped labels such as "HRE minor states") nearest their seat inside their extent; marked approximate on hover;
5. research control points (review/cp, 797 places) where the map shows no state, and at capitals;
6. 1,662 sourced corrections from 12 decade-by-decade regional reviews (review/fix/*.json), stated by modern country and region (applied last).

Year-by-year checks: g4/audit.py checks (flicker, big jumps, anachronisms) and dump2 (decade snapshots per region for reviewers). Remaining flicker is mostly real short events (wars, occupations).

Crash causes fixed: chunks kept in memory forever (2026-10-29); river and lake features carrying canvas-globe caches serialised to about 210 MB on open (2026-10-30). Memory at open: 56 MB page heap.

Known limits: estimated extents are approximate by design; regions mixing owners at sub-province level (treaty ports, small enclaves) can be wrong; some reviewer notes need province-level edits (listed in their reports).
