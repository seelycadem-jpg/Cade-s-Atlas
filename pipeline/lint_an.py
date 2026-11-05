"""Standalone lint for one anNN.py rewrite file: python3 lint_an.py an36.py"""
import sys, re, importlib, os, json
sys.path.insert(0, "/home/claude")
from briefcheck import BANNED, RZ, AUTH, FIELDS
M = importlib.import_module(os.path.basename(sys.argv[1])[:-3])
EV = {e["id"]: e for e in json.load(open("/home/claude/site/data.json"))["events"]}
errs = []
for eid, d in M.A.items():
    if eid not in EV: errs.append(f"{eid}: unknown event id"); continue
    for k in ("bluf", "now", "story", "why", "then"):
        if not d.get(k): errs.append(f"{eid}: missing {k}")
    for k, s in d.items():
        if k not in FIELDS: errs.append(f"{eid}.{k}: unknown field"); continue
        if not s: continue
        low = s.lower()
        for b in BANNED:
            if b in low: errs.append(f"{eid}.{k}: banned '{b}'")
        for rx in RZ:
            m = rx.search(s)
            if m: errs.append(f"{eid}.{k}: rule zero …{m.group(0)[:60]}…")
        m = AUTH.search(s)
        if m: errs.append(f"{eid}.{k}: authority '{m.group(0)}'")
        if k == "bluf" and len(s.split()) > 95: errs.append(f"{eid}.bluf: {len(s.split())} words, cut to 95")
        if k == "bluf" and len(s.split()) < 35: errs.append(f"{eid}.bluf: {len(s.split())} words, too thin")
print(f"{sys.argv[1]}: {len(M.A)} events, {len(errs)} problems")
for x in errs: print("  ", x)
sys.exit(1 if errs else 0)
