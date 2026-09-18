"""One grid system for every section.

Sites paints section backgrounds with `cover`, so the on-screen spacing is
img_step * (element_width / image_width) WHENEVER the scaling is driven by
width. Keep every image 2560 wide with the same step and the vertical lines
land in the same place in every section.

Width drives the scale only while the image is taller in proportion than the
section. Sections get made 2560x2560 so that holds for any realistic height;
the banner has to stay shorter because it carries text, so it is 2560x1000.

Horizontal lines are a different matter: `cover` centres vertically, so their
phase depends on each section's height and cannot be predicted. Hence the
columns-only set, which has nothing to misalign.
"""
import os
import numpy as np
from PIL import Image, ImageDraw
from gen_bg import bloom, dither, NAVY

OUT = "/home/user/drawing-set/google-sites/backgrounds"
STEP = 96                      # one number, every image
MAJOR = 5

def lines(im, step=STEP, colour=(255, 255, 255), a_minor=9, a_major=20,
          verticals=True, horizontals=True):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    w, h = im.size
    if verticals:
        for i, x in enumerate(range(0, w + 1, step)):
            major = i % MAJOR == 0
            d.line([x, 0, x, h], fill=colour + (a_major if major else a_minor,),
                   width=2 if major else 1)
    if horizontals:
        for i, y in enumerate(range(0, h + 1, step)):
            major = i % MAJOR == 0
            d.line([0, y, w, y], fill=colour + (a_major if major else a_minor,),
                   width=2 if major else 1)
    return Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")

def save(im, name):
    p = os.path.join(OUT, name)
    dither(im).save(p, quality=92, optimize=True, subsampling=1)
    print("%-42s %4dx%-5d %5.0f KB" % (name, im.size[0], im.size[1],
                                       os.path.getsize(p) / 1024))

S = (2560, 2560)     # section: square, so width always drives the scale
B = (2560, 1000)     # banner: shorter, carries text

flat_s  = Image.new("RGB", S, NAVY)
bloom_s = bloom(S, NAVY, (26, 78, 140), S[0] * .88, S[1] * .04, S[0] * 1.15, strength=.8)
flat_b  = Image.new("RGB", B, NAVY)
bloom_b = bloom(B, NAVY, (26, 78, 140), B[0] * .86, B[1] * .06, B[0] * 1.15, strength=.8)

# full grid -- vertical lines align across sections, horizontals will not
save(lines(flat_s),  "grid-section-flat.jpg")
save(lines(bloom_s), "grid-section-bloom.jpg")
save(lines(flat_b),  "grid-banner-flat.jpg")
save(lines(bloom_b), "grid-banner-bloom.jpg")

# columns only -- nothing to misalign, matches everywhere
save(lines(flat_s,  horizontals=False), "cols-section-flat.jpg")
save(lines(bloom_s, horizontals=False), "cols-section-bloom.jpg")
save(lines(flat_b,  horizontals=False), "cols-banner-flat.jpg")
save(lines(bloom_b, horizontals=False), "cols-banner-bloom.jpg")
