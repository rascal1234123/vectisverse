(() => {
  const refinementHref = 'assets/css/concepts-visual-refinements-v1.css?v=20260801-1';
  if (!document.querySelector(`link[href="${refinementHref}"]`)) {
    const refinementStyles = document.createElement('link');
    refinementStyles.rel = 'stylesheet';
    refinementStyles.href = refinementHref;
    document.head.appendChild(refinementStyles);
  }

  const galleryImages = document.querySelectorAll('.cards .card-art img');
  galleryImages.forEach(image => {
    image.loading = 'lazy';
    image.decoding = 'async';

    const recordIntrinsicDimensions = () => {
      if (!image.hasAttribute('width') && image.naturalWidth > 0) {
        image.setAttribute('width', String(image.naturalWidth));
      }
      if (!image.hasAttribute('height') && image.naturalHeight > 0) {
        image.setAttribute('height', String(image.naturalHeight));
      }
    };

    if (image.complete) recordIntrinsicDimensions();
    else image.addEventListener('load', recordIntrinsicDimensions, { once: true });
  });

  const menuButton = document.querySelector('.concepts-menu-toggle');
  const menu = document.querySelector('.concepts-site-nav');

  if (menuButton && menu) {
    const closeMenu = (returnFocus = false) => {
      menuButton.setAttribute('aria-expanded', 'false');
      menu.classList.remove('is-open');
      if (returnFocus) menuButton.focus();
    };

    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') !== 'true';
      menuButton.setAttribute('aria-expanded', String(open));
      menu.classList.toggle('is-open', open);
    });

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => closeMenu());
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
        closeMenu(true);
      }
    });

    document.addEventListener('pointerdown', event => {
      if (menuButton.getAttribute('aria-expanded') === 'true' && !menu.contains(event.target) && !menuButton.contains(event.target)) {
        closeMenu();
      }
    });

    window.addEventListener('resize', () => {
      if (window.innerWidth > 700) closeMenu();
    });
  }

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce) return;

  const items = document.querySelectorAll('.service,.card,.why-list li');
  const io = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: .15 });

  items.forEach((element, index) => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(14px)';
    element.style.transition = `opacity .45s ease ${Math.min(index * 45, 280)}ms, transform .45s ease ${Math.min(index * 45, 280)}ms`;
    io.observe(element);
  });

  document.head.insertAdjacentHTML('beforeend', '<style>.is-visible{opacity:1!important;transform:none!important}</style>');
})();
