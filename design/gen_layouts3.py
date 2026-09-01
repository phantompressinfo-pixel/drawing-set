"""8 layouts (25-32) — light directory rail + navy field + CARDS.

Each one resolves the same problem differently: the side index and the icon row
must not repeat the same nine sections. Either the icons carry different
information, or they appear in only one place.
"""
from PIL import Image, ImageDraw
from gen_layouts import (
    FMD, W, H, NAVY, NAVY_DEEP, NAVY_MID, CHAR, PAPER, WHITE, HAIR, MUTE, ICE,
    REDLINE, GOOD, FB, FR, FM, f, NAV, ACTIVE, wrap, radial_glow, lin_grad,
)
from gen_layouts2 import NAV_ICON, TILE, put

RAIL = 344
CX0, CX1 = RAIL + 58, W - 58
ICE_DIM = (168, 192, 216)
PANEL = (11, 46, 92)
PANEL_EDGE = (48, 90, 140)

COUNTS = [None, 4, 6, 4, 6, 5, 6, 8, 3]

# section-level content (used where cards represent sections)
SECTIONS = [
    ("Office Standards", "standards", 6, "Drafting, CAD, file naming, deliverables"),
    ("Templates", "templates", 4, "Title blocks, minutes, transmittals, RFIs"),
    ("Forms", "forms", 6, "PTO, expenses, IT support, onboarding"),
    ("Office Policies", "policies", 5, "Handbook, safety, remote work, IT use"),
    ("SOPs", "sops", 6, "Kickoff, QA/QC, submittals, archiving"),
    ("Revit Standards", "revit", 8, "Worksharing, families, views, LOD"),
]

# document-level content (used where cards represent documents)
DOCS = [
    ("Drafting & CAD Standards", "Line weights, layer naming, hatch patterns, and dimensioning.", "PDF", "ft-pdf", "REQUIRED"),
    ("File Naming Convention", "Naming structure for drawings, models, and project folders.", "PDF", "ft-pdf", "REQUIRED"),
    ("Sheet Numbering Standard", "Discipline prefixes and sequencing for document sets.", "PDF", "ft-pdf", None),
    ("Deliverable Standards", "Required drawing content at SD, DD, CD, and CA phases.", "Google Doc", "ft-doc", None),
    ("Plotting & Print Standards", "Pen tables, plot styles, and PDF export settings.", "PDF", "ft-pdf", "UPDATED"),
    ("Specification Format", "CSI MasterFormat divisions used in office specs.", "DOCX", "ft-doc", None),
]

ACTIONS = [("Request time off", "ft-form"), ("Report an IT issue", "tool"),
           ("Start a new project", "templates"), ("Submit an expense", "ft-sheet"),
           ("Sign up to present", "calendar")]

FILTERS = ["All", "PDF", "Google Docs", "Sheets", "Forms", "Revit files"]
SUBSECTIONS = ["CAD Standards", "Drafting", "File Naming", "Plotting", "Specifications"]


# ---------------------------------------------------------------- rails
def rail(im, d, icons=True, counts=False, compact=False):
    """Light left directory. `icons` False = text-only index."""
    d.rectangle([0, 0, RAIL, H], fill=WHITE)
    d.text((44, 48), "EIGELBERGER", font=f(FB, 25), fill=NAVY)
    d.text((44, 80), "OFFICE HUB", font=f(FM, 12), fill=CHAR)
    d.line([44, 128, RAIL - 44, 128], fill=HAIR, width=2)
    d.text((44, 154), "SECTIONS", font=f(FM, 12), fill=MUTE)
    ny, step = 192, 64 if not compact else 58
    for i, label in enumerate(NAV):
        if i == ACTIVE:
            d.rounded_rectangle([22, ny - 12, RAIL - 22, ny + 44], radius=10, fill=NAVY)
        tx = 44
        if icons:
            put(im, NAV_ICON[i], 44, ny + 1, 28, white=(i == ACTIVE))
            d = ImageDraw.Draw(im)
            tx = 92
        d.text((tx, ny + 6), label, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else CHAR)
        if counts and COUNTS[i]:
            cw = d.textlength(str(COUNTS[i]), font=f(FM, 14))
            d.text((RAIL - 44 - cw, ny + 10), str(COUNTS[i]), font=f(FM, 14),
                   fill=ICE if i == ACTIVE else MUTE)
        ny += step
    return d


def icon_rail(im, d):
    """Narrow icon-only rail — icons appear here and nowhere else."""
    d.rectangle([0, 0, 132, H], fill=WHITE)
    d.line([132, 0, 132, H], fill=HAIR, width=2)
    put(im, "home", 49, 44, 34)
    d = ImageDraw.Draw(im)
    iy = 150
    for i, nm in enumerate(NAV_ICON):
        if i == ACTIVE:
            d.rounded_rectangle([18, iy - 16, 114, iy + 48], radius=14, fill=NAVY)
        put(im, nm, 49, iy, 32, white=(i == ACTIVE))
        d = ImageDraw.Draw(im)
        iy += 92
    return d


# ---------------------------------------------------------------- cards
def doc_card(im, d, box, doc, show_icon=True):
    x0, y0, x1, y1 = box
    name, desc, fmt, ficon, status = doc
    d.rounded_rectangle(box, radius=12, fill=PANEL, outline=PANEL_EDGE, width=2)
    tx = x0 + 24
    if show_icon:
        d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 74, y0 + 74], radius=12, fill=(20, 66, 124))
        put(im, ficon, x0 + 35, y0 + 35, 26, white=True)
        d = ImageDraw.Draw(im)
    if status:
        col = {"REQUIRED": (127, 203, 164), "UPDATED": (224, 174, 85)}[status]
        sw = 104 if status == "REQUIRED" else 96
        d.rounded_rectangle([x1 - sw - 20, y0 + 22, x1 - 20, y0 + 48], radius=5, outline=col, width=2)
        d.text((x1 - sw - 10, y0 + 28), status, font=f(FM, 12), fill=col)
    ty = y0 + (94 if show_icon else 30)
    for line in wrap(name, 22):
        d.text((tx, ty), line, font=f(FB, 24), fill=(255, 255, 255)); ty += 30
    ty += 8
    for line in wrap(desc, 40):
        d.text((tx, ty), line, font=f(FR, 16), fill=ICE_DIM); ty += 22
    d.line([tx, y1 - 46, x1 - 24, y1 - 46], fill=PANEL_EDGE, width=2)
    d.text((tx, y1 - 34), fmt, font=f(FM, 13), fill=ICE_DIM)
    d.text((x1 - 96, y1 - 34), "Open ↗", font=f(FMD, 13), fill=(150, 190, 235))
    return d


def section_card(im, d, box, sec):
    x0, y0, x1, y1 = box
    name, ic, count, desc = sec
    d.rounded_rectangle(box, radius=14, fill=PANEL, outline=PANEL_EDGE, width=2)
    d.rounded_rectangle([x0 + 26, y0 + 26, x0 + 96, y0 + 96], radius=16, fill=(255, 255, 255))
    put(im, ic, x0 + 43, y0 + 43, 36)
    d = ImageDraw.Draw(im)
    d.text((x0 + 26, y0 + 122), name, font=f(FB, 27), fill=(255, 255, 255))
    ty = y0 + 164
    for line in wrap(desc, 32):
        d.text((x0 + 26, ty), line, font=f(FR, 16), fill=ICE_DIM); ty += 22
    d.line([x0 + 26, y1 - 48, x1 - 26, y1 - 48], fill=PANEL_EDGE, width=2)
    d.text((x0 + 26, y1 - 36), "%d documents" % count, font=f(FM, 13), fill=ICE_DIM)
    d.text((x1 - 96, y1 - 36), "Open ↗", font=f(FMD, 13), fill=(150, 190, 235))
    return d


def wide_card(im, d, box, doc):
    """Horizontal card: big icon block left, text right."""
    x0, y0, x1, y1 = box
    name, desc, fmt, ficon, status = doc
    d.rounded_rectangle(box, radius=12, fill=PANEL, outline=PANEL_EDGE, width=2)
    d.rounded_rectangle([x0, y0, x0 + 118, y1], radius=12, fill=(17, 60, 116))
    d.rectangle([x0 + 100, y0 + 2, x0 + 118, y1 - 2], fill=(17, 60, 116))
    put(im, ficon, x0 + 40, y0 + (y1 - y0) / 2 - 19, 38, white=True)
    d = ImageDraw.Draw(im)
    d.text((x0 + 148, y0 + 24), name, font=f(FB, 25), fill=(255, 255, 255))
    d.text((x0 + 148, y0 + 62), desc, font=f(FR, 16), fill=ICE_DIM)
    d.text((x0 + 148, y1 - 38), fmt, font=f(FM, 13), fill=ICE_DIM)
    if status:
        col = {"REQUIRED": (127, 203, 164), "UPDATED": (224, 174, 85)}[status]
        sw = 104 if status == "REQUIRED" else 96
        d.rounded_rectangle([x1 - sw - 130, y0 + 26, x1 - 130, y0 + 52], radius=5, outline=col, width=2)
        d.text((x1 - sw - 120, y0 + 32), status, font=f(FM, 12), fill=col)
    d.text((x1 - 100, y0 + (y1 - y0) / 2 - 10), "Open ↗", font=f(FMD, 14), fill=(150, 190, 235))
    return d


def field(kind="glow"):
    im = Image.new("RGB", (W, H), NAVY)
    if kind == "glow":
        im.paste(radial_glow((W - RAIL, H), NAVY, NAVY_MID, (W - RAIL) * 0.88, H * 0.06,
                             (W - RAIL) * 1.15, strength=0.8), (RAIL, 0))
    else:
        im.paste(lin_grad((W - RAIL, H), NAVY, NAVY_DEEP, horizontal=False, power=1.2), (RAIL, 0))
    return im


def heading(d, title, sub, y=52):
    d.text((CX0, y), title, font=f(FB, 46), fill=(255, 255, 255))
    d.text((CX0 + 3, y + 66), sub, font=f(FR, 19), fill=ICE)
    return y + 112


def card_grid(im, d, y0, y1, cols, rows, renderer, items, gapx=26, gapy=24):
    cw = (CX1 - CX0 - gapx * (cols - 1)) / cols
    ch = (y1 - y0 - gapy * (rows - 1)) / rows
    for i, item in enumerate(items[:cols * rows]):
        c, r = i % cols, i // cols
        x, y = CX0 + c * (cw + gapx), y0 + r * (ch + gapy)
        d = renderer(im, d, (x, y, x + cw, y + ch), item)
    return d


# ===================================================================
# 25 — TEXT INDEX, ICONS ON SECTION CARDS
# ===================================================================
def layout_25():
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=False, counts=True)
    y = heading(d, "Office Hub", "Everything the office needs, in one place.")
    d.text((CX0, y + 10), "BROWSE BY SECTION", font=f(FM, 13), fill=ICE_DIM)
    card_grid(im, d, y + 46, H - 58, 3, 2, section_card, SECTIONS)
    return im


# ===================================================================
# 26 — ICON INDEX + QUICK-ACTION ROW (tasks, not sections)
# ===================================================================
def layout_26():
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=True)
    y = heading(d, "Office Standards",
                "Drafting conventions, CAD standards, file naming, and deliverables.")
    d.text((CX0, y - 2), "QUICK ACTIONS", font=f(FM, 13), fill=ICE_DIM)
    x, ay = CX0, y + 32
    for label, ic in ACTIONS:
        tw = int(d.textlength(label, font=f(FB, 16))) + 96
        d.rounded_rectangle([x, ay, x + tw, ay + 62], radius=31, fill=(255, 255, 255))
        put(im, ic, x + 24, ay + 16, 30)
        d = ImageDraw.Draw(im)
        d.text((x + 68, ay + 20), label, font=f(FB, 16), fill=NAVY)
        x += tw + 16
    card_grid(im, d, ay + 96, H - 58, 3, 2, lambda i, dd, b, doc: doc_card(i, dd, b, doc, show_icon=False), DOCS)
    return im


# ===================================================================
# 27 — ICON INDEX + FILE-TYPE FILTERS (different axis entirely)
# ===================================================================
def layout_27():
    im = field("linear")
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=True)
    y = heading(d, "Office Standards",
                "Drafting conventions, CAD standards, file naming, and deliverables.")
    d.text((CX0, y - 2), "FILTER BY FILE TYPE", font=f(FM, 13), fill=ICE_DIM)
    x, fy = CX0, y + 30
    for i, label in enumerate(FILTERS):
        tw = int(d.textlength(label, font=f(FB, 16))) + 46
        active = i == 0
        d.rounded_rectangle([x, fy, x + tw, fy + 52], radius=26,
                            fill=(255, 255, 255) if active else None,
                            outline=None if active else (66, 108, 160), width=2)
        lw = d.textlength(label, font=f(FB, 16))
        d.text((x + tw / 2 - lw / 2, fy + 16), label, font=f(FB, 16), fill=NAVY if active else ICE)
        x += tw + 14
    card_grid(im, d, fy + 84, H - 58, 3, 2, doc_card, DOCS)
    return im


# ===================================================================
# 28 — TEXT INDEX + PINNED ROW, THEN THE REST
# ===================================================================
def layout_28():
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=False, counts=True)
    y = heading(d, "Office Standards",
                "Drafting conventions, CAD standards, file naming, and deliverables.")
    put(im, "pinned", CX0, y - 6, 22, white=True)
    d = ImageDraw.Draw(im)
    d.text((CX0 + 34, y - 2), "PINNED BY THE OFFICE", font=f(FM, 13), fill=ICE_DIM)
    ph = 262
    cw = (CX1 - CX0 - 26 * 2) / 3
    for i, doc in enumerate(DOCS[:3]):
        x = CX0 + i * (cw + 26)
        d = doc_card(im, d, (x, y + 34, x + cw, y + 34 + ph), doc)
    ry = y + 34 + ph + 40
    d.text((CX0, ry), "EVERYTHING ELSE IN THIS SECTION", font=f(FM, 13), fill=ICE_DIM)
    ch = 236
    cw2 = (CX1 - CX0 - 26 * 2) / 3
    for i, doc in enumerate(DOCS[3:6]):
        x = CX0 + i * (cw2 + 26)
        d = doc_card(im, d, (x, ry + 34, x + cw2, ry + 34 + ch), doc, show_icon=False)
    return im


# ===================================================================
# 29 — ICON-ONLY RAIL, BIG CARDS (icons live in one place only)
# ===================================================================
def layout_29():
    im = Image.new("RGB", (W, H), NAVY)
    im.paste(radial_glow((W - 132, H), NAVY, NAVY_MID, (W - 132) * 0.9, H * 0.08,
                         (W - 132) * 1.1, strength=0.8), (132, 0))
    d = ImageDraw.Draw(im)
    d = icon_rail(im, d)
    gx0, gx1 = 132 + 58, W - 58
    d.text((gx0, 52), "Office Standards", font=f(FB, 46), fill=(255, 255, 255))
    d.text((gx0 + 3, 118), "Drafting conventions, CAD standards, file naming, and deliverables.",
           font=f(FR, 19), fill=ICE)
    cols, rows, gapx, gapy = 3, 2, 28, 26
    cw = (gx1 - gx0 - gapx * (cols - 1)) / cols
    ch = (H - 58 - 200 - gapy * (rows - 1)) / rows
    for i, doc in enumerate(DOCS):
        c, r = i % cols, i // cols
        x, y = gx0 + c * (cw + gapx), 200 + r * (ch + gapy)
        d = doc_card(im, d, (x, y, x + cw, y + ch), doc, show_icon=False)
    return im


# ===================================================================
# 30 — INDEX WITH COUNTS + ICON-LED WIDE CARDS
# ===================================================================
def layout_30():
    im = field("linear")
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=False, counts=True)
    y = heading(d, "Office Standards",
                "Drafting conventions, CAD standards, file naming, and deliverables.")
    ch, gap = 132, 22
    for i, doc in enumerate(DOCS[:5]):
        yy = y + 16 + i * (ch + gap)
        d = wide_card(im, d, (CX0, yy, CX1, yy + ch), doc)
    return im


# ===================================================================
# 31 — ICON INDEX + SUBSECTION TABS (a level down, not a repeat)
# ===================================================================
def layout_31():
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=True)
    y = heading(d, "Office Standards",
                "Drafting conventions, CAD standards, file naming, and deliverables.")
    x, ty = CX0, y
    for i, label in enumerate(SUBSECTIONS):
        tw = int(d.textlength(label, font=f(FB, 17))) + 20
        d.text((x, ty), label, font=f(FB if i == 0 else FR, 17),
               fill=(255, 255, 255) if i == 0 else ICE_DIM)
        if i == 0:
            d.line([x, ty + 32, x + tw - 20, ty + 32], fill=(255, 255, 255), width=4)
        x += tw + 30
    d.line([CX0, ty + 34, CX1, ty + 34], fill=(46, 86, 136), width=2)
    card_grid(im, d, ty + 74, H - 58, 3, 2, doc_card, DOCS)
    return im


# ===================================================================
# 32 — TEXT INDEX + STATUS COLUMNS (organised by state, not section)
# ===================================================================
def layout_32():
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, icons=False, counts=True)
    y = heading(d, "Office Hub", "What needs your attention, and what changed lately.")
    colw = (CX1 - CX0 - 40) / 2
    heads = [("REQUIRED READING", "pinned", CX0), ("RECENTLY UPDATED", "recent", CX0 + colw + 40)]
    for label, ic, x in heads:
        put(im, ic, x, y - 6, 22, white=True)
        d = ImageDraw.Draw(im)
        d.text((x + 34, y - 2), label, font=f(FM, 13), fill=ICE_DIM)
    ch, gap = 250, 22
    for i, doc in enumerate(DOCS[:3]):
        yy = y + 34 + i * (ch + gap)
        d = doc_card(im, d, (CX0, yy, CX0 + colw, yy + ch), doc, show_icon=False)
    for i, doc in enumerate(DOCS[3:6]):
        yy = y + 34 + i * (ch + gap)
        d = doc_card(im, d, (CX0 + colw + 40, yy, CX1, yy + ch), doc, show_icon=False)
    return im


LAYOUTS3 = [
    ("25  TEXT INDEX · ICON SECTION CARDS", layout_25),
    ("26  ICON INDEX · QUICK ACTIONS", layout_26),
    ("27  ICON INDEX · FILE-TYPE FILTERS", layout_27),
    ("28  TEXT INDEX · PINNED + REST", layout_28),
    ("29  ICON-ONLY RAIL · BIG CARDS", layout_29),
    ("30  COUNT INDEX · ICON-LED CARDS", layout_30),
    ("31  ICON INDEX · SUBSECTION TABS", layout_31),
    ("32  TEXT INDEX · STATUS COLUMNS", layout_32),
]

if __name__ == "__main__":
    rendered = []
    for name, fn in LAYOUTS3:
        im = fn()
        im.save("layout_%s.png" % name.split()[0])
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
        sd.text((x, y - 38), name, font=f(FB, 24), fill=NAVY)
        sheet.paste(im.resize((TW, TH), Image.LANCZOS), (x, y))
        sd.rectangle([x, y, x + TW, y + TH], outline=(178, 188, 198), width=2)
    sheet.save("layout_options_4.png")
    print("saved sheet")
