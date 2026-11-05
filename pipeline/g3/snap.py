"""One clean map per period (1400-1885).
For each span of years in which no recorded border changes, the polities alive are made into a single
coverage of the land: overlaps go to the smaller territory, every state is cut to the real coastline,
land within reach of a state that the record leaves uncovered (coastal strips, slivers between
neighbours) goes to the nearest state, and what is left is the peoples of the region.
Output: work/g3/snaps/s{a}.geojson per period, features with a, b (span), k (b|p) and row properties."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import WORK
import json, math, os, re, sys
from multiprocessing import Pool
from shapely.geometry import shape, mapping, MultiPolygon, Polygon, MultiPoint, box
from shapely.ops import unary_union, polylabel
from shapely.validation import make_valid
from shapely import STRtree, voronoi_polygons, prepare
OUT = os.environ.get("OUTS", WORK + "/g3/snaps"); os.makedirs(OUT, exist_ok=True)
D = 0.6  # how far (degrees) a state may be extended over land the record leaves empty
def polys(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def mp(ps): return ps[0] if len(ps) == 1 else MultiPolygon(ps)
def km2(g):
    if g.is_empty: return 0
    return abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
LANDF = json.load(open(WORK + "/g3/landgl.geojson"))["features"]
LANDP = [make_valid(shape(f["geometry"])) for f in LANDF]
LANDP = [p for g in LANDP for p in polys(g) if p.bounds[1] > -60]
LT = STRtree(LANDP)
def land_near(g):
    idx = LT.query(g)
    return unary_union([LANDP[j] for j in idx]) if len(idx) else Polygon()
ROWS = json.load(open(os.environ.get("ROWS", WORK + "/g3/rows.json")))  # written by build.py: base rows with properties and geometry
PEO = json.load(open(WORK + "/g3/peoples.json"))  # survey peoples and regional names with a, b
def work(span):
    a, b = span
    act = [r for r in ROWS if r["properties"]["a"] <= a and r["properties"]["b"] >= b]
    G = [make_valid(shape(r["geometry"])) for r in act]
    # overlaps: the smaller territory keeps the shared ground
    order = sorted(range(len(G)), key=lambda i: km2(G[i]))
    T = STRtree(G); out = {}
    for i in order:
        g = G[i]
        for j in T.query(g):
            if j == i or j not in out: continue
            if out[j].intersects(g):
                try: g = make_valid(g.difference(out[j]))
                except Exception: pass
        out[i] = g
    # cut to the coastline
    C = {}
    for i, g in out.items():
        if g.is_empty: continue
        try: c = make_valid(g.intersection(land_near(g)))
        except Exception: c = g
        ps = [p for p in polys(c) if km2(p) > 20]
        if ps: C[i] = mp(ps)
    if not C: return a, 0
    keys = list(C); U = unary_union([C[i] for i in keys])
    # land within reach of a state but outside every state: each piece to the nearest state (Voronoi of border points)
    reach = make_valid(land_near(U.buffer(D)).intersection(U.buffer(D)).difference(U))
    add = {i: [] for i in keys}
    if not reach.is_empty:
        pts, own = [], []
        for i in keys:
            for p in polys(C[i]):
                ring = p.exterior; L = ring.length; n = max(8, int(L / 0.08))
                for k in range(n):
                    q = ring.interpolate(k / n, normalized=True); pts.append((q.x, q.y)); own.append(i)
        seen = {}; 
        for (x, y), o in zip(pts, own): seen.setdefault((round(x, 3), round(y, 3)), o)
        pts = list(seen.keys()); own = list(seen.values())
        cells = None
        for tol in (0.001, 0.01, 0.05):
            try: cells = voronoi_polygons(MultiPoint(pts), tolerance=tol, extend_to=box(-200, -95, 200, 95)); break
            except Exception: continue
        if cells is None: reach = Polygon()
    if not reach.is_empty:
        cg = list(cells.geoms); ct = STRtree(cg)
        # match each cell to the point it was built from
        P = [__import__("shapely").geometry.Point(x) for x in pts]
        zone = {i: [] for i in keys}
        for k, p in enumerate(P):
            for c in ct.query(p):
                if cg[c].contains(p): zone[own[k]].append(cg[c]); break
        for part in polys(reach):
            prepare(part)
            for i in keys:
                if not zone[i]: continue
                zi = zone[i]
                hits = [z for z in zi if z.intersects(part)]
                if not hits: continue
                piece = make_valid(part.intersection(unary_union(hits)))
                if not piece.is_empty and km2(piece) > 5: add[i].append(piece)
    feats = []
    for i in keys:
        g = make_valid(unary_union([C[i]] + add[i])) if add[i] else C[i]
        ps = [p for p in polys(g) if km2(p) > 20]
        if not ps: continue
        g = mp(ps); big = max(ps, key=lambda q: q.area)
        try: lp = polylabel(big, 0.05)
        except Exception: lp = big.representative_point()
        pr = dict(act[i]["properties"]); pr.update({"a": a, "b": b, "k": "b", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(g)), "bl": round(km2(big))})
        feats.append({"type": "Feature", "properties": pr, "geometry": mapping(g)})
    # what is left: the peoples of the region, cut to the land outside every state
    S = unary_union([shape(f["geometry"]) for f in feats]) if feats else Polygon()
    for q in PEO:
        if not (q["a"] <= a and q["b"] >= b): continue
        g = make_valid(shape(q["geometry"]))
        try: g = make_valid(g.intersection(land_near(g)).difference(S))
        except Exception: continue
        ps = [p for p in polys(g) if km2(p) > 300]
        if not ps: continue
        g = mp(ps); big = max(ps, key=lambda x: x.area); lp = big.representative_point()
        feats.append({"type": "Feature", "properties": {"NAME": q["n"], "a": a, "b": b, "k": "p", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(g)), "bl": round(km2(big))}, "geometry": mapping(g)})
    json.dump({"type": "FeatureCollection", "features": feats}, open(f"{OUT}/s{a}.geojson", "w"))
    return a, len(feats)
def safe(span):
    try: return work(span)
    except Exception as e:
        print("failed", span, e, file=sys.stderr, flush=True); return span[0], -1
if __name__ == "__main__":
    bp = sorted({max(1400, r["properties"]["a"]) for r in ROWS} | {min(1886, r["properties"]["b"]) for r in ROWS} | {1886})
    bp = [x for x in bp if 1400 <= x <= 1886]
    spans = [(bp[i], bp[i + 1]) for i in range(len(bp) - 1)]
    todo = [s for s in spans if not os.path.exists(f"{OUT}/s{s[0]}.geojson")]
    json.dump(spans, open(os.environ.get("SPANS", WORK + "/g3/spans.json"), "w"))
    print(len(spans), "periods,", len(todo), "to do", file=sys.stderr)
    with Pool(2) as pool:
        for a, n in pool.imap_unordered(safe, todo):
            print(a, n, file=sys.stderr, flush=True)
