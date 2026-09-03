import asyncio, glob, os
from playwright.async_api import async_playwright
SRC="/home/user/drawing-set/google-sites/embeds"; os.makedirs("shots",exist_ok=True)
async def main():
    async with async_playwright() as pw:
        b=await pw.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",args=["--no-sandbox"])
        errs=[]
        for f in sorted(glob.glob(SRC+"/dashboard-*.html")):
            n=os.path.basename(f).replace(".html","")
            pg=await b.new_page(viewport={"width":1000,"height":900},device_scale_factor=2)
            pg.on("pageerror", lambda e,n=n: errs.append((n,str(e))))
            await pg.set_content("<body style='margin:0;background:#fff'>"+open(f).read()+"</body>",wait_until="load")
            await pg.wait_for_timeout(1200)
            h=await pg.evaluate("document.getElementById('ead').scrollHeight")
            await pg.set_viewport_size({"width":1000,"height":int(h)+4})
            await pg.wait_for_timeout(250)
            await pg.screenshot(path="shots/%s.png"%n)
            print("%-42s %4dpx" % (n,h)); await pg.close()
        await b.close()
        for e in errs: print("PAGEERROR",e)
        print("js errors:",len(errs))
asyncio.run(main())
