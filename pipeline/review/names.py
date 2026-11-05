"""Polity name matching by lineage: two names match when they name the same state, whatever the regime label
(Kingdom of France / French Third Republic / France) or spelling. Extended by EQUIV for names that share no word."""
import re, unicodedata
GENERIC = set("""kingdom empire sultanate khanate emirate imamate caliphate duchy grand principality republic state states
dynasty confederation confederacy union peoples people's democratic federal federation socialist islamic united of the and
crown realm county margraviate archduchy electorate landgraviate bishopric prince archbishopric lordship lords
khaganate horde tsardom shogunate regency beylik pashalik eyalet viceroyalty colony protectorate territory dominion province
first second third fourth fifth sixth new old great greater lesser later early northern southern eastern western
free imperial royal holy rule period mandate commonwealth company government provisional regime administration
federative popular arab""".split())
SYN = {
 "russian": "russia", "muscovy": "russia", "moscow": "russia", "soviet": "russia", "ussr": "russia", "rsfsr": "russia", "sfsr": "russia",
 "english": "britain", "england": "britain", "british": "britain", "kingdom_gb": "britain", "uk": "britain", "scotland": "scotland",
 "french": "france", "francia": "france", "vichy": "france",
 "spanish": "spain", "espana": "spain", "habsburg_spain": "spain",
 "portuguese": "portugal", "dutch": "netherlands", "holland": "netherlands", "batavian": "netherlands", "voc": "netherlands", "netherland": "netherlands",
 "german": "germany", "prussian": "prussia", "ottoman": "ottoman", "turkey": "ottoman", "turkish": "ottoman", "osmanli": "ottoman",
 "austrian": "austria", "habsburg": "austria", "austria-hungary": "austria", "hungarian": "hungary",
 "polish": "poland", "polish-lithuanian": "poland", "lithuanian": "lithuania", "swedish": "sweden", "danish": "denmark",
 "norwegian": "norway", "italian": "italy", "japanese": "japan", "chinese": "china", "qing": "qing", "ming": "ming",
 "persian": "persia", "iran": "persia", "iranian": "persia", "mughal": "mughal", "moghul": "mughal", "belgian": "belgium",
 "american": "usa", "america": "usa", "usa": "usa", "us": "usa", "mexican": "mexico", "egyptian": "egypt",
 "ethiopian": "ethiopia", "abyssinia": "ethiopia", "abyssinian": "ethiopia", "venetian": "venice", "genoese": "genoa",
 "byzantine": "byzantium", "mamluk": "mamluk", "mamluks": "mamluk", "safavid": "safavid", "timurid": "timurid",
}
EQUIV = [
 {"usa", "united states america"},
 {"britain", "great britain", "united kingdom", "britain ireland", "britain northern ireland"},
 {"germany", "reich", "nazi germany", "weimar"},
 {"russia", "rus"},
 {"austria", "hungary austria"},
]
PHRASE = [("united states", "usa"), ("united kingdom", "britain"), ("great britain", "britain"), ("soviet union", "russia"),
 ("chiang mai", "chiangmai"), ("comtat venaissin", "papal"), ("holy see", "papal"), ("pope", "papal"), ("ya'ruba", "yarubid"), ("ya ruba", "yarubid")]
def strip(s, keep_paren=False):
    s = unicodedata.normalize("NFKD", s.replace("\u2013", " ").replace("\u2014", " ")).encode("ascii", "ignore").decode().lower()
    if not keep_paren: s = re.sub(r"\(.*?\)", " ", s)
    s = s.replace("&", " and ").replace("-", " ").replace("_", " ")
    for a, b in PHRASE: s = s.replace(a, b)
    return s
def toks(s, keep_paren=False):
    ws = re.findall(r"[a-z][a-z']*", strip(s, keep_paren))
    out = []
    for w in ws:
        w = w.strip("'-")
        if w.endswith("'s"): w = w[:-2]
        w = SYN.get(w, w)
        if w in GENERIC or len(w) < 2: continue
        out.append(w)
    return out
def key(s): return " ".join(sorted(set(toks(s))))
ALIAS = [("qing", "china"), ("ming", "china"), ("jagiellon", "poland"), ("jagiellon", "lithuania"), ("rumania", "romania"),
 ("kathmandu", "kantipur"), ("thailand", "rattanakosin"), ("siam", "thailand"), ("siam", "rattanakosin"), ("siam", "ayutthaya"), ("hellenic", "greece"), ("greek", "greece"),
 ("kashmiri", "kashmir"), ("qasimids", "zaydi"), ("qasimid", "zaydi"), ("zaire", "congo"), ("northern yuan", "mongol"), ("mughals", "mughal"),
 ("bharat", "india"), ("burma", "myanmar"), ("burmese", "myanmar"), ("toungoo", "taungoo"), ("vietnam", "dai viet"), ("annam", "dai viet"),
 ("korea", "joseon"), ("choson", "joseon"), ("sicily", "two sicilies"), ("naples", "two sicilies"), ("savoy", "sardinia"), ("piedmont", "sardinia")]
def ali(A, B):
    for x, y in ALIAS:
        xs, ys = set(x.split()), set(y.split())
        if (xs <= A and ys <= B) or (ys <= A and xs <= B): return True
    return False
def same(a, b):
    if isinstance(a, list): return any(same(x, b) for x in a)
    if isinstance(b, list): return any(same(a, x) for x in b)
    if not a or not b: return False
    if strip(a).strip() == strip(b).strip(): return True
    if strip(a).replace(" ", "") == strip(b).replace(" ", ""): return True
    A, B = set(toks(a, True)), set(toks(b, True))
    if ali(A, B): return True
    A, B = set(toks(a)), set(toks(b))
    if not A or not B: return False
    if A & B: return True
    ka, kb = " ".join(sorted(A)), " ".join(sorted(B))
    for g in EQUIV:
        if ka in g and kb in g: return True
    return False
