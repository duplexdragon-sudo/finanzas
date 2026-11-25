#!/usr/bin/env python3
"""DEMO de la receta del vlog del evento (Monster Ultra Vice Guava) usando tomas de las referencias como relleno.
Ritmo a 120 BPM (un golpe cada 0,5 s), palabra por golpe, ráfaga, barridos de cámara, flashes, cámara lenta, color rosa/cian."""
import os, subprocess, wave, math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(HERE, ".."); EV = os.path.join(B, "evento")
W, H, FPS = 720, 1280, 30
ANTON = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "anton-400-normal.ttf"), s)
IT = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "playfair-display-500-italic.ttf"), s)
SONG = "/root/.claude/uploads/400f996d-bb64-5a86-b968-aadbbec0de6b/f5663a40-Foushe__-_Deep_End_Lyrics.mp3"; SONG_AT = 29.3
BEAT = .5

_cache = {}
def frames(ref, t0, dur, speed=1.0):
    key = (ref, t0, dur, speed)
    if key not in _cache:
        n = int(dur * FPS) + 2
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t0), "-i", os.path.join(EV, "ref", ref + ".mp4"), "-vf",
                              f"setpts={1/speed}*PTS,fps={FPS},crop=ih*0.86*9/16:ih*0.86:(iw-ih*0.86*9/16)/2:0,scale={W}:{H}:flags=lanczos", "-frames:v", str(n),
                              "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        _cache[key] = np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3)
    return _cache[key]

PINK = np.array([255, 60, 170.]); CYAN = np.array([0, 200, 220.])
def grade(a):
    f = a.astype(np.float32) / 255; l = f @ np.array([.299, .587, .114], np.float32)
    g = f.mean(2, keepdims=True); f = g + (f - g) * 1.35                     # más saturación
    f = np.clip((f - .5) * 1.12 + .5, 0, 1)                                    # contraste
    sh = np.clip(.45 - l, 0, .45)[..., None] / .45; hi = np.clip(l - .55, 0, .45)[..., None] / .45
    f = f + sh * (CYAN / 255 - f) * .22 + hi * (PINK / 255 - f) * .18          # sombras cian, luces rosas
    yy, xx = np.mgrid[:H, :W]; v = 1 - .35 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    f = f * v[..., None]
    f = f + np.random.default_rng(int(l.sum() * 1000) % 99999).normal(0, .018, f.shape[:2])[..., None]   # grano
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)

UNB = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "unbounded-900.ttf"), s)
UNB5 = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "unbounded-500.ttf"), s)
PAC = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "pacifico.ttf"), s)
POP = lambda s: ImageFont.truetype(os.path.join(B, "fonts", "poppins-500-normal.ttf"), s)
NPINK = (255, 60, 180); NCYAN = (40, 240, 255)
def neon(im, s, font, y, glow=NPINK, core=(255, 255, 255), track=0, sc=1.0, alpha=1.0, rot=0, x=None):
    """Texto neón: núcleo blanco + borde de color + resplandor en 3 capas; tracking opcional."""
    x = W / 2 if x is None else x
    tw = sum(font.getlength(c) for c in s) + track * (len(s) - 1); asc, desc = font.getmetrics(); th = asc + desc
    pad = 90; lay = Image.new("RGBA", (int(tw) + pad * 2, th + pad * 2)); d = ImageDraw.Draw(lay); cx = pad
    for c in s:
        d.text((cx, pad), c, font=font, fill=core + (255,), stroke_width=max(2, font.size // 28), stroke_fill=glow + (255,)); cx += font.getlength(c) + track
    a_ = lay.getchannel("A"); out = Image.new("RGBA", lay.size)
    for r, op in ((38, .55), (16, .75), (5, .9)):
        g = Image.new("RGBA", lay.size, glow + (0,)); g.putalpha(a_.filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(min(255, v * op * 1.6)))); out.alpha_composite(g)
    out.alpha_composite(lay)
    if rot: out = out.rotate(rot, resample=Image.BICUBIC, expand=True)
    if sc != 1.0: out = out.resize((max(1, int(out.width * sc)), max(1, int(out.height * sc))), Image.LANCZOS)
    if alpha < 1: out.putalpha(out.getchannel("A").point(lambda v: int(v * max(0, alpha))))
    im.alpha_composite(out, (int(x - out.width / 2), int(y - out.height / 2)))

MAXW = 600
def _fit(s, mk, size, track=0):
    while size > 20 and sum(mk(size).getlength(c) for c in s) + track * (len(s) - 1) > MAXW: size -= 2
    return mk(size)
SUN = [(70, 120, 255), (230, 70, 220), (255, 90, 140), (255, 160, 70), (255, 225, 100)]
def sunset(im, s, mk, size, y, track=4, sc=1.0, alpha=1.0, rot=0):
    """Título estilo atardecer 'Vice': relleno degradado naranja→rosa→morado, borde oscuro grueso, resplandor rosa."""
    font = _fit(s, mk, size, track); asc, desc = font.getmetrics(); th = asc + desc
    tw = sum(font.getlength(c) for c in s) + track * (len(s) - 1); pad = 80
    m = Image.new("L", (int(tw) + pad * 2, th + pad * 2), 0); d = ImageDraw.Draw(m); cx = pad
    sw = max(3, min(12, font.size // 14)); ms = Image.new("L", m.size, 0); ds = ImageDraw.Draw(ms)
    for c in s:
        d.text((cx, pad), c, font=font, fill=255); ds.text((cx, pad), c, font=font, fill=255, stroke_width=sw, stroke_fill=255); cx += font.getlength(c) + track
    bb = m.getbbox(); h0, h1 = bb[1], bb[3]
    grad = Image.new("RGB", m.size); gd = ImageDraw.Draw(grad)
    for yy in range(m.size[1]):
        u = min(1, max(0, (yy - h0) / max(1, h1 - h0))) * (len(SUN) - 1); i = min(int(u), len(SUN) - 2); f = u - i
        gd.line((0, yy, m.size[0], yy), fill=tuple(int(SUN[i][k] * (1 - f) + SUN[i + 1][k] * f) for k in range(3)))
    out = Image.new("RGBA", m.size)
    mo = m.filter(ImageFilter.MaxFilter(2 * (sw + 4) + 1)); mw = m.filter(ImageFilter.MaxFilter(2 * sw + 1))
    shd = Image.new("RGBA", m.size, (30, 10, 60, 0)); shd.putalpha(mo.filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .6))); out.alpha_composite(shd, (0, 10))
    dk = Image.new("RGBA", m.size, (40, 12, 70, 0)); dk.putalpha(mo); out.alpha_composite(dk)
    wh = Image.new("RGBA", m.size, (255, 255, 255, 0)); wh.putalpha(mw); out.alpha_composite(wh)
    fill = grad.convert("RGBA"); fill.putalpha(m); out.alpha_composite(fill)
    if rot: out = out.rotate(rot, resample=Image.BICUBIC, expand=True)
    if sc != 1.0: out = out.resize((max(1, int(out.width * sc)), max(1, int(out.height * sc))), Image.LANCZOS)
    if alpha < 1: out.putalpha(out.getchannel("A").point(lambda v: int(v * max(0, alpha))))
    im.alpha_composite(out, (int(W / 2 - out.width / 2), int(y - out.height / 2)))

def clean(im, s, size, y, track=None, alpha=1.0, sc=1.0):
    """Texto limpio estilo póster: Poppins blanco, mayúsculas, letras espaciadas, sombra suave."""
    s = s.upper(); track = size * .35 if track is None else track; font = _fit(s, POP, size, track)
    tw = sum(font.getlength(c) for c in s) + track * (len(s) - 1); asc, desc = font.getmetrics(); pad = 30
    lay = Image.new("RGBA", (int(tw) + pad * 2, asc + desc + pad * 2)); d = ImageDraw.Draw(lay); cx = pad
    for c in s: d.text((cx, pad), c, font=font, fill=(255, 255, 255, 255)); cx += font.getlength(c) + track
    sh = Image.new("RGBA", lay.size, (20, 5, 40, 0)); sh.putalpha(lay.getchannel("A").filter(ImageFilter.GaussianBlur(6)).point(lambda v: int(v * .8)))
    out = Image.new("RGBA", lay.size); out.alpha_composite(sh, (0, 3)); out.alpha_composite(lay)
    if sc != 1.0: out = out.resize((max(1, int(out.width * sc)), max(1, int(out.height * sc))), Image.LANCZOS)
    if alpha < 1: out.putalpha(out.getchannel("A").point(lambda v: int(v * max(0, alpha))))
    im.alpha_composite(out, (int(W / 2 - out.width / 2), int(y - out.height / 2)))
def text(im, s, font, y, fill=(255, 255, 255), stroke=0, sc=1.0, alpha=1.0):
    neon(im, s, font, y, sc=sc, alpha=alpha)

# ----- línea de tiempo (en segundos) -----
SEGS = []   # (inicio, duración, ref, t0 en la referencia, velocidad, etiqueta)
t = 0.0
SEGS.append((t, 2.0, "r3", 30.5, 1.0, "hook")); t += 2.0
for k, t0 in enumerate((4.1, 4.6, 5.3, 6.4, 7.1, 8.6, 9.2, 10.0)):          # ráfaga de llegada: 1 clip por golpe
    SEGS.append((t, BEAT, "r1", t0, 1.0, "burst")); t += BEAT
for k, (t0, lab) in enumerate(((15.5, "TP GAMING ARENA"), (25.0, "BOGOTÁ"), (39.5, "21 · NOV"))):
    SEGS.append((t, 2.0, "r3", t0, 1.0, lab)); t += 2.0
SEGS.append((t, 2.5, "r3", 50.5, .45, "slow")); t += 2.5
END0 = t; DUR = t + 3.0

def end_card(T):
    tt = T - END0
    _fr = frames("r3", 54.0, 3.2); base = _fr[min(int(tt * FPS), len(_fr) - 1)]
    im = Image.fromarray(grade(base)).convert("RGBA").filter(ImageFilter.GaussianBlur(6))
    ov = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(ov)
    for y in range(H): d.line((0, y, W, y), fill=(int(255 * y / H), 40, int(170 + 50 * (1 - y / H)), 120))
    im.alpha_composite(ov)
    p = min(1, tt / .35); e = 1 - (1 - p) ** 3
    sunset(im, "MONSTER", UNB, 104, 450, track=4, sc=1.25 - .25 * e, alpha=p)
    if tt > .4: sunset(im, "ULTRA VICE GUAVA", UNB, 52, 580, track=3, alpha=min(1, (tt - .4) / .3))
    if tt > .8: clean(im, "Experiencia GTA VI · TP Gaming Arena", 22, 700, alpha=min(1, (tt - .8) / .3))
    if tt > 1.2: clean(im, "@DuplexDragon_", 24, 790, track=3, alpha=min(1, (tt - 1.2) / .3))
    return im

def frame(T):
    if T >= END0: im = end_card(T)
    else:
        seg = [s for s in SEGS if s[0] <= T][-1]; s0, dur, ref, t0, sp, lab = seg; dt = T - s0
        fr = frames(ref, t0, dur + .1, sp); a = fr[min(int(dt * FPS), len(fr) - 1)]
        im = Image.fromarray(grade(a)).convert("RGBA")
        z = 1 + .06 * max(0, 1 - dt / .3)                                     # zoom de impacto al entrar
        if z > 1.001:
            im = im.resize((int(W * z), int(H * z)), Image.LANCZOS); x0 = (im.width - W) // 2; y0 = (im.height - H) // 2; im = im.crop((x0, y0, x0 + W, y0 + H))
        if lab == "hook":                                                     # una palabra por golpe
            words = ("VICE", "GUAVA", "LAUNCH", "🔥")
            k = min(int(dt / BEAT), 3); w = words[k] if k < 3 else "LAUNCH"
            pw = (dt % BEAT) / .15
            if True: sunset(im, w, UNB, 130, 560, track=6, sc=1.25 - .25 * min(1, pw), alpha=min(1, pw))
            if k == 3: clean(im, "vlog del evento", 30, 680, alpha=min(1, ((dt - 1.5) / .2)))
        elif lab in ("TP GAMING ARENA", "BOGOTÁ", "21 · NOV"):
            p = min(1, dt / .25); clean(im, lab, 34, 300, alpha=p, sc=1.08 - .08 * p)
        elif lab == "slow":
            clean(im, "slow motion", 26, 1000, alpha=.95)
        # barrido de cámara (whip pan) entre bloques: los primeros 0,15 s
        if lab not in ("burst",) and dt < .15 and s0 > 0:
            a2 = np.asarray(im).astype(np.float32); k = 1 - dt / .15; sh = int(160 * k)
            acc = sum(np.roll(a2, s, axis=1) for s in range(0, sh + 1, max(1, sh // 8))) / (len(range(0, sh + 1, max(1, sh // 8))))
            im = Image.fromarray(acc.astype(np.uint8), "RGBA")
    # flash blanco de 2 cuadros en los golpes fuertes
    for hit in [2.0, SEGS[9][0], SEGS[10][0], SEGS[11][0], SEGS[12][0], END0]:
        if 0 <= T - hit < 2 / FPS: im = Image.blend(im, Image.new("RGBA", (W, H), (255, 255, 255, 255)), .75)
    ImageDraw.Draw(im).text((24, 1250), "DEMO · tomas de referencia", font=ImageFont.truetype(os.path.join(B, "fonts", "playfair-display-400-italic.ttf"), 20), fill=(255, 255, 255, 140), anchor="ls")
    return im.convert("RGB")

def audio(out):
    SR = 48000; Ns = int(DUR * SR)
    def rd(p):
        w = wave.open(p); return np.frombuffer(w.readframes(w.getnframes()), np.int16).reshape(-1, 2).astype(np.float32) / 32768
    A = os.path.join(B, "audio") + "/"; fx = np.zeros((Ns, 2), np.float32)
    ev = [("hit808", 0, .7)] + [("hit808", i * BEAT, .45) for i in range(1, 4)] + [("whoosh", s[0] - .1, .5) for s in SEGS[9:]] + [("glitch", s[0], .25) for s in SEGS[1:9]] + [
        ("riser", SEGS[12][0] - 1.5, .5), ("boom", SEGS[12][0], .8), ("boom", END0, .7)]
    for k, t0, g in ev:
        s = rd(A + k + ".48.wav"); j = max(0, int(t0 * SR)); n = min(len(s), Ns - j)
        if n > 0: fx[j:j + n] += s[:n] * g
    p = os.path.join(EV, "demo_sfx.wav"); w = wave.open(p, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(fx * .6, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SONG, "-i", p, "-filter_complex",
                    f"[0:a]atrim=start={SONG_AT},asetpts=PTS-STARTPTS,aresample=48000,volume=0.55[m];[m][1:a]amix=inputs=2:normalize=0:duration=longest,atrim=0:{DUR},afade=t=out:st={DUR-1.2}:d=1.2,loudnorm=I=-14:TP=-1.5[a]",
                    "-map", "[a]", "-ar", "48000", out], check=True)

if __name__ == "__main__":
    import sys
    if "--preview" in sys.argv:
        ts = [float(x) for x in sys.argv[-1].split(",")]; ims = [frame(x).resize((W // 2, H // 2)) for x in ts]
        sh = Image.new("RGB", (W // 2 * len(ims), H // 2)); [sh.paste(x, (k * W // 2, 0)) for k, x in enumerate(ims)]; sh.save(os.path.join(EV, "demo_prev.jpg")); print("ok", round(DUR, 2)); sys.exit()
    out = os.path.join(EV, "DEMO_vlog_evento_Monster.mp4"); mix = os.path.join(EV, "demo_mix.wav"); audio(mix)
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", mix,
                          "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-t", str(DUR), "-vf", "scale=1080:1920:flags=lanczos",
                          "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    for k in range(int(DUR * FPS)): p.stdin.write(frame(k / FPS).tobytes())
    p.stdin.close(); p.wait(); print("OK", out, round(DUR, 2))
