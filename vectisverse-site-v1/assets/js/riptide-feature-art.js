(() => {
  const image = document.querySelector('[data-riptide-feature-art]');
  const frame = image?.closest('[data-riptide-feature-frame]');
  if (!image || !frame) return;

  const chunkUrls = [
    'assets/riptide/riptide-kraken-01.b64?v=20260803-1',
    'assets/riptide/riptide-kraken-02.b64?v=20260803-1',
    'assets/riptide/riptide-kraken-03.b64?v=20260803-1'
  ];

  Promise.all(chunkUrls.map((url) => fetch(url).then((response) => {
    if (!response.ok) {
      throw new Error(`Unable to load artwork data: ${url}`);
    }
    return response.text();
  })))
    .then((chunks) => {
      const binary = atob(chunks.join('').replace(/\s+/g, ''));
      const bytes = new Uint8Array(binary.length);

      for (let index = 0; index < binary.length; index += 1) {
        bytes[index] = binary.charCodeAt(index);
      }

      const objectUrl = URL.createObjectURL(new Blob([bytes], { type: 'image/webp' }));

      image.addEventListener('load', () => {
        image.hidden = false;
        requestAnimationFrame(() => image.classList.add('is-loaded'));
        URL.revokeObjectURL(objectUrl);
      }, { once: true });

      image.src = objectUrl;
    })
    .catch((error) => {
      frame.classList.add('has-error');
      console.error('Unable to load the Riptide feature artwork.', error);
    });
})();
