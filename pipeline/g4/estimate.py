"""Fill and correct province owners.
 A. islands with no recorded owner join the nearest owned province's polity (within 4 degrees);
 B. provinces with no state (none or peoples) go, where the researched gazetteer (/home/claude/review/gaz) places a
    polity, to the nearest such polity whose researched extent covers them (an estimate, marked src 'gaz');
 C. research control points (/home/claude/review/cp): a province whose researched ruler is a state the map does not
    show there takes that ruler when the map has no state, and a capital takes its researched ruler when the map
    names someone unrelated.
Input /tmp/g4/own_base.json, output /home/claude/atlas/maps/own.json."""
import json, glob, math, sys, os
import numpy as np
from shapely.geometry import shape, Point, MultiPoint
from shapely.validation import make_valid
from shapely import STRtree, contains_xy
sys.path.insert(0, "/home/claude/review"); from names import same
B = json.load(open("/tmp/g4/own_base.json")); POL = B["pol"]
# before 1400: the ancient grid (owners_anc.py), every 25 years to 753 BCE and every 10 years to 1390; from 1400 one row per year
A_ = json.load(open("/tmp/g4/own_anc.json")); AOFF = len(POL); POL += A_["pol"]
years = list(A_["grid"]) + list(range(1400, 2020))
F = json.load(open("/tmp/g4/prov.geojson"))["features"]; n = len(F)
pid = [f["properties"]["id"] for f in F]; ix = {p: i for i, p in enumerate(pid)}
G = [make_valid(shape(f["geometry"])) for f in F]
rp = [g.representative_point() for g in G]; CX = np.array([p.x for p in rp]); CY = np.array([p.y for p in rp])
nb = json.load(open("/tmp/g4/nb.json")); ADJ = [[] for _ in range(n)]
for k, v in nb.items():
    for j in v: ADJ[ix[int(k)]].append(ix[j])
PI = {tuple(p): i for i, p in enumerate(POL)}
def pol(*k):
    k = tuple(x or "" for x in k)
    if k not in PI: PI[k] = len(POL); POL.append(list(k))
    return PI[k]
# owners as a year x province matrix
Y = len(years); M = np.zeros((Y, n), dtype=np.int32)
for p, tl in B["prov"].items():
    i = ix[int(p)]; k = 0
    for yi, y in enumerate(years):
        if y < 1400: continue
        while k + 1 < len(tl) and tl[k + 1][0] <= y: k += 1
        M[yi, i] = tl[k][1] if tl[k][0] <= y else 0
for p, tl in A_["prov"].items():
    i = ix[int(p)]; k = 0
    for yi, y in enumerate(years):
        if y >= 1400: break
        while k + 1 < len(tl) and tl[k + 1][0] <= y: k += 1
        o = tl[k][1] if tl[k][0] <= y else 0
        M[yi, i] = o + AOFF if o else 0
import re
LUMP = re.compile(r"Minor States|^Later Mayan City-States$|^Warring States Japan$|^Italian States$|^Hausa States$|^Yoruba States$|^Akan States$|^Mossi States$|^Shan States$|^Rajput States$|^Khanates of the Caucasus$|^Malay States$|^Bantu kingdoms$|^Balinese Kingdom$|^Ceylon$|^Tibet$", re.I)
_PR = re.compile(r"peoples|tribes|nomads|nations|cultures|hunter|gatherer|chiefdoms|confederations|clans|aboriginal|indigenous|foragers|herders|pastoral|bedouin|communities|^Lozi$|^Shona$|^Yeke$|^Nguni$|Khoisan|Bantu", re.I)
for p in POL:
    if p[0] == "gap" and _PR.search(p[1] or ""): p[0] = "pp"  # land the post-1886 record leaves empty, named after its peoples, is peoples' land
isppl = np.array([p[0] == "pp" for p in POL] + [False] * 20000)
islump = np.array([bool(LUMP.search(p[1] or "")) for p in POL] + [False] * 20000)
def ppl_mask(row): return (row == 0) | isppl[row] | islump[row]
# ---------- peoples' land carrying a state's own name is that state's land ----------
PEO_RE = re.compile(r"peoples|tribes|nomads|nations|cultures|hunter|gatherer|chiefdoms|confederations|clans|aboriginal|indigenous|foragers|herders|pastoral|bedouin|communities|settlers|villages", re.I)
byname = {}
for o, p in enumerate(POL):
    if p[0] != "pp" and p[1]: byname.setdefault(p[1], o)
remap = {}
for o, p in enumerate(POL):
    if p[0] == "pp" and p[1] and not PEO_RE.search(p[1]) and p[1] in byname: remap[o] = byname[p[1]]
if remap:
    lut = np.arange(len(POL) + 20000, dtype=np.int32)
    for a_, b_ in remap.items(): lut[a_] = b_
    M[:] = lut[M]
print("peoples labels that were states", len(remap), file=sys.stderr)
# ---------- one polity, one name: names that differ only in word order or a generic title are merged ----------
_GEN = {"of", "the", "kingdom", "sultanate", "empire", "dynasty", "state", "chiefdom", "confederacy", "confederation", "realm"}
def _nk(nm):
    import unicodedata as _u
    t = _u.normalize("NFKD", nm or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"\(.*?\)", " ", t); ws = [w for w in re.findall(r"[a-z]+", t) if w not in _GEN]
    return " ".join(sorted(set(ws)))
grp = {}
for o, p in enumerate(POL):
    if p[0] in ("pp", "cs") or not p[1]: continue  # modern (CShapes) names stay as they are
    k = _nk(p[1])
    if k: grp.setdefault(k, set()).add(p[1])
use_ct = {}
for o in np.unique(M):
    pass
tot = np.bincount(M.ravel(), minlength=len(POL))
nm_ct = {}
for o, p in enumerate(POL):
    if o < len(tot): nm_ct[p[1]] = nm_ct.get(p[1], 0) + int(tot[o])
canon = {}
for k, names in grp.items():
    if len(names) < 2: continue
    best = max(names, key=lambda x: nm_ct.get(x, 0))
    for x in names: canon[x] = best
nmg = 0
for p in POL:
    if p[0] not in ("pp", "cs") and p[1] in canon and canon[p[1]] != p[1]: p[1] = canon[p[1]]; nmg += 1
print("names merged", nmg, file=sys.stderr)
# ---------- stray pieces: a colony, kingdom or people found far from the rest of its land is misfiled ----------
EMP = re.compile(r"Empire|Colonial|Republic of the Netherlands|Dutch Republic|United Kingdom|Kingdom of Great Britain|Kingdom of England|Kingdom of Spain|Kingdom of Portugal|Kingdom of France|French|Spanish|Portuguese|British|Dutch|Danish|Denmark|Swedish|Ottoman|Russia|Soviet|United States|Japan|Germany|Italy|Belgi|Norway|Ma.*Order|Knights|Company", re.I)
nstray = 0
own_sets = {}
for i in range(n):
    for o in np.unique(M[:, i]):
        if o: own_sets.setdefault(int(o), []).append(i)
for o, provs in own_sets.items():
    if len(provs) < 2 or EMP.search(POL[o][1] or "") or EMP.search(POL[o][2] or ""): continue
    P_ = np.array(provs); xs, ys = CX[P_], CY[P_]
    # largest cluster by chaining provinces less than 6 degrees apart
    lab = -np.ones(len(P_), dtype=int); c = 0
    for s0 in range(len(P_)):
        if lab[s0] >= 0: continue
        st = [s0]; lab[s0] = c
        while st:
            u = st.pop(); d = np.hypot((xs - xs[u]) * np.cos(np.radians(ys[u])), ys - ys[u])
            for v in np.nonzero((d < 6) & (lab < 0))[0]: lab[v] = c; st.append(v)
        c += 1
    if c == 1: continue
    sizes = np.bincount(lab); main = sizes.argmax(); mi = np.nonzero(lab == main)[0]
    for k in np.nonzero(lab != main)[0]:
        d = np.hypot((xs[mi] - xs[k]) * np.cos(np.radians(ys[k])), ys[mi] - ys[k]).min()
        if d > 20:
            col = M[:, P_[k]]; m_ = col == o; col[m_] = 0; nstray += int(m_.sum())
print("stray province-years cleared", nstray, file=sys.stderr)
# ---------- 0. continuity: no flashes of empty land, no blips of three years or less (record before 1886) ----------
yrs = np.array(years); dur = np.diff(np.append(yrs, 2026))
pre = int(np.searchsorted(yrs, 1886))
nh = nbp = 0
for i in range(n):
    col = M[:pre, i]
    # a hole between two years with the same owner, or after land of peoples, is filled from before
    for k in range(1, pre):
        if col[k] == 0 and col[k - 1] != 0:
            j = k
            while j < pre and col[j] == 0 and yrs[j] - yrs[k] <= 12: j += 1
            if j < pre and (col[j] == col[k - 1] or isppl[col[k - 1]]) and yrs[j] - yrs[k] <= 12:
                col[k:j] = col[k - 1]; nh += j - k
    for _ in range(2):
        k = 1
        while k < pre - 1:
            if col[k] != col[k - 1]:
                j = k
                while j < pre and col[j] == col[k]: j += 1
                gap = yrs[j] - yrs[k] if j < pre else 99
                short = gap <= 3 or (gap <= 8 and (isppl[col[k]] or isppl[col[k - 1]])) or (gap <= 15 and col[k] == 0 and not isppl[col[k - 1]])  # the record samples years, so state/peoples alternations of a few years are its artefact  # land with no record at all between two spells of the same state; peoples' land stays theirs  # a state losing land to no state and regaining it within 15 years is the record's sampling
                if j < pre and col[j] == col[k - 1] and short and col[k - 1] != 0:
                    col[k:j] = col[k - 1]; nbp += j - k
                k = j
            else: k += 1
    M[:pre, i] = col
print("holes filled", nh, "blips removed", nbp, file=sys.stderr)
# ---------- names the record carries past their time ----------
REN = [("Khmer Empire", 1431, 9999, "Kingdom of Cambodia"),
       ("United States", 0, 9999, "United States of America"), ("Haudenosaunee Confederacy", 0, 9999, "Haudenosaunee"),
       ("Calusa chiefdom", 0, 9999, "Calusa"), ("Natchez chiefdom", 0, 9999, "Natchez"), ("Powhatan Confederacy", 0, 9999, "Powhatan"),
       ("Powhatan Paramount Chiefdom", 0, 9999, "Powhatan"), ("Powhatan", 0, 0, "Powhatan"), ("Comanchería", 0, 9999, "Comanche"), ("Comancheria", 0, 9999, "Comanche"),
       ("Ming dynasty", 0, 9999, "Ming Dynasty"), ("Qing dynasty", 0, 9999, "Qing Dynasty"), ("Livonian Conference", 0, 9999, "Livonian Confederation"),
       ("Kingdom of Hawaï'i", 0, 9999, "Kingdom of Hawaii")]
for nm, a, b, new in REN:
    olds = [o for o, p in enumerate(POL) if p[1] == nm]
    for yi, y in enumerate(years):
        if a <= y < b:
            for o in olds:
                m = M[yi] == o
                if m.any(): src, _, ov, un, ex = POL[o]; M[yi][m] = pol(src, new, ov, un, ex)
# renames that hold only inside a box (lon0, lon1, lat0, lat1): one record name used for two different realms
RENB = [("Golden Horde", 1466, 1503, "Great Horde", (-180, 180, -90, 90)),
        ("Small Horde", 1400, 1800, "Lesser Nogai Horde", (34, 48, 42, 49.5)),
        ("Astrakhan Khanate", 1557, 1800, "Lesser Nogai Horde", (34, 46, 42, 48)),
        ("House of Jagiellon", 1400, 1570, "Grand Duchy of Lithuania", (26, 42, 44, 57)),
        ("New Netherland", 1600, 1820, "Dutch Republic", (-75, -30, -35, 15)),
        ("Omani Slave Coast", 1400, 1856, "Oman", (-180, 180, -90, 90))]
for nm, a, b, new, (x0, x1, y0, y1) in RENB:
    olds = np.array([o for o, p in enumerate(POL) if p[1] == nm], dtype=np.int32)
    inb = (CX >= x0) & (CX <= x1) & (CY >= y0) & (CY <= y1)
    for yi, y in enumerate(years):
        if a <= y < b and len(olds):
            m = np.isin(M[yi], olds) & inb
            for o in np.unique(M[yi][m]):
                src, _, ov, un, ex = POL[o]; mm = m & (M[yi] == o); M[yi][mm] = pol(src, new, ov, un, ex)
# ---------- Iberian Union (1580-1640): Portugal's colonies keep their Portuguese name under the shared crown ----------
y79 = years.index(1579); isspain = np.array([bool(re.search(r"Spanish Empire|Kingdom of Spain|Iberian Union", p[1] or "")) for p in POL] + [False] * 20000)
isport = np.array([bool(re.search(r"Portug", p[1] or "")) for p in POL] + [False] * 20000)
nib = 0
for yi, y in enumerate(years):
    if 1580 <= y < 1640:
        row = M[yi]; m_ = isspain[row] & isport[M[y79]]
        row[m_] = M[y79][m_]; nib += int(m_.sum())
print("Portuguese colonies kept under the union", nib, file=sys.stderr)
# ---------- A. islands ----------
island = np.array([len(ADJ[i]) == 0 for i in range(n)])
na = 0
for yi in range(Y):
    row = M[yi]; un = np.nonzero((row == 0) & island)[0]
    if not len(un): continue
    own = np.nonzero(row != 0)[0]
    if not len(own): continue
    for i in un:
        d = (CX[own] - CX[i]) ** 2 * math.cos(math.radians(CY[i])) ** 2 + (CY[own] - CY[i]) ** 2
        j = d.argmin()
        if d[j] <= 16: row[i] = row[own[j]]; na += 1
print("island fills", na, file=sys.stderr)
# ---------- B. gazetteer ----------
GAZ = []
for f in sorted(glob.glob("/home/claude/review/gaz/*.json")):
    try: d = json.load(open(f))
    except Exception as e: print("bad", f, e, file=sys.stderr); continue
    for p in d.get("polities", []):
        try:
            if p.get("seat") and p.get("from") is not None and p.get("to") is not None and float(p["seat"]["lat"]) and True: GAZ.append(p)
        except Exception: pass
print(len(GAZ), "gazetteer polities", file=sys.stderr)
def kmdeg(lat): return 111.32 * max(.2, math.cos(math.radians(lat)))
def phases(p):
    base = {"from": p["from"], "to": p["to"], "seat": p["seat"], "extent": p.get("extent"), "reach_km": p.get("reach_km")}
    out = []
    for ph in p.get("phases") or []:
        try: out.append({"from": ph["from"], "to": ph["to"], "seat": ph.get("seat") or p["seat"], "extent": ph.get("extent") or p.get("extent"), "reach_km": ph.get("reach_km") or p.get("reach_km")})
        except Exception: pass
    if not out: out = [base]
    return out
UMB = re.compile(r"^(Russian Siberia.*|Holy Roman Empire|Confederation of the Rhine|German Confederation|Burgundian State|North German Confederation)$")
GP = []  # (polity, from, to, seat point, candidate province indices, overlord list)
for p in GAZ:
    for ph in phases(p):
        try:
            s = Point(float(ph["seat"]["lon"]), float(ph["seat"]["lat"]))
            area = None
            if ph.get("extent") and len(ph["extent"]) >= 3:
                pts = [(float(q[1]), float(q[0])) for q in ph["extent"]] + [(s.x, s.y)]
                xs = [p_[0] for p_ in pts]; ys = [p_[1] for p_ in pts]
                if max(xs) - min(xs) <= 60 and max(ys) - min(ys) <= 45:  # an outline wider than this crosses the 180th meridian or is a mistake
                    area = MultiPoint(pts).convex_hull.buffer(0.3)
            if area is None or area.area < 0.05:
                r = float(ph.get("reach_km") or 120) / kmdeg(s.y); area = s.buffer(r)
            area = make_valid(area)
            cand = np.nonzero(contains_xy(area, CX, CY))[0]
            # the seat's own province always belongs
            si = [i for i in range(n) if G[i].bounds[0] <= s.x <= G[i].bounds[2] and G[i].bounds[1] <= s.y <= G[i].bounds[3] and G[i].contains(s)]
            cand = np.unique(np.concatenate([cand, np.array(si, dtype=int)])) if si else cand
            GP.append((p, int(ph["from"]), int(ph["to"]), s, cand))
        except Exception as e:
            pass
print(len(GP), "gazetteer phases", file=sys.stderr)
def ovl(p, y):
    for o in p.get("overlord") or []:
        try:
            if o["from"] <= y < o["to"]: return o["name"]
        except Exception: pass
    return ""
_mc = {}
def present_has(nm, present):
    """is a polity of this name (by lineage) already on the map this year? matches are cached per name pair"""
    for q in present:
        k = (nm, q)
        v = _mc.get(k)
        if v is None: v = _mc[k] = same(nm, q)
        if v: return True
    return False
nb_ = 0
for yi, y in enumerate(years):
    row = M[yi]; open_ = ppl_mask(row)
    present = {POL[o][1] for o in np.unique(row) if o and not isppl[o] and not islump[o]}
    best = np.full(n, 1e9); who = np.full(n, -1)
    for k, (p, a, b, s, cand) in enumerate(GP):
        if not (a <= y < b) or not len(cand): continue
        c = cand[open_[cand]]
        if not len(c): continue
        if present_has(p["name"], present): continue
        if UMB.search(p["name"]): continue  # umbrella realms are drawn through their members
        d = (CX[c] - s.x) ** 2 * math.cos(math.radians(s.y)) ** 2 + (CY[c] - s.y) ** 2
        better = d < best[c]; best[c[better]] = d[better]; who[c[better]] = k
    for i in np.nonzero(who >= 0)[0]:
        p = GP[who[i]][0]; row[i] = pol("gaz", p["name"], ovl(p, y), "", "gaz"); nb_ += 1
print("gazetteer province-years", nb_, file=sys.stderr)
# ---------- C. research control points ----------
CP = [p for f in sorted(glob.glob("/home/claude/review/cp/*.json")) for p in json.load(open(f))["places"]]
T = STRtree(G)
def prov_of(x, y):
    pt = Point(x, y); hit = [i for i in T.query(pt) if G[i].contains(pt)]
    if hit: return hit[0]
    near = [i for i in T.query(pt.buffer(0.15))]
    return min(near, key=lambda i: G[i].distance(pt)) if near else None
nc = 0
for p in CP:
    i = prov_of(p["lon"], p["lat"])
    if i is None: continue
    for yi, y in enumerate(years):
        t = next((t for t in p["timeline"] if t["from"] <= y < t["to"]), None)
        if not t or t["ruler"] == "none": continue
        o = M[yi, i]; names = [t["ruler"]] + (t.get("aliases") or []); ov = t.get("overlord") or ""
        if isinstance(ov, list): ov = "; ".join(ov)
        if o and not isppl[o]:
            src, nm, so, un, ex = POL[o]
            cand = [nm, so, un]
            if src == "cs": cand = [nm, so]
            ok = any(c and (any(same(c, x) for x in names) or (ov and same(c, ov))) for c in cand)
            if ok or p.get("kind") != "capital": continue
        M[yi, i] = pol("cp", t["ruler"], ov, "", "research"); nc += 1
print("research province-years", nc, file=sys.stderr)
# ---------- labels that spill out of their own country: valid only inside a box (lon0, lon1, lat0, lat1) ----------
BOXONLY = [("Qatari tribes (Al-Buainain, Al Musallam)", (50, 52, 24, 26.5)), ("Arab coastal and Bedouin tribes of Qatar", (50, 52.5, 24, 26.5)),
           ("Denmark-Norway", (-60, 32, 50, 82))]
for nm, (x0, x1, y0, y1) in BOXONLY:
    olds = np.array([o for o, p in enumerate(POL) if p[1] == nm], dtype=np.int32)
    out_ = ~((CX >= x0) & (CX <= x1) & (CY >= y0) & (CY <= y1))
    for yi in range(Y):
        m = np.isin(M[yi], olds) & out_
        if m.any(): M[yi][m] = 0
# ---------- E. filling: no blank pockets where a state plainly held the land ----------
isppl = np.array([p[0] == "pp" for p in POL] + [False] * 20000)
islump = np.array([bool(LUMP.search(p[1] or "")) for p in POL] + [False] * 20000)
COSY = np.cos(np.radians(CY))
# E1. peoples labels that carry a state's name: that state's land when the state is near, else nobody's
ppstate = {}
_stk = {_nk(p[1]) for p in POL if p[0] != "pp" and p[1]} - {""}
for o, p in enumerate(POL):
    if p[0] == "pp" and p[1] and not PEO_RE.search(p[1]) and (_nk(p[1]) in _stk or p[1] == "Poland-Lithuania" or EMP.search(p[1]) or "–" in p[1] or "shogunate" in p[1]): ppstate[o] = p[1]
ne1 = 0
for yi, y in enumerate(years):
    row = M[yi]; hit = np.nonzero(np.isin(row, list(ppstate)))[0]
    if not len(hit): continue
    states = [o for o in np.unique(row) if o and not isppl[o]]
    for o in np.unique(row[hit]):
        nm = ppstate[int(o)]
        if nm == "Poland-Lithuania": nm = "Grand Duchy of Lithuania" if y < 1569 else "Polish-Lithuanian Commonwealth"
        cands = [s for s in states if POL[s][1] == nm or _nk(POL[s][1]) == _nk(nm)]
        ii = hit[row[hit] == o]
        for i in ii:
            best, bd = 0, 1e9
            for s in cands:
                js = np.nonzero(row == s)[0]
                d = np.hypot((CX[js] - CX[i]) * COSY[i], CY[js] - CY[i]).min()
                if d < bd: best, bd = s, d
            row[i] = best if bd <= 8 else 0; ne1 += 1
print("peoples labels with state names resolved", ne1, file=sys.stderr)
# E2. short spells of no record between two different states (up to 25 years): split between them
ne2 = 0
for i in range(n):
    col = M[:pre, i]; k = 1
    while k < pre:
        if col[k] == 0 and col[k - 1] != 0:
            j = k
            while j < pre and col[j] == 0: j += 1
            if j < pre and yrs[j] - yrs[k] <= 25:
                h = (k + j) // 2; col[k:h] = col[k - 1]; col[h:j] = col[j]; ne2 += j - k
            k = j
        else: k += 1
    M[:pre, i] = col
print("short no-record spells filled", ne2, file=sys.stderr)
# E3. small pockets of open land (no state, peoples, lumped) wholly surrounded by one state belong to it
ne3 = 0
landnb = [np.array(a, dtype=np.int32) for a in ADJ]
for yi, y in enumerate(years):
    row = M[yi]; op = (row == 0) | isppl[row] | islump[row]
    seen = np.zeros(n, bool)
    for s0 in np.nonzero(op & ~island)[0]:
        if seen[s0]: continue
        comp = [s0]; seen[s0] = True; k = 0; border = set(); big = False
        while k < len(comp):
            u = comp[k]; k += 1
            for v in landnb[u]:
                if op[v]:
                    if not seen[v]: seen[v] = True; comp.append(v)
                else: border.add(int(row[v]))
            if len(comp) > 12: big = True
        if big or len(border) != 1: continue
        o = border.pop(); row[comp] = o; ne3 += len(comp)
print("enclosed pockets filled", ne3, file=sys.stderr)
isppl = np.array([p[0] == "pp" for p in POL] + [False] * 20000)
# ---------- D. reviewers' corrections (/home/claude/review/fix/*.json), by modern country and region ----------
import re as _re
def base(nm): return _re.sub(r"( islands)?( \d+)?$", "", nm).strip()
PC = [F[i]["properties"]["c"] for i in range(n)]; PB = [base(F[i]["properties"]["n"]) for i in range(n)]
nf = 0; bad = []
for f in sorted(glob.glob("/home/claude/review/fix/*.json")):
    try: fixes = json.load(open(f))
    except Exception as e: print("bad fix file", f, e, file=sys.stderr); continue
    if isinstance(fixes, dict): fixes = fixes.get("fixes", [])
    for fx in fixes:
        try:
            a, b = int(fx["from"]), int(fx["to"]); regs = fx.get("regions") or ["*"]; exc = set(fx.get("except") or [])
            if fx.get("at"):  # [lon, lat]: just the province holding that place (a port, an island, an enclave)
                hit = prov_of(float(fx["at"][0]), float(fx["at"][1])); sel = [hit] if hit is not None else []
            else: sel = [i for i in range(n) if PC[i] == fx["country"] and ("*" in regs or PB[i] in regs) and PB[i] not in exc]
            if not sel: bad.append((f, fx.get("country"), regs[:3])); continue
            ow = fx.get("owner") or ""
            if ow.startswith("peoples:"): o = pol("pp", ow[8:].strip(), "", "", "review")
            else: o = 0 if ow.lower() in ("none", "") else pol("fix", ow, fx.get("overlord") or "", fx.get("union") or "", "review")
            for yi, y in enumerate(years):
                if a <= y < b:
                    if fx.get("only_open"):  # fill only land with no state, so states sharing the region are kept
                        row = M[yi]; ss = np.array(sel); ss = ss[(row[ss] == 0) | isppl[row[ss]] | islump[row[ss]]]; row[ss] = o
                    else: M[yi, sel] = o
                    nf += 1
        except Exception as e: bad.append((f, str(e)[:60], ""))
print("review corrections province-years", nf, "unmatched", len(bad), file=sys.stderr)
if bad: json.dump(bad, open("/tmp/g4/fix_unmatched.json", "w"), indent=0, ensure_ascii=False)
# ---------- F. statehood test for the native Americas ----------
# A native polity is drawn as a country when it passes either test:
#  (1) state-level society: a ruler or council governing more than one town from a fixed seat and taking tribute
#      (empires, kingdoms, city-states, Mesoamerican/Andean/Caribbean lordships, paramount chiefdoms, the Haudenosaunee);
#  (2) treaty era: from the first year a colonial or settler state holds land within about 250 km (its frontier), when nations were
#      dealt with as sovereigns (alliances, treaties, wars).
# Otherwise its land is drawn as the named homeland of a people (neutral colour, name shown when zoomed in).
NAT = {}
for f in ("n_america", "latin_america"):
    try: d = json.load(open(f"/home/claude/review/gaz/{f}.json"))
    except Exception: continue
    for p in d.get("polities", []):
        for nm in [p["name"]] + (p.get("aliases") or []):
            if nm: NAT.setdefault(nm, p.get("kind") or "")
STATE_KINDS = {"empire", "kingdom", "city-state", "other"}
PASS = {"Aztec Triple Alliance", "Tepanec Empire", "Inca Empire", "Muisca Confederation", "Michoacán", "Tarascan State", "Later Mayan City-States",
        "Haudenosaunee", "Haudenosaunee Confederacy", "Natchez", "Calusa", "Calusa chiefdom", "Piscataway", "Piscataway chiefdom", "Powhatan", "Powhatan Paramount Chiefdom",
        "Tlaxcala", "Chalco Confederation", "League of Mayapan", "Chakan (Maya province)", "Totonacapan", "Huaxtec chiefdoms", "Colima chiefdom", "Tonallan",
        "Matlatzinca", "Xoconochco", "Zinacantan", "Uspantán", "Izalco", "Copán Chʼortiʼ", "Nicarao", "Chorotega Mangue", "Nicoya", "Coclé chiefdoms", "Urracá",
        "Lenca chiefdoms", "Kowoj", "Yalain", "Zipazgo of Bacatá", "Zacazgo of Hunza", "Iraca", "Tundama", "Guane", "Tairona", "Zenú", "Quimbaya",
        "Chanka Confederation", "Huanca Confederation", "Chachapoya", "Charcas Confederation", "Cañari", "Caranqui-Cayambe Confederation", "Manteño-Huancavilca",
        "Ychsma", "Puruhá", "Diaguita-Calchaquí", "Coosa", "Cofitachequi", "Joara", "Ocute", "Tascalusa", "Moundville", "Casqui", "Pacaha", "Apalachee",
        "Timucua chiefdoms", "Pueblo Revolt confederacy", "Mapuche of Araucanía", "Tahue chiefdoms", "Opata", "Caxcan"}
def _maya(nm): return nm in NAT and NAT[nm] == "chiefdom" and nm in ("Ah Canul", "Chakan", "Ceh Pech", "Ah Kin Chel", "Hocabá", "Maní", "Sotuta", "Cupul", "Tases", "Chikinchel", "Ecab", "Cozumel", "Cochuah", "Uaymil", "Chetumal", "Chakan Putum")
TAINO = re.compile(r"^Taíno|^Borikén$|^Lucayan$")
for nm in PASS: NAT.setdefault(nm, "pass")
def always(nm):  # a state named only by the period maps (Olmec, Teotihuacan, Moche, Tiwanaku...) is state-level by their judgment
    if nm not in NAT: return True
    k = NAT.get(nm, ""); return k in STATE_KINDS or nm in PASS or _maya(nm) or bool(TAINO.search(nm))
CTRY = {f["properties"]["ADMIN"]: f["properties"]["CONTINENT"] for f in json.load(open("/tmp/nev/geojson/ne_10m_admin_0_countries.geojson"))["features"]}
AMER = np.array([CTRY.get(F[i]["properties"]["c"], "") in ("North America", "South America") or F[i]["properties"]["c"] in ("Falkland Islands", "Greenland") or (-125 < CX[i] < -25 and CY[i] > -60) for i in range(n)])
PRE = set()  # every state in the Americas before 1492 is native
for yi in range(years.index(1491) + 1):
    for o in np.unique(M[yi][AMER]): PRE.add(POL[o][1])
isnat = np.zeros(len(POL) + 20000, bool); isnat[[o for o, p in enumerate(POL) if p[0] != "pp" and (p[1] in NAT or p[1] in PRE)]] = True
from scipy.spatial import cKDTree
isppl = np.array([p[0] == "pp" for p in POL] + [False] * 20000)
XY = np.c_[CX * COSY, CY]
first = {}  # first treaty-era year per native name
nf2 = 0
for yi, y in enumerate(years):
    row = M[yi]; amer_owned = AMER & (row != 0)
    col_mask = amer_owned & ~isnat[row] & ~isppl[row]
    natv = np.nonzero(AMER & isnat[row])[0]
    if not len(natv): continue
    tree = cKDTree(XY[col_mask]) if col_mask.any() and y >= 1492 else None
    for o in np.unique(row[natv]):
        nm = POL[o][1]
        if always(nm): continue
        ii = natv[row[natv] == o]
        if nm not in first and tree is not None:
            d, _ = tree.query(XY[ii], k=1)
            if d.min() <= 2.5: first[nm] = y
        if nm in first and y >= first[nm]: continue
        row[ii] = pol("pp", nm, "", "", "native"); nf2 += len(ii)
print("native lands shown as peoples' homelands (province-years)", nf2, "; nations in the treaty era", len(first), file=sys.stderr)
json.dump({k: v for k, v in sorted(first.items(), key=lambda kv: kv[1])}, open("/tmp/g4/native_first.json", "w"), indent=0, ensure_ascii=False)
# ---------- write ----------
prov = {}
for i in range(n):
    tl = []; last = None
    for yi, y in enumerate(years):
        v = int(M[yi, i])
        if v != last: tl.append([y, v]); last = v
    prov[pid[i]] = tl
json.dump({"pol": POL, "prov": prov}, open("/home/claude/atlas/maps/own.json", "w"), separators=(",", ":"), ensure_ascii=False)
print("polities", len(POL), "changes", sum(len(v) for v in prov.values()), os.path.getsize("/home/claude/atlas/maps/own.json") // 1024, "KB", file=sys.stderr)
