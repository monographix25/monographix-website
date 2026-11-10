# -*- coding: utf-8 -*-
"""
Importiert die Original-Fotos, schneidet sie auf das jeweilige Zielformat zu
und legt sie optimiert unter assets/img/photos/ ab.

Aufruf:  python tools/import_photos.py
"""
import json
import pathlib
import sys

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "_fotos"
DST = ROOT / "assets" / "img" / "photos"
MAP_FILE = ROOT / "tools" / "foto_map.json"

# Rolle, Seitenverhaeltnis (B/H), Fokus (0 = oben, 1 = unten)
ROLES = [
    ("hero", 4 / 5, 0.45),
    ("action", 3 / 4, 0.42),
    ("glas", 3 / 4, 0.45),
    ("basteln", 3 / 4, 0.45),
    ("fotografie", 3 / 4, 0.45),
    ("portrait", 4 / 5, 0.35),
    ("team", 3 / 4, 0.45),
    ("studio", 3 / 2, 0.50),
]
FALLBACK = {"team": "action", "studio": "hero"}

MAX_W = 1400
QUALITY = 88


def crop_to(img: Image.Image, ratio: float, focus: float) -> Image.Image:
    w, h = img.size
    target_h = w / ratio
    if target_h <= h:
        extra = h - target_h
        top = extra * focus
        return img.crop((0, round(top), w, round(top + target_h)))
    # Bild ist zu schmal -> seitlich beschneiden
    target_w = h * ratio
    left = (w - target_w) / 2
    return img.crop((round(left), 0, round(left + target_w), h))


def finish(img: Image.Image) -> Image.Image:
    if img.width > MAX_W:
        img = img.resize((MAX_W, round(img.height * MAX_W / img.width)), Image.LANCZOS)
    img = ImageEnhance.Contrast(img).enhance(1.05)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = img.filter(ImageFilter.UnsharpMask(radius=1.2, percent=90, threshold=2))
    return img


def main() -> int:
    DST.mkdir(parents=True, exist_ok=True)

    if not SRC.exists():
        SRC.mkdir(parents=True, exist_ok=True)
        print(f"Ordner angelegt: {SRC}\nBitte Fotos dort ablegen und erneut starten.")
        return 1

    files = sorted(
        [p for p in SRC.iterdir() if p.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")],
        key=lambda p: p.name.lower(),
    )
    if not files:
        print(f"Keine Bilder in {SRC}.")
        return 1

    mapping = json.loads(MAP_FILE.read_text(encoding="utf-8")) if MAP_FILE.exists() else {}
    used, assigned = set(), {}

    for role, filename in mapping.items():
        match = next((f for f in files if f.name == filename), None)
        if match:
            assigned[role] = match
            used.add(match)

    rest = [f for f in files if f not in used]
    for role, _, _ in ROLES:
        if role in assigned:
            continue
        if rest:
            assigned[role] = rest.pop(0)
        elif role in FALLBACK and FALLBACK[role] in assigned:
            assigned[role] = assigned[FALLBACK[role]]

    print("\nZuschnitt:")
    for role, ratio, focus in ROLES:
        src = assigned.get(role)
        if not src:
            continue
        img = ImageOps.exif_transpose(Image.open(src))
        if img.mode != "RGB":
            img = img.convert("RGB")
        img = finish(crop_to(img, ratio, focus))
        out = DST / f"{role}.jpg"
        img.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print(f"  {role:<11} <- {src.name:<24} {img.width}x{img.height}  {out.stat().st_size // 1024} KB")

    print(f"\nFertig. Dateien liegen in {DST}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
