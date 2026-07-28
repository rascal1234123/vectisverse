(() => {
  const menuButton = document.querySelector('.concepts-menu-toggle');
  const menu = document.querySelector('.concepts-site-nav');

  if (menuButton && menu) {
    menuButton.addEventListener('click', () => {
      const open = menuButton.getAttribute('aria-expanded') === 'true';
      menuButton.setAttribute('aria-expanded', String(!open));
      menu.classList.toggle('is-open', !open);
    });

    menu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        menuButton.setAttribute('aria-expanded', 'false');
        menu.classList.remove('is-open');
      });
    });
  }

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !('IntersectionObserver' in window)) return;

  const items = document.querySelectorAll('.service,.card,.why-list li');
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('is-visible');
      observer.unobserve(entry.target);
    });
  }, { threshold: 0.12 });

  items.forEach((element, index) => {
    element.style.opacity = '0';
    element.style.transform = 'translateY(14px)';
    element.style.transition = `opacity .45s ease ${Math.min(index * 40, 260)}ms, transform .45s ease ${Math.min(index * 40, 260)}ms`;
    observer.observe(element);
  });

  document.head.insertAdjacentHTML('beforeend', '<style>.is-visible{opacity:1!important;transform:none!important}</style>');
})();
