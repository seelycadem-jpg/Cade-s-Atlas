"""Stage: topic Q&A for every event, plus fuller story/why/who where the old text was thin."""
import json, importlib
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__))); from paths import SITE
P = _os.path.join(SITE, "data.json")
d = json.load(open(P))
E = {e["id"]: e for e in d["events"]}
n = {"q": 0, "story": 0, "why": 0, "who": 0, "hook": 0, "then": 0, "t": 0}
seen = set()
for k in range(1, 11):
    M = importlib.import_module(f"deepen{k}")
    for i, v in M.DEEP.items():
        if i not in E: raise SystemExit(f"deepen{k}: unknown id {i}")
        if i in seen: raise SystemExit(f"deepen{k}: duplicate id {i}")
        seen.add(i)
        e = E[i]
        for f, val in v.items():
            if f == "q":
                if not e.get("q"): e["q"] = val; n["q"] += 1
                continue
            if f not in n: raise SystemExit(f"deepen{k}: {i} unknown field {f}")
            e[f] = val; n[f] += 1
            if f == "hook": e["what"] = val
            if f == "then": e["sig"] = val
missing = [e["id"] for e in d["events"] if not e.get("q")]
if missing: raise SystemExit(f"events still without Q&A: {len(missing)} {missing[:10]}")
json.dump(d, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
print("deepen:", len(seen), "entries;", ", ".join(f"{k} {v}" for k, v in n.items()), f"; all {len(d['events'])} events have Q&A")
