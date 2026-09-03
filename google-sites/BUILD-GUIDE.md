# EAD Office Hub — Google Sites build guide

Everything here builds inside Google Sites. Nothing is hosted anywhere else,
nothing needs a developer, and nothing needs a subscription you don't already have.

---

## The short answer

**Yes — this can be 100% Google Sites, including the left menu with icons.**

Sites has a feature — **Insert → Embed → Embed code** — that accepts design code
pasted straight into the page. It's a normal, supported feature. That's what makes
the frosted-glass cards, the navy field, the search bar, the action pills, and the
left index rail all reproduce exactly.

**One thing changes from the design, and only one:**

| In the design | In Sites | Why |
|---|---|---|
| Gotham | **Montserrat** | Gotham is a licensed Hoefler typeface. It isn't in Sites' font list and can't be loaded by a page you don't host. Montserrat is the standard geometric substitute — same tall x-height, same feel. Gotham stays where you already use it: print, stamps, deliverables. |

Everything else matches, including the icons and document counts in the left menu.

### How the left menu works

Google Sites' *own* navigation is plain text — it can't take icons or counts. So
the rail isn't Sites' navigation. It's drawn inside each block, exactly as
designed, and its links jump to the real Sites pages. You then hide Sites' own
menu so it doesn't duplicate it (Step 3).

You get the design you picked, and every page still has its own real web address
you can bookmark or paste into an email.

---

## What you've been given

```
google-sites/
├── BUILD-GUIDE.md              this file
├── embeds/                     9 paste-ready blocks, one per page
│   ├── 1-home.html                   6-sops.html
│   ├── 2-office-standards.html       7-revit-standards.html
│   ├── 3-templates.html              8-learning-sessions.html
│   ├── 4-forms.html                  9-staff-directory.html
│   └── 5-office-policies.html
├── icons/                      36 PNGs — every icon, navy and white,
│                               256px, transparent background
├── ead-office-hub-icons.zip    the same icons, zipped
└── backgrounds/
    ├── banner-navy-2560x900.jpg        page banner
    ├── banner-navy-wide-3200x1000.jpg  wider banner
    └── section-navy-2560x1440.jpg      full section background
```

The icons are already built into the blocks as vector artwork, so they stay sharp
at any size and you never upload them. The PNG folder is for everything *outside*
the site — slide decks, printed handouts.

---

## Your brand values, in one place

| | Value |
|---|---|
| Navy (primary) | `#022049` — Pantone 282 C |
| Charcoal | `#4B4B4B` — Pantone 2336 C |
| Glass card border | `#6C94C4` — a navy tint, for edge visibility only |
| "Required" dot | `#7FCBA4` |
| "Updated" dot | `#E0AE55` |
| Heading + body font | Montserrat |
| Label / date font | IBM Plex Mono |

Navy does the work: the field, the card icon chips, the active menu row, and the
search button are all Pantone 282 C exactly. White carries the rail, the search
bar, and the action buttons. Charcoal is the rail's text, as on the brand sheet.

The lighter blues — the glow in the top corner, the card edges, the small grey-blue
text on the cards — are lighter steps of the same navy, all within three degrees of
its hue. A dark field needs lighter steps of its own colour to stay readable; they
aren't a second blue.

---

## Before you start: get Drive right

The site is a front door. The files stay in Drive. Two things to settle first,
because everything else depends on them:

1. **Build the folder structure** in the Shared drive, matching the structure I
   sent you. One top-level folder per section.
2. **Give the office access to the Shared drive.** The Site does *not* grant
   access to files it links to. If someone can't open a Drive folder directly, the
   card will fail for them too. Set access once at the Shared drive member level
   and every link on every page works for everyone.

---

## Step 1 — Create the site

1. **sites.google.com** → **Blank**.
2. Name it `EAD Office Hub` (top-left) and set the site title to match.
3. **Settings (gear) → Brand images → Logo** → upload
   `EAD LOGO BLUE TYPE NO BACKGROUND_300dpi.png` from
   `Shared drives / EAD - Office / Graphics / Stamps, Logos, Letterhead`.

---

## Step 2 — Theme

1. Right panel → **Themes** → scroll to **Custom** → **+**.
2. Name it `EAD`.
3. **Colour** → custom → paste `022049`.
4. **Font style** → set heading and body to **Montserrat**.
5. Pick the flattest of the six style presets — the one with no drop shadows.

---

## Step 3 — Pages, and hiding Sites' own menu

1. **Pages** tab → add these nine pages, **in this order and with these exact
   names**. The names decide each page's web address, and the rail's links are
   built from them — so a typo here breaks that page's link.

   ```
   Home
   Office Standards
   Templates
   Forms
   Office Policies
   SOPs
   Revit Standards
   Learning Sessions
   Staff Directory
   ```

2. **Settings (gear) → Navigation → Top.**

3. In the Pages list, right-click each page → **Hide from navigation**.

   This is the step that stops Sites' plain-text menu from duplicating your
   designed rail. If Sites won't let you hide the last remaining one, leave
   **Home** visible — the bar then shows a single word and reads as a header.

---

## Step 4 — Publish early

Do this now, before pasting anything — the rail needs the site's address.

1. **Publish** (top right) → choose the web address, e.g. `ead-office-hub`.
2. **Manage** → who can view: **Everyone at Eigelberger Architecture & Design**.
   Leave it off the public web.
3. **Copy the published address.** It looks like:

   ```
   https://sites.google.com/eigelberger.com/ead-office-hub
   ```

Keep it handy. You'll paste it into each block once.

---

## Step 5 — Build a page

Once per page, about three minutes each.

1. **Open the page.**

2. **Set the header.** Hover the page banner → **Change image** → **Upload** →
   `backgrounds/banner-navy-2560x900.jpg`. Then **Header type → Title only**.

3. **Open the matching file** from `embeds/` in any text editor (Notepad,
   TextEdit). Near the top you'll see:

   ```js
   siteBase: "",
   ```

   Paste your published address between the quotes, **with no slash on the end**:

   ```js
   siteBase: "https://sites.google.com/eigelberger.com/ead-office-hub",
   ```

   That one line builds all nine of the rail's links. It's the same value in every
   file — paste it once, then copy that line into the other eight.

4. **Paste the block.** Select all in the file, copy. In Sites: right panel →
   **Insert** → **Embed** → the **Embed code** tab (not "By URL") → paste →
   **Next** → **Insert**.

5. **Size it.** Drag the block to the full width of the content area, then drag
   the bottom handle down to:

   | Page | Height | | Page | Height |
   |---|---|---|---|---|
   | Home | 740 px | | SOPs | 740 px |
   | Office Standards | 760 px | | Revit Standards | 765 px |
   | Templates | 715 px | | Learning Sessions | 670 px |
   | Forms | 760 px | | Staff Directory | 560 px |
   | Office Policies | 760 px | | | |

   Too short and the block scrolls inside itself; too tall and you get navy dead
   space below the cards. Adjust by eye after publishing.

6. **Add the live file list underneath.** This is the part that never needs
   maintaining. **Insert → Drive → pick that section's folder → Insert.** Anything
   dropped into that folder from now on appears here on its own.

Repeat for all nine pages, then **Publish** again.

> **Titles:** each block prints its own title and subtitle. If you'd rather the
> Sites page banner carry them, set `title: ""` and `subtitle: ""` in the block —
> it then starts at the search bar.

---

## Step 6 — Turn on search

**Settings (gear) → Search → on.** This adds the magnifier to the published header
and searches your page text.

The white search bar *inside* the design does something different and more useful:
it searches **Drive**, including the text inside your PDFs. Sites' own search
can't do that. Keep both — they answer different questions.

To scope that bar to just the office hub instead of all of Drive, paste the hub's
folder ID into `driveFolderId`. The ID is the long string in the folder's URL
after `/folders/`.

---

## Filling in the document links

Every block has a **CONFIG** section — a plain list, and the only part you edit.
Paste each Drive link between the empty quotes:

```js
cards: [
  {title:"Drafting & CAD Standards",
   blurb:"Line weights and layer naming",
   format:"PDF", icon:"ft-pdf", status:"REQUIRED",
   link:"https://drive.google.com/file/d/.../view"},
```

Rules:

- **Keep the quotes**, and the `https://`.
- **Keep the commas** at the end of each line.
- `status` accepts `"REQUIRED"` (green dot), `"UPDATED"` (amber dot), or `""` for
  no dot.
- To remove a card, delete its whole `{ … },` block. To add one, copy an existing
  block and edit it.
- If you add a link by hand, keep `target="_top"` on it. Blocks live in a frame,
  and without that the page opens *inside* the card.

To update a block later: click it → the pencil icon → paste the new code →
**Next** → **Insert**.

### Changing the left menu

Each block's CONFIG also holds a `menu:` list — the nine sections, their icons,
and the number shown on the right:

```js
menu: [
  ["Home",             "home",      "" ],
  ["Office Standards", "standards", "6"],
  ["Templates",        "templates", "4"],
```

The number counts the **cards featured on that page**, not the files in the Drive
folder — so it only changes when you add or remove a card, not when someone
uploads a file. Set it to `""` for no number at all.

This block is identical in all nine files. Edit it once, then paste it over the
same block in the other eight.

---

## How it stays current

Two layers, on purpose:

- **The cards** are the six-to-eight things people actually need. They change a few
  times a year and are worth curating so the important documents stay on top.
- **The Drive folder list underneath** is everything else, always live. Drop a file
  in the folder and it appears on the site immediately. Nobody edits the site.

That split is what keeps this from becoming a second thing to maintain.

---

## Known limits — read before you promise anything

1. **Blocks aren't found by Sites' own search.** Your page titles are (real Sites
   text), but card titles aren't. This is why the Drive search bar matters.
2. **Block height is fixed.** Sites can't grow a frame to fit its contents. Set it
   once from the table above; if content overflows, the block scrolls inside itself
   rather than breaking the page.
3. **The rail lives in all nine blocks.** So renaming a section, or changing a
   document count, means editing nine files instead of one. It's one copy-paste of
   the `menu:` block into each — but it's nine, not one.
4. **Page names drive the rail's links.** Rename a page in Sites and its rail link
   breaks until you rename it back or update the rail list.
5. **Desktop only.** Per your instruction, there's no phone layout. On a narrow
   screen the cards stack but the spacing isn't tuned.
6. **A card is only as accessible as the file behind it.** The site does not grant
   Drive access — fix this once at the Shared drive level.
7. **Five action pills wrap to two rows** at the Sites content width. It reads
   fine. If you want them on one row, drop one — four fit.

---

## What upkeep actually looks like

Worth being straight about, since it's the thing that decides whether this survives:

| What | How often it changes | What it takes |
|---|---|---|
| Files inside the Drive folders | Constantly | **Nothing.** Drop the file in Drive; the folder list on the page shows it. |
| The cards on a section page | A few times a year | Edit that page's CONFIG list |
| A section name or its number | Rarely | Edit the `menu:` block, paste into all nine |

The cards are a curated shortlist, not a catalogue. Let the Drive folder list
underneath carry everything else — that's the part that never goes stale.

*(Announcements was removed. Staff Directory is in, with its own page and rail
entry. The sample cards still include CAD Standards, Deliverable Standards,
Plotting & Printing, Specifications Format, and IT Support Request — kept per your
instruction; edit the CONFIG lists once the real folder structure is settled.)*
