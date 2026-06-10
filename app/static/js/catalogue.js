/**
 * Category filter for /products page.
 * Filters both the mobile list items and the desktop card grid.
 * Also positions the sticky filter bar just below the fixed navbar.
 */
document.addEventListener('DOMContentLoaded', () => {
  // ── Sticky bar: sit flush under the fixed navbar ────────────
  const nav     = document.getElementById('site-nav');
  const filterBar = document.getElementById('filter-bar');
  if (nav && filterBar) {
    const setTop = () => {
      filterBar.style.top = (nav.offsetTop + nav.offsetHeight) + 'px';
    };
    setTop();
    window.addEventListener('resize', setTop);
  }

  // ── Filter logic ─────────────────────────────────────────────
  const filterContainer = document.getElementById('category-filters');
  if (!filterContainer) return;

  const buttons         = filterContainer.querySelectorAll('.category-chip');
  const cards           = document.querySelectorAll('.product-card[data-category]');
  const listItems       = document.querySelectorAll('.menu-list-item[data-category]');
  const noResults       = document.getElementById('no-results');
  const noResultsMobile = document.getElementById('no-results-mobile');

  function setActive(btn) {
    buttons.forEach(b => b.classList.remove('active-chip'));
    btn.classList.add('active-chip');
  }

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      setActive(btn);

      // Desktop cards
      let visibleCards = 0;
      cards.forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        card.style.display = show ? '' : 'none';
        if (show) visibleCards++;
      });

      // Mobile list items
      let visibleList = 0;
      listItems.forEach(item => {
        const show = filter === 'all' || item.dataset.category === filter;
        item.style.display = show ? '' : 'none';
        if (show) visibleList++;
      });

      if (noResults)       noResults.classList.toggle('hidden', visibleCards > 0);
      if (noResultsMobile) noResultsMobile.classList.toggle('hidden', visibleList > 0);
    });
  });

  // Activate "All" on load
  const allBtn = filterContainer.querySelector('[data-filter="all"]');
  if (allBtn) setActive(allBtn);

  // Handle ?cat= URL param
  const catParam = new URLSearchParams(window.location.search).get('cat');
  if (catParam) {
    const matchBtn = [...buttons].find(b => b.dataset.filter === catParam);
    if (matchBtn) matchBtn.click();
  }
});
