#!/usr/bin/env python3
"""Convert local images to AVIF and report sizes."""

import unicodedata
from pathlib import Path
from PIL import Image

BASE = Path(__file__).parent
FOTOS = BASE / "fotos"
SERVICOS_SRC = BASE / "FOTOS SERVIÇOS"

# (source_name, max_width, quality)
IMAGES = [
    ("troca de bateria.png",    1200, 55),
    ("caiu na água.jpeg",       1200, 55),
    ("iphone não carrega.jpeg", 1200, 55),
    ("bateria ruim.jpeg",       1200, 55),
]

# Fotos reais dos serviços de informática (config/services.json + content/services/*.html).
# Quality mais alta (80) a pedido do cliente: preservar qualidade visual dessas fotos.
# (source_name, max_width, quality, dest_name)
SERVICE_IMAGES = [
    ("backup.jpg",                  1200, 80, "backup.avif"),
    ("conserto computador.jpg",     1200, 80, "conserto-de-computador.avif"),
    ("formatar computador.jpg",     1200, 80, "formatacao.avif"),
    ("instalar windows.jpg",        1200, 80, "instalacao-do-windows.avif"),
    ("instalação de drivers.jpg",   1200, 80, "instalacao-de-drivers.avif"),
    ("limpeza interna.jpg",         1200, 80, "limpeza-interna.avif"),
    ("manutenção preventiva.jpg",   1200, 80, "manutencao-preventiva.avif"),
    ("recuperação de dados.jpg",    1200, 80, "recuperacao-de-dados.avif"),
    ("remover virus.jpg",           1200, 80, "remocao-de-virus.avif"),
    ("reparo de placa mae.jpg",     1200, 80, "reparo-de-placa-mae.avif"),
    ("troca de hd.jpg",             1200, 80, "troca-de-hd.avif"),
    ("upgrade SSD.jpg",             1200, 80, "upgrade-de-ssd.avif"),
]

def convert(src_name, max_width, quality, src_dir=FOTOS, dest_dir=FOTOS, dest_name=None,
            fallback_quality=None):
    src = src_dir / src_name
    if not src.exists():
        print(f"  SKIP (not found): {src_name}")
        return

    if dest_name is None:
        stem = src.stem.replace(" ", "-").lower()
        # normalise accented chars
        stem = unicodedata.normalize("NFD", stem)
        stem = "".join(c for c in stem if unicodedata.category(c) != "Mn")
        dest_name = stem + ".avif"
    dest = dest_dir / dest_name

    img = Image.open(src)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    w, h = img.size
    if w > max_width:
        ratio = max_width / w
        img = img.resize((max_width, int(h * ratio)), Image.LANCZOS)
        new_w, new_h = img.size
    else:
        new_w, new_h = w, h

    img.save(dest, format="AVIF", quality=quality)

    src_kb  = src.stat().st_size / 1024
    dest_kb = dest.stat().st_size / 1024
    saving  = (1 - dest_kb / src_kb) * 100
    print(f"    {src_kb:,.0f} KB  ->  {dest_kb:,.0f} KB  (-{saving:.0f}%)  [{new_w}x{new_h}]  ->  {dest_name}")

    if fallback_quality is not None:
        # JPEG <picture> fallback for browsers without AVIF support, same processed size.
        fallback_dest = dest_dir / (dest.stem + ".jpg")
        img.save(fallback_dest, format="JPEG", quality=fallback_quality)
        fallback_kb = fallback_dest.stat().st_size / 1024
        print(f"                                     fallback -> {fallback_kb:,.0f} KB  -> {fallback_dest.name}")

print("\n=== Converting images to AVIF ===\n")
for item in IMAGES:
    convert(*item)

print("\n=== Converting service photos (FOTOS SERVIÇOS/) to AVIF ===\n")
for src_name, max_width, quality, dest_name in SERVICE_IMAGES:
    convert(src_name, max_width, quality, src_dir=SERVICOS_SRC, dest_name=dest_name,
            fallback_quality=85)

print("\nDone.\n")
