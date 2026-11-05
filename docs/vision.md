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

The world turning points that light up in step 2 are the top chain, "The world": a few
hundred events chosen on purpose. It is also the default timeline view when no chronicle
is chosen.

The draw is random on every load and balanced, so one set never holds eight from one
region or one era.

Still to decide:
- How wide "the same years" is: the same year, the same decade, or set per chronicle.
- The design of the cards and the opening screen, in Phase 1.

## How big an event is (proposed 2026-11-05, for Cade's approval)

Every event gets two judgments, each with one written reason, so the atlas can answer a
reader who asks "why is this a turning point?" The method in brief goes on the About page.

**1. World weight: does the world chain need it?** Three scores, 0 to 2 each, from the
house-style rules Prototype 1 already used:

| Score | Question | 0 | 1 | 2 |
| --- | --- | --- | --- | --- |
| Reach | How far did its effects spread, across regions and across kinds of life (power, money, faith, science)? | One place, one kind | Several places or kinds | Several regions and several kinds |
| Lasting | Could it be undone? | Undone within a generation | Partly undone | Never undone |
| Today | How much of today's world does it explain? | Little | Something still live | A border, institution or idea we live with |

A total of 5 or 6 makes a candidate for "The world", which also needs at least one arrow
into another region. Fame and death tolls score nothing: a famous event that changed
little stays small, and a quiet one that changed much grows.

**2. Size in a chain: what happens to this chain without it?** Asked again in every chain
the event belongs to.
- Turning point: the chain breaks without it. Its arrow inside the chain is graded
  Necessary or Sufficient, with the counterfactual sentence.
- The full story: a step on the path between two turning points.
- Every detail: one step off the path; it explains how or why for the deep reader.

The timeline's Pull button shows the second judgment to the reader: pull a turning point
and the chain downstream greys out.

## Depth grows toward the present

The atlas gets denser as it nears today: more events per century, more detail per event,
the most in the last hundred years. This follows the record (far more survives) and the
reader (more of today's world traces to recent events). The timeline's time scale widens
toward the present for the same reason.

One guard: the effects of a recent event are still unfolding, so its Lasting and Today
scores are provisional for 25 years and marked so in the data header. An ongoing war is a
story, never yet a world turning point, and every figure in it carries its source and date.

## Size of the whole

About 50,000 events, from the first civilisations to today, across every size, built into
the chronicles, stories and their paragraphs. It may end up larger. The build is tested at
50,000 and planned to go past it; the real number grows from the chains, never from a
target. Chains are written biggest first: world turning points, then each chronicle's
turning points, then the full story, then every detail.
