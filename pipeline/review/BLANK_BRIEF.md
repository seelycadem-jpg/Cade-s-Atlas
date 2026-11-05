# Blank-land review (brief for each reviewer)

## Why
A world-history atlas colours every land province by its ruler for each year 1400-2019. The owner says the map still shows "odd blanks": land drawn as no state, or as a generic "peoples" label, where a real state ruled or plainly claimed it. Example: the Libyan coast at Sirte, Misrata and Ajdabiya shows "Saharan nomads" for centuries although Hafsid, Ottoman and Karamanli Tripoli held that coast. Your job is to find every such blank in your area and report corrections. You do not edit anything else.

## What you get
- `/tmp/g4/review2/blanks_<group>.txt`: every modern region in your area that is open land (no state, or peoples) while bordering a state, with how many decades this lasts, the years, the label shown, and the neighbouring states. `COAST` marks regions that touch the sea. Sorted by duration.
- `/tmp/g4/review2/<region>.txt`: decade snapshots of the whole map for a review region (Holders and Changes), and `<region>_places.json`: the exact modern region names you must use. Notation: `X [under Y]` overlord; `~est` estimated extent; `(peoples: ...)` land with no state; `(no polity)` nothing recorded.
These files are long: read them in parts.

## Rules for deciding
1. Fill a blank with a state when a state ruled it, collected tribute from it, or held its coast or towns (coasts and river valleys especially). Nominal sovereignty over a thinly peopled desert next to a state's core counts (the owner prefers a filled map, EU4-style) when that state was recognised as its ruler at the time.
2. Leave land as peoples when no state held it: interior Sahara, Arabian Empty Quarter, New Guinea, Australia before colonisation, Amazonia, Siberia before the Russian advance, Kalahari, stateless highland societies. For these, if the label is wrong or generic and a better name exists, give it with owner "peoples:Name" (e.g. "peoples:Tuareg (Kel Ajjer)").
3. Native nations of the Americas are deliberately drawn as named homelands until their treaty era: do not change those.
4. Also report wrong states you notice in your area (wrong ruler for a decade or more, anachronisms), but blanks come first.
5. Use the map's existing polity names where the same polity already appears, so it keeps one colour.

## How to verify
Use WebSearch and WebFetch (Wikipedia, Britannica, academic pages). Every correction needs a source URL supporting its dates. Do not rely on memory for dates.

## Output
Write a JSON array to `/home/claude/review/fix/zz_blank_<group>.json` (group name given to you), saving after every ~20 corrections:
```json
[{"from": 1551, "to": 1711, "country": "Libya", "regions": ["Surt", "Misratah"], "owner": "Ottoman Empire",
  "why": "Tripolitanian coast under Ottoman rule from the conquest of Tripoli (1551) until the Karamanli dynasty (1711)", "source": "https://en.wikipedia.org/wiki/Ottoman_Tripolitania", "severity": "major"}]
```
- `from` inclusive, `to` exclusive; `country` and `regions` exactly as in the places files (`["*"]` = whole country; optional `except`).
- `owner`: state name, `"none"`, or `"peoples:Name"`; `overlord` optional; `severity` major | minor.
- Corrections in this file are applied after all earlier review files, so they win.
Keep scripts in your own scratchpad subfolder named after your group. When done, check the JSON parses and reply with a short summary: number of corrections, biggest blanks fixed, and what you left blank on purpose.

## Added option: only_open
Add `"only_open": true` to a correction to fill only the provinces of those regions that are open land (no state, or peoples) in those years; provinces already held by a state are kept. Use it where a region is partly held by a real state and partly blank.
