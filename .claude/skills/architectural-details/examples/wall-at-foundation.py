# -*- coding: utf-8 -*-
"""EXAMPLE - exterior transition: wood siding wall at concrete foundation and grade.

Shows the office method end to end: every assembly carries its tag (W1, W2, F1),
and the notes say only what happens where those assemblies meet.  Not a project
detail - the assemblies are the ones in templates/assemblies.yaml.

    python3 examples/wall-at-foundation.py        (from the skill folder)
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "scripts"))
from detailkit import Detail  # noqa: E402

d = Detail(1, "A6.10", "SIDING WALL AT FOUNDATION AND GRADE", scale="3",
           slug="siding-wall-at-foundation", jurisdiction="aspen",
           project="EXAMPLE - OFFICE METHOD")

# real inches; x = 0 is the face of the sheathing / foundation, exterior to the left
T_CONC = 40          # top of foundation
GRADE = 52           # finish grade
SID_B = 44           # bottom of siding
BOT = 92             # bottom break

# --- W2 foundation wall
d.rect(0, T_CONC, 8, BOT - T_CONC, hatch="conc", edge="cut")
d.rect(-2, T_CONC + 1, 2, BOT - T_CONC - 1, hatch="insul", edge="med")        # XPS (in W2)
d.rect(-2.4, T_CONC + 1, 0.4, GRADE + 6 - T_CONC - 1, hatch="none", edge="med")  # protection board
d.rect(-30, GRADE, 27.6, BOT - GRADE, hatch="earth", edge="none")
d.grade(-30, -2.4, GRADE)

# --- F1 floor
d.rect(0.5, 38.5, 5.5, 1.5, hatch="wood", edge="cut")                          # treated sill
d.line([(0.5, 40), (6, 40)], style="membrane")                                   # sill gasket
d.rect(0.5, 26.625, 1.25, 11.875, hatch="wood", edge="cut")                      # rim board
d.rect(1.75, 26.625, 3.5, 11.875, hatch="insul", edge="thin")                    # spray foam at rim
d.rect(0.5, 25.875, 22, 0.75, hatch="ply", edge="med")                           # subfloor
d.line([(5.25, 26.625), (22, 26.625)], style="thin")
d.line([(5.25, 38.5), (22, 38.5)], style="hidden")                               # joist beyond
d.line([(8, 38.5), (22, 38.5)], style="hidden")
d.label(16, 34, "CRAWLSPACE")

# --- W1 wall
d.rect(0.5, 24.375, 5.5, 1.5, hatch="wood", edge="cut")                          # bottom plate
d.batt(0.5, 0, 5.5, 24.375)
d.rect(6, 0, 0.625, 24.375, hatch="gyp", edge="med")                             # gyp
d.rect(0, 0, 0.5, 38.5, hatch="ply", edge="med")                                 # sheathing
d.rect(-2, 0, 2, T_CONC - 0.5, hatch="insul", edge="med")                        # mineral wool CI
d.line([(-2, 0), (-2, 34)], style="airbar")                                      # WRB face
d.rect(-2.75, 0, 0.75, SID_B, hatch="wood", edge="thin")                         # furring
d.rect(-3.5, 0, 0.75, SID_B, hatch="wood", edge="med")                           # siding
d.label(12, 12, "INT.")
d.label(-18, 30, "EXT.")

# transition membrane: sheathing down onto concrete
d.line([(-0.05, 33), (-0.05, T_CONC + 4)], style="membrane")
# Z-flashing: up behind the WRB, out over the foundation insulation, hemmed drip
d.line([(-2.05, 34), (-2.05, T_CONC + 0.5), (-3.2, T_CONC + 0.5), (-3.2, T_CONC + 1.4)], style="metal")
# insect screen at the base of the rainscreen cavity
d.line([(-2.75, SID_B), (-2, SID_B)], style="membrane")

d.break_line(-32, 0, 24, 0)
d.break_line(-32, BOT, 10, BOT)
d.break_line(24, 0, 24, 26)

# --- tags: the build-ups live in the schedule, not in these notes
d.tag("W1", at=(-12, 8), to=(-1, 8))
d.tag("W2", at=(16, 64), to=(6, 64))
d.tag("F1", at=(16, 20), to=(14, 26.2))

# --- dimensions and elevations that the builder has to hold
d.dim((-6, SID_B), (-6, GRADE), '8" MIN.')
d.dim((-4.5, 34), (-4.5, T_CONC + 0.5), '4" MIN. LAP', offset=0)
d.elev(-26, GRADE, "FINISH GRADE - SEE CIVIL")
d.elev(10, T_CONC, "T.O. FOUNDATION")

# --- notes: only the transition and the intent
d.note('Z-FLASHING - UP BEHIND THE WRB 4" MIN., OUT OVER THE TOP OF THE FOUNDATION '
       'INSULATION, HEMMED DRIP 1/2" PAST THE PROTECTION BOARD.', to=(-2.6, T_CONC + 0.5), side="left", flag=True)
d.note('INSECT SCREEN AT THE BASE OF THE RAINSCREEN CAVITY - LEAVE THE CAVITY OPEN TO DRAIN.',
       to=(-2.4, SID_B), side="left", flag=True)
d.note('HOLD THE FACE OF THE WALL CI FLUSH WITH THE FACE OF THE FOUNDATION INSULATION - ONE '
       'PLANE, NO LEDGE TO CATCH WATER.', to=(-2, 36), side="left")
d.note('BOTTOM OF SIDING 8" MIN. ABOVE FINISH GRADE AT THE HIGHEST GRADE POINT ALONG THIS WALL. '
       'NO MULCH OR PLANTING ABOVE THIS LINE.', to=(-3.2, SID_B), side="left")
d.note('PROTECTION BOARD OVER THE EXPOSED FOUNDATION INSULATION, 6" BELOW GRADE UP TO THE '
       'UNDERSIDE OF THE Z-FLASHING.', to=(-2.2, 49), side="left", flag=True)
d.note('SLOPE GRADE AWAY FROM THE WALL - SEE CIVIL.', to=(-20, GRADE), side="left")
d.note('SELF-ADHERED TRANSITION MEMBRANE, SHEATHING TO CONCRETE, 3" MIN. ONTO EACH. THIS IS THE '
       'AIR BARRIER JOINT - INSTALL BEFORE THE WALL CI.', to=(0, 37), side="right", flag=True)
d.note('SILL GASKET, CONTINUOUS. SEAL AROUND EVERY ANCHOR BOLT.', to=(3, 40), side="right", flag=True)
d.note('CLOSED-CELL SPRAY FOAM AT THE RIM, FULL DEPTH - NO GAPS AT JOIST ENDS.', to=(3.5, 32),
       side="right", flag=True)

d.general_note("SEQUENCE: TRANSITION MEMBRANE, THEN Z-FLASHING, THEN WRB LAPPED OVER THE FLASHING "
               "UP-LEG, THEN WALL CI AND RAINSCREEN.")
d.general_note('BUILD A 4\'-0" MOCK-UP OF THIS CORNER, THROUGH THE FLASHING, FOR ARCHITECT REVIEW '
               "BEFORE THE REST OF THE WALL IS CLAD.")
d.verify("FINISH GRADE ELEVATIONS AGAINST CIVIL ALONG THE FULL LENGTH OF THIS WALL.")
d.verify("W1, W2 AND F1 AGREE WITH THE ASSEMBLY SCHEDULE.")

sys.exit(d.save(os.path.join(HERE, "out"),
                assemblies=os.path.join(HERE, "..", "templates", "assemblies.yaml")))
