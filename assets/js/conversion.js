// Déclenche la conversion Google Ads une seule fois par visite de /merci.
// La balise Google (gtag.js) est déjà chargée dans le <head>.
// Tant que le libellé de conversion n'est pas renseigné dans merci.html, aucun événement n'est envoyé.
(() => {
  const c = window.ADS_CONVERSION || {};
  if (!/^AW-\d+$/.test(c.id || '') || !c.label || /^X+$/.test(c.label)) return;
  if (typeof window.gtag !== 'function') return;
  window.gtag('event', 'conversion', { send_to: `${c.id}/${c.label}` });
})();
