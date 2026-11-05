"""Score map sources against the control-point timelines.
Sources: atlas (period maps 1400-1885 + CShapes/gaps from 1886, as the globe draws them), clio (raw Cliopatria base
polities, before the period maps were built), hb (historical-basemaps snapshots), cs (CShapes alone, 1886+).
Output pipeline/review/score.json (every check) and a printed summary."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import ROOT, WORK
import json, glob, os, re, sys, unicodedata, math
from shapely.geometry import shape, Point
from shapely import STRtree
from shapely.validation import make_valid
sys.path.insert(0, os.path.dirname(__file__))
from names import same, key  # lineage matching
CP = []
for f in sorted(glob.glob(ROOT + "/review/cp/*.json")):
    d = json.load(open(f)); reg = os.path.basename(f)[:-5]
    for p in d["places"]:
        p["region"] = reg; CP.append(p)
def truth(p, y):
    for t in p["timeline"]:
        if t["from"] <= y < t["to"]: return t
    return None
class Layer:
    """polygons with properties; lookup returns the smallest polygon containing the point, else the nearest within 0.2 deg"""
    def __init__(self, feats):
        self.F = []; G = []
        for props, g in feats:
            try: g = make_valid(g)
            except Exception: continue
            if g.is_empty: continue
            self.F.append(props); G.append(g)
        self.G = G; self.T = STRtree(G) if G else None
    def at(self, x, y):
        if not self.G: return None
        pt = Point(x, y); hit = [i for i in self.T.query(pt) if self.G[i].contains(pt)]
        if hit: return self.F[min(hit, key=lambda i: self.G[i].area)]
        near = [i for i in self.T.query(pt.buffer(0.2)) if self.G[i].distance(pt) <= 0.2]
        if near: return self.F[min(near, key=lambda i: self.G[i].distance(pt))]
        return None
# ---------- atlas: period maps ----------
spans = json.load(open(os.environ.get("SPANS", WORK + "/g3/spans.json")))
SNAPS = os.environ.get("SNAPS", WORK + "/g3/snaps"); SUB = os.environ.get("SUBSET", "all"); TAG = os.environ.get("TAG", "")
SNAPC = {}
def snap_layer(y):
    a = max(s[0] for s in spans if s[0] <= y)
    if a not in SNAPC:
        fc = json.load(open(f"{SNAPS}/s{a}.geojson"))["features"]
        SNAPC.clear(); SNAPC[a] = Layer([(f["properties"], shape(f["geometry"])) for f in fc])
    return SNAPC[a]
CSF = json.load(open(WORK + "/rv/cs.geojson"))["features"]; GAPF = json.load(open(WORK + "/rv/csgaps.geojson"))["features"]
CSG = [(f["properties"], shape(f["geometry"])) for f in CSF if f.get("geometry")]
GAPG = [(f["properties"], shape(f["geometry"])) for f in GAPF if f.get("geometry")]
CSC = {}
def cs_layer(y, gaps=True):
    k = (y, gaps)
    if k not in CSC:
        t = min(y, 2019) + .5; yy = min(y, 2019)
        fs = [({"NAME": p["o"] or p["r"], "SUBJECTO": p["o"] or None, "REGION": p["r"]}, g) for p, g in CSG if p["a"] <= t < p["b"]]
        if gaps:
            for p, g in GAPG:
                if not (p["a"] <= yy < p["b"]): continue
                if p.get("own"):
                    own = p["own"]; o = own[1] if len(own) > 1 and own[1] else None
                    fs.append(({"NAME": p.get("NAME") or (o or own[0]), "SUBJECTO": o, "REGION": own[0]}, g))
                elif p.get("NAME"): fs.append(({"NAME": p["NAME"]}, g))
        if len(CSC) > 4: CSC.clear()
        CSC[k] = Layer(fs)
    return CSC[k]
def atlas_at(p, y):
    if y < 1886:
        r = snap_layer(y).at(p["lon"], p["lat"])
        if r is None: return None
        return {"NAME": r.get("NAME"), "SUBJECTO": r.get("SUBJECTO"), "people": r.get("k") == "p"}
    r = cs_layer(y).at(p["lon"], p["lat"])
    return r and {"NAME": r["NAME"], "SUBJECTO": r.get("SUBJECTO"), "REGION": r.get("REGION")}
# ---------- clio raw ----------
ROWS = json.load(open(os.environ.get("ROWS", WORK + "/g3/rows.json")))
CLIO = Layer([(r["properties"], shape(r["geometry"])) for r in ROWS])
def clio_at(p, y):
    pt = Point(p["lon"], p["lat"])
    hit = [i for i in CLIO.T.query(pt) if CLIO.F[i]["a"] <= y < CLIO.F[i]["b"] and CLIO.G[i].contains(pt)]
    if not hit:
        hit = [i for i in CLIO.T.query(pt.buffer(0.2)) if CLIO.F[i]["a"] <= y < CLIO.F[i]["b"] and CLIO.G[i].distance(pt) <= 0.2]
        if not hit: return None
        i = min(hit, key=lambda i: CLIO.G[i].distance(pt))
    else: i = min(hit, key=lambda i: CLIO.G[i].area)
    r = CLIO.F[i]; return {"NAME": r["NAME"], "SUBJECTO": r.get("SUBJECTO")}
# ---------- historical-basemaps ----------
HBY = sorted(int(m.group(1)) for f in glob.glob(WORK + "/hb2/geojson/world_*.geojson") for m in [re.match(r".*world_(\d+)\.geojson", f)] if m and int(m.group(1)) >= 1400)
HBC = {}
def hb_at(p, y):
    if y not in HBY: return "skip"
    if y not in HBC:
        fs = json.load(open(f"{WORK}/hb2/geojson/world_{y}.geojson"))["features"]
        HBC[y] = Layer([(f["properties"], shape(f["geometry"])) for f in fs if f.get("geometry")])
    r = HBC[y].at(p["lon"], p["lat"])
    if r is None or not r.get("NAME"): return None
    s = r.get("SUBJECTO") if r.get("SUBJECTO") != r.get("NAME") else None
    return {"NAME": r["NAME"], "SUBJECTO": s or (r.get("PARTOF") if r.get("PARTOF") != r.get("NAME") else None)}
def cs_at(p, y):
    if y < 1886: return "skip"
    r = cs_layer(y, gaps=False).at(p["lon"], p["lat"])
    return r and {"NAME": r["NAME"], "SUBJECTO": r.get("SUBJECTO"), "REGION": r.get("REGION")}
UNIONS = [("Kingdom of Portugal", "Spanish Empire", 1580, 1640), ("Kingdom of Portugal", "Kingdom of Spain", 1580, 1640), ("Kingdom of Portugal", "Crown of Castile", 1580, 1640),
 ("Kingdom of Sweden", "Denmark", 1397, 1523), ("Kingdom of Sweden", "Kalmar Union", 1397, 1523), ("Kingdom of Norway", "Kalmar Union", 1397, 1523), ("Kingdom of Denmark", "Kalmar Union", 1397, 1523),
 ("Kingdom of Bohemia", "Habsburg Monarchy", 1526, 1918), ("Kingdom of Hungary", "Habsburg Monarchy", 1526, 1918), ("Kingdom of Croatia", "Habsburg Monarchy", 1527, 1918),
 ("Crown of Aragon", "Spanish Empire", 1479, 1716), ("Crown of Aragon", "Kingdom of Spain", 1479, 1716), ("Crown of Castile", "Spanish Empire", 1479, 1716), ("Crown of Castile", "Kingdom of Spain", 1479, 1716),
 ("Kingdom of Scotland", "Kingdom of England", 1652, 1660), ("Kingdom of Ireland", "Kingdom of England", 1541, 1801)]
Y = [0]
COARSE = re.compile(r"^(Tibet|Mongol Khanate|Later Mayan City-States|Warring States Japan|Holy Roman Empire Minor States|Balinese Kingdom|Ceylon|Swiss Confederation|Italian States|Malay States|Hausa States|Yoruba States|Akan States|Mossi States|Shan States|Rajput States|Bantu kingdoms)$", re.I)
PEOPLE = re.compile(r"peoples|tribes|nations|cultures|hunter|nomad|chiefdoms|confederations|clans|indigenous|aboriginal|foragers|pastoral", re.I)
def judge(t, m):
    """ok: map shows the ruler (or its overlord / the map's overlord matches); none_ok: no state where none ruled"""
    tr = t["ruler"]; ov = t.get("overlord")
    if tr.lower() == "none":
        if m is None or m.get("people") or PEOPLE.search(m.get("NAME") or ""): return "ok", "no state"
        return "state_where_none", m["NAME"]
    names = [tr] + (t.get("aliases") or [])
    if m is not None and any(same(m.get("NAME"), n) for n in names): return "ok", m["NAME"]
    if m is None or m.get("people") or PEOPLE.search(m.get("NAME") or ""): return "blank", (m or {}).get("NAME")
    names = [tr] + (t.get("aliases") or [])
    cand = [m.get("NAME"), m.get("SUBJECTO"), m.get("REGION")]
    for c in cand:
        if c and any(same(c, n) for n in names): return "ok", c
    if ov and any(c and same(c, ov) for c in cand): return "ok_overlord", m["NAME"]
    for a, b, y0, y1 in UNIONS:
        if y0 <= Y[0] < y1 and any(same(tr, a) or (ov and same(ov, a)) for _ in [0]) and any(c and same(c, b) for c in cand): return "ok_union", m["NAME"]
    if COARSE.search(m.get("NAME") or ""): return "coarse", m["NAME"]
    return "wrong", m["NAME"] + (f" (under {m['SUBJECTO']})" if m.get("SUBJECTO") else "")
def near_change(p, y, w=5):
    return any(abs(t["from"] - y) <= w for t in p["timeline"] if t["from"] > 1400)
if __name__ == "__main__":
    YEARS = sorted(set(range(1400, 2021, 5)) | set(HBY) - {2010} | {2010})
    srcs = {"atlas": atlas_at, "clio": clio_at, "hb": hb_at, "cs": cs_at}
    want = sys.argv[1:] or list(srcs)
    out = []
    for y in YEARS:
        for name in want:
            fn = srcs[name]
            if name == "clio" and y >= 1886: continue
            for i, p in enumerate(CP):
                if SUB != "all" and (i % 2 == 0) != (SUB == "even"): continue
                t = truth(p, y)
                if t is None: continue
                m = fn(p, y); Y[0] = y
                if m == "skip": break
                v, got = judge(t, m)
                out.append({"src": name, "y": y, "i": i, "place": p["place"], "region": p["region"], "kind": p.get("kind"), "truth": t["ruler"], "ov": t.get("overlord"), "conf": t.get("confidence"), "v": v, "got": got, "edge": near_change(p, y)})
        print(y, file=sys.stderr, flush=True)
    json.dump(out, open(ROOT + "/review/score_" + "_".join(want) + TAG + ".json", "w"))
