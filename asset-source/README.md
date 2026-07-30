# Validated website asset pipeline

This folder is the transport layer for PNG, JPEG and WebP files that cannot be sent reliably through a single connector payload.

## Standard deployment sequence

1. Create and locally validate the production image.
2. Give the output a new versioned filename, such as `riptide-home-teaser-v11.webp`.
3. Base64-encode the image and divide the text into small numbered files under an asset-specific folder.
4. Add one entry to `manifest.json` containing the output path, MIME type, exact byte count, SHA-256 checksum, dimensions and ordered chunk list.
5. Commit the chunks and manifest without changing the live HTML reference.
6. Cloudflare runs `node scripts/build-assets.mjs` through Wrangler before deployment.
7. The build fails if the payload is incomplete, corrupt, incorrectly named, outside the approved asset folder, or does not match its checksum and dimensions.
8. After the asset build succeeds, activate the new versioned filename in a separate commit.

## Manifest example

```json
{
  "version": 1,
  "assets": [
    {
      "id": "riptide-home-teaser-v11",
      "output": "vectisverse-site-v1/assets/riptide/riptide-home-teaser-v11.webp",
      "mimeType": "image/webp",
      "expectedBytes": 136440,
      "sha256": "replace-with-the-complete-sha256-value",
      "width": 960,
      "height": 640,
      "parts": [
        "riptide-home-teaser-v11/part-001.b64",
        "riptide-home-teaser-v11/part-002.b64"
      ]
    }
  ]
}
```

## Mandatory production rules

- Never overwrite an active image while testing a replacement.
- Never activate an asset in HTML before its reconstruction build succeeds.
- Every raster asset uses a new versioned filename.
- Chunks are plain Base64 text and are listed in exact reconstruction order.
- The expected byte count, SHA-256 and dimensions must come from the locally validated source file.
- SVG, HTML, CSS and JavaScript remain direct text-file deployments and do not use this pipeline.
