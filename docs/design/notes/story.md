# Story page chat: notes

The page: Weimar Germany, 1919 to 1933, story 8 of the chronicle Germany.
File: `docs/design/mocks/story-v3.html` (story-v2.html is untouched).
This file holds what Cade decided, what is on trial and the questions for the master chat. The
standards docs and `docs/state.md` are the master chat's.

## Status

First pass built 2026-11-16 and published for Cade's phone. Cade has not read it yet, so
nothing below is decided by him. Every item is "on trial" until he says otherwise.

## How the file is made

- The whole stylesheet of `event-v12.html` (its first `<style>` block) is in the page unchanged.
  A second `<style>` block, marked "The story page only", holds everything the story adds.
- The script copies these parts of the event mock by line range, unchanged: the globe, the
  docking title, the globe view, the cartouche, the tab row's scroll logic, the sheets, the
  haptic tick, Cite this page.
- Every word is in the HTML at load: the chapters, every event row and its line, the six link
  notes (a hidden block, `#notes`), the 26 Meanwhile cards. Sheets copy from the page; nothing
  is fetched. The spine's labels are built from the chapter headings already in the page.
- The page loads one data file, `atlas-data.js`, for the globe's land and the 1919 borders.

## Carried from the event mock, unchanged

The globe strip and hint; the ladder with the page's own level last (Chronicle, Story); the
title; the date line with the red timeline and globe signs; two step buttons that say what
they step through ("Previous story in Germany", "Next story in Germany"); the docked header
in three lines ("‹ Germany · ‹ Before · After ›"); Back and search; the tab row and its
cartouche; sheets in the gilt cartouche; the Key as a folding row with the plus sign;
Meanwhile (heading, shuffle, six cards in two columns); Where next; the exits and Cite this
page; type, links, gilt, the 68px section gap; no bottom bar; no floating pills.

## Kept from story-v2

The briefing text; the five chapters and their paragraphs; "Read the chapter ›" at the end of
each paragraph and the title as a link to the chapter page; the chapter spine under the tabs
(red line filling to the chapter in view, a soft box behind it, sliding with arrows when the
chapters do not fit, fading away as the last chapter ends); the chapter in view at full size
and the rest smaller and lighter; the "1 of 5" count on the Chapters tab.

## Brought up to the structure of 2026-11-11

- Events sit in one flat list per chapter, in date order. No fibre sits under a knot and no
  strand under a fibre. One row shape for every event; the mark alone tells the size.
- Every mark carries the generated tooltip text of structure.md (title and label).
- The Treaty's knot is the Treaty of Versailles, 28 June 1919. The briefing's "Paris
  settlement" now reads "Treaty of Versailles" and "the treaty".
- A chapter may hold no knot: The Ruhr and the Mark holds four fibres and four strands.
  The Depression holds one knot and four fibres.
- An event the event mock also shows carries the same size here (hyperinflation and the
  Depression in Germany are fibres, as there).
- Two rows of story-v2 are dropped: "Unemployment Passes Six Million" (a figure, not an
  event) and "Hindenburg Swears in Hitler's First Cabinet" (the same happening as the knot).
  "Germany Signs the Treaty in the Hall of Mirrors" is dropped for the same reason.
- Four grades only. No row graded Sufficient is shown. The Necessary rows draw heavier: a
  3.4px solid line against 1.4px, the sentence in a heavier weight.
- Lines come from the link table alone. Six rows join this story's events. Where the table
  holds no row into a chapter the page says "No graded link into this chapter is recorded
  yet" and draws a faint dotted thread.

## On trial (story page only)

1. **How a chapter shows its events.** Three ways, switched with the Mock button
   ("Events: ..."): (a) knots and fibres listed, strands behind one plus row, the default,
   matching the chain's opening filter; (b) everything folded behind one plus row with the
   counts by mark; (c) everything listed.
2. **An event row**: the Meanwhile dateline (mark and date in small sans, the name in the
   title face under it). A tap opens a preview in the shared sheet: mark, name, date, chapter,
   one line, "Open the event".
3. **Links between chapters.** Before each chapter from the second on, a block "What led
   into Chapter N" lists every table row that runs from an earlier chapter into this one:
   the graded line, the generated plain sentence in italics, the grade and confidence, and
   which chapter it comes from. A tap opens the note (claim, challenge, verdict) in the
   sheet. A thread down the block's left edge takes the style of the strongest row from the
   chapter just before. A row between two events of one chapter sits under that chapter's
   list as "A link inside this chapter".
4. **The spine's ticks are plain strokes, never diamonds.** A chapter has no size, and the
   diamond is the knot's mark. The year sits in small grey sans, as on a Meanwhile card.
5. **The spine with the tab row.** It rides directly under the tabs, on the layer below
   them, with a hairline under it in place of story-v2's soft fade (the event mock's trial
   of a hairline under the docked tabs).
6. **The globe for fourteen years.** The strip opens on Berlin with Germany lit in the
   borders of 1919; the hint reads "Globe 1919 to 1933 · pull down to open". In the globe
   view a stepper walks the chapters ("The whole story", then "Chapter 1 of 5 · The Treaty"
   and so on): the year at the top changes and the globe turns to the chapter's knot, with
   a pin for each of its events that has a place in the mock data.
7. **The Story row of the ladder** reads "8 of 12 in this chronicle · 5 chapters, 26
   events"; the second part is a link that opens the event page's events sheet at the
   story's scope (every chapter, its events in order).
8. **The bottom line sits above the tabs** as the opening paragraph (the event page's
   place for it); the tab "Briefing" holds the three paragraphs that follow.
9. **The Key sits at the foot of the chapters**, with a fourth grade line for Coincident,
   since the page lists a Coincident row.

## Proposals for the master chat (shared parts; not changed in this page)

- None changed. One addition sits beside a shared part: the count on the Chapters tab
  (decided in palette.md, 2026-11-08), set here in the small sans at 11.5px to match the
  two-voice rule; story-v2 set it in the title face.

## Questions for the master chat

1. **The story view line** ("Reading within a story · Clear story view"): page-system.md
   says a story page needs your ruling. This page shows none.
2. **A story in several chronicles.** Weimar sits in one chronicle in the mock, so the
   Chronicle row carries no "Also in N more chronicles". Should it use the stories sheet's
   pattern when a story has two parents?
3. **The italic one-line judgment under the date** (ui-rules rule 20; story-v2 had "The
   republic that signed the peace, paid for it, and fell when the Depression came.") is
   absent, because the event hero carries none. Keep it off every page?
4. **Where the story came from and where it led.** The table holds The Great War →
   Versailles (graded Sufficient, awaiting your ruling) and Hitler Takes Power → The Second
   World War Begins (Necessary). Should the step buttons, or a line beside them, carry the
   graded link between one story and the next?
5. **The notes' verdicts** come from the table as they stand and still rank causes; one
   says "sufficient for the final phase". They wait for the rewrite of the links.
6. **Sizes across the mocks.** I followed the event mock where it shows an event. The
   chapter chat's list for The Treaty may differ from mine; the two should be reconciled.
7. **Links to the other mocks.** The Treaty of Versailles opens the event mock. Germany
   (chronicle) and The Treaty (chapter) have no published mock yet and show a stand-in
   line. The two addresses go into `CHRON_URL` and the first chapter's link when those
   chats publish. The Ruhr and the Mark opens the earlier chapter-v1 mock.
8. **`docs/design/mocks/README.md`** has no row for story-v3.html; I did not edit it.
9. **Tappable figures and a Sources list** are event-page items; this page has neither.
   Does a story page need them for its own figures (2.6 percent, six million)?

## Placeholders in the mock

"8 of 12", "The Great War", "Nazi Germany"; every size; the Meanwhile pool (the 26 other
events the old data holds for 1919 to 1933) and its places; the person preview for Hitler
(story-v2's text); the borders of 1919 used for every chapter; the two exits (unverified);
the page address in Cite this page; the quiz button; every "Would open ..." line.

## Checked before the first link went to Cade

Phone widths 320, 375 and 390, light and dark, in a test browser: no script errors, no
sideways scroll; the hero, the docked header, the tabs and count, the spine (fixed row at
375, sliding row at 320), each chapter, the three event modes, a link note, an event
preview, the events sheet, Cite this page, the Key, Meanwhile and its shuffle, Where next,
and the globe view's chapter steps. Not checked on a real phone: the pull-down gesture and
the smoothness of the chapter emphasis.
