# The page system (consolidated 2026-11-17 from the chain sub chat's log)

> **Status (master chat, 2026-11-17).** Cade confirmed that the decisions made with the event sub chat stand and carry to every page. The decided items of section 7 are now written into CLAUDE.md, event-pages.md, house-style.md, structure.md, narrative-flow.md, architecture.md, palette.md and ui-rules.md; where those files still show an older rule, this file wins on every item it marks decided. Items marked on trial or proposed are not rules. The six rules the sub chat proposed (H3) are confirmed by Cade and count as decided. The full working log is `docs/design/event-page-log.md`.

## What this is

This is the design system as built in `docs/design/mocks/event-v12.html` (version 182), decided by Cade
between 2026-11-11 and 2026-11-17, written down for every page type: chronicle, story, chapter and event.
It consolidates the two handoffs in `docs/state.md`; where a later entry replaced an earlier one, only the
later one is here. Every item carries a status: **decided** (Cade asked for it or confirmed it), **on
trial** (built, seen by Cade, unconfirmed) or **proposed** (a rule the sub chat drafted for the standards).
"Mock" means event-v12.html; line numbers are approximate. The mock's CSS is layered, so the last rule for
a selector is the one in force. No standards doc has been edited yet; section 8 lists the edits.

## 1. Carries to every page (decided, except where an item says on trial or proposed)

### Type

- **Three families** (decided, 2026-11-14). Cormorant Garamond takes the title role: page title, section headings, opening line, Record answers, italic notes, card titles, names in the hero. Newsreader stays the reading face. Public Sans stays the face for labels and controls. Tokens, mock line 22: `--display:"Cormorant Garamond","Newsreader",Georgia,serif`, `--label:"Cormorant Garamond",Georgia,serif`, `--body:"Newsreader",Georgia,serif`, `--ui:"Public Sans",system-ui,sans-serif`. Loaded at line 3: Cormorant 400, 500, 600 and italic 400, 500; Newsreader 400, 500, 600 and italic 400; Public Sans 400, 500, 600. palette.md and the stack still name EB Garamond.
- **Sizes** (on trial, 2026-11-14). Page title `clamp(32px,8.4vw,48px)`, weight 500, line height 1.02 (`.tw h1`, lines 89 and 1114). Section heading 24px, weight 500 (`h2`, line 1115). Opening line 19.5px on 1.42 in `--lede` (`.bluf`, line 1119). Reading text 17px on 1.6 (`body`, line 44). Record answer 16.5px, Record text 16px (lines 1116 to 1118). Italic note under a heading 15px (`.take.how`, line 665). Labels run 9 to 11.5px in Public Sans; the sub chat advised a floor of 10px and Cade has not taken it up.
- **Side margins 20px** (on trial, 2026-11-12), was 16 (`body`, line 1021). The chain, the tabs and the Record's index row still reach the screen edge.
- **Two type voices in a block of controls** (proposed, 2026-11-17). Labels are small sans capitals (9.5px, weight 500, letter-spacing .11em, `--ink3`; `.route .rl`, line 1487). Names are the serif (16px, weight 500, `--title`). In the small sans, what can be tapped is `--ink2` at weight 500; plain counts are `--ink3` at 400. A third face never marks what can be tapped.

### Colour

- **The tokens are palette.md's, unchanged** (decided, 2026-11-08; mock lines 15 to 40). The mock adds tokens palette.md does not list: `--well #EFE9E1 / #150E0B`, `--card #FCFAF6 / #2A1D17`, `--halo` (same value as `--here`), `--glass`, `--scrim`, `--shadow`, `--shadow2`, `--lift`, `--chain #F0EBE3 / #160F0B` (the chain's band, the colour of the globe's sea; line 817), and three map fills `--mger`, `--mnew`, `--mhatch` (line 468). Each has a light and a dark value.
- **Red outside the chain** (decided, 2026-11-12 to 2026-11-17). Red now also marks: the year switch on a graphic, the signs on the date line, the arrows on step buttons and steppers, link underlines, and the one Play button. palette.md says the accent belongs to the chain alone.

### Links

- **Underline width 0.6px** (on trial, 2026-11-14), was 1px: `text-decoration-thickness:.6px`, colour `--accent`, offset 3 to 5px (`.lk`, line 101). A phone draws it finer; a desktop screen still draws 1px.
- **A link with its own sign takes a red sign and no underline; a link in running text keeps the thin red underline** (decided for the date line, 2026-11-17; proposed as a site rule). Mock: `.tw .sub .jump`, line 1560: sign 15px, `--accent`, stroke 1.3.
- **A date opens the timeline at that date; a place opens the globe at that place** (on trial, 2026-11-16, "a rule in the making"). Both sit on the date line and stay in the docked header.
- **Every small text link has a 44px invisible tap area** (decided, 2026-11-12): an `::after` pad, for example line 1561.

### Gilt

Gilt stays a line and never becomes text. Its uses as built:

- **Heading stroke** (in the mock, comment dated Cade 2026-11-12; the log holds no entry). A pen line under every `h2`: `min(250px,72%)` wide, 1.8px at its thickest, starts as a hair, fades out to the right (`h2::after`, line 399). palette.md says 150 by 3px.
- **Tab cartouche and the faint line under each tab** (decided, 2026-11-08; unchanged; lines 112 to 119).
- **Cartouche round sheets and pop-ups** (decided, 2026-11-11). See "Sheets" below.
- **Picture marks** (decided, 2026-11-11): fine double corner marks. See "Pictures".
- **Graphic rule** (on trial, 2026-11-11): the plate's outer line. See "Graphics".
- **The eleven signs** (decided, 2026-11-11 and 2026-11-12): eight kind signs and the globe, timeline and quiz signs, drawn Fine in gilt, hairline strokes, square joins (`.ki`, stroke 1.25, 15px on cards).
- **Small gilt marks**: the 1px line under whatever is switched on in a control strip; the open diamond bullet (5px, 1px gilt border, turned 45 degrees; line 1462); the plus sign; the chain's top rule (on trial, 2026-11-14).
- **The divider diamond is gone between sections** (decided, 2026-11-14). `.layer > .sep{display:none}`, line 1220. Every break between sections is the same gap.

### Corners, pills and spacing

- **Square corners** (on trial, 2026-11-11; "Cade leans this way"). One block squares links, figures, cards, sheets, buttons and the Record (line 350). Round is kept for the globe, the fibre dot, the strand ring and the pin. The story and chapter mocks are still rounded.
- **Fewer floating pills** (decided, 2026-11-11). A bordered pill with a shadow reads as stock design. Back, the globe caption and "Also in" are plain type. Controls sit in ruled strips.
- **One gap between sections** (decided, 2026-11-14; Cade wants it site-wide). `--secgap:68px` on a phone, about two blank lines of reading text, applied as the top margin of every section heading after the first and above "Where next?" (lines 1217 to 1219).

### Tab row

- (decided, 2026-11-08; unchanged) A sticky row of section names in the title face, 15.5px, 86px below the top (`.pageindex`, line 106). The selected tab grows to 105 percent, the rest shrink to 94, and the cartouche draws itself in 0.8s.
- **Hairline** (decided, 2026-11-11; amended on trial, 2026-11-12). The log's decided entry: a hairline sits under the row at rest and fades out once the row sticks. The later trial entry: a hairline stays under the docked tabs and replaces the soft fade. Log and mock disagree with the decided entry: the mock follows the trial (lines 1057 and 1058: the fade is off and the hairline stays when stuck).
- Log and mock disagree on one label: the section heading is "Historical Chain" and its tab reads "The Chain" (line 2057).

### Docking title and docked header

- **The title holds its full size for the first part of the scroll** (decided, 2026-11-11). The shrink starts at 45 percent of the docking distance `--D` and ends at 100 (lines 58 and 1569). Docked scale 0.46, or 0.38 for a two-line title (line 1976). The path block fades from 30 to 72 percent.
- **Docked header: three lines in an 86px band** (decided, 2026-11-11 to 2026-11-16): the title; the date line with the place kept ("28 June 1919 · Versailles, France"; Cade, 2026-11-12); a third line. With a route the third line reads "‹ The Treaty · ‹ Before · After ›" (`.hsub`, line 1676). With no route it reads "In 18 stories: choose one ›" and opens the stories sheet. The docked header is never an empty band. The band's edge line shows only once the title has docked.
- **The small globe** rides at the top right at 52px and 78 percent opacity. No small picture rides in the docked header (decided, 2026-11-11; `.pthumb{display:none}`, line 596).
- **Top row**: Back as plain type and a search magnifier beside it; both fade once the title docks (`.topbar`, lines 1679 to 1682). On trial with the bottom bar, below.

### Hero

Top to bottom for a reader who came through a story (decided, 2026-11-17, unless marked):

1. **Globe strip.** A strip of the globe above the hero, turned so the pin and the place name sit inside it. The place is lettered on the globe beside its pin, italic 19px in the title face (line 1949). On trial: 126px of globe held above the screen (`HIDE=126`), a 50 degree tilt (`TILT=50`).
2. **Hint.** One centred line under the globe's lowest point: "Globe 1919 · pull down to open", 10.5px, `--ink3` (`.hint`, line 1604). Words never cross the globe's edge (proposed, 2026-11-17). On trial: the title block sits 26px lower to make room.
3. **Story view line.** Left: "Reading within a story", small sans italic 11.5px. Right: "Clear story view ×" (`.rview`, lines 1647 to 1650). Clearing is one switch for the page: the ladder folds to the no-route hero and the chain's story filter turns off. Choosing a story restores both.
4. **Ladder.** Rows in one 74px label column: Chronicle, Story, Chapter, Event (`.route .rrow`, line 1517). Chronicle carries "Also in 17 more stories" at the right. Story and Chapter carry steppers ("8 of 12", "1 of 3") with red arrows; an arrow greys at the first or last. A name is a link up to that page. On trial (2026-11-16): no rules between rows, 31px row height.
5. **Title**, close under the last row.
6. **Date line.** Red timeline sign, date, dot, red globe sign, place, dot, type sign in gilt. 16px title face, `--ink2`. The date is neither bold nor red. Nothing on the line is underlined.
7. **Step buttons.** Two, side by side, no rules: a small label above (10.5px sans), a red arrow beside the name (15px title face) (`.chapnav`, lines 1631 to 1640). Both fit at 375px.

Carries to every page: the globe strip, the hint, the level rows above the title with the page's own level
as the last row, the title, the date line with its signs, a pair of step buttons that say what they step
through, and the rule that every "next" names what it is next in (proposed, 2026-11-16). The story view
line carries to chapter pages; a story or chronicle page needs the master chat's ruling.
Event-specific: the Event row's counts ("2 of 3 in this chapter" as a link, "· 7 in the story" as plain
text, no arrows), the type sign, the words "Previous event in this chapter" and "Next event in this
chapter (1 more)", and the events sheet.

- **The hero's story and the chain's story filter are one state** (proposed, 2026-11-17).
- **The level label is light grey** (decided, 2026-11-15): "it only needs to be findable".

### No-route hero and "Also in N more stories"

- **"Also in N more stories"** (decided, 2026-11-11; set italic serif, no bold, 2026-11-17: `.alsoin`, line 1629, italic 14px). The count and the list are by story, never by chapter. It opens the stories sheet. Choosing a story makes the page follow that path.
- **No route** (decided, 2026-11-11; wording on trial, 2026-11-16). A reader from the globe, the timeline, search or an unrelated link sees no ladder and no step buttons. The hero reads "This event belongs to 18 stories." over one link, "Choose a story to read it within", which opens the same sheet. A page always shows a way into its stories (proposed, 2026-11-16). The offer stays at the top; in the docked header the third line repeats it. Not revisited in the last round.

### Globe view

- **Scrolling never opens it** (decided, 2026-11-17). The top of the page is the page's own view; a fling up the page stops there (`html{overscroll-behavior-y:none}`, line 1663).
- **A separate, weighted pull opens it** (decided, 2026-11-17). At the top, a new pull down moves the page away, fades the hero and brings the globe to the middle with the place centred. Letting go early returns. On trial: 300px of finger travel (`PUSH=300`), commit at 60 percent, eased by the power 1.7 (line 2019). A fresh wheel turn does the same on a desktop.
- **In the globe view** (`.gview`, lines 1666 to 1672 and 1579): the year at the top; the name, date, place and type signs at the foot; "Back to the event". A swipe up, the button or Escape returns.
- **Smooth at every speed** (decided, 2026-11-17). Off under reduced motion; the place link and a tap on the docked globe remain the ways in.

### Sheets in a gilt cartouche

- **Every sheet and pop-up sits in the notched gilt cartouche** (decided, 2026-11-11 and 2026-11-12): the title panel of an old map. Corners notched at an 11px radius (`.sheet.gilded`, line 794; `.sheet.places`, line 277); the outer line 1.3px draws itself in 0.9s, a lighter 0.7px inner line fades in (`.places .frame`, lines 281 to 284). The outer gilt line is kept light.
- **Build** (decided, 2026-11-12). The frame stays still, only the text scrolls, and the buttons sit in a footer under a rule as equal squared buttons 44px tall (line 796). A pop-up takes half the screen at most and opens about a tenth of the screen above the bottom edge. On a wide screen it stands at the right and the page stays still.
- **Stories sheet** (decided, 2026-11-11). Stories grouped under their chronicles, a scroll, the reader's own path ticked, a find box when the list passes eight (line 2640).
- **Events sheet** (decided, 2026-11-17; line 2668). Opens on the chapter: chapter number, name, its events in order, each with size mark, year, country and type signs; the page's own event reads "This page". A switch reads "This chapter | Whole story" with a red line under the chosen one. A type filter shows one type at a time and hides when the scope holds one type. Tapping an event opens it.
- **Picture details** use the same cartouche (line 2732).

### One plus, no pop-up messages

- **One plus for everything that opens and closes** (decided, 2026-11-16; a rule for the site). Two thin gilt strokes, 11px by 1px (9px on the Key); the upright one turns to lie flat as the thing opens, in 0.2s; still under reduced motion (`.keybtn i`, line 1151; `.rec summary::before`, line 1510).
- **No pop-up messages** (decided, 2026-11-15; "a standing preference, said twice"). A control is never answered with a message that appears and fades. The result shows in place: counts, the state of the control. Log and mock disagree: the mock still shows a transient slip after choosing a story in the sheet ("The page now follows ...") and after a jump from a note ("Centred on ..."), line 2578. Its other slips ("Would open ...") are mock-only stand-ins for navigation.

### Bottom bar

- (on trial, 2026-11-11; the master chat decides, since the bar is site-wide) The event mock shows no bottom bar (`.pill{display:none!important}`, line 585). Search is the magnifier beside Back and is out of reach mid-page. The globe and the year sit in the docked header; the globe and timeline links in "Where next" take over part of the bar's job. The story and chapter mocks still carry the bar.

### Meanwhile

The same section goes unchanged on story and chapter pages.

- **A section of the page, after the page's own content** (decided, 2026-11-11). Heading "Meanwhile", an ordinary `h2` with the gilt stroke; no diamond divider before it (2026-11-14).
- **Shuffle** (decided, 2026-11-12). A gilt shuffle sign, 22px in a 44px target, at the right of the heading; a tap draws again and the sign turns 180 degrees in 0.35s (`.mwshuf`, lines 1011 to 1017). It hides when the pool holds six or fewer.
- **Six events at most** (on trial, 2026-11-12), drawn at random from the events within the window and set in date order (line 2714).
- **Window of years**: two years either side of the event in the mock. A placeholder (2026-11-11).
- **Layout, third pass** (on trial, 2026-11-12). Two columns, gap 20px by 18px, no rules, no underlines (`.mw`, line 653). Each entry is a dateline: size mark and year (11.5px sans, weight 600, `--ink3`) with up to two kind signs (13px, gilt); the name (17px title face, `--title`); the place (12px sans). The whole entry is the tap target. No graded line to the page's event shows here.
- Cade wants the place as "City, Country" on every entry; the data needs separate fields.
- In the mock and absent from the log: one italic line under the heading, "What else was happening around the world at the time of this event."

### Where next

- (on trial, 2026-11-12; links amended by Cade, 2026-11-14) A closing block after the last section, outside the sections, with no `h2` (`nav.onward`, lines 1842 to 1856; CSS 924 to 965 and 1125 to 1129). A centred italic line "Where next?" (17px). "Open one at random": a chronicle, a story, an event, a person, as underlined links with gilt diamonds between. The globe ("the world in 1919") and the timeline ("around 1919") as a pair. "Have you taken today's quiz?" is the one gilt-framed item with the one red button, "Play"; the quiz is deferred, so the button is a placeholder.
- **The three signs** (decided, 2026-11-12): a library globe carrying the diamond, the dot and the ring; a rule of years carrying the same three marks; a question mark in a diamond.

### Pictures

- **One picture per page, as an inset beside the opening paragraph** (decided, 2026-11-11). A small upright plate, 40 percent of the column, 4 by 5, floated right; the paragraph wraps round it (`main.pic-c`, lines 431 to 440).
- **Frame**: gilt corners. Fine double corner marks set tight to the photograph, 12px and 7px arms, 1px, and a soft shadow that lifts it (lines 457 to 461). A light sepia filter (line 412).
- **Caption**: one short line of description, centred, italic 12.5px (line 434). It is a description; no credit is printed under the picture.
- **Scroll**: it grows a little as it rises (6.5 percent at most), then eases back and fades; it returns when the reader scrolls back (line 2727).
- **Tap for details** in the gilt cartouche: caption, date, place, source, licence, credit.
- **No usable picture, nothing shown.**
- **What a picture may be** (decided, 2026-11-11), as recorded: a later drawing or painting is allowed for an event too old for photographs. A photograph of the place or of that kind of scene is allowed. "A photograph of a living person is allowed. This reverses a hard limit in both docs; no such picture ships until they are changed." Pictures come from open sources, as Wikipedia's do, avoiding Wikipedia's own lead picture where another serves. Source, licence and credit stay recorded beside the file.

### Graphics

- **Title** (decided, 2026-11-12). Every graphic carries a title that says plainly what it shows: whose, what, and the span or comparison. "Germany's borders before and after the Great War".
- **Plate** (on trial, 2026-11-11). A gilt rule outside (55 percent gilt), a fine rule 4px inside, a slight shadow, on `--surface` (`.fig`, lines 669 and 670). All graphics share one frame.
- **Guiding principles** (proposed, 2026-11-15; Cade's direction after he found the first graphic far too big). One graphic makes one point and its title states it. Half a screen at most: about 420px on a phone for the picture, its key and its caption (395px in the mock). The picture carries the facts; words inside the frame are a title, a one-line key and one caption line. Nothing the picture shows is repeated as a list under it. The still image must make the point; a tap adds detail in one line of fixed height and never changes the graphic's size. No empty or placeholder slot. A caption reads as a history textbook's would and never mentions the atlas's records or method.
- **Key and switch on one row** (in the mock, `.bamrow`, line 1409): key at the left, the year switch at the right. The switch is red (decided, 2026-11-12).
- **Results sit inside the graphic** (decided, 2026-11-15). Figures that are results of what the graphic shows stand inside its frame under a short heading ("Results of the treaty"), three lines at most, each led by its figure in bold ink, never red (`.bamres`, lines 1458 to 1463). With them the graphic is about 500px tall. Other figures stay in By the numbers. They are generated from the data header.
- **Graphics hold still** (decided, 2026-11-15). They do not grow or shrink as they cross the screen; that effect is for pictures only.
- **Place**: last in the section it serves (decided, 2026-11-11).

### Performance, gestures, haptics, motion

- **Anything that follows the finger costs less than one screen frame** (proposed, 2026-11-17). For the globe: map data thinned to the globe's size on screen at start-up (land at 0.5 degrees, borders at 0.3; line 1933), the land worked out once per drawing, d3's resampling off (`precision(0)`, line 1936). One drawing fell from about 40ms to about 7ms on the test machine.
- **No pre-drawn frames blended together** (decided, 2026-11-16). Cade saw them look laggy at slow speed. The globe is drawn in full at every step.
- **A gesture that leaves the page for another view is a separate, deliberate pull, never the tail of a scroll** (proposed, 2026-11-17).
- **Haptic tick** (decided as welcome, 2026-11-15; confirmed working on Cade's iPhone, 2026-11-16). On an iPhone each button that ticks carries an invisible real switch laid over it (line 2393). Android vibrates through the page. Nothing may depend on a tick. The pull into the globe view buzzes at the commit point on Android only (on trial).
- **Nothing switches; everything eases** (decided for the chain, 2026-11-15; "a rule"). Any part of a card that appears, leaves or moves does so gradually, tied to the reader's drag.
- **A card in view is never blank** (decided for the chain, 2026-11-15; "a rule"). A card that peeks from behind another shows a faded copy of itself, words included.
- **A page rebuilds a view only when the width changes** (decided, 2026-11-12), since a phone fires a resize each time its address bar hides.

## 2. Event page only (decided, except where marked)

### Page order as built

(decided, 2026-11-11) The hero; the step buttons; the bottom line in one paragraph with the picture
inset; the tab row; **Overview**, with its graphic last; **Historical Chain**; **The Record**, with the
Wikipedia and Britannica exits at its foot (Cade, 2026-11-12); **Meanwhile**; "Where next?". Historical
significance, Lasting impact, What caused it, What it caused, and Before and after have no sections of
their own. The log's first entry put the exits after Meanwhile; the mock follows the later entry.

### Historical Chain

- **A sideways web** (decided, 2026-11-11). Causes run in from the left, effects out to the right, one column per step. Headers read "Cause · 1 step" and "Effect · 1 step" with the column's total in brackets under the name (2026-11-15). One italic line of directions under the heading (15px, `--ink2`).
- **One band** (decided, 2026-11-12). Controls, web and key sit in a full-width band tinted `--chain` with a hairline above and below; the top rule is gilt (on trial, 2026-11-14).
- **Reach 1 to 5 steps**; the chain opens at three (decided, 2026-11-12). The steps control sits in the foot between the two "more" counts (on trial, 2026-11-15).
- **Size filter** (decided, 2026-11-11). Knots, Fibres, Strands, each with its count in brackets whether on or off (2026-11-15). Opens with knots and fibres on, strands off.
- **Filters remove events and the web re-forms** (decided, 2026-11-11; this reverses "Filters dim, never remove" for the chain). An event the filters leave out that a path runs through stays as a full card, faded.
- **Filter panel** (on trial, 2026-11-12). Eight kinds as a grid of switches that add up, a three-way side switch (causes, both, effects), a Backbone switch, Clear and Done.
- **Story lens** (decided, 2026-11-15). Story is its own control, first in the bar: a sign over the word, with one red line under it when on. Arriving through a story turns its lens on; arriving any other way shows every link. The line above the chart is Cade's wording: "Cause and effect filtered to story: Weimar Germany", with "Show all". The panel is titled "Story filter" and lists "All stories", the story the reader came through, then the rest in alphabetical order. The chain itself never changes.
- **Backbone toggle** (on trial, 2026-11-11).
- **Cards** (decided, 2026-11-12 and 2026-11-15). One card of one size for every event; the mark alone tells the size. Top line: the mark, the year, up to two kind signs. Then the title. A foot line names the country. The page's own event has a red date line. The tapped event gets one thin gilt line.
- **Place rule** (decided, 2026-11-15). A card always names the country; a region where the event is larger than one country; a city only after its country ("France, Paris").
- **Long columns** (decided, 2026-11-12 and 2026-11-15). A column shows three events in the page; a longer one turns like a drum, scrolls with the phone's momentum, snaps to a row, and counts what waits ("2 more").
- **Dragging** (on trial, 2026-11-14). The chain slides sideways and settles on a column; a sliver of the next column shows at each edge. "Drag to explore" stands between Key and Zoom.
- **Key** (decided, 2026-11-14 and 2026-11-15). Folds behind a "Key" row with the plus sign; open on a first visit, closed after (`atlasKeySeen`); always open at 1100px and wider. It carries no counts.
- **Full screen** (on trial, 2026-11-14). A button at the right of the bar opens the same chain over the whole screen, at five steps. Zoom by fixed levels: two in the page, five in full screen; no free zoom.
- **Docked card** (on trial, 2026-11-11). A tapped event opens a card without a scrim so the web stays in use. It reads: size, year and step; title and kinds; the brief cut to three lines with "… more"; a "Caused by" row and a "Led to" row, three lines each at most, each ending in a chevron that opens the line's note. Closing the card returns the page to where it was.
- **Lines the web leaves out** (on trial, 2026-11-11). Coincident links, links that skip a step and links inside one step are listed under "How it connects" and never drawn.
- **Centred on another event**: two adjacent lines, "Centred on [event], [year]" and "Back to [the page's event]" (decided, 2026-11-16).
- **Empty side**: "No cause of this event is recorded yet." (decided, 2026-11-15).

### The Record

- **Layout C1, "Lighter"** (decided, 2026-11-13). A plain list of pieces, closed by default, one open at a time. Each row: the section name as a small grey label (9px sans capitals), the one-line answer as the headline (16.5px title face), a gilt plus at the right. The open text is flush, 16px (`.rec`, lines 1102 to 1118 and 1509 to 1512).
- **Pinned index row** (decided, 2026-11-12 and 2026-11-13). A row of the pieces' names sits above the list, pins under the tabs while the reader is inside The Record, marks the piece reached, and hides when an event has three pieces or fewer (`.recidx`, lines 898 to 909).
- **Pieces in the mock**: The account; What it did, and to whom; Why it held or failed; By the numbers; The common misreading; Today; The detail. The headings stay the fixed set; Cade expects the text and its organisation to be rewritten.
- **The name "The Record"** (on trial, 2026-11-11).

## 3. The grades as decided

- **"Sufficient" is withdrawn** (decided; Cade restated it on 2026-11-12: "we got rid of sufficient"). The sub chat holds no record of where it was first decided. The standards still list it. Six of the 36 pilot links are graded Sufficient and still show the word and the sentence "was enough on its own to bring about" in their pop-ups and notes. The master chat must say what each becomes.
- **Line styles** (decided, 2026-11-08; unchanged). Solid for Necessary, dashed for Contributing, dotted for Contested, all red; Coincident is grey with a cross-stroke and is not drawn in the web (`.gl`, lines 149 to 153). Lines leave from a port and arrive at a barbed head.
- **Confidence shows as line weight** (in the mock, line 2162): a backbone line is 2.3 wide and any other 1.35, times 1 for High, 0.84 for Moderate, 0.66 for Low. In a note's head the grade, confidence and years sit in one line ("Necessary · high confidence").
- **Words on lines**: the web prints no grade word on a line. The word shows in the key, in the note's head and in the pop-up's rows.
- **The key** (wording on trial, 2026-11-14; the sub chat's draft, to be checked against the standards): "Necessary. Without this cause, the effect would not have happened." "Contributing. One cause of several. The effect could have happened without it." "Contested. The evidence supports two readings, and the atlas gives no verdict." The three size lines above them use the definitions in structure.md.
- **The plain sentence** (decided, 2026-11-12). Each line gets one sentence generated from its grade, naming both events, set in italics: "The Russian Revolution was one cause of Hitler Takes Power among several."
- **The note** (decided, 2026-11-12, "FINAL"). The title with its graded arrow; the grade, confidence and years; the plain sentence; then three parts. The claim: what the atlas says happened; a Necessary line ends with what would be missing without the cause. The challenge (renamed from "The strongest objection"): the strongest case against, and nothing else. The verdict: one or two sentences answering the challenge. The verdict carries no rank, no list of other causes and no repeat of the grade words. A line with little or no challenge shows the claim alone.
- **A verdict no longer ranks the causes** (decided, 2026-11-12). Cade's reason: the rank is arbitrary, and the reader can see the other causes in the chain. Every cause the atlas relies on must be an event with a link.

## 4. On trial, not settled

- Square corners everywhere (2026-11-11).
- The bottom bar dropped from the event page (2026-11-11).
- Graphics on a plate (2026-11-11); the graphic principles as standards text (2026-11-15).
- The name "The Record" (2026-11-11).
- The chain's docked card without a scrim (2026-11-11); the Backbone toggle (2026-11-11); lines the web leaves out (2026-11-11).
- Where next (2026-11-12).
- Meanwhile: six at random, the two-column layout, the window of years (2026-11-12).
- Reading margins of 20px (2026-11-12); the hairline under the docked tabs in place of the fade (2026-11-12); the chain's filter panel (2026-11-12).
- Type sizes (2026-11-14); link underlines at 0.6px (2026-11-14).
- The chain by dragging with no scale bar; full screen; the folded key; the gilt top rule; the zoom levels (2026-11-14).
- The key's wording for the three kinds of arrow (2026-11-14).
- Steps at the foot of the chain (2026-11-15).
- The date and the place as jumps, as a site rule (2026-11-16).
- The no-route hero's wording (2026-11-16).
- Hero details: no rules between ladder rows; no stepper on the Event row; two type voices; 126px of globe; the 50 degree turn; 300px of travel; commit at 60 percent; the buzz; the title block 26px lower (2026-11-16 and 2026-11-17).
- Five hero options in `hero-demos.html`: superseded by the second handoff's hero.
- Three typeface alternatives in `type-sheet.html`: superseded by the Cormorant decision.

## 5. Open questions for Cade

1. Does the type sign need its word beside it for a first-time reader?
2. Should the events sheet sort by date or size as well as filter by type?
3. The no-route hero was not revisited. Does its wording stand?
4. Desktop layout of the hero, the globe view and the chain is not designed. The chain has no width cap.
5. Does the story lens narrow to the chapter the reader came through, or to its story? Does the control list chapters and chronicles?
6. Should a story lens dim the other events in place or remove them, as the mock does?
7. Does the page also offer the next chapter, now that the step buttons step events?
8. When the old data is re-tagged, does environment get events? Should a card show the political sign only where no other kind applies? (Political sits on 516 of 781 events.)
9. Should each event carry a short noun form for use inside generated sentences?
10. Present-day or period names for the country on a card?
11. A random Meanwhile changes on every visit, which works against a page a reader or a search engine can cite. Keep the random draw?
12. What does each of the six Sufficient links become?
13. Is the label floor 10px?
14. The pillared hall leans classical and Western; gilt signs on the card ground have a contrast near 3 to 1. Accept both?
15. Not proven on a real phone: whether Safari or the Claude app's frame takes the pull-down for its own bounce; smoothness of the fixed globe turn; the "doubling" fault of 2026-11-12; garbled text at the furthest zoom.
16. Not yet applied from the master chat's message of 2026-11-16: the Sources list, tappable figures, "Cite this page", every word in the HTML at load.

## 6. Placeholders in the mock

- The globe view is a stand-in for the Political globe at the event's year.
- Sizes: old tier 1 as knot, tier 2 as fibre, four events set as strands to show the filter.
- Hero counts and names: "8 of 12", "1 of 3", "2 of 3", "7 in the story", "17 more stories", "18 stories", "The Armistice" (no event behind it), "The Crash", "The Ruhr and the Mark".
- Events sheet: six real events from the old arc; three made-up chapter names ("The Treaty", "The Crash", "The Republic Falls") and a made-up split.
- Stories sheet: every row but the first. Story membership uses the old atlas's arcs.
- Meanwhile: the 19 events the old data holds for 1917 to 1921; the two-year window; the places.
- Countries on chain cards: added by hand for 33 events in `build-places.py`.
- The page text is mock text from the worked example. The briefs in pop-ups are Prototype 1 text.
- The two exits are standard addresses, unverified. The picture's licence is unchecked against the Archives' catalogue.
- The quiz button; the "Would open ..." slips; the Mock, Frame, Picture and Theme buttons.
- The results in the graphic are written by hand in the mock.

## 7. Standards docs that need an edit

Decided items only.

| Decided rule | Doc and passage | Proposed wording |
| --- | --- | --- |
| Cormorant Garamond is the title face | palette.md and the stack, where EB Garamond is named | "Titles, headings, the opening line and card titles are set in Cormorant Garamond; reading text in Newsreader; labels and controls in Public Sans." |
| Gilt has more uses | palette.md, `--gilt` row and Rules, "Gilt is a line, never text" | "Gilt also draws the cartouche round every sheet and pop-up, the corner marks on a picture, the signs, the plus sign and the line under a control that is on. It is never text." |
| The heading stroke is a pen line | palette.md, `--gilt` row ("150 by 3 px") | "A pen line under each section heading, up to 250px wide and 1.8px at its thickest, fading to the right." (Confirm with Cade: the log has no entry.) |
| The divider diamond is gone; one gap | palette.md, Rules; ui-rules.md, new rule | "Every section ends with the same gap before the next heading: 68px on a phone. No divider stands between sections." |
| Red on signs and switches | palette.md, Rules, "One accent, and it belongs to the chain" | "Red marks the chain and what opens something: a sign on a link, a stepper arrow, a link underline, the chosen side of a switch." |
| Sufficient is withdrawn | palette.md, Rules (line styles); house-style.md lines 104, 106, 120; structure.md lines 142, 167, 209; ui-rules.md rule 8; CLAUDE.md ("five grade words") | "Grades: Necessary, Contributing, Contested, Coincident. Solid for Necessary." The backbone is the links graded Necessary. The master chat rules on the six pilot links first. |
| A verdict carries no rank | house-style.md line 106 ("Contributing names the set and A's rank") | "Contributing: the other causes are events with links in the chain. The note names no rank and no list." |
| The note is claim, challenge, verdict | house-style.md line 108; CLAUDE.md ("states the verdict first, the challenge second"); event-pages.md, The argument | "A note has three parts: the claim; the challenge; the verdict, one or two sentences answering the challenge. A line with no real challenge shows the claim alone. The grade line and the plain sentence lead." |
| The plain sentence is generated | house-style.md, grades | "Each link shows one sentence generated from its grade and naming both events. No one writes it by hand." |
| Page order | event-pages.md, The layers and The sections; CLAUDE.md, "Never change a section heading or the layer order" | "An event page runs: the bottom line in one paragraph; Overview, its graphic last; Historical Chain; The Record, ending in the exits; Meanwhile." |
| The heading is "Historical Chain" | event-pages.md, The layers ("Follow Historical Chain") | Replace the name. |
| The chain is a sideways web whose filters remove | event-pages.md, layer 4; ui-rules.md rules 8 and 9 | "In the chain every event is one card of one size and the mark tells the size. The chain's filters remove events and the web re-forms; an event a path runs through stays, faded." |
| The Record is layout C1 | event-pages.md, layer 3; ui-rules.md rule 19 and Open | "The Record lists its pieces closed, one open at a time: section name as a label, the one-line answer as the headline, a gilt plus." |
| One picture, inset, gilt corners | event-pages.md, layer 1; narrative-flow.md, Pictures | "One picture per page, a small upright inset beside the opening paragraph, framed by gilt corner marks, with one line of description under it. A tap opens its details." |
| What a picture may be | CLAUDE.md hard limits; narrative-flow.md line 91 ("Out: photographs of living people") | "A later drawing or painting, a photograph of the place or of that kind of scene, and a photograph of a living person are allowed." No such picture ships until both docs are changed. |
| A graphic's title; results inside; graphics hold still | event-pages.md, Graphics | "Every graphic carries a title that says whose, what and the span. Results of what it shows stand inside its frame, three lines at most, generated from the data. A graphic does not move as it crosses the screen." |
| Fewer pills | ui-rules.md rule 6 | "Back, captions and 'Also in' are plain type. A bordered pill with a shadow is kept for nothing on a reading page." |
| Docking title | ui-rules.md rule 20 | "The title holds its full size for the first part of the scroll. The docked header's three lines are the title, the date and place, and the route or the offer to choose a story; it is never an empty band and carries no picture." |
| The hero's ladder replaces the breadcrumb | ui-rules.md rule 15; structure.md lines 332 to 337; CLAUDE.md ("a page without Back or its breadcrumb") | "Every page opens with a ladder of level rows above its title, each a link, the page's own level last. Step buttons under the date name what they step through." |
| "Also in N more stories"; no route | structure.md line 335 ("Also in N more"; "the page's home path") | "'Also in N more stories' counts stories and opens the stories sheet. A reader with no route sees no path; the page offers its stories in one link." |
| The globe view opens on a separate pull | ui-rules.md rules 14 and 20 | "Scrolling never opens the globe view. At the top of a page a separate pull down opens it; the place link and Back to the page are the visible controls." |
| One plus sign | ui-rules.md rule 16 | "Everything that opens and closes uses one sign: two thin gilt strokes, the upright one turning flat in 0.2s." |
| No pop-up messages | ui-rules.md rule 12 | "No control is answered with a message that appears and fades. The result shows in place." |
| Nothing switches; a card in view is never blank | ui-rules.md rule 12 | "A part of a card that appears, leaves or moves does so gradually, in step with the reader's drag. A card that shows at all shows its words." |
| No blended pre-drawn frames | architecture.md, budgets | "Anything that follows the finger is drawn in full within one screen frame; map data is thinned to its size on screen. Pre-drawn frames are never blended." |
| Kind and place signs | house-style.md or ui-rules.md, new passage | "The eight kinds and the globe, the timeline and the quiz each have one sign, drawn Fine in gilt." |
| Place on a chain card | structure.md or event-pages.md, the data header | "Every event carries a country field. A card names the country, or the region where the event is larger; a city follows its country." |
