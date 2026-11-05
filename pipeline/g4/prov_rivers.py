"""River valleys as provinces of their own.
The first states were strips along rivers through desert (Nile, Tigris-Euphrates, Indus, Oxus, Jaxartes, Helmand,
the Sahelian Niger and Senegal, the Tarim, the Yellow River). A province that a listed river crosses is split into the
valley strip (within a few dozen km of the river) and the land beyond, so a valley state is drawn on its valley and
the desert beside it can belong to no one.
Reads and rewrites work/g4/prov.geojson (the original is kept as prov_base.geojson)."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json, math, os, shutil, sys
from shapely.geometry import shape, mapping, LineString, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
if not os.path.exists(WORK + "/g4/prov_base.geojson"): shutil.copy(WORK + "/g4/prov.geojson", WORK + "/g4/prov_base.geojson")
F = json.load(open(WORK + "/g4/prov_base.geojson"))["features"]
T = json.load(open(MAPS + "/phys.json"))
sx, sy = T["transform"]["scale"]; tx, ty = T["transform"]["translate"]
ARCS = []
for a in T["arcs"]:
    x = y = 0; pts = []
    for dx, dy in a: x += dx; y += dy; pts.append((x * sx + tx, y * sy + ty))
    ARCS.append(pts)
def arc(i): return ARCS[i] if i >= 0 else ARCS[~i][::-1]
# river, half-width of the valley in degrees, and where it counts (lon0, lon1, lat0, lat1)
RIV = {"Nile": .14, "Damietta Branch": .12, "Rosetta Branch": .12, "El Bahr el Abyad": .14, "El Bahr el Azraq": .14, "Atbara": .1,
       "Al Furat": .18, "Firat": .18, "Euphrates": .18, "Shatt al Arab": .18, "Gharraf Canal": .12, "Tigris": .18, "Dicle": .18,
       "Indus": .22, "Sutlej": .16, "Chenab": .16, "Amu  Darya": .16, "Syr Darya": .16, "Helmand": .12, "Tarim": .14,
       "Niger": .18, "Sénégal": .14, "Huang": .18, "Jordan": .08}
BOX = {"Nile": (20, 40, 9, 32), "El Bahr el Abyad": (20, 40, 9, 32), "Niger": (-12, 10, 13, 18), "Sénégal": (-17, -10, 14.5, 17.5),
       "Huang": (95, 115, 34, 42), "Indus": (60, 80, 22, 34)}
lines = []
for g in T["objects"]["rivers"]["geometries"]:
    nm = (g.get("properties") or {}).get("n")
    if nm not in RIV: continue
    parts = [g["arcs"]] if g["type"] == "LineString" else g["arcs"]
    for p in parts:
        pts = [q for i in p for q in arc(i)]
        if len(pts) < 2: continue
        L = LineString(pts)
        if nm in BOX:
            x0, x1, y0, y1 = BOX[nm]
            from shapely.geometry import box
            L = L.intersection(box(x0, y0, x1, y1))
            if L.is_empty: continue
        lines.append(L.buffer(RIV[nm], resolution=6))
VAL = make_valid(unary_union(lines))
print("valley area (deg2)", round(VAL.area, 1), file=sys.stderr)
def km2(g): return 0 if g.is_empty else abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    return [p for x in getattr(g, "geoms", []) for p in polys(x)]
out = []; ns = 0
for f in F:
    g = make_valid(shape(f["geometry"])); p = dict(f["properties"])
    if not g.intersects(VAL): out.append((p, g)); continue
    v = make_valid(g.intersection(VAL)); r = make_valid(g.difference(VAL))
    va, ra = km2(v), km2(r)
    vp = [q for q in polys(v) if km2(q) > 30]; rp = [q for q in polys(r) if km2(q) > 30]
    if not vp or not rp or va < 400 or ra < .25 * (va + ra): out.append((p, g)); continue
    out.append((dict(p, n=p["n"], ar=round(va), v=1), MultiPolygon(vp) if len(vp) > 1 else vp[0]))
    out.append((dict(p, n=p["n"], ar=round(ra)), MultiPolygon(rp) if len(rp) > 1 else rp[0])); ns += 1
feats = [{"type": "Feature", "properties": dict(p, id=i + 1), "geometry": mapping(g)} for i, (p, g) in enumerate(out)]
json.dump({"type": "FeatureCollection", "features": feats}, open(WORK + "/g4/prov.geojson", "w"))
print(ns, "provinces split along rivers;", len(feats), "provinces", file=sys.stderr)
