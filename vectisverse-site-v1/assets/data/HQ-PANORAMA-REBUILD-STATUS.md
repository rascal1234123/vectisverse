# Riptide HQ Panorama Rebuild Status

Status: SHARED-SCENE GEOMETRY VALIDATION IN PROGRESS

- Production branch: `riptide-hq-production-rebuild`.
- PR: #15 remains draft and cannot be promoted until release QA passes.
- The earlier image-resize reconstruction path has been rejected and removed because its source presentation imagery contains superseded internal-door relationships and is not a true authoritative shared scene.
- A deterministic Blender shared-scene renderer now generates Nodes 01–05 from one coordinate system using the locked five camera positions.
- The generated validation scene preserves Q1/Q2 partitioning, Q2/Q3 open transition, Q3/Q4 open transition, Q2/Q3/Q4 content containment and one Q4 seaward circular-window relationship.
- Current renders are 1024×512 geometry-validation panoramas with proxy materials. They are DERIVED VALIDATION assets only, not release-final visual masters.
- Repository-native QA checks decode, 2:1 dimensions, nonblank content, seam metrics and presence of the inspectable `.blend` scene.
- Next automatic gate after geometry validation PASS: replace proxy surfaces / objects with approved visual production treatment without altering scene topology, then render 8192×4096 masters and 4096×2048 / 2048×1024 WebP derivatives.