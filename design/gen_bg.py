"""Full-bleed section backgrounds. Sites stretches these edge to edge."""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

OUT = "/home/user/drawing-set/google-sites/backgrounds"
NAVY = (2, 32, 73)
W, H = 2560, 1440
BW, BH = 2560, 760          # banner strip

def dither(im, amt=1):
    """8-bit gradients band badly on large flat fields; noise hides it."""
    a = np.array(im).astype(np.int16)
    a += np.random.randint(-amt, amt + 1, a.shape, dtype=np.int16)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

def bloom(size, base, glow, cx, cy, radius, strength=0.85, power=1.6):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / radius
    t = np.clip(1 - d, 0, 1) ** power * strength
    out = np.zeros((h, w, 3))
    for i in range(3):
        out[..., i] = base[i] + (glow[i] - base[i]) * t
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))

def solid(size, c):
    return Image.new("RGB", size, c)

def grid(im, step=96, colour=(255, 255, 255), major=5, a_minor=9, a_major=20):
    """Drafting grid — reads as paper, not as a table."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i, x in enumerate(range(0, im.size[0] + 1, step)):
        d.line([x, 0, x, im.size[1]], fill=colour + (a_major if i % major == 0 else a_minor,),
               width=2 if i % major == 0 else 1)
    for i, y in enumerate(range(0, im.size[1] + 1, step)):
        d.line([0, y, im.size[0], y], fill=colour + (a_major if i % major == 0 else a_minor,),
               width=2 if i % major == 0 else 1)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def contours(im, colour=(255, 255, 255), n=7, alpha=13):
    """Wide slow arcs — site-plan contour lines, not decoration."""
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    w, h = im.size
    cx, cy = w * 1.02, h * 1.25
    for i in range(n):
        r = w * (0.28 + i * 0.115)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=colour + (alpha,), width=3)
    ov = ov.filter(ImageFilter.GaussianBlur(0.6))
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def hgrad(size, c0, c1, power=1.0):
    w, h = size
    t = (np.linspace(0, 1, w) ** power)[None, :, None]
    a = np.array(c0)[None, None, :] + (np.array(c1) - np.array(c0))[None, None, :] * t
    return Image.fromarray(np.clip(np.repeat(a, h, 0), 0, 255).astype(np.uint8))

def save(im, name, q=90):
    im = dither(im)
    p = os.path.join(OUT, name)
    im.save(p, quality=q, optimize=True, subsampling=1)
    print("%-38s %4dx%-5d %6.0f KB" % (name, im.size[0], im.size[1], os.path.getsize(p) / 1024))

os.makedirs(OUT, exist_ok=True)

# ---- section backgrounds (tall) ------------------------------------
save(solid((W, H), NAVY),                                      "bg-1-navy-solid.jpg")
save(bloom((W, H), NAVY, (26, 78, 140), W * .88, H * .02, W * 1.2),
                                                               "bg-2-navy-bloom.jpg")
save(grid(solid((W, H), NAVY)),                                "bg-3-navy-grid.jpg")
save(contours(bloom((W, H), NAVY, (22, 70, 128), W * .9, H * .0, W * 1.25, strength=.7)),
                                                               "bg-4-navy-contour.jpg")
save(hgrad((W, H), (1, 22, 52), (18, 62, 116), power=1.15),    "bg-5-navy-fade.jpg")
save(grid(solid((W, H), (243, 245, 248)), colour=(2, 32, 73), a_minor=14, a_major=30),
                                                               "bg-6-paper-grid.jpg")

# ---- banner strips (short, for the page header) --------------------
save(bloom((BW, BH), NAVY, (26, 78, 140), BW * .86, BH * .06, BW * 1.15),
                                                               "banner-1-navy-bloom.jpg")
save(contours(bloom((BW, BH), NAVY, (22, 70, 128), BW * .9, BH * .05, BW * 1.2, strength=.7), n=6),
                                                               "banner-2-navy-contour.jpg")
save(grid(solid((BW, BH), NAVY), step=88),                     "banner-3-navy-grid.jpg")
