(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  $('#year').textContent = new Date().getFullYear();

  // Reveal on scroll
  const revealEls = $$('.reveal');
  if ('IntersectionObserver' in window && !reduce) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
    revealEls.forEach((el) => io.observe(el));
  } else revealEls.forEach((el) => el.classList.add('is-in'));

  // Header + sticky mobile CTA
  const header = $('#header'), sticky = $('#sticky-cta'), form = $('#estimation');
  const onScroll = () => {
    const y = scrollY;
    header.classList.toggle('bg-white/85', y > 12);
    header.classList.toggle('backdrop-blur-md', y > 12);
    header.classList.toggle('shadow-soft', y > 12);
    const f = form.getBoundingClientRect();
    const overForm = f.top < innerHeight && f.bottom > 0;
    sticky.classList.toggle('translate-y-full', y < 500 || overForm);
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // FAQ accordion
  $$('.acc-item').forEach((item) => {
    const btn = $('.acc-btn', item);
    btn.addEventListener('click', () => {
      const open = item.dataset.open !== 'true';
      item.dataset.open = open;
      btn.setAttribute('aria-expanded', open);
    });
  });
})();
