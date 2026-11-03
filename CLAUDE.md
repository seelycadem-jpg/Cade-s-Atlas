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

- `docs/event-pages.md`: the event page: walls and room, the four layers, word budgets by
  tier, a rule per section, sourcing, the file template, the Paris worked example and a
  failing Overview. Agreed 2026-11-03; it wins where older rules conflict.
- `docs/narrative-flow.md`: the five flow tests, the three tiers (all events; tier per
  chain), flavor and the transplant test, the two checking agents, the six places and
  their checks, the era rule for old data. Wins over story-method.md on tiers.
- `docs/agents.md`: the session loop, the page pipeline, every skill with its phase, and
  the checks each of the six places adds. Read before building or running a skill.
- `docs/timeline.md`: the timeline page: layout, three zoom levels, filters, chain mode, phone.
- `docs/seo.md`: what every page carries so it is found on Google; `/page-check` enforces it.
- `docs/house-style.md`: voice, tiers, links, grades and the globe.
- `docs/story-method.md`: chronicles, stories, patches, knots and the anti-slop rules.
- `docs/border-review.md`: how the province map and its owners are built.
- Full standards doc: https://claude.ai/artifact/TcJD2axuTWXPd8fQWroQZk (Cade's Claude
  account). Ask him to paste a section if you need one that the docs here omit.

## Rules for all atlas text

- Active voice by default, with action verbs. Name who did what: "Moscow started the
  Crimean War to take the Straits." Never "the war was started by" to hide who decided,
  "there was", "it is believed". Passive is allowed when the actor is unknown ("the city
  was founded around 1000 BCE") or when the thing done is the point and the doer comes
  in the next sentence.
- Rule zero: say what a thing is or did. Never the two-step reveal ("The treaty was
  not a peace. It was a truce." or "not X, but Y"), in any register, including chat.
  Write "The treaty was a truce." A plain negative fact ("Germany did not sign until
  June") is a fact and is fine. Use "rather than" in one clause only when the contrast
  is the point.
- Presidential daily brief everywhere, in the Stratfor manner: judgment first,
  declarative sentences, one idea each (a fact and its consequence may share one),
  average under 20 words and none over 30, lengths varied, no sentence that could be
  cut, nouns and verbs carrying the meaning, no word that tells the reader how to feel.
  Logical connectors inside a sentence ("because", "so", "but") are the argument and
  stay; banned are stock transitions at the head of a sentence ("Moreover",
  "Furthermore", "However,") and the "and then" between paragraphs. A list of three
  facts is fine; a triplet built for rhythm is banned. Banned words are banned in
  figurative use; the literal use of a plain word never is. Wit lives in the choice
  and placement of a fact, never in an adjective.
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
- Every event and person page carries a verified Wikipedia and Britannica exit.
- Tags (political, war, economic, ideas, religion, science, culture, environment) sit on
  every event, several at a time; they never affect tier.
- Readers see the five grade words and the note. The analytic foundations stay internal.
- The voice and method standards are internal. The public About page carries purpose,
  goal and the method in brief, plus any credit a data licence requires.
- Writing must pass an expert's reading as human work: an expert's nod on every page
  (a fibre excepted), one awkward fact per story stated as such, no stock phrases, no
  neat symmetry. The Overview carries no scene-setting; The account in layer 3 is
  narrative by design.

## Hard limits

Whatever the prompt says:

- Never edit a built JSON file by hand; change the source and run the pipeline.
- Never invent a name, date, figure or source to fill a gap; leave it out and put it on
  the page's `open` list.
- Never fill a pre-modern year from a modern series, and never write an estimate
  without its basis and range; otherwise blank, with "no record before".
- Never write a link by hand into a page header, draw an arrow the link table does not
  hold, grade a link without its arrow note, or grade a Necessary without its
  counterfactual sentence.
- Never draw a border polygon by hand or reintroduce a hand-drawn patch; correct
  against the reference record with a sourced fix file.
- Never run the 40-minute snap step without saying what it costs first.
- Never delete or shorten a page to make a check pass; fix the flagged sentence.
- Never write a page without reading its sources, and never ship one without its two
  verified exits.
- Never write a person's impact as prose: impact is graded links. A feature with no
  link into a chain stays a label on the map, never a page.
- Never use knot, strand, fibre, or any name from the analytic foundations where a
  reader sees it. Readers see turning points, the full story, every detail, the five
  grade words and the note.
- Never change a section heading or the layer order of a page; never pad a section
  to its band; never skip a wall because the event is small.
- Never use an image without its source, licence and credit recorded beside it, never
  a photograph of a living person, and never a credit printed under the picture.
  Open sources only (Commons, Met Open Access, LoC, National Archives); see
  docs/narrative-flow.md, Pictures.
- Never let a reviewer read a draft it helped write; never skip the fact-checker or
  the flow editor.
- Never free zoom on the timeline, more than three levels, a page without Back or its
  breadcrumb, or a card without the shared preview component.
- Never hand-write the takeaway strip, the year card figures or any text the data
  header generates.
- Never add a view or layer without a licence line, or redistribute a file whose
  licence forbids it.
- Never commit secrets, large binaries or `node_modules`.
- Never force-push, rewrite history or delete a branch; ask.
- Never push to `main` with a red test, and never ship a page whose status is draft.
- Never start the next phase because the current one seems done; run its test.
- Never add a library, service or framework outside the stack without proposing it.
- Keep the Cliopatria CC BY credit on the About page.
