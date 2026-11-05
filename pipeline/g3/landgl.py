"""Land for the GPU map: planar polygons (cut at the 180th meridian), Antarctica kept."""
import json, subprocess
from shapely.geometry import shape, mapping, box, Polygon
from shapely.affinity import translate
from shapely.validation import make_valid
subprocess.run(["mapshaper", "-i", "/home/claude/atlas/maps/land.json", "-o", "format=geojson", "/tmp/g3/land_raw.geojson"], check=True, capture_output=True)
d = json.load(open("/tmp/g3/land_raw.geojson"))
gs = d["geometries"] if "geometries" in d else [f["geometry"] for f in d["features"]]
out = []
for g in gs:
    s = shape(g)
    for q in getattr(s, "geoms", [s]):
        if q.geom_type != "Polygon": continue
        if q.bounds[2] - q.bounds[0] > 180 and q.bounds[1] > -60:
            sh = make_valid(Polygon([(x + 360 if x < -100 else x, y) for x, y in q.exterior.coords], [[(x + 360 if x < -100 else x, y) for x, y in r.coords] for r in q.interiors]))
            for part, dx in ((sh.intersection(box(-180, -90, 180, 90)), 0), (sh.intersection(box(180, -90, 540, 90)), -360)):
                part = translate(part, dx); out += [p for p in getattr(part, "geoms", [part]) if p.geom_type == "Polygon" and not p.is_empty]
        else:
            v = make_valid(q); out += [p for p in getattr(v, "geoms", [v]) if p.geom_type == "Polygon"]
json.dump({"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {}, "geometry": mapping(p)} for p in out]}, open("/tmp/g3/landgl.geojson", "w"))
subprocess.run(["mapshaper", "-i", "/tmp/g3/landgl.geojson", "name=land", "-o", "format=topojson", "quantization=400000", "/home/claude/atlas/maps/landgl.json"], check=True, capture_output=True)
print("land polygons", len(out))
