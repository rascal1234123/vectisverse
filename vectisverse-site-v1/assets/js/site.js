(() => {
  const refinementHref = 'assets/css/visual-refinements-v1.css?v=20260801-1';
  if (!document.querySelector(`link[href="${refinementHref}"]`)) {
    const refinementStyles = document.createElement('link');
    refinementStyles.rel = 'stylesheet';
    refinementStyles.href = refinementHref;
    document.head.appendChild(refinementStyles);
  }

  const comicsHref = 'assets/css/comics.css?v=20260803-1';
  if (!document.querySelector(`link[href="${comicsHref}"]`)) {
    const comicsStyles = document.createElement('link');
    comicsStyles.rel = 'stylesheet';
    comicsStyles.href = comicsHref;
    document.head.appendChild(comicsStyles);
  }

  const nav = document.querySelector('.site-nav');
  const toggle = document.querySelector('.menu-toggle');
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const comicTitles = [
    ['riptide.html', 'Riptide'],
    ['v-pop.html', 'V POP'],
    ['ftw.html', 'FTW'],
    ['dino-might.html', 'Dino-Might'],
    ['isle-of-night.html', 'Isle of Night']
  ];

  const addComicsMenu = menu => {
    if (!menu || menu.querySelector('.comics-menu')) return null;

    const wrapper = document.createElement('div');
    wrapper.className = 'comics-menu';

    const button = document.createElement('button');
    button.className = 'comics-menu-button';
    button.type = 'button';
    button.setAttribute('aria-expanded', 'false');
    button.setAttribute('aria-controls', 'comics-submenu');
    button.textContent = 'Our Comics';

    const submenu = document.createElement('div');
    submenu.id = 'comics-submenu';
    submenu.className = 'comics-submenu';

    comicTitles.forEach(([href, label]) => {
      const link = document.createElement('a');
      link.href = href;
      link.textContent = label;
      if (currentPage === href) {
        link.setAttribute('aria-current', 'page');
        wrapper.classList.add('has-current');
      }
      submenu.appendChild(link);
    });

    wrapper.append(button, submenu);
    const homeLink = menu.querySelector('a[href="index.html"]');
    if (homeLink) homeLink.insertAdjacentElement('afterend', wrapper);
    else menu.prepend(wrapper);

    const setOpen = open => {
      wrapper.classList.toggle('is-open', open);
      button.setAttribute('aria-expanded', String(open));
    };

    button.addEventListener('click', event => {
      event.stopPropagation();
      setOpen(button.getAttribute('aria-expanded') !== 'true');
    });

    submenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => setOpen(false));
    });

    document.addEventListener('pointerdown', event => {
      if (!wrapper.contains(event.target)) setOpen(false);
    });

    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        button.focus();
      }
    });

    return { wrapper, button, setOpen };
  };

  const comicsMenu = addComicsMenu(nav);

  if (!toggle || !nav) return;

  if (!nav.querySelector('.mobile-menu-social')) {
    const social = document.createElement('div');
    social.className = 'mobile-menu-social';
    social.setAttribute('aria-label', 'Social media');
    social.innerHTML = `
      <a href="https://www.instagram.com/vectisversecomics?igsh=b3VjM3c4OThxNmRk&utm_source=qr" target="_blank" rel="noopener noreferrer" aria-label="VectisVerse on Instagram">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 2h10a5 5 0 0 1 5 5v10a5 5 0 0 1-5 5H7a5 5 0 0 1-5-5V7a5 5 0 0 1 5-5Zm0 2a3 3 0 0 0-3 3v10a3 3 0 0 0 3 3h10a3 3 0 0 0 3-3V7a3 3 0 0 0-3-3H7Zm11.5 1.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5ZM12 7a5 5 0 1 1 0 10 5 5 0 0 1 0-10Zm0 2a3 3 0 1 0 0 6 3 3 0 0 0 0-6Z"/></svg>
      </a>
      <a href="https://www.facebook.com/share/1D2ZVtFuBp/?mibextid=wwXIfr" target="_blank" rel="noopener noreferrer" aria-label="VectisVerse on Facebook">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8h3V4.2c-.5-.1-2.2-.2-4.2-.2C8.7 4 6 6.5 6 7.1V10H3v4h3v8h4v-8h3.1l.9-4H10V7.5c0-1.2.3-2 2-2H14V8Z" transform="translate(2 0)"/></svg>
      </a>`;
    nav.appendChild(social);
  }

  const closeMenu = (returnFocus = false) => {
    nav.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
    if (comicsMenu) comicsMenu.setOpen(false);
    if (returnFocus) toggle.focus();
  };

  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    nav.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });

  nav.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => closeMenu());
  });

  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      closeMenu(true);
    }
  });

  document.addEventListener('pointerdown', event => {
    if (toggle.getAttribute('aria-expanded') === 'true' && !nav.contains(event.target) && !toggle.contains(event.target)) {
      closeMenu();
    }
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 700) closeMenu();
  });
})();
