# Date the territorial transfers for the Meanwhile Atlas globe

The globe shows world borders from survey maps of 1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880 and 1900. A script compared each pair of consecutive maps and found every piece of land whose ruler differs between them. Each line in your input file is one piece:

`index | earlier map year-later map year | from: owner on earlier map | to: owner on later map (label on later map) | area | a point inside the piece (lon, lat)`

Your job: for each piece, decide when the land actually changed hands, so the globe can switch it in the right year instead of jumping at the next survey.

Classify every line as exactly one of:
- `dated`: a real change of rule you can date to a year within (earlier, later]. Give the year the change took effect (a treaty, a conquest completed, an annexation). Where it happened over several years, give the year the bulk passed (e.g. Russian conquest of Siberia: use the year the piece's area was mostly taken; partitions of Poland: 1772, 1793 or 1795 by where the point lies).
- `undated`: a real change, but gradual or with no year you can defend (frontier drift, nomad confederations shifting, a chiefdom's gradual expansion). The globe will hatch it as "changed hands between the two surveys".
- `artefact`: the two maps disagree for mapping reasons rather than a real transfer: the same polity under different names, an umbrella label ("Hindu kingdoms", "Islamic states", "hunter-gatherers") replaced by another umbrella, inconsistent drawing of the same frontier, a state that the earlier map shows after it had already ended. When the earlier map is wrong because the change had already happened before the earlier year, also call it artefact.

Use the point (lon, lat) to tell which part of a large owner is meant. Use real knowledge only; if unsure between dated and undated, choose undated. Never invent a year.

For `dated` lines also write `t`: a ledger line of 4 to 14 words in present tense naming the actors with role where it helps, e.g. "Prussian King Frederick II seizes Silesia from Austria", "Russia annexes Crimea from the Ottoman Empire", "Mughal Emperor Aurangzeb conquers Bijapur". No authorities, no adjectives of scale, no "not X but Y".

Output: write a JSON array to the output file named in your task, one object per input line, in input order:
`{"i": <index>, "k": "dated"|"undated"|"artefact", "y": <year or null>, "t": "<ledger line or null>"}`
Validate with: `python3 -c "import json,sys; a=json.load(open(sys.argv[1])); print(len(a)); assert all(x['k'] in ('dated','undated','artefact') for x in a); assert all((x['y'] is not None)==(x['k']=='dated') for x in a)" <file>` and check the count equals the input line count. Reply only with the counts of each class.
