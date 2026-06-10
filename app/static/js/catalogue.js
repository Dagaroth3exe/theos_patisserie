/**
 * Category filter for /products page.
 * Works across both the mobile scroll row and the desktop grouped rows.
 * Also positions the sticky filter bar just below the fixed navbar.
 */
document.addEventListener('DOMContentLoaded', () => {
  // ── Sticky bar: sit flush under the fixed navbar ────────────
  const nav       = document.getElementById('site-nav');
  const filterBar = document.getElementById('filter-bar');
  if (nav && filterBar) {
    const setTop = () => {
      filterBar.style.top = (nav.offsetTop + nav.offsetHeight) + 'px';
    };
    setTop();
    window.addEventListener('resize', setTop);
  }

  // ── Collect every chip across mobile + desktop layouts ───────
  const buttons        = document.querySelectorAll('.category-chip');
  if (!buttons.length) return;

  const cards          = document.querySelectorAll('.product-card[data-category]');
  const listItems      = document.querySelectorAll('.menu-list-item[data-category]');
  const sectionHeaders = document.querySelectorAll('[data-section-header]');
  const productGrids   = document.querySelectorAll('.product-grid');
  const noResults      = document.getElementById('no-results');
  const noResultsMobile = document.getElementById('no-results-mobile');

  function applyFilter(filter) {
    const isAll = filter === 'all';

    // Sync active state on ALL chips (mobile + desktop) with matching filter
    buttons.forEach(b => b.classList.toggle('active-chip', b.dataset.filter === filter));

    // Section headers only visible in All view
    sectionHeaders.forEach(h => { h.style.display = isAll ? '' : 'none'; });

    // Desktop cards
    let visibleCards = 0;
    cards.forEach(card => {
      const show = isAll || card.dataset.category === filter;
      card.style.display = show ? '' : 'none';
      if (show) visibleCards++;
    });

    // Collapse gap between grids when section header is hidden
    productGrids.forEach(grid => { grid.style.marginBottom = isAll ? '' : '0'; });

    // Mobile list items
    let visibleList = 0;
    listItems.forEach(item => {
      const show = isAll || item.dataset.category === filter;
      item.style.display = show ? '' : 'none';
      if (show) visibleList++;
    });

    if (noResults)       noResults.classList.toggle('hidden', visibleCards > 0);
    if (noResultsMobile) noResultsMobile.classList.toggle('hidden', visibleList > 0);
  }

  buttons.forEach(btn => btn.addEventListener('click', () => applyFilter(btn.dataset.filter)));

  // Initial state — honour ?cat= URL param
  const catParam = new URLSearchParams(window.location.search).get('cat');
  applyFilter(catParam || 'all');
});
