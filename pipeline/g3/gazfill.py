"""Fill every piece of land, as a grand-strategy map does.
For each period map (SRC/s{a}.geojson):
 1. open land = the peoples' land plus any land no feature covers (islands, slivers);
 2. polities from the researched gazetteer (/home/claude/review/gaz/*.json) that the period's map lacks take the open
    land around their seats: each gets the part of its researched extent (or reach) nearest its own seat;
 3. open land left that is not peoples' land (islands, slivers) goes to the nearest state within ISL degrees,
    otherwise to the nearest peoples' land; inland peoples' land stays as the peoples of its region.
Writes OUTS/s{a}.geojson; filled features carry fx='gaz' (approximate extent) or fx='isl'."""
import json, os, sys, glob, math
from multiprocessing import Pool
from shapely.geometry import shape, mapping, Point, MultiPolygon, Polygon, MultiPoint, box
from shapely.ops import unary_union, nearest_points
from shapely.validation import make_valid
from shapely import STRtree, voronoi_polygons, prepare
sys.path.insert(0, "/home/claude/review"); from names import same
SRC = os.environ.get("SRC", "/tmp/g3/snapsF2"); OUT = os.environ.get("OUTS", "/tmp/g3/snapsG"); os.makedirs(OUT, exist_ok=True)
SPANS = os.environ.get("SPANS", "/tmp/g3/spans_f.json")
ISL = 4.0  # an island goes to the nearest state within this many degrees
def polys(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def km2(g):
    return 0 if g.is_empty else abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def mp(ps): return ps[0] if len(ps) == 1 else MultiPolygon(ps)
LAND = [p for f in json.load(open("/tmp/g3/landgl.geojson"))["features"] for p in polys(make_valid(shape(f["geometry"]))) if p.bounds[1] > -60]
LT = STRtree(LAND)
# ---- gazetteer ----
GAZ = []
for f in sorted(glob.glob("/home/claude/review/gaz/*.json")):
    try: d = json.load(open(f))
    except Exception as e: print("bad gazetteer", f, e, file=sys.stderr); continue
    for p in d.get("polities", []):
        try:
            if p.get("from") is None or p.get("to") is None or not p.get("seat"): continue
            GAZ.append(p)
        except Exception: pass
def km_deg(lat): return 111.32 * max(.2, math.cos(math.radians(lat)))
def phase(p, y):
    """seat, area polygon (or None) for year y"""
    seat = p["seat"]; ext = p.get("extent"); reach = p.get("reach_km")
    for ph in p.get("phases") or []:
        try:
            if ph["from"] <= y < ph["to"]:
                seat = ph.get("seat") or seat; ext = ph.get("extent") or ext; reach = ph.get("reach_km") or reach
        except Exception: pass
    s = Point(seat["lon"], seat["lat"])
    area = None
    if ext and len(ext) >= 3:
        try:
            pts = [(q[1], q[0]) for q in ext] + [(s.x, s.y)]
            area = MultiPoint(pts).convex_hull.buffer(0.35, quad_segs=4)  # the sources' edge points, a little generous
        except Exception: area = None
    if area is None:
        r = (reach or 120) / km_deg(s.y)
        area = s.buffer(r, quad_segs=8)
    return s, make_valid(area)
def overlord(p, y):
    for o in p.get("overlord") or []:
        try:
            if o["from"] <= y < o["to"]: return o["name"]
        except Exception: pass
    return None
def work(span):
    a, b = span; mid = int((a + b) / 2)
    fc = json.load(open(f"{SRC}/s{a}.geojson")); F = fc["features"]
    G = [make_valid(shape(f["geometry"])) for f in F]
    S = [i for i, f in enumerate(F) if f["properties"].get("k") == "b"]
    P = [i for i, f in enumerate(F) if f["properties"].get("k") == "p"]
    T = STRtree(G)
    # 1. land no feature covers
    unc = []
    for lp in LAND:
        hit = [G[j] for j in T.query(lp) if G[j].intersects(lp)]
        if not hit: unc.append(lp); continue
        try:
            r = lp.difference(unary_union(hit))
            unc += [q for q in polys(make_valid(r)) if km2(q) > 1]
        except Exception: pass
    names = [F[i]["properties"].get("NAME") or "" for i in S]
    # 2. gazetteer polities the map lacks, on open land
    open_ = [G[i] for i in P] + unc
    OU = make_valid(unary_union(open_)) if open_ else Polygon()
    new = []
    if not OU.is_empty:
        cand = []
        for p in GAZ:
            try:
                if not (p["from"] <= mid < p["to"]): continue
            except Exception: continue
            if any(same(p["name"], n) for n in names): continue
            s, area = phase(p, mid)
            if not area.intersects(OU): continue
            cand.append((p, s, area))
        # a seat can be shared by successive names: keep one per seat
        seen = set(); c2 = []
        for c in cand:
            k = (round(c[1].x, 1), round(c[1].y, 1))
            if k in seen: continue
            seen.add(k); c2.append(c)
        cand = c2
        if cand:
            pts = MultiPoint([c[1] for c in cand])
            cells = list(voronoi_polygons(pts, extend_to=box(-200, -95, 200, 95)).geoms) if len(cand) > 1 else [box(-200, -95, 200, 95)]
            for c in cand:
                cell = next((v for v in cells if v.contains(c[1])), None)
                if cell is None: continue
                p, s, area = c
                try: piece = make_valid(OU.intersection(cell).intersection(area))
                except Exception: continue
                ps = [q for q in polys(piece) if km2(q) > 50]
                if not ps: continue
                # keep the parts connected to the seat's region: drop scraps far from the main body
                big = max(ps, key=lambda q: q.area)
                ps = [q for q in ps if q.distance(big) < 1.5 or q.distance(s) < 1.5]
                piece = mp(ps)
                OU = make_valid(OU.difference(piece))
                lp = s if piece.contains(s) else max(ps, key=lambda q: q.area).representative_point()
                pr = {"NAME": p["name"], "a": a, "b": b, "k": "b", "fx": "gaz", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(piece)),
                      "bl": round(km2(max(ps, key=lambda q: q.area))), "src": p.get("source")}
                ov = overlord(p, mid)
                if ov: pr["SUBJECTO"] = ov
                new.append((pr, piece))
    # peoples lose what the gazetteer took
    for i in P:
        try: G[i] = make_valid(G[i].intersection(OU)) if not OU.is_empty else Polygon()
        except Exception: pass
    # 3. islands and slivers left over: nearest state, else nearest peoples' land
    left = [q for u in unc for q in polys(make_valid(u.intersection(OU))) if km2(q) > 0.5] if not OU.is_empty else []
    owners = S + [("n", k) for k in range(len(new))]
    og = [G[i] for i in S] + [g for _, g in new]
    OT = STRtree(og) if og else None
    add = {}
    for q in left:
        best = None
        if OT is not None:
            for j in OT.query(q.buffer(ISL)):
                d = og[j].distance(q)
                if d <= ISL and (best is None or d < best[0]): best = (d, j)
        if best is None:
            pd = [(G[i].distance(q), i) for i in P if not G[i].is_empty]
            if pd:
                d, i = min(pd)
                if d < ISL: add.setdefault(("p", i), []).append(q)
            continue
        add.setdefault(("s", best[1]), []).append(q)
    for (kind, j), qs in add.items():
        if kind == "p": G[j] = make_valid(unary_union([G[j]] + qs)); continue
        if j < len(S): i = S[j]; G[i] = make_valid(unary_union([G[i]] + qs))
        else: pr, g = new[j - len(S)]; new[j - len(S)] = (pr, make_valid(unary_union([g] + qs)))
    out = []
    for i, f in enumerate(F):
        ps = [q for q in polys(G[i]) if km2(q) > 0.5]
        if not ps: continue
        f["geometry"] = mapping(mp(ps)); out.append(f)
    for pr, g in new:
        ps = [q for q in polys(g) if km2(q) > 0.5]
        if ps: out.append({"type": "Feature", "properties": pr, "geometry": mapping(mp(ps))})
    fc["features"] = out; json.dump(fc, open(f"{OUT}/s{a}.geojson", "w"))
    return a, len(new), len(left)
def safe(s):
    try: return work(s)
    except Exception as e:
        import traceback; traceback.print_exc(); print("fail", s, e, file=sys.stderr, flush=True)
        import shutil; shutil.copy(f"{SRC}/s{s[0]}.geojson", f"{OUT}/s{s[0]}.geojson"); return s[0], -1, -1
if __name__ == "__main__":
    spans = json.load(open(SPANS))
    only = [int(x) for x in sys.argv[1:]]
    if only: spans = [s for s in spans if s[0] in only]
    print(len(GAZ), "gazetteer polities", file=sys.stderr, flush=True)
    with Pool(2) as pool:
        for a, n, l in pool.imap_unordered(safe, spans): print(a, n, l, file=sys.stderr, flush=True)
