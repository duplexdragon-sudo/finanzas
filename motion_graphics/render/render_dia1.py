#!/usr/bin/env python3
"""SU PRIMER DÍA EN T1 — estilo morado editorial. Voz ElevenLabs por frase (../dia1/voz/lXX.wav)."""
import os, sys, math, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import render_tenz_morado as R
from render_tenz_morado import (W, H, PUR, LIL, LILL, WHITE, INK, ANTON, IT, word, pop, bg, obj, duo, card, ghost_tenz, ribbons, brackets,
                                puzzle_tile, tenz_orbit, FACES, T1_W, VLOGO, TW_BACK, COL, KING, HOUR, MON, CROWN, T2, clamp01, text_layer, paste,
                                prog, eo, lerp, SANS, canvas, scale_about)
HERE = os.path.dirname(os.path.abspath(__file__)); D1 = os.path.join(HERE, "..", "dia1"); TZ = os.path.join(HERE, "..", "tenz")
FPS = 30
DL = []
for i in range(10):
    w = wave.open(os.path.join(D1, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
LS = []; t = .5
for d in DL: LS.append(t); t += d + .4
DUR = LS[-1] + DL[-1] + 2.6
CUT = [0.0] + [s - .15 for s in LS[1:]]
def at(i, f): return LS[i] + DL[i] * f        # momento dentro de la frase i (f = 0..1)

EYE = obj("20_ojo", 300); BRAIN = obj("21_cerebro", 300); HEAD = obj("27_audifonos", 300); CUP = obj("45_copa", 330)
def note_back():
    n = obj("44_nota", w=660); tw = TW_BACK.resize((400, int(TW_BACK.height * 400 / TW_BACK.width)), Image.LANCZOS).rotate(-3, expand=True, resample=Image.BICUBIC)
    n = n.copy(); n.alpha_composite(tw, (int(n.width * .54 - tw.width / 2), int(n.height * .56 - tw.height / 2))); return n
NOTE = note_back()
BIG_FACES = {k: R.face(k, (230, 290)) for k in ("tenz", "crashies")}

def scene(i, T):
    t = T - CUT[i]
    if i == 0:   # 12 de noviembre · Corea
        im = bg("w", "Corea")
        rib = Image.new("RGBA", (560, 86), PUR + (255,)); ImageDraw.Draw(rib).text((280, 45), "SU PRIMER DÍA EN T1", font=ANTON(54), fill=WHITE, anchor="mm")
        p = eo(prog(t, .1, .45)); paste(im, rib.crop((0, 0, max(1, int(560 * p)), 86)), 80, 150, 1, "lm")
        pop(im, HOUR, 360, 860, t, .2, .45)
        word(im, "12 · noviembre · 2026", IT(400, 48), 360, 240, T, at(0, 0), INK)
        word(im, "Corea", IT(900, 130), 360, 360, T, at(0, .55), PUR)
        return im
    if i == 1:   # T1 publica: The KING is back
        im = bg("p", "KING"); ghost_tenz(im, t, .15)
        word(im, "3:00 de la mañana en Europa", IT(400, 44), 360, 170, t, .05, LILL)
        pop(im, T1_W, 360, 390, T, at(1, .45), .4)
        word(im, "The King", IT(900, 120), 360, 520, T, at(1, .7), WHITE); word(im, "is back", IT(400, 80), 400, 620, T, at(1, .82), LILL)
        p = eo(prog(T, at(1, .7), at(1, .7) + .5)); paste(im, CROWN.resize((360, int(CROWN.height * 360 / CROWN.width))), 360, lerp(-200, 930, p) + math.sin(T * 2.4) * 8, clamp01(p * 3))
        return im
    if i == 2:   # 11 minutos después: I'm back
        im = bg("w"); ribbons(im, t)
        pop(im, NOTE, 360, 870, t, .1, .45)
        word(im, "11 minutos después", IT(400, 50), 360, 180, t, .05, INK)
        word(im, "I'm back", IT(900, 130), 360, 300, T, at(2, .55), PUR)
        return im
    if i == 3:   # primera partida (clip)
        im = bg("p", "GG"); cf = T2.clip("clip_tenz", t)
        if cf is not None: pop(im, card(duo(cf), 420, border=WHITE), 360, 780, t, .05, .45)
        word(im, "ese mismo día", IT(400, 50), 360, 150, t, .05, LILL)
        word(im, "Primera partida", IT(900, 92), 360, 250, T, at(3, .45), WHITE)
        word(im, "como jugador de T1", IT(400, 44), 360, 1210, T, at(3, .8), LILL)
        return im
    if i == 4:   # 1.000.000 de vistas
        im = bg("w"); pop(im, EYE, 360, 860, t, .05, .45)
        n = int(1_207_916 * eo(prog(T, at(4, 0), at(4, .9))))
        word(im, "más de", IT(400, 52), 360, 200, t, .02, INK)
        paste(im, text_layer(f"{n:,}".replace(",", "."), ANTON(150), PUR), 360, 380, clamp01(t * 4))
        word(im, "personas lo vieron", IT(400, 46), 360, 520, T, at(4, .5), INK)
        return im
    if i == 5:   # Masters Bangkok 2025
        im = bg("w"); ImageDraw.Draw(im).rectangle((0, 980, W, H), fill=PUR + (255,))
        paste(im, COL, 360, lerp(1700, 1100, eo(prog(t, 0, .6))))
        cy = 1100 - COL.height / 2 - CUP.height / 2 + 20; p = eo(prog(T, at(5, .45), at(5, .45) + .6))
        paste(im, CUP, 360, lerp(-250, cy, p) + math.sin(T * 2.5) * 6 * p, clamp01(p * 3))
        word(im, "no llega a cualquier equipo", IT(400, 44), 360, 160, t, .05, INK)
        word(im, "Masters", IT(900, 96), 360, 270, T, at(5, .6), PUR); word(im, "Bangkok 2025", IT(400, 60), 360, 360, T, at(5, .75), INK)
        return im
    if i == 6:   # 2 importados: TenZ y crashies
        im = bg("p"); word(im, "por primera vez", IT(400, 50), 360, 150, t, .05, LILL)
        word(im, "2 importados", IT(900, 104), 360, 260, T, at(6, .35), WHITE)
        for k, (f, n, ff) in enumerate((("tenz", "TenZ", .78), ("crashies", "crashies", .9))):
            x = 200 + k * 320; p = eo(prog(T, at(6, ff), at(6, ff) + .35))
            if p > 0:
                paste(im, BIG_FACES[f], x, lerp(1500, 760, p), p)
                paste(im, text_layer(n, IT(900, 64), WHITE), x, lerp(1700, 980, p), p)
        word(im, "de Norteamérica", IT(400, 46), 360, 360, T, at(6, .6), LILL)
        return im
    if i == 7:   # ¿idioma?
        im = bg("w", "idioma"); pop(im, BRAIN, 230, 860, t, .05, .45); pop(im, HEAD, 500, 900, t, .25, .45)
        word(im, "la gran pregunta", IT(400, 50), 360, 170, t, .05, INK)
        puzzle_tile(im, T, at(7, .4), "?", 360, 470, 230)
        word(im, "¿en qué idioma?", IT(900, 74), 360, 1180, T, at(7, .45), PUR)
        return im
    if i == 8:   # enero · VCT Pacific
        im = bg("p", "2027")
        k = KING.rotate((1 - eo(prog(t, .05, .7))) * 20, expand=True, resample=Image.BICUBIC); paste(im, k, lerp(620, 480, eo(prog(t, .05, .7))), lerp(1700, 1010, eo(prog(t, .05, .7))))
        word(im, "la respuesta", IT(400, 50), 260, 170, t, .05, LILL)
        word(im, "Enero 2027", IT(900, 96), 290, 280, T, at(8, .3), WHITE)
        word(im, "VCT Pacific", IT(900, 72), 250, 400, T, at(8, .65), LILL)
        pop(im, R.tint(VLOGO.resize((150, int(VLOGO.height * 150 / VLOGO.width))), WHITE), 150, 560, T, at(8, .7), .4)
        return im
    # 9: ¿lo logra?
    im = bg("w", "King")
    tenz_orbit(im, T, t, 360, 1340, 600, max(0, t - .2), crown_t0=CUT[9] + .1)
    word(im, "¿Tú crees que", IT(400, 56), 360, 120, t, .02, INK)
    word(im, "lo logra?", IT(900, 130), 360, 240, T, at(9, .4), PUR)
    for k, (s_, x, y, a) in enumerate([("DUPLEXDRAGON", 40, 1210, "lm"), ("@DuplexDragon_", 680, 1210, "rm"),
                                         ("Fuentes: vlr.gg · esports.net · Inven Global · 12–13 nov 2026", 360, 1240, "mm"), ("Clips e imágenes: créditos a sus autores · fan edit", 360, 1262, "mm")]):
        p = prog(t, 1.0 + k * .2, 1.4 + k * .2)
        if p > 0: paste(im, text_layer(s_, SANS(400 if k > 1 else 600, 15 if k > 1 else 18), (110, 100, 125)), x, y, p, a)
    return im

def frame(T):
    i = max(k for k in range(len(CUT)) if T >= CUT[k]); img = scene(i, T)
    if i % 2 == 0: brackets(img, T - CUT[i], PUR, .8)
    if T > at(1, .45): paste(img, R.T1_SMALL_W if i % 2 else R.T1_SMALL_P, 40, 60, .9, "lm")
    dc = T - CUT[i]; s = 1 + .05 * (1 - eo(clamp01(dc / .3))) if i > 0 else 1
    img = scale_about(img, s, bg=WHITE + (255,))
    if i > 0 and dc < .12: img = Image.blend(img, canvas((WHITE if i % 2 else LILL) + (255,)), .85 * (1 - dc / .12))
    if T > DUR - .9: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - .9, DUR - .1))
    return img.convert("RGB")

def audio(out):
    SR = 48000; N = int(DUR * SR); vox = np.zeros((N, 2), np.float32)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for i, s in enumerate(LS):
        v = rd(os.path.join(D1, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), N - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((N, 2), np.float32)
    S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "typing", "clink")}
    ev = [("whoosh", c - .2, .5) for c in CUT[1:]] + [("pop", CUT[0] + .2, .4), ("impact", at(1, .45), .7), ("clink", at(1, .75), .5),
          ("pop", CUT[2] + .15, .5), ("typing", CUT[2] + .2, .2), ("punch", at(2, .55), .6), ("pop", CUT[3] + .1, .5), ("punch", at(3, .45), .5),
          ("shimmer", CUT[4] + .1, .5), ("punch", at(5, .6), .5), ("clink", at(5, .5) + .5, .5), ("pop", at(6, .78), .5), ("pop", at(6, .9), .5),
          ("punch", at(7, .4), .6), ("punch", at(8, .3), .6), ("impact", CUT[9], .8), ("shimmer", CUT[9] + .3, .4)]
    for k, t0, g in ev:
        s = S[k]; j = max(0, int(t0 * SR)); n = min(len(s), N - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .6)):
        w = wave.open(os.path.join(D1, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    song = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/e1b3ea4f-HEAVENLY_JUMPSTYLE.mp3"
    f = (f"[0:a]highpass=f=80,acompressor=threshold=-20dB:ratio=3,loudnorm=I=-16:TP=-1.5,aresample=48000,asplit=3[dry][rv][key];"
         f"[rv][3:a]afir=dry=0:wet=1,highpass=f=200,volume=0.4[wet];[dry][wet]amix=inputs=2:normalize=0[vx];"
         f"[1:a]atrim=start=24,asetpts=PTS-STARTPTS,aresample=48000,volume=0.3[m];[m][key]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=300[md];"
         f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR},afade=t=in:d=0.4,afade=t=out:st={DUR - 1.6}:d=1.6,alimiter=limit=0.95[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(D1, "voz.wav"), "-i", song, "-i", os.path.join(D1, "sfx.wav"), "-i", os.path.join(TZ, "reverb_ir.wav"),
                    "-filter_complex", f, "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for k, x in enumerate(ims): sh.paste(x, (k * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview", [round(c, 2) for c in CUT], round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(D1, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
