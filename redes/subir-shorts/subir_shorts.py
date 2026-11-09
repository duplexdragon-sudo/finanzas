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


def bajar(item, cookies_de):
    VIDEOS.mkdir(exist_ok=True)
    for ext in (".mp4", ".mov"):
        f = VIDEOS / f"{item['codigo']}{ext}"
        if f.exists():
            return f
    destino = VIDEOS / f"{item['codigo']}.mp4"
    cmd = [sys.executable, "-m", "yt_dlp", "-f", "mp4/best", "-o", str(destino), item["instagram"]]
    if cookies_de:
        cmd[3:3] = ["--cookies-from-browser", cookies_de]
    print(f"  Bajando {item['instagram']}")
    r = subprocess.run(cmd)
    if r.returncode != 0 or not destino.exists():
        print(f"  ✗ No se pudo bajar. Guarda el video a mano como videos/{item['codigo']}.mp4"
              " (o prueba con --cookies-de chrome).")
        return None
    return destino


def escribir(page, selector, texto):
    caja = page.locator(selector).first
    caja.click()
    page.keyboard.press("Control+A")
    page.keyboard.press("Delete")
    caja.fill(texto)


def subir(page, item, archivo, privado, ver):
    page.goto(f"{STUDIO}/", wait_until="domcontentloaded")
    page.locator("#create-icon").first.click()
    page.locator("#text-item-0").first.click()  # "Subir videos"
    page.locator("input[type=file]").first.set_input_files(str(archivo))

    page.locator("#title-textarea #textbox").first.wait_for(timeout=120_000)
    time.sleep(2)
    escribir(page, "#title-textarea #textbox", item["titulo"])
    escribir(page, "#description-textarea #textbox", item["descripcion"])
    page.locator("tp-yt-paper-radio-button[name='VIDEO_MADE_FOR_KIDS_NOT_MFK']").first.click()

    for _ in range(3):  # Detalles → Elementos → Comprobaciones → Visibilidad
        page.locator("#next-button").first.click()
        time.sleep(1.5)

    page.locator(f"tp-yt-paper-radio-button[name='{'PRIVATE' if privado else 'PUBLIC'}']").first.click()

    # Espera a que termine de subir (el botón Publicar se habilita y desaparece el % de subida)
    hecho = page.locator("#done-button").first
    barra = page.locator("ytcp-video-upload-progress")
    for _ in range(600):
        texto = barra.first.inner_text(timeout=2_000) if barra.count() else ""
        if hecho.is_enabled() and "%" not in texto:
            break
        time.sleep(1)

    if ver:
        input("  Revisa el video en el navegador y pulsa Enter para publicarlo (Ctrl+C para cancelar)... ")
    hecho.click()
    time.sleep(5)
    enlace = ""
    try:
        enlace = page.locator("ytcp-video-info a, a.ytcp-video-info").first.get_attribute("href", timeout=15_000) or ""
    except Exception:
        pass
    try:
        page.locator("#close-button").first.click(timeout=10_000)
    except Exception:
        pass
    return enlace


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cuantos", type=int, default=1, help="cuántos subir en esta corrida (default 1)")
    ap.add_argument("--solo-bajar", action="store_true", help="solo descargar los videos")
    ap.add_argument("--privado", action="store_true", help="subir en privado en vez de público")
    ap.add_argument("--ver", action="store_true", help="pausar antes de publicar cada video")
    ap.add_argument("--cookies-de", metavar="NAVEGADOR", help="usar tu sesión de Instagram de chrome/edge/firefox para bajar")
    a = ap.parse_args()

    progreso = leer_progreso()
    pendientes = [s for s in SHORTS if s["codigo"] not in progreso]
    print(f"{len(SHORTS) - len(pendientes)} subidos, {len(pendientes)} pendientes.")

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
        if "accounts.google.com" in page.url or not page.locator("#create-icon").count():
            input("Inicia sesión en YouTube con la cuenta de DuplexDragon en la ventana que se abrió "
                  "y, cuando veas YouTube Studio, pulsa Enter aquí... ")
        for s in lote:
            print(f"\n▶ {s['titulo']}")
            archivo = bajar(s, a.cookies_de)
            if not archivo:
                continue
            try:
                enlace = subir(page, s, archivo, a.privado, a.ver)
            except Exception as e:
                print(f"  ✗ Falló la subida: {e}\n  Revisa la ventana; YouTube pudo cambiar su página.")
                break
            progreso[s["codigo"]] = {"titulo": s["titulo"], "enlace": enlace, "fecha": time.strftime("%Y-%m-%d %H:%M")}
            guardar_progreso(progreso)
            print(f"  ✓ Subido {enlace}")
        nav.close()
    print(f"\nListo. Quedan {len([s for s in SHORTS if s['codigo'] not in progreso])} por subir.")


if __name__ == "__main__":
    main()
