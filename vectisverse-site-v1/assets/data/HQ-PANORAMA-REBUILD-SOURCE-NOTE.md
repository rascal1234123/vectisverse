# Riptide HQ Panorama Rebuild — Source Note

The earlier four-panel / panoramic presentation boards are visual-reference evidence only. They contain superseded internal-door relationships at Q2/Q3 and Q3/Q4 and therefore may not be used as production panorama sources.

The active reconstruction path is deterministic shared-scene rendering from:

- `assets/data/riptide-hq-geometry-master-v1.json` — authoritative topology, camera positions and orientation.
- The later locked orthographic / interior population masters — authoritative zone placement and open-transition relationships.
- Recovered Library scene/model data, including `riptide-hq-beta-scene.json` and the Blender block-out generator, used only where they agree with the later geometry lock.

The production branch now renders all five cameras from one Blender scene. Proxy materials and simplified furniture are geometry-validation devices only and cannot silently become release-final visual masters.