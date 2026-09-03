# 02 — ZONING METHOD: the steps, and where to measure

City of Aspen residential zoning submittals. Built from the City's **Complete
Model Zoning Submittal** example set and a full plan-review cycle.
County projects: see §8 at the end — the County measures differently.

**There are no project numbers in this file on purpose.** Every project has a
different lot, different rules, and a different layout. What repeats is the
*method*: what to collect, where to put the tape, what order to do it in.

---

## 0. ORDER OF OPERATIONS — do it in this order or you will redo work

1. **Entitlements first.** Pull every prior land use approval on the parcel
   (P&Z / HPC / Special Review / lot split / variance) and read the dimensional
   table in the resolution. **A resolution cap is the real ceiling.** Zone
   district numbers are only the ceiling when nothing stricter was approved.
2. **Survey second.** You cannot compute Net Lot Area without the surveyor's
   slope analysis, and you cannot compute height without natural grade. Order
   the slope analysis explicitly — it is not automatic.
3. **Measure the geometry ONCE.** One set of CAD polylines per level feeds every
   sheet. (See §1.)
4. **Net Lot Area → Allowable Floor Area.** This sets the budget everything else
   is checked against.
5. **Floor Area** existing and proposed.
6. **Mitigation Floor Area** — same geometry, fewer exemptions.
7. **Demolition** — walls and roof.
8. **Height over topography.**
9. **Site plan, site coverage, summary sheet.**
10. **Self-check** against file 04, then submit.

**Feedback loop to expect:** if the numbers come in over a cap, changing the
design changes grade, and changing grade changes height AND subgrade exposure
AND demolition. Re-run 4 through 8, never just the one sheet.

---

## 1. THE RULE THAT PREVENTS MOST REVIEW COMMENTS

**One measured geometry feeds every sheet.** Measure each level's polylines once.
That single set of gross areas populates the Floor Area sheets, the Mitigation
columns, and the summary. Only the *exemptions applied* differ between them.
Numbers retyped from sheet to sheet spawn variants, and reviewers catch them
instantly ("These numbers do not match").

**The sum test — run it on every level, existing and proposed:**

```
countable area + every tagged exemption = gross area      (exactly, no remainder)
```

If it does not close, there is untagged area on that floor. Find it before the
reviewer does. This one test catches more errors than any other.

**In the spreadsheet:** every total is a cell reference or a formula. Never type
a result. Show the arithmetic in the adjacent cell — the City's own model does
this, and it pre-answers "please show your calculations."

---

## 2. NET LOT AREA AND ALLOWABLE FLOOR AREA

Development rights come from **Net Lot Area**, not gross lot area.

**Collect first:**
- Gross lot area from the survey
- **Slope analysis** from the survey (0–20% / 20–30% / 30–40% / >40%, hatched, with areas)
- Any ROW, vehicular easements, water bodies, dedicated open space on the survey
- Zone district and its allowable-floor-area table
- Any floor area granted or capped by prior approval; any TDRs

**Method — Aspen Table 26.575.020-1.** Two separate results: NLA for **Floor
Area** and NLA for **Density**. Deduct by category (slope bands, area below the
high water line, public and private vehicular ROW/easements). Read the table in
Title 26 for the current percentages — they differ by category and some zone
districts are exempt from the slope reductions.

**Traps in the notes to that table — check every one:**
- Lot area is **not** reduced for **man-made** water features (ditches, ponds).
- Where natural grade was altered by prior development, the Director may accept a
  surveyor's estimate of pre-development topography.
- **The total floor area reduction attributable to slope is capped** — read the
  current cap in the table note and apply it.
- Shared driveway easements and small-parcel access easements have their own
  exceptions.

**Then:** run the zone district's allowable floor area formula on NLA–Floor Area.
Add TDRs or approval bonuses as separate labeled lines. The result is the
Allowable Floor Area. Show the formula text and the citation on the sheet.

**Nonconforming:** if existing countable floor area already exceeds allowable,
the structure is legally nonconforming as to floor area — §26.312.030(c): an
alteration may not increase the nonconformity. Practical test: **proposed
countable ≤ existing countable**. Put that comparison on the summary sheet.
Note also that purposeful Demolition forfeits nonconforming rights entirely.

---

## 3. FLOOR AREA — the three types, and where to measure

§26.575.020(d)(2) defines three. Confusing them is the single biggest source of
wrong sheets.

| Type | What it is | Exemptions applied |
|---|---|---|
| **Gross Floor Area** | all floors, exterior face of framing, unenclosed balconies excluded | **none** |
| **Allowable Floor Area** | what gets checked against the zone district / approval limit | **all** exemptions in (d)(3)–(16) |
| **Mitigation Floor Area** | what drives affordable housing mitigation | all **except** garage (d)(8) and subgrade (d)(9) — those count in full |

Only two exemptions differ between Allowable and Mitigation. **Everything else —
attic, stairs, decks — must be treated identically on both.** A sheet that
exempts an attic on one and counts it on the other is wrong.

### WHERE TO MEASURE — floor area

- **Draw to the exterior face of framing** (or structural block / straw bale).
- **Exclude** sheathing, vapor barrier, weatherproofing membrane, exterior-mounted
  insulation, and **all veneer** — stone, stucco, brick, shingles, clapboard.
  A polyline snapped to the face of stone is wrong and inflates every sheet.
- **Per story.** Where there is no floor structure — an open-to-below void, a
  double-height space — there is **no floor area at that level**. Upper-level
  polylines must exclude existing voids.
- **No exemption exists** for fireplaces, chimneys, or interior wall
  cavities/chases. Anything inside the exterior face of framing counts.
- **At-grade uncovered patios are not floor area at all** — they are outside the
  exterior walls. Keep the row on the chart and show zero.
- **Light wells are not floor area** — they matter only through subgrade
  exposure (below).

### The exemptions that actually come up on a house

**Vertical circulation — (d)(3).** Stairs and elevators are counted on the
**lower** of the two levels connected, and are **not counted at the top-most
interior floor served**. One stacked stairwell = **one** exclusion, at the top.
Two separate runs in different locations are evaluated independently.

**Attic and crawl space — (d)(4).** Exempt only when **unfinished AND
uninhabitable AND accessible only as a matter of necessity**. Access is the
deciding fact, and it is a *per-condition* fact — existing and proposed can
differ, and often do.

| Finish | Access | Result |
|---|---|---|
| unfinished | hatch / pull-down ladder / no access | **exempt** — height is irrelevant |
| unfinished | **door** or fixed stair | **counts** (that is "convenient access") |
| finished | anything | **counts** — removing the door does not cure it |

Also in (d)(4): a low band of attic below a stated clear height is exempt
*regardless of how it is accessed or used*; and a **whole-room rule** — if any
portion of the attic counts, the entire room counts. Read the current subsection
for the exact height. Where a low band sits inside an attic that otherwise
counts, the two rules pull against each other — **get that one in writing.**
Unfinished pockets behind knee walls with no access at all are exempt; tag each
one separately with its own area on the plan.

**Decks, balconies, porches — (d)(5), (d)(6).** An aggregate deck allowance is
computed as a percentage of Allowable Floor Area; only the excess counts.
Railings, fixed seating, and fixed grills count toward deck area. Street-facing
porches within a stated height of finished grade are treated separately.

**Garage — (d)(8).** A tiered exemption: a first block is fully exempt, a second
block is exempt at 50%, everything beyond counts in full. Read the current
numbers in the code. **Show the total garage area first, then the tiers, then the
countable remainder** — the reviewer asks for exactly this. **Not taken for
Mitigation.**

**Subgrade — (d)(9).** The highest-leverage calculation on a residential sheet:

```
Exposed %  =  exposed exterior wall area  ÷  total exterior wall area of that level
Countable  =  subgrade GROSS floor area  ×  Exposed %
```

### WHERE TO MEASURE — subgrade wall exposure

This is worth getting exactly right; it is usually the biggest single lever on a
project that is over its cap.

- **The wall band = the interior wall area projected outward.** Its **top** is
  the **underside of the floor structure above**; its **bottom** is the
  **basement finished floor**. A dropped ceiling does not move the top.
- **Exposed** = the part of that band standing above the **LOWER of natural or
  finished grade** at that location. Below that line is not exposed.
- **At a window well, the finished grade is the top of the well slab.** Raising
  a well slab reduces exposed wall — this is the lever. Its limits: the slab
  cannot rise above the egress sill, the well must still meet building-code
  minimum dimensions, and drainage must still work.
- Wall adjacent to foundation or to floors is excluded from the band.
- A **vaulted ceiling under a pitched roof** — the wall area includes the gable.
- **Garage inside a subgrade level:** take the garage exemption **first** from the
  below-grade gross, then apply the subgrade percentage to the remainder.
- **No exposed wall at all → the level is excluded entirely.**
- **Draw natural AND finished grade across every wall segment diagram.** A fully
  buried wall shows the grade line at or above the top of the segment — that *is*
  the demonstration, and the City asks for it by name.
- **Not taken for Mitigation.**

**Sanity check:** a mostly buried basement produces a *single-digit* exposed
percentage. If you get something near 90%, you have inverted the fraction or
computed the buried portion instead of the exposed one.

---

## 4. MITIGATION FLOOR AREA (affordable housing / GMQS)

**Collect first:** existing and proposed Mitigation Floor Area (same geometry as
FAR, with garage and subgrade exemptions NOT taken), and the demolition
percentage — because the pathway depends on it.

```
Net increase  =  Proposed Mitigation Floor Area  −  Existing Mitigation Floor Area
FTE           =  Net increase  ÷  1,000  ×  (the factor in §26.470.090)
```

| | Demolition NOT triggered | Demolition triggered |
|---|---|---|
| Review | administrative, by right | full GMQS application + allotment |
| Basis | the **net increase** | **no credit for existing floor area** |

Crossing the demolition threshold changes the basis from *net increase* to *the
whole thing*. That is why the demolition number has to be trustworthy before the
mitigation number means anything.

Mitigation options and the fee-in-lieu approval threshold are in §26.470 — read
them; above a stated FTE the fee-in-lieu needs Council approval.

**Where it goes:** Mitigation is normally **not a separate sheet** — it is two
extra columns in the Allowable Floor Area Summary. Provide separate mitigation
plan sheets only if the reviewer asks (they sometimes do), mirroring the floor
area plans.

---

## 5. DEMOLITION — §26.580 — walls and roof

> **The City's own model sheets say, in red:
> "IF YOU ARE TRIGGERING DEMOLITION, DEMOLITION CALCULATIONS ARE NOT REQUIRED."**

The calculation exists to prove you are **under** the threshold. If the project
accepts Demolition and pursues the allotment, skip the calc.

```
Area Used     =  existing exterior WALL assemblies above finished grade
              +  all existing ROOF assemblies
              −  ALL existing fenestration (windows, doors, skylights)

Area Removed  =  the same surfaces being removed

Demolition %  =  Area Removed ÷ Area Used
```

Read the current threshold percentage in §26.580.040 before citing it. (A lower
"documentation" percentage circulates in City checklists that is **not in the
Land Use Code** — confirm against the checklist, don't cite it as code.)

**Collect first:** existing elevations with every wall segment dimensioned ·
existing fenestration schedule or tags per elevation · roof plan with **every
plane's pitch** · demolition plans per level · roof demo plan · finished grade
line on the elevations · **any demolition permitted on this parcel in the last
10 years** (it is cumulative).

### WHERE TO MEASURE — walls

- **Exterior wall assemblies only, and only above finished grade.** Subgrade wall
  never counts. Interior walls never count.
- Measure each wall segment as a **true flat plane** (elevation surface area),
  not a plan dimension.
- "Assembly" means the **structure** — studs, joists, rafters — not the finish.
- **Subtract ALL existing fenestration from BOTH sides of the ratio.** Windows,
  doors, sliding glass units, skylights. This is the column the City flags most
  often, including in its own example set. Pull each value from the CAD elevation
  tags; do not leave the column blank or zero.
- **Removing a wall for a new, relocated, or enlarged opening counts.**
  Replacing an opening in kind does not.
- **Re-skinning does not count.** If the structure stays and only the sheeting is
  replaced, that surface is not demolished — and it stays in the denominator.
  Draw re-skin with a *different hatch* than demolition or the reviewer will read
  the whole building as being demolished.
- **Per-wall invariant:** `Removed ≤ (Wall Area − Fenestration)`. A wall being
  fully demolished has `Removed = Area − Fenestration`, never `= Area`.

### WHERE TO MEASURE — roof

Two accepted methods. **Pick one and use it consistently** — they give slightly
different results, and mixing them is a comment.

**Ratio Method** (measure in plan, correct for slope — no need to draw true planes):

```
Adjustment Factor  =  √(1 + (rise/12)²)
Actual Roof Area   =  plan area (net of fenestration) × Adjustment Factor
```

| Pitch | Factor | | Pitch | Factor |
|---|---|---|---|---|
| flat / 00:00 | 1.0000 | | 8:12 | 1.2019 |
| 1/4:12 | 1.0002 | | 9:12 | 1.2500 |
| 2:12 | 1.0138 | | 10:12 | 1.3017 |
| 3:12 | 1.0308 | | 10.5:12 | 1.3288 |
| 4:12 | 1.0541 | | 12:12 | 1.4142 |
| 6:12 | 1.1180 | | 14:12 | 1.5366 |

**Every plane gets its own factor for its own pitch.** One factor pasted down a
whole column is a classic error — and because the factors look alike, it survives
a casual read.

**Flat Plane Method:** measure each roof segment's true surface area directly.
Simpler table, more drafting.

**Roof element treatment:**

| Element | Treatment |
|---|---|
| **Skylights** | fenestration — deducted from both sides. Demolishing one contributes nothing |
| **New/relocated skylights** cut into roof that remains | that cut area **counts as removed** |
| **Glass roofs / glass canopies** | 100% fenestration — zero to both numerator and denominator. **Mullions and framing are part of the fenestration system** |
| **Chimneys** | not a wall or roof assembly — excluded. Only the parent-plane structure actually cut counts |
| **Dormers demolished** | roof planes go in the roof table with their factor; face and cheek walls go in the wall table, net of their windows |
| **Roof built over, structure remaining** | **not removed** — stays in the denominator |
| **Part of a plane removed** | its own row; that plane's plan area × that plane's factor |

**Exemptions** exist in §26.580.050 (dangerous structures, deed-restricted
affordable housing, de minimus scope, life-safety removals limited to the minimum
necessary, non-historic additions removed per HPC). Any exemption claimed must be
clearly demarcated on the drawings, and the City asks applicants to confirm it
with **comdevzoning@gmail.com** first.

---

## 6. HEIGHT OVER TOPOGRAPHY

**Collect first:** natural grade contours (survey) · proposed finished grade
(civil) · roof plan with **every plane's pitch** · eave and ridge elevations ·
the zone district height limit · the survey benchmark/datum.

### WHERE TO MEASURE — height

- **From the LOWER of natural or finished grade** at each point. Both grade lines
  must be drawn on every elevation, each labeled as more/less restrictive — and
  which one is lower **flips from point to point** on a real site.
- **To the first layer of exterior sheathing or weatherproofing membrane** —
  excluding shakes, shingles, exterior insulation, a second sheathing layer,
  veneer, and ornamentation. **A re-skin therefore does not raise height.**
- **Where on the roof you measure depends on the pitch:**

| Pitch | Measure to |
|---|---|
| under 3:12 | the top-most portion |
| 3:12 to 7:12 | the **1/2 point** between eave and ridge |
| over 7:12 | the **1/3 point** up from the eave |

  For pitched roofs there is **no separate limit on ridge height** — the ridge may
  sit above the height limit line as long as the measured point complies.
  Multiple pitches in one vertical plane, barrel vaults, sheds, mansards, and
  butterflies each have their own rule in §26.575.020(f)(2).
- **Dormers are excluded** from the measurement when their aggregate footprint is
  within the stated share of the roof plane and their ridge is at or below that
  roof's ridge.
- Inside the footprint, points within a stated horizontal distance of the
  perimeter use the perimeter grade; beyond that, natural grade is projected up.

### Deriving a roof point elevation without a 3D model

```
Ridge Elev  =  Eave Elev + (horizontal run eave→ridge × pitch/12)

3:12–7:12   →  Eave + 0.500 × (Ridge − Eave)
   > 7:12   →  Eave + 0.333 × (Ridge − Eave)
   < 3:12   →  use the top-most portion elevation directly
```
In a 3D model, just place a spot elevation on the roof surface at the point's
plan location.

### Height exceptions to know

Chimneys/flues/vents, mechanical equipment (**inclusive of its pad and
screening**), rooftop railings, elevator and stair enclosures, buildings on
slopes, and light wells all have specific allowances in §26.575.020(f)(4) —
**and several of them are expressly NOT available to single-family or duplex**.
Check availability before drawing the allowance, not after.

**A roof below grade** (a green roof over a basement) produces a negative result.
That is correct and compliant — label it "N/A – BELOW GRADE" rather than printing
a bare negative number.

**Put the City's Height Measurement Vignette on the sheet** — the little diagram
showing ridge, 1/2 point, 1/3 point, eave point, and both grade lines. It answers
half the reviewer's method questions before they are asked.

---

## 7. SITE PLAN, SITE COVERAGE, SUMMARY

Existing and proposed site plans show: property line · setback lines with
dimensions · **extent of excavation** · **extent of subgrade space** · contours ·
lot data block · trees · easements with widths · paving types · features to be
removed · north arrow · graphic scale.

Reviewers additionally ask for, every time: **dimensions to window wells** ·
**all hot tubs, pools, outdoor kitchens and grills** (or a statement that there
are none) · **retaining walls with top and bottom of wall elevations** ·
**mechanical and condenser equipment dimensioned from the property lines** ·
**exterior lighting fixtures**.

Fence and driveway height limits within required setbacks are in §26.575.020 /
§26.575.050 — read the current numbers. **Equipment sitting inside a required
setback is a design problem, not a drafting fix.**

The Zoning Summary sheet is the one the reviewer reads first and the one most
often missing. Its full row list is in file 03.

---

## 8. IF THE PROJECT IS IN UNINCORPORATED PITKIN COUNTY

**None of the Aspen sections above apply.** The County has its own Land Use Code
with its own rules of measurement:

| Topic | County section |
|---|---|
| Dimensional standards tables (by zone district) | LUC **§5-10-10** |
| Density reduction for steep slopes | LUC **§5-20-10**, **§5-10-20** |
| **Measurement of building height** | LUC **§5-20-60** |
| **Measurement of floor area** | LUC **§5-20-70** |
| Measurement of gross floor area | LUC **§5-20-80** |
| Setback measurement (road, yard, stream) | LUC **§5-20-30 / -40 / -50** |
| Permitted encroachments into setbacks | LUC **§5-20-100** |
| Growth management / TDRs | LUC **Chapter 6** |
| Non-conformities | LUC **Chapter 9** |
| Definitions | LUC **Chapter 11** |

Several County zone districts run on a **floor area ratio** rather than a sliding
scale, and some measure height to the **top of eave**. Read §5-20-60 and §5-20-70
in full for a County project — do not carry an Aspen method across the city
limit line.
