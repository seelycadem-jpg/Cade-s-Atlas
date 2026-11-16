# Chapter page chat: notes

The chapter page mock, rebuilt in the event page's design. Page: The Treaty, chapter 1 of Weimar Germany.

- File: `docs/design/mocks/chapter-v2.html` (it loads `atlas-data.js` for the globe; nothing else).
- Published: https://claude.ai/artifact/W6637xXgK6LYXiTkun4Qm7 (private to Cade's account).
- First pass: 2026-11-17. Cade has not read it yet. Nothing below is decided.

## What Cade decided

Nothing yet.

## How the page is built

The stylesheet and the shared script are copied from `event-v12.html` by line range, unchanged: the hero and
its ladder, the docking title, the globe view, the tab row, sheets in the gilt cartouche, the docked card,
the note (claim, challenge, verdict), Meanwhile, Where next, the plus sign, type, links, gilt. The chapter's
own styles and script sit after a marked line in each. The thread reuses the chain web's classes, so a card
and a line are the same component here as in the sideways web.

Page order: hero; one step button (Next chapter); the bottom line; tabs; The Briefing; The Thread;
Meanwhile; Where next.

Every word is in the HTML at load: the ten cards, each event's brief, all thirteen notes. The script draws
the lines, sets the kind signs and runs the filters.

## On trial (built, for Cade to judge)

1. **The thread is a column of cards in date order.** Two events next to each other are joined straight down
   the gap. Any other pair is joined round the side: the line leaves the cause's edge, runs down a gutter and
   comes in at the effect's edge. The two gutters share the lines; a longer line takes a lane further out.
2. **Same cards as the web**, one size for every event, the mark alone telling the size. Two changes of
   content: the top line carries the full date (most of the chapter falls in one year), and the title is set
   at 17px because the card is as wide as the column.
3. **Same lines as the web**: solid for Necessary, dashed for Contributing, dotted for Contested; a port
   where a line leaves and a barbed head where it lands; the web's own weights (backbone 2.3, others 1.35,
   scaled by confidence). No grade word on a line.
4. **Backbone** is a fourth cell in the control strip, beside Knots, Fibres and Strands, with its count. On,
   it keeps the links graded Necessary and the events they join; a line under the strip says so and offers
   "Show all".
5. **Filters remove and the thread closes up**, as in the web. An event the filters leave out that a path
   runs through stays, faded. The lines fade, the cards glide, the lines return.
6. **All three sizes are on when the page opens.** The web opens with strands off. A chapter page is where
   every event of the chapter is listed, so the strands show.
7. **A tap on a card** opens the event mock's docked card: size, date, place in the chapter, the brief,
   Caused by and Led to rows, Open the page. A tap on a line opens the note.
8. **Where it came from and where it led** are rows above and below the cards (the sheets' line rows), one
   per link that crosses the chapter's edge. They are not cards on the thread.
9. **The step button repeats at the end of the thread**, so a reader who finishes it is offered the next
   chapter there.
10. **The Chapter row** of the ladder reads "1 of 5 in this story · 10 events". The count opens the events
    sheet.
11. **Section heading "The Briefing".** The event page says "Overview".
12. **No picture.** The repo holds one licensed picture and it belongs to the event page.

## Questions for Cade

1. Is the column with side lines the right thread, or should it be closer to the sideways web?
2. Should a line show its plain sentence on the thread, or only on a tap?
3. Should the note open in place between the two cards, or in the sheet as on the event page?
4. Filters: remove, as built, or fade in place?
5. Should "where it came from" and "where it led" be cards on the thread?
6. Four treaty cards read "France", where each was signed. Should a treaty card name the country it bound?
7. What place does a chapter's date line name? The mock says Paris, where the conference sat.

## For the master chat

1. **The event mock's events sheet does not match this thread, and cannot.** `event-v12.html` lists The
   Treaty as three rows: The Armistice (a row with no event), The Treaty of Versailles, German
   Hyperinflation, and says "2 of 3" and chapter "1 of 3". By structure.md the hyperinflation is chapter 2
   and the story has five chapters. This thread lists ten events (below). For the two pages to agree, the
   event chat changes its sheet: Versailles is 3 of 10, previous The May Fourth Movement, next The Treaty of
   Saint-Germain, chapter 1 of 5.
2. **The ten events, in date order**, all from the repo (event-pages.md, structure.md, site/data.json,
   event-v11.html): The Racial-Equality Vote, 11 April 1919 (strand); The May Fourth Movement, 4 May 1919;
   The Treaty of Versailles, 28 June 1919 (knot); The Treaty of Saint-Germain, 10 September 1919; The US
   Senate Rejects the Treaty, November 1919; The Treaty of Neuilly, 27 November 1919 (strand); The League of
   Nations Founded, January 1920; The Treaty of Trianon, 4 June 1920; The Treaty of Sèvres, 10 August 1920;
   The Treaty of Lausanne, 24 July 1923. Sizes are placeholders. The repo gives the Senate's vote a month and
   no day, so its place before Neuilly is by month only.
3. **One real link runs backward in time.** The pilot's link is The Treaty of Versailles to The May Fourth
   Movement. The march was on 4 May 1919 and the treaty is now dated to its signing on 28 June. The cause
   the note names is the Shandong award, which the conference made before the signing. With Versailles as a
   one-day event, the link needs a different cause event, or the treaty needs a span. The mock draws the link
   as the table holds it, pointing up the page.
4. **The story view line is left out.** page-system.md says it carries to chapter pages. A chapter belongs to
   one story, so there is no story view to clear and no "Also in N more stories". Say if it should show.
5. **The Great War to Versailles** was graded Sufficient in the pilot. The mock draws it as Necessary and
   labels it a placeholder, as the event mock draws it solid.
6. **The story link** points at the story-v2 artifact. It needs the story-v3 address once that page is
   published. The link to the event mock is its present address.
7. **Exits on a chapter page.** CLAUDE.md requires them on event and person pages. The mock keeps a pair
   (the Paris Peace Conference pages, standard addresses, unverified). Rule on whether a chapter carries them.
8. **Seen in the shared docked card, not changed:** its close button sits inside the scrolling text, so it
   scrolls out of reach when a card has many Caused by and Led to rows. The event mock caps those rows at
   three; a chapter's knot can have more.
9. **Proposal, not made:** the thread's control strip uses the web's size cells. "Backbone" here is a cell;
   on the event page it is a switch inside the Filter panel. One of the two should become the rule.

## Placeholders in the mock

- Every grade and every pairing on a line inside the chapter, except Versailles to May Fourth.
- The notes on placeholder lines say they are placeholders. The five real notes are the pilot's text.
- Sizes; "8 of 12"; "1 of 5"; "Also in" lines; the Meanwhile pool (seven events of 1919 to 1923 from
  site/data.json); the briefing (mock text from the worked example); the two exits; the quiz button.

## Checked before the first link (2026-11-17)

Headless Chromium at 375px wide, light and dark: no script errors; no sideways scroll at 375 or 320; the
hero, docked header and tabs; a card tap and the docked card; a line tap and the note; Backbone on and off;
Fibres off (a faded card stays where a path runs through it); the events sheet in both scopes; Meanwhile;
Where next. Not checked on a real phone.
