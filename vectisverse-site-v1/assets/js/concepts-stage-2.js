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
