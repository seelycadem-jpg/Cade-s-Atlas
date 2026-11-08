# Project skills

Skills Claude Code loads in every session on this repo.

The atlas's own:

- `build`: the pipeline check and the site build with browser tests; reports, never commits.
- `ship`: `/build`, then commit and push to the session's branch; waits for GitHub's check. The atlas's own skills
(`/build`, `/ship`, `/page-check` and the rest in `docs/agents.md`) are added here as
each is first done by hand.

Copied from github.com/anthropics/skills (commit ca45fc4), Apache 2.0, licence kept in each folder:

- `frontend-design`: guidance for a distinctive, deliberate visual design. CLAUDE.md and
  the docs win where they conflict.
- `webapp-testing`: testing the site in a real browser with Playwright.

Copied from github.com/addyosmani/agent-skills (commit 301b02b), MIT, licence kept in each
folder; the checklists they point to are in `.claude/references/`:

- `incremental-implementation`: build in thin slices, each one tested.
- `frontend-ui-engineering`: accessible, responsive interfaces.
- `performance-optimization`: measure first; the 3-second phone budget.
- `ci-cd-and-automation`: the build and tests run on every push.
- `debugging-and-error-recovery`: find the cause before fixing.
- `source-driven-development`: check each tool's official docs before using it.
- `shipping-and-launch`: the checks before going live.
- `test-driven-development`: write the test, then the code.

Left out on purpose: that collection's `/build` and `/ship` commands (the atlas has its own,
see `docs/agents.md`), its hooks, and skills that duplicate the roadmap, the built-in
`/code-review` and `/simplify`, or need tools this project does not use. Where a skill's
examples assume another stack (React, Jest, Vercel), the approved stack in
`docs/rebuild-plan.md` wins; CLAUDE.md wins over every skill.

Copied from github.com/nextlevelbuilder/ui-ux-pro-max-skill (commit b7d5353), MIT, licence
kept in the folder:

- `ui-ux-pro-max`: a searchable local database (pure Python, no network): 119 UX rules
  (touch targets, contrast, navigation, forms), 74 font pairings with their licences, 192
  palettes, 80 interface styles. Use it as a checklist and a reference. Its
  `--design-system` output is generic (it proposed a SaaS landing page with Poppins for
  the atlas), so it never decides the look: `docs/design/brief.md`, the `frontend-design`
  skill and CLAUDE.md win. The repo's other six skills (logos, banners, slides, social
  images, a Tailwind kit) are left out: paid image services or a different stack.

Considered and set aside (2026-11-07): `nateherkai/scroll-craft`, a skill for scroll-driven
marketing landing pages with AI-generated imagery. The atlas is a reading and navigation
tool with a phone speed budget and sourced images only, so it does not fit. Its hero-depth
reference may be worth a read for the About page alone.
