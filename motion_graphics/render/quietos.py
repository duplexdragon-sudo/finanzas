import sys, subprocess, numpy as np
p = sys.argv[1]; w, h = 90, 160
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", f"fps=10,scale={w}:{h},format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
f = np.frombuffer(raw, np.uint8).reshape(-1, h, w).astype(np.float32); d = np.abs(np.diff(f, axis=0)).mean((1, 2))
q = np.convolve(d < .6, np.ones(5), "valid") >= 5; segs = []
for i, v in enumerate(q):
    if v and (not segs or segs[-1][1] < i - 1): segs.append([i, i])
    elif v: segs[-1][1] = i
print("tramos quietos:", len(segs), [(round(a / 10, 1), round((b + 5) / 10, 1)) for a, b in segs])
