"""Year-by-year audit of province owners (maps/own.json).
  python3 audit.py checks            -> work/g4/audit_checks.json + printed summary (flicker, big jumps, anachronisms)
  python3 audit.py dump REGION OUT   -> decade snapshots for one review region, in modern place names, for reviewers
Places are named by modern country and first-level region (the province map's own names), so a reviewer can say
'Ukraine: Crimea, 1475-1783 -> Crimean Khanate under the Ottoman Empire' and the fix lands on exactly those provinces."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, ROOT, WORK
import json, sys, re, collections, glob, math
sys.path.insert(0, ROOT + "/review"); from names import same, key
O = json.load(open(MAPS + "/own.json")); POL = O["pol"]
F = json.load(open(WORK + "/g4/prov.geojson"))["features"]
P = [f["properties"] for f in F]; n = len(P)
def base(nm): return re.sub(r"( islands)?( \d+)?$", "", nm).strip()
SUB = {f["properties"]["ADMIN"]: f["properties"]["SUBREGION"] for f in json.load(open(WORK + "/nev/geojson/ne_10m_admin_0_countries.geojson"))["features"]}
SUB.update({"S. Sudan": "Northern Africa", "Czech Republic": "Eastern Europe", "Cape Verde": "Western Africa", "Macedonia": "Southern Europe", "Spratly Is.": "South-Eastern Asia",
            "Guinea Bissau": "Western Africa", "Sao Tome and Principe": "Middle Africa", "Gaza Strip": "Western Asia", "West Bank": "Western Asia", "Swaziland": "Southern Africa"})
REGIONS = {
 "europe_w": ["Western Europe", "Southern Europe", "Northern Europe"],
 "europe_wc": ["Western Europe"], "europe_s": ["Southern Europe"], "europe_n": ["Northern Europe"],
 "europe_e": ["Eastern Europe"],
 "mideast": ["Western Asia"],
 "n_africa": ["Northern Africa"],
 "w_africa": ["Western Africa"],
 "c_africa": ["Middle Africa"],
 "es_africa": ["Eastern Africa", "Southern Africa"],
 "s_asia": ["Southern Asia", "Central Asia"],
 "e_asia": ["Eastern Asia"],
 "se_asia": ["South-Eastern Asia", "Melanesia", "Micronesia", "Polynesia", "Australia and New Zealand"],
 "sea": ["South-Eastern Asia"], "oceania": ["Melanesia", "Micronesia", "Polynesia", "Australia and New Zealand"],
 "n_america": ["Northern America"],
 "latam": ["Central America", "Caribbean", "South America"],
}
TL = {int(k): v for k, v in O["prov"].items()}
pid = [p["id"] for p in P]
def owners(y):
    out = []
    for i in range(n):
        tl = TL[pid[i]]; v = 0
        for yy, o in tl:
            if yy <= y: v = o
            else: break
        out.append(v)
    return out
def label(o, y):
    if not o: return "(no polity)"
    src, nm, ov, un, ex = POL[o]
    if src == "pp": return f"(peoples: {nm})"
    s = nm
    if ov: s += f" [under {ov}]"
    if ex == "gaz": s += " ~est"
    if ex == "hb": s += " ~map"
    return s
def dump(region, out):
    subs = set(REGIONS[region]); idx = [i for i in range(n) if SUB.get(P[i]["c"]) in subs]
    tot = collections.Counter(P[i]["c"] for i in idx)
    lines = []
    for y in list(range(1400, 2021, 10)) + [2025]:
        ow = owners(min(y, 2019))
        by = collections.defaultdict(lambda: collections.defaultdict(set)); cnt = collections.defaultdict(collections.Counter)
        for i in idx: by[label(ow[i], y)][P[i]["c"]].add(base(P[i]["n"])); cnt[label(ow[i], y)][P[i]["c"]] += 1
        lines.append(f"== {y} ==")
        for lab in sorted(by, key=lambda L: -sum(cnt[L].values())):
            parts = []
            for c, regs in sorted(by[lab].items(), key=lambda kv: -cnt[lab][kv[0]]):
                share = cnt[lab][c] / tot[c]
                if share > .9: parts.append(f"{c} (all{'' if share == 1 else ' but a little'})")
                else: parts.append(f"{c}: " + ", ".join(sorted(regs)[:25]) + (" …" if len(regs) > 25 else ""))
            lines.append(f"{lab}: " + "; ".join(parts))
    open(out, "w").write("\n".join(lines))
    # the vocabulary of place names, for corrections
    voc = collections.defaultdict(set)
    for i in idx: voc[P[i]["c"]].add(base(P[i]["n"]))
    json.dump({c: sorted(v) for c, v in voc.items()}, open(out.replace(".txt", "_places.json"), "w"), ensure_ascii=False, indent=0)
def checks():
    years = list(range(1400, 2020))
    W = {y: owners(y) for y in years}
    res = {"flicker": collections.Counter(), "jumps": [], "life": {}}
    # flicker: A -> B -> A with B lasting 3 years or less
    for i in range(n):
        seq = [W[y][i] for y in years]
        k = 0
        while k < len(seq) - 1:
            if seq[k + 1] != seq[k]:
                a, j = seq[k], k + 1
                b = seq[j]
                while j < len(seq) and seq[j] == b: j += 1
                if j < len(seq) and seq[j] == a and (j - (k + 1)) <= 3 and a and b:
                    res["flicker"][(POL[a][1], POL[b][1], years[k + 1])] += 1
                k = j - 1 if j - 1 > k else k + 1
            else: k += 1
    # big jumps: provinces changing owner from one year to the next
    for y0, y1 in zip(years, years[1:]):
        a, b = W[y0], W[y1]; ch = collections.Counter()
        for i in range(n):
            if a[i] != b[i]: ch[(label(a[i], y0), label(b[i], y1))] += 1
        tot = sum(ch.values())
        if tot > 120: res["jumps"].append({"year": y1, "provinces": tot, "top": [[f, t, c] for (f, t), c in ch.most_common(8)]})
    # lifetimes on the map against the research
    life = collections.defaultdict(lambda: [9999, 0])
    for y in years:
        for o in set(W[y]):
            if o and POL[o][0] != "pp":
                L = life[POL[o][1]]; L[0] = min(L[0], y); L[1] = max(L[1], y)
    known = collections.defaultdict(lambda: [9999, 0])
    for f in glob.glob(ROOT + "/review/cp/*.json"):
        for p in json.load(open(f))["places"]:
            for t in p["timeline"]:
                if t["ruler"] != "none": k = known[t["ruler"]]; k[0] = min(k[0], t["from"]); k[1] = max(k[1], t["to"])
    for f in glob.glob(ROOT + "/review/gaz/*.json"):
        try:
            for p in json.load(open(f)).get("polities", []): k = known[p["name"]]; k[0] = min(k[0], int(p["from"])); k[1] = max(k[1], int(p["to"]))
        except Exception: pass
    keys = list(known)
    anach = []
    for nm, (a, b) in life.items():
        ks = [k for k in keys if same(nm, k)]
        if not ks: continue
        ka, kb = min(known[k][0] for k in ks), max(known[k][1] for k in ks)
        if a < ka - 15 or b > kb + 15: anach.append([nm, a, b, ka, kb])
    res["anach"] = sorted(anach, key=lambda x: -((max(0, x[3] - x[1])) + max(0, x[2] - x[4])))
    res["flicker"] = [[a, b, y, c] for (a, b, y), c in res["flicker"].most_common(200)]
    json.dump(res, open(WORK + "/g4/audit_checks.json", "w"), indent=0, ensure_ascii=False)
    print("flicker cases", len(res["flicker"]), "big jump years", len(res["jumps"]), "anachronisms", len(res["anach"]))
def fy(y): return f"{-y} BCE" if y < 0 else (f"{y} CE" if y < 1000 else str(y))
ANC = list(range(-3400, -800, 100)) + list(range(-800, 1400, 50))
def dump2(region, out, steps=None):
    subs = set(REGIONS[region]); idx = [i for i in range(n) if SUB.get(P[i]["c"]) in subs]
    tot = collections.Counter(P[i]["c"] for i in idx)
    def regs(ii): return sorted({base(P[i]["n"]) for i in ii})
    lines = ["Each snapshot: who holds what (share of each modern country's provinces), then what changed since the previous snapshot, by modern region.", ""]
    prev = None
    for y in (steps or (list(range(1400, 2021, 10)) + [2025])):
        ow = owners(min(y, 2019))
        cnt = collections.defaultdict(collections.Counter)
        for i in idx: cnt[label(ow[i], y)][P[i]["c"]] += 1
        lines.append(f"== {fy(y)} ==")
        hold = []
        for lab in sorted(cnt, key=lambda L: -sum(cnt[L].values())):
            parts = [f"{c} {round(100 * k / tot[c])}%" for c, k in cnt[lab].most_common(6)]
            hold.append(f"{lab}: " + ", ".join(parts) + (" …" if len(cnt[lab]) > 6 else ""))
        lines.append("Holders: " + " | ".join(hold))
        if prev is not None:
            moves = collections.defaultdict(list)
            for i in idx:
                if prev[i] != ow[i]: moves[(label(prev[i], y), label(ow[i], y), P[i]["c"])].append(i)
            if moves:
                lines.append("Changes:")
                for (a, b, c), ii in sorted(moves.items(), key=lambda kv: -len(kv[1]))[:60]:
                    r = regs(ii); lines.append(f"  {a} -> {b}: {c}: " + ", ".join(r[:12]) + (f" (+{len(r) - 12} more)" if len(r) > 12 else ""))
        prev = ow
    open(out, "w").write("\n".join(lines))
    voc = collections.defaultdict(set)
    for i in idx: voc[P[i]["c"]].add(base(P[i]["n"]))
    json.dump({c: sorted(v) for c, v in voc.items()}, open(out.replace(".txt", "_places.json"), "w"), ensure_ascii=False, indent=0)
if __name__ == "__main__":
    if sys.argv[1] == "checks": checks()
    elif sys.argv[1] == "dump2": dump2(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "dumpanc": dump2(sys.argv[2], sys.argv[3], ANC)
    else: dump(sys.argv[2], sys.argv[3])
