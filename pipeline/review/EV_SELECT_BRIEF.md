# Event selection, 3400 BCE to 1439 (brief)

## Why
Meanwhile Atlas is a world-history atlas: a globe that runs year by year from 3400 BCE to today, plus a database of events linked by graded causal arrows. Its 781 events start in 1440. The map now reaches back to the first cities, so the database needs events for 3400 BCE to 1439. Your job is the selection list only, not the writing: the events that a serious analyst of world history would need to explain how the world got from the first states to 1440.

## What the atlas is for
An analytic training set: readers learn to grade causal claims (did X cause Y?). Events are evidence in chains of cause; the best candidates are turning points with consequences that can be traced, and the steps that connect them. Prefer politics, war, states, economy, trade, technology, religion and ideas with consequences; avoid trivia and pure "firsts" without consequences.

## Tiers
- Tier 1, knots (about 50): turning points a chain of cause cannot do without, with consequences that reach beyond their region (e.g. the unification of Egypt, the Late Bronze Age collapse, Qin unification, the conversion of Constantine, the Islamic conquests, the Mongol conquests, the Black Death).
- Tier 2, strands (about 170): the events a story is made of; each belongs to one knot as its parent (the knot it leads to or follows from).
- Tier 3, fibres (about 80): fine detail (a battle, a law, a founding) under a parent knot.
Total about 300.

## Balance
Cover all nine regions: eu (Europe), me (Middle East and North Africa, including Egypt and Mesopotamia), sa (South Asia, Central Asia), ea (East Asia), se (Southeast Asia), af (Sub-Saharan Africa), na (North America), la (Latin America incl. Mesoamerica and the Andes), oc (Oceania). Rough targets: me 55, eu 60, ea 45, sa 35, af 25, la 25, se 15, na 10, oc 8, distributed across the ages: Bronze Age (to 1200 BCE) about 45, Iron Age (1200-500 BCE) about 35, Classical (500 BCE-500 CE) about 90, Post-classical (500-1439) about 130. Late events must connect forward: the atlas already has events from 1440 (Gutenberg, the Fall of Constantinople 1453, Columbus, the Ottomans, Ming, Aztec and Inca expansion, the Atlantic slave trade); include the causes that lead into them.

## Dates
Integers; BCE negative (2334 BCE = -2334). Use conventional dates (Middle Chronology for Mesopotamia, standard Egyptian dynastic dates), flagged "approx": true when the date is uncertain by more than a decade. Verify every date with WebSearch/WebFetch (Wikipedia, Britannica); do not rely on memory.

## Output
A JSON array at /home/claude/review/events_anc/select.json, saved as you go:
```json
{"id": "me-3100-egypt-unification", "y": -3100, "approx": true, "r": "me", "tier": 1, "parent": null,
 "h": "Upper and Lower Egypt unified", "where": "Nile Valley, Egypt", "lat": 25.69, "lon": 32.64,
 "wk": "Narmer", "bt": "topic/ancient-Egypt", "c": ["political"], "t": ["empire"],
 "causes": [], "why_selected": "First territorial state; the model of divine kingship and bureaucracy for 3,000 years"}
```
- id: region-year-slug, unique. tier 2/3 need a parent (a tier-1 id from your list, same or another region).
- h: headline, under eight words, plain.
- lat/lon: where it happened (a city or site).
- wk: the exact English Wikipedia article title; bt: the Britannica path ("topic/..." or "event/...", "place/...", "biography/...") when you can find it, else omit.
- c: categories from political, war, economic, ideas, science, religion, culture. t: threads from slavery, empire, indep, revolution, rights, science, money, native, conflict, faith, explore, atrocity, plus new ancient threads where they fit: cities (the first cities and states), law (law and kingship), silk (Silk Roads and trade), steppe (the steppe and the sown).
- causes: ids of earlier events in your list that directly led to this one (the causal chain), at most three.
- why_selected: one line.
Keep scripts in your own scratchpad subfolder named events_select. When done, check the JSON parses and reply with: counts by tier, region and age; the tier-1 list (year, headline); anything you were unsure about.
