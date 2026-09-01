"""33-40 — one layout (25/26 structure), eight surface treatments.

Fixed: light index rail, action bubbles at the top, compact card grid.
Varying: field background, card fill/edge/elevation/radius, type colour.
Restraint is the point — colour sets mood, type carries the information.
"""
from PIL import Image, ImageDraw, ImageFilter
from gen_layouts import (
    FMD, W, H, NAVY, NAVY_DEEP, NAVY_MID, CHAR, PAPER, WHITE, HAIR, MUTE, ICE,
    FB, FR, FM, f, NAV, ACTIVE, wrap, radial_glow, lin_grad,
)
from gen_layouts2 import NAV_ICON, put

RAIL = 336
CX0, CX1 = RAIL + 56, W - 56
COUNTS = [None, 4, 6, 4, 6, 5, 6, 8, 3]

ACTIONS = [("Request time off", "ft-form"), ("Report an IT issue", "tool"),
           ("Start a new project", "templates"), ("Submit an expense", "ft-sheet"),
           ("Sign up to present", "calendar")]

DOCS = [
    ("Drafting & CAD Standards", "Line weights and layer naming", "PDF", "ft-pdf", "REQUIRED"),
    ("File Naming Convention", "Drawings, models, and folders", "PDF", "ft-pdf", "REQUIRED"),
    ("Sheet Numbering Standard", "Discipline prefixes and order", "PDF", "ft-pdf", None),
    ("Deliverable Standards", "Content at SD, DD, CD, and CA", "Google Doc", "ft-doc", None),
    ("Plotting & Print Standards", "Pen tables and export settings", "PDF", "ft-pdf", "UPDATED"),
    ("Specification Format", "CSI MasterFormat divisions", "DOCX", "ft-doc", None),
    ("Title Block Template", "North arrow, scale, revisions", "DWG", "ft-doc", None),
    ("Meeting Minutes Template", "OAC and design meeting format", "Google Doc", "ft-doc", None),
    ("Model Setup Protocol", "Central files and worksets", "PDF", "ft-pdf", "REQUIRED"),
    ("Family Naming Standard", "Library location and naming", "PDF", "ft-pdf", None),
    ("LOD Matrix", "Required detail by phase", "Google Sheet", "ft-sheet", "UPDATED"),
    ("Keynoting Standard", "Keynote file and numbering", "PDF", "ft-pdf", None),
]

GREEN, AMBER = (127, 203, 164), (224, 174, 85)
GREEN_D, AMBER_D = (46, 118, 84), (168, 118, 30)


class T:
    """Surface theme."""
    def __init__(self, name, field, card, title, sub, label, bubble_fill, bubble_text,
                 bubble_edge=None, rail_fill=WHITE, rail_text=CHAR, rail_head=NAVY,
                 rail_active=NAVY, rail_active_text=(255, 255, 255)):
        self.__dict__.update(locals()); del self.self


# ---------------------------------------------------------------- chrome
def rail(im, d, t):
    d.rectangle([0, 0, RAIL, H], fill=t.rail_fill)
    d.text((42, 46), "EIGELBERGER", font=f(FB, 24), fill=t.rail_head)
    d.text((42, 78), "OFFICE HUB", font=f(FM, 11), fill=t.rail_text)
    d.line([42, 124, RAIL - 42, 124], fill=HAIR if t.rail_fill == WHITE else (54, 92, 140), width=2)
    d.text((42, 148), "SECTIONS", font=f(FM, 11), fill=MUTE)
    ny = 184
    for i, label in enumerate(NAV):
        if i == ACTIVE:
            d.rounded_rectangle([20, ny - 11, RAIL - 20, ny + 41], radius=11, fill=t.rail_active)
        d.text((42, ny + 4), label, font=f(FB if i == ACTIVE else FR, 17),
               fill=t.rail_active_text if i == ACTIVE else t.rail_text)
        if COUNTS[i]:
            cw = d.textlength(str(COUNTS[i]), font=f(FM, 13))
            d.text((RAIL - 42 - cw, ny + 8), str(COUNTS[i]), font=f(FM, 13),
                   fill=ICE if i == ACTIVE else MUTE)
        ny += 62
    return d


def header(im, d, t):
    d.text((CX0, 50), "Office Standards", font=f(FB, 42), fill=t.title)
    d.text((CX0 + 2, 110), "Drafting conventions, CAD standards, file naming, and deliverables.",
           font=f(FR, 18), fill=t.sub)
    x, by = CX0, 168
    for label, ic in ACTIONS:
        tw = int(d.textlength(label, font=f(FB, 15))) + 88
        d.rounded_rectangle([x, by, x + tw, by + 56], radius=28, fill=t.bubble_fill,
                            outline=t.bubble_edge, width=2)
        put(im, ic, x + 22, by + 14, 28, white=(t.bubble_text != NAVY))
        d = ImageDraw.Draw(im)
        d.text((x + 62, by + 19), label, font=f(FB, 15), fill=t.bubble_text)
        x += tw + 14
    return d, by + 56


# ---------------------------------------------------------------- cards
def grid(im, d, t, y0):
    cols, rows, gap = 3, 2, 24
    cw = (CX1 - CX0 - gap * (cols - 1)) / cols
    ch = 224
    for i, doc in enumerate(DOCS[:cols * rows]):
        c, r = i % cols, i // cols
        x, y = CX0 + c * (cw + gap), y0 + r * (ch + gap)
        d = t.card(im, d, (x, y, x + cw, y + ch), doc, t)
    return d


def card_body(im, d, box, doc, t, fill, edge, radius, title_col, meta_col, icon_chip,
              icon_white, status_light=True, elevate=None):
    x0, y0, x1, y1 = box
    name, blurb, fmt, ficon, status = doc
    if elevate:
        d.rounded_rectangle([x0 + 3, y0 + 7, x1 + 3, y1 + 7], radius=radius, fill=elevate)
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=edge, width=2 if edge else 0)
    d.rounded_rectangle([x0 + 20, y0 + 20, x0 + 62, y0 + 62], radius=11, fill=icon_chip)
    put(im, ficon, x0 + 30, y0 + 30, 22, white=icon_white)
    d = ImageDraw.Draw(im)
    if status:
        col = (GREEN if status == "REQUIRED" else AMBER) if status_light else \
              (GREEN_D if status == "REQUIRED" else AMBER_D)
        d.ellipse([x1 - 34, y0 + 28, x1 - 20, y0 + 42], fill=col)
    ty = y0 + 78
    for line in wrap(name, 18):
        d.text((x0 + 20, ty), line, font=f(FB, 19), fill=title_col); ty += 25
    ty += 4
    for line in wrap(blurb, 26):
        d.text((x0 + 20, ty), line, font=f(FR, 14), fill=meta_col); ty += 19
    d.text((x0 + 20, y1 - 34), fmt, font=f(FM, 12), fill=meta_col)
    d.text((x1 - 78, y1 - 34), "Open ↗", font=f(FMD, 12), fill=meta_col)
    return d


def glass_card(im, d, box, doc, t):
    """Frosted panel: blur what's behind, lift it toward white, mask to a rounded rect."""
    x0, y0, x1, y1 = [int(v) for v in box]
    region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(18))
    region = Image.blend(region, Image.new("RGB", region.size, (255, 255, 255)), 0.20)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.size[0] - 1, region.size[1] - 1],
                                           radius=22, fill=255)
    im.paste(region, (x0, y0), mask)
    d = ImageDraw.Draw(im)
    return card_body(im, d, box, doc, t, None, (108, 148, 196), 22,
                     (255, 255, 255), (186, 206, 230), (44, 88, 142), True)


LAYOUTS = []


def make(name, field_fn, card_fn, **kw):
    t = T(name, field_fn, card_fn, **kw)

    def render():
        im = t.field()
        d = ImageDraw.Draw(im)
        d = rail(im, d, t)
        d, y = header(im, d, t)
        grid(im, d, t, y + 40)
        return im
    LAYOUTS.append((name, render))


# ---------------------------------------------------------------- fields
def navy_bloom():
    im = Image.new("RGB", (W, H), NAVY)
    im.paste(radial_glow((W - RAIL, H), NAVY, (26, 78, 140), (W - RAIL) * 0.85, H * 0.05,
                         (W - RAIL) * 1.2, strength=0.85), (RAIL, 0))
    return im


def navy_deep():
    im = Image.new("RGB", (W, H), NAVY_DEEP)
    im.paste(lin_grad((W - RAIL, H), (5, 30, 62), (1, 14, 34), horizontal=False, power=1.1), (RAIL, 0))
    return im


def soft_light():
    im = Image.new("RGB", (W, H), PAPER)
    im.paste(radial_glow((W - RAIL, H), (238, 241, 246), (208, 219, 234),
                         (W - RAIL) * 0.9, H * 0.9, (W - RAIL) * 1.1, strength=0.9), (RAIL, 0))
    return im


def duotone():
    im = Image.new("RGB", (W, H), NAVY)
    im.paste(lin_grad((W - RAIL, H), (6, 44, 92), (2, 24, 54), horizontal=False, power=1.3), (RAIL, 0))
    return im


def aurora():
    im = Image.new("RGB", (W, H), NAVY_DEEP)
    a = radial_glow((W - RAIL, H), NAVY_DEEP, (16, 74, 132), (W - RAIL) * 0.18, H * 0.12,
                    (W - RAIL) * 0.85, strength=0.95)
    b = radial_glow((W - RAIL, H), NAVY_DEEP, (12, 92, 116), (W - RAIL) * 0.92, H * 0.82,
                    (W - RAIL) * 0.9, strength=0.9)
    blend = Image.blend(a, b, 0.5).filter(ImageFilter.GaussianBlur(3))
    im.paste(blend, (RAIL, 0))
    return im


def mono():
    im = Image.new("RGB", (W, H), (14, 20, 30))
    im.paste(lin_grad((W - RAIL, H), (18, 25, 36), (10, 15, 24), horizontal=False), (RAIL, 0))
    return im


# ---------------------------------------------------------------- the eight
make("33  FROSTED GLASS", navy_bloom, glass_card,
     title=(255, 255, 255), sub=ICE, label=ICE,
     bubble_fill=(255, 255, 255), bubble_text=NAVY)

make("34  SOFT LIGHT", soft_light,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t, (255, 255, 255), None, 20,
                                        NAVY, MUTE, (233, 238, 245), False, False,
                                        elevate=(214, 221, 232)),
     title=NAVY, sub=CHAR, label=MUTE,
     bubble_fill=(255, 255, 255), bubble_text=NAVY, bubble_edge=HAIR)

make("35  ELEVATED NAVY", navy_bloom,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t, (12, 52, 102), None, 20,
                                        (255, 255, 255), (166, 192, 220), (24, 78, 142), True,
                                        elevate=(1, 18, 42)),
     title=(255, 255, 255), sub=ICE, label=ICE,
     bubble_fill=(255, 255, 255), bubble_text=NAVY)

make("36  DUOTONE DEPTH", duotone,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t, (16, 62, 116), (36, 92, 152), 18,
                                        (255, 255, 255), (172, 198, 224), (255, 255, 255), False),
     title=(255, 255, 255), sub=ICE, label=ICE,
     bubble_fill=None, bubble_text=(255, 255, 255), bubble_edge=(92, 136, 186))

make("37  PAPER ON NAVY", navy_deep,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t, (250, 250, 248), None, 16,
                                        NAVY, MUTE, NAVY, True, False, elevate=(0, 10, 26)),
     title=(255, 255, 255), sub=ICE, label=ICE,
     bubble_fill=None, bubble_text=(255, 255, 255), bubble_edge=(70, 110, 160))

make("38  MONOCHROME", mono,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t, (26, 34, 46), (48, 58, 72), 14,
                                        (244, 246, 249), (150, 162, 178), (40, 52, 68), True),
     title=(244, 246, 249), sub=(158, 170, 186), label=(158, 170, 186),
     bubble_fill=None, bubble_text=(230, 235, 242), bubble_edge=(74, 86, 102),
     rail_fill=(24, 30, 40), rail_text=(196, 204, 216), rail_head=(255, 255, 255),
     rail_active=(255, 255, 255), rail_active_text=(18, 24, 34))

make("39  TINTED CARDS", navy_bloom,
     lambda im, d, b, doc, t: card_body(im, d, b, doc, t,
                                        [(14, 58, 104), (12, 62, 96), (18, 56, 112),
                                         (10, 66, 104)][DOCS.index(doc) % 4],
                                        None, 20, (255, 255, 255), (170, 196, 222),
                                        (255, 255, 255), False, elevate=(1, 20, 46)),
     title=(255, 255, 255), sub=ICE, label=ICE,
     bubble_fill=(255, 255, 255), bubble_text=NAVY)

make("40  AURORA GLASS", aurora, glass_card,
     title=(255, 255, 255), sub=(198, 220, 236), label=(198, 220, 236),
     bubble_fill=(255, 255, 255), bubble_text=NAVY)


if __name__ == "__main__":
    rendered = []
    for name, fn in LAYOUTS:
        im = fn()
        im.save("surface_%s.png" % name.split()[0])
        rendered.append((name, im))
        print("rendered", name)

    TW, TH = 940, 529
    PADX, PADY, LBL = 26, 62, 48
    sheet = Image.new("RGB", (PADX * 3 + TW * 2, PADY + (TH + LBL + PADY) * 4), (255, 255, 255))
    sd = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(rendered):
        col, row = i % 2, i // 2
        x = PADX + col * (TW + PADX)
        y = PADY + row * (TH + LBL + PADY)
        sd.text((x, y - 38), name, font=f(FB, 26), fill=NAVY)
        sheet.paste(im.resize((TW, TH), Image.LANCZOS), (x, y))
        sd.rectangle([x, y, x + TW, y + TH], outline=(178, 188, 198), width=2)
    sheet.save("surface_options.png")
    print("saved sheet")
