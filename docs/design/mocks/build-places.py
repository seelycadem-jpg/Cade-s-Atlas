"""Writes event-v12-places.js: where each event of the mock's chain happened, as a country and a place.

Run from the repo root:  python3 docs/design/mocks/build-places.py

The place is the `where` field of site/data.json (Prototype 1 data, to be rewritten), with any bracketed aside
removed. That data holds no country field, so the country below was added by hand from the place the data names,
as the present-day country. Where the data names something larger than one country (Europe, the Holy Roman
Empire, the Soviet Union) or a region that no one country holds (Silesia), that name stands in the country's
place and no city is given. Every country here is a placeholder until each event carries its own country field.
"""
import json, re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..', '..'))

# id: (country or wider region, place within it or None). The place repeats the data's own words.
PLACES = {
    'af188425': ('Germany', 'Berlin'),
    'as191949': ('China', 'Beijing'),
    'as193153': ('China', 'Manchuria'),
    'd-bismarck1890': ('Germany', 'Berlin'),
    'd-depression1930': ('Germany', 'Berlin'),
    'd-frankfurt': ('Germany', 'Frankfurt'),
    'd-hyperinflation': ('Germany', 'Berlin'),
    'd-zeitenwende': ('Germany', 'Berlin'),
    'd-zollverein': ('Germany', 'Berlin'),
    'eu151712': ('Germany', 'Wittenberg'),
    'eu155520': ('Germany', 'Augsburg'),
    'eu161831': ('Holy Roman Empire', None),
    'eu164833': ('Germany', 'Münster and Osnabrück'),
    'eu174050': ('Silesia', None),
    'eu180662': ('Germany', None),
    'eu181565b': ('Austria', 'Vienna'),
    'eu184871': ('Europe', None),
    'eu187076': ('France', None),
    'eu187177': ('France', 'Versailles'),
    'eu189481': ('Europe', None),
    'eu189882': ('Germany', None),
    'eu191485': ('Europe', None),
    'eu191786': ('Russia', 'Petrograd'),
    'eu191988': ('France', 'Paris'),
    'eu193391': ('Germany', None),
    'eu193893': ('Germany', 'Munich'),
    'eu193994': ('Poland', None),
    'eu194196': ('Soviet Union', None),
    'eu194999b': ('Germany', 'Bonn and East Berlin'),
    'eu1990110': ('Germany', None),
    'na192964': ('United States', 'New York'),
    'na194568': ('United States', 'San Francisco'),
    'w2-rhineland': ('Germany', 'Rhineland'),
}

data = {e['id']: e for e in json.load(open(os.path.join(REPO, 'site', 'data.json'), encoding='utf8'))['events']}
chain = open(os.path.join(ROOT, 'atlas-data.js'), encoding='utf8').read()
ids = sorted(set(re.findall(r'"id"\s*:\s*"([^"]+)"', chain)) & set(data))
missing = [i for i in ids if i not in PLACES]
assert not missing, 'no place for: ' + ', '.join(missing)

out = {}
for i in ids:
    country, place = PLACES[i]
    out[i] = {'c': country, 'p': place} if place else {'c': country}

head = ("/* Where each event of the mock's chain happened: a country (or a wider region) and, where the old data names\n"
        "   one, a place within it. Written by build-places.py; see that file for where each part comes from. The countries\n"
        "   are placeholders until every event carries its own country field. Generated, not hand-edited. */\n")
open(os.path.join(ROOT, 'event-v12-places.js'), 'w', encoding='utf8').write(
    head + 'window.ATLAS_PLACE=' + json.dumps(out, ensure_ascii=False, sort_keys=True) + ';\n')
print(len(out), 'places written')
