# Aspen Residential Zoning Submittal — Sheets, Charts, Equations, Citations

Working reference for City of Aspen single-family/duplex zoning submittals, built from a
full review cycle (844 Roaring Fork Rd) including City reviewer comments. Covers the four
calculation packages: **Height Over Topography**, **Allowable Floor Area**, **Mitigation
Floor Area**, and **Demolition**. Numbers in examples are illustrative — the formats,
equations, citations, and self-checks are the reusable part.

The City publishes **Model Zoning Submission** example sheets on its website. Match their
column headers and row structure exactly; the reviewer checks against them. Their examples
contain occasional internal errors (mismatched totals between sheets, duplicate row labels,
outdated subsection lettering like "26.575.020.D.7" for what is now (d)(8)) — **match the
current code text, not their typos**.

---

## 0. The rule that prevents 90% of review comments

**One measured geometry feeds every sheet.** Measure each level's polylines once in CAD;
that single set of gross areas populates the Floor Area sheets AND the Mitigation sheets.
Only the *exemptions applied* differ between them. Numbers retyped between sheets spawn
variants that reviewers catch instantly ("These numbers do not match").

**The sum test — run it on every level, both existing and proposed:**

```
countable area + every tagged exemption = gross area     (exactly, no remainder)
```

If it doesn't close, there is untagged area on that floor. Find it before submitting.

---

## 1. HEIGHT OVER TOPOGRAPHY

### Governing sections
- **Max height** — zone district table, e.g. R-15 = 25 ft, §26.710.050(d)(7)
- **Measurement method** — §26.575.020(f) *(reviewers write it "26.575.020.F")*

### Measurement by roof pitch — §26.575.020(f)(2)
| Condition | Measure to |
|---|---|
| CC, C-1, CL, NC, SCI zones | top-most point of roof/ridge/parapet — (f)(1) |
| All other zones, pitch < 3:12 | top-most portion of structure |
| Pitch 3:12 – 7:12 | **1/2 point** vertically between eave point and ridge — **no limit on ridge height** |
| Pitch > 7:12 | **1/3 point** up from eave to ridge — **no limit on ridge height** |
| Multiple pitches in one vertical plane | draw line ridge→eave point, apply resulting pitch |
| Barrel vault | line from top-most point to eave point, apply resulting pitch |
| Shed (single pitch) | as above, highest point = ridge |
| Mansard | measure to the flat roof |
| Butterfly | shed methodology |
| Dormers | **excluded** if footprint ≤50% of the roof plane (aggregate if multiple on one plane) AND dormer ridge not higher than that roof's ridge; otherwise measured normally |

### Measurement method — §26.575.020(f)(3)
- **(a) Perimeter:** measured from the **lower of natural or finished grade** at each location.
  *"Building permit plans must depict both natural and finished grades."*
- **(b) Within footprint:** areas within 15 horizontal ft of the perimeter use the perimeter
  measurement; elsewhere project natural grade up. Director may accept surveyor/engineer
  estimate of pre-development topography where grade was altered by prior development.
- **(c) To the roof:** measured to the surface **inclusive of the first layer of exterior
  sheathing or weatherproofing membrane**, but **excluding** shakes, shingles, fireproofing,
  exterior insulation, a second layer of sheathing, veneer, or ornamentation.
  → **This is the re-skin rule: adding new roofing over existing structure does not raise
  measured height.** Eave point = where the plane of the roof intersects the plane of the
  exterior wall, **nominal structure**, excluding exterior treatments.

### Height exceptions — §26.575.020(f)(4)
| Item | Allowance | Sheet-note citation |
|---|---|---|
| a. Chimneys, flues, vents | **10 ft** above height of building **at the point the device connects**. For pitch **≥8:12**, may not exceed the highest ridge by more than building code requires. Caps, shrouds, spark arrestors are **contained within** the allowance. | 26.575.020.F.4.A |
| b. Communications equipment | per §26.575.130 | F.4.B |
| c. Elevator/stair enclosures | +5 ft (+10 ft if set back 20 ft from street façade) — **NOT allowed for single-family, duplex, or accessory buildings** | F.4.C |
| d. Rooftop railings | +5 ft, ≥50% transparent — **NOT allowed for single-family or duplex** | F.4.D |
| e. Mechanical equipment | **+6 ft** above the building at the point of attachment, **inclusive of pad and screening** | 26.575.020.F.4.E |
| f. Energy efficiency / renewable systems | per subsection | F.4.F |
| i. Buildings on slopes | lot declining ≥10% from front lot line: max height of the street-facing façade may extend horizontally for the first 10 ft of building depth | F.4.I |
| j. Lightwells & basement stairwells | egress basement stairwell not counted. **Street-facing:** minimum-size lightwell entirely recessed behind the façade plane closest to the street and enclosed to within 18" of first floor level (not walk-out style) not counted. **Non-street-facing:** lightwell ≤100 sf not counted. **Does not apply to lightwells or stairwells located within a setback.** HPC may exempt >100 sf on landmark properties. | 26.575.020.F.4.J |
| k. Decorative elements (CC/C-1/NC) | up to 24" with Commercial Design Review; not combinable | F.4.K |
| m. Skylights and light tubes | per subsection | F.4.M |

### The height table — City model column set
**For Permit:**

| Elevation Label | Maximum Height | Elevation of Natural Grade | Elevation of Finished Grade | Most Restrictive | Roof Height over Topography | Proposed Roof Height over Most Restrictive |

**For As-Built Survey** (leave blank until post-construction, typically a CO condition):

| Actual Elevation of Finished Grade | Actual Most Restrictive | Actual Roof Height over Topography | Actual Roof Height over Most Restrictive |

**What each column is — this trips people up:**
- **Maximum Height** = the zone district limit (25 ft in R-15), same every row unless a
  documented exception applies.
- **Elevation of Natural / Finished Grade** = *ground* elevations at that XY point, from
  survey and grading plan. Nothing to do with the building.
- **Most Restrictive** = a **text label** — "Natural" or "Finished", whichever elevation is
  **lower**. Not a number. It flips point-to-point across a building.
- **Roof Height over Topography** = the **actual elevation of the tagged measurement point on
  the roof** (the 1/2 point, 1/3 point, or top-most portion) — a building elevation, not a
  height.
- **Proposed Roof Height over Most Restrictive** = the real height, compared against Maximum Height:

```
Proposed Roof Height over Most Restrictive
    = Roof Height over Topography − (elevation of whichever grade is Most Restrictive)
```

**Deriving the roof measurement point elevation** (when not pulled from a 3D model):
```
Ridge Elev = Eave Elev + (horizontal run eave→ridge × pitch/12)
3:12–7:12 → point = Eave + 0.50 × (Ridge − Eave)
   >7:12  → point = Eave + 0.333 × (Ridge − Eave)
   <3:12  → use the top-most portion elevation directly
```
In a 3D model, place a spot elevation on the roof surface at the point's plan location and
read the Z value — faster and exact.

**Below-grade roofs** (green roof over basement, etc.) produce a *negative* result. That is
correct and compliant — label the cell **"N/A – BELOW GRADE"** rather than leaving a bare
negative number, and note the condition on the roof plan.

### What the height sheet must show (City reviewer checklist)
- General note referencing **§26.575.020(F), Measuring Building Height**, plus the zone
  district max height citation — the authority for the whole sheet, stated once, not just
  sub-citations at individual tags
- Property lines and all required setback lines (including any overlay/bluff setbacks)
- Topography **with labeled contour elevations**
- **Dimensions** of proposed roof penetrations — the *actual* measured dimension at each
  chimney/vent/mechanical unit, not just the code maximum
- Numbered height points around the perimeter, keyed roof plan → elevations → table.
  Use a tag shape distinct from grid bubbles so "grid 7.1" isn't confused with "point 7"
- Four elevations minimum plus the topo/roof plan sheet
- **Both natural and finished grade lines drawn across the full width of every elevation**,
  as two distinguishable linetypes, with "(MOST RESTRICTIVE)" labeled **per segment** — the
  designation flips wherever the two profiles cross
- The 25-ft limit line drawn as a true offset of the more-restrictive grade profile — it
  steps and slopes with grade; it is only horizontal if grade is level
- A linetype legend; keep ridge-reference lines visually distinct from the height limit line

### Elevation sheet notes worth carrying forward
```
EXISTING ROOF TO BE RE-SKINNED. STRUCTURAL RIDGE AND RAFTERS UNCHANGED. HEIGHT MEASURED
TO FIRST LAYER OF EXTERIOR SHEATHING; NEW SURFACE TREATMENTS EXCLUDED PER §26.575.020.

[5:12] PITCH — HEIGHT MEASURED AT 1/2 POINT EAVE TO RIDGE PER §26.575.020(F)(2).
NO LIMIT ON RIDGE HEIGHT.

ROOF PITCH <3:12 — HEIGHT MEASURED TO TOP-MOST PORTION PER §26.575.020(F)(2).

DORMER FOOTPRINT ≤50% OF ROOF PLANE ON WHICH LOCATED (AGGREGATE WHERE MULTIPLE DORMERS
SHARE A PLANE); DORMER RIDGE DOES NOT EXCEED RIDGE OF ROOF ON WHICH LOCATED. EXCLUDED
FROM HEIGHT MEASUREMENT PER §26.575.020(F)(2)(G).

CHIMNEY PROJECTION 10' MAX FROM HEIGHT OF BUILDING CONNECTION PER 26.575.020.F.4.A.
[+ the actual measured dimension, e.g. 5'-0"]

MECHANICAL EQUIPMENT/VENTS 6'-0" MAX ABOVE HEIGHT OF BUILDING AT POINT OF ATTACHMENT
PER 26.575.020.F.4.E.

MECHANICAL EQUIPMENT, VENTS, AND ROOF DRAINS ARE NOT VISIBLE ON THIS ELEVATION. SEE ROOF
PLAN, SHEET __, FOR LOCATIONS, TAGS, AND HEIGHT ABOVE POINT OF ATTACHMENT.

ELEVATIONS BASED ON [datum] PER SURVEY BY [surveyor], DATED [date].
```

---

## 2. FLOOR AREA — the three types

§26.575.020(d)(2) defines three distinct floor areas. Getting these confused is the single
biggest source of wrong sheets.

| Type | Definition | Exemptions applied |
|---|---|---|
| **Gross Floor Area** | total horizontal area of all floors, measured to exterior face of framing, excluding unenclosed balconies | **none** |
| **Allowable Floor Area** | what's checked against the zone district limit | **all** of (d)(3)–(16) |
| **Mitigation Floor Area** | used to assess affordable housing mitigation | all **except** garage (d)(8) and subgrade (d)(9), which are **not taken** — those areas count **in their entirety** |

The (d)(2)(a)(iii) table in the code lists exactly two elements not exempted for Mitigation
Floor Area: **Garages and carports (d)(8)** and **Subgrade areas (d)(9)**. Everything else —
attic (d)(4), vertical circulation (d)(3), decks (d)(5), airlocks (d)(16) — applies
**identically to both** Allowable and Mitigation calculations. If a sheet exempts an attic on
one and counts it on the other, that's an error.

### Measurement basis — §26.575.020(d)(1)
Measured from the **exterior face of framing** (or face of structural block/straw bale),
**excluding** sheathing, vapor barrier, weatherproofing membrane, exterior-mounted insulation,
and all veneer/surface treatments (stone, stucco, brick, shingles, clapboard).

### Exemptions that matter on residential sheets

**(d)(3) Vertical circulation**
- Stairs and elevators are counted on the **lower** of the two levels connected and **not
  counted on the top-most interior floor served**.
- Multi-level run: counted on all levels as if solid floor, **except** the top-most level served.
- Elevator mechanical/overrun above the top stop, and area below the lowest stop, not counted.
- **Two separate runs (basement→main, break, main→upper) are evaluated independently**, so the
  main level can have one stair footprint counted (bottom of the upward run) and another
  excluded (top of the lower run) at two different locations. **One stacked stairwell = one
  exclusion, at the very top level served.** If ambiguous, ask the Zoning Officer — the
  difference is one whole stair footprint.

**(d)(4) Attic and crawl space** — exempt when **unfinished and uninhabitable** AND
**accessible only as a matter of necessity**. Four operative rules:
1. Crawl space exempt if ≤6 ft high AND accessible only through interior floor hatch/exterior
   access panel AND minimum size reasonably necessary for mechanical equipment. Stacked crawl
   spaces don't qualify; crawl >6 ft counts under (d)(9).
2. *"Attic space that is conveniently accessible and is either habitable or can be made
   habitable shall be counted."* — an AND test; ladder-only access fails "conveniently accessible"
3. *"Areas of an attic level with thirty (30) vertical inches or less between the finished
   floor level and the finished ceiling shall be exempt, **regardless of how that space is
   accessed or used**."*
4. **Whole-room rule:** *"If any portion of the attic or crawl space of a structure is to be
   counted, then **the entire room** shall be included."*

   Code examples: attic above a hung/false ceiling → exempt · 6-ft crawl w/ interior hatch →
   counts · attic accessible only by interior pull-down ladder → **exempt (no height limit
   in this example)** · unfinished attic **over 4 ft with convenient access** → counts ·
   6-ft crawl, hatch access, sized for mechanical → exempt.

   **Practical decision matrix:**
   | Finish | Access | Result |
   |---|---|---|
   | unfinished | hatch / pull-down ladder / none | **exempt** (height irrelevant) |
   | unfinished | door, fixed stair | **counts** (the ">4 ft + convenient access" example) |
   | finished | any | **counts** — removing the door does not cure it |

   **Rule 3 vs. rule 4 tension:** in an attic that otherwise counts, does the ≤30" band stay
   exempt? Better reading: rule 4 prevents carving by *finish/habitability*; rule 3 carves by
   *geometry* — they operate on different axes, and reading rule 4 to swallow rule 3 would
   make rule 3 surplusage (it only has independent work to do in an attic that counts).
   **Ambiguous — put it in writing to the Zoning Officer.** Appeal path is §26.575.020(k).

   Unfinished pockets behind knee walls with **no access at all** satisfy the exemption a
   fortiori, and are usually also ≤30" — tag each individually with its own area.

**(d)(5) Decks, balconies, loggias, gazebos, trellis, exterior stairways, non-street porches**
- Exempt in aggregate up to **15% of the property's Allowable Floor Area**; only the excess counts.
  ```
  Deck threshold = Allowable Floor Area × 0.15
  ```
  *(Base it on the Allowable Floor Area for the lot — a recurring error is using some other number.)*
- Railings, permanently fixed seating, and fixed grills count toward the deck area. Permanent
  planters/green roofs ≥30" above or below the deck surface and built into the structure do not.
- Unenclosed area beneath decks/balconies/exterior stairs exempt unless used as a carport.
- Enclosed unconditioned area beneath porches/gazebos/decks whose finished floor is within 30"
  of surrounding finished grade is exempt regardless of use.

**(d)(6) Front porches** — street-facing porches developed within 30" of finished ground level
are not counted; otherwise treated as a Deck.

**(d)(8) Garages and carports**
```
Exempt = 250 + (min(max(Garage − 250, 0), 250) × 0.50)      → 375 max
Countable = Garage total − Exempt
```
First 250 sf fully exempt · 251–500 sf at 50% · above 500 sf counts in full.
**Not taken for Mitigation Floor Area.**

**(d)(9) Subgrade areas** — the highest-leverage calculation on a residential sheet
```
Exposed % = (exposed exterior wall area above the LOWER of natural or finished grade)
            ÷ (total exterior wall area of that level)

Countable subgrade floor area = subgrade gross floor area × Exposed %
```
- Subgrade story with **no** exposed wall is excluded entirely.
- Wall area = **interior wall area projected outward**, excluding wall area adjacent to
  foundation or floors. Drop ceilings not included in crawl height.
- **Light-well-exposed wall counts as exposed** — every well added for egress/height reasons
  increases countable basement area here. Cross-sheet tension worth flagging early.
- Multi-level subgrade: adjacent spaces are on the same story if the vertical separation
  between their ceilings is <50% of either space's floor-to-ceiling height.
- Partially subgrade space with a vaulted ceiling in a pitched roof: wall area **includes the
  gable area**.
- **Garage within a subgrade level:** take the garage exemption **first** from the gross
  below-grade area, then apply the subgrade percentage to the remainder.
- Adjoining exempt crawl space: draw a line separating basement from crawl; exempt crawl is
  excluded from perimeter, wall area, and floor area measurements.
- Single-family/duplex: **no more than one floor level below finished grade**; finished floor
  no more than **15 ft** below finished grade (exempt crawl below basement doesn't count
  toward the depth limit).
- **Not taken for Mitigation Floor Area** — the entire subgrade counts.

**(d)(16) Airlocks** — permanently installed interior airlocks exempt up to 100 sf per building.

### Things that are NOT floor area at all
- **At-grade uncovered patios** — §26.104.100 defines Patio as "an outdoor uncovered, at-grade
  space which may be paved or unpaved." Outside the exterior walls → never floor area. Show as
  a row with **0.00 counted** (City model keeps the row) rather than deleting it.
  A *covered* patio not connected to a building is a **Gazebo**; attached, it behaves as a porch —
  either way it moves into (d)(5)/(d)(6).
- **Light wells / areaways** — outdoor uncovered space below grade (§26.104.100). Never floor
  area. They matter only indirectly, via exposed wall area in (d)(9).

### Allowable Floor Area — R-15 sliding scale, §26.710.050(d)(10)
Single-family (duplex/two-detached column is higher; check the table for the actual project):

| Net Lot Area (sf) | Allowable Floor Area, single-family |
|---|---|
| 0 – 3,000 | 80 sf per 100 sf of NLA, max 2,400 |
| 3,000 – 9,000 | 2,400 + 28 sf per additional 100 sf, max 4,080 |
| 9,000 – 15,000 | 4,080 + 7 sf per additional 100 sf, max 4,500 |
| 15,000 – 50,000 | 4,500 + 6 sf per additional 100 sf, max 6,600 |
| 50,000 + | 6,600 + 2 sf per additional 100 sf |

```
e.g. NLA 17,791:  4,500 + ((17,791 − 15,000) ÷ 100 × 6) = 4,500 + 167.5 = 4,667 sf
```
**TDRs:** each extinguished historic TDR certificate adds 250 sf; non-historic lots ≥15,000 sf
with only a single-family residence may extinguish up to two. **Nonconforming structures are
not eligible** for the TDR floor area increase — relevant when the existing house is already
over its allowable.

### Nonconforming floor area — §26.312.030
If existing countable floor area exceeds the allowable, the structure is legally nonconforming
as to floor area. §26.312.030(c): *"A nonconforming structure shall not be extended by an
enlargement or expansion that increases the nonconformity."* Practical test on the sheet:
**proposed countable total ≤ existing countable total.** Put the comparison on the summary
sheet explicitly. Also: §26.312.030(f)(2) — a nonconforming structure that is *purposefully
Demolished* may only be replaced in conformance, so crossing the 40% demolition threshold can
forfeit the nonconforming rights entirely.

### Allowable Floor Area summary table — City model format

```
Allowable Floor Area          | [zone district formula + computed result]      | Reference
Unique Approvals              | [subdivision plat, HPC bonus, etc. or N/A]     | Reference
Variances                     | [or N/A]                                       | Reference
Exemptions                    | Garage / Deck / Subgrade / Attic-Stair rows    | Reference

Floor Area Summary | Existing Gross | Existing Floor Area | Proposed Gross | Proposed Floor Area | Reference
  Subgrade / Basement
  Garage
  Main Level
  Upper Level
  Deck / Patio Area
  ADU
  TOTAL
```
Every summary row carries a **Reference** to the sheet where that area is diagrammed. Keep
zero rows (Deck/Patio, ADU) rather than deleting them — the City model does.

---

## 3. MITIGATION FLOOR AREA (GMQS affordable housing)

### Which path applies
| | Demolition **not** triggered (<40%) | Demolition triggered (≥40%) |
|---|---|---|
| Review | administrative, by-right to building permit — §26.470.090(a) | full GMQS land use application + allotment — §26.470.090(c) |
| Mitigation basis | **net increase** of Mitigation Floor Area | **no credit for existing** — §26.470.140(b) — full proposed area |
| Also triggers | — | Residential Demolition & Redevelopment Standards §26.580.080; §26.312.030(f)(2) |

### The equation — §26.470.090(a)(2)–(3)
```
Net increase of Mitigation Floor Area = Proposed MFA − Existing MFA
FTE = Net increase ÷ 1,000 × 0.107
```
Code's own example: existing 4,500 sf expanded by 250 sf → 250/1,000 × 0.107 = 0.03 FTE.

### Mitigation options — §26.470.090(a)(3)
- RO (resident-occupancy) or lower deed restriction on the dwelling
- Deed-restricted AH unit ≥30% of the Allowable Floor Area increase, Category 2 or lower
- Fee-in-lieu **or** extinguishing a Certificate of Affordable Housing Credit (Category 2 or lower)
- Deferral agreement for a qualified full-time local working resident — §26.470.080(d)(13)

**Fee-in-lieu above 0.10 FTE requires City Council approval** — §26.470.110(c). Anything above
~935 sf of net increase clears that threshold, so most real remodels do.

### Mitigation sheet content (what the reviewer asks for verbatim)
> "Mitigation sheet should include entire subgrade, entire main level including garage and
> upstairs with exemptions for attic or top of stairs."

Existing and Proposed plan sets per level with hatching + area tags, plus:

| LEVEL | EXISTING MITIGATION FLOOR AREA | PROPOSED MITIGATION FLOOR AREA |
|---|---|---|
| SUBGRADE (ENTIRE) | | |
| MAIN LEVEL (INCL. GARAGE) | | |
| UPPER LEVEL | | |
| **TOTAL** | | |
| **NET INCREASE (PROPOSED − EXISTING)** | | |
| **MITIGATION** | net ÷ 1,000 × 0.107 = __ FTE | |

Sheet note:
```
PROJECT DOES NOT MEET THE DEFINITION OF DEMOLITION: TOTAL EXTERIOR WALL + ROOF SURFACE
AREA REMOVED = __% < 40% PER §26.580.040 (SEE DEMOLITION CALCULATIONS, SHEETS __).
MITIGATION BASED ON NET INCREASE OF MITIGATION FLOOR AREA PER §26.470.090(a).
GARAGE AND SUBGRADE EXEMPTIONS NOT TAKEN PER §26.575.020(d)(2)(a)(iii).
```

---

## 4. DEMOLITION CALCULATIONS — §26.580.040

### Thresholds
- **40% = "Demolition"** — §26.580.040(a)(3). This is the only percentage in the current code.
- A **35% documentation/review trigger** circulates in City checklists but is **not in the
  adopted Land Use Code text** — confirm against the current submittal checklist rather than
  citing it as code.

### The calculation
```
Denominator (Area Used) = existing exterior WALL assemblies above finished grade
                        + all existing ROOF assemblies
                        − ALL existing fenestration (doors, windows, skylights)

Numerator (Area Removed) = the same surfaces being removed

Demolition % = Area Removed ÷ Area Used
```

### Counting rules — §26.580.040(c)
| Rule | Effect |
|---|---|
| (c)(1) | "Assembly" = the exterior surface **including studs, joists, rafters** — structure, not finish |
| (c)(2) | If any portion of a wall or roof **stud/rafter** is removed, the associated surface area is diagrammed as removed |
| (c)(3), (b)(2) | **Involuntary collapse counts**, regardless of intent |
| (b)(3) | Removals required for health/safety discovered after work begins are excluded — requires Chief Building Official inspection |
| (c)(4) | Zoning Officer may require **recalculation** as work progresses |
| (c)(5) | Wall/roof removed to accommodate **new, relocated, or expanded** fenestration **counts as removed**; **in-kind replacement does not** |
| (c)(6) | **Only above finished grade** — subgrade and interior elements never count |
| **(c)(7)** | **"Replacement of exterior sheeting when the structural components of that area are to remain, does not count toward the calculation of Demolition"** — the re-skin rule; also covers roof planes **built over** with existing structure remaining |
| (c)(9) | Separate calculation per detached structure; attached duplex calculated as one structure |
| (d) | **Cumulative over 10 years** — prior permits stack |

### Submission format — §26.580.040(b)
*"a diagram showing the calculation… shall depict each exterior wall and roof segment as a
flat plane with an area tabulation."* Lettered wall segments and lettered roof planes, each
keyed to a reference plan, with a three-part legend:
**Existing to Remain / To Be Removed / Area Reduced for Fenestration**.

### Wall demolition table
| Wall Label | Individual Wall Area (sf) | Area Reduced for Fenestration (sf) | Area of Wall to be Removed (sf) |

```
Wall Surface Area Total       = Σ column 2
Area Reduced for Fenestration = Σ column 3
Area Used for Demo Calc       = Total − Fenestration
Wall Surface Area to be Removed = Σ column 4
```
**Per-wall invariant:** `Removed ≤ (Wall Area − Fenestration)`. A fully-demolished wall with
openings has `Removed = Area − Fenestration`, never `= Area`. Any row where Removed equals the
gross while Fenestration > 0 is wrong.

**The fenestration column is the #1 flagged error.** A column of zeros on a house with windows
reads as "not filled in." Pull each value from the CAD elevation tags.

### Roof demolition — Ratio Method
| Roof Label | Roof Area in Plan (sf) | Fenestration (sf) | Net Plan Area (sf) | Roof Slope | Adjustment Factor | Actual Roof Area for Demo Calc (sf) | Area of Roof to be Removed (sf) |

```
Adjustment Factor = √(1 + (rise/12)²)
Actual Roof Area  = Net Plan Area × Adjustment Factor
Removed           = Actual Area (full removal)  |  partial plan area × factor (partial)  |  0 (remains)
```

| Pitch | Factor | | Pitch | Factor |
|---|---|---|---|---|
| flat / membrane | 1.0000 | | 8:12 | 1.2019 |
| 1/4:12 | 1.0002 | | 9:12 | 1.2500 |
| 2:12 | 1.0138 | | 10:12 | 1.3017 |
| 3:12 | 1.0308 | | 10.5:12 | 1.3288 |
| 4:12 | 1.0541 | | 12:12 | 1.4142 |
| 6:12 | 1.1180 | | 14:12 | 1.5366 |

*(1.5366 is the **14:12** factor — a plausible-looking wrong constant to find pasted down an
entire column.)*

City model sheet note, verbatim:
> "Actual area of roof to be removed is calculated by multiplying the plan area by an
> adjustment factor, in lieu of depicting each roof segment as a flat plane. The adjustment
> factor is determined by a ratio of the roof slope."

### Element-by-element treatment
| Element | Treatment |
|---|---|
| **Skylights** | fenestration — deducted from the plane's area; demoing one counts as nothing. New/relocated skylights cut into remaining roof **do** count as removed per (a)(2)(b) |
| **Glass roofs / glazed roof assemblies** | 100% fenestration — zero to both numerator and denominator. **Mullions and framing are part of the fenestration system**, not solid roof. Keep the rows, show 0.00 |
| **Chimneys** | not wall or roof assemblies — excluded per (a)(1), (c)(1). Only the parent-plane structure cut for removal counts. A framed/sided chimney *chase* is arguable — ask |
| **Dormers being demolished** | roof planes → roof table (with slope factor); face and cheek walls → wall table (net of the dormer window) |
| **Roof built over, structure remaining** | **not removed** per (c)(1)–(2), (c)(7); stays in the denominator |
| **Partial plane removal** | its own row or a sub-row; plan area × the plane's factor |

### Demolition Totals block
```
Roof + Wall Area Used for Demo Calculation = [roof Area Used]    + [wall Area Used]
Surface Area to be Removed                 = [roof Area Removed] + [wall Area Removed]
Total                                      = Removed ÷ Used
```
**Every component must be a cell reference to a table on the sheet.** The City's own example
sheets disagree with themselves (one shows 1,388.75 for the same roof another shows as
1,422.95) precisely because these were typed.

### Demolition exemptions — §26.580.050 (Director may grant)
dangerous/unsafe structures · 100% deed-restricted affordable housing · de minimus scope ·
temporary relocation and replacement on a foundation · removals required for normal maintenance
or life-safety (e.g. a failing roof), limited to the minimum necessary · removal of non-historic
additions to designated landmarks per HPC.

---

## 5. ARCHITECTURAL SITE PLAN — reviewer checklist

- Line depicting the extent of **subgrade area**
- **Dimensions to window wells** (and check whether any fall in a setback — §26.575.020(f)(4)(j)
  height exception does **not** apply to lightwells within a setback)
- **Topography contour elevation labels**
- All hot tubs, pools, outdoor kitchens/grills — or state that none are proposed
- **Retaining and site walls with TOW and BOW elevations**
- Mechanical/condenser equipment with **dimensions from property lines** — equipment in a
  required setback is a design problem, not a drafting fix
- Fences: **<42" permitted in any required yard setback**; up to **6 ft only where entirely
  recessed behind the vertical plane of the building façade closest to the street**
  (§26.575.020, materials per §26.575.050). Driveways within a street-facing setback may not
  exceed 24" above/below finished grade; 30" in other setbacks
- Property lines, all setbacks, any overlay setbacks (e.g. Hallam Lake Bluff)

---

## 6. BUILDING CODE — the Aspen trap

**Aspen did not adopt the IRC.** §8.16.010 (Ord. 01-2023): *"The International Residential
Code, 2021 Edition, will not be adopted."* And §8.20.020, amending IBC §101.4.11: *"All
references to the International Residential Code (IRC) within this code shall be deleted and
the requirement of this code as it pertains to one- and two-family dwellings and townhouses
shall apply."*

Single-family work runs entirely under the **2021 IBC as amended by Aspen M.C. §8.20.020**
(IBC Group R-3). There is **no occurrence of "R310" anywhere in Aspen's Title 8** — citing IRC
sections on a sheet cites a code the City does not enforce.

| Element | Correct Aspen citation |
|---|---|
| Guards | 2021 IBC §1015.2 (where required — >30" drop, measured within 36" horizontally of the edge) and §1015.3 (height), as amended by Aspen M.C. §8.20.020. **42"** per City example sets |
| Emergency escape & rescue openings / area wells | 2021 IBC **§1031**, as amended — §1031.3.3 (escape opening shall not be located directly above an area well), §1031.6, §1031.7 |
| Covers over area wells | **§1031.6 prohibits them outright**: *"Bars, grilles, covers, screens and similar devices shall not be permitted over area wells serving emergency escape and rescue openings."* A perimeter guard with a gate around the *sides* of a well is fine; anything over the opening is not |

Base IBC dimensional minimums for area wells (area, projection, ladder if >44" deep) are
copyrighted ICC text not reproduced in the municipal code — pull from the ICC book/viewer.

Sample light-well note:
```
EGRESS LIGHT WELL (AREA WELL) PER 2021 IBC §1031.3.3 & §1031.6, AS AMENDED BY ASPEN M.C.
§8.20.020. NO COVER, GRILLE, OR SCREEN OVER WELL OPENING PER §1031.6. 42" GUARDRAIL PER
§1015.2/1015.3. HEIGHT EXCEPTION PER §26.575.020.F.4.J.
```

---

## 7. RECURRING REVIEWER COMMENTS AND HOW TO ANSWER

| Comment | What it means / response |
|---|---|
| "What is this exemption here?" | A callout with no basis. Name the exemption, cite the subsection, show the tier math |
| "Please include the entire garage floor number" | Show total garage area as one labeled figure, then the exemption tiers, then countable |
| "Does this number include __ countable garage floor area? Please show your calculations." | Break the garage onto its own line so it can't hide inside a main-level figure; show the arithmetic |
| "These numbers do not match." | A plan label disagrees with a table cell. One measured geometry, transcribed once |
| "Please add details on how attic is being accessed." | Access determines the (d)(4) exemption. State finish condition AND access method on the plan, with citation |
| "Demonstrate how approvals are being met in the table. Add more info." | The table shows results but not derivation. Add gross → each exemption with citation → countable, and the comparison line against Allowable |
| "Walls B, C, F, P don't match the diagram below." | Table/diagram divergence in the subgrade wall worksheet |
| "Please add grade to the wall segments." | Draw the natural/finished grade line across each wall segment diagram so the exposed portion is visible. Fully-buried walls: the line sits at or above the top of the segment, which is itself the demonstration |
| "From your legend it appears that all walls are being removed… if siding will be updated, don't use the same color as demolition." | Re-skin ≠ demolition (§26.580.040(c)(7)). Separate graphics for: elements demolished / exterior walls demolished / interior walls demolished / exterior wall material to sheathing / siding / roof material to sheathing / floor |
| "Add the specific demolition legend that shows in the approvals — 'per Resolution XX Series XX'" | Match the legend from the land use approval. If the project has no prior approval (Unique Approvals: N/A), say so rather than inventing one |
| Height sheet checklist | See §1 above — code reference note, property lines, setbacks, labeled topo, penetration dimensions, numbered points, both grade lines |
| Site plan checklist | See §5 above |

---

## 8. SELF-CHECKS BEFORE ANY SUBMITTAL

**Arithmetic**
- [ ] Sum test on every level, both conditions: countable + all tagged exemptions = gross, exactly
- [ ] Same gross geometry on the Mitigation and Floor Area sheets; only exemptions differ
- [ ] Attic/stair/deck treated **identically** on Mitigation and Allowable sheets (only garage & subgrade differ)
- [ ] Subgrade: exposed ÷ total (never inverted — a ~90% "exposed" basement is a red flag; buried basements run 2–10%)
- [ ] Every wall's Removed ≤ (Area − Fenestration)
- [ ] Roof Removed on the **adjusted** basis, never plan area
- [ ] Every SUM range covers **all** rows (truncated ranges are the most common silent error)
- [ ] Totals boxes built from cell references, never typed
- [ ] Percentages computed from full-precision sums, not rounded components

**Documentation**
- [ ] Every exemption tag carries its code citation
- [ ] Hatch legend on every sheet that hatches anything
- [ ] Plan labels equal table cells, everywhere
- [ ] Cross-references between sheets (tags → table → diagram)
- [ ] Survey/benchmark datum note where elevations are used
- [ ] Nonconformity statement on the summary sheet if existing exceeds allowable

**Interpretation calls to put in writing to the Zoning Officer before submitting**
- [ ] Attic access/finish determinations, especially where access changes between existing and proposed
- [ ] The (d)(4) rule 3 vs. rule 4 question on a ≤30" band inside a counted attic
- [ ] Roof planes claimed as "built over, structure remains" rather than removed
- [ ] Stacked vs. separate stair runs for the (d)(3) exclusion
- [ ] TDR eligibility where the structure is nonconforming
- [ ] Whether reallocation between above-grade and below-grade area is acceptable under §26.312.030(c)

§26.470.140(c) requires verifying existing conditions with the Zoning Officer before
demolition anyway — bundle these questions into that conversation.
