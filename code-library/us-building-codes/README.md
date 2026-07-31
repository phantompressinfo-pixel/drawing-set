# US Building Codes Dataset — local subset

Model building code text used by the `us-building-codes` skill
(`.claude/skills/us-building-codes/`). See that SKILL.md for the row schema,
search helper, and coverage limits.

## Provenance

Derived from the `download-v2/` (production) stage of
[thexqin/us-building-codes-dataset](https://github.com/thexqin/us-building-codes-dataset).
Code text was scraped from up.codes; the `ifc_type`, `occupancy`,
`design_phase`, `code_category` and `primary_responsibility` columns are
LLM-inferred metadata, not authored by the code bodies. Upstream `LICENSE` is
kept alongside this file.

## What was kept

The upstream repo ships 22 states (~100 MB). This copy keeps only the three
jurisdictions relevant to the office, 99 CSVs / ~11 MB:

| Path | Contents |
| --- | --- |
| `colorado/` | IBC 2021 (ch 1–18), IRC 2021 (ch 1–15), IEBC 2021 (ch 1–16) |
| `gsa/` | IBC/IRC/IEBC 2024 — unamended ICC baseline |
| `ada/` | 2010 ADA Standards for Accessible Design |

Colorado 2021 matches the IBC edition Aspen has adopted. GSA 2024 is a different
edition — useful for comparison, not as an adopted requirement.

Dropped upstream: the other 19 states, the raw `state-codes/` and `gsa-codes/`
JSON, the intermediate `download/` stage, and the per-run `.log` files recording
LLM calls.

## Authority

This is **model code text only**. City of Aspen and Pitkin County amendments
live in `code-library/aspen/` and `code-library/pitkin/` and override it. Aspen
adopted the 2021 IBC and did not adopt the 2021 IRC.
