# RIPTIDE HQ — BUILD LEDGER

Version: 1.1
Status: ACTIVE

## 2026-08-08 — Autonomous directive reconciliation

### Baseline inspection
- Current production baseline set to `main`.
- `main` contains Pannellum 2.5.7 integration and the current five-node tour code.
- Older branch `riptide-hq-tour-gate-4-5` is behind `main` and is not the production baseline.
- Deterministic shared geometry master exists at `assets/data/riptide-hq-geometry-master-v1.json`.

### Authority reconciliation
- Five-node Gate 4.3/4.4 production route is authoritative over the older seven-node concept where they conflict.
- Locked topology confirmed: Q1/Q2 partition; Q2/Q3 open; Q3/Q4 open; one continuous Q2→Q3→Q4 environment; single Q4 seaward circular window; 0° seaward.

### Lowest failing layer
Current blocker is primarily Layer F/H (export/encoding and asset delivery), not Layer A/B/G:
- Pannellum is already integrated.
- Geometry/topology is already represented deterministically.
- Node 01 config references `node-01-production-beta.webp`.
- Nodes 02–05 config still references SVG beta stand-ins.
- Therefore the current build is not a final release candidate.

### Production-control files established
- `HQ-PRODUCTION-MANIFEST.md`
- `HQ-BUILD-RULES.md`
- `HQ-QA-CHECKLIST.md`
- `HQ-BUILD-LEDGER.md`

## 2026-08-08 — Continuation phase: recovery + client delivery

### Historical raster recovery investigation
- Git history confirms commit `c9b09000f21420a9abdf929057b3c589b9607f17` contained raster panorama assets for Nodes 02–05 under `assets/riptide/hq-tour/node-0X/node-0X-2560.webp`.
- Historical blob for Node 02 remains present in Git (`6fd90753456c5c8c5ef9f1c00a0dc2ac8ed31ee7`).
- Library QA / recovery reports also document prior 4096×2048 and 2048×1024 WebP exports for Nodes 02–05 and prior PASS seam/orientation results.
- Those historical assets are recovery evidence only. They are not automatically promoted to AUTHORITATIVE because the later deterministic shared-geometry correction superseded older scene implementations where they conflict.
- The current tool runtime can inspect historical Git blobs through the GitHub connector but cannot mount those binary blobs into the image-analysis runtime. Low-resolution report thumbnails are therefore explicitly rejected as substitutes for final panorama sources.

### Client delivery defect found and corrected
- Defect: current Pannellum loader used `n.image` unconditionally and ignored configured `n.mobile` assets.
- Layer: J / H (client delivery / asset selection), not design or geometry.
- Fix committed to `main`: `15ee1d65e15ff5433d6742efd73972c5e488aa1f`.
- Page cache bust + production-neutral metadata cleanup committed to `main`: `5f42a883d704ee697b2bfe803493313532f96a4b`.
- Result: below 760 px, the loader now uses a node's mobile asset when present; desktop continues to use the desktop source.

### Current regression state
PASS:
- Five-node config remains 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05.
- Pannellum remains the renderer.
- 0° = seaward convention unchanged.
- Locked geometry untouched.
- Desktop/mobile source-selection logic now behaves as configured.

BLOCKED:
- Final image-level QA for Nodes 02–05 cannot pass while current config points to SVG geometry stand-ins.
- Final production smoke test cannot be claimed until genuine final WebP panoramas are installed and deployed.

### Next autonomous production action
Recover or reconstruct genuine final 2:1 WebP panoramas from authoritative visual sources, install desktop/mobile variants, update config, then run panorama integrity, seam/orientation, forward/reverse navigation, responsive, iPhone Safari and deployment smoke regression.

### Escalation state
No creative approval gate is currently identified. The remaining blocker is technical asset availability / recoverability at Layer F/H.
