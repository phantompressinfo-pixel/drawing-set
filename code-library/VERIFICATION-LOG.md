# Verification log

Dated spot-checks of `code-library/` against live/official sources. This is
not (and can't be) proof the whole library is error-free — see the
"100% accurate" discussion each entry links back to. It's a record of what
was actually checked, when, and what was found, so re-verification has a
starting point instead of starting cold.

## 2026-08-28

Checked against live/official sources (Pitkin County's own code page, an
official City of Aspen zoning checklist PDF, City of Aspen web search
results, and the stored `code-library/aspen/title-26-land-use-regulations.txt`
text itself):

**Confirmed matches:**
- Pitkin LUC currency: repo claims "current through Ord. No. 019-2026" —
  matches pitkincounty.com's own page exactly (adopted 2026-03-25).
- Aspen §26.575.020(f) = "Measuring Building Height", §26.575.020(d) =
  "Measuring Floor Area" — both confirmed against an official City of Aspen
  zoning checklist.
- The height-measurement basics (measured from the lower of natural/finished
  grade) match between the repo and that checklist.
- The single highest-stakes claim in `aspen-pitkin-code/SKILL.md` — Aspen did
  not adopt the 2021 IRC, residential runs under the 2021 IBC — confirmed
  against an official Aspen document titled "Aspen 2021 I-Code Adoption:
  Major Changes — IBC replaces IRC."
- Code edition currency: Aspen's currently adopted codes are still the 2021
  editions (effective for permits after 2023-03-31), no 2024-edition adoption
  found. Matches `code-library/us-building-codes/colorado/`.

**Investigated and resolved — demolition section citation:**
`aspen-pitkin-code/SKILL.md`'s fast facts cite "Demolition §26.580.040: 40%
threshold." An official City of Aspen zoning checklist PDF instead cited
"§26.575.020.H" for the same concept, which read as a conflict.

Resolution: the stored `title-26-land-use-regulations.txt` text's own
definitions section explicitly defines "Demolition" as a 40% threshold and
cross-references "Section 26.580.040, Measurement of demolition" directly —
internally consistent with the SKILL.md fast fact. The checklist PDF that
cited §26.575.020.H is dated 2019-07-05, several years before an August 2022
ordinance that introduced Aspen's demolition-allotment system (see below);
the section-number conflict is best explained by a Land Use Code
reorganization sometime after 2019 that moved the demolition-measurement
provision into its own Chapter 26.580, and the 2019 PDF simply never got
updated. **§26.580.040 is confirmed current; §26.575.020(h) is stale for
this purpose.** `aspen-pitkin-code/SKILL.md` now notes this so the same
question doesn't get re-litigated from scratch.

**New gap found (not an error, a coverage gap):** Aspen limits demolitions to
six (6) per calendar year, first-come-first-served, in effect since an
ordinance effective 2022-08-08 — a hard annual cap independent of the 40%
threshold. This exists in the stored text (searchable via "allotment" in
`code-library/aspen/title-26-land-use-regulations.txt`) but was missing from
`aspen-pitkin-code/SKILL.md`'s fast facts entirely. Added.

**Not independently re-verified this pass:** the model-code CSVs
(`code-library/us-building-codes/`) beyond the currency check above, the
Colorado DPO-amendment list, and the wildfire-code edition-year question
(repo says "2025 Edition," a web summary said "2024" — likely a
development-year-vs-edition-year naming difference, not chased down further).
