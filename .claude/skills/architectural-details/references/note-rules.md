# Note rules - tag the assembly, note the intent

## 1. Tag, then note

- Tag every assembly that is cut or seen on the detail, using the project assembly
  schedule's own tag (W1, R2, F1, C1 ...).
  - One tag per assembly per detail, placed where the assembly is clearest, with a
    dot leader into it.
  - A new tag wherever the build-up changes, such as a wall going below grade, a
    roof going from warm to vented, or a rated wall meeting an unrated one. The
    office catches this one most often: *"R3 should not carry the wall."*
- If an assembly is not in the schedule, **don't write its layers as notes**. Add it
  to the schedule, or put "ADD W_ TO THE ASSEMBLY SCHEDULE" in the verify list.
- The tag is the only mention of the assembly's make-up. A note may *name* a layer to
  say what happens to it at this joint ("LAP THE WRB OVER THE FLASHING"). It never
  restates the layer's spec (thickness, R-value, gauge, spacing, type, product).

`check_notes.py` stops any note that names a tagged layer's material *and* repeats
its spec.

## 2. What a note is for

| Call out | Example |
|---|---|
| The joint between assemblies | `LAP ROOF UNDERLAYMENT UP THE WALL 8" MIN. BEHIND THE BASE FLASHING.` |
| Control-layer continuity | `AIR BARRIER CONTINUOUS FROM ROOF DECK TO WALL - LAP 3" MIN. AND SEAL. THIS IS THE LINE THAT FAILS.` |
| Items in no assembly (flag them) | `■ STAINLESS THROUGH-WALL FLASHING W/ END DAMS, HEMMED DRIP.` |
| A dimension to hold | `BOTTOM OF SIDING 8" MIN. ABOVE FINISH GRADE AT THE HIGHEST GRADE POINT.` |
| Sequence | `INSTALL THE TRANSITION MEMBRANE BEFORE THE WALL CI.` |
| Visible intent | `HOLD THE FACE OF THE CI FLUSH WITH THE FOUNDATION INSULATION - ONE PLANE, NO LEDGE.` |
| Responsibility | `SHELF ANGLE SIZE, ANCHORS AND THERMAL ISOLATION PER STRUCTURAL.` |
| Field verify | `VERIFY FINISH FLOOR THICKNESS AT EACH LEVEL BEFORE CUTTING STRINGERS.` |

Say *why* when the why changes behaviour. For example, "NO LEDGE TO CATCH WATER"
stops someone from "improving" it.

## 3. What never goes in a note

- A layer from the tagged assembly, with its size or type (`5/8" TYPE X GYP. BD.`,
  `2x6 STUDS @ 16" O.C.`, `R-21 BATT`). **The tag says it.**
- Anything already on the structural, civil or interiors drawings. Refer to it
  instead ("PER STRUCTURAL").
- Generic spec language: "INSTALL PER MANUFACTURER'S INSTRUCTIONS" as a note on its
  own, "PROVIDE ALL REQUIRED ...". That belongs in the specs.
- Vague words, which the checker rejects: AS REQUIRED, AS NECESSARY, ETC., OR EQUAL,
  WHERE APPLICABLE, BY OTHERS, PER CODE, ADEQUATE, PROPER, SUITABLE. Say exactly
  what, where and how much.
- "TYP." unless the detail says what it is typical of.

## 4. Where each kind of note goes

| Kind | Where | Length |
|---|---|---|
| Leader note | Beside the drawing, arrow to the item | One idea, about 35 words max |
| Flagged leader note (■) | Same, for items in no assembly | Same |
| Keynote (A, B, C ...) | Hexagon on the drawing, text in the KEYNOTES box | For crowded details: the same item repeated, or text too long for a leader |
| General notes, this detail | Numbered box under the title | Sequence, mock-ups, submittals, and anything that applies to the whole detail |
| Verify / coordinate before issue | Box, dash bullets | Open questions and every assumption. Remove before issue. |

## 5. Wording standard (from the office's issued sets)

- ALL CAPS. Plain construction English, imperative voice: "LAP", "HOLD", "SEAL",
  "RETURN", "DO NOT".
- Dimensions in feet and inches with fractions: `1'-6"`, `3/4"`, `8" MIN.`,
  `4 1/2" MAX.`. Use MIN./MAX. when a dimension is a limit, not a target.
- R-values with a hyphen, `R-21`. A tag has no hyphen, `R2`.
- Cross-references as number/sheet: `SEE 3/A6.31`. Specs by section: `SEE SPEC 07 62 00`.
  Never a bare "SEE DETAIL".
- `**  ...  **` around the one or two warnings that cost money if missed, for example
  `** 11" IS THE TRIGGER LINE, NOT A MARGIN. **`.
- Code citations only where the note depends on a code limit, in the form
  `- 1011.5.2` for the City of Aspen (IBC as amended by M.C. 8.20). Look up every
  section in the code library, never from memory. Never cite the IRC on a City of
  Aspen detail; Pitkin County details may cite it.
- Blanks `__` are allowed only while drafting. The checker warns until they are
  filled.

## 6. Before and after - 6/A6.01, stone wall to standing seam roof

The 100% CD markup of 6/A6.01 (project branch `admiring-galileo`) was written before
this rule. Some of its notes would now be cut:

| Before | After | Why |
|---|---|---|
| `RIGID INSULATION - TWO LAYERS, JOINTS STAGGERED, R-__ MIN. TOTAL PER ENERGY CODE.` | *(cut. Tag R2 carries it.)* | Repeats the roof assembly |
| `CONCRETE WALL - SEE STRUCTURAL FOR THICKNESS, REINFORCING ...` | *(cut. Tag W10 plus the structural drawings.)* | Repeats the assembly and the structural drawings |
| `COVER BOARD, 1/2" GLASS-MAT GYPSUM, MECHANICALLY FASTENED.` | *(cut, or move into R2 if the schedule is missing it.)* | Assembly layer |
| `CONTINUOUS RIGID INSULATION ON WALL - R-__ MIN.; RUN CONTINUOUS INTO ROOF INSULATION WITH NO GAP AT THE CORNER.` | `RUN THE WALL INSULATION CONTINUOUS INTO THE ROOF INSULATION - NO GAP AT THE CORNER. FILL VOIDS WITH SPRAY FOAM.` | Keep the joint, drop the spec |
| `W10 - VERIFY WALL ASSEMBLY TAG ...` as a leader note | Move to the verify box | A verify item, not a construction note |
| `■ BASE FLASHING - TURN UP 8" MIN. ABOVE FINISHED ROOF SURFACE, HEMMED TOP AND BOTTOM EDGES` | *(keep)* | Belongs to no assembly, and it is the joint |
| `■ AIR / VAPOR BARRIER OVER DECK - CONTINUOUS; TURN UP FACE OF CONCRETE WALL AND LAP WITH WALL AIR BARRIER 3" MIN.` | *(keep)* | Continuity across the joint |

## 7. Final pass before a detail goes out

- [ ] Every assembly cut or seen has its tag, and every tag is in the schedule.
- [ ] No note repeats a layer, and `check_notes.py` shows 0 errors.
- [ ] All four control layers are traced across the joint, each with a line or a note.
- [ ] Every item in no assembly is drawn *and* flagged.
- [ ] Every dimension the builder must hold is on the drawing.
- [ ] Every cross-reference has a number and sheet, and the target detail exists.
- [ ] Code sections were checked in the code library for this jurisdiction.
- [ ] The verify box is empty, or its items have gone to the project team.
