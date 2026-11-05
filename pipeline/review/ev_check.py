"""Check written events against the schema and the house voice.
  python3 ev_check.py file.json [more.json ...]   -> prints problems per event and a summary"""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import ROOT, SITE
import json, re, sys
REQ = ["id", "y", "r", "tier", "h", "who", "where", "lat", "lon", "hook", "what", "why", "story", "then", "now", "fact", "bluf", "wk", "c", "t", "causes", "w", "map"]
REG = {"eu", "me", "sa", "ea", "se", "af", "na", "la", "oc"}
BANNED = ["existential", "shaped", "in many ways", "complex interplay", "the stage was set", "it is no coincidence", "in other words",
          "it is important to note", "tapestry", "pivotal", "testament to", "underscore", "delve", "a turning point in history", "paved the way", "ushered in"]
NEG = [re.compile(p, re.I) for p in [r"\bnot (?:just |merely |simply |only )?[^.;]{1,60}, but\b", r"\bdid not [^.]{1,80}\. (?:it|they|he|she) ", r"\bwas not [^.]{1,80}\. (?:it|they) was\b",
                                      r"\bthe (?:question|point|issue) (?:is|was) not\b", r"\bless [^.]{1,40} than\b"]]
SCHOOLS = re.compile(r"\b(historians?|scholars?|archaeologists? (?:argue|believe|think|suggest)|according to)\b", re.I)
def words(s): return len(re.findall(r"\w+", s or ""))
def check(e, ids):
    p = []
    for k in REQ:
        if k not in e or (e[k] in (None, "", []) and k not in ("causes", "t")): p.append(f"missing {k}")
    if e.get("r") not in REG: p.append("bad region")
    if not isinstance(e.get("y"), int): p.append("year not int")
    if e.get("tier") in (2, 3) and not e.get("parent"): p.append("no parent")
    if e.get("parent") and e["parent"] not in ids: p.append(f"parent {e['parent']} unknown")
    for c in e.get("causes") or []:
        if not isinstance(c, dict) or c.get("f") not in ids: p.append(f"cause {c} unknown")
    txt = " ".join(str(e.get(k, "")) for k in ("hook", "what", "why", "story", "then", "now", "fact", "bluf"))
    for b in BANNED:
        if b in txt.lower(): p.append(f"banned '{b}'")
    for r in NEG:
        m = r.search(txt)
        if m: p.append(f"negation pattern: '{m.group(0)[:60]}'")
    if SCHOOLS.search(txt): p.append(f"names authorities: '{SCHOOLS.search(txt).group(0)}'")
    if words(e.get("hook")) > 30: p.append("hook too long")
    if not (25 <= words(e.get("bluf")) <= 110): p.append(f"bluf {words(e.get('bluf'))} words")
    if words(e.get("story")) < 35: p.append("story thin")
    if e.get("then") != e.get("sig"): p.append("sig != then")
    if not (-90 <= (e.get("lat") or 0) <= 90 and -180 <= (e.get("lon") or 0) <= 180): p.append("bad coords")
    return p
if __name__ == "__main__":
    allev = []
    for f in sys.argv[1:]: allev += json.load(open(f))
    known = {e["id"] for e in allev} | {e["id"] for e in json.load(open(SITE + "/data.json"))["events"]}
    try: known |= {e["id"] for e in json.load(open(ROOT + "/review/events_anc/select.json"))}
    except Exception: pass
    bad = 0
    for e in allev:
        p = check(e, known)
        if p: bad += 1; print(e.get("id"), "|", "; ".join(p))
    print(f"{len(allev)} events, {bad} with problems")
