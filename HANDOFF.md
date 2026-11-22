# Handoff
Last updated 2026-11-22 (morning, published v3). Overwrite each time; keep under 40 lines. Change record: HISTORY.md (don't read unless asked).

## Goal
Landing page for the whole project ("the Unassuming Tavern") on Ricky's custom domain: pixel-art tavern floor, title sign, three buttons to Poly Runner, Bloodsoup Hell and Lifebrained on their own subdomains, all served by GitHub Pages (interim hosting bridge before the home server, see the Master Controller plan, item 7).

## Done
- 2026-11-21: repo was empty. Docs scaffolding matched to the other three repos and pushed to `main` (docs-only, so no version bump or release).
- 2026-11-21: page built on `next` (not published): `index.html`, `style.css`, `app.js`, `config.js`, generated floor, self-hosted fonts, favicon, `tools/make_floor.py`, `.github/workflows/release.yml`. Checked in headless Chromium at 320 to 1920px: no console errors, no sideways scroll, link resolution (domain + subdomain, GitHub Page fallback, blank = locked, non-https ignored), hover and keyboard focus states.

- 2026-11-22: published as version 1 (`next` pushed to `main`; release workflow makes the v1 release). Pages not yet switched on.
- 2026-11-22: published as version 2: github.io fallbacks set for Bloodsoup Hell and Lifebrained; locked doors say "Coming soon". Domain is theunassumingtavern.dev (landing on the bare domain; lifebrained. and bsh-companion. subdomains); Poly Runner skipped for now. Pages is on for all four repos.
- 2026-11-22: DNS and Pages custom domains set up on Cloudflare/GitHub for the landing (bare domain), Lifebrained and BSH-Companion; all load over HTTPS. Published v3: `config.js` points the doors at the subdomains.

## In progress
- Nothing.

## Decisions
- `config.js` holds the domain and subdomains; Poly Runner's values stay blank (door locked, "Coming soon") until Ricky gives them. Never guess an address.
- Page uses no service worker, backend or saved data (not a PWA).
- Repo is public (Pages on the free plan needs that). Shipping follows the Lifebrained pattern: work on `next`, publish only when Ricky says so.

## Next steps
1. Poly Runner: when Ricky is ready, pick a subdomain, add a CNAME in Cloudflare (DNS only) to ghstfssil.github.io, set the custom domain in its Pages settings, then set its `subdomain` in `config.js` and publish. The game file is `checker-run.html` (no `index.html` yet).
2. Later: replace Pages hosting with the home server (Master Controller plan, item 7).

## Gotchas
- Pages is on for `main` (root); `CNAME` (theunassumingtavern.dev) was committed by GitHub's settings screen, so merge `main` into `next` before new work.
- Tag pushes from the Claude session get 403; the release workflow makes tags.
- The floor is 192x192 and scales in whole-number steps; on tall phones only a slice of it shows (by design).
- Locked buttons use `aria-disabled`, not `disabled`, so they stay tappable and show the toast.
