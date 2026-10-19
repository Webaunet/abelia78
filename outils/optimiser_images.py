"""Optimise les images retenues (WebP) et détoure le logo fourni. Usage : python3 optimiser_images.py"""
import os
from PIL import Image
import numpy as np

SRC = "/mnt/user-data/uploads/Maquettes/Images/Paysagiste"
LOGO = "/root/.claude/uploads/1b77ae2c-6f54-5707-aa87-539db0c87b37/c78182b0-image.png"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
os.makedirs(OUT, exist_ok=True)

# (source, sortie, largeur max, qualité)
IMAGES = [
    ("imgi_7_entretien-jardin.jpg", "hero-jardin-maison-pierre.webp", 1600, 70),
    ("imgi_4_creation-espace-vert.jpg", "amenagement-creation-espace-vert.webp", 900, 80),
    ("imgi_2_tonte.jpg", "entretien-tonte.webp", 900, 80),
    ("imgi_1_elagage-chene.jpg", "elagage-chene.webp", 900, 80),
    ("imgi_4_taille-haies.jpg", "saisons-taille-haies.webp", 900, 80),
    ("imgi_3_entretien-general.jpg", "equipe-entretien-general.webp", 900, 80),
    ("imgi_6_plantation.jpg", "contact-plantation.webp", 1400, 78),
    # Pages intérieures
    ("imgi_7_entretien-jardin.jpg", "jardin-maison-pierre.webp", 900, 74),
    ("imgi_6_plantation.jpg", "plantation-massif.webp", 900, 76),
    ("imgi_7_terrassement.jpg", "terrassement-jardin.webp", 900, 78),
    ("imgi_8_nivellement.jpg", "nivellement-terrain.webp", 900, 78),
    ("imgi_4_desherbage.jpg", "desherbage-massif.webp", 900, 76),
    ("imgi_5_feuilles.jpg", "ramassage-feuilles.webp", 900, 76),
    ("imgi_1_taille-haies.jpg", "taille-haies-laurier.webp", 900, 78),
    ("imgi_7_dechets-verts.jpg", "evacuation-dechets-verts.webp", 900, 78),
    ("imgi_10_nettoyage.jpg", "nettoyage-jardin.webp", 900, 78),
    ("imgi_3_dessouchage.jpg", "dessouchage-rognage.webp", 900, 78),
    ("imgi_1_hero-elagage-chene.jpg", "elagage-chene-maison-briques.webp", 1200, 76),
]

for src, out, maxw, q in IMAGES:
    im = Image.open(os.path.join(SRC, src)).convert("RGB")
    w, h = im.size
    if w > maxw:  # jamais d'agrandissement
        im = im.resize((maxw, round(h * maxw / w)), Image.LANCZOS)
    path = os.path.join(OUT, out)
    im.save(path, "WEBP", quality=q, method=6)
    print(out, im.size, os.path.getsize(path) // 1024, "Ko")

# Logo : fond blanc -> transparent (alpha déduit de l'écart au blanc)
lg = np.asarray(Image.open(LOGO).convert("RGB")).astype(float)
alpha = 255 - lg.min(axis=2)
alpha = np.clip(alpha * 1.0, 0, 255)
a = np.maximum(alpha, 1)[..., None] / 255.0
rgb = np.clip(255 - (255 - lg) / a, 0, 255)
out = np.dstack([rgb, alpha]).astype("uint8")
# Supprime le liseré de capture d'écran sur les bords (2 px)
out[:2, :, 3] = 0; out[-2:, :, 3] = 0; out[:, :2, 3] = 0; out[:, -2:, 3] = 0
Image.fromarray(out, "RGBA").save(os.path.join(OUT, "logo-abelia.png"), optimize=True)
print("logo-abelia.png", out.shape[1], out.shape[0])

# Favicon : arbre du logo (partie gauche), carré 64 px
logo = Image.open(os.path.join(OUT, "logo-abelia.png"))
tree = logo.crop((0, 0, 118, 127)).crop((0, 0, 118, 118)).resize((64, 64), Image.LANCZOS)
tree.save(os.path.join(OUT, "favicon.png"), optimize=True)
print("favicon.png ok")

# Vignettes de la galerie (560 px de large) dans images/vignettes/
GALERIE = ["amenagement-creation-espace-vert", "plantation-massif", "terrassement-jardin", "nivellement-terrain",
           "jardin-maison-pierre", "entretien-tonte", "equipe-entretien-general", "taille-haies-laurier",
           "saisons-taille-haies", "desherbage-massif", "ramassage-feuilles", "nettoyage-jardin",
           "evacuation-dechets-verts", "elagage-chene", "elagage-chene-maison-briques", "dessouchage-rognage"]
VIG = os.path.join(OUT, "vignettes")
os.makedirs(VIG, exist_ok=True)
for n in GALERIE:
    im = Image.open(os.path.join(OUT, n + ".webp")).convert("RGB")
    w, h = im.size
    im = im.resize((560, round(h * 560 / w)), Image.LANCZOS)
    im.save(os.path.join(VIG, n + ".webp"), "WEBP", quality=72, method=6)
    print("vignette", n, im.size, os.path.getsize(os.path.join(VIG, n + ".webp")) // 1024, "Ko")
