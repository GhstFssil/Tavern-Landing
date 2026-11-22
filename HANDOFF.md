# Handoff
Last updated 2026-11-21 (evening). Overwrite each time; keep under 40 lines. Change record: HISTORY.md (don't read unless asked).

## Goal
Landing page for the whole project ("the Unassuming Tavern") on Ricky's custom domain: pixel-art tavern floor, title sign, three buttons to Poly Runner, Bloodsoup Hell and Lifebrained on their own subdomains, all served by GitHub Pages (interim hosting bridge before the home server, see the Master Controller plan, item 7).

## Done
- 2026-11-21: repo was empty. Docs scaffolding matched to the other three repos and pushed to `main` (docs-only, so no version bump or release).
- 2026-11-21: page built on `next` (not published): `index.html`, `style.css`, `app.js`, `config.js`, generated floor, self-hosted fonts, favicon, `tools/make_floor.py`, `.github/workflows/release.yml`. Checked in headless Chromium at 320 to 1920px: no console errors, no sideways scroll, link resolution (domain + subdomain, GitHub Page fallback, blank = locked, non-https ignored), hover and keyboard focus states.

## In progress
- Nothing.

## Decisions
- Domain, the three subdomains and the three GitHub Page addresses are all blank on purpose. Ricky fills them in `config.js`; no `CNAME` file exists yet (an empty or placeholder one can break Pages).
- Page uses no service worker, backend or saved data (not a PWA).
- Repo is public (Pages on the free plan needs that). Shipping follows the Lifebrained pattern: work on `next`, publish only when Ricky says so.

## Next steps
1. Ricky: register the domain; send it with the three subdomains and each app's `github.io` address, then fill `config.js`.
2. Add the `CNAME` file (domain only), turn on Pages for `main` (root), set DNS records (see README, Domain setup).
3. For each app repo: Pages on, custom domain = its subdomain.
4. Publish when ready: merge `main` into `next`, bump to version 1, push `next` to `main`.

## Gotchas
- Pages is not enabled yet and `main` has docs only until the first publish.
- Tag pushes from the Claude session get 403; the release workflow makes tags.
- The floor is 384x384 and scales in whole-number steps; on tall phones only a slice of it shows (by design).
- Locked buttons use `aria-disabled`, not `disabled`, so they stay tappable and show the toast.
