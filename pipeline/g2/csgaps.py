"""Land the dated state record (1886-2019) leaves empty, year by year, with the name the
survey of that period gives it (or the peoples of the region). Writes site/maps/csgaps.json:
features with a, b (years, b exclusive) so the globe draws them only while the gap exists."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, ROOT, WORK
import json, subprocess, sys, math, hashlib
sys.path.insert(0, ROOT + "/g2")
from shapely.geometry import shape, box, Polygon
from shapely.ops import unary_union
from shapely.validation import make_valid
from shapely import STRtree
M = MAPS
MAPY = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914, 1920, 1930, 1938, 1945, 1960, 1994, 2000, 2010]
def mapYear(y): return max(m for m in MAPY if m <= y)
src = open(ROOT + "/g2/fillblank.py").read()
REGIONS = eval(src[src.index("REGIONS = [") + len("REGIONS = "): src.index("]\ndef km2") + 1])
PEOPLES_RE = src[src.index('re.compile(r"') + 13: src.index('", re.I)')]
import re
PEOPLES = re.compile(PEOPLES_RE, re.I)
def km2(g):
    if g.is_empty: return 0
    return g.area * 111.32 ** 2 * math.cos(math.radians(g.centroid.y))
def polys(g):
    if g.is_empty: return []
    if g.geom_type == "Polygon": return [g]
    if hasattr(g, "geoms"): return [p for x in g.geoms for p in polys(x)]
    return []
def gj(path, tmp):
    subprocess.run(["mapshaper", "-i", path, "-o", "format=geojson", tmp], check=True, capture_output=True)
    return json.load(open(tmp))["features"]
land_gj = json.load(open(WORK + "/land.geojson"))
geoms = land_gj["geometries"] if "geometries" in land_gj else [f["geometry"] for f in land_gj["features"]]
LAND = make_valid(unary_union([make_valid(shape(g)) for g in geoms])).difference(box(-180, -90, 180, -60))
CS = [(make_valid(shape(f["geometry"])).buffer(0.02), f["properties"]) for f in gj(f"{M}/cs.json", WORK + "/csg_cs.geojson") if f.get("geometry")]

STOP = {"of", "the", "and", "empire", "kingdom", "republic", "federal", "democratic", "people's", "socialist", "state", "states", "union", "sultanate", "emirate"}
ALIAS = {"Russia (Soviet Union)": "ussr russia russian soviet white", "Iraq": "mesopotamia", "Iran (Persia)": "persia", "Thailand": "siam", "Turkey (Ottoman Empire)": "ottoman turkey",
         "Myanmar (Burma)": "burma", "Sri Lanka (Ceylon)": "ceylon", "Congo, Democratic Republic of (Zaire)": "congo zaire belgian", "Zimbabwe (Rhodesia)": "rhodesia southern",
         "Tanzania (Tanganyika)": "tanganyika", "Italy/Sardinia": "italy sardinia", "Germany (Prussia)": "germany prussia german", "German Federal Republic": "germany west",
         "German Democratic Republic": "germany east", "Rumania": "romania", "United States of America": "usa", "Cambodia (Kampuchea)": "cambodia", "Madagascar (Malagasy)": "madagascar",
         "Belarus (Byelorussia)": "belarus white russia", "Ukraine": "ukraine ukrainian"}
import re as _re
def toks(s, survey=False):
    s = s.lower()
    if survey: s = _re.sub(r"\(.*?\)", " ", s)
    t = {w for w in _re.split(r"[^a-z']+", s) if w and w not in STOP}
    return t
GREEN = None

from shapely.geometry import Point as _P
GREENLAND = Polygon([(-75, 76), (-70, 79), (-65, 80.6), (-60, 82), (-50, 84.5), (-5, 84.5), (-5, 59), (-48, 58), (-60, 70), (-75, 76)])
SPECIAL = [  # (area, from, to, name, owner) - owner None means a polity outside the recognised states
 (GREENLAND, 1886, 2100, "Greenland", "Denmark"),
 (box(-25, 63, -13, 67), 1886, 1918, "Iceland", "Denmark"),
 (box(-25, 63, -13, 67), 1918, 1944, "Kingdom of Iceland", None),
 (box(-62, -53, -57, -50.8), 1886, 2100, "Falkland Islands", "United Kingdom"),
 (box(9, 76, 35, 81), 1886, 1925, "Svalbard (no sovereign)", None),
 (box(9, 76, 35, 81), 1925, 2100, "Svalbard", "Norway"),
 (box(44, 79.5, 66, 82.5), 1886, 1926, "Franz Josef Land (no sovereign)", None),
 (box(44, 79.5, 66, 82.5), 1926, 2100, "Franz Josef Land", "Russia (Soviet Union)"),
 (box(42, 12, 55, 19), 1886, 1963, "Aden Protectorate (British)", "Aden", r"protectorate|aden|hadhram"),
]
RENAME = {"British Protectorate": "Aden Protectorate (British)", "Arabia": "Najd emirates and tribes"}
ADJ = {"portuguese": "Portugal", "british": "United Kingdom", "french": "France", "german": "Germany (Prussia)", "italian": "Italy/Sardinia", "spanish": "Spain", "belgian": "Belgium", "dutch": "Netherlands"}
ARABIA = {"Arabia", "Najd emirates and tribes", "Arabia (Nejd)", "Hail", "Emirate of Bin Shal'an", "Bedouin tribes", "Hejaz", "Jabal Shammar", "Nejd"}
def arabia(n, y, c):
    """Central Arabia before the Saudi kingdom: the surveys lag the conquests, so name by year."""
    if n not in ARABIA or not box(34, 15, 56, 33).contains(c): return n
    if n == "Hejaz" and y < 1926: return "Kingdom of Hejaz"
    if n == "Hail" and y < 1921: return "Emirate of Jabal Shammar (Al Rashid)"
    if y < 1902: return "Emirate of Jabal Shammar (Al Rashid)"
    if y < 1913: return "Emirate of Nejd (Al Saud)"
    if y < 1921: return "Emirate of Nejd and Hasa (Al Saud)"
    if y < 1926: return "Sultanate of Nejd (Al Saud)"
    return "Kingdom of Hejaz and Nejd (Al Saud)"
def special(g, y, actF, n):
    c = g.representative_point()
    for sp in SPECIAL:
        A, a, b, name, owner = sp[:5]
        if not (a <= y < b) or not A.contains(c): continue
        if len(sp) > 5 and not re.search(sp[5], n, re.I): continue
        if owner is None: return (None, name)
        o = next(((p["r"], p["o"]) for gg, p in actF if p["r"] == owner), None)
        return (o, name) if o else None
    return None
SURV = {}
def survey(my):
    if my not in SURV:
        F = [(make_valid(shape(f["geometry"])), (f["properties"].get("NAME") or "").strip()) for f in gj(f"{M}/w{my}.json", f"{WORK}/csg_{my}.geojson") if f.get("geometry")]
        F = [(g, n) for g, n in F if n]
        SURV[my] = (F, STRtree([g for g, n in F]))
    return SURV[my]
LANDP = polys(LAND)
GREEN = max(polys(LAND), key=lambda p: p.area if p.contains(__import__('shapely.geometry',fromlist=['Point']).Point(-40, 72)) else 0)
out = []; prev_key = None; cur = None
for y in range(1886, 2020):
    t = y + .5
    act = tuple(i for i, (g, p) in enumerate(CS) if p["a"] <= t < p["b"])
    key = (act, mapYear(y))
    if key == prev_key:
        for f in cur: f["properties"]["b"] = y + 1
        continue
    prev_key = key
    U = unary_union([CS[i][0] for i in act])
    gaps = [p for p in polys(make_valid(LAND.difference(U))) if km2(p) > 2500]
    F, T = survey(mapYear(y))
    named = []
    for gp in gaps:
        rest = gp
        for j in T.query(gp):
            g, n = F[j]
            try: piece = make_valid(rest.intersection(g))
            except Exception: continue
            if km2(piece) < 1500: continue
            named.append((piece, n, "survey")); rest = make_valid(rest.difference(g))
            if rest.is_empty: break
        for part in polys(rest):
            if km2(part) < 1500: continue
            c = part.representative_point()
            for bx, name in REGIONS:
                if box(*bx).contains(c): named.append((part, name, "region")); break
    # who holds each piece: a recognised state of the same name, the state it is a sliver of, or
    # (failing both) the polity the survey names, drawn as land outside the recognised states
    cur = []
    actF = [(CS[i][0], CS[i][1]) for i in act]
    T2 = STRtree([g for g, p in actF])
    groups = {}
    owned = []; later = []
    for g, n, how in named:
        n = arabia(RENAME.get(n, n), y, g.representative_point())
        own = None; nm = n
        sp = special(g, y, actF, n)
        if sp is not None:
            own, nm = sp
        else:
            core = toks(n, True) if how != "region" else set()
            if core:
                cands = []
                for gg, p in actF:
                    adj = {a for a in core if ADJ.get(a) == p["o"]}
                    if core <= toks(p["r"]) | toks(ALIAS.get(p["r"], "")) or (p["o"] and core <= toks(p["o"]) | toks(ALIAS.get(p["o"], ""))) or (adj and core - adj and core - adj <= toks(p["r"]) | toks(ALIAS.get(p["r"], ""))):
                        cands.append((gg.distance(g), (p["r"], p["o"])))
                cands.sort()
                if cands and (cands[0][0] < 12 or len({c[1][0] for c in cands}) == 1): own = cands[0][1]; nm = None
            if own is None and how == "region": later.append((g, n)); continue
            if own is None and km2(g) < 8000:
                near = [actF[j] for j in T2.query(g.buffer(1.0))]
                if near:
                    gg, p = max(near, key=lambda q: (q[0].buffer(0.05).intersection(g.buffer(0.05)).area, -q[0].distance(g)))
                    if gg.distance(g) < 1.0: own = (p["r"], p["o"]); nm = None
        if own is not None: owned.append((g, own))
        groups.setdefault((nm if own is None else (own, nm)), []).append(g)
    # land the survey leaves blank goes to the nearest holder (state or owned piece) within 5 degrees
    for g, n in later:
        cands = [(gg.distance(g), (p["r"], p["o"])) for gg, p in (actF[j] for j in T2.query(g.buffer(5.0)))] + [(gg.distance(g), o) for gg, o in owned]
        cands = [c for c in cands if c[0] < 5.0]
        if cands:
            groups.setdefault((min(cands)[1], None), []).append(g)
        else:
            groups.setdefault(n, []).append(g)
    from shapely.geometry import MultiPolygon, mapping
    from shapely.ops import polylabel
    for key, gs in groups.items():
        g = make_valid(unary_union(gs)).simplify(0.03, preserve_topology=True)
        ps = polys(g)
        if not ps: continue
        geom = mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))
        big = max(ps, key=lambda p: p.area); lp = polylabel(big, 0.05)
        pr = {"a": y, "b": y + 1, "ar": round(km2(g)), "bl": round(km2(big)), "lp": [round(lp.x, 2), round(lp.y, 2)]}
        if isinstance(key, tuple):
            pr["own"] = list(key[0])
            if key[1]: pr["NAME"] = key[1]; pr["dep"] = 0 if key[1] in ("Franz Josef Land",) else 1
            if key[1] is None: pr.pop("lp")
        else: pr["NAME"] = key
        cur.append({"type": "Feature", "properties": pr, "geometry": geom})
    out.extend(cur)
    print(y, len(gaps), "free:", ", ".join(f"{f['properties']['NAME']}" for f in cur if "own" not in f["properties"])[:300], "| named owned:", ", ".join(f["properties"]["NAME"] for f in cur if "own" in f["properties"] and "NAME" in f["properties"]), file=sys.stderr)
# extend the last record to the present
for f in out:
    if f["properties"]["b"] == 2020: f["properties"]["b"] = 2100
json.dump({"type": "FeatureCollection", "features": out}, open(WORK + "/csgaps.geojson", "w"))
subprocess.run(["mapshaper", "-i", WORK + "/csgaps.geojson", "name=gaps", "-simplify", "50%", "weighted", "keep-shapes", "-o", "format=topojson", "precision=0.001", f"{M}/csgaps.json"], check=True, capture_output=True)
print("features", len(out))
