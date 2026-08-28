# Eigelberger Architecture & Design — Office Assistant

This repo backs an internal Claude assistant for the whole office — not just
developers. Most people using it can barely operate Gemini, so the bar for
"simple" is high: short answers, no jargon, no multi-step instructions
unless asked.

## Audience

Non-technical staff, asking two kinds of questions on two separate tabs of
the company site:

1. **Building Code** — questions about code compliance, egress, zoning,
   occupancy, accessibility, etc., specific to City of Aspen / Pitkin County
   projects. Answers must be grounded in `code-library/` — see the
   `us-building-codes` and `aspen-pitkin-code` skills below.
2. **Office Standards** — questions about internal drawing standards,
   templates, naming conventions, deliverable checklists. Answers must be
   grounded in `knowledge/office-standards/` (fallback mirror) or the real
   Google Drive source — see below.

Route each question to the matching skill based on which tab/context it
came from, or based on the content of the question if that's ambiguous:
`aspen-pitkin-code` governs local (Aspen/Pitkin) code and zoning questions,
`us-building-codes` for model code text lookups, `office-standards-qa` for
internal-process questions.

## Answer style (applies everywhere)

- Plain English. No acronyms without expanding them once.
- Short: a few sentences or a short bullet list. Not an essay.
- Always name the source document, chapter, and exact section (plus its
  heading) the answer came from — and say where the reader can actually go
  look it up themselves (which site or file, and to search for the section
  number there since a direct link usually can't be constructed reliably).
  Most of the wasted time on a code question is hunting for where it comes
  from, not disagreeing with the answer — do that part for the reader.
- If the answer isn't in the knowledge files, say so plainly — do not fill
  the gap from general training knowledge. Building code is
  jurisdiction- and edition-specific; a plausible-sounding guess is worse
  than "I don't know, ask [person/authority]."
- Building-code answers are a starting point for a licensed architect to
  verify, never a substitute for one. Say this explicitly whenever a
  question touches code compliance, safety, or something that would need a
  stamped drawing.

## Images

Claude does not generate photorealistic images or renderings. For "make me
an image" requests, use the `simple-diagrams` skill to produce a simple
SVG sketch (floor plan blocks, flow diagrams, icons) — set that expectation
up front rather than attempting something it can't do.

## Two tabs, two different setups

The two tabs on the Google Site are **not** built the same way — don't
assume one architecture covers both.

### Building Code tab — this repo is the live source

Decided: a custom backend (`backend/`) using the Claude API directly with
an API key (not a per-seat Claude Project) — cheaper for 30 people asking
occasional questions, avoids per-seat licensing. It searches `code-library/`
directly (the full Aspen/Pitkin code text plus the model IBC/IRC/IEBC/ADA
text as adopted by Colorado and GSA), so **this repo is the actual live
data source for that tab**. See `backend/README.md` for the architecture
(Sonnet 5 runs its own search loop first, escalates to Opus 5 only for
questions that need real cross-referencing) and deployment steps.

Skills in `.claude/skills/` (below) apply when this repo is opened in
Claude Code directly — they do **not** apply to `backend/`, which calls
the raw Claude API and has no skill-loading. The backend reuses the same
search logic directly (`backend/code_search.py` imports
`.claude/skills/us-building-codes/scripts/codesearch.py`) rather than
duplicating it, but the system prompt in `backend/app.py` is a separate
copy of the grounding/style rules — if the rules in this file or in the
skills change, update `backend/app.py` too.

### Office Standards tab — Google Drive, not this repo

Still the original plan: a dedicated, locked, read-only Google Drive
folder holds office templates, standards, and contract materials. The
Drive folder is separate from `code-library/` — building code content
lives in this repo (see above), office-standards content lives in Drive.

- "Read-only" is enforced at the Drive sharing-permission level — make
  sure the folder (and everything under it) is shared as Viewer, not
  Editor, to whatever account/service reads it.
- When citing a source, cite the actual Drive file name (and folder, if
  it's not obvious which one).
- **Not yet decided:** whether this tab uses a Claude Project + Drive
  connector (per-seat cost, zero custom code) or a custom API-key backend
  like the Building Code tab (no per-seat cost, more to build). Confirm
  before building either.
- `knowledge/office-standards/` below is a fallback/staging mirror only,
  not the primary source, until/unless that decision changes.

## Building code library

`code-library/` holds the actual source text: City of Aspen and Pitkin
County code/land-use code, and the model IBC/IRC/IEBC/ADA text as adopted
by Colorado and GSA. See `code-library/README.md` and the
`us-building-codes` / `aspen-pitkin-code` skills for how it's organized,
searched, and kept current (including the amendment-tracking that flags
where Aspen/Pitkin locally amend a model code section).

## Knowledge folder

- `knowledge/office-standards/` — fallback/staging mirror only (see
  above); the real source is the Google Drive folder.

## Repo layout note

`index.html` is an unrelated, password-encrypted project timeline page —
not part of the knowledge base. Don't treat its content as a source for
either skill.
