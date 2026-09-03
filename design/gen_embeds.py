"""Emit paste-ready Google Sites 'Embed code' blocks for every Office Hub page."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_final import PAGES, SECTIONS, ACTIONS


# Two nav sections had no page in the approved render set. Same treatment,
# same card pattern -- sample contents, to be edited to match the real folders.
EXTRA_PAGES = [
    dict(i=5, title="Office Policies",
         sub="Handbook, safety, remote work, and acceptable-use policies.",
         kind="docs", items=[
             ("Employee Handbook", "Conduct, benefits, and leave", "PDF", "ft-pdf", "REQUIRED"),
             ("Health & Safety Policy", "Office and site-visit safety", "PDF", "ft-pdf", "REQUIRED"),
             ("Remote & Hybrid Work", "Eligibility and expectations", "Google Doc", "ft-doc", None),
             ("IT & Acceptable Use", "Devices, accounts, and data", "PDF", "ft-pdf", None),
             ("Travel & Expense Policy", "Limits, receipts, approvals", "PDF", "ft-pdf", "UPDATED")]),
    dict(i=9, title="Staff Directory",
         sub="Who does what, how to reach them, and who to call after hours.",
         kind="docs", items=[
             ("Office Directory", "Names, roles, extensions, emails", "Google Sheet", "ft-sheet", None),
             ("Org Chart", "Teams and reporting lines", "PDF", "ft-pdf", None),
             ("Emergency Contacts", "After-hours and building contacts", "PDF", "ft-pdf", "REQUIRED")]),
]
PAGES = list(PAGES) + EXTRA_PAGES

OUT = "/home/user/drawing-set/google-sites/embeds"
SVG = json.load(open("icon_svg.json"))

def ic(name):
    return SVG[name]

HEAD = """<!-- ==================================================================
     EAD OFFICE HUB  ·  {TITLE}
     Google Sites  >  Insert  >  Embed  >  Embed code  >  paste all of this
     ------------------------------------------------------------------
     TO EDIT: change only the CONFIG block below. Paste each Drive link
     between the quotes. Everything under "--- do not edit ---" is layout.
     ================================================================== -->
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">

<div id="ead"></div>

<script>
/* ===================== CONFIG — edit this part ===================== */
var CFG = {{
  /* ---- FILL THIS IN ONCE, PER FILE ----------------------------------
     Publish the site first, then paste its address here with NO slash at
     the end. The left menu builds all ten of its links from this one line.
       e.g. "https://sites.google.com/eigelberger.com/ead-office-hub"      */
  siteBase: "",

  /* Where the search box sends people. Leave as-is to search all of Drive,
     or paste a Shared-drive folder ID to scope it to the office hub. */
  driveFolderId: "",

  {CONFIG}
}};
/* =================== --- do not edit below --- ==================== */
"""

CSS = """
var CSS = `
#ead *{box-sizing:border-box;margin:0;padding:0}
#ead{
  display:flex; align-items:stretch; overflow:hidden;
  --ui:'Montserrat',system-ui,-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
  --mono:'IBM Plex Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
  font-family:var(--ui);
  background:
    radial-gradient(120% 95% at 88% 2%, #1A4E8C 0%, rgba(26,78,140,0) 62%),
    #022049;
  border-radius:16px; color:#fff;
  -webkit-font-smoothing:antialiased;
}
#ead .hd{font:700 30px/1.15 var(--ui);letter-spacing:-.4px}
#ead .sb{margin-top:9px;font:400 15px/1.5 var(--ui);color:#C6D6E8;max-width:66ch}

/* ---- left index rail ---- */
#ead .rail{flex:0 0 232px;background:#fff;color:#4B4B4B;padding:26px 0 22px;
  display:flex;flex-direction:column}
#ead .rail .brand{padding:0 22px}
#ead .rail .brand b{display:block;font:700 17px/1 var(--ui);color:#022049;letter-spacing:-.2px}
#ead .rail .brand span{display:block;margin-top:6px;font:400 10px var(--mono);
  color:#4B4B4B;letter-spacing:1.4px}
#ead .rail hr{border:0;border-top:1px solid #C9D1D6;margin:18px 22px}
#ead .rail .lbl{padding:0 22px;font:400 10px var(--mono);color:#788492;letter-spacing:1.4px}
#ead .rail nav{margin-top:10px;display:flex;flex-direction:column;gap:1px}
#ead .rail a{display:flex;align-items:center;gap:10px;margin:0 12px;padding:9px 10px;
  border-radius:9px;text-decoration:none;color:#4B4B4B;font:400 13.5px var(--ui)}
#ead .rail a svg{width:17px;height:17px;stroke:#4B4B4B;fill:none;stroke-width:1.7;
  stroke-linecap:round;stroke-linejoin:round;flex:none}
#ead .rail a .n{margin-left:auto;font:400 11px var(--mono);color:#788492}
#ead .rail a:hover{background:#EEF1F5}
#ead .rail a.on{background:#022049;color:#fff;font-weight:600}
#ead .rail a.on svg{stroke:#fff}
#ead .rail a.on .n{color:#C6D6E8}
#ead .rail .ask{margin-top:auto;padding:0 22px}
#ead .rail .ask hr{margin:18px 0}
#ead .rail .ask p{font:400 12.5px/1.45 var(--ui);color:#4B4B4B}
#ead .rail .ask b{display:block;margin-top:3px;font:700 12.5px var(--ui);color:#022049}

/* ---- content column ---- */
#ead .main{flex:1;min-width:0;padding:28px 30px 32px;
  background:
    radial-gradient(120% 95% at 88% 2%, #1A4E8C 0%, rgba(26,78,140,0) 62%),
    #022049}

/* ---- search ---- */
#ead .search{display:flex;align-items:center;gap:12px;background:#fff;
  border-radius:999px;padding:7px 7px 7px 20px;margin-top:22px}
#ead .hd+.search,#ead #ead>.search:first-child{margin-top:0}
#ead .search svg{width:19px;height:19px;stroke:#788492;fill:none;
  stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
#ead .search input{flex:1;border:0;outline:0;background:none;min-width:0;
  font:400 14px var(--mono);color:#022049}
#ead .search input::placeholder{color:#788492}
#ead .search button{border:0;cursor:pointer;background:#022049;color:#fff;
  border-radius:999px;padding:11px 26px;font:700 13px var(--ui);letter-spacing:.6px}
#ead .search button:hover{background:#0B3karma}

/* ---- action pills ---- */
#ead .pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:16px}
#ead .pill{display:inline-flex;align-items:center;gap:9px;background:#fff;
  color:#022049;border-radius:999px;padding:11px 20px 11px 16px;
  font:600 13.5px var(--ui);text-decoration:none;transition:transform .12s,box-shadow .12s}
#ead .pill:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(0,0,0,.24)}
#ead .pill svg{width:17px;height:17px;stroke:#022049;fill:none;
  stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round;flex:none}

/* ---- frosted cards ---- */
#ead .grid{display:grid;gap:18px;margin-top:26px;
  grid-template-columns:repeat(auto-fit,minmax(206px,1fr))}
#ead .grid.wide{grid-template-columns:1fr}
#ead .card{position:relative;display:flex;flex-direction:column;
  background:rgba(255,255,255,.10);
  -webkit-backdrop-filter:blur(18px) saturate(120%);
          backdrop-filter:blur(18px) saturate(120%);
  border:1px solid rgba(108,148,196,.55);border-radius:18px;
  padding:20px;text-decoration:none;color:inherit;min-height:190px;
  transition:background .15s,border-color .15s,transform .15s}
#ead .card:hover{background:rgba(255,255,255,.17);
  border-color:rgba(160,196,238,.85);transform:translateY(-2px)}
#ead .chip{width:42px;height:42px;border-radius:11px;background:#2C588E;
  display:flex;align-items:center;justify-content:center;flex:none}
#ead .chip.lt{background:#fff;width:54px;height:54px;border-radius:14px}
#ead .chip svg{width:21px;height:21px;stroke:#fff;fill:none;
  stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
#ead .chip.lt svg{width:26px;height:26px;stroke:#022049}
#ead .ttl{margin-top:16px;font:700 17.5px/1.28 var(--ui)}
#ead .blurb{margin-top:7px;font:400 13px/1.5 var(--ui);color:#BACEE6;flex:1}
#ead .foot{display:flex;justify-content:space-between;align-items:center;
  margin-top:16px;font:500 11.5px var(--mono);
  color:#BACEE6;letter-spacing:.3px}
#ead .card:hover .foot .open{color:#fff}
#ead .dot{position:absolute;top:24px;right:20px;width:9px;height:9px;border-radius:50%}
#ead .dot.req{background:#7FCBA4}
#ead .dot.upd{background:#E0AE55}

/* ---- notices ---- */
#ead .notice{display:flex;gap:16px;align-items:flex-start;
  background:rgba(255,255,255,.10);
  -webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
  border:1px solid rgba(108,148,196,.55);border-radius:16px;padding:20px 22px}
#ead .notice .body{flex:1;min-width:0}
#ead .notice .row{display:flex;justify-content:space-between;gap:16px;align-items:baseline}
#ead .notice .nt{font:700 16.5px/1.3 var(--ui)}
#ead .notice .dt{font:500 11.5px var(--mono);color:#BACEE6;white-space:nowrap}
#ead .notice p{margin-top:8px;font:400 13.5px/1.55 var(--ui);color:#BACEE6}
#ead .urgent{display:inline-block;width:8px;height:8px;border-radius:50%;
  background:#E0AE55;margin-right:7px;vertical-align:2px}

/* ---- learning sessions ---- */
#ead .sess{min-height:150px}
#ead .sess .dt{font:500 11.5px var(--mono);color:#BACEE6;letter-spacing:.4px}
#ead .sess .ttl{margin-top:10px;font:700 16.5px/1.3 var(--ui)}
#ead .sess .who{display:flex;align-items:center;gap:10px;margin-top:auto;padding-top:14px;
  font:400 13px var(--ui);color:#BACEE6}
#ead .sess .who .chip{width:30px;height:30px;border-radius:9px}
#ead .sess .who .chip svg{width:15px;height:15px}
#ead .sess.open{border-style:dashed;border-color:rgba(160,196,238,.7)}

`;
"""

JS = """
var ICONS = %ICONS%;

function svg(n){ return '<svg viewBox="0 0 24 24">'+(ICONS[n]||'')+'</svg>'; }
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){
  return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

var NAV = [
 ["Home","home",""], ["Announcements","announcements","4"],
 ["Office Standards","standards","6"], ["Templates","templates","4"],
 ["Forms","forms","6"], ["Office Policies","policies","5"],
 ["SOPs","sops","6"], ["Revit Standards","revit","8"],
 ["Learning Sessions","learning",""], ["Staff Directory","directory","3"]
];
/* Sites builds a page address by lower-casing the name and hyphenating it. */
function slug(n){ return n.toLowerCase().replace(/&/g,'').replace(/[^a-z0-9]+/g,'-')
                          .replace(/^-|-$/g,''); }

function rail(){
  var base = (CFG.siteBase || '').replace(/\/+$/,'');
  var items = NAV.map(function(it, i){
    var href = base ? (base + (i === 0 ? '' : '/' + slug(it[0]))) : '#';
    return '<a class="'+(i===CFG.navIndex?'on':'')+'" target="_top" href="'+href+'">'+
      svg(it[1])+'<span>'+esc(it[0])+'</span>'+
      (it[2] ? '<span class="n">'+it[2]+'</span>' : '')+'</a>';
  }).join('');
  return '<div class="rail">'+
    '<div class="brand"><b>EIGELBERGER</b><span>OFFICE HUB</span></div><hr>'+
    '<div class="lbl">SECTIONS</div><nav>'+items+'</nav>'+
    '<div class="ask"><hr><p>Need something added?</p><b>Ask the office manager</b></div>'+
  '</div>';
}

function head(){
  /* Leave title/subtitle empty in CONFIG if you'd rather the Sites page
     banner carry them -- the block then starts at the search bar. */
  var h = (CFG.title    ? '<div class="hd">'+esc(CFG.title)+'</div>' : '') +
          (CFG.subtitle ? '<div class="sb">'+esc(CFG.subtitle)+'</div>' : '') +
          '<form class="search" target="_blank">'+
            svg('search')+
            '<input type="text" placeholder="Search standards, templates, forms, SOPs, Revit standards\\u2026">'+
            '<button type="submit">SEARCH</button>'+
          '</form>';
  if (CFG.actions && CFG.actions.length){
    h += '<div class="pills">' + CFG.actions.map(function(a){
      return '<a class="pill" target="_top" href="'+esc(a.link)+'">'+svg(a.icon)+esc(a.label)+'</a>';
    }).join('') + '</div>';
  }
  return h;
}

function sectionCards(){
  return '<div class="grid">' + CFG.cards.map(function(c){
    return '<a class="card" target="_top" href="'+esc(c.link)+'">'+
      '<div class="chip lt">'+svg(c.icon)+'</div>'+
      '<div class="ttl">'+esc(c.title)+'</div>'+
      '<div class="blurb">'+esc(c.blurb)+'</div>'+
      '<div class="foot"><span>'+esc(c.count)+' documents</span>'+
      '<span class="open">Open \\u2197</span></div></a>';
  }).join('') + '</div>';
}

function docCards(){
  return '<div class="grid">' + CFG.cards.map(function(c){
    var dot = c.status === 'REQUIRED' ? '<span class="dot req"></span>'
            : c.status === 'UPDATED'  ? '<span class="dot upd"></span>' : '';
    return '<a class="card" target="_top" href="'+esc(c.link)+'">'+dot+
      '<div class="chip">'+svg(c.icon)+'</div>'+
      '<div class="ttl">'+esc(c.title)+'</div>'+
      '<div class="blurb">'+esc(c.blurb)+'</div>'+
      '<div class="foot"><span>'+esc(c.format)+'</span>'+
      '<span class="open">Open \\u2197</span></div></a>';
  }).join('') + '</div>';
}

function notices(){
  return '<div class="grid wide">' + CFG.cards.map(function(n){
    return '<div class="notice">'+
      '<div class="chip">'+svg('announcements')+'</div>'+
      '<div class="body"><div class="row">'+
        '<div class="nt">'+(n.urgent?'<span class="urgent"></span>':'')+esc(n.title)+'</div>'+
        '<div class="dt">'+esc(n.date)+'</div></div>'+
        '<p>'+esc(n.body)+'</p></div></div>';
  }).join('') + '</div>';
}

function sessions(){
  return '<div class="grid">' + CFG.cards.map(function(s){
    var open = /^open/i.test(s.presenter);
    return '<a class="card sess'+(open?' open':'')+'" target="_top" href="'+esc(s.link)+'">'+
      '<div class="dt">'+esc(s.date)+'</div>'+
      '<div class="ttl">'+esc(s.topic)+'</div>'+
      '<div class="who"><div class="chip">'+svg('learning')+'</div>'+esc(s.presenter)+'</div></a>';
  }).join('') + '</div>';
}

(function(){
  var host = document.getElementById('ead');
  var st = document.createElement('style'); st.textContent = CSS;
  document.head.appendChild(st);
  var body = { sections: sectionCards, docs: docCards,
               notices: notices, sessions: sessions }[CFG.kind]();
  host.innerHTML = rail() + '<div class="main">' + head() + body + '</div>';
  var form = host.querySelector('.search');
  form.addEventListener('submit', function(e){
    e.preventDefault();
    var q = form.querySelector('input').value.trim();
    if (!q) return;
    var base = 'https://drive.google.com/drive/search?q=';
    var scope = CFG.driveFolderId ? ('%20parent:' + CFG.driveFolderId) : '';
    window.open(base + encodeURIComponent(q) + scope, '_blank');
  });
})();
</script>
"""

def cfg_lines(p):
    L = ['navIndex: %d,' % p["i"],
         'title: %s,' % json.dumps(p["title"]),
         'subtitle: %s,' % json.dumps(p["sub"]),
         'kind: %s,' % json.dumps(p["kind"]), '']
    if p["kind"] != "notices":
        L.append('  actions: [')
        for label, icon in ACTIONS:
            L.append('    {label:%-23s icon:%-13s link:"" },' % (json.dumps(label)+',', json.dumps(icon)+','))
        L.append('  ],'); L.append('')
    L.append('  cards: [')
    if p["kind"] == "sections":
        for name, icon, count, blurb in p["items"]:
            L.append('    {title:%s,' % json.dumps(name))
            L.append('     icon:%s, count:%d,' % (json.dumps(icon), count))
            L.append('     blurb:%s,' % json.dumps(blurb))
            L.append('     link:""},')
    elif p["kind"] == "docs":
        for name, blurb, fmt, ficon, status in p["items"]:
            L.append('    {title:%s,' % json.dumps(name))
            L.append('     blurb:%s,' % json.dumps(blurb))
            L.append('     format:%s, icon:%s, status:%s,' % (
                json.dumps(fmt), json.dumps(ficon), json.dumps(status) if status else '""'))
            L.append('     link:""},')
    elif p["kind"] == "sessions":
        for date, presenter, topic in p["items"]:
            L.append('    {date:%s, presenter:%s,' % (json.dumps(date), json.dumps(presenter)))
            L.append('     topic:%s, link:""},' % json.dumps(topic))
    elif p["kind"] == "notices":
        for title, date, body, urgent in p["items"]:
            L.append('    {title:%s,' % json.dumps(title))
            L.append('     date:%s, urgent:%s,' % (json.dumps(date), 'true' if urgent else 'false'))
            L.append('     body:%s},' % json.dumps(body))
    L.append('  ],')
    return "\n  ".join(L)


NEED = ["search", "announcements", "learning", "home", "directory", "policies"] + [s[1] for s in SECTIONS] + [a[1] for a in ACTIONS]
for p in PAGES:
    if p["kind"] == "docs":
        NEED += [it[3] for it in p["items"]]
ICONS_JSON = json.dumps({k: SVG[k] for k in sorted(set(NEED))}, indent=1)

os.makedirs(OUT, exist_ok=True)
SLUG = {0:"01-home", 1:"02-announcements", 2:"03-office-standards", 3:"04-templates",
        4:"05-forms", 5:"06-office-policies", 6:"07-sops", 7:"08-revit-standards",
        8:"09-learning-sessions", 9:"10-staff-directory"}
for p in PAGES:
    html = (HEAD.format(TITLE=p["title"].upper(), CONFIG=cfg_lines(p))
            + CSS + JS.replace("%ICONS%", ICONS_JSON))
    html = html.replace("#0B3karma", "#0B3A72")   # typo guard
    fn = os.path.join(OUT, SLUG[p["i"]] + ".html")
    open(fn, "w").write(html)
    print("%-34s %6d chars" % (os.path.basename(fn), len(html)))
