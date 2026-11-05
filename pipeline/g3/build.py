"""Chunks for the GPU globe, 1400-1885.
Each chunk file maps/g/c{start}.json holds the polities (base territories), the unions they belong to
(drawn as an outer border and named at low zoom) and the peoples' lands that show where no state was,
for every row alive in [start, start+STEP). Feature properties:
  id, NAME, SUBJECTO (the union or overlord, when the territory is a member rather than the core), AKA (the
  name the older surveys give the same land, for profiles), a, b (first year, year after the last), lp, ar, bl, k (b|u|p)."""
import json, re, math, os, subprocess, sys
from shapely.geometry import shape, mapping
from shapely.ops import polylabel
from shapely.validation import make_valid
from shapely import STRtree
OUT = "/home/claude/atlas/maps/g"; os.makedirs(OUT, exist_ok=True)
STEP = 20
base = json.load(open("/tmp/g3/base_s.geojson"))["features"]
agg = json.load(open("/tmp/g3/agg_s.geojson"))["features"]
def km2(g):
    if g.is_empty: return 0
    return abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def clean(n): return re.sub(r"^\((.*)\)$", r"\1", n)
# ---- unions and overlords ----
U = [f for f in agg if f["properties"]["ty"] == "POLITY"]
REL = [f["properties"] for f in agg if f["properties"]["ty"] == "RELATION"]
umem = {}  # union name -> list of (a,b,mem)
for f in U:
    p = f["properties"]; umem.setdefault(p["n"], []).append((p["a"], p["b"], p.get("mem") or ""))
def top_union(name, a, b):
    """follow MemberOf upward to the outermost union alive over [a,b)"""
    seen = set(); cur = name
    while True:
        rows = [m for (x, y, m) in umem.get(cur, []) if x < b and y > a]
        nxt = next((s for m in rows for s in m.split(";") if s.strip() and s.strip() not in seen), None)
        if not nxt: return cur
        seen.add(cur); cur = nxt.strip()
COLONIAL = re.compile(r"Empire$|Colonial|Coloni|Africa|India|Indies|America|^New |Viceroyalty|Raj$|Company|Guinea|Gold Coast|Ceylon|Canada|Louisiana|Florida|Brazil|Peru|Plata|Granada|Philippines|Formosa|Cape|Algeria|Senegal|Cochinchina|Australia|Zealand", re.I)
def overlord(p):
    n = p["n"]; a, b = p["a"], p["b"]
    for r in REL:
        m = re.match(r"\(Vassalage of (.+) to (.+)\)$", r["n"])
        if m and m.group(1) == n and r["a"] < b and r["b"] > a and (min(b, r["b"]) - max(a, r["a"])) * 2 >= (b - a): return m.group(2)
    mem = [s.strip() for s in (p.get("mem") or "").split(";") if s.strip()]
    if not mem: return None
    top = clean(top_union(mem[0], a, b))
    core = re.sub(r"^(Kingdom of |Crown of |Bourbon Kingdom of )", "", top)
    # the core of a union is the territory of the same name; the rest are members
    if clean(n) == top: return None
    if top in ("Holy Roman Empire", "Kalmar Union", "Polish-Lithuania Kingdom", "Delhi Sultanate"): return top
    if core.split()[0].lower() in n.lower() and not COLONIAL.search(n): return None
    return top
# ---- the older surveys' names for the same land (profiles are keyed to them) ----
MAPY = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880]
def mapYear(y): return max(m for m in MAPY if m <= y)
SV = {}
def survey(my):
    if my not in SV:
        subprocess.run(["mapshaper", "-i", f"/home/claude/atlas/maps/w{my}.json", "-o", "format=geojson", f"/tmp/g3/w{my}.geojson"], check=True, capture_output=True)
        F = [(make_valid(shape(f["geometry"])), f["properties"].get("NAME") or "") for f in json.load(open(f"/tmp/g3/w{my}.geojson"))["features"] if f.get("geometry")]
        F = [(g, n) for g, n in F if n]
        SV[my] = (F, STRtree([g for g, n in F]))
    return SV[my]
PEOPLES = re.compile(r"hunter|gatherer|peoples|cultures|culture$|nomad|aboriginal|tribes|^maori$|^polynesians$|^papuans$|^inuit|^san$|^khoisan$|^siberians$|cereal farmers|chiefdoms|^bantu|herders|pastoralists|foragers|bedouin|indigenous|nations$", re.I)
src = open("/home/claude/g2/fillblank.py").read()
REGIONS = eval(src[src.index("REGIONS = [") + len("REGIONS = "): src.index("]\ndef km2") + 1])
land = json.load(open("/tmp/land.geojson"))
# a generous, simplified coastline: it cuts away land drawn far out to sea, while each record keeps its own coast
LANDP = [make_valid(make_valid(shape(g)).simplify(0.05).buffer(0.15)) for g in land["geometries"]]; LT = STRtree(LANDP)
def onland(g):
    parts = [LANDP[j] for j in LT.query(g)]
    if not parts: return g
    from shapely.ops import unary_union as _uu
    try:
        r = make_valid(g.intersection(_uu(parts)))
        return r if not r.is_empty else g
    except Exception: return g
rows = []
for f in base:
    p = f["properties"]
    g = make_valid(shape(f["geometry"])) if f.get("geometry") else None
    if g is None or g.is_empty: continue
    g = onland(g); ps = polys(g)
    if not ps: continue
    f["geometry"] = mapping(ps[0] if len(ps) == 1 else __import__("shapely.geometry", fromlist=["MultiPolygon"]).MultiPolygon(ps)); big = max(ps, key=lambda q: q.area)
    try: lp = polylabel(big, 0.05)
    except Exception: lp = big.representative_point()
    F, T = survey(mapYear(p["a"]))
    aka, best = None, 0
    for j in T.query(g):
        h, n = F[j]
        try: inter = km2(g.intersection(h))
        except Exception: continue
        iou = inter / max(1, km2(g) + km2(h) - inter)
        if iou > best: best, aka = iou, n
    ov = overlord(p)
    props = {"NAME": p["n"], "a": p["a"], "b": p["b"], "k": "b", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(g)), "bl": round(km2(big))}
    if ov and ov != p["n"]: props["SUBJECTO"] = ov
    if aka and best >= .35 and aka != p["n"]: props["AKA"] = aka
    if p.get("wd"): props["wd"] = p["wd"]
    rows.append({"type": "Feature", "properties": props, "geometry": f["geometry"]})
unions = []
for f in U:
    p = f["properties"]
    if p.get("mem") or not f.get("geometry"): continue
    g = make_valid(shape(f["geometry"])); ps = polys(g)
    if not ps: continue
    big = max(ps, key=lambda q: q.area)
    try: lp = polylabel(big, 0.05)
    except Exception: lp = big.representative_point()
    unions.append({"type": "Feature", "properties": {"NAME": clean(p["n"]), "a": p["a"], "b": p["b"], "k": "u", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(g)), "bl": round(km2(big))}, "geometry": f["geometry"]})
# peoples' lands from the surveys, shown only where no state is drawn above them
peoples = []
for i, my in enumerate(MAPY):
    nx = MAPY[i + 1] if i + 1 < len(MAPY) else 1886
    F, T = survey(my)
    for g0, n0 in F:
      for g in (polys(g0) if not PEOPLES.search(n0) else [g0]):
        n = n0
        if not PEOPLES.search(n):
            # land a survey gives to a state the reference record does not draw: shown, faintly, as the peoples of its region (part by part)
            c = g.representative_point(); n = next((nm for bx, nm in REGIONS if bx[0] <= c.x <= bx[2] and bx[1] <= c.y <= bx[3]), None)
            if not n: continue
        if True: peoples.append({"type": "Feature", "properties": {"NAME": n, "a": my, "b": nx, "k": "p", "lp": None, "ar": round(km2(g))}, "geometry": mapping(g)})
from shapely.ops import unary_union
grp = {}
for q in peoples: grp.setdefault((q["properties"]["NAME"], q["properties"]["a"], q["properties"]["b"]), []).append(make_valid(shape(q["geometry"])))
peoples = []
for (n, a, b), gs in grp.items():
    u = make_valid(unary_union([x.buffer(0.01) for x in gs]).buffer(-0.01)); ps = polys(u)
    if not ps: continue
    from shapely.geometry import MultiPolygon as _MP
    u2 = onland(make_valid(u.simplify(0.04, preserve_topology=True))); ps2 = [x for x in polys(u2) if km2(x) > 300] or ps
    peoples.append({"type": "Feature", "properties": {"NAME": n, "a": a, "b": b, "k": "p", "lp": None, "ar": round(km2(u))}, "geometry": mapping(ps2[0] if len(ps2) == 1 else _MP(ps2))})
for q in peoples:
    g = make_valid(shape(q["geometry"])); ps = polys(g)
    if ps:
        big = max(ps, key=lambda x: x.area); lp = big.representative_point(); q["properties"]["lp"] = [round(lp.x, 2), round(lp.y, 2)]; q["properties"]["bl"] = round(km2(big))
allf = rows + unions + peoples
for i, f in enumerate(allf): f["properties"]["id"] = i + 1
index = []
for s in range(1400, 1886, STEP):
    e = min(1886, s + STEP)
    sel = [f for f in allf if f["properties"]["a"] < e and f["properties"]["b"] > s]
    # neighbours alive at the same time, so the globe can keep adjacent states in different colours
    bs = [f for f in sel if f["properties"]["k"] != "u"]
    G = [make_valid(shape(f["geometry"])) for f in bs]; T = STRtree(G)
    for i, f in enumerate(bs):
        p = f["properties"]; nb = []
        for j in T.query(G[i].buffer(0.05)):
            if j == i: continue
            q = bs[j]["properties"]
            if q["a"] < p["b"] and q["b"] > p["a"] and G[i].buffer(0.05).intersects(G[j]): nb.append(q["id"])
        p["nb"] = nb
    json.dump({"type": "FeatureCollection", "features": sel}, open(f"/tmp/g3/c{s}.geojson", "w"))
    subprocess.run(["mapshaper", "-i", f"/tmp/g3/c{s}.geojson", "name=c", "-o", "format=topojson", "quantization=400000", f"{OUT}/c{s}.json"], check=True, capture_output=True)
    index.append([s, e])
    print(s, len(sel), os.path.getsize(f"{OUT}/c{s}.json") // 1024, "kb", file=sys.stderr)
json.dump({"step": STEP, "chunks": index}, open(f"{OUT}/index.json", "w"))
print("rows", len(rows), "with survey alias", sum(1 for r in rows if "AKA" in r["properties"]), "members", sum(1 for r in rows if "SUBJECTO" in r["properties"]), "unions", len(unions), "peoples", len(peoples))
