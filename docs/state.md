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

## The chain sub chat (2026-11-11): handoff to the master chat

One topic: how an event page shows the chain of cause and effect around its event. It grew
into a rework of the event page. The mock is `docs/design/mocks/event-v12.html`
(https://claude.ai/artifact/Kx3QuaNRt7JLYdqsj1pimc), with the Treaty of Versailles as the
knot. This chat changed no standards doc. Each item names the doc that needs the edit.

### A. Decided by Cade

1. **Page order for every event** (event-pages.md, CLAUDE.md): the bottom line in one
   paragraph; Overview, with its graphic last in the section where there is one; Historical Chain; The Record;
   Meanwhile; the exits. Historical significance, Lasting impact, What caused it, What it
   caused, and Before and after no longer have sections of their own. "What caused it" and
   "What it caused" survive as the labels on the two sides of the chain web.
2. **The heading is "Historical Chain"**, replacing "Follow Historical Chain"
   (event-pages.md, CLAUDE.md).
3. **The chain is a sideways web** (event-pages.md, ui-rules.md): causes run in from the
   left, effects out to the right, one column per step. The reader sets the reach, 1 to 5
   steps, and shows or dims knots, fibres and strands.
4. **Meanwhile is a section on the event page, last**, under the gilt diamond divider
   (event-pages.md). The window of years is still a placeholder (two years in the mock).
5. **One picture per event, as an inset beside the opening paragraph** (event-pages.md,
   which now says "where it earns its place"). The globe still opens the page. The picture
   is a small upright plate at the right of the bottom-line paragraph, which wraps round
   it. Its frame is gilt corners: fine double corner marks set tight to the photograph, and
   a soft shadow that lifts it. One short line of description sits centred under it in
   small italic. On scroll it grows a little as it rises, then eases back and fades; it
   returns when the reader scrolls back. A tap opens its details in the gilt cartouche:
   caption, date, place, source, licence, credit. An event with no usable picture shows
   nothing there.
6. **What a picture may be** (CLAUDE.md hard limits; narrative-flow.md, Pictures):
   - A later drawing or painting is allowed for an event too old for photographs.
   - A photograph of the place or of that kind of scene is allowed.
   - **A photograph of a living person is allowed.** This reverses a hard limit in both
     docs; no such picture ships until they are changed.
   - Pictures come from open sources, as Wikipedia's do, avoiding Wikipedia's own lead
     picture where another serves. Source, licence and credit stay recorded beside the file.
7. **Fewer floating bubbles** (ui-rules.md): a bordered pill with a shadow reads as stock AI
   design. Back, the globe caption and "Also in" are plain type.
8. **The hero** (ui-rules.md): the place is lettered on the globe beside its pin; the
   caption reads "Globe" and the event's year, with no "drag"; the date line carries the
   place ("28 June 1919 · Versailles, France").
9. **"Also in N more stories"** (structure.md, which says "Also in N more"): the count and
   the list are by story, never by chapter. It opens a small sheet in a gilt cartouche:
   stories grouped under their chronicles, a scroll, the reader's own path ticked. Choosing
   a story makes the page follow that path.
10. **Arriving from the globe or the timeline** (structure.md, which says a page with no
    route shows its home path): no chronicle, story and chapter path shows. One line, "Part
    of N stories", opens the same sheet. It stays at the top and never rides in the docked
    header.
11. **Gilt has two new uses** (palette.md, which limits it to headings, tabs and the
    divider): the notched cartouche round the stories sheet and the picture card; and a
    thin gilt rule on graphics and pictures. The outer gilt line is kept light.
12. **The tab row** (ui-rules.md rule 6): a hairline rule sits under it at rest and fades
    out once the row sticks and travels with the page.
13. **The docking title** (ui-rules.md rule 20): it holds its full size for the first part
    of the scroll and shrinks later, so the change no longer starts at once. No small
    picture rides in the docked header.
14. **The chain's one line of directions** is italic, smaller and greyer than body text.

15a. **What an event's graphic is** (event-pages.md, Graphics; sent to the master chat
    after the first handoff). It shows the one change the event turned on, and the reader
    works it: a before-and-after switch and a tap on each part. It sits last in Overview.
    Like the picture it swells a little as it crosses the screen; unlike the picture it
    never fades.
    For a treaty or a conquest: the borders before and after, the land lost, and the
    states that came out of the redraw. For a battle: where it was fought and the lines of
    communication. For a vote: the tally. In the mock: Germany and its neighbours, 1914
    and 1919, drawn from the atlas's own border record, with lost land hatched, new states
    tinted and named, and three figures under it. The reparations bars are folded into
    those figures. Cade also wants the people lost, as a number and a share: the mock
    shows that cell as a placeholder, because no sourced figure is in the project yet
    (open: source Germany's population loss with its basis and range). event-pages.md says the text must say everything a graphic shows; the
    Overview text does not yet name the new states.

15b. **Historical Chain, rebuilt on Cade's brief** (after the first handoff; awaiting his
    read). event-pages.md, ui-rules.md:
    - The controls ride under the tabs while the web is on screen, as the chapter spine
      does on a story page: steps (1 to 5), knots, fibres and strands, and a Filter
      pop-up holding side (causes, both, effects), kind of event, and Backbone only.
    - **Filters now remove and reorganise; they no longer dim.** This reverses ui-rules.md
      rule 9 ("Filters dim, never remove") for the chain. Events that fit grow out of the
      event they join; events that do not fit shrink back into it, and the web re-forms.
    - An event that does not fit but lies on the path to one that does stays as a small
      grey name, so every line drawn is still a row in the link table.
    - A column of more than four events turns like a drum: the row in hand is full size
      and the rest curve away above and below; drag the column or use its two arrows.
    - Lines leave from a port and arrive at a barbed head; a fan of lines spreads along
      the card's edge. A bead runs the lit path once when an event is tapped.
    - A Recentre control returns the view to the centre event.
    - The mock opens with knots and fibres on and strands off.
    - Clean pass (Cade, same day): every event is one card of one size, and the mark alone
      tells knot from fibre from strand. This changes ui-rules.md rule 8, which gives each
      size its own card form. A knot's card carries a gilt top edge. The tapped event gets
      the gilt cartouche, drawn in one stroke as on the tabs. The web sits on the paper
      between two hairlines; the controls are one ruled strip with a gilt line under what
      is on; the small map is a hairline with a tick for each step.

### B. On trial in the mock, for Cade to settle

15. **Square corners everywhere** (ui-rules.md, palette.md). Cade leans this way. The mock
    is squared in one block of styles; round is kept for the globe, the fibre dot, the
    strand ring and the pin. It would change the story and chapter mocks too.
16. **The bottom bar** (Globe, year, search): keep it as a floating pill, or square it.
17. **Graphics on a plate** (event-pages.md, Graphics): a gilt rule, a fine rule inside, a
    slight shadow, static. Cade wants graphics to stand off the page; the treatment is open.
18. (Settled; see item 5.) The mock still carries its trial buttons for other frames and
    placements.
19. **The name "The Record"** for the detail, and its drawers (ui-rules.md rule 19 says no
    gate; its Open list asks for a name to replace "Open the detail").
20. **The docked card in the web** (ui-rules.md rule 3 gives every name the same floating
    preview): here the card docks without a scrim so the web stays in use.
21. **"Backbone" as a toggle** beside the sizes (its design was set for roadmap step 1.6).
22. **Lines the web leaves out**: Coincident links, and links that skip a step or join two
    events of one step, are listed under "How it connects" and never drawn.

### C. Facts for the record

- The mock's sizes are placeholders: old tier 1 as knot, tier 2 as fibre, four events set
  as strands to show the filter. The stories in the sheet are placeholders but one.
- The picture is a public-domain US National Archives photograph of the signing, recorded
  in `docs/design/mocks/versailles-signing-1919.json`. Its licence is as Wikimedia Commons
  records it and is not yet checked against the Archives' catalogue.
- This environment's network now allows commons.wikimedia.org and upload.wikimedia.org.
- The Versailles exits are standard addresses, not yet verified.

Next in this chat: Cade's read of the rebuilt Historical Chain.

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
