import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import ROOT
import json,collections,glob,os
from names import same
CP=[]
for f in sorted(glob.glob(ROOT + "/review/cp/*.json")):
    for p in json.load(open(f))["places"]: CP.append(p)
def truth(p,y):
    for t in p["timeline"]:
        if t["from"]<=y<t["to"]: return t
def matches(t,got):
    if not got: return t["ruler"]=="none"
    g=got.split(" (under ")[0]
    if t["ruler"]=="none": return False
    return any(same(g,n) for n in [t["ruler"]]+(t.get("aliases") or [])) or (t.get("overlord") and same(g,t["overlord"]))
R=json.load(open("score_atlas.json"))
cls=collections.Counter(); off=collections.Counter()
for r in R:
    if r["v"].startswith("ok") or r["v"]=="coarse": continue
    p=CP[r["i"]]; got=None if r["v"]=="blank" else r["got"]
    if r["v"]=="state_where_none": got=r["got"]
    hit=None
    for d in range(1,31):
        for yy in (r["y"]-d,r["y"]+d):
            t=truth(p,yy)
            if t and t["ruler"]!=r["truth"] and matches(t,got): hit=yy-r["y"]; break
        if hit is not None: break
    if hit is not None: cls["timing"]+=1; off[(hit//5)*5]+=1; r["timing"]=hit
    else: cls[r["v"]]+=1
print(cls); print(sorted(off.items()))
json.dump(R,open("score_atlas_t.json","w"))
