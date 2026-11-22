#!/usr/bin/env python3
"""Generate assets/floor.png: a 32-bit style, well-worn wooden tavern floor.

Everything is drawn in tone space (0..15) on a 16-colour warm brown ramp, then
quantised with ordered (Bayer) dithering for the smooth parts (lantern glow, vignette,
foot-traffic wear), so the picture stays crisp pixel art. Seeded, so output is repeatable.

Usage:  python3 tools/make_floor.py [out.png]      (default: assets/floor.png)
Needs:  Pillow, numpy
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

W = H = 384          # drawn at this size, then reduced by DOWN for chunkier pixels
DOWN = 2             # 1 = fine pixels, 2 = twice as coarse (output 192x192)
SEED = 32
rng = np.random.default_rng(SEED)

# 16-step ramp: cool-ish plum shadows, warm amber highlights (the "32-bit" look).
RAMP = [
    "#120909", "#1c0f0e", "#291713", "#371f17", "#46291b", "#56331f", "#673e25", "#78492b",
    "#8a5532", "#9c6439", "#ae7443", "#bf854e", "#ce975c", "#dcaa6d", "#e8be84", "#f2d3a2",
]
PAL = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in RAMP], dtype=np.uint8)
N = len(RAMP)

BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16.0


def bayer_round(x):
    """Round a float field to ints using a 4x4 ordered dither."""
    t = np.tile(BAYER4, (H // 4 + 1, W // 4 + 1))[:H, :W]
    return np.floor(x + t).astype(int)


def value_noise(scale, seed):
    """Smooth 0..1 noise: random grid, bilinear upsampled."""
    r = np.random.default_rng(seed)
    gh, gw = H // scale + 2, W // scale + 2
    g = r.random((gh, gw))
    ys, xs = np.mgrid[0:H, 0:W]
    fy, fx = ys / scale, xs / scale
    y0, x0 = fy.astype(int), fx.astype(int)
    ty, tx = fy - y0, fx - x0
    ty, tx = ty * ty * (3 - 2 * ty), tx * tx * (3 - 2 * tx)
    a = g[y0, x0] * (1 - tx) + g[y0, x0 + 1] * tx
    b = g[y0 + 1, x0] * (1 - tx) + g[y0 + 1, x0 + 1] * tx
    return a * (1 - ty) + b * ty


tone = np.zeros((H, W), dtype=int)   # integer tone (planks, grain, details)
dark_gap = np.zeros((H, W), dtype=bool)
plank_id = np.zeros((H, W), dtype=int)

# ---------- planks ----------
PH = 24                      # plank height in pixels
pid = 0
y = 0
while y < H:
    x = -int(rng.integers(0, 150))
    while x < W:
        length = int(rng.integers(110, 230))
        x0, x1 = max(x, 0), min(x + length, W)
        y0, y1 = y, min(y + PH, H)
        if x1 > x0:
            pid += 1
            base = int(rng.integers(5, 9))
            ph = y1 - y0
            lx = np.arange(x0, x1)[None, :] - x
            ly = np.arange(y0, y1)[:, None] - y
            phase, p2, freq = rng.random() * 6.28, rng.random() * 6.28, 0.55 + rng.random() * 0.5
            warp = 3.2 * np.sin(lx * 0.035 + p2) + 1.2 * np.sin(lx * 0.11 + phase)
            gr = np.sin((ly + warp) * freq + phase)
            plank = np.full((ph, x1 - x0), base, dtype=int)
            plank += (gr > 0.80).astype(int) - (gr < -0.84).astype(int)
            # fine speckle and long thin streaks
            plank -= (rng.random(plank.shape) < 0.035).astype(int)
            for _ in range(int(rng.integers(2, 5))):
                sy = int(rng.integers(2, max(3, ph - 3)))
                sx = int(rng.integers(0, max(1, x1 - x0 - 8)))
                sl = int(rng.integers(10, 46))
                plank[sy, sx:sx + sl] += int(rng.choice([-1, 1]))
            # knot (rings)
            if rng.random() < 0.22 and (x1 - x0) > 60:
                kx, ky = int(rng.integers(20, x1 - x0 - 20)), int(rng.integers(6, ph - 8))
                yy, xx = np.mgrid[0:ph, 0:x1 - x0]
                d = ((xx - kx) / 1.9) ** 2 + ((yy - ky) / 1.2) ** 2
                plank[(d < 12)] -= 1
                plank[(d < 6.5)] -= 1
                plank[(d < 2.2)] -= 1
                plank[(d >= 12) & (d < 17)] += 1
            # bevel: lit top edge, shadowed bottom edge
            plank[0, :] += 2
            if ph > 2:
                plank[1, :] += 1
            tone[y0:y1, x0:x1] = plank
            plank_id[y0:y1, x0:x1] = pid
            # gaps between rows (2px) and plank ends (1px + highlight)
            if ph == PH:
                dark_gap[y1 - 1, x0:x1] = True
                tone[y1 - 2, x0:x1] -= 2
            if x >= 0:
                dark_gap[y0:y1, x0] = True
                if x0 + 1 < x1:
                    tone[y0:y1, x0 + 1] += 2
            # nails near the plank ends (2 per end)
            for nx in (x + 6, x + length - 7):
                if 1 <= nx < W - 2:
                    for ny in (y + 5, y + PH - 8):
                        if 0 <= ny < H - 2:
                            tone[ny:ny + 2, nx:nx + 2] = 2
                            tone[ny, nx] = 10
        x += length
    y += PH

# ---------- cracks (dark jagged lines along the grain) ----------
for _ in range(14):
    cx, cy = int(rng.integers(0, W)), int(rng.integers(0, H))
    for _s in range(int(rng.integers(20, 70))):
        if 0 <= cx < W and 0 <= cy < H and not dark_gap[cy, cx]:
            tone[cy, cx] -= 3
        cx += 1
        if rng.random() < 0.18:
            cy += int(rng.choice([-1, 1]))

# ---------- scratches and boot scuffs (light, short, slightly diagonal) ----------
for _ in range(90):
    sx, sy = int(rng.integers(0, W)), int(rng.integers(0, H))
    ln = int(rng.integers(5, 22))
    sl = rng.random() * 0.6 - 0.3
    for i in range(ln):
        px, py = sx + i, int(sy + i * sl)
        if 0 <= px < W and 0 <= py < H and not dark_gap[py, px]:
            tone[py, px] += 2


# ---------- seam grime: dirt packed into the gaps darkens the pixels beside them ----------
near = np.zeros((H, W), dtype=bool)
for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0)):
    near |= np.roll(np.roll(dark_gap, dy, axis=0), dx, axis=1)
near &= ~dark_gap
tone -= (near & (rng.random((H, W)) < 0.55)).astype(int)

# ---------- dents and chips (small dark pit with a lit lower lip) ----------
for _ in range(120):
    dx_, dy_ = int(rng.integers(2, W - 4)), int(rng.integers(2, H - 4))
    if dark_gap[dy_:dy_ + 2, dx_:dx_ + 3].any():
        continue
    w_, h_ = int(rng.integers(2, 4)), int(rng.integers(1, 3))
    tone[dy_:dy_ + h_, dx_:dx_ + w_] -= 2
    tone[dy_ + h_, dx_:dx_ + w_] += 1

# ---------- chewed plank ends: ragged notches where boards meet ----------
for _ in range(40):
    ex, ey = int(rng.integers(2, W - 6)), int(rng.integers(0, H))
    if dark_gap[ey, ex]:
        for k in range(int(rng.integers(2, 5))):
            if 0 <= ey + k < H:
                tone[ey + k, min(W - 1, ex + 1 + (k % 2))] -= 3

# ---------- floating tone: wear path, blotches, stains, lantern glow, vignette ----------
ys, xs = np.mgrid[0:H, 0:W].astype(float)
blot = value_noise(48, 7) * 3.2 + value_noise(16, 8) * 1.6 + value_noise(5, 11) * 0.8 - 2.9       # patchy colour drift
path_y = H * 0.52 + 70 * np.sin(xs * 0.011 + 0.6) + 18 * np.sin(xs * 0.043)
band = np.clip(1 - np.abs(ys - path_y) / 58, 0, 1) ** 1.5               # well-trodden walkway
wear = band * (2.0 + value_noise(10, 9) * 2.2)

stain = np.zeros((H, W))
for _ in range(5):
    sx, sy, sr = rng.integers(0, W), rng.integers(0, H), rng.integers(14, 34)
    d = np.hypot(xs - sx, ys - sy) / sr + (value_noise(14, int(rng.integers(0, 999))) - 0.5) * 0.55
    stain += np.clip(1.05 - d, 0, 1) * 4.0
    rim = (d > 0.95) & (d < 1.12)
    stain[rim] -= 0.9                                                  # dried-ring edge

cxg, cyg = W * 0.5, H * 0.42
dist = np.hypot((xs - cxg) / W, (ys - cyg) / H)
glow = 3.0 * np.clip(1 - dist / 0.62, 0, 1) ** 1.3
vign = -6.0 * np.clip((dist - 0.26) / 0.46, 0, 1) ** 1.5

field = blot + wear - stain + glow + vign
tone = tone + bayer_round(field)
tone -= ((rng.random((H, W)) < 0.05) & (field < 0.5)).astype(int)
tone[dark_gap] = np.where(rng.random(dark_gap.sum()) < 0.5, 0, 1) + 0  # near-black seams
# keep seams dark even under the glow, but let vignette show
tone = np.clip(tone, 0, N - 1)

# ---------- chunkier pixels: average each DOWN x DOWN block, but keep seams as dark seams ----------
if DOWN > 1:
    blocks = tone.reshape(H // DOWN, DOWN, W // DOWN, DOWN)
    avg = np.floor(blocks.mean(axis=(1, 3)) + 0.5).astype(int)
    seam = dark_gap.reshape(H // DOWN, DOWN, W // DOWN, DOWN).any(axis=(1, 3))
    tone = np.where(seam, blocks.min(axis=(1, 3)), avg)
OH, OW = tone.shape

# ---------- straw and crumbs ----------
rgb = PAL[tone]
STRAW = [(0xC9, 0xA4, 0x4E), (0xE0, 0xC0, 0x6A), (0x9A, 0x7B, 0x3A)]
for _ in range(34):
    sx, sy = int(rng.integers(0, OW - 6)), int(rng.integers(0, OH - 3))
    ln, sl = int(rng.integers(2, 5)), int(rng.choice([-1, 0, 1]))
    col = STRAW[int(rng.integers(0, 3))]
    for i in range(ln):
        px, py = sx + i, min(OH - 1, max(0, sy + (i * sl) // 3))
        rgb[py, px] = col

out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "assets" / "floor.png"
out.parent.mkdir(parents=True, exist_ok=True)
Image.fromarray(rgb, "RGB").save(out, optimize=True)
print(f"wrote {out} ({OW}x{OH}, {out.stat().st_size} bytes)")
