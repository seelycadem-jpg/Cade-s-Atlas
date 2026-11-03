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

Source: Google's SEO starter guide, https://developers.google.com/search/docs/fundamentals/seo-starter-guide
