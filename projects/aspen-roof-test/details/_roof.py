# -*- coding: utf-8 -*-
"""Shared geometry for the A6.05 headwall details: R2 roof meeting a framed wall.

Real inches, y down, roof panel surface at y = 0.  EXT. left, INT. right (as
drawn on A6.05).  The wall's nail base runs down onto the roof's rigid
insulation so the insulation is continuous at the corner, and closed-cell spray
foam runs from the roof cavity up into the wall cavity.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.join(HERE, "..", "..", "..", ".claude", "skills", "architectural-details", "scripts")
sys.path.insert(0, SKILL)
from detailkit import Detail  # noqa: E402,F401

ASSEMBLIES = os.path.join(HERE, "assemblies.yaml")

X0 = -26          # left break of the roof
XNB = 12.5        # exterior face of wall nail base = end of the roof layers
XSH = 15.0        # face of wall sheathing
XFOS = 15.5       # face of stud
XIN = 21.0        # interior face of stud
TOP = -40         # top break of the wall
T_PLY, T_NB, T_SH, T_FR, B_FR = 0.25, 0.75, 2.75, 3.375, 14.625


def roof_and_wall(d):
    # ---- R2 roof (drawn, not noted - the tag carries it)
    d.line([(X0, 0), (11.2, 0), (11.2, -2.0), (11.7, -2.0)], style="metal")          # panel + end hem
    for xs in (-20, -8):
        d.line([(xs, 0), (xs, -1.0), (xs + 0.6, -1.0), (xs + 0.6, 0)], style="metal")  # seams
        d.line([(xs + 0.3, 0.02), (xs + 0.3, -0.7)], style="thin")                      # clip
    d.line([(X0, 0.2), (XNB - 0.1, 0.2), (XNB - 0.1, -8.5)], style="membrane")         # underlayment / HT membrane turn-up
    d.rect(X0, T_PLY, XNB - X0, T_NB - T_PLY, hatch="ply", edge="thin")
    d.rect(X0, T_NB, XSH - X0, T_SH - T_NB, hatch="insul", edge="med")                 # nail base under wall
    d.rect(X0, T_SH, XFOS - X0, T_FR - T_SH, hatch="ply", edge="med")
    d.rect(X0, T_FR, XIN + 1.25 - X0, B_FR - T_FR, hatch="sprayfoam", edge="thin")
    d.xbox(XFOS, T_FR, XIN - XFOS, B_FR - T_FR, edge="med")                          # beam / header at wall
    # ---- wall above roof
    d.rect(XFOS, TOP, XIN - XFOS, 1.875 - TOP, hatch="sprayfoam", edge="med")
    d.xbox(XFOS, 1.875, XIN - XFOS, 1.5)                                             # bottom plate
    d.rect(XIN, TOP, 1.25, T_FR - TOP, hatch="gyp", edge="med")                       # 2 layers gyp
    d.rect(XSH, TOP, XFOS - XSH, T_SH - TOP, hatch="ply", edge="med")
    d.rect(XNB, TOP, XSH - XNB, T_NB - TOP, hatch="insul", edge="med")
    # ---- breaks, reference, labels
    d.break_line(X0, -1.5, X0, B_FR + 0.5)
    d.break_line(X0, B_FR, XIN + 1.25, B_FR)
    d.break_line(XNB - 5, TOP, XIN + 1.25, TOP)
    d.grid(XFOS, "FOS")
    d.label(-16, -30, "EXT.")
    d.label(30, -30, "INT.")
    d.tag("R2", at=(-15, 9), to=(-15, 1.7))
    d.slope(-2, -3, 10, label="SLOPE PER ROOF PLAN", direction=-1)
    d.dim((5.5, 0), (5.5, -8.3), '8" MIN.')


def roof_notes(d):
    """Notes at the roof side of the joint - same on every headwall."""
    d.note("BASE FLASHING - TURN UP 8\" MIN. ABOVE FINISHED ROOF, HEM TOP AND BOTTOM EDGES "
           "- SEE WATERPROOFING DRAWINGS", to=(12.3, -5.5), side="left", flag=True)
    d.note("PANEL END HEM UP 2\" MIN. INTO CONTINUOUS OFFSET CLEAT AT WALL; NO EXPOSED "
           "FASTENERS IN PANEL PAN", to=(11.4, -1.9), side="left", flag=True)
    d.note("CONCEALED CLIP AT EACH SEAM - ALLOW FOR THERMAL MOVEMENT; DO NOT PIN PANEL AT "
           "BOTH ENDS", to=(-19.7, -0.6), side="left")
    d.note("HIGH TEMP. SELF-ADHERED MEMBRANE - TURN UP WALL 8\" MIN. BEHIND BASE FLASHING, "
           "LAP UNDER WALL WRB - SEE WATERPROOFING DRAWINGS", to=(XNB - 0.1, -3), flag=True)
    d.note("RUN WALL NAIL BASE DOWN ONTO ROOF NAIL BASE - NO GAP IN RIGID INSULATION AT "
           "CORNER", to=(13.7, 0.75))
    d.note("CONTINUOUS CLOSED CELL SPRAY FOAM FROM ROOF CAVITY INTO WALL CAVITY - WRAP "
           "AROUND BEAM FOR CONTINUOUS THERMAL ENVELOPE AND AIR BARRIER", to=(19, 6))
    d.note("ROOF FRAMING AND BEAM, S.S.D.", to=(10, 11))
