"""Button images for a hand-built Sites page. Rendered in Chromium so the type
is real Montserrat and matches the site theme exactly."""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open("icon_svg.json"))

SECTIONS = [
    ("office-standards",  "standards", "Office Standards",  "Drafting, CAD, file naming, deliverables"),
    ("templates",         "templates", "Templates",         "Title blocks, minutes, transmittals, RFIs"),
    ("forms",             "forms",     "Forms",             "PTO, expenses, IT support, onboarding"),
    ("office-policies",   "policies",  "Office Policies",   "Handbook, safety, remote work, IT use"),
    ("sops",              "sops",      "SOPs",              "Kickoff, QA/QC, submittals, archiving"),
    ("revit-standards",   "revit",     "Revit Standards",   "Worksharing, families, views, LOD"),
    ("learning-sessions", "learning",  "Learning Sessions", "Weekly knowledge share, by month"),
    ("staff-directory",   "directory", "Staff Directory",   "Roles, extensions, emergency contacts"),
]
PILLS = [
    ("time-off",    "ft-form",   "Time off"),
    ("it-issue",    "tool",      "IT issue"),
    ("new-project", "templates", "New project"),
    ("expense",     "ft-sheet",  "Expense"),
    ("sign-up",     "calendar",  "Sign up"),
]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;padding:0;background:transparent}
  .wrap{display:inline-block;padding:6px}
  .card,.pill{
    --ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
    font-family:var(--ui); box-sizing:border-box;
  }
  .card{width:320px;height:190px;border-radius:18px;padding:20px;
        display:flex;flex-direction:column;position:relative}
  .card.navy {background:#022049;color:#fff}
  .card.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
  .chip{width:48px;height:48px;border-radius:13px;display:flex;
        align-items:center;justify-content:center;flex:none}
  .card.navy  .chip{background:#fff}
  .card.white .chip{background:#022049}
  .chip svg{width:24px;height:24px;fill:none;stroke-width:1.8;
            stroke-linecap:round;stroke-linejoin:round}
  .card.navy  .chip svg{stroke:#022049}
  .card.white .chip svg{stroke:#fff}
  .ttl{margin-top:14px;font:700 18px/1.25 var(--ui);letter-spacing:-.2px}
  .blurb{margin-top:6px;font:400 12.5px/1.45 var(--ui)}
  .card.navy  .blurb{color:#BACEE6}
  .card.white .blurb{color:#5C6672}
  .arw{position:absolute;right:18px;bottom:16px;font:600 12px var(--ui);opacity:.75}

  .pill{height:56px;border-radius:999px;padding:0 26px;display:inline-flex;
        align-items:center;gap:10px;font:600 15px var(--ui);white-space:nowrap}
  .pill.navy {background:#022049;color:#fff}
  .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
  .pill svg{width:18px;height:18px;fill:none;stroke-width:1.9;
            stroke-linecap:round;stroke-linejoin:round;flex:none}
  .pill.navy  svg{stroke:#fff}
  .pill.white svg{stroke:#022049}
</style>
"""

def icon(name):
    return '<svg viewBox="0 0 24 24">%s</svg>' % SVG[name]

def card_html(ic, title, blurb, tone):
    return ('<div class="wrap"><div class="card %s" id="t">'
            '<div class="chip">%s</div>'
            '<div class="ttl">%s</div><div class="blurb">%s</div>'
            '<div class="arw">Open &#8599;</div></div></div>'
            % (tone, icon(ic), title, blurb))

def pill_html(ic, label, tone):
    return ('<div class="wrap"><div class="pill %s" id="t">%s%s</div></div>'
            % (tone, icon(ic), label))


async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 900, "height": 400}, device_scale_factor=3)
        made = []
        for tone in ("navy", "white"):
            for slug, ic, title, blurb in SECTIONS:
                await pg.set_content(CSS + card_html(ic, title, blurb, tone), wait_until="load")
                await pg.wait_for_timeout(450)
                fn = "%s/card-%s-%s.png" % (OUT, slug, tone)
                await pg.locator("#t").screenshot(path=fn, omit_background=True)
                made.append(fn)
            for slug, ic, label in PILLS:
                await pg.set_content(CSS + pill_html(ic, label, tone), wait_until="load")
                await pg.wait_for_timeout(400)
                fn = "%s/button-%s-%s.png" % (OUT, slug, tone)
                await pg.locator("#t").screenshot(path=fn, omit_background=True)
                made.append(fn)
        await b.close()
    for f in made:
        print("%-52s %6.1f KB" % (os.path.basename(f), os.path.getsize(f)/1024))
    print(len(made), "images")

asyncio.run(main())
