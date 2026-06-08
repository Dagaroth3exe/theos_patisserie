/**
 * Scroll-triggered reveal animations — GSAP ScrollTrigger
 */
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

  // Refresh scroll positions after all images have loaded so elements that
  // shifted due to image layout don't get stuck at opacity 0.
  window.addEventListener('load', () => ScrollTrigger.refresh());

  // ── Section kickers (slide in from left) ─────────────────────
  // Use fromTo so GSAP never leaves an element permanently invisible
  // if the trigger fires while layout is still settling.
  gsap.utils.toArray('[data-reveal="kicker"]').forEach(el => {
    gsap.fromTo(el,
      { opacity: 0, x: -24 },
      {
        opacity: 1, x: 0, duration: 0.5, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 95%', once: true },
      }
    );
  });

  // ── Section headings (line-by-line wipe) ─────────────────────
  gsap.utils.toArray('[data-reveal="heading"]').forEach(el => {
    if (typeof SplitType !== 'undefined') {
      const split = new SplitType(el, { types: 'lines' });
      gsap.fromTo(split.lines,
        { opacity: 0, y: 28 },
        {
          opacity: 1, y: 0, stagger: 0.09, duration: 0.65, ease: 'power3.out',
          scrollTrigger: { trigger: el, start: 'top 92%', once: true },
        }
      );
    } else {
      gsap.fromTo(el,
        { opacity: 0, y: 24 },
        {
          opacity: 1, y: 0, duration: 0.6, ease: 'power3.out',
          scrollTrigger: { trigger: el, start: 'top 92%', once: true },
        }
      );
    }
  });

  // ── Product cards (staggered grid entrance) ───────────────────
  gsap.utils.toArray('.product-grid').forEach(grid => {
    const cards = grid.querySelectorAll('.product-card');
    if (!cards.length) return;
    gsap.fromTo(cards,
      { opacity: 0, y: 48, scale: 0.96 },
      {
        opacity: 1, y: 0, scale: 1, stagger: 0.10, duration: 0.6, ease: 'power3.out',
        scrollTrigger: { trigger: grid, start: 'top 85%', once: true },
      }
    );
  });

  // ── Images (clip-path wipe from left) ────────────────────────
  gsap.utils.toArray('[data-reveal="image"]').forEach(el => {
    gsap.fromTo(el,
      { clipPath: 'inset(0 100% 0 0)' },
      {
        clipPath: 'inset(0 0% 0 0)', duration: 0.85, ease: 'power3.inOut',
        scrollTrigger: { trigger: el, start: 'top 85%', once: true },
      }
    );
  });

  // ── Brand story text (alternating slide) ─────────────────────
  gsap.utils.toArray('.story-section').forEach((section, i) => {
    const textEl = section.querySelector('.story-text');
    if (!textEl) return;
    gsap.fromTo(textEl,
      { opacity: 0, x: i % 2 === 0 ? -38 : 38 },
      {
        opacity: 1, x: 0, duration: 0.75, ease: 'power3.out',
        scrollTrigger: { trigger: section, start: 'top 80%', once: true },
      }
    );
  });

  // ── Generic fade-up for any element with data-reveal="fade" ──
  gsap.utils.toArray('[data-reveal="fade"]').forEach(el => {
    gsap.fromTo(el,
      { opacity: 0, y: 20 },
      {
        opacity: 1, y: 0, duration: 0.55, ease: 'power2.out',
        scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      }
    );
  });

  // ── Category showcase items ───────────────────────────────────
  const catItems = document.querySelectorAll('#category-showcase .cat-item');
  if (catItems.length) {
    gsap.from(catItems, {
      scrollTrigger: { trigger: '#category-showcase', start: 'top 85%', once: true },
      opacity: 0,
      y: 20,
      stagger: 0.07,
      duration: 0.5,
      ease: 'power2.out',
    });
  }
});
