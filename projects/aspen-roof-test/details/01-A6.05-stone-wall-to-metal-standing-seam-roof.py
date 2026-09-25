# -*- coding: utf-8 -*-
"""1/A6.05 - STONE WALL TO METAL STANDING SEAM ROOF.  Headwall: W10 stone veneer
wall above an R2 standing seam roof.  Notes cover the joint only."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _roof import ASSEMBLIES, TOP, XNB, Detail, roof_and_wall, roof_notes  # noqa: E402

d = Detail(1, "A6.05", "STONE WALL TO METAL STANDING SEAM ROOF", scale="3",
           jurisdiction="aspen", project="ASPEN ROOF TEST")
roof_and_wall(d)

S_BOT = -8.9                                                      # bottom of stone
d.rect(12.0, TOP, 0.45, -14 - TOP, hatch="none", edge="thin")     # drainage mat
d.line([(XNB - 0.05, TOP), (XNB - 0.05, -9.1)], style="airbar")   # wall WRB
d.rect(8, TOP, 4, S_BOT - TOP, hatch="stone", edge="cut")         # stone veneer
for yj in (-30, -20):
    d.line([(8, yj), (12, yj)], style="med")
d.rect(8, S_BOT, 4.4, 0.4, hatch="steel", edge="med")             # stone support angle
d.rect(12.0, -14, 0.4, 14 + S_BOT, hatch="steel", edge="med")
d.fastener(12.4, -11.5, 8, 0)
d.line([(12.42, -13.5), (12.42, S_BOT - 0.05), (7.5, S_BOT - 0.05), (7.5, -4.3), (7.9, -4.3)],
       style="metal")                                            # thru-wall flashing -> counterflashing
d.line([(7.0, 0.12), (12.3, 0.12), (12.3, -8.3), (12.0, -8.3)], style="metal")  # base flashing
d.line([(12.3, -2.2), (11.6, -2.2), (11.6, -1.8)], style="metal")              # offset cleat
d.dim((4.0, S_BOT), (4.0, -4.3), '4" MIN. LAP')
d.tag("W10", at=(-4, -24), to=(10, -24))

d.note('WEEP VENTS IN FIRST JOINT ABOVE FLASHING @ 33" O.C. MAX.', to=(9.5, -20), side="left")
d.note("STAINLESS THRU-WALL FLASHING W/ END DAMS - LAP UNDER WALL AIR/WEATHER BARRIER, TURN "
       "DOWN AS COUNTERFLASHING OVER BASE FLASHING 4\" MIN. LAP, HEMMED DRIP EDGE",
       to=(8.5, S_BOT - 0.05), side="left", flag=True)
d.note("STONE SUPPORT ANGLE, S.S.D. - SEAL ALL FASTENER PENETRATIONS THROUGH WRB",
       to=(12.2, -12.5), flag=True)
roof_notes(d)

d.verify("WEEP SPACING: THE ORIGINAL NOTE SAID 24\" O.C.; THE WALL SCHEDULE (W3) SAYS 33\" O.C. "
         "MAX. DRAWN AT 33\" - CONFIRM.")
d.verify("W10 IS THE EXISTING STONE WALL TYPE - CONFIRM THIS HEADWALL IS EXISTING (ELSE W3).")
d.verify("R2 UNDERLAYMENT IS VERSASHIELD; THE HIGH-TEMP SA MEMBRANE HERE IS THE WALL TURN-UP "
         "ONLY. CONFIRM WITH THE WATERPROOFING CONSULTANT.")
d.verify("STONE SUPPORT ANGLE SIZE AND ANCHORAGE - STRUCTURAL.")

sys.exit(d.save(HERE, assemblies=ASSEMBLIES))
