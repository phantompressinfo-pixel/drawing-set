#!/usr/bin/env python3
"""Parse an up.codes chapter page into the dataset CSV schema.

Input is the `__NEXT_DATA__` JSON blob up.codes embeds in each chapter page —
either a saved .json (as in the upstream repo's `state-codes-full/`) or a saved
.html page, from which the blob is extracted.

This produced IBC chapters 19-35 in code-library/us-building-codes/, which the
upstream pipeline scraped but never parsed.

Validated against chapter-10-means-of-egress, which exists in both raw and
parsed form upstream: 425/425 rows with identical ids, 399 bodies byte-identical.
The 26 differences are 25 whitespace and one case of upstream leaving `&gt;`
double-escaped where this unescapes correctly.

Usage:
  upcodes_to_csv.py chapter-23-wood.json                 # -> stdout
  upcodes_to_csv.py chapter-23-wood.json -o out/         # -> out/chapter-23-wood.csv
  upcodes_to_csv.py raw-dir/ -o out/                     # whole directory

Metadata columns (ifc_type, occupancy, design_phase, code_category,
primary_responsibility) are emitted empty: they are LLM-inferred upstream and
are not reproduced here. See SKILL.md — they are search filters, not authority.
"""

import argparse
import csv
import glob
import html
import json
import os
import re
import sys

csv.field_size_limit(10_000_000)

COLS = ["id", "section", "title", "ifc_type", "occupancy", "design_phase",
        "code_category", "primary_responsibility", "body"]


def clean(raw):
    """HTML -> the plain-text form used by the rest of the dataset."""
    if not raw:
        return ""
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", raw)
    # upstream stripped every tag with no separator inserted; match that exactly
    # so newly parsed chapters read like the ones already in the dataset
    t = re.sub(r"(?s)<[^>]+>", "", t)
    t = html.unescape(t)
    t = t.replace("\xa0", " ")
    t = re.sub(r"[ \t]*\n[ \t]*", "\n", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    return t.replace("\n", "").strip()


def walk(node, section=""):
    """Flatten the section tree into rows, carrying the parent section heading."""
    out = []
    body = clean(node.get("body"))
    row = {"id": node.get("reference", ""), "section": section,
           "title": node.get("titleText", ""), "body": body}

    if node.get("depth", 0) == 0:                    # chapter overview row
        row["section"] = ""
        out.append(row)
        child_section = ""
    elif node.get("divisionType") == "Section" or not node.get("body"):
        # a heading container: only worth a row if it carries text of its own
        child_section = (node.get("displayTitle") or "").strip() or section
        if body:
            out.append(row)
    else:
        out.append(row)
        child_section = section

    for child in node.get("children", []):
        out += walk(child, child_section)
    return out


def load(path):
    """Return the leanChapterViewerData blob from a .json or .html page."""
    text = open(path, encoding="utf-8", errors="replace").read()
    if path.endswith(".html"):
        m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
                      text, re.S)
        if not m:
            raise RuntimeError(f"no __NEXT_DATA__ blob in {path}")
        text = m.group(1)
    page = json.loads(text)["props"]["pageProps"]
    if page.get("missingRequiredLogin"):
        raise RuntimeError(f"chapter requires a subscription: {path}")
    return page["leanChapterViewerData"]


def parse(path):
    data = load(path)
    rows = []
    for root in data.get("leanCodeSectionsTree", []):
        rows += walk(root)
    return rows


def write(rows, fh):
    w = csv.DictWriter(fh, fieldnames=COLS, extrasaction="ignore")
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in COLS})


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("source", help="a .json/.html chapter page, or a directory of them")
    p.add_argument("-o", "--out-dir", help="write <name>.csv here (default: stdout)")
    p.add_argument("--overwrite", action="store_true",
                   help="replace existing CSVs (default: skip them)")
    args = p.parse_args()

    if os.path.isdir(args.source):
        files = sorted(glob.glob(os.path.join(args.source, "*.json")) +
                       glob.glob(os.path.join(args.source, "*.html")))
    else:
        files = [args.source]
    if not files:
        sys.exit(f"no chapter pages found in {args.source}")
    if len(files) > 1 and not args.out_dir:
        sys.exit("-o/--out-dir is required when parsing a directory")

    for src in files:
        rows = parse(src)
        if not args.out_dir:
            write(rows, sys.stdout)
            continue
        os.makedirs(args.out_dir, exist_ok=True)
        dst = os.path.join(args.out_dir,
                           os.path.splitext(os.path.basename(src))[0] + ".csv")
        if os.path.exists(dst) and not args.overwrite:
            print(f"skip (exists): {dst}", file=sys.stderr)
            continue
        if not any(r["body"] for r in rows):
            print(f"skip (no body text): {src}", file=sys.stderr)
            continue
        with open(dst, "w", newline="", encoding="utf-8") as fh:
            write(rows, fh)
        print(f"{len(rows):5d} rows -> {dst}", file=sys.stderr)


if __name__ == "__main__":
    main()
