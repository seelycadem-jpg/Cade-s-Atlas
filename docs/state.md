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

1. **The pages, top down, one chat per page** (Cade, 2026-11-11): chronicle, story,
   chapter, knot, fibre. The master chat keeps the decisions and the docs; a page chat
   builds one mock, works only in its own mock file, and ends by saving to the branch,
   updating this file and listing any question it could not settle for the master chat.
   - Chronicle: no mock exists yet. It is built in the design of `story-v2.html`
     (palette.md, ui-rules.md): a portrait, then its stories by start date (structure.md).
   - Story, chapter and event mocks exist and predate 2026-11-11. Each is brought up to
     structure.md as its turn comes: one fixed size per event with the tooltip text; the
     path ending at the event with its mark; the backbone drawn heavy on a thread; the
     Paris settlement as the chapter The Treaty with the Treaty of Versailles as its knot.
   - Fibre: a shorter event page in the same shape as the knot's.
2. Cade rates about forty anchor events; the reach line is derived from them
   (structure.md). The first five are in `docs/anchors.md`.
3. Design the idea map and the agent loop for idea events (structure.md, Idea events).
4. Phase 1 steps left: front door (1.5), filters (1.6, with the backbone filter), the two
   globes (1.7), building the shared components (1.8 to 1.12), the people test (1.13).

## The chain sub chat (2026-11-11)

One topic: how an event page shows the chain of cause and effect around its event.

Cade's direction:
- The story, chapter and spine work stands. This chat is about the chain on an event page.
- Keep a horizontal web, as Prototype 1 had. The reader filters it by size (knot, fibre,
  strand) and by how many steps out it reaches, 1 to 5.
- A trial page order for every event: one paragraph of bottom line, Overview, a graphic if
  there is one, the chain, then the detail that opens, under a better name.

Built: `docs/design/mocks/event-v12.html`. Cade's first read: the chain is better. Second
pass, awaiting his read: the globe header and cartouche tabs of the last mock are back, and
the web's controls, cards and motion are reworked to a finer finish.
- Causes on the left, effects on the right, one column per step, three columns to a phone
  screen; the web slides sideways and a small map under it shows the whole.
- A tap on an event lights its strongest path to the centre and docks its card: Open the
  page, Centre the web here, and How it connects, with the weakest line named.
- A tap on a line opens its note: claim, strongest objection, verdict.
- The fixed headings "What caused it" and "What it caused" label the two sides of the web.
- Decided by Cade: keep the sideways web; keep the shrinking globe and the cartouche tabs on
  the event page. The rest waits for his read.
- Cade, third note: the floating bubble (a bordered pill with a shadow) reads as stock AI
  design and is to be used sparingly. In the mock, Back, the globe caption and "Also in" are
  now plain type; the hero letters the place on the globe beside its pin; the caption no
  longer says "drag".
- "Also in N more chapters" opens a sheet: every place the event sits, grouped by chronicle
  under sticky headings, a find box past eight rows, the reader's path ticked, and a scroll.
  Choosing a row makes the page follow that path. Built for 25 places with placeholder rows.
- Cade, fourth note (decided): the plain-type hero is good; the globe caption reads "Globe
  1919", the event's year (the borders are cut at mid-1919); the places stay grouped by
  chronicle; the soft shadow on the content cards stays. The places sheet is smaller and
  sits in a gilt cartouche with notched corners, drawn in one stroke as on the tabs.

Next in this chat: rework the look of the Historical Chain section (Cade, 2026-11-11).

Questions for the master chat (none settled here; no standards doc was changed):
1. The page order. The mock follows Cade's trial order, which differs from the order agreed
   2026-11-08 in event-pages.md. Historical significance, Lasting impact, What caused it,
   What it caused, and Before and after have no section of their own in it.
2. The name of the opening detail. The mock uses "The Record", with one drawer per
   question and its answer in a line when shut. ui-rules.md rule 19 says no gate.
3. The preview card. ui-rules.md rule 3 gives every name the same floating preview. In the
   web, the card docks under the map without a scrim, so the web stays in use.
4. The backbone filter. The mock carries a "Backbone only" chip; its design is set for
   roadmap step 1.6.
5. Coincident links are left off the web and listed under "Other lines" for the event.
6. The web draws a line only between neighbouring steps. A link that skips a step, or runs
   between two events of one step, is listed under "Other lines" and is never drawn.
8. The bubble. Cade wants fewer floating pills. The bottom pill (Globe, year, search) is the
   one left on the page and is a decided element (palette.md); whether it keeps that form is
   his call in the master chat. ui-rules.md has no rule on it yet.
11. Corners. Cade leans toward few or no rounded corners across the atlas, for a sharper,
    more cartographic look (2026-11-11). In the mock only the places sheet is squared so
    as a trial: the whole of event-v12.html is squared (one block at the end of its
    styles, easy to lift out), with round kept for the globe, the dot, the ring and the pin. A site-wide rule belongs in
    ui-rules.md and palette.md, and touches the story and chapter mocks too.
12. The heading. Cade renames "Follow Historical Chain" to "Historical Chain" (2026-11-11).
    The mock carries it; event-pages.md and CLAUDE.md fix the old words and need the change.
13. Graphics. On trial in the mock: a graphic sits on a plate (a gilt rule, a fine rule
    inside it, a slight shadow), static, and kept apart from the notched cartouche. Cade
    wants graphics to stand off the page; the exact treatment is still open.
14. Meanwhile on the event page. On Cade's ask the mock has a Meanwhile section and tab,
    last on the page, after The Record (Cade, 2026-11-11): events within two years, each with its line to this
    event or "no line". event-pages.md has no such section; the window (two years) is a
    placeholder.
15. The tab row. On trial: a hairline rule under the row at rest, in place of a shadow. Once
    the row sticks and travels with the page the rule fades out and the soft fade takes
    over (Cade, 2026-11-11; ui-rules.md rule 6).
16. Arriving with no path (Cade, 2026-11-11). A reader who opens an event from the globe or
    the timeline sees no chronicle, story and chapter path: only "Part of N stories", which
    opens the same sheet. The line stays at the top of the page and never rides in the
    docked header. structure.md says a page with no route shows its home path, so
    that line needs changing.
17. Stories, never chapters (Cade, 2026-11-11). The line reads "Also in N more stories" and
    the sheet lists stories under their chronicles. In the mock each story's row still
    names the chapters in small type, so the reader lands at the right one.
18. The event's picture (Cade, 2026-11-11). Decided by Cade: one picture per event, at the
    top above Overview; the globe still opens the page; the picture fades as the reader
    scrolls and comes back; it has a short description; a tap opens its details in the gilt
    cartouche; an event with no usable picture shows nothing there. Pictures are chosen
    from open sources as Wikipedia does, avoiding Wikipedia's own lead picture where another
    serves. In the mock: a plate between the title and the bottom line with one italic line
    under it; it returns when the reader scrolls back up (a small copy in the docked header
    was tried and withdrawn as clutter); the details card shows caption, date, place, source, licence and credit.
    The picture is a US National Archives photograph of the signing (public domain),
    recorded in `docs/design/mocks/versailles-signing-1919.json`. A mock switch still
    cycles the three placements. event-pages.md says "one picture or visual where it
    earns its place"; a picture on every event changes that line.
20. Frames for pictures, on trial. A mock button cycles five: double gilt, mount, gilt
    corners, ink rule, bare. Cade to choose; palette.md then needs the line.
21. The title's docking. On Cade's note that the change felt rushed, the title now holds its
    full size for the first 45 percent of the scroll and shrinks over the rest; the path
    fades a little later. The globe's shrink is unchanged. The title still docks at the
    same point, because it must dock when it reaches the top of the screen.
22. What a picture may be (Cade, 2026-11-11). A drawing or painting made later is fine for
    an event too old for photographs. A photograph of the place or of the kind of scene is
    fine too (his example: a picture of Trafalgar Square for protests there). Photographs
    of living people are allowed (Cade, 2026-11-11). This reverses a hard limit: CLAUDE.md
    and docs/narrative-flow.md (Pictures) still say "never a photograph of a living
    person", and the master chat must change both before any such picture ships. The
    open-licence rule and the recorded source, licence and credit still apply. The caption must say what the picture is and when it was
    made, so a later painting is never read as a record of the day.
19. This environment's network now allows commons.wikimedia.org and upload.wikimedia.org
    (Cade approved, 2026-11-11), for fetching open-licence pictures.
10. Gilt. palette.md limits gilt to the heading stroke, the tabs and the divider diamond. On
    Cade's ask the places sheet now carries a gilt cartouche too; palette.md needs the line.
9. Superseded by question 17: the sheet now counts stories.
7. The mock's sizes are placeholders: old tier 1 as knot, tier 2 as fibre, four events set
   as strands to show the filter.

## Added to the roadmap (Cade, 2026-11-11)

- Phase 14: accounts (game scores through the year, saved pages), and a daily or weekly
  email whose content and rhythm are still Cade's to decide (step 14.8).
- Step 10.5a: "Report a problem" by email on every page, at launch, with no account.
- The services these need are outside the stack and wait for a proposal (step 14.2).

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
