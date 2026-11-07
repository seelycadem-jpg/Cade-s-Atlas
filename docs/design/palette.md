# The palette: the red thread on espresso (Cade's choices, 2026-11-08)

One idea: the product is the link, so the link gets the only loud colour. A warm paper
ground, espresso-brown inks, and one red used for the chain alone: the knots, the
connectors, the years, the Globe pill. Everything else is quiet. Links in text are ink
with a thin red underline and turn red on hover or tap; the maps sit in soft warm neutrals;
so the thread is the one red thing on the page. One quiet decoration, gilt, marks the
section headings and nothing else. The dark side is a deep espresso ground with cream inks and the red warmed, built
from the same set and never inverted.

Espresso replaced graphite and charcoal on Cade's instruction: brown stands wherever black
stood, in the light inks and the dark ground, so the page reads as ink on paper rather than
screen black.

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
| `--ink` | `#2B1C15` | espresso: titles and body text (14.7 on bg) |
| `--ink2` | `#5C4B42` | the patch, summaries, secondary text (7.4) |
| `--ink3` | `#857469` | labels, captions, the strand ring (4.0; never body text) |
| `--rule` | `#DCD2C7` | hairlines, guides, borders of surfaces |
| `--accent` | `#C81A12` | the chain only: knot marks, fibre dots, connectors, years, the pill (5.2 on bg) |
| `--on-accent` | `#FFFFFF` | text on the accent |
| `--gilt` | `#B08A3E` | the short rule under section headings and the divider diamond; never text |
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
- Gilt is a line, never text: the short rule under section headings and the divider
  diamond. It stays off small labels so it never becomes clutter.
- Grades are told by line style, never by colour alone: solid for Necessary and
  Sufficient, dashed for Contributing, dotted for Contested, grey with a cross-stroke for
  Coincident.
- The three marks sit in the accent (diamond, filled dot) and in `--ink3` (open ring).
- The dark side is built from this table, shifted, never inverted; every text token is
  checked against the same floors: 4.5 for text, 3 for marks and lines.
- Every colour has a value in both modes; no colour is defined in one mode only.
