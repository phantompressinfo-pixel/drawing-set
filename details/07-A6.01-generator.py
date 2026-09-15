# -*- coding: utf-8 -*-
"""100% CD mark-up of detail 7/A6.01 - GREEN ROOF EDGE AT FOUNDATION WALL."""
import textwrap, math

W, H = 2700, 1960
out = []
a = out.append

# ------------------------------------------------------------------ geometry (8px = 1")
S = 8.0
xL, xDrain, xIns, xProt = 1040, 1122, 1134, 1168
xW0, xW1, xIns2, xGyp   = 1180, 1276, 1316, 1326
xEdge, xR               = 1266, 1720
yVeg, yGrade, yFab, yDrn = 340, 440, 536, 560
yIns, yProt, yMem, ySlabB = 600, 610, 622, 702
yClg, yBrk = 904, 1240

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text(x, y, s, cls="n", anchor="start", halo=False):
    h = ' style="paint-order:stroke;stroke:#fff;stroke-width:6;stroke-linejoin:round"' if halo else ''
    a(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{h}>{esc(s)}</text>')

class Col:
    """Auto-stacking note column."""
    def __init__(self, x, y, anchor, wrap, gap=26):
        self.x, self.y, self.anchor, self.wrap, self.gap = x, y, anchor, wrap, gap
    def skip(self, d): self.y += d
    def note(self, body, target=None, flag=False, dash=False):
        lines = textwrap.wrap(body, width=self.wrap)
        y0 = self.y
        tx = self.x
        if flag:
            sq = 13
            bx = tx if self.anchor == "start" else tx - sq
            a(f'<rect x="{bx}" y="{y0-12}" width="{sq}" height="{sq}" fill="#000"/>')
            tx = tx + 22 if self.anchor == "start" else tx - 22
        for i, ln in enumerate(lines):
            text(tx, y0 + i*22, ln, anchor=self.anchor)
        if target:
            if self.anchor == "start":
                fx, sh = self.x - 10, -44
            else:
                fx, sh = self.x + 10, 44
            d = f'M{fx},{y0-7} L{fx+sh},{y0-7} L{target[0]},{target[1]}'
            st = ' stroke-dasharray="11 7"' if dash else ''
            a(f'<path d="{d}" class="lead"{st} marker-end="url(#arw)"/>')
        self.y = y0 + len(lines)*22 + self.gap
        return y0

def zig_h(x0, x1, y, amp=15, seg=50):
    p, x, up = [f'M{x0},{y}'], x0+seg, True
    while x < x1-seg:
        p.append(f'L{x},{y+(-amp if up else amp)}'); up = not up; x += seg
    p.append(f'L{x1},{y}'); return " ".join(p)

def zig_v(x, y0, y1, amp=15, seg=50):
    p, y, r = [f'M{x},{y0}'], y0+seg, True
    while y < y1-seg:
        p.append(f'L{x+(amp if r else -amp)},{y}'); r = not r; y += seg
    p.append(f'L{x},{y1}'); return " ".join(p)

def tag(x, y, label, w=58, h=38):
    a(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="#fff" stroke="#000" stroke-width="1.8"/>')
    text(x, y+8, label, cls="tag", anchor="middle")

def vdim(x, y0, y1, label):
    a(f'<path d="M{x},{y0} L{x},{y1}" class="dim" marker-start="url(#tick)" marker-end="url(#tick)"/>')
    a(f'<path d="M{x-11},{y0} L{x+11},{y0} M{x-11},{y1} L{x+11},{y1}" class="dim"/>')
    a(f'<g transform="translate({x-7},{(y0+y1)/2}) rotate(-90)">')
    text(0, 0, label, cls="dimt", anchor="middle", halo=True); a('</g>')

def hdim(y, x0, x1, label):
    a(f'<path d="M{x0},{y} L{x1},{y}" class="dim" marker-start="url(#tick)" marker-end="url(#tick)"/>')
    a(f'<path d="M{x0},{y-11} L{x0},{y+11} M{x1},{y-11} L{x1},{y+11}" class="dim"/>')
    text((x0+x1)/2, y-10, label, cls="dimt", anchor="middle", halo=True)

def elev(x, y, label):
    a(f'<path d="M{x},{y} l-13,-11 l26,0 z" fill="#000"/>')
    text(x+20, y-8, label, cls="dimt", anchor="start", halo=True)

# ------------------------------------------------------------------ defs
a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
a('''<defs>
<style>
 text{font-family:Arial,Helvetica,sans-serif;fill:#000}
 .n{font-size:17.5px}
 .tag{font-size:21px;font-weight:bold}
 .dimt{font-size:16px;font-weight:bold}
 .h1{font-size:38px;font-weight:bold;letter-spacing:1px}
 .h2{font-size:19px}
 .h3{font-size:20px;font-weight:bold;letter-spacing:.6px}
 .ttl{font-size:40px;fill:#555;letter-spacing:1px}
 .ttl2{font-size:31px;fill:#555;letter-spacing:1px}
 .sc{font-size:20px;fill:#555}
 .lead{fill:none;stroke:#000;stroke-width:1.2}
 .thin{fill:none;stroke:#000;stroke-width:1.0}
 .med{fill:none;stroke:#000;stroke-width:1.8}
 .hvy{fill:none;stroke:#000;stroke-width:5}
 .dim{fill:none;stroke:#000;stroke-width:1.1}
</style>
<marker id="arw" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
 <path d="M0,1 L12,6 L0,11 z" fill="#000"/></marker>
<marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9" orient="auto">
 <path d="M1,9 L9,1" stroke="#000" stroke-width="2"/></marker>
<pattern id="earth" width="40" height="40" patternUnits="userSpaceOnUse">
 <path d="M0,12 L12,0 M0,34 L34,0 M14,40 L40,14 M34,40 L40,34" stroke="#000" stroke-width="0.9" fill="none"/>
 <circle cx="24" cy="22" r="1.5"/><circle cx="8" cy="30" r="1.3"/></pattern>
<pattern id="conc" width="36" height="36" patternUnits="userSpaceOnUse">
 <circle cx="6" cy="8" r="1.7"/><circle cx="21" cy="5" r="1.4"/><circle cx="29" cy="19" r="1.7"/>
 <circle cx="11" cy="26" r="1.4"/><circle cx="24" cy="31" r="1.6"/><circle cx="15" cy="15" r="1.3"/>
 <path d="M31,7 l4,2 l-3,2 z"/><path d="M4,20 l4,2 l-3,2 z"/><path d="M18,33 l4,2 l-3,2 z"/></pattern>
<pattern id="insul" width="20" height="20" patternUnits="userSpaceOnUse">
 <path d="M10,4 L10,16 M4,10 L16,10" stroke="#000" stroke-width="0.9" fill="none"/></pattern>
<pattern id="gravel" width="34" height="34" patternUnits="userSpaceOnUse">
 <circle cx="8" cy="9" r="4.5" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="24" cy="6" r="3.4" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="28" cy="21" r="4.8" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="12" cy="24" r="3.8" fill="none" stroke="#000" stroke-width="1"/>
 <circle cx="19" cy="14" r="2.6" fill="none" stroke="#000" stroke-width="1"/></pattern>
<pattern id="media" width="26" height="26" patternUnits="userSpaceOnUse">
 <circle cx="5" cy="6" r="1.7"/><circle cx="17" cy="3" r="1.3"/><circle cx="22" cy="15" r="1.8"/>
 <circle cx="9" cy="19" r="1.4"/><circle cx="14" cy="11" r="1.2"/><circle cx="2" cy="22" r="1.5"/>
 <path d="M18,21 l5,3 M6,12 l4,-2" stroke="#000" stroke-width="1" fill="none"/></pattern>
<pattern id="drain" width="24" height="24" patternUnits="userSpaceOnUse">
 <path d="M0,18 q6,-14 12,0 q6,14 12,0" stroke="#000" stroke-width="1.1" fill="none"/></pattern>
<pattern id="drainv" width="24" height="24" patternUnits="userSpaceOnUse" patternTransform="rotate(90)">
 <path d="M0,18 q6,-14 12,0 q6,14 12,0" stroke="#000" stroke-width="1.1" fill="none"/></pattern>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a(f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#000" stroke-width="2"/>')

# ------------------------------------------------------------------ sheet header
text(60, 88, "DETAIL 7 / A6.01  —  GREEN ROOF EDGE AT FOUNDATION WALL", cls="h1")
text(60, 122, "100% CD MARK-UP  —  NOTES TO ADD (TEXT AS SHOWN) + DRAWING ELEMENTS TO ADD", cls="h2")
a('<rect x="60" y="142" width="15" height="15" fill="#000"/>')
text(86, 156, "= DRAWING ELEMENT MISSING FROM THE CURRENT DETAIL — DRAW IT, THEN NOTE IT.", cls="h2")
a(f'<path d="M60,176 L{W-60},176" class="med"/>')

# ================================================================== DRAWING
# earth backfill
a(f'<path d="M{xL},472 L{xDrain},{yGrade} L{xDrain},{yBrk} L{xL},{yBrk} z" fill="url(#earth)"/>')
a(f'<path d="M{xL},472 L{xDrain},{yGrade}" class="med"/>')
a(f'<path d="M{xL+30},452 l0,22 m-9,-9 l9,9 l9,-9" class="thin"/>')   # slope arrow
# vertical drainage composite
a(f'<rect x="{xDrain}" y="{yFab}" width="{xIns-xDrain}" height="{yBrk-yFab}" fill="url(#drainv)" stroke="#000" stroke-width="1"/>')
# vertical rigid insulation
a(f'<rect x="{xIns}" y="{yProt}" width="{xProt-xIns}" height="{yBrk-yProt}" fill="url(#insul)" stroke="#000" stroke-width="1.2"/>')
a(f'<path d="M{xIns},814 L{xProt},814" class="thin" stroke-dasharray="10 6"/>')
# protection board on wall face
a(f'<rect x="{xProt}" y="{yMem}" width="{xW0-xProt}" height="{yBrk-yMem}" fill="none" stroke="#000" stroke-width="1"/>')
# concrete wall + deck
a(f'<path d="M{xW0},{yMem} L{xR},{yMem} L{xR},{ySlabB} L{xW1},{ySlabB} L{xW1},{yBrk} L{xW0},{yBrk} z" fill="url(#conc)" stroke="#000" stroke-width="1.8"/>')
a(f'<path d="M{xW1},{yMem} L{xW1},{ySlabB}" class="thin" stroke-dasharray="14 8"/>')
# construction joint + waterstop
a(f'<path d="M{xW0},1060 L{xW1},1060" class="med"/>')
a(f'<rect x="{xW0+28}" y="1049" width="36" height="22" fill="#fff" stroke="#000" stroke-width="1.6"/>')
a(f'<path d="M{xW0+28},1049 L{xW0+64},1071 M{xW0+64},1049 L{xW0+28},1071" class="thin"/>')
# membrane over deck / over wall / down face
a(f'<path d="M{xR},{yMem} L{xW0},{yMem} L{xW0},{yBrk}" class="hvy"/>')
a(f'<path d="M{xR},{yProt} L{xW0-6},{yProt}" class="thin"/>')
a(f'<path d="M{xR},{yProt-8} L{xW0-6},{yProt-8}" class="thin" stroke-dasharray="6 5"/>')
# insulation over deck
a(f'<rect x="{xIns}" y="{yDrn}" width="{xR-xIns}" height="{yIns-yDrn}" fill="url(#insul)" stroke="#000" stroke-width="1.2"/>')
# drainage / retention course
a(f'<rect x="{xDrain}" y="{yFab}" width="{xR-xDrain}" height="{yDrn-yFab}" fill="url(#drain)" stroke="#000" stroke-width="1"/>')
# filter fabric + turn-up
a(f'<path d="M{xR},{yFab} L{xDrain},{yFab} L{xDrain},{yGrade+18}" class="med"/>')
# gravel strip / growing medium
a(f'<rect x="{xDrain}" y="{yGrade}" width="{xEdge-xDrain}" height="{yFab-yGrade}" fill="url(#gravel)"/>')
a(f'<rect x="{xEdge}" y="{yGrade}" width="{xR-xEdge}" height="{yFab-yGrade}" fill="url(#media)"/>')
a(f'<path d="M{xEdge},{yGrade} L{xR},{yGrade}" class="med"/>')
# edge restraint
a(f'<path d="M{xEdge},{yGrade-28} L{xEdge},{yFab}" class="hvy"/>')
for yy in range(yGrade+10, yFab-4, 22):
    a(f'<circle cx="{xEdge}" cy="{yy}" r="4" fill="#fff" stroke="#000" stroke-width="1.4"/>')
# slope arrow on deck
a(f'<path d="M1330,{yMem-1} l130,0 m-16,-8 l16,8 l-16,8" class="thin"/>')
text(1330, yMem-12, 'SLOPE TO DRAIN', cls="dimt", halo=True)
# roof drain + inspection chamber beyond (dashed)
a(f'<g class="thin" stroke-dasharray="12 8" fill="none">')
a(f'<rect x="1478" y="{yGrade+16}" width="92" height="{yMem-yGrade-16}" stroke="#000" fill="#fff" fill-opacity="0.45" stroke-width="1.5"/>')
a(f'<path d="M1478,{yFab} L1570,{yFab} M1500,{yMem} l24,-22 l24,22" stroke="#000"/>')
a('</g>')
# vegetation
def shrub(x, y, s=1.0):
    a(f'<path d="M{x},{y} L{x},{y-42*s}" class="thin"/>')
    for ang in (-55,-25,25,55):
        r = math.radians(ang)
        a(f'<path d="M{x},{y-15*s} q{math.sin(r)*22*s},{-18*s} {math.sin(r)*34*s},{-34*s}" class="thin"/>')
def grass(x, y, s=1.0):
    for dx, cx in ((-16,-26),(-6,-10),(6,10),(16,26)):
        a(f'<path d="M{x},{y} q{dx*s},{-26*s} {cx*s},{-46*s}" class="thin"/>')
shrub(1410, yGrade, 1.1); grass(1630, yGrade); shrub(1690, yGrade, .9)
# interior insulation / gyp / ceiling
a(f'<rect x="{xW1}" y="{ySlabB}" width="{xIns2-xW1}" height="{yBrk-ySlabB}" fill="url(#insul)" stroke="#000" stroke-width="1.2"/>')
a(f'<path d="M{xGyp},{ySlabB} L{xGyp},{yBrk}" class="med"/>')
a(f'<rect x="{xGyp}" y="{yClg}" width="{xR-xGyp}" height="20" fill="#fff" stroke="#000" stroke-width="1.6"/>')
a(f'<path d="M{xGyp},{yClg-7} L{xR},{yClg-7}" class="thin" stroke-dasharray="12 7"/>')
a(f'<rect x="{xGyp}" y="{yClg}" width="17" height="20" fill="#fff" stroke="#000" stroke-width="1.4"/>')
a(f'<path d="M{xGyp},{yClg} L{xGyp+17},{yClg+20} M{xGyp+17},{yClg} L{xGyp},{yClg+20}" class="thin"/>')
# break lines
a(f'<path d="{zig_v(xR, yVeg-30, yBrk)}" class="med"/>')
a(f'<path d="{zig_h(xL, xR, yBrk)}" class="med"/>')
a(f'<path d="M{xL},{yVeg+20} L{xL},{yBrk}" class="thin"/>')
# EXT / INT
for x, lbl in ((1090, "EXT."), (1500, "INT.")):
    a(f'<rect x="{x-52}" y="{yBrk+40}" width="104" height="48" fill="#fff" stroke="#000" stroke-width="1.8"/>')
    text(x, yBrk+73, lbl, cls="tag", anchor="middle")
# tags
tag(1450, 300, "R3"); a(f'<path d="M1450,319 L1450,{yMem}" class="med"/>')
tag(1470, 1030, "C1"); a(f'<path d="M1470,1011 L1470,{yClg+20}" class="med"/>')
tag(985, 1150, "W-?"); a(f'<path d="M1014,1150 L{xIns+10},1150" class="med"/>')
# dims + elevations
vdim(1692, yGrade, yFab, '1\'-0" MIN.')
hdim(400, xDrain, xEdge, '1\'-6" MIN.')
elev(1300, yGrade, 'FIN. GRADE / T.O. MEDIA  EL. = ___')
elev(1600, yMem, 'T.O. STRUCT. SLAB  EL. = ___')

# ================================================================== NOTES
# --- top row
for x, body, tgt, fl in (
    (1046, "GRAVEL MAINTENANCE / VEGETATION-FREE STRIP, 1'-6\" MIN. WIDE — WASHED ROUNDED STONE, 1/2\"–1\" DIA., OVER FILTER FABRIC.", (1180, 482), True),
    (1700, "EDGE RESTRAINT — PERFORATED ALUM. OR STAINLESS, SET ON PROTECTION LAYER. NO FASTENERS THROUGH MEMBRANE.", (xEdge+5, yGrade+14), True),
    (2180, "ROOF DRAIN + OVERFLOW BEYOND, W/ DRAIN INSPECTION CHAMBER — SEE PLUMBING AND ROOF PLAN.", (1572, yGrade+50), True)):
    c = Col(x, 232, "start", 40); c.note(body, target=tgt, flag=fl, dash=(x == 2180))

# --- left column (exterior / below grade), top-to-bottom = target order
LC = Col(940, 372, "end", 54)
LC.note("FINISH GRADE — SLOPE AWAY FROM BUILDING 5% MIN. FOR 10'-0\". SEE CIVIL DRAWINGS FOR GRADING.", (1058, 466))
LC.note("SOIL BACKFILL AND COMPACTION PER GEOTECHNICAL REPORT. DO NOT BACKFILL UNTIL DECK HAS CURED AND IS BRACED / SHORED PER STRUCTURAL.", (1062, 640))
LC.note("PREFABRICATED DRAINAGE COMPOSITE W/ INTEGRAL FILTER FABRIC — CONTINUOUS FROM ROOF DRAINAGE COURSE TO FOOTING DRAIN, NO BREAK AT TRANSITION.", (xDrain+6, 780), flag=True)
LC.note("RIGID INSULATION (XPS) CONTINUOUS DOWN EXTERIOR FACE OF FOUNDATION WALL — EXTEND 2'-0\" MIN. BELOW DECK TO LAP INTERIOR INSULATION AND CLOSE THE THERMAL BRIDGE AT THE SLAB EDGE.", (xIns+16, 890), flag=True)
LC.note("BELOW-GRADE WATERPROOFING — SAME MFR. / SYSTEM AS ROOF MEMBRANE, CONTINUOUS OVER TOP OF WALL AND DOWN FACE. 2-PLY REINFORCING AT ALL CORNERS AND TRANSITIONS.", (xW0-3, 980), flag=True)
LC.note("WATERSTOP AT HORIZONTAL CONSTRUCTION JOINT — SEE STRUCTURAL AND WATERPROOFING MFR.", (xW0+46, 1060), flag=True)
LC.note("CONCRETE FOUNDATION WALL — SEE STRUCTURAL FOR THICKNESS, REINFORCING AND JOINT LOCATIONS.", (1235, 1140))
LC.note("FOOTING, FOUNDATION DRAIN, FILTER FABRIC AND WASHED GRAVEL BELOW — SEE CIVIL. ADD CROSS-REFERENCE TO FOUNDATION DETAIL.", (1080, yBrk-12), flag=True)
LC.note("BELOW-GRADE WALL ASSEMBLY TAG — ADD SEPARATE 'W-__' TAG FOR THE VERTICAL CONDITION; R3 (ROOF) SHOULD NOT CARRY THE WALL ASSEMBLY.", flag=True)

# --- right column A: roof assembly, top-to-bottom
RC = Col(1860, 372, "start", 50)
RC.note("PLANTINGS AND IRRIGATION — SEE LANDSCAPE DRAWINGS.", (1700, 386))
RC.note("GROWING MEDIUM — DEPTH, MIX AND SATURATED UNIT WEIGHT PER LANDSCAPE. CONFIRM LOADING W/ STRUCTURAL.", (1704, 490))
RC.note("FILTER FABRIC — LAP 6\" MIN. AT SEAMS; TURN UP AT EDGE RESTRAINT AND AT BACKFILL INTERFACE.", (1706, yFab), flag=True)
RC.note("DRAINAGE / RETENTION / AERATION COURSE — MAINTAIN CONTINUOUS PATH TO ROOF DRAIN.", (1708, yFab+13), flag=True)
RC.note("RIGID INSULATION, XPS — R-__ MIN. PER ENERGY CODE. LOOSE-LAID, JOINTS STAGGERED (INVERTED / PROTECTED MEMBRANE ASSEMBLY).", (1710, yDrn+20))
RC.note("PROTECTION COURSE / SEPARATION SHEET OVER MEMBRANE.", (1712, yProt-3), flag=True)
RC.note("ROOT BARRIER BY MEMBRANE MFR. — CONTINUOUS, UP AND OVER TOP OF WALL.", (1713, yProt-10), flag=True)
RC.note("ROOFING / WATERPROOFING MEMBRANE — HOT FLUID-APPLIED REINFORCED, FULLY ADHERED. FLOOD TEST AND ELECTRONIC LEAK DETECTION PRIOR TO OVERBURDEN.", (1714, yMem-3))
RC.note("STRUCTURAL CONCRETE DECK — SLOPE 1/4\" PER FT. MIN. TO DRAIN (OR LEVEL DECK W/ TAPERED DRAINAGE COURSE — VERIFY). SEE STRUCTURAL.", (1700, 670))
RC.skip(16)
RC.note("AIR / VAPOR BARRIER CONTINUITY — TRANSITION MEMBRANE FROM ROOF MEMBRANE TO BELOW-GRADE WATERPROOFING. SEAL ALL LAPS.", (1300, 722), flag=True)
RC.note("SEALANT AND FIRE-SAFING AT CEILING-TO-WALL JOINT.", (1345, yClg+10), flag=True)
RC.note("CONTINUOUS RIGID INSULATION AT INTERIOR FACE OF FOUNDATION WALL — LAP EXTERIOR INSULATION 2'-0\" MIN.", (1300, 1020))
RC.note("GYPSUM BOARD / INTERIOR FINISH — SEE FINISH SCHEDULE.", (1330, 1140))

# ------------------------------------------------------------------ general notes
gx, gy, gw, gh = 60, 1330, 930, 560
a(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="#000" stroke-width="1.8"/>')
text(gx+20, gy+38, "GENERAL NOTES — THIS DETAIL", cls="h3")
a(f'<path d="M{gx+20},{gy+52} L{gx+gw-20},{gy+52}" class="thin"/>')
GN = [
 "VEGETATED ROOF ASSEMBLY TO COMPLY W/ IBC 1507.16 AND IFC 317 — PROVIDE VEGETATION-FREE ZONES AT PERIMETER, PENETRATIONS AND DRAINS. CLASS 'A' ASSEMBLY.",
 "ALL VEGETATED ROOF COMPONENTS (MEMBRANE, ROOT BARRIER, PROTECTION, DRAINAGE, FILTER FABRIC) FROM A SINGLE SOURCE MFR. UNDER ONE 20-YEAR NDL WARRANTY.",
 "24-HOUR FLOOD TEST PER ASTM D5957 AND ELECTRONIC LEAK DETECTION PER ASTM D7877 PRIOR TO PLACING ANY OVERBURDEN.",
 "DO NOT PLACE OVERBURDEN UNTIL MEMBRANE IS INSPECTED AND ACCEPTED BY MFR'S REPRESENTATIVE; SUBMIT INSPECTION REPORT.",
 "NO PENETRATIONS OR MECHANICAL FASTENERS THROUGH WATERPROOFING MEMBRANE.",
 "SATURATED WEIGHT OF COMPLETE ASSEMBLY = ___ PSF; VERIFY W/ STRUCTURAL BEFORE ORDERING MATERIALS.",
 "COORDINATE IRRIGATION SLEEVES, LEAK-DETECTION GRID AND ELECTRICAL W/ LANDSCAPE, PLUMBING AND ELECTRICAL.",
 "PROVIDE 4'-0\" LONG MOCK-UP OF THIS EDGE CONDITION FOR REVIEW PRIOR TO PROCEEDING.",
 "PROTECT COMPLETED MEMBRANE FROM CONSTRUCTION TRAFFIC W/ TEMPORARY PROTECTION BOARD.",
]
yy = gy + 84
for i, g in enumerate(GN, 1):
    lines = textwrap.wrap(g, width=84)
    text(gx+22, yy, f"{i}.")
    for j, ln in enumerate(lines): text(gx+54, yy+j*22, ln)
    yy += len(lines)*22 + 12

# ------------------------------------------------------------------ verify box
vx, vy, vw, vh = 1860, 1560, 780, 330
a(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="none" stroke="#000" stroke-width="1.8"/>')
text(vx+20, vy+38, "VERIFY / COORDINATE BEFORE ISSUE", cls="h3")
a(f'<path d="M{vx+20},{vy+52} L{vx+vw-20},{vy+52}" class="thin"/>')
VB = [
 "MEMBRANE TYPE + SPEC SECTION NUMBER",
 "R-VALUE AND ENERGY-CODE COMPLIANCE PATH AT SLAB EDGE",
 "INTENSIVE VS. EXTENSIVE — MEDIA DEPTH AND DEAD LOAD",
 "SOIL RETENTION AT BACKFILL / GRAVEL INTERFACE",
 "DRAIN + OVERFLOW LOCATIONS SHOWN ON ROOF PLAN",
 "R3 / C1 TAGS AGREE W/ ASSEMBLY SCHEDULE",
]
yy = vy + 86
for v in VB:
    lines = textwrap.wrap(v, width=52)
    for j, ln in enumerate(lines): text(vx+24, yy+j*22, ("—  " if j == 0 else "    ") + ln)
    yy += len(lines)*22 + 10

# ------------------------------------------------------------------ title block
a('<path d="M1046,1700 L1800,1700" class="med"/>')
a('<circle cx="1096" cy="1654" r="35" fill="none" stroke="#000" stroke-width="1.8"/>')
a('<path d="M1061,1654 L1131,1654" class="thin"/>')
text(1096, 1650, "7", cls="tag", anchor="middle")
text(1096, 1684, "A6.01", anchor="middle")
text(1160, 1672, "GREEN ROOF EDGE AT FOUNDATION WALL", cls="ttl2")
text(1164, 1728, 'SCALE   1" = 1\'-0"', cls="sc")
a('</svg>')

open("/home/user/drawing-set/details/07-A6.01-green-roof-edge-at-foundation-wall.svg","w").write("\n".join(out))
print("ok")
