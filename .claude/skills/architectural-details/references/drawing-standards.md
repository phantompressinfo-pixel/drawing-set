# Drawing standards and detailkit API

These follow the office's existing detail sheets:
- 6/A6.01 and 7/A6.01 on branch `admiring-galileo`;
- the A6.31 stair set on `stair-details-drawings`.

## Graphics

| Element | Standard | detailkit |
|---|---|---|
| Cut material outline | heavy, 2.6 | `edge="cut"` |
| Seen or secondary outline | medium, 1.7 | `edge="med"` |
| Light lines, hatch edges | thin, 1.0 | `edge="thin"` |
| Hidden / beyond | dashed | `style="hidden"` |
| Sheet metal (flashing, panels) | 4.0 solid | `style="metal"` |
| Membranes (underlayment, SA membrane, gasket) | 3.0 solid | `style="membrane"` |
| Air barrier line, when drawn on its own | dash-dot | `style="airbar"` |
| Vapor retarder | short dash | `style="vapor"` |
| Text | Arial, ALL CAPS; notes 17.5 px, tags 21 px bold | automatic |

Hatches (`hatch=`):
- `conc` concrete
- `cmu`
- `earth`
- `gravel`
- `sand`
- `insul` rigid insulation
- `batt` (use `d.batt()`)
- `wood` (sawn, and cut framing)
- `ply` sheathing / plywood
- `gyp`
- `stone` veneer
- `steel`
- `ice`
- `none`

## Symbols

- **Assembly tag**: a heavy box with the tag, and a dot leader into the assembly
  (`d.tag`).
- **Flagged note**: a black square in front of the note. It marks an item that
  belongs to no assembly (`flag=True`).
- **Keynote**: a hexagon with a letter on the drawing; the text goes in the KEYNOTES
  box (`d.keynote`).
- **Elevation target**: a solid triangle with the label (`d.elev`).
- **Enlarged-detail callout**: a dashed circle with a number/sheet bubble
  (`d.callout`), used on wall sections.
- **Title bubble**: number over sheet, the title underlined, then the scale.
  Automatic.
- **EXT. / INT. / CRAWLSPACE**: boxed labels (`d.label`).
- **Break lines** at every edge where the drawing is cut off (`d.break_line`).

## Scales (`scale=` in inches per foot)

| Use | Scale |
|---|---|
| Enlarged profiles (handrails, trim) | `"12"` full, `"6"` half |
| Typical construction details | `"3"`, or `"1.5"` for larger conditions |
| Wall sections | `"0.75"` or `"0.5"` |

Text stays the same size at every scale; only the drawing scales.

## API (`scripts/detailkit.py`)

```python
from detailkit import Detail
d = Detail(number, sheet, title, scale="3", slug=None, jurisdiction="aspen", project="...")

# geometry, all in REAL inches, y downward
d.rect(x, y, w, h, hatch="conc", edge="cut")
d.poly([(x, y), ...], hatch="none", edge="med", closed=True)
d.line([(x, y), ...], style="metal")
d.batt(x, y, w, h)
d.fastener(x, y, length, angle=0)
d.sealant(x, y, d=0.5)
d.break_line(x0, y0, x1, y1)
d.grade(x0, x1, y)

# annotation
d.tag("W1", at=(x, y), to=(x, y))
d.note("TEXT", to=(x, y), side=None|"left"|"right", flag=False, dash=False)
d.keynote("A", "TEXT", to=(x, y))
d.dim((x0, y0), (x1, y1), label=None)        # label defaults to the measured length
d.elev(x, y, "T.O. SLAB")
d.slope(x, y, length, label="SLOPE - SEE ROOF PLAN", direction=-1)
d.label(x, y, "EXT.")
d.callout(x, y, r, number, sheet)
d.general_note("TEXT")
d.verify("TEXT")

d.save(outdir, assemblies="path/assemblies.yaml")   # returns 1 if the checker fails
```

- **Layout.** Leader notes stack in two columns, sorted by target height. The default
  puts each note on the side nearer its target. Send exterior items left and interior
  items right with `side=` so leaders don't cross.
- **PNG.** Rendered with headless Chromium, found under `/opt/pw-browsers` or through
  `CHROMIUM=`. If it isn't available, the SVG is still the drawing.
- **Checker.** Run it on its own at any time:
  `python3 scripts/check_notes.py details/<file>.json --assemblies <project>/assemblies.yaml`.
