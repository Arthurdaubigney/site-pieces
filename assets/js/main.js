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

  // Preselect type from card links
  const typeSel = $('#type');
  $$('[data-type]').forEach((a) => a.addEventListener('click', () => { typeSel.value = a.dataset.type; }));

  // Photo previews
  $$('.drop').forEach((drop) => {
    const input = $('input[type=file]', drop), img = $('.preview', drop), label = $('.drop-label', drop);
    input.addEventListener('change', () => {
      const f = input.files[0];
      if (!f) return;
      if (img.src.startsWith('blob:')) URL.revokeObjectURL(img.src);
      img.src = URL.createObjectURL(f);
      img.alt = `Aperçu : ${f.name}`;
      img.classList.remove('hidden');
      label.classList.add('opacity-0');
      clearError(input);
    });
  });

  // Validation
  const msgs = {
    type: 'Choisissez un type de pièce.',
    recto: 'Ajoutez la photo du recto.',
    verso: 'Ajoutez la photo du verso.',
    nom: 'Indiquez votre nom.',
    email: 'Indiquez une adresse e-mail valide.',
    consent: 'Votre accord est nécessaire pour traiter la demande.',
  };
  const errEl = (field) => (field.closest('div'))?.querySelector('.err') || field.parentElement.querySelector('.err');
  function setError(field) {
    const el = errEl(field);
    field.setAttribute('aria-invalid', 'true');
    if (el) { el.textContent = msgs[field.name] || 'Champ requis.'; el.classList.remove('hidden'); }
  }
  function clearError(field) {
    field.removeAttribute('aria-invalid');
    const el = errEl(field);
    if (el) el.classList.add('hidden');
  }

  const formEl = $('#estimation-form'), success = $('#success');
  const required = $$('[required]', formEl);
  required.forEach((f) => {
    f.addEventListener('blur', () => { if (f.checkValidity()) clearError(f); else if (f.type !== 'file') setError(f); });
    f.addEventListener('input', () => { if (f.getAttribute('aria-invalid') && f.checkValidity()) clearError(f); });
    f.addEventListener('change', () => { if (f.getAttribute('aria-invalid') && f.checkValidity()) clearError(f); });
  });

  formEl.addEventListener('submit', async (e) => {
    e.preventDefault();
    const bad = required.filter((f) => !f.checkValidity());
    required.forEach((f) => (f.checkValidity() ? clearError(f) : setError(f)));
    if (bad.length) {
      const first = bad[0];
      (first.type === 'file' ? first.closest('label') : first).scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
      if (first.type !== 'file') first.focus({ preventScroll: true }); else first.focus({ preventScroll: true });
      formEl.classList.remove('is-shaking'); void formEl.offsetWidth; formEl.classList.add('is-shaking');
      return;
    }
    const btn = $('button[type=submit]', formEl), label = $('.btn-label', btn);
    btn.disabled = true; label.textContent = 'Envoi en cours…';
    try {
      // Tant que l'endpoint n'est pas configuré (REPLACE_ME), on simule l'envoi.
      if (!formEl.action.includes('REPLACE_ME')) {
        const res = await fetch(formEl.action, { method: 'POST', body: new FormData(formEl), headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error('send');
      } else await new Promise((r) => setTimeout(r, 600));
      formEl.classList.add('is-hidden');
      success.classList.remove('is-hidden');
      success.focus({ preventScroll: true });
      success.scrollIntoView({ block: 'center', behavior: reduce ? 'auto' : 'smooth' });
    } catch {
      btn.disabled = false; label.textContent = 'Recevoir mon estimation gratuite';
      alert("L'envoi a échoué. Merci de réessayer dans un instant.");
    }
  });
})();
