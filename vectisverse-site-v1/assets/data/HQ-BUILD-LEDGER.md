# RIPTIDE HQ — BUILD LEDGER

Version: 1.3
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

### Production-control files established
- `HQ-PRODUCTION-MANIFEST.md`
- `HQ-BUILD-RULES.md`
- `HQ-QA-CHECKLIST.md`
- `HQ-BUILD-LEDGER.md`

## 2026-08-08 — Recovery + client delivery

### Historical raster recovery investigation
- Git history confirms commit `c9b09000f21420a9abdf929057b3c589b9607f17` contained files named as raster panorama assets for Nodes 02–05.
- Exact historical blobs were reattached without modification on isolated branch `riptide-hq-recovery-staging`.
- Staging recovery commit: `d1cf16bfc2be7fec57cad665618b7c3596758a49`.
- Staging config wiring commit: `45f902ec0a5cf8f13bd100ced06444d324989b2e`.
- Draft PR #14 exists solely for repository-native binary QA and is not approved for merge.

### Binary QA result — historical recovery rejected
- VectisVerse Static QA: PASS.
- Riptide HQ Panorama QA: FAIL.
- Node 02: 14,997 bytes; non-image magic; decode FAIL.
- Node 03: 14,999 bytes; non-image magic; decode FAIL.
- Node 04: 14,997 bytes; non-image magic; decode FAIL.
- Node 05: 4,255 bytes; RIFF/WebP header present but decoder creation FAIL.
- All four historical raster blobs are CORRUPTED / INVALID FOR PRODUCTION and must never be promoted.

### Node 01 repository corruption found and mitigated
- Repository `assets/riptide-hq/node-01-production-beta.webp` was extracted through GitHub Actions and tested independently.
- It is only 15,009 bytes and fails WebP decoder creation.
- This means the prior `main` starting panorama was also corrupted at Layer F/H.
- Library production sources survive intact:
  - `node-01-q2-production-equirect-v2.webp` — 1,041,454 bytes, WEBP, 4096×2048, 2:1, decode PASS.
  - `node-01-q2-production-equirect-v2-mobile.webp` — 426,782 bytes, WEBP, 2048×1024, 2:1, decode PASS.
- Until the validated Library pair can be reintroduced as repository binaries, `main` has been restored to the valid shared-geometry Node 01 SVG fallback.
- Fallback config commit: `56c67002137273ef458865cf002350c6f003c997`.
- Cache-bust commit: `d4e5a3ac425f74f2f8543e09a5f849158229457c`.

### Client delivery defect found and corrected
- Defect: Pannellum loader ignored configured `mobile` assets.
- Fix: `15ee1d65e15ff5433d6742efd73972c5e488aa1f`.
- Page cache bust: `5f42a883d704ee697b2bfe803493313532f96a4b`.
- Result: viewport ≤760 px uses `mobile` when supplied; desktop uses `image`.

### Current regression state
PASS:
- Five-node config remains 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05.
- Pannellum remains the renderer.
- 0° = seaward convention unchanged.
- Locked geometry untouched.
- All five configured `main` assets are now geometry-valid SVG stand-ins rather than corrupt raster binaries.
- Historical recovery was tested safely without contaminating `main`.

BLOCKED:
- Final production raster assets are absent from the repository.
- Node 01 has valid production sources in the Library but requires safe binary reintroduction.
- Nodes 02–05 require genuine reconstruction from authoritative geometry plus approved visual masters; historical Git rasters are unusable.
- Final release, browser QA and deployment smoke test remain blocked until that final raster set exists.

### Next autonomous production action
Reconstruct / reintroduce genuine 2:1 production panoramas, generate desktop/mobile WebP derivatives, then run decode, dimensions, seam/orientation, visual continuity, Pannellum, navigation, responsive, iPhone Safari and deployment smoke QA before promotion.

### Escalation state
No creative approval gate is currently identified. The remaining blocker is Layer E/F production rendering and safe binary delivery, not repository permissions, Pannellum, navigation or approved design.
