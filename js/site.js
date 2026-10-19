(function () {
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  var toast = document.querySelector('.toast');
  var timer;

  function say(msg) {
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(timer);
    timer = setTimeout(function () { toast.classList.remove('show'); }, 3200);
  }

  function setMenu(open) {
    if (!burger || !menu) return;
    menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Fermer le menu' : 'Ouvrir le menu');
  }

  if (burger && menu) {
    burger.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
    menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('open')) { setMenu(false); burger.focus(); }
    });
    window.addEventListener('resize', function () { if (window.innerWidth > 980) setMenu(false); });
  }

  // Séries de cartes défilantes : accessibles au clavier quand elles débordent
  var sliders = document.querySelectorAll('[data-slider]');
  function syncSliders() {
    sliders.forEach(function (el) {
      var scrolls = el.scrollWidth > el.clientWidth + 2;
      if (scrolls) {
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'region');
        el.setAttribute('aria-label', el.getAttribute('data-slider'));
      } else {
        el.removeAttribute('tabindex'); el.removeAttribute('role'); el.removeAttribute('aria-label');
      }
    });
  }
  if (sliders.length) { syncSliders(); window.addEventListener('resize', syncSliders); }

  // Boutons « Copier »
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.getElementById(btn.getAttribute('data-copy'));
      if (!target) return;
      var text = target.textContent.trim();
      var fallback = function () {
        var r = document.createRange();
        r.selectNodeContents(target);
        var s = window.getSelection();
        s.removeAllRanges();
        s.addRange(r);
        say('Texte sélectionné : faites Ctrl+C pour le copier.');
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () { say('Copié : ' + text); }, fallback);
      } else { fallback(); }
    });
  });
})();
