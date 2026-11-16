(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('[data-theme-toggle]');
  const updateThemeLabel = () => themeButton?.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  updateThemeLabel();
  themeButton?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (_) {}
    updateThemeLabel();
  });
  const menu = document.querySelector('[data-menu]');
  document.querySelector('[data-menu-toggle]')?.addEventListener('click', (event) => {
    const open = menu.dataset.open !== 'true';
    menu.dataset.open = String(open);
    event.currentTarget.setAttribute('aria-expanded', String(open));
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu?.dataset.open === 'true') {
      menu.dataset.open = 'false';
      const button = document.querySelector('[data-menu-toggle]');
      button?.setAttribute('aria-expanded', 'false');
      button?.focus();
    }
  });
  const query = document.querySelector('#publication-search');
  const filters = [...document.querySelectorAll('[data-filter]')];
  let category = 'all';
  const filterPublications = () => {
    const terms = (query?.value || '').toLowerCase().trim().split(/\s+/).filter(Boolean);
    let visible = 0;
    document.querySelectorAll('[data-publication]').forEach((paper) => {
      const match = terms.every(term => paper.dataset.search.includes(term)) && (category === 'all' || paper.dataset.category === category);
      paper.hidden = !match;
      if (match) visible++;
    });
    document.querySelectorAll('.pub-group').forEach(group => { group.hidden = !group.querySelector('[data-publication]:not([hidden])'); });
    const count = document.querySelector('#results-count');
    if (count) count.textContent = `${visible} publication${visible === 1 ? '' : 's'}`;
    const empty = document.querySelector('#empty-results');
    if (empty) empty.hidden = visible !== 0;
  };
  query?.addEventListener('input', filterPublications);
  filters.forEach(button => button.addEventListener('click', () => {
    category = button.dataset.filter;
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    filterPublications();
  }));
  document.querySelectorAll('[data-demo]').forEach(button => button.addEventListener('click', () => {
    const image = button.querySelector('img');
    const playing = button.dataset.playing === 'true';
    image.src = playing ? image.dataset.poster : button.dataset.demo;
    button.dataset.playing = String(!playing);
    button.setAttribute('aria-label', `${playing ? 'Play' : 'Pause'} demonstration: ${image.alt}`);
    button.setAttribute('aria-pressed', String(!playing));
  }));
  document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
    const text = document.getElementById(button.dataset.copy)?.textContent || '';
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy BibTeX'; }, 1800);
    } catch (_) { button.textContent = 'Select and copy the citation above'; }
  }));
  document.querySelector('[data-print]')?.addEventListener('click', () => window.print());
})();
