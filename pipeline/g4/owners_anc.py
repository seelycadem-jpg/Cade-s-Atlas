"""Who owns each province before 1400: from the first cities (3400 BCE) to 1399.
Time grid: every 25 years until Rome's founding (753 BCE), then every 10 years to 1390 (year 0 does not exist: 1 CE).
Sources, in order of precedence for each province and step:
 1. Cliopatria (Seshat) polity shapes active that year;
 2. states in the historical-basemaps world map in force (the latest snapshot at or before the year); a basemap state
    that mostly lies inside one Cliopatria polity is that polity (the two sources name the same realm differently);
 3. cultures and peoples of the basemaps, as named peoples' land (no state).
Output /tmp/g4/own_anc.json in the own_base format."""
import json, re, sys, glob, os
import numpy as np
from shapely.geometry import shape
from shapely.validation import make_valid
from shapely import contains_xy, prepare
rng = np.random.default_rng(3)
GRID = list(range(-3400, -753, 25)) + [-753] + list(range(-750, 0, 10)) + [1] + list(range(10, 1400, 10))
F = json.load(open("/tmp/g4/prov.geojson"))["features"]; NP = len(F)
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
POL = [["", "", "", "", ""]]; PI = {}
def pol(src, name, ov="", un="", extra=""):
    k = (src, name or "", ov or "", un or "", extra or "")
    if k not in PI: PI[k] = len(POL); POL.append(list(k))
    return PI[k]
def assign(feats, minvotes=1):
    votes = np.zeros(NP, dtype=np.int32); best = np.zeros(NP, dtype=np.int32); cnt = {}
    for pi, g, bb in feats:
        x0, y0, x1, y1 = bb
        m = (X >= x0) & (X <= x1) & (Y >= y0) & (Y <= y1)
        if not m.any(): continue
        idx = np.nonzero(m)[0]
        try: ok = contains_xy(g, X[idx], Y[idx])
        except Exception: continue
        for o in O[idx[ok]]: cnt[(o, pi)] = cnt.get((o, pi), 0) + 1
    for (o, pi), c in cnt.items():
        if c > votes[o] and c >= minvotes: votes[o] = c; best[o] = pi
    return best
# --- Cliopatria ---
CL = []
for f in json.load(open("/tmp/clio/cliopatria_polities_only_v021.geojson"))["features"]:
    p = f["properties"]
    if p.get("Type") != "POLITY" or p["FromYear"] >= 1400 or not f.get("geometry"): continue
    try: g = make_valid(shape(f["geometry"])); prepare(g)
    except Exception: continue
    CL.append((p["FromYear"], p["ToYear"], p["Name"], g, g.bounds))
print(len(CL), "Cliopatria shapes before 1400", file=sys.stderr, flush=True)
# --- historical basemaps ---
def hbyear(fn):
    s = os.path.basename(fn)[6:-8]
    return -int(s[2:]) if s.startswith("bc") else int(s)
HB = sorted((hbyear(fn), fn) for fn in glob.glob("/tmp/hb/geojson/world_*.geojson"))
HB = [(y, fn) for y, fn in HB if -5000 <= y <= 1400]
CULT = re.compile(r"cultur|hunter|gatherer|farmer|nomad|pastoral|tribe|people|aborigin|forag|fisher|fichers|Austronesians|Bantu|Khoisan|Semites|Dravidians|^Ainu$|J[oō]mon|Cycladic|Únětice|Beaker|Andronovo|Sintashta|Namazga|Afanasevo|Valdivia|Norte Chico|^Oxus$|^Thai$|Koreans|Tibeto|Tibetans|Arameans|Berbers|Celtiberians|Illyrians|Cimerians|Chinchor|Guanches|Saami|Vedic Aryans|Burmese|Sinic|Proto-|Paleo|Inuit|Dorset|Thule|Athabaskan|Innu|Beothuk|Arawaks|Ciboney|Malagasy|^Malay$|^Finns$|Karelians|Ests|Mordvinians|^Mari$|Bashkirs|Baltic|Slav|Germanic|Celts$|Scythians|Sarmatians|Saka$|Alans|Huns$|Xiongnu|Magyars|Northmen|Danes$|Czechs|Kipchak|Cuman|Turkic|Mongol|Tungus|Jurchen|Khitan(?! )|Hainan|Anasazi|Mogollon|Hohokam|Hopewell|Adena|Mississippian|Fremont|complex|Complex|Focus|^Miller$|^Porter$|Blemmyes|neolithic|megalith|Bronze Age|Urnfield|Hallstatt|La T[eè]ne", re.I)
hbcache = {}
def hbfeats(fn):
    if fn in hbcache: return hbcache[fn]
    out = []
    for f in json.load(open(fn))["features"]:
        p = f["properties"]; nm = (p.get("NAME") or "").strip()
        if not nm or not f.get("geometry"): continue
        try: g = make_valid(shape(f["geometry"])); prepare(g)
        except Exception: continue
        out.append((nm, bool(CULT.search(nm)) or nm in ("city-states",), (p.get("SUBJECTO") or "").strip(), g, g.bounds))
    hbcache.clear(); hbcache[fn] = out
    return out
own = {}
for t in GRID:
    cl = [(pol("cl", nm, "", "", "clio"), g, bb) for a, b, nm, g, bb in CL if a <= t <= b]
    oc = assign(cl)
    hfn = max((h for h in HB if h[0] <= t), default=HB[0])[1]
    H = hbfeats(hfn)
    st = [(pol("cl", nm, ov if ov and ov != nm else "", "", "hb"), g, bb) for nm, c, ov, g, bb in H if not c]
    pp = [(pol("pp", nm, "", "", "hb"), g, bb) for nm, c, ov, g, bb in H if c]
    os_ = assign(st); op = assign(pp)
    # a basemap state lying mostly inside one Cliopatria polity is that polity
    for s in np.unique(os_[os_ > 0]):
        ii = np.nonzero(os_ == s)[0]; held = oc[ii]; held = held[held > 0]
        if len(held) and np.bincount(held).max() >= .4 * len(ii):
            c = np.bincount(held).argmax(); free = ii[oc[ii] == 0]; oc[free] = c
    row = np.where(oc > 0, oc, np.where(os_ > 0, os_, op))
    own[t] = row
    if t % 500 == 0 or t == GRID[0]: print(t, len(cl), "clio", len(st), "hb states", len(pp), "cultures", file=sys.stderr, flush=True)
prov = {}
for k in range(NP):
    tl = []; last = None
    for t in GRID:
        v = int(own[t][k])
        if v != last: tl.append([t, v]); last = v
    prov[F[k]["properties"]["id"]] = tl
json.dump({"pol": POL, "prov": prov, "grid": GRID}, open("/tmp/g4/own_anc.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("polities", len(POL), file=sys.stderr)
