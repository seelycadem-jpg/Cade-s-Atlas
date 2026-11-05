"""Assemble maps/pieces.json (dated and undated transfers) and maps/changes.json (the yearly ledger)."""
import json, glob, subprocess, re
G = "/home/claude/g2"; M = "/home/claude/atlas/maps"
P = json.load(open(f"{G}/pieces.json"))
gj = json.load(open(f"{G}/pieces.geojson"))
D = {}
for f in sorted(glob.glob(f"{G}/dated_0*.json")) + [f"{G}/dated_fix.json"]:
    for x in json.load(open(f)): D[x["i"]] = x
feats, changes = [], []
IGNORE = {0}  # survey disagreements where neither map is right; handled by curated areas
nd = {"dated": 0, "undated": 0}
for i, p in enumerate(P):
    d = D.get(i)
    if i in IGNORE: continue
    if not d: continue
    if d["k"] == "artefact":
        # the later survey is taken as the better record for the whole interval
        d = dict(d, k="dated", y=p["a"], t=None, fixup=True)
    if d["k"] == "dated" and not d.get("fixup") and not (p["a"] < d["y"] <= p["b"]):
        d = dict(d, y=max(p["a"] + 1, min(p["b"], d["y"])))
    nd[d["k"]] += 1
    props = dict(id=i, a=p["a"], b=p["b"], k=d["k"], y=d.get("y"), NAME=p["tn"] or p["to"], SUBJECTO=(p["to"] if p["tk"].startswith("E:") and p["to"] != p["tn"] else None), frm=p["frm"], to=p["to"], ar=p["ar"], lp=[p["lon"], p["lat"]], t=d.get("t"), fx=1 if d.get("fixup") else 0)
    feats.append({"type": "Feature", "properties": props, "geometry": gj["features"][i]["geometry"]})
    if d["k"] == "dated" and d["y"] < 1886 and not d.get("fixup"):
        changes.append(dict(y=d["y"], d=str(d["y"]), t=d["t"] or f"{p['to']} takes land from {p['frm']}", k="transfer", lon=p["lon"], lat=p["lat"], ar=p["ar"], src="pc"))
json.dump({"type": "FeatureCollection", "features": feats}, open("/tmp/pieces_kept.geojson", "w"))
subprocess.run(["mapshaper", "-i", "/tmp/pieces_kept.geojson", "name=pieces", "-o", "format=topojson", "precision=0.01", f"{M}/pieces.json"], check=True, capture_output=True)
# survey notes: when a new survey map takes over, say how much changed at unrecorded dates
YEARS = [1400, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880]
for i, a in enumerate(YEARS[1:], 1):
    prev = YEARS[i - 1]; n = sum(1 for f in feats if f["properties"]["a"] == prev and f["properties"]["k"] == "undated")
    changes.append(dict(y=a, d=str(a), t=f"New survey map of {a}: borders redrawn" + (f"; {n} areas changed hands since {prev} at dates not recorded (hatched before {a})" if n else ""), k="survey", lon=None, lat=None, src="survey"))
changes.append(dict(y=1886, d="1886", t="From 1886 the borders follow a day-by-day record of states and colonies, changing when a treaty, annexation or independence took effect", k="survey", lon=None, lat=None, src="survey"))
cs = json.load(open(f"{G}/cs_changes.json")) + json.load(open(f"{G}/isl_changes.json"))
seen = set(); allc = []
for c in sorted(changes + cs, key=lambda c: (c["y"], c["d"], c["t"])):
    key = (c["y"], c["t"])
    if key in seen: continue
    seen.add(key); allc.append(c)
json.dump(allc, open(f"{M}/changes.json", "w"), separators=(",", ":"), ensure_ascii=False)
print(nd, "changes", len(allc))
