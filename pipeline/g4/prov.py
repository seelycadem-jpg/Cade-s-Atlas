"""The province map: one fixed division of the world's land into provinces, made once.
Starts from the modern first-level regions (Natural Earth admin-1, 10m), merges small regions within a country and
splits large ones into parts of even size, so a province is about 5,000 km2 in the old, dense cores (Europe, the
Mediterranean, the Middle East, India, China, Japan, Java), about 20,000 km2 elsewhere and up to 80,000 km2 in
desert, tundra and ice. Islands far from their region's main body become provinces of their own when large enough.
Output work/g4/prov.geojson (id, name, country, area) for the topology step."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import WORK
import json, math, sys, random, os
import numpy as np
from shapely.geometry import shape, mapping, Point, MultiPolygon, Polygon, MultiPoint, box
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree, voronoi_polygons, prepare, contains_xy
os.makedirs(WORK + "/g4", exist_ok=True)
random.seed(7); np.random.seed(7)
def km2(g): return 0 if g.is_empty else abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def polys(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def mp(ps): return ps[0] if len(ps) == 1 else MultiPolygon(ps)
# target province size (km2) by place
CORE = [(-12, 34, 45, 62), (25, 12, 62, 42), (66, 6, 92, 36), (98, 18, 123, 42), (125, 30, 146, 46), (104, -9, 116, -5), (28, 22, 34, 32), (124, 33, 130, 43)]
SPARSE = [(-180, 62, 180, 90), (-18, 17, 33, 31), (42, 15, 56, 27), (118, -32, 144, -19), (124, -28, 138, -20), (-75, 60, -10, 85), (55, 38, 90, 50), (88, 40, 120, 48), (-120, 55, -60, 62), (75, 31, 98, 37)]
def target(pt):
    x, y = pt.x, pt.y
    if any(a <= x <= c and b <= y <= d for a, b, c, d in CORE): return 5000
    if any(a <= x <= c and b <= y <= d for a, b, c, d in SPARSE): return 80000
    if y < -60: return 1e12
    return 20000
d = json.load(open(WORK + "/nev/geojson/ne_10m_admin_1_states_provinces.geojson"))
U = []
for f in d["features"]:
    p = f["properties"]
    g = make_valid(shape(f["geometry"]))
    if g.is_empty or g.bounds[3] < -60: continue
    U.append({"name": p.get("name") or "", "country": p.get("admin") or "", "iso": p.get("adm0_a3") or "", "g": g})
print(len(U), "regions", file=sys.stderr)
# ---- 1. islands far from their region's main body become regions of their own ----
V = []
for u in U:
    ps = polys(u["g"])
    if len(ps) == 1: V.append(u); continue
    big = max(ps, key=lambda q: q.area); main = [big]; rest = []
    for q in ps:
        if q is big: continue
        (main if q.distance(big) < 0.25 else rest).append(q)
    # group outlying islands into clusters (an archipelago is one region)
    groups = []
    for q in rest:
        for gq in groups:
            if any(q.distance(x) < 0.4 for x in gq): gq.append(q); break
        else: groups.append([q])
    V.append(dict(u, g=mp(main)))
    for gq in groups:
        V.append(dict(u, g=mp(gq), name=u["name"] + " islands"))
print(len(V), "regions after islands", file=sys.stderr)
# ---- 2. merge small regions with a neighbour in the same country ----
for v in V: v["ar"] = km2(v["g"]); v["T"] = target(v["g"].representative_point())
alive = list(range(len(V)))
T = STRtree([v["g"] for v in V])
changed = True; rounds = 0
while changed and rounds < 8:
    changed = False; rounds += 1
    order = sorted([i for i in alive if V[i] is not None and V[i]["ar"] < V[i]["T"] * 0.45], key=lambda i: V[i]["ar"])
    for i in order:
        v = V[i]
        if v is None or v["ar"] >= v["T"] * 0.45: continue
        best = None
        for j in T.query(v["g"].buffer(0.02)):
            w = V[j]
            if j == i or w is None or w["country"] != v["country"]: continue
            if w["g"].distance(v["g"]) > 0.02: continue
            score = w["ar"]
            if best is None or score < best[0]: best = (score, j)
        if best is None: continue
        j = best[1]; w = V[j]
        if w["ar"] + v["ar"] > w["T"] * 1.4: continue
        w["g"] = make_valid(unary_union([w["g"], v["g"]])); w["ar"] += v["ar"]
        if v["ar"] > w["ar"] * .5: w["name"] = w["name"] + "–" + v["name"]
        V[i] = None; changed = True
    alive = [i for i in alive if V[i] is not None]
    T = STRtree([V[i]["g"] for i in alive]); idx = {k: i for k, i in enumerate(alive)}
    # remap tree indices to V indices
    class _T:
        def __init__(s, t, m): s.t, s.m = t, m
        def query(s, g): return [s.m[k] for k in s.t.query(g)]
    T = _T(T, idx)
R = [V[i] for i in alive]
print(len(R), "regions after merging", file=sys.stderr)
# ---- 3. split large regions into parts of even size (k-means seeds, Voronoi cells) ----
def kmeans(P, k, it=25):
    C = P[np.random.choice(len(P), k, replace=False)]
    for _ in range(it):
        D = ((P[:, None, :] - C[None, :, :]) ** 2).sum(-1); L = D.argmin(1)
        for c in range(k):
            m = P[L == c]
            if len(m): C[c] = m.mean(0)
    return C
out = []
for v in R:
    n = int(round(v["ar"] / v["T"]))
    if n <= 1: out.append(v); continue
    n = min(n, 400)
    g = v["g"]; x0, y0, x1, y1 = g.bounds
    prepare(g)
    # sample points inside, in an equal-area frame
    m = 0; P = []
    while len(P) < max(60 * n, 400) and m < 40:
        xs = np.random.uniform(x0, x1, 4000); ys = np.random.uniform(y0, y1, 4000)
        ok = contains_xy(g, xs, ys); P += list(zip(xs[ok], ys[ok])); m += 1
    if len(P) < n * 3: out.append(v); continue
    P = np.array(P); lat = math.cos(math.radians(g.representative_point().y))
    Q = P.copy(); Q[:, 0] *= lat
    C = kmeans(Q, n); C[:, 0] /= lat
    cells = voronoi_polygons(MultiPoint([tuple(c) for c in C]), extend_to=box(x0 - 1, y0 - 1, x1 + 1, y1 + 1))
    k = 0
    for cell in cells.geoms:
        piece = make_valid(g.intersection(cell)); ps = [q for q in polys(piece) if km2(q) > 0.5]
        if not ps: continue
        k += 1
        out.append(dict(v, g=mp(ps), name=f"{v['name']} {k}" if n > 1 else v["name"], ar=km2(mp(ps))))
feats = []
for i, v in enumerate(out):
    feats.append({"type": "Feature", "properties": {"id": i + 1, "n": v["name"], "c": v["country"], "iso": v["iso"], "ar": round(v["ar"])}, "geometry": mapping(v["g"])})
json.dump({"type": "FeatureCollection", "features": feats}, open(WORK + "/g4/prov.geojson", "w"))
A = sorted(f["properties"]["ar"] for f in feats)
print(len(feats), "provinces; median", A[len(A) // 2], "km2; p10", A[len(A) // 10], "p90", A[int(.9 * len(A))], file=sys.stderr)
