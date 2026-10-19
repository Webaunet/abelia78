(function () {
  var form = document.getElementById('contact-form');
  if (!form) return;

  // Numéro utilisé par le bouton SMS. À remplacer par un mobile si l'entreprise en a un.
  var SMS_NUMBER = '+33139586558';
  var MAIL = 'bruno@abelia78.fr';

  var f = {
    nom: document.getElementById('f-nom'),
    tel: document.getElementById('f-tel'),
    mail: document.getElementById('f-mail'),
    commune: document.getElementById('f-commune'),
    presta: document.getElementById('f-presta'),
    msg: document.getElementById('f-msg')
  };
  var errs = { nom: 'e-nom', tel: 'e-tel', mail: 'e-mail', presta: 'e-presta' };
  var out = document.getElementById('recap-msg');
  var help = document.getElementById('recap-help');
  var status = document.getElementById('form-status');
  var sms = document.getElementById('act-sms');
  var mail = document.getElementById('act-mail');
  var copy = document.getElementById('act-copy');
  var touched = false;
  var lastText = '';

  var rules = {
    nom: function (v) { return v.trim().length >= 2 ? '' : 'Indiquez votre nom.'; },
    tel: function (v) {
      var t = v.replace(/[\s.\-]/g, '');
      if (!t) return 'Indiquez votre numéro de téléphone.';
      return /^(?:(?:\+|00)33|0)[1-9]\d{8}$/.test(t) ? '' : 'Le numéro doit comporter 10 chiffres, par exemple 01 23 45 67 89.';
    },
    mail: function (v) {
      v = v.trim();
      if (!v) return 'Indiquez votre adresse e-mail.';
      return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : "L'adresse e-mail doit ressembler à nom@exemple.fr.";
    },
    presta: function (v) { return v ? '' : 'Choisissez la prestation concernée.'; }
  };

  function check(name) {
    var el = f[name];
    var msg = rules[name](el.value);
    var box = document.getElementById(errs[name]);
    box.textContent = msg;
    if (msg) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid');
    return !msg;
  }

  function setLink(a, href) {
    if (href) {
      a.setAttribute('href', href);
      a.removeAttribute('aria-disabled');
      a.removeAttribute('tabindex');
    } else {
      a.setAttribute('href', '#formulaire');
      a.setAttribute('aria-disabled', 'true');
      a.setAttribute('tabindex', '-1');
    }
  }

  function message() {
    var lines = ['Bonjour, je souhaite une demande de devis : ' + f.presta.value + '.', ''];
    lines.push('Nom : ' + f.nom.value.trim());
    lines.push('Téléphone : ' + f.tel.value.trim());
    lines.push('E-mail : ' + f.mail.value.trim());
    if (f.commune.value.trim()) lines.push('Commune : ' + f.commune.value.trim());
    if (f.msg.value.trim()) { lines.push(''); lines.push('Message : ' + f.msg.value.trim()); }
    return lines.join('\n');
  }

  function render(valid) {
    if (!valid) {
      lastText = '';
      out.textContent = 'Votre demande apparaîtra ici dès que le formulaire est complet.';
      setLink(sms, null); setLink(mail, null);
      copy.disabled = true;
      help.textContent = "Les boutons SMS, copie et e-mail s'activent quand le formulaire est valide.";
      return;
    }
    lastText = message();
    out.textContent = lastText;
    var body = encodeURIComponent(lastText);
    setLink(sms, 'sms:' + SMS_NUMBER + '?body=' + body);
    setLink(mail, 'mailto:' + MAIL + '?subject=' + encodeURIComponent('Demande de devis') + '&body=' + body);
    copy.disabled = false;
    help.textContent = "Rien n'est envoyé automatiquement : choisissez une action ci-dessus.";
  }

  function allValid(show) {
    var ok = true;
    Object.keys(rules).forEach(function (k) {
      if (show) { if (!check(k)) ok = false; }
      else if (rules[k](f[k].value)) ok = false;
    });
    return ok;
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    touched = true;
    var ok = allValid(true);
    render(ok);
    if (ok) {
      status.textContent = 'Message prêt : choisissez une action à droite.';
      var t = document.getElementById('h-recap');
      if (window.matchMedia('(max-width: 980px)').matches) t.scrollIntoView({ behavior: 'smooth', block: 'start' });
    } else {
      status.textContent = 'Corrigez les champs signalés.';
      var first = form.querySelector('[aria-invalid="true"]');
      if (first) first.focus();
    }
  });

  Object.keys(f).forEach(function (k) {
    var ev = f[k].tagName === 'SELECT' ? 'change' : 'input';
    f[k].addEventListener(ev, function () {
      if (rules[k] && f[k].hasAttribute('aria-invalid')) check(k);
      if (touched) { render(allValid(false)); }
    });
    if (rules[k]) f[k].addEventListener('blur', function () { if (f[k].value) check(k); });
  });

  copy.addEventListener('click', function () {
    if (!lastText) return;
    var fallback = function () {
      var r = document.createRange();
      r.selectNodeContents(out);
      var s = window.getSelection();
      s.removeAllRanges(); s.addRange(r);
      status.textContent = 'Message sélectionné : faites Ctrl+C pour le copier.';
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(lastText).then(function () { status.textContent = 'Message copié.'; }, fallback);
    } else { fallback(); }
  });
})();
