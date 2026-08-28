# Case Log — 844 Roaring Fork Rd (Aspen, R-15, single-family remodel/addition)

The complete record of one full zoning review cycle: every error found, how it was caught,
every City reviewer comment and its resolution, and the working method that emerged. This is
the experiential layer on top of `zoning-submittal.md` (the rules). Read both. When checking
a new project's sheets, hunt for **these exact error patterns first** — every one of them
actually happened.

Project profile: existing house partly re-skinned, partly demolished, large new basement
(~6,000 sf), R-15 (25 ft height, 4,667 sf allowable on 17,791 sf Net Lot Area), existing
structure nonconforming as to floor area, prior P&Z Special Review resolution (§26.430)
continuing the nonconformity with a hard proposed-floor-area cap.

---

## 1. ERROR CATALOG — what went wrong, in the order it was caught

### Height package
1. **No zone-district height-limit line** on elevations; only ~3 unnumbered measurement
   points; grade lines illegible as two profiles; no height table; missing mechanical/vents,
   site wall TOW, chimney dimensions. Fixed by building to the City model format: numbered
   points (distinct tag shape from grid bubbles), both grade lines full-width with
   per-condition restrictive labels, table keyed to points.
2. **A pitch misread** (5:12 called 8:12) would have moved a point from the 1/2-point rule to
   the 1/3-point rule. Verify every pitch label against the model.
3. **Height table columns misunderstood**: "Most Restrictive" is a *word* (Natural/Finished),
   not a number; "Roof Height over Topography" is the *elevation of the roof measurement
   point*, not a computed ceiling. First drafts had grade math in the roof column and vice
   versa; one point carried a 8029' value ~150 ft above the site (copy/paste from another
   row) and two points showed roof elevations at/below their own grade (grade values pasted
   into the roof column).
4. **A roof point below grade** (green roof over basement) produced a negative height —
   correct, label "N/A – BELOW GRADE," not an error.
5. Sheet citations initially `IRC R310.2` for egress wells — Aspen deleted the IRC
   (§8.16.010; IBC §101.4.11 amended). Correct: IBC §1031 + zoning §26.575.020.F.4.J.
   *Nuance:* the City's own model sheets also say "PER IRC R.310.2" — so zoning reviewers
   don't flag it; don't spend a resubmittal on it, but IBC is the technically adopted code.
   §1031.6 **prohibits covers/grilles over area wells outright** — a "gate and latch" is
   only legal as part of the perimeter guard around the well, never over the opening.

### Floor area package
6. **The inverted subgrade calc — the single worst error.** Sheet computed 2.42% exposed,
   then reported countable = 931 of 1,024 (≈91%) — the complement, not the product. Correct:
   1,024 × 2.42% = 25. The wrong 931 kept resurrecting across sheets for multiple revisions
   ("zombie number"). A ~90% countable basement is always wrong; buried basements run 2–10%.
7. **Garage math wrong twice differently**: one sheet put the *exempt* amount (375) in the
   countable column; another showed countable = total − 65. Correct: countable =
   total − (250 + 50% of next 250). Also the garage area itself flip-flopped 561/565/567
   between CAD and spreadsheet — one measured number, everywhere.
8. **Garage folded invisibly into the main-level figure** while labeled "Excl Garage" —
   reviewer asked "does this number include countable garage floor area?" Keep garage on its
   own line with its tier math shown.
9. **Patios counted at full value** in floor area. At-grade uncovered patios are not floor
   area at all (§26.104.100 definition). Keep the row, show 0.
10. **Deck exemption computed on the wrong base** (3,118 × 15% = 467.7 from an unknown
    number). Correct base is the property's Allowable Floor Area: 4,667 × 15% = 700.
11. **The attic saga** — the facts changed three times and the answer changed with them:
    - Claimed exempt while described as *finished with a door* → counts (finished kills the
      exemption regardless of access).
    - Then established as *unfinished*: door access (existing) → **counts** ("unfinished
      >4 ft with convenient access is counted"); ceiling-hatch-only (proposed, door removed)
      → **exempt** (pull-down-ladder example). **Different treatment per side is correct
      when the physical facts differ per side** — document access + finish on each plan.
    - Whole-room rule vs ≤30" band (rule 4 vs rule 3 of (d)(4)): genuinely ambiguous whether
      a counted attic keeps its ≤30" band exemption. Flagged to the Zoning Officer in
      writing rather than guessed.
12. **Mitigation and FAR sheets treated the attic differently** (counted on one, exempt on
    the other). Only garage (d)(8) and subgrade (d)(9) may differ between those two
    calculations; everything else must match.
13. **Upper-level gross drifted across five values** (1,059 → 1,086 → 1,367 → 1,426 → 1,675
    existing; 978 → 1,195 → 1,511 → 1,926 → 1,760 proposed) because levels were re-measured
    per sheet. The fix that ended it: the **sum test** — habitable + every tagged exemption
    must equal the measured gross exactly (existing closed at 1,675+118+121+24+6+9+7=1,960;
    proposed at 1,195+565=1,760). A persistent 59-sf ghost was a polyline discrepancy.
14. **Unfinished no-access knee-wall pockets** (94/90/14/14 sf) qualify as exempt a fortiori
    — but each needs its own hatch, area, and citation, and equivalent pockets must be
    treated the same on the existing side.
15. **Airlock exemption does NOT apply to single-family** — (d)(16) is non-residential only.
    (An early draft of the playbook got this wrong.)
16. **No exemption exists for fireplaces, chimneys, or wall cavities.** Only legitimate
    trims: polylines drawn to face of veneer instead of face of framing (code excludes
    sheathing/insulation/veneer), and open-to-below voids (no floor = no area at that story).

### Demolition package
17. **Fenestration column almost all zeros** — the classic error; the City flags it in its
    own model set. The CAD elevations already carried the values; the spreadsheet was never
    transcribed from them. One row had the *net wall* value (784−427=357) sitting in the
    fenestration column; another had the *removed* value there.
18. **Removed column on mixed bases** — some rows adjusted (slope-factored), some plan-area.
    Removed is always on the same basis as the denominator. Per-wall invariant:
    Removed ≤ (Area − Fenestration); a fully-removed wall with a window = net, never gross
    (wall E: 70 gross, 7 window, removed = 63 not 70).
19. **Wrong slope factor pasted down the whole roof table**: 1.5366 (the 14:12 factor) used
    for 8:12 planes (correct 1.2019); 6:12 rows also wrong; 10.5:12 rows blank (omitted from
    the denominator entirely). Factor = √(1+(rise/12)²); compute it, never type it.
20. **SUM ranges truncated** — roof total summed only rows A–K (verified by re-adding);
    exposed-wall total omitted wall P (76 sf). Any total that a hand re-add doesn't match is
    a range bug.
21. **Orphan totals box** — "4,761 + 2,589.87 = 7,350.87 … 11.65%" survived four revisions;
    the components matched no table anywhere (and eventually didn't even equal their own
    displayed sum). Totals boxes must be cell references to the tables on the sheet. The
    City's own model has the same disease (roof used = 1,388.75 on one sheet, 1,422.95 on
    another, for the same roof).
22. **Element rulings established**: glass roofs = 100% fenestration incl. mullions (zero
    both sides); skylights = fenestration (new/relocated ones cut into remaining roof DO
    count as removed); masonry chimneys = not assemblies, excluded; demolished dormers land
    in BOTH tables (roof planes + face/cheek walls net of window); roof *built over* with
    structure remaining = not removed (c)(7); partial-plane cutouts get their own factored
    rows; re-skin (structure remains) = zero.
23. **The demo % journey: 11.65% → 23.85% → 36.31%** as fenestration honesty, correct
    factors, complete ranges, diagram-vs-table reconciliation (plane BB hatched removed but
    tabulated 0), and element rulings landed. Lesson: an early low demo % is usually errors,
    not margin. Also: the "35% documentation trigger" in project notes is NOT in the current
    code — only 40% is; and cross-checking 40% matters double because §26.470.140(b) strips
    mitigation credit and §26.312.030(f)(2) strips nonconforming rights past it.
24. **Diagram/table divergence** — wall labels and areas must match between flat-plane
    diagrams and the table (reviewer: "Walls B, C, F, P don't match the diagram below");
    an unlabeled hatched sliver on a diagram is a missing table row.

### Entitlement discovery (late — should have been first)
25. **A prior P&Z Special Review resolution (§26.430) existed the whole time** with a hard
    cap: proposed floor area ≤ 5,252 sf. The sheets said "Unique Approvals: N/A" and the
    compliance analysis ran against the wrong ceilings for weeks. The reviewer's cryptic
    "Demonstrate how approvals are being met in the table" was asking for exactly this.
    **First question on any Aspen project: is there a prior land use approval? Get the
    resolution before drawing anything.** Its dimensional tables govern; don't relitigate
    its "existing" figure even if re-measurement differs.
26. **Closing the gap**: proposed was 176 sf over the cap. Patios (already 0), fireplaces
    (no exemption), and wall cavities (no exemption) were dead ends. The working levers:
    (1) polyline basis check — face of framing, not veneer; (2) **subgrade exposure** — the
    big one: raising window-well slabs and grade cut exposed wall 275→41 sf, countable
    383→57, total 5,428→5,102, from 176 over to 150 under; (3) open-to-below voids 1:1;
    (4) garage to ≤500 sf. Exposure mechanics: the measured band runs from basement finished
    floor to the underside of the floor structure above ("interior wall area projected
    outward"; drop ceilings don't count); exposed = that band above the lower of
    natural/finished grade; at a well, the well slab is the finished grade, so exposed =
    well width × (ceiling plane − slab), and the top never moves — only the bottom.
    Constraints: slab at/below the egress sill, IBC well minimums, drainage. Every sf of
    exposed wall ≈ (subgrade gross ÷ total wall) sf of countable.
    **Ripple check:** raising finished grade changes the height table's grade values and
    restrictive labels (never worsens height — lower-of governs) and must match civil.

---

## 2. THE CITY'S REVIEW COMMENTS (reviewer: magdad, 7/2026) — all 17, with resolutions

| # | Sheet | Comment (verbatim gist) | Resolution |
|---|---|---|---|
| 1 | Cover | "What is this depicting?" | Label the unclear graphic |
| 2 | Existing FA | "What is this exemption here?" (garage tiers) | Name it, cite (d)(8), show tier math |
| 3 | Existing FA | "Please include the entire garage floor number" | Total garage as one figure + tiers + countable |
| 4 | Existing FA | "Add sheet with mitigation floor area existing vs proposed… entire subgrade, entire main level including garage and upstairs with exemptions for attic or top of stairs" | Mitigation columns/sheets; garage & subgrade counted in full per (d)(2)(a)(iii) |
| 5 | Proposed FA | "Does this number include 125 countable garage floor area? Please show your calculations" | Garage on its own line; arithmetic in adjacent cell |
| 6 | Proposed FA | "These numbers do not match" | One measured geometry; plan label = table cell |
| 7 | Proposed FA | "Please add details on how attic is being accessed" + red note "THIS ATTIC SPACE DOES NOT HAVE ACCESS" | Access + finish stated on plan with (d)(4) citation; per-side facts |
| 8 | Proposed FA | "Demonstrate how approvals are being met in the table. Add more info" | Show derivation AND the P&Z resolution cap with the comparison |
| 9 | Subgrade walls | "Walls B, C, F, P don't match the diagram below. Please correct" | Reconcile table to CAD; found the missing wall-P sum too |
| 10 | Subgrade walls | "Please add grade to the wall segments" | Natural + finished grade drawn on every segment diagram (matches the model's own Staff Note) |
| 11 | Height | "Look at the example on our website… add: reference 26.575.020.F; property lines and minimum setbacks; topography; dimensions of any proposed roof penetrations; height points around perimeter; measurements from lower of natural/finished grade; both grade lines depicted" | Rebuild to model format; general method note; actual penetration dimensions, not just code maximums |
| 12 | Demo plan p17 | "From your legend it appears that all walls are being removed, windows etc. If siding will be updated, don't use the same color as demolition. Ensure demolition matches actual demolition calculations sheet" | Separate graphics per condition; re-skin ≠ demo per (c)(7); plans coordinated to calc sheet |
| 13 | Demo plan p18 | (same) | (same) |
| 14 | Demo elevations | "Add the specific demolition legend that shows in the approvals. Call it 'per Resolution XX Series XX'" | Match the resolution's Exhibit A legend — another pointer to the prior approval |
| 15 | Site plan | "Add: line depicting subgrade area; dimensions to window wells; topography line numbers; all hot tubs, pools, outdoor kitchens/grills; retaining walls including TOW and BOW height measurements" | All added; state "none proposed" where true |
| 16 | Site plan | "Proposed CU equipment is in the setback. Please add dimensions. The equipment fence is also in the setback. Add dimensions to demonstrate compliance with fence materials and height" | Dimensions from property lines; fence <42" in setback / 6 ft only behind street façade (§26.575.020, materials §26.575.050). Equipment in a setback is a design problem, not a drafting fix |
| 17 | Lighting | "This is unshielded/partially shielded fixture. Please update your calculator" | Fully shielded fixture; update lighting calc |

---

## 3. THE WORKING METHOD (what made the numbers finally converge)

1. **One measured geometry.** Each level's polylines measured once; every sheet transcribes
   from that one set. Retyping between sheets spawned five versions of the upper level.
2. **The sum test on every level, both conditions**: countable + every tagged exemption =
   gross, exactly. Untagged area means a missing hatch or a wrong gross.
3. **Formulas, not typed results**: slope factor =SQRT(1+(rise/12)^2); removed cells =G(row);
   totals = full-range SUMs; totals boxes = cell references across sheets; percentages from
   full-precision sums. Every hand-typed total in this project was eventually wrong.
4. **Per-row invariants as audits**: Removed ≤ Area − Fenestration; countable ≤ gross;
   basement countable % ≈ 2–10%; roof removed on the adjusted basis.
5. **Show the arithmetic in the adjacent cell** (the City model's own habit): "(1,024 ×
   2.42%)", "(250 @ 100% + 250 @ 50%)". It answers "show your calculations" pre-emptively.
6. **Every exemption tag carries its citation** in sheet-note style (26.575.020.F.4.A style
   for height; (d)(3)/(d)(4)/(d)(8)/(d)(9) for floor area).
7. **Facts are per-side**: existing and proposed each get the exemption analysis their own
   physical condition supports (the attic door). Same rulebook, each side's own facts.
8. **Interpretation calls go to the Zoning Officer in writing** (comdevzoning@gmail.com):
   attic rule-3-vs-rule-4, built-over roofs, stacked-vs-separate stairs, TDR eligibility on
   a nonconforming structure. §26.470.140(c) requires pre-demo verification anyway.
9. **Cross-sheet ripples**: light wells help egress/height but count as exposed wall in
   (d)(9); raising grade fixes FAR but changes the height table's grade values and must
   match civil; crossing 40% demo would strip both mitigation credit and nonconforming
   rights. No number changes alone.
10. **Read the entitlements first.** The prior resolution should have been step zero.

---

## 4. FINAL STATE (for continuity if this project returns)

- Height: 8 points, all compliant; tallest 21'-0" vs 25' limit; P6 N/A below grade.
- Demolition: walls 5,277/1,426 fen/3,851 used/1,663 removed; roof 4,493 plan/89 fen/
  5,272 used/1,651 removed (one unlabeled K/L sliver still to add); **36.31% < 40%**.
- Mitigation: existing 6,849 / proposed 11,436 (upper 1,675 vs 1,195); net 4,587 →
  **0.49 FTE** (>0.10 → fee-in-lieu needs Council; certificate/RO/deferral are by-right).
- Floor area: existing 5,475 (nonconforming); **P&Z resolution cap 5,252**; proposed after
  the exposure fix (exposed 275→41, subgrade 383→57): **5,102 — under cap by 150**.
- Open at last update: per-wall breakdown of the 41 sf exposed; resolution number/series/
  reception # onto Unique Approvals and the summary comparison rows; demo legend per the
  resolution's exhibit; height-table grade values updated for the regrading; K/L roof
  sliver; egress check on raised well slabs; CAD tag sync to final table values.
