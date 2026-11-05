# Ancient arcs: story design and event selection (brief for each arc designer)

## Why
Meanwhile Atlas is a world-history atlas built for analysis: events linked by graded causal arrows, gathered into stories and arcs with a thesis. The owner wants far more depth from the Late Bronze Age collapse to the birth of Islam: Greek city-states, the Peloponnesian War, the rise and fall of the Roman Republic and Empire, the birth of Judaism, Christianity and Islam, and the empires around them. You design one arc and select the events it needs.

## Read first
- /home/claude/review/story-method.md is not on disk; the method is below. One fully built arc exists as a model: /home/claude/site/graph.json, key "stories", id "german-question" (thesis, assumptions, disconfirm, awkward, shelf, chapters with hinge and support events, s1/s2 text). Read it.
- The event selection so far: /home/claude/review/events_anc/select.json (308 events, 3300 BCE-1439, schema in /home/claude/review/EV_SELECT_BRIEF.md). Reuse its events where they fit (cite their ids); add new ones in the same schema.
- Existing events from 1440: /home/claude/site/data.json ("events").

## The method (follow it)
1. DEFINE: name the contest (a tension, never a period); a thesis in one sentence that could be wrong; up to three assumptions; a disconfirmation line (what would have to be true for the thesis to be wrong); the awkward fact (one thing that does not fit the thesis, stated as such); a shelf of 3-6 real works (author, title, year) for the editors only.
2. SELECT: list candidates, score them, pick 4-7 chapters per story with one hinge event each. Connector test between chapters: "therefore" or "but"; an "and then" means merge or cut.
3. An arc holds 2-4 stories; a story holds 3-7 chapters; each chapter has one hinge (tier 1 or 2) and 2-6 support events (tier 2 or 3).
4. Naming: the arc title is the thesis compressed into two to four plain words, or a term of art; no puns, no borrowed lines, no topic labels; the subtitle carries scope and dates.

## Voice for s1/s2 (chapter text)
Presidential daily brief: judgment first, every sentence carries information. Never the negation-then-reveal construction ("It did not X. It Y'd.", "Not X, but Y"). Name no historians or books in s1/s2 (the shelf stays internal). Actors with role and name on first mention. s1: one sentence, the chapter's claim. s2: 4-7 sentences, the argument with specifics, including the expert's nod (one fact a general reader would not know and an expert would recognise). No "shaped", "pivotal", "tapestry", "paved the way", "ushered in", "the stage was set".

## Events
Each chapter's events must exist in the selection. For every new event, write a selection entry exactly as in EV_SELECT_BRIEF.md (id region-year-slug, y BCE negative, r, tier, parent = a tier-1 id, h, where, lat, lon, wk, bt if found, c, t, causes [ids], why_selected, approx). Verify every date with WebSearch/WebFetch (Wikipedia, Britannica). Aim for depth: an arc of this period should bring 40-70 new events, so that a reader can follow the chain year by year.

## Output (in /home/claude/review/events_anc/arcs/<arc-id>.json)
```json
{"arc": {"id": "...", "size": "arc", "title": "...", "sub": "...", "span": [-1250, -600], "themes": {"primary": "power", "secondary": ["war"]},
         "thesis": "...", "assumptions": ["..."], "disconfirm": "...", "awkward": "...", "shelf": [{"a": "...", "t": "...", "y": 2014}],
         "stories": ["story-id-1", "story-id-2"]},
 "stories": [{"id": "...", "size": "story", "title": "...", "sub": "...", "span": [..], "parent": "<arc id>", "thesis": "...", "assumptions": [..], "disconfirm": "...", "awkward": "...", "shelf": [..],
              "chapters": [{"id": "c1", "title": "...", "hinge": "<event id>", "conn": null, "s1": "...", "s2": "...", "support": ["<event id>", ...]},
                           {"id": "c2", "title": "...", "hinge": "...", "conn": "therefore", ...}],
              "today": "2-3 sentences: where it reaches today, checkable, no flourish."}],
 "new_events": [ selection entries ]}
```
Themes are from: power, god, war, scarcity, machine, nature, stranger, truth, time, memory.
Save after each story. Keep scripts in your own scratchpad subfolder named after your arc. When done, check the JSON parses and reply with: the arc title and thesis, each story's title and chapter hinges, the number of new events, and anything you were unsure of.
