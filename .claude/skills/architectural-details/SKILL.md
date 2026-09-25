---
name: architectural-details
description: Draw and note construction details the office way - exterior details, interior details, roof details, foundation details, exterior transition details and wall sections - as SVG/PNG sheets with leader notes, keynotes, general notes and a verify list. Every assembly on a detail carries its assembly-schedule tag, and the notes never repeat what the tag already says; they call out only the design intent, transitions, sequencing and dimensions the GC or sub must hold. Use when asked to draw, redraw, mark up, note, check or review a detail or wall section, or to write the notes for one.
---

# Architectural details - office method

## The rule this skill exists for

**The tag carries the assembly. The notes carry the intent.**

Every wall, roof, floor, ceiling and foundation cut on a detail gets its tag from
the project assembly schedule (W1, R2, F1 ...). The tag already tells the builder
every layer, thickness, R-value, gauge and spacing. A note that says it again is
noise at best; at worst it drifts from the schedule and the sheet contradicts
itself.

A note earns its place only if it tells the GC or sub something the assembly
schedule cannot:

1. **What happens where assemblies meet** - laps, turn-ups, terminations, which
   layer goes over which.
2. **Continuity of the control layers** - water, air, thermal, vapor (and fire, where
   rated) carried across the joint without a break.
3. **Items that belong to no assembly** - flashings, transition membranes, blocking,
   sealant joints, anchors, screens, trim. These get the black-square flag.
4. **Dimensions and tolerances that must be held**, and why when it isn't obvious.
5. **Sequence** - what has to go in before what.
6. **Visible design intent** - flush, reveal, shadow line, alignment, no exposed
   fasteners.
7. **Responsibility and coordination** - per structural, deferred submittal, shop
   drawings, mock-up.
8. **Field-verify items** - things that must be checked before work proceeds.

Two tests for every note, before it goes on the sheet:
- *Would the builder do it differently without this note?* If no, cut it.
- *Is it in the assembly schedule?* If yes, cut it and make sure the tag is there.

Full rules, wording standards and before/after examples:
`references/note-rules.md`. Read it before writing notes.

## What to have before drawing

Ask for whatever is missing. Don't guess at any of it.

| Input | Why |
|---|---|
| Detail type and condition (for example, "roof eave at the stone wall, north side") | Picks the checklist in `references/detail-types.md` |
| Detail number and sheet (for example, 6 / A6.01), and scale | Title bubble, file name, cross-references |
| **Project assembly schedule** as `<project>/assemblies.yaml` (template: `templates/assemblies.yaml`) | The tags, and what the notes must not repeat. Copy it from the project's schedule sheet. Never invent a build-up. |
| Jurisdiction (City of Aspen or Pitkin County) | Code basis. The City runs houses under the IBC (the IRC is not adopted); the County adopts the IRC. |
| The existing sketch, markup or photo, if there is one | Draw to what the office has, then fix it |
| Structural, civil and interiors information that governs the detail | Refer to it with "PER STRUCTURAL" rather than guessing sizes |

If there is no assembly schedule yet, draw the tags anyway, leave the layers out
of the yaml file, and put "W_ AGREES WITH THE ASSEMBLY SCHEDULE" in the verify
list.

## Workflow

1. **Read the condition.** State in one or two lines what the detail shows and which
   assemblies meet in it. If the condition is ambiguous (for example, headwall vs
   sidewall, or above vs below grade), ask. Don't pick.
2. **Open the checklist** for the type in `references/detail-types.md`: what must be
   drawn, the continuity lines, and the usual verify items.
3. **Draw it** with `scripts/detailkit.py`, one Python script per detail, saved beside
   its output as `details/<NN>-<SHEET>-<slug>.py`. Enter geometry in real inches.
   Graphics standards and the API are in `references/drawing-standards.md`. The
   worked example is `examples/wall-at-foundation.py`.
4. **Tag every assembly** that is cut or seen, once per detail. Where an assembly
   changes (for example, a wall going below grade), that is a new tag. Don't stretch
   one tag across the change.
5. **Write the notes** per `references/note-rules.md`. Flag (black square) every item
   that belongs to no assembly.
6. **Code.** Cite a code section only where a note depends on a code limit the
   builder must hold. Get the section from the code library
   (phantom-press-hq/code-library, `aspen-pitkin-code` skill). Never cite it from
   memory. On a City of Aspen detail, never cite the IRC.
7. **Save and check.** `d.save("details", assemblies="<project>/assemblies.yaml")`
   writes the SVG, PNG, `.notes.txt` and `.json`, then runs
   `scripts/check_notes.py`. Fix every ERROR. Read every WARN.
8. **Look at the PNG** and fix any overlaps, crossed leaders, or text over linework.
   Move notes with `side=`, or move the targets. Re-save.
9. **Report** in plain words:
   - what was drawn;
   - the tags used;
   - any flagged items;
   - anything assumed, which goes in the verify list and in the reply;
   - the file paths.

Checking or marking up an existing detail follows the same rules. List the notes
that repeat an assembly, the missing tags, the missing continuity lines, and the
missing flagged items. The 100% CD checklists in `details/` on the project branches
are the format.

## Output conventions

- Files go in `details/` on the project's branch in the drawing-set repo. Name them
  `<NN>-<SHEET>-<slug>`, for example `06-A6.01-stone-wall-to-standing-seam-roof.svg`.
- Keep the `.py` next to the drawing so the detail can be regenerated after
  comments.
- Notes are ALL CAPS on the sheet.
- The `.notes.txt` file is the sheet text, ready to paste into the CAD note block.
- This repo is drawings only. The code library lives in phantom-press-hq/code-library.
  Don't copy code text into it.

## Files

| Path | What |
|---|---|
| `references/note-rules.md` | The tag-vs-note rule in full, wording standards, before/after examples |
| `references/detail-types.md` | Checklists for the six detail types |
| `references/drawing-standards.md` | Line weights, hatches, tags, symbols, scales, and the detailkit API |
| `scripts/detailkit.py` | Drawing library: SVG + PNG + notes + manifest |
| `scripts/check_notes.py` | Enforces the rules; run automatically by `save()` |
| `templates/assemblies.yaml` | Project assembly schedule format |
| `examples/wall-at-foundation.py` | Worked example, an exterior transition |
