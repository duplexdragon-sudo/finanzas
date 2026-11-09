"""Sube a YouTube Shorts los Reels de Valorant de @duplex_dragon.

1. Baja cada Reel de Instagram con yt-dlp (o usa tu archivo original si lo pones en
   la carpeta videos/ con el nombre <codigo>.mp4).
2. Abre YouTube Studio en Brave (o Chrome/Edge) con tu sesión (la primera vez inicias sesión
   a mano; queda guardada en la carpeta perfil/).
3. Sube cada video con su título y descripción de shorts.json, marca "No es para
   niños" y lo deja público o programado.
4. Anota en progreso.json lo que ya subió, para no repetir.

Uso:
    python subir_shorts.py --solo-bajar          # solo descarga los videos
    python subir_shorts.py --cuantos 1           # sube el siguiente (recomendado: 1 al día)
    python subir_shorts.py --cuantos 1 --ver     # pausa antes de publicar para revisar
    python subir_shorts.py --privado             # los sube en privado (para probar)
"""
import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
VIDEOS = AQUI / "videos"
PERFIL = AQUI / "perfil"
PROGRESO = AQUI / "progreso.json"
SHORTS = json.loads((AQUI / "shorts.json").read_text(encoding="utf-8"))
STUDIO = "https://studio.youtube.com"


def buscar_navegador():
    """Brave primero (el de Carlos), luego Chrome y Edge."""
    import os
    rutas = []
    for base in (os.environ.get("PROGRAMFILES", r"C:\Program Files"),
                 os.environ.get("PROGRAMFILES(X86)", r"C:\Program Files (x86)"),
                 os.environ.get("LOCALAPPDATA", "")):
        if base:
            rutas += [Path(base) / "BraveSoftware/Brave-Browser/Application/brave.exe",
                      Path(base) / "Google/Chrome/Application/chrome.exe",
                      Path(base) / "Microsoft/Edge/Application/msedge.exe"]
    for r in rutas:
        if r.exists():
            return str(r)
    return None


def leer_progreso():
    try:
        return json.loads(PROGRESO.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def guardar_progreso(p):
    PROGRESO.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")


COOKIES = AQUI / "cookies.txt"


def exportar_cookies(nav):
    """Guarda las cookies de Instagram de la ventana de la herramienta en formato de yt-dlp."""
    lineas = ["# Netscape HTTP Cookie File"]
    hay_sesion = False
    for c in nav.cookies("https://www.instagram.com"):
        dom = c["domain"]
        hay_sesion |= c["name"] == "sessionid"
        lineas.append("\t".join([dom, "TRUE" if dom.startswith(".") else "FALSE", c.get("path", "/"),
                                 "TRUE" if c.get("secure") else "FALSE",
                                 str(int(c["expires"])) if c.get("expires", -1) > 0 else "0",
                                 c["name"], c["value"]]))
    COOKIES.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    return hay_sesion


def bajar(item, cookies_de=None, nav=None, page=None):
    VIDEOS.mkdir(exist_ok=True)
    for ext in (".mp4", ".mov"):
        f = VIDEOS / f"{item['codigo']}{ext}"
        if f.exists():
            return f
    destino = VIDEOS / f"{item['codigo']}.mp4"
    base = [sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "-f", "mp4/best", "-o", str(destino)]
    print(f"  Bajando {item['instagram']}")
    intentos = [[]]
    if cookies_de:
        intentos.append(["--cookies-from-browser", cookies_de])
    if nav is not None:
        intentos.append("ventana")
    for extra in intentos:
        if extra == "ventana":
            if not exportar_cookies(nav):
                page.goto("https://www.instagram.com/accounts/login/")
                input("  Instagram pide sesión: inicia sesión en Instagram en la ventana de Brave "
                      "y pulsa Enter aquí... ")
                exportar_cookies(nav)
            extra = ["--cookies", str(COOKIES)]
        subprocess.run(base + extra + [item["instagram"]])
        if destino.exists():
            return destino
    print(f"  ✗ No se pudo bajar. Guarda el video a mano como videos/{item['codigo']}.mp4")
    return None


def primero(page, selectores, timeout=60_000):
    """Devuelve el primer elemento visible de una lista de selectores (YouTube cambia su página)."""
    fin = time.time() + timeout / 1000
    while time.time() < fin:
        for sel in selectores:
            loc = page.locator(sel)
            try:
                for i in range(loc.count()):
                    if loc.nth(i).is_visible():
                        return loc.nth(i)
            except Exception:
                pass
        time.sleep(0.5)
    raise RuntimeError(f"No encontré en la página: {selectores[0]}")


def escribir(caja, page, texto):
    caja.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    page.keyboard.insert_text(texto)


def subir(page, item, archivo, privado, ver):
    # Ir directo al cuadro de subida (sin depender del botón "Crear")
    page.goto("https://www.youtube.com/upload", wait_until="domcontentloaded")
    entrada = page.locator("input[type=file]").first
    entrada.wait_for(state="attached", timeout=60_000)
    entrada.set_input_files(str(archivo))

    cajas = ["#title-textarea #textbox", "ytcp-video-title #textbox", "#textbox[contenteditable=true]"]
    titulo = primero(page, cajas, 180_000)
    time.sleep(3)
    escribir(titulo, page, item["titulo"])
    desc = primero(page, ["#description-textarea #textbox", "ytcp-video-description #textbox"], 30_000)
    escribir(desc, page, item["descripcion"])

    primero(page, ["tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']",
                   "[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']",
                   "text=/no es contenido creado para ni|not made for kids/i"], 30_000).click()

    for _ in range(3):  # Detalles → Elementos → Comprobaciones → Visibilidad
        primero(page, ["#next-button", "ytcp-button#next-button"], 30_000).click()
        time.sleep(2)

    nombre = "PRIVATE" if privado else "PUBLIC"
    primero(page, [f"tp-yt-paper-radio-button[name='{nombre}']", f"[name='{nombre}']"], 30_000).click()

    # Espera a que termine de subir (el botón Publicar se habilita y desaparece el % de subida)
    hecho = primero(page, ["#done-button", "ytcp-button#done-button"], 30_000)
    barra = page.locator("ytcp-video-upload-progress")
    for _ in range(900):
        try:
            texto = barra.first.inner_text(timeout=2_000) if barra.count() else ""
        except Exception:
            texto = ""
        if hecho.is_enabled() and "%" not in texto:
            break
        time.sleep(1)

    if ver:
        input("  Revisa el video en el navegador y pulsa Enter para publicarlo (Ctrl+C para cancelar)... ")
    hecho.click()
    time.sleep(6)
    enlace = ""
    try:
        enlace = page.locator("a[href*='youtube.com/shorts/'], a[href*='youtu.be/']").first.get_attribute("href", timeout=20_000) or ""
    except Exception:
        pass
    try:
        page.locator("#close-button").first.click(timeout=10_000)
    except Exception:
        pass
    return enlace


def abrir_navegador(pw):
    exe = buscar_navegador()
    if not exe:
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    return pw.chromium.launch_persistent_context(str(PERFIL), headless=False, executable_path=exe,
                                                 viewport={"width": 1400, "height": 900},
                                                 args=["--disable-blink-features=AutomationControlled"])


def revisar(progreso):
    """Lista lo subido y lee la tabla de Shorts de YouTube Studio (visibilidad, restricciones, vistas)."""
    print("\nSubidos con la herramienta:")
    for i, (cod, d) in enumerate(progreso.items(), 1):
        print(f"  {i}. {d['titulo']}\n     {d.get('enlace') or '(sin enlace)'}  ·  {d['fecha']}")
    from playwright.sync_api import sync_playwright
    with sync_playwright() as pw:
        nav = abrir_navegador(pw)
        page = nav.pages[0] if nav.pages else nav.new_page()
        page.goto("https://studio.youtube.com/channel/UCYlEih7xACf_uOIzXgE-ckg/videos/short")
        try:
            page.locator("ytcp-video-row").first.wait_for(timeout=60_000)
            time.sleep(3)
        except Exception:
            print("\nNo pude leer la tabla de YouTube Studio.")
        filas = page.locator("ytcp-video-row")
        print("\nYouTube Studio (Shorts más recientes):")
        for i in range(min(filas.count(), len(progreso) + 2)):
            texto = " | ".join(t.strip() for t in filas.nth(i).inner_text().splitlines() if t.strip())
            print(f"  - {texto}")
        page.screenshot(path=str(AQUI / "revisar.png"))
        print(f"\nCaptura guardada en {AQUI / 'revisar.png'}")
        try:
            nav.close()
        except Exception:
            pass


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cuantos", type=int, default=1, help="cuántos subir en esta corrida (default 1)")
    ap.add_argument("--solo-bajar", action="store_true", help="solo descargar los videos")
    ap.add_argument("--privado", action="store_true", help="subir en privado en vez de público")
    ap.add_argument("--ver", action="store_true", help="pausar antes de publicar cada video")
    ap.add_argument("--revisar", action="store_true", help="mostrar el estado de los Shorts subidos")
    ap.add_argument("--cookies-de", metavar="NAVEGADOR", help="usar tu sesión de Instagram de chrome/edge/firefox para bajar")
    a = ap.parse_args()

    progreso = leer_progreso()
    pendientes = [s for s in SHORTS if s["codigo"] not in progreso]
    print(f"{len(SHORTS) - len(pendientes)} subidos, {len(pendientes)} pendientes.")

    if a.revisar:
        revisar(progreso)
        return

    if a.solo_bajar:
        for s in pendientes:
            bajar(s, a.cookies_de)
        return

    lote = pendientes[: a.cuantos]
    if not lote:
        print("¡Ya están todos subidos!")
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as pw:
        exe = buscar_navegador()
        print(f"Navegador: {exe or 'Chromium de Playwright'}")
        if not exe:
            subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
        nav = pw.chromium.launch_persistent_context(str(PERFIL), headless=False, executable_path=exe,
                                                    viewport={"width": 1400, "height": 900},
                                                    args=["--disable-blink-features=AutomationControlled"])
        page = nav.pages[0] if nav.pages else nav.new_page()
        page.goto(STUDIO)
        page.wait_for_load_state("domcontentloaded")
        if "accounts.google.com" in page.url or "studio.youtube.com" not in page.url:
            input("Inicia sesión en YouTube con la cuenta de DuplexDragon en la ventana que se abrió "
                  "y, cuando veas YouTube Studio, pulsa Enter aquí... ")
        for s in lote:
            print(f"\n▶ {s['titulo']}")
            archivo = bajar(s, a.cookies_de, nav, page)
            if not archivo:
                continue
            try:
                enlace = subir(page, s, archivo, a.privado, a.ver)
            except Exception as e:
                try:
                    page.screenshot(path=str(AQUI / "error.png"))
                except Exception:
                    pass
                print(f"  ✗ Falló la subida: {str(e).splitlines()[0]}\n"
                      f"  Guardé una captura en {AQUI / 'error.png'}: mándasela a Claude.")
                input("  Pulsa Enter para cerrar... ")
                break
            progreso[s["codigo"]] = {"titulo": s["titulo"], "enlace": enlace, "fecha": time.strftime("%Y-%m-%d %H:%M")}
            guardar_progreso(progreso)
            print(f"  ✓ Subido {enlace}")
        try:
            nav.close()
        except Exception:
            pass
    print(f"\nListo. Quedan {len([s for s in SHORTS if s['codigo'] not in progreso])} por subir.")


if __name__ == "__main__":
    main()
