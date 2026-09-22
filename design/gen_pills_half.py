"""Pills built to the card's width, so sizing becomes an alignment job.

Every previous attempt set a width in the file and asked for it to survive
the drop. It does not -- the live page put 220px files on screen at the
equivalent of 131. So the target moves from a number to an edge: make each
pill exactly as wide as the card beneath it, and Sites' own alignment
guides snap it there.

That forces the shape. At 320 wide a 42-tall pill would be chunky, so the
proportions are re-cut for the width: 46 tall, 7:1, with the label centred
in the extra room rather than stretched into it.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/icon_svg.json"))

# Half a card. 12.25 is the largest type that still leaves the longest
# label real padding in 160px -- at a card's full width there was room to
# spare, at half there is not.
W, H, FS, IC, GAP = 160, 38, 12.25, 14.6, 8
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
  gap:%.1fpx;width:%dpx;height:%dpx;border-radius:999px;white-space:nowrap;
  font:600 %.2fpx var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:%.1fpx;height:%.1fpx;fill:none;stroke-width:1.9;
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
        pg = await b.new_page(viewport={"width": 700, "height": 200}, device_scale_factor=3)
        for tone in ("white", "navy"):
            for slug, ic, label in LABELS:
                await pg.set_content(CSS + ('<div class="wrap"><div class="pill %s" id="t">'
                    '<svg viewBox="0 0 24 24">%s</svg>%s</div></div>' % (tone, SVG[ic], label)),
                    wait_until="load")
                await pg.wait_for_timeout(350)
                await pg.locator("#t").screenshot(
                    path="%s/half-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()
    from PIL import Image
    im = Image.open("%s/half-%s-white.png" % (OUT, LABELS[0][0]))
    print("canvas %dx%d  ratio %.2f:1" % (im.width, im.height, im.width / im.height))
    print("over a 417px card, half is 208 wide -> %.0fpx tall" % (208 * im.height / im.width))
asyncio.run(main())
