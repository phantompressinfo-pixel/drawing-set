#!/usr/bin/env python3
"""Backfill code_category / primary_responsibility on locally-parsed chapters.

Chapters parsed locally (IBC 19-35, IRC 16-44 + appendices) never went through
the upstream LLM enrichment pass, so their metadata columns are empty. That made
them invisible to `codesearch.py --category` / `--responsibility` filters.

This assigns those two fields at CHAPTER level from the static table below —
a chapter's subject determines them reliably (ch. 23 is Wood; every section in
it is structural). It is deterministic and auditable, not inferred per section.

Deliberately NOT filled: ifc_type, occupancy and design_phase. Those genuinely
vary section to section and guessing them at chapter level would be wrong.

Never overwrites a non-empty value, so upstream's LLM metadata is left intact.
Idempotent — safe to re-run.

The mapping is calibrated against upstream's own dominant values for adjacent
chapters, so filters behave consistently across the whole dataset: upstream put
IBC 16-18 under structural_design/structural_engineer and IRC 12-15 under
mechanical_systems/mechanical_engineer; the entries here follow that.

Usage:  backfill_metadata.py [--dry-run] [path-to-dataset]
"""

import argparse
import csv
import glob
import os
import re
import sys

csv.field_size_limit(10_000_000)

COLS = ["id", "section", "title", "ifc_type", "occupancy", "design_phase",
        "code_category", "primary_responsibility", "body"]

STRUCT = ("structural_design", "structural_engineer")
MECH = ("mechanical_systems", "mechanical_engineer")
PLUMB = ("plumbing_systems", "mechanical_engineer")
ELEC = ("electrical_systems", "electrical_engineer")
ARCH_ENV = ("assemblies_envelope", "architect")
ARCH_FIN = ("finishes_materials", "architect")
ARCH_SPEC = ("special_construction", "architect")
ARCH_OCC = ("occupancy_classification", "architect")
ARCH_INT = ("interior_environment", "architect")

# IBC chapters 19-35 (same numbering in the 2021 and 2024 editions here)
IBC = {
    19: STRUCT,                                    # concrete
    20: STRUCT,                                    # aluminum
    21: STRUCT,                                    # masonry
    22: STRUCT,                                    # steel
    23: STRUCT,                                    # wood
    24: ARCH_ENV,                                  # glass and glazing
    25: ARCH_FIN,                                  # gypsum board and plaster
    26: ARCH_FIN,                                  # plastic
    27: ELEC,                                      # electrical
    28: MECH,                                      # mechanical systems
    29: PLUMB,                                     # plumbing systems
    30: ("elevators_conveying_systems", "elevator_consultant"),
    31: ARCH_SPEC,                                 # special construction
    32: ("site_planning", "architect"),            # encroachments into ROW
    33: ("special_construction", "owner"),         # safeguards during construction
    # 34 reserved and 35 referenced standards carry no design requirements
}

# IRC chapters 16-44
IRC = {}
IRC.update({n: MECH for n in range(16, 25)})       # 16-23 mechanical, 24 fuel gas
IRC.update({n: PLUMB for n in range(25, 33)})      # 25-32 plumbing
IRC[33] = ("plumbing_systems", "civil_engineer")   # storm drainage
IRC.update({n: ELEC for n in range(34, 44)})       # 34-43 electrical
# 44 referenced standards: no design requirements

# IRC appendices, keyed by the letter code in the filename
IRC_APPENDIX = {
    "AA": MECH, "AB": MECH, "AD": MECH, "AN": MECH,
    "AG": PLUMB, "AP": PLUMB,
    "AI": ("plumbing_systems", "civil_engineer"),   # private sewage disposal
    "AE": ARCH_OCC, "AJ": ARCH_OCC, "AM": ARCH_OCC, "AQ": ARCH_OCC,
    "AF": ARCH_INT,                                  # radon control
    "AK": ARCH_INT,                                  # sound transmission
    "AH": ARCH_SPEC, "AO": ARCH_SPEC,
    "AR": STRUCT, "AS": STRUCT, "AU": STRUCT, "AW": STRUCT,
    "AT": ARCH_ENV, "AX": ARCH_ENV,
    "AL": ("site_planning", "owner"), "AV": ("site_planning", "owner"),
    # AC is reserved
}

DEFAULT_ROOT = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..",
    "code-library", "us-building-codes"))


def lookup(path):
    """Return (category, responsibility) for a chapter CSV, or None."""
    name = os.path.basename(path)
    edition = os.path.basename(os.path.dirname(path))
    m = re.match(r"chapter-([0-9]+|A[A-Z])-", name)
    if not m:
        return None
    ref = m.group(1)
    if edition.startswith("ibc"):
        return IBC.get(int(ref)) if ref.isdigit() else None
    if edition.startswith("irc"):
        return IRC.get(int(ref)) if ref.isdigit() else IRC_APPENDIX.get(ref)
    return None


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("root", nargs="?", default=DEFAULT_ROOT)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    touched = filled = 0
    for path in sorted(glob.glob(os.path.join(args.root, "*", "*", "*.csv"))):
        pair = lookup(path)
        if not pair:
            continue
        cat, resp = pair
        rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
        n = 0
        for r in rows:
            # only ever fill blanks; upstream LLM values win
            if not (r.get("code_category") or "").strip():
                r["code_category"] = cat
                n += 1
            if not (r.get("primary_responsibility") or "").strip():
                r["primary_responsibility"] = resp
        if not n:
            continue
        touched += 1
        filled += n
        print(f"  {n:5d} rows  {cat:32} {resp:20} "
              f"{os.path.relpath(path, args.root)}")
        if args.dry_run:
            continue
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
            w.writeheader()
            for r in rows:
                w.writerow({c: r.get(c, "") for c in COLS})

    verb = "would fill" if args.dry_run else "filled"
    print(f"\n{verb} {filled} rows across {touched} chapters")


if __name__ == "__main__":
    main()
