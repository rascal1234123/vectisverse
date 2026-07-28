(() => {
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
