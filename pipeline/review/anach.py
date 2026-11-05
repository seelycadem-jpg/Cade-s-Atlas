"""Rows whose name the research dates to a different era: the record shows polity X in years when, by every
researched place, X ruled nowhere (and X does rule somewhere in the research at other times)."""
import json, glob, collections, sys
from names import same, key
CP=[p for f in sorted(glob.glob("cp/*.json")) for p in json.load(open(f))["places"]]
life=collections.defaultdict(lambda:[9999,0])  # name -> [first, last] over all researched intervals
names=set()
for p in CP:
    for t in p["timeline"]:
        for n in [t["ruler"]]+(t.get("aliases") or []):
            if n=="none" or not isinstance(n,str): continue
            L=life[n]; L[0]=min(L[0],t["from"]); L[1]=max(L[1],t["to"])
ROWS=json.load(open("/tmp/g3/rows.json"))
cache={}
def span(nm):
    if nm in cache: return cache[nm]
    s=[v for n,v in life.items() if same(nm,n)]
    cache[nm]=(min(x[0] for x in s), max(x[1] for x in s)) if s else None
    return cache[nm]
out=collections.defaultdict(lambda:[9999,0,0])
for r in ROWS:
    p=r["properties"]; sp=span(p["NAME"])
    if not sp: continue
    if p["a"]>=sp[1]+15 or p["b"]<=sp[0]-15:
        o=out[(p["NAME"],sp)]; o[0]=min(o[0],p["a"]); o[1]=max(o[1],p["b"]); o[2]+=1
for (n,sp),(a,b,c) in sorted(out.items(), key=lambda x:-x[1][2]): print(f"{n}: drawn {a}-{b} ({c} rows); researched {sp[0]}-{sp[1]}")
