"""Two shapes for the single-page dashboard. Cards link into Drive folders."""
import json, os, re
SVG = json.load(open("icon_svg.json"))
OUT = "/home/user/drawing-set/google-sites/embeds"

SECTIONS = [
    ("Office Standards", "standards", "Drafting, CAD, file naming, deliverables"),
    ("Templates",        "templates", "Title blocks, minutes, transmittals, RFIs"),
    ("Forms",            "forms",     "PTO, expenses, IT support, onboarding"),
    ("Office Policies",  "policies",  "Handbook, safety, remote work, IT use"),
    ("SOPs",             "sops",      "Kickoff, QA/QC, submittals, archiving"),
    ("Revit Standards",  "revit",     "Worksharing, families, views, LOD"),
    ("Learning Sessions","learning",  "Weekly knowledge share, filed by month"),
    ("Staff Directory",  "directory", "Roles, extensions, emergency contacts"),
]
START = [
    ("Office Standards Manual", "The one to read first", "ft-pdf"),
    ("Employee Handbook",       "Conduct, benefits, leave", "ft-pdf"),
    ("Sheet Title Block",       "Current office title block", "ft-doc"),
    ("PTO / Time-Off Request",  "Vacation, sick, personal", "ft-form"),
    ("Project Kickoff SOP",     "Numbering, folders, team setup", "ft-doc"),
    ("Model Setup & Worksharing","Revit central files and worksets", "ft-pdf"),
]
ACTIONS = [("Request time off","ft-form"), ("Report an IT issue","tool"),
           ("Start a new project","templates"), ("Submit an expense","ft-sheet"),
           ("Sign up to present","calendar")]

NEED = sorted(set(["search"] + [s[1] for s in SECTIONS] +
                  [s[2] for s in START] + [a[1] for a in ACTIONS]))
ICONS_JSON = json.dumps({k: SVG[k] for k in NEED}, indent=1)

CSS = """
#ead *{box-sizing:border-box;margin:0;padding:0}
#ead{
  display:flex; align-items:stretch; overflow:hidden;
  --ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-family:var(--ui); border-radius:16px; color:#fff;
  background:radial-gradient(120% 95% at 88% 2%, #1A4E8C 0%, rgba(26,78,140,0) 62%),#022049;
  -webkit-font-smoothing:antialiased;
}
#ead .main{flex:1;min-width:0;padding:30px 32px 34px}
#ead .hd{font:700 31px/1.15 var(--ui);letter-spacing:-.4px}
#ead .sb{margin-top:9px;font:400 15px/1.5 var(--ui);color:#C6D6E8;max-width:68ch}
#ead .lbl2{margin:30px 0 14px;font:400 10.5px var(--mono);color:#8FAAC9;letter-spacing:1.6px}

#ead .rail{flex:0 0 236px;background:#fff;color:#4B4B4B;padding:26px 0 22px;
  display:flex;flex-direction:column}
#ead .rail .brand{padding:0 22px}
#ead .rail .brand b{display:block;font:700 17px/1 var(--ui);color:#022049;letter-spacing:-.2px}
#ead .rail .brand span{display:block;margin-top:6px;font:400 10px var(--mono);
  color:#4B4B4B;letter-spacing:1.4px}
#ead .rail hr{border:0;border-top:1px solid #C9D1D6;margin:18px 22px}
#ead .rail .lbl{padding:0 22px;font:400 10px var(--mono);color:#788492;letter-spacing:1.4px}
#ead .rail nav{margin-top:10px;display:flex;flex-direction:column;gap:1px}
#ead .rail a{display:flex;align-items:center;gap:11px;margin:0 12px;padding:10px;
  border-radius:9px;text-decoration:none;color:#4B4B4B;font:500 13.5px var(--ui)}
#ead .rail a svg{width:17px;height:17px;stroke:#4B4B4B;fill:none;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round;flex:none}
#ead .rail a:hover{background:#022049;color:#fff}
#ead .rail a:hover svg{stroke:#fff}
#ead .rail .ask{margin-top:auto;padding:0 22px}
#ead .rail .ask hr{margin:18px 0}
#ead .rail .ask p{font:400 12.5px/1.45 var(--ui);color:#4B4B4B}
#ead .rail .ask b{display:block;margin-top:3px;font:700 12.5px var(--ui);color:#022049}

#ead .search{display:flex;align-items:center;gap:12px;background:#fff;
  border-radius:999px;padding:7px 7px 7px 20px;margin-top:22px}
#ead .search svg{width:19px;height:19px;stroke:#788492;fill:none;stroke-width:2;
  stroke-linecap:round;stroke-linejoin:round;flex:none}
#ead .search input{flex:1;border:0;outline:0;background:none;min-width:0;
  font:400 14px var(--mono);color:#022049}
#ead .search input::placeholder{color:#788492}
#ead .search button{border:0;cursor:pointer;background:#022049;color:#fff;
  border-radius:999px;padding:11px 26px;font:700 13px var(--ui);letter-spacing:.6px}
#ead .search button:hover{background:#0B3A72}

#ead .pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
#ead .pill{display:inline-flex;align-items:center;gap:9px;background:#fff;color:#022049;
  border-radius:999px;padding:11px 20px 11px 16px;font:600 13.5px var(--ui);
  text-decoration:none;transition:transform .12s,box-shadow .12s}
#ead .pill:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(0,0,0,.24)}
#ead .pill svg{width:17px;height:17px;stroke:#022049;fill:none;stroke-width:1.9;
  stroke-linecap:round;stroke-linejoin:round;flex:none}

#ead .grid{display:grid;gap:18px;grid-template-columns:repeat(auto-fit,minmax(212px,1fr))}
#ead .card{position:relative;display:flex;flex-direction:column;
  background:rgba(255,255,255,.10);
  -webkit-backdrop-filter:blur(18px) saturate(120%);
          backdrop-filter:blur(18px) saturate(120%);
  border:1px solid rgba(108,148,196,.55);border-radius:18px;padding:20px;
  text-decoration:none;color:inherit;min-height:186px;
  transition:background .15s,border-color .15s,transform .15s}
#ead .card:hover{background:rgba(255,255,255,.17);
  border-color:rgba(160,196,238,.85);transform:translateY(-2px)}
#ead .card.sm{min-height:0;flex-direction:row;align-items:center;gap:14px;padding:16px 18px}
#ead .chip{width:54px;height:54px;border-radius:14px;background:#fff;
  display:flex;align-items:center;justify-content:center;flex:none}
#ead .chip svg{width:26px;height:26px;stroke:#022049;fill:none;stroke-width:1.8;
  stroke-linecap:round;stroke-linejoin:round}
#ead .card.sm .chip{width:42px;height:42px;border-radius:11px;background:#2C588E}
#ead .card.sm .chip svg{width:20px;height:20px;stroke:#fff}
#ead .ttl{margin-top:16px;font:700 17.5px/1.28 var(--ui)}
#ead .card.sm .ttl{margin-top:0;font-size:15px}
#ead .blurb{margin-top:7px;font:400 13px/1.5 var(--ui);color:#BACEE6;flex:1}
#ead .card.sm .blurb{margin-top:3px;font-size:12.5px;flex:0}
#ead .foot{display:flex;justify-content:flex-end;margin-top:16px;
  font:500 11.5px var(--mono);color:#BACEE6;letter-spacing:.3px}
#ead .card:hover .foot{color:#fff}
"""

JS_COMMON = """
function svg(n){ return '<svg viewBox="0 0 24 24">'+(ICONS[n]||'')+'</svg>'; }
function esc(s){ return String(s).replace(/[&<>"]/g,function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

function headBlock(){
  return (CFG.title ? '<div class="hd">'+esc(CFG.title)+'</div>' : '')+
    (CFG.subtitle ? '<div class="sb">'+esc(CFG.subtitle)+'</div>' : '')+
    '<form class="search" target="_blank">'+svg('search')+
      '<input type="text" placeholder="Search standards, templates, forms, SOPs, Revit standards\\u2026">'+
      '<button type="submit">SEARCH</button></form>'+
    '<div class="pills">'+CFG.actions.map(function(a){
      return '<a class="pill" target="_top" href="'+esc(a.link)+'">'+svg(a.icon)+esc(a.label)+'</a>';
    }).join('')+'</div>';
}

function bigCards(list){
  return '<div class="grid">'+list.map(function(c){
    return '<a class="card" target="_blank" href="'+esc(c.link)+'">'+
      '<div class="chip">'+svg(c.icon)+'</div>'+
      '<div class="ttl">'+esc(c.title)+'</div>'+
      '<div class="blurb">'+esc(c.blurb)+'</div>'+
      '<div class="foot">Open \\u2197</div></a>';
  }).join('')+'</div>';
}

function smallCards(list){
  return '<div class="grid">'+list.map(function(c){
    return '<a class="card sm" target="_blank" href="'+esc(c.link)+'">'+
      '<div class="chip">'+svg(c.icon)+'</div><div>'+
      '<div class="ttl">'+esc(c.title)+'</div>'+
      '<div class="blurb">'+esc(c.blurb)+'</div></div></a>';
  }).join('')+'</div>';
}

function wire(host){
  var f = host.querySelector('.search');
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var q = f.querySelector('input').value.trim(); if(!q) return;
    var s = CFG.driveFolderId ? ('%20parent:'+CFG.driveFolderId) : '';
    window.open('https://drive.google.com/drive/search?q='+encodeURIComponent(q)+s,'_blank');
  });
}
"""

def cfg(sections, start=None):
    L = ['  driveFolderId: "",', '',
         '  title: "Office Hub",',
         '  subtitle: "Everything the office needs, in one place.",', '',
         '  actions: [']
    for label, icon in ACTIONS:
        L.append('    {label:%-23s icon:%-13s link:"" },' % (json.dumps(label)+',', json.dumps(icon)+','))
    L += ['  ],', '', '  /* Each card opens a Drive FOLDER. Paste the folder link. */',
          '  sections: [']
    for name, icon, blurb in sections:
        L += ['    {title:%s,' % json.dumps(name),
              '     icon:%s, blurb:%s,' % (json.dumps(icon), json.dumps(blurb)),
              '     link:""},']
    L.append('  ],')
    if start:
        L += ['', '  /* The handful of documents everyone opens. Paste FILE links. */',
              '  startHere: [']
        for name, blurb, icon in start:
            L += ['    {title:%s,' % json.dumps(name),
                  '     icon:%s, blurb:%s,' % (json.dumps(icon), json.dumps(blurb)),
                  '     link:""},']
        L.append('  ],')
    return "\n".join(L)


def build(name, header, config, render_js, rail):
    return """<!-- ==================================================================
     EAD OFFICE HUB  ·  %s
     Google Sites  >  Insert  >  Embed  >  Embed code  >  paste all of this
     ------------------------------------------------------------------
     TO EDIT: change only the CONFIG block. Paste Drive links between the
     quotes. Everything under "--- do not edit ---" is layout.
     ================================================================== -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<div id="ead"></div>

<script>
/* ===================== CONFIG — edit this part ===================== */
var CFG = {
%s
};
/* =================== --- do not edit below --- ==================== */

var CSS = `%s`;

var ICONS = %s;
%s
%s
(function(){
  var host = document.getElementById('ead');
  var st = document.createElement('style'); st.textContent = CSS;
  document.head.appendChild(st);
  host.innerHTML = %s;
  wire(host);
})();
</script>
""" % (header, config, CSS, ICONS_JSON, JS_COMMON, rail, render_js)


RAIL_JS = """
function rail(){
  return '<div class="rail">'+
    '<div class="brand"><b>EIGELBERGER</b><span>OFFICE HUB</span></div><hr>'+
    '<div class="lbl">SECTIONS</div><nav>'+
    CFG.sections.map(function(s){
      return '<a target="_blank" href="'+esc(s.link)+'">'+svg(s.icon)+
             '<span>'+esc(s.title)+'</span></a>';
    }).join('')+'</nav>'+
    '<div class="ask"><hr><p>Need something added?</p>'+
    '<b>Ask the office manager</b></div></div>';
}
"""

os.makedirs(OUT, exist_ok=True)

# ---- A: no rail, the eight section cards are the whole dashboard
a = build("DASHBOARD A - CARDS ONLY", "DASHBOARD A", cfg(SECTIONS), """
    '<div class="main">' + headBlock() +
    '<div class="lbl2">SECTIONS</div>' + bigCards(CFG.sections) + '</div>'
""", "")
open(os.path.join(OUT, "dashboard-A-cards-only.html"), "w").write(a)

# ---- B: rail carries the sections, main carries the everyday documents
b = build("DASHBOARD B - RAIL + START HERE", "DASHBOARD B", cfg(SECTIONS, START), """
    rail() + '<div class="main">' + headBlock() +
    '<div class="lbl2">START HERE</div>' + smallCards(CFG.startHere) + '</div>'
""", RAIL_JS)
open(os.path.join(OUT, "dashboard-B-rail-plus-start-here.html"), "w").write(b)

for f in ("dashboard-A-cards-only.html", "dashboard-B-rail-plus-start-here.html"):
    print("%-42s %6d chars" % (f, os.path.getsize(os.path.join(OUT, f))))
