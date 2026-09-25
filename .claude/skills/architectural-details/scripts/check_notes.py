# -*- coding: utf-8 -*-
"""check_notes.py - hold a detail's notes to the office rules before it is issued.

    python3 check_notes.py <detail>.json [--assemblies assemblies.yaml]

<detail>.json is the manifest detailkit writes next to the SVG.  Exit code 1 when
there is an ERROR (the detail must not go out); WARN lines are for review.

ERRORS
  - an assembly tag on the detail that is not in the project assembly schedule
  - a note that names a tag (W3, R2 ...) which is not tagged on the detail
  - a note that repeats an assembly's build-up: it names a layer's material AND
    that layer's spec (thickness, R-value, gauge, spacing, type) - the tag already
    says it
  - vague words the office does not issue: AS REQUIRED, ETC., OR EQUAL ...
  - an IRC section cited on a City of Aspen detail (Aspen did not adopt the IRC,
    M.C. 8.16.010 - residential work runs under the IBC)
  - the same note twice
WARN
  - no assembly schedule given, so tags and repeats were not checked
  - no assembly tag on the detail at all
  - blanks left to fill (__)
  - leader notes over 35 words (move the extra to the general notes)
  - "SEE DETAIL" / "SEE SPEC" without a number
  - code section numbers - verify each against the code-library before issue

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

VAGUE = [
    r"\bAS REQUIRED\b", r"\bAS REQ'?D\b", r"\bAS NECESSARY\b", r"\bAS NEEDED\b",
    r"\bETC\b\.?", r"\bOR EQUAL\b", r"\bOR APPROVED EQUAL\b", r"\bWHERE APPLICABLE\b",
    r"\bIF APPLICABLE\b", r"\bBY OTHERS\b", r"\bPER CODE\b", r"\bAS APPROPRIATE\b",
    r"\bSUITABLE\b", r"\bADEQUATE(LY)?\b", r"\bPROPER(LY)?\b",
]
TAG_RE = re.compile(r"\b([A-Z]{1,3}-?\d{1,3}[A-Z]?)\b")
# words that look like tags but are not (sizes, lumber, standards, code editions)
NOT_TAGS = re.compile(r"^(R-\d+|U-\d+|[0-9]+|ASTM|UL\d*|E\d+|C\d{3,}|D\d{3,}|PVC|CPVC|IBC|IRC|IECC|IFC|NFPA\d*|TYPE|GA\d*)$")
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


def load_assemblies(path):
    if yaml is None:
        sys.exit("check_notes: PyYAML is needed to read the assembly schedule (pip install pyyaml)")
    with open(path) as f:
        data = yaml.safe_load(f) or {}
    asm = data.get("assemblies") or {}
    return {str(k).upper(): v or {} for k, v in asm.items()}, data


def check(manifest, assemblies=None, schedule_meta=None):
    errors, warns = [], []
    tags = set(manifest.get("tags", []))
    juris = (manifest.get("jurisdiction") or (schedule_meta or {}).get("jurisdiction") or "").lower()
    texts = ([("NOTE", t) for t in manifest.get("notes", [])]
             + [(f"KEYNOTE {k}", t) for k, t in manifest.get("keynotes", {}).items()]
             + [(f"GENERAL {i}", t) for i, t in enumerate(manifest.get("general", []), 1)])

    if assemblies is None:
        warns.append("no assembly schedule given - tags and repeated build-ups were NOT checked "
                     "(pass --assemblies <project>/assemblies.yaml)")
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

        for m in TAG_RE.finditer(t):
            tok = m.group(1)
            if NOT_TAGS.match(tok) or tok in tags:
                continue
            if assemblies is not None and tok.upper() in assemblies:
                errors.append(f"{where} names {tok}, which is not tagged on the detail - tag it on the drawing")

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
        if re.search(r"\bSEE (DETAIL|DETAILS|SPEC|SPECS|DRAWINGS)\b(?!\s+\d)", t) and not re.search(r"\d+/[A-Z]+\d", t):
            warns.append(f"{where}: reference without a number - give n/SHEET or the spec section: {t[:80]}")
        if re.search(r"\b\d{3,4}\.\d+(\.\d+)*\b|\bSECTION\s\d", t):
            warns.append(f"{where}: code section cited - verify it in the code-library for "
                         f"{juris or 'the jurisdiction'} before issue: {t[:70]}")
    return errors, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--assemblies")
    a = ap.parse_args()
    with open(a.manifest) as f:
        manifest = json.load(f)
    asm, meta = (load_assemblies(a.assemblies) if a.assemblies else (None, None))
    errors, warns = check(manifest, asm, meta)
    name = f"{manifest.get('number')}/{manifest.get('sheet')} {manifest.get('title')}"
    for e in errors:
        print("ERROR", e)
    for w in warns:
        print("WARN ", w)
    print(f"check_notes: {name}: {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
