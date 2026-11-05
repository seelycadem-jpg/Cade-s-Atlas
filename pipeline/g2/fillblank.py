"""Fill land that a survey map leaves blank. A blank area takes, in order of preference:
1. the polity drawn there on both the survey before and the survey after (it existed throughout);
2. a people drawn there on the survey before or after (peoples persist);
3. a broad regional name for the peoples of that land.
Every filled area is marked INF so the globe can say it was inferred."""
import json, re, subprocess, sys, math
from shapely.geometry import shape, mapping as _m, Polygon, MultiPolygon, box, Point
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
M = "/home/claude/atlas/maps"
YEARS = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914]
FILL_UNTIL = 1900  # later surveys only show through where the dated record has no state
PEOPLES = re.compile(r"hunter|gatherer|peoples|cultures|culture$|nomad|aboriginal|tribes|^maori$|^polynesians$|^papuans$|^inuit|^san$|^khoisan$|^siberians$|cereal farmers|chiefdoms|^bantu|herders|pastoralists|foragers|bedouin", re.I)
REGIONS = [  # last resort, by box; first match wins
 ((-11, 51.3, -5.4, 55.5), "Gaelic Irish lordships"),
 ((-25, 63, -13, 67), "Norse Icelanders"),
 ((14, 65, 45, 72), "Sámi"),
 ((-17, 14, 34, 33.5), "Saharan nomads (Tuareg, Moors, Tubu)"),
 ((34, 12, 60, 32), "Bedouin tribes"),
 ((-18, 3, 16, 14), "West African peoples"),
 ((28, -12, 52, 14), "East African peoples"),
 ((16, -5, 30, 14), "Central African peoples"),
 ((8, -35, 42, 3), "Bantu-speaking peoples"),
 ((-20, -36, 8, 3), "Bantu-speaking peoples"),
 ((44, 35, 92, 56), "Steppe nomads"),
 ((56, 50, 180, 80), "Siberian peoples"),
 ((-180, 50, -150, 75), "Siberian peoples"),
 ((92, 36, 125, 50), "Mongol and Turkic nomads"),
 ((-82, -22, -34, 13), "Amazonian peoples"),
 ((-76, -56, -50, -22), "Pampas and Patagonian peoples"),
 ((-75, 58, -10, 84), "Inuit"),
 ((-170, 14, -50, 76), "Indigenous nations"),
 ((112, -45, 155, -10), "Aboriginal nations"),
 ((95, -11, 180, 22), "Island peoples"),
 ((60, 5, 110, 40), "Hill and forest peoples"),
]
def km2(g):
    if g.is_empty: return 0
    return g.area * 111.32 ** 2 * math.cos(math.radians(g.centroid.y))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def mapping(g):
    ps = polys(g)
    return _m(ps[0] if len(ps) == 1 else MultiPolygon(ps)) if ps else None
land_gj = json.load(open("/tmp/land.geojson"))
geoms = land_gj["geometries"] if "geometries" in land_gj else [f["geometry"] for f in land_gj["features"]]
LAND = make_valid(unary_union([make_valid(shape(g)) for g in geoms]))
ANT = box(-180, -90, 180, -60)
def load(y):
    tmp = f"/tmp/fb_{y}.geojson"
    subprocess.run(["mapshaper", "-i", f"{M}/w{y}.json", "-o", "format=geojson", tmp], check=True, capture_output=True)
    fc = json.load(open(tmp))
    out = []
    for f in fc["features"]:
        if not f.get("geometry"): continue
        n = (f["properties"].get("NAME") or "").strip()
        out.append((make_valid(shape(f["geometry"])), n, f))
    return fc, out
cache = {y: load(y) for y in YEARS}
PEO = {}
for y in YEARS:
    L = [(g, n) for g, n, f in cache[y][1] if n and PEOPLES.search(n)]
    PEO[y] = (L, STRtree([g for g, n in L]))
for k, y in enumerate(YEARS):
    if y > FILL_UNTIL: break
    fc, F = cache[y]
    named = [(g, n) for g, n, f in F if n]
    U = unary_union([g for g, n in named])
    gaps = [p for p in polys(make_valid(LAND.difference(U).difference(ANT))) if km2(p) > 4000]
    prev = cache[YEARS[k - 1]][1] if k > 0 else []
    nxt = cache[YEARS[k + 1]][1] if k + 1 < len(YEARS) else []
    def fe(lst):
        L = [(g, n) for g, n, f in lst if n]
        return L, STRtree([g for g, n in L])
    PV, TV = fe(prev); NX, TN = fe(nxt)
    added = []
    for gp in gaps:
        rest = gp
        # 1 and 2: take pieces from the neighbouring surveys
        for (L, T, other, otherT, people_only) in ((PV, TV, NX, TN, False), (NX, TN, PV, TV, True), (PV, TV, None, None, True)):
            if rest.is_empty: break
            for j in T.query(rest):
                g, n = L[j]
                try: piece = make_valid(rest.intersection(g))
                except Exception: continue
                if km2(piece) < 3000: continue
                ok = PEOPLES.search(n) is not None
                if not ok and not people_only and other is not None:
                    c = piece.representative_point()
                    ok = any(other[i][1] == n and other[i][0].contains(c) for i in otherT.query(c))
                if not ok: continue
                added.append((piece, n, "survey"))
                rest = make_valid(rest.difference(g))
                if rest.is_empty: break
        # 2b: peoples drawn on any other survey, nearest in time first
        if not rest.is_empty:
            for yy in sorted([z for z in YEARS if z != y and z <= 1900], key=lambda z: abs(z - y)):
                if rest.is_empty or km2(rest) < 3000: break
                L, T = PEO[yy]
                for j in T.query(rest):
                    g, n = L[j]
                    try: piece = make_valid(rest.intersection(g))
                    except Exception: continue
                    if km2(piece) < 3000: continue
                    added.append((piece, n, "survey")); rest = make_valid(rest.difference(g))
                    if rest.is_empty: break
        # 2c: a polity the nearest survey draws there (Naples and Crimea are blank on the survey of 1400)
        if not rest.is_empty:
            near = sorted([(abs(YEARS[k - 1] - y), PV, TV)] if k > 0 else [], key=lambda t: t[0]) + ([(abs(YEARS[k + 1] - y), NX, TN)] if k + 1 < len(YEARS) else [])
            for _, L, T in sorted(near, key=lambda t: t[0]):
                if rest.is_empty or km2(rest) < 3000: break
                for j in T.query(rest):
                    g, n = L[j]
                    try: piece = make_valid(rest.intersection(g))
                    except Exception: continue
                    if km2(piece) < 3000: continue
                    added.append((piece, n, "survey")); rest = make_valid(rest.difference(g))
                    if rest.is_empty: break
        # 3: what is left goes whole to the broad region its centre falls in
        for part in polys(rest):
            if km2(part) < 1500: continue
            c = part.representative_point()
            for bx, name in REGIONS:
                if box(*bx).contains(c): added.append((part, name, "region")); break
    # merge additions by name and write them into the survey map
    byname = {}
    for g, n, how in added: byname.setdefault((n, how), []).append(g)
    for (n, how), gs in byname.items():
        g = make_valid(unary_union(gs))
        m = mapping(g)
        if m: fc["features"].append({"type": "Feature", "properties": {"NAME": n, "SUBJECTO": None, "INF": how}, "geometry": m})
    json.dump(fc, open(f"/tmp/fb_{y}_out.geojson", "w"))
    subprocess.run(["mapshaper", "-i", f"/tmp/fb_{y}_out.geojson", f"name=world_{y}", "-simplify", "60%", "weighted", "keep-shapes", "-o", "format=topojson", "precision=0.001", f"{M}/w{y}.json"], check=True, capture_output=True)
    print(y, "blank areas", len(gaps), "filled", len(byname), "groups:", ", ".join(sorted({n for (n, h) in byname}))[:300], file=sys.stderr)
