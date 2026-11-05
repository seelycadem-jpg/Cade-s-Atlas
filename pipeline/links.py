# Stage 5: encyclopedia links. Sets e["wk"] (Wikipedia title) and e["bt"] (Britannica path) on every event.
import json, sys
sys.path.insert(0, "/home/claude")
from bt import BT

P = "/home/claude/site/data.json"
D = json.load(open(P)); EV = D["events"]

# Wikipedia titles that turned out to be wrong or too broad when checked
WKFIX = {
    "af15298": "Ethiopian–Adal War",
    "af-1886": "German East Africa",
    "af187322": "Slavery in Zanzibar",
    "af-zanzslavery": "Slavery in Zanzibar",
    "oc-lastconvicts": "Convicts in Australia",
    "se-burma1948": "Burma Independence Act 1947",
    "af195741": "Ghana Independence Act 1957",
    "af196344b": "Kenya Colony",
}
unknown = [k for k in list(WKFIX) + list(BT) if k not in {e["id"] for e in EV}]
if unknown: raise SystemExit("unknown ids: %s" % unknown)

nowk, nobt = [], []
for e in EV:
    if e["id"] in WKFIX: e["wk"] = WKFIX[e["id"]]
    if not e.get("wk"): nowk.append(e["h"])
    b = BT.get(e["id"])
    if b: e["bt"] = b
    else: e.pop("bt", None); nobt.append(e["h"])

# Readable label for each Britannica article, built from its URL path (Britannica slugs drop accents and punctuation)
import re, unicodedata
def _strip(s): return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
def _norm(s): return re.sub(r"[^a-z0-9]", "", _strip(s).lower())
_words = {}
for e in EV:
    for f in ("h", "who", "what", "where", "wk", "story", "why"):
        for w in re.findall(r"[^\W\d_]+", e.get(f) or ""): _words.setdefault(_strip(w), set()).add(w)
# restore an accent only when the plain spelling never appears on its own (so "Revolution" is never touched)
ACC = {k: next(iter(v)) for k, v in _words.items() if k not in v and len(v) == 1}
BTT = {
    "biography/Joaquim-Aurelio-Barreto-Nabuco-de-Araujo": "Joaquim Nabuco", "biography/Min-queen-of-Korea": "Queen Min",
    "biography/Victoria-queen-of-United-Kingdom": "Queen Victoria", "topic/han-Japanese-government-unit": "Han (feudal domain)",
    "biography/Sejong-Korean-ruler": "Sejong", "biography/Philippe-Petain": "Philippe Pétain", "biography/Suleyman-the-Magnificent": "Süleyman the Magnificent",
    "event/2022-Russian-invasion-of-Ukraine": "Russia-Ukraine War", "event/January-6-U-S-Capitol-attack": "January 6 U.S. Capitol attack",
    "event/Hay-Bunau-Varilla-Treaty": "Hay–Bunau-Varilla Treaty", "place/Manchuria/Manchuria-since-c-1900": "Manchuria since c. 1900",
    "place/Korea/Korea-under-Japanese-rule": "Korea under Japanese rule", "event/Civil-Rights-Act-United-States-1964": "Civil Rights Act of 1964",
    "event/American-Revolution/Final-campaigns-in-the-South-and-the-surrender-of-Cornwallis": "American Revolution: the surrender of Cornwallis",
    "event/American-Revolution/The-end-of-the-war-and-the-terms-of-the-Peace-of-Paris-1783": "American Revolution: the Peace of Paris",
    "place/Kashmir-region-Indian-subcontinent": "Kashmir", "event/Massacre-of-Amritsar": "Jallianwala Bagh Massacre",
    "event/Srebrenica-massacre": "Srebrenica genocide", "topic/intifadah": "Intifada", "topic/BP-PLC": "BP (Anglo-Persian Oil Company)",
    "event/Treaty-of-Paris-1898": "Treaty of Paris (1898)", "event/Treaty-of-Paris-1783": "Treaty of Paris (1783)",
    "place/Empire-of-Japan/The-Russo-Japanese-War": "Empire of Japan: the Russo-Japanese War", "biography/Muhammad-Ali-pasha-and-viceroy-of-Egypt": "Muhammad Ali of Egypt",
    "biography/Abbas-I": "Abbas I", "event/Rwanda-genocide-of-1994": "Rwanda genocide of 1994",
}
FIXW = {"Nurnberg": "Nürnberg", "Petain": "Pétain", "Eighty Years War": "Eighty Years' War", "Bartholomews": "Bartholomew's",
        "Anglo Burmese": "Anglo-Burmese", "Franco German": "Franco-German", "German Soviet": "German-Soviet", "Russo Finnish": "Russo-Finnish",
        "Russo Japanese": "Russo-Japanese", "Israel Hamas": "Israel-Hamas", "Lettow Vorbeck": "Lettow-Vorbeck", "Jean Jacques": "Jean-Jacques",
        "Brown v Board": "Brown v. Board", "Dot com": "Dot-com", "German Herero": "German-Herero", "Diet of Worms Germany": "Diet of Worms"}
def bt_label(p, e):
    if p in BTT: return BTT[p]
    segs = []
    for x in p.split("/")[1:]:
        x = x.replace("-", " ")
        x = re.sub(r" (United States|European|German|Egyptian|Irish|English|British|Chinese) history.*$", "", x, flags=re.I)
        x = re.sub(r" (king|queen|emperor|archduke|pasha|shah) (of|and) .*$", "", x, flags=re.I)
        m = re.search(r" of (\d{4})(?: (\d{2,4}))?$", x)
        if m: x = x[:m.start()] + " of " + m.group(1) + ("–" + m.group(2)[-2:] if m.group(2) else "")
        else: x = re.sub(r"( \d{4})( \d{2,4})?$", "", x)
        x = re.sub(r" (Indian subcontinent|Marshall Islands|island nation Pacific Ocean|English Quaker leader and colonist|European and American social movement|United States Constitution|Great Britain|Europe|Thailand|Bolivia|Safavid|painting|English ship|ship|Spanish naval fleet|state)$", "", x)
        segs.append(x)
    t = ": ".join(segs); t = t[0].upper() + t[1:]
    for cand in (e.get("wk", ""), re.sub(r"\s*\(.*\)$", "", e.get("wk", "")), e["h"]):
        if cand and _norm(cand) == _norm(t): return cand
    t = " ".join(ACC.get(w, w) for w in t.split(" "))
    t = re.sub(r"\b([A-HJ-UWYZ]) (?=[A-Z])", r"\1. ", t); t = re.sub(r" Jr$", " Jr.", t)
    for a, b in FIXW.items(): t = t.replace(a, b)
    return t
for e in EV:
    if e.get("bt"): e["btt"] = bt_label(e["bt"], e)
    else: e.pop("btt", None)

if nowk: raise SystemExit("no Wikipedia title: %s" % nowk)
print("links: %d events, %d with a Britannica article, %d fall back to Britannica search: %s" % (len(EV), len(EV) - len(nobt), len(nobt), nobt))
json.dump(D, open(P, "w"), ensure_ascii=False, separators=(",", ":"))
