"""The dashboard's second round: a Templates page banner, Staff Directory
demoted to a pill, and a Quick Links card to take its place in the grid.

Everything here reuses the existing recipes verbatim -- the banner from
gen_d_aligned.py, the pill from gen_snug.py, the card from gen_buttons.py --
so the new pieces sit beside the old ones without a seam.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

BTN  = "/home/user/drawing-set/google-sites/buttons"
BNR  = "/home/user/drawing-set/google-sites/banners"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/bnr"
SVG  = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/icon_svg.json"))

def icon(name, cls=""):
    return '<svg viewBox="0 0 24 24" class="%s">%s</svg>' % (cls, SVG[name])

# ---------------------------------------------------------------- banner
BANNER_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
 :root{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
 *{box-sizing:border-box;margin:0;padding:0}
 body{width:1280px;height:500px;overflow:hidden;font-family:var(--ui);color:#fff}
 .bn{width:1280px;height:500px;background-size:cover;background-position:center;
     display:flex;padding:0 96px}
 .row{display:flex;align-items:center;margin:auto 0}
 .mark{font:500 25px var(--ui);letter-spacing:9px;white-space:nowrap}
 .mark .thin{display:block;font:300 11.5px var(--ui);letter-spacing:6.2px;
             margin-top:9px;color:#AFC6E2}
 .vrule{width:1px;background:rgba(255,255,255,.3);margin:0 46px;height:96px}
 .hubwide{font:600 34px/1 var(--ui);letter-spacing:13px}
 .sub{font:400 15px var(--ui);color:#C6D6E8;margin-top:14px}
</style>
"""
MARK = ('<div class="mark">EIGELBERGER'
        '<span class="thin">ARCHITECTURE &amp; DESIGN</span></div>')

# Page banners: the right-hand half is all that changes between them.
PAGES = [("templates", "TEMPLATES", "Title blocks, minutes, transmittals, RFIs"),
         ("quick-links", "QUICK LINKS", "Codes, Pitkin County, City of Aspen")]

async def banners(b):
    for slug, head, sub in PAGES:
        for bg, ext in (("grid-banner-flat.png", "png"),
                        ("cols-banner-flat.png", "png")):
            body = ('<div class="row">%s<div class="vrule"></div><div>'
                    '<div class="hubwide">%s</div>'
                    '<div class="sub">%s</div></div></div>' % (MARK, head, sub))
            html = (BANNER_CSS + '<div class="bn" style="background-image:url(\'bg/%s\')">%s</div>'
                    % (bg, body))
            p = os.path.join(HERE, "_%s_%s.html" % (slug, bg))
            open(p, "w").write(html)
            pg = await b.new_page(viewport={"width": 1280, "height": 500},
                                  device_scale_factor=2)
            await pg.goto("file://" + p, wait_until="networkidle")
            await pg.wait_for_timeout(900)
            tone = "grid" if bg.startswith("grid") else "cols"
            await pg.screenshot(path="%s/banner-%s-%s-flat.%s" % (BNR, slug, tone, ext))
            await pg.close()
            print("banner-%s-%s-flat.%s" % (slug, tone, ext))

# ------------------------------------------------------------------ pill
# Same 198x50 canvas and 13.5px type as the row- set, so Staff Directory
# lines up with Sign up to present at any width.
PILL_W, PILL_H = 198, 50
PILL_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  box-sizing:border-box;display:flex;align-items:center;justify-content:center;gap:9px;
  border-radius:999px;white-space:nowrap;font:600 13.5px var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:16px;height:16px;fill:none;stroke-width:1.9;
   stroke-linecap:round;stroke-linejoin:round;flex:none}
 .pill.white svg{stroke:#022049}
 .pill.navy svg{stroke:#fff}
</style>
"""
PILLS = [("staff-directory", "directory", "Staff Directory")]

async def pills(b):
    pg = await b.new_page(viewport={"width": 600, "height": 200}, device_scale_factor=3)
    for tone in ("white", "navy"):
        for slug, ic, label in PILLS:
            html = PILL_CSS + ('<div class="wrap"><div class="pill %s" id="t" '
                               'style="width:%dpx;height:%dpx">%s%s</div></div>'
                               % (tone, PILL_W, PILL_H, icon(ic), label))
            await pg.set_content(html, wait_until="load")
            await pg.wait_for_timeout(350)
            await pg.locator("#t").screenshot(
                path="%s/row-%s-%s.png" % (BTN, slug, tone), omit_background=True)
            print("row-%s-%s.png" % (slug, tone))
    await pg.close()

# ------------------------------------------------------------------ card
CARD_CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;padding:0;background:transparent}
  .wrap{display:inline-block;padding:6px}
  .card{--ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
    font-family:var(--ui);box-sizing:border-box;
    width:320px;height:190px;border-radius:18px;padding:20px;
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
</style>
"""
CARDS = [("quick-links", "link-external", "Quick Links",
          "Codes, Pitkin County, City of Aspen"),
         # The Templates page. Blurbs name what is actually in 02 Templates
         # rather than describing the app -- nobody needs telling what Docs is.
         ("google-docs",   "ft-doc",    "Google Docs",
          "Transmittals, minutes, RFIs, proposals"),
         ("google-slides", "gs-slides", "Google Slides",
          "Client presentations, design reviews"),
         ("google-sheets", "gs-sheets", "Google Sheets",
          "Submittal logs, punch lists, fee schedules")]

async def cards(b):
    pg = await b.new_page(viewport={"width": 900, "height": 400}, device_scale_factor=3)
    for tone in ("white", "navy"):
        for slug, ic, title, blurb in CARDS:
            html = CARD_CSS + ('<div class="wrap"><div class="card %s" id="t">'
                               '<div class="chip">%s</div>'
                               '<div class="ttl">%s</div><div class="blurb">%s</div>'
                               '<div class="arw">Open &#8599;</div></div></div>'
                               % (tone, icon(ic), title, blurb))
            await pg.set_content(html, wait_until="load")
            await pg.wait_for_timeout(450)
            await pg.locator("#t").screenshot(
                path="%s/card-%s-%s.png" % (BTN, slug, tone), omit_background=True)
            print("card-%s-%s.png" % (slug, tone))
    await pg.close()

async def main():
    os.makedirs(HERE, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox", "--allow-file-access-from-files"])
        await banners(b); await pills(b); await cards(b)
        await b.close()

asyncio.run(main())
