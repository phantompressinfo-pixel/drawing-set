# -*- coding: utf-8 -*-
"""detailkit - draw one office construction detail, with its notes.

The deliverable is the DETAIL ONLY: drawing, tags, leader notes and the office
title (bubble, underlined title, SCALE : 3" = 1'-0"). There is no sheet border or
title block, because the detail goes onto the office's own Revit sheet.

Geometry is entered in REAL INCHES (x to the right, y DOWN, any origin).
save() writes:

    <out>/<NN>-<SHEET>-<slug>.svg        the detail
    <out>/<NN>-<SHEET>-<slug>.png        a render of it (headless Chromium)
    <out>/<NN>-<SHEET>-<slug>.dxf        full-size (1" = 1") for a Revit drafting view
    <out>/<NN>-<SHEET>-<slug>.notes.txt  the notes, ready to paste
    <out>/<NN>-<SHEET>-<slug>.json       manifest the checker reads

Minimal use:

    from detailkit import Detail
    d = Detail(3, "A6.16", "TYP. FIXED WINDOW SILL @ STONE VENEER", scale="3")
    d.rect(0, 0, 4, 30, hatch="stone")
    d.tag("2/3/4/5A-X", at=(-8, 20), to=(2, 20))
    d.note("CUT STONE SILL", to=(2, -1))
    d.save("details", assemblies="assemblies.yaml")

See SKILL.md for the office rules the notes must follow.
"""
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

# ------------------------------------------------------------------ scales
# "3" means 3" = 1'-0".
PX = 96.0   # px per paper inch - text is fixed, the drawing scales
SCALES = {k: (lab, PX * float(k) / 12) for k, lab in {
    "12": '1\'-0" = 1\'-0"', "6": '6" = 1\'-0"', "3": '3" = 1\'-0"', "1.5": '1 1/2" = 1\'-0"',
    "1": '1" = 1\'-0"', "0.75": '3/4" = 1\'-0"', "0.5": '1/2" = 1\'-0"', "0.375": '3/8" = 1\'-0"',
    "0.25": '1/4" = 1\'-0"'}.items()}

HATCHES = ("none", "conc", "cmu", "earth", "gravel", "insul", "batt", "wood", "ply",
           "gyp", "stone", "steel", "air", "sand", "ice", "sprayfoam", "glass", "grout")

# DXF: hatch -> (pattern, scale factor per paper-inch of scale)
DXF_PATTERN = {"conc": ("AR-CONC", 0.6), "cmu": ("ANSI31", 4), "earth": ("EARTH", 0.8),
               "gravel": ("GRAVEL", 2), "insul": ("CROSS", 2), "wood": ("WOOD1", 1),
               "ply": ("ANSI31", 1.5), "gyp": ("DOTS", 2), "stone": ("ANSI33", 4),
               "steel": ("ANSI32", 1), "sand": ("AR-SAND", 0.6), "ice": ("ANSI37", 4),
               "sprayfoam": ("DOTS", 3), "grout": ("AR-SAND", 0.6), "glass": ("ANSI31", 6)}

BLUE = "#2340c8"   # self-adhered membranes / air-water barriers, as the office sets show them

STYLE = """
 text{font-family:Arial,Helvetica,sans-serif;fill:#000}
 .n{font-size:15px}
 .tag{font-size:15px}
 .tagb{font-size:17px;font-weight:bold}
 .kn{font-size:15px;font-weight:bold}
 .dimt{font-size:14px}
 .ttl{font-size:26px;letter-spacing:.5px}
 .sc{font-size:13px}
 .lead{fill:none;stroke:#000;stroke-width:1}
 .cut{fill:none;stroke:#000;stroke-width:2.6}
 .med{fill:none;stroke:#000;stroke-width:1.6}
 .thin{fill:none;stroke:#000;stroke-width:0.9}
 .hidden{fill:none;stroke:#000;stroke-width:1.1;stroke-dasharray:12 7}
 .center{fill:none;stroke:#000;stroke-width:0.9;stroke-dasharray:28 6 5 6}
 .metal{fill:none;stroke:#000;stroke-width:3.4;stroke-linejoin:miter}
 .membrane{fill:none;stroke:%s;stroke-width:3}
 .airbar{fill:none;stroke:%s;stroke-width:2.2;stroke-dasharray:16 5 3 5}
 .vapor{fill:none;stroke:#000;stroke-width:1.4;stroke-dasharray:4 4}
 .dim{fill:none;stroke:#000;stroke-width:0.9}
""" % (BLUE, BLUE)

DEFS = """
<marker id="arw" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="10" markerHeight="10" orient="auto-start-reverse">
 <path d="M0,1.5 L12,6 L0,10.5 z" fill="#000"/></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7">
 <circle cx="5" cy="5" r="4" fill="#000"/></marker>
<marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9" orient="auto">
 <path d="M1,9 L9,1" stroke="#000" stroke-width="2"/></marker>
<pattern id="conc" width="52" height="52" patternUnits="userSpaceOnUse">
 <circle cx="30" cy="12" r="1.6"/><circle cx="8" cy="36" r="1.4"/><circle cx="45" cy="6" r="1.3"/>
 <circle cx="22" cy="45" r="1.5"/><circle cx="44" cy="47" r="1.2"/><circle cx="14" cy="10" r="1"/>
 <circle cx="36" cy="30" r="1"/><path d="M26,25 l5,3 l-4,3 z M6,20 l4,-3 l1,5 z M40,38 l5,1 l-3,4 z"/></pattern>
<pattern id="grout" width="16" height="16" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="4" r="0.9"/><circle cx="11" cy="9" r="0.9"/><circle cx="6" cy="13" r="0.9"/><circle cx="13" cy="2" r="0.6"/></pattern>
<pattern id="cmu" width="18" height="18" patternUnits="userSpaceOnUse">
 <path d="M0,18 L18,0 M-4,4 L4,-4 M14,22 L22,14" stroke="#000" stroke-width="0.8" fill="none"/></pattern>
<pattern id="earth" width="40" height="40" patternUnits="userSpaceOnUse">
 <path d="M4,12 l10,0 M20,28 l12,0 M26,6 l8,0 M6,34 l8,0 M4,12 l5,-6 M20,28 l5,-6" stroke="#000" stroke-width="0.9" fill="none"/></pattern>
<pattern id="gravel" width="30" height="30" patternUnits="userSpaceOnUse">
 <circle cx="7" cy="7" r="4.5" fill="none" stroke="#000" stroke-width="0.9"/>
 <circle cx="22" cy="19" r="5" fill="none" stroke="#000" stroke-width="0.9"/>
 <circle cx="8" cy="24" r="3" fill="none" stroke="#000" stroke-width="0.9"/></pattern>
<pattern id="sand" width="16" height="16" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="4" r="1"/><circle cx="11" cy="9" r="1"/><circle cx="6" cy="13" r="1"/></pattern>
<pattern id="insul" width="10" height="10" patternUnits="userSpaceOnUse">
 <path d="M0,0 L10,0 M0,0 L0,10" stroke="#000" stroke-width="0.7" fill="none"/></pattern>
<pattern id="sprayfoam" width="12" height="12" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="3" r="1.1" fill="none" stroke="#000" stroke-width="0.6"/>
 <circle cx="9" cy="8" r="1.4" fill="none" stroke="#000" stroke-width="0.6"/></pattern>
<pattern id="wood" width="60" height="16" patternUnits="userSpaceOnUse">
 <path d="M0,4 C15,1 30,7 60,4 M0,11 C20,14 35,8 60,11" stroke="#000" stroke-width="0.7" fill="none"/></pattern>
<pattern id="ply" width="8" height="8" patternUnits="userSpaceOnUse">
 <path d="M0,8 L8,0" stroke="#000" stroke-width="0.6" fill="none"/></pattern>
<pattern id="gyp" width="10" height="10" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="3" r="0.8"/><circle cx="8" cy="8" r="0.8"/></pattern>
<pattern id="stone" width="16" height="16" patternUnits="userSpaceOnUse">
 <path d="M0,16 L16,0 M-4,4 L4,-4 M12,20 L20,12" stroke="#000" stroke-width="0.8" fill="none"/></pattern>
<pattern id="steel" width="6" height="6" patternUnits="userSpaceOnUse">
 <path d="M0,6 L6,0 M-1.5,1.5 L1.5,-1.5 M4.5,7.5 L7.5,4.5" stroke="#000" stroke-width="1" fill="none"/></pattern>
<pattern id="glass" width="20" height="20" patternUnits="userSpaceOnUse">
 <rect width="20" height="20" fill="#dfe8f7"/></pattern>
<pattern id="ice" width="20" height="20" patternUnits="userSpaceOnUse">
 <path d="M0,20 L20,0" stroke="#000" stroke-width="0.6" fill="none" stroke-dasharray="3 3"/></pattern>
"""


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slugify(s):
    out = "".join(c.lower() if c.isalnum() else "-" for c in s)
    while "--" in out:
        out = out.replace("--", "-")
    return out.strip("-")


def feet_inches(inches):
    """38.25 -> 3'-2 1/4"   (rounded to 1/16")."""
    sixteenths = round(abs(inches) * 16)
    ft, rem = divmod(sixteenths, 192)
    whole, frac = divmod(rem, 16)
    fr = ""
    if frac:
        g = math.gcd(frac, 16)
        fr = f"{frac // g}/{16 // g}"
    inch = f"{whole} {fr}" if whole and fr else (fr or str(whole))
    if ft:
        return f"{ft}' - {whole}{' ' + fr if fr else ''}\""
    return f"{inch}\""


class Detail:
    def __init__(self, number, sheet, title, scale="3", slug=None, jurisdiction=None,
                 project=None, note_wrap=38):
        if str(scale) not in SCALES:
            raise ValueError(f"scale must be one of {sorted(SCALES)} (inches per foot)")
        self.number, self.sheet, self.title = str(number), sheet.upper(), title.upper()
        self.scale = float(scale)
        self.scale_label, self.k = SCALES[str(scale)]
        self.slug = slug or slugify(title)
        self.jurisdiction, self.project = jurisdiction, project
        self.note_wrap = note_wrap
        self.items = []          # (kind, payload) in real inches
        self.notes, self.tags, self.keynotes = [], [], []
        self.general, self.verify_items, self.refs = [], [], []
        self.bbox = [math.inf, math.inf, -math.inf, -math.inf]

    # ---------------------------------------------------------- geometry
    def _grow(self, *pts):
        for x, y in pts:
            self.bbox[0] = min(self.bbox[0], x); self.bbox[1] = min(self.bbox[1], y)
            self.bbox[2] = max(self.bbox[2], x); self.bbox[3] = max(self.bbox[3], y)

    def rect(self, x, y, w, h, hatch="none", edge="med"):
        """A cut or seen material.  hatch: one of HATCHES.  edge: cut|med|thin|none."""
        self.poly([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], hatch, edge)

    def poly(self, pts, hatch="none", edge="med", closed=True):
        if hatch not in HATCHES:
            raise ValueError(f"hatch must be one of {HATCHES}")
        self._grow(*pts)
        self.items.append(("poly", (list(pts), hatch, edge, closed)))

    def line(self, pts, style="med"):
        """style: cut|med|thin|hidden|center|metal|membrane|airbar|vapor.
        membrane and airbar draw blue, the way the office shows SA membranes and
        air/water barriers."""
        self._grow(*pts)
        self.items.append(("line", (list(pts), style)))

    def batt(self, x, y, w, h):
        """Batt / blanket insulation (loops) in a cavity."""
        self._grow((x, y), (x + w, y + h))
        self.items.append(("batt", (x, y, w, h)))

    def xbox(self, x, y, w, h, edge="med"):
        """Framing member in section: box with the X (blocking, plates, headers)."""
        self._grow((x, y), (x + w, y + h))
        self.items.append(("xbox", (x, y, w, h, edge)))

    def fastener(self, x, y, length, angle=0):
        x2 = x + length * math.cos(math.radians(angle)); y2 = y + length * math.sin(math.radians(angle))
        self._grow((x, y), (x2, y2))
        self.items.append(("fastener", (x, y, x2, y2)))

    def sealant(self, x, y, d=0.5):
        """Sealant joint with backer rod, centred at x,y."""
        self._grow((x - d, y - d), (x + d, y + d))
        self.items.append(("sealant", (x, y, d)))

    def break_line(self, x0, y0, x1, y1):
        self._grow((x0, y0), (x1, y1))
        self.items.append(("break", (x0, y0, x1, y1)))

    def grade(self, x0, x1, y):
        self._grow((x0, y), (x1, y))
        self.items.append(("grade", (x0, x1, y)))

    # ---------------------------------------------------------- annotation
    def tag(self, label, at, to=None, sim=False):
        """Assembly tag, drawn the office way: plain box with the tag (e.g. R2, F2, A,
        C13, 3A-X, 2/3/4/5A-X).  sim=True adds SIM under it.  The tag carries the
        build-up - never write a note that repeats it."""
        self._grow(at)
        self.tags.append({"label": label.upper(), "at": at, "to": to, "sim": sim})

    def note(self, text, to, side=None, flag=False, dash=False):
        """Leader note to `to`.  side: 'left'|'right' (default right, the office's usual
        column).  flag=True marks an item that belongs to no assembly - it is listed
        as such in the notes file; the drawing itself stays in the office style."""
        self.notes.append({"text": text.upper(), "to": to, "side": side, "flag": flag, "dash": dash})

    def keynote(self, letter, text, to):
        self.keynotes.append({"key": letter.upper(), "text": text.upper(), "to": to})

    def dim(self, p0, p1, label=None, offset=0):
        (x0, y0), (x1, y1) = p0, p1
        if label is None:
            label = feet_inches(abs(x1 - x0) if abs(x1 - x0) > abs(y1 - y0) else abs(y1 - y0))
        self._grow(p0, p1)
        self.items.append(("dim", (x0, y0, x1, y1, label.upper(), offset)))

    def elev(self, x, y, label, value=None, length=None):
        """Revit-style elevation target: quartered circle, dashed reference line back
        to the drawing, label over EL = value.  e.g. elev(40, 0, 'T.O.F.F. @ MAIN LEVEL',
        "100' - 0\"")."""
        self._grow((x, y))
        self.items.append(("elev", (x, y, label.upper(), (value or "").upper(), length)))

    def grid(self, x, label, y_top=None, y_bot=None):
        """Grid / reference line (GL, FOS, A, 5 ...) - vertical dash-dot with a bubble."""
        self.items.append(("grid", (x, label.upper(), y_top, y_bot)))

    def slope(self, x, y, length, label="SLOPE", direction=-1):
        self._grow((x, y), (x + direction * length, y))
        self.items.append(("slope", (x, y, length, label.upper(), direction)))

    def label(self, x, y, text, underline=True):
        """EXT. / INT. / room names - bold, underlined, as on the office sheets."""
        self._grow((x, y))
        self.items.append(("label", (x, y, text.upper(), underline)))

    def callout(self, x, y, r, number, sheet):
        """Enlarged-detail callout: dashed circle around the area plus a number/sheet bubble."""
        self._grow((x - r, y - r), (x + r, y + r))
        self.items.append(("callout", (x, y, r, str(number), sheet.upper())))
        self.refs.append(f"{number}/{sheet.upper()}")

    def general_note(self, text):
        self.general.append(text.upper())

    def verify(self, text):
        self.verify_items.append(text.upper())

    # ---------------------------------------------------------- render
    def _P(self, x, y):
        return (self.ox + (x - self.bbox[0]) * self.k, self.oy + (y - self.bbox[1]) * self.k)

    def _M(self, X, Y):
        """px back to real inches (for the DXF)."""
        return ((X - self.ox) / self.k + self.bbox[0], (Y - self.oy) / self.k + self.bbox[1])

    def _render(self):
        pad = 2
        self.bbox = [self.bbox[0] - pad, self.bbox[1] - pad, self.bbox[2] + pad, self.bbox[3] + pad]
        dw = (self.bbox[2] - self.bbox[0]) * self.k
        dh = (self.bbox[3] - self.bbox[1]) * self.k
        colw = 9.2 * self.note_wrap + 60
        has_left = any(n["side"] == "left" for n in self.notes)
        grid_top = any(k == "grid" for k, _ in self.items)
        self.ox = 30 + (colw if has_left else 40)
        self.oy = 40 + (70 if grid_top else 0)
        W = int(self.ox + dw + colw + 30)
        body_bottom = self.oy + dh
        self.ann = []   # annotation in px, for the DXF: (kind, data)

        o = []; a = o.append

        def text(x, y, s, cls="n", anchor="start", halo=False, dxf=True):
            h = ' style="paint-order:stroke;stroke:#fff;stroke-width:5;stroke-linejoin:round"' if halo else ''
            a(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{h}>{esc(s)}</text>')
            if dxf:
                self.ann.append(("text", (x, y, s, cls, anchor)))

        def pline(pts, cls, arrow=False, dot=False):
            d = " ".join(("M" if i == 0 else "L") + f"{px:.1f},{py:.1f}" for i, (px, py) in enumerate(pts))
            m = (' marker-end="url(#arw)"' if arrow else '') + (' marker-end="url(#dot)"' if dot else '')
            a(f'<path d="{d}" class="{cls}"{m}/>')
            self.ann.append(("pline", (pts, cls, arrow)))

        P = self._P
        SW = {"cut": 2.6, "med": 1.6, "thin": 0.9, "none": 0}
        for kind, v in self.items:
            if kind == "poly":
                pts, hatch, edge, closed = v
                d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % P(*p) for i, p in enumerate(pts)) + (" z" if closed else "")
                fill = "#fff" if hatch == "none" else f"url(#{hatch})"
                if not closed:
                    fill = "none"
                sw = SW[edge]
                a(f'<path d="{d}" fill="{fill}"' + (f' stroke="#000" stroke-width="{sw}"/>' if sw else '/>'))
            elif kind == "line":
                pts, style = v
                d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % P(*p) for i, p in enumerate(pts))
                a(f'<path d="{d}" class="{style}"/>')
            elif kind == "batt":
                x, y, w, h = v
                (X, Y), (X2, Y2) = P(x, y), P(x + w, y + h)
                a(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{X2-X:.1f}" height="{Y2-Y:.1f}" fill="#fff" stroke="#000" stroke-width="0.9"/>')
                a(f'<path d="{" ".join(_batt_path(X, Y, X2, Y2))}" class="thin"/>')
            elif kind == "xbox":
                x, y, w, h, edge = v
                (X, Y), (X2, Y2) = P(x, y), P(x + w, y + h)
                a(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{X2-X:.1f}" height="{Y2-Y:.1f}" fill="#fff" stroke="#000" stroke-width="{SW[edge]}"/>')
                a(f'<path d="M{X:.1f},{Y:.1f} L{X2:.1f},{Y2:.1f} M{X:.1f},{Y2:.1f} L{X2:.1f},{Y:.1f}" class="thin"/>')
            elif kind == "fastener":
                x, y, x2, y2 = v
                (X, Y), (X2, Y2) = P(x, y), P(x2, y2)
                a(f'<path d="M{X:.1f},{Y:.1f} L{X2:.1f},{Y2:.1f}" class="med" marker-start="url(#dot)"/>')
            elif kind == "sealant":
                x, y, dd = v
                X, Y = P(x, y); r = max(dd * self.k, 4)
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r:.1f}" fill="#fff" stroke="#000" stroke-width="1.1"/>')
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r*0.45:.1f}" fill="#000"/>')
            elif kind == "break":
                x0, y0, x1, y1 = v
                a(f'<path d="{_break_path(*P(x0, y0), *P(x1, y1))}" class="med"/>')
            elif kind == "grade":
                x0, x1, y = v
                (X0, Y), (X1, _) = P(x0, y), P(x1, y)
                a(f'<path d="M{X0:.1f},{Y:.1f} L{X1:.1f},{Y:.1f}" class="cut"/>')
            elif kind == "dim":
                x0, y0, x1, y1, lab, off = v
                (X0, Y0), (X1, Y1) = P(x0, y0), P(x1, y1)
                a(f'<path d="M{X0:.1f},{Y0:.1f} L{X1:.1f},{Y1:.1f}" class="dim" marker-start="url(#tick)" marker-end="url(#tick)"/>')
                self.ann.append(("pline", ([(X0, Y0), (X1, Y1)], "dim", False)))
                if abs(X1 - X0) >= abs(Y1 - Y0):
                    a(f'<path d="M{X0:.1f},{Y0-9:.1f} l0,18 M{X1:.1f},{Y1-9:.1f} l0,18" class="dim"/>')
                    text((X0 + X1) / 2, Y0 - 6 - off * self.k, lab, cls="dimt", anchor="middle", halo=True)
                else:
                    a(f'<path d="M{X0-9:.1f},{Y0:.1f} l18,0 M{X1-9:.1f},{Y1:.1f} l18,0" class="dim"/>')
                    a(f'<g transform="translate({X0-6-off*self.k:.1f},{(Y0+Y1)/2:.1f}) rotate(-90)">')
                    text(0, 0, lab, cls="dimt", anchor="middle", halo=True, dxf=False)
                    a('</g>')
                    self.ann.append(("vtext", (X0 - 6 - off * self.k, (Y0 + Y1) / 2, lab)))
            elif kind == "elev":
                x, y, lab, val, length = v
                X, Y = P(x, y)
                L = (length * self.k) if length else 0
                if L:
                    pline([(X - L, Y), (X - 14, Y)], "hidden")
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="9" fill="#fff" stroke="#000" stroke-width="1.2"/>')
                a(f'<path d="M{X:.1f},{Y:.1f} L{X:.1f},{Y-9:.1f} A9,9 0 0 1 {X+9:.1f},{Y:.1f} z M{X:.1f},{Y:.1f} L{X:.1f},{Y+9:.1f} A9,9 0 0 1 {X-9:.1f},{Y:.1f} z" fill="#000"/>')
                self.ann.append(("target", (X, Y)))
                text(X - 16, Y - 16, lab, cls="dimt", anchor="end", halo=True)
                a(f'<path d="M{X-16-8.2*len(lab):.1f},{Y-12:.1f} L{X-16:.1f},{Y-12:.1f}" class="thin"/>')
                if val:
                    text(X - 16, Y + 3, f"EL = {val}", cls="dimt", anchor="end", halo=True)
            elif kind == "grid":
                x, lab, yt, yb = v
                X, _ = P(x, 0)
                Yt = self.oy - 30 if yt is None else P(0, yt)[1]
                Yb = body_bottom if yb is None else P(0, yb)[1]
                pline([(X, Yt), (X, Yb)], "center")
                a(f'<circle cx="{X:.1f}" cy="{Yt-22:.1f}" r="22" fill="#fff" stroke="#000" stroke-width="1.2"/>')
                self.ann.append(("circle", (X, Yt - 22, 22)))
                text(X, Yt - 16, lab, cls="tag", anchor="middle")
            elif kind == "slope":
                x, y, L, lab, dr = v
                X, Y = P(x, y); Lp = L * self.k * dr
                a(f'<path d="M{X:.1f},{Y:.1f} l{Lp:.1f},0 m{-14*dr},-6 l{14*dr},6 l{-14*dr},6" class="thin"/>')
                text(X + Lp / 2, Y - 6, lab, cls="dimt", anchor="middle", halo=True)
            elif kind == "label":
                x, y, lab, ul = v
                X, Y = P(x, y)
                text(X, Y, lab, cls="kn", anchor="middle", halo=True)
                if ul:
                    w = 9.2 * len(lab)
                    pline([(X - w / 2, Y + 4), (X + w / 2, Y + 4)], "thin")
            elif kind == "callout":
                x, y, r, num, sh = v
                X, Y = P(x, y); R = r * self.k
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R:.1f}" class="hidden"/>')
                bx, by = X + R * 0.72 + 36, Y - R * 0.72 - 36
                pline([(X + R * 0.707, Y - R * 0.707), (bx - 24, by + 24)], "lead")
                a(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="24" fill="#fff" stroke="#000" stroke-width="1.2"/>')
                pline([(bx - 24, by), (bx + 24, by)], "thin")
                text(bx, by - 5, num, cls="n", anchor="middle")
                text(bx, by + 17, sh, cls="sc", anchor="middle")

        # assembly tags - plain box, the office's Revit tag
        for t in self.tags:
            X, Y = P(*t["at"])
            w = max(40, 9.5 * len(t["label"]) + 18); h = 30
            if t["to"]:
                X2, Y2 = P(*t["to"])
                pline([(X, Y), (X2, Y2)], "lead", dot=True)
            a(f'<rect x="{X-w/2:.1f}" y="{Y-h/2:.1f}" width="{w:.1f}" height="{h}" fill="#fff" stroke="#000" stroke-width="1.2"/>')
            self.ann.append(("box", (X - w / 2, Y - h / 2, w, h)))
            text(X, Y + 5, t["label"], cls="tag", anchor="middle")
            if t["sim"]:
                text(X, Y + h / 2 + 15, "SIM", cls="sc", anchor="middle")

        for kn in self.keynotes:
            X, Y = P(*kn["to"])
            pline([(X, Y), (X + 26, Y - 26)], "lead")
            a(f'<path d="M{X+26:.1f},{Y-44:.1f} l15,9 l0,18 l-15,9 l-15,-9 l0,-18 z" fill="#fff" stroke="#000" stroke-width="1.2"/>')
            text(X + 26, Y - 21, kn["key"], cls="kn", anchor="middle")

        # leader notes: right column by default (office habit), left on request
        right = [n for n in self.notes if n["side"] != "left"]
        left = [n for n in self.notes if n["side"] == "left"]
        bottom = body_bottom
        for col, anchor, xcol in ((left, "end", self.ox - 50), (right, "start", self.ox + dw + 50)):
            col.sort(key=lambda n: n["to"][1])
            y = self.oy + 6
            for n in col:
                X2, Y2 = P(*n["to"])
                lines = textwrap.wrap(n["text"], width=self.note_wrap)
                y = max(y, Y2 + 5 - (len(lines) - 1) * 9)
                for i, ln in enumerate(lines):
                    text(xcol, y + i * 18, ln, anchor=anchor)
                fx, sh = (xcol - 8, -26) if anchor == "start" else (xcol + 8, 26)
                cls = "lead"
                pline([(fx, y - 5), (fx + sh, y - 5), (X2, Y2)], cls, arrow=True)
                y += len(lines) * 18 + 10
            bottom = max(bottom, y)

        # office title: bubble (number / sheet), title underlined, scale under
        ty = bottom + 60
        tx0 = 40
        a(f'<circle cx="{tx0+20:.1f}" cy="{ty:.1f}" r="24" fill="none" stroke="#000" stroke-width="1.2"/>')
        a(f'<path d="M{tx0-4:.1f},{ty:.1f} l48,0" class="thin"/>')
        self.ann.append(("circle", (tx0 + 20, ty, 24)))
        self.ann.append(("pline", ([(tx0, ty), (tx0 + 40, ty)], "thin", False)))
        text(tx0 + 20, ty - 5, self.number, cls="sc", anchor="middle")
        text(tx0 + 20, ty + 14, self.sheet, cls="sc", anchor="middle")
        text(tx0 + 58, ty + 2, self.title, cls="ttl")
        tl = max(W - 70, tx0 + 58 + 15.5 * len(self.title))
        pline([(tx0 + 40, ty + 10), (tl, ty + 10)], "med")
        text(tx0 + 58, ty + 30, "SCALE : " + self.scale_label, cls="sc")
        W = int(max(W, tl + 30))
        H = int(ty + 50)
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
                f"<defs><style>{STYLE}</style>{DEFS}</defs>",
                f'<rect width="{W}" height="{H}" fill="#fff"/>']
        return "\n".join(head + o + ["</svg>"]), W, H

    # ---------------------------------------------------------- DXF
    def _dxf(self, path):
        try:
            import ezdxf
            from ezdxf.enums import TextEntityAlignment
        except ImportError:
            print("DXF skipped - pip install ezdxf")
            return
        doc = ezdxf.new("R2010", setup=True)
        doc.units = ezdxf.units.IN
        msp = doc.modelspace()
        LAY = {"cut": ("A-DETL-HEVY", 7, 50), "med": ("A-DETL-MEDM", 7, 30), "thin": ("A-DETL-LITE", 7, 13),
               "hidden": ("A-DETL-HIDN", 7, 18), "center": ("A-ANNO-GRID", 7, 13), "metal": ("A-DETL-MTL", 7, 50),
               "membrane": ("A-DETL-MEMB", 5, 35), "airbar": ("A-DETL-MEMB", 5, 35), "vapor": ("A-DETL-VAPR", 7, 18),
               "patt": ("A-DETL-PATT", 8, 9), "lead": ("A-ANNO-NOTE", 7, 13), "dim": ("A-ANNO-DIMS", 7, 13),
               "text": ("A-ANNO-NOTE", 7, 13), "tag": ("A-ANNO-TAGS", 7, 18)}
        for name, color, lw in set(LAY.values()):
            if name not in doc.layers:
                doc.layers.add(name, color=color, lineweight=lw)
        doc.layers.get("A-DETL-HIDN").dxf.linetype = "DASHED"
        doc.layers.get("A-ANNO-GRID").dxf.linetype = "CENTER"
        f = 12.0 / self.scale             # model inches per paper inch
        th = 3 / 32 * f                   # 3/32" text on paper

        def m(x, y):                      # real inches, y down -> DXF y up
            return (x, -y)

        def M(X, Y):
            x, y = self._M(X, Y)
            return (x, -y)

        for kind, v in self.items:
            if kind == "poly":
                pts, hatch, edge, closed = v
                q = [m(*p) for p in pts]
                if hatch not in ("none", "batt") and hatch in DXF_PATTERN and closed:
                    pat, sc = DXF_PATTERN[hatch]
                    h = msp.add_hatch(color=256, dxfattribs={"layer": "A-DETL-PATT"})
                    h.set_pattern_fill(pat, scale=sc * f / 12)
                    h.paths.add_polyline_path(q, is_closed=True)
                if edge != "none":
                    msp.add_lwpolyline(q, close=closed, dxfattribs={"layer": LAY[edge][0]})
            elif kind == "line":
                pts, style = v
                msp.add_lwpolyline([m(*p) for p in pts], dxfattribs={"layer": LAY.get(style, LAY["med"])[0]})
            elif kind == "batt":
                x, y, w, h = v
                msp.add_lwpolyline([m(x, y), m(x + w, y), m(x + w, y + h), m(x, y + h)], close=True,
                                   dxfattribs={"layer": LAY["thin"][0]})
                vert = h >= w
                span, run = (w, h) if vert else (h, w)
                n = max(int(run // (span * 0.5)), 1); step = run / n
                zz = []
                for i in range(n + 1):
                    t = i * step; s = 0 if i % 2 == 0 else span
                    zz.append(m(x + s, y + t) if vert else m(x + t, y + s))
                msp.add_lwpolyline(zz, dxfattribs={"layer": LAY["thin"][0]})
            elif kind == "xbox":
                x, y, w, h, edge = v
                msp.add_lwpolyline([m(x, y), m(x + w, y), m(x + w, y + h), m(x, y + h)], close=True,
                                   dxfattribs={"layer": LAY[edge][0]})
                msp.add_line(m(x, y), m(x + w, y + h), dxfattribs={"layer": LAY["thin"][0]})
                msp.add_line(m(x, y + h), m(x + w, y), dxfattribs={"layer": LAY["thin"][0]})
            elif kind == "fastener":
                x, y, x2, y2 = v
                msp.add_line(m(x, y), m(x2, y2), dxfattribs={"layer": LAY["med"][0]})
            elif kind == "sealant":
                x, y, dd = v
                msp.add_circle(m(x, y), dd, dxfattribs={"layer": LAY["thin"][0]})
            elif kind == "break":
                x0, y0, x1, y1 = v
                msp.add_lwpolyline([m(*p) for p in _break_pts(x0, y0, x1, y1, 1.0 / self.k)],
                                   dxfattribs={"layer": LAY["med"][0]})
            elif kind == "grade":
                x0, x1, y = v
                msp.add_line(m(x0, y), m(x1, y), dxfattribs={"layer": LAY["cut"][0]})
            elif kind == "slope":
                x, y, L, lab, dr = v
                msp.add_line(m(x, y), m(x + dr * L, y), dxfattribs={"layer": LAY["dim"][0]})

        for kind, v in self.ann:
            if kind == "pline":
                pts, cls, arrow = v
                lay = LAY.get(cls, LAY["lead"])[0]
                q = [M(*p) for p in pts]
                msp.add_lwpolyline(q, dxfattribs={"layer": lay})
                if arrow and len(q) >= 2:
                    (x1, y1), (x2, y2) = q[-2], q[-1]
                    ang = math.atan2(y2 - y1, x2 - x1); L = 0.09 * f; wdt = 0.03 * f
                    bx, by = x2 - L * math.cos(ang), y2 - L * math.sin(ang)
                    px, py = -math.sin(ang) * wdt, math.cos(ang) * wdt
                    s = msp.add_solid([(x2, y2), (bx + px, by + py), (bx - px, by - py)],
                                      dxfattribs={"layer": lay})
            elif kind == "text":
                X, Y, s, cls, anchor = v
                hgt = th * (1.6 if cls == "ttl" else 1.0)
                al = {"start": TextEntityAlignment.BOTTOM_LEFT, "middle": TextEntityAlignment.BOTTOM_CENTER,
                      "end": TextEntityAlignment.BOTTOM_RIGHT}[anchor]
                msp.add_text(s, height=hgt, dxfattribs={"layer": LAY["text"][0], "style": "OpenSans"}
                             ).set_placement(M(X, Y), align=al)
            elif kind == "vtext":
                X, Y, s = v
                msp.add_text(s, height=th, rotation=90, dxfattribs={"layer": LAY["dim"][0]}
                             ).set_placement(M(X, Y), align=TextEntityAlignment.BOTTOM_CENTER)
            elif kind == "box":
                X, Y, w, h = v
                msp.add_lwpolyline([M(X, Y), M(X + w, Y), M(X + w, Y + h), M(X, Y + h)], close=True,
                                   dxfattribs={"layer": LAY["tag"][0]})
            elif kind == "circle":
                X, Y, r = v
                msp.add_circle(M(X, Y), r / self.k, dxfattribs={"layer": LAY["tag"][0]})
            elif kind == "target":
                X, Y = v
                msp.add_circle(M(X, Y), 9 / self.k, dxfattribs={"layer": LAY["tag"][0]})
        doc.saveas(path)
        print("wrote", path)

    # ---------------------------------------------------------- output
    def notes_text(self):
        """Notes in the order they go into Revit, plus what the reviewer needs."""
        L = [f"{self.number} / {self.sheet}   {self.title}", f"SCALE : {self.scale_label}", ""]
        if self.tags:
            L.append("TAGS (build-up is in the assembly schedule - not repeated in the notes)")
            for t in sorted({t['label'] + (' SIM' if t['sim'] else '') for t in self.tags}):
                L.append(f"    {t}")
            L.append("")
        if self.notes:
            L.append("LEADER NOTES  (top to bottom; # = item in no assembly)")
            for n in sorted(self.notes, key=lambda n: (n["side"] == "left", n["to"][1])):
                body = textwrap.wrap(n["text"], width=60)
                L.append(("  # " if n["flag"] else "    ") + body[0])
                L += ["      " + b for b in body[1:]]
            L.append("")
        if self.keynotes:
            L.append("KEYNOTES")
            for k in sorted(self.keynotes, key=lambda k: k["key"]):
                body = textwrap.wrap(k["text"], width=60)
                L.append(f"{k['key']}.  {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        if self.general:
            L.append("NOTES FOR THIS DETAIL")
            for i, g in enumerate(self.general, 1):
                body = textwrap.wrap(g, width=80)
                L.append(f"{i}.  {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        if self.verify_items:
            L.append("VERIFY BEFORE ISSUE (not on the drawing)")
            for v in self.verify_items:
                body = textwrap.wrap(v, width=80)
                L.append(f"-   {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        return "\n".join(L) + "\n"

    def manifest(self):
        return {
            "number": self.number, "sheet": self.sheet, "title": self.title,
            "scale": self.scale_label, "jurisdiction": self.jurisdiction, "project": self.project,
            "tags": sorted({t["label"] for t in self.tags}),
            "notes": [n["text"] for n in self.notes],
            "flagged": [n["text"] for n in self.notes if n["flag"]],
            "keynotes": {k["key"]: k["text"] for k in self.keynotes},
            "general": self.general, "verify": self.verify_items, "callouts": self.refs,
        }

    def save(self, outdir, assemblies=None, png=True, dxf=True, check=True):
        os.makedirs(outdir, exist_ok=True)
        num = self.number.zfill(2) if self.number.isdigit() else self.number
        base = os.path.join(outdir, f"{num}-{self.sheet}-{self.slug}")
        svg, W, H = self._render()
        with open(base + ".svg", "w") as fh:
            fh.write(svg)
        with open(base + ".notes.txt", "w") as fh:
            fh.write(self.notes_text())
        with open(base + ".json", "w") as fh:
            json.dump(self.manifest(), fh, indent=1)
        print("wrote", base + ".svg")
        if png:
            render_png(base + ".svg", base + ".png", W, H)
        if dxf:
            self._dxf(base + ".dxf")
        status = 0
        if check:
            here = os.path.dirname(os.path.abspath(__file__))
            cmd = [sys.executable, os.path.join(here, "check_notes.py"), base + ".json"]
            if assemblies:
                cmd += ["--assemblies", assemblies]
            status = subprocess.call(cmd)
        return status


def _batt_path(X, Y, X2, Y2):
    vertical = (Y2 - Y) >= (X2 - X)
    span, run = ((X2 - X), (Y2 - Y)) if vertical else ((Y2 - Y), (X2 - X))
    step = max(span * 0.5, 6)
    out = []
    for i in range(int(run // step)):
        t0 = i * step
        if vertical:
            c = X if i % 2 == 0 else X2
            out.append(f"M{c:.1f},{Y+t0:.1f} A{span/2:.1f},{step/2:.1f} 0 0 {1 if i % 2 == 0 else 0} {c:.1f},{Y+t0+step:.1f}")
        else:
            c = Y if i % 2 == 0 else Y2
            out.append(f"M{X+t0:.1f},{c:.1f} A{step/2:.1f},{span/2:.1f} 0 0 {0 if i % 2 == 0 else 1} {X+t0+step:.1f},{c:.1f}")
    return out


def _break_pts(X0, Y0, X1, Y1, u=1.0):
    L = math.hypot(X1 - X0, Y1 - Y0) or 1
    ux, uy = (X1 - X0) / L, (Y1 - Y0) / L
    nx, ny = -uy, ux
    mx, my = (X0 + X1) / 2, (Y0 + Y1) / 2
    return [(X0 - ux * 12 * u, Y0 - uy * 12 * u), (mx - ux * 10 * u, my - uy * 10 * u),
            (mx - ux * 4 * u + nx * 16 * u, my - uy * 4 * u + ny * 16 * u),
            (mx + ux * 4 * u - nx * 16 * u, my + uy * 4 * u - ny * 16 * u),
            (mx + ux * 10 * u, my + uy * 10 * u), (X1 + ux * 12 * u, Y1 + uy * 12 * u)]


def _break_path(X0, Y0, X1, Y1):
    return " ".join(("M" if i == 0 else "L") + f"{px:.1f},{py:.1f}" for i, (px, py) in enumerate(_break_pts(X0, Y0, X1, Y1)))


def _chromium():
    for p in (os.environ.get("CHROMIUM"), "/opt/pw-browsers/chromium", shutil.which("chromium"),
              shutil.which("chromium-browser"), shutil.which("google-chrome")):
        if p and os.path.isfile(p) and os.access(p, os.X_OK):
            return p
    root = "/opt/pw-browsers"
    if os.path.isdir(root):
        for d in sorted(os.listdir(root), reverse=True):
            p = os.path.join(root, d, "chrome-linux", "chrome")
            if d.startswith("chromium-") and os.path.isfile(p):
                return p
    return None


def render_png(svg_path, png_path, W, H):
    """Render with headless Chromium (no Python image libraries needed)."""
    chrome = _chromium()
    if not chrome:
        print("PNG skipped - no Chromium found (set CHROMIUM=/path/to/chrome). The SVG is the drawing.")
        return
    html = (f'<html><body style="margin:0;background:#fff"><img src="file://{os.path.abspath(svg_path)}" '
            f'width="{W}" height="{H}"></body></html>')
    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "p.html")
        with open(page, "w") as fh:
            fh.write(html)
        r = subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--allow-file-access-from-files", f"--window-size={W},{H + 160}",
                            f"--screenshot={os.path.abspath(png_path)}", "file://" + page],
                           capture_output=True, text=True, timeout=120)
    if os.path.exists(png_path):
        print("wrote", png_path)
    else:
        print("PNG render failed:", r.stderr.strip()[-400:])
