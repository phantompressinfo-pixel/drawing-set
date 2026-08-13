---
name: aspen-pitkin-code
description: Answer questions about the City of Aspen Municipal Code (zoning, building, land use) and the Pitkin County Code / Land Use Code from the full copy of both codes bundled with this plugin, and help build or check Aspen zoning submittal sheets. Use whenever the user asks about Aspen or Pitkin code requirements, zoning (R-15, setbacks, height, floor area, demolition, mitigation/GMQS), building codes (IBC amendments, guardrails, egress, chimneys), permit/submittal requirements, responses to City zoning review comments, or sends a screenshot of a drawing sheet or calculation table with a code question. Answer from the local files — do not search the web first.
---

# Aspen + Pitkin County Code Library

The complete text of both codes ships with this plugin, under
`${CLAUDE_PLUGIN_ROOT}/code-library/`.
Answer code questions by searching these files with Grep, then quote the exact
section with its citation. Never answer Aspen/Pitkin code questions from memory
alone — always verify against the stored text.

## Building or checking a zoning submittal? Read the reference first

**`${CLAUDE_PLUGIN_ROOT}/skills/aspen-pitkin-code/references/zoning-submittal.md`** — the working playbook for City of Aspen
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

## Office package (project-number-free, portable to other AI tools)

`gem-package/` holds a self-contained version of this knowledge built for a
shared **Gemini Gem** (Google Workspace): `GEM-INSTRUCTIONS.txt`,
`SETUP-README.md`, `USER-GUIDE.md`, and ten `knowledge-files/`. It is **not
bundled in this plugin** — it lives at the root of the source repo,
`github.com/phantompressinfo-pixel/drawing-set`, because it is delivered to
Workspace rather than to Claude Code. Files 01–05 are
the tool-agnostic method — how to answer, the steps and **where to measure** for
each calculation package, blank chart templates for every sheet, the mistake
catalog and reviewer comments, and the IBC/IRC jurisdictional split. Files 06–10
are the code text.

**These carry no project numbers by design** — the numbers change every project;
the method does not.

## Nothing in this plugin is project-specific, and nothing should become so

This skill ships to every project the office runs. It therefore holds **rules and
method only**. No lot areas, no floor-area totals, no permit numbers, no prior
resolutions, no sheet numbering from a past job.

Per-project records live outside the plugin, in that project's own files —
in this office's source repo, under `projects/<project>/`. Read one only when
working on **that** project, and never carry a figure, an assembly, or a
resolution from one project into another. Two jobs in the same zone district
still have different lot areas, different nonconformities, and different prior
approvals; a number reused across projects is a wrong number on a sheet.

When a past project's pattern is genuinely general — a recurring reviewer
comment, an error worth checking for every time — the place for it is
`zoning-submittal.md`, stated generically, not a project record quoted verbatim.

## Need the model code text itself? Use the `us-building-codes` skill

Aspen's Title 8 adopts the IBC and amends it — it does not reprint it. When a
question needs the **full wording of an IBC section** (or IEBC or ADA text,
which this library has no copy of at all), search
`${CLAUDE_PLUGIN_ROOT}/code-library/us-building-codes/` via the `us-building-codes` skill. It holds
Colorado's 2021 IBC — the same edition Aspen adopted — plus IEBC 2021 and the
2010 ADA Standards.

**This skill still governs.** Always check Title 8 for an Aspen amendment before
presenting model text as the requirement, and say which layer you are quoting.

This is not a theoretical risk. **Aspen amends 46 IBC sections and Pitkin
amends 20 IBC + 15 IRC sections**, listed in
`${CLAUDE_PLUGIN_ROOT}/skills/us-building-codes/references/locally-amended-sections.txt`.
`codesearch.py` reads that list and stamps `*** AMENDED LOCALLY ***` on any
result it covers. Heed the stamp — the model text shown is superseded.

Example: model IBC §1015.2 requires guards along "aisles, stairs, ramps and
landings"; Aspen's §1015.2 adds **"and adjacent to hot tubs, spas, and pools"**,
and its §1015.3 adds Exception 9 (18 in. guards where the open side is under
18 in. from the water's edge). Quoting the model text there would be wrong.

## What is stored

### City of Aspen — `${CLAUDE_PLUGIN_ROOT}/code-library/aspen/` (one .txt per title)
- Source: Municode, Supp. No. 7 Update 1, codified through Ord. No. 06-2026
  (enacted 2026-03-24). Retrieved 2026-07-22. `_INDEX.txt` lists all files.
- Key files:
  - `title-8-buildings-and-building-regulations.txt` — adopted building codes +
    Aspen amendments (2021 IBC, energy, wildfire, NEC 2023)
  - `title-26-land-use-regulations.txt` — the entire Aspen Land Use Code
    (zone districts, dimensional requirements, measurements, nonconformities,
    demolition, GMQS/mitigation, TDRs, historic preservation)

### Pitkin County — `${CLAUDE_PLUGIN_ROOT}/code-library/pitkin/` (one .txt per title/chapter)
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
  §26.710.050(d)(10) — a lot-area table, not a single ratio. The neighbouring
  zone districts are at their own *sections*: **R-15A = §26.710.060,
  R-15B = §26.710.070** (section numbers, not FAR values).
- **Height** §26.575.020(f): 3:12–7:12 → 1/2 point eave-to-ridge; >7:12 → 1/3
  point; <3:12 → top-most portion. **No limit on ridge height** for pitched roofs.
  Measured from the lower of natural/finished grade; both must be depicted.
  Measured to the **first layer of sheathing** — re-skin does not raise height.
- **Three floor areas** §26.575.020(d)(2): Gross · Allowable (all exemptions) ·
  Mitigation (all exemptions **except** garage (d)(8) and subgrade (d)(9)).
- **Subgrade** (d)(9): countable = gross × (exposed wall ÷ total wall).
- **Garage** (d)(8): three different rules — check the property type first.
  - Single-family / two single-family / duplex, **outside R-15B**: first 250
    exempt, 251–500 at 50%, over 500 counts (Table 26.575.020-2).
  - **R-15B**: flat 500 sq ft maximum exemption **for the whole parcel**.
  - Multi-family, parcels with >2 units, or units in a mixed-use building: flat
    250 sq ft per residence, **no 50% tier** — everything above 250 counts.
  - No residential units on the parcel: no exclusion at all.
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
