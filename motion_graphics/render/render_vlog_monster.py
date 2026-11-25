#!/usr/bin/env python3
"""Vlog del lanzamiento Monster Ultra Vice Guava × GTA VI (TP Gaming Arena) — solo clips.
Look de cine en las tomas + gráficos blancos/morados (plantilla de la guía) + voz Andrés + cierre tipo portada.
Uso: python3 render_vlog_monster.py salida.mp4 | --preview t1,t2,..."""
import os, sys, json, wave, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import plantilla_texto as T
import grade_cine as G
import cierre_monster as C
HERE = os.path.dirname(os.path.abspath(__file__)); EV = os.path.join(HERE, "..", "evento"); W, H, FPS = 720, 1280, 30
SONG = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/f5663a40-Foushe__-_Deep_End_Lyrics.mp3"; SONG_AT = 29.3
TOM = os.path.join(EV, "tomas"); E = os.path.join(EV, "ev")

# ---------- voz ----------
N = len(json.load(open(os.path.join(EV, "guion.json")))); DL, WT = [], []
for i in range(N):
    w = wave.open(os.path.join(EV, "voz", f"l{i:02d}.wav")); DL.append(w.getnframes() / w.getframerate())
    al = json.load(open(os.path.join(EV, "voz", f"l{i:02d}.json"))); ws, cur, st = [], "", None
    for ch, a in zip(al["characters"], al["character_start_times_seconds"]):
        if ch.isspace():
            if cur: ws.append((cur, st)); cur = ""
        else:
            if not cur: st = a
            cur += ch
    if cur: ws.append((cur, st))
    WT.append(ws)
LS = []; t = .25
for i_, d in enumerate(DL): LS.append(t); t += d + .65 + (2.0 if i_ == 4 else 0)
SEG = [0.0] + [LS[i] - .15 for i in range(1, N)]
CIERRE0 = SEG[N - 1]; DUR = max(LS[-1] + DL[-1] + .9, CIERRE0 + 4.6)
def wt(k, s):
    h = [st for w_, st in WT[k] if s.lower() in w_.lower()]; return LS[k] + (h[0] if h else 0)

# ---------- tomas (archivo, inicio, velocidad, peso) ----------
SHOTS = [
    [(f"{E}/01_IMG_2730.mp4", 1.0, 1, 1), (f"{E}/15_b16.mp4", 11.3, 1, 1), (f"{E}/17_d34.mp4", 14.0, 1, 1), (f"{E}/04_IMG_2729.mp4", 2.2, 1, 1),
     (f"{E}/05_IMG_2714.mp4", .5, 1, 1), (f"{E}/15_b16.mp4", 5.6, 1, 1), (f"{E}/13_wa.mp4", 2.5, 1, 1), (f"{E}/02_IMG_2685.mp4", 1.0, 1, 1),
     (f"{E}/17_d34.mp4", 30.5, 1, 1), (f"{E}/14_wa.mp4", .3, 1, 1), (f"{E}/06_IMG_2731.mp4", .5, 1, 1), (f"{E}/15_b16.mp4", 9.4, 1, 1.3)],
    [(f"{TOM}/t2674.mp4", .5, 1, .9), (f"{TOM}/t2674.mp4", 3.6, 1, .8), (f"{TOM}/t2674.mp4", 15.8, .5, 1.5), (f"{TOM}/t2674.mp4", 20.3, 1, .9)],
    [(f"{E}/10_IMG_2682.mp4", .3, 1, 1.0), (f"{E}/10_IMG_2682.mp4", 1.6, 1, 1.0), (f"{E}/16_IMG_2684.mp4", 2.0, 1, .3), (f"{E}/16_IMG_2684.mp4", 6.0, 1, 1.0)],
    [(f"{E}/02_IMG_2685.mp4", 1.0, 1, 1.0), (f"{E}/16_IMG_2684.mp4", 14.7, 1, 1.0), (f"{E}/07_IMG_2690.mp4", .5, 1, 1.0), (f"{E}/09_IMG_2688.mp4", .5, 1, 1.0)],
    [(f"{E}/17_d34.mp4", 2.5, 1, 1.2), (f"{E}/05_IMG_2714.mp4", .5, 1, .8), (f"{E}/17_d34.mp4", 10.5, 1, 1.2), (f"{E}/17_d34.mp4", 19.5, 1, 1.2), (f"{E}/12_wa.mp4", .5, 1, .8), (f"{E}/17_d34.mp4", 30.5, 1, 1.2), (f"{E}/17_d34.mp4", 36.0, 1, 1.2)],
    [(f"{E}/04_IMG_2729.mp4", 2.2, 1, 1.0), (f"{E}/06_IMG_2731.mp4", .5, 1, 1.0), (f"{E}/13_wa.mp4", .2, 1, 1.0), (f"{E}/13_wa.mp4", 2.5, 1, 1.0)],
    [(f"{E}/15_b16.mp4", 7.2, 1, 1.0), (f"{E}/04_IMG_2729.mp4", 1.0, 1, 1.0), (f"{E}/15_b16.mp4", 9.4, 1, 1.0), (f"{E}/15_b16.mp4", 11.3, 1, 1.0), (f"{E}/01_IMG_2730.mp4", 3.5, 1, 1.0)],
]
TL = []   # (inicio, duración, archivo, t0, velocidad, sección)
for s, shots in enumerate(SHOTS):
    a, b = SEG[s], SEG[s + 1]; tot = sum(x[3] for x in shots); c = a
    for k, (f, t0, sp, wgt) in enumerate(shots):
        d = (b - a) * wgt / tot if k < len(shots) - 1 else b - c
        TL.append((c, d, f, t0, sp, s)); c += d
_cache = {}
def frames(f, t0, dur, sp):
    key = (f, t0, sp)
    if key not in _cache:
        _cache.clear(); n = int(math.ceil(dur * FPS)) + 3
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", f, "-vf",
                              f"setpts={1 / sp}*PTS,fps={FPS},crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale={W}:{H}:flags=lanczos",
                              "-frames:v", str(n), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _cache[key] = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return _cache[key]

# ---------- textos ----------
TIT = {0: ("MONSTER × GTA VI", "lanzamiento", None), 1: ("A ALISTARSE", "primero", None), 2: ("TP GAMING ARENA", None, "BOGOTÁ · 21 NOV"),
       3: ("VICE CITY", "bienvenidos a", None), 4: ("JUGAMOS GTA VI", None, "¡UNA LOCURA!"), 5: ("PURA ENERGÍA", None, None),
       6: ("ZERO SUGAR", "full flavor", "ULTRA VICE GUAVA")}
CHUNKS = []
for i in range(N - 1):
    ws = WT[i]
    for j in range(0, len(ws), 3):
        txt = " ".join(w_ for w_, _ in ws[j:j + 3]).strip(".,:").replace("ge-te-a seis", "GTA VI").replace("ge-te-a", "GTA"); t0 = LS[i] + ws[j][1]
        t1 = LS[i] + ws[j + 3][1] if j + 3 < len(ws) else LS[i] + DL[i] + .1
        CHUNKS.append((t0, t1, txt))
def ease(p): return 1 - (1 - max(0, min(1, p))) ** 3

def frame(Tm):
    if Tm >= CIERRE0:
        im = Image.fromarray(np.asarray(C.frame(Tm - CIERRE0))).convert("RGBA")
    else:
        sh = [x for x in TL if x[0] <= Tm][-1]; c0, d, f, t0, sp, s = sh; dt = Tm - c0
        fr = frames(f, t0, d + .2, sp); a = fr[min(int(dt * FPS), len(fr) - 1)]
        im = Image.fromarray(G.cine(a, int(Tm * 30))).convert("RGBA")
        z = (1 + .14 * (1 - ease(dt / .18)) if s == 0 else 1 + .05 * (1 - ease(dt / .3))) + .02 * dt / max(d, .1)                       # golpe de zoom al entrar + empuje lento
        im = im.resize((int(W * z), int(H * z)), Image.LANCZOS); x0 = (im.width - W) // 2; y0 = (im.height - H) // 2; im = im.crop((x0, y0, x0 + W, y0 + H))
        if dt < .12 and c0 > 0:                                                          # barrido (motion blur) en cada corte
            arr = np.asarray(im).astype(np.float32); k = int((120 if s == 0 else 60) * (1 - dt / .12)) + 1
            im = Image.fromarray(sum(np.roll(arr, s_, axis=1) for s_ in range(0, k, max(1, k // 6))).astype(np.float32).__truediv__(len(range(0, k, max(1, k // 6)))).astype(np.uint8), "RGBA")
        ts = SEG[s]; ttl, acc, tag = TIT[s]; p = Tm - ts; ty = 720 if s in (1, 6) else T.TIT_Y
        if p < 2.0:                                                                       # titular de sección (1,8 s)
            al = min(1, p / .2) * (1 - max(0, (p - 1.7) / .3))
            if acc: T.acento(im, acc, color=T.LILL, y=ty - 85, alpha=al)
            T.titular(im, ttl, y=ty, sc=1.15 - .15 * ease(p / .3), alpha=al)
            if tag: T.etiqueta(im, tag, y=ty + 95, alpha=al)
        for t0c, t1c, txt in CHUNKS:                                                      # subtítulos de la voz
            if t0c <= Tm < t1c: T.subtitulo(im, txt, y=900, size=44, alpha=min(1, (Tm - t0c) / .08))
    ImageDraw.Draw(im).text((40, 175), "@DuplexDragon_", font=T.MONT(18), fill=(255, 255, 255, 170), anchor="lm")
    for ts in SEG[1:]:                                                                    # flash blanco de 2 cuadros por sección
        if 0 <= Tm - ts < 2 / FPS: im = Image.blend(im, Image.new("RGBA", (W, H), (255, 255, 255, 255)), .7)
    if Tm < .1: im = Image.blend(im, Image.new("RGBA", (W, H), (255, 255, 255, 255)), .8 * (1 - Tm / .1))
    return im.convert("RGB")

def audio(out):
    SR = 48000; Ns = int(DUR * SR)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    vox = np.zeros((Ns, 2), np.float32)
    for i, s in enumerate(LS):
        v = rd(os.path.join(EV, "voz", f"l{i:02d}.wav")); j = int(s * SR); n = min(len(v), Ns - j); vox[j:j + n] += v[:n]
    A = os.path.join(HERE, "..", "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    ev = [("braam", 0, .6)] + [("whoosh", ts - .15, .45) for ts in SEG[1:]] + [("hit808", x[0], .4) for x in TL if x[0] > 0] + [
        ("riser", SEG[6] - 1.4, .45), ("boom", SEG[6], .7), ("boom", CIERRE0, .7), ("pop", CIERRE0 + 1.0, .5)]
    for k, t0, g in ev:
        s = rd(A + k + ".48.wav"); j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    for name, arr in (("vlog_voz.wav", vox), ("vlog_sfx.wav", fx * .55)):
        w = wave.open(os.path.join(EV, name), "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(arr, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(EV, "vlog_voz.wav"), "-i", SONG, "-i", os.path.join(EV, "vlog_sfx.wav"), "-filter_complex",
                    f"[0:a]loudnorm=I=-15:TP=-1.5:LRA=11,apad=whole_dur={DUR},atrim=0:{DUR},asplit=2[vx][key];"
                    f"[1:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,equalizer=f=3000:t=q:w=1.2:g=-4,volume=0.22[m];"
                    f"[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=15:release=350[md];"
                    f"[vx][md][2:a]amix=inputs=3:normalize=0:duration=first,atrim=0:{DUR},afade=t=out:st={DUR - 1.2}:d=1.2,alimiter=limit=0.95[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    if "--preview" in a:
        ts = [float(x) for x in a[-1].split(",")]; ims = [frame(x).resize((W // 2, H // 2)) for x in ts]
        sh = Image.new("RGB", (W // 2 * min(6, len(ims)), H // 2 * ((len(ims) + 5) // 6)))
        for k, x in enumerate(ims): sh.paste(x, ((k % 6) * W // 2, (k // 6) * H // 2))
        sh.save(os.path.join(EV, "vlog_prev.jpg"), quality=85); print("preview", [round(x, 2) for x in SEG], round(DUR, 2)); sys.exit()
    out = a[0]; mix = os.path.join(EV, "vlog_mix.wav"); audio(mix)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
                          "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "256k", "-t", str(DUR), "-vf", "scale=1080:1920:flags=lanczos",
                          "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
