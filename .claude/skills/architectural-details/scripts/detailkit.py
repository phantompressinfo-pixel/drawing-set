# -*- coding: utf-8 -*-
"""detailkit - draw an office construction detail as SVG (+ PNG), with its notes.

Geometry is entered in REAL INCHES (x to the right, y DOWN, any origin). The kit
scales it for the detail scale, lays the leader notes out in columns either side
of the drawing, and writes four files:

    <out>/<NN>-<SHEET>-<slug>.svg        the detail sheet
    <out>/<NN>-<SHEET>-<slug>.png        a render of it (headless Chromium)
    <out>/<NN>-<SHEET>-<slug>.notes.txt  the notes as sheet text
    <out>/<NN>-<SHEET>-<slug>.json       manifest the checker reads

Minimal use:

    from detailkit import Detail
    d = Detail(6, "A6.01", "STONE WALL TO STANDING SEAM ROOF", scale="3", slug="stone-wall-roof")
    d.rect(0, 0, 12, 40, hatch="conc")                 # 12" concrete wall
    d.tag("W10", at=(-10, 8), to=(6, 8))               # assembly tag, leader to the wall
    d.note("BASE FLASHING - TURN UP 8\\" MIN. ABOVE FINISHED ROOF.", to=(-1, 30))
    d.save("details", assemblies="assemblies.yaml")    # runs check_notes.py too

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
# Paper is drawn at 56 px per paper inch, so text is the same size on every sheet
# and a drawing's px-per-real-inch follows from its scale.  "3" means 3" = 1'-0".
SCALES = {
    "12": ("FULL SIZE", 56.0),
    "6": ('6" = 1\'-0"', 28.0),
    "3": ('3" = 1\'-0"', 14.0),
    "1.5": ('1 1/2" = 1\'-0"', 7.0),
    "1": ('1" = 1\'-0"', 56 / 12),
    "0.75": ('3/4" = 1\'-0"', 3.5),
    "0.5": ('1/2" = 1\'-0"', 56 / 24),
    "0.375": ('3/8" = 1\'-0"', 1.75),
    "0.25": ('1/4" = 1\'-0"', 56 / 48),
}

HATCHES = ("none", "conc", "cmu", "earth", "gravel", "insul", "batt", "wood", "ply",
           "gyp", "stone", "steel", "membrane", "air", "sand", "ice")

STYLE = """
 text{font-family:Arial,Helvetica,sans-serif;fill:#000}
 .n{font-size:17.5px}
 .tag{font-size:21px;font-weight:bold}
 .kn{font-size:17px;font-weight:bold}
 .dimt{font-size:16px;font-weight:bold}
 .h1{font-size:34px;font-weight:bold;letter-spacing:1px}
 .h3{font-size:20px;font-weight:bold;letter-spacing:.6px}
 .ttl{font-size:28px;letter-spacing:1px}
 .sc{font-size:19px;fill:#444}
 .lead{fill:none;stroke:#000;stroke-width:1.2}
 .cut{fill:none;stroke:#000;stroke-width:2.6}
 .med{fill:none;stroke:#000;stroke-width:1.7}
 .thin{fill:none;stroke:#000;stroke-width:1.0}
 .hidden{fill:none;stroke:#000;stroke-width:1.2;stroke-dasharray:12 7}
 .center{fill:none;stroke:#000;stroke-width:1.0;stroke-dasharray:28 6 5 6}
 .metal{fill:none;stroke:#000;stroke-width:4;stroke-linejoin:miter}
 .membrane{fill:none;stroke:#000;stroke-width:3}
 .airbar{fill:none;stroke:#000;stroke-width:2.2;stroke-dasharray:16 5 3 5}
 .vapor{fill:none;stroke:#000;stroke-width:1.6;stroke-dasharray:4 4}
 .dim{fill:none;stroke:#000;stroke-width:1.1}
"""

DEFS = """
<marker id="arw" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
 <path d="M0,1 L12,6 L0,11 z" fill="#000"/></marker>
<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="8" markerHeight="8">
 <circle cx="5" cy="5" r="4" fill="#000"/></marker>
<marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9" orient="auto">
 <path d="M1,9 L9,1" stroke="#000" stroke-width="2"/></marker>
<pattern id="conc" width="52" height="52" patternUnits="userSpaceOnUse">
 <path d="M12,8 l0,10 M7,13 l10,0 M38,30 l0,10 M33,35 l10,0" stroke="#000" stroke-width="1.1" fill="none"/>
 <circle cx="30" cy="12" r="1.8"/><circle cx="8" cy="36" r="1.6"/><circle cx="45" cy="6" r="1.5"/>
 <circle cx="22" cy="45" r="1.7"/><circle cx="44" cy="47" r="1.4"/><path d="M26,25 l5,3 l-4,3 z"/></pattern>
<pattern id="cmu" width="18" height="18" patternUnits="userSpaceOnUse">
 <path d="M0,18 L18,0 M-4,4 L4,-4 M14,22 L22,14" stroke="#000" stroke-width="0.9" fill="none"/></pattern>
<pattern id="earth" width="40" height="40" patternUnits="userSpaceOnUse">
 <path d="M4,12 l10,0 M20,28 l12,0 M26,6 l8,0 M6,34 l8,0 M4,12 l5,-6 M20,28 l5,-6" stroke="#000" stroke-width="1" fill="none"/></pattern>
<pattern id="gravel" width="30" height="30" patternUnits="userSpaceOnUse">
 <circle cx="7" cy="7" r="4.5" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="22" cy="19" r="5" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="8" cy="24" r="3" fill="none" stroke="#000" stroke-width="1"/></pattern>
<pattern id="sand" width="16" height="16" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="4" r="1"/><circle cx="11" cy="9" r="1"/><circle cx="6" cy="13" r="1"/></pattern>
<pattern id="insul" width="14" height="14" patternUnits="userSpaceOnUse">
 <path d="M0,0 L14,0 M0,0 L0,14" stroke="#000" stroke-width="0.8" fill="none"/></pattern>
<pattern id="wood" width="60" height="16" patternUnits="userSpaceOnUse">
 <path d="M0,4 C15,1 30,7 60,4 M0,11 C20,14 35,8 60,11" stroke="#000" stroke-width="0.8" fill="none"/></pattern>
<pattern id="ply" width="10" height="10" patternUnits="userSpaceOnUse">
 <path d="M0,10 L10,0" stroke="#000" stroke-width="0.7" fill="none"/></pattern>
<pattern id="gyp" width="12" height="12" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="3" r="0.9"/><circle cx="9" cy="9" r="0.9"/></pattern>
<pattern id="stone" width="16" height="16" patternUnits="userSpaceOnUse">
 <path d="M0,16 L16,0 M-4,4 L4,-4 M12,20 L20,12" stroke="#000" stroke-width="0.9" fill="none"/></pattern>
<pattern id="steel" width="8" height="8" patternUnits="userSpaceOnUse">
 <path d="M0,8 L8,0 M-2,2 L2,-2 M6,10 L10,6" stroke="#000" stroke-width="1.2" fill="none"/></pattern>
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
        return f"{ft}'-{whole}{' ' + fr if fr else ''}\""
    return f"{inch}\""


class Detail:
    def __init__(self, number, sheet, title, scale="3", slug=None, jurisdiction=None,
                 project=None, note_wrap=44):
        if str(scale) not in SCALES:
            raise ValueError(f"scale must be one of {sorted(SCALES)} (inches per foot)")
        self.number, self.sheet, self.title = str(number), sheet.upper(), title.upper()
        self.scale_label, self.k = SCALES[str(scale)]
        self.slug = slug or slugify(title)
        self.jurisdiction, self.project = jurisdiction, project
        self.note_wrap = note_wrap
        self.items = []          # (kind, payload) drawn in real inches
        self.notes = []          # leader notes
        self.tags = []           # assembly tags
        self.keynotes = []       # lettered keynotes
        self.general = []        # detail general notes
        self.verify_items = []   # verify / coordinate before issue
        self.refs = []           # SEE n/Ax.xx callouts
        self.bbox = [math.inf, math.inf, -math.inf, -math.inf]

    # ---------------------------------------------------------- geometry
    def _grow(self, *pts):
        for x, y in pts:
            self.bbox[0] = min(self.bbox[0], x); self.bbox[1] = min(self.bbox[1], y)
            self.bbox[2] = max(self.bbox[2], x); self.bbox[3] = max(self.bbox[3], y)

    def rect(self, x, y, w, h, hatch="none", edge="med"):
        """A cut or seen material.  hatch: one of HATCHES.  edge: cut|med|thin|none."""
        if hatch not in HATCHES:
            raise ValueError(f"hatch must be one of {HATCHES}")
        self._grow((x, y), (x + w, y + h))
        self.items.append(("rect", (x, y, w, h, hatch, edge)))

    def poly(self, pts, hatch="none", edge="med", closed=True):
        self._grow(*pts)
        self.items.append(("poly", (list(pts), hatch, edge, closed)))

    def line(self, pts, style="med"):
        """style: cut|med|thin|hidden|center|metal|membrane|airbar|vapor."""
        self._grow(*pts)
        self.items.append(("line", (list(pts), style)))

    def batt(self, x, y, w, h):
        """Batt / blanket insulation (loop pattern) in a cavity."""
        self._grow((x, y), (x + w, y + h))
        self.items.append(("batt", (x, y, w, h)))

    def fastener(self, x, y, length, angle=0):
        """A screw / nail / anchor drawn as a line with a head, angle in degrees from +x."""
        x2 = x + length * math.cos(math.radians(angle)); y2 = y + length * math.sin(math.radians(angle))
        self._grow((x, y), (x2, y2))
        self.items.append(("fastener", (x, y, x2, y2)))

    def sealant(self, x, y, d=0.5):
        """Sealant joint with backer rod, centered at x,y."""
        self._grow((x - d, y - d), (x + d, y + d))
        self.items.append(("sealant", (x, y, d)))

    def break_line(self, x0, y0, x1, y1):
        self._grow((x0, y0), (x1, y1))
        self.items.append(("break", (x0, y0, x1, y1)))

    def grade(self, x0, x1, y):
        """Finish grade line with the earth tick marks below."""
        self._grow((x0, y), (x1, y))
        self.items.append(("grade", (x0, x1, y)))

    # ---------------------------------------------------------- annotation
    def tag(self, label, at, to=None):
        """Assembly tag (boxed) at `at`, optional leader to `to`.  The tag carries the
        assembly's build-up - do not write a note that repeats it."""
        self._grow(at)
        self.tags.append({"label": label.upper(), "at": at, "to": to})

    def note(self, text, to, side=None, flag=False, dash=False):
        """Leader note pointing at `to`.  side: 'left'|'right' (default: nearer side).
        flag=True prints a black square: an item that is NOT in any assembly and must
        be built exactly as noted."""
        self.notes.append({"text": text.upper(), "to": to, "side": side, "flag": flag, "dash": dash})

    def keynote(self, letter, text, to):
        self.keynotes.append({"key": letter.upper(), "text": text.upper(), "to": to})

    def dim(self, p0, p1, label=None, offset=0):
        """Dimension between two real points (horizontal or vertical); label defaults to
        the measured distance.  offset shifts the string perpendicular, in real inches."""
        (x0, y0), (x1, y1) = p0, p1
        if label is None:
            label = feet_inches(abs(x1 - x0) if abs(x1 - x0) > abs(y1 - y0) else abs(y1 - y0))
        self._grow(p0, p1)
        self.items.append(("dim", (x0, y0, x1, y1, label.upper(), offset)))

    def elev(self, x, y, label):
        """Elevation target: 'T.O. SLAB EL. 100'-0"'."""
        self._grow((x, y))
        self.items.append(("elev", (x, y, label.upper())))

    def slope(self, x, y, length, label="SLOPE - SEE ROOF PLAN", direction=-1):
        self._grow((x, y), (x + direction * length, y))
        self.items.append(("slope", (x, y, length, label.upper(), direction)))

    def label(self, x, y, text, anchor="middle"):
        """Plain in-drawing label such as EXT. / INT. / CRAWLSPACE."""
        self._grow((x, y))
        self.items.append(("label", (x, y, text.upper(), anchor)))

    def callout(self, x, y, r, number, sheet):
        """Enlarged-detail callout (wall sections): dashed circle radius r (real inches)
        around the area, plus a bubble reading number / sheet."""
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

    def _hatch_fill(self, hatch):
        return "#fff" if hatch == "none" else f"url(#{hatch})"

    def _render(self):
        pad = 1.5
        self.bbox = [self.bbox[0] - pad, self.bbox[1] - pad, self.bbox[2] + pad, self.bbox[3] + pad]
        dw = (self.bbox[2] - self.bbox[0]) * self.k
        dh = (self.bbox[3] - self.bbox[1]) * self.k
        colw = 12 * self.note_wrap + 40        # note column width in px
        self.ox, self.oy = 60 + colw, 200
        W = int(self.ox + dw + colw + 60)
        body_bottom = self.oy + dh

        o = []; a = o.append

        def text(x, y, s, cls="n", anchor="start", halo=False):
            h = ' style="paint-order:stroke;stroke:#fff;stroke-width:6;stroke-linejoin:round"' if halo else ''
            a(f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{h}>{esc(s)}</text>')

        P = self._P
        for kind, v in self.items:
            if kind == "rect":
                x, y, w, h, hatch, edge = v
                (X, Y), (X2, Y2) = P(x, y), P(x + w, y + h)
                sw = {"cut": 2.6, "med": 1.7, "thin": 1.0, "none": 0}[edge]
                a(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{X2-X:.1f}" height="{Y2-Y:.1f}" fill="{self._hatch_fill(hatch)}"'
                  + (f' stroke="#000" stroke-width="{sw}"/>' if sw else '/>'))
            elif kind == "poly":
                pts, hatch, edge, closed = v
                d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % P(*p) for i, p in enumerate(pts)) + (" z" if closed else "")
                sw = {"cut": 2.6, "med": 1.7, "thin": 1.0, "none": 0}[edge]
                a(f'<path d="{d}" fill="{self._hatch_fill(hatch) if closed else "none"}"'
                  + (f' stroke="#000" stroke-width="{sw}"/>' if sw else '/>'))
            elif kind == "line":
                pts, style = v
                d = " ".join(("M" if i == 0 else "L") + "%.1f,%.1f" % P(*p) for i, p in enumerate(pts))
                a(f'<path d="{d}" class="{style}"/>')
            elif kind == "batt":
                x, y, w, h = v
                (X, Y), (X2, Y2) = P(x, y), P(x + w, y + h)
                a(f'<rect x="{X:.1f}" y="{Y:.1f}" width="{X2-X:.1f}" height="{Y2-Y:.1f}" fill="#fff" stroke="#000" stroke-width="1"/>')
                vertical = (Y2 - Y) >= (X2 - X)
                span, run = ((X2 - X), (Y2 - Y)) if vertical else ((Y2 - Y), (X2 - X))
                step = max(span * 0.5, 6)
                n = int(run // step)
                path = []
                for i in range(n):
                    t0 = i * step
                    if vertical:
                        cx0 = X if i % 2 == 0 else X2
                        path.append(f"M{cx0:.1f},{Y+t0:.1f} A{span/2:.1f},{step/2:.1f} 0 0 {1 if i % 2 == 0 else 0} {cx0:.1f},{Y+t0+step:.1f}")
                    else:
                        cy0 = Y if i % 2 == 0 else Y2
                        path.append(f"M{X+t0:.1f},{cy0:.1f} A{step/2:.1f},{span/2:.1f} 0 0 {0 if i % 2 == 0 else 1} {X+t0+step:.1f},{cy0:.1f}")
                a(f'<path d="{" ".join(path)}" class="thin"/>')
            elif kind == "fastener":
                x, y, x2, y2 = v
                (X, Y), (X2, Y2) = P(x, y), P(x2, y2)
                a(f'<path d="M{X:.1f},{Y:.1f} L{X2:.1f},{Y2:.1f}" class="med" marker-start="url(#dot)"/>')
            elif kind == "sealant":
                x, y, d = v
                X, Y = P(x, y)
                r = max(d * self.k, 4)
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r:.1f}" fill="#fff" stroke="#000" stroke-width="1.2"/>')
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r*0.45:.1f}" fill="#000"/>')
            elif kind == "break":
                x0, y0, x1, y1 = v
                (X0, Y0), (X1, Y1) = P(x0, y0), P(x1, y1)
                L = math.hypot(X1 - X0, Y1 - Y0) or 1
                ux, uy = (X1 - X0) / L, (Y1 - Y0) / L
                nx, ny = -uy, ux
                mx, my = (X0 + X1) / 2, (Y0 + Y1) / 2
                pts = [(X0 - ux * 12, Y0 - uy * 12), (mx - ux * 10, my - uy * 10),
                       (mx - ux * 4 + nx * 16, my - uy * 4 + ny * 16),
                       (mx + ux * 4 - nx * 16, my + uy * 4 - ny * 16),
                       (mx + ux * 10, my + uy * 10), (X1 + ux * 12, Y1 + uy * 12)]
                a('<path d="' + " ".join(("M" if i == 0 else "L") + f"{px:.1f},{py:.1f}" for i, (px, py) in enumerate(pts)) + '" class="med"/>')
            elif kind == "grade":
                x0, x1, y = v
                (X0, Y), (X1, _) = P(x0, y), P(x1, y)
                a(f'<path d="M{X0:.1f},{Y:.1f} L{X1:.1f},{Y:.1f}" class="cut"/>')
                tx = X0 + 8
                while tx < X1 - 20:
                    a(f'<path d="M{tx:.1f},{Y:.1f} l14,14 M{tx+8:.1f},{Y:.1f} l14,14 M{tx+16:.1f},{Y:.1f} l14,14" class="thin"/>')
                    tx += 60
            elif kind == "dim":
                x0, y0, x1, y1, lab, off = v
                (X0, Y0), (X1, Y1) = P(x0, y0), P(x1, y1)
                a(f'<path d="M{X0:.1f},{Y0:.1f} L{X1:.1f},{Y1:.1f}" class="dim" marker-start="url(#tick)" marker-end="url(#tick)"/>')
                if abs(X1 - X0) >= abs(Y1 - Y0):
                    a(f'<path d="M{X0:.1f},{Y0-11:.1f} l0,22 M{X1:.1f},{Y1-11:.1f} l0,22" class="dim"/>')
                    text((X0 + X1) / 2, Y0 - 8 - off * self.k, lab, cls="dimt", anchor="middle", halo=True)
                else:
                    a(f'<path d="M{X0-11:.1f},{Y0:.1f} l22,0 M{X1-11:.1f},{Y1:.1f} l22,0" class="dim"/>')
                    a(f'<g transform="translate({X0-8-off*self.k:.1f},{(Y0+Y1)/2:.1f}) rotate(-90)">')
                    text(0, 0, lab, cls="dimt", anchor="middle", halo=True)
                    a('</g>')
            elif kind == "elev":
                x, y, lab = v
                X, Y = P(x, y)
                a(f'<path d="M{X:.1f},{Y:.1f} l-13,-12 l26,0 z" fill="#000"/>')
                text(X + 20, Y - 8, lab, cls="dimt", halo=True)
            elif kind == "slope":
                x, y, L, lab, dr = v
                X, Y = P(x, y)
                Lp = L * self.k * dr
                a(f'<path d="M{X:.1f},{Y:.1f} l{Lp:.1f},0 m{-16*dr},-8 l{16*dr},8 l{-16*dr},8" class="thin"/>')
                text(X, Y - 8, lab, cls="dimt", anchor="end" if dr < 0 else "start", halo=True)
            elif kind == "label":
                x, y, lab, anc = v
                X, Y = P(x, y)
                w = 13 * len(lab) + 30
                bx = X - w / 2 if anc == "middle" else (X if anc == "start" else X - w)
                a(f'<rect x="{bx:.1f}" y="{Y-30:.1f}" width="{w}" height="44" fill="#fff" stroke="#000" stroke-width="1.6"/>')
                text(bx + w / 2, Y, lab, cls="tag", anchor="middle")
            elif kind == "callout":
                x, y, r, num, sh = v
                X, Y = P(x, y)
                R = r * self.k
                a(f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{R:.1f}" class="hidden"/>')
                bx, by = X + R * 0.72 + 40, Y - R * 0.72 - 40
                a(f'<path d="M{X+R*0.707:.1f},{Y-R*0.707:.1f} L{bx-28:.1f},{by+28:.1f}" class="lead"/>')
                a(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="38" fill="#fff" stroke="#000" stroke-width="1.8"/>')
                a(f'<path d="M{bx-38:.1f},{by:.1f} l76,0" class="thin"/>')
                text(bx, by - 8, num, cls="tag", anchor="middle")
                text(bx, by + 26, sh, cls="n", anchor="middle")

        # assembly tags
        for t in self.tags:
            X, Y = P(*t["at"])
            w = max(64, 16 * len(t["label"]) + 24)
            if t["to"]:
                X2, Y2 = P(*t["to"])
                a(f'<path d="M{X:.1f},{Y:.1f} L{X2:.1f},{Y2:.1f}" class="lead" marker-end="url(#dot)"/>')
            a(f'<rect x="{X-w/2:.1f}" y="{Y-19:.1f}" width="{w}" height="38" fill="#fff" stroke="#000" stroke-width="2.2"/>')
            text(X, Y + 8, t["label"], cls="tag", anchor="middle")

        # keynote bubbles on the drawing
        for kn in self.keynotes:
            X, Y = P(*kn["to"])
            a(f'<path d="M{X:.1f},{Y:.1f} l30,-30" class="lead" marker-start="url(#dot)"/>')
            a(f'<path d="M{X+30:.1f},{Y-50:.1f} l17,10 l0,20 l-17,10 l-17,-10 l0,-20 z" fill="#fff" stroke="#000" stroke-width="1.6"/>')
            text(X + 30, Y - 24, kn["key"], cls="kn", anchor="middle")

        # leader notes - two columns, sorted by target height, no overlaps
        cx = (self.bbox[0] + self.bbox[2]) / 2
        left = [n for n in self.notes if (n["side"] or ("left" if n["to"][0] <= cx else "right")) == "left"]
        right = [n for n in self.notes if n not in left]
        bottom = body_bottom
        for col, anchor, xcol in ((left, "end", self.ox - 40), (right, "start", self.ox + dw + 40)):
            col.sort(key=lambda n: n["to"][1])
            y = self.oy + 10
            for n in col:
                X2, Y2 = P(*n["to"])
                lines = textwrap.wrap(n["text"], width=self.note_wrap)
                y = max(y, Y2 - 7 - (len(lines) - 1) * 11)
                tx = xcol
                if n["flag"]:
                    bx = tx if anchor == "start" else tx - 13
                    a(f'<rect x="{bx}" y="{y-12:.1f}" width="13" height="13" fill="#000"/>')
                    tx = tx + 22 if anchor == "start" else tx - 22
                for i, ln in enumerate(lines):
                    text(tx, y + i * 22, ln, anchor=anchor)
                fx, sh = (xcol - 10, -30) if anchor == "start" else (xcol + 10, 30)
                st = ' stroke-dasharray="11 7"' if n["dash"] else ''
                a(f'<path d="M{fx:.1f},{y-7:.1f} L{fx+sh:.1f},{y-7:.1f} L{X2:.1f},{Y2:.1f}" class="lead"{st} marker-end="url(#arw)"/>')
                y += len(lines) * 22 + 16
            bottom = max(bottom, y)

        # title bubble under the drawing
        ty = bottom + 90
        tx0 = self.ox
        a(f'<circle cx="{tx0+40:.1f}" cy="{ty:.1f}" r="38" fill="none" stroke="#000" stroke-width="1.8"/>')
        a(f'<path d="M{tx0+2:.1f},{ty:.1f} l76,0" class="thin"/>')
        text(tx0 + 40, ty - 8, self.number, cls="tag", anchor="middle")
        text(tx0 + 40, ty + 28, self.sheet, anchor="middle")
        text(tx0 + 100, ty + 6, self.title, cls="ttl")
        a(f'<path d="M{tx0+100:.1f},{ty+20:.1f} L{max(tx0+100+17*len(self.title), tx0+500):.1f},{ty+20:.1f}" class="med"/>')
        text(tx0 + 100, ty + 50, "SCALE   " + self.scale_label, cls="sc")
        y = ty + 110

        # boxes below: keynotes, general notes, verify
        def box(title, rows, numbered, marker="—"):
            nonlocal y
            if not rows:
                return
            wrap = max(60, int((W - 160) / 11))
            lines_total = sum(len(textwrap.wrap(r, width=wrap)) for r in rows)
            h = 70 + lines_total * 22 + len(rows) * 10
            a(f'<rect x="60" y="{y}" width="{W-120}" height="{h}" fill="none" stroke="#000" stroke-width="1.8"/>')
            text(80, y + 36, title, cls="h3")
            a(f'<path d="M80,{y+50} L{W-80},{y+50}" class="thin"/>')
            yy = y + 80
            for i, r in enumerate(rows, 1):
                if isinstance(r, tuple):
                    key, r = r
                else:
                    key = f"{i}." if numbered else marker
                for j, ln in enumerate(textwrap.wrap(r, width=wrap)):
                    if j == 0:
                        text(82, yy, key, cls="kn" if not numbered and key != marker else "n")
                    text(122, yy + j * 22, ln)
                yy += len(textwrap.wrap(r, width=wrap)) * 22 + 10
            y += h + 30

        box("KEYNOTES", [(k["key"], k["text"]) for k in sorted(self.keynotes, key=lambda k: k["key"])], False)
        box(f"GENERAL NOTES - {self.number}/{self.sheet}", self.general, True)
        box("VERIFY / COORDINATE BEFORE ISSUE", self.verify_items, False)

        H = int(y + 30)
        head = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
                f"<defs><style>{STYLE}</style>{DEFS}</defs>",
                f'<rect width="{W}" height="{H}" fill="#fff"/>',
                f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#000" stroke-width="2"/>']
        hdr = f"DETAIL {self.number} / {self.sheet}  —  {self.title}"
        head.append(f'<text x="60" y="92" class="h1">{esc(hdr)}</text>')
        sub = "  ·  ".join(s for s in (self.project, (self.jurisdiction or "").upper(), self.scale_label) if s)
        head.append(f'<text x="60" y="130" class="sc">{esc(sub)}</text>')
        head.append(f'<path d="M60,150 L{W-60},150" class="med"/>')
        return "\n".join(head + o + ["</svg>"]), W, H

    # ---------------------------------------------------------- output
    def notes_text(self):
        """The notes as they go on the sheet, in the office's plain-text format."""
        L = [f"{self.title}  -  {self.number}/{self.sheet}", f"SCALE {self.scale_label}", ""]
        if self.tags:
            L.append("ASSEMBLIES (SEE ASSEMBLY SCHEDULE - NOT REPEATED IN THESE NOTES)")
            for t in sorted({t["label"] for t in self.tags}):
                L.append(f"    {t}")
            L.append("")
        if self.notes:
            L.append("LEADER NOTES")
            for n in self.notes:
                body = textwrap.wrap(n["text"], width=86)
                L.append(("  # " if n["flag"] else "    ") + body[0])
                L += ["    " + b for b in body[1:]]
            L.append("")
        if self.keynotes:
            L.append("KEYNOTES")
            for k in sorted(self.keynotes, key=lambda k: k["key"]):
                body = textwrap.wrap(k["text"], width=84)
                L.append(f"{k['key']}.  {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        if self.general:
            L.append("GENERAL NOTES")
            for i, g in enumerate(self.general, 1):
                body = textwrap.wrap(g, width=84)
                L.append(f"{i}.{' ' if i > 9 else '  '} {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        if self.verify_items:
            L.append("VERIFY / COORDINATE BEFORE ISSUE")
            for v in self.verify_items:
                body = textwrap.wrap(v, width=84)
                L.append(f"-   {body[0]}"); L += ["    " + b for b in body[1:]]
            L.append("")
        L.append("#  = ITEM NOT IN ANY ASSEMBLY - BUILD EXACTLY AS NOTED.")
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

    def save(self, outdir, assemblies=None, png=True, check=True):
        os.makedirs(outdir, exist_ok=True)
        num = self.number.zfill(2) if self.number.isdigit() else self.number
        base = os.path.join(outdir, f"{num}-{self.sheet}-{self.slug}")
        svg, W, H = self._render()
        with open(base + ".svg", "w") as f:
            f.write(svg)
        with open(base + ".notes.txt", "w") as f:
            f.write(self.notes_text())
        with open(base + ".json", "w") as f:
            json.dump(self.manifest(), f, indent=1)
        print("wrote", base + ".svg")
        if png:
            render_png(base + ".svg", base + ".png", W, H)
        status = 0
        if check:
            here = os.path.dirname(os.path.abspath(__file__))
            cmd = [sys.executable, os.path.join(here, "check_notes.py"), base + ".json"]
            if assemblies:
                cmd += ["--assemblies", assemblies]
            status = subprocess.call(cmd)
        return status


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
    html = f'<html><body style="margin:0"><img src="file://{os.path.abspath(svg_path)}" width="{W}" height="{H}"></body></html>'
    with tempfile.TemporaryDirectory() as td:
        page = os.path.join(td, "p.html")
        with open(page, "w") as f:
            f.write(html)
        r = subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                            "--allow-file-access-from-files", f"--window-size={W},{H + 160}",
                            f"--screenshot={os.path.abspath(png_path)}", "file://" + page],
                           capture_output=True, text=True, timeout=120)
    if os.path.exists(png_path):
        print("wrote", png_path)
    else:
        print("PNG render failed:", r.stderr.strip()[-400:])
