"""One canvas ratio for all five, set by the LONGEST label.

Equal width then gives equal height, so dragging them all to the same width
-- the thing anyone would naturally do -- just works. And because the canvas
is only as wide as the longest label needs, the short labels sit in far less
empty space than they did on the 5.2:1 canvas.
"""
import asyncio, json, os
from playwright.async_api import async_playwright
OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open("icon_svg.json"))
LABELS = [("time-off","ft-form","Time off"), ("it-issue","tool","IT issue"),
          ("new-project","templates","New project"), ("expense","ft-sheet","Expense"),
          ("signup-present","calendar","Sign up to present")]
W, H = 198, 50          # 3.96:1 -- the natural ratio of the longest label
# Type, icon and gap are lifted verbatim from gen_fit.py, because
# fit-signup-present is the button the office signed off on. 198 is that
# button's own natural width, so row-signup-present comes out identical to
# it and every other label inherits its type size.
CSS = """
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
async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width":600,"height":200}, device_scale_factor=3)
        for tone in ("white","navy"):
            for slug, ic, label in LABELS:
                html = CSS + ('<div class="wrap"><div class="pill %s" id="t" '
                              'style="width:%dpx;height:%dpx">'
                              '<svg viewBox="0 0 24 24">%s</svg>%s</div></div>'
                              % (tone, W, H, SVG[ic], label))
                await pg.set_content(html, wait_until="load")
                await pg.wait_for_timeout(320)
                await pg.locator("#t").screenshot(
                    path="%s/row-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()
    from PIL import Image
    ws = []
    for slug,_,_ in LABELS:
        im = Image.open("%s/row-%s-white.png" % (OUT, slug))
        ws.append(im.width)
        print("row-%-16s %3dx%-3d ratio %.2f:1" % (slug, im.width, im.height, im.width/im.height))
    disp = 160
    print("\nall five at %dpx wide -> %.0fpx tall each, row = %dpx"
          % (disp, disp*Image.open("%s/row-time-off-white.png"%OUT).height
                   / Image.open("%s/row-time-off-white.png"%OUT).width,
             5*disp + 4*12))
asyncio.run(main())
