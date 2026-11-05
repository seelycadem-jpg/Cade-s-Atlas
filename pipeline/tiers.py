# Stage 4: the 1 -> 2 -> 3 hierarchy, read from tiers_tree.txt (indentation = tier).
# Build order: make_json.py -> arcs_build.py -> refine.py -> tiers.py
import json, sys
D = json.load(open("/home/claude/site/data.json")); EV = D["events"]
H = {}
for e in EV: H.setdefault(e["h"], []).append(e)
dup = [h for h, v in H.items() if len(v) > 1]
if dup: raise SystemExit("duplicate heads: %s" % dup)
H = {h: v[0] for h, v in H.items()}
for e in EV: e.pop("parent", None)
placed, stack, errs = set(), {}, []
for ln, raw in enumerate(open("/home/claude/tiers_tree.txt"), 1):
    if not raw.strip() or raw.lstrip().startswith("#"): continue
    ind = len(raw) - len(raw.lstrip(" ")); h = raw.strip()
    if ind % 2: errs.append("odd indent line %d" % ln); continue
    lvl = ind // 2
    if h == "~": stack = {0: None}; continue
    if h not in H: errs.append("line %d unknown head: %s" % (ln, h)); continue
    if h in placed: errs.append("line %d placed twice: %s" % (ln, h)); continue
    e = H[h]; placed.add(h); e["tier"] = lvl + 1; stack[lvl] = e
    for k in list(stack):
        if k > lvl: del stack[k]
    if lvl > 0:
        p = stack.get(lvl - 1)
        if p is not None: e["parent"] = p["id"]
# key events and details added in details1.py / details2.py, placed under an existing parent
sys.path.insert(0, "/home/claude")
import details1, details2, details3
todo = details1.PLACE + details2.PLACE + details3.PLACE
for _ in range(4):
    left = []
    for h, ph in todo:
        if h not in H: errs.append("PLACE unknown head: %s" % h); continue
        if ph not in H: errs.append("PLACE unknown parent: %s" % ph); continue
        if ph not in placed: left.append((h, ph)); continue
        if h in placed: errs.append("PLACE placed twice: %s" % h); continue
        e, p = H[h], H[ph]
        if p["tier"] >= 3: errs.append("PLACE parent is already a detail: %s > %s" % (ph, h)); continue
        e["tier"] = p["tier"] + 1; e["parent"] = p["id"]; placed.add(h)
    todo = left
if todo: errs.append("PLACE parents never placed: %s" % todo)
# Re-homing: key events that sat under the wrong turning point. None = a key event that stands on its own.
MOVES = {
    "Mona Lisa painted": None, "Michelangelo paints Sistine ceiling": None, "Adal invades Ethiopia": None,
    "Tumu Crisis": None, "Erie Canal opens": None, "War of 1812": None, "Irish Famine": None, "Paraguayan War": None,
    "Hundred Years' War ends": "Tudors take the English throne", "Wars of the Roses begin": "Tudors take the English throne",
    "Boer War": "Apartheid begins", "Summer Palace burned": "First Opium War",
    "Kingdom of Saudi Arabia proclaimed": "Sykes-Picot Agreement",
    "Battle of Kursk": "Germany invades USSR", "Operation Bagration": "Germany invades USSR", "Tehran Conference": "D-Day",
    "Bombing of Dresden": "Germany surrenders", "Potsdam Conference": "Germany surrenders",
    "Hong Kong returned to China": "Deng's market reforms", "Xi Jinping takes power": "Deng's market reforms",
}
for h, ph in MOVES.items():
    if h not in H or (ph and ph not in H): errs.append("MOVE unknown: %s > %s" % (h, ph)); continue
    e = H[h]
    if ph is None: e.pop("parent", None); e["tier"] = 2
    else: e["parent"] = H[ph]["id"]; e["tier"] = H[ph]["tier"] + 1
def retier(pid, t):
    for k in EV:
        if k.get("parent") == pid:
            k["tier"] = t + 1
            if k["tier"] > 3: errs.append("MOVE makes a tier-4 event: %s" % k["h"])
            retier(k["id"], k["tier"])
for e in EV:
    if not e.get("parent"): retier(e["id"], e["tier"])
missing = [e["h"] for e in EV if e["h"] not in placed]
if missing: errs.append("not placed: %s" % missing)
if errs: raise SystemExit("\n".join(errs))
for e in EV: e["w"] = {1: 3, 2: 2, 3: 1}[e["tier"]]
json.dump(D, open("/home/claude/site/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
from collections import Counter
kids = Counter(e.get("parent") for e in EV if e.get("parent"))
print("tiers", dict(Counter(e["tier"] for e in EV)), "| with parent", sum(1 for e in EV if "parent" in e),
      "| T1 with key events", sum(1 for e in EV if e["tier"] == 1 and kids[e["id"]]), "of", sum(1 for e in EV if e["tier"] == 1),
      "| standalone T2", sum(1 for e in EV if e["tier"] == 2 and "parent" not in e))
