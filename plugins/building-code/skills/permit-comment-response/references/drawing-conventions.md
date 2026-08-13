# Drawing response details as inline SVG

Details drawn to answer a comment must read as though they came out of the same
set as the drawings around them. A detail in a foreign graphic language invites
the reviewer to treat it as a sketch rather than as the answer.

The classes below are defined in `../assets/response-sheet.html`. They are all
`var(--…)`-based, so details stay legible in light and dark and print correctly.

## Frame

```html
<figure>
  <div class="figframe">
    <svg viewBox="0 0 1200 700" role="img"
         aria-label="[The condition, and what the drawing demonstrates.]">
      ...
    </svg>
  </div>
  <figcaption>[Why this detail exists — the ask it answers.]</figcaption>
</figure>
```

`viewBox="0 0 1200 700"` is the house proportion; keep it so details stack at a
consistent scale. The `aria-label` is a real sentence describing the condition
and what it demonstrates — it is the only description a screen reader gets, and
it is also what makes the figure searchable in the file.

## Line weights — the hierarchy carries the meaning

| Class | Weight | Use |
| --- | --- | --- |
| `.abd` | 2.4, dashed `11 6` | **The designated barrier.** Nothing else. |
| `.dln` | 1.0 solid | Object lines — assemblies, framing, substrate |
| `.dlead` | 0.8 solid | Leaders |
| `.ghost` | 1.1, `--faint` | Context that is present but not the subject |

**The heavy dash is reserved for the designated barrier, on every detail, with
no exceptions.** This is the single most important convention here. A reviewer
traces continuity by following that line from detail to detail; if a dashed line
somewhere else means a grid, a reference line or a hidden edge, the trace breaks
and the comment reopens. If the set already uses dashes for something else,
change the *other* thing or add a legend that resolves it — and say so in the
response.

Put a barrier legend on the sheet whenever more than one detail is involved.

## Fills and materials

Hatch patterns go in `<defs>` as `patternUnits="userSpaceOnUse"` and are drawn
with `--graphite` at `stroke-width: .55`, so they read as texture rather than
line work:

```html
<defs>
  <pattern id="[id]" width="16" height="16" patternUnits="userSpaceOnUse">
    <!-- concrete: scattered dots and chips · earth: broken horizontals ·
         insulation: lens/loop pattern · gravel: circles -->
  </pattern>
</defs>
<rect x="[x]" y="[y]" width="[w]" height="[h]" fill="url(#[id])"/>
```

- `.dfoam` — tinted fill (`--foamfill`) for the continuous sealing material, so
  the eye picks up where it is and where it stops. Reserve it for the material
  that is actually doing the sealing.
- `.seal` / `.sealdot` — sealant and gasket in the accent colour. Small, at
  joints. These mark the discrete seals the barrier depends on; they are what a
  reviewer counts.

Every material shown gets a callout. An unlabelled drawn element is the defect
that recurs most — a drain, a gasket or a membrane drawn and unnamed reads as
decoration, and the reviewer cannot confirm it is the thing the note refers to.

## Leaders and callouts

- Plain leader, arrowhead **on the element being named**, not near it.
- If a note covers two runs of the same element, **two arrowheads** or a leader
  placed where both read. A leader that lands on only one leg gets read as
  describing only that leg.
- Callout text is `.t-d` or `.t-dl`, mono, **uppercase**, worded exactly as it
  will be lettered.
- `.t-ds` in graphite for secondary annotation that is not itself a callout.
- `.t-dt` for the detail title, `.t-dn` for the detail number — bottom left, in
  the set's own tag format.

## What the drawing is for

A response detail exists to carry a specific note or resolve a specific
transition. Draw the condition at the point where continuity is in question —
the handoff, the penetration, the change of assembly — and not the general
assembly, which the set already shows elsewhere.

Where one drawing genuinely resolves two asks, draw it once and say so in the
caption. Where a condition cannot be built or inspected as sequenced, the
drawing exists to make that visible, and the caption should say that plainly.

## Check before shipping

- The heavy dash appears on every detail and means only the barrier.
- Every drawn element has a callout.
- Every leader lands on its element.
- Detail titles and numbers match the set's tag format — not a placeholder tag
  left over from drafting.
- The drawing reads in both light and dark (all colours via `var(--…)`).
