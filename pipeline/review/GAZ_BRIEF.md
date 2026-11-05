# Polity gazetteer (brief for each regional agent)

## Why
A world-history atlas colours every polity on a globe for each year from 1400 to 1900, aiming at the completeness of a grand-strategy map such as Europa Universalis IV. The borders dataset it uses draws the large states well but leaves much land blank, where many real states, sultanates, chiefdoms and tribal nations existed. Examples are Rajput and Gond kingdoms in India, the sultanates of the Philippines and Moluccas, West African forest kingdoms, and Native nations of North America. Your job is to list those polities for your region, with dates, seats and approximate extents, so the atlas can fill the blank land with them.

## What to list
List every polity in your region that governed territory at some point in 1400–1900:
- kingdoms, sultanates, emirates and principalities;
- city-states and chiefdoms with a recognised ruler and seat;
- tribal confederations and nations with a home territory (e.g. Lakota, Comanche, Tuareg confederations, Kazakh jüz, Ainu, Māori iwi groupings);
- vassals and tributaries, with their overlord.

Include large well-known states too (the atlas uses them to check its existing data), but put most of your effort into the many smaller polities that ordinary world maps omit. Aim for 80–200 polities, covering the whole land area of your region in every half-century. Where land truly had no polity (deep rainforest bands, uninhabited desert), say so in `gaps`.

## Fields (one JSON object per polity)
```json
{
  "name": "Malwa Sultanate",
  "aliases": ["Sultanate of Malwa", "Mandu"],
  "from": 1392, "to": 1562,
  "seat": {"name": "Mandu", "lat": 22.35, "lon": 75.40},
  "extent": [[23.2, 74.2], [24.6, 77.5], [21.4, 78.0], [21.6, 74.3]],
  "reach_km": 220,
  "overlord": [{"from": 1531, "to": 1537, "name": "Gujarat Sultanate"}],
  "phases": [{"from": 1392, "to": 1500, "extent": [[...]]}, {"from": 1500, "to": 1562, "extent": [[...]]}],
  "kind": "sultanate",
  "source": "https://en.wikipedia.org/wiki/Malwa_Sultanate",
  "confidence": "high",
  "note": "ended with Mughal conquest 1562"
}
```
- `from`/`to`: years of effective existence (to = year it ended; clip to 1400–1900 is not needed).
- `seat`: capital or main seat (lat/lon decimal degrees on land, ±0.05°). If the seat moved, use `phases` with their own `seat`.
- `extent`: 3–8 [lat, lon] points around the edge of the territory it actually governed at its typical size, going round the border (not a straight line), from a map or description in your sources. This is the most important field after the dates: be as faithful as the sources allow. If you cannot find any extent information, omit `extent` and give `reach_km` (radius of effective control from the seat).
- `phases`: optional, when the extent or seat changed a lot (each phase: from, to, and seat and/or extent).
- `overlord`: optional list of dated overlords.
- `kind`: kingdom | sultanate | empire | city-state | chiefdom | confederation | tribal nation | principality | other.
- `confidence`: high | moderate | low.

## Sources
Use WebSearch and WebFetch (Wikipedia articles on the polity and its region, Britannica, academic pages; Wikipedia infobox maps and "territory" sections are good for extents). Every polity needs a source URL. Do not copy from any game data or game wiki (no Europa Universalis wiki, no Paradox forums): use historical sources.

## Output
Write a JSON file to the path in your prompt: `{"region": "...", "polities": [ ... ], "gaps": [{"area": "...", "from": 1400, "to": 1900, "note": "..."}]}`. Keep any scripts in your own subfolder of the scratchpad (named after your region), never a shared filename like build.py, since other agents share the scratchpad. When done, check the file parses with python, and reply with a short summary: count, the parts of your region still thin, anything low confidence.
