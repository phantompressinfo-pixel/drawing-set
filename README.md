# drawing-set

The office's shared code knowledge, packaged so anyone can use it — in Claude
Code, or in Google Workspace.

This repo is a **Claude Code plugin marketplace**. It publishes one plugin,
`building-code`, which carries the full text of the codes we work under plus the
method for answering with them. Install it once and it works in every project.

## Install (Claude Code)

In any project, run:

```
/plugin marketplace add phantompressinfo-pixel/drawing-set
/plugin install building-code@office-code
```

That's it. There is nothing to clone, no data to copy, and no paths to
configure — the code library ships inside the plugin. Update later with
`/plugin marketplace update office-code`.

Working *in this repo* needs no install: `.claude/settings.json` registers the
marketplace and enables the plugin automatically when you trust the folder.

## What you get

Two skills, which Claude loads on its own when a question calls for them.

**`aspen-pitkin-code`** — the authority for anything local. City of Aspen
Municipal Code (Title 8 buildings, Title 26 land use) and the Pitkin County Code
and Land Use Code, complete, as text. It also carries the working playbook for
Aspen residential zoning submittals — the four calculation packages (Height Over
Topography, Allowable Floor Area, Mitigation Floor Area/GMQS, Demolition), the
chart formats the City expects, every equation, element-by-element treatment,
and the reviewer comments that recur with how to answer them.

**`us-building-codes`** — the model code text underneath. IBC, IRC, IEBC, IPC,
IMC, IFGC and the 2010 ADA Standards, ~24,300 provisions across 217 CSVs, in
both Colorado's adopted 2021 editions and the unamended ICC baseline.

The two are wired together deliberately. Local amendments **govern**, so when a
model section has been changed by Aspen or Pitkin, a lookup stamps
`*** AMENDED LOCALLY ***` on the result and tells you the text shown is
superseded. A second flag marks text that is itself Colorado-amended where the
jurisdiction adopted the ICC edition instead. Both flags exist because quoting
the wrong layer is the easiest way to put a wrong citation on a sheet.

Ask in plain language — "what does Aspen require for guards at a hot tub", "what
counts toward mitigation floor area", "is a vented attic allowed here" — and
answers come back cited to section, read from the stored text rather than from
memory.

### Searching directly

The CSV bodies are long single lines, so raw grep is unreadable. Use the helper:

```bash
python3 "$CLAUDE_PLUGIN_ROOT/skills/us-building-codes/scripts/codesearch.py" "guard" --code ibc --chapter 10
python3 "$CLAUDE_PLUGIN_ROOT/skills/us-building-codes/scripts/codesearch.py" --section 1015.2 -j colorado
python3 "$CLAUDE_PLUGIN_ROOT/skills/us-building-codes/scripts/codesearch.py" "grab bar" -j ada --full
```

## Refreshing the code text

Both jurisdictions re-publish on their own schedule. The scrapers that built the
library are kept with it, so a refresh is reproducible rather than manual:

```bash
cd plugins/building-code
python3 code-library/tools/refresh-aspen.py     # Municode -> code-library/aspen/
bash    code-library/tools/refresh-pitkin.sh    # county PDFs -> code-library/pitkin/
python3 skills/us-building-codes/scripts/extract_amendments.py   # rebuild the amendment flags
```

Re-run `extract_amendments.py` after any re-supplement — the amendment list is
what drives the `*** AMENDED LOCALLY ***` warnings, and a stale list means a
superseded section quotes clean. See `plugins/building-code/code-library/tools/README.md`
for provenance and what each source actually publishes.

## For people not using Claude Code

`gem-package/` is the same knowledge built as a shared **Gemini Gem** for Google
Workspace — no git, no install, nothing to set up per person. Files `01`–`05`
are the tool-agnostic method (how to answer, where to measure for each
calculation package, blank chart templates, the mistake catalog); `06`–`10` are
the code text. `gem-package/SETUP-README.md` covers standing it up for an office,
and `USER-GUIDE.md` is what you hand to whoever will use it.

These files carry **no project numbers by design** — the numbers change every
project, the method does not.

## Layout

| Path | What it is |
| --- | --- |
| `.claude-plugin/marketplace.json` | Makes this repo an installable marketplace |
| `plugins/building-code/` | The plugin: two skills plus the bundled code library |
| `gem-package/` | The Workspace/Gemini delivery of the same method |
| `GEMINI.md` | Orientation for Gemini-based tools |
| `index.html` | Project timeline (password-protected) |
