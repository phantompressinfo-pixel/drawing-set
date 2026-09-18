"""Action buttons, uniform width, three heights.

Sites scales an inserted image proportionally, so the only way to get a
shorter button at a given width is to make the image itself proportionally
wider. Same pill, three canvas ratios -- pick the one whose height lands
where you want it. Uniform width also makes the five line up in a row
instead of stepping in and out with the length of the label.
"""
import asyncio, json, os
from playwright.async_api import async_playwright

OUT = "/home/user/drawing-set/google-sites/buttons"
SVG = json.load(open("icon_svg.json"))

LABELS = [
    ("time-off",        "ft-form",   "Time off"),
    ("it-issue",        "tool",      "IT issue"),
    ("new-project",     "templates", "New project"),
    ("expense",         "ft-sheet",  "Expense"),
    # four ways of saying what the Learning Sessions button actually does
    ("present-session", "calendar",  "Present a session"),
    ("signup-present",  "calendar",  "Sign up to present"),
    ("teach-session",   "learning",  "Teach a session"),
    ("claim-week",      "calendar",  "Claim a week"),
]
# name, css width, css height  ->  ratio decides how tall it lands in Sites
HEIGHTS = [("tall", 260, 62), ("medium", 260, 50), ("slim", 260, 42)]

CSS = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap" rel="stylesheet">
<style>
 html,body{margin:0;padding:0;background:transparent}
 .wrap{display:inline-block;padding:6px}
 .pill{--ui:'Montserrat',-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
   box-sizing:border-box;display:flex;align-items:center;justify-content:center;
   gap:9px;border-radius:999px;white-space:nowrap;font-family:var(--ui)}
 .pill.navy {background:#022049;color:#fff}
 .pill.white{background:#fff;color:#022049;border:1.5px solid #D5DCE4}
 .pill svg{fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;flex:none}
 .pill.navy  svg{stroke:#fff}
 .pill.white svg{stroke:#022049}
</style>
"""

def html(ic, label, tone, w, h):
    fs = 15 if h >= 60 else (13.5 if h >= 50 else 12.5)
    isz = 18 if h >= 60 else (16 if h >= 50 else 14)
    return (CSS + '<div class="wrap"><div class="pill %s" id="t" '
            'style="width:%dpx;height:%dpx;font-size:%.1fpx;font-weight:600">'
            '<svg viewBox="0 0 24 24" style="width:%dpx;height:%dpx">%s</svg>%s'
            '</div></div>' % (tone, w, h, fs, isz, isz, SVG[ic], label))

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox"])
        pg = await b.new_page(viewport={"width": 700, "height": 220}, device_scale_factor=3)
        n = 0
        for hname, w, h in HEIGHTS:
            for tone in ("white", "navy"):
                for slug, ic, label in LABELS:
                    await pg.set_content(html(ic, label, tone, w, h), wait_until="load")
                    await pg.wait_for_timeout(320)
                    await pg.locator("#t").screenshot(
                        path="%s/btn-%s-%s-%s.png" % (OUT, slug, tone, hname),
                        omit_background=True)
                    n += 1
        await b.close()
    print(n, "buttons")
    for hname, w, h in HEIGHTS:
        # at a 1000px content column, five across with 12px gaps
        disp = (1000 - 4*12) / 5
        print("  %-7s canvas %dx%-3d ratio %.1f:1  -> %.0fpx wide lands %.0fpx tall"
              % (hname, w, h, w/h, disp, disp*h/w))

asyncio.run(main())
