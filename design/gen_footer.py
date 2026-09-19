"""The footer bar: a hairline rule, the firm name, and a use notice.

Transparent PNG so it sits on the charcoal band or the navy one without a
seam. Drawn 1000px wide -- the width of the Sites content column -- and cut
at 3x, so dropping it at full column width lands it at 1:1.
"""
import asyncio
from playwright.async_api import async_playwright
OUT = "/home/user/drawing-set/google-sites/footer"
W = 1000
HEAD = """<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;700&display=swap" rel="stylesheet">
<style>
 :root{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif}
 html,body{margin:0;padding:0;background:transparent}
 .bar{box-sizing:border-box;width:%dpx;padding-top:1px}
 .rule{height:1px;background:%s}
 .row{display:flex;align-items:baseline;justify-content:space-between;padding:20px 0 6px}
 .n{font:700 12px var(--ui);font-family:var(--ui);letter-spacing:.14em;
    text-transform:uppercase;color:%s}
 .m{font:500 11px var(--ui);font-family:var(--ui);color:%s}
</style>"""
# (rule, name colour, notice colour) for a bar sitting on a dark band
TONES = {"light": ("rgba(255,255,255,.16)", "#ffffff", "#a8aeb7"),
         "dark":  ("rgba(2,32,73,.18)",     "#022049", "#6b7280")}

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": W + 80, "height": 200},
                              device_scale_factor=3)
        for tone, (rule, name, note) in TONES.items():
            html = (HEAD % (W, rule, name, note)) + (
                '<div class="bar" id="t"><div class="rule"></div><div class="row">'
                '<div class="n">Eigelberger Architecture &amp; Design</div>'
                '<div class="m">Internal use only</div></div></div>')
            await pg.set_content(html, wait_until="load")
            await pg.wait_for_timeout(400)
            await pg.locator("#t").screenshot(
                path="%s/footer-bar-%s.png" % (OUT, tone), omit_background=True)
        await b.close()
    from PIL import Image
    for tone in TONES:
        im = Image.open("%s/footer-bar-%s.png" % (OUT, tone))
        print("footer-bar-%-6s %dx%-4d -> drop at %dpx wide" % (tone, im.width, im.height, W))
asyncio.run(main())
