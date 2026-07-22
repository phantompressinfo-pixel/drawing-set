---
name: aspen-pitkin-code
description: Answer questions about the City of Aspen Municipal Code (zoning, building, land use) and the Pitkin County Code / Land Use Code from the full local copy in code-library/. Use whenever the user asks about Aspen or Pitkin code requirements, zoning (R-15, setbacks, height, floor area, demolition), building codes (IBC amendments, guardrails, egress, chimneys), permit/submittal requirements, or sends a screenshot of a drawing sheet with a code question. Answer from the local files — do not search the web first.
---

# Aspen + Pitkin County Code Library

The complete text of both codes is stored in this repo under `code-library/`.
Answer code questions by searching these files with Grep, then quote the exact
section with its citation. Never answer Aspen/Pitkin code questions from memory
alone — always verify against the stored text.

## What is stored

### City of Aspen — `code-library/aspen/` (one .txt per title)
- Source: Municode, Supp. No. 7 Update 1, codified through Ord. No. 06-2026
  (enacted 2026-03-24). Retrieved 2026-07-22. `_INDEX.txt` lists all files.
- Key files:
  - `title-8-buildings-and-building-regulations.txt` — adopted building codes +
    Aspen amendments (2021 IBC, energy, wildfire, NEC 2023)
  - `title-26-land-use-regulations.txt` — the entire Aspen Land Use Code
    (zone districts, dimensional requirements, measurements, nonconformities,
    demolition, TDRs, historic preservation)

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
   `guard`, `demolition`, `lightwell`, `nonconform`). Aspen section headers
   look like `===== Sec. 26.575.020. - ...`.
2. Quote the controlling language and cite it precisely
   (e.g. `§26.575.020(f)(4)(a)`, sheet-note style `26.575.020.F.4.A`).
3. City of Aspen parcels → Aspen Municipal Code. Unincorporated Pitkin County
   parcels → County Code + LUC. If jurisdiction is unclear, ask.
4. For screenshots of drawing sheets: read the tags/notes in the image, check
   each cited code section against the library, and flag wrong citations.

## Verified facts for the current project (single-family remodel, R-15, Aspen)

- R-15 max height **25 ft** — §26.710.050(d)(7). R-15A is .060, R-15B is .070.
- Height measurement — §26.575.020(f): pitch 3:12–7:12 → 1/2 point eave-to-ridge;
  >7:12 → 1/3 point; <3:12 → top-most portion. **No limit on ridge height** for
  pitched roofs. Measured from the lower of natural/finished grade at each
  point; both grades must be shown on permit plans ((f)(3)(a)). Within the
  footprint >15 ft from perimeter, use projected natural grade ((f)(3)(b)).
  Roof measured to first layer of sheathing/membrane; surface treatments
  (reskin) excluded ((f)(3)(c)).
- Height exceptions — §26.575.020(f)(4): chimneys 10 ft above connection (a);
  mechanical 6 ft incl. pad/screening (e); lightwells/basement stairwells (j);
  dormer exclusion (≤50% of roof plane, ridge not above main) is (f)(2)(g).
  Rooftop railings & elevator/stair enclosures get NO exception on
  single-family/duplex.
- **Aspen did NOT adopt the 2021 IRC** (§8.16.010) — residential work runs under
  the **2021 IBC as amended by §8.20.020**. Egress wells: IBC §1031 (not IRC
  R310). Guards: IBC §1015.2 (amended) / §1015.3 — 42" per City example sets.
- Demolition: 40% triggers "demolition"; 35% triggers documentation/review;
  measured on exterior wall + roof surface above finished grade minus
  fenestration. Nonconforming structures — §26.312.030: purposeful demolition
  (≥40%) forfeits nonconforming rights ((f)(2)).

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
