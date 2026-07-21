VECTISVERSE WEBSITE GOLD MASTER v1.0 — UPDATE PACKAGE
=======================================================

This package is designed to be MERGED into the existing GitHub folder:

    vectisverse-site-v1/

It deliberately reuses the approved layered Riptide, V, FTW, Shop, Concepts and
VectisVerse brand assets already present in that folder.

WHAT TO UPLOAD
--------------
Upload the CONTENTS of this ZIP into vectisverse-site-v1 and allow GitHub to
replace index.html and concepts.html.

New files:
- css/goldmaster.css
- js/site.js
- assets/brand/hero-composite-reference.jpg

Existing required asset folders (already in the repository):
- assets/brand/
- assets/riptide/
- assets/v/
- assets/ftw/
- assets/shop/
- assets/concepts/

IMPORTANT
---------
Do not delete the existing assets folders before merging this update package.
This is intentionally an update package rather than a complete duplicate of all
existing binary artwork, because the approved production artwork is already in
the repository.

Cloudflare remains configured with:
- Production branch: main
- Root directory: vectisverse-site-v1
- Build command: exit 0
- Output directory: .

After committing, confirm Cloudflare deploys the newest Git commit and review the
deployment-specific pages.dev address first.
