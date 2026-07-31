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
jurisdictions relevant to the office, 133 CSVs / ~12 MB:

| Path | Contents |
| --- | --- |
| `colorado/` | IBC 2021 (ch 1–35), IRC 2021 (ch 1–15), IEBC 2021 (ch 1–16) |
| `gsa/` | IBC 2024 (ch 1–35), IRC/IEBC 2024 — unamended ICC baseline |
| `ada/` | 2010 ADA Standards for Accessible Design |

### IBC chapters 19–35 were generated here, not upstream

Upstream's published CSVs stop at IBC ch. 18, but its raw `state-codes-full/`
and `gsa-codes-full/` scrapes contain all 35 chapters — the pipeline simply
never parsed them. Those chapters were parsed locally from that JSON with
`.claude/skills/us-building-codes/scripts/upcodes_to_csv.py`.

The parser was validated against ch. 10, which exists in both forms: it
reproduces all 425 rows with identical ids, and 399 bodies byte-identical. Of
the 26 differences, 25 are whitespace and one is upstream leaving `&gt;`
double-escaped where this parser correctly unescapes to `>`.

These chapters have **empty metadata columns** — they never went through the
upstream LLM enrichment pass. Body text is complete.

### IRC 16–44 is still missing

Not recoverable from the upstream repo: those chapters were never scraped, so
no raw JSON exists for them either. Fetching them from up.codes is blocked by
that site's `robots.txt` (`User-agent: * / Disallow: /`). Relevant to Pitkin
County work, which adopts the IRC; not to Aspen, which does not.

Colorado 2021 matches the IBC edition Aspen has adopted. GSA 2024 is a different
edition — useful for comparison, not as an adopted requirement.

Dropped upstream: the other 19 states, the raw `state-codes/` and `gsa-codes/`
JSON, the intermediate `download/` stage, and the per-run `.log` files recording
LLM calls.

## Authority

This is **model code text only**. City of Aspen and Pitkin County amendments
live in `code-library/aspen/` and `code-library/pitkin/` and override it. Aspen
adopted the 2021 IBC and did not adopt the 2021 IRC.
