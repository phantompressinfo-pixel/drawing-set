---
name: us-building-codes
description: Look up model building code text — IBC, IRC, IEBC and the 2010 ADA Standards — from the local dataset in code-library/us-building-codes/. Use when the user asks what a model code section says, asks for the text or number of an IBC/IRC/IEBC/ADA provision (egress, guards, stairs, occupancy, fire ratings, accessibility, heights and areas, existing-building alterations), asks which code sections apply to a building element or design phase, or wants to compare Colorado's adopted code against the unamended ICC baseline. For City of Aspen or Pitkin County local amendments, zoning, floor area or height calculations, use the aspen-pitkin-code skill instead — that one governs.
---

# US Building Codes Dataset (IBC / IRC / IEBC / ADA)

Structured model-code text stored under `code-library/us-building-codes/`.
Answer from these files — never from memory — and always cite the section number.

## When this skill vs. `aspen-pitkin-code`

`aspen-pitkin-code` is the **authority** for anything local: Aspen/Pitkin
amendments, zoning, land use, floor area, height, demolition, GMQS. It wins on
conflict, because Aspen amends the IBC and those amendments are not in this
dataset.

This skill is the **model-code text underneath** — the full wording of a section
when the local code only names it, plus IEBC and ADA, which `code-library/`
otherwise has no copy of.

Typical division of labor: Aspen adopts the 2021 IBC (`§8.20.010`) and
explicitly did *not* adopt the 2021 IRC — `§8.16.010` states it "will not be
adopted", and `§101.4.11` as amended deletes every IRC reference. So a
residential egress or guard question resolves to 2021 IBC, and this dataset
holds Colorado's 2021 IBC text for it. Pitkin County *does* adopt the 2021 IRC
(`§11.20.010`).

### Locally amended sections are flagged automatically

`references/locally-amended-sections.txt` lists every model section Aspen or
Pitkin amends — **46 IBC sections for Aspen, 20 IBC + 15 IRC for Pitkin**.
`codesearch.py` stamps `*** AMENDED LOCALLY ***` on any result it covers and
repeats them in the summary.

**When you see that stamp, the text shown is superseded — do not quote it.**
Read the amendment in `code-library/aspen/title-8-…` or
`code-library/pitkin/title-11-…` and cite that instead.

The stamp is a floor, not a ceiling: it covers sections named in the adopting
ordinances as of 2026-07-31. Re-extract it when either code is re-supplemented,
and still check Title 8 / Title 11 for anything submittal-critical.

## What is stored

`code-library/us-building-codes/<jurisdiction>/<code>-<year>/chapter-N-*.csv`

| Jurisdiction | Codes | Chapters | Notes |
| --- | --- | --- | --- |
| `colorado/` | ibc-2021, irc-2021, iebc-2021 | **IBC 1–35 · IRC 1–44 · IEBC 1–16** | Matches Aspen's adopted 2021 IBC edition |
| `gsa/` | ibc-2024, irc-2024, iebc-2024 | IBC 1–35 · IRC 1–15 · IEBC 1–16 | Unamended ICC baseline — the "source of truth" |
| `ada/` | `ada-standards-2010.csv` | flat | 2010 ADA Standards for Accessible Design |

~20,200 provisions across 163 CSVs. Source: scraped from up.codes, enriched with
LLM-inferred metadata. Origin repo: `github.com/thexqin/us-building-codes-dataset`
(see `LICENSE` in the data folder).

### Coverage limits — read before claiming a section is absent

- **Colorado IBC and IRC are both complete** — IBC 1–35 (concrete, masonry,
  steel, wood, aluminum, glazing, gypsum, plastics, electrical, mechanical,
  plumbing, elevators, special construction) and IRC 1–44 (mechanical 12–23,
  fuel gas 24, plumbing 25–33, electrical 34–43). **IEBC 1–16** is complete.
  IRC section numbers carry their letter prefix — `P2903.5`, `M1601.4`,
  `E3901.1`, `G2415` — so search by that form.
- **GSA IRC still stops at chapter 15.** Only the Colorado IRC was completed.
  GSA is the comparison baseline, so this rarely matters; if a GSA IRC question
  lands in 16–44, use the Colorado copy and note the edition difference.
- **No IBC or IRC appendices**, with one exception (IRC `AG`, piping standards).
  up.codes marks them `disabled` for Colorado — the state's adoption does not
  publish them.

  **This is a real gap for Pitkin County**, which adopts more appendices than
  the dataset carries (verified against
  `code-library/pitkin/title-11-building-construction.txt`):

  | Jurisdiction | Adopts appendices | Held locally? |
  | --- | --- | --- |
  | **Aspen** IBC 2021 (§8.20.010) | C, E, P | **No** |
  | **Pitkin** IBC 2021 (§11.04.010) | C, E, I, J | **No** |
  | **Pitkin** IRC 2021 (§11.20.010) | AE, AF, AH, AK, AQ | **No** — except the AQ amendments |

  Pitkin adopts these **by reference** ("as published by the International Code
  Council"), so title-11 contains only its *amendments*, not the appendix text.
  The only appendix content actually in the repo is Pitkin's amendment of
  Appendix AQ — `AQ106.1` (air leakage ≤0.30 cfm50/sf) and `AQ106.2`
  (alternative energy compliance).

  So for radon control (AF), patio covers (AH/I), sound transmission (AK),
  manufactured housing (AE), agricultural buildings (C), supplementary
  accessibility (E) or grading (J): **the requirement text is not in this repo
  at all.** Say so and point to up.codes or the ICC-published appendix. Do not
  imply title-11 answers it — it only says the appendix is adopted.
- Tables and figures flatten badly into `body` text — see the note below.
- IBC ch. 35 and IRC ch. 44 (referenced standards) are each a single row holding
  the whole standards table; search with a keyword rather than expecting
  per-standard rows.
- Tables and figures flatten badly into the `body` text. When a provision turns
  on a table (occupant load factors, fire-resistance ratings, height/area), say
  the value came from flattened text and recommend confirming against the
  published table.
- `gsa/` is the **2024** edition; `colorado/` is **2021**. Do not present a GSA
  section as the adopted Colorado requirement — the edition differs.

## How to search

Use the helper — CSV bodies are long single lines and raw Grep output is
unreadable:

```bash
python3 .claude/skills/us-building-codes/scripts/codesearch.py "guard" --code ibc --chapter 10
python3 .claude/skills/us-building-codes/scripts/codesearch.py --section 1015.2 -j colorado
python3 .claude/skills/us-building-codes/scripts/codesearch.py "grab bar" -j ada --full
python3 .claude/skills/us-building-codes/scripts/codesearch.py --category means_of_egress --responsibility architect -j colorado
```

Flags: `-j/--jurisdiction` (colorado|gsa|ada) · `-c/--code` (ibc|irc|iebc) ·
`-n/--chapter` · `-s/--section` (exact id) · `--category` · `--responsibility` ·
`--occupancy` · `--ifc-type` · `--phase` · `--full` · `--limit` · `--count`.

Start with `--count` on a broad term to gauge the result size, then narrow by
chapter or section. Plain `Grep` on the CSVs also works (no embedded newlines) —
use it when you want to confirm a section number exists before pulling the text.

## Row schema

`id, section, title, ifc_type, occupancy, design_phase, code_category,
primary_responsibility, body` — multi-value fields are pipe-delimited.

- `id` — section number (`1015.2`). Chapter overview rows carry a bare number.
- `section` — hierarchy path (`Section 1015 Guards`).
- `body` — cleaned plain text of the provision, including its exceptions.

### Metadata is inferred — treat it as a filter, not as fact

`ifc_type`, `occupancy`, `design_phase`, `code_category` and
`primary_responsibility` were not written by the code authors. They are good for
*narrowing a search* and worthless as an authority. Never tell the user "this
section applies to Residential (R)" on the strength of the metadata — that
determination comes from the `body` text and the local code.

Two provenances, both non-authoritative:

- **Upstream chapters** (IBC 1–18, IRC 1–15, IEBC, ADA) — per-section LLM
  inference. All five fields populated.
- **Locally-parsed chapters** (IBC 19–35, IRC 16–44) — `code_category` and
  `primary_responsibility` only, assigned per chapter by
  `scripts/backfill_metadata.py` from a static table (ch. 23 is Wood, so every
  section in it is `structural_design`/`structural_engineer`). Deterministic and
  auditable. `ifc_type`, `occupancy` and `design_phase` are left **empty** —
  those vary section to section and were not guessed.

So `--occupancy`, `--ifc-type` and `--phase` reach only upstream chapters.
`codesearch.py` prints a `NOTE:` counting rows that matched everything except an
empty metadata field, so this never silently narrows a result. Heed that note —
re-run without the filter when it appears.

The values are also dirty: `ifc_type` case varies (`StairFlight` /
`Stairflight`), and a few `occupancy` cells contain leaked Python list syntax.
The helper substring-matches case-insensitively, which absorbs this.

Vocabularies actually present:

- `code_category` (18): `means_of_egress`, `fire_resistance_smoke_protection`,
  `fire_protection_alarm_systems`, `structural_design`, `accessibility`,
  `assemblies_envelope`, `finishes_materials`, `occupancy_classification`,
  `building_height_area_limits`, `construction_type_ratings`,
  `special_construction`, `site_planning`, `interior_environment`,
  `mechanical_systems`, `plumbing_systems`, `electrical_systems`,
  `elevators_conveying_systems`, `hazardous_materials`
- `primary_responsibility` (8): `architect`, `structural_engineer`,
  `mechanical_engineer`, `electrical_engineer`, `civil_engineer`,
  `fire_protection_engineer`, `elevator_consultant`, `owner`
- `design_phase` (5): `concept`, `sd`, `dd`, `cd`, `ca`
- `occupancy` — IBC groups, e.g. `Assembly (A)`, `Business (B)`, `Residential (R)`
- `ifc_type` — IFC element classes, e.g. `Wall`, `Stair`, `Door`, `Railing`, `Roof`

## How to answer

1. Search this dataset for the section; quote the controlling language.
2. Cite precisely and name the edition — `2021 IBC §1015.2`, not just `§1015.2`.
   Colorado and GSA are different editions and will diverge.
3. **For an Aspen or Pitkin project, check `aspen-pitkin-code` for a local
   amendment before presenting the text as the governing requirement.** Say
   which layer you are quoting.
4. If the answer depends on a table or figure, flag it — see coverage limits.
5. If the section falls in an uncovered chapter range, say so plainly and point
   to up.codes rather than guessing.

## Refreshing

Regenerate from the upstream pipeline (`upcodes-links.txt` → scrape → LLM
enrich → `download-v2/`) and re-copy the `colorado/`, `gsa/` and `ada/` CSVs.
Editions roll over — Colorado moving off the 2021 IBC, or Aspen adopting a newer
edition, makes this copy stale.
