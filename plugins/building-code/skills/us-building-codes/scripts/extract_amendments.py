#!/usr/bin/env python3
"""Regenerate references/locally-amended-sections.txt from the local code text.

Reads Aspen Title 8 and Pitkin Title 11, finds each adopted code's amendment
block, and pulls the section numbers those blocks name.

Two things make the output trustworthy rather than a regex guess:

1. Several patterns are unioned. The ordinances write references inconsistently
   -- "Section 1015.2", "[F] 1015.2", a bare "1015.2" at line start, and
   letter-prefixed IRC forms like "P3103.1.3" or "G2420.5.2". Matching only one
   shape silently drops amendments, which is how an earlier hand-built list
   missed Pitkin's prose-style "Section 101.1 Title. Insert:" entries.

2. Block boundaries come from every chapter heading, and a heading must look
   like one (1-2 digits dot exactly 2). Both matter: ending a block at the next
   *mapped* chapter let Pitkin's IFGC run to end of file and report 81
   amendments where it makes 11, and a loose heading pattern let the amendment
   line "409.5.3 Located at manifold is hereby deleted." pass as a heading,
   truncating the block and dropping everything after it.

Candidates are checked against the section ids in the CSVs, but that check is
REPORTING ONLY (--verbose) and does not filter. A reference absent from our text
costs nothing, since no search result can match it, whereas dropping one loses a
real safety flag -- filtering on presence discarded 8 of Pitkin's 11 IFGC
amendments, because Colorado deletes the admin sections they amend.

Validated against hand-read blocks: Pitkin IMC matches 11/11 exactly, IFGC and
IPC match every section their ordinance names.

This list is a FLOOR, in two ways. An ordinance that amends something in prose
without naming a number cannot be caught. And a typo in the ordinance carries
through: Pitkin writes "Section 9043.1 Roof Extension", which is not a real
section -- it means IPC 904.1 -- so 904.1 goes unflagged.

Usage:  extract_amendments.py [-o OUT] [--verbose] [--dry-run]
"""

import argparse
import csv
import glob
import os
import re
import sys

csv.field_size_limit(10_000_000)

HERE = os.path.dirname(os.path.abspath(__file__))
# scripts/ -> us-building-codes/ -> skills/ -> the plugin root, which holds
# code-library/. Resolved from __file__ so this runs from any install path.
PLUGIN = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
DATA = os.path.join(PLUGIN, "code-library", "us-building-codes")
ASPEN = os.path.join(PLUGIN, "code-library", "aspen",
                     "title-8-buildings-and-building-regulations.txt")
PITKIN = os.path.join(PLUGIN, "code-library", "pitkin",
                      "title-11-building-construction.txt")
OUT = os.path.join(HERE, "..", "references", "locally-amended-sections.txt")

# Aspen Title 8: chapter -> code. Ranges run to the next chapter heading.
ASPEN_CH = {"8.20": "ibc", "8.32": "iebc", "8.36": "ipc",
            "8.44": "imc", "8.28": "ifgc"}
# Pitkin Title 11: chapter -> code.
PITKIN_CH = {"11.04": "ibc", "11.08": "imc", "11.16": "ipc",
             "11.20": "irc", "11.24": "iebc", "11.28": "ifgc"}

# union of the reference shapes the two ordinances actually use
PATTERNS = [
    # a leading verb is common: "Add Section 606.7", "Delete Section 305.4"
    r'^\s*(?:\[[A-Z]\]\s*)?(?:\w+\s+)?(?:Section|SECTION)\s+((?:[MPGE])?\d{3,4}(?:\.\d+)*)',
    r'^\s*(?:\[[A-Z]\]\s*)?((?:[MPGE])?\d{3,4}(?:\.\d+)*)\s',
    r'\b((?:[MPG])\d{4}(?:\.\d+)*)\b',
    r'\bAPPENDIX\s+([A-Z]{1,2}\d{3}(?:\.\d+)*)',
    r'^\s*(A[A-Z]\d{3}(?:\.\d+)*)',
]


def known_sections(code):
    """Every section id present in the CSVs for this code, lowercased."""
    ids = set()
    for path in glob.glob(os.path.join(DATA, "*", f"{code}-*", "*.csv")):
        try:
            with open(path, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    sid = (row.get("id") or "").strip()
                    if sid:
                        ids.add(sid.lower())
        except OSError:
            continue
    return ids


def blocks(path, chapters, heading):
    """Yield (code, text) for each adopted code's chapter block."""
    lines = open(path, encoding="utf-8", errors="replace").read().split("\n")
    # Boundaries come from EVERY chapter heading, not just the mapped ones.
    # Ending a block at the next *mapped* chapter lets the final code run to end
    # of file and absorb the energy, wildfire and fire codes that follow, which
    # is how Pitkin's IFGC picked up 81 sections when it amends 11.
    marks = []
    for i, line in enumerate(lines):
        # table-of-contents rows use dot leaders and a trailing page number
        if re.search(r"\.{4,}", line) or re.search(r"\.{2,}\s*\d+\s*$", line):
            continue
        m = re.match(heading, line)
        if m:
            marks.append((i, chapters.get(m.group(1))))
    for n, (start, code) in enumerate(marks):
        if code is None:
            continue
        end = marks[n + 1][0] if n + 1 < len(marks) else len(lines)
        yield code, "\n".join(lines[start:end])


def refs(text):
    out = set()
    for pat in PATTERNS:
        for m in re.finditer(pat, text, re.M):
            r = m.group(1)
            if re.match(r"^0", r):            # leading zero -> page debris
                continue
            out.add(r)
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("-o", "--out", default=OUT)
    p.add_argument("--verbose", action="store_true",
                   help="list candidates rejected as not-a-real-section")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    sources = [
        ("aspen", ASPEN, ASPEN_CH, r"^===== Chapter (\d+\.\d+)\."),
        # Chapter numbers are 1-2 digits dot exactly 2 (11.28.040). Allowing
        # \d+\.\d+ let an amendment line -- "409.5.3 Located at manifold is
        # hereby deleted." -- pass as a chapter heading and truncate the block,
        # silently losing every amendment after it.
        ("pitkin", PITKIN, PITKIN_CH, r"^(\d{1,2}\.\d{2})\.\d+:?\s"),
    ]

    found, dropped = {}, {}
    for juris, path, chapters, heading in sources:
        if not os.path.exists(path):
            sys.exit(f"missing {path}")
        for code, text in blocks(path, chapters, heading):
            valid = known_sections(code)
            if not valid:
                continue                       # code not held locally; skip
            for r in refs(text):
                # Keep every plausible reference. Validation is REPORTING only:
                # a ref absent from the CSVs costs nothing (no result can match
                # it), whereas dropping one loses a real safety flag. Colorado
                # deletes many IFGC/IPC admin sections, so Pitkin amendments to
                # them are legitimately absent from our text -- filtering on
                # presence silently discarded 8 of Pitkin's 11 IFGC amendments.
                found.setdefault((juris, code), set()).add(r)
                if r.lower() not in valid:
                    dropped.setdefault((juris, code), set()).add(r)

    lines = [
        "# Sections of the model code that Aspen or Pitkin County AMEND.",
        "#",
        "# The CSVs in code-library/us-building-codes/ hold UNAMENDED model text.",
        "# For any section listed here that text is SUPERSEDED locally and must not",
        "# be quoted as the requirement. Read the local amendment first:",
        "#   Aspen  -> code-library/aspen/title-8-buildings-and-building-regulations.txt",
        "#   Pitkin -> code-library/pitkin/title-11-building-construction.txt",
        "#",
        "# codesearch.py reads this file and flags matching results automatically.",
        "# Format: <jurisdiction> <code> <section>",
        "#",
        "# GENERATED by scripts/extract_amendments.py -- do not hand-edit; re-run it.",
        "# Every entry is a section number named in an adopting ordinance. Entries are",
        "# NOT filtered on presence in the CSVs: one that is absent is harmless (nothing",
        "# can match it), while dropping one would lose a real flag.",
        "#",
        "# This is a FLOOR, in two ways. An ordinance that amends something in prose",
        "# without naming a section number cannot be detected. And an ordinance typo",
        "# carries through -- Pitkin writes 'Section 9043.1 Roof Extension', which is not",
        "# a real section (it means IPC 904.1), so 904.1 goes unflagged.",
        "#",
        "# Worked example -- IBC 1015.2 Guards:",
        '#   model : "...aisles, stairs, ramps and landings that are located more',
        '#            than 30 inches..."',
        '#   Aspen : "...aisles, stairs, ramps, landings AND ADJACENT TO HOT TUBS,',
        '#            SPAS, AND POOLS that are located more than 30 inches..."',
        "#   Aspen also adds 1015.3 Exception 9: guards next to hot tubs/spas/pools",
        "#   with an open side under 18 in. from the water's edge may be 18 in. high.",
        "",
    ]
    total = 0
    for (juris, code) in sorted(found):
        secs = sorted(found[(juris, code)],
                      key=lambda s: (s[0].isalpha(), len(s), s))
        lines.append(f"# ---- {juris} {code.upper()} ({len(secs)}) ----")
        for s in secs:
            lines.append(f"{juris} {code} {s}")
        lines.append("")
        total += len(secs)
        print(f"  {juris:7} {code.upper():5} {len(secs):3} sections")

    print(f"\n  TOTAL {total}")
    if args.verbose:
        print("\n  rejected (not a real section id in the CSVs):")
        for k in sorted(dropped):
            print(f"    {k[0]} {k[1]}: {' '.join(sorted(dropped[k]))}")

    if not args.dry_run:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines))
        print(f"\n  wrote {os.path.relpath(args.out, REPO)}")


if __name__ == "__main__":
    main()
