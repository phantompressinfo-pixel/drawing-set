---
name: architectural-details
description: Draw and note construction details the office way - exterior details, interior details, roof details, foundation details, exterior transition details and wall sections. The deliverable is the detail only (no sheet or title block), drawn in the office's Revit style, with a DXF for a Revit drafting view and the notes ready to paste. Every assembly carries its schedule tag, and the notes never repeat what the tag says; they call out only design intent, transitions, sequencing and the dimensions the GC or sub must hold, in the office's own wording. Use when asked to draw, redraw, mark up, note, check or review a detail or wall section, or to write the notes for one.
---

# Architectural details - office method

## The rule this skill exists for

**The tag carries the assembly. The notes carry the intent.**

Every wall, roof, floor, ceiling and foundation cut on a detail gets its tag from
the project assembly schedule. The office tags look like this:
- walls: `3A-X`, `2/3/4/5B-X`, `3C-E`;
- roofs: `R1` to `R8`;
- floors and finishes: `F2`, `A`, `B`, `A/B`;
- ceilings: `C1`, `C2`, `C13`.

A tag may carry `SIM` under it. The tag already tells the builder every layer. A
note that says it again is noise, and it drifts out of step with the schedule.

A note earns its place only if it tells the GC or sub something the assembly
schedule cannot:

1. **What happens where assemblies meet**: laps, turn-ups, terminations, which
   layer goes over which.
2. **Continuity** of water, air, thermal and vapor control (and fire, where rated)
   across the joint.
3. **Items in no assembly**: flashings, pans, membranes, blocking, headers, shims,
   sealant, trim, anchors, screens.
4. **Dimensions and slopes to hold**: `1/2" PER FT SLOPE MIN.`,
   `RETURN UP @ JAMBS 6" MIN`.
5. **Sequence**: what laps over what.
6. **Visible design intent**: `3/16" REVEAL`, `ALIGN ...`, `MITER CORNER AT NOSING`.
7. **Who owns it**:
   - `S.S.D.`, `S.L.D.`, `S.M.D.`;
   - `SEE WATERPROOFING DRAWINGS`;
   - `PER SCHEDULE`;
   - `BY G.C.`;
   - `FRAMING AS REQ.`
8. **Field verify**: `V.I.F.`

Two tests for every note:
- *Would the builder do it differently without it?* If not, cut it.
- *Is it in the assembly schedule?* If yes, cut it and make sure the tag is there.

Full rules: `references/note-rules.md`. Office wording, by condition:
`references/office-note-library.md`. **Use the office's wording before writing
new wording.**

## What the office wants back

**The detail only.** No sheet border, no title block. The detail goes onto the
office's own Revit sheet. For each detail, deliver:

| File | Use |
|---|---|
| `<NN>-<SHEET>-<slug>.png` | To look at and review |
| `<NN>-<SHEET>-<slug>.dxf` | Import into a Revit drafting view (Insert > Import CAD, units inches, 1:1). Layers are named A-DETL-* and A-ANNO-*. |
| `<NN>-<SHEET>-<slug>.notes.txt` | The notes top to bottom, the tags, and the verify list, for typing into or pasting over the Revit text |
| `<NN>-<SHEET>-<slug>.svg` / `.py` / `.json` | Source, to regenerate after comments |

The office uses a cold roof most of the time, but it varies by project. **Ask
which roof** (cold/vented or unvented/hot) before drawing any roof, eave, rake or
ridge.

## What to have before drawing

Ask for whatever is missing. Don't guess.

| Input | Why |
|---|---|
| Detail type and condition, with any sketch, markup or similar office detail | Picks the checklist in `references/detail-types.md` |
| Detail number, sheet and scale | Title, file name, cross-references. Scales are usually 3" = 1'-0", or 1 1/2" = 1'-0" for eaves and rakes. |
| **This project's assembly schedule** | **Wall assemblies are different on every project**, so there is no office-wide set. See "Start of every project" below. |
| Jurisdiction: City of Aspen or Pitkin County | Code basis. The City runs houses under the IBC (the IRC is not adopted); the County adopts the IRC. |
| Roof type (cold or unvented), for roof work | See above |
| Structural, waterproofing-consultant and interiors information | The office points to these; it doesn't size them |

## Start of every project: the assembly schedule

Wall, roof, floor and ceiling assemblies change on every project, so the tags and
build-ups can't be carried over from a previous job.

1. Ask for the project's assembly schedule sheet (A5.02 or equivalent), as a PDF or
   screenshot.
2. Transcribe it into `details/assemblies.yaml` on the project's branch, using the
   format in `templates/assemblies.yaml`. Use the tag exactly as it prints in Revit,
   and the layers exactly as the schedule lists them.
3. Show the transcription to the user and get a yes before drawing. A mistyped
   layer means the checker misses a repeated note.
4. If the schedule isn't drawn yet, list the tags with no layers. The checker will
   still confirm every tag exists, and each detail's verify list gets "__ AGREES
   WITH THE ASSEMBLY SCHEDULE".
5. When the schedule is revised, update the file and re-run every detail script.
   `python3 details/<file>.py` redraws and re-checks each one.

Never reuse another project's `assemblies.yaml`, and never fill in a build-up from
an office habit.

## Workflow

1. **Read the condition.** State in one line what the detail shows and which
   assemblies meet in it. If it's ambiguous (headwall or sidewall, above or below
   grade, cold or unvented roof), ask.
2. **Open the checklist** for the type in `references/detail-types.md`, and the
   matching section of `references/office-note-library.md`.
3. **Draw it** with `scripts/detailkit.py`, one script per detail, saved as
   `details/<NN>-<SHEET>-<slug>.py`. Enter geometry in real inches, with INT. to the
   left and EXT. to the right, as the office does. Graphics and the API are in
   `references/drawing-standards.md`; the worked example is
   `examples/window-sill-wood-siding.py`.
4. **Tag every assembly** that is cut or seen, once per detail. Where the build-up
   changes, use a new tag.
5. **Write the notes** from the office library. Mark items that belong to no
   assembly with `flag=True`; they're listed with `#` in the notes file.
6. **Code.** Cite a code section only where a note depends on a code limit. Get it
   from the code library (phantom-press-hq/code-library), never from memory. Never
   cite the IRC on a City of Aspen detail.
7. **Save and check.**
   `d.save("details", assemblies="details/assemblies.yaml")` runs
   `scripts/check_notes.py`. Pass the code library with
   `CODE_LIBRARY=/path/to/code-library` so section numbers are checked against the
   2021 dataset. Fix every ERROR and read every WARN.
8. **Look at the PNG.** Fix overlaps, crossed leaders, and text over linework.
   Re-save.
9. **Report**:
   - what was drawn;
   - the tags;
   - the notes;
   - anything assumed (it goes in the verify list);
   - the files.

Checking an existing detail follows the same rules. List:
- notes that repeat an assembly;
- missing tags;
- missing continuity;
- missing flashings or other items;
- anything the checker flags.

## Files

| Path | What |
|---|---|
| `references/note-rules.md` | The tag-vs-note rule in full, the office voice, before/after examples |
| `references/office-note-library.md` | The office's own note wording, by condition, from the 22 sample sheets |
| `references/detail-types.md` | Checklists for the six detail types |
| `references/drawing-standards.md` | Office graphics (Revit look), symbols, scales, detailkit API, DXF |
| `scripts/detailkit.py` | Drawing library: SVG + PNG + DXF + notes + manifest |
| `scripts/check_notes.py` | Enforces the rules; `save()` runs it automatically |
| `templates/assemblies.yaml` | Project assembly schedule format |
| `templates/standard-general-notes.txt` | The DETAILING / WATERPROOFING GEN NOTES block, corrected |
| `examples/window-sill-wood-siding.py` | Worked example, based on 1/A6.16 |
