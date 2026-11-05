# The rebuild, step by step (proposed 2026-11-05)

A plain-words plan for rebuilding Meanwhile Atlas from scratch. Written for Cade, who is new
to code, Git and GitHub. Every phase ends with a test we can run; we only move on when it
passes. Where this plan and the "Meanwhile Atlas: Build Plan" doc disagree, the Build Plan
doc wins and this file gets corrected.

---

## Part 1: The big picture

### What "from scratch" means here

Three things get rebuilt. Two things are kept, because they already work and were checked.

| | What it is | Rebuilt or kept |
| --- | --- | --- |
| The website (the app) | What readers see and tap | **Rebuilt** in a new folder, `app/` |
| The writing | Every event page, chronicle, theme | **Rebuilt** to the new event-page standard, in `content/` |
| The data model | How an event, a link, a person is described | **Rebuilt** to the fields agreed on 3 Nov |
| The border maps | Who owned which province, every year | **Kept**. Built by the pipeline from sourced records |
| The pipeline | The Python scripts that turn sources into data | **Kept**, then cleaned up |

The old 781 events become a to-do list and a source of leads. Each one is rewritten and
checked before readers see it. Nothing old ships as it is.

### How the pieces fit

Think of a kitchen:

1. **Content** (the recipes): one text file per event, person, chronicle and theme, in
   `content/`. Agents write them; reviewers check them; you approve.
2. **Pipeline** (the prep cook): scripts that check every file has its required fields,
   build the link table, and prepare the map files.
3. **App** (the dining room): the website. It turns each content file into a real web
   page with its own address, and draws the globe and the timeline.
4. **Tests** (the health inspector): small programs that open the site on a phone-sized
   and a laptop-sized screen and check nothing is broken. Nothing is saved to `main`
   if they fail.
5. **Hosting** (the building): a service that puts the site on the internet.

### The one big idea: one finished slice before scaling up

We first build **one event, completely**, chosen by you (Part 3). Its page, its spot on the globe, its
place on the timeline, its links, on a phone, tested, live on the internet. Only then do
we scale up to hundreds of events. If something about the design is wrong, we find out
after one page, not after five hundred.

### Built to be big

The finished atlas will be many times the size of Prototype 1: thousands of events at three
sizes, many chronicles and stories, a thousand people, and tens of thousands of links. Until
Cade gives better numbers, the plan assumes about **50,000 events or more, 1,000 people, 100
chronicles and 50,000 links**. Ten rules follow from that, and they are built in from the
start because they are expensive to change later.

1. **Addresses never change.** Every event's web address and id are fixed when it is
   created. Thousands of links, Google results and shared game scores point at them.
2. **One event, many chains, from day one.** The data model records an event's size per
   chain (`docs/narrative-flow.md`), so the same event can be a turning point in one
   chronicle and a small step in another.
3. **The phone never loads everything.** The timeline and globe load only the slice of
   time, region and size on screen, and fetch the rest as the reader moves. A size budget
   per slice is tested.
4. **Split files.** Links live in one file per chain, never in one giant file. Content
   lives in one file per event, in folders by region.
5. **The build checks everything, fast.** Every field, every `[[link]]`, every arrow,
   across every file, on every build. A check that takes too long gets rebuilt, never
   skipped.
6. **Search is built in advance.** With thousands of pages, search uses a ready-made
   index split into small pieces (Pagefind is the proposed tool; it needs Cade's OK).
7. **Big files stay out of the repo.** Images and map tiles go to Cloudflare R2.
8. **Hosting limits are checked early.** Cloudflare Pages caps the number of files per
   upload (about 20,000 on the free plan, well under 50,000 pages; to be confirmed). The page count is planned
   against that cap before it is reached.
9. **Writing is a production line.** Thousands of pages through four reviewers each means
   batches run in cloud sessions, a progress board showing every page's status, and
   turning points written first, small events last.
10. **Cade reviews by sample.** Nobody reads every page. Cade reads a few from every
    batch, and a batch that fails gets fixed and sampled again.

---

## Part 2: Words you will see

| Word | Plain meaning |
| --- | --- |
| Repo | The project folder, kept on GitHub with its full history |
| Commit | A saved snapshot with a note saying what changed. You can always go back to one |
| Push | Send your commits up to GitHub |
| Branch | A safe side copy of the project. `main` is the official one |
| Pull request (PR) | "Please merge my branch into `main`". It shows every change for you to approve |
| Stack | The set of tools the website is built with |
| Framework | A ready-made toolkit that does the boring parts of building a site |
| Build | Running the scripts that turn content into the finished site |
| Deploy | Putting the finished site on the internet |
| CI | GitHub running the tests by itself every time we push |
| Schema | The list of fields a file must have, checked by the build |
| Component | A reusable piece of the screen, like the preview card or the nav bar |
| Static page | A page built once in advance, so it loads fast and Google can read it |

---

## Part 3: Decisions only Cade can make

I recommend an answer for each. Say yes, or tell me what you'd prefer.

1. **The stack.** Approved by Cade on 5 Nov 2026.
2. **Hosting account.** Your docs already put images and map tiles on Cloudflare R2, so I
   recommend Cloudflare Pages for the site too: free at this size, fast worldwide. You
   create the account (about 10 minutes, I'll walk you through it).
3. **Domain name.** The web address, about $10 to $15 a year. Not needed until launch.
4. **The first event.** The one event we build end to end before scaling up. Pick one you
   know well and care about, so you can judge whether the page is right. Paris 1919 in
   `docs/event-pages.md` is only an example of the writing style.
5. **Ancient events.** 690 events from 3400 BCE to 1439 are selected but not written. I
   recommend they wait until after launch, so the first version covers 1440 to today.

### The stack (approved 2026-11-05)

| Job | Tool | Why |
| --- | --- | --- |
| Turn content files into fast web pages | **Astro** | Built for content sites: every event gets a real page Google can read, which `docs/seo.md` requires. It checks every file's fields against a schema, which `docs/event-pages.md` requires |
| Interactive parts (timeline, year cursor, cards) | **Svelte**, used only inside those parts | Small and simple; keeps the shared year cursor in step across the globe, timeline and pages |
| The globe | **MapLibre GL** with **PMTiles** | Already chosen and used; draws on the phone's graphics chip, so it stays smooth |
| Pipeline | **Python** (kept) | Already works and is verified |
| Tests | **Playwright** | Opens the site in a real browser at phone and laptop sizes |
| Hosting | **Cloudflare Pages** and **R2** | R2 is already in the docs for images and tiles |
| Search (proposed, not yet approved) | **Pagefind** | Builds a search index split into small pieces, so search stays fast with thousands of pages |
| Running tests on every push | **GitHub Actions** | Free, built into GitHub |

---

## Part 4: The phases

Each phase lists its small steps, who does each one, and the test that says the phase is
done. Phases 0 to 2 are planned in full detail. Later phases are listed at a coarser level,
and each one is broken into small steps when we reach it, because what we learn earlier
will change them.

Phase numbers follow `docs/agents.md`. Phases 1 and 2 are my best reading of the gap there;
correct me from the Build Plan doc.

### Phase 0: Foundation (the workbench)

Goal: the project builds and tests itself, and a blank site is live on the internet.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 0.1 | Approve the stack (Part 3) | Cade | You've said yes |
| 0.2 | Point the pipeline scripts at this project's folders instead of the old chat's folders (one settings file) | Claude | `pipeline/build.sh` runs inside the repo |
| 0.3 | Check the rebuilt data matches the old data exactly | Claude | Same 781 events, same 36 links |
| 0.4 | Drop the one unused build step (`polities.py`, per `pipeline/README.md`) | Claude | `rules.json` matches too |
| 0.5 | Create the empty `app/` with Astro: one blank page that says "Meanwhile Atlas" | Claude | It opens in a browser here |
| 0.6 | Add the first test: open the page at phone and laptop size, check the title, save screenshots | Claude | The test passes; you see both screenshots |
| 0.7 | Make GitHub run the build and the test on every push (CI) | Claude | A green tick appears on GitHub |
| 0.8 | Create a Cloudflare account | Cade, with me guiding | You can log in |
| 0.9 | Connect the repo to Cloudflare Pages so each push puts the site online | Cade and Claude | The blank page has a web address you can open on your phone |
| 0.10 | Write the `/build` and `/ship` skills from what worked | Claude | Each runs with one command |
| 0.11 | Your first pull request: review it, then merge it into `main` | Cade, with me guiding | `main` holds Phase 0 |

**Phase 0 test:** `build.sh` runs clean, the test passes on push, and the blank site opens on
your phone.

### Phase 1: Look and feel (the design system)

Goal: decide how the atlas looks and feels on a phone before building real screens. "Top-tier
UI is the key measure", so this phase gets its own time.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 1.1 | Collect what you liked and disliked in Prototype 1, and 3 to 5 sites whose look you admire | Cade | A short list |
| 1.2 | Propose two or three directions: fonts, colours, spacing, with a mock event page on a phone | Claude | You can tap through each mock |
| 1.3 | Pick one direction, or mix | Cade | Chosen |
| 1.3a | Mock the front door on a phone: the plain earth, the eight chronicle cards, the turn to a first year with its political map and the world's turning points of those years (`docs/vision.md`) | Claude, Cade approves | You can tap through it |
| 1.4 | Build the colour and font settings (light and dark) as one shared file | Claude | Every page uses it |
| 1.5 | Build the navigation bar: bottom strip on a phone, left rail on a laptop, the six places, Back, the year, search | Claude | Test: present on every page, both sizes |
| 1.6 | Build the one shared preview card (picture, title, date, one line, Open) | Claude | Test: opens on long-press and hover; closing returns to the same spot |
| 1.7 | Build the breadcrumb and the Return chip | Claude | Test: Back lands on the exact place left |
| 1.8 | Accessibility check: text size, contrast, tap-target size | Claude | Passes the check |

**Phase 1 test:** you open the mock pages on your phone and say they look right.

### Phase 2: The data model and the first slice

Goal: describe each kind of thing exactly, then take the first event all the way through.

| # | Step | Who | Done when |
| --- | --- | --- | --- |
| 2.1 | Write the schemas for the seven objects (event, link, person, polity, feature, layer, theme) from `docs/narrative-flow.md` and `docs/event-pages.md` | Claude | The build rejects a file with a missing field |
| 2.2 | Fix the address and id rules for every kind of thing; they never change after this | Claude proposes, Cade approves | Written into the schemas |
| 2.3 | Create `content/` with its folders, split by region | Claude | Exists |
| 2.4 | **Size test:** generate 50,000 fake test events and 150,000 fake links (marked fake, deleted after, never shipped) and measure build time, file count and phone load | Claude | Build under 10 minutes; the phone loads a timeline slice in under 3 seconds; file count fits the host |
| 2.5 | Make a starter file for each old event: header fields filled where the old data holds them, text empty, status `draft` | Claude, by script | 781 draft files; none visible to readers |
| 2.6 | Move the 36 graded links into the link table (built by the pipeline, never by hand) | Claude, by script | Same 36 links, each with its note |
| 2.7 | Write the first event through the full writing pipeline: draft from sources, four reviewers, merge, recheck | Claude agents | Status `reviewed` |
| 2.8 | You read the first event | Cade | Approved, or notes sent back |
| 2.9 | Build the event page: the takeaway strip from the data header, the four layers, "Open the detail" | Claude | The page renders on phone and laptop |
| 2.10 | Inline links (`[[...]]`) open the preview card | Claude | Test: every link resolves or is queued |
| 2.11 | `/page-check`: title, description, address in words, structured data, alt text, sitemap | Claude | Fails the build on a miss |
| 2.12 | Put the first event live | Claude | It opens on your phone at its own web address |

**Phase 2 test:** the first event is live, passes every check, and you approve it on your phone.

### Phase 3: The year card and the timeline (first version)

Goal: the shared year cursor and the timeline grid, using the events published so far.

- The year card from the summed data (`/year-brief`).
- The timeline grid: nine region lanes plus Ideas, three fixed zoom levels, phone layout
  (`docs/timeline.md`).
- The year cursor moves the timeline and every other place together.
- Test: the cursor check (one year, every place).

### Phase 4: The political globe

Goal: the border maps on the new globe, fast on a phone.

- Package the province map and owners as map tiles (PMTiles) on R2.
- The globe page: year cursor, borders, polity cards, Open country.
- Place every event by coordinates and lane (`/place-events`).
- Border corrections only through sourced fix files (`/border-fix`).
- Test: loads in under 3 seconds on a phone; record check and placement check pass.

### Phase 5: Country profiles

- A profile per polity per era, a source and year on every figure (`/profile`).
- Old eras use the best record for the era, with its basis and range, or stay blank.
- Test: provenance check.

### Phase 6: Event pages at scale

- Write the `/event-page` skill and the reviewer skills from what worked on the first event.
- Build the progress board: every page's status, by region, era and size, with gaps shown.
- Batches of about forty events, Europe first, each batch through the four reviewers.
- You spot-read a few from each batch.
- Test: every published page passes the fact check, style checks and `/page-check`.

### Phase 7: Chronicles and stories

- Start with the German Question (36 links already exist) and the Ottomans.
- Flow editor at assembly (`/chronicle`, `/flow-check`).

### Phase 8: Links, themes, and the timeline's chain mode

- Grade links across all events (`/link`); themes essays (`/theme`).
- Timeline chain mode: Follow, upstream and downstream, Pull a Necessary event.
- Test: web check (every arrow is a link and every link is drawn).

### Phase 9: Great people

- The thousand from Pantheon, then person pages as chains (`/people-cut`, `/person-page`).

### Phase 10: Launch

- Domain name, About page with the Cliopatria credit, sitemap sent to Google, final
  phone speed check.

### Phase 11: The Explore globe

- Layers, features and the trade view, each with its licence line.

### Phase 12: The daily game

- The Wordle-style daily history game, seeded from "today in history". The quiz stays
  deferred until links and arrow notes have shipped.

---

## Part 5: How every session runs

1. One task per session.
2. I say what I'll do in plain words before I do it.
3. I work on a branch, so `main` is never at risk.
4. Tests run before every commit; you get phone and laptop screenshots.
5. I commit small pieces with clear notes and push at the end of the session.
6. You review the pull request and merge it, with me explaining what you're looking at.

## Right now

Step 0.2: point the pipeline scripts at this project's folders.
