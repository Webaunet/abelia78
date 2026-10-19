"""Génère la version artefact (HTML autonome, CSS/JS en ligne) de index.html.
Usage : python3 build_artefact.py <dossier_sortie>"""
import os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
out_dir = sys.argv[1]
os.makedirs(out_dir, exist_ok=True)

def read(p):
    with open(os.path.join(ROOT, p), encoding="utf-8") as f:
        return f.read()

html = read("index.html")
css = read("css/style.css")
js = read("js/site.js")

fonts = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com[^"]+)">', html)
if not fonts:
    sys.exit("ERREUR : lien Google Fonts introuvable")
body = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
if not body:
    sys.exit("ERREUR : corps introuvable")
inner = body.group(1)
if '<script src="js/site.js"></script>' not in inner:
    sys.exit("ERREUR : balise script introuvable")
inner = inner.replace('<script src="js/site.js"></script>', "")

page = (
    "<title>Abélia Aménagements de Jardins</title>\n"
    '<meta name="claude:viewport-fit-sides" content="cover">\n'
    '<link rel="stylesheet" href="%s">\n<style>\n%s\n</style>\n'
    '<div id="top">%s</div>\n<script>\n%s\n</script>\n'
) % (fonts.group(1), css, inner, js)

dest = os.path.join(out_dir, "accueil.html")
with open(dest, "w", encoding="utf-8") as f:
    f.write(page)
print(dest, len(page) // 1024, "Ko")
