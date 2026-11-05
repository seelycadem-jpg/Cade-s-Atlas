"""Province topology for the globe: maps/prov.json.
objects.p = provinces (id, n name, c country, ar km2, lp label point); objects.e = one line per shared border or
coast arc with the two provinces it separates (a, b; b=0 for a coast). Long straight cut lines (where a large region
was split) are roughened by midpoint displacement, the same on both sides because the arc is shared."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json, subprocess, math, random, sys, os
import numpy as np
from shapely.geometry import shape, LineString
random.seed(11)
subprocess.run(["mapshaper", "-i", WORK + "/g4/prov.geojson", "name=p", "-clean", "-simplify", "weighted", os.environ.get("KEEP", "30%"), "keep-shapes", "-o", "format=topojson", "quantization=2000000", WORK + "/g4/prov_raw.json"], check=True)
T = json.load(open(WORK + "/g4/prov_raw.json")); tr = T["transform"]; sx, sy = tr["scale"]; tx, ty = tr["translate"]
def dec(a):
    x = y = 0; o = []
    for p in a: x += p[0]; y += p[1]; o.append([x * sx + tx, y * sy + ty])
    return o
arcs = [dec(a) for a in T["arcs"]]
G = T["objects"]["p"]["geometries"]
use = {}
def walk(o, gi):
    if isinstance(o, list):
        for x in o: walk(x, gi)
    else: use.setdefault(o if o >= 0 else ~o, []).append(gi)
for gi, g in enumerate(G): walk(g.get("arcs", []), gi)
def rough(pts, depth=3):
    """midpoint displacement on long segments only (cut lines are long and straight; real borders are already detailed)"""
    out = [pts[0]]
    for i in range(1, len(pts)):
        a, b = pts[i - 1], pts[i]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 0.2: out.append(b); continue
        seg = [a, b]
        for d in range(depth):
            nxt = [seg[0]]
            for j in range(1, len(seg)):
                p, q = seg[j - 1], seg[j]; l = math.hypot(q[0] - p[0], q[1] - p[1])
                if l < 0.03: nxt.append(q); continue
                mx, my = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
                nx, ny = -(q[1] - p[1]) / l, (q[0] - p[0]) / l
                r = random.uniform(-0.22, 0.22) * l
                nxt += [[mx + nx * r, my + ny * r], q]
            seg = nxt
        out += seg[1:]
    return out
new = []
for k, a in enumerate(arcs):
    users = use.get(k, [])
    new.append(rough(a) if len(users) == 2 else a)
# edges object: one LineString per arc
E = []
for k in range(len(new)):
    us = use.get(k, [])
    if not us: continue
    pa = G[us[0]]["properties"]["id"]; pb = G[us[1]]["properties"]["id"] if len(us) > 1 else 0
    E.append({"type": "LineString", "arcs": [k], "properties": {"a": pa, "b": pb}})
T["objects"]["e"] = {"type": "GeometryCollection", "geometries": E}
T.pop("transform", None); T["arcs"] = [[[round(x, 5), round(y, 5)] for x, y in a] for a in new]
json.dump(T, open(WORK + "/g4/prov_r.json", "w"))
subprocess.run(["mapshaper", "-i", WORK + "/g4/prov_r.json", "-o", "format=topojson", "quantization=1000000", MAPS + "/prov.json"], check=True)
# label points and neighbours for the pipeline
from shapely.geometry import shape as sh
F = json.load(open(WORK + "/g4/prov.geojson"))["features"]
nb = {}
for e in E:
    a, b = e["properties"]["a"], e["properties"]["b"]
    if b: nb.setdefault(a, set()).add(b); nb.setdefault(b, set()).add(a)
json.dump({str(k): sorted(v) for k, v in nb.items()}, open(WORK + "/g4/nb.json", "w"))
print(len(G), "provinces", len(E), "edges", file=sys.stderr)
# ---- files for the globe: the map's worker loads the shapes itself; the page keeps only small tables ----
subprocess.run(["mapshaper", "-i", MAPS + "/prov.json", "-o", "format=geojson", "precision=0.0001", WORK + "/g4/out/"], check=True)
P = json.load(open(WORK + "/g4/out/p.json")); E = json.load(open(WORK + "/g4/out/e.json"))
for f in P["features"]: f["properties"] = {"id": f["properties"]["id"]}
for k, f in enumerate(E["features"]):
    c = f["geometry"]["coordinates"] if f.get("geometry") else []
    seam = 1 if (not c or all(abs(p[0]) > 179.99 for p in c) or all(p[1] < -59.9 for p in c)) else 0
    f["properties"] = {"id": k + 1, "b": 1 if f["properties"]["b"] else 0, "s": seam}
E["features"] = [f for f in E["features"] if f.get("geometry")]
# roughened arcs can cross themselves: repair those fills (the shared edges file keeps the arcs as drawn)
from shapely.geometry import shape as _s0, mapping as _m0, MultiPolygon as _MP
def _r4(o): return round(o, 4) if isinstance(o, float) else [_r4(x) for x in o] if isinstance(o, (list, tuple)) else o
for f in P["features"]:
    if not f.get("geometry"): continue
    g = _s0(f["geometry"])
    if g.is_valid: continue
    h = g.buffer(0); ps = [h] if h.geom_type == "Polygon" else [q for q in getattr(h, "geoms", []) if q.geom_type == "Polygon"]
    if ps: m = _m0(ps[0] if len(ps) == 1 else _MP(ps)); f["geometry"] = {"type": m["type"], "coordinates": _r4(m["coordinates"])}
json.dump(P, open(MAPS + "/prov_p.json", "w"), separators=(",", ":"))
json.dump(E, open(MAPS + "/prov_e.json", "w"), separators=(",", ":"))
from shapely.geometry import shape as _sh
ids = []; ar = []; cx = []; cy = []
for f in P["features"]:
    g = _sh(f["geometry"]) if f.get("geometry") else None
    rp = g.representative_point() if g is not None and not g.is_empty else None
    ids.append(f["properties"]["id"]); cx.append(round(rp.x, 3) if rp else 0); cy.append(round(rp.y, 3) if rp else 0)
pa = {g["properties"]["id"]: g["properties"].get("ar", 1) for g in json.load(open(WORK + "/g4/prov_raw.json"))["objects"]["p"]["geometries"]}
ar = [pa.get(i, 1) for i in ids]
EA = []; EB = []
Tt = json.load(open(MAPS + "/prov.json"))
for k, g in enumerate(Tt["objects"]["e"]["geometries"]):
    EA.append(g["properties"]["a"]); EB.append(g["properties"]["b"])
json.dump({"id": ids, "ar": ar, "cx": cx, "cy": cy, "ea": EA, "eb": EB}, open(MAPS + "/prov_meta.json", "w"), separators=(",", ":"))
