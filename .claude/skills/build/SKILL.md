---
name: build
description: Build and check the atlas. Runs the pipeline safety check and the site build with its browser tests, then reports. Use before any commit, when asked to build, or to confirm a change works.
---

# /build

Runs everything GitHub runs on a push (`.github/workflows/check.yml`), locally, and reports
in plain words. Never commits.

## Steps

1. From the repo root: `bash pipeline/check_build.sh`. It rebuilds the data into
   `work/check/` and compares it with `site/`. Report "pipeline check passed" or the
   first file that differs.
2. From `app/`: `npm test`. It builds the site, serves it, and runs the browser tests at
   phone and laptop size. If "already used" or "exited early" appears, run
   `npx astro preview stop` and try once more.
3. If a test fails, read the error (Playwright prints it under the test name), fix the
   cause (never the test), and rerun. Follow the `debugging-and-error-recovery` skill.
4. Report: each job's result in one line, how long it took, and the screenshot paths
   under `app/test-results/`. Send the screenshots to Cade when the look changed.

## Rules

- A red result blocks the commit (CLAUDE.md: never push to main with a red test).
- Never edit `site/` to make the pipeline check pass; it is Prototype 1, frozen.
- Never skip, disable or weaken a test to get green.
- Python packages: `pip install -r pipeline/requirements.txt`. Node: `npm ci` in `app/`.
