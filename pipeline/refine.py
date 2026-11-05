import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import ROOT, SITE
# Stage 3 of the build: make every event singular, merge duplicates, add Oceania,
# assign the nine regions, and attach encyclopedia titles.
# Build order: make_json.py -> arcs_build.py -> refine.py -> tiers.py
import json, sys, copy
sys.path.insert(0, ROOT)
from refine_splits import SPLITS
from refine_splits2 import SPLITS2, MERGES, RENAME, WHY, NEWLINKS
import refine_oceania as OC

D = json.load(open(SITE + "/data.json"))
EV = D["events"]; ARCS = D["arcs"]
by = {e["id"]: e for e in EV}
OLDHEAD = {e["id"]: e["h"] for e in EV}
CMAP = {"P":"political","W":"war","E":"economic","I":"ideas","R":"religion","S":"science","C":"culture"}
BASE = [1400,1492,1500,1530,1600,1650,1700,1715,1783,1800,1815,1880,1900,1914,1920,1930,1938,1945,1960,1994,2000,2010]
basemap = lambda y: max(b for b in BASE if b <= y)
ALL = {**SPLITS, **SPLITS2}

def build(part, old=None, first=False):
    e = {}
    if old:
        for k in ("t",): e[k] = copy.deepcopy(old.get(k, []))
        if first:
            for k in ("q","myth","src","fact","sites"):
                if k in old: e[k] = copy.deepcopy(old[k])
    e.update(id=part["id"], y=part["y"], h=part["h"], tier=part["tier"], who=part["who"], where=part["where"],
             lat=part["lat"], lon=part["lon"], hook=part["hook"], what=part["hook"], story=part["story"], why=part["why"],
             then=part["then"], sig=part["then"], now=part["now"], wk=part["wk"], c=[CMAP[x] for x in part["c"]],
             map=basemap(part["y"]), arcs=[], causes=[])
    if part.get("m"): e["m"] = part["m"]
    for k in ("fact","myth","t","r","q"):
        if part.get(k) is not None: e[k] = copy.deepcopy(part[k])
    if "sites_keep" in part:
        e["sites"] = [s for s in (old or {}).get("sites", []) if s["n"] in part["sites_keep"]]
        if not e["sites"]: e.pop("sites")
    elif not first: e.pop("sites", None)
    e.setdefault("t", [])
    e["w"] = {1:3, 2:2, 3:1}[e["tier"]]
    return e

# ---- 1. edges as (src, dst, why) on old ids
edges = [(c["f"], e["id"], c["why"]) for e in EV for c in e["causes"]]

# ---- 2. split events
newEV = []; parts_of = {}
for e in EV:
    if e["id"] in ALL:
        ps = ALL[e["id"]]; parts_of[e["id"]] = ps
        for i, p in enumerate(ps): newEV.append(build(p, e, first=(i == 0)))
    else:
        newEV.append(e)

def route(src, dst):
    S = [p["id"] for p in parts_of[src] if OLDHEAD.get(dst) in p.get("cout", [])] if src in parts_of else [src]
    if src in parts_of and not S: S = [parts_of[src][0]["id"]]
    T = [p["id"] for p in parts_of[dst] if OLDHEAD.get(src) in p.get("cin", [])] if dst in parts_of else [dst]
    if dst in parts_of and not T: T = [parts_of[dst][0]["id"]]
    return [(s, t) for s in S for t in T]

E2 = []
for s, d, why in edges:
    for a, b in route(s, d): E2.append([a, b, why])

# ---- 3. story membership for split parts
for A in ARCS:
    items = []
    for it in A["items"]:
        if it["id"] in parts_of:
            for p in parts_of[it["id"]]:
                if "arcs" not in p or A["id"] in p["arcs"]: items.append(dict(id=p["id"], chap=it["chap"]))
        else: items.append(it)
    A["items"] = items
ARCX = {A["id"]: A for A in ARCS}
for oid, ps in parts_of.items():
    for p in ps:
        for a in p.get("arcs", []):
            if a in ARCX and not any(it["id"] == p["id"] for it in ARCX[a]["items"]): ARCX[a]["items"].append(dict(id=p["id"], chap=0))

# ---- 4. merges
gone = {d: k for k, ds in MERGES.items() for d in ds}
byN = {e["id"]: e for e in newEV}
for k, ds in MERGES.items():
    keep = byN[k]
    for d in ds:
        x = byN[d]
        for f in ("fact","sites","myth","q"):
            if f not in keep and f in x: keep[f] = x[f]
        keep["t"] = sorted(set(keep.get("t", [])) | set(x.get("t", [])))
        keep["tier"] = min(keep["tier"], x["tier"])
newEV = [e for e in newEV if e["id"] not in gone]
E2 = [[gone.get(a, a), gone.get(b, b), w] for a, b, w in E2]
for A in ARCS:
    seen = set(); items = []
    for it in A["items"]:
        i = gone.get(it["id"], it["id"])
        if i not in seen: seen.add(i); items.append(dict(id=i, chap=it["chap"]))
    A["items"] = items

# ---- 5. renames / rewrites
byN = {e["id"]: e for e in newEV}
for i, ch in RENAME.items():
    e = byN[i]
    for k, v in ch.items():
        if k == "arcs":
            for A in ARCS:
                ids = [it["id"] for it in A["items"]]
                if A["id"] in v and i not in ids: A["items"].append(dict(id=i, chap=0))
                if A["id"] not in v and i in ids: A["items"] = [it for it in A["items"] if it["id"] != i]
        elif k == "sites_keep":
            e["sites"] = [s for s in e.get("sites", []) if s["n"] in v]
        elif v is None: e.pop(k, None)
        else: e[k] = v
    if "hook" in ch: e["what"] = ch["hook"]
    if "then" in ch: e["sig"] = ch["then"]
    if "y" in ch: e["map"] = basemap(e["y"])
    if "c" in ch and ch["c"] and len(ch["c"][0]) == 1: e["c"] = [CMAP[x] for x in ch["c"]]

# ---- 6. Oceania
for p in OC.NEW:
    e = build(p); e.setdefault("r", "oc"); newEV.append(e)
byN = {e["id"]: e for e in newEV}
ARCS.append(dict(id=OC.ARC["id"], short=OC.ARC["short"], title=OC.ARC["title"], span=OC.ARC["span"], summary=OC.ARC["summary"],
                 chapters=[dict(t=c[0], a=c[1], b=c[2], d=c[3]) for c in OC.ARC["chapters"]], sources=[], reading=OC.ARC["reading"],
                 items=[], region="oc"))
ARC = {A["id"]: A for A in ARCS}
for p in OC.NEW:
    for a in p.get("arcs", []): ARC[a]["items"].append(dict(id=p["id"], chap=0))

# ---- 6b. new events for the Middle East, South Asia and Southeast Asia, and two new stories
import refine_regions as RG
for p in RG.NEW: newEV.append(build(p))
for A in RG.ARCS_NEW:
    ARCS.append(dict(id=A["id"], short=A["short"], title=A["title"], span=A["span"], summary=A["summary"],
                     chapters=[dict(t=c[0], a=c[1], b=c[2], d=c[3]) for c in A["chapters"]], sources=[], reading=A["reading"], items=[], region=A["region"]))
ARC = {A["id"]: A for A in ARCS}
for p in RG.NEW:
    for a in p.get("arcs", []): ARC[a]["items"].append(dict(id=p["id"], chap=0))
byN = {e["id"]: e for e in newEV}

# ---- 6c. new key events and details for the 1 -> 2 -> 3 hierarchy
import details1 as DT1, details2 as DT2, details3 as DT3
DETAILS = [DT1, DT2, DT3]
for M in DETAILS:
    for p in M.NEW: newEV.append(build(p))
ARC = {A["id"]: A for A in ARCS}
for M in DETAILS:
    for p in M.NEW:
        for a in p.get("arcs", []): ARC[a]["items"].append(dict(id=p["id"], chap=0))
byN = {e["id"]: e for e in newEV}

H = {}
for e in newEV: H.setdefault(e["h"], []).append(e["id"])
def hid(h):
    if h not in H: raise SystemExit("unknown head: " + h)
    if len(H[h]) > 1: raise SystemExit("ambiguous head: " + h)
    return H[h][0]
for h in OC.ARC_EXTRA: ARC["oceania"]["items"].append(dict(id=hid(h), chap=0))
for A in RG.ARCS_NEW:
    for h in A["extra"]: ARC[A["id"]]["items"].append(dict(id=hid(h), chap=0))
for a, hs in RG.ARC_ADD.items():
    for h in hs:
        if not any(it["id"] == hid(h) for it in ARC[a]["items"]): ARC[a]["items"].append(dict(id=hid(h), chap=0))

# ---- 7. link fixes: WHY (upsert / delete), new links, Oceania links
def upsert(fh, th, why):
    if fh not in H or th not in H: return False
    a, b = hid(fh), hid(th)
    global E2
    E2 = [x for x in E2 if not (x[0] == a and x[1] == b)]
    if why: E2.append([a, b, why])
    return True
missing = []
for (fh, th), why in WHY.items():
    if not upsert(fh, th, why) and why is not None: missing.append((fh, th))
for fh, th in RG.WHY_DEL: upsert(fh, th, None)
for fh, th, why in NEWLINKS + OC.LINKS + RG.LINKS + DT1.LINKS + DT2.LINKS:
    if why is None: continue
    if not upsert(fh, th, why): missing.append((fh, th))
if missing: print("WARN links with unknown heads:", missing)

# ---- 8. regions
OVR = {"Fall of Constantinople":"eu","Berlin Conference":"af","Tehran Conference":"eu","Young Turk Revolution":"me",
       "Treaty of Tordesillas":"la","Treaty of Paris: Britain wins Canada":"na","Independence recognized":"na",
       "Sykes-Picot Agreement":"me","Iwakura Mission tours the West":"ea","Anglo-Japanese Alliance":"ea",
       "Heligoland-Zanzibar Treaty":"af","Britain and Germany divide East Africa":"af","Imperial British East Africa Company chartered":"af",
       "Portuguese begin Atlantic slave trade":"af","Congress of Berlin":"eu","Gallipoli: the ANZAC landing":"oc"}
OVR.update(DT1.OVR); OVR.update(DT2.OVR)
def region(e, old):
    lat, lon = e["lat"], e["lon"]
    if -170 < lon < -25 and not (lon < -140 and lat < 35):
        return old if old in ("na", "la") else ("na" if lat > 25 else "la")
    if (lon <= -140 and lat < 35) or lon >= 160 or (lon >= 112 and lat <= -10) or (lon >= 140 and lat < 0) or (lon >= 141.5 and lat < 30): return "oc"
    if lat >= 50 and lon >= 40: return "eu"                       # Russia east of the Urals
    if -20 <= lon <= 52:
        north_africa = ((lon < -1.5 and lat < 35.95) or (-1.5 <= lon < 3 and lat < 36.5) or (3 <= lon < 11.5 and lat < 37.4)
                        or (11.5 <= lon < 25 and lat < 33.5) or (25 <= lon < 35 and lat < 31.7))
        if lat < 19.5 and not (lon >= 42.5 and lat >= 12.4): return "af"
        if north_africa: return "me"
    if 26 <= lon < 60.5 and 12 <= lat < 42 and not (40 <= lon < 50 and lat >= 41.3): return "me"
    if 60.5 <= lon <= 92.5 and lat < 38 and (lat < 29.5 or lon < 80): return "sa"
    if (92.5 <= lon <= 141 and -11 <= lat <= 20.0) or (92.5 <= lon <= 101.5 and lat <= 28.5) or (101.5 < lon <= 109.5 and lat <= 22.6):
        return "se"
    if lon >= 73 and lat >= 18: return "ea"
    return "eu"
for e in newEV:
    old = e.get("r")
    if e["h"] in OVR: e["r"] = OVR[e["h"]]
    elif e["id"] in RENAME and "r" in RENAME[e["id"]]: e["r"] = RENAME[e["id"]]["r"]
    elif any(e["id"] == p["id"] and p.get("r") for ps in ALL.values() for p in ps): pass
    elif e["id"].startswith("oc-"): e["r"] = "oc"
    else: e["r"] = region(e, old)

# ---- 8b. encyclopedia titles
from wk import WK
for e in newEV:
    if e["id"] in WK: e["wk"] = WK[e["id"]]
nowk = [e["h"] for e in newEV if not e.get("wk")]
if nowk: print("WARN no encyclopedia title:", nowk)

# ---- 9. rebuild causes, arcs, chapters; sort
byN = {e["id"]: e for e in newEV}
for e in newEV: e["causes"] = []
seen = set()
for a, b, w in E2:
    if a == b or (a, b) in seen or a not in byN or b not in byN: continue
    fa, fb = byN[a], byN[b]
    if (fa["y"], fa.get("m", 0)) > (fb["y"], fb.get("m", 13)): print("WARN backwards:", fa["h"], "->", fb["h"]); continue
    seen.add((a, b)); fb["causes"].append(dict(f=a, why=w))
fy = lambda e: e["y"] + ((e.get("m") or 6) - 1) / 12
for A in ARCS:
    chs = A["chapters"]
    for it in A["items"]:
        y = byN[it["id"]]["y"]
        ci = next((i for i, c in enumerate(chs) if c["a"] <= y <= c["b"]), None)
        if ci is None: ci = min(range(len(chs)), key=lambda i: min(abs(y - chs[i]["a"]), abs(y - chs[i]["b"])))
        it["chap"] = ci
    A["items"].sort(key=lambda it: fy(byN[it["id"]]))
    A["region"] = {"as": None}.get(A["region"], A["region"])
ARCREG = {"ottomans":"me","gunpowder":"sa","eastasia":"ea","searoutes":"se","china":"ea","india":"sa","pacific":"ea","asiadecol":"se",
          "middleeast":"me","prc":"ea","terror":"me","japan":"ea","africadecol":"af","scramble":"af"}
for A in ARCS:
    if A["id"] in ARCREG: A["region"] = ARCREG[A["id"]]
for e in newEV: e["arcs"] = [A["id"] for A in ARCS if any(it["id"] == e["id"] for it in A["items"])]
newEV.sort(key=lambda e: (e["y"], e.get("m") or 6, e["r"]))

D["events"] = newEV
D["regions"] = [dict(id="eu", name="Europe", short="Europe"), dict(id="me", name="Middle East & North Africa", short="Mid. East & N. Africa"),
                dict(id="sa", name="South Asia", short="South Asia"), dict(id="ea", name="East Asia", short="East Asia"),
                dict(id="se", name="Southeast Asia", short="Southeast Asia"), dict(id="af", name="Sub-Saharan Africa", short="Sub-Saharan Africa"),
                dict(id="na", name="North America", short="North America"), dict(id="la", name="Latin America", short="Latin America"),
                dict(id="oc", name="Oceania", short="Oceania")]
json.dump(D, open(SITE + "/data.json", "w"), ensure_ascii=False, separators=(",", ":"))

# old head -> new head, for other files (map place profiles)
HMAP = {}
for oid, h in OLDHEAD.items():
    nid = gone.get(oid, oid)
    if oid in parts_of: nid = parts_of[oid][0]["id"]
    nid = gone.get(nid, nid)
    if nid in byN and byN[nid]["h"] != h: HMAP[h] = byN[nid]["h"]
json.dump(HMAP, open(ROOT + "/headmap.json", "w"), ensure_ascii=False, indent=0)

from collections import Counter
print("events", len(newEV), "edges", sum(len(e["causes"]) for e in newEV), "regions", Counter(e["r"] for e in newEV))
comb = [e["h"] for e in newEV if ";" in e["h"] or "→" in e["h"] or " & " in e["h"]]
print("still combined:", comb)
print("no story:", [e["h"] for e in newEV if not e["arcs"]])
