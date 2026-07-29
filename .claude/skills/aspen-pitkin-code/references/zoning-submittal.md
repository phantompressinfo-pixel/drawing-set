# Aspen Residential Zoning Submittal — Sheets, Charts, Equations, Citations

Working reference for City of Aspen residential zoning submittals. Built from (a) the City's
**Complete Model Zoning Submittal** example set (14 sheets, updated 04.21.2026), including the
red **Staff Notes** the City embeds in it, and (b) a full plan-review cycle with reviewer
comments. Examples' numbers are illustrative — the sheet list, formats, equations, citations,
legends, and self-checks are the reusable part.

**Get the current example set from the City website before starting.** It is dated and
periodically revised. Also request the **zoning checklist** and **engineering survey
checklist** — the model set repeatedly refers to them and they carry requirements not shown
on the sheets. For demolition-exemption questions the City directs applicants to
**comdevzoning@gmail.com**.

⚠️ The model set contains internal errors (totals that disagree between its own sheets,
duplicate row labels, an NLA column that doesn't foot, outdated subsection lettering like
`26.575.020.D.5` for what is now `(d)(5)`). **Match the current code text; copy the model's
structure, not its arithmetic.**

---

## 0. THE COMPLETE SHEET SET

The City model runs 14 sheets. Every sheet carries the architect's stamp, consultant block,
date of publication table, and sheet number.

| # | Sheet | Contents |
|---|---|---|
| 1 | **Roof Demolition Calculations** | Ratio Method **or** Flat Plane Method table, roof plane diagrams, roof demo legend, demo reference plan |
| 2 | **Zoning Summary** | Zoning Allowance & Project Summary · Net Lot Area · Allowable Floor Area Summary |
| 3 | **Survey** (by surveyor) | Monumented Land & Improvement Survey w/ vicinity map, legend, buried utilities, surveyor's cert + notes, legal description, flood statement, **slope analysis**, benchmark/datum |
| 4 | **Existing Site Plan** | property line, setback line, extent of excavation, contours, lot data block |
| 5 | **Proposed Site Plan** | same + extent of subgrade, easements, paving, dimensions to setbacks |
| 6 | **Site Coverage** | table (existing/proposed) + building footprint diagrams |
| 7 | **Wall Demolition Calculations** | wall table, flat-plane wall segment diagrams, exposed wall legend, wall demo reference plans per level |
| 8 | **Floor Area Calculations — Existing** | per-level tables + total, floor area plans with areas labeled on plan |
| 9 | **Floor Area Calculations — Proposed** | same + subgrade exposed wall table, subgrade wall diagrams, subgrade legend |
| 10–13 | **Heights** (4 elevations) | one elevation per sheet, fully annotated |
| 14 | **Height Over Topography** | table (For Permit + For As-Built Survey), roof plan with numbered points, **Height Measurement Vignette** |

Mitigation Floor Area is **not a separate sheet** in the model — it is two extra columns in
the Allowable Floor Area Summary (see §2). Provide the separate Mitigation plan sheets only
if the reviewer asks (they sometimes do).

---

## 1. THE RULE THAT PREVENTS MOST COMMENTS

**One measured geometry feeds every sheet.** Measure each level's polylines once in CAD; that
single set of gross areas populates the Floor Area sheets, the Mitigation columns, and the
summary. Only the *exemptions applied* differ. Numbers retyped between sheets spawn variants
that reviewers catch instantly ("These numbers do not match").

**The sum test — run it on every level, both existing and proposed:**
```
countable area + every tagged exemption = gross area     (exactly, no remainder)
```
If it doesn't close, there is untagged area on that floor.

**Staff Note, verbatim: "please include a floor area legend on every page."**

---

## 2. SHEET 2 — ZONING SUMMARY

Three tables. This is the sheet the reviewer reads first, and the one most often missing.

### 2a. Zoning Allowance & Project Summary

| Block | Rows |
|---|---|
| Header | Address · Proposed Use · Zone District · Parcel # |
| Overlays | Planned Development · Environmentally Sensitive Area · Historically Designated Property |
| Scope | Scope of Work |
| **Setbacks** | Front · Rear · Combined Front/Rear · Side · Combined Side — columns: **Allowed (Principal) · Allowed (Accessory) · Reference** |
| **Height** | Building Height — Allowed · Reference |
| **Supplemental Information** | Net Leasable · Pedestrian Amenity · Site Coverage · On-Site Parking · Distance between Buildings — columns: **Existing · Required · Proposed · Reference** |
| **Unique Approvals** | Details · Reference · **Reception #** |
| **Variances** | Details · Reference · Reception # |
| **Deed Restrictions** | Details · Reference · Reception # |
| **Nonconforming Use or Structure** | Details · Reference |
| **Demolition** | Demolition Area (sq ft) · Existing Roof & Wall Area (sq ft) · Demolition Percentage · **"Any other demo since 2022?"** |
| **Transferable Development Right (TDR)** | Previously Extinguished TDR? · Proposed Extinguished TDR? · TDR Sending Site? |

The "**Any other demo since 2022?**" row is how the City administers the **10-year cumulative
demolition rule** (§26.580.040(d)) — 2022 being the ordinance date. Answer it honestly;
prior permits stack.

Use "N/A" or "None" rather than blanks — the model does.

### 2b. Net Lot Area — Table 26.575.020-1

Development rights derive from **Net Lot Area**, not gross lot area. Two separate NLA results
are computed: one for **Floor Area**, one for **Density**.

| Area of parcel | % included for **Floor Area** | % for **Density** |
|---|---|---|
| 0% to 20% slope | 100% | 100% |
| >20% and up to 30% slope | **50%** (R-15B: 100%) | 100% |
| >30% slope | **0%** (R-15B: 100%) | 100% |
| Below high water line of a river or natural body of water | 0% | 0% |
| Dedicated to City/County for open space or public trail | 100% | 100% |
| Public vehicular ROW, public vehicular easement, or emergency access easement | 0% | 0% |
| Private vehicular ROW or vehicular easement (dedicated / proposed) | 0% | 0% |
| Vacated private vehicular ROW/easement — affected parcel has **no** other access | 0% | 0% |
| Vacated private vehicular ROW/easement — all affected parcels **have** alternate access | 100% | 100% |
| Above/below ground surface easements (utilities, irrigation ditch) not coinciding with vehicular easements | 100% | 100% |

**Notes to the table — each one is a trap:**
1. Lot Area is **not** reduced for **man-made** water courses or features (ditches, ponds).
2. Where natural grade was altered by prior development, the Director may accept a surveyor's
   or engineer's estimate of **pre-development topography**.
3. **The total Floor Area reduction attributable to slope shall not exceed 25%.** ← cap
4. Shared driveway easement where both properties abut a public ROW → **not deducted**.
5. Parcel ≤9,000 sf with a private vehicular access easement serving no more than one back
   parcel that has no other access → **not deducted** (Floor Area or density).
6. Lodge zone: vehicular ROW/easement vacated before Ord. 11, Series 1975 → not deducted.

Sheet layout: Gross Lot Area per Survey · Zone District Requirements (Minimum Gross Lot Area,
Minimum Net Lot Area per Dwelling Unit) · the table above with columns **Area (sq ft) | NLA –
Floor Area (sq ft) | NLA – Density (sq ft)** · **Total Net Lot Area** for both.

The **slope analysis on the survey** (0–20 / 20–30 / 30–40 / >40% hatched, with areas) is the
source for the slope rows — coordinate with the surveyor early.

### 2c. Allowable Floor Area Summary — the six-column table

| Allowable Floor Area | | Reference |
|---|---|---|
| Zone District Allowable Floor Area Calculation | [formula text from the zone district] | 26.710.0xx.d.10 |
| Unique Approvals | [lot split / HPC bonus / etc.] | Resolution #, Series |
| **Allowable Floor Area** | **[result]** | |

| Floor Area Summary | Existing Gross (sf) | **Existing Mitigation** | Existing Floor Area | Proposed Gross | **Proposed Mitigation** | Proposed Floor Area |
|---|---|---|---|---|---|---|
| Subgrade Level | | | | | | |
| Lower Level | | | | | | |
| Garage | | | | | | |
| Main Level | | | | | | |
| Upper Level | | | | | | |
| Deck Area | | | | | | |
| ADU | | | | | | |
| **Total (sq ft)** | | | | | | |

**Mitigation Floor Area lives here as two columns — not on a separate sheet.** This is the
cleanest answer to the "please add mitigation floor area existing vs proposed" comment.
Because garage and subgrade exemptions are **not taken** for mitigation, the Mitigation column
equals Gross for most residential rows.

---

## 3. SHEET 6 — SITE COVERAGE

| Site Coverage | Gross Lot Area (sf) | Site Coverage (sf) | Site Coverage (%) |
|---|---|---|---|
| Existing | | | |
| Proposed | | | |

Plus existing and proposed diagrams showing **BUILDING FOOTPRINT [area] / COVERAGE = [%]**
against the lot outline with gross lot size labeled. Note: R-15 has **no site coverage
requirement** ("Not req'd for R-15A" in the model) — but the sheet is still provided.

---

## 4. FLOOR AREA — the three types

§26.575.020(d)(2) defines three. Confusing them is the biggest source of wrong sheets.

| Type | Definition | Exemptions applied |
|---|---|---|
| **Gross Floor Area** | total horizontal area of all floors, exterior face of framing, excluding unenclosed balconies | **none** |
| **Allowable Floor Area** | checked against the zone district limit | **all** of (d)(3)–(16) |
| **Mitigation Floor Area** | assesses affordable housing mitigation | all **except** garage (d)(8) and subgrade (d)(9) — those count **in their entirety** |

The (d)(2)(a)(iii) table lists exactly two elements not exempted for Mitigation Floor Area:
**garages/carports (d)(8)** and **subgrade areas (d)(9)**. Everything else — attic (d)(4),
vertical circulation (d)(3), decks (d)(5), airlocks (d)(16) — applies **identically to both**.
A sheet that exempts an attic on one and counts it on the other is wrong.

### Measurement basis — §26.575.020(d)(1)
**Exterior face of framing** (or structural block/straw bale), **excluding** sheathing, vapor
barrier, weatherproofing membrane, exterior-mounted insulation, and all veneer/surface
treatments (stone, stucco, brick, shingles, clapboard).

### Sheet 8/9 table structure (per the model)

```
Existing [Level] Floor Area Calculations
  [Level] Gross Floor Area (Sq Ft)            xxx
  [Level] Countable Floor Area (Sq Ft)        xxx     ← bold/shaded

Existing Deck/Porch Floor Area Calculations
  Front Porch Gross Floor Area                xxx     "Exempt per 26.575.020(d)(6)"
  Deck Gross Floor Area                       xxx     "Exempt per 15% of allowable"
  Structural Steps Floor Area                 xxx     ← counts toward deck
  Exempt Deck Floor Area                      xxx     "(allowable × 15%)"
  Deck/Porch Countable Floor Area             xxx     "(Deck + Steps − Exempt)"

[Proposed] Subgrade Level Exposed Wall Calculations
  Subgrade Level Wall Label | Total Wall Area | Exposed Wall Area
  Overall Total Wall Area / Exposed Wall Area / % of Exposed Wall (Exposed / Total)

[Proposed] Subgrade Floor Area Calculations
  Subgrade Gross Floor Area                   xxx
  Subgrade Countable Floor Area               xxx     "(gross × exposed %)"  ← show the math

Total [Existing/Proposed] Floor Area Calculations
  Subgrade / Lower Level / Main Level / Upper / Garage / Deck-Porch / Total
```
Show the arithmetic in an adjacent cell — the model does (`(1,702.75 x 2.25%)`,
`(529.25+18 – 261.75)`). That single habit answers "Please show your calculations."

**Label areas directly on the floor area plans:** `776.75 sq ft INTERIOR SPACE`,
`59.00 sq ft EXEMPT FRONT PORCH`, `90.00 sq ft EXEMPT DECK`.
Subgrade wall segments are labeled with **numbers (1–9)** in the model, not letters.

### Exemptions that matter on residential sheets

**(d)(3) Vertical circulation** — stairs/elevators counted on the **lower** of the two levels
connected; **not counted on the top-most interior floor served**. Multi-level run: counted on
all levels as if solid floor except the top-most. Elevator overrun above the top stop and area
below the lowest stop not counted.
*Two separate runs (basement→main, break, main→upper) are evaluated independently — the main
level can have one stair footprint counted and another excluded at two different locations.
**One stacked stairwell = one exclusion, at the very top level served.*** Ask if ambiguous.

**(d)(4) Attic and crawl space** — exempt when **unfinished and uninhabitable** AND
**accessible only as a matter of necessity**.
1. Crawl exempt if ≤6 ft high AND hatch/access-panel only AND minimum size for mechanical.
   Stacked crawls don't qualify; crawl >6 ft counts under (d)(9).
2. *"Attic space that is conveniently accessible and is either habitable or can be made
   habitable shall be counted."* — an AND test.
3. *"Areas of an attic level with thirty (30) vertical inches or less between the finished
   floor level and the finished ceiling shall be exempt, **regardless of how that space is
   accessed or used**."*
4. **Whole-room rule:** *"If any portion of the attic or crawl space of a structure is to be
   counted, then **the entire room** shall be included."*

   | Finish | Access | Result |
   |---|---|---|
   | unfinished | hatch / pull-down ladder / none | **exempt** (height irrelevant) |
   | unfinished | door, fixed stair | **counts** (the ">4 ft + convenient access" example) |
   | finished | any | **counts** — removing the door does not cure it |

   **Rule 3 vs. rule 4 tension:** in an attic that otherwise counts, does the ≤30" band stay
   exempt? Better reading: rule 4 prevents carving by *finish/habitability*, rule 3 carves by
   *geometry* — different axes; reading 4 to swallow 3 makes 3 surplusage. **Ambiguous — get
   it in writing.** Appeal path §26.575.020(k).

   Unfinished pockets behind knee walls with **no access at all** satisfy the exemption a
   fortiori and are usually also ≤30". Tag each individually with its own area.

**(d)(5) Decks, balconies, loggias, gazebos, trellis, exterior stairways, non-street porches**
```
Deck threshold = Allowable Floor Area × 0.15        (aggregate; only the excess counts)
Deck countable = Deck + Structural Steps − Exempt threshold
```
Railings, permanently fixed seating, and fixed grills count toward deck area. Permanent
planters/green roofs ≥30" above or below the deck surface and built into the structure do not.
Unenclosed area beneath decks exempt unless a carport. Enclosed unconditioned area beneath
porches/gazebos/decks with finished floor within 30" of grade exempt regardless of use.

**(d)(6) Front porches** — street-facing, within 30" of finished ground level, not counted;
otherwise treated as a Deck.

**(d)(8) Garages and carports**
```
Exempt    = 250 + (min(max(Garage − 250, 0), 250) × 0.50)      → 375 max
Countable = Garage total − Exempt
```
**Not taken for Mitigation Floor Area.**

**(d)(9) Subgrade areas** — highest-leverage calculation on a residential sheet
```
Exposed %  = exposed exterior wall area above the LOWER of natural or finished grade
             ÷ total exterior wall area of that level
Countable  = subgrade gross floor area × Exposed %
```
- No exposed wall → level excluded entirely.
- Wall area = **interior wall area projected outward**, excluding wall adjacent to foundation
  or floors. Drop ceilings not included in crawl height.
- **Light-well-exposed wall counts as exposed** — wells added for egress or height reasons
  increase countable basement area here. Flag this cross-sheet tension early.
- Multi-level subgrade: same story if vertical separation between ceilings is <50% of either
  space's floor-to-ceiling height.
- Vaulted ceiling in a pitched roof: wall area **includes the gable area**.
- **Garage within a subgrade level:** take the garage exemption **first** from the gross
  below-grade area, then apply the subgrade percentage to the remainder.
- Adjoining exempt crawl: draw a separating line; exempt crawl excluded from perimeter, wall
  area, and floor area.
- Single-family/duplex: **one floor level below finished grade** max; finished floor ≤**15 ft**
  below finished grade (exempt crawl below basement doesn't count toward the depth limit).
- **Not taken for Mitigation Floor Area.**
- **Staff Note, verbatim: "Include natural and finished grade on these subgrade diagrams."**
  Draw both grade lines across each wall segment. A fully-buried wall shows the grade line at
  or above the top of the segment — that *is* the demonstration.
- **SUBGRADE CALCULATIONS LEGEND: EXPOSED WALL / WALL BELOW GRADE**

**(d)(16) Airlocks** — exempt up to 100 sf per building.

### Not floor area at all
- **At-grade uncovered patios** — §26.104.100 defines Patio as "an outdoor uncovered, at-grade
  space." Outside the exterior walls → never floor area. Keep the row, show **0.00**.
  A *covered* patio not connected to a building is a **Gazebo**; attached, it behaves as a
  porch — either way it moves into (d)(5)/(d)(6).
- **Light wells / areaways** — outdoor uncovered space below grade. Never floor area; they
  matter only indirectly via exposed wall area in (d)(9).

### Allowable Floor Area — R-15 sliding scale, §26.710.050(d)(10)
| Net Lot Area (sf) | Allowable Floor Area, single-family |
|---|---|
| 0 – 3,000 | 80 sf per 100 sf NLA, max 2,400 |
| 3,000 – 9,000 | 2,400 + 28 sf per additional 100 sf, max 4,080 |
| 9,000 – 15,000 | 4,080 + 7 sf per additional 100 sf, max 4,500 |
| 15,000 – 50,000 | 4,500 + 6 sf per additional 100 sf, max 6,600 |
| 50,000 + | 6,600 + 2 sf per additional 100 sf |

Duplex / two detached column is higher — read the actual zone district table. Other districts
(R-6, R-15A, R-15B, R-30, RR…) have their own tables at §26.710.0xx(d).

**TDRs:** +250 sf per extinguished historic certificate; non-historic lots ≥15,000 sf with only
a single-family residence may extinguish up to two. **Nonconforming structures are not
eligible.**

### Nonconforming floor area — §26.312.030
If existing countable exceeds allowable, the structure is legally nonconforming as to floor
area. §26.312.030(c): *"shall not be extended by an enlargement or expansion that increases
the nonconformity."* Practical test: **proposed countable ≤ existing countable**. Put the
comparison on the summary sheet. §26.312.030(f)(2): purposeful **Demolition** forfeits the
nonconforming rights entirely — so crossing 40% has floor-area consequences too.

---

## 5. MITIGATION FLOOR AREA (GMQS affordable housing)

| | Demolition **not** triggered (<40%) | Demolition triggered (≥40%) |
|---|---|---|
| Review | administrative, by-right — §26.470.090(a) | full GMQS application + allotment — §26.470.090(c) |
| Basis | **net increase** of Mitigation Floor Area | **no credit for existing** — §26.470.140(b) |
| Also | — | Residential Demolition & Redevelopment Standards §26.580.080; §26.312.030(f)(2) |

```
Net increase = Proposed Mitigation Floor Area − Existing Mitigation Floor Area
FTE          = Net increase ÷ 1,000 × 0.107
```
Options — §26.470.090(a)(3): RO deed restriction · AH unit ≥30% of the floor area increase,
Category 2 or lower · fee-in-lieu or Certificate of Affordable Housing Credit · deferral
agreement for a qualified full-time local working resident (§26.470.080(d)(13)).
**Fee-in-lieu above 0.10 FTE requires City Council approval** — §26.470.110(c).

Report it in the Allowable Floor Area Summary's Mitigation columns (§2c). If separate
Mitigation plan sheets are requested, mirror the Floor Area plans and add:
```
PROJECT DOES NOT MEET THE DEFINITION OF DEMOLITION: TOTAL EXTERIOR WALL + ROOF SURFACE AREA
REMOVED = __% < 40% PER §26.580.040 (SEE DEMOLITION CALCULATIONS, SHEETS __). MITIGATION
BASED ON NET INCREASE OF MITIGATION FLOOR AREA PER §26.470.090(a). GARAGE AND SUBGRADE
EXEMPTIONS NOT TAKEN PER §26.575.020(d)(2)(a)(iii).
```

---

## 6. DEMOLITION — §26.580.040

> **Model set header, verbatim (red, on both demo sheets):**
> ***"IF YOU ARE TRIGGERING DEMOLITION, DEMOLITION CALCULATIONS ARE NOT REQUIRED."***

If the project accepts Demolition and pursues the allotment, skip the calc entirely. The
calculations exist to *prove you're under* 40%.

- **40% = "Demolition"** — §26.580.040(a)(3). The only percentage in the adopted code text.
  A **35% documentation trigger** circulates in City checklists but is **not in the Land Use
  Code** — confirm against the current checklist rather than citing it as code.

```
Area Used    = existing exterior WALL assemblies above finished grade
             + all existing ROOF assemblies
             − ALL existing fenestration (doors, windows, skylights)
Area Removed = the same surfaces being removed
Demolition % = Area Removed ÷ Area Used
```

### Counting rules — §26.580.040(c)
| Rule | Effect |
|---|---|
| (c)(1) | "Assembly" = exterior surface **including studs, joists, rafters** — structure, not finish |
| (c)(2) | Any portion of a wall/roof **stud or rafter** removed → that surface area diagrams as removed |
| (c)(3), (b)(2) | **Involuntary collapse counts**, regardless of intent |
| (b)(3) | Health/safety removals discovered after work begins are excluded — requires Chief Building Official inspection |
| (c)(4) | Zoning Officer may require **recalculation** as work progresses |
| (c)(5) | Wall/roof removed for **new, relocated, or expanded** fenestration **counts**; **in-kind replacement does not** |
| (c)(6) | **Only above finished grade** — subgrade and interior never count |
| **(c)(7)** | **"Replacement of exterior sheeting when the structural components of that area are to remain, does not count"** — the re-skin rule; also covers roof planes **built over** with structure remaining |
| (c)(9) | Separate calculation per detached structure; attached duplex = one structure |
| (d) | **Cumulative over 10 years** — the Zoning Summary's "any other demo since 2022?" row |

### Two acceptable roof methods — the model shows both with "OR" between them

**Ratio Method** (plan area × slope factor — no need to draw true flat planes)
| Roof Label | Individual Roof Area in Plan (Sq Ft) | Roof Slope | Adjustment Factor | Actual Area of Roof Used for Demo Calc (Sq Ft) | Area of Roof to be Removed (Sq Ft) |

```
Adjustment Factor = √(1 + (rise/12)²)
Actual Roof Area  = plan area (net of fenestration) × factor
```
Model note, verbatim: *"Actual area of roof to be removed is calculated by multiplying the
plan area by an adjustment factor, in lieu of depicting each roof segment as a flat plane.
The adjustment factor is determined by a ratio of the roof slope."*

Roof slopes are written **`04:12`, `12:12`, `00:00`** (flat) in the model.

| Pitch | Factor | | Pitch | Factor |
|---|---|---|---|---|
| flat / `00:00` | 1.000 | | 8:12 | 1.2019 |
| 1/4:12 | 1.0002 | | 9:12 | 1.2500 |
| 2:12 | 1.014 | | 10:12 | 1.3017 |
| 3:12 | 1.0308 | | 10.5:12 | 1.3288 |
| 4:12 | 1.054 | | 12:12 | 1.414 |
| 6:12 | 1.118 | | 14:12 | 1.5366 |

*(1.5366 is the **14:12** factor — a plausible-looking wrong constant to find pasted down a column.)*

**Flat Plane Method** (measure each roof segment's true area directly)
| Roof Label | Individual Roof Area (Sq Ft) as Flat Plane | Area of Roof to be Removed (Sq Ft) |

Simpler table, more drafting. The two methods give slightly different results (43.47% vs
43.71% in the model) — pick one and use it consistently.

### Wall demolition table
| Wall Label | Individual Wall Area (Sq Ft) | **Fenestration Area (Sq Ft)** | Area of Wall to be Removed (Sq Ft) |
```
Wall Surface Area Total         = Σ col 2
Fenestration Area Total         = Σ col 3
Area Used for Demo Calculation  = Total − Fenestration
Wall Surface Area to be Removed = Σ col 4
```
**Per-wall invariant:** `Removed ≤ (Wall Area − Fenestration)`. A fully-demolished wall with
openings has `Removed = Area − Fenestration`, never `= Area`.

> **Staff Note on the City's own example, verbatim: "this column is not correctly filled out —
> this column should be filled out if there is existing fenestration."**

The City flags the empty fenestration column **in its own model set**. It is the single most
common defect. Pull each value from the CAD elevation tags.

### Demolition Totals block
```
Roof + Wall Area Used for Demo Calculation = [roof Area Used]    + [wall Area Used]
Surface Area to be Removed                 = [roof Area Removed] + [wall Area Removed]
Total                                      = Removed ÷ Used
```
**Every component a cell reference to a table on the sheet.** The model's own two sheets
disagree (1,388.75 vs 1,422.95 for the same roof) because these were typed.

### Legends — four distinct ones, don't mix them
| Legend | Entries |
|---|---|
| **ROOF DEMO LEGEND** | EXISTING ROOF TO REMAIN / ROOF TO BE REMOVED |
| **WALL DEMO LEGEND** (reference plans) | EXISTING TO REMAIN / WALL TO DEMOLISH |
| **EXPOSED WALL LEGEND** (segment diagrams) | EXISTING WALL TO REMAIN / WALL AREA TO BE REMOVED / **AREA REDUCED FOR FENESTRATION** |
| **SUBGRADE CALCULATIONS LEGEND** | EXPOSED WALL / WALL BELOW GRADE |

Staff Notes: *"Marking aligned with legend — this grey area is area reduced for fenestration"*
and *"Please clearly demarcate any exempt demolition area on the roof and wall drawings. Refer
to 26.580 for exemptions — if you believe portions of the project meet the criteria, please
reach out to **comdevzoning@gmail.com** for confirmation."*

For a re-skin project the reviewer will comment if siding replacement is drawn in the same
graphic as demolition. Use separate hatches for: elements demolished · exterior walls
demolished · interior walls demolished · exterior wall material to sheathing · exterior siding
· roof material to sheathing · floor.

### Element-by-element
| Element | Treatment |
|---|---|
| **Skylights** | fenestration — deducted; demoing one counts as nothing. New/relocated skylights cut into remaining roof **do** count as removed per (a)(2)(b) |
| **Glass roofs** | 100% fenestration — zero to numerator and denominator. **Mullions/framing are part of the fenestration system** |
| **Chimneys** | not wall or roof assemblies — excluded per (a)(1), (c)(1). Only parent-plane structure cut counts. A framed chimney *chase* is arguable — ask |
| **Dormers demolished** | roof planes → roof table (with factor); face and cheek walls → wall table (net of the window) |
| **Roof built over, structure remaining** | **not removed** per (c)(1)–(2), (c)(7); stays in the denominator |
| **Partial plane removal** | its own row; plan area × that plane's factor |

### Exemptions — §26.580.050 (Director may grant)
dangerous/unsafe structures · 100% deed-restricted affordable housing · de minimus scope ·
temporary relocation and replacement on a foundation · removals required for normal maintenance
or life-safety (e.g. a failing roof), limited to the minimum necessary · removal of non-historic
additions to designated landmarks per HPC.

---

## 7. HEIGHT — SHEETS 10–14

### Governing sections
- **Max height** — zone district table, e.g. R-15 §26.710.050(d)(7). Model cites `26.710.060.D.7` (R-15A).
- **Measurement method** — §26.575.020(f), written `26.575.020.F` on sheets.

### Measurement by pitch — §26.575.020(f)(2)
| Condition | Measure to |
|---|---|
| CC, C-1, CL, NC, SCI | top-most point of roof/ridge/parapet — (f)(1) |
| All other zones, < 3:12 | top-most portion |
| 3:12 – 7:12 | **1/2 point** eave-to-ridge — **no limit on ridge height** |
| > 7:12 | **1/3 point** up from eave — **no limit on ridge height** |
| Multiple pitches in one vertical plane | line ridge→eave point, apply resulting pitch |
| Barrel vault | line top-most→eave point, apply resulting pitch |
| Shed | as above, highest point = ridge |
| Mansard | measure to the flat roof |
| Butterfly | shed methodology |
| Dormers | **excluded** if footprint ≤50% of the roof plane (aggregate) AND dormer ridge ≤ that roof's ridge |

### Method — §26.575.020(f)(3)
- **(a)** measured from the **lower of natural or finished grade** at each location; *"Building
  permit plans must depict both natural and finished grades."*
- **(b)** within the footprint, areas within **15 horizontal ft** of the perimeter use the
  perimeter measurement; elsewhere project natural grade up.
- **(c)** measured to the **first layer of exterior sheathing or weatherproofing membrane**,
  **excluding** shakes, shingles, fireproofing, exterior insulation, second sheathing layer,
  veneer, ornamentation. → **the re-skin rule.** Eave point = roof plane ∩ exterior wall plane,
  **nominal structure**, excluding exterior treatments.

### Exceptions — §26.575.020(f)(4)
| Item | Allowance | Sheet citation |
|---|---|---|
| a. Chimneys, flues, vents | **10 ft** above the building at the point of connection. Pitch **≥8:12**: may not exceed the highest ridge by more than building code requires. Caps/shrouds/spark arrestors **contained within** the allowance | 26.575.020.F.4.A |
| c. Elevator/stair enclosures | +5 ft (+10 ft if set back 20 ft from street façade) — **NOT for single-family, duplex, or accessory** | F.4.C |
| d. Rooftop railings | +5 ft, ≥50% transparent — **NOT for single-family or duplex**. Model labels these "ROOFTOP GUARD PER 26.575.020.F.4.D" and "GREEN ROOFTOP GUARD PER 26.575.020.F.4.D" | F.4.D |
| e. Mechanical equipment | **+6 ft** at the point of attachment, **inclusive of pad and screening** | 26.575.020.F.4.E |
| i. Buildings on slopes | lot declining ≥10% from front lot line: max height of the street-facing façade may extend horizontally the first 10 ft of building depth | F.4.I |
| j. Lightwells & basement stairwells | egress basement stairwell not counted. **Street-facing:** minimum-size lightwell entirely recessed behind the street-facing façade plane and enclosed to within 18" of first floor level (not walk-out) not counted. **Non-street-facing:** ≤100 sf not counted. **Does not apply to lightwells within a setback.** HPC may exempt >100 sf on landmarks | 26.575.020.F.4.J |
| k | decorative elements CC/C-1/NC, 24", w/ Commercial Design Review | F.4.K |
| m | skylights and light tubes | F.4.M |

### Height Over Topography table — the model's exact column set

**For Permit:**

| Elevation Label | Maximum Height | Elevation of Natural Grade | Elevation of Finished Grade | Most Restrictive | Roof Height over Topography | Proposed Roof Height over Most Restrictive |

**For As-Built Survey** (blank until post-construction, typically a CO condition):

| Actual Elevation of Finished Grade | Actual Most Restrictive | Actual Roof Height over Topography | Actual Roof Height over Most Restrictive |

- **Maximum Height** = the zone district limit, same every row unless a documented exception.
- **Elevation of Natural / Finished Grade** = *ground* elevations at that XY point.
- **Most Restrictive** = the **word** "Natural" or "Finished" — whichever elevation is **lower**.
  It flips point-to-point (the model's own example has both).
- **Roof Height over Topography** = the **actual elevation of the tagged roof measurement
  point** — a building elevation, not a height.
- **Proposed Roof Height over Most Restrictive** = the real height, checked against Maximum Height:
```
= Roof Height over Topography − (elevation of whichever grade is Most Restrictive)
```

Deriving the roof point elevation without a 3D model:
```
Ridge Elev = Eave Elev + (horizontal run eave→ridge × pitch/12)
3:12–7:12 → Eave + 0.50 × (Ridge − Eave)
   >7:12  → Eave + 0.333 × (Ridge − Eave)
   <3:12  → use the top-most portion elevation directly
```
In a 3D model, place a spot elevation on the roof surface at the point's plan location.

**Below-grade roofs** (green roof over basement) give a negative result — correct and
compliant. Label **"N/A – BELOW GRADE"**, not a bare negative, and note it on the roof plan.

### Height Measurement Vignette
The model puts a small diagram in the corner of the Height Over Topography sheet showing:
RIDGE · **1/2 POINT BETWEEN RIDGE & EAVE (FOR PITCH FROM 3:12 TO 7:12)** · **1/3 POINT BETWEEN
RIDGE & EAVE (FOR PITCH GREATER THAN 7:12)** · EAVE POINT · ROOF HEIGHT dimensions ·
**FINISHED GRADE (LESS RESTRICTIVE)** and **EXISTING/NATURAL GRADE (MOST RESTRICTIVE)**.
Include it — it answers half the method questions before they're asked.

### What the Height Over Topography roof plan shows
Numbered height point tags (diamond markers) · pitch labels at each plane · **MECHANICAL
PLATFORM** · **ROOF VENT** · **ROOF DRAIN** · **WASTE VENT 12" MIN. HEIGHT** · **CHIMNEY
PROJECTION 10' MAX FROM HEIGHT OF BUILDING CONNECTION PER 26.575.020.F.4.A** · GREEN ROOF DECK ·
**T.O. WALL @ PLANTER / @ DRIVEWAY / @ PATIO with elevations** · **FENCE NOT TO EXCEED 6' ABOVE
DRIVEWAY / ABOVE FINISH GRADE** · LINE OF EXISTING TOPOGRAPHY, TYP · LINE OF SETBACK · PROPERTY
LINE · labeled contours · dimensions.

### What each Height elevation sheet shows
- **ZONE DISTRICT HEIGHT LIMIT PER 26.710.0xx.D.x** — drawn as a line **following the grade
  profile**, not horizontal, with the 25'-0" dimension shown
- **LINE OF SETBACK @ [NORTH/SOUTH/EAST/WEST] ELEVATION** — dashed
- **Both grade lines**, labeled **NATURAL GRADE (MORE RESTRICTIVE)** and **FINISHED GRADE
  (LESS RESTRICTIVE)** — and the model shows the designation reversing on other elevations,
  so label per condition
- Measurement point tags with **pitch triangles**: `1/3 POINT FROM EAVE TO RIDGE`,
  `1/2 POINT FROM EAVE TO RIDGE`, `TOP-MOST PORTION`, `RIDGE @ EXISTING ROOF`,
  `EAVE @ EXISTING ROOF` — each with its elevation
- Level datums: `T.O. FF @ MAIN LEVEL`, `@ LOWER LEVEL`, `@ SUBGRADE`, `T.O. PLATE @ ADDITION`,
  `T.O. GRADE @ GREEN ROOF` — with elevations and inter-level dimension strings
- `CHIMNEY PROJECTION < 10' FROM HEIGHT OF BUILDING CONNECTION PER 26.575.020.F.4.A` with the
  actual dimension
- `EGRESS LIGHT WELL PER IRC R.310.2 (10'-6" SQ FT) PER 26.575.020.F.4.J` — see the IRC note in §9
- Material notes cross-referencing the Residential Design Standards sheet (`Z-005 RDS E.1.`)
- **Staff Note, verbatim: "show any mechanical equipment, lighting, projections, etc."**
- A **3D height vignette** (axonometric with height points tagged) — the model includes one on
  the South sheet; useful for complex roofs

### General note for the height sheet
```
BUILDING HEIGHT MEASURED PER CITY OF ASPEN LAND USE CODE §26.575.020(F), MEASURING BUILDING
HEIGHTS. MAXIMUM PERMITTED HEIGHT __'-0" PER §26.710.0__(d)(_). HEIGHT MEASURED FROM THE
LOWER OF NATURAL OR FINISHED GRADE AT EACH POINT PER §26.575.020(F)(3)(a). ROOFS 3:12–7:12
MEASURED AT THE 1/2 POINT FROM EAVE TO RIDGE; ROOFS OVER 7:12 AT THE 1/3 POINT; ROOFS UNDER
3:12 AT THE TOP-MOST PORTION PER §26.575.020(F)(2).
```

---

## 8. SITE PLAN — SHEETS 4 & 5

> **Staff Note, verbatim: "refer to zoning checklist for site plan requirements, including
> depicting the extent of subgrade space. Please provide labels for features that are not
> clear."**

Model shows: property line · line of setback with dimensions · **extent of excavation**
(dotted) · **extent of subgrade space** · lot data block (LOT / BLOCK / address / lot size /
zone district) · labeled contours · trees · easements (sidewalk, ditch, utility) with widths ·
paving types (pervious-paved driveway/parking) · existing features to be removed · setback
variance callouts with resolution reference · north arrow · graphic scale.

Reviewers also ask for: **dimensions to window wells** · **all hot tubs, pools, outdoor
kitchens/grills** (or state none) · **retaining walls with TOW and BOW elevations** ·
**mechanical/condenser equipment with dimensions from property lines**.

Fences: **<42" permitted in any required yard setback**; up to **6 ft only where entirely
recessed behind the vertical plane of the building façade closest to the street**
(§26.575.020, materials §26.575.050). Model labels: *"FENCE NOT TO EXCEED 6' ABOVE DRIVEWAY"*,
*"FENCE NOT TO EXCEED 6' ABOVE FINISH GRADE."* Driveways within a street-facing setback may
not exceed 24" above/below finished grade; 30" in other setbacks.

Equipment sitting inside a required setback is a **design problem, not a drafting fix**.

---

## 9. BUILDING CODE — the Aspen IRC trap, and a real conflict

**Aspen did not adopt the IRC.** §8.16.010 (Ord. 01-2023): *"The International Residential
Code, 2021 Edition, will not be adopted."* §8.20.020 amends IBC §101.4.11: *"All references to
the International Residential Code (IRC) within this code shall be deleted and the requirement
of this code as it pertains to one- and two-family dwellings and townhouses shall apply."*
Single-family work runs under the **2021 IBC as amended** (Group R-3). There is **no occurrence
of "R310" anywhere in Aspen's Title 8**.

| Element | Adopted-code citation |
|---|---|
| Guards | 2021 IBC §1015.2 (required at >30" drop, measured within 36" horizontally of the edge) and §1015.3 (height), as amended by Aspen M.C. §8.20.020. **42"** per City sets |
| Emergency escape & rescue openings / area wells | 2021 IBC **§1031** — §1031.3.3 (escape opening not directly above an area well), §1031.6, §1031.7 |
| Covers over area wells | **§1031.6 prohibits them outright**: *"Bars, grilles, covers, screens and similar devices shall not be permitted over area wells serving emergency escape and rescue openings."* A perimeter guard with a gate around the *sides* is fine; anything over the opening is not |

⚠️ **Conflict to be aware of:** the City's own model height sheets label light wells
**"PER IRC R.310.2 (10'-6" SQ FT) PER 26.575.020.F.4.J"** — an IRC citation, on a City-issued
example, for a code the City deleted. Practical read: a **zoning** reviewer works from the
model and is unlikely to flag either citation; the **zoning** part of the note
(§26.575.020.F.4.J) is what that sheet is actually about. For the building-code portion,
IBC §1031 is the technically correct reference. Safest: cite the zoning exception plus IBC
§1031, or mirror the model if you want zero friction — and don't spend a resubmittal on it.

Base IBC dimensional minimums for area wells (area, projection, ladder if >44" deep) are
copyrighted ICC text not reproduced in the municipal code.

---

## 10. RECURRING REVIEWER COMMENTS AND HOW TO ANSWER

| Comment | Response |
|---|---|
| "What is this exemption here?" | Name the exemption, cite the subsection, show the tier math |
| "Please include the entire garage floor number" | Show total garage area as one labeled figure, then tiers, then countable |
| "Please add sheet with mitigation floor area existing vs proposed… entire subgrade, entire main level including garage and upstairs with exemptions for attic or top of stairs" | Add the Mitigation columns to the Allowable Floor Area Summary (§2c), and mitigation plan sheets if asked |
| "Does this number include __ countable garage floor area? Please show your calculations." | Garage on its own line; arithmetic shown in the adjacent cell |
| "These numbers do not match." | A plan label disagrees with a table cell. One measured geometry, transcribed once |
| "Please add details on how attic is being accessed." | Access determines the (d)(4) exemption. State finish condition AND access method on the plan, with citation |
| "Demonstrate how approvals are being met in the table. Add more info." | Show gross → each exemption with citation → countable, and the comparison against Allowable. Fill the Unique Approvals / Variances / Reception # rows |
| "Walls B, C, F, P don't match the diagram below." | Table/diagram divergence in the subgrade wall worksheet |
| "Please add grade to the wall segments." | Draw natural **and** finished grade across each subgrade wall segment diagram (the model's own Staff Note says the same) |
| "From your legend it appears that all walls are being removed… if siding will be updated, don't use the same color as demolition." | Re-skin ≠ demolition (§26.580.040(c)(7)). Separate graphics per condition; coordinate with the calc sheet |
| "Add the specific demolition legend that shows in the approvals — 'per Resolution XX Series XX'" | Match the legend in the land use approval. If the project has no prior approval, say so rather than inventing one |
| Height sheet checklist (code reference, property lines, setbacks, topography, roof penetration dimensions, height points, both grade lines) | See §7 |
| Site plan checklist | See §8 |

---

## 11. SELF-CHECKS BEFORE SUBMITTAL

**Completeness**
- [ ] All ~14 model sheets present, or a documented reason one doesn't apply
- [ ] Zoning Summary present with Net Lot Area and the six-column Floor Area Summary
- [ ] **Floor area legend on every page** (Staff Note)
- [ ] Site Coverage sheet
- [ ] Height Measurement Vignette on the Height Over Topography sheet
- [ ] "Any other demo since 2022?" answered

**Arithmetic**
- [ ] Sum test on every level, both conditions: countable + all tagged exemptions = gross, exactly
- [ ] Same gross geometry across Floor Area and Mitigation columns
- [ ] Attic/stair/deck treated identically for Allowable and Mitigation (only garage & subgrade differ)
- [ ] Net Lot Area computed with the slope table — and the **25% slope-reduction cap** applied
- [ ] Subgrade: exposed ÷ total (never inverted — buried basements run 2–10%, not 90%)
- [ ] Every wall's Removed ≤ (Area − Fenestration)
- [ ] Roof Removed on the **adjusted** basis, never plan area (Ratio Method)
- [ ] One demolition method used consistently
- [ ] Every SUM range covers all rows
- [ ] Totals boxes from cell references, never typed
- [ ] Percentages computed from full-precision sums

**Documentation**
- [ ] Every exemption tag carries its code citation
- [ ] Arithmetic shown in adjacent cells (the model's habit)
- [ ] Correct legend on each sheet type — four distinct demo/subgrade legends
- [ ] Plan labels equal table cells everywhere
- [ ] Natural **and** finished grade on subgrade wall diagrams and all height elevations
- [ ] Mechanical, vents, roof drains, lighting, projections shown (Staff Note)
- [ ] Survey benchmark/datum note
- [ ] Nonconformity statement if existing exceeds allowable

**Interpretation calls to put in writing (comdevzoning@gmail.com) before submitting**
- [ ] Attic access/finish determinations, especially where access changes existing→proposed
- [ ] The (d)(4) rule 3 vs. rule 4 question on a ≤30" band inside a counted attic
- [ ] Roof planes claimed as "built over, structure remains" rather than removed
- [ ] Any claimed §26.580.050 demolition exemption — the City asks for this explicitly
- [ ] Stacked vs. separate stair runs for the (d)(3) exclusion
- [ ] TDR eligibility where the structure is nonconforming
- [ ] Whether reallocation between above-grade and below-grade area satisfies §26.312.030(c)

§26.470.140(c) requires verifying existing conditions with the Zoning Officer before
demolition anyway — bundle these questions into that conversation.
