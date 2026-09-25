# -*- coding: utf-8 -*-
"""2/A6.05 - EXTERIOR WOOD TO METAL STANDING SEAM ROOF.  Headwall: W4 wood siding
wall above an R2 standing seam roof.  Notes cover the joint only."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _roof import ASSEMBLIES, TOP, XNB, Detail, roof_and_wall, roof_notes  # noqa: E402

d = Detail(2, "A6.05", "EXTERIOR WOOD TO METAL STANDING SEAM ROOF", scale="3",
           jurisdiction="aspen", project="ASPEN ROOF TEST")
roof_and_wall(d)

SID_B = -2.0                                                       # bottom of siding
d.line([(XNB - 0.05, TOP), (XNB - 0.05, -12.3)], style="airbar")   # wall WRB, lapped over base flashing
d.rect(11.25, TOP, 0.75, SID_B - TOP, hatch="wood", edge="cut")    # vertical wood siding
d.line([(7.0, 0.12), (12.3, 0.12), (12.3, -8.3), (12.0, -8.3)], style="metal")  # base flashing
d.line([(12.3, -2.2), (11.6, -2.2), (11.6, -1.8)], style="metal")              # offset cleat
d.dim((9.5, 0), (9.5, SID_B), '2" MIN.')
d.tag("W4", at=(-4, -24), to=(11.6, -24))

d.note("LAP WALL WRB OVER VERTICAL LEG OF BASE FLASHING 4\" MIN. - SHINGLE LAP, NO REVERSE LAPS",
       to=(XNB - 0.05, -10.5), flag=True)
d.note('HOLD BOTTOM OF SIDING 2" MIN. ABOVE FINISHED ROOF - SIDING NOT TO BEAR ON FLASHING',
       to=(11.6, SID_B), side="left")
roof_notes(d)

d.verify("R2 TAG ADDED - THE DRAFT OF THIS DETAIL HAD NO ROOF TAG.")
d.verify('SIDING CLEARANCE ABOVE ROOF: 2" MIN. ASSUMED - CONFIRM AGAINST THE SIDING AND '
         "FIRE-RETARDANT TREATMENT MFR.")
d.verify("R2 UNDERLAYMENT IS VERSASHIELD; THE HIGH-TEMP SA MEMBRANE HERE IS THE WALL TURN-UP "
         "ONLY. CONFIRM WITH THE WATERPROOFING CONSULTANT.")

sys.exit(d.save(HERE, assemblies=ASSEMBLIES))
