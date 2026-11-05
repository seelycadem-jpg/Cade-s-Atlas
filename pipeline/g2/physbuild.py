"""Physical geography for the globe: mountain ranges (with hill-mark points), deserts, plateaus,
rivers, lakes and sea names. Writes site/maps/phys.json (topology) and site/maps/physpts.json."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, ROOT, WORK
import json, math, random, subprocess, re
from shapely.geometry import shape, mapping, Point
from shapely.validation import make_valid
from shapely.ops import polylabel
N = ROOT + "/g2/ne"; M = MAPS
random.seed(7)
def tc(s):
    s = re.sub(r"\s+", " ", s.strip())
    if s.upper() != s: return s
    small = {"of", "de", "del", "do", "da"}
    return " ".join(w.capitalize() if w.lower() not in small or i == 0 else w.lower() for i, w in enumerate(s.lower().split(" ")))
FIX = {"Mts.": "Mountains", "Ra.": "Range", "Cord.": "Cordillera", "Sikhote-alin’": "Sikhote-Alin", "Sea of Japan": "Sea of Japan (East Sea)", "Persian Gulf": "Persian Gulf (Arabian Gulf)", "Appennini": "Apennines", "Kjølen Mountains": "Scandinavian Mountains", "Chaîne Annamitique": "Annamite Range"}
def fix(n):
    for a, b in FIX.items(): n = n.replace(a, b)
    return n
def axis(g):
    r = g.minimum_rotated_rectangle; xs = list(r.exterior.coords)
    best = None
    for i in range(4):
        (x0, y0), (x1, y1) = xs[i], xs[i + 1]
        lat = (y0 + y1) / 2; dx = (x1 - x0) * math.cos(math.radians(lat)); dy = y1 - y0
        L = math.hypot(dx, dy)
        if best is None or L > best[0]: best = (L, math.degrees(math.atan2(dy, dx)))
    a = best[1]
    if a > 90: a -= 180
    if a < -90: a += 180
    return round(a, 1), round(best[0], 1)
regions = json.load(open(f"{N}/ne_50m_geography_regions_polys.geojson"))["features"]
keep = []; pts = {"mtn": [], "desert": []}; labels = []
for f in regions:
    p = f["properties"]; cla = p["FEATURECLA"]; sr = p["SCALERANK"]
    if cla not in ("Range/mtn", "Desert", "Plateau"): continue
    if cla == "Plateau" and sr > 3: continue
    nm = fix(tc(p["NAME"]))
    if "antarc" in (p.get("REGION") or "").lower() or "Transantarctic" in nm or "Queen Maud" in nm or "Ellsworth" in nm or "Pensacola" in nm: continue
    g = make_valid(shape(f["geometry"]))
    kind = {"Range/mtn": "mtn", "Desert": "desert", "Plateau": "plateau"}[cla]
    lp = polylabel(max(g.geoms, key=lambda x: x.area) if hasattr(g, "geoms") else g, 0.05)
    ang, L = axis(g)
    labels.append({"n": nm, "k": kind, "sr": sr, "lon": round(lp.x, 2), "lat": round(lp.y, 2), "ang": ang, "len": L})
    keep.append({"type": "Feature", "properties": {"k": kind, "sr": sr}, "geometry": mapping(g)})
    if kind in ("mtn", "desert"):
        # hill marks / stipple: a jittered grid at three densities
        minx, miny, maxx, maxy = g.bounds
        for lvl, step in ((0, 1.6), (1, 0.8), (2, 0.4)):
            y = miny
            while y <= maxy:
                cx = step / max(0.25, math.cos(math.radians(y)))
                x = minx
                while x <= maxx:
                    jx, jy = x + random.uniform(-.35, .35) * cx, y + random.uniform(-.35, .35) * step
                    if g.contains(Point(jx, jy)): pts[kind].append([round(jx, 2), round(jy, 2), lvl])
                    x += cx
                y += step
json.dump({"type": "FeatureCollection", "features": keep}, open(WORK + "/regions.geojson", "w"))
rv = [f for f in json.load(open(f"{N}/ne_50m_rivers_lake_centerlines.geojson"))["features"] if f["properties"]["scalerank"] <= 6]
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"sr": f["properties"]["scalerank"], "n": f["properties"].get("name")}, "geometry": f["geometry"]} for f in rv]}, open(WORK + "/rivers.geojson", "w"))
lk = [f for f in json.load(open(f"{N}/ne_50m_lakes.geojson"))["features"] if f["properties"]["scalerank"] <= 4]
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {"sr": f["properties"]["scalerank"], "n": f["properties"].get("name")}, "geometry": f["geometry"]} for f in lk]}, open(WORK + "/lakes.geojson", "w"))
subprocess.run(["mapshaper", "-i", WORK + "/regions.geojson", WORK + "/rivers.geojson", WORK + "/lakes.geojson", "combine-files",
                "-rename-layers", "regions,rivers,lakes", "-simplify", "20%", "weighted", "keep-shapes",
                "-o", "format=topojson", "precision=0.01", f"{M}/phys.json"], check=True, capture_output=True)
marine = json.load(open(f"{N}/ne_50m_geography_marine_polys.geojson"))["features"]
for f in marine:
    p = f["properties"]; cla = p["featurecla"]
    if cla not in ("ocean", "sea", "gulf", "bay", "strait", "channel"): continue
    g = make_valid(shape(f["geometry"]))
    big = max(g.geoms, key=lambda x: x.area) if hasattr(g, "geoms") else g
    lp = polylabel(big, 0.1)
    ang, L = axis(big)
    labels.append({"n": fix(tc(p.get("name_en") or p["name"])), "k": cla, "sr": p["scalerank"], "lon": round(lp.x, 2), "lat": round(lp.y, 2), "ang": ang if cla not in ("ocean",) else 0, "len": L})
json.dump({"labels": labels, "mtn": pts["mtn"], "desert": pts["desert"]}, open(f"{M}/physpts.json", "w"), separators=(",", ":"))
print("regions", len(keep), "labels", len(labels), "hill marks", len(pts["mtn"]), "stipple", len(pts["desert"]))
