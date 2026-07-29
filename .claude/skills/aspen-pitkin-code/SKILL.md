---
name: aspen-pitkin-code
description: Answer questions about the City of Aspen Municipal Code (zoning, building, land use) and the Pitkin County Code / Land Use Code from the full local copy in code-library/, and help build or check Aspen zoning submittal sheets. Use whenever the user asks about Aspen or Pitkin code requirements, zoning (R-15, setbacks, height, floor area, demolition, mitigation/GMQS), building codes (IBC amendments, guardrails, egress, chimneys), permit/submittal requirements, responses to City zoning review comments, or sends a screenshot of a drawing sheet or calculation table with a code question. Answer from the local files — do not search the web first.
---

# Aspen + Pitkin County Code Library

The complete text of both codes is stored in this repo under `code-library/`.
Answer code questions by searching these files with Grep, then quote the exact
section with its citation. Never answer Aspen/Pitkin code questions from memory
alone — always verify against the stored text.

## Building or checking a zoning submittal? Read the reference first

**`references/zoning-submittal.md`** — the working playbook for City of Aspen
residential zoning submittals, built from a full review cycle including the City
reviewer's comments. Covers, for each of the four calculation packages:
the sheet content the City requires, the exact chart/column formats (matched to
the City's Model Zoning Submission examples), every equation, the code citations
for sheet notes, element-by-element treatment (skylights, glass roofs, chimneys,
dormers, patios, light wells, attics, stairs, garages), the reviewer comments that
recur and how to answer them, and a pre-submittal self-check list.

Packages covered: **Height Over Topography · Allowable Floor Area · Mitigation
Floor Area (GMQS) · Demolition** — plus the architectural site plan checklist and
the Aspen IRC/IBC trap.

Load it whenever the task involves: floor area or height calculations, demolition
percentages, mitigation/FTE, a screenshot of a calc table or zoning sheet, or
drafting a response to City zoning review comments.

## What is stored

### City of Aspen — `code-library/aspen/` (one .txt per title)
- Source: Municode, Supp. No. 7 Update 1, codified through Ord. No. 06-2026
  (enacted 2026-03-24). Retrieved 2026-07-22. `_INDEX.txt` lists all files.
- Key files:
  - `title-8-buildings-and-building-regulations.txt` — adopted building codes +
    Aspen amendments (2021 IBC, energy, wildfire, NEC 2023)
  - `title-26-land-use-regulations.txt` — the entire Aspen Land Use Code
    (zone districts, dimensional requirements, measurements, nonconformities,
    demolition, GMQS/mitigation, TDRs, historic preservation)

### Pitkin County — `code-library/pitkin/` (one .txt per title/chapter)
- Source: pitkincounty.com/468/County-Code PDFs. LUC current through
  Ord. No. 019-2026. Retrieved 2026-07-22.
- `title-11-building-construction.txt` — county building code adoption/amendments
- `luc-ch01` … `luc-ch12` — Title 8 Land Use Code: ch03 zoning districts,
  ch04 permitted uses, ch05 dimensional requirements (incl. 5-20-60 building
  height measurement), ch07 development standards, ch09 non-conformities,
  ch11 definitions
- `pdf/` — the official source PDFs. Text extraction loses figures/diagrams;
  when a question involves a figure (e.g., height measurement diagrams), Read
  the matching PDF pages.

## How to answer

1. Grep the relevant file(s) for the topic term (e.g. `height`, `setback`,
   `guard`, `demolition`, `lightwell`, `nonconform`, `mitigation`). Aspen section
   headers look like `===== Sec. 26.575.020. - ...`.
2. Quote the controlling language and cite it precisely
   (e.g. `§26.575.020(f)(4)(a)`, sheet-note style `26.575.020.F.4.A`).
3. City of Aspen parcels → Aspen Municipal Code. Unincorporated Pitkin County
   parcels → County Code + LUC. If jurisdiction is unclear, ask.
4. For screenshots of drawing sheets or calc tables: read the tags/notes in the
   image, verify each cited section against the library, check the arithmetic,
   and flag wrong citations, non-closing sums, and cross-sheet contradictions.
5. Deep link to a section on Municode:
   `https://library.municode.com/co/aspen/codes/municipal_code?nodeId=<nodeId>`
   e.g. §26.575.020 → `TIT26LAUSRE_PT500SURE_CH26.575MISURE_S26.575.020CAME`

## Fast facts (verify in the text before citing on a sheet)

- **R-15** max height 25 ft §26.710.050(d)(7); allowable floor area sliding scale
  §26.710.050(d)(10). R-15A is .060, R-15B is .070.
- **Height** §26.575.020(f): 3:12–7:12 → 1/2 point eave-to-ridge; >7:12 → 1/3
  point; <3:12 → top-most portion. **No limit on ridge height** for pitched roofs.
  Measured from the lower of natural/finished grade; both must be depicted.
  Measured to the **first layer of sheathing** — re-skin does not raise height.
- **Three floor areas** §26.575.020(d)(2): Gross · Allowable (all exemptions) ·
  Mitigation (all exemptions **except** garage (d)(8) and subgrade (d)(9)).
- **Subgrade** (d)(9): countable = gross × (exposed wall ÷ total wall).
- **Garage** (d)(8): first 250 exempt, 251–500 at 50%, over 500 counts.
- **Attic** (d)(4): unfinished + necessity-only access = exempt; ≤30" clear height
  exempt regardless of access; whole-room rule if any portion counts.
- **Demolition** §26.580.040: 40% threshold; wall + roof above finished grade
  minus fenestration; re-skin over remaining structure doesn't count (c)(7);
  cumulative over 10 years (d).
- **Mitigation** §26.470.090(a): net increase ÷ 1,000 × 0.107 = FTE. Crossing 40%
  demolition forfeits credit for existing area (§26.470.140(b)).
- **Aspen did NOT adopt the 2021 IRC** (§8.16.010; IBC §101.4.11 as amended by
  §8.20.020) — residential runs under the **2021 IBC**. Egress/area wells: IBC
  §1031, not IRC R310. Guards: IBC §1015.2/§1015.3, 42" per City examples.
- **Nonconforming floor area** §26.312.030(c): alterations may not increase the
  nonconformity — proposed countable ≤ existing countable.

## Refreshing the library (codes get amended)

- Aspen: Municode API —
  `https://api.municode.com/Clients/name?clientName=Aspen&stateAbbr=co` (ClientID 1085)
  → `Jobs/latest/18107` (productId) for current jobId
  → `CodesContent?jobId=<job>&nodeId=<node>&productId=18107`.
  The library site blocks plain fetches; the API does not. Downloader pattern:
  walk `codesToc/children`, fetch content per title, dedupe docs by Id.
- Pitkin: re-download PDFs linked from `https://pitkincounty.com/468/County-Code`,
  extract with `pdftotext -layout`.
- Check the "codified through" banner against today's date when currency matters;
  advise the user to confirm interpretation with City/County staff for
  submittal-critical items.
