"""Writes event-v12-stories.js: which stories each event of the mock's chain belongs to.

Run from the repo root:  python3 docs/design/mocks/build-stories.py

PLACEHOLDER MEMBERSHIP. The standards say links, never dates alone, put an event in a chapter, and the new atlas
has not yet built its stories. This file stands in for that with the `arcs` of site/data.json (Prototype 1): each
old arc is treated as one story, named by the arc's own `short` name. It exists so the chain's Story control can be
judged. It is not the atlas's list of stories and the names are not final.
"""
import json, re, os

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(ROOT, '..', '..', '..'))

d = json.load(open(os.path.join(REPO, 'site', 'data.json'), encoding='utf8'))
data = {e['id']: e for e in d['events']}
arcs = {a['id']: (a.get('short') or a.get('title') or a['id']) for a in d['arcs']}
# The mock's page says it was reached through the story "Weimar Germany" (the line under its title). The old arc that
# stands in for that story takes that name here, so the chain's line matches the page. Its events are still the old
# arc's ("Depression & dictators"); only the name changes.
arcs['interwar'] = 'Weimar Germany'
chain = open(os.path.join(ROOT, 'atlas-data.js'), encoding='utf8').read()
ids = sorted(set(re.findall(r'"id"\s*:\s*"([^"]+)"', chain)) & set(data))

of, used = {}, {}
for i in ids:
    mine = [a for a in (data[i].get('arcs') or []) if a in arcs]
    if mine:
        of[i] = mine
        for a in mine:
            used[a] = arcs[a]

head = ("/* PLACEHOLDER: which stories each event of the mock's chain belongs to, taken from the `arcs` of site/data.json\n"
        "   (Prototype 1), one old arc standing for one story. Written by build-stories.py; see that file. Not the atlas's\n"
        "   list of stories. Generated, not hand-edited. */\n")
open(os.path.join(ROOT, 'event-v12-stories.js'), 'w', encoding='utf8').write(
    head + 'window.ATLAS_STORY=' + json.dumps({'names': used, 'of': of}, ensure_ascii=False, sort_keys=True) + ';\n')
print(len(of), 'events,', len(used), 'stories:', ', '.join(sorted(used.values())))
