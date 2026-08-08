# RIPTIDE HQ — PANORAMA REBUILD SPECIFICATION

Version: 1.0
Status: ACTIVE — PRODUCTION REBUILD
Branch: `riptide-hq-production-rebuild`

## Purpose
Reconstruct the final five-node panorama delivery set from the locked deterministic shared-environment master and approved Q2/Q3/Q4 visual masters. This specification does not reopen creative design.

## Locked scene
- One continuous Q2 → Q3 → Q4 longitudinal environment.
- Q1/Q2 full-height partition/access relationship retained.
- Q2/Q3 OPEN: no wall, no door.
- Q3/Q4 OPEN: no wall, no door.
- Q3 equipment contained entirely within Q3.
- Q4 briefing configuration contained entirely within Q4.
- Exactly one circular seaward window at Q4 termination.
- 0° yaw = seaward/+z.
- Camera eye height = 1.675 m.

## Cameras
- Node 01: x=0.0, z=0.50 — Q2 Team Area centre.
- Node 02: x=0.0, z=1.00 — Q2/Q3 open threshold.
- Node 03: x=0.0, z=1.50 — Q3 Training Area centre.
- Node 04: x=0.0, z=2.00 — Q3/Q4 open threshold.
- Node 05: x=0.0, z=2.50 — Q4 Briefing Area centre.

## Visual content constraints
Q2 must contain two opposed L-shaped sofas, round coffee table, lower-wall kitchen, upper-wall exterior entrance, Q1 access door and open view into Q3. No gym or Q4 objects.

Q3 must contain the approved training equipment set: Smith machine/power rack, adjustable bench, barbell/plate storage, dumbbell rack, kettlebell rack, medicine/slam-ball rack, resistance bands, plyometric boxes and rubber training tiles. No Q2 lounge or Q4 briefing furniture.

Q4 must contain the approved Riptide shield-shaped briefing table, approximately eight chairs, clear circulation, technology/display wall, approved bookshelf and one very large circular seaward window. No gym equipment and no duplicate circular window.

## Render contract
Every node is rendered from the same deterministic scene. No panorama may be independently redrawn in a way that changes architecture or object placement.

Master render target: 8192×4096, 2:1 equirectangular, full 360°×180°, horizon level, no blank hemisphere, no duplicated strip, no text labels baked into production imagery.

Delivery derivatives:
- Desktop: 4096×2048 WebP.
- Mobile: 2048×1024 WebP.
- WebP must decode successfully and retain exact 2:1 dimensions.

## Orientation contract
- Image horizontal centre / initial yaw 0° = seaward.
- +90° = upper wall/+x.
- 180° = landward/-z.
- 270° = lower wall/-x.
- Node-to-node orientation must not rotate between renders.

## QA gates
1. Binary decode PASS.
2. Exact 2:1 dimensions PASS.
3. Full-frame content / no blank hemisphere PASS.
4. Left/right equirectangular seam continuity PASS.
5. Horizon/orientation PASS.
6. Shared-environment architectural continuity PASS.
7. Q2/Q3 and Q3/Q4 openness PASS.
8. Zone-content containment PASS.
9. Single Q4 circular window PASS.
10. Pannellum desktop/mobile loading PASS.
11. Navigation 01→02→03→04→05 and reverse PASS.
12. Responsive/iPhone Safari regression PASS before promotion.

## Prohibited sources
The historical Node 02–05 blobs from commit `c9b09000f21420a9abdf929057b3c589b9607f17` are corrupted and prohibited from production. The repository's former Node 01 `node-01-production-beta.webp` is also corrupt and prohibited. SVG beta panoramas may be used only as topology/geometry validation references, never as final visual masters.
