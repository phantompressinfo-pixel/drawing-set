import asyncio, glob, os, sys
from playwright.async_api import async_playwright

SRC = "/home/user/drawing-set/google-sites/embeds"
OUTD = "shots"; os.makedirs(OUTD, exist_ok=True)

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
                                     args=["--no-sandbox"])
        errs = []
        for f in sorted(glob.glob(SRC + "/*.html")):
            name = os.path.basename(f).replace(".html", "")
            for label, w in (("wide", 1000),):
                pg = await b.new_page(viewport={"width": w, "height": 900},
                                      device_scale_factor=2)
                pg.on("console", lambda m: errs.append((name, m.type, m.text))
                      if m.type == "error" else None)
                pg.on("pageerror", lambda e: errs.append((name, "pageerror", str(e))))
                # Sites drops the embed in a plain white iframe body
                await pg.set_content("<body style='margin:0;background:#fff'>" +
                                     open(f).read() + "</body>", wait_until="load")
                await pg.wait_for_timeout(1400)
                h = await pg.evaluate("document.getElementById('ead').scrollHeight")
                await pg.set_viewport_size({"width": w, "height": int(h) + 4})
                await pg.wait_for_timeout(300)
                await pg.screenshot(path="%s/%s_%s.png" % (OUTD, name, label))
                if label == "wide":
                    print("%-26s content height %4dpx" % (name, h))
                await pg.close()
        await b.close()
        for e in errs: print("ERROR", e)
        print("errors:", len(errs))

asyncio.run(main())
