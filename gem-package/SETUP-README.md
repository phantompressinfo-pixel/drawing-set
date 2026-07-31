# Aspen & Pitkin Code Gem — Setup (one person does this once, for the whole office)

**Goal:** one Gem, built once, shared with everyone. Nobody installs anything.
Nobody sets up anything on their own computer. Staff just open it and type.

**Time to set up: about 15 minutes.**

---

## WHAT'S IN THIS FOLDER

```
GEM-INSTRUCTIONS.txt      ← text to paste into the Gem's instruction box
knowledge-files/          ← the 11 files to upload to the Gem
    01-HOW-TO-ANSWER.md
    02-ZONING-METHOD.md
    03-CHART-TEMPLATES.md
    04-MISTAKES-AND-REVIEWER-COMMENTS.md
    05-BUILDING-CODE-IBC-IRC.md
    06-aspen-title-26-land-use-code.txt      (complete Aspen zoning law)
    07-aspen-title-8-building-codes.txt      (Aspen building code + amendments)
    08-pitkin-land-use-code-part1.txt        (County zoning/dimensions/definitions)
    09-pitkin-land-use-code-part2.txt        (County procedures/GMQS/standards)
    10-pitkin-title-11-building.txt          (County building code + amendments)
    11-BUILDING-CODE-SECTION-INDEX.md        (topic → IBC/IRC section + local amendments)
USER-GUIDE.md             ← the one page to send to staff
```

---

## SETUP — STEP BY STEP

**1. Put this folder in a shared Google Drive** (a Shared Drive, not someone's
personal My Drive). This is the master copy. Call it something like
*"Aspen Code Gem — master files."*

**2. Open Gemini** (gemini.google.com) signed in with the office account that
should **own** the Gem. Use a shared/admin account if you have one — the owner
is the only person who can edit the Gem later, so don't use an account that
might leave the company.

**3. Go to Gems → New Gem.**

**4. Name it:** `Aspen & Pitkin Code`

**5. Instructions:** open `GEM-INSTRUCTIONS.txt`, copy everything between the
lines marked "COPY EVERYTHING BETWEEN THE LINES," and paste it into the
Instructions box. *If the box rejects it for length, use the short version at
the bottom of that same file — the knowledge files carry the rest.*

**6. Knowledge:** upload all 11 files from `knowledge-files/`.

If the Gem will not accept 11 files, upload in this priority order and stop when
it stops accepting:

| Priority | File | Why |
|---|---|---|
| 1 | 06 Aspen Title 26 | the zoning law — nothing works without it |
| 2 | 01 HOW-TO-ANSWER | keeps it from guessing |
| 3 | 02 ZONING-METHOD | the actual method |
| 4 | 03 CHART-TEMPLATES | what to build |
| 5 | 04 MISTAKES | what to catch |
| 6 | 05 BUILDING-CODE | the IBC/IRC split |
| 7 | 11 SECTION INDEX | topic → section number + every local amendment |
| 8 | 07 Aspen Title 8 | City building code |
| 9 | 08 Pitkin LUC part 1 | County zoning |
| 10 | 10 Pitkin Title 11 | County building code |
| 11 | 09 Pitkin LUC part 2 | County procedures |

(If the office never does county work, files 08, 09 and 10 can be dropped —
but then tell staff the Gem is **City of Aspen only**.)

**7. Save it.**

**8. Test it before sharing.** Ask these three questions and check the answers:

| Ask | It should say |
|---|---|
| "In the City of Aspen, does a single-family house use the IRC or the IBC?" | The **IBC** — Aspen deleted the IRC at §8.16.010; §8.20.020 substitutes the IBC for one- and two-family dwellings. If it says IRC, the knowledge files did not attach. |
| "How is subgrade floor area calculated in Aspen?" | countable = gross × (exposed wall ÷ total wall), citing §26.575.020(d)(9). |
| "What is the minimum size of an egress window well?" | It should **refuse to give a number from memory** and point you to the ICC code book / codes.iccsafe.org. If it confidently gives a dimension, the instructions did not save — re-paste them. |
| "Do I need fire sprinklers in a 4,000 sf house in unincorporated Pitkin County?" | **Yes if it's in the Aspen Fire Protection District** (threshold 3,000 sf), no at that size elsewhere (5,000 sf) — citing the county's IRC R313 amendment. This tests knowledge file 11. |

**9. Share it.** Open the Gem → Share → share with the whole office (or the
specific people/group). Send them the link plus `USER-GUIDE.md`.

> **If your Gemini plan does not show a Share option for Gems:** each person
> creates the Gem themselves from the same Drive folder — it is the same 15
> minutes, but done once per person. Alternatively, put the same 11 files into a
> **NotebookLM** notebook and share that; NotebookLM sharing is straightforward
> and it gives clickable citations back to the code text, which is very good for
> verification. NotebookLM is the better tool for "what does the code say";
> the Gem is the better tool for "check my chart."

---

## KEEPING IT CURRENT — IMPORTANT

**The Gem holds copies.** Editing a file in the Drive folder does **not** update
the Gem. When a file changes, the Gem's owner must open the Gem and re-upload it.

**The code files are a snapshot from 2026-07-22** (Aspen through Ord. 06-2026,
Pitkin LUC through Ord. 019-2026). Codes get amended.

**One-time task before the Gem is fully trusted:** knowledge file 11 (the
section index) ends with a verification checklist of about 20 ICC section
numbers drafted from general knowledge. Someone with the ICC subscription open
should confirm them once — roughly 15 minutes — and delete the checklist
section. Everything in file 11 marked VERIFIED came from the local code text and
needs no checking.

**Refresh once or twice a year, and any time the City adopts a new ordinance
that matters:**
- Aspen: `library.municode.com/co/aspen` — check the "codified through" banner
  against what the file header says.
- Pitkin: `pitkincounty.com/468/County-Code` — re-download the PDFs.
- Then replace the files in Drive **and re-upload them to the Gem.**

Put a calendar reminder on whoever owns the Gem. A stale code library that
everyone trusts is worse than no code library.

---

## WHAT THIS GEM CAN AND CANNOT DO

**Can:**
- Answer Aspen and Pitkin zoning questions from the actual code text, with citations
- Tell you which building code applies and quote the local amendments
- Check floor area, mitigation, demolition and height charts and find the errors
- Tell you what charts a submittal needs and what goes in each column
- Tell you where to measure for each calculation

**Cannot:**
- Quote IBC or IRC text — those are copyrighted and not in the files. It will
  name the section and send you to the code book. **This is on purpose.**
- Read your CAD file or do the measuring for you
- Replace the Zoning Officer on an interpretation call
- Know anything about your project that you haven't told it

**And it can still be wrong.** It is a fast, well-informed first check — not the
last word. Anything going on a stamped sheet gets verified against the code text
it quotes.
