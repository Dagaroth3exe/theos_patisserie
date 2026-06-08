/**
 * Scroll-triggered reveal animations — GSAP ScrollTrigger
 */
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') return;

  // ── Section kickers (slide in from left) ─────────────────────
  gsap.utils.toArray('[data-reveal="kicker"]').forEach(el => {
    gsap.from(el, {
      scrollTrigger: { trigger: el, start: 'top 90%', once: true },
      opacity: 0,
      x: -24,
      duration: 0.5,
      ease: 'power2.out',
    });
  });

  // ── Section headings (line-by-line wipe) ─────────────────────
  gsap.utils.toArray('[data-reveal="heading"]').forEach(el => {
    if (typeof SplitType !== 'undefined') {
      const split = new SplitType(el, { types: 'lines' });
      gsap.from(split.lines, {
        scrollTrigger: { trigger: el, start: 'top 87%', once: true },
        opacity: 0,
        y: 28,
        stagger: 0.09,
        duration: 0.65,
        ease: 'power3.out',
      });
    } else {
      gsap.from(el, {
        scrollTrigger: { trigger: el, start: 'top 87%', once: true },
        opacity: 0,
        y: 24,
        duration: 0.6,
        ease: 'power3.out',
      });
    }
  });

  // ── Product cards (staggered grid entrance) ───────────────────
  gsap.utils.toArray('.product-grid').forEach(grid => {
    const cards = grid.querySelectorAll('.product-card');
    if (!cards.length) return;
    gsap.from(cards, {
      scrollTrigger: { trigger: grid, start: 'top 82%', once: true },
      opacity: 0,
      y: 48,
      scale: 0.96,
      stagger: 0.10,
      duration: 0.6,
      ease: 'power3.out',
    });
  });

  // ── Images (clip-path wipe from left) ────────────────────────
  gsap.utils.toArray('[data-reveal="image"]').forEach(el => {
    gsap.from(el, {
      scrollTrigger: { trigger: el, start: 'top 82%', once: true },
      clipPath: 'inset(0 100% 0 0)',
      duration: 0.85,
      ease: 'power3.inOut',
    });
  });

  // ── Brand story text (alternating slide) ─────────────────────
  gsap.utils.toArray('.story-section').forEach((section, i) => {
    const textEl = section.querySelector('.story-text');
    if (!textEl) return;
    gsap.from(textEl, {
      scrollTrigger: { trigger: section, start: 'top 78%', once: true },
      opacity: 0,
      x: i % 2 === 0 ? -38 : 38,
      duration: 0.75,
      ease: 'power3.out',
    });
  });

  // ── Generic fade-up for any element with data-reveal="fade" ──
  gsap.utils.toArray('[data-reveal="fade"]').forEach(el => {
    gsap.from(el, {
      scrollTrigger: { trigger: el, start: 'top 88%', once: true },
      opacity: 0,
      y: 20,
      duration: 0.55,
      ease: 'power2.out',
    });
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
