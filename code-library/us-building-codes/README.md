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
jurisdictions relevant to the office, 163 CSVs / ~14 MB:

| Path | Contents |
| --- | --- |
| `colorado/` | IBC 2021 (ch 1–35), IRC 2021 (ch 1–44), IEBC 2021 (ch 1–16) |
| `gsa/` | IBC 2024 (ch 1–35), IRC 2024 (ch 1–15), IEBC 2024 — unamended baseline |
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

### Colorado IRC 16–44 was fetched from up.codes

Those chapters were never scraped upstream, so no raw JSON existed. They were
fetched directly from up.codes (29 chapters, rate-limited at 3 s) and parsed
with the same script: +2,069 provisions covering mechanical (16–23), fuel gas
(24), plumbing (25–33) and electrical (34–43).

Note up.codes' `robots.txt` disallows general crawlers; this was run once, at
the repo owner's explicit direction, as an UpCodes subscriber, for the office's
own reference. Re-run it the same way — deliberately and rate-limited — rather
than wiring it into anything automated.

**Appendices are not available.** up.codes marks IRC appendices `disabled` for
Colorado (they 404), since the state's adoption does not publish them; only
`AG` came through. Pitkin County separately adopts **AE, AF, AH, AK and AQ** and
amends AQ — for those, use `code-library/pitkin/title-11-building-construction.txt`.

### Metadata on locally-parsed chapters

Locally-parsed chapters never went through upstream's LLM enrichment, which left
their metadata columns empty and made them invisible to metadata filters.
`.claude/skills/us-building-codes/scripts/backfill_metadata.py` fills
`code_category` and `primary_responsibility` per chapter from a static table
(4,238 rows across 59 chapters) — deterministic, idempotent, and calibrated
against upstream's own values for adjacent chapters. It never overwrites a
non-empty value.

`ifc_type`, `occupancy` and `design_phase` are deliberately left empty on these
chapters: they vary section to section and were not guessed. `codesearch.py`
reports how many rows a metadata filter excluded for having an empty field, so
the gap is never silent.

Colorado 2021 matches the IBC edition Aspen has adopted. GSA 2024 is a different
edition — useful for comparison, not as an adopted requirement.

Dropped upstream: the other 19 states, the raw `state-codes/` and `gsa-codes/`
JSON, the intermediate `download/` stage, and the per-run `.log` files recording
LLM calls.

## Authority

This is **model code text only**. City of Aspen and Pitkin County amendments
live in `code-library/aspen/` and `code-library/pitkin/` and override it. Aspen
adopted the 2021 IBC and did not adopt the 2021 IRC.
