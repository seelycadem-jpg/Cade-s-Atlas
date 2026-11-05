---
name: ship
description: Ship the atlas. Runs /build, then commits and pushes to the session's branch and reports what went up and whether GitHub's checks passed. Use when asked to ship, push, or save work to GitHub.
---

# /ship

## Steps

1. Run `/build`. Stop on red and say what failed.
2. `git status --short`: list what changed. Nothing from `site/`, no `node_modules/`,
   `dist/`, `work/` or `test-results/`, no secrets. If any of those appear, fix
   `.gitignore` first.
3. Commit with a message in the house style: a one-line summary of what the reader of
   the log gets, then a short paragraph on what changed and what was checked. Name the
   roadmap step and "closes #N" when a step issue is done.
4. `git push -u origin <branch>`; on a network failure retry with 2, 4, 8, 16 second waits.
5. Wait for GitHub's check (the `check` workflow) and report its result. On red, read the
   failed job's log, fix, and ship again.
6. Report to Cade in plain words: what shipped, the check result, and the next step.

## Rules

- Push only to the session's branch; never to `main` (Cade merges through a pull request).
- Never force-push, rewrite history or delete a branch.
- Explain any Git word the first time it comes up in the report.
