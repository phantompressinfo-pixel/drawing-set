import json, re, html, os, time, urllib.request, ssl

CA = "/root/.ccr/ca-bundle.crt"
ctx = ssl.create_default_context(cafile=CA)
JOB, PROD = 491032, 18107
OUT = "/home/user/drawing-set/code-library/aspen"
os.makedirs(OUT, exist_ok=True)

def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            if i == tries - 1: raise
            time.sleep(2 * (i + 1))

def children(node):
    q = f"&nodeId={urllib.parse.quote(node)}" if node else ""
    return get(f"https://api.municode.com/codesToc/children?jobId={JOB}&productId={PROD}{q}") or []

def content(node):
    return get(f"https://api.municode.com/CodesContent?jobId={JOB}&nodeId={urllib.parse.quote(node)}&productId={PROD}")

def clean(c):
    t = re.sub(r"</t[dh]>", " | ", c)
    t = re.sub(r"</tr>", "\n", t)
    t = re.sub(r"<[^>]+>", "\n", t)
    t = html.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t.strip()

import urllib.parse
root = get(f"https://api.municode.com/codesToc?jobId={JOB}&productId={PROD}")
top = root["Children"]

# collect fetch units: leaf/part-level nodes; expand big containers (Part II titles)
units = []
for n in top:
    if not n["HasChildren"]:
        units.append(n)
    else:
        kids = children(n["Id"])
        # if children are Titles (e.g., PART II), fetch per child; else fetch the part whole
        if any(k["Heading"].strip().upper().startswith("TITLE") for k in kids):
            units.extend(kids)
        else:
            units.append(n)

seen = set()
index = []
for u in units:
    nid, head = u["Id"], re.sub(r"\s+", " ", u["Heading"]).strip()
    try:
        d = content(nid)
    except Exception as e:
        print("FAIL", nid, e); continue
    docs = d.get("Docs", []) or []
    new = [doc for doc in docs if doc.get("Id") not in seen]
    for doc in new: seen.add(doc.get("Id"))
    if not new:
        print("skip (all dup)", head); continue
    fn = re.sub(r"[^A-Za-z0-9]+", "-", head).strip("-").lower()[:70] + ".txt"
    with open(f"{OUT}/{fn}", "w") as f:
        f.write(f"# CITY OF ASPEN MUNICIPAL CODE — {head}\n")
        f.write("# Source: Municode (api.municode.com), Supp. No. 7 Update 1, codified through Ord. No. 06-2026 (enacted 2026-03-24)\n")
        f.write("# Retrieved: 2026-07-22\n\n")
        for doc in new:
            f.write(f"\n===== {doc.get('Title','')}\n")
            f.write(clean(doc.get("Content", "") or "") + "\n")
    index.append((fn, head, len(new)))
    print(f"{head}: {len(new)} docs -> {fn}")

with open(f"{OUT}/_INDEX.txt", "w") as f:
    f.write("City of Aspen Municipal Code — file index (retrieved 2026-07-22)\n\n")
    for fn, head, n in index:
        f.write(f"{fn}\t{head}\t{n} sections\n")
print("TOTAL docs:", len(seen))
