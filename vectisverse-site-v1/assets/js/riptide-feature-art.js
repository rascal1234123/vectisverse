(() => {
  const image = document.querySelector('[data-riptide-feature-art]');
  const frame = image?.closest('[data-riptide-feature-frame]');
  if (!image || !frame) return;

  // The 900 × 1125 WebP was uploaded in ten base64 chunks. The first four
  // retained the original "hd" filename, while chunks five to ten were
  // inadvertently given an "avif" filename even though they are continuations
  // of the same WebP file. Load the complete sequence before using the smaller
  // 400 × 500 WebP as a true fallback.
  const hdWebpChunkUrls = [
    ...Array.from(
      { length: 4 },
      (_, index) => `assets/riptide/riptide-kraken-hd-${String(index + 1).padStart(2, '0')}.b64?v=20260803-2`
    ),
    ...Array.from(
      { length: 6 },
      (_, index) => `assets/riptide/riptide-kraken-avif-${String(index + 5).padStart(2, '0')}.b64?v=20260803-2`
    )
  ];

  const fallbackWebpChunkUrls = [
    'assets/riptide/riptide-kraken-01.b64?v=20260803-2',
    'assets/riptide/riptide-kraken-02.b64?v=20260803-2',
    'assets/riptide/riptide-kraken-03.b64?v=20260803-2'
  ];

  const createArtworkUrl = async (urls, type) => {
    const chunks = await Promise.all(urls.map(async (url) => {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Unable to load artwork data: ${url}`);
      }
      return response.text();
    }));

    const binary = atob(chunks.join('').replace(/\s+/g, ''));
    const bytes = Uint8Array.from(binary, character => character.charCodeAt(0));
    return URL.createObjectURL(new Blob([bytes], { type }));
  };

  const showImage = objectUrl => new Promise((resolve, reject) => {
    image.onload = () => {
      image.onload = null;
      image.onerror = null;
      image.hidden = false;
      requestAnimationFrame(() => image.classList.add('is-loaded'));
      URL.revokeObjectURL(objectUrl);
      resolve();
    };

    image.onerror = () => {
      image.onload = null;
      image.onerror = null;
      URL.revokeObjectURL(objectUrl);
      reject(new Error('The browser could not decode the artwork.'));
    };

    image.src = objectUrl;
  });

  const loadArtwork = async () => {
    try {
      const hdWebpUrl = await createArtworkUrl(hdWebpChunkUrls, 'image/webp');
      await showImage(hdWebpUrl);
    } catch (hdError) {
      console.warn('High-resolution artwork unavailable; using the smaller WebP fallback.', hdError);
      const fallbackWebpUrl = await createArtworkUrl(fallbackWebpChunkUrls, 'image/webp');
      await showImage(fallbackWebpUrl);
    }
  };

  loadArtwork().catch((error) => {
    frame.classList.add('has-error');
    console.error('Unable to load the Riptide feature artwork.', error);
  });
})();
