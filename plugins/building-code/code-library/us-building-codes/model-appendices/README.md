# ICC model appendices adopted by Aspen and Pitkin County

These are the **ICC model appendix texts that Aspen and Pitkin adopt by
reference** in their adopting ordinances. They are not another state's code.

Colorado's up.codes publication marks appendices `disabled` — the state's
adoption does not print them — so the text had to come from a jurisdiction that
publishes the same unamended ICC appendix. That is why the source column names
other states: they are the *printer*, not the authority.

## Who adopts what

| Appendix | Adopted by | Ordinance |
| --- | --- | --- |
| IBC C, E, P | Aspen | §8.20.010 |
| IBC C, E, I, J | Pitkin County | §11.04.010 |
| IRC AE, AF, AH, AK, AQ | Pitkin County | §11.20.010 |

Pitkin **amends** IRC Appendix AQ (`AQ106.1` air leakage, `AQ106.2` alternative
compliance). Those amendments are in
`code-library/pitkin/title-11-building-construction.txt` and **override** the
AQ file here.

## Provenance and verification

Where two jurisdictions publish the same appendix, both were fetched and the
parsed rows diffed. "VERIFIED identical" means every row id and body matched
across two independent publications — strong evidence the text is unamended ICC
model text.

| Appendix | Rows | Source | Verification |
| --- | --- | --- | --- |
| IBC C — Group U Agricultural Buildings | 7 | Connecticut 2021 IBC portion | **VERIFIED** identical vs Arkansas |
| IBC E — Supplementary Accessibility | 64 | Arkansas Building Code 2021 | **VERIFIED** identical vs Washington (one whitespace diff) |
| IBC I — Patio Covers | 8 | Connecticut 2021 IBC portion | **VERIFIED** identical vs Oregon |
| IBC J — Grading | 29 | North Carolina Building Code 2024 | **UNVERIFIED** — only source; 2024-branded code |
| IBC P — Construction and Demolition Material Management | 7 | Washington State Building Code 2021 | **UNVERIFIED** — only source |
| IRC AE — Manufactured Housing Used as Dwellings | 70 | Connecticut 2021 IRC portion | **UNVERIFIED** — Oregon prints only a fragment |
| IRC AF — Radon Control Methods | 32 | Washington State Residential Code 2021 | **UNVERIFIED** — see warning below |
| IRC AH — Patio Covers | 21 | Connecticut 2021 IRC portion | **VERIFIED** identical vs Texas |
| IRC AK — Sound Transmission | 6 | Connecticut 2021 IRC portion | **VERIFIED** identical vs Texas |
| IRC AQ — Tiny Houses | 27 | Connecticut 2021 IRC portion | **VERIFIED** identical vs Texas |

Six of ten are cross-verified. Treat the other four as a working reference and
confirm against the ICC-published appendix before relying on them for a
submittal.

### Why AF (radon) carries the strongest warning

up.codes' chapter-level `amendType` flag is **not reliable**. Oregon's AF is
flagged `amendType=None` yet is plainly state-amended: its `AF101.1` names Baker,
Clackamas, Hood River, Multnomah, Polk, Washington and Yamhill counties and cites
ORS 455.365, and it adds seven `new_AF103.5.*` sections absent from the model.
Connecticut's AF is flagged `edit`. That leaves Washington as the only candidate
for clean text, with nothing to check it against.

Radon matters in Pitkin County. Verify AF against the ICC book before relying on
it.

## Not a substitute for the local amendments

These files are **model text**. Aspen's Title 8 and Pitkin's Title 11
amendments override them, and
`skills/us-building-codes/references/locally-amended-sections.txt`
lists the sections involved.
