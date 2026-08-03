(() => {
  const image = document.getElementById('riptide-title-hero');
  const chunks = window.__RIPTIDE_HERO_CHUNKS;

  if (!image || !Array.isArray(chunks) || chunks.length !== 6) return;

  try {
    const binary = atob(chunks.join(''));
    const bytes = new Uint8Array(binary.length);

    for (let index = 0; index < binary.length; index += 1) {
      bytes[index] = binary.charCodeAt(index);
    }

    const objectUrl = URL.createObjectURL(new Blob([bytes], { type: 'image/avif' }));
    image.addEventListener('load', () => {
      URL.revokeObjectURL(objectUrl);
      delete window.__RIPTIDE_HERO_CHUNKS;
    }, { once: true });
    image.src = objectUrl;
  } catch (error) {
    console.error('Unable to load the Riptide title artwork.', error);
  }
})();
