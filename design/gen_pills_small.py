"""A tighter pill for the home row.

The row- set was 198x50 with 27px of padding each side, which made every
button chunky at any width that kept the type readable. This one drops the
height to 42 and the padding to 18, so the same drag width gives a shorter
button with LARGER type -- text size is set by width/canvas-width, and a
narrower canvas raises that ratio.

Canvas width is the longest label's own natural width, measured rather than
guessed, so equal width still gives equal height across the set.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open(os.path.dirname(os.path.abspath(__file__)) + "/icon_svg.json"))

H, PAD, FS, IC, GAP = 42, 18, 13, 15.5, 8.5
LABELS = [("staff-directory", "directory", "Staff Directory"),
          ("signup-present",  "calendar",  "Sign up to present"),
          ("it-issue",        "tool",      "IT issue"),
          ("expense",         "ft-sheet",  "Expense")]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  box-sizing:border-box;display:%DISP%;align-items:center;justify-content:center;
  gap:%GAPpx;height:%Hpx;border-radius:999px;white-space:nowrap;
  font:600 %FSpx var(--ui);font-family:var(--ui)}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill.navy{background:#022049;color:#fff}
 .pill svg{width:%ICpx;height:%ICpx;fill:none;stroke-width:1.9;
   stroke-linecap:round;stroke-linejoin:round;flex:none}
 .pill.white svg{stroke:#022049}
 .pill.navy svg{stroke:#fff}
</style>
"""
def css(disp):
    return (CSS.replace("%DISP%", disp).replace("%H", str(H)).replace("%FS", str(FS))
               .replace("%IC", str(IC)).replace("%GAP", str(GAP)))

def markup(ic, label, tone, style=""):
    return ('<div class="wrap"><div class="pill %s" id="t" style="%s">'
            '<svg viewBox="0 0 24 24">%s</svg>%s</div></div>'
            % (tone, style, SVG[ic], label))

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 700, "height": 200}, device_scale_factor=3)

        # Measure: let each pill hug its label, then take the widest.
        widest = 0
        for slug, ic, label in LABELS:
            await pg.set_content(css("inline-flex") + markup(
                ic, label, "white", "padding:0 %dpx" % PAD), wait_until="load")
            await pg.wait_for_timeout(320)
            box = await pg.locator("#t").bounding_box()
            print("%-18s natural %6.1f" % (slug, box["width"]))
            widest = max(widest, box["width"])
        W = round(widest)

        for tone in ("white", "navy"):
            for slug, ic, label in LABELS:
                await pg.set_content(css("flex") + markup(
                    ic, label, tone, "width:%dpx" % W), wait_until="load")
                await pg.wait_for_timeout(320)
                await pg.locator("#t").screenshot(
                    path="%s/pill-%s-%s.png" % (OUT, slug, tone), omit_background=True)
        await b.close()

    from PIL import Image
    im = Image.open("%s/pill-expense-white.png" % OUT)
    print("\ncanvas %dx%d  ratio %.2f:1" % (im.width, im.height, im.width / im.height))
    for w in (160, 180, 200):
        print("  at %dpx wide -> %.0fpx tall, type reads ~%.1fpx"
              % (w, w * im.height / im.width, FS * w / W))
asyncio.run(main())
