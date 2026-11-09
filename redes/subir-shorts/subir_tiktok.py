"""Sube a TikTok los Reels de Valorant de @duplex_dragon con los textos de tiktok.json.

Usa la misma ventana de Brave (sesión guardada en perfil/). Baja cada Reel de Instagram
(o usa videos/<codigo>.mp4 si ya está), abre TikTok Studio, sube el video, pega el texto
y publica.

Uso:
    py subir_tiktok.py --ver          # sube el siguiente, pausando para revisar
    py subir_tiktok.py                # sube el siguiente (1 por día)
    py subir_tiktok.py --cuantos 2    # sube 2
"""
import argparse
import json
import re
import time

from subir_shorts import AQUI, abrir_navegador, bajar

TEXTOS = json.loads((AQUI / "tiktok.json").read_text(encoding="utf-8"))
PROGRESO = AQUI / "tiktok_progreso.json"
SUBIR = "https://www.tiktok.com/tiktokstudio/upload?from=upload"
PUBLICAR = re.compile(r"^\s*(publicar|post)\s*$", re.I)
AHORA = re.compile(r"publicar ahora|post now", re.I)


def leer():
    try:
        return json.loads(PROGRESO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def con_sesion(nav):
    return any(c["name"] == "sessionid" and c["value"] for c in nav.cookies("https://www.tiktok.com"))


def escribir_texto(page, texto, codigo):
    # La caja de descripción visible, que TikTok llena con el nombre del archivo
    cajas = page.locator("div[contenteditable='true']")
    caja = None
    fin = time.time() + 180
    while time.time() < fin and caja is None:
        for i in range(cajas.count()):
            c = cajas.nth(i)
            try:
                if c.is_visible() and codigo in (c.inner_text() or ""):
                    caja = c
                    break
            except Exception:
                pass
        time.sleep(1)
    if caja is None:
        raise RuntimeError("No encontré la caja de descripción de TikTok")
    time.sleep(1)
    try:
        caja.click(timeout=8_000)
    except Exception:
        caja.focus()
    page.keyboard.press("End")
    for _ in range(3):
        page.keyboard.press("Control+A")
        page.keyboard.press("Backspace")
        time.sleep(0.3)
        if not (caja.inner_text() or "").strip():
            break
    if codigo in (caja.inner_text() or ""):
        raise RuntimeError("No pude borrar el nombre del archivo en la descripción")
    lineas = texto.split("\n")
    for i, linea in enumerate(lineas):
        if linea.startswith("#"):
            # Hashtags uno por uno: espacio para cerrar la lista de sugerencias de TikTok
            for tag in linea.split():
                page.keyboard.insert_text(tag)
                time.sleep(1.2)
                page.keyboard.press("Space")
                time.sleep(0.4)
            page.keyboard.press("Escape")
        else:
            if linea:
                page.keyboard.insert_text(linea)
            if i < len(lineas) - 1:
                page.keyboard.press("Enter")
    time.sleep(1)
    if lineas[0][:20] not in (caja.inner_text() or ""):
        raise RuntimeError("El texto no quedó escrito en la descripción")


def bajar_portada(page, item):
    """Baja la portada del Reel de Instagram (la misma imagen que se ve en el perfil)."""
    destino = AQUI / "videos" / f"{item['codigo']}.jpg"
    if destino.exists():
        return destino
    urls = [item.get("portada")]
    try:
        p2 = page.context.new_page()
        p2.goto(item["instagram"], wait_until="domcontentloaded")
        time.sleep(3)
        og = p2.locator("meta[property='og:image']").first.get_attribute("content", timeout=5_000)
        p2.close()
        urls.append(og)
    except Exception:
        pass
    for u in urls:
        if not u:
            continue
        try:
            r = page.context.request.get(u, timeout=30_000)
            if r.ok and len(r.body()) > 5_000:
                destino.write_bytes(r.body())
                return destino
        except Exception:
            pass
    return None


def poner_portada(page, imagen):
    """Editar portada → Cargar portada → imagen de Instagram → Confirmar. Si falla, deja la de TikTok."""
    try:
        page.get_by_text(re.compile(r"editar portada|edit cover", re.I)).first.click(timeout=15_000)
        time.sleep(2)
        page.get_by_text(re.compile(r"cargar portada|subir portada|upload cover", re.I)).first.click(timeout=10_000)
        time.sleep(1)
        page.locator("input[type=file][accept*='image']").last.set_input_files(str(imagen))
        time.sleep(4)
        page.get_by_role("button", name=re.compile(r"^\s*(confirmar|guardar|listo|confirm|save|done)\s*$", re.I)).last.click(timeout=15_000)
        time.sleep(2)
        print("  ✓ Portada de Instagram puesta")
    except Exception as e:
        print(f"  ! No pude poner la portada ({str(e).splitlines()[0][:80]}); queda la de TikTok.")
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass


def subir(page, item, archivo, ver):
    page.goto(SUBIR, wait_until="domcontentloaded")
    entrada = page.locator("input[type=file]").first
    entrada.wait_for(state="attached", timeout=60_000)
    entrada.set_input_files(str(archivo))
    escribir_texto(page, item["texto"], item["codigo"])
    imagen = bajar_portada(page, item)
    if imagen:
        poner_portada(page, imagen)
    else:
        print("  ! No pude bajar la portada de Instagram; queda la de TikTok.")

    boton = page.locator("button[data-e2e='post_video_button']")
    if not boton.count():
        boton = page.get_by_role("button", name=PUBLICAR)
    boton = boton.first
    # Espera a que termine de subir (el botón Publicar se habilita)
    for _ in range(600):
        try:
            if boton.is_enabled() and boton.get_attribute("aria-disabled") != "true" \
                    and boton.get_attribute("data-disabled") != "true":
                break
        except Exception:
            pass
        time.sleep(1)
    time.sleep(3)
    if ver:
        input("  Revisa el video y el texto en Brave y pulsa Enter para publicar (Ctrl+C para cancelar)... ")
    boton.click()
    time.sleep(3)
    try:  # TikTok a veces pregunta si publicar antes de terminar su revisión
        page.get_by_role("button", name=AHORA).first.click(timeout=5_000)
    except Exception:
        pass
    time.sleep(8)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cuantos", type=int, default=1)
    ap.add_argument("--ver", action="store_true", help="pausar antes de publicar")
    a = ap.parse_args()
    hechos = leer()
    pendientes = [t for t in TEXTOS if t["codigo"] not in hechos][: a.cuantos]
    print(f"{len(hechos)} subidos a TikTok, {len(TEXTOS) - len(hechos)} pendientes.")
    if not pendientes:
        print("¡Ya están todos!")
        return
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = abrir_navegador(pw)
        page = nav.pages[0] if nav.pages else nav.new_page()
        page.goto("https://www.tiktok.com/")
        time.sleep(3)
        while not con_sesion(nav):
            page.goto("https://www.tiktok.com/login")
            input("Inicia sesión en TikTok en la ventana de Brave y pulsa Enter aquí... ")
        for t in pendientes:
            print(f"\n▶ {t['agente']}")
            archivo = bajar(t, None, nav, page)
            if not archivo:
                continue
            try:
                subir(page, t, archivo, a.ver)
            except Exception as e:
                try:
                    page.screenshot(path=str(AQUI / "error_tiktok.png"))
                except Exception:
                    pass
                print(f"  ✗ Falló: {str(e).splitlines()[0]}\n  Captura en {AQUI / 'error_tiktok.png'}: mándasela a Claude.")
                input("  Pulsa Enter para cerrar... ")
                break
            hechos[t["codigo"]] = time.strftime("%Y-%m-%d %H:%M")
            PROGRESO.write_text(json.dumps(hechos, indent=2), encoding="utf-8")
            print("  ✓ Publicado en TikTok")
        try:
            nav.close()
        except Exception:
            pass
    print(f"\nListo. Quedan {len(TEXTOS) - len(hechos)}.")


if __name__ == "__main__":
    main()
