# The palette: the red thread on espresso (Cade's choices, 2026-11-08)

One idea: the product is the link, so the link gets the only loud colour. A warm paper
ground, warm-black text with espresso titles, and one red used for the chain alone: the knots, the
connectors, the years, the Globe pill. Everything else is quiet. Links in text are ink
with a thin red underline and turn red on hover or tap; the maps sit in soft warm neutrals;
so the thread is the one red thing on the page. One quiet decoration, gilt, marks the
section headings and nothing else. The dark side is a deep espresso ground with cream inks and the red warmed, built
from the same set and never inverted.

Espresso is Cade's colour (2026-11-08). In light mode it is the title colour: page titles,
section headings, chapter and event titles, where large type shows the brown. Body text stays
a warm black, because espresso at reading size looked like faded black. In dark mode
espresso is the ground, with cream text and titles.

The red is a shade darker than the Economist's, on Cade's instruction, which also lifts
its contrast on the paper ground past the 4.5 floor (5.2).

Chosen from eight candidates shown on the same slice of story page, light and dark:
`docs/design/palette-options.html` (A to D) and `docs/design/palette-options-2.html`
(E to H). The build takes its colours from this table and nowhere else.

## Light

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#F6F2EC` | the page ground, warm paper |
| `--surface` | `#FCFAF6` | cards, chips, the pill |
| `--surface2` | `#EFE9E1` | a second surface where two sit together |
| `--ink` | `#1C1916` | warm black: body text (15.7 on bg) |
| `--title` | `#3B2217` | espresso: titles, headings, chapter and event titles (13.2) |
| `--lede` | `#5A3220` | a lighter espresso for the briefing's opening paragraph, set in the title face a size up, so the brown shows at reading size (9.8). Alternatives in `docs/design/opener-options.html` |
| `--ink2` | `#4D4843` | the patch, summaries, secondary text (8.1) |
| `--ink3` | `#7B746D` | labels, captions, the strand ring (4.1; never body text) |
| `--rule` | `#DCD2C7` | hairlines, guides, borders of surfaces |
| `--accent` | `#C81A12` | the chain only: knot marks, fibre dots, connectors, years, the pill (5.2 on bg) |
| `--on-accent` | `#FFFFFF` | text on the accent |
| `--gilt` | `#B08A3E` | a fountain-pen stroke under section headings (150 by 3 px: a rounded drop of ink that thins to a point and fades); a faint 1px line under each section tab, and a flourish that draws itself under the selected tab; the divider diamond. Never text |
| `--sea` | `#F0EBE3` | the globe's sea |
| `--land` | `#E3DBD0` | the globe's land |
| `--coast` | `#A79A8D` | coastlines |
| `--grat` | `#D9D0C5` | graticule |
| `--border` | `rgba(64,44,34,.42)` | political borders, in brown so the red stays the chain's |
| `--here` | `rgba(200,26,18,.14)` | the tint on the event's own country |
| owner fills | `#DFE3E8 #E8DDD2 #DDE4D8 #ECE5CC #E2DCE8 #E6DDD5` | the six fills for the before-and-after maps, quiet on purpose |

## Dark

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#1C130F` | espresso |
| `--surface` | `#261A15` | |
| `--surface2` | `#2E211B` | |
| `--ink` | `#F2E9E0` | cream (15.2 on bg) |
| `--title` | `#F2E9E0` | cream, the same as the text |
| `--lede` | `#E8C9A8` | warm sand for the opener (11.6) |
| `--ink2` | `#C4B4A7` | (9.1) |
| `--ink3` | `#948174` | (4.9) |
| `--rule` | `#3E2E26` | |
| `--accent` | `#FF6B5C` | the red, warmed for a dark ground (6.5) |
| `--on-accent` | `#1C130F` | |
| `--gilt` | `#C9A45C` | |
| `--sea` | `#1C130F` | |
| `--land` | `#2C201A` | |
| `--coast` | `#64524A` | |
| `--grat` | `#2E231D` | |
| `--border` | `rgba(214,196,182,.4)` | |
| `--here` | `rgba(255,107,92,.2)` | |
| owner fills | `#33404C #4C3F36 #3B4A3B #4D4631 #44405A #4D433B` | |

## Rules

- One accent, and it belongs to the chain. Nothing decorative is red: no headings, no
  buttons that are not about the chain, no rules.
- One link style (Cade, 2026-11-08): ink text with a 1px red underline, red on hover and
  focus. Links are no longer coloured by kind; the preview card names the kind. This
  retired the four link pigments (plum, teal, slate, moss).
- Gilt is a line, never text (Cade, 2026-11-08): the pen stroke under section headings,
  the faint line under each tab, the flourish that draws on under the selected tab, and the
  divider diamond. It stays off small labels so it never becomes clutter. The flourish draws
  in 0.7 s and appears without motion for readers who ask for reduced motion.
- Grades are told by line style, never by colour alone: solid for Necessary and
  Sufficient, dashed for Contributing, dotted for Contested, grey with a cross-stroke for
  Coincident.
- The three marks sit in the accent (diamond, filled dot) and in `--ink3` (open ring).
- The dark side is built from this table, shifted, never inverted; every text token is
  checked against the same floors: 4.5 for text, 3 for marks and lines.
- Every colour has a value in both modes; no colour is defined in one mode only.
