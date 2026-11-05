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
chronicles and 150,000 links**. Ten rules follow from that, and they are built in from the
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

The full list of phases and their small steps is in `docs/roadmap.md`. Each step is a
GitHub issue, grouped under one parent issue per phase.

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
