"""Three full-page layouts, assembled only from things Sites can actually do:
full-bleed section backgrounds, a 1000px content column, image buttons, text."""
import asyncio, os
from playwright.async_api import async_playwright

BG  = "bg"
BTN = "btn"
OUT = "/tmp/claude-0/-home-user-drawing-set/4abccc73-5df9-5ad5-9792-19a3f012db48/scratchpad/native"

SECTIONS = ["office-standards","templates","forms","office-policies",
            "sops","revit-standards","learning-sessions","staff-directory"]
PILLS = ["time-off","it-issue","new-project","expense","sign-up"]

BASE = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
 *{box-sizing:border-box;margin:0;padding:0}
 body{font-family:'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;background:#fff}
 /* the slim bar Google keeps at the top of every published page */
 .chrome{height:58px;background:#fff;border-bottom:1px solid #E4E8ED;
   display:flex;align-items:center;gap:30px;padding:0 34px;
   font:600 13.5px 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;color:#3C4550}
 .chrome .nm{font-weight:700;color:#022049;font-size:15px;margin-right:12px}
 .chrome a{color:#5A6470;text-decoration:none}
 .sec{width:100%;background-size:cover;background-position:center}
 .col{max-width:1000px;margin:0 auto;padding:0 20px}
 .eyebrow{font:600 11px 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;letter-spacing:2.2px}
 h1{font:700 44px/1.1 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;letter-spacing:-.8px}
 h2{font:700 22px/1.2 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;letter-spacing:-.2px}
 .lede{font:400 16px/1.6 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif}
 .cards{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
 .cards img{width:100%;display:block}
 .pills{display:flex;gap:12px;flex-wrap:wrap}
 .pills img{height:52px}
 .drive{background:#fff;border:1px solid #DDE2E8;border-radius:10px;overflow:hidden}
 .drive .hd{background:#F5F7F9;border-bottom:1px solid #E4E8ED;padding:11px 16px;
   font:600 12px 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;color:#5A6470;letter-spacing:.4px}
 .drive .row{display:flex;align-items:center;gap:12px;padding:11px 16px;
   border-bottom:1px solid #EEF1F4;font:400 13.5px 'Montserrat',-apple-system,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;color:#33404E}
 .drive .row:last-child{border-bottom:0}
 .dot{width:16px;height:20px;border-radius:2px;background:#C9D2DC;flex:none}
 .muted{color:#7C8794;margin-left:auto;font-size:12px}
</style>
"""

CHROME = ('<div class="chrome"><span class="nm">EAD Office Hub</span>'
          '<a>Main Home</a><a>Employee Center</a><a>Office Hub</a></div>')

def cards(tone, n=8):
    return '<div class="cards">' + "".join(
        '<img src="%s/card-%s-%s.png">' % (BTN, s, tone) for s in SECTIONS[:n]) + '</div>'

def pills(tone):
    return '<div class="pills">' + "".join(
        '<img src="%s/button-%s-%s.png">' % (BTN, p, tone) for p in PILLS) + '</div>'

DRIVE = """
<div class="drive">
  <div class="hd">OFFICE STANDARDS &nbsp;&middot;&nbsp; LIVE FROM DRIVE</div>
  <div class="row"><div class="dot"></div>Drafting &amp; CAD Standards.pdf<span class="muted">Jun 1</span></div>
  <div class="row"><div class="dot"></div>File Naming Convention.pdf<span class="muted">May 20</span></div>
  <div class="row"><div class="dot"></div>Sheet Numbering Standard.pdf<span class="muted">May 2</span></div>
  <div class="row"><div class="dot"></div>Deliverable Standards<span class="muted">Apr 28</span></div>
</div>
"""

# ---------------------------------------------------------------- A
A = CHROME + f"""
<div class="sec" style="background-image:url('{BG}/banner-1-navy-bloom.jpg')">
  <div class="col" style="padding-top:64px;padding-bottom:64px;color:#fff">
    <div class="eyebrow" style="color:#9DB8D8">EIGELBERGER ARCHITECTURE &amp; DESIGN</div>
    <h1 style="margin-top:14px">Office Hub</h1>
    <div class="lede" style="color:#C6D6E8;margin-top:12px;max-width:52ch">
      Everything the office needs, in one place.</div>
  </div>
</div>
<div class="sec" style="background:#fff">
  <div class="col" style="padding:52px 20px 20px">
    <h2 style="color:#022049">Sections</h2>
    <div style="height:22px"></div>{cards('navy')}
  </div>
</div>
<div class="sec" style="background:#F2F4F7;margin-top:46px">
  <div class="col" style="padding:38px 20px">
    <div class="eyebrow" style="color:#7C8794">QUICK ACTIONS</div>
    <div style="height:16px"></div>{pills('navy')}
  </div>
</div>
<div class="sec"><div class="col" style="padding:46px 20px 64px">{DRIVE}</div></div>
"""

# ---------------------------------------------------------------- B
B = CHROME + f"""
<div class="sec" style="background-image:url('{BG}/bg-4-navy-contour.jpg')">
  <div class="col" style="padding:60px 20px 70px;color:#fff">
    <div class="eyebrow" style="color:#9DB8D8">EIGELBERGER ARCHITECTURE &amp; DESIGN</div>
    <h1 style="margin-top:14px">Office Hub</h1>
    <div class="lede" style="color:#C6D6E8;margin-top:12px;max-width:52ch">
      Everything the office needs, in one place.</div>
    <div style="height:34px"></div>{pills('white')}
    <div style="height:46px"></div>{cards('white')}
    <div style="height:56px"></div>
    <div class="eyebrow" style="color:#9DB8D8">EVERYTHING ELSE, STRAIGHT FROM DRIVE</div>
    <div style="height:16px"></div>{DRIVE}
  </div>
</div>
"""

# ---------------------------------------------------------------- C
C = CHROME + f"""
<div class="sec" style="background-image:url('{BG}/banner-3-navy-grid.jpg')">
  <div class="col" style="padding:56px 20px 58px;color:#fff">
    <div class="eyebrow" style="color:#9DB8D8">EIGELBERGER ARCHITECTURE &amp; DESIGN</div>
    <h1 style="margin-top:14px">Office Hub</h1>
  </div>
</div>
<div class="sec" style="background-image:url('{BG}/bg-6-paper-grid.jpg')">
  <div class="col" style="padding:48px 20px 54px">
    <h2 style="color:#022049">Sections</h2>
    <div style="height:20px"></div>{cards('navy')}
  </div>
</div>
<div class="sec" style="background-image:url('{BG}/bg-5-navy-fade.jpg')">
  <div class="col" style="padding:40px 20px">
    <div class="eyebrow" style="color:#9DB8D8">QUICK ACTIONS</div>
    <div style="height:16px"></div>{pills('white')}
  </div>
</div>
<div class="sec"><div class="col" style="padding:46px 20px 64px">{DRIVE}</div></div>
"""

async def main():
    os.makedirs(OUT, exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch(
            executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
            args=["--no-sandbox", "--allow-file-access-from-files"])
        for name, html in (("A-banner-light", A), ("B-full-navy", B), ("C-banded", C)):
            path = "%s/_%s.html" % (OUT, name)
            open(path, "w").write(BASE + html)
            pg = await b.new_page(viewport={"width": 1440, "height": 1000}, device_scale_factor=2)
            await pg.goto("file://" + os.path.abspath(path), wait_until="networkidle")
            await pg.wait_for_timeout(1500)
            missing = await pg.evaluate(
                "[...document.images].filter(i=>!i.naturalWidth).length")
            print("   broken images:", missing)
            await pg.screenshot(path="%s/layout-%s.png" % (OUT, name), full_page=True)
            h = await pg.evaluate("document.body.scrollHeight")
            print("%-16s %d px tall" % (name, h))
            await pg.close()
        await b.close()

asyncio.run(main())
