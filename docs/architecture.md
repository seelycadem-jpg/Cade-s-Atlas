# How the site is built (agreed 2026-11-05)

Prototype 1 was one 320 KB HTML file that loaded every screen, all 781 events (a 2.4 MB
data file) and several megabytes of maps at startup. It crashed on phones, and Google saw
one page. The new atlas is built the opposite way. These rules hold at 50,000 events and
past it.

## The rules

1. **A page per thing.** Every event, person, chronicle, story, theme, feature and polity
   is its own static page, built in advance by Astro, at a worded address that never
   changes. A page loads only itself. Google reads each one (`docs/seo.md`).
2. **No script unless the page needs one.** A reading page ships HTML and CSS. Interactive
   parts (the globe, the timeline, filters, the year cursor) load only on the pages that
   show them, as islands.
3. **Load the slice on screen.** The timeline and globes fetch the years, regions and
   sizes in view, and the next slice as the reader moves. No page loads the whole atlas.
4. **Maps as tiles.** Shapes are served as PMTiles from Cloudflare R2, coarse when zoomed
   out and fine when zoomed in. Changing the year recolours the map; it never reloads it.
5. **Big files stay out of Git.** Map tiles and images live on R2; the repo holds sources
   and code.
6. **Budgets, tested.** The build fails when a page is over its size budget, a page
   misses its Google fields, or a phone takes over 3 seconds. Budgets are set in Phase 2
   by the size test at 50,000 events and tightened, never loosened, after that.
7. **One source, one build.** Content lives in `content/`; the pipeline checks and
   prepares it; Astro turns it into pages; nothing built is edited by hand.

## Where things live

| Folder | Holds |
| --- | --- |
| `app/` | The website: Astro pages, layouts and components |
| `content/` | One file per event, person, chronicle and theme (from Phase 2) |
| `pipeline/` | Python checks and data preparation; map building |
| `site/` | Prototype 1, frozen; a source of leads only |
| `work/` | Scratch and large intermediates; never committed |

## Hosting

Cloudflare Workers, as static assets (`wrangler.jsonc` at the root serves `dist/`). GitHub
deploys on every merge to `main` (`.github/workflows/deploy.yml`) with a token held in the
repository secret `CLOUDFLARE_API_TOKEN`; Cloudflare's own Git-connected build is not used.
Live at https://cade-s-atlas.seelycadem.workers.dev until the domain arrives (Phase 10).
Limits checked 2026-11-05: 20,000 files on the free plan, 100,000 on Workers Paid.

## Running it

From `app/`: `npm run dev` starts a local preview; `npm run build` writes the finished site
to `app/dist/`.
`npm test` builds the site, serves it, and runs the browser tests at a phone size (Pixel 7)
and a laptop size (1280 by 800) with Playwright; screenshots land in `app/test-results/`.
Playwright is pinned to 1.63.0 to match the browser installed in the cloud sessions.

Astro is pinned to an exact version (7.4.2, which needs Node 22.23.4 or later). Upgrades are
their own step, never a side effect.
