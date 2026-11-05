// CShapes 2.0 -> maps/cs.json (topology with compact props) + changes from 1886 on.
const fs = require("fs");
const topo = require("topojson-client");
const _pl = require("polylabel"); const polylabel = _pl.default || _pl;
const d3 = require("d3-geo");
const T = JSON.parse(fs.readFileSync(__dirname + "/cs_20.json"));
const NAMES = JSON.parse(fs.readFileSync(__dirname + "/names.json")).map(r => ({ re: new RegExp(r[0]), o: r[1] ? new RegExp(r[1]) : null, a: r[2], b: r[3], n: r[4] }));
const obj = T.objects.cshapes_2_gw;
const G = obj.geometries;
const dec = s => { const [y, m, d] = s.split("-").map(Number); const t0 = Date.UTC(y, 0, 1), t1 = Date.UTC(y + 1, 0, 1); return +(y + (Date.UTC(y, m - 1, d) - t0) / (t1 - t0)).toFixed(4); };
const rawName = {}; G.forEach(g => { if (g.properties.status === "independent") rawName[g.properties.gwcode] = g.properties.country_name; });
rawName[0] = "League of Nations"; rawName[1] = "United Nations";
function clean(n) {
  return n.replace(/ \((Soviet Union|Prussia|Ottoman Empire|Persia|Kampuchea|Zaire|Malagasy|Upper Volta|Byelorussia|FYROM\/North Macedonia|Rhodesia|Ceylon|Burma|Tanganyika|Eswatini|Somaliland Republic|North Borneo)\)/, "")
          .replace(/^Congo, Democratic Republic of/, "DR Congo").replace(/^Korea, People's Republic of/, "North Korea").replace(/^Korea, Republic of/, "South Korea")
          .replace(/ \(Arab Republic of Yemen\)/, "").replace(/ \(German New Guinea\) \(Kaiser Wilhelmsland\)/, "").replace(/ \(Dutch New Guinea\)/, "").replace(/ \(Annam\/Cochin China\/Tonkin\)/, "")
          .replace(/^Italy\/Sardinia$/, "Italy").replace(/^Rumania$/, "Romania");
}
function display(raw, ownerRaw, y) { for (const r of NAMES) if (r.re.test(raw) && y >= r.a && y < r.b && (!r.o || r.o.test(ownerRaw || ""))) return r.n; return clean(raw); }
const feats = topo.feature(T, obj).features;
const R = 6371;
const out = [];
feats.forEach((f, i) => {
  const p = f.properties, g = G[i];
  // largest polygon for the label
  const polys = f.geometry.type === "Polygon" ? [f.geometry.coordinates] : f.geometry.coordinates;
  let best = null, ba = -1;
  for (const poly of polys) { const a = d3.geoArea({ type: "Polygon", coordinates: poly }); const aa = a > 2 * Math.PI ? 4 * Math.PI - a : a; if (aa > ba) { ba = aa; best = poly; } }
  const lat0 = d3.geoCentroid({ type: "Polygon", coordinates: best })[1], k = Math.cos(lat0 * Math.PI / 180) || 1;
  const pl = polylabel(best.map(r => r.map(c => [c[0] * k, c[1]])), 0.05);
  let area = d3.geoArea(f); if (area > 2 * Math.PI) area = 4 * Math.PI - area;
  const ownerRaw = p.status === "independent" ? "" : (rawName[p.owner] || "");
  g.properties = { r: p.country_name, o: ownerRaw, st: p.status, a: dec(p.start), b: dec(p.end) + 1 / 366, g: p.gwcode,
    cap: p.capname ? [p.capname, +(+p.caplong).toFixed(2), +(+p.caplat).toFixed(2)] : null,
    lp: [+(pl[0] / k).toFixed(2), +pl[1].toFixed(2)], ar: Math.round(area * R * R), bl: +(ba * R * R).toFixed(0) };
  out.push({ i, ...g.properties, f });
});
fs.writeFileSync(__dirname + "/../atlas/maps/cs.json", JSON.stringify(T));
fs.writeFileSync(__dirname + "/../atlas/maps/csnames.json", JSON.stringify(JSON.parse(fs.readFileSync(__dirname + "/names.json"))));

// ---------- the change ledger ----------
const byG = {}; out.forEach(o => (byG[o.g] = byG[o.g] || []).push(o)); Object.values(byG).forEach(a => a.sort((x, y) => x.a - y.a));
const ST = { colony: "colony", protectorate: "protectorate", mandate: "mandate", occupied: "occupied territory", independent: "independent state", "N/A": "contested territory" };
const changes = [];
const art = w => (/^[aeiou]/.test(w) ? "an " : "a ") + w;
const activeAt = t => out.filter(o => o.a <= t && t < o.b);
const fmtD = t => { const y = Math.floor(t); const d = new Date(Date.UTC(y, 0, 1) + (t - y) * 365.25 * 864e5); return d.toISOString().slice(0, 10); };
const km = n => n >= 1e6 ? (n / 1e6).toFixed(1) + " million km²" : Math.round(n / 1000) * 1000 >= 1000 ? (Math.round(n / 1000) * 1000).toLocaleString("en-GB") + " km²" : n + " km²";
for (const o of out) {
  if (o.a <= 1886.001) continue;
  const prevs = (byG[o.g] || []).filter(x => x !== o && Math.abs(x.b - o.a) < 0.01);
  const name = display(o.r, o.o, o.a + 0.001);
  const own = n => display(n, "", o.a);
  let t = null, kind = "border";
  if (!prevs.length) {
    // new unit: from what?
    let before = activeAt(o.a - 0.003).filter(x => x !== o && d3.geoContains(x.f, o.lp)); if (!before.length) before = activeAt(o.a - 0.02).filter(x => x !== o && d3.geoContains(x.f, o.lp));
    const from = before.length ? display(before[0].r, before[0].o, o.a - 0.003) : null;
    if (o.st === "independent") { t = `${name} becomes independent${from && from !== name ? ` from ${from}` : ""}`; kind = "independence"; }
    else { t = `${name} appears as ${art(ST[o.st])}${o.o ? ` of ${own(o.o)}` : ""}${from && from !== name ? `, taken from ${from}` : ""}`; kind = "new"; }
  } else {
    const p = prevs.sort((x, y) => y.ar - x.ar)[0];
    const pname = display(p.r, p.o, p.b - 0.003);
    if (p.st !== "independent" && o.st === "independent") { t = `${name} becomes independent from ${own(p.o)}`; kind = "independence"; }
    else if (p.o !== o.o && o.st !== "independent") { t = `${name} passes from ${p.o ? own(p.o) : pname} to ${own(o.o)}${o.st !== p.st ? ` as ${art(ST[o.st])}` : ""}`; kind = "transfer"; }
    else if (p.st !== o.st) { t = `${pname}: ${ST[p.st]} becomes ${ST[o.st]}${o.o ? ` of ${own(o.o)}` : ""}`; kind = "status"; }
    else if (pname !== name && Math.abs(o.ar - p.ar) < 0.02 * p.ar) { t = `${pname} becomes ${name}`; kind = "rename"; }
    else {
      const dA = o.ar - p.ar; if (Math.abs(dA) < 5000 && Math.abs(dA) < 0.01 * p.ar) continue;
      t = `${name} ${dA > 0 ? "gains" : "loses"} about ${km(Math.abs(dA))}`; kind = "border";
    }
  }
  changes.push({ y: Math.floor(o.a), d: fmtD(o.a), t, k: kind, lon: o.lp[0], lat: o.lp[1], g: o.g, ar: o.ar, src: "cs" });
}
// ends without successor
for (const o of out) {
  if (o.b >= 2019.99) continue;
  const next = (byG[o.g] || []).filter(x => Math.abs(x.a - o.b) < 0.01); if (next.length) continue;
  const after = activeAt(o.b + 0.003).filter(x => d3.geoContains(x.f, o.lp));
  const nm = display(o.r, o.o, o.b - 0.003), to = after.length ? display(after[0].r, after[0].o, o.b + 0.003) : null;
  if (to === nm) continue;
  changes.push({ y: Math.floor(o.b), d: fmtD(o.b), t: to ? `${nm} ends; its land passes to ${to}` : `${nm} ends`, k: "end", lon: o.lp[0], lat: o.lp[1], g: o.g, ar: o.ar, src: "cs" });
}
// merge repeated border changes of one state in one year
const mg = {}; const merged = [];
for (const c of changes) { if (c.k !== "border") { merged.push(c); continue; } const k = c.y + "|" + c.g; if (!mg[k]) { mg[k] = { ...c, dA: 0, n: 0, nm: c.t.replace(/ (gains|loses) about .*/, "") }; merged.push(mg[k]); } const m = c.t.match(/(gains|loses) about ([\d.,]+)( million)?/); const v = parseFloat(m[2].replace(/,/g, "")) * (m[3] ? 1e6 : 1); mg[k].dA += m[1] === "gains" ? v : -v; mg[k].n++; }
for (const k in mg) { const c = mg[k]; if (Math.abs(c.dA) < 3000) { c.drop = 1; continue; } c.t = `${c.nm} ${c.dA > 0 ? "gains" : "loses"} about ${km(Math.abs(c.dA))}${c.n > 1 ? ` in ${c.n} changes` : ""}`; }
// pair a gain with an equal loss on the same day: one state took land from another
const B = merged.filter(c => !c.drop && c.k === "border" && c.n === 1);
for (const g of B) { if (g.dA <= 0 || g.paired) continue; const l = B.find(x => !x.paired && x !== g && x.d === g.d && x.dA < 0 && Math.abs(x.dA + g.dA) <= 0.05 * g.dA); if (l) { g.paired = l.paired = true; g.t = `${g.nm} takes about ${km(g.dA)} from ${l.nm}`; g.k = "transfer"; l.drop = 1; } }
changes.length = 0; merged.filter(c => !c.drop).forEach(c => { delete c.dA; delete c.n; delete c.nm; delete c.paired; changes.push(c); });
// de-duplicate same-text same-year
const seen = new Set(); const C = changes.filter(c => { const k = c.y + c.t; if (seen.has(k)) return false; seen.add(k); return true; }).sort((a, b) => a.d < b.d ? -1 : 1);
fs.writeFileSync(__dirname + "/cs_changes.json", JSON.stringify(C, null, 0));
console.log("features", out.length, "changes", C.length);
const by = {}; C.forEach(c => by[c.k] = (by[c.k] || 0) + 1); console.log(by);
for (const y of [1890, 1919, 1920, 1945, 1960, 1964, 1991]) console.log(y, C.filter(c => c.y === y).map(c => c.t).join(" | "));
