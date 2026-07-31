# 04 — MISTAKES TO HUNT FOR, AND HOW TO ANSWER THE CITY

Every error pattern below actually happened on a real Aspen submittal and was
caught either in-house or by the City. **When you check a set of sheets, hunt for
these first.** They repeat from project to project because they come from how the
work is done, not from what the numbers are.

---

## PART 1 — THE FAST AUDIT (run this on any chart, in this order)

1. **Sum test, every level, both conditions:** countable + every tagged exemption
   = gross, exactly. A remainder means untagged area or a wrong gross.
2. **Re-add every column by hand** and compare to the printed total. A mismatch
   is almost always a SUM range that stops short of the last row.
3. **Every total traces to a table on the sheet.** If a totals box shows numbers
   that appear nowhere else, it is an orphan — delete and rebuild from references.
4. **Per-row invariants:**
   - Demolition: `Removed ≤ (Wall Area − Fenestration)`
   - Floor area: `countable ≤ gross`
   - Subgrade: `countable = gross × exposed %` — a **product**, not a remainder
5. **Reality check the subgrade percentage.** A buried basement is single digits.
6. **Cross-sheet consistency:** the same level's gross area must be identical on
   the floor area sheet, the mitigation columns, and the summary.
7. **Plan labels equal table cells.** Every one.

---

## PART 2 — THE ERROR CATALOG

### Floor area

**The inverted subgrade calculation — the worst one.** The sheet correctly
computed a small exposed percentage, then reported countable area as the
*complement* (roughly 90% of gross) instead of the *product*. Countable =
gross × exposed %. A basement showing ~90% countable is always wrong.
This kind of wrong number **resurrects** — it gets copied to other sheets and
survives revisions. When you fix one, search every sheet for the old value.

**Garage math wrong two different ways.** One sheet put the *exempt* amount in
the countable column. Another subtracted an unexplained figure. Countable =
total − (first tier at 100% + second tier at 50%). And the garage area itself
drifted between CAD and spreadsheet across several values — one measured number,
everywhere.

**Garage folded invisibly into the main level** while the row was labeled
"excluding garage." The reviewer asked directly whether the number included
countable garage area. Keep the garage on its own line with its tier math shown.

**Patios counted at full value.** At-grade uncovered patios are not floor area at
all — they sit outside the exterior walls. Keep the row, show zero.

**Deck exemption computed on the wrong base.** The deck allowance is a percentage
of the property's **Allowable Floor Area**, not of the deck area or of some
intermediate figure.

**The attic problem — it will come up on every remodel.** The facts changed three
times on one project and the correct answer changed with them:
- Described as *finished with a door* → **counts** (finish alone kills the exemption).
- Established as *unfinished* with **door** access → still **counts** (a door is
  convenient access).
- *Unfinished*, door removed, **ceiling hatch and ladder only** → **exempt**.

**Different treatment on existing vs proposed is correct when the physical facts
differ per side.** Document finish condition AND access method on each plan, with
the citation. And where a low-clear-height band sits inside an attic that
otherwise counts, the code's own rules pull against each other — **get that in
writing from the Zoning Officer, don't pick one.**

**Mitigation and FAR treated the attic differently** — counted on one, exempt on
the other. Only the garage and subgrade exemptions may differ between those two
calculations. Everything else must match.

**A level's gross area drifted across five different values** because each sheet
re-measured it. What ended it was the sum test. A stubborn small ghost remainder
turned out to be a polyline discrepancy in CAD.

**Unfinished, no-access pockets behind knee walls** do qualify as exempt — but
each one needs its own hatch, its own area, and its own citation, and equivalent
pockets must be treated the same way on the existing side.

**Exemptions people reach for that do not exist:**
- The **airlock** exemption is **non-residential only** — not available to
  single-family, duplex, or multi-family.
- There is **no exemption** for fireplaces, chimneys, or interior wall cavities
  and chases. Anything inside the exterior face of framing counts.

**Legitimate ways to reduce countable area** (when a project is over a cap):
1. Check the **polyline basis** — drawn to face of framing, not face of veneer.
2. **Subgrade exposure** — usually the biggest lever; raising window-well slabs
   and finished grade reduces exposed wall directly. Limits: the slab cannot rise
   above the egress sill, the well must keep its code-minimum dimensions, and
   drainage must still work.
3. **Open-to-below voids** — removing floor structure removes floor area 1:1.
4. **Garage sizing** relative to the exemption tiers.

### Height

**No zone-district height-limit line on the elevations**, only a few unnumbered
measurement points, grade lines not legible as two distinct profiles, and no
height table. Rebuild to the City model format: numbered points with a tag shape
distinct from grid bubbles, both grade lines drawn full width with per-condition
restrictive labels, and a table keyed to the point numbers.

**A misread pitch** moved a point from the 1/2-point rule to the 1/3-point rule
and changed the answer. Verify every pitch label against the roof plan.

**The height table columns get misunderstood constantly:**
- "Most Restrictive" is a **word** (Natural or Finished), not a number.
- "Roof Height over Topography" is the **elevation of the roof measurement
  point**, not a computed height.
- Grade math ended up in the roof column and roof elevations in the grade column.
- One point carried an elevation copy-pasted from another row that sat far above
  the site — an impossible number that survived several revisions.

**A roof point below grade** produced a negative height. That is correct — label
it "N/A – BELOW GRADE."

### Demolition

**The fenestration column was almost all zeros.** This is the classic error — the
City flags it even in its own example set. The CAD elevations already carried the
values; nobody transcribed them into the spreadsheet. Watch for the wrong value
landing in that column too: one row held the *net wall* figure, another held the
*removed* figure.

**The removed column mixed bases** — some rows slope-adjusted, some raw plan
area. Removed must always be on the same basis as the denominator.

**One slope factor pasted down the whole roof table.** The 14:12 factor was used
for 8:12 planes; other rows were blank and dropped out of the denominator
entirely. Compute the factor per plane — `=SQRT(1+(rise/12)^2)` — never type it.
The factors look similar enough that this survives a casual read.

**SUM ranges truncated.** The roof total summed only part of the table; a wall
total omitted one wall entirely. Any total a hand re-add does not match is a
range bug, not a rounding issue.

**An orphan totals box** survived four revisions — its components matched no
table anywhere on the sheet, and eventually did not even equal its own displayed
sum. Totals boxes must be cell references.

**Diagram/table divergence.** Wall labels and areas must match between the
flat-plane diagrams and the table — the reviewer compares them. An unlabeled
hatched sliver on a diagram is a missing table row. One roof plane was hatched as
removed on the drawing but tabulated as zero.

**The demolition percentage climbed steeply as errors were corrected** — it more
than tripled from the first draft to the final honest number, entirely from
fixing fenestration, factors, SUM ranges, and diagram reconciliation. **An early
low demolition percentage is usually errors, not margin.** Treat a comfortable
first number as a red flag and audit it before relying on it.

That matters double because crossing the threshold strips mitigation credit for
existing floor area **and** strips nonconforming rights.

### Entitlements — the expensive one

**A prior P&Z resolution with a hard floor-area cap existed the entire time.**
The sheets said "Unique Approvals: N/A" and the whole compliance analysis ran
against the wrong ceiling for weeks. The reviewer's cryptic comment —
*"demonstrate how approvals are being met in the table"* — was asking for exactly
this.

**First question on any project: is there a prior land use approval? Get the
resolution before drawing anything.** Its dimensional tables govern, and you do
not relitigate its "existing" figure even if your re-measurement differs.

### Cross-sheet ripples — no number changes alone

- Light wells help egress and height, but they **increase** exposed subgrade wall
  and therefore countable floor area.
- Raising finished grade fixes floor area but **changes the height table's grade
  values and restrictive labels**, and has to match the civil drawings.
- Changing the attic determination changes **both** the floor area and the
  mitigation sheets.
- Crossing the demolition threshold changes the **mitigation basis** and the
  **nonconforming rights**.

---

## PART 3 — REVIEWER COMMENTS AND HOW TO ANSWER THEM

These are real City zoning review comments. The wording repeats.

| Comment | What it means / how to answer |
|---|---|
| "What is this depicting?" | An unlabeled graphic. Label it. |
| "What is this exemption here?" | Name the exemption, cite the subsection, show the tier math. |
| "Please include the entire garage floor number." | Total garage area as one labeled figure, then the tiers, then countable. |
| "Add sheet with mitigation floor area existing vs proposed — entire subgrade, entire main level including garage and upstairs, with exemptions for attic or top of stairs." | Add the two Mitigation columns to the summary (or separate sheets if pressed). Garage and subgrade counted **in full**; attic and stairs exempted the same as on the FAR sheet. |
| "Does this number include countable garage floor area? Please show your calculations." | Garage on its own line, arithmetic in the adjacent cell. |
| "These numbers do not match." | A plan label disagrees with a table cell. One measured geometry, transcribed once. |
| "Please add details on how attic is being accessed." | Access determines the exemption. State finish condition AND access method on the plan with the citation. |
| **"Demonstrate how approvals are being met in the table. Add more info."** | Show gross → each exemption with citation → countable, **and** the prior approval's caps with the comparison rows. Fill in Unique Approvals / Variances / Reception #. |
| "Walls __ don't match the diagram below. Please correct." | Table/diagram divergence in the subgrade or demo wall worksheet. |
| "Please add grade to the wall segments." | Draw natural **and** finished grade across every subgrade wall segment diagram. |
| "Look at the example on our website" (height) | Rebuild to the model format: code reference, property lines and setbacks, topography, dimensions of roof penetrations, numbered height points around the perimeter, both grade lines, measured from the lower of the two. Give **actual** penetration dimensions, not just the code maximum. |
| "From your legend it appears that all walls are being removed. If siding will be updated, don't use the same color as demolition. Ensure demolition matches the calculations sheet." | Re-skin is not demolition. Separate hatches per condition, coordinated with the calc sheet. |
| "Add the specific demolition legend that shows in the approvals — call it 'per Resolution XX Series XX.'" | Match the legend in the land use approval's exhibit. Another pointer to read the resolution. |
| "Add: line depicting subgrade area; dimensions to window wells; topography line numbers; all hot tubs, pools, outdoor kitchens and grills; retaining walls including TOW and BOW." | Add them all; state "none proposed" where true. |
| "Proposed equipment is in the setback. Please add dimensions. The equipment fence is also in the setback." | Dimension from the property lines and demonstrate compliance with fence height and material limits. **Equipment inside a required setback is a design problem, not a drafting fix.** |
| "This is an unshielded/partially shielded fixture. Please update your calculator." | Specify a fully shielded fixture and update the lighting calculation. |

---

## PART 4 — PUT THESE IN WRITING BEFORE SUBMITTING

Interpretation calls that should go to the City in writing
(**comdevzoning@gmail.com**) rather than be guessed on a sheet:

- Attic access and finish determinations, especially where access changes between
  existing and proposed
- Whether a low-clear-height band stays exempt inside an attic that otherwise counts
- Roof planes claimed as "built over, structure remains" rather than removed
- Any claimed demolition exemption — the City asks for this explicitly
- Stacked vs. separate stair runs for the vertical circulation exclusion
- TDR eligibility where the structure is nonconforming
- Whether reallocating area between above-grade and below-grade satisfies the
  nonconformity rule

The code already requires verifying existing conditions with the Zoning Officer
before demolition — bundle these questions into that conversation.

---

## PART 5 — PRE-SUBMITTAL CHECKLIST

**Completeness**
- [ ] All sheets present, or a documented reason one does not apply
- [ ] Zoning Summary with Net Lot Area and the six-column Floor Area Summary
- [ ] **Floor area legend on every page**
- [ ] Site coverage sheet
- [ ] Height measurement vignette on the height sheet
- [ ] Cumulative-demolition question answered
- [ ] Prior approvals listed with resolution number, series, and reception #

**Arithmetic**
- [ ] Sum test on every level, both conditions
- [ ] Same gross geometry across floor area, mitigation, and summary
- [ ] Attic, stairs, and decks treated identically for Allowable and Mitigation
- [ ] Net Lot Area computed from the slope table, with the reduction cap applied
- [ ] Subgrade: exposed ÷ total, never inverted; countable = gross × %
- [ ] Every wall's Removed ≤ (Area − Fenestration)
- [ ] Roof removed on the adjusted basis; one demolition method used throughout
- [ ] Every slope factor computed for its own pitch
- [ ] Every SUM range covers every row
- [ ] Every totals box built from cell references
- [ ] Percentages computed from full-precision sums

**Documentation**
- [ ] Every exemption tag carries its citation
- [ ] Arithmetic shown in adjacent cells
- [ ] Correct legend on each sheet type — the four are distinct
- [ ] Plan labels equal table cells everywhere
- [ ] Natural and finished grade on subgrade diagrams and all height elevations
- [ ] Mechanical, vents, roof drains, lighting, and projections shown
- [ ] Survey benchmark and datum noted
- [ ] Nonconformity statement if existing exceeds allowable
