(() => {
  const artefacts = window.RIPTIDE_ARTEFACTS || [];
  const maps = window.RIPTIDE_HOTSPOTS || {};
  const layer = document.querySelector('[data-hotspot-layer]');
  const dialog = document.querySelector('[data-artefact-dialog]');
  const desktopImage = document.querySelector('[data-hq-desktop]');
  const mobileSource = document.querySelector('[data-hq-mobile]');

  if (desktopImage && window.RIPTIDE_HQ_DESKTOP_PARTS) {
    desktopImage.src = `data:image/webp;base64,${window.RIPTIDE_HQ_DESKTOP_PARTS.join('')}`;
  }
  if (mobileSource && window.RIPTIDE_HQ_MOBILE_PARTS) {
    mobileSource.srcset = `data:image/webp;base64,${window.RIPTIDE_HQ_MOBILE_PARTS.join('')}`;
  }

  if (!layer || !dialog || !artefacts.length || !maps.desktop || !maps.mobile) return;

  const title = dialog.querySelector('[data-title]');
  const teaser = dialog.querySelector('[data-teaser]');
  const body = dialog.querySelector('[data-body]');
  const quote = dialog.querySelector('[data-quote]');
  const category = dialog.querySelector('[data-category]');
  const indexText = dialog.querySelector('[data-dialog-index]');
  const progress = document.querySelector('[data-progress]');
  const live = document.querySelector('[data-live]');
  const closeButton = dialog.querySelector('[data-close]');
  const previousButton = dialog.querySelector('[data-previous]');
  const nextButton = dialog.querySelector('[data-next]');
  const visited = new Set();
  let currentIndex = 0;
  let returnFocus = null;

  function hotspotStyle(id) {
    const d = maps.desktop.items[id];
    const m = maps.mobile.items[id];
    return `--dx:${d.x};--dy:${d.y};--dw:${d.width};--dh:${d.height};--mx:${m.x};--my:${m.y};--mw:${m.width};--mh:${m.height};`;
  }

  artefacts.forEach((item, index) => {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'hotspot';
    button.dataset.artefactId = item.id;
    button.dataset.visited = 'false';
    button.setAttribute('aria-label', item.ariaLabel);
    button.setAttribute('aria-haspopup', 'dialog');
    button.style.cssText = hotspotStyle(item.id);
    const label = document.createElement('span');
    label.className = 'hotspot-label';
    label.textContent = item.title;
    button.appendChild(label);
    button.addEventListener('click', () => openArtefact(index, button));
    layer.appendChild(button);
  });

  function updateProgress() {
    progress.textContent = `${visited.size} of ${artefacts.length} discovered`;
  }

  function renderArtefact(index) {
    currentIndex = (index + artefacts.length) % artefacts.length;
    const item = artefacts[currentIndex];
    title.textContent = item.title;
    teaser.textContent = item.teaser;
    body.textContent = item.body;
    quote.querySelector('p').textContent = `“${item.quote}”`;
    category.textContent = item.category;
    indexText.textContent = `${currentIndex + 1} / ${artefacts.length}`;
    visited.add(item.id);
    const hotspot = layer.querySelector(`[data-artefact-id="${CSS.escape(item.id)}"]`);
    if (hotspot) hotspot.dataset.visited = 'true';
    updateProgress();
    live.textContent = `${item.title} opened. ${visited.size} of ${artefacts.length} artefacts discovered.`;
  }

  function openArtefact(index, sourceButton) {
    returnFocus = sourceButton || document.activeElement;
    renderArtefact(index);
    if (!dialog.open) dialog.showModal();
    closeButton.focus();
  }

  function closeDialog() {
    if (dialog.open) dialog.close();
  }

  previousButton.addEventListener('click', () => renderArtefact(currentIndex - 1));
  nextButton.addEventListener('click', () => renderArtefact(currentIndex + 1));
  closeButton.addEventListener('click', closeDialog);
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    const inside = event.clientX >= rect.left && event.clientX <= rect.right && event.clientY >= rect.top && event.clientY <= rect.bottom;
    if (!inside) closeDialog();
  });
  dialog.addEventListener('close', () => {
    if (returnFocus && typeof returnFocus.focus === 'function') returnFocus.focus();
  });
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') { event.preventDefault(); renderArtefact(currentIndex - 1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); renderArtefact(currentIndex + 1); }
  });

  updateProgress();
})();
