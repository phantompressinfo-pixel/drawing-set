"""EAD Office Hub — every page in the chosen treatment (33, frosted glass)."""
import os
from PIL import Image, ImageDraw, ImageFilter
from gen_layouts import (
    FMD, W, H, NAVY, CHAR, WHITE, HAIR, MUTE, ICE, FB, FR, FM, f, wrap, radial_glow,
)
from gen_layouts2 import put

RAIL = 336
CX0, CX1 = RAIL + 56, W - 56
ICE_DIM = (186, 206, 230)
GREEN, AMBER = (127, 203, 164), (224, 174, 85)
GLASS_EDGE = (108, 148, 196)
CHIP = (44, 88, 142)

NAV = ["Home", "Announcements", "Office Standards", "Templates", "Forms",
       "Office Policies", "SOPs", "Revit Standards", "Learning Sessions", "Staff Directory"]
COUNTS = [None, 4, 6, 4, 6, 5, 6, 8, None, 3]

ACTIONS = [("Request time off", "ft-form"), ("Report an IT issue", "tool"),
           ("Start a new project", "templates"), ("Submit an expense", "ft-sheet"),
           ("Sign up to present", "calendar")]


# ------------------------------------------------------------------ chrome
def field():
    im = Image.new("RGB", (W, H), NAVY)
    im.paste(radial_glow((W - RAIL, H), NAVY, (26, 78, 140), (W - RAIL) * 0.85, H * 0.05,
                         (W - RAIL) * 1.2, strength=0.85), (RAIL, 0))
    return im


def rail(im, d, active):
    d.rectangle([0, 0, RAIL, H], fill=WHITE)
    d.text((42, 46), "EIGELBERGER", font=f(FB, 24), fill=NAVY)
    d.text((42, 78), "OFFICE HUB", font=f(FM, 11), fill=CHAR)
    d.line([42, 124, RAIL - 42, 124], fill=HAIR, width=2)
    d.text((42, 148), "SECTIONS", font=f(FM, 11), fill=MUTE)
    ny = 182
    for i, label in enumerate(NAV):
        if i == active:
            d.rounded_rectangle([20, ny - 10, RAIL - 20, ny + 38], radius=11, fill=NAVY)
        d.text((42, ny + 2), label, font=f(FB if i == active else FR, 16),
               fill=(255, 255, 255) if i == active else CHAR)
        if COUNTS[i]:
            cw = d.textlength(str(COUNTS[i]), font=f(FM, 13))
            d.text((RAIL - 42 - cw, ny + 5), str(COUNTS[i]), font=f(FM, 13),
                   fill=ICE if i == active else MUTE)
        ny += 58
    d.line([42, H - 112, RAIL - 42, H - 112], fill=HAIR, width=2)
    d.text((42, H - 88), "Need something added?", font=f(FR, 15), fill=CHAR)
    d.text((42, H - 64), "Ask the office manager", font=f(FB, 15), fill=NAVY)
    return d


def search_bar(im, d, y, height=66):
    d.rounded_rectangle([CX0, y, CX1, y + height], radius=height // 2, fill=(255, 255, 255))
    cy = y + height // 2
    d.ellipse([CX0 + 28, cy - 11, CX0 + 50, cy + 11], outline=MUTE, width=3)
    d.line([CX0 + 48, cy + 9, CX0 + 58, cy + 19], fill=MUTE, width=3)
    d.text((CX0 + 74, cy - 11), "Search standards, templates, forms, SOPs, Revit standards…",
           font=f(FM, 16), fill=MUTE)
    bw = 138
    d.rounded_rectangle([CX1 - bw - 11, y + 11, CX1 - 11, y + height - 11],
                        radius=(height - 22) // 2, fill=NAVY)
    tw = d.textlength("SEARCH", font=f(FB, 15))
    d.text((CX1 - 11 - bw / 2 - tw / 2, cy - 9), "SEARCH", font=f(FB, 15), fill=(255, 255, 255))
    return y + height


def bubbles(im, d, y):
    x = CX0
    for label, ic in ACTIONS:
        tw = int(d.textlength(label, font=f(FB, 15))) + 88
        d.rounded_rectangle([x, y, x + tw, y + 56], radius=28, fill=(255, 255, 255))
        put(im, ic, x + 22, y + 14, 28)
        d = ImageDraw.Draw(im)
        d.text((x + 62, y + 19), label, font=f(FB, 15), fill=NAVY)
        x += tw + 14
    return d, y + 56


def header(im, d, title, sub, show_actions=True):
    d.text((CX0, 46), title, font=f(FB, 42), fill=(255, 255, 255))
    d.text((CX0 + 2, 106), sub, font=f(FR, 18), fill=ICE)
    y = search_bar(im, d, 160)
    if show_actions:
        d, y = bubbles(im, d, y + 26)
    return d, y


# ------------------------------------------------------------------ glass
def glass(im, box, radius=22):
    x0, y0, x1, y1 = [int(v) for v in box]
    region = im.crop((x0, y0, x1, y1)).filter(ImageFilter.GaussianBlur(18))
    region = Image.blend(region, Image.new("RGB", region.size, (255, 255, 255)), 0.20)
    mask = Image.new("L", region.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, region.size[0] - 1, region.size[1] - 1],
                                           radius=radius, fill=255)
    im.paste(region, (x0, y0), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle(box, radius=radius, outline=GLASS_EDGE, width=2)
    return d


def doc_card(im, d, box, doc):
    x0, y0, x1, y1 = box
    name, blurb, fmt, ficon, status = doc
    d = glass(im, box)
    d.rounded_rectangle([x0 + 20, y0 + 20, x0 + 62, y0 + 62], radius=11, fill=CHIP)
    put(im, ficon, x0 + 30, y0 + 30, 22, white=True)
    d = ImageDraw.Draw(im)
    if status:
        d.ellipse([x1 - 34, y0 + 28, x1 - 20, y0 + 42], fill=GREEN if status == "REQUIRED" else AMBER)
    ty = y0 + 78
    for line in wrap(name, 18):
        d.text((x0 + 20, ty), line, font=f(FB, 19), fill=(255, 255, 255)); ty += 25
    ty += 4
    for line in wrap(blurb, 26):
        d.text((x0 + 20, ty), line, font=f(FR, 14), fill=ICE_DIM); ty += 19
    d.text((x0 + 20, y1 - 34), fmt, font=f(FM, 12), fill=ICE_DIM)
    d.text((x1 - 78, y1 - 34), "Open ↗", font=f(FMD, 12), fill=ICE_DIM)
    return d


def section_card(im, d, box, sec):
    x0, y0, x1, y1 = box
    name, ic, count, blurb = sec
    d = glass(im, box)
    d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 82, y0 + 82], radius=15, fill=(255, 255, 255))
    put(im, ic, x0 + 37, y0 + 37, 30)
    d = ImageDraw.Draw(im)
    d.text((x0 + 22, y0 + 100), name, font=f(FB, 23), fill=(255, 255, 255))
    ty = y0 + 136
    for line in wrap(blurb, 30):
        d.text((x0 + 22, ty), line, font=f(FR, 14), fill=ICE_DIM); ty += 19
    d.text((x0 + 22, y1 - 34), "%d documents" % count, font=f(FM, 12), fill=ICE_DIM)
    d.text((x1 - 78, y1 - 34), "Open ↗", font=f(FMD, 12), fill=ICE_DIM)
    return d


def notice_card(im, d, box, n):
    x0, y0, x1, y1 = box
    title, date, body, urgent = n
    d = glass(im, box, radius=18)
    d.rounded_rectangle([x0 + 22, y0 + 22, x0 + 64, y0 + 64], radius=11, fill=CHIP)
    put(im, "announcements", x0 + 32, y0 + 32, 22, white=True)
    d = ImageDraw.Draw(im)
    dw = d.textlength(date, font=f(FM, 13))
    d.text((x1 - 24 - dw, y0 + 32), date, font=f(FM, 13), fill=ICE_DIM)
    if urgent:
        d.ellipse([x1 - 40 - dw - 24, y0 + 34, x1 - 40 - dw - 10, y0 + 48], fill=AMBER)
    d.text((x0 + 84, y0 + 30), title, font=f(FB, 21), fill=(255, 255, 255))
    ty = y0 + 82
    for line in wrap(body, 84):
        d.text((x0 + 24, ty), line, font=f(FR, 15), fill=ICE_DIM); ty += 21
    return d


def session_card(im, d, box, s):
    x0, y0, x1, y1 = box
    date, presenter, topic = s
    d = glass(im, box, radius=18)
    d.text((x0 + 20, y0 + 20), date, font=f(FM, 13), fill=ICE_DIM)
    ty = y0 + 48
    for line in wrap(topic, 20):
        d.text((x0 + 20, ty), line, font=f(FB, 19), fill=(255, 255, 255)); ty += 25
    d.rounded_rectangle([x0 + 20, y1 - 46, x0 + 52, y1 - 14], radius=16, fill=CHIP)
    put(im, "learning", x0 + 28, y1 - 38, 16, white=True)
    d = ImageDraw.Draw(im)
    d.text((x0 + 62, y1 - 38), presenter, font=f(FR, 14), fill=ICE_DIM)
    return d


def grid(im, d, y0, items, renderer, cols=3, ch=224, gap=24):
    cw = (CX1 - CX0 - gap * (cols - 1)) / cols
    for i, item in enumerate(items):
        c, r = i % cols, i // cols
        x, y = CX0 + c * (cw + gap), y0 + r * (ch + gap)
        d = renderer(im, d, (x, y, x + cw, y + ch), item)
    return d


# ------------------------------------------------------------------ content
SECTIONS = [
    ("Office Standards", "standards", 6, "Drafting, CAD, file naming, deliverables"),
    ("Templates", "templates", 4, "Title blocks, minutes, transmittals, RFIs"),
    ("Forms", "forms", 6, "PTO, expenses, IT support, onboarding"),
    ("Office Policies", "policies", 5, "Handbook, safety, remote work, IT use"),
    ("SOPs", "sops", 6, "Kickoff, QA/QC, submittals, archiving"),
    ("Revit Standards", "revit", 8, "Worksharing, families, views, LOD"),
]

PAGES = [
    dict(i=0, title="Office Hub", sub="Everything the office needs, in one place.",
         kind="sections", items=SECTIONS),
    dict(i=1, title="Announcements", sub="Office notices, deadlines, closures, and maintenance windows.",
         kind="notices", items=[
             ("Revit 2027 rollout begins next month", "25 AUG 2026",
              "IT will begin migrating active projects starting mid-September. Watch for your migration window.", True),
             ("Office closed — Labor Day", "07 SEP 2026",
              "Closed Monday, September 7. Deadlines falling on this date shift to September 8.", False),
             ("New QA/QC checkpoint before CD issue", "18 AUG 2026",
              "See the QA/QC Review SOP for the updated milestone review requirement.", False),
             ("Server maintenance — Saturday, 6–10am", "28 AUG 2026",
              "File server and Revit central files will be unavailable during this window.", False)]),
    dict(i=2, title="Office Standards", sub="Drafting conventions, CAD standards, file naming, and deliverables.",
         kind="docs", items=[
             ("Drafting & CAD Standards", "Line weights and layer naming", "PDF", "ft-pdf", "REQUIRED"),
             ("File Naming Convention", "Drawings, models, and folders", "PDF", "ft-pdf", "REQUIRED"),
             ("Sheet Numbering Standard", "Discipline prefixes and order", "PDF", "ft-pdf", None),
             ("Deliverable Standards", "Content at SD, DD, CD, and CA", "Google Doc", "ft-doc", None),
             ("Plotting & Print Standards", "Pen tables and export settings", "PDF", "ft-pdf", "UPDATED"),
             ("Specification Format", "CSI MasterFormat divisions", "DOCX", "ft-doc", None)]),
    dict(i=3, title="Templates", sub="Ready-to-use templates for drawings, correspondence, and project documents.",
         kind="docs", items=[
             ("Sheet Title Block", "North arrow, scale, revisions", "DWG", "ft-doc", "REQUIRED"),
             ("Meeting Minutes", "OAC and design meeting format", "Google Doc", "ft-doc", None),
             ("Transmittal", "Cover sheet for issued documents", "DOCX", "ft-doc", None),
             ("RFI Template", "Numbering and response fields", "Google Sheet", "ft-sheet", None)]),
    dict(i=4, title="Forms", sub="Fillable forms for HR, IT, expenses, and project administration.",
         kind="docs", items=[
             ("PTO / Time-Off Request", "Vacation, sick, and personal", "Form", "ft-form", "REQUIRED"),
             ("Expense Reimbursement", "Receipts and mileage", "Form", "ft-form", None),
             ("IT Support Request", "Hardware, software, network", "Form", "ft-form", None),
             ("New-Hire Onboarding", "Accounts, licenses, workstation", "Google Doc", "ft-doc", None),
             ("Project Closeout", "Archive and record documents", "Google Sheet", "ft-sheet", "REQUIRED"),
             ("Timesheet Correction", "Fix a submitted week", "Form", "ft-form", None)]),
    dict(i=6, title="Standard Operating Procedures", sub="Step-by-step procedures for recurring project workflows.",
         kind="docs", items=[
             ("Project Kickoff", "Numbering, folders, team setup", "Google Doc", "ft-doc", "REQUIRED"),
             ("QA/QC Review", "Milestone checkpoints and sign-off", "PDF", "ft-pdf", "REQUIRED"),
             ("Submittal Review", "Log, route, and respond", "Google Doc", "ft-doc", None),
             ("Client Onboarding", "Contracts and kickoff scheduling", "Google Doc", "ft-doc", None),
             ("File Backup & Archiving", "Cadence and archive procedure", "PDF", "ft-pdf", None),
             ("Drawing Issue & Plotting", "Review, plot, log transmittals", "PDF", "ft-pdf", "UPDATED")]),
    dict(i=7, title="Revit Standards", sub="BIM execution standards for models, families, views, sheets, and plotting.",
         kind="docs", items=[
             ("Model Setup & Worksharing", "Central files and worksets", "PDF", "ft-pdf", "REQUIRED"),
             ("Family Library & Naming", "Approved library and convention", "PDF", "ft-pdf", None),
             ("View Templates & Graphics", "Overrides and view standards", "RVT", "ft-doc", None),
             ("Sheet & View Numbering", "Aligned to office numbering", "PDF", "ft-pdf", None),
             ("Level of Development Matrix", "Required detail by phase", "Google Sheet", "ft-sheet", "UPDATED"),
             ("Model Health & Audit", "Monthly purge and warnings review", "Google Sheet", "ft-sheet", None)]),
    dict(i=8, title="Learning Sessions", sub="Weekly knowledge share — one person presents something new, or something we need to work on.",
         kind="sessions", items=[
             ("2026-09-04", "Jane Doe", "Revit Keynoting Tips"),
             ("2026-09-11", "Open — sign up", "Topic to be confirmed"),
             ("2026-09-18", "Open — sign up", "Topic to be confirmed"),
             ("2026-08-28", "Marc Ellis", "Reading the 2026 Energy Code"),
             ("2026-08-21", "Priya Shah", "Lessons from the Harbor View CA phase"),
             ("2026-08-14", "Tom Reyes", "Faster sheet setup in Revit")]),
]


def render(p):
    im = field()
    d = ImageDraw.Draw(im)
    d = rail(im, d, p["i"])
    d, y = header(im, d, p["title"], p["sub"], show_actions=(p["kind"] != "notices"))
    y += 34
    if p["kind"] == "sections":
        grid(im, d, y, p["items"], section_card, cols=3, ch=246)
    elif p["kind"] == "docs":
        grid(im, d, y, p["items"], doc_card, cols=3, ch=224)
    elif p["kind"] == "sessions":
        grid(im, d, y, p["items"], session_card, cols=3, ch=180)
    elif p["kind"] == "notices":
        cw = CX1 - CX0
        for i, n in enumerate(p["items"]):
            yy = y + i * (146 + 20)
            d = notice_card(im, d, (CX0, yy, CX0 + cw, yy + 146), n)
    return im


if __name__ == "__main__":
    for n, p in enumerate(PAGES, 1):
        im = render(p)
        name = "page_%02d_%s.png" % (n, p["title"].split()[0].lower().strip(","))
        im.save(name)
        print("rendered", name)
