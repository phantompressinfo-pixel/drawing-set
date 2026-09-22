"""The long pill: 320x46, the geometry the home row is actually using.

Kept as its own script because the half-card cut lives in gen_pills_half.py
and the two are easy to confuse -- on the live page Office Information came
out 62px tall against 39 on the other three, which is exactly what mixing
the two sets looks like.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/icon_svg.json"))

W, H, FS, IC, GAP = 320, 46, 14, 17, 9
LABELS = [("office-information","home",      "Office Information"),
          ("staff-directory",   "directory", "Staff Directory"),
          ("signup-present",    "calendar",  "Sign up to present"),
          ("drawing-standards", "ft-pdf",    "Drawing Standards")]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  box-sizing:border-box;display:flex;align-items:center;justify-content:center;
  gap:%dpx;width:%dpx;height:%dpx;border-radius:999px;white-space:nowrap;
  font:600 %dpx var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:%dpx;height:%dpx;fill:none;stroke-width:1.9;
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
                    path="%s/wide-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()
    from PIL import Image
    import numpy as np
    for slug, _, _ in LABELS:
        a = np.array(Image.open("%s/wide-%s-white.png" % (OUT, slug)).convert("RGBA"))
        ink = (a[:, :, 3] > 80) & (a[:, :, 0] < 120) & (a[:, :, 2] > 60)
        xs = np.where(ink)[1]
        print("wide-%-19s %dx%-4d padding %d / %d"
              % (slug, a.shape[1], a.shape[0], xs.min() / 3, (a.shape[1] - 1 - xs.max()) / 3))
asyncio.run(main())
