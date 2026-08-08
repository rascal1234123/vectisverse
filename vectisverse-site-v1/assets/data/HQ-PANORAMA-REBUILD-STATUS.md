# Riptide HQ Panorama Rebuild Status

Status: SHARED-SCENE GEOMETRY / TOPOLOGY PASS — VISUAL PRODUCTION TREATMENT NEXT

- Production branch: `riptide-hq-production-rebuild`.
- PR: #15 remains draft and cannot be promoted until release QA passes.
- The earlier image-resize reconstruction path has been rejected and removed because its source presentation imagery contains superseded internal-door relationships and is not a true authoritative shared scene.
- A deterministic Blender shared-scene renderer generates Nodes 01–05 from one coordinate system using the locked five camera positions.
- Geometry/topology gate passed on GitHub Actions production-rebuild run #16.
- Blender-native structural QA passed against the saved `.blend`: shell footprint 10.50 m × 24.00 m; corrected opposing roof pitches close at the ridge; Q1/Q2 full-height partition/gable exists; no Q2/Q3 or Q3/Q4 partition objects exist; exactly one seaward circular-window glass/frame assembly exists; all five equirectangular cameras are at their locked positions; Q2/Q3/Q4 prefixed content has no zone-boundary violations.
- Equirectangular image QA also passed for all five validation panoramas: exact 1024×512 2:1 output, zero extreme-blank ratio, healthy dynamic range and seam-edge MAE approximately 3.3–3.6.
- Visual inspection confirms the previously identified roof/wall void bands have been removed, the shell closes correctly, Q2→Q3→Q4 remains open, and the single Q4 seaward circular-window relationship is visually present.
- Current renders remain 1024×512 geometry-validation panoramas with proxy materials / simplified proxy objects. They are DERIVED VALIDATION assets only, not release-final visual masters.
- Next production gate: replace proxy surfaces and simplified objects with the approved visual production treatment without altering validated topology, camera positions, zone containment or the single-window relationship.
- Final render target remains 8192×4096 masters with 4096×2048 desktop and 2048×1024 mobile WebP derivatives, followed by Pannellum navigation, responsive/iPhone Safari and release QA.
