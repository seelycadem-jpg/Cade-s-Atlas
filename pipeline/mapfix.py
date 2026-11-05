"""Stage: map corrections. Reads site/maps/w*.json, patches NAME and SUBJECTO by rule, drops 1492, writes site/maps/."""
import os as _os, sys as _sys; _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '.')); from paths import MAPS, SITE
import json, re, os, shutil
SRC=SITE + "/maps"; DST=MAPS
YEARS=[1400,1500,1530,1600,1650,1700,1715,1783,1800,1815,1880,1900,1914,1920,1930,1938,1945,1960,1994,2000,2010]
UK="United Kingdom"; FR="France"; PT="Portugal"; ES="Spain"; NL="Netherlands"; BE="Belgium"; IT="Italy"; DE="German Empire"; JP="Empire of Japan"; US="United States"; RU="Russian Empire"; SU="USSR"; TR="Ottoman Empire"; CN="China"; ZA="South Africa"; AU="Australia"; DK="Denmark"
# (name regex, from, to, subject or None to clear, new name or None)  -- applied in order; first match wins per feature
R=[
# ---- Africa, British ----
(r"^kenya$|^british east africa$",1895,1962,UK,"Kenya Colony"),
(r"^tanzania|^german e\. africa",1919,1960,UK,"Tanganyika"),
(r"^tanzania",1961,1963,None,"Tanganyika"),(r"^tanzania",1964,2025,None,"Tanzania"),
(r"^german e\. africa",1885,1918,DE,"German East Africa"),
(r"^uganda$",1894,1961,UK,"Uganda Protectorate"),
(r"^zambia$|^northern rhodesia$",1911,1963,UK,"Northern Rhodesia (Zambia)"),
(r"^zimbabwe$|^rhodesia$|^southern rhodesia$",1895,1964,UK,"Southern Rhodesia (Zimbabwe)"),
(r"^zimbabwe$|^rhodesia$",1965,1979,None,"Rhodesia"),
(r"^malawi$|^nyasaland$",1891,1963,UK,"Nyasaland (Malawi)"),
(r"^botswana$",1885,1965,UK,"Bechuanaland (Botswana)"),
(r"^lesotho$|^basutoland$",1868,1965,UK,"Basutoland (Lesotho)"),
(r"^swaziland$",1903,1967,UK,"Swaziland"),(r"^swaziland$",2018,2025,None,"Eswatini"),
(r"^nigeria$|^lagos$|^calabar$|^opobo$|^ibadan$|^oyo$|^benin$|^sokoto",1900,1959,UK,"Nigeria"),
(r"^ghana$|^gold coast|^accra$|^asante$",1896,1956,UK,"Gold Coast (Ghana)"),
(r"^sierra leone$",1808,1960,UK,None),(r"^gambia",1816,1964,UK,"The Gambia"),(r"^gambia, the$",1965,2025,None,"The Gambia"),
(r"^sudan$|^anglo-egyptian sudan$",1899,1955,UK,"Anglo-Egyptian Sudan"),
(r"^egypt$",1882,1921,UK,"Egypt (British occupation)"),(r"^egypt$",1922,2025,None,None),(r"^jamaica \(uk\)$",1945,1961,UK,"Jamaica"),(r"^guyana$",1831,1965,UK,"British Guiana (Guyana)"),(r"^burkina faso$",1960,1983,None,"Upper Volta (Burkina Faso)"),(r"^benin$",1960,1974,None,"Dahomey (Benin)"),
(r"^somalia$|^british somaliland$",1884,1959,UK,"British Somaliland"),
(r"^south africa$|^union of south africa$|^cape colony$|^natal$|^zululand$|^griqualand west$",1910,1930,UK,"Union of South Africa"),
(r"^cape colony$|^natal$|^zululand$|^griqualand west$|^ndebele$|^shona$|^lozi$|^barotse$|^ngwato$|^nguni$|^buganda$|^bunyoro$",1890,1909,UK,None),
(r"^namibia$",1915,1989,ZA,"South West Africa (Namibia)"),(r"^german south-west africa$",1884,1914,DE,None),
(r"^walbis bay$",1878,1993,ZA,"Walvis Bay"),
(r"^malaysia$|^malaya$",1874,1956,UK,"British Malaya"),(r"^malaysia$",1957,1962,None,"Malaya"),
(r"^ceylon|^sri lanka$",1796,1947,UK,"Ceylon (Sri Lanka)"),(r"^sri lanka$|^ceylon$",1948,1971,None,"Ceylon"),
(r"^burma$",1886,1947,UK,"Burma (British India)"),(r"^burma$",1989,2025,None,"Myanmar (Burma)"),
(r"^india$|^british raj$",1858,1946,UK,"British India"),(r"^pakistan$",1945,1946,UK,"British India"),(r"^bangladesh$",1945,1946,UK,"British India"),(r"^bangladesh$",1947,1970,None,"East Pakistan (Bangladesh)"),
(r"^brunei$",1888,1983,UK,None),(r"^hong kong$",1842,1996,UK,None),(r"^hong kong$",1997,2025,CN,None),
(r"^papua new guinea$",1884,1913,DE,"German New Guinea and British Papua"),(r"^papua new guinea$",1914,1974,AU,"Papua and New Guinea (Australia)"),
(r"^fiji$",1874,1969,UK,None),(r"^tonga$",1900,1969,UK,"Tonga (British protectorate)"),(r"^samoa$",1900,1913,DE,"German Samoa"),(r"^samoa$",1914,1961,"New Zealand","Western Samoa"),
(r"^cyprus$",1878,1959,UK,None),(r"^malta$",1800,1963,UK,None),
(r"^jamaica|^trinidad$|^barbados$|^bahamas$|^belize$|^guyana$|^british guiana$|^grenada$|^saint lucia$|^saint vincent|^saint kitts|^antigua|^dominica$|^montserrat$|^anguilla$|^turks and caicos",1700,1961,UK,None),
(r"^trinidad$",1962,2025,None,"Trinidad and Tobago"),(r"^guyana$|^british guiana$",1962,1965,UK,"British Guiana"),(r"^belize$",1962,1980,UK,"British Honduras (Belize)"),(r"^bahamas$",1962,1972,UK,None),(r"^barbados$",1962,1965,UK,None),
(r"^ireland$",1801,1921,UK,None),(r"^iceland$",1380,1917,DK,None),(r"^greenland$",1721,2025,DK,None),
(r"^kuwait$",1899,1960,UK,"Kuwait (British protectorate)"),(r"^qatar$",1916,1970,UK,"Qatar (British protectorate)"),(r"^trucial oman$|^united arab emirates$",1820,1970,UK,"Trucial States (UAE)"),(r"^muscat and oman$|^oman \(british|^oman$",1891,1970,UK,"Muscat and Oman"),
(r"^yemen \(uk\)$|^aden",1839,1966,UK,"Aden Protectorate (South Yemen)"),
(r"^mesopotamia|^iraq$",1920,1931,UK,"Iraq (British mandate)"),(r"^jordan$|^transjordan",1921,1945,UK,"Transjordan (British mandate)"),(r"^israel$|^mandatory palestine",1920,1947,UK,"Palestine (British mandate)"),
(r"^cyraneica|^tripolitan",1943,1950,UK,"Libya (British administration)"),(r"^fezzan",1943,1950,FR,"Fezzan (French administration)"),
(r"^eritrea$",1941,1951,UK,"Eritrea (British administration)"),(r"^eritrea$",1952,1992,"Ethiopia","Eritrea"),
(r"^somalia$",1950,1959,IT,"Italian Somaliland (UN trusteeship)"),
# ---- Africa, French ----
(r"^algeria|^algiers$",1830,1961,FR,"French Algeria"),(r"^tunisia$|^tunis$",1881,1955,FR,"Tunisia (French protectorate)"),(r"^morocco|^morocco \(france\)$",1912,1955,FR,"Morocco (French and Spanish protectorates)"),
(r"^french west africa$|^senegal|^mali$|^guinea$|^ivory coast$|^burkina faso$|^upper volta$|^niger$|^benin$|^dahomey$|^mauritania$|^mossi states$|^futa jalon$|^futa toro$|^tukular|^wassoulou|samori|^kong|^dendi|^borgu|^sultanate of damagaram$|^kaarta$|^segu$",1895,1959,FR,"French West Africa"),
(r"^french equatorial africa$|^chad$|^central african republic$|^gabon$|^congo$|^congo \(france\)$|^teke$|^wadai|^rabih",1910,1959,FR,"French Equatorial Africa"),
(r"^congo$|^gabon$|^teke$",1880,1909,FR,"French Congo"),
(r"^cameroon$|^french cameroons$",1919,1959,FR,"French Cameroun"),(r"^kamerun$|^cameroon$",1884,1918,DE,"Kamerun"),(r"^southern cameroon$",1919,1960,UK,"British Cameroons"),
(r"^togo$|^togoland$",1884,1913,DE,"Togoland"),(r"^togo$|^togoland$",1914,1959,FR,"French Togoland"),
(r"^madagascar|^imerina$|^merina kingdom$",1896,1959,FR,"Madagascar (France)"),
(r"^djibouti$|^french somaliland$",1884,1976,FR,"French Somaliland (Djibouti)"),
(r"^syria|^lebanon$",1920,1943,FR,"Syria and Lebanon (French mandate)"),
(r"^french indo-?china$|^annam$|^tonkin$|^cochin china$|^cambodia$|^laos$|^vietnam$",1887,1953,FR,"French Indochina"),
(r"^cambodia$|^cochin china$",1941,1944,JP,"French Indochina (Japanese occupation)"),
(r"^french guiana$|^guadeloupe$|^martinique|^saint martin$|^saint barthelemy$|^new caledonia$|^wallis and futuna|^french polynesia",1650,2025,FR,None),(r"^new hebrides$",1906,1979,FR,"New Hebrides (Anglo-French condominium)"),
(r"^luisiana$|^louisiana$",1699,1762,FR,"Louisiana"),(r"^luisiana$|^louisiana$",1763,1800,ES,"Louisiana (Spanish)"),(r"^quebec$",1763,1866,UK,"Quebec (British)"),(r"^rupert's land$",1670,1869,UK,None),
# ---- Africa, Portuguese / Belgian / Italian / Spanish / German ----
(r"^angola|^ndongo$|^mbailundu$|^ovimbundu$",1575,1974,PT,"Portuguese Angola"),(r"^mozambique|^portuguese east africa$",1505,1974,PT,"Portuguese East Africa (Mozambique)"),(r"^guinea-bissau|^portuguese guinea$",1650,1973,PT,"Portuguese Guinea"),
(r"^zaire|^belgian congo$|^luba$|^lunda$|^kuba$|^yaka$|^yeke$|^sultanate of utetera$",1885,1907,"Congo Free State","Congo Free State"),(r"^zaire|^belgian congo$|^luba$|^lunda$|^kuba$|^yaka$|^yeke$",1908,1959,BE,"Belgian Congo"),
(r"^zaire$",1960,1970,None,"Congo (Kinshasa)"),(r"^zaire$",1971,1996,None,"Zaire"),(r"^zaire$",1997,2025,None,"Democratic Republic of the Congo"),
(r"^rwanda|^burundi$",1899,1918,DE,"German East Africa"),(r"^rwanda|^burundi$",1919,1961,BE,"Ruanda-Urundi"),
(r"^mirambo|^unyanyembe",1890,1918,DE,"German East Africa"),
(r"^eritrea",1890,1940,IT,"Italian Eritrea"),(r"^italian somaliland$",1889,1940,IT,None),(r"^libya|^tripolitania$|^cyrenaica$",1911,1942,IT,"Italian Libya"),(r"^ethiopia \(italy\)$|^ethiopia$|^abyssinia$",1936,1940,IT,"Italian East Africa"),
(r"^equatorial guinea$|^spanish guinea$",1778,1967,ES,"Spanish Guinea (Equatorial Guinea)"),(r"^western sahara$|^spanish sahara$|^rio de oro$",1884,1975,ES,"Spanish Sahara"),(r"^spanish morocco$",1912,1955,ES,None),
(r"^cuba \(spain\)$|^cuba$",1511,1897,ES,"Cuba (Spanish)"),(r"^cuba$",1898,1901,US,"Cuba (US occupation)"),(r"^puerto rico$",1508,1897,ES,None),(r"^puerto rico$",1898,2025,US,None),(r"^philippines$",1565,1897,ES,"Spanish Philippines"),(r"^philippines$",1898,1945,US,"Philippines (United States)"),
(r"^santo domingo|^dominican republic$",1715,1820,ES,"Santo Domingo (Spanish)"),(r"^hispaniola \(spain\)$",1530,1700,ES,None),
(r"^guam$|^american samoa$|^united states virgin islands$|^saipan$",1898,2025,US,None),(r"^kingdom of hawaii$",1898,1900,US,"Hawaii (United States)"),
(r"^hawaii",1898,2025,US,None),
# ---- Dutch ----
(r"^dutch east indies$|^netherlands indies$|^indonesia$",1800,1948,NL,"Dutch East Indies (Indonesia)"),(r"^dutch east indies$|^netherlands indies$",1602,1799,"Dutch East India Company","Dutch East Indies"),
(r"^suriname$|^surinam$|^dutch guiana$",1667,1974,NL,"Dutch Guiana (Suriname)"),(r"^netherlands antilles$|^aruba|^curaçao",1634,2025,NL,None),(r"^dutch guinea$",1828,1962,NL,"Dutch New Guinea"),(r"^guyana$",1945,1945,NL,"Dutch Guiana (Suriname)"),
(r"^dutch formosa$",1624,1662,NL,None),(r"^ceylon \(dutch\)$",1640,1796,NL,"Dutch Ceylon"),
# ---- Japanese ----
(r"^korea$",1910,1944,JP,"Korea (Japanese rule)"),(r"^taiwan$",1895,1944,JP,"Taiwan (Japanese rule)"),(r"^manchuria$",1932,1944,JP,"Manchukuo"),(r"^sakhalin",1905,1944,JP,"Karafuto (Japan)"),
(r"^korea \(usa\)$",1945,1947,US,"Korea, US zone"),(r"^korea \(ussr\)$",1945,1947,SU,"Korea, Soviet zone"),(r"^korea, republic of$",1948,2025,None,"South Korea"),(r"^korea, democratic",1948,2025,None,"North Korea"),
(r"^japan \(usa\)$",1945,1951,US,"Japan (Allied occupation)"),
# ---- Russia / USSR ----
(r"^armenia$|^georgia$|^azerbaijan$",1922,1990,SU,None),(r"^armenia$|^georgia$|^azerbaijan$",1801,1917,RU,None),
(r"^ukraine$|^white russia$|^byelarus$|^far eastern ssr$",1922,1990,SU,None),(r"^byelarus$",1991,2025,None,"Belarus"),
(r"^finland$",1809,1916,RU,"Grand Duchy of Finland"),(r"^poland$",1815,1914,RU,"Congress Poland (Russian)"),
(r"^central asian khanates|^bokhara|^bukara|^khiva",1868,1919,RU,"Russian Turkestan and the khanates"),(r"^central asian khanates",1400,1867,None,"Central Asian khanates"),
(r"^kazakhstan$|^uzbekistan$|^turkmenistan$|^kyrgyzstan$|^tajikistan$",1924,1990,SU,None),
(r"^estonia$|^latvia$|^lithuania$",1940,1990,SU,None),
(r"^germany \(soviet\)$",1945,1948,SU,"Germany, Soviet zone"),(r"^germany \(uk\)$",1945,1948,UK,"Germany, British zone"),(r"^germany \(usa\)$",1945,1948,US,"Germany, American zone"),(r"^germany \(france\)$",1945,1948,FR,"Germany, French zone"),(r"^saar",1947,1956,FR,"Saar Protectorate"),
# ---- China ----
(r"^tibet$",1720,1911,"Qing Empire","Tibet (Qing protectorate)"),(r"^tibet$",1951,2025,CN,"Tibet (China)"),(r"^xinjiang$",1884,1949,CN,"Xinjiang (China)"),(r"^manchu empire$|^qing",1644,1911,None,"Qing Empire"),(r"^manchu empire$",1912,1914,None,"Republic of China"),(r"^chinese warlords$",1916,1927,None,"Republic of China (warlord era)"),(r"^chinese warlords$",1928,1944,None,"Republic of China"),
(r"^mongolia$",1691,1910,"Qing Empire","Outer Mongolia (Qing)"),
# ---- Ottoman and Middle East ----
(r"^egypt$",1517,1804,TR,"Ottoman Egypt"),(r"^egypt$",1805,1881,TR,"Egypt (khedivate)"),(r"^algiers$",1516,1829,TR,"Regency of Algiers"),(r"^tunis$",1574,1880,TR,"Beylik of Tunis"),(r"^tripolitania$|^cyrenaica$",1551,1910,TR,"Ottoman Tripolitania"),(r"^hejaz$",1517,1915,TR,"Hejaz (Ottoman)"),(r"^yemen$",1872,1917,TR,"Yemen (Ottoman)"),(r"^iraq$|^mesopotamia",1534,1917,TR,"Ottoman Iraq"),
(r"^ottoman sultanate$",1920,1922,None,"Ottoman Empire"),(r"^republic of turkey$",1923,2025,None,"Turkey"),
(r"^iran$",1700,1934,None,"Persia"),(r"^persia$",1935,2025,None,"Iran"),
(r"^rattanakosin kingdom$|^siam$",1782,1938,None,"Siam (Thailand)"),(r"^kingdom of brazil$",1822,1888,None,"Empire of Brazil"),(r"^kingdom of brazil$",1889,1930,None,"Brazil"),
(r"^abyssinia$",1855,1935,None,"Ethiopia"),(r"^imperial japan$",1868,1946,None,"Empire of Japan"),(r"^united states of america$",1776,2025,None,"United States"),(r"^harer \(egypt\)$",1875,1884,"Egypt","Harar (Egyptian occupation)"),
(r"^sicily$",1400,1400,None,"Kingdom of Naples"), (r"^blue horde$",1400,1500,None,"Golden Horde"), (r"^bulgar khanate$",1400,1400,None,"Ottoman Empire"), (r"^great khanate$",1400,1400,None,"Northern Yuan (Mongols)"),
(r"^macedonia$",2019,2025,None,"North Macedonia"),(r"^czech republic$",2016,2025,None,"Czechia"),
]
R=[(re.compile(a,re.I),b,c,d,e) for a,b,c,d,e in R]
os.makedirs(DST,exist_ok=True)
shutil.copy(f"{SRC}/land.json",f"{DST}/land.json")
if os.path.exists(f"{DST}/w1492.json"): os.remove(f"{DST}/w1492.json")
log=[]
for y in YEARS:
    t=json.load(open(f"{SRC}/w{y}.json")); g=t["objects"][f"world_{y}"]["geometries"]; n=0
    for x in g:
        p=x["properties"]; name=p.get("NAME") or ""
        if not name: continue
        for rx,a,b,subj,new in R:
            if a<=y<=b and rx.search(name):
                p["SUBJECTO"]=subj
                if new: p["NAME"]=new
                n+=1; break
        if p.get("SUBJECTO")==p.get("NAME"): p["SUBJECTO"]=None
    json.dump(t,open(f"{DST}/w{y}.json","w"),separators=(",",":"),ensure_ascii=False); log.append(f"{y}: {n} patched")
print("; ".join(log))
