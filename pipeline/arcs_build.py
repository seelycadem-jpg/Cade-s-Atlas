import json, sys
sys.path.insert(0, "/home/claude")
import arc_japan, arc_ww2, arc_africa
from rewrites import TOP

M = {"P":"political","W":"war","E":"economic","I":"ideas","R":"religion","S":"science","C":"culture"}
D = json.load(open("/home/claude/site/data.json"))
EV = D["events"]

EXTRA_T1 = {
 "Jamestown founded","Louisiana Purchase","Mexican-American War","Reconstruction ends → Jim Crow","Spanish-American War; Hawaii annexed",
 "Brown v. Board of Education","FDR's New Deal","Korean War","Voting Rights Act; Vietnam escalation","Indian Removal Act",
 "Copernicus: sun-centered universe","Henry VIII breaks with Rome","Spanish Armada defeated","Thirty Years' War begins","Glorious Revolution",
 "Seven Years' War","Napoleon invades Russia","Franco-Prussian War","Gorbachev comes to power","Dutch VOC founded","English East India Company",
 "Ming falls; Qing dynasty","Tokugawa shogunate","Perry's 'black ships' reach Japan","Taiping Rebellion","Indian Rebellion","British Raj begins",
 "Atatürk's Turkish Republic","Chinese Civil War begins","Japan invades China","Great Leap Forward","Six-Day War","Saigon falls; Khmer Rouge",
 "Safavid Persia founded","Babur founds Mughal Empire","First Sino-Japanese War","Japan annexes Korea",
 "Dutch found Cape Town","Mandela freed","Suez Crisis","Algerian War","Congo wars begin",
 "Pizarro captures Atahualpa","Bolívar wins at Boyacá","Mexican Revolution","Brazil abolishes slavery","Mexico independent",
 "Fall of France","D-Day","Treaty of Versailles","Russian Revolution","Galileo's telescope","Maji Maji Rebellion",
}
for e in EV:
    e["tier"] = 1 if (e["h"] in TOP or e["h"] in EXTRA_T1) else 2
    e.setdefault("arcs", []); e.setdefault("causes", [])

def basemap(y):
    ys=[1400,1492,1500,1530,1600,1650,1700,1715,1783,1800,1815,1880,1900,1914,1920,1930,1938,1945,1960,1994,2000,2010]
    return max(b for b in ys if b<=y)

def find(head, prefer):
    c=[e for e in EV if e["h"]==head]
    if not c: raise SystemExit("missing ref: "+head)
    for e in c:
        if e["r"]==prefer: return e
    return c[0]

ARCS=[]
pending=[]
for mod, thread in [(arc_japan,"japan"),(arc_ww2,"worldwars"),(arc_africa,"empire")]:
    A=mod.ARC; items=[]
    for it in mod.E:
        if "ref" in it:
            e=find(it["ref"], A["color"])
            if "tier" in it: e["tier"]=it["tier"]
        else:
            e=dict(id=it["id"], y=it["y"], r=it["r"], h=it["h"], who=it["who"], where=it["where"], what=it["hook"], why=it["why"],
                   sig=it["then"], lat=it["lat"], lon=it["lon"], map=basemap(it["y"]), c=[M[x] for x in it["c"]], w=1,
                   hook=it["hook"], story=it["story"], then=it["then"], now=it["now"], tier=it["tier"], arcs=[], causes=[],
                   t=[thread] + (["eastafrica"] if A["id"]=="scramble" and it["lon"]>28 and it["lat"]<5 else []))
            if it.get("m"): e["m"]=it["m"]
            EV.append(e)
        for k in ("q","myth","src","fact"):
            if k in it: e[k]=it[k]
        if A["id"] not in e["arcs"]: e["arcs"].append(A["id"])
        if it.get("causes"): pending.append((e, it["causes"], A["color"]))
        items.append(dict(id=e["id"], chap=it["chap"]))
    ARCS.append(dict(id=A["id"], title=A["title"], span=A["span"], summary=A["summary"], chapters=[dict(t=c[0],a=c[1],b=c[2],d=c[3]) for c in A["chapters"]],
                     sources=A["sources"], items=items, region=A["color"]))

ids={e["id"]:e for e in EV}
SHORT={"japan":"Japan's rise","ww2":"WWII in Europe","scramble":"Scramble for Africa"}
for A in ARCS: A["short"]=SHORT[A["id"]]

# ---- framework arcs: every event placed in at least one story, with explained links ----
import arcs_all1, arcs_all2, arcs_all3
def resolve(h):
    r=None
    if len(h)>3 and h[2]=="|" and h[:2] in ("na","eu","as","af","la"): r,h=h[:2],h[3:]
    c=[e for e in EV if e["h"]==h and (r is None or e["r"]==r)]
    if not c: raise SystemExit("missing head: "+h)
    if len(c)>1: raise SystemExit("ambiguous head (add rr| prefix): "+h+" "+str([x["r"] for x in c]))
    return c[0]
bad=[]
for A in arcs_all1.ARCS+arcs_all2.ARCS+arcs_all3.ARCS:
    chs=A["chapters"]; items=[]
    for h in A["items"]:
        e=resolve(h)
        ci=next((i for i,c in enumerate(chs) if c[1]<=e["y"]<=c[2]), None)
        if ci is None: ci=min(range(len(chs)), key=lambda i: min(abs(e["y"]-chs[i][1]),abs(e["y"]-chs[i][2]))); bad.append((A["id"],h,"outside chapters"))
        if any(it["id"]==e["id"] for it in items): bad.append((A["id"],h,"dup")); continue
        items.append(dict(id=e["id"], chap=ci))
        if A["id"] not in e["arcs"]: e["arcs"].append(A["id"])
    for f,t,why in A["links"]:
        a,b=resolve(f),resolve(t)
        if (a["y"],a.get("m",0))>(b["y"],b.get("m",13)): raise SystemExit("backwards link: %s -> %s"%(f,t))
        if not any(c["f"]==a["id"] for c in b["causes"]): b["causes"].append(dict(f=a["id"], why=why))
    ARCS.append(dict(id=A["id"], short=A["short"], title=A["title"], span=A["span"], summary=A["summary"],
                     chapters=[dict(t=c[0],a=c[1],b=c[2],d=c[3]) for c in chs], sources=[], reading=A["reading"], items=items, region=A["region"]))
for f,t,why in arcs_all3.LINKS:
    a,b=resolve(f),resolve(t)
    if (a["y"],a.get("m",0))>(b["y"],b.get("m",13)): raise SystemExit("backwards link: %s -> %s"%(f,t))
    if not any(c["f"]==a["id"] for c in b["causes"]): b["causes"].append(dict(f=a["id"], why=why))
if bad: print("WARN", bad)
for e, causes, pref in pending:
    for src, why in causes:
        sid = find(src[4:], pref)["id"] if src.startswith("ref:") else src
        if sid not in ids: raise SystemExit("bad cause "+src)
        if not any(c["f"]==sid for c in e["causes"]): e["causes"].append(dict(f=sid, why=why))

# order arcs' items chronologically
for A in ARCS:
    A["items"].sort(key=lambda it: (ids[it["id"]]["y"], ids[it["id"]].get("m",0)))
EV.sort(key=lambda e: (e["y"], e.get("m",6), e["r"]))
D["arcs"]=ARCS
json.dump(D, open("/home/claude/site/data.json","w"), ensure_ascii=False, separators=(",",":"))
from collections import Counter
print("events",len(EV), Counter(e["tier"] for e in EV), "arcs", [(a["id"],len(a["items"])) for a in ARCS])
print("edges", sum(len(e["causes"]) for e in EV))
orphans=[(e["y"],e["r"],e["h"]) for e in EV if not e["arcs"]]
print("events in no story:", len(orphans)); [print("  ",o) for o in orphans]
