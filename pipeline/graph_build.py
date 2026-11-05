"""Stage: the link graph. Reads graph/*.py (LINKS, STORY or STORIES, THEMES), runs the hard checks, writes site/graph.json."""
import json, glob, importlib, os, re, sys
sys.path.insert(0, "/home/claude/graph"); sys.path.insert(0, "/home/claude")
D = json.load(open("/home/claude/site/data.json")); EV = D["events"]; E = {e["id"]: e for e in EV}
GRADES = ["Necessary", "Sufficient", "Contributing", "Contested", "Coincident"]
TYPES = ["Structural", "Material", "Ideological", "Reactive", "Enabling", "Precedent"]
CONF = ["High", "Moderate", "Low"]
CONN = [None, "therefore", "but"]
BANNED = ["existential", "in many ways", "complex interplay", "the stage was set", "it is no coincidence", "in other words", "it is important to note", "tapestry", "testament to", "delve", "in conclusion"]
# rule zero: "did not X. It Y" / "not X, but Y" / "not only ... but"
RZ = [re.compile(r"\b(did not|didn't|was not|wasn't|is not|isn't|were not|weren't|never)\b[^.;:]{3,90}[.;]\s+(It|They|He|She|This|That|What|The|Its)\b"),
      re.compile(r"\bnot (?:just|only|merely|simply)\b[^.]{0,80}\bbut\b", re.I),
      re.compile(r"\bis not (?:a|an|the)\b[^.]{0,60}\bbut (?:a|an|the)\b", re.I)]
links, stories, themes, errs = [], [], [], []
def text_checks(where, s):
    low = s.lower()
    for b in BANNED:
        if b in low: errs.append(f"{where}: banned phrase '{b}'")
    for rx in RZ:
        if rx.search(s): errs.append(f"{where}: rule zero (negation-then-reveal): …{rx.search(s).group(0)[:70]}…")
for path in sorted(glob.glob("/home/claude/graph/*.py")):
    M = importlib.import_module(os.path.basename(path)[:-3])
    for l in getattr(M, "LINKS", []):
        w = f"{path}:{l['id']}"
        for end in ("f", "t"):
            x = l[end]
            if not (x in E or (x.startswith("story:"))): errs.append(f"{w}: unknown endpoint {x}")
        if l["grade"] not in GRADES: errs.append(f"{w}: bad grade {l['grade']}")
        if l["type"] not in TYPES: errs.append(f"{w}: bad type {l['type']}")
        if l["conf"] not in CONF: errs.append(f"{w}: bad confidence {l['conf']}")
        n = l["note"]
        for k in ("claim", "objection", "warrant", "verdict"):
            if not n.get(k) or len(n[k]) < 20: errs.append(f"{w}: note.{k} missing")
            else: text_checks(f"{w}.{k}", n[k])
        v = n.get("verdict", "").lower()
        if l["grade"] in ("Necessary", "Sufficient") and not re.search(r"\bwithout\b|\bno other\b|\bis conceivable\b|\bcounterfactual\b|\benough to explain\b|\bneeded\b", v):
            errs.append(f"{w}: {l['grade']} verdict lacks a counterfactual sentence")
        if l["grade"] == "Contributing" and not re.search(r"\bset\b|\branks\b|\bbehind\b", v):
            errs.append(f"{w}: Contributing verdict does not name the set")
        if l["grade"] == "Contested" and not re.search(r"school|holds|hold that|argue", (n["objection"] + " " + v).lower()):
            errs.append(f"{w}: Contested verdict does not name the schools")
        if l["f"] in E and l["t"] in E:
            a, b = E[l["f"]], E[l["t"]]
            if (a["y"], a.get("m") or 0) > (b["y"], b.get("m") or 0): errs.append(f"{w}: link runs backwards in time")
            l["cross"] = bool(l.get("cross")) or (a["r"] != b["r"])
        wc = sum(len(n[k].split()) for k in ("claim", "objection", "warrant", "verdict"))
        l["words"] = wc
        links.append(l)
    for S in ([getattr(M, "STORY")] if hasattr(M, "STORY") else []) + list(getattr(M, "STORIES", [])):
        w = f"{path}:{S['id']}"
        if S["size"] not in ("arc", "story", "thread"): errs.append(f"{w}: bad size")
        for k in ("thesis", "disconfirm", "awkward", "today"):
            if not S.get(k): errs.append(f"{w}: missing {k}")
            else: text_checks(f"{w}.{k}", S[k])
        if len(S.get("assumptions", [])) > 3: errs.append(f"{w}: more than 3 assumptions")
        if not (3 <= len(S.get("shelf", [])) <= 8): errs.append(f"{w}: shelf must hold 3 to 8 works")
        ch = S["chapters"]
        if not ch or (S["size"] != "arc" and not (3 <= len(ch) <= 7)) or (S["size"] == "arc" and len(ch) > 10):
            errs.append(f"{w}: chapter count {len(ch)} out of range")
        for i, c in enumerate(ch):
            cw = f"{w}.{c['id']}"
            if c["hinge"] not in E: errs.append(f"{cw}: unknown hinge {c['hinge']}")
            if c.get("conn") not in CONN or (i == 0) != (c.get("conn") is None): errs.append(f"{cw}: bad connector {c.get('conn')}")
            for k in ("s1", "s2"):
                if not c.get(k): errs.append(f"{cw}: missing {k}")
                else:
                    text_checks(f"{cw}.{k}", c[k])
                    if re.search(r"\b(therefore|and then)\b", c[k].lower()): errs.append(f"{cw}.{k}: connector word in prose")
            if len(c.get("s1", "").split()) > 40: errs.append(f"{cw}: s1 longer than 40 words")
            for s in c.get("support", []):
                if s not in E: errs.append(f"{cw}: unknown support {s}")
            # the arrow between consecutive hinges must exist
            if i > 0:
                prev = ch[i - 1]["hinge"]
                ids = {prev, c["hinge"]}
                # allow a path through one support event
                ok = any(l["f"] == prev and l["t"] == c["hinge"] for l in links)
                if not ok:
                    via = [l["t"] for l in links if l["f"] == prev]
                    ok = any(any(l2["f"] == v and l2["t"] == c["hinge"] for l2 in links) for v in via)
                if not ok: errs.append(f"{cw}: no graded arrow from {prev} to {c['hinge']} (direct or one hop)")
        for t in S.get("tiers", []):
            if t[0] not in E: errs.append(f"{w}: tier score for unknown event {t[0]}")
        stories.append(S)
    for T in getattr(M, "THEMES", []):
        text_checks(f"{path}:{T['id']}", T["passage"])
        themes.append(T)
if errs:
    print("\n".join(errs)); raise SystemExit(f"graph: {len(errs)} problems")
# derived: per-event in/out link ids, story membership
out = {}
for l in links:
    out.setdefault(l["f"], {"out": [], "in": []})["out"].append(l["id"])
    out.setdefault(l["t"], {"out": [], "in": []})["in"].append(l["id"])
mem = {}
for S in stories:
    for c in S["chapters"]:
        mem.setdefault(c["hinge"], []).append(dict(story=S["id"], chapter=c["id"], role="hinge"))
        for s in c.get("support", []): mem.setdefault(s, []).append(dict(story=S["id"], chapter=c["id"], role="support"))
json.dump(dict(links=links, stories=stories, themes=themes, ev=out, mem=mem), open("/home/claude/site/graph.json", "w"), ensure_ascii=False, separators=(",", ":"))
g = {}
for l in links: g[l["grade"]] = g.get(l["grade"], 0) + 1
print(f"graph: {len(links)} links {g}; cross-region {sum(1 for l in links if l['cross'])}; {len(stories)} stories; {len(themes)} themes; note words avg {sum(l['words'] for l in links)//max(1,len(links))}")
