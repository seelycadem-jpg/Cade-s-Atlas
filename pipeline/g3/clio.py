"""Borders 1400-1885 from Cliopatria (Seshat Global History Databank, CC BY 4.0).
Base polities are the territories drawn; parenthesised rows are unions (an empire with its parts) and
relations (vassalage). Consecutive rows of one polity with the same outline are merged.
Writes /tmp/g3/base.geojson and /tmp/g3/agg.geojson with a (first year) and b (year after the last)."""
import json, hashlib, os, re, sys
os.makedirs("/tmp/g3", exist_ok=True)
d = json.load(open("/tmp/clio/cliopatria_polities_only_v021.geojson"))
Y0, Y1 = 1400, 1885
rows = [f for f in d["features"] if f["properties"]["ToYear"] >= Y0 and f["properties"]["FromYear"] <= Y1 and f.get("geometry")]
def gh(g): return hashlib.md5(json.dumps(g["coordinates"], separators=(",", ":")).encode()).hexdigest()
def merge(fs):
    by = {}
    for f in fs: by.setdefault(f["properties"]["Name"], []).append(f)
    out = []
    for n, L in by.items():
        L.sort(key=lambda f: f["properties"]["FromYear"])
        cur = None
        for f in L:
            p = f["properties"]; h = gh(f["geometry"])
            a, b = max(Y0, p["FromYear"]), min(Y1, p["ToYear"]) + 1
            if cur and cur["h"] == h and cur["b"] >= a and cur["comp"] == p.get("Components", "") and cur["mem"] == p.get("MemberOf", ""):
                cur["b"] = max(cur["b"], b); continue
            cur = {"n": n, "a": a, "b": b, "h": h, "g": f["geometry"], "wd": p.get("Wikidata") or "", "wp": p.get("Wikipedia") or "", "comp": p.get("Components", "") or "", "mem": p.get("MemberOf", "") or "", "ty": p["Type"], "ar": p.get("Area") or 0}
            out.append(cur)
    return out
base = merge([f for f in rows if not f["properties"]["Name"].startswith("(")])
agg = merge([f for f in rows if f["properties"]["Name"].startswith("(")])
print("base rows", len(base), "union/relation rows", len(agg), file=sys.stderr)
def fc(L, keep):
    return {"type": "FeatureCollection", "features": [{"type": "Feature", "properties": {k: r[k] for k in keep}, "geometry": r["g"]} for r in L]}
json.dump(fc(base, ["n", "a", "b", "wd", "wp", "mem", "ar"]), open("/tmp/g3/base.geojson", "w"))
json.dump(fc(agg, ["n", "a", "b", "comp", "mem", "ty", "ar"]), open("/tmp/g3/agg.geojson", "w"))
