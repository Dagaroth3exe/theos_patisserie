/**
 * Hero & page-load animations — GSAP + SplitType
 * Runs only when GSAP and SplitType are available.
 */
document.addEventListener('DOMContentLoaded', () => {
  if (typeof gsap === 'undefined') return;

  // ── Page enter fade ──────────────────────────────────────────
  gsap.from('body', { opacity: 0, duration: 0.35, ease: 'power2.out' });

  // ── Navbar drop-in ───────────────────────────────────────────
  const nav = document.querySelector('.site-nav');
  if (nav) {
    gsap.from(nav, { y: -60, opacity: 0, duration: 0.75, ease: 'power3.out', delay: 0.1 });
  }

  // ── Hero headline character stagger ─────────────────────────
  const heroHeadline = document.querySelector('.hero-headline');
  if (heroHeadline && typeof SplitType !== 'undefined') {
    const split = new SplitType(heroHeadline, { types: 'chars, words' });
    gsap.from(split.chars, {
      opacity: 0,
      y: 45,
      rotateX: -50,
      stagger: 0.033,
      duration: 0.65,
      ease: 'back.out(1.3)',
      delay: 0.45,
    });
  } else if (heroHeadline) {
    // Fallback: fade up the whole headline
    gsap.from(heroHeadline, { opacity: 0, y: 30, duration: 0.7, ease: 'power3.out', delay: 0.4 });
  }

  // ── Hero sub-elements ────────────────────────────────────────
  const heroSub = document.querySelector('.hero-sub');
  const heroCta = document.querySelector('.hero-cta');
  const heroKicker = document.querySelector('.hero-headline')?.closest('section')?.querySelector('.section-kicker');

  [heroKicker, heroSub, heroCta].forEach((el, i) => {
    if (!el) return;
    gsap.from(el, {
      opacity: 0,
      y: 22,
      duration: 0.6,
      ease: 'power2.out',
      delay: 0.9 + i * 0.15,
    });
  });

  // ── Floating dessert illustrations ───────────────────────────
  const floatLeft = document.querySelector('.hero-float-left');
  const floatRight = document.querySelector('.hero-float-right');

  if (floatLeft) {
    gsap.fromTo(floatLeft,
      { y: 0, opacity: 0 },
      { opacity: 1, duration: 0.8, delay: 0.6, ease: 'power2.out', onComplete: () => {
        gsap.to(floatLeft, { y: '-=16', duration: 3.5, repeat: -1, yoyo: true, ease: 'sine.inOut' });
      }}
    );
  }

  if (floatRight) {
    gsap.fromTo(floatRight,
      { y: 0, opacity: 0 },
      { opacity: 1, duration: 0.8, delay: 0.8, ease: 'power2.out', onComplete: () => {
        gsap.to(floatRight, { y: '+=14', duration: 4, repeat: -1, yoyo: true, ease: 'sine.inOut' });
      }}
    );
  }

  // ── Navbar scroll behaviour ──────────────────────────────────
  if (nav && typeof ScrollTrigger !== 'undefined') {
    ScrollTrigger.create({
      start: 'top -60',
      onUpdate: (self) => {
        nav.classList.toggle('nav-scrolled', self.progress > 0);
      },
    });
  }
});
