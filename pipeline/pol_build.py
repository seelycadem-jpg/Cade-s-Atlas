"""Stage: polity profiles. Reads pol/*.py (L lists), validates, writes atlas/polities.json."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import ROOT, SITE
import importlib.util, json, re, sys, os
BANNED = ["existential", "in many ways", "complex interplay", "the stage was set", "it is no coincidence", "in other words", "it is important to note", "tapestry", "testament to", "delve", "in conclusion", "genuinely", "honestly", "straightforward"]
RULE0 = [re.compile(r"\bnot\b[^.;]{0,60},? but\b", re.I), re.compile(r"\b(did|does|was|were|is|are) not\b[^.]{0,80}\.\s+(It|They|He|She|This)\b"), re.compile(r"\bnot (only|just|merely|simply)\b", re.I), re.compile(r"\brather than\b.*\brather than\b", re.I)]
errs=[]; out=[]; seen=set()
for name in ["eu","me","asia","af","am","extra"]:
    spec=importlib.util.spec_from_file_location(name, f"{ROOT}/pol/{name}.py"); M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
    for p in M.L:
        w=f"{name}:{p['t']} {p['a']}"
        try: re.compile(p["rx"], re.I)
        except re.error as e: errs.append(f"{w}: bad regex {e}")
        if not (1400<=p["a"]<=p["b"]<=2025): errs.append(f"{w}: bad years")
        for k in ("key","gov","now","how","next"):
            if not p.get(k): errs.append(f"{w}: missing {k}")
        for k in ("now","how","next","gov","head","econ"):
            t=p.get(k) or ""; low=t.lower()
            for b in BANNED:
                if b in low: errs.append(f"{w}.{k}: banned '{b}'")
            for r in RULE0:
                if r.search(t): errs.append(f"{w}.{k}: rule zero: '{r.search(t).group(0)[:60]}'")
        key=(p["key"],p["a"])
        if key in seen: errs.append(f"{w}: duplicate key/year")
        seen.add(key)
        out.append(p)
# overlap check within a key
by={}
for p in out: by.setdefault(p["key"],[]).append(p)
for k,ps in by.items():
    ps.sort(key=lambda p:p["a"])
    for a,b in zip(ps,ps[1:]):
        if a["rx"]==b["rx"] and a["b"]>=b["a"]: errs.append(f"{k}: overlap {a['a']}-{a['b']} and {b['a']}-{b['b']}")
if errs:
    print("\n".join(errs)); sys.exit(1)

def classify(p):
    g=(p.get("gov","")).lower(); t=p["t"].lower()
    if p.get("cls"): return p["cls"]
    first=g.split(";")[0]
    def has(x,*ks): return any(k in x for k in ks)
    if has(first,"colony","protectorate","mandate","dependency","viceroyalty","under british","under french","under japan","occupation","condominium","possession","company","crown colony","personal union with spain","under the spanish crown","station"): return "colony"
    if has(first,"theocra","imamate","prince-bishop","papal","dalai","buddhist theocracy","theocratic"): return "theocracy"
    if has(first,"one-party","dictator","junta","military rule","military regime","military socialism","authoritarian","communist","totalitarian","personal rule","personalised","apartheid","white minority","fascist","nazi","security state","police state","führer","emirate of the ","taliban","revolutionary military","military-backed","military dictatorship","kleptocracy","terror","closed dictatorship","soviet","coups"): return "autocracy"
    if has(first,"democracy","parliamentary","republic","confederation of cantons","federal","responsible government","presidential","direct democracy"): 
        if has(first,"constitutional monarchy") and not has(first,"parliamentary democracy","parliamentary government","democracy"): return "monarchy"
        return "republic"
    if has(first,"monarchy","sultanate","empire","kingdom","khanate","shogunate","caliphate","emirate","tsardom","grand duchy","duchy","shahdom","principality","dynasty","electorate","horde","regency","beylik","sharifian","shahs","autocracy","khans","sultans","kings","chakri","hereditary"): return "monarchy"
    if has(first,"chiefdom","confederac","city-state","stateless","nations","peoples","tribal","age-set","clan","hundreds","no central"): return "stateless"
    return "other"

OVERRIDE={("Holy Roman Empire after Westphalia",1648):"monarchy",("Habsburg Netherlands",1530):"monarchy",("Dutch Republic",1600):"republic",("Austrian Netherlands",1715):"monarchy",("Kalmar Union",1400):"monarchy",("State of the Teutonic Order",1400):"theocracy",("Georgian kingdoms",1400):"monarchy",("Malta",1880):"colony",("Ottoman Egypt under the Mamluk beys",1715):"monarchy",("Timurid and Turkmen Persia",1400):"monarchy",("Ottoman Tunis",1574):"monarchy",("French Algeria",1830):"colony",("Ottoman Tripoli",1715):"monarchy",("Egyptian and Anglo-Egyptian Sudan",1821):"colony",("Federal Democratic Republic of Ethiopia",1991):"autocracy",("Kyrgyzstan",1992):"republic",("The Ming-Qing transition in the south",1644):"monarchy",("Xinjiang under warlords",1914):"autocracy",("Manchuria",1920):"colony",("Republic of Korea",1945):"republic",("The Mughal succession",1708):"monarchy",("Asante and the Akan states",1492):"monarchy",("French West Africa",1895):"colony",("French Equatorial Africa",1910):"colony",("Angola",1961):"autocracy",("Democratic Republic of the Congo",1960):"autocracy",("Portuguese Mozambique",1505):"colony",("Aztec Empire",1428):"monarchy",("Inca Empire",1438):"monarchy",("Aotearoa before the Treaty",1400):"stateless",("Colonial Brazil",1500):"colony",("The Mexican Revolution",1911):"other",("Uruguay",1830):"republic",("Guatemala",1945):"republic",("Honduras",1945):"republic",("The Caribbean and Guianas",1650):"colony",("British North American colonies",1607):"colony",("British North America",1763):"colony",("Nyamwezi chiefdoms",1880):"stateless",("Russian Turkestan and the protected khanates",1880):"colony",("Northern Yuan Mongols",1400):"monarchy",("Persia under the Afsharids, Zands and Qajars",1736):"monarchy",("Taiwan before Japan",1492):"colony",("Maratha Confederacy",1715):"monarchy",("Hausa city-states",1492):"monarchy",("Montenegro",1715):"monarchy",("Oman",1530):"monarchy",("Mongolia",1914):"autocracy",("Bhutan",1650):"monarchy",("Republic of Austria",1919):"republic",("Kuwait",1914):"monarchy",("Qatar",1880):"monarchy",("Mamluk Sultanate",1400):"monarchy",("Ghana",1957):"republic",("Kenya",1963):"republic",("Argentina's rise",1831):"republic",("Venezuela",1831):"republic",("Republic of China on Taiwan",1945):"republic",("Chile since the coup",1973):"republic",("Republic of Turkey",1923):"republic",("Republic of Benin",1960):"republic",("Tibet under China",1950):"autocracy",("Antarctica",1945):"stateless"}
for p in out: p["cls"]=OVERRIDE.get((p["t"],p["a"]),classify(p))

import collections; print(collections.Counter(p["cls"] for p in out))
for c in ["other","stateless","theocracy"]:
    print(c, [(p["t"],p["a"]) for p in out if p["cls"]==c][:40])

json.dump(dict(polities=out), open(SITE + "/polities.json","w"), ensure_ascii=False, separators=(",",":"))
words=sum(len((p.get("now","")+p.get("how","")+p.get("next","")).split()) for p in out)
print(f"polities: {len(out)} entries, {len(by)} keys, {words} words")
