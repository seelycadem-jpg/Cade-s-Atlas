import sys, json, re
sys.path.insert(0, "/home/claude")
import data_us, data_eu, data_eu2, data_asia, data_africa, data_africa2, data_latam
from coords import C
from facts import F, S

src = open("/mnt/user-data/uploads/build.py").read().split("REGIONS = {")[0]
ns = {}; exec(src, ns)

REG = [
    ("na", "North America", data_us.E),
    ("eu", "Europe", [e for e in data_eu.E if e[0] < 1845] + data_eu2.E),
    ("as", "Asia & Middle East", data_asia.E),
    ("af", "Africa", [e for e in data_africa.E if e[0] < 1882] + data_africa2.E),
    ("la", "Latin America", data_latam.E),
]

THREADS = {
 "slavery": ("Slavery & Freedom", r"slave|enslav|abolish|abolition|emancipat|jim crow|segregat|civil rights|apartheid|dred scott|plessy|brown v|voting rights|cotton gin|missouri compromise|kansas-nebraska|haiti|liberia|elmina|kongo|montgomery|reconstruction|mandela|stono|compromise of 1850|juneteenth|13th amendment"),
 "empire": ("Empires & Colonization", r"conquer|conquest|colon|scramble|berlin conference|east india|\bvoc\b|raj|plassey|opium|annex|takes goa|takes malacca|singapore|manila|protectorate|congo free|\bcape\b|occup|sack|cortés|pizarro|tenochtitlan|imperial|empress of india|indochina|takes taiwan|takes the cape|takes philippines|seize"),
 "indep": ("Independence & Decolonization", r"independen|decoloni|year of africa|partition|oau|african union|gran colombia|bolívar|ayacucho|hidalgo|argentina independent|mau mau|algerian war|tanzania formed|ghana|zimbabwe"),
 "revolution": ("Revolutions & Uprisings", r"revolution|revolt|rebellion|uprising|commune|mau mau|maji maji|boxer|taiping|coup|arab spring|tiananmen|solidarity|prague spring|bacon's"),
 "rights": ("Rights & Self-Government", r"rights|constitution|suffrage|assembly|parliament|democra|declaration of independence|seneca|locke|rousseau|mayflower|civil rights|glorious|magna|elected|republic"),
 "coldwar": ("The Cold War", r"cold war|soviet|ussr|nato|berlin wall|cuban missile|bay of pigs|sputnik|korean war|vietnam|marshall plan|truman doctrine|inf treaty|gorbachev|hungarian|prague spring|helsinki|che |lumumba|guatemala|pinochet|afghanistan|sandinista|moon landing|dien bien"),
 "worldwars": ("World Wars", r"wwi|wwii|world war|armistice|versailles|pearl harbor|d-day|hitler|munich|fall of france|invades ussr|hiroshima|atomic|holocaust|east africa campaign|sykes|japan invades china|manchuria|nagasaki"),
 "science": ("Science & Technology", r"print|telescope|newton|copernicus|darwin|steam|railway|railroad|canal|wright|model t|sputnik|moon|dot-com|\bwatt\b|cotton gin|chernobyl|atomic|hiroshima|guns reach|hangul|galileo"),
 "money": ("Money, Trade & Resources", r"spice|trade route|free trade|trading|bubble|\bbank\b|stock market|gold rush|gold standard|gold fields|gold mines|silver|\boil\b|debt|default|federal reserve|nafta|wto|\beuro\b|financial|joint-stock|\bvoc\b|embargo|galleon|potosí|wealth of nations|clove|rubber|diamond|bailout|inflation|mercantil"),
 "native": ("Indigenous Americas", r"native|indigenous|cherokee|lakota|wampanoag|powhatan|inca|aztec|taíno|tenochtitlan|trail of tears|wounded knee|little bighorn|túpac|zapatista|indian removal|king philip"),
 "westward": ("US Expansion", r"louisiana purchase|lewis|florida acquired|texas|mexican-american|gold rush|alaska|transcontinental|manifest destiny|frontier|half its land|hawaii|philippines|spanish-american|monroe doctrine|roosevelt corollary|panama"),
 "atrocity": ("Atrocities & Genocide", r"genocide|massacre|holocaust|khmer|srebrenica|herero|rwanda|nanjing massacre|trail of tears|wounded knee|terror|famine killed|purges"),
 "conflict": ("Wars of the Great Powers", r"hundred years|wars of the roses|italian wars|thirty years|spanish succession|austrian succession|seven years|napoleon|trafalgar|crimean|franco-prussian|triple alliance|franco-russian|entente|navy|lepanto|armada|westphalia|utrecht|poltava|yorktown|1812|gettysburg|civil war"),
 "faith": ("Religion & Ideas", r"church|luther|reformation|inquisition|catholic|protestant|islam|shi'a|jihad|caliph|puritan|quaker|pilgrim|huguenot|nantes|augsburg|trent|henry viii|witch|worms|bartholomew|\bisis\b|khomeini|iranian revolution|sokoto"),
 "china": ("China's Long Century", r"china|chinese|qing|\bming\b|beijing|\bmao\b|deng|\bxi jinping\b|taiwan|hong kong|opium|boxer|taiping|nanjing|tiananmen|manchuria|kangxi|tumu|sino-japanese|summer palace|may fourth|great leap|cultural revolution"),
 "mideast": ("Ottomans to the Modern Middle East", r"ottoman|turk|constantinople|istanbul|suleiman|sykes|israel|\biraq\b|\biran\b|gaza|suez|\barab\b|\bisis\b|safavid|persia|egypt|gulf|six-day|yom kippur|syria|mohács|vienna|lepanto|nader shah|tanzimat"),
 "russia": ("Russia & the USSR", r"russia|soviet|ussr|tsar|stalin|lenin|gorbachev|putin|peter the great|catherine|poltava|crimea|ukraine|chernobyl|serfs|sputnik|georgia war"),
 "eastafrica": ("East Africa & the Swahili Coast", r"kilwa|mombasa|zanzibar|tanganyika|tanzania|kenya|uganda|\bamin\b|ethiopia|adal|adwa|maji maji|mau mau|nyerere|east africa|selassie|tigray|sudan|darfur|rwanda|arusha|somalia|\boman\b"),
 "japan": ("Japan's Rise", r"japan|shogun|meiji|\bedo\b|tokugawa|hideyoshi|perry|sekigahara|ōnin|tsushima|fukushima|hiroshima|pearl harbor|manchuria"),
 "explore": ("Exploration & Contact", r"reaches|rounds|explores|columbus|cabot|cartier|da gama|balboa|cabral|dias|lewis & clark|tordesillas|jamestown|mayflower|quebec|roanoke|guns reach|black ships"),
}

CATRX = {
 "war": r"war\b|wars\b|battle|siege|invade|invasion|conquer|massacre|genocide|army|attack|armada|revolt|rebellion|uprising|coup|bomb",
 "political": r"treaty|independen|constitution|empire|republic|revolution|annex|parliament|act\b|doctrine|alliance|union|unif|state|throne|emperor|king|president|elected|rights|suffrage|colony|partition|dynasty|shogun|congress|league|nato|\beu\b",
 "economic": r"trade|company|bank|bubble|crash|gold|silver|oil|debt|default|economy|market|tax|canal|railroad|railway|cotton|nafta|wto|euro|financial|slave trade|purchase|plan\b|reforms|embargo",
 "ideas": r"rights|declaration|manifesto|locke|rousseau|machiavelli|hobbes|smith|enlightenment|communis|social contract|wealth of nations|leviathan|prince\b|socialis|nationalis|democra",
 "religion": r"church|luther|reformation|inquisition|catholic|protestant|islam|shi'a|jihad|caliph|puritan|quaker|pilgrim|huguenot|nantes|augsburg|trent|witch|worms|bartholomew|isis|khomeini|pope|religio|sokoto|jews",
 "science": r"press|telescope|newton|copernicus|darwin|steam|railway|flight|model t|sputnik|moon|internet|dot-com|watt|cotton gin|nuclear|atomic|chernobyl|galileo|guns|cannon|ebola|covid|pandemic|alphabet",
 "culture": r"mona lisa|sistine|taj mahal|hangul|alphabet|shakespeare|newspaper|art\b|music|film|olympic",
}
def auto_cats(text, head):
    t = (head + " " + text).lower()
    c = [k for k, rx in CATRX.items() if re.search(rx, t)]
    return c[:3] or ["political"]
try:
    from rewrites import REWRITE
except Exception:
    REWRITE = {}

def basemap(y):
    ys = [1400, 1492, 1500, 1530, 1600, 1650, 1700, 1715, 1783, 1800, 1815, 1880, 1900, 1914, 1920, 1930, 1938, 1945, 1960, 1994, 2000, 2010]
    return max([b for b in ys if b <= y])

events, missing = [], []
for rid, rname, E in REG:
    seen = set()
    for i, (yr, head, who, where, what, why, sig) in enumerate(sorted(E, key=lambda e: e[0])):
        if (yr, head) in seen: continue
        seen.add((yr, head))
        if head not in C: missing.append(head); continue
        lat, lon = C[head]
        text = " ".join([head, what, why, sig]).lower()
        th = [k for k, (_, rx) in THREADS.items() if re.search(rx, text)]
        if rid != "as" and "china" in th and not re.search(r"china|qing|beijing|boxer|opium|taiwan|hong kong", head.lower()): th.remove("china")
        if rid != "af": th = [x for x in th if x != "eastafrica"]
        EXCL = {("slavery","Haiti earthquake"),("slavery","Haiti's president assassinated"),("slavery","JFK assassinated"),("faith","Fall of France"),("faith","Taj Mahal begun"),("faith","Tudors take the English throne")}
        th = [x for x in th if (x, head) not in EXCL]
        cats = auto_cats(text, head)
        ev = dict(id=f"{rid}{yr}{i}", y=yr, r=rid, h=head, who=who, where=where, what=what, why=why, sig=sig,
                  lat=lat, lon=lon, map=basemap(yr), t=th, c=cats, w=2)
        RW = REWRITE.get(rid+"|"+head)
        if RW:
            ev.update(c=RW[0], w=RW[1], hook=RW[2], story=RW[3], then=RW[4], now=RW[5])
        if head in F: ev["fact"] = F[head]
        if head in S: ev["sites"] = [dict(n=n, lat=a, lon=b, d=d) for n, a, b, d in S[head]]
        events.append(ev)

events.sort(key=lambda e: (e["y"], e["r"]))
bands = dict(
    era=[dict(a=a, b=b + 9, t=t.title(), c=c) for a, b, t, c in ns["ERAS"]],
    order=[dict(a=s[0], b=s[1] + 9, t=s[2]) for s in ns["EXPLORE"]],
    war=[dict(a=s[0], b=s[1] + 9, t=s[2]) for s in ns["CONFLICTS"]],
    tech=[dict(a=s[0], b=s[1] + 9, t=s[2]) for s in ns["TECH"]],
)
out = dict(events=events, threads={k: v[0] for k, v in THREADS.items()}, bands=bands,
           regions=[dict(id=r, name=n) for r, n, _ in REG])
json.dump(out, open("/home/claude/site/data.json", "w"), ensure_ascii=False, separators=(",", ":"))
print(len(events), "events; missing coords:", missing)
print("facts:", sum("fact" in e for e in events), "sites:", sum("sites" in e for e in events))
from collections import Counter
print(Counter(t for e in events for t in e["t"]))
print("no thread:", [e["h"] for e in events if not e["t"]][:40])
