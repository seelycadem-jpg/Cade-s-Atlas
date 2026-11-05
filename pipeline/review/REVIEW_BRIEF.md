# Year-by-year map review (brief for each regional reviewer)

## Why
A world-history atlas colours every land province by its ruler for each year from 1400 to 2025. Readers will rely on it, so the map must flow through time without major historical mistakes. You review one region and report corrections. You do not edit anything else.

## What you get
- `/tmp/g4/review/<region>.txt`: decade snapshots of the map. For each decade, "Holders" lists every polity with the share of each modern country's provinces it holds, then "Changes" lists provinces that changed hands since the previous decade, named by modern country and first-level region. Notation: `X [under Y]` means X with overlord Y; `~est` means the extent was estimated from a researched seat and reach; `(peoples: …)` means land with no state; `(no polity)` means nothing recorded.
- `/tmp/g4/review/<region>_places.json`: the exact modern region names you may use in corrections, by country. Use these names exactly.

The file is long. Read it in parts (e.g. 300 lines at a time) and work through every decade.

## What to look for (major mistakes first)
1. A region held by the wrong polity for a decade or more (e.g. a state shown after its conquest, or before it existed).
2. Missing states: land shown as peoples or no polity where a known state ruled, or a well-known state absent entirely.
3. Anachronistic names (a polity shown long after it ended, or a name from another century).
4. Wrong timing: a well-known change of hands shown a decade or more early or late (treaties, conquests, independence).
5. Flow problems: a state vanishing and reappearing, territory flipping back and forth without cause, implausible `~est` extents.
6. Wrong overlord relations where they matter (vassals and colonies).
Ignore spelling and small labelling choices unless they mislead. Do not "fix" things that are matters of reasonable cartographic choice.

## How to verify
Use WebSearch and WebFetch (Wikipedia, Britannica, academic pages). Every correction needs a source URL that supports its dates. Do not rely on memory for dates.

## Output
Write a JSON array to `/home/claude/review/fix/<region>.json`, saving after every ~20 corrections so work survives an interruption:
```json
[
  {"from": 1475, "to": 1783, "country": "Ukraine", "regions": ["Crimea"], "owner": "Crimean Khanate", "overlord": "Ottoman Empire",
   "why": "Crimean Khanate under Ottoman suzerainty from 1475 until Russian annexation in 1783", "source": "https://en.wikipedia.org/wiki/Crimean_Khanate", "severity": "major"}
]
```
- `from` inclusive, `to` exclusive (year the next ruler took over).
- `country` and `regions` must be names from the places file; `regions: ["*"]` means the whole modern country; `except: [...]` optional.
- `owner`: the polity name (use the map's existing name when the same polity already appears on the map, so it keeps one colour; otherwise the standard English name). `owner: "none"` for land with no state.
- `overlord` optional; `severity`: major | minor.
Keep scripts in your own scratchpad subfolder named after your region (never a shared name like build.py). When done, check the JSON parses, and reply with a short summary: how many corrections, the biggest mistakes you found, and anything you could not resolve.
