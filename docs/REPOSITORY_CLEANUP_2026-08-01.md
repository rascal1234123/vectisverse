# VectisVerse Repository Cleanup — 1 August 2026

## Scope

This report records the controlled cleanup performed after `docs/REPOSITORY_AUDIT_2026-08-01.md`.

The cleanup preserves the production model defined in `SOURCE_OF_TRUTH.md`:

- production branch: `main`
- published directory: `vectisverse-site-v1`
- Cloudflare framework preset: `None`
- build command: `exit 0`

No live HTML, CSS, JavaScript, form settings, current logos, current hero images or currently referenced featured boards were changed.

## Recovery branch

Before removing any asset, the complete pre-cleanup state of `main` was preserved as:

`archive/pre-repository-cleanup-2026-08-01`

This branch points to commit:

`fb0275632593d90749e439c8e9f976546ac72abd`

It contains the exact superseded SVG masters, PNG previews and README removed from the active production tree.

## Removed from the published production tree

### Superseded layered SVG masters

The following eight unreferenced layered masters were removed from `main` after the recovery branch was created:

- `vectisverse-site-v1/assets/featured/sports_club_identity_layered.svg`
- `vectisverse-site-v1/assets/featured/corporate_character_system_layered.svg`
- `vectisverse-site-v1/assets/featured/childrens_charity_layered.svg`
- `vectisverse-site-v1/assets/featured/heritage_brand_layered.svg`
- `vectisverse-site-v1/assets/featured/outdoor_brand_layered.svg`
- `vectisverse-site-v1/assets/featured/science_centre_layered.svg`
- `vectisverse-site-v1/assets/featured/educational_universe_layered.svg`
- `vectisverse-site-v1/assets/featured/esports_team_layered.svg`

### Superseded PNG preview exports

The matching eight unreferenced preview exports were also removed from `main`:

- `sports_club_identity.png`
- `corporate_character_system.png`
- `childrens_charity.png`
- `heritage_brand.png`
- `outdoor_brand.png`
- `science_centre.png`
- `educational_universe.png`
- `esports_team.png`

### Outdated README

The superseded `vectisverse-site-v1/assets/featured/README.txt` was removed because it described the older eight-board set as active production material.

## Production assurance

The current `concepts.html` continues to reference:

- the four retained original layered featured boards;
- the ten finished UUID-named PNG boards.

None of the removed files was referenced by the current production page.

A removed layered master was confirmed absent from `main` and present on `archive/pre-repository-cleanup-2026-08-01` with the same blob SHA.

## Branch comparison results

### Safe deletion candidates — no unique file content

The following branches are fully behind `main` with no unique commits or file differences:

- `backup/pre-clean-build-001`
- `backup-before-build-001-2026-07-26`
- `site-consolidation-test`
- `temp-ignore`

`ftw-asset-upload` is divergent by two commits but has no file differences against `main`; it is also a strong deletion candidate after confirming the two commits are empty or metadata-only.

### Duplicate Stage 3 branches

The following four branches have identical comparison results and file sets:

- `stage3-tree-test`
- `stage3-tree-test2`
- `stage3-tree-test3`
- `stage3-tree-test4`

Recommended action:

- retain at most one as an intentional historical branch if the BUILD-002 reports are still useful;
- delete the other three duplicates.

### Retain pending consolidation or historical decision

- `agent/vectisverse-version-fix` — contains a divergent historical Concepts implementation and `VECTISVERSE_VERSION_REGISTER.md`.
- `cloudflare/workers-autoconfig` — contains abandoned `.gitignore` and `wrangler.jsonc` files; it contradicts the chosen Pages-only build but should be deleted only after confirming no Cloudflare account process still references it.
- `archive/concepts-release-candidate-2026-07-27` — intentionally historical.
- `vectis-concepts-production-v1` — explicitly identified by `SOURCE_OF_TRUTH.md` as an archived historical source.
- `archive/pre-repository-cleanup-2026-08-01` — required recovery branch for this cleanup.

## Branch deletion limitation

The connected GitHub API available during this cleanup supports branch comparison and creation but does not expose branch-ref deletion. No branch was therefore deleted automatically.

The branches listed as safe deletion candidates can be removed through the GitHub branch interface without affecting `main`.

## Wider binary inventory limitation

A complete recursive tree and duplicate-hash export was not available through the connector. No claim is made that every unreferenced binary, ZIP, editor file or historic numbered asset has been identified.

A later full clone-based inventory can still check for:

- ZIP archives;
- `.DS_Store`, `Thumbs.db` and editor files;
- filenames containing `copy`, `old`, `backup`, `test`, `preview` or redundant version numbers;
- identical binary hashes;
- large unreferenced PNG, WebP and SVG files.

## Final state

- Production references preserved.
- Current Concepts artwork preserved.
- Superseded board assets removed from the published tree.
- Exact recovery state preserved on an intentional archive branch.
- Branch cleanup candidates classified by evidence.
- No Cloudflare configuration changed.
