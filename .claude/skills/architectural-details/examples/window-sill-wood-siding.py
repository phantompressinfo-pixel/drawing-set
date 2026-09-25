# -*- coding: utf-8 -*-
"""EXAMPLE - typical fixed window sill at wood siding, drawn the office way.

Modelled on 1/A6.16 of the office's sample set: INT. left, EXT. right, the wall
carries its tag, and the notes cover only the sill: window, shim, sealant, sill,
slope, drip, pan and the flashing laps. The wall build-up is left to the tag.

    python3 examples/window-sill-wood-siding.py        (from the skill folder)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from detailkit import Detail  # noqa: E402

d = Detail(1, "A6.16", "TYP. FIXED WINDOW SILL @ WOOD SIDING", scale="3",
           slug="typ-fixed-window-sill-wood-siding", jurisdiction="aspen",
           project="EXAMPLE - OFFICE METHOD")

BOT = 22
# wall below the opening (3B-X) - drawn, not noted
d.rect(-0.625, 1, 0.625, BOT - 1, hatch="gyp", edge="med")
d.batt(0, 3, 5.5, BOT - 3)
d.xbox(0, 0, 5.5, 1.5)
d.xbox(0, 1.5, 5.5, 1.5)
d.rect(5.5, 0, 0.5, BOT, hatch="ply", edge="med")
d.rect(6.1, 3.2, 0.75, BOT - 3.2, hatch="wood", edge="thin")
d.rect(6.85, 3.2, 0.75, BOT - 3.2, hatch="wood", edge="med")
d.line([(6.05, 3), (6.05, BOT)], style="airbar")                     # WRB

# the sill itself - every piece here is noted
d.line([(0.6, 0.05), (6.05, 0.05), (6.05, 3.0)], style="membrane")   # liquid-applied flashing
d.line([(1.2, -1.0), (1.2, -0.1), (10.2, -0.1), (10.2, 1.2), (9.9, 1.5)], style="metal")  # copper pan
d.rect(2.0, -0.4, 2.8, 0.25, hatch="none", edge="thin")             # synthetic wood shim
d.rect(1.5, -6, 3.7, 5.6, hatch="none", edge="med")                 # window frame
d.rect(2.8, -13, 1.1, 10.5, hatch="glass", edge="thin")             # IGU
d.poly([(5.3, -2.6), (10, -2.4), (10, -0.15), (5.3, -0.15)], hatch="wood", edge="cut")  # 3x sill
d.line([(9.25, -0.15), (9.25, -0.55), (9.5, -0.55), (9.5, -0.15)], style="thin")          # drip kerf
d.sealant(5.3, -2.85, 0.3)
d.rect(-1.75, -0.75, 3.1, 0.75, hatch="wood", edge="med")           # interior sill
d.line([(-0.625, 1), (-0.9, 1), (-0.9, 0.9)], style="thin")         # J-bead

d.break_line(1.2, -13, 5.6, -13)
d.break_line(-1.2, BOT, 8, BOT)
d.grid(3.35, "GL")      # grid line
d.grid(5.5, "FOS")      # face of stud
d.label(-4, -9, "INT.")
d.label(12.5, -9, "EXT.")
d.tag("3B-X", at=(12.5, 12), to=(7.2, 12))
d.elev(19, -2.4, "T.O. SILL", "SEE SCHEDULE", length=9)

d.note("WINDOW PER SCHEDULE", to=(4.9, -5))
d.note("SEALANT W/ BACKER ROD", to=(5.3, -2.85))
d.note('1/2" PER FT SLOPE MIN.', to=(8.3, -2.47))
d.note("3x WOOD SILL", to=(7.5, -1.2))
d.note("SYNTHETIC WOOD W/ KERF CUTS PER WINDOW MFR. INSTALL REQS", to=(3.4, -0.28))
d.note("DRIP KERF", to=(9.37, -0.5))
d.note('COPPER SHT. METAL FLASHING PAN - RETURN UP @ JAMBS 6" MIN.', to=(10.2, 0.7), flag=True)
d.note("LIQUID-APPLIED FLASHING - WRAP INTO OPENING, LAP OVER WRB - SEE WATERPROOFING DRAWINGS",
       to=(6.05, 2.0), flag=True)
d.note("SEE 1 / A5.02 FOR WALL ASSEMBLY", to=(7.6, 19))
d.note("PAN FLASHING W/ END DAMS SET IN FULL BED OF SEALANT - SEE WATERPROOFING DRAWINGS",
       to=(1.2, -0.7), side="left", flag=True)
d.note("SILL PER INTERIOR ELEVATIONS", to=(-1.2, -0.4), side="left")
d.note("J-BEAD", to=(-0.85, 1), side="left")

d.verify("3B-X AGREES WITH THE ASSEMBLY SCHEDULE (A5.02).")
d.verify("PAN AND FLASHING SEQUENCE AGREES WITH THE WATERPROOFING CONSULTANT'S DRAWINGS.")

sys.exit(d.save(os.path.join(HERE, "out"), assemblies=os.path.join(HERE, "assemblies-example.yaml")))
