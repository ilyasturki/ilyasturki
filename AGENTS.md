# AGENTS.md

## What this repo is

This is the special GitHub profile repo at https://github.com/ilyasturki/ilyasturki — the one whose name matches the username, so its `README.md` renders on the profile page at https://github.com/ilyasturki.

Changes land on the profile as soon as they're pushed to `main`. The look follows ilyasturki.com: pencil strokes, Caveat and Kalam, greys.

- `assets/*.svg` are the hand-drawn header and section labels, one `-light` and one `-dark` per image, swapped by `<picture>`. GitHub loads no fonts inside an SVG, so their text is outlined to paths: change the wording in `scripts/draw.py` and regenerate with `nix-shell -p 'python3.withPackages(p: [p.fonttools p.brotli])' --run 'python3 scripts/draw.py ~/Projects/ilyasturki/public/fonts assets'`.
- The list between `<!-- journal:start -->` and `<!-- journal:end -->` belongs to `.github/workflows/journal.yml`, which rewrites it daily from the site's feed through `scripts/journal.py`. Pull before editing the README: the bot commits to `main`.

## Owner

Ilyas Turki — full-stack developer based in Paris. Contact: turki.ilyass@gmail.com.
