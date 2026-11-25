#!/usr/bin/env python3
"""Revisa qué material recibido (fotos, logos, clips, recortes) usa cada vídeo y cuál quedó sin usar.
Uso: python3 inventario.py  → tabla por proyecto."""
import os, re, glob
B = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROY = {"prx": "render_prx.py", "fnc": "render_fnc.py", "vit": "render_vit.py", "zek": "render_zek.py", "lev": "render_lev.py",
        "evento": "render_vlog_monster.py", "c9": "render_c9.py"}
EXT = (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov")
for p, scr in PROY.items():
    src = ""
    if scr and os.path.exists(os.path.join(B, "edit", scr)):
        src = open(os.path.join(B, "edit", scr)).read()
        for m in re.findall(r"import (\w+)", src):
            f = os.path.join(B, "edit", m + ".py")
            if os.path.exists(f) and m.startswith(("cierre", "portada")): src += open(f).read()
    items = []
    for sub in ("fotos", "logos", "clips", "rec", "ev", "tomas", "fotos_ev"):
        for f in sorted(glob.glob(os.path.join(B, p, sub, "*"))):
            if f.lower().endswith(EXT): items.append((sub, os.path.basename(f)))
    if not items: print(f"\n== {p}: sin material recibido"); continue
    usados = [i for i in items if os.path.splitext(i[1])[0] in src]
    sin = [i for i in items if i not in usados]
    print(f"\n== {p} ({scr}): {len(usados)}/{len(items)} usados")
    for sub, n in sin: print(f"   ✗ SIN USAR  {sub}/{n}")
