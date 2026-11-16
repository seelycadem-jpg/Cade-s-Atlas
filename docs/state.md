# Where the atlas stands (read this first in any new chat)

Updated 2026-11-11. The one page that says what has been decided, where it lives and what
comes next. CLAUDE.md holds the rules; this file holds the state. Update it at the end of
every working session.

## The project in one paragraph

Meanwhile Atlas is a phone-first public website that connects human history through cause
and effect: chronicles, stories, chapters and events, a living globe, a timeline, and later
a daily game. Cade owns it and is new to Git; explain each Git step in plain words. The old
site in `site/` is Prototype 1, reference only. The new app is built in `app/` (Astro),
deployed to https://cade-s-atlas.seelycadem.workers.dev by GitHub when a pull request is
merged into `main`.

## Phase

Phase 0 (foundation) passed 2026-11-05. Phase 1 (look and feel) is in progress: design
mocks, judged on Cade's phone. Steps are in `docs/roadmap.md`; status in `docs/plan.md`.

## Decided (all 2026-11-08 unless dated)

**Structure** (`docs/structure.md`, picture: `docs/design/structure-map.html`)
- Four levels: chronicle, story, chapter, event (Cade, 2026-11-11; replaces "six levels").
  A chronicle is any long subject that needs several stories: a place or people, a system
  or idea, an age or contest (Germany, Capitalism, The Second World War).
- Three sizes of event, rated once by impact on world history and fixed on every page:
  knot, fibre, strand. Reach is counted in people of the
  event's own connected world, never in countries. Two guard rails: an audit of knots
  against each region's share of people (never a quota), and chronicles planned the same way.
- A chapter is a stretch of a story in which one thing changes; any number of knots,
  including none. Links, never dates alone, put an event in a chapter.
- Sizes have plain definitions, tooltips and a three-step method with a recorded defence
  (structure.md). An event is one happening with one outcome; the Paris settlement becomes
  a chapter with Versailles as its knot (mock and worked example to rework).
- The globe shows each region's biggest events for the years in view: knots first, then a
  fibre or strand where a region has no knot. Sizes never change to fill the map.
- A strand is an event in its own right: it changed the course of a city, an institution
  or a movement.
- What a chapter turns on comes from link grades (Necessary or Sufficient): drawn heavy on
  the thread and filterable; the control is designed in step 1.6.
- People: a life ("Follow this life", on the shared year cursor), a card, or a name; links
  decide, never fame or a quota. A gap in the record can be true and stays.
- Dynasties are told inside stories; no dynasty chronicle is planned.
- Event pages may carry a graphic where it beats prose (a vote tally, a comparison), knots
  first and few: `docs/event-pages.md`, Graphics.
- Themes are built after V1.0 (roadmap 8.8, 8.8a, 9.8 moved); direction in structure.md.
- Idea events (a thinker's great work) are in V1.0: an idea map on the page, a higher
  writing bar and their own agent loop, all still to be designed.
- The 781 old events and their tiers are placeholders; all are rated afresh.
- A chapter has its own page: a longer briefing and the thread of its events. Its patch is
  the short form on the story page.
- No caps: a chapter holds as many knots as it needs, a story as many chapters.
- One event, one page, listing every chapter it sits in. Context lives on the chapter.
- Titles in title case; the First World War is The Great War.

**Look** (`docs/design/palette.md`, `docs/design/ui-rules.md`)
- The red thread: one red (`#C81A12`, warmed to `#FF6B5C` in dark) for the chain only.
- Light: warm paper, warm-black body text, espresso titles. Dark: espresso ground, cream.
- The briefing opener: title face (EB Garamond) a size up, in a lighter espresso.
- Links: ink with a thin red underline, red on tap. No colour by kind.
- Gilt: a tapered, fading hairline under section headings, and the divider diamond only.
- Type: EB Garamond for titles and labels, Newsreader for reading, Public Sans for controls.
- Marks: diamond (knot), filled dot (fibre), open ring (strand).

**Motion** (`docs/design/ui-rules.md`, rules 6, 8, 12, 20)
- Scroll effects run on the browser's scroll timeline, only change transform and opacity,
  and are measured at phone speed before they ship.
- The title rides the page and docks into a three-line header: title, years, parent and Next.
- Sticky bars end in a soft fade while stuck; layers run header, tabs, spine.
- Chapters: the one being read at full size, the rest smaller and lighter; edge chapters
  recede only as the reader leaves them.
- The chapter spine (rule 8): a red line fills to the chapter in view and a soft box sits
  behind it, sized to its whole title. When chapters do not fit, the row slides, starting
  at the left edge, with arrows below that move it three chapters. The spine fades and slides
  up under the tabs as the last chapter ends, so it is gone before Meanwhile.
- Section tabs (`palette.md`, gilt): the selected tab draws a gilt cartouche (0.8 s), grows
  to 105 percent while the others shrink to 94, and Chapters shows a count ("1 of 5"). A
  frame that tracked the scroll was tried and dropped. Each page ends with just enough room
  for its last section to be selected.
- On the story page a chapter's title opens its chapter page; a small "Read the chapter ›"
  sits at the end of its paragraph.

**Writing** (CLAUDE.md, `docs/house-style.md`): active voice, the PDB register, no hedges,
no invented specifics, title case for titles.

## The mocks to open on a phone

| Page | Link | File |
| --- | --- | --- |
| Story: Weimar Germany | https://claude.ai/artifact/AWaup7weY8H6EUwNDCXS37 | `docs/design/mocks/story-v2.html` |
| Chapter: The Ruhr and the Mark | https://claude.ai/artifact/5SyFXi5sACFqRQe6zcvmyW | `docs/design/mocks/chapter-v1.html` |
| The six levels (retired 2026-11-11; the structure map replaces it) | https://claude.ai/artifact/Y9GbTwZBYFKiwvCfbqhpku | `docs/design/levels-chart.html` |
| Structure map: four levels, three sizes (2026-11-11) | https://claude.ai/artifact/52xBGzcx6DQn8kaoyhG5f5 | `docs/design/structure-map.html` |
| Spine test, twenty chapters | https://claude.ai/artifact/GS6K2eL7M9fe2QA6VxQWpi | `docs/design/mocks/spine-test.html` |
| Event: The Paris Peace Settlement | https://claude.ai/artifact/MdJzwkT1viFnjFEdqqcaaP | `docs/design/mocks/event-v11.html` |
| Event with the chain web: The Treaty of Versailles (first demo, 2026-11-11) | https://claude.ai/artifact/Kx3QuaNRt7JLYdqsj1pimc | `docs/design/mocks/event-v12.html` |

The artifacts are private to Cade's account. The repo files are the source of truth.

## Next, in order

1. **The chronicle, story and chapter pages, redone in the event page's design** (Cade,
   2026-11-17), one sub chat per page. Each builds from `docs/design/page-system.md` and
   `docs/design/mocks/event-v12.html`, and keeps the shared parts (the hero and its ladder,
   the tab row, sheets, Meanwhile, the plus sign, type, links, gilt) identical to the event
   mock. A change to a shared part is proposed to the master chat, never made in one page.
   - Chronicle: `docs/design/mocks/chronicle-v1.html` (new). Germany.
   - Story: `docs/design/mocks/story-v3.html`. Weimar Germany, 1919 to 1933.
   - Chapter: `docs/design/mocks/chapter-v2.html`. The Treaty, whose knot is the Treaty of
     Versailles, so the four mocks link top to bottom.
   - Each chat keeps its notes in `docs/design/notes/<page>.md` and works only in its own
     mock file. The event sub chat continues in `event-v12.html` and
     `docs/design/event-page-log.md`.
   - Fibre: a shorter event page in the same shape as the knot's, after these.
2. Cade rates about forty anchor events; the reach line is derived from them
   (structure.md). The first five are in `docs/anchors.md`.
3. Design the idea map and the agent loop for idea events (structure.md, Idea events).
4. Phase 1 steps left: front door (1.5), filters (1.6, with the backbone filter), the two
   globes (1.7), building the shared components (1.8 to 1.12), the people test (1.13).

## The event page and the design system (2026-11-17)

Cade and the event sub chat reworked the event page between 2026-11-11 and 2026-11-17; the
mock is `docs/design/mocks/event-v12.html` (https://claude.ai/artifact/Kx3QuaNRt7JLYdqsj1pimc).
- **`docs/design/page-system.md` is the design standard** every page chat builds from: what
  carries to every page, what belongs to the event page, the grades, what is on trial.
- The decided rules are written into the standards docs (see that file's status note).
- The working log behind it is `docs/design/event-page-log.md`.
- Sufficient is withdrawn as a grade; the backbone is the links graded Necessary. The six
  pilot links graded Sufficient are regraded when the links are rewritten (Phase 8).
- Page chats keep their notes in `docs/design/notes/<page>.md`, never in this file, so two
  chats never edit the same lines. The master chat keeps this file.

## Added to the roadmap (Cade, 2026-11-11)

- Phase 14: accounts (game scores through the year, saved pages), and a daily or weekly
  email whose content and rhythm are still Cade's to decide (step 14.8).
- Step 10.5a: "Report a problem" by email on every page, at launch, with no account.
- The services these need are outside the stack and wait for a proposal (step 14.2).

## Growth (Cade, 2026-11-16)

- `docs/seo.md`, Growth: year pages, On this day pages, every word in the HTML, question
  titles, Cite this page, embeddable graphics, the About page naming the editor, and a
  hard list of tactics never used. Roadmap 1.5a (year page mock), 10.5b, 10.5c.
- `docs/marketing.md`: a draft launch and social plan (X, Instagram, Facebook, TikTok),
  with five decisions for Cade. Roadmap 10.10 and 10.11.

## Sources (Cade, 2026-11-16)

- Every event page shows a Sources list; every hard figure and quotation is a tap to its
  source; cause and effect rely on the link note (event-pages.md, Sourcing).
- Primary record first for terms, dates and quotations; scholarship for interpretation;
  Wikipedia never cited.
- No source is cited unread: a finder fetches and quotes, a script resolves, an
  independent verifier passes it, and Cade audits a share by hand (agents.md, Source
  verification; a new hard limit in CLAUDE.md).

## Desktop (Cade, 2026-11-08)

Phone first, desktop second, and the desktop is designed, never the phone layout stretched
(roadmap step 1.7a). Direction agreed with Cade:
- The globe takes a much larger share of the page, on the right, and turns to the chapter
  or event in view. The reading shifts to the left.
- The reading column stays about 65 characters wide; the spare width carries the tools.
- Meanwhile runs as a side column beside the briefing instead of a section below it.
- The chapter spine becomes a vertical rail.
- Still open: how preview cards open on a wide screen (a side panel is the first idea);
  decided when the step comes.

## Open questions and loose ends

- The mock data still carries the pilot's old story names (The split, The settlement, The
  void, The collapse, The division). Only names that clearly match a new story are mapped on
  the event page; the rest wait for the data rebuild in Phase 2.
- The event page's Wikipedia and Britannica links come from the earlier mock and are not
  re-verified in this session.

- The Versailles mock's Wikipedia and Britannica links are standard addresses, not yet
  verified.
- The Ruhr chapter's Wikipedia and Britannica links are standard addresses, not yet
  verified (the build session could not reach either site).
- Links between events inside a chapter are not graded yet (Phase 8), so the chapter
  thread shows them as dotted "order in time".
- The site's name: Worldspan is pencilled, not decided.
- The "Theme" pill on the mocks is a mock-only control.

## How the work is saved

All work is on the branch `claude/epic-sagan-y62xj8` and reaches `main` when Cade merges a
pull request. A session that starts from `main` sees only what has been merged.

To update a published mock from a new chat, give it the artifact link from the table above;
it reads the page first and republishes to the same link.
