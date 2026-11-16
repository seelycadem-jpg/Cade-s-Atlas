# The event page sub chat: working log (2026-11-11 to 2026-11-17)

Moved out of `docs/state.md` by the master chat on 2026-11-17. The consolidated result is
`docs/design/page-system.md`; read that first. This file is the record behind it. Later
entries replace earlier ones. The event sub chat keeps adding its notes here.

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
  ways on: a random chronicle, story, event or person (person added by Cade; the random
  row and the globe and timeline pair are set as one unboxed ledger between hairlines so
  the quiz stays the most pronounced item); the globe and the timeline at the event's
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
  sentence is gone. A shuffle sign at the right of the heading draws again (Cade, 2026-11-12; it replaced a "Show six others" button). The mock reads the 19 events of 1917 to
  1921 from `site/data.json` through the new `event-v12-meanwhile.js`. Open for the master
  chat: a random draw changes on every visit, which works against a page a reader or a
  search engine can cite; and the old data's place field is uneven ("Europe" for the US
  entry into the war).

- **Review after a "doubling" fault** (Cade, 2026-11-12). His screenshot showed the chain's
  bar drawn twice, one copy just below the other, when scrolling slowly. Not reproduced: a
  fresh load at phone and desktop width holds one bar, pinned flush under the tabs at every
  scroll step, and the 140-action tap test passes (84 checks, none failed). Likely cause:
  the artifact page was left open through many republishes and held parts of two versions.
  A start-up guard now reloads the page once if the script finds it has already run or
  finds two elements with one id. Unproven until he reloads and tries again. He reloaded and
  still saw it, now at rest: a second copy of the bar in a strip about 18px tall directly
  under the real one. That is the size and place of the bar's fade strip (a pseudo-element
  with an opacity transition), so the strip is the suspect: the fade strips above and below
  the bar are removed and the bar tucks 8px under the tabs to close the gap. Still not
  reproduced in the test browser (Chromium), light or dark, phone, tablet or desktop width;
  his browser and zoom are not yet known. Other faults
  fixed in the same review: chain cards painting over the pinned bars (the web is now its
  own layer), a sliver of cards showing between the tabs and a pinned bar, and long words
  split in card titles.

- **Blind review** (2026-11-12). A fresh reviewer with none of this chat's context rated the
  event mock on a phone, light and dark, and at desktop width: 6.5 of 10 overall
  (consistency 8; first impression, flow and reading comfort 7; clarity, pop-ups and touch
  controls 6; the chain diagram and desktop width 5). Cade's ruling: fix problems 1, 2 and 5
  now; 3 (the verdict text reads as internal notes) and 4 (the opening line squeezed beside
  the picture, and repeated by the Overview) go to the rewrite. Fixed: (1) every change to
  Steps, the sizes or the filter now says how many events match and how many wait off
  screen on each side, and the arrow on that side beats; (2) the key names the three kinds
  of line; (5) the pop-up takes half the screen at most with its text scrolling inside,
  hides while a sheet is open, and on a wide screen stands to the right with the page left
  still. A second pass the same day fixed six more: a card squeezed out of a column
  drops its words so "N more" reads cleanly; a long card title is set smaller and shows
  whole; the chain's box grows to hold the open filter panel; the large globe answers a
  tap and Escape closes the filter; on the map the names sit over the highlight and a 1914
  land carries no later name in brackets; small text links have a 44px target. Left from
  the review after that: desktop is a phone column in empty space, and the path line's
  site words meet a newcomer before the subject. The original list, for the record: "1 more" paints over a faded card; one card
  title is still cut ("The Depression Reaches..."); the filter panel hangs over the next
  section after a filter shrinks the web; tapping the large globe does nothing; Escape does
  not close the filter; the Danzig label is crossed by the highlight; the 1914 map names
  "Russia (Soviet Union)"; several text links are under 44px; desktop is a phone column in
  empty space; and the path line's site words (chronicle, story 8 of 12, knot) meet a
  newcomer before the subject.

- **"Sufficient" is withdrawn as a grade** (Cade, restated 2026-11-12: "we got rid of
  sufficient"). This chat holds no record of where that was decided, and the standards on
  this branch and on main still list it: house-style.md (the grade list, the counterfactual
  rule, the line styles), structure.md (the backbone, and the rule that drops an event a
  size) and state.md. Six of the 36 pilot links are graded Sufficient. Done in the mock:
  the key names the solid line "Necessary" only. NOT done, because it is data and rules:
  the six links still show "Sufficient" in their pop-ups and notes, with the sentence "was
  enough on its own to bring about". For the master chat: write the ruling into the
  standards, say what each Sufficient link becomes (Necessary, Contributing, or regraded
  one by one), and restate the backbone and the size rule without the word.
- Pop-ups from the chain open about a tenth of the screen above the bottom edge (Cade,
  2026-11-12), where they had sat on it.

- **The chain's scroll ruler moved under the chart** (Cade, 2026-11-12; on trial) and is drawn
  as a map's scale bar: a checkered bar with one segment a step, the red diamond at this
  event, a gilt bracket over the part in view, the "N more" arrows at each end and the
  caption "steps from this event". The top of the chart now holds only the control bar
  and the column headings.

- **Reading margins** (Cade, 2026-11-12; on trial, to compare on his phone). Side margins 20px
  where they were 16; the opening line 21px (was 23); section headings 27px (was 30); the
  page title a touch smaller on a phone so it still fits one line. Body text stays 17px.
  The chain, the tabs and the Record's row still reach the screen edge.

- **The chain's filter, reworked** (Cade, 2026-11-12; on trial). The panel is smaller. The
  eight kinds are a grid of switches, four across, each a sign with its name and count;
  several can be on at once and they add up (Political and War shows events that are
  either). None on means all shown; "All kinds" is gone. Side is a slim three-way switch,
  Backbone a one-line switch, then Clear and Done. On the cards, the sign of every kind
  that is on turns ink. The filter button reads the one filter's name, or "N filters".
- The chain opens at three steps (Cade, 2026-11-12; it was two). The short message that
  follows a change is a slip of paper with a gilt hairline, serif italic.
- On trial: a hairline under the docked tabs in place of the fade; the chain's control
  bar and its scale bar set thinner, with smaller marks and labels.

- **Three demos for The Record** (Cade asked, 2026-11-12; awaiting his pick):
  `docs/design/mocks/record-demos.html`, the same seven pieces of text set three ways.
  A, Read through: nothing hidden, one long read, each piece under a numbered label with
  its one-line answer in italics, and the index row for jumping. B, One at a time: one
  piece on screen, a bar underneath naming the piece before and the piece after, swipe or
  tap. C, Answers first: the one-line answer is the headline and the section name a label
  above it; tap to open the detail under a gilt rule; "Open all". The event mock still
  carries the list-with-index-row version until he chooses.
  Cade chose C (2026-11-12) and found it still cluttered; content is set aside until the
  rewrite. The page now shows three quieter variants of C, each with no counter, no "Open
  all" and one piece open at a time: 1, Open air (no rules or chevrons; a gilt diamond
  marks each piece and fills when open; the section name in italics under the answer); 2,
  Numbered (a gilt numeral in the margin, the answer, the section name as a caption);
  3, Ledger (two columns: section name left, answer right). Awaiting his pick.
  Cade's answer to those three: "meh" (2026-11-13). The page now shows a second try,
  further from a list: 1, Tiles and sheet (the seven answers in two columns, set like
  Meanwhile; a tap opens the piece in the gilt sheet, with Before and Next; the page never
  grows); 2, Tabs in place (the row of names is the control, one panel beneath, the answer
  as its headline); 3, Thread (the pieces hang on a gilt line with a diamond at each and
  open where they hang). Awaiting his pick.
  Cade rejected those too: he wants variations of C itself, the layout he chose. The page
  now shows C as chosen beside three close variations that keep its rows: C1, Lighter (no
  counter line, a gilt plus for the arrow, the label stays grey, the open text flush);
  C2, Roomier (no counter and no rules between rows, a fainter arrow, the gilt rule beside
  the open text kept); C3, Lead open (the first piece open on load and set larger, the
  rest as C). DECIDED (Cade, 2026-11-13): C1, Lighter. The event mock's Record now
  carries it, with the pinned index row kept above the list. Lesson for this chat: when he names a chosen option,
  vary it in small steps and show the original beside the variations.

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

- **Type sizes (2026-11-14, on trial).** Cade asked for smaller titles and Record text. The mock now
  sets: page title 32px on a phone (clamp 32 to 48), section heading 24, opening line 19.5, reading
  text 17, Record answer 16.5, Record text 16; side margins 20px. Labels still run 8 to 10px; the sub
  chat advised a floor of 10px and Cade has not taken that up.
- **Titles in Cormorant Garamond (Cade, 2026-11-14).** Cade chose Cormorant Garamond for the title
  role (page title, headings, opening line, Record answers, italic notes, card titles) and kept
  Newsreader and Public Sans. The mock uses it from Version 105. The palette doc and the stack still
  name EB Garamond: the master chat updates them. Cormorant has finer strokes and a smaller body than
  EB Garamond, so the small title jobs (card titles 14.5px, italic notes 15px) need a check on a phone.
- **Where next, links that look like links (Cade, 2026-11-14).** The rule with the diamond above the
  block is gone and the line reads "Where next?". The four random choices and the titles of The globe
  and The timeline carry the house link underline (thin, red); the chevron tried on the pair was dropped the same day.
- **Link underlines at 0.6px (Cade, 2026-11-14, on trial).** Every link underline in the mock went from
  1px to 0.6px. A phone screen draws that as a finer line; an ordinary desktop screen still draws 1px.
- **The chain moves by dragging; the scale bar is gone (Cade, 2026-11-14, on trial).** The chain already
  slid sideways and settled on a column; the scale bar under it repeated that job. Now a column past the
  last full one is drawn narrower, fainter and pulled in, so a sliver shows at each edge of the screen
  (the same idea as the tall columns' drums). A tap on a sliver slides one screen that way. The foot keeps
  the two counts and arrows, with "Drag to explore the chain" between them. On a phone the three full
  columns keep the page's 20px margin (cards 90px wide at 390px, was 99px); the margin holds only the
  slivers. The arrows follow the curve: an arrow meets a full card at its edge and runs in behind a card
  as it curves away, shrinking and fading with it. Not done: a width cap for the chain on a desktop.
- **Closing a chain card returns the page (Cade, 2026-11-14).** A tap on an event can push the page down
  so the event stays visible above its card. Closing the card now scrolls the page back to where it was,
  unless the reader has scrolled more than about 140px away in the meantime.
- **The chain: full screen, a folded key, a gilt top rule (Cade, 2026-11-14, on trial).**
  - Full screen: a button at the right end of the chain's bar opens the same chain with the same
    controls over the whole screen; the button becomes an X, and Escape closes too. The page behind is
    held still and returns to the same place. A phone turned sideways shows five columns. A tapped event's
    card opens inside the view, and the view scrolls within itself to keep the event visible. No side
    borders: the slivers say the chain continues, and a border would say it ends.
  - The key (Knot, Fibre, Strand and the three line kinds) folds behind a small "Key" row under the chart.
    It is open on a reader's first visit and closed after (browser storage, key `atlasKeySeen`); always
    open at 1100px and wider.
  - The chain's top rule is gilt.
  - Full screen is fitted to the way the phone is held (same day). Sideways: one thin bar, then the chart
    to the bottom edge; the two counts and the Key button sit in the bar; the key opens as a small gilt
    panel; a tapped event's card stands at the right and the chart narrows to three columns beside it.
    Upright: a column shows as many events as the height allows (up to six) before it becomes a drum, and
    a line says "Turn your phone for a wider view" on the first open. The number of rows a column shows is
    now a variable (two to six), no longer fixed at three; in the page it stays three. A sideways phone
    is short, so it shows two rows per column.
  - Where zoom is offered (Cade, same day; this replaces an earlier "full screen only" trial). In the
    page: full size and one level out, no further. In full screen: the chain opens at five steps and one
    level out, with one more level out on offer; zooming back in to full size is allowed. Closing full
    screen puts back the steps and the zoom the page had. The sub chat advised against free zoom: fixed
    levels keep whole columns, whole cards and the settle-on-a-column drag.
  - Zoom (same day, on trial): three levels, by a minus and plus control (beside the Key upright, in the
    bar sideways) or a two-finger pinch on the chart. Zooming out fits more columns and rows: upright 3,
    4 or 5 columns; sideways 5, 7 or 9. The cards are the same cards drawn smaller (CSS `zoom` on the
    card), so titles wrap the same at every level; at the far level a title is about 8px tall, an
    overview only. Column labels shorten to "Cause 2" when zoomed out. Three fixed levels, no free zoom,
    in line with the timeline's rule.
  - Full screen fills its height (Cade, same day). The chart takes all the room the bar, the foot and the
    key leave; the rows that fit are counted from that, then the rows spread to use it (up to 1.7 times
    the tightest spacing), which gives the arrows room between events. A zoomed-out column gap is never
    under 28px. The key shows by default in full screen as one compact strip under the chart: the three
    size names and the three line kinds, no definitions. Closing full screen puts the key back as the
    page had it. In the page, zoomed-out rows sit a little further apart than before.
  - Full screen has five zoom levels (Cade, same day): one closer than the page's full size and one
    further than before. Columns across, upright: 2, 3, 4, 5, 6; sideways: 3, 5, 7, 9, 11. It still opens
    on the middle-out level (4 upright, 7 sideways). At the furthest level the column labels shorten to
    "C2", "Here", "E1" and a title is about 6px tall. The page keeps two levels.
  - Full screen, second pass (Cade, same day). Zoom sits at the right: last before the X sideways, at the
    right of the key row upright. Sideways, the two "more" counts left the bar and stand as small tabs at
    the left and right of the chart, in a 40px margin the full cards keep clear. Small cards: the page
    tells the phone not to enlarge small text on its own (`text-size-adjust`), clips a card's contents to
    the card and caps a zoomed-out title at three lines. Cade reported garbled text at the furthest zoom
    on his phone; the sub chat could not reproduce it in its test browser, so this fix is unconfirmed.
  - Gaps scale with the cards (Cade, same day; corrects the two notes above). Cade found the gaps between
    events odd when zoomed out: rows spread up to 1.7 times and columns held a 28px gap while the cards
    shrank. Now the row gap shrinks with the card and rows spread by at most 1.22 times; the column gap
    may fall to 20px. A zoomed-out chain sits as one tight group in the middle of the screen and no
    longer stretches to fill the height. A third-pass change (plain Key switch, drag to the chain's ends)
    was rolled back at Cade's request the same day; both needs stay open.
  - A blank band under the chart in upright full screen (Cade's screenshot, same day) is fixed. The cause
    was the sub chat's own "measure and correct" step: it measured while the chart was still easing to
    its new height and so cut the chart short, by about 135px on Cade's phone. That step is gone. The
    chart's room is now the box less its padding less each other part measured by itself. Tested at six
    screen sizes, key open and closed, both zoom steps: 3px of slack at most, nothing spilling.
  - Sideways full screen, fourth pass (Cade's screenshot, same day). The side tabs stood on top of the
    first cards on a phone with a notch, because they stepped clear of the notch twice; they now sit at
    the chart's true edge, and a tab with nothing behind it is hidden. The bar is two groups under one
    unbroken hairline: steps, sizes, filter and recentre at the left; Key, Zoom and the X at the right.
    In full screen the chain can be dragged until its first or last column stands in the middle, at every
    zoom level (the part of the rolled-back third pass Cade asked for again). A drum's "N more" label no
    longer sits on the key's rule at far zoom.
  - Arrows at the closest zoom (Cade's screenshot, same day). With two columns across, the neighbouring
    columns are half in view, and their arrows ran in behind them with no head, which read as clipping.
    An arrow now runs behind a card only once the card is a thin sliver (the last 30% of its way out); a
    half-visible card keeps its arrow at its edge, with its head. Sideways, the closest zoom a view offers
    is the closest at which two rows of cards fit: five columns on a tall phone, seven on a short one
    (under 362px high), since larger cards spilled off the bottom.
  For the master chat: full screen is a new mode of the event page that the standards do not describe.
- **One gap between sections; Cade wants it as a site-wide rule (2026-11-14).** Every section of the event
  page now ends with the same space before the next heading: 68px on a phone, about two blank lines of
  reading text (was 34px). The same gap sits above "Where next?". The diamond rule that stood before
  Meanwhile is gone, so every break is the same. In the mock it is one value, `--secgap`. For the master
  chat: Cade asked for this as a rule across the whole website; it belongs in the standards, which the
  sub chat does not edit.
- **The key defines the three kinds of arrow (Cade, 2026-11-14).** In the page, Key sits at the left of its
  row and Zoom at the right, as in full screen. The key now gives each arrow a full line, as it does each
  size. The wording is the sub chat's draft and needs the master chat's check against the standards:
  "Necessary. Without this cause, the effect would not have happened." "Contributing. One cause of
  several. The effect could have happened without it." "Contested. The evidence supports two readings,
  and the atlas gives no verdict." The compact strip in full screen shows the names only.
- **Four chain changes (Cade, 2026-11-15).**
  1. No message pops up on zoom.
  2. The key counts what the chain shows: events of each size and arrows of each kind, as "Knot (5)" in
     the page and "Knot 9" in the compact strip.
  3. Each chain card carries one small line at its foot saying where the event happened, so a reader sees
     an event in one country reach another. The card grew 12px (82 to 94) and the row pitch with it.
     The line shows the last part of the old data's `where` field, from the new generated file
     `event-v12-places.js`. That field is uneven: some events give a country ("Germany"), some a city only
     ("Paris", "Beijing"), some a region ("Europe"). The card needs a real country field per event: this
     adds weight to the open question on city and country fields.
  4. Neighbours linger: a card leaving at the side, or at the top or bottom of a turning column, fades
     more slowly and stays a little more visible; arrows fade in step with no jump.
- **Place rule for the chain (Cade, 2026-11-15).** A card always names the country. Where the event is larger
  than one country, it names the region. A city may show only after its country: "France, Paris". The card
  shows the country alone; the event's pop-up shows country and place under the title. The old data has no
  country field, so `build-places.py` holds a country for each of the 33 chain events, added by hand from
  the place the data names (present-day country), and writes `event-v12-places.js`. Four events name
  something wider and show that: Europe (three), the Holy Roman Empire, the Soviet Union, Silesia. These
  are placeholders. For the master chat: every event needs a country field, and a rule on present-day
  against period names (Petrograd is "Russia", Münster in 1648 is "Germany").
- **A turning column fades (Cade, 2026-11-15).** The fade Cade asked about was a tall column scrolled up or
  down. The cause of the pop was the words: they switched off at once when a card began to leave. Words
  now fade with the card, and the card fades to a ghost that stays while any of it can be seen.
- **The key in full, in full screen (Cade, 2026-11-15).** Upright full screen shows the page's own key under
  the chart, every definition and count, open on arrival; the chart takes the height that is left and grows
  back when Key is switched off. Sideways there is no height for that (the key would leave the chart less
  than two rows), so the strip of names and counts always shows and the Key button opens the full
  definitions as a gilt panel over the foot of the chart, three across; a tap on the panel closes it.
- **TAKEAWAY FOR THE MASTER CHAT: stories and the chain (Cade and the sub chat, 2026-11-15).** Proposed
  rule, for the standards (the sub chat does not edit them):
  1. **The route sets where the lens starts; the chain itself never changes (amended by Cade, 2026-11-15).**
     A reader who comes to an event through a story or one of its chapters finds that story's lens already
     on, with its name in the line above the chart and "Show all" one tap away. A reader who comes any other
     way (search, the globe, the timeline, a link from another event) finds every link showing. An event has
     one set of causes and effects: the lens only chooses which of them show first. The links that
     cross from one story into another (the Treaty of Versailles to the May Fourth Movement) are the
     atlas's best material and are never hidden by default.
  2. **The story is a lens the reader turns on.** The chain carries a Story control. It lists "All stories"
     and each story the page's event belongs to. Choosing one keeps the events that belong to that story;
     the rest leave, except an event a path runs through, which stays faded. The reader can switch to
     another of the event's stories or back to all.
  3. **Story is its own control, first in the chain's bar.** It is not inside the Filter panel (Cade). It
     shows its state at all times: "All", or the story's name in red with a gilt line.
  4. **The route still shows elsewhere on the page.** The line under the title and the Next link carry the
     story the reader came through. The chain does not repeat that job.
  5. **Membership uses the standards' own test.** An event belongs to a story by its links, never by its
     dates alone. The chain's Story control must read the same membership the story and chapter pages use.
  In the mock the page opens with the lens on, because its line under the title says the reader came through
  a story; the Story panel lists that story first, marked "the story you came through". Cade spoke of the
  lens for "that specific chapter": the mock works at story level only.
  Open for the master chat: (e) whether the lens narrows to the chapter the reader came through, or to its
  story, and whether the control lists chapters; (a) the membership data does not exist yet; the mock uses the old atlas's arcs
  as stand-ins (`build-stories.py`, clearly marked), so its story names ("WWII in Europe", "Road to WWI",
  "Depression & dictators") do not match the page's own line ("Germany · Weimar Germany · The Treaty");
  (b) whether the story the reader arrived through is marked or listed first in the control; (c) whether
  the control also offers chronicles and chapters, or stories only; (d) whether a story lens should dim
  the others in place, as first proposed, or remove them, as the mock does by reusing the filter's rule.
- **No pop-up messages from the chain (Cade, 2026-11-15; a standing preference, said twice).** Cade does not
  like a message box that appears and fades after a control is used. The chain's controls (steps, sizes,
  filter, story, zoom, opening full screen) now show none. The result of a change reads from the page: the
  two "more" counts, the counts in the key, the state of the control. For the master chat: treat this as a
  rule for the site. Do not answer a control with a transient message; show the result in place.
- **A story lens announces itself (Cade, 2026-11-15).** With a story chosen: the Story control carries a
  gilt frame and a slow glint along its foot (still under reduced motion), and one line sits above the
  chart, "This event's chain within the story [name].", with "Show all" beside it. Sideways in full screen
  there is no height for the line, so the Story control widens to show the whole name.
- **Story control, third pass; the key closed in full screen (Cade, 2026-11-15).** The Story control no longer
  prints the story's name: it is a sign (two diamonds on a line) over the word Story, as Filter is a sign
  over its word. Turned on, it takes a thin red frame and red ink, with the glint along its foot. The name
  lives in the line above the chart, now thinner and shorter: "Within the story [name]." with "Show all".
  Sideways in full screen that line has no room, so the name sits beside the sign. The sub chat chose a red
  frame over a red fill: the fill is kept for the page's own event and the Play button. Full screen now
  opens with the key closed, upright and sideways (this replaces "open on arrival" and the always-on strip);
  the Key button opens it, in place upright and as the panel sideways.
- **The lens is named for the page's own story (Cade, 2026-11-15).** The line above the chart reads "Within
  the story Weimar Germany.", matching the line under the title. In the mock the old arc that stands in for
  that story carries the name; its events are still the old arc's. Rule for the master chat: the lens always
  uses the story's own name, the same words the page's line and the story page use.
- **The Story filter panel (Cade, 2026-11-15).** Its title is "Story filter". One italic line sits under the
  title: "Show only the causes and effects of this event that belong to one story." The list runs: "All
  stories"; then the story the reader came through, if any, marked as such; then the event's other stories
  in alphabetical order. The control in the bar keeps the one word "Story".
- **A card in view is never blank (Cade, 2026-11-15; a rule).** The next card out of a tall column peeks
  from behind the last full one as a faded copy of itself, words included: below a column it shows the end of
  its title, above it shows its year and the start of its title. The "N more" label stands at the outer end
  of the peek. The card after that waits behind, unseen. The peek is deeper than before (the column's ends
  take 58px each, were 34px), so a chain with a tall column is about 48px taller in the page. Sideways in
  full screen keeps the shallow peek, for want of height, but shows the words too. This replaces the earlier
  note that words fade out as a card tucks away. Also: changing the story filter recentres the chain on the
  event; before, "Show all" could leave it one column off.
- **Nothing on a chain card switches; everything eases (Cade, 2026-11-15; a rule).** As a column turns, a
  card's country fades in and out in step with the turn, and its title slides between the top of the card and
  its foot. Before, both changed in one step and the country popped. For the master chat: in the chain, any
  part of a card that appears, leaves or moves does so gradually, tied to the reader's drag.
- **The story line's words (Cade, 2026-11-15; his wording, replacing "Within the story ...").** The line above
  the chart reads "Cause and effect filtered to story: Weimar Germany", with "Show all" beside it; one line at phone
  width. Cade's first wording ("Filtering cause and effect for this event specific to story: ...") took two
  lines and he asked for it shorter.
- **Long columns on a fast turn (Cade, 2026-11-15).** In a column with three or more events folded away,
  years, signs and titles of cards further back showed through the cards in front. Cause: every card leaving
  the column shared one layer, so whichever the page had made last lay on top. Now the cards stack by depth
  (the nearer always over the one behind), a tucking card stays solid for the first third of its way, and its
  year and signs fade with its country. Recreated and checked with a six-event column at eight points of a
  turn. Also: a three-line title sits 2px higher, clear of the country under it.
- **The Story control when on, final (Cade, 2026-11-15).** One red line under it, the same 1px line the sizes
  and the filter carry in gilt, with the sign and the word in red. The red frame and the animated glint are
  gone (this replaces the two earlier notes on them).
- **TAKEAWAY FOR THE MASTER CHAT: guiding principles for a graphic (Cade and the sub chat, 2026-11-15).**
  Proposed for the standards. Cade found the Overview's before-and-after graphic far too big: 733px tall at
  phone width, on a screen of about 844px, with the map a third of it.
  1. One graphic makes one point, and its title states that point (the title rule of 2026-11-12 stands).
  2. Half a screen at most: about 420px tall on a phone, title and key included.
  3. The picture carries the facts. Words inside the frame are a title, a one-line key and one caption or
     source line.
  4. Nothing the picture already shows is repeated as a list under it.
  5. Key figures are not part of a graphic. They stand in the page's own figures strip, which the data
     header generates.
  9. **A caption reads as a history textbook's would (Cade, 2026-11-15).** It states what the picture shows,
     as fact, in the atlas's voice. It never mentions the atlas's own records, data, tables or method ("the
     border record", "the link table"): that is the standing rule against explaining the method outside the
     About page, and the sub chat broke it in its first caption. Credits a licence requires go on the About
     page.
  6. The still image must make the point. A tap adds detail in one line of fixed height and never changes
     the graphic's size.
  7. No empty or placeholder slot is shown. A figure or label without a source is left out.
  8. Every graphic shares one frame: the same border, type and colours, and the same places for the title,
     the switch, the key and the source.
  The rebuilt graphic in the mock follows them: a title, the map (seven tenths as tall as it is wide, was
  eight), one row with the key at the left and the 1914/1919 switch at the right, and one caption line two
  lines high that also answers a tap. The caption at rest reads "The treaty took 13% of Germany's land in
  Europe. France and Poland gained land. Tap a country."; every tap answer was rewritten the same way, and
  the chain's two empty-side lines now read "No cause of this event is recorded yet." It is 395px tall and does not grow on a tap. Gone: the list of nine new
  countries (the map names them) and the fourth, unsourced figure. The three sourced figures stand under the
  graphic in a strip of three; in the real site that strip is generated, never written by hand.
- **Results sit inside the graphic; graphics hold still (Cade, 2026-11-15; this replaces the "Key figures"
  note below and amends principles 2 and 5 for graphics).** Where figures are results of the thing a graphic
  shows, they stand inside its frame under a short heading ("Results of the treaty"), at most three lines,
  each led by its figure in bold ink, never red (Cade). Figures that are not about the graphic stay in By the numbers. With the results
  the graphic is about 500px tall on a phone: the half-screen measure applies to the picture, its key and its
  caption (395px), and the results add to it. The caption no longer repeats a figure the results give.
  Graphics no longer grow and shrink as they cross the screen; that effect is kept for pictures only. The
  three-layout "Key figures" trial and its mock switch are removed.
- **Key figures under the Overview's graphic (Cade, 2026-11-15, on trial; a layout to be chosen).** The
  figures that left the graphic stand in a block headed "Key figures", three at most, each a number and a few
  words, with a link "All the numbers" that goes to By the numbers in The Record. The mock offers three
  layouts behind a dashed mock-only switch: A, three across; B, a short table with the numbers in one column;
  C, three sentences each led by its number in red. Naming, for the master chat: Cade suggested "Takeaways",
  but the standards already use "takeaway strip" for the strip at the top of the page (when, where, who, the
  strongest arrow each way), so the sub chat used "Key figures" to keep the two apart. The block must be
  generated from the page's `figures` header, never written by hand.
- **Where the chain's counts go (Cade, 2026-11-15; this replaces "the key counts what the chain shows").** The
  key carries no counts. Each size control in the bar shows how many events of that size lie within reach:
  "Knots (5)", "Fibres (10)", "Strands (3)". The number counts a size whether or not it is switched on, so a
  reader sees what turning Strands on would add; the story and type filters do apply. Each column shows its
  own total under its name as a number in brackets, the same form as the size counts: "Effect · 1 step"
  over "(4)", in the page and in full screen at every zoom level.
- **"Drag to explore" is back (Cade, 2026-11-15).** The line lost its place when Steps moved to the foot. It
  now stands in italics between Key and Zoom, on the row under the chart, in the page and in upright full
  screen. Sideways in full screen that row does not exist, so the line does not show there.
- **TAKEAWAY FOR THE MASTER CHAT: the event page's hero says where the reader is (Cade, 2026-11-15, on
  trial).** Three needs from Cade, and how the mock meets them:
  1. *Say lightly that this is an event page* (not a chapter, story, chronicle or person). A small red label
     "Event", with the event's size mark beside it, sits directly over the title. Every kind of page should
     carry its own such label in the same place.
  2. *Show the route.* A reader who came through a chapter sees a ladder over the title: three thin rows,
     each naming its level in small capitals and then the thing itself as a link: Chronicle, Germany; Story,
     Weimar Germany, "8 of 12"; Chapter, The Treaty, "1 of 3". Read downward the ladder ends in the Event label
     and the title: chronicle, story, chapter, event. This replaces the breadcrumb, where the level words sat
     under the names and were easy to miss.
  3. *Back to the chapter, on to the next chapter.* Under the date, two buttons side by side: "Back to
     chapter, The Treaty" and "Next chapter, The Ruhr and the Mark". When the title docks at the top, the line
     under it reads "‹ The Treaty · Next chapter ›".
  A reader who came another way (the globe, the timeline, search) sees the Event label and "Part of 18
  stories", with no ladder and no buttons. "Also in 17 more stories" sits on the Event row and still opens
  the list of every story the event belongs to.
  Open for the master chat: (a) the old "Next: German Hyperinflation" link, the next event in the chapter,
  is gone from the hero; Cade asked for the next chapter. Whether the page also offers the next event, and
  where, is undecided. (b) The standards' takeaway strip says "no size word" beside the route; the mock keeps
  the size as a mark only. (c) "The Ruhr and the Mark" and "1 of 3" are placeholders. (d) The ladder adds
  about 30px to the hero against the old breadcrumb.
- **Five hero options for Cade to choose from (2026-11-15, undecided).** `hero-demos.html`
  (https://claude.ai/artifact/JgMdtfyqAeTQot9jGb3jRy): 1 Ladder (what event-v12 has), 2 one line and a flip bar
  (steps to the event before and after in the chapter, with the event's place in it), 3 three tabs, 4 the
  thread (the route on a gilt line ending at this event), 5 a sentence (title first; three buttons: chapter,
  next event, next chapter). Cade's aims: simple navigation, room for curiosity, knowing where to go, flipping
  around quickly. The Event label is light grey in all five and in event-v12 (Cade: not too important).
- **Hero: Cade narrowed to a mix of the ladder (1) and the flip bar (2) (2026-11-15, undecided).**
  `hero-demos.html` now shows those two beside three mixes. A, the ladder that steps: every row carries its
  level, its name, its place ("8 of 12") and arrows to its neighbours, so the Story row steps stories, the
  Chapter row chapters and the Event row events; no other buttons. B, a labelled line and the flip bar: the
  route on one row with each level word over its name, the flip bar under the date stepping events, and two
  links, back to the chapter and next chapter. C, title first and one navigator: the title leads, and one box
  under the date holds the three rows, "Next chapter" on the chapter row, and a foot naming the event before
  and after. Options 3, 4 and 5 of the first round (tabs, thread, sentence) were dropped from the page.
- **A light tap in the hand when the steps change (Cade, 2026-11-15, on trial; third attempt, still
  unconfirmed on a phone).** Cade felt nothing from the first two attempts. Cause, from the web-haptics
  projects' own notes: an iPhone ticks when a finger flips a real switch control (Safari 17.4 on), and from
  iOS 26.5 it no longer ticks when a script flips one. Both earlier attempts flipped the switch by script.
  Now each steps button carries an invisible switch laid over it, so the reader's finger lands on the switch
  itself, the phone ticks, and the tap is passed on to the button. One tick per tap on an iPhone; a page
  cannot double it there. Android still vibrates through the page, doubled at the first and last step. Not
  known: whether the tick passes through the Claude app's frame, where Cade views the mock. Checked by the sub
  chat: with the overlay in place a tap changes the steps exactly once. For the master chat: haptics are
  welcome where they work, each needs its own overlaid switch on iPhone, and nothing may depend on them.
- **The haptic tick works on Cade's iPhone (confirmed by Cade, 2026-11-16).** The third attempt, an invisible
  switch laid over each steps button, gives the tick, inside the Claude app's frame too. This settles the
  "unconfirmed" in the note below it.
- **The "Centred on" lines sit close together (Cade, 2026-11-16).** When the chain is centred on another event,
  "Centred on [event], [year]" and "Back to [the page's event]" now sit on two adjacent lines, 52px in all (was
  about 100px). The link keeps a 44px invisible tap area. Cade likes the lines and wants them kept.
- **A full column no longer loses its last card (Cade's screenshot, 2026-11-16).** Zoomed out one level in the
  page, a column of four cards had its last card cut off above the "Centred on" lines. Cause: the chart's
  height was capped at four rows of the tightest spacing, while a column that shows all its cards spaces them
  a little wider. The chart now takes the height such a column needs.
- **One plus for everything that opens and closes (Cade, 2026-11-16; a rule for the site).** Wherever a plus
  opens something and a minus closes it, it is the same sign with the same small motion: two thin gilt
  strokes, and the upright one turns to lie flat as the thing opens (0.2s; still under reduced motion). The
  Key had it; The Record's pieces now have it, where the upright stroke used to vanish in one step. Any new
  open-and-close control uses this sign.
- **Hero on trial in event-v12: mix A with the neighbours named (2026-11-16; the sub chat's pick, built so
  Cade can judge it on the page; he has not chosen).** Every row of the ladder carries its level, its name, its
  place and a pair of arrows to its own neighbours: Story "8 of 12" steps stories, Chapter "1 of 3" steps
  chapters (the back arrow greys at the first), and the Event row, directly over the title, "2 of 5" steps
  events. A name is a link up to that page. Under the date two buttons name the events on each side ("Event
  before, The Armistice"; "Event after, German Hyperinflation"), taken from mix C. "Also in 17 more stories"
  moved to the right of the Chronicle row. Docked, the line reads "‹ The Treaty · ‹ Before · After ›". The six
  row arrows give the haptic tick on an iPhone. This replaces the "Back to chapter" and "Next chapter"
  buttons: back to the chapter is a tap on the chapter's name, and the next chapter is the arrow on its row.
  Placeholders: "The Armistice", "2 of 5", "1 of 3", "The Ruhr and the Mark". The other options stay in
  `hero-demos.html`.
- **The hero says what the route means, and is never bare (Cade's two worries, 2026-11-16, on trial).**
  1. *Does the reader know they are reading the event through one story, and that "next" means next in that
     story?* The sub chat's answer was no. Fixes: a line over the ladder, "You are reading this event within
     the story Weimar Germany"; the event's stepper reads "2 of 5 in chapter"; the two buttons under the date
     read "Before, in this chapter" and "Next, in this chapter".
  2. *Does the hero look empty for a reader from the globe, the timeline or an unrelated link?* It did: only
     the Event label and a count. Now it reads "This event belongs to 18 stories." over one link, "Choose a
     story to read it within", which opens the list of all of them; choosing one gives the page that route
     and the full ladder. A first version listed three stories in the hero; Cade judged the one link to be
     enough and the rows were removed the same day.
  For the master chat, a rule in the making: an event page always shows a way into its stories, whether or not
  the reader came through one; and every "next" on the page says what it is next in.
- **The event's type signs in the hero (Cade, 2026-11-16).** The signs for the event's types (the Treaty has
  one, Political) stand beside the Event label in gilt, the same signs its chain card carries, with the type's
  name for screen readers and as a tooltip. Signs only, no words: the row also holds the event's stepper.
- **The docked header is never an empty band (Cade, 2026-11-16).** For a reader with no route the docked
  header used to show the title and date over a blank third line. It now carries "In 18 stories: choose one ›",
  which opens the list of the event's stories, the same offer the hero makes. With a route it still reads
  "‹ The Treaty · ‹ Before · After ›".
- **Two jumps on the date line (Cade, 2026-11-16, on trial).** At the top of the event page the date is the
  way to the timeline at this event and the place is the way to the globe at it: "28 June 1919" carries the
  timeline's sign, "Versailles, France" the globe's sign, and each the thin red line of a link. The date line
  stays in the docked header, so both jumps are in reach down the whole page. No new row or button was added.
  For the master chat, a rule in the making: on every page, a date is a link to the timeline at that date and
  a place is a link to the globe at that place.
- **The chain's foot is thinner (Cade, 2026-11-15).** Each count and the steps read on one line ("4 more",
  "− 3 steps +", "7 more"), the two small rules beside the step number are gone, and the row is about 30px
  high with 44px invisible targets.
- **Steps moved to the foot of the chain (Cade, 2026-11-15, on trial).** To make room for Story, the steps
  control left the bar and sits in the foot between the two "more" counts, where "Drag to explore the
  chain" stood; that line is gone. Sideways in full screen the foot is the side tabs, so steps stays in the
  bar there, first, before Story.
- **Typefaces (2026-11-14, open).** `type-sheet.html` shows every type job at its real size with
  switches for other faces (https://claude.ai/artifact/VenRt5pSyfVRW7UCsX2YW5). The sub chat advises
  keeping EB Garamond and Newsreader and trying Inter or the system face for controls and labels.
  A change of typeface is a change to the stack and the palette doc: the master chat decides.

### C. Facts for the record

- The mock's sizes are placeholders: old tier 1 as knot, tier 2 as fibre, four events set
  as strands to show the filter. The stories in the sheet are placeholders but one.
- The picture is a public-domain US National Archives photograph of the signing, recorded
  in `docs/design/mocks/versailles-signing-1919.json`. Its licence is as Wikimedia Commons
  records it and is not yet checked against the Archives' catalogue.
- This environment's network now allows commons.wikimedia.org and upload.wikimedia.org.
- The Versailles exits are standard addresses, not yet verified.

Next in this chat: Cade's read of the rebuilt Historical Chain.

## The chain sub chat, second handoff (2026-11-17): the hero and the globe view

For the master chat. This is everything the sub chat changed after the first handoff above (sections A to C),
written as the state the mock is in now. The twelve dated entries under it are the working notes it was built from;
where they disagree with this list, this list is right. The mock is `docs/design/mocks/event-v12.html`
(https://claude.ai/artifact/Kx3QuaNRt7JLYdqsj1pimc, version 182). This chat changed no standards doc.

It replaces these items of section B above: the line "You are reading this event within the story ...", the type
signs on the hero's Event row, the Event row's own stepper, the buttons "Before, in this chapter" and "Next, in this
chapter", and every earlier note on how the page opens over the globe.

### H1. Decided by Cade (he asked for each in these words or close to them)

The hero, top to bottom, for a reader who came through a story:

1. **Globe strip.** The page opens with a strip of the globe above the hero, less than before. The globe is turned
   so the event's pin and place name sit inside that strip: the reader sees where the event happened without
   opening anything. (Doc: ui-rules.md, hero.)
2. **Hint.** One small centred line under the globe's lowest point: "Globe 1919 · pull down to open". Words never
   cross the globe's edge.
3. **Story view line.** Left: "Reading within a story", in the small sans, italic. Right: "Clear story view ×".
   Clearing is one switch for the page: the ladder folds to the no-route hero, and the chain's story filter turns
   off. Choosing a story again restores the ladder and turns the chain's filter on for that story.
4. **Ladder.** Four rows in one label column: Chronicle, Story, Chapter, Event. Chronicle carries "Also in 17 more
   stories" in italic serif, no bold. Story and Chapter keep their steppers ("8 of 12", "1 of 3"). The Event row
   carries "2 of 3 in this chapter" as a link and "· 7 in the story" as plain text, with no arrows.
5. **Title**, close under the Event row.
6. **Date line.** Red timeline sign, date, dot, red globe sign, place, dot, type sign in gilt. The date is neither
   bold nor red. Nothing on this line is underlined: the red sign marks what opens something.
7. **Step buttons.** "Previous event in this chapter" and "Next event in this chapter (1 more)". Label above, red
   arrow beside the event's name, no rules around or between them. The count is the events left in the chapter.
8. **Events sheet.** The Event row's link opens a sheet on this chapter: chapter number, name, its events in order,
   each with size mark, year, country and type signs; the page's own event reads "This page". A switch reads
   "This chapter | Whole story". A type filter shows one type at a time. Tapping an event opens it.

The globe view:

9. **Scrolling never opens it.** The top of the page is the event view; a fling up the page stops there.
10. **A separate, weighted push opens it.** At the top, a new pull down moves the page away, fades the hero and
    brings the globe to the middle with the place centred. Letting go early returns to the event. In the globe
    view: year at the top; event name, date, place and type signs at the foot; "Back to the event". A swipe up
    also returns.
11. **Smooth at every speed.** Cade rejected a version that looked laggy on a slow pull.
12. **Type signs** show in the globe view and on the hero's date line.

### H2. On trial (the sub chat's choices; Cade has seen them and not objected, and has not confirmed them)

- No rules between the ladder's rows; white space separates them.
- The Event row has no stepper; the two step buttons do that job.
- Two type voices in the hero: small sans capitals for labels, serif for names. In the small sans, what can be
  tapped is darker grey at medium weight; plain counts are light grey. The × is grey. "Also in ..." is the one
  italic serif; "Reading within a story" is the one italic sans.
- The numbers: 126px of globe held above the screen at opening; a 50 degree turn of the globe; 300px of finger
  travel to open; commit at 60%; the page buzzes at the commit point where the browser allows it (Android; an
  iPhone cannot buzz from a pull).
- The title block sits 26px lower than it otherwise would, to keep the hint clear of the globe.

### H3. Rules proposed for the standards docs (none written into a doc)

1. A link that carries its own sign takes the red sign and no underline. A link in running text keeps the thin
   red underline. (house-style.md or ui-rules.md)
2. Words never cross the edge of the globe; a caption for the globe sits clear of it. (ui-rules.md)
3. The hero's story and the chain's story filter are one state. (ui-rules.md, structure.md)
4. A block of controls uses at most two type voices. Weight and a darker grey mark what can be tapped; a third
   face never does. (house-style.md)
5. Anything that follows the finger costs less than one screen frame. For the globe: map data thinned to the
   globe's size on screen (points under about a third of a degree apart dropped at start-up), the land worked out
   once per drawing, d3's resampling off. One drawing fell from about 40 ms to about 7 ms on the test machine.
   Pre-drawn frames blended together look laggy at slow speed; do not use them. (architecture.md, budgets)
6. A gesture that leaves the page for another view needs a separate, deliberate push, never the tail of a scroll.
   (ui-rules.md)

### H4. Placeholders in the mock (labelled in the code; none is atlas data)

- The globe view is a stand-in. The real one is the Political globe at the event's year, centred on the event.
- The events sheet: six real events (the chain's events the old arc holds), three made-up chapter names ("The
  Treaty", "The Crash", "The Republic Falls") and a made-up split; "The Armistice" is a row with no event behind
  it. The hero's "2 of 3", "7 in the story", "8 of 12", "1 of 3" and "17 more stories" are placeholders.
- The real page needs, from the link table: each story's ordered events with chapter membership, and the counts.

### H5. Open questions for Cade, through the master chat

1. Does the type sign need its word beside it for a first-time reader? It has none in the hero or the globe view.
2. Should the events sheet sort (by date, by size) as well as filter by type?
3. The no-route hero (a reader from the globe, the timeline or an unrelated link) was not revisited in this round.
   It still reads "This event belongs to 18 stories. Choose a story to read it within".
4. Desktop layout of all of the above is not designed.

### H6. Not proven on a real phone

The test browser has no graphics chip and no finger. Cade tried the push on his iPhone and called it "pretty
great", then reported the slow-pull lag, which was fixed; he has not reported on the fix. Unchecked: whether Safari
or the Claude app's frame takes the pull-down for its own bounce; smoothness of the fixed version on the phone.

### H7. Not yet applied in the mock from the master chat's message of 2026-11-16

The Sources list, tappable figures, "Cite this page", every word in the HTML at load, and the graphics limits.
The sub chat listed them to Cade and waits for his word before building.

### Working notes behind the list above (superseded where they differ)

### Event page hero: red signs on the date line, and opening with less globe (sub chat, 2026-11-15)

- **Date-line jumps.** The timeline sign and the globe sign on the date line are red (the accent colour). Their words
  carry no underline. The red sign is the mark that says "this opens something"; an underline as well made the line busy.
  Proposed as a site rule for the master chat: a link that carries its own sign takes the red sign and no underline;
  a link inside running text keeps the thin 0.6px underline.
- **Opening view.** The page opens 110px down its own scroll, so the first screen shows the globe's lower arc and more
  of the page (route ladder, title, date line, the start of the Overview). Scrolling up pulls the whole globe into view.
  The globe rides up with the page through that first 110px, so it never sits behind the hero text. The docking
  animation starts after that stretch. Under reduced motion the offset is off and the page opens at the top.
- Not yet checked on a real phone: Safari's own scroll restore and the scroll-driven ranges with the offset.

### Event page hero: scroll up opens the globe view; date in ink; type signs on the date line (sub chat, 2026-11-16)

- **Opening view shows a little less globe.** The page opens 150px down (was 110px).
- **Scroll up opens the globe view.** From the opening view, scrolling up moves the globe to the middle of the screen
  and fades the hero and the page out; the globe view's own words fade in over the second half (year at the top, the
  event's name, date and place at the foot, "Back to the event"). Everything follows the finger. Letting go part-way
  settles on the nearer view. The hint under the globe reads "Globe 1919 · scroll up to open". The globe view in the
  mock is a labelled stand-in; the real one is the Political globe at that year, centred on the event. Off under
  reduced motion, where the tap on the docked globe remains the way in.
- **Date in ink.** The date is bold ink, no longer red. Red on the date line now belongs to the two signs alone.
- **Type signs sit on the date line**, after the place, in gilt. They left the Event row of the ladder.
- Open question for the master chat: the type signs carry no words here; the chain's key defines them. Decide whether
  a first-time reader needs the word beside the sign.
- Not yet checked on a real phone: the settle after letting go, and Safari's scroll-driven ranges.

### Event page hero: the scroll up to the globe is a weighted push (sub chat, 2026-11-16)

- The reader scrolls 260px up to open the globe view. The first half of that push moves the page little (the page and
  the globe follow the scroll raised to the power 2.6), and the second half carries it. Letting go before about 60% of
  the push returns to the event; past it, the page finishes opening the globe by itself.
- The opening view is unchanged (150px of the globe hidden), and the page always opens on the event view: it sets that
  position at start-up, on load and when the page is shown again.

### Event page hero: the globe opens on a separate push; the place shows in the opening strip (sub chat, 2026-11-16)

Replaces the two entries above on how the globe view opens.

- **Scrolling never opens the globe view.** The top of the page is the event view. A fling up the page stops there.
- **A separate push opens it.** At the top, a new finger pull down the screen (or a fresh turn of the wheel, after the
  earlier scroll has stopped) moves the page down, fades the hero and brings the globe to the middle. The push is
  weighted: 300px of finger travel, eased so the first part moves little. Letting go before 60% returns to the event;
  past it, the globe view finishes opening. In the globe view, a swipe up, "Back to the event" or Escape returns.
- **The place shows in the opening strip.** The globe is tilted 50 degrees in the opening view so the event's pin and
  name sit in the strip of globe the reader sees. The tilt eases to centred as the globe view opens and as the globe
  docks into the corner.
- The hint reads "Globe 1919 · pull down to open".
- Not yet checked on a real phone: whether Safari, or the Claude app's own frame, takes the pull for its own
  pull-to-refresh or bounce before the page sees it.

### Event page hero: smoothness pass, buzz on entering the globe, plainer date line (sub chat, 2026-11-16)

- **Smoothness.** A frame-timing test on a processor slowed four times found the globe's turn stalled every other
  frame: each step of the turn redrew the whole globe. The turn is now drawn ahead of time as 20 still frames, and the
  moving globe shows the two nearest, blended; the full drawing returns when the globe rests. Finger moves are applied
  once per screen frame. Rule proposed for the master chat: nothing that follows the finger may redraw the globe in
  full; draw ahead, or move a finished picture.
- **Buzz.** The page buzzes once where the push commits (and again if the reader backs out). This works on phones
  whose browser lets a page buzz (Android). iPhone Safari gives a tick only when a finger taps a real switch, so a
  pull cannot tick there.
- **Date line.** The type sign is gone from the hero. The date is no longer bold; it reads in the same weight and
  colour as the place. The line is now: red sign, date, red sign, place.

### Event page hero: the globe is drawn for real at every step (sub chat, 2026-11-16)

Replaces the "drawn ahead of time as 20 still frames" note above. Cade saw the slow push look laggy: the blended
still frames showed doubled lines and flipped between soft and sharp.

- The pre-drawn frames are gone. The globe is drawn in full on every step of its turn, at any speed.
- That is affordable because one drawing fell from about 40 ms to about 7 ms on the test machine: map points closer
  than a third to half a degree (about one screen pixel at this size) are dropped once at start-up; the land is worked
  out once per drawing and used for both fill and coast; d3's in-between resampling is off (`precision(0)`).
- Rule for the master chat, amended: anything that follows the finger must cost less than one screen frame. For the
  globe that means thinned data sized to the globe on screen. Carry this into the real app's globe.
- Dragging the globe by hand uses the same drawing and is faster too.
- Still unproven on a real phone; the test browser has no graphics chip.

### Event page hero: cleaner ladder, a little more globe (sub chat, 2026-11-16, on trial)

- The opening view shows a little more globe (126px held above the screen, was 150px).
- The ladder has no rules between its rows; white space separates them.
- The Event row is the small "Event" label alone. Its stepper is gone: the two named buttons under the title
  ("Before, in this chapter" / "Next, in this chapter") do that job and name where they go.
- The line "You are reading this event within the story ..." is gone when the reader came through a story; the Story
  row says it. A reader with no route still gets the one line and the offer to choose a story.
- The two named buttons keep their top rule and lose their bottom rule.
- On trial: Cade has not yet confirmed these.

### Event page hero: Event row in the ladder, hint clear of the globe, type signs in the globe view (sub chat, 2026-11-16)

- **Event is the ladder's last row.** Chronicle, Story, Chapter, Event share one label column, and the title follows
  as the event's name. The Event row carries two counts in small grey text and no arrows: "2 of 5 in this chapter ·
  6 events in the story". PLACEHOLDER figures: "2 of 5" was already a placeholder; the story count is the number of
  the mock chain's events that the stand-in story holds. The real page needs both from the link table.
- **Hint.** "Globe 1919 · pull down to open" is centred under the globe's lowest point, smaller and lighter, and no
  longer crosses the globe's edge. The title block sits 26px lower to make room.
- **Type signs** show in the globe view, after the date and place. They stay out of the hero.
- Proposed rule for the master chat: words never cross the edge of the globe; a caption for the globe sits clear of it.

### Event page hero: the story's events sheet, plainer step buttons, type sign after the place (sub chat, 2026-11-17)

- **Type sign after the place** on the hero's date line (Cade reversed the earlier removal). No dot before it.
- **Step buttons** under the title read "Previous event in this chapter" and "Next event in this chapter", in small
  sentence-case grey. They carry no rules and sit closer to the date line. Cade weighed a count of events remaining
  and left it out.
- **"7 events in the story" is a link** on the Event row. It opens a sheet: the story's name, the events under their
  chapters in order, each with its size mark, year, country and type signs; the page's own event marked "This page".
  A row of type filters (All, then each type the story holds) shows one type at a time. Tapping an event opens it.
- PLACEHOLDER data throughout that sheet: the six events are the chain's events the old arc holds; the three chapter
  names and the split are made up for the mock; "The Armistice" is a row with no event behind it. The hero's counts
  now agree with the sheet ("2 of 3 in this chapter", "7 events in the story").
- Open for the master chat: the real page needs each story's ordered event list with chapter membership from the link
  table; and whether the sheet should also sort (by date, by size) as well as filter by type.

### Event page hero: chapter-first events sheet, step links, italic "Also in" (sub chat, 2026-11-17)

- A dot sits between the place and the type sign on the date line.
- **Event row:** "2 of 3 in this chapter" is the link; "7 in the story" follows as plain text.
- **Events sheet opens on this chapter**: chapter number, name and its events in order. A switch at the top reads
  "This chapter | Whole story" (red underline on the chosen one); the whole story lists every chapter. The type
  filter shows only the types present in the chosen scope and hides itself when there is one type.
- **Step links:** "Previous event in this chapter" and "Next event in this chapter (1 more)". The count is the events
  left in the chapter after this one. The arrows are gone; the names carry the thin red underline every link carries.
  That is what lets both fit side by side on a 375px phone.
- **"Also in 17 more stories"** is italic serif with no bold.

### Event page hero: one switch for the story view; arrows back on the step buttons (sub chat, 2026-11-17)

- **Story view line.** Above the ladder: "Reading within a story" on the left, "Clear story view ×" on the right.
- **Clearing is one switch for the page.** It drops the ladder to the no-route hero ("This event belongs to 18
  stories. Choose a story to read it within") and takes the story filter off the chain. Choosing a story again puts
  the ladder back and turns the chain's filter on for that story. Rule proposed for the master chat: the hero's story
  and the chain's story filter are one state; no page shows one story in the hero and another in the chain unless the
  reader changed the chain's filter by hand afterwards.
- **Step buttons** have their red arrows again, beside the event's name on the second line, with the label above.
  The names lost the underline they briefly had. Both fit side by side at 375px.
- The title sits about 10px closer to the Event row.

### Event page hero: two voices only (sub chat, 2026-11-17)

- The hero's type is held to two voices. Labels are the ladder's small sans capitals; names are the serif.
- The story-view line follows that: "STORY VIEW" as a ladder label on the left, "Clear story view ×" on the right.
- In the small sans, anything a reader can tap is the darker grey at medium weight ("Clear story view", "2 of 3 in
  this chapter"); plain counts stay light grey. The × is grey; red stays for arrows, signs and link underlines.
- "Also in 17 more stories" stays italic serif at Cade's request; it is the hero's one italic.
- Proposed rule for the master chat: a block of controls uses at most two type voices, and weight plus a darker grey,
  never a third face, marks what can be tapped.

- Amended the same day (Cade): the story-view line reads "Reading within a story" again, in the small sans, italic,
  sentence case. It is no longer a capitals label.


### Sources, tappable figures and Cite this page in the mock (sub chat, 2026-11-17)

Built at Cade's request, following the master chat's message of 2026-11-16. Everything shown is a labelled placeholder.

- **Sources** sits at the end of The Record, after the two exits, as one more fold of the same kind (same plus
  sign), **closed by default on Cade's decision**. The master chat's note said "a visible Sources list"; Cade chose
  a closed fold. Its words are in the page when it loads, which is what search needs (seo.md, Growth). For the
  master chat to settle in event-pages.md: "visible" means present in the page and one tap away.
- Each entry: its kind in small capitals (Primary record, Scholarship), its title in serif, then author, title,
  year, publisher or archive, link. The mock's three entries are placeholders and cite nothing.
- **A figure is a tap.** Trial mark: a thin dotted grey underline, unlike a link's red line; gilt and solid while
  open. A tap opens a note under the paragraph, in the page (no pop-up): the figure, then Source, Year, Basis,
  Range, and "Show in Sources", which opens the fold and scrolls to the entry. A second tap closes it. The mock
  marks three figures in the Overview's first paragraph only.
- **Cite this page** sits under Sources. It opens a sheet with APA, MLA and Chicago; the reader picks one, the
  citation is written with today's date, and Copy copies it. The page address is a placeholder.
- Open for Cade through the master chat: whether figures in The Record and the chain's notes take the same mark;
  which citation styles to offer; whether Cite also sits near the top of the page.
