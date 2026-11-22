# The Unassuming Tavern (landing page)

A single static page: a worn wooden tavern floor in 32-bit pixel art, a title sign reading "the Unassuming Tavern", and three bright orange and teal buttons that open Poly Runner, Bloodsoup Hell and Lifebrained. No build step, no backend.

## Deploy (GitHub Pages)
1. Repo Settings > Pages: Source "Deploy from a branch", branch `main`, folder `/ (root)`.
2. Once you have a domain, put it in Settings > Pages > Custom domain, and in a file named `CNAME` at the repo root (the domain on one line, nothing else). Tick "Enforce HTTPS" when GitHub offers it.

## Domain setup
Fill in the blanks (nothing is set yet):

| What | Value |
|---|---|
| Custom domain | `<domain>` |
| Poly Runner subdomain | `<subdomain>.<domain>` |
| Bloodsoup Hell subdomain | `<subdomain>.<domain>` |
| Lifebrained subdomain | `<subdomain>.<domain>` |

DNS records at your registrar (set them DNS-only at first, so GitHub can issue the HTTPS certificate):
- This landing page, at the bare domain: either the four GitHub Pages `A` records (see GitHub's "Managing a custom domain for your GitHub Pages site" page for the current addresses), or a `CNAME` from `<domain>` to `<github-name>.github.io` if your DNS host flattens apex CNAMEs.
- Each app: a `CNAME` record from its subdomain to `<github-name>.github.io`.

In each app's repo: Settings > Pages > Custom domain = its subdomain (this also creates its `CNAME` file there).

Then open `config.js`, set `domain` and each site's `subdomain`, and the buttons link to `https://<subdomain>.<domain>/`. Until a subdomain works, a site's `githubPage` (its `github.io` address) can be used instead. Anything left blank shows a barred door.

## Updating
The version is `APP_VERSION` in `app.js`, bumped with every push to `main` except a docs-only one. Each such push also makes a GitHub release with a zip of the site. To redraw the floor: `python3 tools/make_floor.py` (needs Pillow and numpy).

## Files
See `ARCHITECTURE.md` for what each file does. The fonts (Press Start 2P and VT323) are under the SIL Open Font License; the license files sit in `assets/fonts/`.
