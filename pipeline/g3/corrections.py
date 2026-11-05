"""Corrections to the reference record's labels, each found by the border review (control-point research,
/home/claude/review/cp) and checked against the dated sources cited there. Shapes are not redrawn: a correction
renames a polity, sets its overlord, or moves the misfiled part of a shape to the polity research places there.
Input /tmp/g3/rows.json, output /tmp/g3/rows_c.json and /tmp/g3/corrections_log.json."""
import json, os
from shapely.geometry import shape, mapping, MultiPolygon
ROWS = json.load(open(os.environ.get("IN", "/tmp/g3/rows.json")))
def W(g):  # west bound
    return shape(g).bounds[0]
def parts(g):
    s = shape(g); return list(s.geoms) if s.geom_type == "MultiPolygon" else [s]
def mp(ps): return mapping(ps[0] if len(ps) == 1 else MultiPolygon(ps))
# (test, change, why)
C = [
 (lambda p, g: p["NAME"] == "Golden Horde" and p["a"] >= 1547 and W(g) > 75 and p["a"] < 1636, {"NAME": "Northern Yuan"},
  "The Golden Horde broke up by 1502; the Mongolian plateau in 1547-1635 was the Northern Yuan (Ulaanbaatar, Hailar, Hohhot research)."),
 (lambda p, g: p["NAME"] == "Golden Horde" and p["a"] >= 1636 and W(g) > 75 and p["a"] < 1691, {"NAME": "Khalkha khanates"},
  "After Ligdan Khan's death (1634) the Khalkha khanates held northern Mongolia until they submitted to the Qing at Dolon Nor in 1691."),
 (lambda p, g: p["NAME"] == "Golden Horde" and p["a"] >= 1691 and W(g) > 75, {"NAME": "Khalkha khanates", "SUBJECTO": "Qing Dynasty"},
  "Khalkha submitted to the Qing at Dolon Nor in 1691."),
 (lambda p, g: p["NAME"] == "Mongol Khanate" and p["a"] < 1636, {"NAME": "Northern Yuan"},
  "The Mongol khanate of 1368-1635 is the Northern Yuan."),
 (lambda p, g: p["NAME"] == "Astrakhan Khanate" and p["a"] >= 1600 and p["a"] < 1721, {"NAME": "Kalmyk Khanate", "SUBJECTO": "Tsardom of Russia"},
  "Russia annexed the Astrakhan Khanate in 1556; the lower Volga-Don steppe in 1634-1771 was the Kalmyk Khanate under Russian suzerainty (Elista research)."),
 (lambda p, g: p["NAME"] == "Astrakhan Khanate" and p["a"] >= 1721, {"NAME": "Kalmyk Khanate", "SUBJECTO": "Russian Empire"},
  "Kalmyk Khanate under the Russian Empire until its abolition in 1771."),
 (lambda p, g: p["NAME"] == "Hashemite Arab Federation" and p["a"] < 1500, {"NAME": "Qara Qoyunlu"},
  "A 20th-century name on 15th-century Iraq; Qara Qoyunlu held Baghdad and Basra from 1410/11 (Basra research)."),
 (lambda p, g: p["NAME"] == "Eastern Moghulistan" and p["a"] >= 1514, {"NAME": "Yarkent Khanate"},
  "Sultan Said Khan founded the Yarkent Khanate in 1514; Kashgar research gives Yarkent from 1514."),
 (lambda p, g: p["NAME"] == "Tümed" and p["a"] >= 1637 and W(g) > 88, {"NAME": "Khoshut Khanate"},
  "Güshi Khan's Khoshut took Kokonor in 1637 (Kokonor research)."),
 (lambda p, g: p["NAME"] == "Sultanate of Malacca" and p["a"] >= 1512, {"NAME": "Johor Sultanate"},
  "Portugal took Malacca in 1511; the sultanate continued as Johor (Malacca and Johor research)."),
 (lambda p, g: p["NAME"] == "Republic of Florence" and 1532 <= p["a"] < 1569, {"NAME": "Duchy of Florence"},
  "The Republic ended in 1532; Duchy of Florence 1532-1569."),
 (lambda p, g: p["NAME"] == "Republic of Florence" and p["a"] >= 1569, {"NAME": "Grand Duchy of Tuscany"},
  "Grand Duchy of Tuscany from 1569 (Florence research)."),
 (lambda p, g: p["NAME"] == "Kingdom of Hawaï'i", {"NAME": "Kingdom of Hawaii"}, "Spelling."),
 (lambda p, g: p["NAME"] == "Serbs" and p["a"] < 1815, {"NAME": "Revolutionary Serbia"}, "First Serbian Uprising, 1804-1813."),
 (lambda p, g: p["NAME"] == "Serbs" and 1815 <= p["a"] < 1878, {"NAME": "Principality of Serbia", "SUBJECTO": "Ottoman Empire"},
  "Principality of Serbia under Ottoman suzerainty, 1815/1817-1878 (Belgrade research)."),
 (lambda p, g: p["NAME"] == "Serbs" and 1878 <= p["a"] < 1882, {"NAME": "Principality of Serbia"}, "Independent from the Congress of Berlin, 1878."),
 (lambda p, g: p["NAME"] == "Serbs" and p["a"] >= 1882, {"NAME": "Kingdom of Serbia"}, "Kingdom from 1882."),
 (lambda p, g: p["NAME"] == "Zululand" and p["a"] < 1879, {"NAME": "Zulu Kingdom"}, "Zulu Kingdom until the British conquest of 1879."),
 (lambda p, g: p["NAME"] == "Helvetic Republic" and p["a"] >= 1803, {"NAME": "Swiss Confederation", "SUBJECTO": "French Empire"},
  "The Act of Mediation (1803) ended the Helvetic Republic; the Confederation stood under French protection until 1813."),
 (lambda p, g: p["NAME"] == "Kingdom of Naples (Napoleonic)" and p["b"] <= 1806, {"NAME": "Kingdom of Naples"},
  "The Bourbon Kingdom of Naples; the Napoleonic kingdom began in 1806."),
 (lambda p, g: p["NAME"] == "Sultanate of Harar" and p["a"] < 1577, {"NAME": "Adal Sultanate"},
  "Harar was Adal's capital until 1577 (Harar research)."),
 (lambda p, g: p["NAME"] == "Sloboda Ukraine" and p["a"] < 1721, {"SUBJECTO": "Tsardom of Russia"}, "Cossack regiments under Muscovite rule."),
 (lambda p, g: p["NAME"] == "Sloboda Ukraine" and p["a"] >= 1721, {"SUBJECTO": "Russian Empire"}, "Under the Russian Empire."),
 (lambda p, g: p["NAME"] == "Greenland" and 1721 <= p["a"] < 1814, {"SUBJECTO": "Denmark-Norway"}, "Danish-Norwegian colony from 1721 (Nuuk research)."),
 (lambda p, g: p["NAME"] == "Greenland" and p["a"] >= 1814, {"SUBJECTO": "Kingdom of Denmark"}, "Danish colony after 1814."),
 (lambda p, g: p["NAME"] == "Maynila" and p["a"] >= 1572 and shape(g).bounds[1] > 20, {"NAME": "Ryukyu Kingdom", "SUBJECTO": "Ming Dynasty"},
  "These islands are the Ryukyus (Shuri research), filed under Manila."),
]
out = []; log = []; split = 0
for r in ROWS:
    p = r["properties"]; g = r["geometry"]
    # parts of 'Maynila' north of 20N are the Ryukyus: move them to a Ryukyu row
    if p["NAME"] == "Maynila" and p["a"] < 1572:
        ps = parts(g); north = [q for q in ps if q.representative_point().y > 20]; south = [q for q in ps if q.representative_point().y <= 20]
        if north and south:
            r = dict(r, geometry=mp(south)); out.append(r)
            q = dict(p, NAME="Ryukyu Kingdom", SUBJECTO="Ming Dynasty"); q.pop("wd", None); q.pop("AKA", None)
            out.append({"type": "Feature", "properties": q, "geometry": mp(north)}); split += 1
            log.append({"row": p["NAME"], "a": p["a"], "b": p["b"], "change": "islands north of 20N moved to Ryukyu Kingdom", "why": "Ryukyu filed under Manila (Shuri research)."})
            continue
    for test, ch, why in C:
        if test(p, g):
            old = {k: p.get(k) for k in ch}; p.update(ch)
            if "NAME" in ch: p.pop("AKA", None)
            log.append({"row": old.get("NAME") or p["NAME"], "a": p["a"], "b": p["b"], "change": ch, "why": why}); break
    out.append(r)
json.dump(out, open(os.environ.get("OUT", "/tmp/g3/rows_c.json"), "w"))
json.dump(log, open("/tmp/g3/corrections_log.json", "w"), indent=0, ensure_ascii=False)
print("rows corrected", len(log), "split", split)
