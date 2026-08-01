# VectisVerse Repository Audit — 1 August 2026

## Purpose

This is a read-only cleanup audit of `rascal1234123/vectisverse`. No assets, branches or production files were deleted or moved during this stage.

The audit follows these rules:

- `main` and `vectisverse-site-v1` are the only authorised production source.
- Production references take precedence over tidiness.
- Gold Masters and layered production sources are protected.
- Archive before delete.
- Uncertain files are retained.

## Audit limitations

The connected GitHub API does not currently expose a recursive repository-tree listing. The audit therefore combines:

- the current production HTML and dependency mapping;
- direct verification of named files on `main`;
- commit-history inspection;
- branch inventory;
- the existing source-of-truth and operations documents.

Binary-only files that were never referenced, committed with descriptive names, or exposed through inspected commits may require a second inventory pass before deletion.

## Protected production source

The following remain protected:

- `main`
- `vectisverse-site-v1/`
- all files referenced by current HTML, CSS or JavaScript;
- `_headers`, `robots.txt`, `sitemap.xml` and `404.html`;
- `.github/workflows/site-qa.yml`;
- `scripts/qa_static_site.py`;
- `README.md`, `SOURCE_OF_TRUTH.md` and `docs/WEBSITE_OPERATIONS.md`;
- current VectisVerse and Vectis Concepts logos;
- current homepage, Contact and Concepts assets;
- the four original featured layered SVG boards currently referenced by `concepts.html`;
- the ten finished featured PNG boards currently referenced by `concepts.html`.

## Confirmed archive batch: superseded Vectis Concepts production masters

The current Concepts page uses the ten finished UUID-named PNG boards. The following older layered SVG masters remain present on `main` but are no longer referenced by the production page:

- `vectisverse-site-v1/assets/featured/sports_club_identity_layered.svg`
- `vectisverse-site-v1/assets/featured/corporate_character_system_layered.svg`
- `vectisverse-site-v1/assets/featured/childrens_charity_layered.svg`
- `vectisverse-site-v1/assets/featured/heritage_brand_layered.svg`
- `vectisverse-site-v1/assets/featured/outdoor_brand_layered.svg`
- `vectisverse-site-v1/assets/featured/science_centre_layered.svg`
- `vectisverse-site-v1/assets/featured/educational_universe_layered.svg`
- `vectisverse-site-v1/assets/featured/esports_team_layered.svg`

Classification: **Historical production source / archive**.

Recommended action: move these eight SVG files, together with their explanatory `README.txt`, to a clearly labelled archive directory outside the published `vectisverse-site-v1` tree. Do not delete them.

Suggested destination:

`archive/vectis-concepts/featured-masters-2026-07-31/`

## Strong delete candidates after visual/hash confirmation

The same upload batch included matching PNG previews for the eight layered masters:

- `sports_club_identity.png`
- `corporate_character_system.png`
- `childrens_charity.png`
- `heritage_brand.png`
- `outdoor_brand.png`
- `science_centre.png`
- `educational_universe.png`
- `esports_team.png`

These previews are not referenced by the current Concepts page, which instead uses later finished PNG boards.

Classification: **Unreferenced generated exports**.

Recommended action: compare each preview against its layered SVG and the later finished board. Delete only where the preview is reproducible from the archived SVG and contains no unique artwork. Until that comparison is completed, retain them.

## Production directory documentation candidate

`vectisverse-site-v1/assets/featured/README.txt` describes the eight superseded SVG masters as suitable for the existing featured-card layout. That statement is now historically accurate but operationally outdated because those masters are no longer used by `concepts.html`.

Classification: **Archive with associated masters**.

Recommended action: move it with the eight SVG masters and add a short archive note identifying the replacement commit and current finished PNG boards.

## Branch audit

### Protected

- `main` — canonical production branch.

### Intentionally archived; retain for now

- `archive/concepts-release-candidate-2026-07-27`
- `vectis-concepts-production-v1`

The source-of-truth document explicitly identifies `vectis-concepts-production-v1` as an archived historical source. It must not be used for production.

### Likely cleanup candidates; compare before deletion

- `agent/vectisverse-version-fix`
- `backup/pre-clean-build-001`
- `backup-before-build-001-2026-07-26`
- `cloudflare/workers-autoconfig`
- `ftw-asset-upload`
- `site-consolidation-test`
- `stage3-tree-test`
- `stage3-tree-test2`
- `stage3-tree-test3`
- `stage3-tree-test4`
- `temp-ignore`

These names indicate temporary, backup, upload or test purposes. They are not authorised production branches. Before deletion, compare each branch with `main` and confirm it contains no unique Gold Master or production source that has not been consolidated.

Recommended branch policy after comparison:

- delete fully merged test and temporary branches;
- retain only one intentionally labelled archive branch where it contains unique historical value;
- avoid keeping multiple backup branches once their commits are reachable from `main` or a retained archive tag;
- never attach Cloudflare automatic deployments to any non-`main` branch.

## Commit-history findings

The repository has already removed several known obsolete assets, including old Concepts logo versions and early Contact hero versions. This is positive evidence that some historical clutter has already been addressed.

The history also contains many `Add files via upload` commits. Those commits are not defects, but their generic descriptions make later provenance and cleanup harder. Future asset commits should use descriptive names and identify whether files are production, master, preview or archive material.

## Recommended cleanup order

### Batch 1 — No-risk documentation and archive structure

1. Create `archive/vectis-concepts/featured-masters-2026-07-31/` outside the published site directory.
2. Move the eight superseded layered SVG masters and their README into that archive.
3. Add an archive manifest describing their replacement by the later finished PNG boards.
4. Run repository QA and confirm the production Concepts page is unchanged.

### Batch 2 — Preview export assessment

1. Compare the eight unreferenced PNG previews against their SVG masters and later finished PNG replacements.
2. Delete exact/reproducible previews only.
3. Retain any preview containing unique artwork or a useful approved state.
4. Commit the deletion as one reversible logical batch.

### Batch 3 — Branch cleanup

1. Compare each likely cleanup branch against `main`.
2. Record unique files or commits.
3. Preserve unique approved production sources in `main` or an intentional archive branch.
4. Delete fully merged test, temporary, upload and redundant backup branches.
5. Retain the two explicitly historical Concepts branches until the asset archive is fully verified.

### Batch 4 — Wider binary inventory

Perform a second pass for:

- ZIP archives;
- files named `copy`, `final`, `old`, `backup`, `test` or `preview`;
- numbered logo and hero revisions still present on `main`;
- duplicate binary hashes;
- unused large PNG, WebP and SVG files;
- `.DS_Store`, `Thumbs.db`, temporary and editor files.

This pass requires a complete recursive tree export or local clone and should not rely only on filename search.

## Current audit decision

No deletion is authorised by this report alone.

The safest immediate cleanup is to archive the eight superseded layered Concepts masters and their README outside the published directory. The eight matching PNG previews are probable deletion candidates, but require visual or hash confirmation first. Branch deletion should follow branch-by-branch comparison.
