# RIPTIDE HQ — BUILD RULES

Version: 1.0
Status: ACTIVE

## Execution loop
BUILD → INSPECT → TEST → PASS? → REGRESSION TEST → NEXT STAGE.
On failure: DIAGNOSE → CORRECT LOWEST FAILING LAYER → REBUILD → RETEST.

## Lowest-failing-layer order
A Approved design
B Geometry
C Materials / objects
D Camera
E Renderer
F Export / encoding
G Pannellum
H Asset delivery
I Deployment / cache
J Client browser

Never alter a higher layer to conceal a lower-layer fault.

## Shared environment
- Q2, Q3 and Q4 are one deterministic environment.
- Nodes 01–05 are camera positions, not independently invented rooms.
- Camera path: 01 ⇄ 02 ⇄ 03 ⇄ 04 ⇄ 05.
- 0° = seaward; 180° = landward.
- Node transitions must preserve spatial orientation unless a deliberate transition heading is defined by an authoritative master.

## Panorama production
- Final source projection: equirectangular 2:1.
- Archive target: 8192×4096 WebP where source quality supports it.
- Desktop target: 4096×2048 WebP.
- Mobile target: 2048×1024 WebP.
- No duplicated horizontal strips, blank hemispheres, upside-down projection, seam discontinuities, accidental geometry or non-authoritative object changes.
- Derived files must never be promoted to design authority merely because they are newer.

## Viewer
- Pannellum is the production viewer unless explicitly reopened by the user.
- Preserve pitch limits -55° to +55° and limited zoom unless an authoritative UI master supersedes them.
- Preserve drag/touch look-around, keyboard navigation, Return to Start, Exit Tour and reduced-motion behaviour.
- Navigation controls must remain visually restrained and spatially located.

## Browser / delivery
- Desktop: current supported Safari, Chrome, Edge and Firefox.
- Mobile release gate includes current iPhone Safari.
- Asset failures must be diagnosed at export/encoding, delivery/cache or browser layers before any scene/design intervention.
- Cache-busting must change only when the referenced asset/config actually changes.

## Change control
Routine technical corrections are pre-approved. Escalation is required only when a proposed fix would change a locked creative/design decision or when authoritative sources materially conflict and cannot be reconciled by chronology/scope.