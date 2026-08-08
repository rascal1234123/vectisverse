# Riptide HQ Panorama Rebuild Status

Status: AUTOMATED REBUILD PIPELINE READY

- Production branch: `riptide-hq-production-rebuild`
- PR: #15
- Approved four-panel Node 02–05 visual-reference payload stored as base64 rebuild source.
- Deterministic rebuild script added at `tools/rebuild_hq_panoramas.py`.
- Repository-native workflow added at `.github/workflows/riptide-hq-production-rebuild.yml`.
- Workflow reconstructs Nodes 02–05, removes presentation labels only, normalises panorama seam edges, exports 4096×2048 and 2048×1024 WebP derivatives, validates decode/dimensions/format, and uploads the resulting binaries as a GitHub Actions artifact.
- Generated assets remain DERIVED until QA passes and are not automatically promoted to `main`.
