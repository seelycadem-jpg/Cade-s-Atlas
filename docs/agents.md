# Meanwhile Atlas: agents, skills and the workflow per place (agreed 2026-11-03)

The full version, with the drawings, is the "Meanwhile Atlas: Build Plan" doc (Agent workflow tab, and the six sub-tabs under The six places).

## The session loop

One task per session. Plan mode first for anything over three files. A branch for anything risky. The Playwright test runs green before any commit; phone and laptop screenshots both. Commit small, push at the end of every session. `/code-review` before Cade reads the diff. A rule stated twice goes into CLAUDE.md; a pattern becomes a skill. Cloud sessions for long batches.

## The page pipeline

Draft from sources -> four reviewers in parallel, none of which has seen the draft being written (fact-checker, style editor, red team, flavor check) -> merge, where fact fixes bind and the other notes are answered -> recheck any claim added at merge -> published with an audit line. Data pages add a fifth reviewer, the provenance check. Stories and chronicles add the flow editor at assembly. Every reviewer returns a list of places with the failing test named, never a rewrite.

## Source verification (Cade, 2026-11-16)

Models invent sources: a real author with a book that does not exist, a real book with a page
that says something else. So no source reaches a page on one agent's word.

1. **Find.** The source finder searches and returns each candidate with its identifier (DOI,
   ISBN, archive reference or stable URL), the passage that supports the claim copied from
   the fetched text, and its kind (primary, scholarly, reference). It works only from what
   it fetches. It never adds a source from memory.
2. **Resolve, by script.** A script resolves every identifier against its registry (the DOI
   resolver, an ISBN catalogue, the archive's own catalogue, the URL itself) and fails a
   source whose record does not exist or whose author, title or year differ. Where the text
   is open, the script finds the copied passage in it, word for word. A script, never an
   agent, does this step.
3. **Verify, independently.** A source verifier that took no part in finding reads each
   passage against the claim it is cited for and answers: does it say this? It also checks
   independence (no shared author, neither drawing on the other) and the order of
   preference in event-pages.md.
4. **Rank.** The verifier fails a page whose terms, dates or quotations rest on scholarship
   where the primary record is available, or whose interpretation rests on a primary source
   alone.
5. **Bind.** The fact-checker checks every name, date and figure against verified sources
   only. A claim with no verified source is cut and goes to `open`; it is never softened.
6. **Keep.** Every cited web page is saved to the Internet Archive at verification, and a
   monthly script re-checks every link and reports the broken ones.
7. **Audit.** For the first batch Cade checks one source in five by hand; afterwards one in
   twenty. The error rate is recorded, and a rise stops the batch.

The build fails a page with a source missing its identifier, its passage, its verifier or
its date of verification. A paywalled book counts only where its passage can be read in a
catalogue preview or a library scan; otherwise it is left out.

Fetching sources needs the session's network to reach them. Where a host is blocked, the
session asks Cade to allow it (environment settings) and never cites the source unread.

## Skills

Each skill lives in `.claude/skills/<name>/SKILL.md` and is written once, in the session that first does the job by hand, from what worked.

| Skill | Does | Phase |
| --- | --- | --- |
| `/build` | Pipeline, schema validator, tests; reports | 0 |
| `/ship` | `/build`, commit, push; reports what deployed | 0 |
| `/page-check` | Title, description, worded address, structured data, alt text, sitemap entry on every page; fails the build on a miss | 3 |
| `/border-fix <polity> <years>` | Sourced fix file, owners rebuild, audit, ten spot-check screenshots | 4 |
| `/place-events <year>` | Places the year's events by coordinates and lane; placement check | 4 |
| `/profile <polity> <year>` | Country profile by era, source and year on every figure; provenance check | 5 |
| `/event-page <id>` | Drafts from sources; four reviewers; merge; recheck | 6 |
| `/find-sources <id>` | Searches and fetches candidate sources; returns identifier, kind and the copied passage per claim; never from memory | 6 |
| `/verify-sources <path>` | The resolver script, then the independent verifier: existence, passage, support, independence, order of preference; binding | 6 |
| `/fact-check <path>` | Every name, date, figure against verified sources only; binding | 6 |
| `/slop-check <path>` | Banned list, sentence length, active voice; fails on a match | 6 |
| `/red-team <path>` | "Where would you stop reading, and why" | 6 |
| `/flavor-check <path>` | Transplant test per paragraph; the four sources counted | 6 |
| `/image <event>` | Open sources only; licence by script; plain caption; never forced | 6 |
| `/chronicle <name>` | Portrait, story summaries, patches per knot; calls the flow editor | 7 |
| `/flow-check <story or chronicle>` | The five flow tests, top down and bottom up | 7 |
| `/link <a> <b>` | Graded link with arrow note, type, grade, confidence, actor; queues implied events | 8 |
| `/theme <name>` | Links behind each proposition; Cicero essay; real-question, three-civilisation, node checks | 8 |
| `/people-cut` | The thousand from Pantheon by tier scoring with a civilisation quota, for review | 9 |
| `/person-page <id>` | Life as a chain, impact as links; chain check | 9 |
| `/year-brief <year>` | The world-in-that-year card from the summed profiles | 3, refined in 8 |
| `/web-check <span>` | Arrows and links match both ways; coverage check | 8 |
| `/layer <name>` | Fetch, licence by script, PMTiles, ranked table, brief, licence line | 11 |
| `/feature <id>` | A feature page: geometry from its layer, brief, figures with source, links into chains, exits; four reviewers plus provenance | 11 |
| `/trade-view <country>` | Exports, imports, partners and the chokepoints the routes depend on, from OEC, Comtrade and the shipping layer; provenance binds | 11 |

## Per place: the checks on top of the pipeline

| Place | Skills | Extra checks | Fails when |
| --- | --- | --- | --- |
| Great people | `/people-cut`, `/person-page` | Chain check (every life event is an atlas event; every impact claim is a link); quota at selection; exits | An impact claim is prose; a life event has no page and no queue entry; length set by fame |
| Political globe | `/border-fix`, `/place-events`, `/profile` | Record check; placement check; provenance check; 3-second budget on a phone | A hand-edited polygon; an event without coordinates; a figure without source or year; a modern series filling an ancient year |
| Event pages | `/event-page` and its four reviewers, `/image` | Link check (every `[[id|words]]` resolves or is queued); exits; flow editor at assembly | A fact fix outstanding; rule zero or the active voice broken; a transplantable paragraph; a page shortened to pass |
| Explore globe | `/layer`, `/feature`, `/trade-view` | Licence check; rank check (reproducible by script); size budget; link check (every brief and every feature links into a chronicle); provenance on every figure | Licence unreadable; ranking not reproducible; over budget; a brief or feature with no link; a figure without source or year |
| Great themes | `/theme` | Real-question check; three-civilisation check; node check; link check on every case | A question asked to sound deep; a case without a link; a bare name; one civilisation |
| Timeline | `/year-brief`, `/web-check` | Web check; coverage check (gaps marked, never hidden); cursor check (one year, every place); provenance on the year card | An arrow without a link; a link without an arrow; a silent gap; a cursor that moves one place and not another |

## Eras without modern data

Where the modern series stop, name the best record for the era, state its basis and range, and write the figure as an estimate with that basis. A field with no record is blank and says so. Never fill an ancient year from a modern series.
