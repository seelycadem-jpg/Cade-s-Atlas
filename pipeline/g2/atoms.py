"""Cut each survey period (1400-1885) into atoms: the smallest pieces of land whose ruler is the same
for every year of the period. Every survey shape, dated change, hatched (undated) change and island or
area patch is overlaid into one flat mosaic; each atom then carries its ruler year by year.
The globe merges atoms by ruler for fills and labels and draws borders once, only between different
rulers - so no seams, no overlaps, no masking.

Writes atlas/maps/a{year}.json: topology "atoms", properties
  t  = [[year, owner, change], ...]   ruler from that year on (owner indexes `owners`, change indexes `changes` or -1)
  hz = index into `changes` of an undated change over this atom (hatched), or -1
  lp, ar = label point and area in km2
and top-level `owners` [[NAME, SUBJECTO, INF]] and `changes` [{y, t, frm, to, a, b, k}]."""
import json, subprocess, sys, math, os
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.ops import unary_union, polylabel
from shapely.validation import make_valid
from shapely import STRtree
M = "/home/claude/atlas/maps"
MAPY = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880]
NEXT = {y: (MAPY[i + 1] if i + 1 < len(MAPY) else 1886) for i, y in enumerate(MAPY)}
def gj(path, tmp):
    subprocess.run(["mapshaper", "-i", path, "-o", "format=geojson", tmp], check=True, capture_output=True)
    return json.load(open(tmp))["features"]
def km2(g):
    if g.is_empty: return 0
    return abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
PIECES = gj(f"{M}/pieces.json", "/tmp/at_pieces.geojson")
ISL = gj(f"{M}/islands.json", "/tmp/at_isl.geojson")
for my in MAPY:
    nx = NEXT[my]
    base = [f for f in gj(f"{M}/w{my}.json", f"/tmp/at_w{my}.geojson") if f.get("geometry") and (f["properties"].get("NAME") or "").strip()]
    pcs = [f for f in PIECES if f.get("geometry") and f["properties"].get("a") == my]
    isl = [f for f in ISL if f.get("geometry") and f["properties"]["a"] < nx and f["properties"]["b"] > my]
    src = []
    for i, f in enumerate(base): src.append({"type": "Feature", "properties": {"sid": f"b{i}"}, "geometry": f["geometry"]})
    for i, f in enumerate(pcs): src.append({"type": "Feature", "properties": {"sid": f"p{i}"}, "geometry": f["geometry"]})
    for i, f in enumerate(isl): src.append({"type": "Feature", "properties": {"sid": f"i{i}"}, "geometry": f["geometry"]})
    json.dump({"type": "FeatureCollection", "features": src}, open("/tmp/at_src.geojson", "w"))
    subprocess.run(["mapshaper", "-i", "/tmp/at_src.geojson", "snap", "-mosaic", "calc=ids=collect(sid)", "snap-interval=0.005",
                    "-o", "format=geojson", "/tmp/at_mos.geojson"], check=True, capture_output=True)
    mos = json.load(open("/tmp/at_mos.geojson"))["features"]
    owners, oix = [], {}
    def own(n, s, inf=None):
        key = (n, s or None, inf or None)
        if key not in oix: oix[key] = len(owners); owners.append(list(key))
        return oix[key]
    changes = []
    def chg(p, kind):
        q = p["properties"]
        changes.append({"y": q.get("y"), "t": q.get("t"), "frm": q.get("frm"), "to": q.get("to") or q.get("NAME"), "a": my, "b": nx, "k": kind})
        return len(changes) - 1
    pc_ch = {}
    atoms = []
    for f in mos:
        g = f.get("geometry")
        if not g: continue
        ids = f["properties"].get("ids") or []
        bs = [base[int(s[1:])] for s in ids if s[0] == "b"]
        ps = [int(s[1:]) for s in ids if s[0] == "p"]
        iss = sorted((int(s[1:]) for s in ids if s[0] == "i"))
        if not bs and not ps and not iss: continue
        bp = bs[0]["properties"] if bs else None
        t0 = own(bp["NAME"], bp.get("SUBJECTO"), bp.get("INF")) if bp else -1
        events = []  # (effective year, order, owner, change)
        hz = -1
        for j in ps:
            q = pcs[j]["properties"]
            if q.get("k") == "undated":
                if j not in pc_ch: pc_ch[j] = chg(pcs[j], "undated")
                hz = pc_ch[j]; continue
            if j not in pc_ch: pc_ch[j] = chg(pcs[j], "fix" if q.get("fx") else "dated")
            eff = my if q.get("fx") else max(my, int(q.get("y") or my))
            events.append((eff, 0 if q.get("fx") else 1, own(q.get("NAME"), q.get("SUBJECTO")), -1 if q.get("fx") else pc_ch[j]))
        events.sort(key=lambda e: (e[0], e[1]))
        # ruler year by year: base, then dated changes, then any island or area patch in force
        cuts = sorted({my} | {e[0] for e in events} | {max(my, isl[j]["properties"]["a"]) for j in iss} | {min(nx, isl[j]["properties"]["b"]) for j in iss})
        t = []
        for yy in cuts:
            if yy >= nx: continue
            o, c = t0, -1
            for e in events:
                if e[0] <= yy: o, c = e[2], (e[3] if e[0] == yy else c)
            for j in iss:
                q = isl[j]["properties"]
                if q["a"] <= yy < q["b"]: o, c = own(q["NAME"], q.get("SUBJECTO")), c
            if not t or t[-1][1] != o: t.append([yy, o, c])
        if not t or (len(t) == 1 and t[0][1] == -1): continue
        if iss: hz = -1  # a curated patch decides this land; no hatch over it
        atoms.append({"g": make_valid(shape(g)), "t": t, "hz": hz})
    # slivers between nearly coincident outlines take the timeline of the neighbour they share most edge with
    G = [a["g"] for a in atoms]; tree = STRtree(G); merged = 0
    for i, a in enumerate(atoms):
        if km2(a["g"]) > 40: continue
        best = None
        for j in tree.query(a["g"].buffer(0.01)):
            if j == i or km2(G[j]) <= 40: continue
            L = a["g"].boundary.intersection(G[j].buffer(0.01)).length
            if best is None or L > best[0]: best = (L, j)
        if best and best[0] > 0: a["t"] = atoms[best[1]]["t"]; a["hz"] = atoms[best[1]]["hz"]; merged += 1
    feats = []
    for a in atoms:
        ps = polys(a["g"])
        if not ps: continue
        big = max(ps, key=lambda p: p.area)
        try: lp = polylabel(big, 0.05)
        except Exception: lp = big.representative_point()
        feats.append({"type": "Feature", "properties": {"t": a["t"], "hz": a["hz"], "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(a["g"]))},
                      "geometry": mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))})
    json.dump({"type": "FeatureCollection", "features": feats}, open("/tmp/at_out.geojson", "w"))
    subprocess.run(["mapshaper", "-i", "/tmp/at_out.geojson", "name=atoms", "-o", "format=topojson", "precision=0.0005", "/tmp/at_out.json"], check=True, capture_output=True)
    T = json.load(open("/tmp/at_out.json"))
    T["owners"] = owners; T["changes"] = changes
    json.dump(T, open(f"{M}/a{my}.json", "w"), separators=(",", ":"), ensure_ascii=False)
    print(my, "atoms", len(feats), "owners", len(owners), "changes", len(changes), "slivers merged", merged, "kb", os.path.getsize(f"{M}/a{my}.json") // 1024, file=sys.stderr)
