# VectisVerse Website — Source of Truth

This repository and configuration are the only authorised production source for the VectisVerse website.

## Canonical source

- Repository: `rascal1234123/vectisverse`
- Production branch: `main`
- Website directory: `vectisverse-site-v1`
- Canonical Cloudflare Pages project: `vectisverse-pages`
- Production Pages domain: `vectisverse-pages.pages.dev`
- Cloudflare framework preset: `None`
- Build command: `exit 0`
- Root directory: `vectisverse-site-v1`
- Build output directory: `.`

## Working rule

All future website changes must be committed to `main` inside `vectisverse-site-v1`. Do not build from historical branches, copied folders, ZIP uploads, preview deployments or detached Cloudflare projects.

The approved Vectis Concepts production assets have now been consolidated into `main`. The `vectis-concepts-production-v1` branch is an archived historical source and must not be used for future editing or deployment.

## Cloudflare cleanup

The `vectisverse-pages` project is the only production project to retain automatic deployments and the public custom domains.

The older `vecverse` Pages project is a duplicate. Remove any VectisVerse custom domains from it, pause automatic deployments, and delete it only after the canonical project and both custom domains have been verified.

## Production domains

Attach these domains to `vectisverse-pages` only:

- `vectisverse.com`
- `www.vectisverse.com`

No other Cloudflare Pages project should retain either custom domain.
