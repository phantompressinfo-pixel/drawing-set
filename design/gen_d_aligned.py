import asyncio, os
from playwright.async_api import async_playwright
OUT  = "/home/user/drawing-set/google-sites/banners"
HERE = os.path.dirname(os.path.abspath(__file__)) + "/bnr"

CSS = """
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
MARK = '<div class="mark">EIGELBERGER<span class="thin">ARCHITECTURE &amp; DESIGN</span></div>'
BODY = ('<div class="row">%s<div class="vrule"></div><div>'
        '<div class="hubwide">OFFICE HUB</div>'
        '<div class="sub">Everything the office needs, in one place.</div>'
        '</div></div>' % MARK)

VARIANTS = {
  "D-grid-flat":   "grid-banner-flat.jpg",
  "D-grid-bloom":  "grid-banner-bloom.jpg",
  "D-cols-flat":   "cols-banner-flat.jpg",
  "D-cols-bloom":  "cols-banner-bloom.jpg",
}

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox", "--allow-file-access-from-files"])
        for name, bg in VARIANTS.items():
            html = CSS + '<div class="bn" style="background-image:url(\'bg/%s\')">%s</div>' % (bg, BODY)
            p = os.path.join(HERE, "_%s.html" % name)
            open(p, "w").write(html)
            pg = await b.new_page(viewport={"width": 1280, "height": 500}, device_scale_factor=2)
            await pg.goto("file://" + p, wait_until="networkidle")
            await pg.wait_for_timeout(1100)
            await pg.screenshot(path="%s/banner-%s.jpg" % (OUT, name), quality=92, type="jpeg")
            print(name, "ok")
            await pg.close()
        await b.close()
asyncio.run(main())
