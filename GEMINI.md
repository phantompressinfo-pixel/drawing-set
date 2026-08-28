# Aspen + Pitkin County Code Assistant — Project Instructions

You are helping an architectural drafting team (Eigelberger Architecture) with
City of Aspen and Pitkin County zoning/building code questions and zoning
submittal sheets. This repo contains the **complete text of both codes** plus a
battle-tested playbook and case log from a full City review cycle.

**Never answer an Aspen/Pitkin code question from memory alone.** Always search
the local files below and quote the exact section with its citation.

## What is in this repo

| Path | Contents |
|---|---|
| `code-library/aspen/` | Every title of the Aspen Municipal Code as .txt (Supp. No. 7 Update 1, through Ord. 06-2026, retrieved 2026-07-22). See `_INDEX.txt`. |
| `code-library/aspen/title-26-land-use-regulations.txt` | The entire Aspen Land Use Code — zoning districts, dimensional requirements, measurements, demolition, GMQS/mitigation, nonconformities. |
| `code-library/aspen/title-8-buildings-and-building-regulations.txt` | Adopted building codes + Aspen amendments (2021 IBC, energy, wildfire, NEC 2023). |
| `code-library/pitkin/` | Pitkin County Code + Land Use Code as .txt (through Ord. 019-2026); `pdf/` holds the official source PDFs (use them when a figure/diagram matters). |
| `.claude/skills/aspen-pitkin-code/references/zoning-submittal.md` | **The playbook.** For each of the four calc packages (Height Over Topography, Allowable Floor Area, Mitigation Floor Area/GMQS, Demolition): required sheet content, exact chart formats matched to the City's Model Zoning Submission, every equation, code citations for sheet notes, element-by-element rules (skylights, glass roofs, chimneys, dormers, patios, light wells, attics, stairs, garages), recurring reviewer comments and how to answer them, and pre-submittal self-checks. |
| `gem-package/knowledge-files/01`–`05` | **The portable method, with no project numbers in it**: how to answer, the steps and where to measure for each calculation package, blank chart templates for every sheet, the mistake catalog and reviewer comments, and the IBC/IRC jurisdictional split. Start here. |
| `gem-package/SETUP-README.md` | How to stand this up as a shared Gemini Gem for a whole office. |
| `.claude/skills/aspen-pitkin-code/references/case-log-844-roaring-fork.md` | **The case log** for 844 Roaring Fork Rd (permit 0065-2026-BRES): 26-item catalog of real errors and their fixes, all 17 City reviewer comments with resolutions, the 10-point working method, and final project numbers. |

## How to answer a code question

1. Search the relevant .txt file for the topic term (`height`, `setback`,
   `guard`, `demolition`, `lightwell`, `nonconform`, `mitigation`, ...).
   Aspen section headers look like `===== Sec. 26.575.020. - ...`.
2. Quote the controlling language and cite precisely
   (e.g. `§26.575.020(f)(4)(a)`; sheet-note style `26.575.020.F.4.A`).
3. City of Aspen parcels → Aspen Municipal Code. Unincorporated Pitkin County
   parcels → County Code + LUC. If jurisdiction is unclear, ask.
4. For screenshots of drawing sheets or calc tables: read every tag and note,
   verify each cited section against the library, **check the arithmetic**
   (sum every column yourself), and flag wrong citations, non-closing totals,
   and cross-sheet contradictions.
5. Building or checking any zoning submittal sheet? Read
   `zoning-submittal.md` first, and skim the case-log error catalog — the same
   mistakes recur on every project.
6. Municode deep link:
   `https://library.municode.com/co/aspen/codes/municipal_code?nodeId=<nodeId>`
   e.g. §26.575.020 → `TIT26LAUSRE_PT500SURE_CH26.575MISURE_S26.575.020CAME`

## Fast facts (verify in the text before citing on a sheet)

- **R-15**: max height 25 ft §26.710.050(d)(7); allowable floor area sliding
  scale §26.710.050(d)(10).
- **Height** §26.575.020(f): roof pitch 3:12–7:12 → measure at the 1/2 point
  eave-to-ridge; >7:12 → 1/3 point; <3:12 → top-most portion. **No limit on
  ridge height** for pitched roofs. Measured from the **lower** of natural or
  finished grade (depict both). Measured to the **first layer of sheathing**
  — a re-skin does not raise height.
- **Three floor areas** §26.575.020(d)(2): Gross · Allowable (all exemptions)
  · Mitigation (all exemptions **except** garage (d)(8) and subgrade (d)(9)).
- **Subgrade** (d)(9): countable = gross × (exposed wall ÷ total wall). Wall
  band = interior wall area projected outward — basement finished floor to
  underside of the floor structure above. Exposed = band above the **lower**
  of natural/finished grade; at window wells, finished grade is the well slab.
- **Garage** (d)(8): first 250 SF exempt, 251–500 at 50% (max 375 exempt),
  over 500 counts in full.
- **Attic** (d)(4): unfinished + necessity-only access (hatch/ladder) =
  exempt; a door = convenient access = counts; finished = counts regardless;
  ≤30" clear-height band exempt regardless of access or use; whole-room rule
  if any portion counts. Treat the attic **identically** in Allowable and
  Mitigation tables.
- **Stairs** (d)(3): counted at the lower level, excluded only at the
  top-most level served; a stacked stairwell gets ONE exclusion.
- **Airlock** (d)(16): non-residential only — **not** available for
  single-family homes.
- **No exemption** for fireplaces, chimneys, or wall cavities; open-to-below
  voids carry no floor area at that story. Measure to exterior face of
  framing, excluding veneer.
- **Demolition** §26.580.040: 40% threshold (35% is NOT in current code);
  wall + roof surface above finished grade, minus fenestration on both sides
  of the ratio; roof areas × slope factor √(1+(rise/12)²) (8:12 → 1.2019);
  re-skin/built-over with structure remaining is not demolition (c)(7);
  glass roofs = 100% fenestration including mullions; chimneys excluded;
  cumulative over 10 years (d).
- **Mitigation/GMQS** §26.470.090(a): net increase ÷ 1,000 × 0.107 = FTE;
  fee-in-lieu above 0.10 FTE requires Council. Crossing 40% demolition
  forfeits credit for existing floor area (§26.470.140(b)).
- **Nonconforming floor area** §26.312.030(c): alterations may not increase
  the nonconformity — proposed countable ≤ existing countable.
- **Prior land use approvals govern.** If the project has a P&Z/Council
  resolution, its dimensional table is a **binding ceiling** that can be
  stricter than zoning. "Demonstrate how approvals are being met in the
  table" = add resolution-vs-proposed comparison rows.
- **Aspen did NOT adopt the 2021 IRC** (§8.16.010; IBC §101.4.11 as amended
  by §8.20.020) — residential runs under the **2021 IBC**. Egress/area wells:
  IBC §1031 (no covers over required wells, §1031.6). Guards: IBC
  §1015.2/.3, 42" per City examples. (The City's own model set still uses IRC
  R310 citations — don't spend a resubmittal fighting it.)

## Working method (learned the hard way — see the case log)

1. One measured geometry: every number traces to a CAD polyline; charts
   reference cells, never re-typed results.
2. Sum test on every table: parts must add to the stated gross; column totals
   must cover every row (truncated SUM ranges were a repeat bug).
3. Per-row invariants: removed ≤ net wall; fenestration excluded from both
   numerator and denominator; countable subgrade = gross × ratio (never the
   complement).
4. No orphan totals boxes — every printed total must trace to a table.
5. Facts per side: existing vs proposed conditions (attic access, finishes)
   are separate determinations.
6. Anything ambiguous in the code → short letter to the Zoning Officer, don't
   guess on the sheet.
7. Check cross-sheet ripples: regrading changes height-table grade values and
   subgrade exposure; attic decisions hit FAR and Mitigation together.
8. Entitlements first: read prior approvals before drawing — the resolution
   cap, not the zone district, may control.

## Refreshing the library (codes get amended)

- Aspen (Municode backend API — the library website blocks plain fetches, the
  API does not):
  1. `https://api.municode.com/Clients/name?clientName=Aspen&stateAbbr=co` → ClientID 1085
  2. `https://api.municode.com/Jobs/latest/18107` → current jobId (productId 18107)
  3. Walk `https://api.municode.com/codesToc/children?jobId=<job>&nodeId=<node>&productId=18107`
  4. Fetch `https://api.municode.com/CodesContent?jobId=<job>&nodeId=<node>&productId=18107`,
     dedupe docs by Id.
- Pitkin: re-download the PDFs linked from
  `https://pitkincounty.com/468/County-Code`, extract with `pdftotext -layout`.
- Check the "codified through" banner when currency matters, and advise
  confirming interpretation with City/County staff for submittal-critical
  items.
