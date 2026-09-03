# EAD Office Hub — Google Sites build guide

Everything here builds inside Google Sites. Nothing is hosted anywhere else,
nothing needs a developer, and nothing needs a subscription you don't already have.

---

## The short answer

**Yes — this can be 100% Google Sites.**

I told you earlier that the Embed block only accepts an iframe pointing at an
outside URL. That was wrong, and it changes the answer. Sites' **Insert → Embed →
Embed code** tab accepts raw HTML and CSS pasted directly into the box. That is a
normal, supported Sites feature — not a workaround, not a hack, and it keeps
everything inside your Google Workspace.

So the frosted-glass cards, the navy field, the search bar, the action pills, the
status dots, and the hover behaviour all reproduce exactly. You paste one block per
page. Everything else — navigation, page titles, the auto-updating Drive file
lists, publishing, and permissions — is built with the normal Sites editor.

**Two things genuinely change from the design.** Both are hard limits in Sites,
not shortcuts:

| In the design | In Sites | Why |
|---|---|---|
| Gotham | **Montserrat** | Gotham is a licensed Hoefler typeface. It isn't in Sites' font list and can't be loaded by a page you don't host. Montserrat is the standard geometric substitute — same tall x-height, same feel. Gotham stays where you already use it: print, stamps, deliverables. |
| Left rail with icons + document counts | **Sites side navigation** | Same position, and it takes your navy from the theme. But Sites won't put an icon or a count next to a nav item. The icons move onto the cards — which is where you said you preferred them. |

Everything else matches.

---

## What you've been given

```
google-sites/
├── BUILD-GUIDE.md              this file
├── embeds/                     10 paste-ready blocks, one per page
│   ├── 01-home.html
│   ├── 02-announcements.html
│   ├── 03-office-standards.html
│   ├── 04-templates.html
│   ├── 05-forms.html
│   ├── 06-office-policies.html
│   ├── 07-sops.html
│   ├── 08-revit-standards.html
│   ├── 09-learning-sessions.html
│   └── 10-staff-directory.html
├── icons/                      36 PNGs — every icon, navy and white,
│                               256px, transparent background
├── ead-office-hub-icons.zip    the same icons, zipped
└── backgrounds/
    ├── banner-navy-2560x900.jpg        page banner
    ├── banner-navy-wide-3200x1000.jpg  wider banner
    └── section-navy-2560x1440.jpg      full section background
```

The icons are already baked into the embed blocks as vector artwork, so they stay
sharp at any size and you never have to upload them. The PNG folder is there for
everything *outside* the embeds — the site logo, slide decks, printed handouts.

---

## Your brand values, in one place

| | Value |
|---|---|
| Navy (primary) | `#022049` — Pantone 282 C |
| Charcoal (text) | `#4B4B4B` — Pantone 2336 C |
| Card chip / accent | `#2C588E` |
| Glass card border | `#6C94C4` |
| "Required" dot | `#7FCBA4` |
| "Updated" dot | `#E0AE55` |
| Heading + body font | Montserrat |
| Label / date font | IBM Plex Mono |

---

## Before you start: get Drive right

The site is a front door. The files stay in Drive. Two things to settle first,
because everything else depends on them:

1. **Build the folder structure** in the Shared drive, matching the structure
   I sent you. One top-level folder per section.
2. **Give the office access to the Shared drive.** The Site does *not* grant
   access to files it links to. If someone can't open a Drive folder directly,
   the card will fail for them too. Set access on the Shared drive once, at the
   member level, and every link on every page works for everyone.

---

## Step 1 — Create the site

1. Go to **sites.google.com** → **Blank**.
2. Name it `EAD Office Hub` (top-left) and set the same as the site title.
3. **Settings (gear) → Brand images → Logo** → upload
   `EAD LOGO BLUE TYPE NO BACKGROUND_300dpi.png` from
   `Shared drives / EAD - Office / Graphics / Stamps, Logos, Letterhead`.
   Sites will ask for a matching text colour — choose the dark option.

---

## Step 2 — Theme

1. Right panel → **Themes** → scroll to **Custom** → **+** (create a theme).
2. Name it `EAD`.
3. **Colour** → custom → paste `022049`.
4. **Font style** → set both the heading and body font to **Montserrat**.
5. Pick the flattest of the six style presets — the one with no drop shadows.

This makes the Sites chrome (nav, titles, buttons) match the embedded cards,
so the seam doesn't show.

---

## Step 3 — Navigation

1. **Pages** tab → add these ten pages, in this order. The names matter — they
   are the section names people will learn:

   ```
   Home
   Announcements
   Office Standards
   Templates
   Forms
   Office Policies
   SOPs
   Revit Standards
   Learning Sessions
   Staff Directory
   ```

2. **Settings (gear) → Navigation → Side.**
   This puts the index on the left, where the design has it.

---

## Step 4 — Build a page

Do this once per page. It takes about three minutes each.

1. **Open the page.**

2. **Set the header.** Hover the page banner → **Change image** → **Upload** →
   `backgrounds/banner-navy-2560x900.jpg`. Then **Header type → Title only**
   (or **Banner** if you want it taller).

3. **Paste the block.** Right panel → **Insert** → **Embed** → the
   **Embed code** tab (not "By URL") → open the matching file from `embeds/`,
   select all, copy, paste into the box → **Next** → **Insert**.

4. **Size it.** Drag the block to the full width of the content area, then drag
   the bottom handle down. Suggested heights:

   | Page | Height |
   |---|---|
   | Home | 780 px |
   | Announcements | 680 px |
   | Office Standards | 780 px |
   | Templates | 760 px |
   | Forms | 760 px |
   | Office Policies | 760 px |
   | SOPs | 760 px |
   | Revit Standards | 780 px |
   | Learning Sessions | 700 px |
   | Staff Directory | 550 px |

   Too short and the block scrolls inside itself; too tall and you get navy
   dead space. Adjust by eye after you publish.

5. **Add the live file list underneath.** This is the part that never needs
   maintaining. **Insert → Drive → pick that section's folder → Insert.**
   Anything anyone drops in that folder from now on shows up here on its own.

Repeat for all ten pages.

> **Titles:** each block prints its own title and subtitle. If you'd rather the
> Sites page banner carry them, open the block and set `title: ""` and
> `subtitle: ""` in the CONFIG — the block then starts at the search bar.

---

## Step 5 — Turn on search

**Settings (gear) → Search → on.** This adds the magnifier to the published
header and searches your page text.

Note that the white search bar *inside* the cards does something different and
more useful: it searches **Drive**, including the text inside your PDFs. Sites'
own search can't do that. Keep both — they answer different questions.

To scope that bar to just the office hub instead of all of Drive, open any
block and paste the hub's folder ID into `driveFolderId`. The ID is the long
string in the folder's URL after `/folders/`.

---

## Step 6 — Publish

1. **Publish** (top right) → choose the web address, e.g. `ead-office-hub`.
2. **Manage** → set who can view: **Everyone at Eigelberger Architecture &
   Design**. Leave it off the public web.
3. Send the link out, and pin it as the browser homepage on office machines.

---

## Filling in the links

Every block opens with a **CONFIG** section. It is a plain list — the only
thing you ever edit. Paste each Drive link between the empty quotes:

```js
cards: [
  {title:"Drafting & CAD Standards",
   blurb:"Line weights and layer naming",
   format:"PDF", icon:"ft-pdf", status:"REQUIRED",
   link:"https://drive.google.com/file/d/.../view"},
```

Rules:

- **Keep the quotes.** `link:"https://…"` — the `https://` included.
- **Keep the commas** at the end of each line.
- `status` accepts `"REQUIRED"` (green dot), `"UPDATED"` (amber dot), or `""`
  for no dot.
- To remove a card, delete its whole `{ … },` block. To add one, copy an
  existing block and edit it.
- If you add a link by hand anywhere, keep `target="_top"` on it. Embedded
  blocks live in a frame, and without that the page opens *inside* the card.

After editing: click the block → the pencil icon → paste the updated code →
**Next** → **Insert**.

---

## How it stays current

Two layers, on purpose:

- **The cards** are the six-to-eight things people actually need. They change
  a few times a year, and they're worth curating by hand so the important
  documents stay at the top.
- **The Drive folder list underneath** is everything else, always live. Drop a
  file in the folder and it appears on the site immediately. Nobody edits the
  site.

That split is what keeps this from becoming a second thing to maintain.

---

## Known limits — read before you promise anything

1. **Embedded blocks aren't found by Sites' own search.** Your section names and
   page titles are (those are real Sites text), but card titles are not. This
   is why the Drive search bar inside the block matters.
2. **The block height is fixed.** Sites can't grow a frame to fit its contents.
   Set it once per the table above; if content overflows, the block scrolls
   inside itself rather than breaking the page.
3. **Desktop only.** Per your instruction, there's no phone layout. On a narrow
   screen the cards will stack but the spacing won't be tuned.
4. **Sites nav can't take icons or counts.** Covered above.
5. **A card is only as accessible as the file behind it.** The site does not
   grant Drive access. Fix this once at the Shared drive level.
6. **Five action pills wrap to two rows** at the Sites content width (1000px).
   It reads fine. If you want them on one row, drop one — four fit.

---

## One thing to decide

The sample card lists include documents you'd previously told me to cut from the
folder structure: **CAD Standards**, **Deliverable Standards**, **Plotting &
Printing Standards**, **Specifications Format**, **IT Support Request**, and the
whole **Staff Directory** section.

I left them in rather than guess, because you approved the rendered pages with
them showing. Once the real folder structure is settled, edit the CONFIG lists to
match it — or tell me and I'll strip them and regenerate the blocks.
