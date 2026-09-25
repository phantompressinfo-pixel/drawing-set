# Drawing standards and the detailkit API

These follow the office's Revit details (the 22 sample sheets: A6.01-A6.38).

## What a detail looks like

- **The detail only.** No sheet border, no title block, no note boxes on the
  drawing. General notes and verify items go in the `.notes.txt` file and the
  reply.
- **Title:** a small bubble with the detail number over the sheet, the title in
  caps on an underline, and `SCALE : 3" = 1'-0"` under it.
- **Orientation:** INT. on the left and EXT. on the right, with each label bold and
  underlined near the top.
- **Leader notes:** mostly one column to the right of the drawing, text left-aligned,
  with a short horizontal leader and then an angled leg to an arrowhead. Put a few
  notes in a left column, right-aligned, for items on the interior side.
- **Reference lines:** grid / reference bubbles (GL, FOS, A, B, 1, 5 ...) at the top,
  with a dash-dot line through the detail.
- **Elevations:** a quartered target (two black quadrants) with the label and
  `EL = 100' - 0"` beside it, and a dashed line back to the surface. Examples:
  `T.O.F.F. @ MAIN LEVEL`, `B.O. FIN. CEILING`, `T.O. CONC. SLAB`.
- **Tags:** a plain box with the tag (`R2`, `F2`, `A`, `C13`, `3A-X`,
  `2/3/4/5B-X`), `SIM` under it where used, and a leader with a dot into the
  assembly.
- **Blue:** self-adhered membranes and air/water barriers draw blue. Glass is light
  blue. Everything else is black.

## Graphics

| Element | detailkit |
|---|---|
| Cut outline (heavy) | `edge="cut"` |
| Seen / secondary outline | `edge="med"` |
| Light lines | `edge="thin"` |
| Hidden / beyond | `style="hidden"` |
| Sheet metal (flashing, pans, cleats, panels) | `style="metal"` |
| SA membrane / liquid-applied flashing (blue) | `style="membrane"` |
| Air / water barrier (blue dash-dot) | `style="airbar"` |
| Vapor retarder | `style="vapor"` |
| Framing member in section (box with X) | `d.xbox()` |
| Batt insulation | `d.batt()` |

Hatches (`hatch=`):
- `conc`, `grout`, `cmu`, `earth`, `gravel`, `sand`
- `insul` (rigid), `sprayfoam`
- `wood`, `ply`, `gyp`
- `stone`, `steel`, `glass`, `ice`
- `none`

## Scales (`scale=`, in inches per foot)

| Use | Scale |
|---|---|
| Window, door, wall, parapet and stair details | `"3"` |
| Eaves, rakes, ridges, curbs | `"1.5"` |
| Handrail profiles | `"6"` |
| Stair plans and sections | `"0.5"` or `"0.375"` |

Text stays the same size at every scale; only the drawing scales.

## API (`scripts/detailkit.py`)

```python
from detailkit import Detail
d = Detail(number, sheet, title, scale="3", jurisdiction="aspen"|"pitkin", project="...")

# geometry - REAL inches, y downward, INT. left / EXT. right
d.rect(x, y, w, h, hatch="conc", edge="cut")
d.poly([(x, y), ...], hatch="wood", edge="cut", closed=True)
d.line([(x, y), ...], style="metal")
d.xbox(x, y, w, h)
d.batt(x, y, w, h)
d.fastener(x, y, length, angle=0)
d.sealant(x, y, d=0.5)
d.break_line(x0, y0, x1, y1)
d.grade(x0, x1, y)

# annotation
d.tag("3B-X", at=(x, y), to=(x, y), sim=False)
d.note("TEXT", to=(x, y), side=None|"left", flag=False)   # flag = item in no assembly
d.keynote("A", "TEXT", to=(x, y))
d.dim((x0, y0), (x1, y1), label=None)
d.elev(x, y, "T.O.F.F. @ MAIN LEVEL", "100' - 0\"", length=12)
d.grid(x, "GL")
d.label(x, y, "INT.")
d.slope(x, y, length, label="1/4\" / FT", direction=-1)
d.callout(x, y, r, number, sheet)
d.general_note("TEXT")     # notes file only
d.verify("TEXT")           # notes file only

d.save(outdir, assemblies="path/assemblies.yaml")   # returns 1 if the checker fails
```

## DXF for Revit

- **Import.** The `.dxf` is full size (1 unit = 1 inch). In Revit: open a drafting
  view, then Insert > Import CAD, colors black and white, units inches, and place
  it.
- **Layers:**
  - `A-DETL-HEVY`, `-MEDM`, `-LITE`, `-HIDN` (dashed), `-MTL`;
  - `A-DETL-MEMB` (blue), `-VAPR`, `-PATT` (hatches);
  - `A-ANNO-NOTE`, `A-ANNO-TAGS`, `A-ANNO-DIMS`, `A-ANNO-GRID`.

  Map them to your line styles on import, or through the object styles afterwards.
- **Text** is 3/32" on paper at the detail scale. Leader notes come in as plain
  text and lines. To match the office text style, retype them from the
  `.notes.txt` file as Revit text, or keep them as placed.
- **Hatches** come in as CAD hatches. Swap them for Revit filled regions if the
  sheet needs the office's patterns.
