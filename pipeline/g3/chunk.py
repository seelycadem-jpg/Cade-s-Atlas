"""Twenty-year chunks of period maps for the GPU globe, with smoothed borders.
Each chunk is one topology, so a border shared by two states is a single line: the stair-steps the source
maps carry (they were traced from scans) are removed by simplifying and then rounding (Chaikin) every inland
border once, which keeps neighbours meeting exactly. Coastlines are left as the real coast."""
import json, os, subprocess, sys
import numpy as np
from shapely.geometry import shape, LineString
from shapely.ops import unary_union
from shapely import prepare, contains_xy
IN = os.environ.get("SNAPS","/tmp/g3/snaps"); OUT = os.environ.get("OUTG","/home/claude/atlas/maps/g"); ONLY=[int(x) for x in sys.argv[1:]]; os.makedirs(OUT, exist_ok=True)
STEP = 20
SMT = float(os.environ.get('SMT', '0.004'))  # rounded borders keep a point only where it bends by more than this (degrees)
spans = json.load(open(os.environ.get("SPANS", "/tmp/g3/spans.json")))
feats = []
for a, b in spans:
    fn = f"{IN}/s{a}.geojson"
    if not os.path.exists(fn): print("missing", a, file=sys.stderr); continue
    for f in json.load(open(fn))["features"]:
        f["properties"]["id"] = len(feats) + 1; feats.append(f)
land = json.load(open("/tmp/g3/landgl.geojson"))["features"]
coast = unary_union([shape(f["geometry"]).boundary for f in land]).buffer(2e-4)
prepare(coast)
LANDU = unary_union([shape(f["geometry"]) for f in land]); prepare(LANDU)
def chaikin(pts, n=2):
    for _ in range(n):
        out = [pts[0]]
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            out += [(.75 * x0 + .25 * x1, .75 * y0 + .25 * y1), (.25 * x0 + .75 * x1, .25 * y0 + .75 * y1)]
        out.append(pts[-1]); pts = out
    return pts
index = []; smoothed = kept = seac = 0
for s in range(1400, 1886, STEP):
    e = min(1886, s + STEP)
    if ONLY and s not in ONLY: index.append([s, e]); continue
    sel = [f for f in feats if f["properties"]["a"] < e and f["properties"]["b"] > s]
    json.dump({"type": "FeatureCollection", "features": sel}, open(f"/tmp/g3/k{s}.geojson", "w"))
    subprocess.run(["mapshaper", "-i", f"/tmp/g3/k{s}.geojson", "name=c", "-o", "format=topojson", "precision=0.00001", f"/tmp/g3/k{s}.topo.json"], check=True, capture_output=True)
    T = json.load(open(f"/tmp/g3/k{s}.topo.json"))
    tr = T.get("transform")
    def dec(arc):
        if not tr: return [tuple(p[:2]) for p in arc]
        x = y = 0; o = []
        for p in arc: x += p[0]; y += p[1]; o.append((x * tr["scale"][0] + tr["translate"][0], y * tr["scale"][1] + tr["translate"][1]))
        return o
    arcs = [dec(a) for a in T["arcs"]]; T.pop("transform", None)
    new = []
    for arc in arcs:
        xy = np.array(arc)
        onc = contains_xy(coast, xy[:, 0], xy[:, 1])
        if len(arc) < 3 or onc.all(): new.append([list(p) for p in arc]); kept += 1; continue
        if IN != "/tmp/g3/snaps":
            sea = ~onc & ~contains_xy(LANDU, xy[:, 0], xy[:, 1])
            if sea.any():
                # an outline out at sea, hidden under the sea mask: rough is fine (exact where it runs along a coast)
                tol = 0.03 if not onc.any() else 0.002
                ls = LineString(arc).simplify(tol, preserve_topology=False); pts = list(ls.coords) if len(ls.coords) >= 2 else [arc[0], arc[-1]]
                pts[0], pts[-1] = arc[0], arc[-1]; new.append([[round(x, 4), round(y, 4)] for x, y in pts]); seac += 1; continue
        ls = LineString(arc).simplify(0.1, preserve_topology=False)
        pts = list(ls.coords) if len(ls.coords) >= 2 else [arc[0], arc[-1]]
        pts[0], pts[-1] = arc[0], arc[-1]
        sm = LineString(chaikin(pts, 3)).simplify(SMT); new.append([[round(x, 5), round(y, 5)] for x, y in sm.coords]); smoothed += 1
    T["arcs"] = new
    # neighbours alive together: geometries that share an arc
    G = T["objects"]["c"]["geometries"]; users = {}
    def walk(o, gi):
        if isinstance(o, list):
            for x in o: walk(x, gi)
        else: users.setdefault(o if o >= 0 else ~o, set()).add(gi)
    for gi, g in enumerate(G): walk(g.get("arcs", []), gi)
    nb = [set() for _ in G]
    for us in users.values():
        us = list(us)
        for i in us:
            for j in us:
                if i != j:
                    p, q = G[i]["properties"], G[j]["properties"]
                    if p["a"] < q["b"] and q["a"] < p["b"]: nb[i].add(q["id"])
    for gi, g in enumerate(G): g["properties"]["nb"] = sorted(nb[gi])
    json.dump(T, open(f"/tmp/g3/k{s}.sm.json", "w"))
    subprocess.run(["mapshaper", "-i", f"/tmp/g3/k{s}.sm.json", "-o", "format=topojson", "quantization=400000", f"{OUT}/c{s}.json"], check=True, capture_output=True)
    index.append([s, e])
    print(s, len(sel), os.path.getsize(f"{OUT}/c{s}.json") // 1024, "kb", file=sys.stderr, flush=True)
json.dump({"step": STEP, "chunks": index}, open(f"{OUT}/index.json", "w"))
print("features", len(feats), "arcs smoothed", smoothed, "coast arcs kept", kept, "sea arcs", seac)
