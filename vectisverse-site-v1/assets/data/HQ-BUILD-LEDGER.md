# RIPTIDE HQ — BUILD LEDGER

Version: 1.2
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
- Git history confirms commit `c9b09000f21420a9abdf929057b3c589b9607f17` contained files named as raster panorama assets for Nodes 02–05 under `assets/riptide/hq-tour/node-0X/node-0X-2560.webp`.
- Exact historical blobs were reattached without modification on isolated branch `riptide-hq-recovery-staging`.
- Staging recovery commit: `d1cf16bfc2be7fec57cad665618b7c3596758a49`.
- Staging config wiring commit: `45f902ec0a5cf8f13bd100ced06444d324989b2e`.
- Draft PR #14 was created solely to run repository-native binary QA; it is not approved for merge.

### Binary QA result — historical recovery rejected
- VectisVerse Static QA: PASS.
- Riptide HQ Panorama QA: FAIL.
- Nodes 02, 03 and 04 cannot be identified by Pillow as image files.
- Node 05 presents as a WebP/RIFF-type object but the decoder cannot create a decoder object.
- Therefore all four historical raster blobs are classified CORRUPTED / INVALID FOR PRODUCTION.
- They must never be promoted, renamed as final assets, or used as visual masters.

### Surviving raw production asset inventory
- Library inventory confirms the surviving Node 01 production pair exists as raw WebPs:
  - `node-01-q2-production-equirect-v2.webp`
  - `node-01-q2-production-equirect-v2-mobile.webp`
- No corresponding raw Node 02–05 WebP delivery files are present in the Library inventory.
- Approved QA / panorama boards survive for Nodes 02–05 and document the intended visual result, orientation and seam metrics, but those boards are reference material rather than the original 8192×4096 sources.

### Client delivery defect found and corrected
- Defect: current Pannellum loader used `n.image` unconditionally and ignored configured `n.mobile` assets.
- Layer: J / H (client delivery / asset selection), not design or geometry.
- Fix committed to `main`: `15ee1d65e15ff5433d6742efd73972c5e488aa1f`.
- Page cache bust committed to `main`: `5f42a883d704ee697b2bfe803493313532f96a4b`.
- Result: below 760 px, the loader now uses a node's mobile asset when present; desktop continues to use the desktop source.

### Current regression state
PASS:
- Five-node config remains 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05.
- Pannellum remains the renderer.
- 0° = seaward convention unchanged.
- Locked geometry untouched.
- Desktop/mobile source-selection logic now behaves as configured.
- Historical recovery was tested safely without modifying `main`.

BLOCKED:
- Historical Node 02–05 binaries are invalid and cannot be reused.
- Final production panoramas for Nodes 02–05 must therefore be reconstructed from authoritative geometry plus approved visual masters.
- Final production smoke test cannot be claimed until genuine final WebP panoramas are installed and deployed.

### Next autonomous production action
Reconstruct Nodes 02–05 as genuine 2:1 equirectangular production panoramas from the locked shared environment and approved visual masters; create desktop/mobile WebP derivatives; run binary decode, dimensions, seam/orientation, visual continuity, Pannellum, forward/reverse navigation, responsive, iPhone Safari and deployment smoke QA before promotion to `main`.

### Escalation state
No creative approval gate is currently identified. The remaining blocker is production rendering/reconstruction at Layer E/F, not repository access, navigation, Pannellum, or approved design.
