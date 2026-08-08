# RIPTIDE HQ — PRODUCTION MANIFEST

Version: 1.1
Status: ACTIVE
Production baseline: `main`

## Authority hierarchy

### AUTHORITATIVE
- `assets/data/riptide-hq-geometry-master-v1.json` — deterministic shared-environment topology, zone rules, coordinate system, camera nodes and orientation.
- Gate 4.3 panorama production rules: five-node sequence 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05; 2:1 equirectangular delivery; 0° = seaward.
- Gate 4.4.2 navigation UI visual master: restrained forward/back floor-positioned movement, Q2/Q3/Q4 location indication, Return to Start, Exit Tour, drag/touch look-around, limited zoom, keyboard support and reduced-motion crossfade.
- Approved production design masters for Q2 Team Area, Q3 Training Area and Q4 Briefing Area.

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

### RECOVERY REFERENCE — NOT FINAL AUTHORITY
- Historical commit `c9b09000f21420a9abdf929057b3c589b9607f17` contains raster Node 02–05 panorama assets from the earlier Gate 4.5 implementation.
- Historical Node 02 raster blob confirmed intact as Git blob `6fd90753456c5c8c5ef9f1c00a0dc2ac8ed31ee7`.
- Library panorama QA / delivery reports document prior 4096×2048 and 2048×1024 WebP exports and seam/orientation PASS results.
- These sources may be used for recovery comparison, but may not override the later shared-geometry master or be promoted directly to release-final without current geometry / visual QA.

### OBSOLETE / EXPERIMENTAL
- Branch `riptide-hq-tour-gate-4-5` as a production baseline; it is behind current `main` and uses an earlier custom WebGL viewer and mixed 1024/2560 assets.
- `hq-node-02-beta.svg` through `hq-node-05-beta.svg` as final panorama assets. They are geometry-validation stand-ins only.
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

## Release blockers at v1.1
1. Node 01 remains production-beta rather than release-final.
2. Nodes 02–05 remain SVG beta geometry stand-ins in current configuration and do not meet the final WebP 2:1 panorama requirement.
3. Historical raster assets are recoverable references but require validation against the later shared-geometry lock before reuse.
4. Full cross-browser and iPhone Safari release QA must be rerun against the final WebP asset set.
5. Production smoke test must be run after final assets and config are deployed.
