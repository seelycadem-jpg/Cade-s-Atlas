# Border review: control-point timelines (brief for each regional agent)

## Why
A world-history atlas draws political borders on a globe for every year from 1400 to today. Readers will make judgments from it, so its borders must be correct. You are building independent ground truth for one region: a set of places with a dated record of who ruled each one. The maps will be scored against your timelines automatically, so accuracy and dates matter more than prose.

## Your task
For your region (given in your prompt), choose about 50 places and, for each, write who ruled it from 1400 to 2025 as a sequence of dated intervals with a source for each change.

Choose places so that they:
- include every capital and major city in the region over the period;
- include places that changed hands (frontier towns, contested provinces, ports taken by colonial powers, places that moved between empires), because these are where maps go wrong;
- include interior and peripheral places (the hinterland of colonies, steppe, desert, forest, highlands), including places where no state ruled for part of the period. For those intervals, give ruler "none" and name the people in `peoples`, e.g. "Tuareg confederations" or "Lakota";
- cover the region's whole land area, not only its core. Spread them out.

## Rules on what counts as ruling
- `ruler` is the polity that actually governed the place on the ground at that time: it collected tax, held the fort or appointed the governor. A claim on paper does not count; for example, Spanish claims to the North American interior do not make Spain the ruler of the Great Plains.
- If the place was governed by a vassal, tributary, protectorate or member state, `ruler` is that local polity and `overlord` is the suzerain. Examples: Wallachia, overlord Ottoman Empire; Bavaria, overlord Holy Roman Empire; Hyderabad after 1798, overlord British East India Company.
- Colonial rule counts from effective occupation of that place, not the claim or the conference that recognised it. Berlin 1884–85 by itself made no one the ruler of the African interior.
- Use the common English name of the polity, plus aliases (local names, alternative English names, and the Wikidata QID if you find it). Distinguish successive polities where the name or regime changed, e.g. Kingdom of France → French First Republic → French Empire. Keep a single state in a single interval even when the dynasty changed (Ming then Qing are separate, though; they are separate states).
- Dates: give the year of the change (and month if known). Use the date power actually changed hands (capture, treaty taking effect, occupation), and say which in `note`.
- War-time occupations of less than about a year can be skipped unless they changed the map.

## Sources
Use WebSearch and WebFetch. Prefer encyclopedic and scholarly sources: Wikipedia articles on the place's history and on specific treaties and wars are acceptable as the citation, as are Britannica, national historical atlases and academic pages. Every interval needs at least one source URL that supports its start date. Where sources disagree, choose the better-supported date, record the other in `note`, and set `confidence` to "moderate" or "low".

Do not rely on memory alone for dates. Look them up. Do not consult or copy any map dataset (historical-basemaps, Cliopatria, GeaCron, Euratlas, CShapes) — the point is an independent check on those.

## Output
Write one JSON file to the path given in your prompt, structured like this (valid JSON, UTF-8):

```json
{
  "region": "Western Europe",
  "places": [
    {
      "place": "Calais",
      "lat": 50.95, "lon": 1.86,
      "kind": "city",            
      "timeline": [
        {"from": 1400, "to": 1558, "ruler": "Kingdom of England", "aliases": ["England"], "overlord": null, "peoples": null,
         "date": "1347 (siege), held until January 1558", "source": "https://en.wikipedia.org/wiki/Calais", "confidence": "high", "note": "English Pale of Calais"},
        {"from": 1558, "to": 1792, "ruler": "Kingdom of France", "aliases": ["France"], "overlord": null, "peoples": null,
         "date": "7 January 1558, captured by Duke of Guise", "source": "https://en.wikipedia.org/wiki/Siege_of_Calais_(1558)", "confidence": "high", "note": ""}
      ]
    }
  ]
}
```

- `kind`: "capital" (capital of a state at some point in 1400–2025), "city", "frontier", or "interior".
- `from` is the first year the ruler held the place (use 1400 if it was already held then); `to` is the year the next ruler took it (exclusive). Intervals must be contiguous from 1400 to 2025 with no gaps or overlaps. The last interval ends at 2025.
- Coordinates in decimal degrees, accurate to about 0.05°, on land.

When finished, check that the file parses (`python3 -c "import json;json.load(open('PATH'))"`) and that each timeline runs 1400→2025 without gaps. Then reply with a short summary: number of places, any intervals you marked low confidence, and any place where sources sharply disagree.
