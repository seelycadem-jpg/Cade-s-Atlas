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
    RULE (Cade, 2026-11-12), for the master chat to write into event-pages.md, Graphics:
    every graphic carries a title that says plainly what it shows: whose, what, and the
    span or comparison. "Germany's borders before and after the Great War", never
    "Germany and its neighbours". A reader who sees only the title knows what the graphic
    is. The mock's map now carries that title. Its year switch is red (Cade, same day),
    a step outside the palette note that keeps red for the chain; the map already uses
    red for the land lost.
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
      size its own card form. The tapped event gets one thin gilt line round its card
      (a cartouche round the card was tried and withdrawn; the cartouche stays for pop-ups). The web sits on the paper
      between two hairlines; the controls are one ruled strip with a gilt line under what
      is on; the small map is a hairline with a tick for each step.
    - Second clean pass (Cade, same day). The gilt top edge on knots is withdrawn ("only
      some have this weird gold line"). Every event is the same labelled card: a date line
      with the mark, a hairline, then the title; the centre event's date line is red.
      A ruler sits over the web: an arrow at each end counts the events off screen that
      way ("2 more"), and a scale between them shows every step with the part in view
      marked. The column headers read "Cause · 1 step" and "Effect · 1 step"; the words
      "What caused it" and "What it caused" no longer appear on the page. Recentre is an
      icon in the controls. The key is three lines (knot, fibre, strand); line styles are
      explained in each line's note. The pop-up for a tapped event, and every sheet, sit
      in the gilt cartouche; the pop-up states the relation in one sentence generated
      from the grade ("The Treaty of Versailles was one cause of it among several.").
    - Third pass (Cade, same day). The whole instrument (controls, ruler, web, key) sits
      in one full-width band with a hairline above and below and a faint tint, the colour
      of the globe's sea. A column shows three events; a longer one turns, with a faded
      sliver and an arrow that counts what is above or below ("2 more"). Selecting an
      event turns any column on its path so the path is in view. The controls and the key
      are smaller and tighter.
    - Scrolling (Cade, same day). A long column is now a real scrolling list laid over
      its cards, so it moves with the phone's own momentum, snaps to a row, and hands the
      scroll on to the page at its ends. The arrows with their counts stay as a second
      way. Moves made with a button (the ruler's arrows, Recentre, a column's arrow) glide
      with weight: quick to start, slow to settle, longer for a longer move. The feel on a
      phone is not yet judged by Cade.
    - Kinds (Cade, same day; published). Every card carries a small line icon for each of
      its kinds, two at most, grey by default; the kind being filtered for shows dark. An
      event the filters leave out but the path runs through stays a full card and fades
      back; the small grey names are withdrawn. The card's top line shows the year only;
      the full date is in the pop-up, which also lists the kinds in words. Cade approved
      the idea and asked for icons that are the atlas's own. The second set is drawn as the
      signs in an old atlas's key: crown (political), crossed swords (war), cash coin with a
      square hole (economic), open book (ideas), domed shrine (religion), dividers
      (science), amphora (culture), mountains over water (environment). Fine line work with
      one small inked detail.
      Cade rejected that set: the lines were too heavy and the look "bubbly", like every
      other icon set. He asked for five designs for each kind to choose from, with thinner
      lines, the atlas's own look, and small details. The chooser is
      `docs/design/mocks/kind-icons.html`: forty signs, five for each kind, drawn with
      hairline pen strokes and square joins. Three ways to draw them: Engraved (small
      details and engraver's hatching for shade), Fine (details, no hatching), Solid
      (filled shapes). Two colours: ink or gilt. The card-size copy is 15px, two more than
      the event mock uses, so the thin lines hold.
      DECIDED (Cade, 2026-11-11): pillared hall (political), crossed swords (war), coins
      (economic), open book (ideas), sacred flame (religion), telescope (science), lute
      (culture), tree (environment), drawn Fine, in gilt. The event mock now carries these
      at 15px on the cards, in the filter list and in the pop-up; the kind being filtered
      for turns ink and heavier. Two cautions put to Cade: gilt on the card ground has a
      contrast near 3 to 1, the floor for a graphic, and hairlines make it fainter; and the
      pillared hall leans classical and Western.
    - Kinds, two facts for the master chat. (1) The eight signs match the fixed list in
      CLAUDE.md and docs/narrative-flow.md, but `site/data.json` uses seven: no event of
      the 781 carries `environment` (political 516, war 287, economic 144, ideas 63,
      science 58, religion 53, culture 21). (2) Political sits on 516 of 781 events, so its
      sign will show on about two cards in three and tells a reader little. Question: when
      the old data is re-tagged, does environment get its events, and should a card show
      the political sign only where no other kind applies?
    - The pop-up on a tapped event, reworked (Cade, 2026-11-11). It now reads top to bottom:
      size, year and step; the title and kinds; the event's one-paragraph brief cut to three
      lines with "… more" to open the rest in place; a "Caused by" row and a "Led to" row
      listing the event's own direct lines from the link table (grade mark, name, year;
      three at most, then "N more" into How it connects; Coincident lines left out); then
      one labelled line for its part in the event the page is about. Tapping a name in
      either row moves the pop-up to that event, so a reader can walk the chain one step at
      a time without closing it. The briefs are the Prototype 1 text from `site/data.json`,
      loaded whole from the new `event-v12-briefs.js` because `atlas-data.js` cuts them at
      220 characters; they await the rewrite.
      A second pass that drew the block as a small left-to-right flow (causes, a box for
      this event, effects, an arrow per line) was rejected by Cade the same day and rolled
      back to the two rows. He still finds cause and effect hard to see; what he wants
      instead was this (Cade, with a phone screenshot, 2026-11-12): he likes the two rows;
      each row needed an arrow at its right end that opens the note on that line (the
      claim, the strongest objection, the verdict), because the way to that pane was hard
      to find. Built: every "Caused by" and "Led to" row now ends in a chevron and opens
      its note. A row no longer moves the pop-up to the other event; tapping that card in
      the web does. "You are reading this event." is set in italics.
      Then (Cade, same day): in the note, the two event names in the title are links; a tap
      closes the note and moves the pop-up and the web to that event.
      The buttons of every gilt sheet (the note, How it connects) now sit in a footer under a
      rule, outside the scrolling text, as two equal squared buttons; on a long note they
      had run into the bottom of the frame.
      The note's head, by Cade's direction: the title comes first, its arrow drawn in the
      line's grade (solid, dashed, dotted) as on the web; the grade, confidence and years
      sit in one line under it. Scrolled text stops short of the gilt line at the top.
      The plain sentence under it names both events in place of "the first" and "the
      second" (Cade): "The Russian Revolution was one cause of Hitler Takes Power among
      several." It is generated from the grade, never hand-written, and set in italics.
      Trimmed (Cade, 2026-11-12): the line on the event's part in the page's event shows
      only for a path of two lines or more, since one line is already a row above it; a
      "Caused by" or "Led to" row with nothing in it is left out; events that share only the
      same years get one line that opens How it connects.
      Fault fixed (Cade's screenshot, 2026-11-12): with the synopsis opened on a long
      event, the whole pop-up scrolled and "Open the page" slid out under the gilt frame.
      The pop-up now has the same build as the sheets: the frame stays still, only the text
      scrolls, and the buttons sit in a footer. Long names in the rows wrap in place of
      being cut with dots.
      DECIDED by Cade (2026-11-12), for the master chat to write into house-style.md line
      106 and to apply when the verdicts are rewritten: a verdict no longer ranks the
      causes. His reason: the rank is arbitrary, and the reader can see the other causes
      listed in the chain. The mock now shows them in the note of a Contributing line,
      under "The other causes of X", read from the link table, each row opening its own
      note. Follows from it: a cause a verdict names that has no event (for example "elite
      co-option") must become an event with a link or be dropped. The verdict text itself
      is data and is unchanged in the mock, so the old ranks still show there.
      DECIDED by Cade (2026-11-12): the note shows no Verdict section. It reads: the
      title with its graded arrow; the grade, confidence and years; the plain sentence; the
      other causes where the table holds them; The claim; The challenge (renamed from "The
      strongest objection"). The grade line and the plain sentence are the verdict. The
      mock no longer prints the verdict text; the data still holds it.
      Two things this leaves for the master chat. (1) CLAUDE.md says the Argument "states
      the verdict first, the challenge second" and that no Necessary is graded without its
      counterfactual sentence. In the pilot that sentence lives in the verdict text, so it
      must move into the claim or the reader loses it. (2) The verdict text is also where
      the atlas says why the challenge does not overturn the grade; with it gone, the
      claim has to carry that.
      DECIDED by Cade (2026-11-12): neither the claim nor the note names the other causes
      of a Contributing line. The chain shows them, and an event may have twenty or more.
      The "other causes" list is withdrawn from the note. Pattern for the rewritten text,
      agreed in drafts: The claim says what happened, in order, and for a Necessary or
      Sufficient line ends with what would be missing without the cause. The challenge
      states the strongest case against and ends with one sentence on what it does and
      does not change. No verdict section, no rank, no list of other causes.
      Consequence: the chain is now the only place a reader sees the other causes, so every
      cause the atlas relies on must be an event with a link.
      FINAL (Cade, 2026-11-12), replacing the two-part pattern above: a note has three
      parts, each with one job. The claim: what the atlas says happened; a Necessary or
      Sufficient line ends with what would be missing without the cause. The challenge: the
      strongest case against, and nothing else. The verdict: one or two sentences answering
      the challenge, saying why the grade stands or what the challenge cost it. The verdict
      carries no rank, no list of other causes and no repeat of the grade words. A line
      with little or no challenge shows the claim alone: no challenge section and no
      verdict (never manufacture a fact against). The mock prints the verdict again and
      hides both sections where a line has no challenge. The old verdict text in the data
      still carries ranks; Cade accepts that until the rewrite removes them.
      Header (Cade, 2026-11-12): the place stays beside the date when the title docks
      ("28 June 1919 · Versailles, France"); it used to fade out with the path line.
      Count for the master chat: of the 18 Contributing lines in the pilot, 10 have another
      cause of the same event in the link table and 8 have none. For those 8 (May Fourth
      is one) the reader sees "one cause among several" and no other cause anywhere but in
      the verdict's words. Dropping the list from the verdict is safe only once each of
      those causes is an event with a link.
      Background, as first recorded: the verdict on a Contributing line
      ranks the causes ("Versailles (second), Bolshevik fear (third)"). Cade finds the rank
      arbitrary and wants it gone. house-style.md line 106 requires it ("Contributing names
      the set and A's rank"); 18 of the 36 pilot verdicts do it. This chat's view: keep
      naming the set, which is the test for a Contributing grade, and drop the rank, which
      has no stated method. Some sets also name causes the link table does not hold (for
      example "elite co-option"), which a reader cannot follow anywhere. Not changed in the
      mock: the verdicts are data.
      Question for the master chat: event names that are phrases with a verb ("Hitler Takes
      Power") read stiffly inside this sentence; should each event carry a short noun form?
    - Fault fixed: a phone fires a resize each time its address bar hides or shows, and
      the web rebuilt itself on every one, jumping back to the centre and resetting any
      turned column, so events seemed to vanish. It now rebuilds only when the width
      changes and keeps the column in view. A test of 140 random taps, filter changes and
      height changes found no event missing afterwards.

- **The Record, second pass** (Cade, 2026-11-12; on trial). The Record is a plain list of
  its pieces: each shows its heading and one line saying what is inside, closed by default,
  and opens in place. One piece is open at a time; the open one's heading turns red and its
  rule gilt. A small index row above the list names the pieces and jumps to one; it stays
  pinned under the main tabs while the reader is inside The Record, as the chain's bar does
  (Cade, same day), marks the piece the reader has reached and slides sideways to keep
  that name in view; it hides
  when an event has three pieces or fewer. The list is as long as the event supports
  (event-pages.md already leaves the optional sections to the writer). The Wikipedia and
  Britannica exits sit at the foot of The Record (Cade), moved from under Meanwhile. Cade expects the
  Record's text and organisation to be rewritten; the headings stay the fixed set unless
  the master chat rules otherwise.

- **Where next** (Cade, 2026-11-12; on trial). A closing block under Meanwhile with three
  ways on: a random chronicle, story or event; the globe and the timeline at the event's
  year; and "Have you taken today's quiz?", the one gilt-framed item with the one red
  button. It is navigation, carries no h2 and sits outside the page's sections. Three signs
  drawn in this chat in the manner of the kind signs (hairline, square joins, gilt): a
  library globe in its meridian ring on a stand; a time rule carrying the diamond, the dot
  and the ring; a question mark in the notched cartouche. Cade asked for a variety to choose
  from: the chooser (`kind-icons.html`) now opens with five designs each for the globe,
  the timeline and the quiz, above the eight kinds, which start on his picks. After two
  more rounds (an old-map set, then ten designs a row with varieties of the globe) he
  DECIDED (2026-11-12): the globe is the library globe carrying the diamond, the dot and
  the ring on its face; the timeline is the rule of years carrying the same three marks;
  the quiz is a question mark in a diamond. All drawn Fine, in gilt, like the eight kind
  signs, which he confirmed unchanged. The event mock carries all three. For the
  master chat: it adds a block after the last section of every event page; the globe and
  timeline links take over part of the job of the bottom bar this mock dropped; and the
  quiz is deferred in CLAUDE.md until the link and arrow-note work ships, so the button is
  a placeholder for the daily game.
- **Meanwhile, third pass** (Cade, 2026-11-12; on trial; replaces the row list below, which he
  found busy). Six entries in two columns with no rules and no underlines. Each is a
  dateline: the size mark and year with the kind signs at the right, the name, the place.
  The whole entry is the tap target. The graded line to the page's event no longer shows
  here; the chain carries it. Cade wants the place as "City, Country" on every entry; the
  old data's place field is free text and often lacks one or the other, so the rewrite
  needs separate city and country fields, named as they were at the time.
- **Meanwhile, second pass** (Cade, 2026-11-12; on trial). Six events at most, drawn at
  random from what the atlas holds within two years of the event and set in date order.
  Each row is one line where it fits: the size mark (diamond, dot or ring) and the year,
  as on a chain card; the name; the place; and up to two kind signs. Sizes are placeholders:
  the old data's tiers 1, 2 and 3 shown as knot, fibre and strand. A row shows the
  graded line to the page's event only where the link table holds one; the "no line"
  sentence is gone. "Show six others" draws again. The mock reads the 19 events of 1917 to
  1921 from `site/data.json` through the new `event-v12-meanwhile.js`. Open for the master
  chat: a random draw changes on every visit, which works against a page a reader or a
  search engine can cite; and the old data's place field is uneven ("Europe" for the US
  entry into the war).

### B. On trial in the mock, for Cade to settle

15. **Square corners everywhere** (ui-rules.md, palette.md). Cade leans this way. The mock
    is squared in one block of styles; round is kept for the globe, the fibre dot, the
    strand ring and the pin. It would change the story and chapter mocks too.
- DECIDED (Cade, 2026-11-11): the event picture is the C inset with gilt corners. The frame and
  placement switches are withdrawn from the mock (hidden; their trial styles remain in the file).

16. **The bottom bar** (Globe, year, search): keep it as a floating pill, or square it.
    Cade asked (2026-11-11) whether to drop it. This chat's view: drop it from the event page; the
    docked header already carries the globe and the year, and search belongs in the site header.
    It is site-wide navigation, so the master chat decides.
    Cade then said to go ahead (same day): the event mock now shows no bottom bar; search is a
    magnifier beside Back in the top row and fades with the Back label once the title docks, so
    search is out of reach mid-page. Pop-ups sit lower to use the freed space. On trial on this
    mock only; the story and chapter mocks still carry the bar.
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
