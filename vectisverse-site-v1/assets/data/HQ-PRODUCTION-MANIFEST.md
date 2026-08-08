# RIPTIDE HQ — PRODUCTION MANIFEST

Version: 1.2
Status: ACTIVE
Production baseline: `main`

## Authority hierarchy

### AUTHORITATIVE
- `assets/data/riptide-hq-geometry-master-v1.json` — deterministic shared-environment topology, zone rules, coordinate system, camera nodes and orientation.
- Gate 4.3 panorama production rules: five-node sequence 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05; 2:1 equirectangular delivery; 0° = seaward.
- Gate 4.4.2 navigation UI visual master: restrained forward/back floor-positioned movement, Q2/Q3/Q4 location indication, Return to Start, Exit Tour, drag/touch look-around, limited zoom, keyboard support and reduced-motion crossfade.
- Approved production design masters for Q2 Team Area, Q3 Training Area and Q4 Briefing Area.
- Approved Node 02–05 panorama QA / reconstruction boards as visual-reference evidence only; they document the intended viewpoints, spatial relationships, orientation and accepted seam results but are not substitutes for raw delivery masters.

### DERIVED
- Delivery panoramas rendered from the authoritative shared environment.
- Desktop/mobile WebP derivatives.
- Pannellum configuration and cache-busted deployment references.

### DEPLOYED / CURRENT TECHNICAL BASELINE
- `riptide-hq-tour.html`
- `assets/js/riptide-hq-tour.js`
- `assets/js/riptide-hq-tour-config.js`
- Pannellum 2.5.7 integration.
- Responsive panorama selection: desktop uses `image`; viewport ≤760 px uses `mobile` when supplied.

### SURVIVING RAW PRODUCTION ASSETS
- Library: `node-01-q2-production-equirect-v2.webp` — Node 01 desktop production equirectangular.
- Library: `node-01-q2-production-equirect-v2-mobile.webp` — Node 01 mobile production equirectangular.

### CORRUPTED / INVALID — PROHIBITED FROM PROMOTION
Historical files from commit `c9b09000f21420a9abdf929057b3c589b9607f17` that were named as Node 02–05 WebPs have been binary-tested in GitHub Actions and rejected:
- Node 02 historical blob `6fd90753456c5c8c5ef9f1c00a0dc2ac8ed31ee7` — decode FAIL.
- Node 03 historical blob `e09a7b462930fa40b72b6b2248d67383fed29379` — decode FAIL.
- Node 04 historical blob `9807dd3f2402c6f6bc6be373270597a7a4080606` — decode FAIL.
- Node 05 historical blob `6739b102e69da0a9cf3e7a469e257544a231110b` — decoder creation FAIL.
- These objects are recovery evidence only and must never be used as final, authoritative, or deployed panorama assets.

### OBSOLETE / EXPERIMENTAL
- Branch `riptide-hq-tour-gate-4-5` as a production baseline; it is behind current `main` and uses an earlier custom WebGL viewer and mixed assets.
- `hq-node-02-beta.svg` through `hq-node-05-beta.svg` as final panorama assets. They are geometry-validation stand-ins only.
- `riptide-hq-recovery-staging` and draft PR #14 are technical recovery/QA scaffolding only; no recovered historical raster from that branch is approved for production.
- Earlier seven-node virtual-tour concept material where it conflicts with the later five-node production route.
- Any derivative render that has not passed the current QA checklist.

## Locked topology
- Q1/Q2: full-height partition/access relationship retained.
- Q2→Q3: open transition; no invented wall or door.
- Q3→Q4: open transition; no invented wall or door.
- Q2→Q3→Q4: one continuous longitudinal environment.
- Q3 equipment remains inside Q3.
- Q4 briefing configuration remains inside Q4.
- Exactly one circular seaward window at the Q4 termination.
- Nodes 01–05 share one coordinate system.
- Camera eye height: 1.675 m unless an authoritative master supersedes it.
- 0° yaw = seaward.

## Release blockers at v1.2
1. Node 01 remains production-beta in repository configuration and requires final asset-path normalization against the surviving production pair.
2. Nodes 02–05 remain SVG beta geometry stand-ins in current `main` configuration.
3. Historical Node 02–05 raster recovery has definitively failed binary decode QA and is closed as a production route.
4. Nodes 02–05 must be reconstructed from authoritative geometry plus approved visual-reference masters and exported as genuine 2:1 WebPs.
5. Full cross-browser and iPhone Safari release QA must be rerun against that final WebP asset set.
6. Production smoke test must be run after final assets and config are deployed.
