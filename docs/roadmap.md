# The roadmap: every phase in small steps (drafted 2026-11-05)

The working list behind `docs/rebuild-plan.md`. Each step is small enough for one session
or less, names who does it, and says how we know it is done. Each phase ends with its
test; the next phase starts only when the test passes.

How sure each phase is:
- **Phases 0 to 2: firm.** We start on these now.
- **Phases 3 to 13: drafted.** Each is reviewed and corrected when we reach it, because the
  earlier phases will teach us things. Steps may be split, merged or added then.

Every step becomes a GitHub issue, grouped under one parent issue per phase. Where this
file and the "Meanwhile Atlas: Build Plan" doc disagree, the Build Plan doc wins and this
file is corrected.

Who: **C** = Cade, **AI** = Claude, **C+AI** = together. "Cade approves" means nothing
moves until he says yes.

---

## Phase 0: Foundation

Goal: the project builds and tests itself, and a blank site is live on the internet.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 0.1 | Approve the stack | C | Done 2026-11-05 |
| 0.2 | One settings file that tells every pipeline script where this project's folders are (`pipeline/` for code, `site/` for output, a git-ignored `work/` for scratch) | AI | Done 2026-11-05 |
| 0.3 | Safety check that moving the scripts broke nothing: run `build.sh` from another folder into a test copy | AI | Done 2026-11-05 with step 0.2 |
| 0.4 | ~~Drop the unused `polities.py` step~~ | AI | Not needed: the old content scripts are retired in Phase 2 |
| 0.5 | Install Node and Astro; create `app/` with one blank page | AI | Done 2026-11-05 |
| 0.6 | First test (Playwright): open the page at phone and laptop size, check the title, save screenshots | AI | Done 2026-11-05 |
| 0.7 | GitHub Actions: run the build and the test on every push | AI | Done 2026-11-05 |
| 0.8 | Create a Cloudflare account | C, AI guides | Done 2026-11-05 |
| 0.9 | Connect the repo to Cloudflare so each push to `main` goes live. Checked 2026-11-05 on Cloudflare's limits pages: Pages holds 20,000 files on the free plan and 100,000 on paid; Workers static hosting holds 20,000 free and 100,000 on Workers Paid (about $5 a month). Start free; move to Workers Paid before the site passes 20,000 files; past 100,000, serve pages from R2 through a Worker | C+AI | Done 2026-11-05: GitHub deploys to Cloudflare Workers on every merge to `main` (`.github/workflows/deploy.yml`, token in a GitHub secret); live at https://cade-s-atlas.seelycadem.workers.dev |
| 0.10 | Write the `/build` and `/ship` skills from what worked | AI | Done 2026-11-05 |
| 0.11 | Cade's first pull request: read it, merge it | C, AI guides | Done 2026-11-05 (#58, then #59 and #60 for hosting) |
| 0.12 | Update `docs/plan.md` to Phase 1 | AI | Done 2026-11-05 |

**Test:** `build.sh` runs clean, the test passes on push, the blank site opens on a phone. **Passed 2026-11-05.**

## Phase 1: Look and feel

Goal: decide how the atlas looks and works on a phone before building real screens.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 1.1 | List what worked and what didn't in Prototype 1, and 3 to 5 sites whose look you admire | C | Done 2026-11-05: `docs/design/brief.md` |
| 1.2 | Write the UI rules: one obvious next action per screen; one tap opens a preview, Open inside it navigates; the same control behaves the same on every page | AI, C approves | Done 2026-11-07: `docs/design/ui-rules.md` |
| 1.3 | Two or three design directions (type, colour, spacing), each as a mock event page on a phone | AI | Cade can tap through each |
| 1.4 | Pick a direction, or mix | C | Chosen |
| 1.5 | Mock the front door: plain earth, eight random chronicle pins and cards, the turn to a first year with its political map and the world's turning points of those years | AI, C approves | Tap-through mock |
| 1.6 | Mock the filters on a phone: type and depth chips up front, region chips, the rest behind More; filtered-out events fade | AI, C approves | Tap-through mock (the "detail" wording question is closed: the gate is dropped, 2026-11-07) |
| 1.7 | Mock the two globes as two pages sharing one map, one look, one set of gestures; show how quiet peoples' homelands should be | AI, C approves | Tap-through mock |
| 1.8 | Build the colour and type settings (light and dark) as one shared file | AI | Every page uses it |
| 1.9 | Build the navigation bar: bottom strip on a phone, left rail on a laptop; Back, the six places, the year, search | AI | Test: on every page, both sizes |
| 1.10 | Build the one shared preview card | AI | Test: tap opens it, close returns to the same spot |
| 1.11 | Build the breadcrumb and the Return chip | AI | Test: Back lands on the exact place left |
| 1.12 | Accessibility check: text size, contrast, tap-target size, keyboard, reduced motion | AI | Passes |
| 1.13 | People test: 3 to 5 people, a phone and a task; watch where they get stuck | C finds people; AI writes tasks and sums up | Every place two or more got stuck is fixed |

**Test:** Cade opens the mocks on his phone and says they are right, after the people test.

## Phase 2: The data model and the first slice

Goal: describe every kind of thing exactly, prove the design holds at full size, then take
one event all the way to live.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 2.1 | Approve the sizing method in `docs/vision.md` (three world-weight scores; the per-chain question) | C | Approved or changed |
| 2.2 | Decide whether launch covers only 1440 onward, or the ancient world too (the front-door examples include Rome and early Christianity) | C, AI advises | Decided; the plan updated |
| 2.3 | Schemas for the seven objects (event, link, person, polity, feature, layer, theme) plus chronicle, story and patch | AI | The build rejects a file with a missing field |
| 2.4 | Address and id rules; they never change after this | AI, C approves | In the schemas |
| 2.5 | `content/` with its folders, split by region | AI | Exists |
| 2.6 | Size test: 50,000 fake events and 150,000 fake links (marked fake, deleted after); measure build time, file count, phone load | AI | Build under 10 minutes; a timeline slice loads on a phone in under 3 seconds; the file count has a hosting route (step 0.9) |
| 2.6a | Licence check of every map and data source for a public site: Natural Earth, CShapes, Cliopatria (CC BY), historical-basemaps (GPL-3.0: what sharing derived data requires), Pantheon, OEC, Comtrade. Pulled forward from Phase 4 so a failed licence is known before the globe is designed | AI, C approves | A licence line per source; any problem raised |
| 2.7 | Act on the size test: change what failed | AI | The test passes |
| 2.8 | Starter files for the old 781 events: header fields filled where the old data holds them, text empty, status draft | AI, by script | 781 drafts; none visible to readers |
| 2.9 | The 36 graded links into the link table, built by the pipeline | AI, by script | Same 36 links with their notes |
| 2.10 | Preview mode: drafts visible on Cade's private preview, never on the live site | AI | Test: a draft never reaches the live build |
| 2.11 | Choose the first event to build end to end | C | Chosen |
| 2.12 | Write it through the full writing pipeline: sources read, draft, four reviewers who never saw the draft written, merge, recheck | AI | Status reviewed |
| 2.13 | Cade reads it | C | Approved, or notes sent back and fixed |
| 2.14 | The event page: takeaway strip from the data header, four layers, the detail control | AI | Renders on phone and laptop |
| 2.15 | Inline links open the preview card | AI | Test: every link resolves or is queued |
| 2.16 | Search (Pagefind, needs Cade's OK) | C approves, AI builds | Test: finds the page by name |
| 2.17 | `/page-check`: title, description, worded address, structured data, alt text, sitemap | AI | Fails the build on a miss |
| 2.18 | The first event goes live | AI | Opens on Cade's phone at its own address |
| 2.19 | People test on the live page | C+AI | Fixes made |

**Test:** the first event is live, passes every check, and Cade approves it on his phone.

## Phase 3: The year card and the timeline, first version

Goal: the shared year cursor and the timeline grid, built on the events that exist.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 3.1 | The pipeline writes the timeline in slices (by era, region and size), each within a size budget | AI | Test: every slice under budget |
| 3.2 | One shared year cursor; the year sits in the address, so Back returns to the same year | AI | Test: cursor check |
| 3.3 | Laptop grid: nine region lanes plus Ideas, time running down, scale widening toward today | AI | Renders with the test events |
| 3.4 | Phone layout: region chips, one or two lanes open | AI | Renders on a phone |
| 3.5 | Three fixed zoom levels (century, decade, year), chosen with a control | AI | Test: no free zoom |
| 3.6 | Cards by size: full card, half card, dot; each opens the preview | AI | Test |
| 3.7 | Arrows from the link table in the grade language; line weight by confidence; a stub where an arrow leaves the screen | AI | Test: web check (every arrow is a link) |
| 3.8 | Filters: type and depth chips, region, the rest behind More; dim, never remove | AI | Test |
| 3.9 | Coverage: a faint hatch where a lane has no event | AI | Test: coverage check |
| 3.10 | `/year-brief` and the year card, generated from data with a source on every figure | AI | Test: provenance check |
| 3.11 | Phone speed check | AI | Under 3 seconds |
| 3.12 | People test | C+AI | Fixes made |

**Test:** cursor, web, coverage and provenance checks pass; the timeline is quick on a phone.

## Phase 4: The political globe

Goal: the border maps on the new globe, fast on a phone.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 4.1 | Act on the licence check from step 2.6a: replace any source whose licence fails | AI | Every source cleared |
| 4.2 | A download script for the raw sources, recording version and licence | AI | Sources fetched by one command |
| 4.3 | Point the map scripts at the settings file from 0.2 | AI | Scripts run in the repo |
| 4.4 | Regenerate the province mesh | AI | 11,203 provinces |
| 4.5 | Fix the unseeded tie-breaking in `estimate.py` | AI | Two runs give identical output |
| 4.6 | Package shapes as PMTiles (coarse zoomed out, fine zoomed in) and owners as per-era tables | AI | Within the size budget |
| 4.7 | Upload to R2 | C+AI | Files served |
| 4.8 | The globe page: MapLibre globe; changing the year recolours without reloading | AI | Renders every year |
| 4.9 | Unions and overlords in lighter shades of the overlord's colour; names at low zoom | AI | Matches the rules |
| 4.10 | Peoples' homelands in a quiet colour, names when zoomed in; reader-facing names ("Aboriginal Australians") | AI | Test on sample years |
| 4.11 | Polity card: type, years, one line, territory thumbnail; Open country, Open the chronicle | AI | Test |
| 4.12 | `/place-events`: every event placed by coordinates and lane | AI | Test: placement check |
| 4.13 | Borders after 2019: the 2019 map carried forward plus dated, sourced fix files; ATLYNX as a reference for de facto borders (licence checked first) | AI | Each change sourced |
| 4.14 | `/border-fix` skill | AI | Runs end to end on one fix |
| 4.15 | Speed and record checks; people test | AI, C+AI | Under 3 seconds on a phone; record check passes |

**Test:** record check, placement check and the 3-second phone budget pass.

## Phase 5: Country profiles

Goal: a profile per polity per era, every figure sourced.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 5.1 | Profile schema: government, head, capital, religion, population, economy; every figure with source, year, basis and range | AI | In the schemas |
| 5.2 | The record per era (modern series, then Maddison, HYDE, Seshat, censuses, chronicles), with licences | AI, C approves | A list |
| 5.3 | Old `polities.json` profiles become leads (drafts) | AI, by script | Drafts made |
| 5.4 | `/profile` skill and the provenance reviewer | AI | Runs on one polity |
| 5.5 | The first 20 polities, reviewed | AI | Reviewed |
| 5.6 | Profile panel on the globe; Open country lands on it | AI | Test |
| 5.7 | The year card adds the summed profiles, with their basis | AI | Provenance check |

**Test:** provenance check passes; no pre-modern year filled from a modern series.

## Phase 6: Event pages at scale

Goal: the writing production line running, world turning points first.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 6.1 | Write the skills from what worked on the first event: `/event-page`, `/fact-check`, `/slop-check`, `/red-team`, `/flavor-check`, `/image` | AI | Each runs on one page |
| 6.2 | The progress board: every page's status by region, era and size, gaps shown | AI | Cade can open it |
| 6.3 | Score candidates for "The world" chain (three scores, one written reason each) | AI | A ranked list |
| 6.4 | Cade approves the first world turning points (a few hundred) | C | Approved list |
| 6.5 | The batch runner: 40 pages a batch in cloud sessions | AI | One batch runs end to end |
| 6.5a | Measure the first batch: cost and hours per page at the full standard; set the launch target from the number (hundreds of pages done properly, never thousands done thinly) | AI reports, C decides | A written pace and a launch target |
| 6.6 | Batches of world turning points, region by region | AI | Each batch reviewed |
| 6.7 | Cade samples three pages per batch | C | Signed off, or the batch fixed and sampled again |
| 6.8 | Pictures for each batch from open sources | AI | Licence line on every image |
| 6.9 | The world chain as the timeline's default view | AI | Test |

**Test:** every published page passes the fact check, the style checks and `/page-check`.

## Phase 7: Chronicles, stories and the front door

Goal: the chronicles readers follow, and the front door that offers them.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 7.1 | `/chronicle` and `/flow-check` (the five flow tests) | AI | Run on one chronicle |
| 7.2 | The German Question rebuilt as a chronicle (its 36 links exist) | AI | Flow tests pass |
| 7.3 | The Ottomans | AI | Flow tests pass |
| 7.4 | The chronicle page: portrait, story summaries, the depth control | AI | Renders on a phone |
| 7.5 | Cade's list of the next chronicles (Rome, the Spanish Empire, the Inca, the Atomic Age, Yemen, Christianity and more) | C | A ranked list |
| 7.6 | Decide on the six ancient story sets drafted in Prototype 1: recut or retire | C, AI advises | Decided |
| 7.7 | Write the next chronicles, biggest first | AI | Each through its checks |
| 7.8 | The front door goes live: random balanced eight, pins, the turn to a year, the world's turning points of those years | AI | Test; people test |

**Test:** flow tests pass on every chronicle; the front door passes a people test.

## Phase 8: Links, themes and chain mode

Goal: the web of cause and effect at scale, and the tools to follow it.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 8.1 | `/link`: type, grade, confidence, arrow note, the counterfactual for Necessary, the actor | AI | Runs on one link |
| 8.2 | Link the published events, chain by chain, each link red-teamed | AI | Batches reviewed |
| 8.3 | `/web-check`: arrows and links match both ways | AI | Passes |
| 8.4 | Chain mode: Follow, upstream and downstream toggles, three hops, the breadcrumb bar, the weakest-arrow bar | AI | Test |
| 8.5 | Pull: remove a Necessary event and grey everything downstream | AI | Test |
| 8.6 | Contested arrows show both readings on tap | AI | Test |
| 8.7 | The meanwhile line | AI | Test |
| 8.8 | `/theme` and the ten themes, each case a link | AI | Real-question, three-civilisation and node checks pass |
| 8.8a | Prototype one theme as a scroll-driven essay (Cade's lead, 2026-11-07): the argument unfolds as the reader scrolls, with sourced images and the themes voice; emotion from the order of facts, never adjectives; phone budget holds. If it works, every theme gets it, and the chronicle page tries the same with the globe and year moving as the reader scrolls | AI, C judges | A prototype Cade approves, or a note on why it failed |
| 8.9 | The Ideas lane | AI | Test |
| 8.10 | Compare two years | AI | Test |

**Test:** web check passes; chain mode passes a people test.

## Phase 9: Great people

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 9.1 | Pantheon: licence check and download | AI | Licence line |
| 9.2 | `/people-cut`: the thousand by tier scoring with a civilisation quota | AI | A list for Cade |
| 9.3 | Cade reviews the cut | C | Approved |
| 9.4 | `/person-page` and the chain check | AI | Runs on one person |
| 9.5 | The first 50 people | AI | Chain checks pass |
| 9.6 | Person cards everywhere; Follow their chain | AI | Test |
| 9.7 | Lives as bars on the timeline | AI | Test |
| 9.8 | The great man number, computed by the pipeline, and its theme essay | AI | Built |

**Test:** chain check passes on every person; no impact written as prose.

## Phase 10: Launch

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 10.1 | Buy the domain | C, AI guides | Owned |
| 10.2 | Connect the domain | C+AI | The site opens at it |
| 10.3 | About page: purpose, goal, the method in brief, the Cliopatria credit, every licence line | AI, C approves | Published |
| 10.4 | Visitor counting that respects privacy (proposed: Cloudflare Web Analytics; needs Cade's OK) | C approves | On |
| 10.5 | Not-found page and error pages | AI | Test |
| 10.6 | Speed and accessibility audit on a mid-range phone | AI | Passes |
| 10.7 | Google Search Console: submit the sitemap, check the structured data | C+AI | No errors |
| 10.8 | People test with five people who have never seen the atlas | C+AI | Fixes made |
| 10.9 | Launch | C | Public |

**Test:** every check green; Cade says go.

## Phase 11: The Explore globe

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 11.1 | `/layer`: fetch, licence by script, tiles, ranked table, brief, licence line | AI | Runs on one layer |
| 11.2 | The first layers: relief, rivers, climate, resources and minerals | AI | Each with its licence line |
| 11.3 | `/feature` and the first features (straits, fields, rivers), each linked into a chain | AI | Link check passes |
| 11.4 | `/trade-view` from OEC and UN Comtrade, licences checked | AI | Provenance on every figure |
| 11.5 | The control layer: per conflict, a licensed source, dated areas, review dates, neutral names | AI, C approves sources | Dated and sourced |
| 11.6 | Developing stories linked to the control layer | AI | Link check |
| 11.7 | Size budget and rank check | AI | Pass |

**Test:** licence, rank, size and link checks pass.

## Phase 12: The daily game

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 12.1 | Three original game designs built on the atlas's links and dates | AI | Written up |
| 12.2 | Cade picks one | C | Chosen |
| 12.3 | Prototype and play-test it | C+AI | Fun to play twice |
| 12.4 | The daily puzzle generator, from "today in history" and the links, with a review queue | AI | A month of puzzles queued |
| 12.5 | Shareable results that spoil nothing | AI | Test |
| 12.6 | Streaks kept on the reader's phone | AI | Test |
| 12.7 | Launch the game | C | Live |

**Test:** a month of puzzles reviewed; people test passes.

## Phase 13: The ancient world (unless step 2.2 folds it in earlier)

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 13.1 | Turn the 690 selected ancient events into starter files | AI | Drafts made |
| 13.2 | Ancient world turning points scored and approved | AI, C | Approved list |
| 13.3 | Ancient chronicles written (Rome, Persia, the Greek cities, early China, Egypt) | AI | Flow tests pass |
| 13.4 | The globe's years before 1400 checked on the new globe | AI | Record check passes |

**Test:** as Phases 6 and 7.
