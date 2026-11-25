"""Look de cine de las referencias: sombras verde-azuladas, pieles/luces cálidas, contraste suave, saturación baja, grano y viñeta."""
import numpy as np, subprocess
from PIL import Image
TEAL = np.array([.10, .32, .36]); WARM = np.array([1.0, .80, .58])
def cine(a, seed=0):
    f = a.astype(np.float32) / 255; l = f @ np.array([.299, .587, .114], np.float32)
    f = np.clip((f - .5) * .92 + .5 + .02, 0, 1)                                   # contraste suave, negros levantados
    g = f.mean(2, keepdims=True); f = g + (f - g) * .82                            # saturación baja
    sh = (np.clip(.5 - l, 0, .5) / .5)[..., None]; hi = (np.clip(l - .45, 0, .55) / .55)[..., None]
    f = f * (1 - .30 * sh) + TEAL * .30 * sh                                        # sombras verde-azuladas
    f = f * (1 - .14 * hi) + WARM * .14 * hi                                        # luces y pieles cálidas
    H, W = l.shape; yy, xx = np.mgrid[:H, :W]; v = 1 - .28 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2) / 2
    f = f * v[..., None] + np.random.default_rng(seed).normal(0, .016, (H, W))[..., None]
    return (np.clip(f, 0, 1) * 255).astype(np.uint8)
def toma(path, t, crop, size=(720, 1280)):
    x, y, w, h = crop
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", path, "-frames:v", "1", "-vf", f"crop={w}:{h}:{x}:{y},scale={size[0]}:{size[1]}:flags=lanczos",
                          "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(size[1], size[0], 3)
    return Image.fromarray(cine(a, int(t * 100))).convert("RGBA")
