# Writing events, 3400 BCE to 1439 (brief for each writer)

## The job
Write full event entries for Meanwhile Atlas from a selection list. Each entry follows the database schema and the house voice exactly. Read three existing events first in /home/claude/site/data.json ("events"): ids eu14400 (tier 1), d-gutbible (tier 2) and eu14532 (tier 3). Match their length, density and register.

## Voice (non-negotiable)
- Presidential daily brief register: judgment first, every sentence carries information or argument, no sentence that could be cut. Analytical, never storytelling for its own sake.
- Rule zero: never the negation-then-reveal construction ("It did not X. It Y'd.", "Not X, but Y", "The question is not X but Y"). State what a thing is or did. A contrast goes in one clause with "rather than" or "instead of", only when the contrast is the point.
- Name no historians, archaeologists, books or schools of thought. Historical actors are named as actors. Where readings differ: "one reading holds ... the other holds ...", each with its evidence.
- Actors carry role and name on first mention ("Akkadian King Sargon", "Athenian statesman Pericles", "Han Emperor Wu").
- The bottom line (field bluf) always has one shape, two or three sentences: purpose (what the actors were trying to do, in plain words), outcome and cost, then the consequence for the political, international or social order.
- Banned: "existential", "shaped", "in many ways", "complex interplay", "the stage was set", "it is no coincidence", "in other words", "it is important to note", "tapestry", "pivotal", "testament", "underscore", "delve"; aphoristic closers; antitheses for rhythm; triplets for rhythm; rhetorical questions; "for the first time in N centuries" unless sourced; hedging boilerplate; a "now" paragraph ending on a flourish.
- Expert's nod: each entry carries one specific fact a general reader would not know and an expert would recognise (field fact, or inside story).
- No invented specifics: any name, number or date you cannot source is left out. Dates before 700 BCE are approximate; write "around" or "c." and use conventional chronologies.

## Fields (all strings unless noted)
- id, y (integer, BCE negative), r, tier (1/2/3), parent (tier 2/3), lat, lon, wk, bt, c, t, causes: take from the selection entry. "causes" becomes a list of {"f": id, "why": one sentence on how that event led to this one}.
- h: the headline from the selection (you may tighten it).
- who: the main actors with roles.
- where: place, modern country.
- hook: one sentence for a card, plain, under 25 words.
- what: one or two sentences: what happened.
- why: 2-4 sentences: the causes, specific.
- story: 3-5 sentences: the account, with figures where sourced.
- then: 2-3 sentences: the immediate consequences (to about a century).
- sig: same text as then.
- now: 2-3 sentences: the long consequence, written forward to what it still governs, checkable, no flourish.
- fact: one sourced, specific, surprising fact.
- bluf: the bottom line (shape above).
- btt: Britannica article title (if bt given).
- w: 3 for tier 1, 2 for tier 2, 1 for tier 3. map: the event year y.
- figs (optional, tier 1 and 2 when real figures exist): {"kv": [[figure, label], ...]}, 2-4 items, each sourced in your notes.
- sites (optional): up to three [{"n": name, "lat":, "lon":, "d": one line}] for multi-site events.
- trig (optional): one sentence on the immediate trigger.
- src: list of URLs you used (Wikipedia, Britannica, museum or university pages).

## How to verify
Use WebSearch and WebFetch for every date, figure and name; Wikipedia and Britannica first. If a fetch fails, try the Britannica page or another reliable source. Keep the URLs in src.

## Output
A JSON array in the file you are given, saved after every five entries so work survives interruption. When done, check it parses and reply with: count written, any selection entries you changed or dropped and why, and any you could not source.
