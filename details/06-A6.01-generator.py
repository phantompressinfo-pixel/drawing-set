# -*- coding: utf-8 -*-
"""100% CD mark-up of detail 6/A6.01 - STONE WALL TRANSITION TO METAL STANDING SEAM ROOF."""
import textwrap

W, H = 2700, 2260
out = []
a = out.append

# ---------------------------------------------------- geometry (14px = 1")
xBrkL   = 760
xStoneO = 1180; xStoneI = 1236            # 4" stone
xCavI   = 1250                            # 1" drainage cavity
xCIi    = 1292                            # 3" cont. insulation / face of concrete
xConcI  = 1460                            # 12" concrete wall
xBrkR   = 1500
yTopBrk = 300
yStoneB = 942                             # bottom of stone
yShelf  = 948                             # top of shelf angle leg
yBFtop  = 1068                            # top of base flashing turn-up (8" above roof)
yCFbot  = 1124                            # bottom of counterflashing (4" lap)
yPanel  = 1180                            # top of metal panel
yUL     = 1188; ySlip = 1196; yCBb = 1206 # underlayment / slip sheet / cover bd
yInsB   = 1288; yAVB = 1290
yDeckT  = 1292; yDeckB = 1420; yBotBrk = 1460

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text(x, y, s, cls="n", anchor="start", halo=False):
    h = ' style="paint-order:stroke;stroke:#fff;stroke-width:6;stroke-linejoin:round"' if halo else ''
    a(f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}"{h}>{esc(s)}</text>')

class Col:
    def __init__(self, x, y, anchor, wrap, gap=22):
        self.x, self.y, self.anchor, self.wrap, self.gap = x, y, anchor, wrap, gap
    def skip(self, d): self.y += d
    def note(self, body, target=None, flag=False, dash=False):
        lines = textwrap.wrap(body, width=self.wrap); y0 = self.y; tx = self.x
        if flag:
            bx = tx if self.anchor == "start" else tx-13
            a(f'<rect x="{bx}" y="{y0-12}" width="13" height="13" fill="#000"/>')
            tx = tx+22 if self.anchor == "start" else tx-22
        for i, ln in enumerate(lines): text(tx, y0+i*22, ln, anchor=self.anchor)
        if target:
            fx, sh = (self.x-10, -44) if self.anchor == "start" else (self.x+10, 44)
            st = ' stroke-dasharray="11 7"' if dash else ''
            a(f'<path d="M{fx},{y0-7} L{fx+sh},{y0-7} L{target[0]},{target[1]}" class="lead"{st} marker-end="url(#arw)"/>')
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

def tag(x, y, label, w=64, h=38):
    a(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" fill="#fff" stroke="#000" stroke-width="1.8"/>')
    text(x, y+8, label, cls="tag", anchor="middle")

def vdim(x, y0, y1, label):
    a(f'<path d="M{x},{y0} L{x},{y1}" class="dim" marker-start="url(#tick)" marker-end="url(#tick)"/>')
    a(f'<path d="M{x-11},{y0} L{x+11},{y0} M{x-11},{y1} L{x+11},{y1}" class="dim"/>')
    a(f'<g transform="translate({x-7},{(y0+y1)/2}) rotate(-90)">'); text(0,0,label,cls="dimt",anchor="middle",halo=True); a('</g>')

def elev(x, y, label):
    a(f'<path d="M{x},{y} l-13,-11 l26,0 z" fill="#000"/>')
    text(x+20, y-8, label, cls="dimt", halo=True)

# ---------------------------------------------------- defs
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
 .ttl2{font-size:31px;fill:#555;letter-spacing:1px}
 .sc{font-size:20px;fill:#555}
 .lead{fill:none;stroke:#000;stroke-width:1.2}
 .thin{fill:none;stroke:#000;stroke-width:1.0}
 .med{fill:none;stroke:#000;stroke-width:1.8}
 .mtl{fill:none;stroke:#000;stroke-width:4;stroke-linejoin:miter}
 .mem{fill:none;stroke:#000;stroke-width:3}
 .dim{fill:none;stroke:#000;stroke-width:1.1}
</style>
<marker id="arw" viewBox="0 0 12 12" refX="11" refY="6" markerWidth="11" markerHeight="11" orient="auto-start-reverse">
 <path d="M0,1 L12,6 L0,11 z" fill="#000"/></marker>
<marker id="tick" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="9" markerHeight="9" orient="auto">
 <path d="M1,9 L9,1" stroke="#000" stroke-width="2"/></marker>
<pattern id="conc" width="52" height="52" patternUnits="userSpaceOnUse">
 <path d="M12,8 l0,10 M7,13 l10,0 M38,30 l0,10 M33,35 l10,0" stroke="#000" stroke-width="1.1" fill="none"/>
 <circle cx="30" cy="12" r="1.8"/><circle cx="8" cy="36" r="1.6"/><circle cx="45" cy="6" r="1.5"/>
 <circle cx="22" cy="45" r="1.7"/><circle cx="44" cy="47" r="1.4"/>
 <path d="M26,25 l5,3 l-4,3 z"/></pattern>
<pattern id="insul" width="14" height="14" patternUnits="userSpaceOnUse">
 <path d="M0,0 L14,0 M0,0 L0,14" stroke="#000" stroke-width="0.8" fill="none"/></pattern>
<pattern id="stone" width="16" height="16" patternUnits="userSpaceOnUse">
 <path d="M0,16 L16,0 M-4,4 L4,-4 M12,20 L20,12" stroke="#000" stroke-width="0.9" fill="none"/></pattern>
<pattern id="mortarnet" width="12" height="12" patternUnits="userSpaceOnUse">
 <circle cx="3" cy="3" r="1.4"/><circle cx="9" cy="9" r="1.4"/></pattern>
</defs>''')
a(f'<rect width="{W}" height="{H}" fill="#fff"/>')
a(f'<rect x="22" y="22" width="{W-44}" height="{H-44}" fill="none" stroke="#000" stroke-width="2"/>')

# ---------------------------------------------------- header
text(60, 88, "DETAIL 6 / A6.01  —  STONE WALL TRANSITION TO METAL STANDING SEAM ROOF", cls="h1")
text(60, 122, "100% CD MARK-UP  —  NOTES TO ADD (TEXT AS SHOWN) + DRAWING ELEMENTS TO ADD", cls="h2")
a('<rect x="60" y="142" width="15" height="15" fill="#000"/>')
text(86, 156, "= DRAWING ELEMENT MISSING FROM THE CURRENT DETAIL — DRAW IT, THEN NOTE IT.", cls="h2")
a(f'<path d="M60,176 L{W-60},176" class="med"/>')

# ==================================================== DRAWING
# concrete wall + deck
a(f'<path d="M{xCIi},{yTopBrk} L{xBrkR},{yTopBrk} L{xBrkR},{yBotBrk} L{xCIi},{yBotBrk} z" fill="url(#conc)" stroke="#000" stroke-width="1.8"/>')
a(f'<path d="M{xBrkL},{yDeckT} L{xCIi},{yDeckT} L{xCIi},{yDeckB} L{xBrkL},{yDeckB} z" fill="url(#conc)" stroke="#000" stroke-width="1.8"/>')
a(f'<path d="M{xCIi},{yDeckT} L{xCIi},{yDeckB}" class="thin" stroke-dasharray="14 8"/>')
# continuous insulation - wall + roof (meeting at the corner)
a(f'<rect x="{xCavI}" y="{yTopBrk}" width="{xCIi-xCavI}" height="{yInsB-yTopBrk}" fill="url(#insul)" stroke="#000" stroke-width="1.2"/>')
a(f'<rect x="{xBrkL}" y="{yCBb}" width="{xCavI-xBrkL}" height="{yInsB-yCBb}" fill="url(#insul)" stroke="#000" stroke-width="1.2"/>')
a(f'<path d="M{xBrkL},1247 L{xCavI},1247" class="thin"/>')
# air / vapor barrier: roof deck up face of concrete (transition membrane)
a(f'<path d="M{xBrkL},{yAVB} L{xCIi},{yAVB} L{xCIi},{yTopBrk}" class="mem"/>')
# roof cover board / slip sheet / underlayment
a(f'<path d="M{xBrkL},{yCBb} L{xCavI},{yCBb}" class="thin"/>')
a(f'<path d="M{xBrkL},{ySlip} L{xCavI},{ySlip}" class="thin" stroke-dasharray="9 6"/>')
a(f'<path d="M{xBrkL},{yUL} L1248,{yUL} L1248,1056" class="mem"/>')
# metal panel + seams + end hem
a(f'<path d="M{xBrkL},{yPanel} L1240,{yPanel} L1240,1145 l10,0" class="mtl"/>')
for xs in (880, 1030, 1170):
    a(f'<path d="M{xs},{yPanel} l0,-34 q0,-11 10,-11 q10,0 10,11 l0,34" class="mtl"/>')
a(f'<path d="M888,1152 l0,26 M1038,1152 l0,26 M1178,1152 l0,26" class="thin"/>')   # clips
# base flashing + blocking + shelf angle + through-wall flashing / counterflashing
a(f'<rect x="{xCavI}" y="1040" width="{xCIi-xCavI}" height="28" fill="#fff" stroke="#000" stroke-width="1.6"/>')
a(f'<path d="M{xCavI},1040 L{xCIi},1068 M{xCavI},1068 L{xCIi},1040" class="thin"/>')
a(f'<path d="M1246,{yBFtop} L1246,1138 L1090,1138 L1090,1168" class="mtl"/>')
a(f'<path d="M1240,1054 l14,0" class="med"/>')                      # fastener at top of base flashing
a(f'<path d="M{xCIi},900 L1276,900 L1276,964 L1222,964 L1222,948" class="mtl"/>')   # shelf angle
a(f'<path d="M{xCIi},916 L{xCIi},{yShelf-2} L1232,{yShelf-2} L1232,{yCFbot} l-12,-10" class="mtl"/>')  # TWF -> counterflashing
# cavity: mortar net + weep
a(f'<rect x="{xStoneI}" y="880" width="{xCavI-xStoneI}" height="60" fill="url(#mortarnet)"/>')
a(f'<path d="M1238,928 q6,6 12,0" class="med"/>')
# stone veneer
a(f'<rect x="{xStoneO}" y="{yTopBrk+18}" width="{xStoneI-xStoneO}" height="{yStoneB-yTopBrk-18}" fill="url(#stone)" stroke="#000" stroke-width="1.6"/>')
for yj in (430, 542, 654, 766, 878):
    a(f'<path d="M{xStoneO},{yj} L{xStoneI},{yj}" class="med"/>')
a(f'<path d="M{xStoneO},{yStoneB} L{xStoneI},{yStoneB}" class="med"/>')
# stone anchor
a(f'<path d="M{xCIi},612 L1408,612 L1408,628 L{xCIi},628 z" fill="#fff" stroke="#000" stroke-width="1.6"/>')
a(f'<path d="M1396,604 l0,32 M1384,604 l0,32" class="thin"/>')
a(f'<path d="M{xCIi},598 L{xCIi},642 M{xCIi},620 L1240,620 L1240,606 L1218,606" class="mtl"/>')
# sealant at counterflashing head
a(f'<circle cx="1243" cy="884" r="6" fill="#000"/>')
# break lines
a(f'<path d="{zig_v(xBrkR, yTopBrk, yBotBrk)}" class="med"/>')
a(f'<path d="{zig_h(xBrkL, xBrkR, yBotBrk)}" class="med"/>')
a(f'<path d="{zig_h(xStoneO-20, xBrkR, yTopBrk, amp=10, seg=58)}" class="med"/>')
a(f'<path d="M{xBrkL},{yPanel-60} L{xBrkL},{yBotBrk}" class="thin"/>')
# slope arrow / elevation / dims
a(f'<path d="M1080,1120 l-180,0 m16,-8 l-16,8 l16,8" class="thin"/>')
text(1080, 1112, 'SLOPE — SEE ROOF PLAN', cls="dimt", anchor="end", halo=True)
a(f'<path d="M778,{yPanel} L778,1016" class="dim" stroke-dasharray="10 6"/>')
elev(778, yPanel, '')
text(790, 1010, 'T.O. ROOF PANEL  EL. = ___', cls="dimt", halo=True)
vdim(1210, yBFtop, yPanel, '8" MIN.')
vdim(1168, yBFtop, yCFbot, '4" MIN. LAP')
vdim(1096, yStoneB, yPanel, 'CLR. — VERIFY')
# EXT / INT
for x, lbl in ((1090, "EXT."), (1575, "INT.")):
    a(f'<rect x="{x-52}" y="{yBotBrk+40}" width="104" height="48" fill="#fff" stroke="#000" stroke-width="1.8"/>')
    text(x, yBotBrk+73, lbl, cls="tag", anchor="middle")
# assembly tags
tag(1082, 392, "W10"); a(f'<path d="M1114,392 L1430,392" class="mtl"/>')
tag(860, 1062, "R2");  a(f'<path d="M860,1081 L860,{yDeckB-6}" class="mtl"/>')

# ==================================================== NOTES
# top row
c = Col(806, 232, "start", 44)
c.note("STONE VENEER — TYPE, THICKNESS, FINISH AND JOINT SIZE PER SPEC. ANCHORAGE PER ENGINEERED SHOP DRAWINGS (DEFERRED SUBMITTAL, SIGNED AND SEALED).", target=(xStoneO+18, 470))
c = Col(1660, 232, "start", 46)
c.note("W10 — VERIFY WALL ASSEMBLY TAG AGAINST ASSEMBLY SCHEDULE; CONFIRM IT CARRIES THE STONE, CAVITY, INSULATION AND AIR BARRIER SHOWN HERE.", target=(1360, 392), dash=True)

# left column
LC = Col(700, 392, "end", 50, gap=20)
LC.note("STONE ANCHOR — STAINLESS, THERMALLY ISOLATED, TYPE AND SPACING PER STONE ENGINEER. SEAL EVERY PENETRATION THROUGH THE AIR / WATER BARRIER.", (1268, 620), flag=True)
LC.note("1\" MIN. CLEAR DRAINAGE CAVITY — KEEP FREE OF MORTAR DROPPINGS.", (xStoneI+7, 780), flag=True)
LC.note("MORTAR NET / DRAINAGE MESH AT BASE OF CAVITY.", (1242, 906), flag=True)
LC.note("WEEP VENTS @ 24\" O.C. MAX. IN FIRST JOINT ABOVE FLASHING.", (1244, 930), flag=True)
LC.note("SEALANT AND BACKER ROD AT COUNTERFLASHING HEAD JOINT.", (1247, 884), flag=True)
LC.note("STANDING SEAM METAL ROOF PANEL — 24 GA. PREFINISHED (PVDF), __\" WIDE, __\" SEAM HT., CONCEALED FLOATING CLIPS @ __\" O.C. PER UPLIFT CALCULATIONS.", (1015, 1148))
LC.note("CONCEALED CLIP AT EACH SEAM — ALLOW FOR THERMAL MOVEMENT; DO NOT PIN PANEL AT BOTH ENDS.", (1178, 1168), flag=True)
LC.note("HIGH-TEMPERATURE SELF-ADHERED UNDERLAYMENT (240°F MIN.) — FULL COVERAGE, 3\" SIDE / 6\" END LAPS. TURN UP WALL 8\" MIN. BEHIND BASE FLASHING.", (960, yUL), flag=True)
LC.note("SLIP SHEET / ROSIN PAPER BETWEEN UNDERLAYMENT AND PANEL.", (900, ySlip), flag=True)
LC.note("COVER BOARD, 1/2\" GLASS-MAT GYPSUM, MECHANICALLY FASTENED.", (860, yCBb+3), flag=True)
LC.note("RIGID INSULATION — TWO LAYERS, JOINTS STAGGERED, R-__ MIN. TOTAL PER ENERGY CODE.", (820, 1250))
LC.note("AIR / VAPOR BARRIER OVER DECK — CONTINUOUS; TURN UP FACE OF CONCRETE WALL AND LAP WITH WALL AIR BARRIER 3\" MIN.", (800, yAVB), flag=True)
LC.note("STRUCTURAL CONCRETE ROOF DECK — SEE STRUCTURAL. SLOPE PER ROOF PLAN.", (790, 1380))

# right column
RC = Col(1640, 392, "start", 58, gap=20)
RC.note("CONCRETE WALL — SEE STRUCTURAL FOR THICKNESS, REINFORCING AND ANCHOR EMBEDMENT.", (1400, 500))
RC.note("CONTINUOUS RIGID INSULATION ON WALL — R-__ MIN.; RUN CONTINUOUS INTO ROOF INSULATION WITH NO GAP AT THE CORNER. FILL VOIDS W/ SPRAY FOAM.", (1272, 700), flag=True)
RC.note("AIR / WATER BARRIER ON CONCRETE FACE — CONTINUOUS FROM ROOF AIR BARRIER UP THE WALL; LAP AND SEAL ALL TRANSITIONS.", (xCIi+3, 830), flag=True)
RC.note("SHELF / RELIEVING ANGLE AT BASE OF VENEER — SIZE, ANCHORS AND THERMAL ISOLATION PER STRUCTURAL. CONFIRM VENEER IS SUPPORTED AT THIS LEVEL.", (1278, 930), flag=True)
RC.note("STAINLESS THROUGH-WALL FLASHING W/ END DAMS — LAP UNDER WALL AIR BARRIER, TURN DOWN AS COUNTERFLASHING OVER BASE FLASHING, 4\" MIN. LAP, HEMMED DRIP EDGE.", (1232, 1010), flag=True)
RC.note("CONTINUOUS TREATED BLOCKING OR METAL SUB-GIRT FOR BASE FLASHING ATTACHMENT — FASTEN THROUGH INSULATION TO CONCRETE.", (1270, 1054), flag=True)
RC.note("BASE FLASHING — 24 GA., TURN UP 8\" MIN. ABOVE FINISHED ROOF SURFACE, HEMMED TOP AND BOTTOM EDGES, LAP JOINTS 4\" MIN. W/ SEALANT.", (1246, 1110), flag=True)
RC.note("PANEL END — HEM UP 2\" MIN. INTO CONTINUOUS OFFSET CLEAT AT WALL; NO EXPOSED FASTENERS IN PANEL PAN.", (1243, 1158), flag=True)
RC.note("R2 — VERIFY ROOF ASSEMBLY TAG AGAINST ASSEMBLY SCHEDULE.", (872, 1300), dash=True)

# ---------------------------------------------------- general notes
gx, gy, gw, gh = 60, 1560, 930, 630
a(f'<rect x="{gx}" y="{gy}" width="{gw}" height="{gh}" fill="none" stroke="#000" stroke-width="1.8"/>')
text(gx+20, gy+38, "GENERAL NOTES — THIS DETAIL", cls="h3")
a(f'<path d="M{gx+20},{gy+52} L{gx+gw-20},{gy+52}" class="thin"/>')
GN = [
 "ROOF ASSEMBLY TO BE UL 790 CLASS 'A' AND TESTED FOR UPLIFT PER ASTM E1592 / UL 580 CLASS 90. SUBMIT UPLIFT CALCULATIONS SIGNED BY A LICENSED ENGINEER.",
 "STANDING SEAM PANELS: VERIFY MIN. ROOF SLOPE AGAINST PANEL PROFILE (HYDROKINETIC VS. HYDROSTATIC / SEAM-SEALED) AND MFR. REQUIREMENTS.",
 "ALL FLASHING SAME METAL AND FINISH FAMILY; ISOLATE DISSIMILAR METALS W/ SEPARATION TAPE OR COATING.",
 "FLASHING TURN-UP AT ALL WALL TRANSITIONS 8\" MIN. ABOVE FINISHED ROOF SURFACE; 12\" MIN. WHERE DRIFTING OCCURS.",
 "END DAMS AND SOLDERED / SEALED CORNERS AT ALL FLASHING TERMINATIONS AND DIRECTION CHANGES.",
 "MAINTAIN CONTINUOUS AIR BARRIER FROM ROOF DECK TO WALL — SEAL ALL ANCHOR AND FASTENER PENETRATIONS.",
 "PROVIDE 4'-0\" LONG MOCK-UP OF THIS TRANSITION, INCLUDING STONE, FLASHING AND PANEL END, FOR REVIEW PRIOR TO PROCEEDING.",
 "PROTECT PANEL FINISH DURING STONE WORK; CLEAN MORTAR FROM PANELS AND FLASHING IMMEDIATELY.",
 "COORDINATE SNOW RETENTION, IF REQUIRED, W/ ROOF PLAN — DO NOT PENETRATE PANELS; CLAMP-ON AT SEAMS ONLY.",
]
yy = gy + 84
for i, g in enumerate(GN, 1):
    lines = textwrap.wrap(g, width=84)
    text(gx+22, yy, f"{i}.")
    for j, ln in enumerate(lines): text(gx+54, yy+j*22, ln)
    yy += len(lines)*22 + 12

# ---------------------------------------------------- verify box
vx, vy, vw, vh = 1860, 1700, 780, 400
a(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="none" stroke="#000" stroke-width="1.8"/>')
text(vx+20, vy+38, "VERIFY / COORDINATE BEFORE ISSUE", cls="h3")
a(f'<path d="M{vx+20},{vy+52} L{vx+vw-20},{vy+52}" class="thin"/>')
VB = [
 "HEADWALL OR SIDEWALL? IF SLOPE RUNS PARALLEL TO THE WALL, ADD STEP FLASHING AND A KICKOUT AT THE LOW END",
 "ROOF SLOPE + PANEL PROFILE (SEAM TYPE, WIDTH, GAUGE, FINISH)",
 "STONE VENEER SUPPORT LEVEL — SHELF ANGLE HERE OR BEARING BELOW",
 "SNOW DRIFT / SNOW RETENTION REQUIREMENTS",
 "CLEARANCE, BOTTOM OF STONE TO ROOF SURFACE (8\" MIN. RECOMMENDED)",
 "W10 / R2 TAGS AGREE W/ ASSEMBLY SCHEDULE",
]
yy = vy + 86
for v in VB:
    lines = textwrap.wrap(v, width=52)
    for j, ln in enumerate(lines): text(vx+24, yy+j*22, ("—  " if j == 0 else "    ") + ln)
    yy += len(lines)*22 + 10

# ---------------------------------------------------- title block
a('<path d="M1046,1700 L1800,1700" class="med"/>')
a('<circle cx="1096" cy="1654" r="35" fill="none" stroke="#000" stroke-width="1.8"/>')
a('<path d="M1061,1654 L1131,1654" class="thin"/>')
text(1096, 1650, "6", cls="tag", anchor="middle")
text(1096, 1684, "A6.01", anchor="middle")
text(1160, 1672, "STONE WALL TRANSITION TO METAL STANDING SEAM ROOF", cls="ttl2")
text(1164, 1728, 'SCALE   3" = 1\'-0"', cls="sc")
a('</svg>')

open("/home/user/drawing-set/details/06-A6.01-stone-wall-to-standing-seam-roof.svg","w").write("\n".join(out))
print("ok")
