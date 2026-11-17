#!/usr/bin/env python3
"""Versión CORTA (~33 s) de "Su primer día en T1" con gancho al inicio. Voz: Andrés (ElevenLabs), colombiano."""
import os, sys, math, wave, subprocess
import numpy as np
from PIL import Image, ImageDraw
import render_dia1u as U          # aplica parches del cierre CTA sobre render_dia1
import render_dia1 as B
from render_dia1 import (W, H, PUR, LILL, WHITE, INK, IT, ANTON, SANS, word, pop, bg, brackets, tenz_orbit, text_layer, paste, prog, eo, lerp,
                         clamp01, canvas, scale_about, ghost_tenz, T1_W, CROWN, R)
HERE = os.path.dirname(os.path.abspath(__file__)); CO = os.path.join(HERE, "..", "corto"); FPS = 30
DL = []
for i in range(9):
    w = wave.open(os.path.join(CO, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
LS = []; t = .15
for d in DL: LS.append(t); t += d + .25
DUR = LS[-1] + DL[-1] + 1.6
SEG = [s - .1 if i else 0.0 for i, s in enumerate(LS)]            # inicio de cada escena
def sat(k, f): return LS[k] + DL[k] * f
# segmento → escena de render_dia1 (contenido)
MAP = {1: 4, 3: 2, 4: 3, 5: 5, 6: 6}
CUTC = [0.0] * 10
for k, c in MAP.items(): CUTC[c] = SEG[k]
CUTC[9] = SEG[7]
SPANC = {c: k for k, c in MAP.items()}
B.CUT[:] = CUTC
B.at = lambda c, f: sat(SPANC[c], f) if c in SPANC else 0.0
U.CUT[:] = CUTC
U.VOFF = 0.0
U.CTA = {"coment": (LS[7] + DL[7] * .15, LS[7] + DL[7]), "sigue": (LS[8], sat(8, .3)), "comparte": (sat(8, .3), sat(8, .55)), "guarda": (sat(8, .55), sat(8, 1.0))}

def hook(T):
    """Segundo 0: TenZ con la corona y el titular, sin esperar."""
    im = bg("w", "KING")
    tenz_orbit(im, T, T + 2, 360, 1360, 600, T + 1.5, crown_t0=-.4)
    rib = Image.new("RGBA", (640, 100), PUR + (255,)); ImageDraw.Draw(rib).text((320, 52), "EL REY YA JUGÓ EN T1", font=ANTON(64), fill=WHITE, anchor="mm")
    s = lerp(1.25, 1.0, eo(clamp01(T / .25))); paste(im, rib.resize((int(640 * s), int(100 * s))), 360, 190)
    word(im, "su primera partida", IT(900, 70), 360, 300, T, sat(0, .45), PUR)
    return im

def king(T):
    t = T - SEG[2]; im = bg("p", "KING"); ghost_tenz(im, t, .15)
    word(im, "12 · noviembre · 2026", IT(400, 48), 360, 170, t, .02, LILL)
    pop(im, T1_W, 360, 390, T, sat(2, .3), .4)
    word(im, "The King", IT(900, 120), 360, 520, T, sat(2, .65), WHITE); word(im, "is back", IT(400, 80), 400, 620, T, sat(2, .78), LILL)
    p = eo(prog(T, sat(2, .65), sat(2, .65) + .5)); paste(im, CROWN.resize((360, int(CROWN.height * 360 / CROWN.width))), 360, lerp(-200, 930, p) + math.sin(T * 2.4) * 8, clamp01(p * 3))
    return im

def scene(k, T):
    if k == 0: return hook(T)
    if k == 2: return king(T)
    if k >= 7: return U.scene_cta(T)
    return B.scene(MAP[k], T)

def frame(T):
    k = max(i for i in range(len(SEG)) if T >= SEG[i]); k = 7 if k == 8 else k
    img = scene(k, T)
    if k % 2 == 0 and k < 7: brackets(img, T - SEG[k], PUR, .8)
    if T > sat(2, .3): paste(img, R.T1_SMALL_W if k in (2, 4, 6) else R.T1_SMALL_P, 40, 60, .9, "lm")
    dc = T - SEG[k]; s = 1 + .05 * (1 - eo(clamp01(dc / .3))) if k > 0 else 1
    img = scale_about(img, s, bg=WHITE + (255,))
    if k > 0 and dc < .1: img = Image.blend(img, canvas((WHITE if k % 2 else LILL) + (255,)), .85 * (1 - dc / .1))
    if T < .08: img = Image.blend(img, canvas(WHITE + (255,)), .7 * (1 - T / .08))
    if T > DUR - .8: img = Image.blend(img, canvas(WHITE + (255,)), prog(T, DUR - .8, DUR - .1))
    return img.convert("RGB")

def audio(out):
    SR = 48000; N = int(DUR * SR); vox = np.zeros((N, 2), np.float32)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    for i, s in enumerate(LS):
        v = rd(os.path.join(CO, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), N - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((N, 2), np.float32)
    S = {k: rd(A + k + ".48.wav") for k in ("whoosh", "pop", "punch", "impact", "shimmer", "typing", "clink")}
    ev = [("impact", 0.0, .8), ("clink", .2, .5)] + [("whoosh", c - .2, .5) for c in SEG[1:8]] + [
        ("shimmer", SEG[1] + .1, .5), ("impact", sat(2, .3), .6), ("clink", sat(2, .75), .5), ("pop", SEG[3] + .1, .5), ("punch", sat(3, .7), .6),
        ("pop", SEG[4] + .1, .5), ("clink", sat(5, .6), .5), ("pop", sat(6, .78), .5), ("pop", sat(6, .9), .5),
        ("pop", U.CTA["coment"][0] + .3, .6), ("pop", sat(8, .2), .7), ("whoosh", sat(8, .35), .5), ("pop", sat(8, .65), .6), ("shimmer", sat(8, .8), .5)]
    for k_, t0, g in ev:
        s = S[k_]; j = max(0, int(t0 * SR)); n = min(len(s), N - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("voz.wav", vox), ("sfx.wav", fx * .6)):
        w = wave.open(os.path.join(CO, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    song = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/e1b3ea4f-HEAVENLY_JUMPSTYLE.mp3"; ir = os.path.join(HERE, "..", "dia1", "plate_ir.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(CO, "voz.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR}[o]", "-map", "[o]", "-ar", "48000", os.path.join(CO, "voz_pro.wav")], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(CO, "voz_pro.wav"), "-i", song, "-i", os.path.join(CO, "sfx.wav"), "-filter_complex",
                    f"[0:a]asplit=2[vx][key];[1:a]atrim=start=24,asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.17[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=350[md];"
                    f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=longest,atrim=0:{DUR},afade=t=out:st={DUR - 1.2}:d=1.2,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[a.index("--preview") + 1].split(",")]
        ims = [frame(x).resize((W // 2, H // 2)) for x in ts]; sh = Image.new("RGB", (W // 2 * len(ims), H // 2))
        for k, x in enumerate(ims): sh.paste(x, (k * W // 2, 0))
        sh.save(os.path.join(HERE, "preview.jpg"), quality=88); print("preview", [round(c, 2) for c in SEG], round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(CO, "mezcla.wav"); audio(mix)
    cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
           "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR),
           "-vf", "scale=1080:1920:flags=lanczos", "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); n = int(DUR * FPS)
    for k in range(n): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
