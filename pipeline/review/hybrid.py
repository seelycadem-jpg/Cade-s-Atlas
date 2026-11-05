import json, collections, sys
import score as S
R = [r for r in json.load(open("score_atlas.json")) if r["y"] < 1886]
HBY = [y for y in S.HBY if y <= 1900]
res = collections.Counter(); tab = collections.Counter()
for D in (15, 30, 50):
    c = collections.Counter()
    for r in R:
        p = S.CP[r["i"]]; t = S.truth(p, r["y"])
        v = r["v"]
        if v == "blank" or (v == "ok" and t["ruler"] == "none"):
            sy = min(HBY, key=lambda y: abs(y - r["y"]))
            if abs(sy - r["y"]) <= D:
                m = S.hb_at(p, sy)
                if m and m != "skip" and not S.PEOPLE.search(m.get("NAME") or ""):
                    v2, _ = S.judge(t, m); c[(v, v2)] += 1; continue
        c[(v, v)] += 0
    gain = sum(n for (a, b), n in c.items() if not a.startswith("ok") and b.startswith("ok"))
    loss = sum(n for (a, b), n in c.items() if a.startswith("ok") and not b.startswith("ok"))
    print("D", D, "fixed", gain, "broken", loss, "of", len(R), dict(c))
