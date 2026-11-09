"""Cambia el texto (caption) de los 20 Reels de Valorant de @duplex_dragon en Instagram.

Usa la misma ventana de Brave que subir_shorts.py (la sesión queda guardada en perfil/).
Instagram no permite editar captions por su API, así que lo hace como tú: abre el Reel,
⋯ → Editar, borra el texto, pega el nuevo de textos_ig.json y toca Listo.

Uso:
    py editar_instagram.py --cuantos 1 --ver     # el primero, pausando para revisar
    py editar_instagram.py --cuantos 20          # todos los que falten
"""
import argparse
import json
import re
import time

from subir_shorts import AQUI, abrir_navegador

TEXTOS = json.loads((AQUI / "textos_ig.json").read_text(encoding="utf-8"))
PROGRESO = AQUI / "ig_progreso.json"

MAS = re.compile(r"más opciones|more options|opciones", re.I)
EDITAR = re.compile(r"^\s*(editar|edit)\s*$", re.I)
LISTO = re.compile(r"^\s*(listo|hecho|done|guardar|save)\s*$", re.I)


def leer():
    try:
        return json.loads(PROGRESO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def boton(page, nombre, timeout=20_000):
    fin = time.time() + timeout / 1000
    while time.time() < fin:
        for loc in (page.get_by_role("button", name=nombre), page.get_by_role("menuitem", name=nombre),
                    page.get_by_text(nombre)):
            try:
                for i in range(loc.count()):
                    if loc.nth(i).is_visible():
                        return loc.nth(i)
            except Exception:
                pass
        time.sleep(0.5)
    raise RuntimeError(f"No encontré el botón {nombre.pattern}")


def editar(page, item, ver):
    page.goto(f"https://www.instagram.com/p/{item['codigo']}/", wait_until="domcontentloaded")
    time.sleep(4)
    mas = page.locator("svg[aria-label='Más opciones'], svg[aria-label='More options'], svg[aria-label='Más opciones.']")
    mas.first.wait_for(timeout=30_000)
    mas.first.click()
    boton(page, EDITAR).click()
    caja = page.locator("div[role='textbox'][contenteditable='true'], div[contenteditable='true'][aria-label]").first
    caja.wait_for(timeout=30_000)
    caja.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    lineas = item["texto"].split("\n")
    for i, linea in enumerate(lineas):
        if linea:
            page.keyboard.insert_text(linea)
        if i < len(lineas) - 1:
            page.keyboard.press("Enter")
    time.sleep(1)
    if ver:
        input("  Revisa el texto en Brave y pulsa Enter para guardarlo (Ctrl+C para cancelar)... ")
    boton(page, LISTO).click()
    time.sleep(4)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cuantos", type=int, default=20)
    ap.add_argument("--ver", action="store_true", help="pausar antes de guardar cada texto")
    a = ap.parse_args()
    hechos = leer()
    pendientes = [t for t in TEXTOS if t["codigo"] not in hechos][: a.cuantos]
    print(f"{len(hechos)} editados, {len(TEXTOS) - len(hechos)} pendientes.")
    if not pendientes:
        print("¡Ya están todos!")
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = abrir_navegador(pw)
        page = nav.pages[0] if nav.pages else nav.new_page()
        page.goto("https://www.instagram.com/")
        time.sleep(4)
        while not any(c["name"] == "sessionid" and c["value"] for c in nav.cookies("https://www.instagram.com")):
            input("Instagram no tiene la sesión abierta. En la ventana de Brave toca 'Usar otro perfil' "
                  "e inicia sesión con @duplex_dragon. Cuando veas tu inicio de Instagram, pulsa Enter aquí... ")
        page.goto("https://www.instagram.com/duplex_dragon/")
        time.sleep(4)
        if not page.get_by_text(re.compile(r"editar perfil|edit profile", re.I)).count():
            input("Parece que la sesión no es de @duplex_dragon. Cambia de cuenta en Brave y pulsa Enter... ")
        for t in pendientes:
            print(f"\n▶ {t['agente']}  (instagram.com/reel/{t['codigo']})")
            try:
                editar(page, t, a.ver)
            except Exception as e:
                try:
                    page.screenshot(path=str(AQUI / "error_ig.png"))
                except Exception:
                    pass
                print(f"  ✗ Falló: {str(e).splitlines()[0]}\n  Captura en {AQUI / 'error_ig.png'}: mándasela a Claude.")
                input("  Pulsa Enter para cerrar... ")
                break
            hechos[t["codigo"]] = time.strftime("%Y-%m-%d %H:%M")
            PROGRESO.write_text(json.dumps(hechos, indent=2), encoding="utf-8")
            print("  ✓ Texto cambiado")
        try:
            nav.close()
        except Exception:
            pass
    print(f"\nListo. Quedan {len(TEXTOS) - len(hechos)}.")


if __name__ == "__main__":
    main()
