(function () {
  var gal = document.getElementById('gal');
  if (!gal) return;
  var items = [].slice.call(gal.querySelectorAll('li'));
  var chips = [].slice.call(document.querySelectorAll('.filters .chip'));
  var more = document.getElementById('gal-more');
  var count = document.getElementById('gal-count');
  var mq = window.matchMedia('(min-width: 981px)');
  var PAGE = mq.matches ? 8 : 6, cat = 'all', shown = PAGE;

  function matching() { return items.filter(function (li) { return cat === 'all' || li.getAttribute('data-cat') === cat; }); }

  function render() {
    var m = matching();
    items.forEach(function (li) { li.hidden = true; });
    m.forEach(function (li, i) { li.hidden = i >= shown; });
    var n = Math.min(shown, m.length);
    count.textContent = n + ' photo' + (n > 1 ? 's' : '') + ' affichée' + (n > 1 ? 's' : '') + ' sur ' + m.length;
    more.hidden = shown >= m.length;
    more.textContent = 'Voir ' + Math.min(PAGE, m.length - shown) + ' photos de plus';
    chips.forEach(function (c) { c.setAttribute('aria-pressed', c.getAttribute('data-filter') === cat ? 'true' : 'false'); });
  }

  function setCat(c) { cat = c; shown = PAGE; render(); }

  chips.forEach(function (c) { c.addEventListener('click', function () { setCat(c.getAttribute('data-filter')); }); });
  more.addEventListener('click', function () { shown += PAGE; render(); });

  // Boutons « Voir les photos » des cartes de métier
  [].slice.call(document.querySelectorAll('[data-show]')).forEach(function (b) {
    b.addEventListener('click', function () {
      setCat(b.getAttribute('data-show'));
      var sec = document.getElementById('galerie');
      sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      var chip = chips.filter(function (c) { return c.getAttribute('data-filter') === cat; })[0];
      if (chip) setTimeout(function () { chip.focus({ preventScroll: true }); }, 400);
    });
  });

  // Visionneuse
  var lb = document.getElementById('lb');
  var img = document.getElementById('lb-img');
  var cap = document.getElementById('lb-cap');
  var num = document.getElementById('lb-n');
  var list = [], idx = 0, opener = null;

  function show(i) {
    idx = (i + list.length) % list.length;
    var b = list[idx];
    img.src = b.getAttribute('data-full');
    img.width = +b.getAttribute('data-w'); img.height = +b.getAttribute('data-h');
    img.alt = b.getAttribute('data-alt');
    cap.textContent = b.getAttribute('data-cap');
    num.textContent = (idx + 1) + ' / ' + list.length;
  }
  function open(btn) {
    list = matching().filter(function (li) { return !li.hidden; }).map(function (li) { return li.querySelector('.shot'); });
    opener = btn;
    show(list.indexOf(btn));
    if (!lb.open) lb.showModal();
    document.body.classList.add('lb-open');
  }
  gal.addEventListener('click', function (e) { var b = e.target.closest('.shot'); if (b) open(b); });
  document.getElementById('lb-prev').addEventListener('click', function () { show(idx - 1); });
  document.getElementById('lb-next').addEventListener('click', function () { show(idx + 1); });
  document.getElementById('lb-close').addEventListener('click', function () { lb.close(); });
  lb.addEventListener('click', function (e) { if (e.target === lb || e.target.classList.contains('lb__box')) lb.close(); });
  lb.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
  });
  lb.addEventListener('close', function () {
    document.body.classList.remove('lb-open');
    if (opener && document.contains(opener) && !opener.closest('[hidden]')) opener.focus();
  });

  var onMq = function () { PAGE = mq.matches ? 8 : 6; shown = PAGE; render(); };
  if (mq.addEventListener) mq.addEventListener('change', onMq);
  render();
})();
