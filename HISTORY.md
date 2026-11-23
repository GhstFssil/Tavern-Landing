# History
Append-only record of every change to this repo since 2026-11-21. Never edit or delete a line; correct a mistake with a new line. Sessions don't read this file unless Ricky asks. Times are America/Chicago.
Format: `- YYYY-MM-DD HH:MM | branch or version | what changed (and why, briefly)`
Add a line with `echo '- ...' >> HISTORY.md`.

- 2026-11-21 18:12 | main | Repo scaffolding matched to Poly-Runner, Lifebrained and BSH-Companion: CLAUDE.md, ARCHITECTURE.md, README.md, BACKLOG.md, HANDOFF.md, HISTORY.md, .gitattributes (union merge for HISTORY.md), .gitignore
- 2026-11-21 18:20 | next | Landing page built: index.html, style.css, app.js (APP_VERSION 0.1), config.js (domain, subdomains and GitHub Page addresses blank), generated pixel tavern floor (tools/make_floor.py), self-hosted fonts, favicon, release workflow
- 2026-11-21 19:10 | next | Removed the button icons; button labels now centered and sized to nearly fill the buttons (config.js no longer has an icon field)
- 2026-11-21 19:25 | next | Floor pixels twice as coarse: tools/make_floor.py averages the 384px drawing down to 192px (DOWN=2) and fitFloor() in app.js scales from 192
- 2026-11-22 08:31 | next | Version 1: first publish of the landing page (APP_VERSION 0.1 -> 1); pushed to main
- 2026-11-22 08:49 | next | Added github.io fallbacks for Bloodsoup Hell and Lifebrained (Poly Runner left blank); locked doors now say "<name>: Coming soon."; domain and subdomains still blank until DNS works
- 2026-11-22 08:52 | v2 | Published: github.io fallbacks for Bloodsoup Hell and Lifebrained, "Coming soon" on locked doors (APP_VERSION 1 -> 2); pushed next to main
- 2026-11-22 09:45 | v3 | Published: config.js now has domain theunassumingtavern.dev and subdomains bsh-companion and lifebrained (Poly Runner still blank, shows Coming soon); APP_VERSION 2 -> 3; pushed next to main
- 2026-11-23 17:58 | next | Removed the torches (sprites, buildTorches(), torch CSS) and the chains above the sign, per Ricky's backlog; docs and handoff updated
- 2026-11-23 18:00 | v4 | Published: torches and sign chains removed (APP_VERSION 3 -> 4); pushed next to main
