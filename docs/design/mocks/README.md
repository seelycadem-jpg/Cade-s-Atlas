# Design mocks

Tap-through pages for Cade to judge on a phone. Each is a single HTML file, published as a
private page on claude.ai for review and kept here for the record. They are mocks: the
text comes from `docs/event-pages.md` (the Paris worked example) and the preview lines
are plain sentences for the mock, never atlas content.

| File | Step | Published |
| --- | --- | --- |
| `1.3-directions.html` | 1.3 Design directions: the Paris event page in three directions (Engraved, Night chart, Daylight), light and dark, with the preview card and the navigation bar | https://claude.ai/artifact/6PqwkJNYiCVYP1nYhsHR6C |
| `1.3-event-v2.html` + `atlas-data.js` | 1.3 second pass, after Cade's notes on the first: Direction B rebuilt. The globe (the atlas's own land outline) dimmed behind the hero; the ladder (chronicle, story, turning point, strands); the Overview with its first paragraph as the lede; a live chain over the 36 real German Question links with plain phrases per grade, time running down, tap an arrow for its claim and objection, tap + on any card to re-centre; links coloured by kind; a floating pill (Globe, year, search) in place of the bar. `atlas-data.js` is read-only data drawn from `site/` for the mock | https://claude.ai/artifact/MzvW4s52BgBSfF8ZaZJUGr |
| `1.3-event-v3.html` + `atlas-data.js` | 1.3 third pass, after Cade's second round: the 1919 borders on the hero globe (from `site/maps/cs.json`, slimmed by `build-borders-1919.cjs`), Germany lit; the kicker in place of the ladder; no size word on the event, size as marks (filled, ring, dot) with the depth words Main events / The full story / Every detail; no gate: four visible layers with an index; the strongest arrows under the title; the chain last with the strands as "Inside this event"; a sticky title and small globe that turn to whatever is tapped, hover or tap to grow | https://claude.ai/artifact/5MBXLLTSQzpvwm6N1Bxipu |
