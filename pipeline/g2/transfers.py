"""Pieces of territory that changed hands between consecutive survey maps, 1400-1886."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, ROOT, WORK
import json, re, subprocess, os, sys
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
import math
ROOT = ROOT
R = json.load(open(f"{ROOT}/atlas/rules.json"))
EMP = {k: dict(v, re=re.compile(v["rx"], re.I)) for k, v in R["empires"].items()}
COL = [dict(c, re=re.compile(c["rx"], re.I)) for c in R["colonial"]]
REN = [dict(r, re=re.compile(r["rx"], re.I)) for r in R["rename"]]
YEARS = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880]
NEXT = {1880: 1900}
STRIP = re.compile(r"\b(kingdom|empire|sultanate|khanate|emirate|duchy|grand|principality|republic|electorate|margraviate|landgraviate|county|the|of|and)\b|[^a-z ]", re.I)
def norm(n): return re.sub(r"\s+", " ", STRIP.sub(" ", (n or "").lower())).strip()
def owner(p, y):
    n, s = p.get("NAME") or "", p.get("SUBJECTO") or ""
    for c in COL:
        if c["a"] <= y < c["b"] and c["re"].search(n): return ("E:" + c["emp"], c["name"]) if c["emp"] else ("N:" + norm(c["name"]), c["name"])
    for r in REN:
        if y in r["ys"] and r["re"].search(n): return ("E:" + r["emp"], r["name"]) if r.get("emp") else ("N:" + norm(r["name"]), r["name"])
    for k, e in EMP.items():
        if e["re"].search(n): return ("E:" + k, e["name"])
    if s:
        for k, e in EMP.items():
            if e["re"].search(s): return ("E:" + k, e["name"])
    if not n.strip(): return (None, None)
    return ("N:" + norm(n), n)
def load(y):
    gj = f"{WORK}/hb_{y}.geojson"
    if not os.path.exists(gj):
        subprocess.run(["mapshaper", "-i", f"{MAPS}/w{y}.json", "-o", "format=geojson", gj], check=True, capture_output=True)
    fs = json.load(open(gj))["features"]
    out = []
    for f in fs:
        if not f.get("geometry"): continue
        g = make_valid(shape(f["geometry"]))
        k, label = owner(f["properties"], y)
        if not k: continue
        out.append((g, k, label, f["properties"].get("NAME")))
    return out
def km2(g):
    c = g.centroid; return g.area * (111.32 ** 2) * math.cos(math.radians(c.y))
pieces = []
for i, a in enumerate(YEARS):
    b = YEARS[i + 1] if i + 1 < len(YEARS) else NEXT[a]
    A, B = load(a), load(b)
    tree = STRtree([x[0] for x in B])
    for ga, ka, la, na in A:
        for j in tree.query(ga):
            gb, kb, lb, nb = B[j]
            if ka == kb: continue
            # name drift guard: same normalised plain name counts as same owner
            if ka[2:] == kb[2:] or (ka.startswith("N:") and kb.startswith("N:") and (ka[2:] in kb[2:] or kb[2:] in ka[2:])): continue
            try: x = ga.intersection(gb)
            except Exception: continue
            if x.is_empty: continue
            x = x.buffer(0)
            if x.is_empty: continue
            ar = km2(x)
            if ar < 15000: continue
            # sliver guard: compactness
            if x.area / max(1e-9, x.length ** 2) < 0.004: continue
            pieces.append(dict(a=a, b=b, frm=la, fk=ka, to=lb, tk=kb, tn=nb, ar=round(ar), lon=round(x.representative_point().x, 2), lat=round(x.representative_point().y, 2), geom=x))
    print(a, b, sum(1 for p in pieces if p["a"] == a), file=sys.stderr)
# merge pieces with the same (a, from, to)
M = {}
for p in pieces:
    k = (p["a"], p["fk"], p["tk"])
    if k in M: M[k]["geom"] = unary_union([M[k]["geom"], p["geom"]]); M[k]["ar"] += p["ar"]
    else: M[k] = p
out = sorted(M.values(), key=lambda p: (p["a"], -p["ar"]))
for p in out:
    rp = p["geom"].representative_point(); p["lon"], p["lat"] = round(rp.x, 2), round(rp.y, 2)
json.dump([{k: v for k, v in p.items() if k != "geom"} for p in out], open(f"{ROOT}/g2/pieces.json", "w"), indent=0)
# geometry as geojson for later topology build
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"id": i}, "geometry": mapping(p["geom"].simplify(0.05))} for i, p in enumerate(out)]}, open(f"{ROOT}/g2/pieces.geojson", "w"))
print(len(out), "pieces")
