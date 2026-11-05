# The timeline page (agreed 2026-11-03)

Full spec with the drawing: the Build Plan doc, The six places tab.

Layout: a grid. Columns = the nine regions in the atlas order (Europe, Middle East, South Asia, East Asia, Southeast Asia, Sub-Saharan Africa, North America, Latin America, Oceania) plus an Ideas lane for the themes' dated ideas. Rows = time, running down, scale widening toward the present as the Prototype 1 slider does. The ages strip and the year cursor never leave the screen. Cards by tier: knot = full card (title + one line); strand = half card; fibre = a dot that opens on tap. Arrows between cards in the fixed grade language (solid Necessary/Sufficient, dashed Contributing, dotted Contested, struck through Coincident); an arrow leaving the screen ends in a tappable stub. Right rail: the world-in-that-year card. The cursor is the globe's cursor: moving it here moves the globe, the stories and the themes.

Zoom: three fixed levels chosen with a control, never a free zoom (Histography rejected free zoom as too much effort; ChronoZoom found readers lose their place past about three nested levels).
- Century: 100-300 years per screen by density; knots only; Tier 1 links only.
- Decade: 10-30 years; knots and strands; people of the span as thin bars across the lanes; every link with both ends on screen.
- Year: 1-3 years; everything, fibres included; grade word on every arrow; the year card opens to the full world profile.
Tapping a card opens the event; a lane header opens that region's chronicle at the cursor year; the age name opens the age brief.

Filters (combine; dim the rest rather than remove it): region, tag, theme, chronicle, person, grade, polity (from the actors field).

Chain mode (the page's reason to exist): tap a card, Follow; the page draws the chain upstream and downstream, every hop a graded arrow, across lanes and years; everything off the chain dims; a breadcrumb of the chain's knots along the top; a grade bar showing the weakest arrow. Upstream and downstream are separate toggles. Depth defaults to three hops. Contested arrows show both readings on tap. Pull removes a Necessary event and greys everything downstream.

Other interactions, in build order: the meanwhile line (a band of years around a card, every lane, with the note that a coincidence is a coincidence unless an arrow says otherwise); the year card; lives as bars; compare two years (pin one, move the cursor); trace a theme with the Ideas lane open; today in history (also the game's seed); coverage (a faint hatch where a lane has no event for a span).

Phone: time runs down; lanes become region chips at the top, one or two open at a time; chain breadcrumb becomes a swipe bar; the year card sits behind a tap on the year. Same levels, same filters, same taps.

Checks: web check, coverage check, cursor check, provenance on the year card (docs/agents.md).

Preview: hovering a card or dot (a tap on a phone; amended 2026-11-05, since few readers find a long press) shows the preview card: the event's picture where it has one, title and date, the one-line description, Open. The same component serves every name, marker and bar in the atlas.
