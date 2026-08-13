# Anatomy of a response sheet

The template is `../assets/response-sheet.html`. This is what each part is for,
in the order it appears, and when to drop it.

Everything here is **structure**. Every value shown is a placeholder standing in
for something read off the project currently being worked on.

---

## 1. Title block — always

Borrowed from a drawing sheet's title block, and it earns the space by making
the response self-identifying when printed and passed around.

```html
<header class="titleblock">
  <div class="tb-main">
    <p class="tb-eyebrow">Plan Review Response · Comment [NN] · [scope]</p>
    <h1>[Subject in plain language]</h1>
    <p class="tb-sub">[What this covers, and explicitly what it does not.]</p>
  </div>
  <div class="tb-fields">
    <div><span class="tb-k">[Key]</span><span class="tb-v">[Value]</span></div>
    ...four cells...
  </div>
</header>
```

- **Eyebrow** carries the reviewer's own comment number. Theirs, not yours —
  the reply is checked against their list. If the sheet is a partial response,
  say so here (`Open items only`), so nobody reads silence as completion.
- **H1** states the subject the way you would say it out loud, not the way the
  comment is worded. The comment is quoted below; the heading orients.
- **Sub** draws the boundary. A response that does not say what it excludes
  gets read as a response to everything.
- **Four fields** are the parameters a reviewer checks first. Which four depends
  on the comment — the governing code section, the performance target, the
  method or assembly, the date. Pick the four that decide the answer.

## 2. Where it stands — when the response is partial

One `.lede` paragraph: what is resolved, what is not, what changed since the
last submission. Skip it on a first, complete response — there is no standing to
report.

## 3. Checks on what is already drawn — when details exist

One `.detcard` per detail, in the set's own detail numbering.

```html
<div class="detcard">
  <div class="det-h">
    <span class="det-n">[N — what the detail shows]</span>
    <span class="det-w">[one-line verdict]</span>
  </div>
  <div class="det-b">
    <ol>
      <li><b>[The problem, as a statement.]</b> [Why it matters, then the exact
        text to add: UPPERCASE STRING, AS IT GOES ON THE DRAWING.]</li>
    </ol>
  </div>
</div>
```

- **`det-w`** is the verdict at a glance — `Two additions`, `Still missing the
  handoff`, `One leader on the wrong target`. It lets someone triage without
  reading the list.
- Each `<li>` opens with a **bolded statement of what is wrong**, not an
  instruction. `The vapor retarder leader points only at the turn-up.` The fix
  follows. Stating the defect first is what lets the architect check it against
  the drawing rather than take it on faith.
- Then the literal callout. Uppercase. Complete. Lettering-ready.
- Say **where the leader lands**, not only what to write. A correct note on the
  wrong element still fails review.

## 4. What is not yet drawn — when new details are needed

Inline SVG in `.figframe`, one `<figure>` per detail, with a `<figcaption>`
saying **why the detail exists** — the condition it resolves and the keynote or
ask it answers. A detail with no stated purpose invites a reviewer to wonder
what it is for.

See `drawing-conventions.md`. Combine conditions where one drawing genuinely
resolves two asks; say so in the caption.

## 5. Sheet notes to place — when note text is part of the answer

```html
<div class="notes notes-plain">
  <div class="notes-h">[Sheet __] — [note block name]</div>
  <ol start="[N]" style="counter-reset: n [N-1]"> ... </ol>
</div>
```

- **`start` and `counter-reset` must match the set's real note numbering.** The
  note has to drop into an existing block without renumbering it. Read the
  numbers off the sheet; if they are unknown, placeholder them.
- Say plainly which notes **replace** existing text and which are **additions**.
  A revised note that looks like an addition leaves the superseded text on the
  sheet, and the two then contradict each other.
- Note text is uppercase throughout, as it appears on the sheet.
- `.notes` without `.notes-plain` numbers items `AS-01`, `AS-02` … for a keyed
  schedule; `.notes-plain` numbers them `1.` `2.` for a general note block.

## 6. Compliance schedule — when the comment cites a code table

Three columns, and the order is the argument:

| Column | Class | Content |
| --- | --- | --- |
| Component | `c-comp` | The code table's own row name |
| Code criteria | `c-code` | The criterion **quoted**, not paraphrased. `.crit` sub-labels split multiple criteria in one row. |
| This project | `c-proj` | What this project does, uppercase, as it reads on the sheet |

**Reproduce every row of the code table, including rows that do not apply** —
say `NOT APPLICABLE — [why]`. A reviewer checks the table off line by line, and
a missing row reads as an omission rather than a non-condition.

Add `.flagrow` to any row still unresolved, so it is visible rather than buried.

The project column is where the answer lives: it must cross-reference the detail
that shows it. That cross-reference is what turns a note block into a response.

## 7. Then it is finished — always

The closing list. Every reviewer ask resolves to exactly one row.

```html
<div class="open">
  <div>
    <span class="tag tag-block">Draw</span>
    <div class="open-b"><b>[What]</b>[Where it is, or what it depends on.]</div>
  </div>
</div>
```

`tag-block` (red) for work not yet done — **Draw**. `tag-conf` (blue) for work
that is prepared and needs placing — **Fix**, **Place**, **Copy**. The colour
split is the point: red is what still blocks the resubmittal.

This section is the one a principal reads. It must be complete and honest — if
something is unresolved, it belongs here as red, not omitted.

## 8. Footer — always

Provenance in one line: code edition quoted, adopting ordinance, and
`Figures are schematic and not to scale.` The last clause is not boilerplate —
it is what keeps a response figure from being read as a construction detail.

---

## Conventions that hold throughout

- **Uppercase = goes on the sheet. Sentence case = explanation.** Never blur it.
- **`<span class="fill">[BRACKETED]</span>` for every unconfirmed value.** It
  renders in the accent colour so an unfilled blank cannot ship unnoticed.
  Grep `class="fill"` before sending.
- **`.ref` for sheet and detail cross-references** (`6/A6.01`) so they are
  visually distinct from body text.
- **Drop empty sections.** A heading with nothing under it costs credibility.
- **Self-contained.** No external CSS, fonts or scripts — the file gets emailed,
  opened offline, and printed.
