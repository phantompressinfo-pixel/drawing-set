"""Render 8 distinct dashboard layout concepts as mock pages for review."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1920, 1080

NAVY      = (2, 32, 73)
NAVY_DEEP = (1, 20, 46)
NAVY_MID  = (16, 56, 106)
CHAR      = (75, 75, 75)
PAPER     = (241, 243, 246)
WHITE     = (252, 253, 253)
HAIR      = (201, 209, 214)
MUTE      = (120, 132, 146)
ICE       = (198, 214, 232)
REDLINE   = (193, 67, 42)
GOOD      = (62, 125, 92)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FM = "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf"
FMB = "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf"
FMD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"  # has the ↗ glyph
def f(path, size): return ImageFont.truetype(path, size)

NAV = ["Home", "Announcements", "Office Standards", "Templates", "Forms",
       "Office Policies", "SOPs", "Revit Standards", "Staff Directory"]
ACTIVE = 2
TITLE = "Office Standards"
SUB   = "Drafting conventions, CAD standards, file naming, and deliverable requirements."
CARDS = [
    ("STD-101", "Drafting & CAD Standards", "Line weights, layer naming, hatch patterns, and dimensioning.", "PDF", "REQUIRED"),
    ("STD-102", "File Naming Convention", "Naming structure for drawings, models, and project folders.", "PDF", "REQUIRED"),
    ("STD-103", "Sheet Numbering Standard", "Discipline prefixes and sequencing for document sets.", "PDF", None),
    ("STD-104", "Deliverable Standards", "Required drawing content at SD, DD, CD, and CA phases.", "Google Doc", None),
    ("STD-105", "Plotting & Print Standards", "Pen tables, plot styles, and PDF export settings.", "PDF", "UPDATED"),
    ("STD-106", "Specification Format", "CSI MasterFormat divisions used in office specs.", "DOCX", None),
]


# ---------- gradient helpers ----------
def lin_grad(size, c0, c1, horizontal=True, power=1.0):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    t = (xx / max(w - 1, 1)) if horizontal else (yy / max(h - 1, 1))
    t = np.clip(t, 0, 1) ** power
    a = np.array(c0, dtype=np.float32)[None, None, :]
    b = np.array(c1, dtype=np.float32)[None, None, :]
    img = a + (b - a) * t[..., None]
    rng = np.random.default_rng(7)
    img = np.clip(img + (rng.random(img.shape) - 0.5) * 2.0, 0, 255).astype(np.uint8)
    return Image.fromarray(img)


def radial_glow(size, base, glow, cx, cy, radius, strength=0.6, power=1.6):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / radius
    t = np.clip(1 - d, 0, 1) ** power * strength
    a = np.array(base, dtype=np.float32)[None, None, :]
    b = np.array(glow, dtype=np.float32)[None, None, :]
    img = a + (b - a) * t[..., None]
    rng = np.random.default_rng(9)
    img = np.clip(img + (rng.random(img.shape) - 0.5) * 2.0, 0, 255).astype(np.uint8)
    return Image.fromarray(img)


def shadow(d, box, radius=10, spread=5, color=(210, 216, 222)):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0 + spread // 2, y0 + spread, x1 + spread // 2, y1 + spread],
                        radius=radius, fill=color)


# ---------- card renderers ----------
def light_card(d, box, card, radius=10):
    x0, y0, x1, y1 = box
    code, title, desc, fmt, status = card
    shadow(d, box, radius=radius, spread=5, color=(216, 221, 227))
    d.rounded_rectangle(box, radius=radius, fill=WHITE, outline=HAIR, width=2)
    d.text((x0 + 22, y0 + 18), code, font=f(FM, 13), fill=MUTE)
    if status:
        col = {"REQUIRED": GOOD, "UPDATED": (184, 132, 42), "NEW": REDLINE}[status]
        sw = 96 if status != "REQUIRED" else 104
        d.rounded_rectangle([x1 - sw - 18, y0 + 14, x1 - 18, y0 + 40], radius=4, outline=col, width=2)
        d.text((x1 - sw - 8, y0 + 20), status, font=f(FM, 12), fill=col)
    ty = y0 + 50
    for line in wrap(title, 20):
        d.text((x0 + 22, ty), line, font=f(FB, 25), fill=NAVY); ty += 30
    ty += 12
    for line in wrap(desc, 38):
        d.text((x0 + 22, ty), line, font=f(FR, 16), fill=CHAR); ty += 22
    d.line([x0 + 22, y1 - 46, x1 - 22, y1 - 46], fill=HAIR, width=2)
    d.text((x0 + 22, y1 - 34), fmt, font=f(FM, 13), fill=MUTE)
    d.text((x1 - 92, y1 - 34), "Open ↗", font=f(FMD, 13), fill=NAVY)


def dark_card(d, box, card, panel=(14, 48, 92), border=(44, 84, 132),
              title_col=(240, 246, 250), body_col=(168, 190, 212), radius=10):
    x0, y0, x1, y1 = box
    code, title, desc, fmt, status = card
    d.rounded_rectangle(box, radius=radius, fill=panel, outline=border, width=2)
    d.text((x0 + 22, y0 + 18), code, font=f(FM, 13), fill=body_col)
    if status:
        col = {"REQUIRED": (127, 203, 164), "UPDATED": (224, 174, 85), "NEW": (240, 121, 95)}[status]
        sw = 96 if status != "REQUIRED" else 104
        d.rounded_rectangle([x1 - sw - 18, y0 + 14, x1 - 18, y0 + 40], radius=4, outline=col, width=2)
        d.text((x1 - sw - 8, y0 + 20), status, font=f(FM, 12), fill=col)
    ty = y0 + 50
    for line in wrap(title, 20):
        d.text((x0 + 22, ty), line, font=f(FB, 25), fill=title_col); ty += 30
    ty += 12
    for line in wrap(desc, 38):
        d.text((x0 + 22, ty), line, font=f(FR, 16), fill=body_col); ty += 22
    d.line([x0 + 22, y1 - 46, x1 - 22, y1 - 46], fill=border, width=2)
    d.text((x0 + 22, y1 - 34), fmt, font=f(FM, 13), fill=body_col)
    d.text((x1 - 92, y1 - 34), "Open ↗", font=f(FMD, 13), fill=(150, 190, 235))


def wrap(text, n):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        if len(cur) + len(w_) + 1 <= n:
            cur = (cur + " " + w_).strip()
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines


def grid(d, x0, y0, x1, y1, cols, rows, renderer, gapx=32, gapy=30):
    cw = (x1 - x0 - gapx * (cols - 1)) / cols
    chh = (y1 - y0 - gapy * (rows - 1)) / rows
    for i, card in enumerate(CARDS[:cols * rows]):
        c, r = i % cols, i // cols
        bx0 = x0 + c * (cw + gapx); by0 = y0 + r * (chh + gapy)
        renderer(d, (bx0, by0, bx0 + cw, by0 + chh), card)


# =====================================================================
# LAYOUT 01 — SIDEBAR BLEED : navy rail dissolving right into the page
# =====================================================================
def layout_01():
    im = lin_grad((W, H), NAVY, PAPER, horizontal=True, power=0.55)
    d = ImageDraw.Draw(im)
    RAIL = 330
    d.rectangle([0, 0, RAIL, H], fill=NAVY)
    d.text((36, 46), "EIGELBERGER", font=f(FB, 28), fill=(255, 255, 255))
    d.text((36, 82), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.line([36, 126, RAIL - 36, 126], fill=(38, 74, 122), width=2)
    ny = 168
    for i, it in enumerate(NAV):
        if i == ACTIVE:
            d.rounded_rectangle([18, ny - 10, RAIL - 18, ny + 40], radius=8, fill=(20, 60, 112))
            d.rectangle([18, ny - 10, 24, ny + 40], fill=(255, 255, 255))
        d.text((44, ny), it, font=f(FB if i == ACTIVE else FR, 20),
               fill=(255, 255, 255) if i == ACTIVE else ICE)
        ny += 62
    d.rounded_rectangle([RAIL + 70, 44, RAIL + 700, 100], radius=28, fill=(255, 255, 255), outline=HAIR, width=2)
    d.text((RAIL + 100, 62), "Search standards, templates, forms, SOPs…", font=f(FM, 17), fill=MUTE)
    d.text((RAIL + 70, 150), TITLE, font=f(FB, 54), fill=NAVY)
    d.text((RAIL + 74, 218), SUB, font=f(FR, 20), fill=CHAR)
    grid(d, RAIL + 70, 290, W - 60, H - 60, 3, 2, light_card)
    return im


# =====================================================================
# LAYOUT 02 — HERO HEADER : full navy band up top, horizontal nav
# =====================================================================
def layout_02():
    im = Image.new("RGB", (W, H), PAPER)
    band = radial_glow((W, 330), NAVY, NAVY_MID, W * 0.16, 330 * 0.2, W * 0.55, strength=0.75)
    im.paste(band, (0, 0))
    d = ImageDraw.Draw(im)
    d.text((60, 40), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((60, 74), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.rounded_rectangle([W - 700, 36, W - 60, 92], radius=28, fill=(14, 52, 100), outline=(46, 88, 140), width=2)
    d.text((W - 668, 54), "Search the office hub…", font=f(FM, 17), fill=ICE)
    d.text((60, 136), TITLE, font=f(FB, 56), fill=(255, 255, 255))
    d.text((64, 206), SUB, font=f(FR, 20), fill=ICE)
    x = 60
    for i, it in enumerate(NAV[:7]):
        tw = int(d.textlength(it, font=f(FB, 18))) + 44
        if i == ACTIVE:
            d.rounded_rectangle([x, 268, x + tw, 316], radius=24, fill=(255, 255, 255))
        d.text((x + 22, 281), it, font=f(FB, 18), fill=NAVY if i == ACTIVE else ICE)
        x += tw + 14
    grid(d, 60, 380, W - 60, H - 60, 3, 2, light_card)
    return im


# =====================================================================
# LAYOUT 03 — FLOATING SHEET : content as a white sheet on navy
# =====================================================================
def layout_03():
    im = radial_glow((W, H), NAVY_DEEP, NAVY_MID, W * 0.12, H * 0.9, W * 0.85, strength=0.85)
    d = ImageDraw.Draw(im)
    d.text((54, 48), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((54, 82), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    ny = 168
    for i, it in enumerate(NAV):
        if i == ACTIVE:
            d.rectangle([40, ny - 8, 46, ny + 34], fill=(255, 255, 255))
        d.text((62, ny), it, font=f(FB if i == ACTIVE else FR, 19),
               fill=(255, 255, 255) if i == ACTIVE else (150, 176, 204))
        ny += 58
    SX, SY = 400, 108
    d.rounded_rectangle([SX + 6, SY + 10, W - 48, H - 40], radius=26, fill=(1, 16, 38))
    d.rounded_rectangle([SX, SY, W - 54, H - 48], radius=26, fill=WHITE)
    d.text((SX + 52, SY + 46), TITLE, font=f(FB, 50), fill=NAVY)
    d.text((SX + 55, SY + 112), SUB, font=f(FR, 19), fill=CHAR)
    d.line([SX + 52, SY + 158, W - 106, SY + 158], fill=HAIR, width=2)
    grid(d, SX + 52, SY + 194, W - 106, H - 100, 3, 2, light_card, gapx=26, gapy=24)
    return im


# =====================================================================
# LAYOUT 04 — DIAGONAL SPLIT : navy wedge across the upper left
# =====================================================================
def layout_04():
    im = Image.new("RGB", (W, H), PAPER)
    wedge = radial_glow((W, H), NAVY, NAVY_MID, W * 0.1, H * 0.1, W * 0.8, strength=0.7)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (W, 0), (W, 250), (0, 620)], fill=255)
    im.paste(wedge, (0, 0), mask)
    d = ImageDraw.Draw(im)
    d.text((60, 44), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((60, 78), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    ny = 150
    for i, it in enumerate(NAV[:6]):
        if i == ACTIVE:
            d.rectangle([46, ny - 6, 52, ny + 32], fill=(255, 255, 255))
        d.text((66, ny), it, font=f(FB if i == ACTIVE else FR, 19),
               fill=(255, 255, 255) if i == ACTIVE else ICE)
        ny += 52
    d.text((560, 120), TITLE, font=f(FB, 58), fill=(255, 255, 255))
    d.text((564, 196), SUB, font=f(FR, 20), fill=ICE)
    grid(d, 60, 470, W - 60, H - 60, 3, 2, light_card)
    return im


# =====================================================================
# LAYOUT 05 — DARK MODE : whole page navy, panels instead of cards
# =====================================================================
def layout_05():
    im = radial_glow((W, H), NAVY_DEEP, (10, 44, 88), W * 0.85, H * 0.12, W * 0.9, strength=0.8)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 128], fill=(3, 24, 54))
    d.line([0, 128, W, 128], fill=(34, 70, 116), width=2)
    d.text((48, 34), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((48, 68), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.rounded_rectangle([560, 34, 1330, 92], radius=10, fill=(9, 38, 76), outline=(40, 78, 124), width=2)
    d.text((588, 52), "Search standards, templates, forms, SOPs…", font=f(FM, 17), fill=(140, 168, 196))
    RAIL = 330
    d.rectangle([0, 128, RAIL, H], fill=(3, 24, 54))
    d.line([RAIL, 128, RAIL, H], fill=(34, 70, 116), width=2)
    ny = 178
    for i, it in enumerate(NAV):
        if i == ACTIVE:
            d.rectangle([0, ny - 10, RAIL, ny + 40], fill=(10, 44, 88))
            d.rectangle([0, ny - 10, 6, ny + 40], fill=(240, 121, 95))
        d.text((36, ny), it, font=f(FB if i == ACTIVE else FR, 19),
               fill=(255, 255, 255) if i == ACTIVE else (150, 176, 204))
        ny += 60
    d.text((RAIL + 60, 168), TITLE, font=f(FB, 52), fill=(255, 255, 255))
    d.text((RAIL + 63, 236), SUB, font=f(FR, 19), fill=(160, 186, 212))
    d.line([RAIL + 60, 286, W - 60, 286], fill=(40, 78, 124), width=2)
    grid(d, RAIL + 60, 322, W - 60, H - 60, 3, 2, dark_card)
    return im


# =====================================================================
# LAYOUT 06 — EDITORIAL SPLIT : navy left third holds nav + title
# =====================================================================
def layout_06():
    im = Image.new("RGB", (W, H), PAPER)
    col = lin_grad((720, H), NAVY, NAVY_MID, horizontal=False, power=1.4)
    im.paste(col, (0, 0))
    d = ImageDraw.Draw(im)
    d.text((60, 52), "EIGELBERGER", font=f(FB, 28), fill=(255, 255, 255))
    d.text((60, 90), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.text((60, 200), "Office", font=f(FB, 72), fill=(255, 255, 255))
    d.text((60, 276), "Standards", font=f(FB, 72), fill=(255, 255, 255))
    ty = 386
    for line in wrap(SUB, 34):
        d.text((62, ty), line, font=f(FR, 20), fill=ICE); ty += 30
    d.line([62, ty + 26, 620, ty + 26], fill=(48, 88, 138), width=2)
    ny = ty + 64
    for i, it in enumerate(NAV[:7]):
        if i == ACTIVE:
            d.rectangle([60, ny - 4, 66, ny + 30], fill=(240, 121, 95))
        d.text((82, ny), it, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else (168, 192, 216))
        ny += 46
    d.rounded_rectangle([780, 52, W - 60, 108], radius=28, fill=WHITE, outline=HAIR, width=2)
    d.text((812, 70), "Search the office hub…", font=f(FM, 17), fill=MUTE)
    grid(d, 780, 158, W - 60, H - 60, 2, 3, light_card, gapx=30, gapy=26)
    return im


# =====================================================================
# LAYOUT 07 — BLUEPRINT NEGATIVE : white linework on deep navy
# =====================================================================
def layout_07():
    im = radial_glow((W, H), NAVY_DEEP, (8, 42, 84), W * 0.25, H * 0.85, W * 0.95, strength=0.7)
    d = ImageDraw.Draw(im)
    for gx in range(0, W, 60):
        d.line([gx, 0, gx, H], fill=(20, 58, 104), width=1)
    for gy in range(0, H, 60):
        d.line([0, gy, W, gy], fill=(20, 58, 104), width=1)
    for gx in range(0, W, 300):
        d.line([gx, 0, gx, H], fill=(34, 78, 130), width=2)
    for gy in range(0, H, 300):
        d.line([0, gy, W, gy], fill=(34, 78, 130), width=2)
    d.text((54, 44), "EIGELBERGER", font=f(FB, 26), fill=(255, 255, 255))
    d.text((54, 78), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=ICE)
    d.line([54, 122, 330, 122], fill=(90, 140, 190), width=2)
    ny = 164
    for i, it in enumerate(NAV):
        if i == ACTIVE:
            d.rectangle([40, ny - 8, 44, ny + 34], fill=(255, 255, 255))
        d.text((62, ny), it, font=f(FB if i == ACTIVE else FR, 19),
               fill=(255, 255, 255) if i == ACTIVE else (146, 176, 208))
        ny += 58
    d.text((400, 130), TITLE.upper(), font=f(FB, 50), fill=(255, 255, 255))
    d.text((403, 198), SUB, font=f(FM, 17), fill=(160, 194, 226))
    d.line([400, 244, W - 60, 244], fill=(120, 168, 214), width=2)
    grid(d, 400, 286, W - 60, H - 60, 3, 2,
         lambda dd, box, card: dark_card(dd, box, card, panel=(6, 34, 70),
                                         border=(86, 138, 190), title_col=(255, 255, 255),
                                         body_col=(168, 200, 228), radius=4))
    return im


# =====================================================================
# LAYOUT 08 — GHOST MARK : airy page, oversized faint plan mark, navy foot
# =====================================================================
def layout_08():
    im = radial_glow((W, H), PAPER, (206, 216, 230), W * 0.92, H * 0.1, W * 0.75, strength=0.9)
    d = ImageDraw.Draw(im)
    ghost = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(ghost)
    for i, r in enumerate(range(180, 900, 90)):
        gd.ellipse([W - 320 - r, H - 210 - r, W - 320 + r, H - 210 + r],
                   outline=(2, 32, 73, 34), width=6)
    gd.line([W - 980, H - 40, W - 100, H - 900], fill=(2, 32, 73, 30), width=6)
    gd.line([W - 1180, H - 160, W - 60, H - 620], fill=(2, 32, 73, 24), width=6)
    ghost = ghost.filter(ImageFilter.GaussianBlur(1.2))
    im.paste(ghost, (0, 0), ghost)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 118], fill=WHITE)
    d.line([0, 118, W, 118], fill=NAVY, width=3)
    d.text((54, 30), "EIGELBERGER", font=f(FB, 26), fill=NAVY)
    d.text((54, 64), "ARCHITECTURE & DESIGN", font=f(FM, 12), fill=CHAR)
    d.rounded_rectangle([560, 28, 1330, 88], radius=30, fill=PAPER, outline=HAIR, width=2)
    d.text((592, 47), "Search standards, templates, forms, SOPs…", font=f(FM, 17), fill=MUTE)
    x = 54
    for i, it in enumerate(NAV[:7]):
        tw = int(d.textlength(it, font=f(FB, 18))) + 10
        d.text((x, 158), it, font=f(FB if i == ACTIVE else FR, 18), fill=NAVY if i == ACTIVE else CHAR)
        if i == ACTIVE:
            d.line([x, 190, x + tw - 10, 190], fill=REDLINE, width=4)
        x += tw + 36
    d.text((54, 236), TITLE, font=f(FB, 58), fill=NAVY)
    d.text((58, 312), SUB, font=f(FR, 20), fill=CHAR)
    grid(d, 54, 386, W - 54, H - 118, 3, 2, light_card)
    d.rectangle([0, H - 76, W, H], fill=NAVY)
    d.text((54, H - 52), "EIGELBERGER ARCHITECTURE & DESIGN   ·   OFFICE HUB", font=f(FM, 15), fill=ICE)
    return im


LAYOUTS = [
    ("01  SIDEBAR BLEED", layout_01),
    ("02  HERO HEADER", layout_02),
    ("03  FLOATING SHEET", layout_03),
    ("04  DIAGONAL SPLIT", layout_04),
    ("05  DARK MODE", layout_05),
    ("06  EDITORIAL SPLIT", layout_06),
    ("07  BLUEPRINT NEGATIVE", layout_07),
    ("08  GHOST MARK", layout_08),
]

if __name__ == "__main__":
    imgs = []
    for name, fn in LAYOUTS:
        im = fn()
        slug = name.split()[0]
        im.save("layout_%s.png" % slug)
        imgs.append((name, im))
        print("rendered", name)

    TW, TH = 940, 529
    PADX, PADY, LBL = 26, 60, 46
    sheet = Image.new("RGB", (PADX * 3 + TW * 2, PADY + (TH + LBL + PADY) * 4), (255, 255, 255))
    sd = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(imgs):
        col, row = i % 2, i // 2
        x = PADX + col * (TW + PADX)
        y = PADY + row * (TH + LBL + PADY)
        sd.text((x, y - 36), name, font=f(FB, 27), fill=NAVY)
        sheet.paste(im.resize((TW, TH), Image.LANCZOS), (x, y))
        sd.rectangle([x, y, x + TW, y + TH], outline=(178, 188, 198), width=2)
    sheet.save("layout_options.png")
    print("saved contact sheet", sheet.size)
