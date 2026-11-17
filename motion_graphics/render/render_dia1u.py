#!/usr/bin/env python3
"""SU PRIMER DÍA EN T1 con la VOZ DEL USUARIO (Grabación 60) + cierre con llamado a la acción."""
import os, sys, math, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_dia1 as B
from render_dia1 import (W, H, PUR, LIL, LILL, WHITE, INK, IT, ANTON, SANS, word, pop, bg, brackets, tenz_orbit, text_layer, paste, prog, eo, lerp,
                         clamp01, canvas, scale_about)
VOZ = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/ecef1f82-Grabaci_n_60.m4a"
VOFF = 2.4
# frases medidas en la grabación (segundos de la grabación)
SPAN = [(2.68, 5.14), (5.64, 10.76), (11.42, 16.2), (15.2, 19.92), (20.38, 22.64), (23.5, 29.6), (29.8, 36.12), (36.76, 39.8), (40.36, 43.3),
        (45.32, 56.34)]
CTA = {"coment": (45.32, 48.54), "sigue": (49.08, 51.14), "comparte": (51.5, 53.9), "guarda": (53.9, 56.34)}
v = lambda raw: raw - VOFF
B.CUT = [0.0] + [v(s) - .15 for s, _ in SPAN[1:]]
B.at = lambda i, f: v(SPAN[i][0] + (SPAN[i][1] - SPAN[i][0]) * f)
B.DUR = v(56.34) + 2.2
CUT, at, DUR = B.CUT, B.at, B.DUR
def ct(k, f=0): s, e = CTA[k]; return v(s + (e - s) * f)

# ---------------- íconos del llamado a la acción ----------------
def icon_comment(s=150):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((10, 14, s - 10, s - 40), 34, fill=PUR + (255,)); d.polygon([(40, s - 44), (40, s - 8), (78, s - 44)], fill=PUR + (255,))
    for k in range(3): d.ellipse((42 + k * 26, 58, 58 + k * 26, 74), fill=WHITE + (255,))
    return im
def icon_share(s=150):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.polygon([(s * .55, 18), (s - 12, s * .45), (s * .55, s * .78), (s * .55, s * .6), (24, s * .62), (40, s * .3), (s * .55, s * .3)], fill=PUR + (255,))
    return im
def icon_save(s=150, fill=0.0):
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im); pts = [(34, 12), (s - 34, 12), (s - 34, s - 10), (s / 2, s - 46), (34, s - 10)]
    d.polygon(pts, outline=PUR + (255,), width=9)
    if fill > 0:
        m = Image.new("L", (s, s), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
        cut = Image.new("L", (s, s), 0); ImageDraw.Draw(cut).rectangle((0, s * (1 - fill), s, s), fill=255)
        layer = Image.new("RGBA", (s, s), PUR + (255,)); layer.putalpha(Image.fromarray(np.minimum(np.asarray(m), np.asarray(cut)))); im.alpha_composite(layer)
    return im
COMMENT, SHARE = icon_comment(), icon_share()
def follow_btn(clicked):
    w, h = 520, 110; im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 55, fill=(PUR if not clicked else WHITE) + (255,), outline=PUR + (255,), width=6)
    d.text((w / 2, h / 2 - 14), "SIGUIENDO" if clicked else "SEGUIR", font=ANTON(46), fill=(WHITE if not clicked else PUR), anchor="mm")
    d.text((w / 2, h / 2 + 28), "@DuplexDragon_", font=SANS(600, 22), fill=(LILL if not clicked else PUR), anchor="mm"); return im

def scene_cta(T):
    t = T - CUT[9]; im = bg("w", "King")
    tenz_orbit(im, T, t, 360, 1380, 520, max(0, t - .2), crown_t0=CUT[9] + .1, a=1 - .45 * eo(prog(T, ct("sigue"), ct("sigue") + .4)))
    word(im, "¿Tú crees que", IT(400, 52), 360, 100, t, .02, INK)
    word(im, "lo logran?", IT(900, 120), 360, 210, T, ct("coment", .25), PUR)
    # 💬 comentarios
    pc = prog(T, ct("coment", .55), ct("coment", .55) + .4)
    if pc > 0:
        bob = math.sin(T * 6) * 8 * (1 - prog(T, ct("sigue"), ct("sigue") + .3)); pop(im, COMMENT, 600, 400 + bob, T, ct("coment", .55), .35)
        word(im, "comenta", IT(900, 40), 600, 490, T, ct("coment", .6), PUR)
    # SEGUIR con cursor que hace clic
    if T >= ct("sigue"):
        clicked = T > ct("sigue", .6); pop(im, follow_btn(clicked), 360, 640, T, ct("sigue"), .35)
        cp = eo(prog(T, ct("sigue", .15), ct("sigue", .55))); paste(im, B.R.CURSOR if hasattr(B.R, "CURSOR") else canvas(), lerp(650, 420, cp), lerp(900, 660, cp), clamp01(cp * 3), "lt")
    # ↗ compartir
    if T >= ct("comparte"):
        p = eo(prog(T, ct("comparte", .2), ct("comparte", .6))); pop(im, SHARE, 200, 840, T, ct("comparte"), .35)
        if p > 0: paste(im, SHARE.resize((70, 70)), lerp(200, 330, p), lerp(840, 720, p), 1 - p)
        word(im, "comparte", IT(900, 40), 200, 930, T, ct("comparte", .1), PUR)
    # 🔖 guardar
    if T >= ct("guarda"):
        f = eo(prog(T, ct("guarda", .3), ct("guarda", .8))); pop(im, icon_save(150, f), 520, 840, T, ct("guarda"), .35)
        word(im, "guárdalo", IT(900, 40), 520, 930, T, ct("guarda", .1), PUR)
    for k, (s_, x, y, a) in enumerate([("Fuentes: vlr.gg · esports.net · Inven Global · 12–13 nov 2026", 360, 1240, "mm"), ("Clips e imágenes: créditos a sus autores · fan edit", 360, 1262, "mm")]):
        p = prog(t, 1.0 + k * .2, 1.4 + k * .2)
        if p > 0: paste(im, text_layer(s_, SANS(400, 15), (110, 100, 125)), x, y, p, a)
    return im

_scene = B.scene
def scene(i, T): return scene_cta(T) if i == 9 else _scene(i, T)
B.scene = scene

def audio(out):
    SR = 48000; N = int(DUR * SR); A = os.path.join(B.HERE, "..", "audio") + "/"
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    fx = np.zeros((N, 2), np.float32); S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "typing", "clink")}
    ev = [("whoosh", c - .2, .5) for c in CUT[1:]] + [("pop", .3, .4), ("impact", at(1, .45), .7), ("clink", at(1, .75), .5), ("pop", CUT[2] + .15, .5),
          ("typing", CUT[2] + .2, .2), ("punch", at(2, .55), .6), ("pop", CUT[3] + .1, .5), ("punch", at(3, .45), .5), ("shimmer", CUT[4] + .1, .5),
          ("punch", at(5, .6), .5), ("clink", at(5, .5) + .5, .5), ("pop", at(6, .78), .5), ("pop", at(6, .9), .5), ("punch", at(7, .4), .6),
          ("punch", at(8, .3), .6), ("impact", CUT[9], .7), ("pop", ct("coment", .55), .6), ("typing", ct("sigue", .5), .35), ("pop", ct("sigue", .6), .7),
          ("whoosh", ct("comparte", .2), .5), ("pop", ct("guarda", .3), .6), ("shimmer", ct("guarda", .5), .5)]
    for k, t0, g in ev:
        s = S[k]; j = max(0, int(t0 * SR)); n = min(len(s), N - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    sfx = os.path.join(B.D1, "sfx_u.wav"); w = wave.open(sfx, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(fx * .6, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    song = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/e1b3ea4f-HEAVENLY_JUMPSTYLE.mp3"
    f = (f"[0:a]atrim=start={VOFF},asetpts=PTS-STARTPTS,highpass=f=80,acompressor=threshold=-20dB:ratio=3,loudnorm=I=-16:TP=-1.5,aresample=48000,"
         f"aformat=channel_layouts=stereo,apad=whole_dur={DUR},asplit=3[dry][rv][key];[rv][3:a]afir=dry=0:wet=1,highpass=f=200,volume=0.4[wet];"
         f"[dry][wet]amix=inputs=2:normalize=0[vx];[1:a]atrim=start=24,asetpts=PTS-STARTPTS,aresample=48000,volume=0.3[m];"
         f"[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
         f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR},afade=t=out:st={DUR - 1.6}:d=1.6,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VOZ, "-i", song, "-i", sfx, "-i", os.path.join(B.TZ, "reverb_ir.wav"),
                    "-filter_complex", f, "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [B.frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for k, x in enumerate(ims): sh.paste(x, (k * W // 2, 0))
        sh.save(os.path.join(B.HERE, "preview.jpg"), quality=88); print("preview", [round(c, 2) for c in CUT], round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(B.D1, "mezcla_u.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(B.FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * B.FPS)
    for k in range(n): p.stdin.write(B.frame(k / B.FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
