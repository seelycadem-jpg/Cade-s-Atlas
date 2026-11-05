import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import ROOT, SITE
# Stage: "By the numbers" for events, read from fig[0-9][0-9].py (F = {id: dict(rec=, kv=[(value,label)], toll=(title, unit, [(side, low, high_or_None, text_or_None)], note), n=note)}).
import json, glob, importlib, os, sys
sys.path.insert(0, ROOT)
D = json.load(open(SITE + "/data.json")); EV = D["events"]; E = {e["id"]: e for e in EV}
for e in EV: e.pop("figs", None)
errs = []; n = 0; nt = 0
for path in sorted(glob.glob(ROOT + "/fig[0-9][0-9].py")):
    M = importlib.import_module(os.path.basename(path)[:-3])
    for i, v in M.F.items():
        if i not in E: errs.append(f"{path}: unknown id {i}"); continue
        if "figs" in E[i]: errs.append(f"{path}: {i} set twice"); continue
        bad = set(v) - {"rec", "kv", "toll", "n"}
        if bad: errs.append(f"{path}: {i} bad keys {bad}"); continue
        o = {}
        if v.get("rec"): o["rec"] = v["rec"]
        if v.get("kv"):
            if len(v["kv"]) > 4: errs.append(f"{i}: more than 4 tiles")
            o["kv"] = [[str(a), str(b)] for a, b in v["kv"]]
        if v.get("toll"):
            t, u, sides, note = v["toll"]
            S = []
            for s in sides:
                nm, lo, hi = s[0], s[1], s[2] if len(s) > 2 else None
                txt = s[3] if len(s) > 3 else None
                if hi is not None and hi < lo: errs.append(f"{i}: range reversed for {nm}")
                S.append([nm, lo, hi, txt] if txt else [nm, lo, hi])
            o["toll"] = {"t": t, "s": S}
            if u: o["toll"]["u"] = u
            if note: o["toll"]["n"] = note
            nt += 1
        if v.get("n"): o["n"] = v["n"]
        E[i]["figs"] = o; n += 1
if errs: raise SystemExit("\n".join(errs))
json.dump(D, open(SITE + "/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
war = [e for e in EV if "war" in e["c"]]
print(f"figs: {n} events, {nt} with casualty bars; war events without figs: {sum(1 for e in war if 'figs' not in e)} of {len(war)}")
