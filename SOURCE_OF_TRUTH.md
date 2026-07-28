# VectisVerse Website — Source of Truth

This repository and configuration are the only authorised production source for the VectisVerse website.

## Canonical source

- Repository: `rascal1234123/vectisverse`
- Production branch: `main`
- Website directory: `vectisverse-site-v1`
- Cloudflare framework preset: `None`
- Build command: `exit 0`
- Root directory: `vectisverse-site-v1`
- Build output directory: `.`

## Working rule

All future website changes must be committed to `main` inside `vectisverse-site-v1`. Do not build from historical branches, copied folders, ZIP uploads, preview deployments or detached Cloudflare projects.

The `vectis-concepts-production-v1` branch is an archived historical source and must not be used for future editing once its approved assets have been consolidated into `main`.

## Production domains

Only one Cloudflare Pages project should have automatic deployments enabled and carry the public custom domains. Any duplicate Pages projects should be paused or deleted after the canonical project is verified.

The public domains should be attached to the canonical Pages project only:

- `vectisverse.com`
- `www.vectisverse.com`

The non-canonical Pages project must not retain either custom domain.
