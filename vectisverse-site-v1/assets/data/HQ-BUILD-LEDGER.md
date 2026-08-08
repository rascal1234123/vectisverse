# RIPTIDE HQ — BUILD LEDGER

Version: 1.0
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

### Next autonomous production action
Replace beta/stand-in panorama assets with final 2:1 equirectangular WebP delivery assets derived from the authoritative shared environment, then update config, run panorama integrity QA, Pannellum functional regression, browser regression and production smoke tests.

### Escalation state
No creative approval gate is currently identified. Production remains technically blocked only by creation/availability and verification of the final panorama render set.