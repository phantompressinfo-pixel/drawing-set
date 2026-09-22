"""The home-row pills at their intended display size, 1:1.

Sites places an image at its intrinsic pixel size, so a file cut at exactly
220x51 lands at 220x51 with nothing to drag -- which is the whole point,
since every sizing problem on this page has come from dragging by eye.

220 is the midpoint of what the live page had: 130px on two pills and 317
on the third. Geometry is the pill- set scaled 220/180.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/icon_svg.json"))

K = 220 / 180.0                      # scale from the pill- design
H, FS, IC, GAP = 42 * K, 13 * K, 15.5 * K, 8.5 * K
W = 220

LABELS = [("staff-directory",   "directory", "Staff Directory"),
          ("signup-present",    "calendar",  "Sign up to present"),
          ("drawing-standards", "ft-pdf",    "Drawing Standards")]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  box-sizing:border-box;display:flex;align-items:center;justify-content:center;
  gap:%.2fpx;width:%dpx;height:%.2fpx;border-radius:999px;white-space:nowrap;
  font:600 %.2fpx var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.8px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:%.2fpx;height:%.2fpx;fill:none;stroke-width:1.9;
   stroke-linecap:round;stroke-linejoin:round;flex:none}
 .pill.white svg{stroke:#022049}
 .pill.navy svg{stroke:#fff}
</style>
""" % (GAP, W, H, FS, IC, IC)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 600, "height": 200}, device_scale_factor=1)
        for tone in ("white", "navy"):
            for slug, ic, label in LABELS:
                await pg.set_content(CSS + ('<div class="wrap"><div class="pill %s" id="t">'
                    '<svg viewBox="0 0 24 24">%s</svg>%s</div></div>' % (tone, SVG[ic], label)),
                    wait_until="load")
                await pg.wait_for_timeout(350)
                await pg.locator("#t").screenshot(
                    path="%s/drop-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()
    from PIL import Image
    for slug, _, _ in LABELS:
        im = Image.open("%s/drop-%s-white.png" % (OUT, slug))
        print("drop-%-19s %dx%d" % (slug, im.width, im.height))
asyncio.run(main())
