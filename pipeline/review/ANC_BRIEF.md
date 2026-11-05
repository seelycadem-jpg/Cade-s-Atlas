# Ancient and medieval map review, 3400 BCE to 1400 CE (brief for each era reviewer)

## Why
The atlas now runs from the first cities (3400 BCE) to today. Before 1400 the province owners come from two period sources: dated polity shapes (good for the Near East, the Mediterranean and China, thin elsewhere) and world maps drawn every few centuries (marked `~map`; their states jump at the snapshot years and their extents are rough). Your job: make your region's map historically sound, step by step, from 3400 BCE to 1400 CE.

## Rules the map follows
- **Statehood test.** A polity is drawn as a state (coloured) when it is a state-level society: a ruler or council governing more than one settlement from a fixed seat, with tribute or taxes (kingdoms, empires, city-states, confederations of cities). Everything else is drawn as the named land of a people or culture (neutral colour, name when zoomed): archaeological cultures, chiefdoms without a seat, pastoral and foraging peoples. Do not colour cultures; do name them well.
- **Fill where states held land.** Missing states are the main fault: a known state absent, or present for only part of its life, or drawn too small or too big. Use the polity's real core and the land it ruled at that time.
- **One name per polity**, the standard English name, consistent across its life (Old/Middle/New Kingdom of Egypt are separate phases; that is fine). Use the map's existing name when the polity already appears, so it keeps one colour.
- **Dates before 700 BCE are approximate** (chronologies differ). Use the conventional dates of the standard references (e.g. the Middle Chronology for Mesopotamia) and say which.

## What you get
- `/tmp/g4/review3/<region>.txt`: snapshots every 100 years to 800 BCE, then every 50 years to 1350 CE. "Holders" lists each polity with its share of each modern country's provinces; "Changes" lists provinces that changed hands since the previous snapshot, by modern country and region. `X [under Y]` = overlord; `~map` = from the coarse world maps; `(peoples: ...)` = land of peoples or cultures; `(no polity)` = nothing recorded.
- `/tmp/g4/review3/<region>_places.json`: the exact modern region names you must use.
These files are long: read them in parts.

## Output
A JSON array in `/home/claude/review/fix/zz_anc_<group>.json` (group name given to you), saved after every ~20 corrections:
```json
[{"from": -2334, "to": -2154, "country": "Iraq", "regions": ["Baghdad", "Babil", "Al-Qadisiyah"], "owner": "Akkadian Empire",
  "why": "Sargon of Akkad unites Sumer and Akkad c. 2334 BCE (Middle Chronology); the empire falls to the Gutians c. 2154 BCE",
  "source": "https://en.wikipedia.org/wiki/Akkadian_Empire", "severity": "major"}]
```
- Years are integers; BCE years are negative (2334 BCE = -2334). `from` inclusive, `to` exclusive.
- `country` and `regions` exactly as in the places file (`["*"]` = whole modern country; optional `except`).
- `owner`: state name, `"none"`, or `"peoples:Name"` for a culture or people (e.g. `"peoples:Yamnaya culture"`). `overlord` optional. `severity` major | minor.
- `"only_open": true` fills only provinces with no state in those years and keeps provinces already held by a state.
- `"at": [lon, lat]` targets the single province holding that place (use for city-states, ports, islands, oases: Ur, Mohenjo-daro, Knossos, Tikal, Jenne-jeno). `country` and `regions` are still required but ignored.
- Corrections in this file are applied after all others, in file order, so later lines win.

## How to verify
Use WebSearch and WebFetch (Wikipedia, Britannica, academic pages). Every correction needs a source URL that supports its dates. Do not rely on memory for dates or extents.

## Work order
Major first: (1) missing or wrongly absent states; (2) wrong ruler for a century or more; (3) anachronisms (a state shown before it existed or after it ended); (4) generic or wrong culture labels. Keep scripts in your own scratchpad subfolder named after your group. When done, check the JSON parses and reply with a short summary: number of corrections, biggest problems fixed, and what is still weak.
