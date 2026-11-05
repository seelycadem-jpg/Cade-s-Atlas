"""Stage: house-style checks on event briefs. Errors for events rewritten in an34+ files; a warning count for the rest."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import ROOT, SITE
import json, re, glob, importlib, os, sys
sys.path.insert(0, ROOT)
D = json.load(open(SITE + "/data.json")); EV = D["events"]
FIELDS = ["bluf", "now", "story", "why", "trig", "then", "myth", "fact"]
BANNED = ["existential", "in many ways", "complex interplay", "the stage was set", "it is no coincidence", "in other words", "it is important to note", "tapestry", "testament to", "delve", "in conclusion", "inevitabl", "destined", "had to happen", "sent shockwaves", "changed everything", "paved the way", "watershed moment"]
RZ = [re.compile(r"\b(did not|didn't|was not|wasn't|is not|isn't|were not|weren't|never)\b[^.;:]{3,90}[.;]\s+(It|They|He|She|This|That|What|The|Its)\b"),
      re.compile(r"\bnot (?:just|only|merely|simply)\b[^.]{0,80}\bbut\b", re.I),
      re.compile(r"\bis not (?:a|an|the)\b[^.]{0,60}\bbut (?:a|an|the)\b", re.I),
      re.compile(r"\bnot (?:a|an|the|because|about|for|from|in|to)\b[^.]{0,60}, but\b", re.I)]
AUTH = re.compile(r"\b(historians?|scholars?|academics?|economists?|sociologists?|political scientists?|a study|studies show|according to|the consensus|revisionist|orthodox school|literature)\b", re.I)
if __name__ == "__main__":
    DONE = set()
    for path in sorted(glob.glob(ROOT + "/an[0-9][0-9].py")):
        n = int(os.path.basename(path)[2:4])
        if n >= 34:
            M = importlib.import_module(os.path.basename(path)[:-3]); DONE |= set(M.A.keys())
    errs, warns = [], 0
    for e in EV:
        for k in FIELDS:
            s = e.get(k)
            if not s: continue
            probs = []
            low = s.lower()
            for b in BANNED:
                if b in low: probs.append(f"banned '{b}'")
            for rx in RZ:
                m = rx.search(s)
                if m: probs.append(f"rule zero: …{m.group(0)[:60]}…")
            m = AUTH.search(s)
            if m: probs.append(f"authority: '{m.group(0)}'")
            if k == "bluf" and len(s.split()) > 95: probs.append(f"bluf long: {len(s.split())} words")
            for p in probs:
                if e["id"] in DONE: errs.append(f"{e['id']}.{k}: {p}")
                else: warns += 1
    print(f"briefcheck: {len(DONE)} rewritten events checked, {len(errs)} errors; {warns} warnings in events awaiting rewrite")
    for x in errs: print("  ERR", x)
    if errs: sys.exit(1)
