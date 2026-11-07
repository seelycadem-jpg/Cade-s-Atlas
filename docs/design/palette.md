# The palette: the red thread (Cade's choice, 2026-11-08)

One idea: the product is the link, so the link gets the only loud colour. A bone-white
ground, graphite inks, and one red used for the chain alone: the knots, the connectors,
the years, the Globe pill. Everything else is quiet. Links by kind sit in plum, teal,
slate and moss; the maps in soft neutrals; so the thread is the one red thing on the page.
The dark side is charcoal with the red warmed, built from the same set and never inverted.

The red is a shade darker than the Economist's, on Cade's instruction, which also lifts
its contrast on the bone ground from 4.5 to 5.4.

Chosen from eight candidates shown on the same slice of story page, light and dark:
`docs/design/palette-options.html` (A to D) and `docs/design/palette-options-2.html`
(E to H). The build takes its colours from this table and nowhere else.

## Light

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#F7F6F3` | the page ground, bone |
| `--surface` | `#FDFDFB` | cards, chips, the pill |
| `--surface2` | `#F0EFEB` | a second surface where two sit together |
| `--ink` | `#1A1A1A` | titles and body text (16.1 on bg) |
| `--ink2` | `#505050` | the patch, summaries, secondary text (7.5) |
| `--ink3` | `#7C7C7C` | labels, captions, the strand ring (3.9; never body text) |
| `--rule` | `#DCDAD5` | hairlines, guides, borders of surfaces |
| `--accent` | `#C81A12` | the chain only: knot marks, fibre dots, connectors, years, the pill (5.4 on bg) |
| `--on-accent` | `#FFFFFF` | text on the accent |
| `--k-person` | `#6B4A7A` | links to people, plum (6.7) |
| `--k-polity` | `#2A6A6A` | links to countries and governments, teal (5.8) |
| `--k-chron` | `#3F4F73` | links to chronicles and stories, slate (7.5) |
| `--k-feature` | `#6B6A2A` | links to places and features, moss (5.2) |
| `--sea` | `#F1F0EC` | the globe's sea |
| `--land` | `#E4E2DC` | the globe's land |
| `--coast` | `#A5A29A` | coastlines |
| `--grat` | `#D8D6D0` | graticule |
| `--border` | `rgba(70,70,70,.45)` | political borders, neutral so the red stays the chain's |
| `--here` | `rgba(200,26,18,.14)` | the tint on the event's own country |
| owner fills | `#DFE3E8 #E8DDD2 #DDE4D8 #ECE5CC #E2DCE8 #E6DDD5` | the six fills for the before-and-after maps, quiet on purpose |

## Dark

| Token | Value | Use |
| --- | --- | --- |
| `--bg` | `#161616` | charcoal |
| `--surface` | `#1F1F1F` | |
| `--surface2` | `#262626` | |
| `--ink` | `#ECECEC` | (15.3 on bg) |
| `--ink2` | `#B4B4B4` | (8.7) |
| `--ink3` | `#828282` | (4.7) |
| `--rule` | `#353535` | |
| `--accent` | `#FF6B5C` | the red, warmed for a dark ground (6.5) |
| `--on-accent` | `#161616` | |
| `--k-person` | `#C9A6DC` | (8.6) |
| `--k-polity` | `#7FCACA` | (9.7) |
| `--k-chron` | `#A9B9E6` | (9.3) |
| `--k-feature` | `#C8C77A` | (10.3) |
| `--sea` | `#161616` | |
| `--land` | `#262626` | |
| `--coast` | `#5A5A5A` | |
| `--grat` | `#2A2A2A` | |
| `--border` | `rgba(190,190,190,.45)` | |
| `--here` | `rgba(255,107,92,.2)` | |
| owner fills | `#33404C #4C3F36 #3B4A3B #4D4631 #44405A #4D433B` | |

## Rules

- One accent, and it belongs to the chain. Nothing decorative is red: no headings, no
  buttons that are not about the chain, no rules.
- The four link colours never share the accent's hue, so a link is never mistaken for a
  knot and a knot never for a link.
- Grades are told by line style, never by colour alone: solid for Necessary and
  Sufficient, dashed for Contributing, dotted for Contested, grey with a cross-stroke for
  Coincident.
- The three marks sit in the accent (diamond, filled dot) and in `--ink3` (open ring).
- The dark side is built from this table, shifted, never inverted; every text token is
  checked against the same floors: 4.5 for text, 3 for marks and lines.
- Every colour has a value in both modes; no colour is defined in one mode only.
