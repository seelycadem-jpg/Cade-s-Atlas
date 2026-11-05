"""Planar copy of the land for the Python steps: polygons that cross the 180th meridian (Wrangel
Island, Fiji) are cut there, or shapely reads them as bands around the whole world."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json
from shapely.geometry import shape, mapping, box, MultiPolygon, Polygon
from shapely.affinity import translate
from shapely.validation import make_valid
import subprocess
subprocess.run(["mapshaper", "-i", MAPS + "/land.json", "-o", "format=geojson", WORK + "/land.geojson"], check=True, capture_output=True)
d = json.load(open(WORK + "/land.geojson"))
gs = d["geometries"] if "geometries" in d else [f["geometry"] for f in d["features"]]
out = []; cut = 0
for g in gs:
    s = shape(g)
    for q in getattr(s, "geoms", [s]):
        if q.geom_type != "Polygon": continue
        if q.bounds[2] - q.bounds[0] > 180 and q.bounds[3] > -60:
            cut += 1
            if q.bounds[1] < -60: continue  # Antarctica: the steps cut it away anyway
            sh = make_valid(Polygon([(x + 360 if x < -100 else x, y) for x, y in q.exterior.coords], [[(x + 360 if x < -100 else x, y) for x, y in r.coords] for r in q.interiors]))
            for part, dx in ((sh.intersection(box(-180, -90, 180, 90)), 0), (sh.intersection(box(180, -90, 540, 90)), -360)):
                part = translate(part, dx)
                out += [p for p in getattr(part, "geoms", [part]) if p.geom_type == "Polygon" and not p.is_empty]
        else: out.append(make_valid(q))
flat = []
for p in out: flat += [x for x in getattr(p, "geoms", [p]) if x.geom_type == "Polygon"]
json.dump({"type": "GeometryCollection", "geometries": [mapping(p) for p in flat]}, open(WORK + "/land.geojson", "w"))
print("land polygons", len(out), "cut at the 180th meridian", cut)
