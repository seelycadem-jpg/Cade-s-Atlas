"""Move recorded border changes to the year the research dates them.
The reference record changes its shapes at sample years. For each researched change of ruler at a place (A to B in
year T), find where the record makes the same change at that place (year T', within 35 years) and move that change
of the two polities' shapes to T: B's new shape starts at T and A's old shape ends at T (with their neighbouring
versions adjusted to meet). Where several places date the same change, the median year is used.
Input /tmp/g3/rows.json, output /tmp/g3/rows_t.json and /tmp/g3/retime_log.json."""
import json, os, sys, glob, statistics, collections
from shapely.geometry import shape, Point
from shapely import STRtree
from shapely.validation import make_valid
sys.path.insert(0, "/home/claude/review"); from names import same
EVID = os.environ.get("EVID", "all")
CP = [p for f in sorted(glob.glob("/home/claude/review/cp/*.json")) for p in json.load(open(f))["places"]]
if EVID != "all": CP = [p for i, p in enumerate(CP) if (i % 2 == 0) == (EVID == "even")]
ROWS = json.load(open(os.environ.get("IN", "/tmp/g3/rows.json")))
P = [r["properties"] for r in ROWS]
G = [make_valid(shape(r["geometry"])) for r in ROWS]
T = STRtree(G)
byname = collections.defaultdict(list)
for i, p in enumerate(P): byname[p["NAME"]].append(i)
def owner(pt, y, cand):
    hit = [i for i in cand if P[i]["a"] <= y < P[i]["b"] and G[i].contains(pt)]
    return min(hit, key=lambda i: G[i].area) if hit else None
def is_(i, t):
    if i is None or t is None: return t is not None and t["ruler"] == "none" and i is None
    n = P[i]["NAME"]; s = P[i].get("SUBJECTO")
    if t["ruler"] == "none": return False
    names = [t["ruler"]] + (t.get("aliases") or [])
    return any(same(n, x) for x in names) or (s and any(same(s, x) for x in names))
props = collections.defaultdict(list)  # (rowA_old, rowB_new, T') -> [T]
for p in CP:
    pt = Point(p["lon"], p["lat"]); cand = list(T.query(pt))
    tl = p["timeline"]
    for k in range(1, len(tl)):
        tA, tB, Ty = tl[k - 1], tl[k], tl[k]["from"]
        if not (1405 <= Ty <= 1880) or tA["ruler"] == "none" or tB["ruler"] == "none": continue
        if is_(owner(pt, Ty, cand), tB) and is_(owner(pt, Ty - 1, cand), tA): continue  # already right
        # search the record's own change at this place
        best = None
        for d in range(1, 36):
            for Tp in (Ty - d, Ty + d):
                if Tp <= 1400 or Tp >= 1886: continue
                a0, b0 = owner(pt, Tp - 1, cand), owner(pt, Tp, cand)
                if a0 is not None and b0 is not None and a0 != b0 and is_(a0, tA) and is_(b0, tB) and P[a0]["b"] == Tp and P[b0]["a"] == Tp:
                    best = (a0, b0, Tp); break
            if best: break
        if best: props[best].append(Ty)
edits = {}; log = []
for (a0, b0, Tp), ts in props.items():
    Tn = int(round(statistics.median(ts)))
    if Tn == Tp: continue
    A, B = P[a0]["NAME"], P[b0]["NAME"]
    an = next((i for i in byname[A] if P[i]["a"] == Tp), None)   # A's next version
    bp = next((i for i in byname[B] if P[i]["b"] == Tp), None)   # B's previous version
    if Tn < Tp:
        if Tn <= P[a0]["a"] or (bp is not None and Tn <= P[bp]["a"]): continue
        ch = {a0: ("b", Tn), b0: ("a", Tn)}
        if an is not None: ch[an] = ("a", Tn)
        if bp is not None: ch[bp] = ("b", Tn)
    else:
        if Tn >= P[b0]["b"] or (an is not None and Tn >= P[an]["b"]): continue
        ch = {a0: ("b", Tn), b0: ("a", Tn)}
        if an is not None: ch[an] = ("a", Tn)
        if bp is not None: ch[bp] = ("b", Tn)
    if any(i in edits and edits[i] != v for i, v in ch.items()): continue  # conflicting moves: leave the record as it is
    edits.update(ch); log.append({"from": A, "to": B, "record": Tp, "research": Tn, "places": len(ts)})
for i, (k, v) in edits.items(): P[i][k] = v
ROWS = [r for r in ROWS if r["properties"]["a"] < r["properties"]["b"]]
json.dump(ROWS, open(os.environ.get("OUT", "/tmp/g3/rows_t.json"), "w"))
json.dump(log, open(os.environ.get("LOG", "/tmp/g3/retime_log.json"), "w"), indent=0)
print("changes moved", len(log), "rows edited", len(edits))
