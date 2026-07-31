#!/usr/bin/env python3
"""Search the US building codes dataset in code-library/us-building-codes/.

Bodies are long single-line CSV fields, so plain Grep dumps unreadable walls of
text. This prints a citation header per hit plus a trimmed body.

Examples:
  codesearch.py "guard" --code ibc --chapter 10
  codesearch.py "chimney" --jurisdiction colorado --full
  codesearch.py --section 1015.2
  codesearch.py "landing" --category means_of_egress --responsibility architect
  codesearch.py "grab bar" --jurisdiction ada
"""

import argparse
import csv
import os
import re
import sys

csv.field_size_limit(10_000_000)

ROOT = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..",
                 "code-library", "us-building-codes")
)

AMENDED_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "references", "locally-amended-sections.txt")


def load_amended():
    """{(code, section): [jurisdictions]} that Aspen/Pitkin amend locally."""
    out = {}
    try:
        with open(AMENDED_FILE, encoding="utf-8") as fh:
            for line in fh:
                line = line.split("#", 1)[0].strip()
                if not line:
                    continue
                parts = line.split()
                if len(parts) != 3:
                    continue
                juris, code, section = parts
                out.setdefault((code.lower(), section.lower()), []).append(juris)
    except OSError:
        pass
    return out


def corpus(jurisdiction=None, code=None, chapter=None):
    """Yield (path, jurisdiction, code_edition) for CSVs matching the filters."""
    if not os.path.isdir(ROOT):
        sys.exit(f"dataset not found at {ROOT}")
    for juris in sorted(os.listdir(ROOT)):
        jdir = os.path.join(ROOT, juris)
        if not os.path.isdir(jdir):
            continue
        if jurisdiction and juris != jurisdiction:
            continue
        # ada/ is flat; colorado/ and gsa/ nest one level by code edition
        subdirs = [d for d in sorted(os.listdir(jdir))
                   if os.path.isdir(os.path.join(jdir, d))]
        for group in subdirs or [""]:
            if code and not group.startswith(code.lower()):
                continue
            gdir = os.path.join(jdir, group)
            for name in sorted(os.listdir(gdir)):
                if not name.endswith(".csv"):
                    continue
                if chapter is not None:
                    m = re.match(r"chapter-(\d+)-", name)
                    if not m or int(m.group(1)) != chapter:
                        continue
                yield os.path.join(gdir, name), juris, group or juris


def matches(row, args, pattern, blind):
    """True if the row matches. `blind` counts rows dropped only because a
    metadata field is empty — those chapters were never enriched, so a metadata
    filter silently excludes them. Reported so the miss is never invisible."""
    if pattern:
        hay = " ".join(filter(None, (row.get("title"), row.get("body"), row.get("id"))))
        if not pattern.search(hay):
            return False
    if args.section and (row.get("id") or "").strip() != args.section:
        return False
    # metadata values are pipe-delimited and inconsistently cased -> substring match
    dropped_on_blank = False
    for field, want in (("code_category", args.category),
                        ("primary_responsibility", args.responsibility),
                        ("occupancy", args.occupancy),
                        ("ifc_type", args.ifc_type),
                        ("design_phase", args.phase)):
        if not want:
            continue
        have = (row.get(field) or "").strip()
        if not have:
            dropped_on_blank = True
            continue
        if want.lower() not in have.lower():
            return False
    if dropped_on_blank:
        blind[0] += 1
        return False
    return True


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("query", nargs="?", help="regex searched over id, title and body")
    p.add_argument("--jurisdiction", "-j", help="colorado | gsa | ada")
    p.add_argument("--code", "-c", help="ibc | irc | iebc")
    p.add_argument("--chapter", "-n", type=int, help="chapter number")
    p.add_argument("--section", "-s", help="exact section id, e.g. 1015.2")
    p.add_argument("--category", help="code_category, e.g. means_of_egress")
    p.add_argument("--responsibility", help="e.g. architect, structural_engineer")
    p.add_argument("--occupancy", help="e.g. 'Residential (R)' or just R")
    p.add_argument("--ifc-type", dest="ifc_type", help="e.g. Stair, Guard, Wall")
    p.add_argument("--phase", help="concept | sd | dd | cd | ca")
    p.add_argument("--full", action="store_true", help="print untruncated bodies")
    p.add_argument("--limit", type=int, default=25, help="max hits (default 25)")
    p.add_argument("--count", action="store_true", help="print only the hit count")
    args = p.parse_args()

    if not any([args.query, args.section, args.category, args.responsibility,
                args.occupancy, args.ifc_type, args.phase]):
        p.error("give a query or at least one filter")

    pattern = re.compile(args.query, re.IGNORECASE) if args.query else None
    hits = shown = 0
    blind = [0]
    amended = load_amended()
    flagged = []

    for path, juris, edition in corpus(args.jurisdiction, args.code, args.chapter):
        chapter = os.path.basename(path)[:-4]
        with open(path, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if not matches(row, args, pattern, blind):
                    continue
                hits += 1
                if args.count or shown >= args.limit:
                    continue
                shown += 1
                body = (row.get("body") or "").strip()
                if not args.full and len(body) > 900:
                    body = body[:900] + " […]"
                sec_id = (row.get("id") or "").strip()
                who = amended.get((edition.split("-")[0].lower(), sec_id.lower()))
                print(f"\n=== {juris}/{edition} §{sec_id or '?'} — "
                      f"{row.get('title','')} ===")
                if who:
                    label = " and ".join(w.capitalize() for w in who)
                    print(f"    *** AMENDED LOCALLY by {label} — the text below is "
                          f"SUPERSEDED. ***\n"
                          f"    *** Read the amendment before quoting this section. ***")
                    flagged.append(f"{edition} §{sec_id} ({label})")
                print(f"    {chapter} | {row.get('section','')}")
                meta = " | ".join(f"{k}={row[k]}" for k in
                                  ("code_category", "primary_responsibility",
                                   "occupancy", "ifc_type", "design_phase")
                                  if row.get(k))
                if meta:
                    print(f"    {meta}")
                print(f"\n{body}")

    print(f"\n--- {hits} hit(s){'' if args.count else f', {shown} shown'} ---")
    if hits > shown and not args.count:
        print("    narrow with --code/--chapter/--section or raise --limit")
    if blind[0]:
        print(f"    NOTE: {blind[0]} row(s) otherwise matched but have no metadata "
              f"on the filtered field, so they were excluded.\n"
              f"    Re-run without the metadata filter to see them.")
    if flagged:
        print(f"\n    !! {len(flagged)} result(s) are AMENDED locally and the text "
              f"shown is superseded:")
        for f in flagged:
            print(f"       - {f}")
        print("    Check code-library/aspen/title-8-buildings-and-building-regulations.txt"
              "\n    or code-library/pitkin/title-11-building-construction.txt "
              "before citing.")


if __name__ == "__main__":
    main()
