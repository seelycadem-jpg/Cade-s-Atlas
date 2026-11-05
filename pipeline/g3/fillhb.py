"""Evidence-checked repairs to the period maps, from the survey maps (historical-basemaps), applied only where the
independent dated research (control points, /home/claude/review/cp) confirms them:
  fill  - land the reference record leaves to 'peoples' becomes the survey's state there, when a researched place
          inside that land was ruled by that state in that period; the state takes the researched name.
  carve - land the reference record gives to a state becomes peoples' land, when the survey shows no state there and
          researched places inside it were ruled by no state in that period (and none was ruled by that state).
Input /tmp/g3/snaps, output /tmp/g3/snaps2 (same format; repaired features carry fx='fill'|'carve')."""
import json, os, re, sys, glob
from multiprocessing import Pool
from shapely.geometry import shape, mapping, Point, MultiPolygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
sys.path.insert(0, "/home/claude/review"); from names import same
OUT = "/tmp/g3/snaps2"; os.makedirs(OUT, exist_ok=True)
PEOPLES = re.compile(r"hunter|gatherer|peoples|cultures|culture$|nomad|aboriginal|tribes|^maori|polynesian|papuan|inuit|^san$|khoisan|siberian|farmers|chiefdoms|^bantu|herders|pastoralist|forager|bedouin|indigenous|nations$|clans|tribal", re.I)
CP = [p for f in sorted(glob.glob("/home/claude/review/cp/*.json")) for p in json.load(open(f))["places"]]
EVID = os.environ.get("EVID", "all"); MODE = os.environ.get("MODE", "point")  # 'even' uses every other place as evidence, so the rest can test the repair fairly
if EVID != "all": CP = [p for i, p in enumerate(CP) if (i % 2 == 0) == (EVID == "even")]
OUT = os.environ.get("OUTS", OUT); os.makedirs(OUT, exist_ok=True); SRC = os.environ.get("SRC", "/tmp/g3/snaps"); SPANS = os.environ.get("SPANS", "/tmp/g3/spans.json")
def truth(p, y):
    for t in p["timeline"]:
        if t["from"] <= y < t["to"]: return t
HBY = sorted(int(re.search(r"world_(\d+)", f).group(1)) for f in glob.glob("/tmp/hb2/geojson/world_*.geojson") if re.search(r"world_(\d+)\.geojson$", f) and 1300 <= int(re.search(r"world_(\d+)", f).group(1)) <= 1900)
HB = {}
def hb(y):
    if y not in HB:
        fs = []
        for f in json.load(open(f"/tmp/hb2/geojson/world_{y}.geojson"))["features"]:
            if not f.get("geometry"): continue
            try: g = make_valid(shape(f["geometry"]))
            except Exception: continue
            fs.append((f["properties"].get("NAME") or "", f["properties"].get("SUBJECTO"), g))
        HB[y] = fs
    return HB[y]
def polys(g):
    if g is None or g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def km2(g):
    import math
    return 0 if g.is_empty else abs(g.area) * 111.32 ** 2 * math.cos(math.radians(g.representative_point().y))
def mp(ps): return ps[0] if len(ps) == 1 else MultiPolygon(ps)
def work(span):
    a, b = span; mid = (a + b) / 2
    fc = json.load(open(f"{SRC}/s{a}.geojson")); F = fc["features"]
    sy = min(HBY, key=lambda y: abs(y - mid))
    if abs(sy - mid) > 60: json.dump(fc, open(f"{OUT}/s{a}.geojson", "w")); return a, 0, 0
    H = hb(sy)
    G = [make_valid(shape(f["geometry"])) for f in F]
    pts = [(p, Point(p["lon"], p["lat"])) for p in CP]
    # which feature holds each researched place
    T = STRtree(G); where = {}
    for k, (p, pt) in enumerate(pts):
        hit = [i for i in T.query(pt) if G[i].contains(pt)]
        if hit: where[k] = hit[0]
    nfill = ncarve = 0; new = []
    # ---- fill ----
    P = [i for i, f in enumerate(F) if f["properties"].get("k") == "p"]
    if P:
        PU = unary_union([G[i] for i in P])
        for name, subj, h in H:
            if not name or PEOPLES.search(name) or not h.intersects(PU): continue
            # researched places inside this survey state that sit on peoples' land
            ev = []
            for k, (p, pt) in enumerate(pts):
                if where.get(k) in P and h.contains(pt):
                    t = truth(p, int(mid))
                    if t and t["ruler"] != "none" and (same(name, t["ruler"]) or any(same(name, x) for x in (t.get("aliases") or []))):
                        if all((truth(p, yy) or {}).get("ruler") == t["ruler"] for yy in (a, max(a, b - 1))): ev.append(t)
            if not ev and MODE == "exist":
                # no researched place inside, but the state is on record as ruling somewhere in this period
                ok = any((t := truth(p, int(mid))) and t["ruler"] != "none" and (same(name, t["ruler"]) or any(same(name, x) for x in (t.get("aliases") or []))) for p in CP)
                if ok: ev = [{"ruler": name, "overlord": None, "source": None}]
            if not ev and MODE == "all": ev = [{"ruler": name, "overlord": None, "source": None}]
            if not ev: continue
            piece = make_valid(h.intersection(PU))
            ps = [q for q in polys(piece) if km2(q) > 200]
            if not ps: continue
            piece = mp(ps); t = ev[0]
            for i in P:
                if G[i].intersects(piece):
                    try: G[i] = make_valid(G[i].difference(piece))
                    except Exception: pass
            PU = make_valid(PU.difference(piece))
            big = max(ps, key=lambda q: q.area); lp = big.representative_point()
            pr = {"NAME": t["ruler"], "a": a, "b": b, "k": "b", "fx": "fill", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(piece)), "bl": round(km2(big)), "src": t.get("source")}
            if t.get("overlord"): pr["SUBJECTO"] = t["overlord"] if isinstance(t["overlord"], str) else "; ".join(t["overlord"])
            new.append({"type": "Feature", "properties": pr, "geometry": piece}); nfill += 1
    # ---- carve ----
    for name, subj, h in H:
        if name and not PEOPLES.search(name): continue
        for i, f in enumerate(F):
            if f["properties"].get("k") != "b" or not G[i].intersects(h): continue
            nm = f["properties"].get("NAME")
            yes = no = 0; peo = None
            for k, (p, pt) in enumerate(pts):
                if where.get(k) != i: continue
                t = truth(p, int(mid))
                if not t: continue
                inside = h.contains(pt)
                if t["ruler"] == "none" and inside and all((truth(p, yy) or {}).get("ruler") == "none" for yy in (a, max(a, b - 1))): yes += 1; peo = peo or t.get("peoples")
                elif inside and (same(nm, t["ruler"]) or (t.get("overlord") and same(nm, t["overlord"]))): no += 1
            if yes and not no:
                piece = make_valid(G[i].intersection(h)); ps = [q for q in polys(piece) if km2(q) > 200]
                if not ps: continue
                piece = mp(ps); G[i] = make_valid(G[i].difference(piece))
                big = max(ps, key=lambda q: q.area); lp = big.representative_point()
                new.append({"type": "Feature", "properties": {"NAME": (peo if isinstance(peo, str) else ", ".join(peo)) if peo else (name or "Peoples"), "a": a, "b": b, "k": "p", "fx": "carve", "lp": [round(lp.x, 2), round(lp.y, 2)], "ar": round(km2(piece)), "bl": round(km2(big))}, "geometry": piece}); ncarve += 1
    out = []
    for i, f in enumerate(F):
        ps = [q for q in polys(G[i]) if km2(q) > 20]
        if not ps: continue
        g = mp(ps); f["geometry"] = mapping(g)
        if km2(g) < 0.98 * f["properties"].get("ar", 0):
            big = max(ps, key=lambda q: q.area); f["properties"]["ar"] = round(km2(g)); f["properties"]["bl"] = round(km2(big))
            lp = f["properties"].get("lp")
            if lp and not g.contains(Point(*lp)): q = big.representative_point(); f["properties"]["lp"] = [round(q.x, 2), round(q.y, 2)]
        out.append(f)
    for f in new: f["geometry"] = mapping(f["geometry"]); out.append(f)
    fc["features"] = out; json.dump(fc, open(f"{OUT}/s{a}.geojson", "w"))
    return a, nfill, ncarve
def safe(s):
    try: return work(s)
    except Exception as e: print("fail", s, e, file=sys.stderr, flush=True); return s[0], -1, -1
if __name__ == "__main__":
    spans = json.load(open(SPANS))
    with Pool(2) as pool:
        tf = tc = 0
        for a, nf, nc in pool.imap_unordered(safe, spans):
            tf += max(0, nf); tc += max(0, nc); print(a, nf, nc, file=sys.stderr, flush=True)
    print("fills", tf, "carves", tc)
