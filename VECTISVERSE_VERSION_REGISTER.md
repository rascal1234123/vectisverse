# VectisVerse Website Version Register

Last verified: 28 July 2026

This file is the repository source of truth for the VectisVerse website. It
separates the homepage, the Vectis Concepts page, protected recovery snapshots,
and work awaiting approval.

## Authoritative versions

| Area | Authoritative branch | Verified commit/base | Status |
| --- | --- | --- | --- |
| Live website and homepage | `main` | `153d4ccb1f2679956d084e0f4b6711465bc7737c` | Current production baseline |
| Vectis Concepts release candidate | `archive/concepts-release-candidate-2026-07-27` | `c60af6fd9a113a2ee54ddb2b83b4e203faa9949d` | Protected recovery snapshot; do not edit |
| Combined website review | `agent/vectisverse-version-fix` | Created from the verified `main` baseline above | Review only until approved |

## Vectis Concepts release candidate

The deployable Concepts page is:

- `vectisverse-site-v1/concepts.html`

Its active production assets are:

- `vectisverse-site-v1/assets/css/concepts-stage-2.css`
- `vectisverse-site-v1/assets/js/concepts-stage-2.js`
- `vectisverse-site-v1/assets/hero/hero-logo.svg`
- `vectisverse-site-v1/assets/hero/hero-production-desktop.png`
- `vectisverse-site-v1/assets/services/`
- `vectisverse-site-v1/assets/featured/`
- `vectisverse-site-v1/assets/shared/`
- `vectisverse-site-v1/assets/footer/`

The layered sketch-transition source remains protected on the release-candidate
archive branch under:

- `vectisverse-site-v1/assets/hero/hero-composite-desktop.svg`
- `vectisverse-site-v1/VectisVerse-Website-GoldMaster-v1/assets/hero/`

## Working rules

1. `main` is the live production baseline. It is changed only through an
   approved integration branch.
2. Protected `archive/` branches are never used for ongoing design changes.
3. Homepage and Concepts work must use separate feature branches.
4. Do not merge the historical `vectis-concepts-production-v1` branch wholesale
   into `main`; it contains mixed Homepage and Concepts changes.
5. Integrate only the files required by the page being approved.
6. Approved logos, posters, character art and other locked assets must be reused
   without redraws or unapproved substitutions.
7. Every review branch must be checked at desktop, tablet and iPhone widths
   before it can be merged into `main`.

## Recovery note

The 27 July Concepts page and its source assets were not lost. They were
preserved on the protected release-candidate branch before this clean
integration branch was created from the latest homepage baseline.
