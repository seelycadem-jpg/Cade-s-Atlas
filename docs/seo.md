# Found on Google (agreed 2026-11-03)

Every event, person, feature, chronicle and theme is a static page with its own address. The build enforces, on every page:

- Address: words, never ids (`/events/fall-of-constantinople-1453`).
- Title: the thing, its year, the site ("Fall of Constantinople, 1453 - Meanwhile Atlas"); unique to the page.
- Description: the Overview's first sentence, under 160 characters.
- Headings: the page structure as headings.
- Structured data: JSON-LD generated from the data model: Article for the page; Event with date and place; Person on people pages; Place on features; the Wikipedia and Britannica exits as sameAs.
- Images: alt text on every image; an Open Graph image per page.
- Sitemap rebuilt on every deploy; one canonical address per page; draft pages excluded.
- Speed: static pages, the globe loaded only where it appears, images sized at build; under 3 seconds on a phone.

`/page-check` runs in the build and fails any page missing a title, a description, structured data or alt text. Phase 10 submits the sitemap and checks the structured data with Google's tools.

Expectation: for the plain name of a famous event the encyclopedias rank first for a long time; the atlas competes on why, what it caused and who gained, and on the long tail of strands and fibres no one else has a page for. Inbound links from the daily game's shared results are part of being found.

## Growth: being found as widely as possible (Cade, 2026-11-16)

The aim is every search the atlas can answer well. Every tactic below is one Google
rewards; a tactic Google penalises costs the whole domain, so the bans at the end are hard.

**New kinds of page**
- **Year pages** (`/years/1453`): what happened in that year across the world, the knots
  first and every region's biggest events (structure.md, What the globe shows at a year),
  with the year card and a generated paragraph per region. "What happened in 1453" is
  one of the atlas's largest families of searches, and Meanwhile is its whole idea. A year
  with no event held gets no page.
- **On this day** (`/on-this-day/june-28`): the events of a calendar date across the
  years. The daily game and the email draw on the same material.
- **Chronicle and story pages** answer the broad searches ("history of Germany",
  "Weimar Republic"); their titles use the words people search.

**Inside every page**
- Every word a page holds is in its HTML when it loads. Drawers, tabs and the chain
  web's notes fold content; they never fetch it on a tap, because Google reads only what
  loads.
- Titles carry the question people ask where it fits, from a fixed pattern per page
  type, e.g. "Treaty of Versailles (1919): Causes and Consequences - Meanwhile Atlas".
  The visible heading stays the event's name.
- The description is the bottom line's first sentence, under 160 characters.
- Every link in the link table is also a plain text link between the two pages, so
  Google follows the chain as readers do.
- Large images (1,200 px wide or more, `max-image-preview:large`) on every page that has
  one, for Google Discover and Google Images; every map and graphic carries alt text.

**Trust**
- The About page names the editor (Cade) and the method in brief, and every page links
  to it. Pages name no authors in their text (CLAUDE.md); the site states who stands
  behind it.
- "Cite this page" on every page gives a ready citation for students and teachers.
  Citations are the links that raise a site's rank most.
- Graphics and maps can be embedded on other sites with their credit and a link back.

**Measuring**
- Google Search Console from launch: each month, the searches that show a page but win
  few clicks get a rewritten title or description.

**Never** (hard): bought or swapped links; words stuffed into a page; text shown to
Google and hidden from readers; thin pages made only to rank (an empty year, a name with
no event); the atlas's own site added to Wikipedia by us.

Source: Google's SEO starter guide, https://developers.google.com/search/docs/fundamentals/seo-starter-guide
