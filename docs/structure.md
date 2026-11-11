# The structure: four levels and three sizes of event (agreed 2026-11-11)

The one place the hierarchy lives. Where an older doc says otherwise (story-method.md,
narrative-flow.md, house-style.md), this file wins. It replaces the "six levels" version
of 2026-11-08. The chart `docs/design/levels-chart.html` still shows the old version and
is redrawn next.

## The map

```
CHRONICLE   one long subject followed through time
   │        Germany · The Jewish People · Capitalism · The Second World War
   │        page = a portrait, then its stories by start date (a two-minute read)
   │
   ├─ STORY   one argument: why this part went the way it did
   │     Germany: Weimar Germany 1919–1933 · Nazi Germany 1933–1945 · ...
   │     page = the argument, then its chapters
   │
   │     └─ CHAPTER   a stretch of the story in which one thing changes
   │          Weimar: The Treaty · The Ruhr and the Mark · The Golden Years
   │                  The Depression · The Seizure of Power
   │          page = a longer briefing, then the thread of its events
   │
   │          └─ EVENTS   joined to each other by graded links
   │               ◆ knot    The Paris Peace Settlement, 1919 to 1923
   │               ● fibre   the Senate rejects the treaty
   │               ○ strand  the racial-equality vote, 11 April 1919
```

Four levels: chronicle, story, chapter, event. Knot, fibre and strand are the three sizes
of an event. The events of a chapter are a flat set joined by links; no event sits
"inside" another.

## The levels

| Level | What it is | Its page holds |
| --- | --- | --- |
| Chronicle | One long subject followed through time by its chain of events. It needs several stories, each with its own argument | A portrait, then its stories by start date: the two-minute read |
| Story | A part of a chronicle with one argument: why it went as it did | The argument, then its chapters, each a paragraph (its patch) that opens to the chapter page; Previous and Next story |
| Chapter | A stretch of a story in which one thing changes. It holds every event linked into that change | A longer briefing (how the period moved), the thread of its events in date order with the graded link between each pair, where it came from and where it led, Meanwhile, Previous and Next chapter |
| Event | Something that happened, with a date and a place | The event page (docs/event-pages.md), at a length set by the event |

### Chronicle

Three kinds, one definition:

- A place or people: Germany, the Ottomans, The Jewish People.
- A system or idea: mercantilism, capitalism, communism.
- An age or contest: The Cold War, the atomic age, The Second World War.

Three tests:

1. **It needs several stories.** A subject with one argument is a story. The Second World
   War lasts six years and is a chronicle, because the war in Europe, the Eastern Front and
   the Pacific each carry their own argument. The Space Race is decided when it is outlined.
2. **It is a chain of dated events with a start.** Capitalism passes. "Power" fails and
   belongs to the themes layer.
3. **It makes an argument no existing chronicle makes.** Its portrait and stories are new
   writing; its events mostly have pages already. A chronicle that would only list another
   chronicle's stories is never built.

A chronicle is named for its subject, never for where it ends. "The Jewish People" is a
chronicle; "The Jewish People to the Creation of Israel" presumes the outcome. The link
from one story to the next is a graded link like any other.

### Story

- A story has one argument and its own page.
- A story can belong to more than one chronicle. The Holocaust belongs to The Jewish People
  and to The Second World War: one page, two parents, each listing it.
- Stories in one chronicle are ordered by start date and may overlap in time.
- A page has one level. The Second World War (chronicle) and Nazi Germany 1933–1945
  (story) are two pages with two arguments, sharing events.

### Chapter

- A chapter is a stretch of its story in which one thing changes: in The Ruhr and the
  Mark, the currency collapses.
- It holds as many knots as there are, including none. A chapter whose events are all
  fibres is a full chapter.
- A chapter that covers two changes is two chapters.
- A chapter belongs to one story. Its events may sit in many chapters.
- **Membership comes from links, never from dates alone.** An event sits in a chapter when
  a graded link joins it to that chapter's change. The Senate's rejection of the treaty
  happened in Washington and sits in The Treaty because the arrow runs there. An unlinked
  event of the same years belongs in Meanwhile.
- The chapter's paragraph on the story page is its patch.

### Event

- One event, one page, whatever chapters it sits in.
- An event with no graded link into any chapter is a line on another page or a label on
  the map, never a page.
- A figure, a date or a quotation on its own is a line inside a page, never an event.

## The three sizes (Cade, 2026-11-11)

Every event is rated once, by its impact on world history. The size is fixed: the same
word and the same mark on every page, whatever path the reader took.

| Size | Mark | Test |
| --- | --- | --- |
| Knot | diamond | Passes reach, depth and lasting, all three |
| Fibre | filled dot | Passes for one people or region only, or for a short time |
| Strand | open ring | Explains how or why a bigger event went as it did |

The three tests of a knot:

1. **Reach.** It changed life for a large share of the people alive in its world at the
   time. Reach is counted in people, never in countries. "Its world" is the connected
   world of its day: before 1492 the Americas are a world of their own, and so is Oceania
   before sustained contact. An event that reshaped the American world is a knot.
2. **Depth.** It changed who ruled, how people worked, what they believed, or who lived
   and who died.
3. **Lasting.** The change held for generations.

Size and links do separate jobs. The size says how much the event moved world history.
The links say what caused what and which chapters the event sits in. The Paris settlement
is a knot in Weimar Germany's chapter The Treaty and a knot in every Ottoman and Arab
chapter that holds it.

Length follows the event and its sources, never the size. A knot that is one day is short.

## Two guard rails against a Western lean

1. **The audit, never a quota.** For each era, each region's share of the knots is
   compared with its share of the world's people at the time. A wide gap marks a place to
   research. An event is never promoted to close a gap; that would invent importance.
2. **Chronicles are planned by the same measure.** The order in which chronicles are
   written is checked against the same shares, because knots follow the chronicles that
   exist.

From about 1750 to 1950 many knots start in Europe, because European empires reached most
of the world. In those years the events where the impact landed get their full size:
Plassey, the Opium War, the Haitian Revolution, the rebellion of 1857 in India.

The 781 events in `site/data.json` and their tiers are placeholders. Every event is rated
afresh by these tests in the rebuild.

## One event, many chapters (Cade, 2026-11-08)

- The event page says what the event was and what it caused, across every chain. It lists
  every chapter it sits in, and each opens that chapter at the event.
- The chapter page says what the event meant in that chain: why it sits there, what came
  before it and what it led to there. That framing lives on the chapter, never copied into
  the event page.
- On a chapter's thread, an event that sits in other chapters shows them as "Also in".
- A reader who arrives from a chapter sees that chapter in the event page's breadcrumb and
  Back, so the context they came through is the one offered first.
- Every page opens with its path, each step labelled with its level: Germany (chronicle) ›
  Weimar Germany (story 8 of 12) › The Treaty (chapter 1) › the event with its mark. The
  path is the one the reader came by; with no route, the page's home path. Where a page
  sits in more than one place, "Also in N more" ends the path and opens every path, the
  reader's own marked. Choosing another path makes the page follow it: its Next and its
  chain. The size stays the same on every path.

## What a reader can do

Open Germany and read it in two minutes. Open Weimar and read why it fell. Open The Treaty
and read how the year moved. Open the settlement. Four taps from the long view to one
event, and Back at every step. From the event, the links lead on to the events that caused
it and the events it caused. A chapter's thread shows its events with their marks, and the
depth control shows knots, then fibres, then strands; a chapter with no knot opens at its
fibres. Every chain view carries the key: knot, an event that changed the course of its
world; fibre, an event that changed the course of one people or region; strand, an event
that explains how or why a bigger one went as it did.

## Open

- The levels chart is redrawn to four levels and three sizes.
- "A large share" in the reach test has no number yet; it is set when the first chronicles
  are rated.
- The pilot's "German Question" (1517 to today) becomes stories inside the Germany
  chronicle in Phase 7.
