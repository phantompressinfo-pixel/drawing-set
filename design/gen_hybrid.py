"""Hybrid of 22 (light directory rail + navy field) and 24 (search-led content). 3 variations."""
import os
from PIL import Image, ImageDraw
from gen_layouts import (
    FMD, W, H, NAVY, NAVY_DEEP, NAVY_MID, CHAR, PAPER, WHITE, HAIR, MUTE, ICE,
    REDLINE, FB, FR, FM, f, NAV, ACTIVE, wrap, radial_glow, lin_grad,
)
from gen_layouts2 import NAV_ICON, TILE, put, icon

RAIL = 372                      # left directory rail width
CX0, CX1 = RAIL + 62, W - 62    # content column: hard left/right bounds
ICE_DIM = (168, 192, 216)

RECENT = [
    ("Drafting & CAD Standards", "Office Standards", "PDF", "01 JUN 2026"),
    ("Model Setup & Worksharing", "Revit Standards", "PDF", "20 MAY 2026"),
    ("PTO / Time-Off Request", "Forms", "Google Form", "05 JAN 2026"),
    ("Project Kickoff SOP", "SOPs", "Google Doc", "14 FEB 2026"),
    ("Employee Handbook", "Office Policies", "PDF", "15 JAN 2026"),
]


def directory_rail(im, d, subtitle="OFFICE HUB"):
    """Light left rail: logo block, then the section directory with icons."""
    d.rectangle([0, 0, RAIL, H], fill=WHITE)
    put(im, "home", 46, 52, 34)
    d = ImageDraw.Draw(im)
    d.text((100, 48), "EIGELBERGER", font=f(FB, 25), fill=NAVY)
    d.text((100, 80), subtitle, font=f(FM, 12), fill=CHAR)
    d.line([46, 132, RAIL - 46, 132], fill=HAIR, width=2)
    d.text((46, 158), "SECTIONS", font=f(FM, 12), fill=MUTE)
    ny = 196
    for i, (label, ic) in enumerate(zip(NAV, NAV_ICON)):
        if i == ACTIVE:
            d.rounded_rectangle([24, ny - 12, RAIL - 24, ny + 46], radius=10, fill=NAVY)
        put(im, ic, 46, ny + 1, 30, white=(i == ACTIVE))
        d = ImageDraw.Draw(im)
        d.text((96, ny + 7), label, font=f(FB if i == ACTIVE else FR, 18),
               fill=(255, 255, 255) if i == ACTIVE else CHAR)
        ny += 66
    d.line([46, H - 116, RAIL - 46, H - 116], fill=HAIR, width=2)
    d.text((46, H - 92), "Need something added?", font=f(FR, 16), fill=CHAR)
    d.text((46, H - 66), "Ask the office manager", font=f(FB, 16), fill=NAVY)
    return d


def search_bar(im, d, y, height=92, label="Search standards, templates, forms, SOPs, Revit standards…",
               on_navy=True):
    d.rounded_rectangle([CX0, y, CX1, y + height], radius=height // 2,
                        fill=WHITE if on_navy else (238, 241, 245),
                        outline=None if on_navy else HAIR, width=2)
    d.ellipse([CX0 + 30, y + height // 2 - 13, CX0 + 56, y + height // 2 + 13], outline=MUTE, width=3)
    d.line([CX0 + 54, y + height // 2 + 11, CX0 + 66, y + height // 2 + 23], fill=MUTE, width=3)
    d.text((CX0 + 84, y + height // 2 - 13), label, font=f(FM, 19), fill=MUTE)
    bw = 168
    d.rounded_rectangle([CX1 - bw - 14, y + 14, CX1 - 14, y + height - 14], radius=(height - 28) // 2, fill=NAVY)
    tw = d.textlength("SEARCH", font=f(FB, 17))
    d.text((CX1 - 14 - bw / 2 - tw / 2, y + height // 2 - 10), "SEARCH", font=f(FB, 17), fill=(255, 255, 255))
    return y + height


def shortcut_tiles(im, d, y, on_navy=True, tile_h=132):
    n = len(TILE)
    gap = 20
    tw = (CX1 - CX0 - gap * (n - 1)) / n
    for i, (label, ic) in enumerate(TILE):
        x = CX0 + i * (tw + gap)
        active = i == 0
        d.rounded_rectangle([x, y, x + tw, y + tile_h], radius=14,
                            fill=WHITE if (active or not on_navy) else (13, 50, 98),
                            outline=None if active else ((58, 100, 152) if on_navy else HAIR), width=2)
        cx = x + tw / 2
        put(im, ic, cx - 19, y + 26, 38, white=(on_navy and not active))
        d = ImageDraw.Draw(im)
        lw = d.textlength(label.upper(), font=f(FB, 14))
        d.text((cx - lw / 2, y + 82), label.upper(), font=f(FB, 14),
               fill=NAVY if (active or not on_navy) else ICE)
    return y + tile_h


def recent_rows(im, d, y, rows=4, on_navy=True, row_h=84, x0=None, x1=None):
    x0 = CX0 if x0 is None else x0
    x1 = CX1 if x1 is None else x1
    span = x1 - x0
    line_col = (46, 86, 136) if on_navy else (222, 228, 236)
    title_col = (255, 255, 255) if on_navy else NAVY
    meta_col = ICE_DIM if on_navy else CHAR
    d.line([x0, y, x1, y], fill=line_col, width=2)
    yy = y
    for name, section, fmt, date in RECENT[:rows]:
        yy += row_h
        ty = yy - row_h
        d.text((x0, ty + 26), name, font=f(FB, 23), fill=title_col)
        d.text((x0 + span * 0.44, ty + 31), section, font=f(FR, 17), fill=meta_col)
        d.text((x0 + span * 0.67, ty + 31), fmt, font=f(FM, 15), fill=meta_col)
        d.text((x0 + span * 0.82, ty + 31), date, font=f(FM, 15), fill=meta_col)
        d.text((x1 - 74, ty + 27), "Open ↗", font=f(FMD, 15),
               fill=(150, 190, 235) if on_navy else NAVY)
        d.line([x0, yy, x1, yy], fill=line_col, width=2)
    return yy


# ===================================================================
# A — navy field, search hero, tiles, recent list straight on the navy
# ===================================================================
def hybrid_a():
    im = Image.new("RGB", (W, H), NAVY)
    field = radial_glow((W - RAIL, H), NAVY, NAVY_MID, (W - RAIL) * 0.85, H * 0.05, (W - RAIL) * 1.15, strength=0.8)
    im.paste(field, (RAIL, 0))
    d = ImageDraw.Draw(im)
    d = directory_rail(im, d)
    d.text((CX0, 56), "Office Hub", font=f(FB, 44), fill=(255, 255, 255))
    d.text((CX0 + 3, 116), "Everything the office needs, in one place.", font=f(FR, 20), fill=ICE)
    d.text((CX1 - 190, 68), "28 AUG 2026", font=f(FM, 15), fill=ICE_DIM)
    y = search_bar(im, d, 176)
    d.text((CX0, y + 44), "JUMP TO A SECTION", font=f(FM, 13), fill=ICE_DIM)
    y = shortcut_tiles(im, d, y + 76)
    d.text((CX0, y + 56), "RECENTLY UPDATED", font=f(FM, 13), fill=ICE_DIM)
    recent_rows(im, d, y + 92, rows=5)
    return im


# ===================================================================
# B — navy field with a white sheet holding the recently-updated list
# ===================================================================
def hybrid_b():
    im = Image.new("RGB", (W, H), NAVY)
    field = lin_grad((W - RAIL, H), NAVY, NAVY_DEEP, horizontal=False, power=1.2)
    im.paste(field, (RAIL, 0))
    d = ImageDraw.Draw(im)
    d = directory_rail(im, d)
    d.text((CX0, 54), "Office Standards", font=f(FB, 46), fill=(255, 255, 255))
    d.text((CX0 + 3, 118), "Drafting conventions, CAD standards, file naming, and deliverables.",
           font=f(FR, 19), fill=ICE)
    y = search_bar(im, d, 180, height=84)
    y = shortcut_tiles(im, d, y + 44, tile_h=122)
    sheet = (CX0 - 24, y + 48, CX1 + 24, H - 48)
    d.rounded_rectangle(sheet, radius=20, fill=WHITE)
    d.text((sheet[0] + 40, sheet[1] + 32), "RECENTLY UPDATED", font=f(FM, 13), fill=MUTE)
    recent_rows(im, d, sheet[1] + 68, rows=5, on_navy=False, row_h=78,
                x0=sheet[0] + 40, x1=sheet[2] - 40)
    return im


# ===================================================================
# C — softer field, centred search, circular shortcuts, list on navy
# ===================================================================
def hybrid_c():
    im = Image.new("RGB", (W, H), NAVY)
    field = radial_glow((W - RAIL, H), NAVY_DEEP, (14, 62, 122), (W - RAIL) * 0.45, H * -0.05,
                        (W - RAIL) * 1.1, strength=0.95)
    im.paste(field, (RAIL, 0))
    d = ImageDraw.Draw(im)
    d = directory_rail(im, d, subtitle="ARCHITECTURE & DESIGN")
    head = "What are you looking for?"
    tw = d.textlength(head, font=f(FB, 46))
    d.text((RAIL + (W - RAIL) / 2 - tw / 2, 92), head, font=f(FB, 46), fill=(255, 255, 255))
    y = search_bar(im, d, 178, height=96)
    n = len(TILE)
    dia, gap = 122, 46
    total = n * dia + (n - 1) * gap
    x = RAIL + (W - RAIL) / 2 - total / 2
    for i, (label, ic) in enumerate(TILE):
        active = i == 0
        cy = y + 78
        d.ellipse([x, cy, x + dia, cy + dia], fill=WHITE if active else (12, 48, 96),
                  outline=None if active else (62, 106, 158), width=2)
        put(im, ic, x + dia / 2 - 25, cy + 32, 50, white=not active)
        d = ImageDraw.Draw(im)
        lw = d.textlength(label.upper(), font=f(FB, 14))
        d.text((x + dia / 2 - lw / 2, cy + dia + 20), label.upper(), font=f(FB, 14),
               fill=(255, 255, 255) if active else ICE)
        x += dia + gap
    ry = y + 78 + dia + 74
    d.text((CX0, ry), "RECENTLY UPDATED", font=f(FM, 13), fill=ICE_DIM)
    recent_rows(im, d, ry + 36, rows=5, row_h=80)
    return im


VARIANTS = [("22+24  A — OPEN FIELD", hybrid_a),
            ("22+24  B — WHITE SHEET", hybrid_b),
            ("22+24  C — CENTRED SEARCH", hybrid_c)]

if __name__ == "__main__":
    rendered = []
    for name, fn in VARIANTS:
        im = fn()
        slug = name.split()[1].strip("—")
        im.save("hybrid_%s.png" % slug)
        rendered.append((name, im))
        print("rendered", name)

    TW, TH = 1420, 799
    PADX, PADY, LBL = 30, 62, 46
    sheet = Image.new("RGB", (PADX * 2 + TW, PADY + (TH + LBL + PADY) * 3), (255, 255, 255))
    sd = ImageDraw.Draw(sheet)
    for i, (name, im) in enumerate(rendered):
        y = PADY + i * (TH + LBL + PADY)
        sd.text((PADX, y - 38), name, font=f(FB, 28), fill=NAVY)
        sheet.paste(im.resize((TW, TH), Image.LANCZOS), (PADX, y))
        sd.rectangle([PADX, y, PADX + TW, y + TH], outline=(178, 188, 198), width=2)
    sheet.save("hybrid_options.png")
    print("saved sheet", sheet.size)
