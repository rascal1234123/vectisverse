# Riptide HQ native artwork verification

This directory contains the native high-resolution artwork candidates for the interactive Riptide HQ page.

Expected production files:

- `riptide-hq-desktop.webp` — 2560 × 1920
- `riptide-hq-mobile.webp` — 1440 × 2560

The isolated `/riptide-hq-image-test.html` page must pass before these files are connected to the live interactive page. The working `riptide-hq.html` implementation remains unchanged on this test branch.

Acceptance checks:

1. Both files decode in Safari and Chromium.
2. Natural dimensions match the expected values above.
3. Direct asset URLs load without visible alt text or a broken-image icon.
4. HTTP response is successful and uses `Content-Type: image/webp`.
5. Only after the image-only test passes should the interactive HQ page be updated on a separate integration branch.
