# How the code library was built, and how to refresh it

Two jurisdictions, two completely different acquisition methods, because they
publish their codes completely differently.

Nothing in `code-library/` was typed from memory or from a web search. Every
file traces to one of the two pipelines below, and each file carries a
provenance header stating the source, the supplement/ordinance it is current
through, and the retrieval date.

---

## CITY OF ASPEN — Municode's backend JSON API

**Script:** `refresh-aspen.py`

Aspen's code lives on `library.municode.com`, which is a JavaScript application —
a plain HTTP fetch of a code page returns an empty shell, not the code. But that
application gets its content from a public JSON API at `api.municode.com`, and
that API answers plain requests. **We pull from the same API the official site
uses**, so the text is the publisher's text, not a scrape of rendered pages.

### The endpoint chain

| Step | Endpoint | Returns |
|---|---|---|
| 1 | `Clients/name?clientName=Aspen&stateAbbr=co` | Aspen's **ClientID = 1085** |
| 2 | `Jobs/latest/18107` | the current **jobId** for productId 18107 (Aspen's Code of Ordinances) |
| 3 | `codesToc?jobId=&productId=` | the top-level table of contents |
| 4 | `codesToc/children?jobId=&nodeId=&productId=` | children of any TOC node — walk this down |
| 5 | `CodesContent?jobId=&nodeId=&productId=` | the actual sections, as `Docs[]` with HTML in `Content` |

**The `jobId` is the whole ballgame for currency.** It identifies one published
snapshot of the code. The capture in this repo used **jobId 491032**, which is
Supp. No. 7 Update 1, codified through **Ord. No. 06-2026** (enacted 2026-03-24).
Re-running step 2 returns whatever the current snapshot is; if the jobId has
changed, the code has been amended since our capture.

### What the script does with it

- Walks the TOC and builds a list of fetch units — one per Title, expanding
  containers (like "PART II") whose children are Titles.
- **Deduplicates documents by `Doc.Id`.** Fetching a container returns the same
  sections as fetching its children, so without this you get every section two
  or three times.
- Converts HTML to text, preserving table structure: `</td>` → ` | ` and
  `</tr>` → newline, so code tables (the floor area sliding scales, the Net Lot
  Area table) survive as readable pipe-delimited rows instead of collapsing.
- Writes one `.txt` per title with a provenance header, plus `_INDEX.txt`.
- Retries with backoff on network failure.

**Result: 29 files, 1,908 sections — the entire municipal code.**

### To refresh

```bash
python3 code-library/tools/refresh-aspen.py
```

First update the `JOB` constant at the top of the script if the jobId changed:

```bash
curl -s "https://api.municode.com/Jobs/latest/18107" | head -c 400
```

### Deep-linking a section for a colleague

```
https://library.municode.com/co/aspen/codes/municipal_code?nodeId=<nodeId>
```
e.g. §26.575.020 → `TIT26LAUSRE_PT500SURE_CH26.575MISURE_S26.575.020CAME`

---

## PITKIN COUNTY — PDFs from the county website

**Script:** `refresh-pitkin.sh`

The County has no API. It posts each Title and each Land Use Code chapter as a
PDF in its DocumentCenter, linked from
`https://pitkincounty.com/468/County-Code`.

The script downloads each PDF and extracts text with:

```bash
pdftotext -layout
```

**`-layout` is not optional.** It preserves column positions, which is what keeps
the dimensional standards tables in LUC Chapter 5 readable. Without it the
multi-column zone district tables scramble into unusable word soup.

It also **verifies each download is actually a PDF** before extracting — if a
document has moved, the server returns an HTML error page, and without that
check you would silently end up with an "error page" text file sitting in the
library looking like code.

**Result: 24 files, plus the original PDFs kept in `code-library/pitkin/pdf/`.**

### Two real limitations — know these

**1. The URLs rot.** Each document is a numeric DocumentCenter View ID
(`.../View/35921/chapter-05`). When the County amends a chapter, it uploads a
**new document with a new ID** — the old link may still work and still serve the
**old** text. So refreshing Pitkin is not just "re-run the script": you must
re-harvest the current links from the County Code page first and update the URLs
in the script. Check each file's "current through" line after refreshing.

**2. Text extraction loses figures.** Diagrams do not survive `pdftotext` — and
the County's building height measurement rules (**LUC §5-20-60**) depend on
figures. That is why the source PDFs are kept in `code-library/pitkin/pdf/`.
**For any question involving a diagram, open the PDF, not the .txt.**

### To refresh

```bash
bash code-library/tools/refresh-pitkin.sh
```

---

## ONE ENVIRONMENT-SPECIFIC DETAIL

Both scripts pass a CA bundle (`--cacert /root/.ccr/ca-bundle.crt`, and the
matching `ssl.create_default_context(cafile=...)` in Python) because this
container routes HTTPS through a proxy. **On a normal office machine, delete
those arguments** — they will not exist and are not needed.

---

## WHAT IS NOT HERE, AND WHY

**The IBC and IRC themselves.** Both jurisdictions adopt ICC codes by reference.
Those are copyrighted publications with no public full-text source, so the
library contains the **adopting ordinances and every local amendment** — which
is the part that is actually local law and the part that overrides the ICC base
text — but not the ICC text itself. Free read-only access: `codes.iccsafe.org`.

**City checklists, forms, and the Model Zoning Submittal set.** These are posted
separately by Community Development, are revised without notice, and are not part
of the codified ordinances. Download the current versions from the City site at
the start of each project.

---

## VERIFYING A REFRESH WORKED

After re-running either script, spot-check a section you already know:

```bash
grep -n "will not be adopted" code-library/aspen/title-8-*.txt      # 8.16.010, IRC deleted
grep -n "5-20-60" code-library/pitkin/luc-ch05-*.txt                # County height measurement
grep -c "^===== Sec" code-library/aspen/title-26-*.txt              # section count
```

And compare each file's header line against the "codified through" banner on the
publisher's site. If they disagree, the refresh did not take.
