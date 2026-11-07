# UI rules (approved by Cade 2026-11-07)

The promises every screen keeps. The mock-ups in step 1.3 follow them; the browser tests
check the ones that can be checked. Written from `docs/design/brief.md`, the navigation
rules in `docs/narrative-flow.md` (Getting around), `docs/timeline.md`, and the two design
skills. Where a rule here and an older doc differ, this file wins once approved.

## The three ideas behind every rule

- **The globe is home.** Every place is reached from it and returns to it.
- **The reader never loses their place.** Cards float over the page; Back lands on the
  exact sentence; the year travels with the reader.
- **One thing at a time.** Each screen has one obvious next action; everything else is
  one tap away.
- **Strategic, operational, tactical.** Cade's analogy for the three levels: the
  chronicle read in two minutes, its stories, then the events and their detail. Every
  screen lets the reader drop a level or climb one without losing the thread.

## Rules

1. **One obvious next action per screen.** The thing most readers want next is the
   biggest, clearest control on the screen. Everything else sits one tap away, behind
   More, in the bar, or in a card. No screen shows every control at once.

2. **One navigation bar, everywhere.** A strip along the bottom on a phone, a rail down
   the left on a laptop. It holds: Back, the six places (People, Globe, Events, Explore,
   Themes, Timeline) with the current one marked, the year, and search. Never more than
   that. The year is the shared cursor: tapping it opens the year card.

3. **One preview card, everywhere.** Every name, dot, marker, pin, card and bar opens the
   same preview, and so does every linked name inside a sentence (the `[[...]]` links in
   event, story and theme text): a picture where there is one, the title and date, the one line, and
   Open. On a phone one tap opens it; on a laptop, hover. The preview floats over the
   page; closing it changes nothing underneath.

4. **Only Open navigates.** A tap on a name shows the preview. Only the preview's Open (or
   Read more, Open country, Open on the map, Open the chronicle) leaves the page. The
   reader always knows which tap is a look and which tap is a move.

5. **Back returns to the exact place.** Same page, same scroll position, same year, same
   open card. Whenever a card's button leaves the page, a Return chip appears in the bar,
   named for where the reader came from, and takes them back to the same sentence.

6. **Cards and panels float, with their own edges.** Previews, year cards, filters and
   detail panels sit over the globe or the page as distinct surfaces: a visible edge, a
   small shadow, a scrim behind them on a phone. They never push the page around.

7. **The year travels with the reader.** Move the year on any page and every other
   place opens at that year. A chronicle scrolled to 1453 opens the globe at 1453. The
   year is in the address, so a link shares the moment.

8. **Three depth levels, the same words everywhere:** Turning points, The full story,
   Every detail. This is the strategic-to-tactical ladder: a reader at any level can see
   the level above (the breadcrumb, the parent chronicle) and the level below (the next
   depth word, the linked names) from where they stand. One control, in one place, on the globe, the timeline and every
   chronicle. No other depth control exists. (The event page's "Open the detail" button
   is renamed in step 1.6 so "detail" means one thing.)

9. **Filters dim, never remove.** Filtered-out events fade; they never vanish. Type and
   depth sit up front as one row of chips; region as lane chips; theme, chronicle,
   person, grade and country behind More. The same filter looks and works the same on
   every page.

10. **Phone first.** Every screen is designed at phone width first and widened for a
    laptop, never the reverse. No sideways scrolling. Tap targets at least 44 by 44
    pixels with 8 pixels between them. Body text at least 16 pixels. Text can be
    enlarged by the reader without breaking the layout.

11. **Readable over the globe.** Text over the globe sits on a surface that keeps
    contrast at 4.5:1 or better, light or dark. The globe behind a chronicle is dimmed
    so the words win.

12. **Motion answers the reader, and that is all.** The globe turns when the reader turns
    it or scrolls a chronicle. Cards open and close with a short transition (150 to
    300 ms) that shows what changed. Nothing animates on its own to decorate. Readers
    who ask their phone for reduced motion get none.

13. **Names stay plain.** Readers see turning points, the full story, every detail, the
    five grade words and the note. No internal word (knot, strand, fibre, tier) and no
    method talk outside the About page.

14. **Nothing hides behind a gesture.** Every action has a visible control. Long-press,
    swipe and shake never carry anything a tap cannot reach.

15. **Breadcrumb on every page.** Atlas > Ottomans > Rise > 1453, each part a link. The
    reader can always say where they are, what came before and what comes next.

16. **The same control behaves the same on every page.** A chip, a card, a toggle or a
    slider learned once works the same everywhere. Two pages by two sessions must read
    as one atlas.

17. **Speed is a rule, not a hope.** A page is usable on a mid-range phone within 3
    seconds on an ordinary connection. The build fails when a page breaks its size
    budget.

18. **Light and dark, both first-class.** The reader's system setting decides; every
    surface, text and map colour has a value in both, and the globe's borders read in
    both.

## Checked by the browser tests (from Phase 1 on)

Rules 2, 5, 10, 11, 15 and 17 are tested on every push: the bar is present at both sizes;
Back returns to the same scroll position; no horizontal overflow; tap-target sizes;
contrast of text over the globe; the breadcrumb; the size budget. The rest are checked by
reading, in the people test (1.13) and at `/code-review`.

## Open

- The wording that replaces "Open the detail" on event pages (step 1.6: Cade chooses
  from the mock).
- Whether the six places are six words or five words plus a globe icon on the narrowest
  phones (decided in the mock).
