# Meanwhile Atlas: vision and goal (agreed 2026-11-05)

Cade's statement of what the atlas is for. Every phase, page and screen is judged against
it. Where a later decision changes it, this file is updated first.

## The statement

History is best understood as a narrative: events linked by cause and effect, over the
short run and the long. Meanwhile Atlas gives readers the historical significance of
events, links them through time, places them on the globe, and tracks the people whose
impact shaped the modern world.

To understand a game of chess you must know the board. The geography view presents our
present world as an interactive map: how geography, resources and minerals, climate and
weather continue to shape our collective story.

Wikipedia tells you what happened. The atlas tells you why it mattered, what it caused,
and how sure we can be.

The atlas takes the long view of humanity's confrontation with the big questions, such as
man and government, and man and machine. It shows the events that shaped our collective
understanding of these ideas, how they altered our course, and how they still challenge
us today, because they are forever debated.

Its top-tier interface is built for the curious: readers move seamlessly between events
and stories. Top-tier analytic writing gives the reader the so-what in hard facts, and
the option to go deeper into the events and turning points that interest them.

## Prototype 1 is inspiration, never the standard

Prototype 1 (`site/`, and the scripts in `pipeline/`) is old data and ideas to learn from.
The new atlas improves on it in every way: the writing, the design, the data model, the
maps and the speed. Nothing old ships as it is. Matching the old output is never a goal;
the old content scripts are retired once `content/` replaces them, and the map scripts are
kept only as a base to improve (seeded, licence-checked, carried past 2019, fast on a
phone).

## The parts, and the place each lives

| The statement says | Where it lives | Spec |
| --- | --- | --- |
| Events linked by cause and effect, short and long | Event pages; graded links; the timeline's chain mode; chronicles and stories | `event-pages.md`, `narrative-flow.md`, `timeline.md` |
| Placed on the globe, through time | The Political globe and the shared year cursor | `house-style.md` (The globe), `border-review.md` |
| The people whose impact shaped the modern world | Great people: a life ("Follow this life"), a card or a name, decided by graded links | `structure.md` (People), `narrative-flow.md` (People) |
| Know the board | The Explore globe: the present world, its resources, routes and chokepoints | `narrative-flow.md` (the feature) |
| The big questions, forever debated | Great themes, written in their own voice; built after V1.0. Thinkers and their works are in V1.0 as idea events | `structure.md` (Themes, Idea events), `story-method.md` (Themes) |
| Why it mattered, what it caused, how sure we can be | The Overview; the five grade words and the arrow note | `event-pages.md`, `house-style.md` (Links) |
| Seamless for the curious; go deeper by choice | One navigation bar, the preview card, the four layers of every page | `narrative-flow.md` (Getting around) |

## How it differs from Wikipedia

Wikipedia is the reference shelf, and every page links to it and to Britannica. The atlas
competes on what an encyclopedia is built to avoid:

- **The link is the unit.** Causes are graded arrows with an argued note and the best
  case against, where an encyclopedia lists causes in prose.
- **Judgment first.** The atlas says what mattered, who gained and who paid, and how
  sure it is. An encyclopedia stays neutral by rule.
- **Size is judged, by stated tests.** Every event is rated once as a knot, a fibre or a
  strand by its reach, depth and lasting effect; the link grades show what each chapter
  turns on (structure.md).
- **Layered reading.** Thirty seconds, three minutes, ten minutes, then the chain.
- **Meanwhile.** One year cursor shows what else was happening across the world, and an
  arrow says when two events are connected.
- **The board.** Geography and resources are shown as forces, on a live map of today.
- **The questions.** Themes follow the big ideas across civilisations and centuries.

## What follows for the build

- The links are the product. A page exists because it carries an arrow; an arrow is
  never added to justify a page.
- The atlas is designed to hold about 50,000 events. The real number grows from the
  chains we build, never from a target.

## The front door (agreed 2026-11-05)

1. **Open.** The reader lands on a plain earth with no year set. Eight chronicles or
   stories, drawn at random on every load, sit on the globe as pins where each begins,
   with a card for each: the title and the year range. On a phone the cards sit under the
   globe. The eight mix sizes, places and eras, for example: the rise of the Roman
   Republic (a story inside the chronicle of Rome, from its founding to its fall); the
   Spanish Empire; the rise and fall of the Inca; the Atomic Age (the science and the
   politics, from fission to fusion); the civil war in Yemen today.
2. **Pick one.** The globe turns to where the chronicle begins and moves to its first year.
   The political map for that year appears. The chronicle's opening turning point is
   marked, and so are the world's other turning points of the same years, each opening
   the preview card on tap. This is the "meanwhile" moment.
3. **Go in, or wander.** The reader follows the chronicle as a chain, opens any other
   marked event, or goes back to the cards.

The world turning points that light up in step 2 are the knots of the years in view
(structure.md, 2026-11-11). Their number follows the tests, never a target. The knots are
also the default timeline view when no chronicle is chosen.

The draw is random on every load and balanced, so one set never holds eight from one
region or one era.

Still to decide:
- How wide "the same years" is: the same year, the same decade, or set per chronicle.
- The design of the cards and the opening screen, in Phase 1.

## How big an event is (agreed 2026-11-11; replaces the proposal of 2026-11-05)

Every event gets one size, rated once by its impact on world history, with a written
reason, so the atlas can answer a reader who asks "why is this a knot?" The method in
brief goes on the About page. The full rules are in `docs/structure.md`.

- **Knot:** it passes three tests. Reach: it changed life for a large share of the people
  alive in its world at the time, counted in people, never in countries. Depth: it changed
  who ruled, how people worked, what they believed, or who lived and died. Lasting: the
  change held for generations.
- **Fibre:** it passes for one people or region, or only for a short time.
- **Strand:** an event that changed the course of things for part of a people: a city,
  an institution, an army, a movement.

Fame scores nothing: a famous event that changed little stays small, and a quiet one that
changed much grows. "How much of today it explains" is no part of the test; it lives in
an event page's Lasting impact and, later, on the theme pages.

What a chapter turns on is a separate judgment, carried by the link grades. An event whose
link in a chapter is graded Necessary or Sufficient, with its counterfactual sentence, is
part of that chapter's backbone, whatever its size. The backbone draws heavy on the thread
and can be filtered. The timeline's Pull button shows the same judgment: pull such an
event and the chain downstream greys out.

Two guard rails keep the sizes from leaning West: an audit of each region's share of the
knots against its share of the world's people at the time, never a quota; and chronicles
planned by the same measure. A gap that remains after research is true and stays.

## Depth grows toward the present

The atlas gets denser as it nears today: more events per century, more detail per event,
the most in the last hundred years. This follows the record (far more survives) and the
reader (more of today's world traces to recent events). The timeline's time scale widens
toward the present for the same reason.

One guard: the effects of a recent event are still unfolding, so its size is
provisional for 25 years and marked so in the data header. An ongoing war is a
story, never yet a knot, and every figure in it carries its source and date.

## A lead for themes and chronicles (2026-11-07)

Themes may take a scroll-driven essay form: the argument unfolds as the reader scrolls,
in the themes voice, with sourced images, the weight carried by the order of the facts.
Chronicles may try the same with the globe behind the text, dimmed so the words stay
readable, turning and changing its borders as the reader scrolls down the stories; on a
phone, the globe in the top third with the story scrolling up over it. A tap on the globe
leaves the chronicle for the Political globe at the year the reader has reached, centred on
the story's place, with the Return chip to come back to the same sentence. Both are prototyped on one page first (roadmap 8.8a) and kept
only if they hold the phone budget and Cade's judgment.

## Chronicles run long (Cade, 2026-11-07)

A chronicle is one long subject followed through time: a place or people, a system or
idea, an age or contest (structure.md, 2026-11-11). It is as long as its subject's story,
so the curious reader can keep travelling.
Germany's runs from Rome's frontier through the Franks and the Empire, the Reformation,
Austria and Prussia, unification, the Reich, the treaty, the collapse, the division and
reunification to today; each era is a story with its own main events, steps and detail.
"The German Question" (1517 to today) is the pilot's name for the later part of that
chronicle and becomes stories inside it in Phase 7. Every story page carries Previous
and Next, so a reader who finishes one is offered the next.

## Developing stories and who holds what (proposed 2026-11-05)

A conflict still under way is a **developing story**: a story like any other, belonging to
every chronicle it touches. Yemen's war today sits in the chronicle of Yemen (North and
South, unification in 1990, the 2011 uprising, the Houthi entry into Sanaa in 2014), in
the rivalry between Riyadh and Tehran, and in the story of the Red Sea and the Bab
el-Mandeb, where it meets the strait's page on the Explore globe.

On the Explore globe, a **control layer** shows the major armed groups of today and the
ground each holds (the Houthis, M23 in eastern Congo, the armed groups of Colombia, and
others), each labelled "Developing story" and linked to its chronicles. Rules:

- **Licence first.** Each conflict's map comes from a source whose licence allows it,
  checked by script; nothing is drawn by hand. Where no usable map exists, the conflict
  shows as a pin and its story, without an area.
- **Dated.** Every area carries its source and "as of" date. A map past its review date is
  flagged on screen or withdrawn.
- **Neutral.** Each group under its own name, with plain verbs ("holds", "controls"); each
  side's claim at equal length (house-style.md, Politics).
- **Current.** Every fact is checked against current sources when the story is written
  and again at each review date.

Developing stories can be written in any phase; the control layer ships with the Explore
globe (Phase 11).

## Size of the whole

About 50,000 events, from the first civilisations to today, across every size, built into
the chronicles, stories and their paragraphs. It may end up larger. The build is tested at
50,000 and planned to go past it; the real number grows from the chains, never from a
target. The writing is the slow part: every page goes through sources, four reviewers
and a recheck, so launch is a few hundred pages done to the full standard, and the
atlas grows from there for years. Chains are written biggest first: knots, then fibres, then strands.
