# Meanwhile Atlas

A public website, usable on a phone browser, that connects human history through
narrative, a living globe, themes and a timeline. It is for the curious: people who
want to know how humanity's story fits together.

## Current goal

Build the real atlas from scratch. The site in `site/` is Prototype 1: finished,
frozen, and raw material only. Every page, brief and screen is rewritten; the pipeline
and the map data are kept. Top-tier UI is the key measure: a curious person should be
able to open it and click around, on a phone first. A daily Wordle-style history game
comes last and is what brings readers back. The quiz stays deferred until the link and
arrow-note work ships.

The build plan, the stack and the agent workflow are in the "Meanwhile Atlas: Build
Plan" doc in Cade's Claude project; the phase in progress is named in `docs/plan.md`.

## The owner

Cade is new to Git and GitHub. Explain Git steps in plain words, and commit working
pieces often with clear messages. Work on a branch for anything risky.

## Repo layout

- `site/`: Prototype 1, the last published atlas. Reference and data source only;
  never edit it. The new app is written in `app/`, the content in `content/`.
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

- Active voice with action verbs. Name who did what: "Moscow started the Crimean War
  to take the Straits." Never "the war was started by", "there was", "it is believed".
- Rule zero: say what a thing is or did. Never the negation-then-reveal ("The treaty
  was not a peace. It was a truce." or "not X, but Y"), in any register, including
  chat. Write "The treaty was a truce." The first sentence of the banned shape makes the
  reader hold a wrong idea so the second can correct it. Use "rather than" in one
  clause only when the contrast is the point.
- Presidential daily brief everywhere, in the Stratfor manner: judgment first, short
  declarative sentences, one fact or judgment each, none over 25 words, no sentence
  that could be cut, nouns and verbs carrying the meaning, no word that tells the
  reader how to feel.
- The themes layer alone ("Man and Power" and the rest) is written like Cicero: it may
  ask real questions, address the reader and take a style of its own. Rule zero holds.
- Event pages open with an Overview: the so-what in hard facts, in 2-3 short paragraphs.
- Name a person with role and name on first mention (German Chancellor Olaf Scholz). A
  government may act under its capital or seat when that is the actor: Moscow, London,
  the Porte.
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

Whatever the prompt says:

- Never edit a built JSON file by hand; change the source and run the pipeline.
- Never invent a name, date, figure or source to fill a gap; leave it out and queue it.
- Never draw a border polygon by hand or reintroduce a hand-drawn patch; correct
  against the reference record with a sourced fix file.
- Never run the 40-minute snap step without saying what it costs first.
- Never delete or shorten a page to make a check pass; fix the flagged sentence.
- Never write a page without reading its sources.
- Never use a photo of a real person or an image without a licence.
- Never commit secrets, large binaries or `node_modules`.
- Never force-push, rewrite history or delete a branch; ask.
- Never push to `main` with a red test.
- Never start the next phase because the current one seems done; run its test.
- Never add a library, service or framework outside the stack without proposing it.
- Keep the Cliopatria CC BY credit on the About page.
