# Meanwhile Atlas

A public website, usable on a phone browser, that connects human history through
narrative, a living globe, themes and a timeline. It is for the curious: people who
want to know how humanity's story fits together.

## Current goal

Rebuild the app from scratch. Keep the data and the pipeline. Top-tier UI is the key
measure: a curious person should be able to open it and click around. A daily
Wordle-style history game comes later and is what brings readers back. The quiz stays
deferred until the link and arrow-note work ships.

## The owner

Cade is new to Git and GitHub. Explain Git steps in plain words, and commit working
pieces often with clear messages. Work on a branch for anything risky.

## Repo layout

- `site/`: last published atlas. `index.html` is the old app; treat it as reference
  and write the new app separately.
- `site/data.json`: 781 events plus threads, bands, regions and arcs. `graph.json`
  holds links and stories.
- `site/maps/`: borders and the province map. See `docs/border-review.md`.
- `pipeline/`: build scripts. Read `pipeline/README.md`; the scripts are still missing
  until it is deleted.
- `docs/`: the standards below.

The old app loads D3 7.9.0, topojson-client 3.1.0 and MapLibre GL 5.24.0 from CDNs.

## Read before writing atlas text

- `docs/event-pages.md`: event pages and writing rules for this build. Agreed
  2026-11-02; it wins where older rules conflict.
- `docs/house-style.md`: voice, tiers, links, grades and the globe.
- `docs/story-method.md`: chronicles, stories, patches, knots and the anti-slop rules.
- `docs/border-review.md`: how the province map and its owners are built.
- Full standards doc: https://claude.ai/artifact/TcJD2axuTWXPd8fQWroQZk (Cade's Claude
  account). Ask him to paste a section if you need one that the docs here omit.

## Rules for all atlas text

- Rule zero: never write the negation-then-reveal ("It did not X. It Y'd." or "not X,
  but Y"), in any register, including chat. State what a thing is or did. Use "rather
  than" in one clause only when the contrast is the point.
- Presidential daily brief everywhere: short declarative sentences, one fact or
  judgment each, none over 25 words, no sentence that could be cut.
- The themes layer alone ("Man and Power" and the rest) is written like Cicero and may
  ask questions in the prose.
- Event pages open with an Overview: the so-what in hard facts, in 2-3 short paragraphs.
- Name actors with role and name on first mention (German Chancellor Olaf Scholz).
- Name no academics, historians, authors or schools in product text. Give the facts and
  the judgment.
- Use plain literal verbs. No idioms, cliches or figurative phrases.
- Include no invented specifics. Leave out any name, date or figure that cannot be
  sourced.
- Readers see the five grade words and the note. The analytic foundations stay internal.
- The voice and method standards are internal. The public About page carries purpose,
  goal and the method in brief, plus any credit a data licence requires.
- Writing must pass an expert's reading as human work: expert-level specifics, one
  awkward fact per story, no stock phrases, no neat symmetry.

## Hard limits

- Do not reintroduce hand-drawn map polygons. Border corrections go against the
  reference record.
- Use no photos of real people.
- Keep the Cliopatria CC BY credit on the About page.
