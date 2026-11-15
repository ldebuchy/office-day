"""
Génère le fond pixel art du menu (assets/images/menu_background.png).

L'image est dessinée en basse résolution puis agrandie sans lissage,
pour obtenir des pixels nets et exactement la taille de la fenêtre du jeu.

Usage : python tools/generate_menu_background.py [--seed N] [--out chemin.png]
"""

import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw

LOW_W, LOW_H = 300, 150      # Résolution de dessin
SCALE = 4                    # 300x150 x4 = 1200x600 (taille de la fenêtre)
HORIZON = 118                # Ligne de l'eau

# Palette (ciel clair du matin, bleus et crème)
SKY = [(52, 98, 140), (66, 116, 156), (84, 136, 172), (106, 156, 186), (132, 176, 198), (160, 194, 208)]
CLOUD = (232, 222, 196)
CLOUD_SHADOW = (196, 196, 190)
FAR = (118, 150, 176)
FAR_WINDOW = (134, 166, 190)
MID = [(46, 76, 108), (56, 88, 122), (40, 66, 96)]
MID_WINDOW = (76, 110, 142)
LIT_WINDOW = (226, 206, 158)
SHORE = (70, 98, 128)
WATER = [(40, 70, 100), (34, 62, 90), (30, 54, 80)]
WATER_SHINE = (92, 130, 160)


def draw_sky(d: ImageDraw.ImageDraw) -> None:
    """Dégradé en bandes avec un tramage en damier à chaque transition."""
    band_h = HORIZON / len(SKY)
    for y in range(HORIZON):
        i = min(int(y / band_h), len(SKY) - 1)
        in_band = y - i * band_h
        for x in range(LOW_W):
            color = SKY[i]
            # Les 2 dernières lignes de chaque bande alternent avec la suivante
            if i + 1 < len(SKY) and in_band > band_h - 3 and (x + y) % 2 == 0:
                color = SKY[i + 1]
            d.point((x, y), fill=color)


def draw_cloud(d: ImageDraw.ImageDraw, rng: random.Random, cx: int, cy: int, size: int) -> None:
    """Nuage fait de bosses arrondies posées sur une base plate, avec une ombre dessous."""
    half = size * 3
    d.rectangle((cx - half + 1, cy + 1, cx + half - 1, cy + 1), fill=CLOUD_SHADOW)
    d.rectangle((cx - half, cy - 1, cx + half, cy), fill=CLOUD)
    bumps = rng.randint(2, 3)
    for i in range(bumps):
        r = rng.randint(max(2, size - 1), size + 1) if i else size + 1
        bx = cx + rng.randint(-half + r, half - r)
        d.ellipse((bx - r, cy - 2 * r, bx + r, cy), fill=CLOUD)


def draw_far_skyline(d: ImageDraw.ImageDraw, rng: random.Random) -> None:
    """Silhouettes lointaines, claires et peu contrastées."""
    x = 0
    while x < LOW_W:
        w = rng.randint(6, 14)
        h = rng.randint(10, 30)
        top = HORIZON - h
        d.rectangle((x, top, x + w - 1, HORIZON - 1), fill=FAR)
        for wy in range(top + 2, HORIZON - 2, 3):
            for wx in range(x + 1, x + w - 1, 2):
                d.point((wx, wy), fill=FAR_WINDOW)
        x += w + rng.randint(0, 2)


def draw_mid_skyline(d: ImageDraw.ImageDraw, rng: random.Random) -> None:
    """Immeubles de bureaux au premier plan."""
    x = 0
    while x < LOW_W:
        w = rng.randint(8, 18)
        h = rng.randint(14, 48)
        top = HORIZON - h
        color = rng.choice(MID)
        d.rectangle((x, top, x + w - 1, HORIZON - 1), fill=color)
        roof = rng.random()
        if roof < 0.2 and h > 24:  # Toit en flèche
            cx = x + w // 2
            d.rectangle((cx - 2, top - 4, cx + 2, top - 1), fill=color)
            d.line((cx, top - 10, cx, top - 5), fill=color)
        elif roof < 0.45:          # Toit en gradins
            d.rectangle((x + 2, top - 3, x + w - 3, top - 1), fill=color)
        for wy in range(top + 2, HORIZON - 1, 3):
            for wx in range(x + 2, x + w - 2, 3):
                lit = rng.random() < 0.12
                d.rectangle((wx, wy, wx + 1, wy), fill=LIT_WINDOW if lit else MID_WINDOW)
        x += w + rng.randint(-2, 1)


def draw_water(img: Image.Image, d: ImageDraw.ImageDraw, rng: random.Random) -> None:
    """Fleuve en bandes, reflets brisés de la ville et éclats de lumière."""
    rows = LOW_H - HORIZON
    for y in range(HORIZON, LOW_H):
        band = min((y - HORIZON) * len(WATER) // rows, len(WATER) - 1)
        d.line((0, y, LOW_W - 1, y), fill=WATER[band])
    d.line((0, HORIZON, LOW_W - 1, HORIZON), fill=SHORE)
    # Reflet : on recopie la ligne d'horizon assombrie, une ligne sur deux, décalée
    for i, y in enumerate(range(HORIZON + 2, min(HORIZON + 14, LOW_H), 2)):
        shift = rng.randint(-1, 1)
        src_y = HORIZON - 2 - i * 3
        for x in range(0, LOW_W, 2):  # Un pixel sur deux : reflet discret et brisé
            r, g, b = img.getpixel((x, src_y))
            wr, wg, wb = img.getpixel((x, y))
            d.point(((x + shift) % LOW_W, y), fill=((r + wr * 3) // 4, (g + wg * 3) // 4, (b + wb * 3) // 4))
    for _ in range(45):
        x = rng.randint(0, LOW_W - 6)
        y = rng.randint(HORIZON + 3, LOW_H - 2)
        d.line((x, y, x + rng.randint(2, 5), y), fill=WATER_SHINE)


def generate(seed: int) -> Image.Image:
    rng = random.Random(seed)
    img = Image.new("RGB", (LOW_W, LOW_H))
    d = ImageDraw.Draw(img)

    draw_sky(d)
    for cx, cy, size in [(36, 26, 4), (130, 16, 3), (208, 34, 5), (268, 20, 3), (244, 62, 2), (22, 62, 2)]:
        draw_cloud(d, rng, cx, cy, size)
    draw_far_skyline(d, rng)

    draw_mid_skyline(d, rng)
    draw_water(img, d, rng)

    return img.resize((LOW_W * SCALE, LOW_H * SCALE), Image.NEAREST)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--seed", type=int, default=2025)
    parser.add_argument("--out", type=Path, default=Path("assets/images/menu_background.png"))
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    generate(args.seed).save(args.out)
    print(f"Fond généré : {args.out} ({LOW_W * SCALE}x{LOW_H * SCALE})")


if __name__ == "__main__":
    main()
