"""Distance from every sea pixel to the nearest coast, in km (0-255), on an 8192x4096 equirectangular grid.
The globe draws its engraved coastal water lines from this on the graphics card, so they cost nothing per frame."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, WORK
import json, math, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import distance_transform_edt
from shapely.geometry import shape
W, H = 8192, 4096
land = json.load(open(WORK + "/land.geojson"))
im = Image.new("L", (W, H), 0); dr = ImageDraw.Draw(im)
def px(c): return [((x + 180) / 360 * W, (90 - y) / 180 * H) for x, y in c]
n = 0
for g in land["geometries"]:
    s = shape(g)
    for p in getattr(s, "geoms", [s]):
        a = abs(p.area) * 111.32 ** 2 * math.cos(math.radians(p.representative_point().y))
        if a < 1600: continue  # the same islands the strokes ringed (over about 1,600 km2)
        dr.polygon(px(p.exterior.coords), fill=255); n += 1
        for r in p.interiors: dr.polygon(px(r.coords), fill=0)
landm = np.array(im) > 0
dy = 180 / H * 111.32
out = np.zeros((H, W), np.float32)
band = 128; pad = 64
for y0 in range(0, H, band):
    a, b = max(0, y0 - pad), min(H, y0 + band + pad)
    lat = 90 - (y0 + band / 2) / H * 180
    dx = max(0.05, math.cos(math.radians(lat))) * 360 / W * 111.32
    sea = ~landm[a:b]
    sea3 = np.concatenate([sea[:, -W // 8:], sea, sea[:, :W // 8]], axis=1)  # wrap across the 180th meridian
    d = distance_transform_edt(sea3, sampling=(dy, dx))[:, W // 8:W // 8 + W]
    out[y0:min(H, y0 + band)] = d[y0 - a:y0 - a + min(band, H - y0)]
img = np.clip(np.round(out), 0, 255).astype(np.uint8)
Image.fromarray(img).save(MAPS + "/coast.png", optimize=True)
print("land polygons", n, "size", Image.open(MAPS + "/coast.png").size)
