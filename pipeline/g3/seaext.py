"""Extend every period-map shape a little way out to sea, so the globe can draw the coast from one exact
land layer (a sea mask over the states) instead of repeating the full coastline in every state of every period.
Each shape g becomes: (g simplified, buffered 0.12 deg) minus all land that is not g. Its inland borders stay
exact; its sea edge is a rough outline hidden under the mask. Output /tmp/g3/snapx/s{a}.geojson."""
import json, os, sys, hashlib
from multiprocessing import Pool
from shapely.geometry import shape, mapping, box, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
OUT = "/tmp/g3/snapx"; os.makedirs(OUT, exist_ok=True)
B = 0.12
LANDF = json.load(open("/tmp/g3/landgl.geojson"))["features"]
def polys(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
LANDP = [p for f in LANDF for p in polys(make_valid(shape(f["geometry"])))]
LT = STRtree(LANDP)
def extend(gj):
    g = make_valid(shape(gj))
    bb = box(*g.bounds).buffer(B + 0.05, join_style=2)
    near = [LANDP[j] for j in LT.query(bb)]
    try:
        L = make_valid(unary_union([p.intersection(bb) if not bb.contains(p) else p for p in near])) if near else None
        buf = g.simplify(0.01).buffer(B, quad_segs=2)
        sea = make_valid(bb.difference(L)) if L is not None else bb
        r = make_valid(g.union(buf.intersection(sea)))
        r = make_valid(r.buffer(2e-4, quad_segs=1, join_style=2).buffer(-2e-4, quad_segs=1, join_style=2))  # close hairline gaps along the coast
        r = make_valid(r.union(g))
        ps = [p for p in polys(r) if p.area > 1e-5]
        if not ps: return gj
        r = ps[0] if len(ps) == 1 else MultiPolygon(ps)
        return mapping(r)
    except Exception as e:
        print("fail", e, file=sys.stderr); return gj
def key(gj): return hashlib.md5(json.dumps(gj, sort_keys=True).encode()).hexdigest()
def job(item):
    k, gj = item; return k, extend(gj)
if __name__ == "__main__":
    spans = json.load(open("/tmp/g3/spans.json"))
    only = [int(x) for x in sys.argv[1:]]
    if only: spans = [s for s in spans if s[0] in only]
    files = {a: json.load(open(f"/tmp/g3/snaps/s{a}.geojson")) for a, b in spans}
    uniq = {}
    for fc in files.values():
        for f in fc["features"]: uniq.setdefault(key(f["geometry"]), f["geometry"])
    print(len(uniq), "unique shapes", file=sys.stderr, flush=True)
    done = {}
    with Pool(2) as pool:
        for i, (k, g) in enumerate(pool.imap_unordered(job, uniq.items(), chunksize=8)):
            done[k] = g
            if i % 500 == 0: print(i, file=sys.stderr, flush=True)
    for a, fc in files.items():
        for f in fc["features"]: f["geometry"] = done[key(f["geometry"])]
        json.dump(fc, open(f"{OUT}/s{a}.geojson", "w"))
    print("done", file=sys.stderr)
