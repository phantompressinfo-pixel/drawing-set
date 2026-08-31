"""16 further dashboard layout concepts (09-24), all using the EAD icon set + brand colours."""
import os
from PIL import Image, ImageDraw, ImageFilter
from gen_layouts import (
    W, H, NAVY, NAVY_DEEP, NAVY_MID, CHAR, PAPER, WHITE, HAIR, MUTE, ICE,
    REDLINE, GOOD, FB, FR, FM, f, NAV, ACTIVE, TITLE, SUB, CARDS,
    lin_grad, radial_glow, light_card, dark_card, wrap, grid, shadow,
)

ICON_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
NAV_ICON = ["home", "announcements", "standards", "templates", "forms",
            "policies", "sops", "revit", "directory"]
TILE = [("Standards", "standards"), ("Templates", "templates"), ("Forms", "forms"),
        ("Policies", "policies"), ("SOPs", "sops"), ("Revit Std.", "revit"),
        ("Learning", "learning")]
CHARCOAL = (75, 75, 75)
CHAR_DEEP = (48, 48, 48)


def icon(name, size, white=False):
    p = os.path.join(ICON_DIR, name + ("_white" if white else "") + ".png")
    return Image.open(p).convert("RGBA").resize((size, size), Image.LANCZOS)


def put(im, name, x, y, size, white=False):
    ic = icon(name, size, white)
    im.paste(ic, (int(x), int(y)), ic)


def tint_icon(name, size, color):
    ic = icon(name, size, white=True)
    solid = Image.new("RGBA", ic.size, color + (0,))
    solid.putalpha(ic.split()[3])
    return solid


def put_tinted(im, name, x, y, size, color):
    ic = tint_icon(name, size, color)
    im.paste(ic, (int(x), int(y)), ic)


# ===================================================================
# 09 — ICON RAIL : slim icon-only navy rail + text nav column
# ===================================================================
def layout_09():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 118, H], fill=NAVY)
    d.rectangle([118, 0, 400, H], fill=WHITE)
    d.line([400, 0, 400, H], fill=HAIR, width=2)
    put(im, "home", 43, 44, 34, white=True)
    d = ImageDraw.Draw(im)
    iy = 156
    for i, nm in enumerate(NAV_ICON):
        if i == ACTIVE:
            d.rounded_rectangle([16, iy - 14, 102, iy + 46], radius=12, fill=(255, 255, 255))
            put(im, nm, 43, iy, 32)
        else:
            put(im, nm, 43, iy, 32, white=True)
        d = ImageDraw.Draw(im)
        iy += 88
    d.text((150, 46), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((150, 78), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    ny = 160
    for i, it in enumerate(NAV):
        if i == ACTIVE:
            d.rectangle([118, ny - 12, 400, ny + 40], fill=(233, 238, 244))
            d.rectangle([394, ny - 12, 400, ny + 40], fill=REDLINE)
        d.text((150, ny), it, font=f(FB if i == ACTIVE else FR, 19), fill=NAVY if i == ACTIVE else CHAR)
        ny += 62
    d.text((450, 60), TITLE, font=f(FB, 52), fill=NAVY)
    d.text((453, 128), SUB, font=f(FR, 20), fill=CHAR)
    d.line([450, 176, W - 60, 176], fill=NAVY, width=3)
    grid(d, 450, 214, W - 60, H - 60, 3, 2, light_card)
    return im


# ===================================================================
# 10 — ICON TILES : no sidebar, oversized icon tiles are the interface
# ===================================================================
def layout_10():
    im = radial_glow((W, H), PAPER, (198, 210, 226), W * 0.5, H * 1.1, W * 0.95, strength=0.9)
    d = ImageDraw.Draw(im)
    d.text((60, 48), "EIGELBERGER", font=f(FB, 28), fill=NAVY)
    d.text((60, 86), "OFFICE HUB", font=f(FM, 13), fill=CHAR)
    d.rounded_rectangle([W - 760, 44, W - 60, 104], radius=30, fill=WHITE, outline=HAIR, width=2)
    d.text((W - 726, 64), "Search standards, templates, forms, SOPs…", font=f(FM, 17), fill=MUTE)
    d.text((60, 176), "What are you looking for?", font=f(FB, 46), fill=NAVY)
    cols, cw, ch, gx, gy = 4, 424, 250, 30, 28
    x0, y0 = 60, 274
    for i, (label, ic) in enumerate(TILE):
        c, r = i % cols, i // cols
        x, y = x0 + c * (cw + gx), y0 + r * (ch + gy)
        shadow(d, (x, y, x + cw, y + ch), radius=16, spread=6, color=(210, 218, 228))
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=16, fill=WHITE, outline=HAIR, width=2)
        d.rounded_rectangle([x + 28, y + 34, x + 116, y + 122], radius=20, fill=NAVY)
        put(im, ic, x + 50, y + 56, 44, white=True)
        d = ImageDraw.Draw(im)
        d.text((x + 28, y + 148), label.upper(), font=f(FB, 26), fill=NAVY)
        d.text((x + 28, y + 188), "6 documents", font=f(FM, 15), fill=MUTE)
    return im


# ===================================================================
# 11 — HERO + ICON CHIPS : navy hero, icon chip row beneath the title
# ===================================================================
def layout_11():
    im = Image.new("RGB", (W, H), PAPER)
    im.paste(radial_glow((W, 420), NAVY, NAVY_MID, W * 0.78, 0, W * 0.7, strength=0.8), (0, 0))
    d = ImageDraw.Draw(im)
    d.text((60, 44), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((60, 78), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.text((60, 140), TITLE, font=f(FB, 58), fill=(255, 255, 255))
    d.text((64, 214), SUB, font=f(FR, 20), fill=ICE)
    x = 60
    for label, ic in TILE:
        tw = int(d.textlength(label.upper(), font=f(FB, 17))) + 96
        active = label == "Standards"
        d.rounded_rectangle([x, 286, x + tw, 358], radius=36,
                            fill=(255, 255, 255) if active else (16, 56, 106),
                            outline=None if active else (58, 100, 152), width=2)
        put(im, ic, x + 26, 306, 32, white=not active)
        d = ImageDraw.Draw(im)
        d.text((x + 74, 312), label.upper(), font=f(FB, 17), fill=NAVY if active else ICE)
        x += tw + 16
    grid(d, 60, 462, W - 60, H - 60, 3, 2, light_card)
    return im


# ===================================================================
# 12 — BENTO : one feature tile plus a mosaic of smaller ones
# ===================================================================
def layout_12():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 116], fill=WHITE)
    d.line([0, 116, W, 116], fill=NAVY, width=3)
    d.text((54, 30), "EIGELBERGER", font=f(FB, 26), fill=NAVY)
    d.text((54, 64), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    x = 620
    for i, it in enumerate(NAV[:7]):
        d.text((x, 52), it, font=f(FB if i == ACTIVE else FR, 17), fill=NAVY if i == ACTIVE else CHAR)
        if i == ACTIVE:
            d.line([x, 82, x + int(d.textlength(it, font=f(FB, 17))), 82], fill=REDLINE, width=4)
        x += int(d.textlength(it, font=f(FR, 17))) + 40
    d.text((54, 152), TITLE, font=f(FB, 48), fill=NAVY)
    # feature tile
    feat = (54, 240, 880, 700)
    grad = radial_glow((feat[2] - feat[0], feat[3] - feat[1]), NAVY, NAVY_MID,
                       (feat[2] - feat[0]) * 0.15, (feat[3] - feat[1]) * 0.9, (feat[2] - feat[0]), strength=0.8)
    m = Image.new("L", grad.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, grad.size[0], grad.size[1]], radius=20, fill=255)
    im.paste(grad, (feat[0], feat[1]), m)
    d = ImageDraw.Draw(im)
    put(im, "standards", feat[0] + 46, feat[1] + 46, 56, white=True)
    d = ImageDraw.Draw(im)
    d.text((feat[0] + 46, feat[1] + 132), "Drafting & CAD", font=f(FB, 44), fill=(255, 255, 255))
    d.text((feat[0] + 46, feat[1] + 184), "Standards", font=f(FB, 44), fill=(255, 255, 255))
    ty = feat[1] + 268
    for line in wrap("Line weights, layer naming, hatch patterns, and dimensioning conventions for every drawing set.", 44):
        d.text((feat[0] + 48, ty), line, font=f(FR, 19), fill=ICE); ty += 28
    d.rounded_rectangle([feat[0] + 46, feat[3] - 90, feat[0] + 250, feat[3] - 40], radius=25, fill=(255, 255, 255))
    d.text((feat[0] + 86, feat[3] - 78), "OPEN  ↗", font=f(FB, 17), fill=NAVY)
    # mosaic
    small = [(920, 240, 1400, 460), (1440, 240, 1866, 460),
             (920, 484, 1250, 700), (1290, 484, 1866, 700)]
    for i, box in enumerate(small):
        card = CARDS[i + 1]
        shadow(d, box, radius=16, spread=5, color=(214, 220, 228))
        d.rounded_rectangle(box, radius=16, fill=WHITE, outline=HAIR, width=2)
        put(im, TILE[(i + 1) % len(TILE)][1], box[0] + 26, box[1] + 26, 34)
        d = ImageDraw.Draw(im)
        ty = box[1] + 82
        for line in wrap(card[1], 22):
            d.text((box[0] + 26, ty), line, font=f(FB, 24), fill=NAVY); ty += 29
        d.text((box[0] + 26, box[3] - 40), card[3], font=f(FM, 13), fill=MUTE)
    # bottom strip
    d.rounded_rectangle([54, 726, W - 54, H - 54], radius=16, fill=(232, 237, 243), outline=HAIR, width=2)
    d.rectangle([54, 726, 60, H - 54], fill=REDLINE)
    d.text((96, 754), "LATEST ANNOUNCEMENT", font=f(FM, 14), fill=NAVY)
    d.text((96, 790), "Revit 2027 rollout begins next month", font=f(FB, 26), fill=NAVY)
    d.text((96, 830), "IT will begin migrating active projects starting mid-September.", font=f(FR, 18), fill=CHAR)
    return im


# ===================================================================
# 13 — FLAT PANELS : icon strip, no card chrome, ruled sections
# ===================================================================
def layout_13():
    im = Image.new("RGB", (W, H), (247, 248, 250))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 128, H], fill=NAVY)
    put(im, "home", 47, 40, 34, white=True)
    d = ImageDraw.Draw(im)
    iy = 150
    for i, nm in enumerate(NAV_ICON):
        if i == ACTIVE:
            d.rectangle([0, iy - 16, 128, iy + 48], fill=(255, 255, 255))
            d.rectangle([0, iy - 16, 6, iy + 48], fill=REDLINE)
            put(im, nm, 47, iy, 32)
        else:
            put(im, nm, 47, iy, 32, white=True)
        d = ImageDraw.Draw(im)
        iy += 92
    d.text((190, 56), TITLE, font=f(FB, 54), fill=NAVY)
    d.text((193, 126), SUB, font=f(FR, 20), fill=CHAR)
    y = 210
    for i, card in enumerate(CARDS):
        d.line([190, y, W - 70, y], fill=(224, 229, 235), width=2)
        put(im, TILE[i % len(TILE)][1], 200, y + 34, 34)
        d = ImageDraw.Draw(im)
        d.text((266, y + 30), card[1], font=f(FB, 27), fill=NAVY)
        d.text((266, y + 68), card[2], font=f(FR, 18), fill=CHAR)
        d.text((W - 340, y + 42), card[0], font=f(FM, 14), fill=MUTE)
        d.text((W - 200, y + 42), card[3], font=f(FM, 14), fill=MUTE)
        d.text((W - 108, y + 42), "↗", font=f(FB, 22), fill=NAVY)
        y += 122
    return im


# ===================================================================
# 14 — RIBBON : navy toolbar of icon+label between header and content
# ===================================================================
def layout_14():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 108], fill=WHITE)
    d.text((54, 26), "EIGELBERGER", font=f(FB, 26), fill=NAVY)
    d.text((54, 60), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=CHAR)
    d.rounded_rectangle([W - 700, 26, W - 54, 82], radius=28, fill=(238, 241, 245), outline=HAIR, width=2)
    d.text((W - 668, 44), "Search the office hub…", font=f(FM, 16), fill=MUTE)
    ribbon = lin_grad((W, 168), NAVY, NAVY_MID, horizontal=True, power=1.0)
    im.paste(ribbon, (0, 108))
    d = ImageDraw.Draw(im)
    seg = W / 7
    for i, (label, ic) in enumerate(TILE):
        cx = seg * i + seg / 2
        active = label == "Standards"
        if active:
            d.rectangle([seg * i, 108, seg * (i + 1), 276], fill=(255, 255, 255))
            d.rectangle([seg * i, 268, seg * (i + 1), 276], fill=REDLINE)
        put(im, ic, cx - 20, 140, 40, white=not active)
        d = ImageDraw.Draw(im)
        tw = d.textlength(label.upper(), font=f(FB, 16))
        d.text((cx - tw / 2, 200), label.upper(), font=f(FB, 16), fill=NAVY if active else (255, 255, 255))
    d.text((54, 316), TITLE, font=f(FB, 48), fill=NAVY)
    d.text((57, 380), SUB, font=f(FR, 19), fill=CHAR)
    grid(d, 54, 434, W - 54, H - 54, 3, 2, light_card)
    return im


# ===================================================================
# 15 — BADGE ROW : circular navy icon badges over a table-style list
# ===================================================================
def layout_15():
    im = radial_glow((W, H), PAPER, (204, 215, 230), W * 0.08, H * 0.05, W, strength=0.85)
    d = ImageDraw.Draw(im)
    d.text((60, 48), "EIGELBERGER  ·  OFFICE HUB", font=f(FB, 24), fill=NAVY)
    d.rounded_rectangle([W - 700, 38, W - 60, 96], radius=29, fill=WHITE, outline=HAIR, width=2)
    d.text((W - 666, 57), "Search the office hub…", font=f(FM, 16), fill=MUTE)
    x0, seg = 60, 250
    for i, (label, ic) in enumerate(TILE):
        cx = x0 + seg * i + 62
        active = label == "Standards"
        d.ellipse([cx - 52, 140, cx + 52, 244], fill=NAVY if active else WHITE,
                  outline=NAVY, width=0 if active else 3)
        put(im, ic, cx - 26, 166, 52, white=active)
        d = ImageDraw.Draw(im)
        tw = d.textlength(label.upper(), font=f(FB, 16))
        d.text((cx - tw / 2, 262), label.upper(), font=f(FB, 16), fill=NAVY)
    d.text((60, 336), TITLE, font=f(FB, 44), fill=NAVY)
    d.line([60, 402, W - 60, 402], fill=NAVY, width=3)
    y = 424
    for i, card in enumerate(CARDS):
        if i % 2 == 0:
            d.rectangle([60, y, W - 60, y + 96], fill=(255, 255, 255))
        d.text((84, y + 34), card[0], font=f(FM, 15), fill=MUTE)
        d.text((240, y + 28), card[1], font=f(FB, 24), fill=NAVY)
        d.text((900, y + 34), card[2], font=f(FR, 17), fill=CHAR)
        d.text((W - 260, y + 34), card[3], font=f(FM, 15), fill=MUTE)
        d.text((W - 120, y + 30), "Open ↗", font=f(FM, 15), fill=NAVY)
        d.line([60, y + 96, W - 60, y + 96], fill=(222, 228, 236), width=2)
        y += 96
    return im


# ===================================================================
# 16 — ICON WATERMARK : giant faint icon bleeding off the page
# ===================================================================
def layout_16():
    im = lin_grad((W, H), PAPER, (214, 223, 236), horizontal=True, power=1.2)
    ghost = tint_icon("standards", 1250, (2, 32, 73))
    ghost.putalpha(ghost.split()[3].point(lambda a: int(a * 0.10)))
    im.paste(ghost, (W - 780, H - 760), ghost)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 360, H], fill=NAVY)
    d.text((44, 48), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((44, 84), "OFFICE HUB", font=f(FM, 12), fill=ICE)
    ny = 168
    for i, (it, nm) in enumerate(zip(NAV, NAV_ICON)):
        if i == ACTIVE:
            d.rounded_rectangle([22, ny - 12, 338, ny + 42], radius=10, fill=(18, 58, 110))
        put(im, nm, 44, ny - 2, 28, white=True)
        d = ImageDraw.Draw(im)
        d.text((90, ny + 2), it, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else ICE)
        ny += 60
    d.text((420, 70), TITLE, font=f(FB, 54), fill=NAVY)
    d.text((423, 140), SUB, font=f(FR, 20), fill=CHAR)
    grid(d, 420, 210, W - 60, H - 60, 3, 2, light_card)
    return im


# ===================================================================
# 17 — LIST + DETAIL : master list left, expanded detail panel right
# ===================================================================
def layout_17():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 110], fill=NAVY)
    d.text((54, 28), "EIGELBERGER", font=f(FB, 25), fill=(255, 255, 255))
    d.text((54, 62), "OFFICE HUB", font=f(FM, 12), fill=ICE)
    x = 560
    for i, it in enumerate(NAV[:7]):
        d.text((x, 44), it, font=f(FB if i == ACTIVE else FR, 17),
               fill=(255, 255, 255) if i == ACTIVE else ICE)
        x += int(d.textlength(it, font=f(FR, 17))) + 38
    d.rectangle([0, 110, 700, H], fill=WHITE)
    d.line([700, 110, 700, H], fill=HAIR, width=2)
    d.text((44, 142), TITLE.upper(), font=f(FM, 15), fill=MUTE)
    y = 190
    for i, card in enumerate(CARDS):
        sel = i == 0
        if sel:
            d.rectangle([0, y, 700, y + 118], fill=(233, 238, 245))
            d.rectangle([0, y, 6, y + 118], fill=NAVY)
        put(im, TILE[i % len(TILE)][1], 44, y + 40, 32)
        d = ImageDraw.Draw(im)
        d.text((104, y + 30), card[1], font=f(FB, 23), fill=NAVY)
        d.text((104, y + 66), card[0] + "   ·   " + card[3], font=f(FM, 14), fill=MUTE)
        d.line([44, y + 118, 700, y + 118], fill=(228, 233, 239), width=2)
        y += 118
    panel = (760, 160, W - 60, H - 60)
    shadow(d, panel, radius=20, spread=6, color=(212, 219, 228))
    d.rounded_rectangle(panel, radius=20, fill=WHITE, outline=HAIR, width=2)
    d.rounded_rectangle([panel[0] + 44, panel[1] + 44, panel[0] + 148, panel[1] + 148], radius=24, fill=NAVY)
    put(im, "standards", panel[0] + 70, panel[1] + 70, 52, white=True)
    d = ImageDraw.Draw(im)
    d.text((panel[0] + 178, panel[1] + 58), "STD-101", font=f(FM, 15), fill=MUTE)
    d.text((panel[0] + 178, panel[1] + 88), "Drafting & CAD Standards", font=f(FB, 38), fill=NAVY)
    ty = panel[1] + 190
    for line in wrap("Line weights, layer naming, hatch patterns, and dimensioning conventions used on every "
                     "drawing set the office issues. Applies to all disciplines and all phases.", 62):
        d.text((panel[0] + 46, ty), line, font=f(FR, 20), fill=CHAR); ty += 32
    d.line([panel[0] + 46, ty + 26, panel[2] - 46, ty + 26], fill=HAIR, width=2)
    for j, (k, v) in enumerate([("FORMAT", "PDF"), ("STATUS", "Required"), ("UPDATED", "01 JUN 2026")]):
        d.text((panel[0] + 46 + j * 250, ty + 60), k, font=f(FM, 13), fill=MUTE)
        d.text((panel[0] + 46 + j * 250, ty + 88), v, font=f(FB, 21), fill=NAVY)
    d.rounded_rectangle([panel[0] + 46, panel[3] - 106, panel[0] + 266, panel[3] - 46], radius=30, fill=NAVY)
    d.text((panel[0] + 96, panel[3] - 90), "OPEN  ↗", font=f(FB, 18), fill=(255, 255, 255))
    return im


# ===================================================================
# 18 — CHARCOAL BASE : charcoal surfaces, navy as the accent
# ===================================================================
def layout_18():
    im = radial_glow((W, H), (38, 38, 38), (66, 66, 66), W * 0.8, H * 0.1, W, strength=0.8)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 340, H], fill=CHAR_DEEP)
    d.text((44, 46), "EIGELBERGER", font=f(FB, 25), fill=(255, 255, 255))
    d.text((44, 80), "OFFICE HUB", font=f(FM, 12), fill=(168, 168, 168))
    ny = 156
    for i, (it, nm) in enumerate(zip(NAV, NAV_ICON)):
        if i == ACTIVE:
            d.rounded_rectangle([18, ny - 12, 322, ny + 44], radius=10, fill=NAVY)
        put(im, nm, 44, ny, 28, white=True)
        d = ImageDraw.Draw(im)
        d.text((90, ny + 3), it, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else (188, 188, 188))
        ny += 60
    d.text((400, 60), TITLE, font=f(FB, 50), fill=(255, 255, 255))
    d.text((403, 128), SUB, font=f(FR, 19), fill=(190, 190, 190))
    d.line([400, 178, W - 60, 178], fill=NAVY, width=4)
    grid(d, 400, 216, W - 60, H - 60, 3, 2,
         lambda dd, box, card: dark_card(dd, box, card, panel=(56, 56, 56), border=(90, 90, 90),
                                         title_col=(255, 255, 255), body_col=(186, 186, 186)))
    return im


# ===================================================================
# 19 — SHEET FRAME : thick navy border framing the page, corner block
# ===================================================================
def layout_19():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    B = 26
    d.rectangle([0, 0, W, H], fill=NAVY)
    d.rectangle([B, B, W - B, H - B], fill=PAPER)
    d.rectangle([B, B, W - B, 132], fill=WHITE)
    d.line([B, 132, W - B, 132], fill=NAVY, width=3)
    put(im, "home", B + 28, 52, 34)
    d = ImageDraw.Draw(im)
    d.text((B + 82, 46), "EIGELBERGER", font=f(FB, 26), fill=NAVY)
    d.text((B + 82, 80), "ARCHITECTURE & DESIGN   ·   OFFICE HUB", font=f(FM, 12), fill=CHAR)
    x = 700
    for i, it in enumerate(NAV[:7]):
        d.text((x, 62), it, font=f(FB if i == ACTIVE else FR, 17), fill=NAVY if i == ACTIVE else CHAR)
        if i == ACTIVE:
            d.line([x, 92, x + int(d.textlength(it, font=f(FB, 17))), 92], fill=REDLINE, width=4)
        x += int(d.textlength(it, font=f(FR, 17))) + 34
    d.text((B + 40, 176), TITLE, font=f(FB, 50), fill=NAVY)
    d.text((B + 43, 244), SUB, font=f(FR, 19), fill=CHAR)
    grid(d, B + 40, 306, W - B - 40, H - 190, 3, 2, light_card)
    d.rectangle([W - 470, H - 158, W - B, H - B], fill=WHITE, outline=NAVY, width=3)
    d.line([W - 470, H - 104, W - B, H - 104], fill=NAVY, width=2)
    d.text((W - 452, H - 146), "EIGELBERGER ARCHITECTURE & DESIGN", font=f(FM, 13), fill=NAVY)
    d.text((W - 452, H - 90), "OFFICE HUB", font=f(FB, 22), fill=NAVY)
    d.text((W - 180, H - 84), "28 AUG 2026", font=f(FM, 13), fill=CHAR)
    return im


# ===================================================================
# 20 — MESH GLOW : soft multi-point navy bloom, glassy white cards
# ===================================================================
def layout_20():
    base = radial_glow((W, H), PAPER, (150, 174, 208), W * 0.08, H * 0.12, W * 0.75, strength=0.9)
    b2 = radial_glow((W, H), PAPER, (176, 190, 220), W * 0.95, H * 0.85, W * 0.7, strength=0.9)
    im = Image.blend(base, b2, 0.5).filter(ImageFilter.GaussianBlur(2))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, 32, W - 40, 118], radius=43, fill=(255, 255, 255))
    put(im, "home", 74, 58, 34)
    d = ImageDraw.Draw(im)
    d.text((128, 52), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((128, 82), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    x = 560
    for i, it in enumerate(NAV[:7]):
        tw = int(d.textlength(it, font=f(FB, 17))) + 36
        if i == ACTIVE:
            d.rounded_rectangle([x - 18, 46, x + tw - 18, 104], radius=29, fill=NAVY)
        d.text((x, 65), it, font=f(FB if i == ACTIVE else FR, 17),
               fill=(255, 255, 255) if i == ACTIVE else CHAR)
        x += tw + 8
    d.text((60, 172), TITLE, font=f(FB, 56), fill=NAVY)
    d.text((64, 248), SUB, font=f(FR, 20), fill=(60, 72, 92))
    x = 60
    for label, ic in TILE:
        d.ellipse([x, 318, x + 68, 386], fill=(255, 255, 255))
        put(im, ic, x + 17, 335, 34)
        d = ImageDraw.Draw(im)
        x += 92
    grid(d, 60, 428, W - 60, H - 56, 3, 2, light_card)
    return im


# ===================================================================
# 21 — ICON TABS : tabs made of icon + label, joined to the panel
# ===================================================================
def layout_21():
    im = Image.new("RGB", (W, H), (236, 240, 245))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((54, 26), "EIGELBERGER", font=f(FB, 25), fill=(255, 255, 255))
    d.text((54, 60), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.rounded_rectangle([W - 660, 24, W - 54, 80], radius=28, fill=(14, 52, 100), outline=(48, 90, 142), width=2)
    d.text((W - 628, 42), "Search the office hub…", font=f(FM, 16), fill=ICE)
    tabw, x, ty = 250, 54, 128
    for i, (label, ic) in enumerate(TILE):
        active = label == "Standards"
        if active:
            d.rounded_rectangle([x, ty, x + tabw, ty + 108], radius=14, fill=WHITE)
            d.rectangle([x, ty + 60, x + tabw, ty + 108], fill=WHITE)
        else:
            d.rounded_rectangle([x, ty + 14, x + tabw, ty + 108], radius=14, fill=(220, 226, 234))
        put(im, ic, x + 24, ty + (32 if active else 40), 34)
        d = ImageDraw.Draw(im)
        d.text((x + 76, ty + (42 if active else 50)), label.upper(), font=f(FB, 17), fill=NAVY)
        x += tabw + 10
    panel = (54, 236, W - 54, H - 54)
    d.rounded_rectangle(panel, radius=14, fill=WHITE)
    d.text((panel[0] + 48, panel[1] + 42), TITLE, font=f(FB, 44), fill=NAVY)
    d.text((panel[0] + 51, panel[1] + 104), SUB, font=f(FR, 19), fill=CHAR)
    d.line([panel[0] + 48, panel[1] + 150, panel[2] - 48, panel[1] + 150], fill=HAIR, width=2)
    grid(d, panel[0] + 48, panel[1] + 186, panel[2] - 48, panel[3] - 44, 3, 2, light_card, gapx=28, gapy=24)
    return im


# ===================================================================
# 22 — INVERTED RAIL : light sidebar, navy content field
# ===================================================================
def layout_22():
    im = radial_glow((W, H), NAVY, NAVY_MID, W * 0.95, H * 0.95, W * 1.1, strength=0.75)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 360, H], fill=WHITE)
    put(im, "home", 44, 48, 34)
    d = ImageDraw.Draw(im)
    d.text((98, 44), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((98, 76), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    d.line([44, 124, 316, 124], fill=HAIR, width=2)
    ny = 166
    for i, (it, nm) in enumerate(zip(NAV, NAV_ICON)):
        if i == ACTIVE:
            d.rounded_rectangle([22, ny - 12, 338, ny + 44], radius=10, fill=NAVY)
        put(im, nm, 44, ny, 28, white=(i == ACTIVE))
        d = ImageDraw.Draw(im)
        d.text((90, ny + 3), it, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else CHAR)
        ny += 60
    d.rounded_rectangle([420, 44, 1180, 104], radius=30, fill=(12, 50, 98), outline=(52, 94, 146), width=2)
    d.text((454, 63), "Search standards, templates, forms, SOPs…", font=f(FM, 16), fill=ICE)
    d.text((420, 148), TITLE, font=f(FB, 52), fill=(255, 255, 255))
    d.text((423, 218), SUB, font=f(FR, 19), fill=ICE)
    d.line([420, 268, W - 60, 268], fill=(70, 112, 162), width=2)
    grid(d, 420, 306, W - 60, H - 60, 3, 2,
         lambda dd, box, card: dark_card(dd, box, card, panel=(10, 44, 88), border=(52, 94, 146)))
    return im


# ===================================================================
# 23 — POSTER TYPE : oversized title column, compact card stack
# ===================================================================
def layout_23():
    im = lin_grad((W, H), PAPER, (206, 217, 232), horizontal=False, power=1.3)
    d = ImageDraw.Draw(im)
    d.text((70, 60), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((70, 92), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=CHAR)
    d.text((70, 190), "OFFICE", font=f(FB, 96), fill=NAVY)
    d.text((70, 292), "STANDARDS", font=f(FB, 96), fill=NAVY)
    d.line([70, 424, 760, 424], fill=REDLINE, width=6)
    ty = 462
    for line in wrap(SUB, 36):
        d.text((70, ty), line, font=f(FR, 22), fill=CHAR); ty += 34
    x = 70
    for label, ic in TILE[:5]:
        d.ellipse([x, 620, x + 74, 694], fill=WHITE, outline=NAVY, width=2)
        put(im, ic, x + 19, 639, 36)
        d = ImageDraw.Draw(im)
        x += 92
    d.text((70, 736), "6 DOCUMENTS IN THIS SECTION", font=f(FM, 15), fill=MUTE)
    y = 70
    for card in CARDS[:5]:
        box = (900, y, W - 70, y + 174)
        shadow(d, box, radius=12, spread=4, color=(206, 214, 226))
        d.rounded_rectangle(box, radius=12, fill=WHITE, outline=HAIR, width=2)
        d.text((box[0] + 28, y + 26), card[0], font=f(FM, 13), fill=MUTE)
        d.text((box[0] + 28, y + 56), card[1], font=f(FB, 27), fill=NAVY)
        d.text((box[0] + 28, y + 100), card[2], font=f(FR, 17), fill=CHAR)
        d.text((box[0] + 28, y + 136), card[3], font=f(FM, 13), fill=MUTE)
        d.text((box[2] - 100, y + 132), "Open ↗", font=f(FM, 14), fill=NAVY)
        y += 194
    return im


# ===================================================================
# 24 — SEARCH FIRST : search as the hero, icon shortcuts beneath
# ===================================================================
def layout_24():
    im = radial_glow((W, H), (238, 241, 246), (168, 188, 214), W * 0.5, H * -0.1, W * 1.0, strength=0.95)
    d = ImageDraw.Draw(im)
    d.text((60, 46), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((60, 78), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    x = W - 120
    for it in reversed(NAV[:5]):
        tw = int(d.textlength(it, font=f(FR, 17)))
        d.text((x - tw, 58), it, font=f(FR, 17), fill=CHAR)
        x -= tw + 40
    tw = d.textlength("Everything the office needs, in one place.", font=f(FB, 46))
    d.text(((W - tw) / 2, 168), "Everything the office needs, in one place.", font=f(FB, 46), fill=NAVY)
    d.rounded_rectangle([(W - 1180) / 2 + 5, 268, (W + 1180) / 2 + 5, 364], radius=48, fill=(198, 208, 222))
    d.rounded_rectangle([(W - 1180) / 2, 262, (W + 1180) / 2, 358], radius=48, fill=WHITE, outline=HAIR, width=2)
    d.text(((W - 1180) / 2 + 54, 294), "Search standards, templates, forms, SOPs, Revit standards…",
           font=f(FM, 22), fill=MUTE)
    d.rounded_rectangle([(W + 1180) / 2 - 168, 278, (W + 1180) / 2 - 20, 342], radius=32, fill=NAVY)
    d.text(((W + 1180) / 2 - 128, 298), "SEARCH", font=f(FB, 18), fill=(255, 255, 255))
    total = 7 * 150 + 6 * 26
    x = (W - total) / 2
    for label, ic in TILE:
        d.rounded_rectangle([x, 428, x + 150, 578], radius=18, fill=WHITE, outline=HAIR, width=2)
        d.rounded_rectangle([x + 51, 456, x + 99, 504], radius=14, fill=NAVY)
        put(im, ic, x + 63, 468, 24, white=True)
        d = ImageDraw.Draw(im)
        lw = d.textlength(label.upper(), font=f(FB, 14))
        d.text((x + 75 - lw / 2, 526), label.upper(), font=f(FB, 14), fill=NAVY)
        x += 176
    d.text((60, 638), "RECENTLY UPDATED", font=f(FM, 15), fill=NAVY)
    d.line([60, 674, W - 60, 674], fill=NAVY, width=2)
    y = 694
    for card in CARDS[:4]:
        d.text((60, y + 16), card[1], font=f(FB, 24), fill=NAVY)
        d.text((700, y + 22), card[2], font=f(FR, 17), fill=CHAR)
        d.text((W - 300, y + 22), card[3], font=f(FM, 14), fill=MUTE)
        d.text((W - 140, y + 18), "Open ↗", font=f(FM, 15), fill=NAVY)
        d.line([60, y + 74, W - 60, y + 74], fill=(216, 224, 234), width=2)
        y += 84
    return im


LAYOUTS2 = [
    ("09  ICON RAIL", layout_09), ("10  ICON TILES", layout_10),
    ("11  HERO + ICON CHIPS", layout_11), ("12  BENTO GRID", layout_12),
    ("13  FLAT PANELS", layout_13), ("14  RIBBON NAV", layout_14),
    ("15  BADGE ROW", layout_15), ("16  ICON WATERMARK", layout_16),
    ("17  LIST + DETAIL", layout_17), ("18  CHARCOAL BASE", layout_18),
    ("19  SHEET FRAME", layout_19), ("20  MESH GLOW", layout_20),
    ("21  ICON TABS", layout_21), ("22  INVERTED RAIL", layout_22),
    ("23  POSTER TYPE", layout_23), ("24  SEARCH FIRST", layout_24),
]

if __name__ == "__main__":
    rendered = []
    for name, fn in LAYOUTS2:
        im = fn()
        slug = name.split()[0]
        im.save("layout_%s.png" % slug)
        rendered.append((name, im))
        print("rendered", name)

    TW, TH = 940, 529
    PADX, PADY, LBL = 26, 60, 46
    for sheet_i in range(2):
        chunk = rendered[sheet_i * 8:(sheet_i + 1) * 8]
        sheet = Image.new("RGB", (PADX * 3 + TW * 2, PADY + (TH + LBL + PADY) * 4), (255, 255, 255))
        sd = ImageDraw.Draw(sheet)
        for i, (name, im) in enumerate(chunk):
            col, row = i % 2, i // 2
            x = PADX + col * (TW + PADX)
            y = PADY + row * (TH + LBL + PADY)
            sd.text((x, y - 36), name, font=f(FB, 27), fill=NAVY)
            sheet.paste(im.resize((TW, TH), Image.LANCZOS), (x, y))
            sd.rectangle([x, y, x + TW, y + TH], outline=(178, 188, 198), width=2)
        sheet.save("layout_options_%d.png" % (sheet_i + 2))
        print("saved sheet", sheet_i + 2)
