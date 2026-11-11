# Meanwhile Atlas: narrative flow, tiers, flavor and the six places (agreed 2026-11-03)

Supersedes the tier definitions in story-method.md where they conflict. The full version with the drawings and the worked tables is the "Meanwhile Atlas: Build Plan" doc in Cade's Claude project.

## Narrative flow

Every level of the atlas is made of the summaries of the level below, and every move a reader makes, up, down or across, lands on the same argument at a different depth. A chronicle read in two minutes and the same chronicle read in two hours tell one story; the long one adds evidence, never a different claim.

Five tests, checked by the flow editor on every story and chronicle assembly:

1. Composition. A story's text says nothing its patches do not carry; a chronicle's text says nothing its stories do not carry.
2. One change per patch. Each paragraph of a story covers one change, with as many knots as there are, including none (docs/structure.md).
3. The connector test. Between any two patches the unspoken word is "therefore" or "but". If only "and then" fits, the patches merge or one is cut.
4. Causation runs through every level. A fibre can spark a knot; the graded arrow is the same object at every depth.
5. Orientation. On every page the reader can say where they are, what came before and what comes next: breadcrumb, previous and next knot, the parents this page belongs to.

## The levels

Atlas (the globe, the year, the doors) > Chronicle (a place, practice or transformation; a portrait, no thesis; its page is its story summaries) > Story (a phase; carries the argument) > Patch (one paragraph around one knot) > Event. The link (type, grade, confidence) runs across the levels between any two events or stories. Themes are read off the links, never assigned.

## The three tiers are events

All three tiers are events: a thing that happened on a date in a place, with a page, carrying at least one arrow.

- Knot: an event that changed the course of history for much of its world.
- Fibre: an event that changed the course of history for one people or region.
- Strand: an event that changed the course of things for part of a people: a city, an institution, an army, a movement.

The order of size is knot, fibre, strand; the full tests are in docs/structure.md.

Figures, documents and quotes are detail. Detail is a section of a page ("The detail"), never a tier. A fact that carries no arrow is a line inside its parent page, never an event.

Tier belongs to the event (Cade, 2026-11-11). Each event is rated once, by its impact on world history, and carries the same size in every chain; the tests are in docs/structure.md, which wins where this file differs. The data model records one tier per event.

Going deeper opens a chain. There is no fourth tier. A reader who wants more than a fibre opens the event as a chain of its own, where it becomes a knot with strands and fibres under it. Readers see three plain labels (turning points, the full story, every detail); knot, strand and fibre stay internal.

## Flavor

Flavor is the texture that belongs to one chronicle and no other. The transplant test: swap the proper nouns in a paragraph for those of another chronicle; if the paragraph still reads as true, it fails. A page draws on at least three of four sources: constraint (geography, demography, money), institution (by its own name, with one line on what it did), actor (role, name, the option declined), the expert's nod and the fact against. A detail earns its place by changing the judgment.

## The two checking agents

- Flavor check: reads one page or one story; runs the transplant test on every paragraph; counts the sources; checks every actor has a role and every verb is specific. Fails on any transplantable paragraph, fewer than three sources, or a missing nod or fact against. Runs beside the fact-checker, style editor and red team.
- Flow editor: reads a whole story, then a whole chronicle, top down and bottom up; runs the five tests. Runs on every assembly and after any page in it is rewritten.

Both return a list of places with the failing test named, never a rewrite.

## The six places

One front door; six places that read the same objects (events, links, people, polities, layers, themes):

| Place | Question it answers | Extra checks |
| --- | --- | --- |
| Great people | Who | Chain check: every life event is an atlas event; every impact claim is a graded link. Quota check at selection |
| Political globe | Where and when | Record check: every border change cites the reference record. Placement check: every event has a place, a year, a lane |
| Event pages | What happened | The standard four reviewers, then the flow editor |
| Explore globe | What the world is made of | Licence check per layer; rank check: every ranking reproducible by script |
| Great themes | Why | Real-question check; three-civilisation check; node check (every thinker, work or event named is a page) |
| Timeline | What else was happening | Web check: every arrow drawn is a graded link and every on-screen link is drawn. Coverage check: every region has an event in every span, or the gap is marked |

One year cursor moves the globe, the stories, the themes and the timeline together. Only the Explore globe stands outside it. A name in any text opens a card (role, years, one line) with a button that follows that person's own chain.

## People

A person page is an event page turned ninety degrees: a life read as a chain. Parts: Overview, the life (dated events on the globe), impact (graded links, with the counterfactual sentence where Necessary), constraints, the option declined, today. Length follows the links a life carries, never fame. Candidates from Pantheon (MIT, 11,341 verified biographies); the cut by links, never by quota (docs/structure.md, People, 2026-11-11, which wins here): a life, a card or a name, with an audit of the shares and gaps left where the record leaves them. The front door of the section is a theme essay on the great man question, which the atlas answers with a number: the share of Tier 1 knots whose chain holds a person-level link graded Necessary.

## Eras without modern data

Where the modern series stop, the agent names the best record that exists for the era (chronicles, tax rolls, census fragments, archaeology, the Maddison and Seshat estimates), states its basis and range, and writes the figure as an estimate with that basis. A field with no record for an era is blank and says so. Picking the right record is the agent's job; inventing one is a hard limit.

## Fields the model needs (agreed 2026-11-03)

- Link.actor: the person whose decision the mechanism runs through, if any, with one flag: does the counterfactual hold if that person is removed? Actor named and flag "no" = a person-level Necessary link. The share of Tier 1 knots whose chain holds one is the great man number; the pipeline computes it.
- Event.actors: the polities and people involved, each with a role (initiator, target, ally, victim, mediator).
- Event.place: a point, always; an extent where the event covers ground (a war, a famine, a plague).
- Event.time: a date with its precision (day, month, year, decade, approximate) and era (BCE or CE); a span where the event lasts, with the date that places it on the timeline named.
- Event.tags: several per event from a fixed list: political, war, economic, ideas, religion, science, culture, environment. Tags never affect tier. Tags feed the Practice and Transformation chronicles: an event tagged science is a candidate for the gunpowder chain and the pipeline proposes it.
- Event.exits: a verified Wikipedia article and a verified Britannica article on every event; a person carries the same two. No page ships without them.
- Page.status: draft, reviewed or published, with the audit line and the date of the last check. The site hides unpublished pages; the flow editor reads only reviewed pages.

The cannon test: the bombards at the Theodosian Walls are a strand inside the 1453 knot in the Ottoman chronicle and a knot in a gunpowder chronicle. Same event, two sizes; the tags let the second chronicle find it.

## Pictures

An image earns its place as a visual does: by showing what the prose cannot (a portrait painted in the sitter's lifetime, a drawing of the siege, the plan for D-Day).

Sources: only those that state an open licence or public-domain status on the file itself, with the licence recorded beside the image: Wikimedia Commons (licence metadata readable by script), the Met Open Access collection (CC0, API), the Rijksmuseum, the Library of Congress, the US National Archives (US government works, including the D-Day plans and most twentieth-century war photographs), Europeana, Gallica, the Wellcome Collection. A museum page that shows a work without terms is a lead, never a source: for Bellini's 1480 portrait of Mehmed II, use the Commons reproduction with its licence line, since the National Gallery's page states no terms.

Every image carries in the repo: source, creator, date made, licence, credit line, alt text. The reader sees one short line under the image, plain description, no source: "Mehmed II, painted by Gentile Bellini in 1480, the year before the sultan died." The line says what it is and when it was made; a later artist's imagination is labelled as such. A public-domain or CC0 image shows no credit anywhere; a CC BY image shows its credit behind a tap on the image, since the licence requires it.

Out: photographs of living people; stock imagery; any file whose licence cannot be read from the source; decoration. Never forced: the agent looks for a picture on every page, and a page with nothing worth showing ships without one, finished. A battle needs no plan; a photograph or painting of the battle is the picture, and a plan appears only where the plan itself is the point.

Build: images are assets on R2 beside the map tiles, sized at build for phone and laptop; the design system sets the treatment; the `/image <event>` skill searches the open sources, checks the licence by script, writes caption and credit, and places the image. No licence line, no image.

## A seventh object: the feature (agreed 2026-11-03)

A named piece of the physical or economic world: strait, field, lake, river, range, plain, farmland belt, port, mine, reef. Fields: type; geometry (point, line or area); the layer it is drawn on; a brief on what it is and why it matters, in hard facts; figures with source and year; exits; links to the events and chronicles that ran through it. Features link from any text as [[feature-id|words]] and open a card on tap (type, one line, Read more). A feature earns its page by carrying at least one link; the rest stay labels on the map. The shared objects are events, links, people, polities, features, layers and themes.

The Explore globe opens on the present: it is the board on which the chains are still being played. Its trade view draws a country's top exports and imports by product, its main partners as flows, and the ports and chokepoints its trade depends on (OEC and UN Comtrade for goods; the World Bank shipping density for routes), each figure with its year; tapping a chokepoint inverts the view to who depends on it.

## Getting around (agreed 2026-11-03)

One navigation bar, the same on every page: Back (returns to the exact place and year left); the six places as six words (People, Globe, Events, Explore, Themes, Timeline) with the current one marked; the year, which is the shared cursor and opens the year card; search. A rail down the left on a laptop; a strip along the bottom on a phone. Every page carries its breadcrumb (Atlas > Ottomans > Rise > 1453). Any page is at most one tap from the Timeline and the Globe at its own year, with the item highlighted. One preview component everywhere: hover, or tap on a phone (amended 2026-11-05: few readers find a long press), any name, dot, card, marker or bar and it shows the picture where there is one, the one line, and Open. The card is an overlay: the reader never leaves the page; closing it lands on the same sentence. Only Open or Read more navigates, and Back returns to the exact spot. Polity names link like people and features ([[polity:id|words]]): the card shows the polity's type and years, one line, and a globe thumbnail of its territory at the page's year with the place in the text marked (Genoa, maritime republic, 1099 to 1797, with Galata marked at 1453), and Open the chronicle. A polity card carries two buttons: Open country, which goes to the Political globe at the page's year centred on that polity with its territory lit and its profile open; and Open the chronicle. Whenever a card's button leaves the page, a Return chip appears in the navigation bar named for where the reader came from ("Return to Fall of Constantinople, 1453") and takes them back to the same sentence; it stays until tapped or until the reader moves on to something else. A feature card (the Bosporus, the Ghawar field, Lake Victoria) carries Open on the map, which goes to the Explore globe centred on the feature with its layer on, and Read more for its page. The same Return chip serves people, features and events opened from a card. A curious reader's question is answered without losing the thread.
