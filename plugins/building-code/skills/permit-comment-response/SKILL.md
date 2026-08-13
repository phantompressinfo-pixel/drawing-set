---
name: permit-comment-response
description: Draft a response to a building department plan review comment, correction notice or redline — work out what the comment is actually asking, what the set already shows, what has to be drawn, and produce a response sheet with the exact callouts, sheet notes, compliance schedule and details needed to close it. Use when the user pastes or uploads a plan check comment, correction letter, review comment, redline or reviewer markup, asks how to answer or close out a comment, asks what a reviewer is asking for, or asks to draw a detail that answers a comment. For zoning review comments specifically (floor area, height, demolition, GMQS), also load aspen-pitkin-code and its zoning-submittal playbook.
---

# Responding to plan review comments

A comment is closed when a reviewer can open the set and see the answer on a
sheet. Not when the reply explains the intent — when the drawing carries it.
Everything below serves that.

## Project isolation — read this before anything else

**This skill is method only. It ships to every project the office runs.**

Nothing project-specific belongs in it, and nothing from one project may be
carried into another. Two jobs in the same zone district, under the same code
edition, still differ in: designated barrier and assemblies, sheet numbering and
note numbering, detail tags, which conditions actually occur, what the reviewer
already accepted, and what a prior approval capped.

So, every time:

- **Read the answer off *this* project's drawings and *this* comment.** Never
  off a previous project's response sheet, and never from memory of one.
- **Never copy a filled-in value forward.** Assemblies, R-values, ACH50 targets,
  sheet numbers, note numbers, detail tags, product names — all of it is
  per-project. Reuse the *structure*; re-derive the *content*.
- **Anything not yet confirmed from this project's set stays a visible
  placeholder** — `<span class="fill">[SHEET __]</span>` — never a plausible
  guess. A guessed sheet number that ships is a wrong cross-reference, and the
  reviewer finds it before you do.
- **One file per comment, in this project's own folder** —
  `permit-comments/comment-NN-<slug>.html` inside the project you are working
  in. Never write project output into this plugin.

If you have context from another project in the session, say so and set it
aside rather than letting it inform the answer.

## Method

**1. Read what the comment actually asks.** Reviewers usually ask two things at
once: a *designation* ("identify the continuous air barrier") and a
*demonstration* ("show it at every transition"). Answering only one leaves the
comment open. Split it into numbered asks before drafting, and keep the
reviewer's own numbering — replies are checked against their list, not yours.

**2. Find the governing text and quote it, not a paraphrase.** Use
`aspen-pitkin-code` for anything local — it governs — and `us-building-codes`
for the model text underneath. Heed the `*** AMENDED LOCALLY ***` stamp: quoting
model text that the jurisdiction amended is the fastest way to reopen a comment.
Cite the edition and the adopting ordinance in the footer.

**3. Inventory what the set already shows** before proposing anything. For each
ask, find the detail or note that covers it. Most comments are half-answered
already, and a response that redraws what exists reads as though the reviewer's
markup was not read.

**4. Classify every item into exactly one action.** These are the tags on the
closing list:

| Tag | Meaning |
| --- | --- |
| **Draw** | The condition occurs and no detail covers it |
| **Fix** | A detail exists but is missing a callout, a leader lands on the wrong thing, or a tag is wrong |
| **Place** | Note, schedule or legend text that has to land on a specific sheet |
| **Copy** | The department's own sample detail covers it — use theirs |

Prefer **Fix** over **Draw**. Adding a callout to an existing detail is cheaper
than a new one and keeps the set's detail count honest.

**5. Give the literal text, never a description of it.** "Call out the sill
gasket" is not usable. `GASKET SILL PLATE TO FOUNDATION` is — it goes straight
onto the drawing. Every fix names the words to add and the thing the leader
points at.

**6. Check continuity across sheets, not just within a detail.** Most reviewer
pushback is at handoffs: below-grade to above-grade, membrane to framing, one
assembly's barrier to the next. A detail that is correct alone and silent at its
edge is where the comment reopens. Name the transition explicitly in a note.

**7. Say what is schematic.** Figures drawn to answer a comment are not
construction documents. The footer says so.

## The two voices

The sheet mixes two registers and must never blur them:

- **Prose, sentence case** — to the architect. Why this is required, what the
  reviewer will look for, what is still unresolved.
- **UPPERCASE** — the literal string to letter onto the drawing or type into a
  note block. If it is uppercase in the response, it goes on the sheet verbatim.

A reader must be able to tell, at a glance, which text is explanation and which
is deliverable. Keep placeholders inside the uppercase runs marked with
`.fill` so an unfilled blank is impossible to miss.

## Producing the sheet

Copy the template and fill it in:

```
${CLAUDE_PLUGIN_ROOT}/skills/permit-comment-response/assets/response-sheet.html
```

It is self-contained — no external CSS, fonts or scripts — light and dark aware,
and prints. Section-by-section anatomy, including which sections to drop when
they do not apply:

- `${CLAUDE_PLUGIN_ROOT}/skills/permit-comment-response/references/sheet-anatomy.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/permit-comment-response/references/drawing-conventions.md`
  — how to draw the details as inline SVG in the set's conventions

Drop any section with nothing real in it. A compliance schedule is the right
answer to a comment citing a code table and pure noise otherwise; an empty
section reads as padding and costs the response credibility.

## Before it goes back

- Every reviewer ask has a matching item in the closing list.
- No `[BRACKETED]` placeholder is left unfilled — grep the file for `class="fill"`.
- Every sheet number, detail tag and note number was read off **this** project's
  set, not assumed.
- Every code citation was verified in the library and checked for a local
  amendment.
- Each uppercase string is something that can be lettered onto a drawing as-is.
- Nothing from another project survived into the text.
