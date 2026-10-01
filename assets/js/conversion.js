// Déclenche la conversion Google Ads une seule fois par visite de /merci.
// Tant que l'ID et le libellé ne sont pas renseignés dans merci.html, rien n'est envoyé.
(() => {
  const c = window.ADS_CONVERSION || {};
  if (!/^AW-\d+$/.test(c.id || '') || !c.label || /^X+$/.test(c.label)) return;
  const s = document.createElement('script');
  s.async = true;
  s.src = `https://www.googletagmanager.com/gtag/js?id=${c.id}`;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function () { window.dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', c.id);
  gtag('event', 'conversion', { send_to: `${c.id}/${c.label}` });
})();
