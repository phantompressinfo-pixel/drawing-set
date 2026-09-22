"""Quick Links as images: one image per destination.

A single image per column would give the whole column one link, since Sites
has no image maps -- so every link is its own card, placed and linked
individually. Cards rather than the mockup's plain text: on a page whose
whole job is leaving the site, the things you can click should look like
things you can click.
"""
import asyncio, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/quicklinks"
W, H = 320, 100          # drag to 300 -> three across fits the 1000 column

GROUPS = [
 ("codes", "Codes", [
   ("icc",     "ICC Digital I-Codes",            "codes.iccsafe.org",       ""),
   ("wildfire","Colorado Wildfire Resiliency Code","dfpc.colorado.gov",      ""),
   ("energy",  "Colorado Building Energy Codes",  "energyoffice.colorado.gov",""),
 ]),
 ("pitkin", "Pitkin County", [
   ("comdev",  "Community Development",          "pitkincounty.com",        ""),
   ("code",    "County Code: Title 8 — Land Use","pitkincounty.com",    ""),
   ("permits", "Permitting — SagesGov",     "sagesgov.com",            "personal login"),
   ("gis",     "GIS — Maps & More",        "pitkincounty.com",        ""),
 ]),
 # The only internal group. Its second line names what is inside rather
 # than a domain -- there is no domain to warn anyone about, and "what
 # will I find" is the more useful thing to say about our own document.
 ("ead", "EAD", [
   ("office",  "EAD Office Information",         "Address, hours, wifi, printers", ""),
 ]),
 ("aspen", "City of Aspen", [
   ("comdev",  "Community Development",          "aspen.gov",               ""),
   ("code",    "Municipal Code: Title 26 — Land Use","library.municode.com",""),
   ("permits", "Permitting — Salesforce",   "cityofaspen.my.site.com", "personal login"),
 ]),
]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .card{--ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
   font-family:var(--ui);box-sizing:border-box;width:%dpx;height:%dpx;
   background:#fff;border:1.5px solid #D5DCE4;border-radius:14px;
   padding:16px 18px;display:flex;flex-direction:column;justify-content:center;
   position:relative}
 .ttl{font:700 14px/1.3 var(--ui);color:#022049;padding-right:22px}
 .dom{font:400 11.5px var(--ui);color:#6B7280;margin-top:6px}
 .tag{align-self:flex-start;margin-top:8px;padding:2px 8px;border-radius:999px;
   background:#FDF3E2;color:#8A6417;font:600 10px var(--ui);letter-spacing:.04em}
 .arw{position:absolute;right:15px;top:13px;font:600 13px var(--ui);color:#022049;opacity:.5}
 /* Group heading: caps, hairline rule, sits straight on the navy. */
 .head{--ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
   font-family:var(--ui);box-sizing:border-box;width:%dpx;padding-bottom:10px;
   border-bottom:2px solid rgba(255,255,255,.45)}
 .head span{font:700 12px var(--ui);letter-spacing:.16em;text-transform:uppercase;color:#fff}
</style>
""" % (W, H, W)

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 700, "height": 300}, device_scale_factor=3)
        made = 0
        for gslug, gname, rows in GROUPS:
            await pg.set_content(CSS + '<div class="wrap"><div class="head" id="t">'
                                 '<span>%s</span></div></div>' % gname, wait_until="load")
            await pg.wait_for_timeout(350)
            await pg.locator("#t").screenshot(
                path="%s/head-%s.png" % (OUT, gslug), omit_background=True)
            made += 1
            for slug, title, dom, note in rows:
                tag = '<div class="tag">%s</div>' % note if note else ""
                await pg.set_content(CSS + ('<div class="wrap"><div class="card" id="t">'
                    '<div class="arw">&#8599;</div><div class="ttl">%s</div>'
                    '<div class="dom">%s</div>%s</div></div>' % (title, dom, tag)),
                    wait_until="load")
                await pg.wait_for_timeout(350)
                await pg.locator("#t").screenshot(
                    path="%s/%s-%s.png" % (OUT, gslug, slug), omit_background=True)
                made += 1
        await b.close()
    print(made, "images ->", OUT)
asyncio.run(main())
