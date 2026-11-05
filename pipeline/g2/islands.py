"""Who held the islands before 1886. The survey maps leave many islands blank or wrong; this list
gives each island its ruler period by period. Geometry is the coastline polygon under the point."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..')); from paths import MAPS, ROOT, SITE, WORK
import json, subprocess
from shapely.ops import unary_union
from shapely.geometry import shape, Point, mapping
from shapely.validation import make_valid
V, OT, GR = ("Republic of Venice", None), ("Ottoman Empire", None), ("Greece", None)
SP, FR, BR = ("Spain", None), ("France", None), ("Malta", "British Empire")
AR = ("Aragón", None)
CYC = [(1400, 1566, "Duchy of the Archipelago", "Republic of Venice"), (1566, 1830, *OT), (1830, 1886, *GR)]
IONIAN = [(1797, 1800, "Ionian Islands", "French"), (1800, 1807, "Septinsular Republic", None), (1807, 1815, "Ionian Islands", "French"), (1815, 1864, "United States of the Ionian Islands", "British Empire"), (1864, 1886, *GR)]
I = [
 ("Crete", [(24.9, 35.2)], [(1400, 1669, *V), (1669, 1886, *OT)]),
 ("Cyprus", [(33.2, 35.0)], [(1400, 1489, "Kingdom of Cyprus", None), (1489, 1571, *V), (1571, 1878, *OT), (1878, 1886, "Cyprus", "British Empire")]),
 ("Rhodes", [(28.0, 36.2), (27.15, 36.85), (26.95, 36.95)], [(1400, 1522, "Knights Hospitaller", None), (1522, 1886, *OT)]),
 ("Euboea", [(23.8, 38.5)], [(1400, 1470, *V), (1470, 1830, *OT), (1830, 1886, *GR)]),
 ("the Cyclades", [(25.45, 37.05), (25.15, 37.05), (24.85, 37.85), (25.15, 37.55), (25.35, 37.45), (25.45, 36.4), (24.45, 36.7), (24.95, 37.45), (24.35, 37.65)], CYC),
 ("Chios", [(26.0, 38.4)], [(1400, 1566, "Chios", "Republic of Genoa"), (1566, 1886, *OT)]),
 ("Lesbos", [(26.3, 39.2)], [(1400, 1462, "Lesbos", "Republic of Genoa"), (1462, 1886, *OT)]),
 ("Lemnos", [(25.2, 39.9)], [(1400, 1479, "Lemnos", "Republic of Genoa"), (1479, 1886, *OT)]),
 ("Samos", [(26.8, 37.75)], [(1400, 1475, "Samos", "Republic of Genoa"), (1475, 1886, *OT)]),
 ("Corfu", [(19.9, 39.6)], [(1400, 1797, *V)] + IONIAN),
 ("Kefalonia", [(20.6, 38.2), (20.65, 38.7)], [(1400, 1479, "County Palatine of Cephalonia", None), (1479, 1500, *OT), (1500, 1797, *V)] + IONIAN),
 ("Zakynthos", [(20.8, 37.8)], [(1400, 1479, "County Palatine of Cephalonia", None), (1479, 1485, *OT), (1485, 1797, *V)] + IONIAN),
 ("Sicily", [(14.2, 37.5)], [(1400, 1516, *AR), (1516, 1713, *SP), (1713, 1720, "Kingdom of Sicily", "Savoy"), (1720, 1735, "Kingdom of Sicily", "Austria (Habsburg)"), (1735, 1816, "Kingdom of Sicily", None), (1816, 1861, "Kingdom of the Two Sicilies", None), (1861, 1886, "Italy", None)]),
 ("Sardinia", [(9.0, 40.1)], [(1400, 1479, *AR), (1479, 1708, *SP), (1708, 1720, "Sardinia", "Austria (Habsburg)"), (1720, 1861, "Kingdom of Sardinia", None), (1861, 1886, "Italy", None)]),
 ("Corsica", [(9.1, 42.1)], [(1400, 1768, "Corsica", "Republic of Genoa"), (1768, 1886, *FR)]),
 ("Malta", [(14.4, 35.9), (14.25, 36.05)], [(1400, 1530, *AR), (1530, 1798, "Knights Hospitaller", None), (1798, 1800, "Malta", "French"), (1800, 1886, *BR)]),
 ("Mallorca", [(2.9, 39.6), (1.4, 38.95)], [(1400, 1479, *AR), (1479, 1886, *SP)]),
 ("Menorca", [(4.1, 39.95)], [(1400, 1479, *AR), (1479, 1708, *SP), (1708, 1756, "Minorca", "British Empire"), (1756, 1763, "Minorca", "French"), (1763, 1782, "Minorca", "British Empire"), (1782, 1798, *SP), (1798, 1802, "Minorca", "British Empire"), (1802, 1886, *SP)]),
 ("Lanzarote and Fuerteventura", [(-13.6, 29.0), (-14.0, 28.4)], [(1400, 1402, "Guanches", None), (1402, 1886, "Canary Islands", "Spanish")]),
 ("Gran Canaria", [(-15.6, 27.95)], [(1400, 1483, "Guanches", None), (1483, 1886, "Canary Islands", "Spanish")]),
 ("Tenerife and La Palma", [(-16.6, 28.3), (-17.85, 28.65), (-17.2, 28.1), (-17.95, 27.75)], [(1400, 1493, "Guanches", None), (1493, 1886, "Canary Islands", "Spanish")]),
 ("Madeira", [(-16.95, 32.75)], [(1420, 1886, "Madeira", "Portuguese")]),
 ("the Azores", [(-25.5, 37.8), (-27.2, 38.7), (-28.4, 38.5), (-28.1, 38.45), (-28.7, 38.6), (-31.2, 39.45)], [(1432, 1886, "Azores", "Portuguese")]),
 ("Cape Verde", [(-23.6, 15.1), (-24.4, 14.95), (-25.0, 16.85), (-22.9, 16.1), (-24.25, 16.6), (-23.0, 16.75)], [(1462, 1886, "Cape Verde", "Portuguese")]),
 ("Zanzibar", [(39.3, -6.1), (39.75, -5.15)], [(1503, 1698, "Zanzibar", "Portuguese"), (1698, 1856, "Zanzibar", "Oman"), (1856, 1886, "Sultanate of Zanzibar", None)]),
 ("Mauritius", [(57.55, -20.25)], [(1638, 1710, "Mauritius", "Dutch"), (1715, 1810, "Isle de France", "French"), (1810, 1886, "Mauritius", "British Empire")]),
 ("Réunion", [(55.5, -21.1)], [(1642, 1886, "Bourbon", "French")]),
 ("Ceylon", [(80.7, 7.8)], [(1658, 1796, "Dutch Ceylon", "Dutch"), (1796, 1886, "Ceylon", "British Empire")]),
 ("Ireland", [(-8.0, 53.4)], [(1400, 1500, "Gaelic Irish lordships", None)]),
 ("Tasmania", [(146.6, -42.0)], [(1400, 1803, "Aboriginal Tasmanians", None), (1803, 1886, "Van Diemen's Land (Tasmania)", "British Empire")]),
 ("New Zealand", [(175.5, -38.5), (170.5, -44.0), (167.9, -46.9)], [(1400, 1840, "Maori", None), (1840, 1886, "New Zealand", "British Empire")]),
 ("Hawaii", [(-155.5, 19.6), (-156.3, 20.75), (-157.0, 21.45), (-157.95, 21.45), (-159.5, 22.05)], [(1400, 1795, "Hawaiian chiefdoms", None), (1795, 1886, "Kingdom of Hawaii", None)]),
 ("Iceland", [(-19.0, 64.9)], [(1400, 1814, "Iceland", "Denmark-Norway"), (1814, 1886, "Iceland", "Denmark")]),
 ("Taiwan", [(121.0, 23.7)], [(1400, 1624, "Formosan peoples", None), (1624, 1662, "Dutch Formosa", "Dutch"), (1662, 1683, "Kingdom of Tungning", None), (1683, 1886, "Qing Empire", None)]),
 ("Hainan", [(109.7, 19.2)], [(1400, 1644, "Ming Chinese Empire", None), (1644, 1886, "Qing Empire", None)]),
 ("Luzon", [(121.0, 16.0)], [(1400, 1571, "Luzon polities", None), (1571, 1886, "Philippines", "Spanish")]),
 ("Jamaica", [(-77.3, 18.1)], [(1400, 1509, "Taino chiefdoms", None), (1509, 1655, "Jamaica", "Spanish"), (1655, 1886, "Jamaica", "British Empire")]),
 ("Cuba", [(-79.0, 21.8)], [(1400, 1511, "Taino chiefdoms", None), (1511, 1886, "Cuba", "Spanish")]),
 ("Puerto Rico", [(-66.5, 18.2)], [(1400, 1508, "Taino chiefdoms", None), (1508, 1886, "Puerto Rico", "Spanish")]),
 ("Newfoundland", [(-56.0, 48.5)], [(1400, 1713, "Beothuk", None), (1713, 1886, "Newfoundland", "British Empire")]),
]
# areas the survey maps get wrong, given by a survey polygon (or the land) cut to a box
GREECE_N = [(19.3, 42.2), (23.4, 42.0), (23.9, 40.6), (24.2, 39.2), (23.3, 38.75), (22.2, 38.75), (21.7, 39.35), (20.55, 39.3), (19.9, 39.6), (19.2, 41.0)]
ARTA = [(20.0, 39.6), (20.55, 39.3), (21.7, 39.35), (21.6, 38.55), (20.6, 38.55), (20.0, 39.2)]
ATHENS = [(22.2, 38.75), (23.3, 38.75), (24.3, 38.5), (24.3, 37.6), (23.0, 37.85), (22.45, 38.15)]
MOREA = [(21.0, 38.4), (22.45, 38.15), (23.0, 37.85), (23.6, 37.4), (23.6, 36.2), (21.4, 36.6)]
AREAS = [
 ("Thessaly, Macedonia and Epirus", ("poly", GREECE_N), [(1400, 1500, "Ottoman Empire", None)]),
 ("southern Epirus", ("poly", ARTA), [(1400, 1449, "Despotate of Epirus", None), (1449, 1500, "Ottoman Empire", None)]),
 ("Attica and Boeotia", ("poly", ATHENS), [(1400, 1456, "Duchy of Athens", None), (1456, 1500, "Ottoman Empire", None)]),
 ("the Morea", ("poly", MOREA), [(1400, 1460, "Byzantine Empire", None), (1460, 1500, "Ottoman Empire", None)]),
 ("Karaman", ("poly", [(31.3, 38.7), (33.2, 39.3), (34.8, 39.2), (35.4, 38.0), (34.9, 36.7), (33.5, 36.1), (32.0, 36.4), (31.0, 37.3)]), [(1400, 1468, "Karamanids", None), (1468, 1500, "Ottoman Empire", None)]),
 ("Kastamonu and Sinop", ("poly", [(32.0, 41.8), (35.3, 42.2), (35.7, 41.2), (34.0, 40.9), (32.6, 40.9), (32.0, 41.2)]), [(1400, 1461, "Isfendiyarids (Candar)", None), (1461, 1500, "Ottoman Empire", None)]),
 ("Elbistan and Maras", ("poly", [(35.8, 38.7), (37.9, 38.9), (38.6, 37.7), (37.2, 37.0), (36.0, 37.4)]), [(1400, 1500, "Dulkadirids", "Mamluke Sultanate")]),
 ("Diyarbakir", ("poly", [(38.6, 39.4), (41.0, 39.6), (42.3, 38.8), (42.4, 37.3), (39.6, 36.8), (38.6, 37.7)]), [(1400, 1500, "Aq Qoyunlu", None)]),
 ("Trebizond", ("poly", [(37.6, 41.3), (41.7, 41.7), (41.7, 40.6), (39.2, 40.3), (37.6, 40.7)]), [(1400, 1461, "Empire of Trebizond", None), (1461, 1500, "Ottoman Empire", None)]),
 ("Karelia", ("hb", 1400, r"^Novgorod$", (25, 56, 44, 70)), [(1400, 1478, "Novgorod Republic", None), (1478, 1500, "Grand Duchy of Moscow", None)]),
 ("the middle Volga", ("hb", 1400, r"^White Horde$", (44, 54, 56, 60)), [(1400, 1438, "Golden Horde", None), (1438, 1500, "Kazan Khanate", None)]),
 ("the English Pale", ("poly", [(-6.95, 53.05), (-6.0, 52.95), (-5.9, 53.95), (-6.9, 53.85)]), [(1400, 1500, "English territory", None)]),
 ("Greenland", ("poly", [(-75, 76), (-70, 79), (-65, 80.6), (-60, 82), (-50, 84.5), (-5, 84.5), (-5, 59), (-48, 58), (-60, 70), (-75, 76)]), [(1400, 1721, "Inuit", None), (1721, 1814, "Greenland", "Denmark-Norway"), (1814, 1886, "Greenland", "Denmark")]),
 ("Flanders and Artois", ("poly", [(1.6, 50.9), (2.5, 51.1), (3.4, 51.45), (4.0, 51.2), (3.8, 50.6), (3.1, 50.3), (2.0, 50.2)]), [(1400, 1477, "Burgundian State", None), (1477, 1500, "Habsburg Netherlands", "Holy Roman Empire")]),
 ("Brabant, Holland and Hainaut", ("poly", [(3.4, 51.45), (4.2, 52.0), (4.7, 53.1), (5.5, 53.4), (6.9, 53.4), (7.1, 52.3), (6.2, 51.9), (6.1, 50.8), (5.0, 50.5), (4.2, 49.98), (3.8, 50.6), (4.0, 51.2)]), [(1430, 1477, "Burgundian State", None), (1477, 1500, "Habsburg Netherlands", "Holy Roman Empire")]),
 ("Burgundy", ("poly", [(3.0, 47.2), (3.9, 48.1), (5.0, 47.9), (5.9, 47.85), (6.9, 47.5), (6.7, 46.4), (5.5, 46.2), (4.6, 46.2), (3.7, 46.6)]), [(1400, 1477, "Burgundian State", None), (1477, 1500, "France", None)]),
 ("Normandy", ("poly", [(-1.95, 49.72), (-1.0, 49.7), (0.1, 49.5), (1.4, 50.07), (1.8, 49.7), (1.7, 49.0), (0.9, 48.6), (0.0, 48.4), (-1.1, 48.5), (-1.6, 48.6)]), [(1417, 1450, "English territory", None)]),
 ("Gascony", ("poly", [(-1.8, 46.2), (-0.3, 45.7), (0.6, 44.9), (0.5, 43.9), (-0.5, 43.3), (-1.8, 43.4)]), [(1453, 1500, "France", None)]),
 ("Muscovy", ("poly", [(35.2, 55.3), (35.6, 56.5), (37.4, 57.3), (38.0, 58.6), (40.0, 60.3), (44.0, 59.8), (46.0, 57.8), (45.6, 56.0), (43.5, 55.3), (41.5, 55.6), (39.8, 55.0), (38.0, 54.3), (36.5, 54.6)]), [(1400, 1500, "Grand Duchy of Moscow", None)]),
 ("Tver", ("poly", [(33.5, 56.3), (34.2, 57.9), (36.8, 57.6), (37.4, 57.3), (35.6, 56.5)]), [(1400, 1485, "Grand Duchy of Tver", None), (1485, 1500, "Grand Duchy of Moscow", None)]),
 ("Ryazan", ("poly", [(38.0, 54.3), (39.8, 55.0), (41.5, 55.6), (42.3, 54.5), (41.0, 53.2), (39.0, 53.0)]), [(1400, 1500, "Grand Duchy of Ryazan", None)]),
 ("the lands of Novgorod", ("poly", [(27.8, 58.6), (28.5, 60.5), (30.0, 61.2), (32.5, 64.5), (34.0, 66.5), (40.0, 67.0), (44.0, 68.3), (52.0, 68.5), (60.0, 67.5), (60.0, 62.0), (52.0, 61.5), (46.0, 60.5), (44.0, 59.8), (40.0, 60.3), (38.0, 58.6), (37.4, 57.3), (34.2, 57.9), (31.5, 57.3), (30.0, 57.8)]), [(1400, 1478, "Novgorod Republic", None), (1478, 1500, "Grand Duchy of Moscow", None)]),
 ("Pskov", ("poly", [(27.4, 56.9), (27.8, 58.6), (30.0, 57.8), (29.5, 56.8)]), [(1400, 1500, "Pskov Republic", None)]),
 ("Kazan", ("poly", [(46.0, 57.8), (48.5, 58.3), (52.5, 58.0), (54.0, 56.0), (52.5, 54.0), (49.5, 54.0), (47.0, 55.0), (45.6, 56.0)]), [(1400, 1438, "Golden Horde", None), (1438, 1500, "Kazan Khanate", None)]),
 ("Azerbaijan and Iraq", ("poly", [(43.3, 41.2), (46.5, 41.6), (48.8, 41.0), (49.4, 38.4), (50.2, 36.6), (48.6, 34.3), (47.6, 32.0), (47.8, 30.2), (45.5, 30.8), (43.0, 32.0), (41.2, 34.2), (41.0, 35.8), (42.4, 37.3), (42.3, 38.8), (43.6, 39.8)]), [(1410, 1468, "Qara Qoyunlu", None), (1468, 1500, "Aq Qoyunlu", None)]),
 ("the Kipchak steppe", ("hb", 1400, r"^White Horde$", (40, 38, 100, 56)), [(1428, 1500, "Uzbek Khanate", None)]),
 ("western Siberia", ("hb", 1400, r"^White Horde$", (55, 56, 100, 70)), [(1400, 1500, "Tyumen Khanate", None)]),
 ("Vyatka and Perm", ("hb", 1400, r"^Novgorod$", (44, 54, 70, 66)), [(1400, 1489, "Vyatka and Perm lands", None), (1489, 1500, "Grand Duchy of Moscow", None)]),
 ("Constantinople", ("poly", [(28.0, 41.0), (28.3, 41.35), (29.15, 41.3), (29.1, 40.95), (28.6, 40.95)]), [(1400, 1453, "Byzantine Empire", None), (1453, 1500, "Ottoman Empire", None)]),
 ("Crimea", ("box", (32.4, 44.3, 36.8, 46.3)), [(1400, 1441, "Golden Horde", None), (1441, 1475, "Crimean Khanate", None), (1475, 1500, "Crimean Khanate", "Ottoman Empire")]),
 ("Mongolia", ("hb", 1500, r"^Chagatai Khanate$", (95, 41.6, 128, 56)), [(1500, 1530, "Northern Yuan (Mongols)", None)]),
]
import re
def hb_geom(y, rx, box):
    gj = f"{WORK}/hb_{y}.geojson"
    subprocess.run(["mapshaper", "-i", f"{SITE}/maps/w{y}.json", "-o", "format=geojson", gj], check=True, capture_output=True)
    from shapely.geometry import box as bx
    from shapely.ops import unary_union as uu
    F = json.load(open(gj))["features"]
    gs = [make_valid(shape(f["geometry"])) for f in F if f.get("geometry") and re.search(rx, f["properties"].get("NAME") or "")]
    return make_valid(uu(gs).intersection(bx(*box)))
land_gj = json.load(open(WORK + "/land.geojson"))
geoms = [make_valid(shape(g)) for g in (land_gj["geometries"] if "geometries" in land_gj else [f["geometry"] for f in land_gj["features"]])]
polys = []
for g in geoms:
    polys += list(g.geoms) if hasattr(g, "geoms") else [g]
feats, changes = [], []
for name, pts, tl in I:
    if not pts or not tl: continue
    parts = []
    for lon, lat in pts:
        pt = Point(lon, lat); hit = None
        for p in polys:
            if p.contains(pt): hit = p; break
        if hit is None:
            best = min(polys, key=lambda p: p.distance(pt))
            if best.distance(pt) < 0.2: hit = best
        if hit is not None and hit.area < 30: parts.append(hit)
    if not parts: print("no land for", name); continue
    geom = unary_union(parts)
    for a, b, nm, sub in tl:
        feats.append({"type": "Feature", "properties": {"isl": name, "a": a, "b": b, "NAME": nm, "SUBJECTO": sub}, "geometry": mapping(geom)})
    for (a0, b0, n0, s0), (a1, b1, n1, s1) in zip(tl, tl[1:]):
        frm = s0 or n0; to = s1 or n1
        frm = {"French": "France", "Spanish": "Spain", "Portuguese": "Portugal", "Dutch": "the Dutch", "British Empire": "Britain", "Ottoman Empire": "the Ottoman Empire", "Republic of Venice": "Venice", "Republic of Genoa": "Genoa", "Crown of Aragon": "Aragon", "Aragón": "Aragon"}.get(frm, frm)
        to2 = {"French": "France", "Spanish": "Spain", "Portuguese": "Portugal", "Dutch": "the Dutch", "British Empire": "Britain", "Ottoman Empire": "the Ottoman Empire", "Republic of Venice": "Venice", "Republic of Genoa": "Genoa", "Crown of Aragon": "Aragon", "Aragón": "Aragon", "Greece": "Greece"}.get(to, to)
        if a1 >= 1886 or frm == to2: continue
        c = geom.representative_point()
        changes.append({"y": a1, "d": str(a1), "t": f"{name[0].upper()+name[1:]} passes from {frm} to {to2}", "k": "transfer", "lon": round(c.x, 2), "lat": round(c.y, 2), "ar": int(geom.area * 9000), "src": "isl"})
from shapely.geometry import box as _bx
LANDU = unary_union(polys)
for name, spec, tl in AREAS:
    from shapely.geometry import Polygon as _Pg
    geom = hb_geom(spec[1], spec[2], spec[3]) if spec[0] == "hb" else make_valid(LANDU.intersection(_Pg(spec[1]) if spec[0] == "poly" else _bx(*spec[1])))
    if geom.is_empty: print("empty area", name, spec); continue
    for a, b, nm, sub in tl:
        feats.append({"type": "Feature", "properties": {"isl": name, "a": a, "b": b, "NAME": nm, "SUBJECTO": sub}, "geometry": mapping(geom)})
    for (a0, b0, n0, s0), (a1, b1, n1, s1) in zip(tl, tl[1:]):
        frm, to = (s0 or n0), (s1 or n1)
        if frm == to or a1 >= 1886: continue
        c = geom.representative_point()
        txt = {("Crimea", 1441): "The Crimean Khanate breaks away from the Golden Horde", ("Crimea", 1475): "The Crimean Khanate becomes an Ottoman vassal"}.get((name, a1), f"{name[0].upper()+name[1:]} passes from the {frm} to the {to}")
        changes.append({"y": a1, "d": str(a1), "t": txt, "k": "transfer", "lon": round(c.x, 2), "lat": round(c.y, 2), "ar": int(geom.area * 9000), "src": "isl"})
json.dump({"type": "FeatureCollection", "features": feats}, open(WORK + "/islands.geojson", "w"))
subprocess.run(["mapshaper", "-i", WORK + "/islands.geojson", "name=islands", "-o", "format=topojson", "precision=0.005", MAPS + "/islands.json"], check=True, capture_output=True)
json.dump(changes, open(ROOT + "/g2/isl_changes.json", "w"))
print(len(feats), "island periods;", len(changes), "ledger lines")
