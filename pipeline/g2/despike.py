"""Survey-map repairs that are about drawing, not history:
1. remove spikes - a single vertex flung thousands of kilometres off a border (Imerina in 1880
   reached from Madagascar to Australia), which clips onto whatever land lies under the spike;
2. regional names for peoples kept to their region: a 'West African' people drawn in the Horn of
   Africa takes the name of the region it lies in."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json, subprocess, sys, math
from shapely.geometry import shape, mapping, Polygon, MultiPolygon, box
from shapely.validation import make_valid
M = MAPS
YEARS = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914, 1920, 1930, 1938, 1945, 1960, 1994, 2000, 2010]
def dist(a, b):
    lat = math.radians((a[1] + b[1]) / 2)
    return math.hypot((a[0] - b[0]) * math.cos(lat), a[1] - b[1])
def despike(ring):
    pts = list(ring[:-1]) if ring[0] == ring[-1] else list(ring)
    removed = 0; changed = True
    while changed and len(pts) > 6:
        changed = False; L = len(pts)
        for i in range(L):
            a = pts[i - 1]
            for run in range(1, 9):
                if run >= L - 3: break
                j = (i + run - 1) % L; c = pts[(j + 1) % L]
                out_ = [pts[(i + k) % L] for k in range(run)]
                da, dc, dac = dist(a, out_[0]), dist(out_[-1], c), dist(a, c)
                span = max(dist(out_[0], x) for x in out_)
                if da > 4 and dc > 4 and dac < .2 * min(da, dc) and span < .5 * min(da, dc):
                    idx = sorted(((i + k) % L for k in range(run)), reverse=True)
                    for q in idx: del pts[q]
                    removed += run; changed = True; break
            if changed: break
    return pts + [pts[0]], removed
REGIONAL = {"west african": (-18, 3, 16, 17), "east african": (28, -12, 52, 14), "central african": (12, -6, 31, 12)}
REGNAME = [((-18, 3, 16, 17), "West African peoples"), ((28, -12, 52, 14), "East African peoples"), ((12, -6, 31, 12), "Central African peoples"), ((8, -35, 42, 3), "Bantu-speaking peoples")]
GENERIC = {"West African peoples", "Central African peoples", "East African peoples", "Bantu-speaking peoples"}
PARTS = [((-20, -6, 10, 26), "West African peoples"), ((10, -6, 28, 26), "Central African peoples"), ((28, -6, 56, 26), "East African peoples"), ((-20, -40, 56, -6), "Bantu-speaking peoples")]
total = 0
for y in YEARS:
    tmp = f"{WORK}/ds_{y}.geojson"
    subprocess.run(["mapshaper", "-i", f"{M}/w{y}.json", "-o", "format=geojson", tmp], check=True, capture_output=True)
    fc = json.load(open(tmp)); out = []; n_sp = 0; n_rn = 0
    for f in fc["features"]:
        g = f.get("geometry")
        if not g: out.append(f); continue
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]] if g["type"] == "Polygon" else None
        if polys is None: out.append(f); continue
        newp = []
        for p in polys:
            rings = []
            for r in p:
                r2, k = despike([tuple(x) for x in r]); n_sp += k
                if len(r2) >= 4: rings.append([list(x) for x in r2])
            if rings: newp.append(rings)
        if not newp: continue
        f["geometry"] = {"type": "MultiPolygon", "coordinates": newp} if len(newp) > 1 else {"type": "Polygon", "coordinates": newp[0]}
        name = (f["properties"].get("NAME") or "")
        if name in GENERIC:
            # a broad regional name is cut along the regions, so the Guinea coast is never called Central African
            G = make_valid(shape(f["geometry"])); hit = False
            for bx, nm in PARTS:
                part = make_valid(G.intersection(box(*bx)))
                ps = [x for x in getattr(part, "geoms", [part]) if x.geom_type == "Polygon" and not x.is_empty]
                if not ps: continue
                pr = dict(f["properties"]); pr["NAME"] = nm; hit = True
                out.append({"type": "Feature", "properties": pr, "geometry": mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))})
            if hit: n_rn += 1; continue
        key = next((k for k in REGIONAL if k in name.lower()), None)
        if key:
            G = make_valid(shape(f["geometry"]))
            parts = [x for x in getattr(G, "geoms", [G]) if x.geom_type == "Polygon"]
            home = box(*REGIONAL[key]); keep = []; moved = {}
            for part in parts:
                c = part.representative_point()
                if home.contains(c): keep.append(part); continue
                nm = next((n for bx, n in REGNAME if box(*bx).contains(c)), None)
                if nm: moved.setdefault(nm, []).append(part); n_rn += 1
                else: keep.append(part)
            if moved:
                if keep: f["geometry"] = mapping(keep[0] if len(keep) == 1 else MultiPolygon(keep)); out.append(f)
                for nm, ps in moved.items():
                    pr = dict(f["properties"]); pr["NAME"] = nm
                    out.append({"type": "Feature", "properties": pr, "geometry": mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))})
                continue
        out.append(f)
    fc["features"] = out
    json.dump(fc, open(tmp, "w"))
    subprocess.run(["mapshaper", "-i", tmp, f"name=world_{y}", "-o", "format=topojson", "precision=0.0001", f"{M}/w{y}.json"], check=True, capture_output=True)
    total += n_sp
    if n_sp or n_rn: print(y, "spikes removed", n_sp, "peoples renamed by region", n_rn, file=sys.stderr)
print("spikes", total)
