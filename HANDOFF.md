# Handoff
Last updated 2026-11-23 (evening, torches removed on `next`, not published). Overwrite each time; keep under 40 lines. Change record: HISTORY.md (don't read unless asked).

## Goal
Landing page for the whole project ("the Unassuming Tavern") on theunassumingtavern.dev: pixel-art tavern floor, title sign, three buttons to Poly Runner, Bloodsoup Hell and Lifebrained on their own subdomains, all served by GitHub Pages (interim bridge before the home server, Master Controller plan item 7).

## Done
- 2026-11-21/22: page built and published as v1-v3; DNS and Pages custom domains live for the landing, Lifebrained and BSH-Companion (see HISTORY.md).
- 2026-11-23: merged `main` into `next` (Ricky's backlog items). Removed the torches (sprites, `buildTorches()`, torch CSS) and the sign's chains; checked at 390 and 1280px: no console errors, three doors, no sideways scroll. On `next` only; ships as v4 when Ricky says publish.

## In progress
- Nothing.

## Decisions
- `config.js` holds the domain and subdomains; Poly Runner stays blank (locked, "Coming soon") until Ricky gives it. Never guess an address.
- No service worker, backend or saved data (not a PWA). Repo is public for free Pages.
- Shipping: work on `next`, publish only when Ricky says so.

## Next steps (agreed plan, 2026-11-23, in order)
1. Publish v4 when Ricky says so.
2. Docs refresh across all four repos: replace Netlify references with Pages + Cloudflare DNS; check docs are consistent across repos. Docs-only, straight to `main`; CLAUDE.md edits need Ricky's OK.
3. Push/add-repo permissions: check the nightly sweep scheduled task's repo sources and push access; add a startup step that attaches all four repos with push; test with a manual run.
4. One Tavern account: design doc first (one main Supabase project, a schema per app, merge users by email, dry run on a copy). Open question: do it now or once Supabase is self-hosted.
5. Future Projects in BACKLOG.md (Warden, storage cleaner, trading wrapper, Magic cards) to move into the Master Controller plan.
6. Poly Runner door: pick a subdomain, Cloudflare CNAME to ghstfssil.github.io, Pages custom domain, set `subdomain` in `config.js`. Game file is `checker-run.html` (no `index.html` yet).

## Gotchas
- `CNAME` was committed by GitHub's settings screen; merge `main` into `next` before new work.
- Tag pushes from the Claude session get 403; the release workflow makes tags.
- Floor is 192x192 and scales in whole-number steps; on tall phones only a slice shows (by design).
- Locked buttons use `aria-disabled`, not `disabled`, so they stay tappable and show the toast.
