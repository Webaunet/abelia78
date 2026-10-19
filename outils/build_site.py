"""Assemble les pages du site : en-tête, pied de page et <head> communs + corps dans outils/src/<page>.html.
Usage : python3 build_site.py"""
import os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
BASE = "https://webaunet.github.io/abelia78/"

PAGES = [
    # fichier, clé de menu, <title>, meta description, script supplémentaire
    ("index.html", "index", "Abélia, paysagistes et élagueurs à L'Étang-la-Ville (78)",
     "Abélia, paysagistes et élagueurs à L'Étang-la-Ville (78) : conception et aménagement de jardins, entretien, élagage et abattage près de Saint-Germain-en-Laye.", None),
    ("amenagement.html", "amenagement", "Aménagement de jardin à L'Étang-la-Ville | Abélia",
     "Conception paysagère, maçonnerie, terrasses, clôtures, terrassement, engazonnement et arrosage automatique par Abélia, paysagistes à L'Étang-la-Ville (78).", None),
    ("entretien.html", "entretien", "Entretien de jardin à L'Étang-la-Ville | Abélia",
     "Tonte, taille des haies, débroussaillage et désherbage manuel par Abélia, paysagistes à L'Étang-la-Ville (78). Travaux éligibles au service à la personne.", None),
    ("elagage.html", "elagage", "Élagage et abattage d'arbres près de Saint-Germain-en-Laye | Abélia",
     "Élagueurs-grimpeurs à L'Étang-la-Ville (78) : élagage, abattage par démontage et dessouchage par rognage, pour particuliers, parcs et châteaux.", None),
    ("a-propos.html", "a-propos", "À propos d'Abélia, paysagistes à L'Étang-la-Ville",
     "Entreprise de paysage fondée en 1997 à L'Étang-la-Ville (78) : équipe, zone d'intervention en Île-de-France et horaires.", None),
    ("contact.html", "contact", "Contact et devis | Abélia, paysagistes à L'Étang-la-Ville",
     "Contactez Abélia, paysagistes et élagueurs à L'Étang-la-Ville (78) : téléphone, e-mail, adresse et formulaire de demande de devis.", "js/contact.js"),
    ("mentions-legales.html", None, "Mentions légales | Abélia, L'Étang-la-Ville",
     "Mentions légales du site d'Abélia (AAJ Abélia Aménagements de Jardins), paysagistes à L'Étang-la-Ville (78).", None),
]

NAV = [("index", "index.html", "Accueil"), ("amenagement", "amenagement.html", "Aménagement"),
       ("entretien", "entretien.html", "Entretien"), ("elagage", "elagage.html", "Élagage"),
       ("a-propos", "a-propos.html", "À propos"), ("contact", "contact.html", "Contact")]

PHONE_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>'


def header(key):
    items = []
    for k, href, label in NAV:
        cur = ' aria-current="page"' if k == key else ""
        items.append(f'        <li><a href="{href}"{cur}>{label}</a></li>')
    return f'''<header class="hd">
  <div class="wrap hd__in">
    <a class="logo" href="{BASE}" aria-label="Abélia, retour à l'accueil du site"><img src="images/logo-abelia.png" width="402" height="127" alt="Abélia, paysagistes élagueurs, service à la personne"></a>
    <nav class="nav" id="menu" aria-label="Navigation principale">
      <ul>
{chr(10).join(items)}
      </ul>
    </nav>
    <a class="btn btn--tel" href="tel:+33139586558" aria-label="Appeler le 01 39 58 65 58">{PHONE_SVG}<span>01 39 58 65 58</span></a>
    <button class="burger" type="button" aria-expanded="false" aria-controls="menu" aria-label="Ouvrir le menu"><span></span><span></span><span></span></button>
  </div>
</header>'''


def footer(key, page):
    def a(href, label, opt=True):
        cur = ' aria-current="page"' if href == page else ""
        cls = ' class="opt"' if opt else ""
        return f'<li{cls}><a href="{href}"{cur}>{label}</a></li>'
    links = "\n        ".join([a("amenagement.html", "Aménagement"), a("entretien.html", "Entretien"), a("elagage.html", "Élagage"),
                              a("a-propos.html", "À propos"), a("mentions-legales.html", "Mentions légales", False)])
    return f'''<footer class="ft">
  <div class="wrap ft__in">
    <p><strong>SAS Abélia</strong> · AAJ Abélia Aménagements de Jardins<br>20 Chemin des Brosses, 78620 L'Étang-la-Ville · <a href="tel:+33139586558">01 39 58 65 58</a> · <a href="mailto:bruno@abelia78.fr">bruno@abelia78.fr</a></p>
    <nav aria-label="Pied de page">
      <ul>
        {links}
      </ul>
    </nav>
  </div>
</footer>'''


def build():
    for page, key, title, desc, extra in PAGES:
        src = os.path.join(HERE, "src", page)
        if not os.path.exists(src):
            print("ABSENT :", src)
            continue
        body = open(src, encoding="utf-8").read().rstrip()
        if body.count("<h1") != 1:
            sys.exit(f"ERREUR : {page} doit avoir un seul h1")
        scripts = '<script src="js/site.js"></script>'
        if extra:
            scripts += f'\n<script src="{extra}"></script>'
        html = f'''<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="images/favicon.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@500&family=Outfit:wght@300;400;500;600&display=swap">
<link rel="stylesheet" href="css/style.css">
</head>
<body id="top">
<a class="skip" href="#main">Aller au contenu</a>

{header(key)}

<main id="main">
{body}
</main>

{footer(key, page)}

<div class="toast" role="status" aria-live="polite"></div>
{scripts}
</body>
</html>
'''
        with open(os.path.join(ROOT, page), "w", encoding="utf-8") as f:
            f.write(html)
        print("OK", page, len(html) // 1024, "Ko")


if __name__ == "__main__":
    build()
