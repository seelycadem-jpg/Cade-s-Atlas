# Chronicle page chat: notes

The chronicle page mock, Germany. File: `docs/design/mocks/chronicle-v1.html`.
Published for Cade's phone: https://claude.ai/artifact/EFkvFGtpqfLBp2WMSkYgjQ

Data beside it: `atlas-data.js` (shared, unchanged) and `chronicle-v1-meanwhile.js`, written by
`build-chronicle-meanwhile.py` from `site/data.json`. To republish from another chat, pass the link
above as the artifact to update and send both data files with the page.

## Status

First pass built 2026-11-16. Cade has not read it yet. Nothing below is decided.

## What Cade decided

Nothing yet.

## Carried from event-v12.html unchanged

- The whole style sheet of event-v12.html is copied in as it stands, so every shared rule is the same
  rule. The chronicle's own rules sit in one block after it, under a comment that marks the line.
- The script's shared parts are the event mock's own lines: the globe, the docking title and docked
  header, the pull into the globe view, the tabs and cartouche, the signs, the haptic tick, the gilt
  frame, the sheets, Cite this page, the theme switch.
- The hero: globe strip, hint, ladder, title, date line with its two red signs, two step buttons.
- Meanwhile: the same heading, shuffle sign and cards. Where next: the same block.
- No picture is shown, because the mock holds no licensed picture for Germany.

## New on the chronicle, all on trial

1. **The ladder is one row.** "Chronicle" is the page's own level and the only row. It carries
   "11 stories" as a link that opens the stories sheet, then "by start date" as plain text, the way
   the Event row carries its counts. No story view line and no "Also in".
2. **The step buttons are two ways in.** "Begin with the first story: Germania and Rome" and "Or
   start with the latest: Reunified Germany". Both move the page to that story. A chronicle has no
   chronicle before or after it, so the pair names where to start reading.
3. **The docked header's third line** reads "11 stories: choose one ›" and opens the stories sheet.
4. **The date line** reads "Antiquity to today · Central Europe" and carries no type sign.
5. **Tabs:** Portrait, Stories, Meanwhile. The Stories tab shows "8 of 11" while selected.
6. **Portrait:** the opening line above the tabs, then four short paragraphs under the heading.
7. **Stories:** one entry per story, in order of start year. Each has a small label line ("Story 8
   of 11", the years), the title as the link to the story, one paragraph, "Read the story" with a
   red arrow, and a "Chapters" fold on the one plus sign. Stories carry no size mark.
8. **The story spine** pins under the tabs while the reader is among the stories. Year, a tick on
   the axis, the name. A red line fills to the story in view and a soft box sits behind it. The row
   slides under the finger and keeps the story in view near the middle. A red arrow at each end
   steps one story and greys at the first and the last. Tapping a name goes to that story.
9. **The stories sheet:** all eleven in the gilt cartouche, the one in view ticked; choosing one
   moves the page to it.
10. **Meanwhile covers one story's years.** A row in the ladder's form says whose years ("During ·
    Reunified Germany · 11 of 11") with the ladder's stepper. It opens on the latest story. A story
    with no event in the data shows "The atlas holds no event for these years yet."
11. **The globe.** It opens on the plain earth with "Germany" lettered across the land and no pin.
    It takes a story's borders while that story is in view (1914 for The Great War, 1919 for Weimar
    Germany, the two years the mock holds). The hint carries no year.

## Differences from the story mock's chapter spine (rule 8), for the master chat

- The marks on the axis are plain ticks, because a story has no size and a diamond would claim one.
- The arrows sit at the ends of the row and step one story. Rule 8 puts them in their own row below
  and moves the row three. This saves about 30px of a sticky stack that is already 215px tall.
- The row scrolls under the finger like the Record's index row in the event mock.
- The stories do not shrink and fade as the reader leaves them. The story mock did this for chapters.

## Questions for Cade

1. Does the chronicle keep Meanwhile, and is "one story's years at a time" the right window?
2. Should the globe follow the story in view, or stay on the plain earth for the whole page?
3. Are two ways in ("first story", "latest story") the right pair of step buttons?
4. Is the spine worth its height on a phone, or is the count in the tab plus the sheet enough?
5. Should each story show its chapters on the chronicle page, or only on the story page?
6. Should the story being read stand at full strength and the others fade, as chapters did?
7. Does the page want a graphic: the eleven stories on one line of time?

## Questions for the master chat

1. The story view line and "Also in" are left off the chronicle. Confirm.
2. The published link for story-v3.html is needed. The Weimar links point to `story-v3.html` in the
   repo and to the current story artifact (https://claude.ai/artifact/AWaup7weY8H6EUwNDCXS37) when
   the page is opened anywhere else. If the story chat publishes to a new link, tell this chat.
3. The link from one story to the next is a graded link (structure.md). The link table holds none
   between stories, so the mock draws nothing between entries. Is a connector wanted once they exist?
4. Does a chronicle page carry the Wikipedia and Britannica exits? The mock leaves them out, since
   the rule names event and person pages and no address here is verified.
5. `docs/design/mocks/README.md` has no row for this mock yet. This chat did not edit it, so two
   chats never change the same file.
6. The mock's label for a story with no dated event is "Years to come". The date line says
   "Antiquity to today". Both need real values from the outline of the first two stories.

## Placeholders in the mock

- Story years: taken from events the old data holds (1517, 1648, 1815, 1871, 1914, 1918, then the
  plan's own 1919, 1933, 1945, 1990). The first two stories carry none; the old data starts in 1440.
- All page text is mock text, unchecked. It uses only names and dates the old data or the docs hold.
- Chapters: Weimar Germany's five are from structure.md. Every other fold says it is a placeholder.
- "Also in 1 more chronicle" on The Great War.
- Meanwhile: 748 events from `site/data.json`, less the 33 of the German pilot chain; old tiers as sizes.
- "Would open ..." slips, the quiz button, the Mock and Theme buttons.

## How it was checked (2026-11-16)

In a headless browser at 390px and 375px wide, light and dark: no console errors, no sideways
scroll, the title docks, the tabs select, the spine follows the story in view, the arrows and names
move the page, the Chapters fold opens, the Meanwhile stepper and the gap line work, the stories
sheet and Cite this page open. Not checked on a real phone: the pull into the globe view and the tick.
