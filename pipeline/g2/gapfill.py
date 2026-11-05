"""Close the gaps between the survey maps and the coastline: land that no polity covers,
and unnamed slivers, are merged into the neighbour that shares the longest edge.
Large blank areas (genuinely outside any recorded polity) are left alone."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json, subprocess, sys, math, os
from shapely.geometry import shape, mapping as _mapping, MultiPolygon, Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
M = MAPS
YEARS = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914, 1920, 1930, 1938, 1945, 1960, 1994, 2000, 2010]
land_gj = json.load(open(WORK + "/land.geojson"))
geoms = land_gj["geometries"] if "geometries" in land_gj else [f["geometry"] for f in land_gj["features"]]
LAND = make_valid(unary_union([make_valid(shape(g)) for g in geoms]))
COAST = LAND.boundary.buffer(0.35)
def km2(g):
    if g.is_empty: return 0
    return g.area * 111.32 ** 2 * math.cos(math.radians(g.centroid.y))
def mapping(g):
    ps = polys(g)
    if not ps: return None
    return _mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
for y in YEARS:
    src = f"{M}/w{y}.json"; tmp = f"{WORK}/gf_{y}.geojson"
    subprocess.run(["mapshaper", "-i", src, "-o", "format=geojson", tmp], check=True, capture_output=True)
    fc = json.load(open(tmp)); F = fc["features"]
    G = []
    for f in F:
        g = make_valid(shape(f["geometry"])) if f.get("geometry") else Polygon()
        G.append(g)
    named = [i for i, f in enumerate(F) if (f["properties"].get("NAME") or "").strip()]
    U = unary_union([G[i] for i in named])
    gaps = polys(make_valid(LAND.difference(U)))
    tree = STRtree([G[i] for i in named])
    add = {i: [] for i in named}; merged = 0; kept = 0
    for gp in gaps:
        a = km2(gp)
        if a < 1: continue
        thin = gp.area / max(1e-9, gp.length ** 2)
        if a > 250000 or (a > 40000 and thin > 0.02): kept += 1; continue  # a real blank area
        ring = gp.buffer(0.03)
        best, bl = None, 0
        for j in tree.query(ring):
            i = named[j]
            try: l = ring.intersection(G[i].boundary).length
            except Exception: continue
            if l > bl: best, bl = i, l
        if best is None: kept += 1; continue
        add[best].append(gp); merged += 1
    for i, ps in add.items():
        if not ps: continue
        g = make_valid(unary_union([G[i]] + [p.buffer(0.005) for p in ps]))
        F[i]["geometry"] = mapping(g)
    # inland spurs: thin corridors drawn across deserts and steppe on the older surveys are trimmed
    if y <= 1880:
        trimmed = 0
        G2 = [make_valid(shape(F[i]['geometry'])) if F[i].get('geometry') else Polygon() for i in named]; tree2 = STRtree(G2)
        for i in named:
            g = make_valid(shape(F[i]["geometry"])) if F[i].get("geometry") else None
            if g is None or g.is_empty or km2(g) < 60000: continue
            try:
                core = g.buffer(-1.3).buffer(1.3)
                spur = make_valid(g.difference(core))
            except Exception: continue
            cut = []
            others = None
            for sp in polys(make_valid(spur.difference(COAST))):  # keep the strip along every coast
                if km2(sp) < 3000: continue
                # trim only corridors that run out into unclaimed land, never arms wedged between neighbours
                if others is None:
                    others = [G2[j] for j in tree2.query(g.buffer(0.1)) if named[j] != i]
                    others = unary_union(others) if others else Polygon()
                b = sp.boundary
                shared = b.intersection(others.buffer(0.06)).length / max(1e-9, b.length) if not others.is_empty else 0
                # and only where the corridor's sides face open land, not its own coast (a peninsula such as Naples)
                own = make_valid(g.difference(sp)).buffer(0.06)
                selfs = b.intersection(own).length / max(1e-9, b.length)
                if shared < 0.25 and selfs < 0.4: cut.append(sp)
            if cut:
                g2 = make_valid(g.difference(unary_union([c.buffer(0.01) for c in cut])))
                if not g2.is_empty: F[i]["geometry"] = mapping(g2); trimmed += len(cut)
        print(y, "inland spurs trimmed", trimmed, file=sys.stderr)
    # drop unnamed slivers that now sit inside named land
    keepF = [f for i, f in enumerate(F) if i in add or km2(G[i]) > 40000]
    fc["features"] = keepF
    json.dump(fc, open(tmp, "w"))
    subprocess.run(["mapshaper", "-i", tmp, f"name=world_{y}", "-simplify", "18%", "weighted", "keep-shapes", "-o", "format=topojson", "precision=0.001", src], check=True, capture_output=True)
    print(y, "gaps merged", merged, "kept", kept, file=sys.stderr)
