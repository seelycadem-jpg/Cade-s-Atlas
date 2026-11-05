"""Stage: analytical rewrite. Bottom line up front, causes, trigger, consequences, legacy, takeaway."""
import json, importlib, glob, re, os, sys
sys.path.insert(0, "/home/claude")
P = "/home/claude/site/data.json"
d = json.load(open(P))
E = {e["id"]: e for e in d["events"]}
OK = {"bluf", "why", "trig", "then", "now", "lens", "story", "who", "hook", "fact", "myth"}
n = {k: 0 for k in OK}; seen = set(); setf = set()
mods = sorted(glob.glob("/home/claude/an[0-9][0-9].py"))
for path in mods:
    M = importlib.import_module(os.path.basename(path)[:-3])
    for i, v in M.A.items():
        if i not in E: raise SystemExit(f"{path}: unknown id {i}")
        seen.add(i); e = E[i]
        for f, val in v.items():
            if f not in OK: raise SystemExit(f"{path}: {i} unknown field {f}")
            if (i, f) in setf and not getattr(M, "OVERRIDE", False): raise SystemExit(f"{path}: {i}.{f} set twice")
            setf.add((i, f))
            if val is None: continue
            val = re.sub(r"\s+", " ", val).strip()
            e[f] = val; n[f] += 1
            if f == "then": e["sig"] = val
            if f == "hook": e["what"] = val
json.dump(d, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
miss = [e["id"] for e in d["events"] if not e.get("bluf")]
print(f"analysis: {len(mods)} files, {len(seen)} events; " + ", ".join(f"{k} {n[k]}" for k in sorted(n)) + f"; without bottom line: {len(miss)}")
