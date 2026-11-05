import json, sys, collections
R=json.load(open(sys.argv[1]))
def era(y): return "1400-1599" if y<1600 else "1600-1799" if y<1800 else "1800-1885" if y<1886 else "1886-1945" if y<1946 else "1946-2020"
def acc(rows):
    n=len(rows); ok=sum(r["v"].startswith("ok") for r in rows); return ok/n if n else None, n
S=collections.defaultdict(list)
for r in R: S[(r["src"],r["region"],era(r["y"]))].append(r)
srcs=sorted({r["src"] for r in R}); regs=sorted({r["region"] for r in R}); eras=["1400-1599","1600-1799","1800-1885","1886-1945","1946-2020"]
for s in srcs:
    rows=[r for r in R if r["src"]==s]; a,n=acc(rows); print(f"\n== {s}: {a:.1%} of {n}")
    print("region".ljust(16)+"".join(e.rjust(11) for e in eras))
    for g in regs:
        line=g.ljust(16)
        for e in eras:
            a,n=acc(S[(s,g,e)]); line+=(f"{a:.0%}({n})" if a is not None else "-").rjust(11)
        print(line)
    c=collections.Counter(r["v"] for r in rows); print(dict(c))
