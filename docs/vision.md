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

## The parts, and the place each lives

| The statement says | Where it lives | Spec |
| --- | --- | --- |
| Events linked by cause and effect, short and long | Event pages; graded links; the timeline's chain mode; chronicles and stories | `event-pages.md`, `narrative-flow.md`, `timeline.md` |
| Placed on the globe, through time | The Political globe and the shared year cursor | `house-style.md` (The globe), `border-review.md` |
| The people whose impact shaped the modern world | Great people: a life as a chain, impact as graded links | `narrative-flow.md` (People) |
| Know the board | The Explore globe: the present world, its resources, routes and chokepoints | `narrative-flow.md` (the feature) |
| The big questions, forever debated | Great themes, written in their own voice | `story-method.md` (Themes) |
| Why it mattered, what it caused, how sure we can be | The Overview; the five grade words and the arrow note | `event-pages.md`, `house-style.md` (Links) |
| Seamless for the curious; go deeper by choice | One navigation bar, the preview card, the four layers of every page | `narrative-flow.md` (Getting around) |

## How it differs from Wikipedia

Wikipedia is the reference shelf, and every page links to it and to Britannica. The atlas
competes on what an encyclopedia is built to avoid:

- **The link is the unit.** Causes are graded arrows with an argued note and the best
  case against, where an encyclopedia lists causes in prose.
- **Judgment first.** The atlas says what mattered, who gained and who paid, and how
  sure it is. An encyclopedia stays neutral by rule.
- **Size is chosen.** An editor decides what is a turning point, per story.
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

## Open questions

1. **A default size for the front door.** Size belongs to an event inside a chain. Proposal:
   a top chain, "The world", of a few hundred world turning points chosen on purpose, which
   is the default timeline view and the front door; every chronicle hangs off it.
2. **How the 50,000 are reached.** By opening events as chains of their own ("go deeper"),
   chronicle by chronicle: world turning points first, then each chronicle's turning
   points, then the full story, then every detail.
