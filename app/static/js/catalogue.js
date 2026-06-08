/**
 * Category filter for /products page.
 * Reads data-category attribute on each .product-card and
 * shows/hides based on the clicked filter button.
 */
document.addEventListener('DOMContentLoaded', () => {
  const filterContainer = document.getElementById('category-filters');
  if (!filterContainer) return;

  const buttons = filterContainer.querySelectorAll('.category-filter-btn');
  const cards = document.querySelectorAll('.product-card[data-category]');
  const noResults = document.getElementById('no-results');

  // Apply active style
  const ACTIVE_BG = '#2b1d1a';
  const ACTIVE_TEXT = '#fffdfa';
  const ACTIVE_BORDER = '#2b1d1a';

  function setActive(btn) {
    buttons.forEach(b => {
      b.style.backgroundColor = '';
      b.style.color = '';
      b.style.borderColor = '';
    });
    btn.style.backgroundColor = ACTIVE_BG;
    btn.style.color = ACTIVE_TEXT;
    btn.style.borderColor = ACTIVE_BORDER;
  }

  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      const filter = btn.dataset.filter;
      setActive(btn);

      let visibleCount = 0;
      cards.forEach(card => {
        const show = filter === 'all' || card.dataset.category === filter;
        if (show) {
          card.style.display = '';
          card.style.opacity = '1';
          visibleCount++;
        } else {
          card.style.display = 'none';
        }
      });

      if (noResults) {
        noResults.classList.toggle('hidden', visibleCount > 0);
      }
    });
  });

  // Apply active style to "All" button on load
  const allBtn = filterContainer.querySelector('[data-filter="all"]');
  if (allBtn) setActive(allBtn);

  // Handle ?cat= URL param on page load
  const params = new URLSearchParams(window.location.search);
  const catParam = params.get('cat');
  if (catParam) {
    const matchBtn = [...buttons].find(b => b.dataset.filter === catParam);
    if (matchBtn) matchBtn.click();
  }
});
