# -*- coding: utf-8 -*-
"""check_notes.py - hold a detail's notes to the office rules before it is issued.

    python3 check_notes.py <detail>.json [--assemblies assemblies.yaml]

<detail>.json is the manifest detailkit writes next to the SVG.  Exit code 1 when
there is an ERROR (the detail must not go out); WARN lines are for review.

ERRORS
  - an assembly tag on the detail that is not in the project assembly schedule
  - a note that names a scheduled tag which is not tagged on the detail
  - a note that repeats an assembly's build-up: it names a layer's material AND
    that layer's spec (thickness, R-value, gauge, spacing, type) - the tag already
    says it
  - vague words: ETC., AS NECESSARY, WHERE APPLICABLE, PER CODE, ADEQUATE ...
  - a blank reference ("REFER TO DETAIL  FOR ...")
  - an I-code edition other than 2021 on an Aspen or Pitkin County detail
  - a code section that does not exist in the 2021 IBC/IRC (when the code library
    is available: --code-library or CODE_LIBRARY)
  - an IRC section cited on a City of Aspen detail (M.C. 8.16.010)
  - the same note twice
WARN
  - no assembly schedule given, or no tag on the detail
  - OR EQUAL / BY OTHERS; "AS REQ." on anything but framing, blocking, shims ...
  - blanks left to fill (__); leader notes over 35 words
  - code sections, when the code library is not available to check them

Write R-values with a hyphen (R-21).  R2 without one is read as roof tag R2.
"""
import argparse
import json
import re
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

VAGUE = [   # errors - nothing a builder can act on
    r"\bETC\b\.?", r"\bAS NECESSARY\b", r"\bAS NEEDED\b", r"\bWHERE APPLICABLE\b",
    r"\bIF APPLICABLE\b", r"\bPER CODE\b", r"\bAS APPROPRIATE\b",
    r"\bSUITABLE\b", r"\bADEQUATE(LY)?\b", r"\bPROPER(LY)?\b",
]
SOFT = [    # warnings - the office uses these on purpose in some places
    r"\bOR EQUAL\b", r"\bOR APPROVED EQUAL\b", r"\bBY OTHERS\b",
]
# "FRAMING AS REQ." hands framing to the GC and is office practice; anywhere else it
# needs a reason.
AS_REQ = re.compile(r"\bAS REQ(UIRED|'D|\.|D)?(?=\W|$)")
AS_REQ_OK = re.compile(r"\b(FRAMING|BLOCKING|BLOCK|SHIMS?|PACK ?OUT|FURRING|NAILERS?|PLY|SPACER|SLEEPERS?|"
                       r"LEDGER|STRAPPING|CANT|CARRIAGE|HEADER|STUDS?)\b")
EDITION = re.compile(r"\b(20\d\d)\s+(IECC|IBC|IRC|IFC|IEBC|IMC|IPC|IFGC)\b")
CODE_SEC = re.compile(r"\b(R\d{3}(?:\.\d+)+|N\d{4}(?:\.\d+)+|R\d{3}\.\d+|\b1\d{3}\.\d+(?:\.\d+)*)\b")
SPEC_RE = re.compile(
    r"(\d+\s\d+/\d+\"|\d+/\d+\"|\d+(?:\.\d+)?\"|\d+'-\d+(?:\s\d+/\d+)?\"|"   # 1 1/2"  5/8"  2"  1'-6"
    r"\bR-\d+(?:\.\d+)?\b|\b\d+\s?GA\.?\b|\b\d+\s?MIL\b|\bTYPE\s[A-Z0-9]+\b|"  # R-21  24 GA  40 MIL  TYPE X
    r"@\s?\d+\"\s?O\.?C\.?|\b\d+X\d+\b|\b\d+x\d+\b)")                           # @ 16" O.C.  2X6
STOP = set("""A AN AND OR THE OF TO AT ON IN WITH W/ FOR BY PER OVER UNDER INTO FROM AS
MIN MAX MIN. MAX. O.C. OC CONT CONT. CONTINUOUS TYP TYP. EACH ALL SEE @ - — =""".split())


def words(s):
    return [w.strip(".,;:()") for w in s.upper().replace("/", " / ").split()]


def material_words(layer):
    """The nouns that name a layer's material, without its spec tokens."""
    bare = SPEC_RE.sub(" ", layer.upper())
    return {w for w in words(bare) if len(w) > 2 and w not in STOP and not re.search(r"\d", w)}


def load_code_index(path):
    """Section ids from the code library's 2021 datasets (phantom-press-hq/code-library,
    code-library/us-building-codes).  Returns {'IRC': set, 'IBC': set} or None."""
    import csv
    import glob
    import os
    cands = [path, os.environ.get("CODE_LIBRARY"),
             os.path.join(os.path.dirname(__file__), "../../../../../code-library"),
             os.path.expanduser("~/code-library"), "/home/user/code-library"]
    for c in cands:
        if not c:
            continue
        root = os.path.join(c, "code-library", "us-building-codes") if os.path.isdir(
            os.path.join(c, "code-library", "us-building-codes")) else os.path.join(c, "us-building-codes")
        if not os.path.isdir(root):
            continue
        idx = {"IRC": set(), "IBC": set()}
        csv.field_size_limit(10 ** 8)
        for code in idx:
            for f in glob.glob(os.path.join(root, "**", f"{code.lower()}-2021", "*.csv"), recursive=True):
                with open(f, newline="") as fh:
                    for row in csv.DictReader(fh):
                        if row.get("id"):
                            idx[code].add(row["id"].strip().upper())
        if idx["IRC"] or idx["IBC"]:
            return idx
    return None


def load_assemblies(path):
    if yaml is None:
        sys.exit("check_notes: PyYAML is needed to read the assembly schedule (pip install pyyaml)")
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    asm = data.get("assemblies") or {}
    return {str(k).upper(): v or {} for k, v in asm.items()}, data


def check(manifest, assemblies=None, schedule_meta=None, code_index=None):
    errors, warns = [], []
    tags = set(manifest.get("tags", []))
    juris = (manifest.get("jurisdiction") or (schedule_meta or {}).get("jurisdiction") or "").lower()
    texts = ([("NOTE", t) for t in manifest.get("notes", [])]
             + [(f"KEYNOTE {k}", t) for k, t in manifest.get("keynotes", {}).items()]
             + [(f"GENERAL {i}", t) for i, t in enumerate(manifest.get("general", []), 1)])

    if assemblies is None:
        warns.append("no assembly schedule given - tags and repeated build-ups were NOT checked "
                     "(pass --assemblies details/assemblies.yaml - built from this project's schedule)")
    else:
        for t in sorted(tags - set(assemblies)):
            errors.append(f"tag {t} is on the detail but not in the assembly schedule")
    if not tags:
        warns.append("no assembly tag on this detail - every wall, roof, floor, ceiling and "
                     "foundation cut here should carry its schedule tag")

    seen = {}
    for where, t in texts:
        key = re.sub(r"\s+", " ", t.strip())
        if key in seen:
            errors.append(f"{where} repeats {seen[key]}: {t[:70]}")
        seen.setdefault(key, where)

        for pat in VAGUE:
            m = re.search(pat, t)
            if m:
                errors.append(f"{where}: vague '{m.group(0).strip()}' - say exactly what, where and how much: {t[:80]}")
        for pat in SOFT:
            m = re.search(pat, t)
            if m:
                warns.append(f"{where}: '{m.group(0).strip()}' - confirm this is intended: {t[:80]}")
        if AS_REQ.search(t) and not AS_REQ_OK.search(t):
            warns.append(f"{where}: 'AS REQ.' on something other than framing/blocking - say what is "
                         f"required: {t[:80]}")

        # a scheduled tag named in a note must be tagged on the drawing
        if assemblies is not None:
            for key in assemblies:
                if len(key) < 2 or key in tags:
                    continue
                if re.search(rf"(?<![\w/]){re.escape(key)}(?![\w])", t):
                    errors.append(f"{where} names {key}, which is not tagged on the detail - tag it on the drawing")

        # blank references: "REFER TO DETAIL  FOR ..." / "SEE DETAIL FOR"
        if re.search(r"\b(DETAIL|DETAILS|SHEET)\s+(FOR|AT|TO|ON)\b", t) or re.search(r"\b(SEE|REFER TO)\s*$", t):
            errors.append(f"{where}: reference is blank - fill the detail number/sheet: {t[:80]}")

        # code editions: Aspen and Pitkin both adopted the 2021 I-codes (code library:
        # Aspen M.C. 8.20 / 8.46, Pitkin Title 11)
        for m in EDITION.finditer(t):
            if m.group(1) != "2021" and juris.startswith(("aspen", "pitkin")):
                errors.append(f"{where}: cites the {m.group(1)} {m.group(2)} - {juris.title()} has adopted the "
                              f"2021 edition; update the edition and re-check the section: {t[:80]}")
            elif m.group(1) != "2021":
                warns.append(f"{where}: cites the {m.group(1)} {m.group(2)} - confirm the adopted edition: {t[:70]}")

        # code sections: must exist in the 2021 dataset when the code library is available
        if code_index:
            for m in CODE_SEC.finditer(t):
                sec = m.group(1).upper()
                book = "IRC" if sec.startswith(("R", "N")) else "IBC"
                if sec.startswith("N") or (re.match(r"R4\d\d", sec) and "IECC" in t):
                    continue          # IECC sections - the IECC is not in the dataset
                if sec not in code_index[book]:
                    errors.append(f"{where}: {book} {sec} does not exist in the 2021 {book} - wrong or "
                                  f"out-of-date section number: {t[:80]}")

        if assemblies is not None:
            for tag in sorted(tags & set(assemblies)):
                for layer in assemblies[tag].get("layers", []) or []:
                    specs = {s.strip() for s in SPEC_RE.findall(layer.upper())}
                    specs = {s for s in specs if s}
                    mats = material_words(layer)
                    note_specs = {s.strip() for s in SPEC_RE.findall(t)}
                    hit_spec = specs & note_specs
                    hit_mat = mats & set(words(t))
                    if hit_spec and hit_mat:
                        errors.append(
                            f"{where} repeats {tag} layer \"{layer}\" "
                            f"({', '.join(sorted(hit_spec))} {'/'.join(sorted(hit_mat))}) - the tag already "
                            f"carries it; note only what happens at this condition: {t[:80]}")

        if juris.startswith("aspen") and re.search(r"\bR\d{3}(\.\d+)*\b|\bIRC\b", t):
            errors.append(f"{where}: IRC cited on a City of Aspen detail - Aspen did not adopt the IRC "
                          f"(M.C. 8.16.010); cite the IBC as amended by M.C. 8.20: {t[:80]}")
        if "__" in t:
            warns.append(f"{where}: blank to fill before issue: {t[:80]}")
        if where == "NOTE" and len(t.split()) > 35:
            warns.append(f"{where}: {len(t.split())} words on a leader - keep leaders short, move the rest "
                         f"to the general notes: {t[:60]}")
        if CODE_SEC.search(t) and not code_index:
            warns.append(f"{where}: code section cited - verify it in the code-library for "
                         f"{juris or 'the jurisdiction'} before issue (pass --code-library to check "
                         f"automatically): {t[:70]}")
    return errors, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--assemblies")
    ap.add_argument("--code-library", help="clone of phantom-press-hq/code-library (or set CODE_LIBRARY)")
    a = ap.parse_args()
    with open(a.manifest) as f:
        manifest = json.load(f)
    asm, meta = (load_assemblies(a.assemblies) if a.assemblies else (None, None))
    errors, warns = check(manifest, asm, meta, load_code_index(a.code_library))
    name = f"{manifest.get('number')}/{manifest.get('sheet')} {manifest.get('title')}"
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"check_notes: {name}: {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
