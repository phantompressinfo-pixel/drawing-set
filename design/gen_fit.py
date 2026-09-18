"""Content-width buttons: the pill hugs its label instead of every button
sharing one canvas. Heights still match, because every canvas is 50px tall."""
import asyncio, json, os
from playwright.async_api import async_playwright
OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open("icon_svg.json"))
LABELS = [("time-off","ft-form","Time off"), ("it-issue","tool","IT issue"),
          ("new-project","templates","New project"), ("expense","ft-sheet","Expense"),
          ("signup-present","calendar","Sign up to present")]
CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  box-sizing:border-box;display:inline-flex;align-items:center;gap:9px;
  height:50px;padding:0 26px;border-radius:999px;white-space:nowrap;
  font:600 13.5px var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:16px;height:16px;fill:none;stroke-width:1.9;
   stroke-linecap:round;stroke-linejoin:round;flex:none}
 .pill.white svg{stroke:#022049}
 .pill.navy svg{stroke:#fff}
</style>
"""
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":700,"height":200}, device_scale_factor=3)
        for tone in ("white","navy"):
            for slug, ic, label in LABELS:
                html = CSS + ('<div class="wrap"><div class="pill %s" id="t">'
                              '<svg viewBox="0 0 24 24">%s</svg>%s</div></div>'
                              % (tone, SVG[ic], label))
                await pg.set_content(html, wait_until="load")
                await pg.wait_for_timeout(320)
                await pg.locator("#t").screenshot(
                    path="%s/fit-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()
    from PIL import Image
    for slug,_,_ in LABELS:
        im = Image.open("%s/fit-%s-white.png" % (OUT, slug))
        print("fit-%-16s %4dx%-4d ratio %.2f:1" % (slug, im.width, im.height, im.width/im.height))
asyncio.run(main())
