"""Who owns each province, year by year.
1400-1885: the corrected period maps (/tmp/g3/snapsF2): each province goes to the polity holding most of it,
  judged by sample points inside the province. Land of peoples is recorded as such.
1886-2019: CShapes 2.0 at mid-year, plus the land it leaves empty (csgaps), the same way.
Output /tmp/g4/own_base.json: {"pol": [[src, name, overlord, union, extra]], "prov": {id: [[year, pol], ...]}} with
pol 0 = no polity recorded. Later steps (estimate.py) fill the unowned provinces and apply research overrides."""
import json, math, sys, os
import numpy as np
from shapely.geometry import shape, Point
from shapely.validation import make_valid
from shapely import contains_xy, prepare
rng = np.random.default_rng(3)
F = json.load(open("/tmp/g4/prov.geojson"))["features"]
pid = [f["properties"]["id"] for f in F]
X, Y, O = [], [], []
for k, f in enumerate(F):
    g = make_valid(shape(f["geometry"])); prepare(g)
    rp = g.representative_point(); pts = [(rp.x, rp.y)]
    x0, y0, x1, y1 = g.bounds; tries = 0
    while len(pts) < 13 and tries < 6:
        xs = rng.uniform(x0, x1, 60); ys = rng.uniform(y0, y1, 60); ok = contains_xy(g, xs, ys)
        pts += list(zip(xs[ok], ys[ok]))[: 13 - len(pts)]; tries += 1
    for x, y in pts: X.append(x); Y.append(y); O.append(k)
X, Y, O = np.array(X), np.array(Y), np.array(O)
NP = len(F)
print(len(X), "sample points", file=sys.stderr, flush=True)
POL = [["", "", "", "", ""]]; PI = {}
def pol(src, name, ov, un="", extra=""):
    k = (src, name or "", ov or "", un or "", extra or "")
    if k not in PI: PI[k] = len(POL); POL.append(list(k))
    return PI[k]
def assign(feats):
    """feats: list of (polity index, geometry). Returns owner index per province (0 = none)."""
    votes = np.zeros((NP,), dtype=np.int32); best = np.zeros((NP,), dtype=np.int32); cnt = {}
    for pi, g in feats:
        x0, y0, x1, y1 = g.bounds
        m = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        if not m.any(): continue
        idx = np.nonzero(m)[0]
        try: ok = contains_xy(g, X[idx], Y[idx])
        except Exception: continue
        for o in O[idx[ok]]:
            key = (o, pi); cnt[key] = cnt.get(key, 0) + 1
    for (o, pi), c in cnt.items():
        if c > votes[o]: votes[o] = c; best[o] = pi
    return best
spans = json.load(open(os.environ.get("SPANS", "/tmp/g3/spans_f.json")))
SNAPS = os.environ.get("SNAPS", "/tmp/g3/snapsF2")
own = {}  # year -> owner array
for a, b in spans:
    fc = json.load(open(f"{SNAPS}/s{a}.geojson"))["features"]
    feats = []
    for f in fc:
        p = f["properties"]
        src = "pp" if p.get("k") == "p" else "cl"
        pi = pol(src, p.get("NAME"), p.get("SUBJECTO"), p.get("un"), p.get("fx") or "")
        try: g = make_valid(shape(f["geometry"]))
        except Exception: continue
        feats.append((pi, g))
    own[a] = assign(feats)
    print(a, file=sys.stderr, flush=True)
CSF = json.load(open("/tmp/rv/cs.geojson"))["features"]; GAP = json.load(open("/tmp/rv/csgaps.geojson"))["features"]
CSG = [(f["properties"], make_valid(shape(f["geometry"]))) for f in CSF if f.get("geometry")]
GPG = [(f["properties"], make_valid(shape(f["geometry"]))) for f in GAP if f.get("geometry")]
for y in range(1886, 2020):
    t = y + .5; feats = []
    for p, g in CSG:
        if p["a"] <= t < p["b"]: feats.append((pol("cs", p["r"], p["o"] or "", "", p.get("st") or ""), g))
    for p, g in GPG:
        if not (p["a"] <= y < p["b"]): continue
        if p.get("own"):
            own_ = p["own"]; feats.append((pol("cs", own_[0], own_[1] if len(own_) > 1 else "", "", "gap"), g))
        elif p.get("NAME"): feats.append((pol("gap", p["NAME"], "", "", ""), g))
    own[y] = assign(feats)
    if y % 10 == 0: print(y, file=sys.stderr, flush=True)
years = sorted(own)
prov = {}
for k in range(NP):
    tl = []; last = None
    for y in years:
        v = int(own[y][k])
        if v != last: tl.append([y, v]); last = v
    prov[pid[k]] = tl
json.dump({"pol": POL, "prov": prov, "years": years}, open("/tmp/g4/own_base.json", "w"))
print("polities", len(POL), "changes", sum(len(v) for v in prov.values()), file=sys.stderr)
