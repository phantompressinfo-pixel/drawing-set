"""Page-banner options for the Sites header. 2560x800, full-bleed."""
import asyncio, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/banners"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/bnr"
W, H = 1280, 400          # drawn at 1280x400, captured at 2x -> 2560x800

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
 :root{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
 *{box-sizing:border-box;margin:0;padding:0}
 body{width:1280px;height:400px;overflow:hidden;font-family:var(--ui);color:#fff}
 .bn{width:1280px;height:400px;background-size:cover;background-position:center;
     display:flex;padding:0 96px;position:relative}
 .mid{margin:auto 0}
 /* the firm name, set as type -- swap for the real logo artwork */
 .mark{font:500 25px var(--ui);letter-spacing:9px;white-space:nowrap}
 .mark .thin{display:block;font:300 11.5px var(--ui);letter-spacing:6.2px;
             margin-top:9px;color:#AFC6E2}
 .hub{font:700 62px/1 var(--ui);letter-spacing:-1.4px;margin-top:22px}
 .hubwide{font:600 40px/1 var(--ui);letter-spacing:13px}
 .rule{height:1px;background:rgba(255,255,255,.34);margin:22px 0}
 .centre{text-align:center;align-items:center;justify-content:center;flex-direction:column}
 .plate{border:1px solid rgba(255,255,255,.38);padding:38px 58px;text-align:center}
 .vrule{width:1px;background:rgba(255,255,255,.3);margin:0 46px}
 .row{display:flex;align-items:center;margin:auto 0}
 .sub{font:400 15px var(--ui);color:#C6D6E8;margin-top:14px}
 .huge{font:700 110px/.92 var(--ui);letter-spacing:-3px}
</style>
"""

def page(bg, inner, cls=""):
    return CSS + '<div class="bn %s" style="background-image:url(\'bg/%s\')">%s</div>' % (cls, bg, inner)

MARK = '<div class="mark">EIGELBERGER<span class="thin">ARCHITECTURE &amp; DESIGN</span></div>'

BANNERS = {
 # D on the drafting grid
 "D-split-grid": page("banner-3-navy-grid.jpg",
    '<div class="row">%s<div class="vrule" style="height:96px"></div>'
    '<div><div class="hubwide" style="font-size:34px">OFFICE HUB</div>'
    '<div class="sub">Everything the office needs, in one place.</div></div></div>' % MARK),

 # D on the grid with a little light in the corner
 "D-split-grid-bloom": page("banner-4-navy-grid-bloom.jpg",
    '<div class="row">%s<div class="vrule" style="height:96px"></div>'
    '<div><div class="hubwide" style="font-size:34px">OFFICE HUB</div>'
    '<div class="sub">Everything the office needs, in one place.</div></div></div>' % MARK),

 # A — firm name, then Office Hub beneath. Left aligned, contour field.
 "A-stacked-left": page("bg-4-navy-contour.jpg",
    '<div class="mid">%s<div class="hub">Office&nbsp;Hub</div></div>' % MARK),

 # B — centred, hairline rule between the two
 "B-centred-rule": page("banner-1-navy-bloom.jpg",
    '<div class="mid" style="width:100%%;text-align:center">%s<div class="rule" '
    'style="width:360px;margin-left:auto;margin-right:auto"></div>'
    '<div class="hubwide">OFFICE HUB</div></div>' % MARK, "centre"),

 # C — HUB as the whole statement
 "C-big-hub": page("banner-3-navy-grid.jpg",
    '<div class="mid">%s<div class="huge">HUB</div></div>' % MARK),

 # D — firm name and Hub side by side, divided
 "D-split-rule": page("bg-5-navy-fade.jpg",
    '<div class="row">%s<div class="vrule" style="height:96px"></div>'
    '<div><div class="hubwide" style="font-size:34px">OFFICE HUB</div>'
    '<div class="sub">Everything the office needs, in one place.</div></div></div>' % MARK),

 # E — ruled plate, the most formal of the set
 "E-plate": page("bg-1-navy-solid.jpg",
    '<div class="plate">%s<div class="rule" style="margin:20px 0"></div>'
    '<div class="hubwide" style="font-size:30px">OFFICE HUB</div></div>', "centre"),

 # F — quiet: name small at top, Hub large, lots of air
 "F-quiet": page("bg-2-navy-bloom.jpg",
    '<div class="mid">%s<div class="hub" style="font-size:54px">Office Hub</div>'
    '<div class="sub">Standards, templates, forms and SOPs</div></div>' % MARK),
}
BANNERS["E-plate"] = BANNERS["E-plate"].replace("%s", MARK)

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox", "--allow-file-access-from-files"])
        for name, html in BANNERS.items():
            p = os.path.join(HERE, "_%s.html" % name)
            open(p, "w").write(html)
            pg = await b.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
            await pg.goto("file://" + p, wait_until="networkidle")
            await pg.wait_for_timeout(1200)
            bad = await pg.evaluate("[...document.images].filter(i=>!i.naturalWidth).length")
            await pg.screenshot(path="%s/banner-%s.jpg" % (OUT, name), quality=92, type="jpeg")
            print("%-18s broken:%d" % (name, bad))
            await pg.close()
        await b.close()

asyncio.run(main())
