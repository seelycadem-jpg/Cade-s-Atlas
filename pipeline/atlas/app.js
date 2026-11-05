(async function(){
"use strict";
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s??"").replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const main=$("#main"), whereEl=$("#where");
const REDUCED=matchMedia("(prefers-reduced-motion: reduce)").matches;
const store={get(k,d){try{const v=localStorage.getItem(k);return v==null?d:JSON.parse(v)}catch(e){return d}},set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};

/* ---------- data ---------- */
let DATA,WORLD,RULES,GRAPH;
try{ [DATA,WORLD,RULES,GRAPH]=await Promise.all(["data.json","world.json","rules.json","graph.json"].map(u=>fetch(u).then(r=>{if(!r.ok)throw new Error(u);return r.json()}))); }
catch(e){ main.innerHTML='<p class="lede" style="padding-top:40px">The atlas data did not load. Reload the page.</p>'; return; }

const EV=DATA.events, byId=Object.fromEntries(EV.map(e=>[e.id,e]));
const fy=e=>e.y+(e.m?(e.m-1)/12:0);
EV.sort((a,b)=>fy(a)-fy(b));
const REG=Object.fromEntries(DATA.regions.map(r=>[r.id,r]));
const rname=e=>REG[e.r]?REG[e.r].short||REG[e.r].name:"";
const LINKS=GRAPH.links||[], LK=Object.fromEntries(LINKS.map(l=>[l.id,l]));
const inLinks=id=>((GRAPH.ev[id]||{}).in||[]).map(k=>LK[k]).filter(Boolean);
const outLinks=id=>((GRAPH.ev[id]||{}).out||[]).map(k=>LK[k]).filter(Boolean);
const linkBetween=(a,b)=>LINKS.find(l=>l.f===a&&l.t===b);
function arrowBetween(a,b){ const d=linkBetween(a,b); if(d) return {link:d,grade:d.grade,via:null}; for(const l of outLinks(a)){ const h=linkBetween(l.t,b); if(h) return {link:l,grade:l.grade,via:l.t}; } return {link:null,grade:"none",via:null}; }
const GRADES=["Necessary","Sufficient","Contributing","Contested","Coincident"];
const GRADEHELP={Necessary:"take it away and the effect does not happen",Sufficient:"on its own it was enough",Contributing:"it raised the odds, among other causes",Contested:"serious schools disagree",Coincident:"it came before and did not cause"};

/* stories: graded ones from the graph, then the older ungraded ones */
const STORIES=[];
for(const S of GRAPH.stories||[]) STORIES.push(Object.assign({},S,{graded:true,kind:S.size||"arc"}));
for(const A of DATA.arcs||[]){
  if(STORIES.some(s=>s.id===A.id)) continue;
  const chapters=A.chapters.map((c,i)=>{ const items=A.items.filter(it=>it.chap===i).map(it=>byId[it.id]).filter(Boolean).sort((a,b)=>fy(a)-fy(b)); if(!items.length) return null; const h=items.find(e=>e.tier===1)||items[0]; return {id:"c"+(i+1),title:c.t,hinge:h.id,conn:null,s1:c.d,s2:"",support:items.filter(e=>e!==h).map(e=>e.id)}; }).filter(Boolean);
  if(!chapters.length) continue;
  STORIES.push({id:A.id,title:A.title,sub:A.short&&A.short!==A.title?A.short:"",span:A.span,kind:"story",graded:false,thesis:A.summary,chapters,themes:null,shelf:[],sources:A.sources||[]});
}
const SB=Object.fromEntries(STORIES.map(s=>[s.id,s]));
const MEM={}; STORIES.forEach(S=>S.chapters.forEach((c,i)=>{ (MEM[c.hinge]=MEM[c.hinge]||[]).push({story:S.id,chapter:i,role:"knot"}); (c.support||[]).forEach(s=>{ if(byId[s]) (MEM[s]=MEM[s]||[]).push({story:S.id,chapter:i,role:"strand"}); }); }));
const THEMES=GRAPH.themes||[], TB=Object.fromEntries(THEMES.map(t=>[t.id,t]));
const storiesOfTheme=id=>STORIES.filter(s=>s.themes&&(s.themes.primary===id||(s.themes.secondary||[]).includes(id)));
const threadLines=(S,opts={})=>{ const hs=S.chapters.map(c=>byId[c.hinge]).filter(e=>e&&e.lat!=null); const out=[]; for(let i=0;i<hs.length-1;i++){ out.push(Object.assign({coords:[[+hs[i].lon,+hs[i].lat],[+hs[i+1].lon,+hs[i+1].lat]],grade:S.graded?arrowBetween(hs[i].id,hs[i+1].id).grade:"none"},opts)); } return out; };
const CATS={political:"Political",war:"War",economic:"Economic",ideas:"Ideas",religion:"Religion",science:"Science and technology",culture:"Culture"};
const THREADS=DATA.threads||{};
const tagName=id=>CATS[id]||THREADS[id]||id;
const tagsOf=e=>[...(e.c||[]).map(c=>({id:c,kind:"cat"})),...(e.t||[]).map(t=>({id:t,kind:"thread"}))].filter(x=>CATS[x.id]||THREADS[x.id]);
const chips=e=>{ const seen=new Set(), ts=tagsOf(e).filter(t=>{ const n=tagName(t.id).toLowerCase(); if(seen.has(n)) return false; seen.add(n); return true; }); return ts.length?`<div class="chips">${ts.map(t=>`<a class="chip ${t.kind}" href="#tag-${t.id}">${esc(tagName(t.id))}</a>`).join("")}</div>`:""; };
const hasTag=(e,id)=>!id||(e.c||[]).includes(id)||(e.t||[]).includes(id);
const evLink=e=>`<a href="#event-${e.id}">${esc(e.h)}</a>`;
const yr=e=>e.y;


/* ---------- sound: synthesised, no files ---------- */
const SND={on:store.get("ma-sound",true),ctx:null,last:0,
  ac(){ if(!this.ctx){ try{ this.ctx=new (window.AudioContext||window.webkitAudioContext)(); }catch(e){ this.ctx=null; } } if(this.ctx&&this.ctx.state==="suspended") this.ctx.resume(); return this.ctx; },
  noise(len){ const c=this.ac(); if(!c) return null; const b=c.createBuffer(1,Math.floor(c.sampleRate*len),c.sampleRate), d=b.getChannelData(0); for(let i=0;i<d.length;i++) d[i]=(Math.random()*2-1)*(1-i/d.length); return b; },
  tick(){ if(!this.on) return; const c=this.ac(); if(!c) return; const t=c.currentTime; const s=c.createBufferSource(); s.buffer=this.noise(.035); const f=c.createBiquadFilter(); f.type="bandpass"; f.frequency.value=2600; f.Q.value=.9; const g=c.createGain(); g.gain.setValueAtTime(.18,t); g.gain.exponentialRampToValueAtTime(.001,t+.05); s.connect(f).connect(g).connect(c.destination); s.start(t); const o=c.createOscillator(); o.type="sine"; o.frequency.setValueAtTime(1800,t); o.frequency.exponentialRampToValueAtTime(900,t+.03); const g2=c.createGain(); g2.gain.setValueAtTime(.05,t); g2.gain.exponentialRampToValueAtTime(.001,t+.04); o.connect(g2).connect(c.destination); o.start(t); o.stop(t+.05); },
  page(){ if(!this.on) return; const c=this.ac(); if(!c) return; const t=c.currentTime; const s=c.createBufferSource(); s.buffer=this.noise(.18); const f=c.createBiquadFilter(); f.type="lowpass"; f.frequency.setValueAtTime(1800,t); f.frequency.exponentialRampToValueAtTime(300,t+.18); const g=c.createGain(); g.gain.setValueAtTime(.16,t); g.gain.exponentialRampToValueAtTime(.001,t+.2); s.connect(f).connect(g).connect(c.destination); s.start(t); },
  step(){ if(!this.on) return; const now=performance.now(); if(now-this.last<45) return; this.last=now; const c=this.ac(); if(!c) return; const t=c.currentTime; const o=c.createOscillator(); o.type="triangle"; o.frequency.value=1400; const g=c.createGain(); g.gain.setValueAtTime(.035,t); g.gain.exponentialRampToValueAtTime(.001,t+.025); o.connect(g).connect(c.destination); o.start(t); o.stop(t+.03); },
  bead(){ if(!this.on) return; const c=this.ac(); if(!c) return; const t=c.currentTime; [660,990].forEach((hz,i)=>{ const o=c.createOscillator(); o.type="sine"; o.frequency.value=hz; const g=c.createGain(); g.gain.setValueAtTime(0,t+i*.06); g.gain.linearRampToValueAtTime(.06,t+i*.06+.01); g.gain.exponentialRampToValueAtTime(.001,t+i*.06+.25); o.connect(g).connect(c.destination); o.start(t+i*.06); o.stop(t+i*.06+.3); }); }
};
document.addEventListener("click",e=>{ const b=e.target.closest("button, .seg button, .results a, .arcs a, .themes a, .lk a, .century a, .periods button"); if(b&&!b.classList.contains("snd")) SND.tick(); },true);
document.addEventListener("input",e=>{ if(e.target&&e.target.type==="range") SND.step(); },true);

/* ---------- running head ---------- */
function where(parts){ whereEl.innerHTML=parts.map((p,i)=>{ const last=i===parts.length-1; const t=last?`<span class="now">${esc(p[0])}</span>`:`<a href="${p[1]}">${esc(p[0])}</a>`; return (i?'<span class="sep">›</span>':'')+t; }).join(""); const h=(location.hash||"#atlas").slice(1); const sec=/^(story|event|atlas|meanwhile)/.test(h)||!h?"#atlas":/^theme/.test(h)?"#themes":/^knots/.test(h)?"#knots":/^timeline/.test(h)?"#timeline":/^about/.test(h)?"#about":"#atlas"; $$("#nav a").forEach(a=>{ if(a.getAttribute("href")===sec) a.setAttribute("aria-current","page"); else a.removeAttribute("aria-current"); }); }

/* ---------- maps and the globe ---------- */
/*GLOBE*/
let POLS=[]; try{ const pj=await (await fetch("polities.json")).json(); POLS=pj.polities; }catch(e){ POLS=(RULES.polities||[]).map(p=>Object.assign({key:p.t,gov:p.k},p)); } POLS.forEach(p=>{ p.re=new RegExp(p.rx,"i"); if(!p.key) p.key=p.t; });
const EMP=RULES.empires||{}; for(const k in EMP){ EMP[k].re=new RegExp(EMP[k].rx,"i"); EMP[k].he=EMP[k].home?new RegExp(EMP[k].home,"i"):null; }
(RULES.colonial||[]).forEach(c=>c.re=new RegExp(c.rx,"i")); (RULES.rename||[]).forEach(r=>r.re=new RegExp(r.rx,"i")); (RULES.polities||[]).forEach(p=>p.re=new RegExp(p.rx,"i"));
function empireOf(f,y){ const n=f.properties.NAME||"", s=f.properties.SUBJECTO||""; for(const c of RULES.colonial||[]) if(y>=c.a&&y<c.b&&c.re.test(n)) return {k:c.emp,label:c.name}; for(const r of RULES.rename||[]) if(r.ys.includes(mapYear(y))&&r.re.test(n)) return {k:r.emp,label:r.name}; for(const k in EMP) if(EMP[k].re.test(n)) return {k,label:EMP[k].name}; if(s) for(const k in EMP) if(EMP[k].re.test(s)) return {k,label:EMP[k].name}; return null; }
const css=()=>getComputedStyle(document.documentElement);
const isDark=()=>document.documentElement.dataset.theme==="dark"||(document.documentElement.dataset.theme!=="light"&&matchMedia("(prefers-color-scheme: dark)").matches);
const tintCache={};
function tint(hex,mode){ const key=hex+(isDark()?"d":"l")+(mode||""); if(tintCache[key]) return tintCache[key]; const c=d3.hsl(hex); const sat={soft:.45,colony:.72,home:.7}[mode]||.6, L=isDark()?({soft:.28,colony:.35,home:.4}[mode]||.33):({soft:.85,colony:.765,home:.72}[mode]||.8); /* a dependency is a lighter shade of its ruler, still clearly coloured */ c.s=Math.min(c.s,.55)*sat; c.l=L; /* sand and ochre hues sit too close to the cream land: give them more depth so a state never reads as empty land */ if(!isDark()&&c.h>=22&&c.h<=72&&mode!=="soft"){ c.s=Math.min(.55,c.s*1.45); c.l=L-.07; } return tintCache[key]=c.formatHex(); }
const CLS={monarchy:{name:"Monarchy",color:"#C9A227"},republic:{name:"Republic or democracy",color:"#2E6B63"},autocracy:{name:"One-party or military rule",color:"#B0302A"},colony:{name:"Colony or dependency",color:"#4E78B0"},theocracy:{name:"Theocracy",color:"#6F4BA3"},stateless:{name:"Peoples without a state",color:"#7A7A7A"},other:{name:"In transition",color:"#9FB3C2"}};

const BLOCS=[
 {a:1914,b:1918,t:"The First World War",cls:{entente:{name:"Entente and allies",color:"#2F5FB3"},central:{name:"Central Powers",color:"#B0302A"},neutral:{name:"Neutral",color:"#9A9A9A"}},
  rx:{entente:/^(united kingdom|france|russia|italy|empire of japan|japan|serbia|belgium|montenegro|romania|portugal|greece|united states|brazil|china|siam|liberia|cuba|panama|canada|australia|new zealand|union of south africa|south africa|british india|newfoundland)/i,central:/^(german|austro|austria|ottoman|bulgaria)/i},dflt:"neutral"},
 {a:1939,b:1945,t:"The Second World War",cls:{allies:{name:"Allies",color:"#2F5FB3"},axis:{name:"Axis and co-belligerents",color:"#B0302A"},neutral:{name:"Neutral",color:"#9A9A9A"}},
  rx:{axis:/^(germany|italy|empire of japan|japan|hungary|romania|bulgaria|finland|slovakia|croatia|siam|thailand|manchukuo|italian|albania)/i,allies:/^(united kingdom|france|ussr|soviet|united states|china|poland|czechoslovakia|yugoslavia|greece|norway|denmark|netherlands|belgium|luxembourg|canada|australia|new zealand|union of south africa|south africa|british india|india|brazil|mexico|ethiopia|egypt|iraq|iran|philippines|cuba|colombia|peru|chile|bolivia|ecuador|venezuela|uruguay|paraguay|guatemala|honduras|el salvador|nicaragua|costa rica|panama|dominican|haiti|liberia|saudi|turkey|newfoundland|mongolia|tuva)/i},dflt:"neutral"},
 {a:1947,b:1991,t:"The Cold War",cls:{west:{name:"Western alliance and US-aligned",color:"#2F5FB3"},soviet:{name:"Soviet bloc and allies",color:"#B0302A"},redother:{name:"Communist, outside Moscow's bloc",color:"#D4751A"},nonaligned:{name:"Non-aligned and others",color:"#C9A227"}},
  rx:{soviet:/^(ussr|soviet|poland|east germany|germany, soviet|czechoslovakia|hungary|romania|bulgaria|mongolia|north korea|korea, soviet|vietnam|laos|cuba|afghanistan|ethiopia|angola|mozambique|south yemen|yemen \(aden|benin|congo$|congo \(brazzaville|nicaragua|syria|iraq|libya|grenada)/i,redother:/^(china|albania|yugoslavia|cambodia|kampuchea)/i,west:/^(united states|united kingdom|france|west germany|germany, (american|british|french)|italy|canada|belgium|netherlands|luxembourg|denmark|norway|iceland|portugal|greece|turkey|spain|japan|south korea|korea, us|taiwan|philippines|thailand|australia|new zealand|pakistan|iran|israel|saudi|kuwait|qatar|bahrain|united arab|trucial|oman|muscat|jordan|south africa|zaire|congo \(kinshasa|kenya|ivory coast|morocco|tunisia|liberia|malaysia|malaya|singapore|argentina|brazil|chile|colombia|venezuela|peru|bolivia|ecuador|paraguay|uruguay|mexico|guatemala|honduras|el salvador|costa rica|panama|dominican|haiti|jamaica|trinidad|puerto rico|hawaii|japan \(allied|ryukyu|south vietnam|indonesia|cameroon|senegal|gabon|togo|niger$|chad|central african|rhodesia)/i},dflt:"nonaligned"},
 {a:1992,b:2025,t:"After the Cold War",cls:{west:{name:"NATO, EU and US allies",color:"#2F5FB3"},russia:{name:"Russia-aligned",color:"#B0302A"},china:{name:"China-aligned",color:"#D4751A"},other:{name:"Others",color:"#9A9A9A"}},
  rx:{russia:/^(russia|belarus|byelarus|armenia|kazakhstan|kyrgyzstan|tajikistan|syria|venezuela|cuba|nicaragua|north korea|iran|eritrea|mali|burkina|niger$|central african|tajikistan|uzbekistan|turkmenistan|serbia)/i,china:/^(china|cambodia|laos|pakistan|myanmar|burma|djibouti)/i,west:/^(united states|united kingdom|france|germany|italy|canada|belgium|netherlands|luxembourg|denmark|norway|iceland|portugal|greece|turkey|spain|poland|czech|slovakia|hungary|romania|bulgaria|estonia|latvia|lithuania|slovenia|croatia|albania|montenegro|north macedonia|macedonia|finland|sweden|austria|ireland|cyprus|malta|japan|south korea|taiwan|australia|new zealand|israel|saudi|kuwait|qatar|bahrain|united arab|oman|jordan|egypt|morocco|tunisia|philippines|singapore|thailand|ukraine|georgia|moldova|colombia|chile|argentina|mexico|brazil|peru|panama|costa rica|dominican|guatemala|honduras|el salvador|paraguay|uruguay|ecuador|india|indonesia|vietnam|malaysia|kenya|nigeria|ghana|senegal|ivory coast|south africa|iraq|bosnia|kosovo|greenland|puerto rico|guam|hong kong)/i},dflt:"other"}];
function blocTable(y){ return BLOCS.find(b=>y>=b.a&&y<=b.b)||null; }
function blocOf(f,y){ const B=blocTable(y); if(!B) return null; const n=f.properties.NAME||"", s=f.properties.SUBJECTO||""; const test=name=>{ for(const k in B.rx) if(B.rx[k].test(name)) return k; return null; }; let k=test(n); if(!k&&s) k=test(s); if(!k){ const e=empireOf(f,y); if(e&&EMP[e.k]) k=test(EMP[e.k].name)||test(EMP[e.k].name.replace(/ empire$/i,"")); } return k||B.dflt; }

let COLORBY=store.get("ma-colorby","empire");
function classOf(f,y){ const n=f.properties.NAME||"", s=f.properties.SUBJECTO||""; const p=POLS.find(p=>p.re.test(n)&&y>=p.a&&y<=p.b); if(p) return p.cls||"other"; if(s&&s!==n&&empireOf(f,y)) return "colony"; if(PEOPLE_RX.test(n)) return "stateless"; return null; }


/* ---------- charts ---------- */
const fmtN=v=>v>=1e9?(v/1e9).toFixed(1).replace(/\.0$/,"")+" bn":v>=1e6?(v/1e6).toFixed(v<1e7?1:0)+" m":v>=1e4?Math.round(v/1e3)+",000":v>=1000?Math.round(v).toLocaleString("en-US"):String(Math.round(v*10)/10);
function lineChart(F,o={}){ const w=o.w||640, h=o.h||220, ml=o.ml||46, mr=14, mt=F.unit?30:16, mb=26, kind=o.kind||(F.log?"step":"line"); const S=F.series; const xs=S.map(d=>d[0]), ys=S.map(d=>d[1]);
  const x=d3.scaleLinear().domain([o.x0!=null?o.x0:d3.min(xs),o.x1!=null?o.x1:d3.max(xs)]).range([ml,w-mr]);
  const y=(F.log?d3.scaleLog().domain([Math.max(.6,d3.min(ys)*.55),d3.max(ys)*1.4]):d3.scaleLinear().domain([0,d3.max(ys)*1.08])).range([h-mb,mt]);
  const line=d3.line().x(d=>x(d[0])).y(d=>y(d[1])).curve(kind==="step"?d3.curveStepAfter:d3.curveMonotoneX);
  const yt=F.log?[1,10,100,1000].filter(v=>v>=y.domain()[0]&&v<=y.domain()[1]):y.ticks(3); const xt=x.ticks(Math.min(8,Math.round((w-ml)/90)));
  const valAt=yr=>{ if(kind==="step"){ let v=S[0][1]; for(const d of S) if(d[0]<=yr) v=d[1]; return v; } const i=d3.bisector(d=>d[0]).left(S,yr); if(i<=0) return S[0][1]; if(i>=S.length) return S[S.length-1][1]; const a=S[i-1], b=S[i]; return a[1]+(b[1]-a[1])*(yr-a[0])/(b[0]-a[0]); };
  const knots=(o.knots||[]).filter(k=>k.y>=x.domain()[0]&&k.y<=x.domain()[1]);
  const id="ch"+Math.random().toString(36).slice(2,7);
  const svg=`<svg class="chart" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" data-id="${id}" role="img" aria-label="${esc(F.t)}">
   ${yt.map(v=>`<g><line class="grid" x1="${ml}" x2="${w-mr}" y1="${y(v)}" y2="${y(v)}"/><text class="ax" x="${ml-6}" y="${y(v)+4}" text-anchor="end">${fmtN(v)}</text></g>`).join("")}
   ${xt.map(v=>`<text class="ax" x="${x(v)}" y="${h-8}" text-anchor="middle">${v}</text>`).join("")}
   <line class="base" x1="${ml}" x2="${w-mr}" y1="${h-mb}" y2="${h-mb}"/>
   <path class="ln" d="${line(S)}"/>
   ${kind==="step"?S.filter((d,i)=>i===0||d[1]!==S[i-1][1]).map(d=>`<text class="vl" x="${x(d[0])+5}" y="${y(d[1])-7}">${fmtN(d[1])}</text>`).join(""):""}
   ${F.unit?`<text class="ax" x="${ml}" y="12">${esc(F.unit)}${F.log?", log scale":""}</text>`:""}
   ${o.cursor!=null?`<line class="cur" x1="${x(o.cursor)}" x2="${x(o.cursor)}" y1="${mt}" y2="${h-mb}"/><circle class="curdot" cx="${x(o.cursor)}" cy="${y(valAt(o.cursor))}" r="4.5"/><text class="curv" x="${x(o.cursor)+(x(o.cursor)>w*.7?-8:8)}" y="${Math.max(mt+10,y(valAt(o.cursor))-10)}" text-anchor="${x(o.cursor)>w*.7?"end":"start"}">${fmtN(valAt(o.cursor))}${F.unit?" "+esc(F.unit):""}</text>`:""}
   ${(()=>{ let px=-99, lift=0; return knots.map(k=>{ const kx=x(k.y), ky=y(valAt(k.y)); lift=kx-px<18?lift+12:0; px=kx; return `<a href="#event-${k.id}"><circle class="kn" cx="${kx}" cy="${ky}" r="4"/><title>Knot ${k.n}, ${esc(k.t)}, ${k.y}</title></a>`; }).join(""); })()}
   <g class="hov" hidden><line y1="${mt}" y2="${h-mb}"/><circle r="4"/><rect rx="2" height="22"/><text/></g>
   <rect class="hit" x="${ml}" y="${mt}" width="${w-ml-mr}" height="${h-mt-mb}" fill="none" pointer-events="all"/></svg>`;
  const html=`<figure class="fig"><figcaption><b>${esc(F.t)}</b>${F.sub?`<span>${esc(F.sub)}</span>`:""}</figcaption><div class="chartwrap">${svg}</div>${F.note?`<p class="fn">${esc(F.note)}</p>`:""}</figure>`;
  CHARTS[id]={x,y,valAt,unit:F.unit||"",w,h,mt,mb,ml,mr,kind,S}; return html; }
const CHARTS={};
document.addEventListener("pointermove",e=>{ const svg=e.target.closest&&e.target.closest("svg.chart"); if(!svg) return; const C=CHARTS[svg.dataset.id]; if(!C) return; const pt=svg.createSVGPoint(); pt.x=e.clientX; pt.y=e.clientY; const p=pt.matrixTransform(svg.getScreenCTM().inverse()); const g=svg.querySelector(".hov"); if(p.x<C.ml||p.x>C.w-C.mr){ g.hidden=true; return; } const yr=Math.round(C.x.invert(p.x)), v=C.valAt(yr), yy=C.y(v); g.hidden=false; g.querySelector("line").setAttribute("x1",p.x); g.querySelector("line").setAttribute("x2",p.x); const c=g.querySelector("circle"); c.setAttribute("cx",p.x); c.setAttribute("cy",yy); const t=g.querySelector("text"); t.textContent=`${yr}: ${fmtN(v)}${C.unit?" "+C.unit:""}`; const tw=t.textContent.length*6.6+12, left=p.x+tw>C.w-C.mr?p.x-tw-8:p.x+8; t.setAttribute("x",left+6); t.setAttribute("y",C.mt+15); const r=g.querySelector("rect"); r.setAttribute("x",left); r.setAttribute("y",C.mt); r.setAttribute("width",tw); });
document.addEventListener("pointerleave",e=>{ if(e.target&&e.target.matches&&e.target.matches("svg.chart")){ const g=e.target.querySelector(".hov"); if(g) g.hidden=true; } },true);
function barsH(rows,o={}){ const max=d3.max(rows,r=>r[1]); return `<div class="bars">${rows.map(r=>`<div class="br"><span class="bl">${esc(r[0])}</span><span class="bb"><i style="width:${(r[1]/max*100).toFixed(1)}%"></i></span><span class="bv">${o.fmt?o.fmt(r[1]):fmtN(r[1])}${o.unit||""}</span></div>`).join("")}</div>`; }
const POP=()=>({t:"World population",unit:"people",series:WORLD.snaps.map(s=>[s.y,s.pop*1e6])});

/* ---------- shared pieces ---------- */
function meanwhile(e,n=5){ const f=fy(e); return EV.filter(x=>x!==e&&x.tier<=2&&x.r!==e.r&&Math.abs(fy(x)-f)<=3).sort((a,b)=>(a.tier-b.tier)||(Math.abs(fy(a)-f)-Math.abs(fy(b)-f))).slice(0,n); }
function meanHTML(e){ const m=meanwhile(e); if(!m.length) return ""; return `<h4>Meanwhile, elsewhere</h4>`+m.map(x=>`<div class="mi"><span class="yr">${x.y}</span><a href="#event-${x.id}">${esc(x.h)}</a><span class="rel">${esc(rname(x))}${x.hook?". "+esc(x.hook):""}</span></div>`).join("")+`<p class="mnote">Within three years of ${fmtY(e.y)}, outside ${esc(rname(e))}.</p>`; }
const gradeTag=(g,label)=>`<span class="g ${g}"><i></i>${esc(label||(g==="none"?"ungraded":g))}</span>`;
function noteHTML(l,full=true){ const n=l.note||{}; const via=l._via?`<span>through ${esc(byId[l._via]?byId[l._via].h:l._via)}</span>`:""; return `<div class="note ${l.grade}"><div class="nh">${gradeTag(l.grade)}<span>${esc(l.type)}</span><span>${esc(l.conf)} confidence</span>${via}</div><p><em>Claim</em>${esc(n.claim)}</p>${full?`<p><em>Objection</em>${esc(n.objection)}</p><p><em>Warrant</em>${esc(n.warrant)}</p><p><em>Verdict</em>${esc(n.verdict)}</p>${l.tests?`<div class="meta">Hoop test: ${esc(l.tests.hoop)}. Smoking gun: ${esc(l.tests.gun)}.</div>`:""}${l.audit?`<div class="meta">Graded by <b>${esc(l.audit.by)}</b>, red team ${esc(l.audit.red)}, ${esc(l.audit.date)}.</div>`:""}`:""}</div>`; }
function figsHTML(e){ const f=e.figs; if(!f) return ""; let h=""; if(f.kv&&f.kv.length) h+=`<div class="numbers">${f.kv.map(([v,l])=>`<div><b>${esc(v)}</b><span>${esc(l)}</span></div>`).join("")}</div>`; if(f.toll&&f.toll.s&&f.toll.s.length){ const max=Math.max(...f.toll.s.map(r=>r[2]||r[1])); const fmt=n=>n>=1e6?(n/1e6).toFixed(n%1e6?1:0)+" m":n>=1e3?Math.round(n/1e3)+",000":String(n); h+=`<div class="toll"><h4>${esc(f.toll.t)}</h4>${f.toll.s.map(([n,lo,hi])=>`<div class="trow"><span>${esc(n)}</span><div class="bar">${hi?`<i class="rng" style="width:${hi/max*100}%"></i>`:""}<i style="width:${lo/max*100}%"></i></div><span class="v">${fmt(lo)}${hi?" to "+fmt(hi):""}</span></div>`).join("")}${f.toll.n?`<p class="nt">${esc(f.toll.n)}</p>`:""}</div>`; } return h; }
function searchIndex(){ return EV.map(e=>({e,s:[e.h,e.who,e.where,e.wk,String(e.y)].filter(Boolean).join(" ").toLowerCase()})); }
let IDX=null;
function search(q){ q=q.trim().toLowerCase(); if(q.length<2) return []; IDX=IDX||searchIndex(); const ws=q.split(/\s+/); return IDX.filter(x=>ws.every(w=>x.s.includes(w))).sort((a,b)=>(a.e.h.toLowerCase().startsWith(q)?-1:0)-(b.e.h.toLowerCase().startsWith(q)?-1:0)||a.e.tier-b.e.tier).slice(0,12).map(x=>x.e); }
const sInput=$("#q"), sRes=$("#results");
const sndBtn=$("#snd"); const sndUI=()=>{ sndBtn.setAttribute("aria-pressed",SND.on); sndBtn.textContent=SND.on?"sound on":"sound off"; }; sndBtn.onclick=()=>{ SND.on=!SND.on; store.set("ma-sound",SND.on); sndUI(); if(SND.on) SND.tick(); }; sndUI();
sInput.addEventListener("input",()=>{ const r=search(sInput.value); if(!sInput.value.trim()){ sRes.hidden=true; return; } sRes.hidden=false; sRes.innerHTML=r.length?r.map(e=>`<a href="#event-${e.id}"><span class="yr">${fmtY(e.y)}</span><span>${esc(e.h)}</span><span class="rg">${esc(rname(e))}</span></a>`).join(""):`<div class="none">Nothing matches. Try a person, a place or a year.</div>`; });
sInput.addEventListener("keydown",e=>{ if(e.key==="Enter"){ const a=$("a",sRes); if(a){ location.hash=a.getAttribute("href"); sRes.hidden=true; sInput.value=""; } } if(e.key==="Escape"){ sRes.hidden=true; } });
document.addEventListener("click",e=>{ if(!e.target.closest(".search")) sRes.hidden=true; if(e.target.closest("#results a")){ sRes.hidden=true; sInput.value=""; } });

/* ---------- page: atlas ---------- */
let page={destroy(){}};
/* ---------- years before the common era, the time grid and the ages ---------- */
const fmtY=y=>y<0?`${-y} BCE`:y<1000?`${y} CE`:`${y}`;
const gridStep=y=>y<-753?25:y<1400?10:1;
const snapY=y=>{ y=Math.round(y); if(y<-753){ const s=-3400+25*Math.round((y+3400)/25); return Math.min(s,-775); } if(y<-745) return -753; if(y<1400){ const s=10*Math.round(y/10); return s===0?(y<0?-10:1):s; } return y; };
const YSEG=[[-3400,-753,0,220],[-753,1400,220,500],[1400,2025,500,1000]];
const yPos=y=>{ for(const [a,b,p,q] of YSEG) if(y<=b) return Math.round(p+(Math.max(y,a)-a)/(b-a)*(q-p)); return 1000; };
const posY=v=>{ for(const [a,b,p,q] of YSEG) if(v<=q) return snapY(a+(v-p)/(q-p)*(b-a)); return 2025; };
const AGES=[
 {a:-3400,b:-1200,n:"Bronze Age",d:"Cities, writing and kings: the first states rise on the floodplains of the Tigris and Euphrates, the Nile, the Indus and the Yellow River."},
 {a:-1200,b:-500,n:"Iron Age",d:"The Bronze Age palace states collapse around 1200 BCE; iron arms larger armies, and the first territorial empires, Assyria and then Persia, rule several river worlds at once."},
 {a:-500,b:500,n:"Classical Age",d:"Empires span whole regions (Persia, Rome, Han China, the Mauryas), and the philosophies and religions that still order much of the world take shape."},
 {a:500,b:1450,n:"Post-classical Age",d:"Universal religions organise politics from Spain to Japan; Islam spreads from Arabia; steppe peoples, the Mongols above all, bind Eurasia's trade routes together."},
 {a:1450,b:1650,n:"Age of Exploration",d:"Ocean navigation links every inhabited continent; Iberian empires conquer the Americas and gunpowder empires consolidate Asia."},
 {a:1650,b:1760,n:"Early Modern Age",d:"Sovereign states, standing armies and chartered trading companies; science and the Enlightenment recast how rulers justify power."},
 {a:1760,b:1914,n:"Industrial Age",d:"Steam, coal and rail multiply output; revolutions remake governments, nations form, and Europe colonises most of Africa and Asia."},
 {a:1914,b:1945,n:"Age of World Wars",d:"Two world wars and a depression break the European empires and the liberal order of the nineteenth century."},
 {a:1945,b:1991,n:"Atomic Age",d:"Nuclear weapons, decolonisation and the Cold War between the United States and the Soviet Union."},
 {a:1991,b:2100,n:"Digital Age",d:"The internet and global markets bind the world into one network; economic weight shifts toward Asia."}];
const ageOf=y=>AGES.find(A=>y>=A.a&&y<A.b)||AGES[AGES.length-1];
function atlasPage(){
  where([["Atlas","#atlas"]]);
  const YMIN=-3400, YMAX=2025; let flat=store.get("ma-flat",false), year=store.get("ma-year",1914), win=store.get("ma-win",5), by=store.get("ma-mby","region"), showAll=store.get("ma-tall",false), sel=null, tag=store.get("ma-tag","");
  main.innerHTML=`<section class="front2">
    <div class="yearrow"><div class="year"><div class="yv"><b id="yv">${fmtY(year)}</b><span class="age" id="age"></span></div><div class="yslide"><input type="range" id="yr" min="0" max="1000" value="${yPos(year)}" aria-label="Year" aria-valuetext="${fmtY(year)}"><div class="ages" aria-hidden="true">${AGES.map((A,i)=>`<span class="ag${i%2}" style="left:${yPos(A.a)/10}%;width:${(yPos(Math.min(A.b,2025))-yPos(A.a))/10}%" title="${esc(A.n)}"></span>`).join("")}</div><div class="ticks" aria-hidden="true">${[[-3000,1],[-1500,0],[1,1],[1000,0],[1500,1],[1800,0],[1900,0],[2000,1]].map(([t,k])=>`<span class="${k?"k":""}" style="left:${yPos(t)/10}%${yPos(t)<60?";transform:none":""}">${t<0?-t+" BCE":t===1?"1 CE":t}</span>`).join("")}</div></div><span class="cap">everything on this page follows the year</span></div>
     <div class="ctl"><div class="cg"><span class="l">Colour the map</span><div class="seg small"><button data-c="empire" aria-pressed="${COLORBY==="empire"}">By country</button><button data-c="gov" aria-pressed="${COLORBY==="gov"}">By form of government</button><button data-c="bloc" aria-pressed="${COLORBY==="bloc"}">By alliance</button></div><span class="hint" id="chint"></span></div>
     <div class="cg"><span class="l">Span</span><div class="seg small">${[3,5,10].map(w=>`<button data-w="${w}" aria-pressed="${w===win}">± ${w} years</button>`).join("")}</div><span class="hint">events this close to the year are shown on the globe and listed by region</span><label class="hint">only <select id="tagsel"><option value="">all events</option><optgroup label="Categories">${Object.entries(CATS).map(([k,v])=>`<option value="${k}"${k===tag?" selected":""}>${esc(v)}</option>`).join("")}</optgroup><optgroup label="Threads">${Object.entries(THREADS).map(([k,v])=>`<option value="${k}"${k===tag?" selected":""}>${esc(v)}</option>`).join("")}</optgroup></select></label></div>
     <div class="cg"><span class="l">Arcs in motion</span><div class="seg small"><button data-b="region" aria-pressed="${by==="region"}">By region</button><button data-b="theme" aria-pressed="${by==="theme"}">By theme</button></div><label class="hint"><input type="checkbox" id="tall"${showAll?" checked":""}> include fibres, the smallest events</label></div></div></div>
    <div class="fgrid${flat?" wide":""}">
     <div class="gcol"><div class="gbar"><div class="seg small" role="group" aria-label="Projection"><button data-p="globe" aria-pressed="${!flat}">Globe</button><button data-p="flat" aria-pressed="${flat}">Flat map</button></div><button class="btn soft play" id="play" aria-pressed="false">Play the years</button><select id="pspeed" aria-label="Playback speed"><option value="1">1 year a step</option><option value="5">5 years a step</option><option value="25">25 years a step</option></select><label class="cmp"><input type="checkbox" id="phys"${SHOWPHYS?" checked":""}> Relief, rivers and seas</label><label class="cmp">Compare with <select id="cmp"><option value="">no other year</option>${[-2500,-1200,-500,1,500,1000,1250,1500,1600,1700,1789,1815,1870,1885,1900,1914,1920,1938,1945,1960,1990,2010].map(y=>`<option value="${y}">${fmtY(y)}</option>`).join("")}</select></label></div><div class="chartbox" id="chart" aria-label="Map of the world with the borders of the chosen year"><div class="zoom"><button id="zi" aria-label="Zoom in">+</button><button id="zo" aria-label="Zoom out">−</button><button id="zr" aria-label="Whole world" title="Whole world">○</button></div><div class="tip" id="tip" hidden></div><svg class="rose" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="3"/><path class="n" d="M32 6 L36 30 L32 26 L28 30 Z"/><path d="M32 58 L36 34 L32 38 L28 34 Z M6 32 L30 28 L26 32 L30 36 Z M58 32 L34 28 L38 32 L34 36 Z"/><text x="32" y="4" text-anchor="middle">N</text></svg></div><div class="legend" id="legend"></div><p class="small quiet" style="margin-top:8px">Drag to turn, scroll or pinch to zoom: names, capitals and cities appear as you come closer. Click a country for its state in this year, or an event for its brief.</p><div class="evcard" id="evcard" hidden></div><div class="ledger2" id="ledger"></div></div>
     <div class="pcol"><div id="place" hidden></div><div id="worldcard"></div></div>
    </div>
    <div class="csmain"><h3 id="mh"></h3><div id="motion"></div><h3 id="rh"></h3><div class="regions" id="regions"></div></div>
    <div class="doors"><div><h3>Arcs</h3><ul class="arcs" id="arcs"></ul><h3>Stories, awaiting grading</h3><ul class="arcs" id="stories"></ul></div><div><h3>Themes</h3><ul class="themes" id="themes"></ul></div></div>
  </section>`;
  const tip=$("#tip"), chart=$("#chart");
  const g=new (GL_OK?GlobeProv:Globe)(chart,{wheel:true,labels:true,onDraw:renderLegend,onMarker:m=>showEvent(m.id),onCountry:(f)=>showPlace(f),onHover:(hit,ev)=>{ if(hit&&hit.unnamed){ const r=chart.getBoundingClientRect(); tip.hidden=false; tip.style.left=Math.min(r.width-270,ev.clientX-r.left+14)+"px"; tip.style.top=(ev.clientY-r.top+14)+"px"; chart.style.cursor="grab"; tip.innerHTML=`<b>No state recorded</b><span>the map marks no polity here in ${fmtY(year)}</span>`; return; } if(!hit||(!hit.marker&&!hit.feature)){ tip.hidden=true; chart.style.cursor="grab"; return; } const r=chart.getBoundingClientRect(); tip.hidden=false; tip.style.left=Math.min(r.width-270,ev.clientX-r.left+14)+"px"; tip.style.top=(ev.clientY-r.top+14)+"px"; chart.style.cursor="pointer"; if(hit.marker){ const e=byId[hit.marker.id]; tip.innerHTML=`<b>${esc(e.h)}</b><span>${fmtY(e.y)}, ${esc(e.where||rname(e))}; ${["","knot","strand","fibre"][e.tier]||""}</span>`; } else { const f=hit.feature, pr=profileFor(f,year); const B=COLORBY==="bloc"?blocTable(year):null; const bl=B?B.cls[blocOf(f,year)].name:""; const st=f.src==="cs"?(STATUS_NOTE[f.properties.NAME]||(f.properties.st==="independent"?"independent state":`${STATUS[f.properties.st]||f.properties.st}${f.properties.SUBJECTO?" of "+f.properties.SUBJECTO:""}`)):f.src==="cl"?`${pr.sub?pr.sub+"; ":""}${f.properties.SUBJECTO?"within "+f.properties.SUBJECTO+"; ":""}${f.properties.fx==="gaz"?"extent approximate, drawn from its seat and researched reach":f.properties.fx==="fill"?"shape from historical basemaps, confirmed by dated research":f.properties.fx==="hb"?"borders approximate, from the period map nearest this date":f.properties.a<1400?"borders as recorded around "+fmtY(f.properties.a):"borders as recorded for "+f.properties.a+" to "+(f.properties.b-1)}`:f.src==="pp"?(f.properties.fx==="native"?"homeland of a native nation; coloured as a country from the treaty era, when colonial powers dealt with it as a sovereign":"lands of peoples with no state"):""; const since=f.src==="cs"&&f.properties.a>CS0+.01?`; these borders since ${Math.floor(f.properties.a)}`:""; const hn=hit.hatch?`<span class="hn">Part of this land changed hands between ${hit.hatch.properties.a} and ${hit.hatch.properties.b}, from ${esc(hit.hatch.properties.frm)} to ${esc(hit.hatch.properties.to)}; the date is not recorded.</span>`:""; const un=(hit.under||hit.gap)?`<span class="hn">Outside the recognised states of ${year}; named as the survey of ${mapYear(year)} names it.</span>`:""; const inf=f.properties.INF?`<span class="hn">${f.properties.INF==="region"?`The survey of ${mapYear(year)} leaves this land blank; it is named here by the peoples of the region.`:`The survey of ${mapYear(year)} leaves this land blank; the name comes from the neighbouring survey.`}</span>`:""; const pc=f.src!=="cs"&&f.properties.t?`<span class="hn">${esc(f.properties.t)}, ${f.properties.y}.</span>`:""; tip.innerHTML=`<b>${esc(pr.title)}</b><span>${esc(st||pr.sub||"")}${since}${bl?"; "+esc(bl):""}</span>${pc}${hn}${un}${inf}`; } }});
  window.MA={globe:g}; $("#zi").onclick=()=>g.setZoom(g.zoom*1.5); $("#zo").onclick=()=>g.setZoom(g.zoom/1.5); $("#zr").onclick=()=>{ g.pan=[0,0]; g.setZoom(1); };
  if(flat){ g.flat=1; g.place(); }
  $$(".gbar button[data-p]").forEach(b=>b.onclick=()=>{ flat=b.dataset.p==="flat"; store.set("ma-flat",flat); $$(".gbar button[data-p]").forEach(x=>x.setAttribute("aria-pressed",x===b)); $(".fgrid").classList.toggle("wide",flat); requestAnimationFrame(()=>{ g.resize(); g.setFlat(flat); }); });
  let playT=null; const stopPlay=()=>{ clearInterval(playT); playT=null; $("#play").setAttribute("aria-pressed","false"); $("#play").textContent="Play the years"; };
  $("#play").onclick=()=>{ if(playT){ stopPlay(); return; } $("#play").setAttribute("aria-pressed","true"); $("#play").textContent="Pause"; if(year>=YMAX) setYear(YMIN,true); playT=setInterval(()=>{ const st=Math.max(+$("#pspeed").value,gridStep(year)); if(year+st>YMAX){ setYear(YMAX,true); stopPlay(); return; } setYear(year+st,true); },st0()); };
  const st0=()=>REDUCED?1400:900;
  $("#phys").onchange=e=>{ SHOWPHYS=e.target.checked; store.set("ma-phys",SHOWPHYS); g.draw(); };
  $("#cmp").onchange=e=>{ const v=e.target.value; g.setCompare(v?+v:null); renderLedger(); };
  function renderLedger(){ const el=$("#ledger"); if(!el) return; const all=changesIn(year).filter(c=>c.k!=="survey"||c.y===year), cmp=$("#cmp").value; const big=all.filter(c=>c.k!=="survey").sort((a,b)=>(b.ar||0)-(a.ar||0)).slice(0,30).sort((a,b)=>a.d<b.d?-1:a.d>b.d?1:0); const notes=all.filter(c=>c.k==="survey");
    const near=(dir)=>{ const ys=[...new Set((CHG||[]).filter(c=>c.k!=="survey").map(c=>c.y))].sort((a,b)=>a-b); return dir<0?ys.filter(x=>x<year).pop():ys.find(x=>x>year); }; const pv=near(-1), nx=near(1);
    el.innerHTML=`<div class="lh"><h3>Borders that changed in ${fmtY(year)}</h3><span class="nav">${pv?`<button data-y="${pv}" aria-label="Previous year with a change">← ${pv}</button>`:""}${nx?`<button data-y="${nx}" aria-label="Next year with a change">${nx} →</button>`:""}</span></div>${notes.map(n=>`<p class="sv">${esc(n.t)}.</p>`).join("")}${big.length?`<ol class="chg">${big.slice(0,14).map((c,i)=>`<li><button data-i="${i}"><span class="d">${c.d.length>4?new Date(c.d+"T12:00:00Z").toLocaleDateString("en-GB",{day:"numeric",month:"short",timeZone:"UTC"}):c.y}</span><span class="t">${esc(c.t)}</span></button></li>`).join("")}</ol>${big.length>14?`<p class="quiet small">And ${big.length-14} smaller changes.</p>`:""}`:`<p class="quiet small">No border moved this year${pv||nx?"; step to the nearest year that has a change":""}.</p>`}${cmp?`<p class="small quiet">Dashed red lines: the borders of ${cmp}.</p>`:""}`;
    $$("#ledger .chg button").forEach(b=>b.onclick=()=>{ const c=big[+b.dataset.i]; if(c&&c.lon!=null){ g.flash(c); SND.bead(); } });
    $$("#ledger .nav button").forEach(b=>b.onclick=()=>setYear(+b.dataset.y,true)); }
  chgP.then(()=>renderLedger());
  function renderLegend(present,unnamed){ const el=$("#legend"); if(!el) return; const W=g.W, my=mapYear(year), nx=MAPY.find(m=>m>my); const base=W&&W.src==="cs"?`<span class="g quiet">Borders as they stood in mid-${year}; dependencies dashed and in the lighter shade of their ruler.</span>`:`<span class="g quiet">Borders as recorded for ${year}; members of a union and vassals dashed and in the lighter shade of their overlord; peoples outside any state faint.</span>`; const none=unnamed?`<span class="g"><span class="dot" style="background:var(--land);border:1px solid var(--rule)"></span>No state recorded</span>`:"";
    if(COLORBY==="gov"){ const order=["monarchy","republic","autocracy","theocracy","colony","stateless","other"]; el.innerHTML=order.filter(k=>present.has(k)).map(k=>`<span class="g"><span class="dot" style="background:${tint(CLS[k].color)};border:1px solid var(--rule)"></span>${esc(CLS[k].name)}</span>`).join("")+none+base; return; }
    if(COLORBY==="bloc"){ const B=blocTable(year); el.innerHTML=(B?`<span class="g"><b>${esc(B.t)}</b></span>`+Object.keys(B.cls).filter(k=>present.has(k)).map(k=>`<span class="g"><span class="dot" style="background:${tint(B.cls[k].color,"home")};border:1px solid var(--rule)"></span>${esc(B.cls[k].name)}</span>`).join("")+`<span class="g quiet">dependencies in the lighter shade of their overlord</span>`:`<span class="g quiet">No bloc table for ${year}: blocs are drawn for 1914 to 1918, 1939 to 1945, 1947 to 1991 and 1992 onward.</span>`)+none+base; return; }
    el.innerHTML=none+base; }
  const snap=y=>{ const s=WORLD.snaps; let b=s[0]; for(const x of s) if(x.y<=y) b=x; return b; };
  const nearestOf=(arr,y)=>{ let b=null; for(const x of arr) if(x.y<=y&&(!b||x.y>b.y)) b=x; return b||arr[0]; };
  function renderWorld(){ const A=ageOf(year), ageP=`<p class="agep"><b>${esc(A.n)}</b>, ${fmtY(A.a)} to ${A.b>2025?"today":fmtY(A.b)}. ${esc(A.d)}</p>`;
    if(year<WORLD.snaps[0].y){ $("#worldcard").innerHTML=`<div class="wc"><h2>The world in ${fmtY(year)}</h2>${ageP}<p class="quiet small">Population, cities and economies are recorded from ${WORLD.snaps[0].y}; before then the map carries the account.${year<-700?" Dates before 700 BCE are approximate: the chronologies of Egypt and Mesopotamia differ by decades.":""}</p></div>`; return; }
    const s=snap(year), ec=nearestOf(WORLD.econ||[],year), rl=nearestOf(WORLD.rel||[],year);
    $("#worldcard").innerHTML=`<div class="wc"><h2>The world in ${s.y}</h2>${ageP}${s.y!==year?`<p class="quiet small">The nearest snapshot before ${year}.</p>`:""}<p class="wl"><b>${s.pop>=1000?(s.pop/1000).toFixed(1)+" billion":s.pop+" million"}</b> people; life expectancy at birth <b>${s.life}</b>. Largest economy, ${esc(s.economy)}. Largest state by area, ${esc(s.state)}.</p>${lineChart(POP(),{h:120,w:520,ml:46,cursor:year,x0:1440,x1:2025})}<div class="wcols">${s.cities?`<div><p class="k">Largest cities, ${s.y}</p>${barsH(s.cities.slice(0,6).map(c=>[c[0],c[3]*1e6]))}</div>`:""}${ec?`<div><p class="k">Share of world output, ${ec.y}</p>${barsH(ec.top.slice(0,5),{fmt:v=>v,unit:"%"})}</div>`:""}${rl?`<div><p class="k">Religion, ${rl.y}</p>${barsH(rl.top.slice(0,5),{fmt:v=>v,unit:"%"})}</div>`:""}</div>${s.powers?`<p class="k">Powers, ${s.y}</p><p>${esc(s.powers)}</p>`:""}${s.money?`<p class="k">Money, ${s.y}</p><p>${esc(s.money)}</p>`:""}${s.travel||s.news?`<p class="k">Distance</p><p>${esc(s.travel||"")} ${esc(s.news||"")}</p>`:""}${s.people?`<p class="k">Alive in ${s.y}</p><p>${s.people.map(esc).join("; ")}.</p>`:""}${s.dyk?`<p class="k">One detail</p><p>${esc(s.dyk)}</p>`:""}</div>`; }
  function renderMotion(){ const active=STORIES.filter(S=>year>=S.span[0]&&year<=S.span[1]).map(S=>{ const hs=S.chapters.map(c=>byId[c.hinge]).filter(Boolean); let i=-1; hs.forEach((h,k)=>{ if(h.y<=year) i=k; }); const cur=i>=0?hs[i]:null, nxt=hs[i+1]||null; const gr=cur&&nxt&&S.graded?arrowBetween(cur.id,nxt.id).grade:"none"; return {S,i,cur,nxt,gr}; });
    const regionOf=S=>S.region||(byId[S.chapters[0].hinge]||{}).r||"eu";
    const groups=by==="region"?DATA.regions.map(r=>[r.name,active.filter(a=>regionOf(a.S)===r.id)]):THEMES.map(t=>[t.title,active.filter(a=>a.S.themes&&(a.S.themes.primary===t.id||(a.S.themes.secondary||[]).includes(t.id)))]).concat([["No theme yet",active.filter(a=>!a.S.themes)]]);
    $("#mh").textContent=`${active.length} ${active.length===1?"arc":"arcs and stories"} in motion in ${year}`;
    $("#motion").innerHTML=groups.filter(g=>g[1].length).map(([name,as])=>`<div class="grp"><h4>${esc(name)}</h4>${as.map(a=>`<div class="mo"><a class="t" href="#story-${a.S.id}">${esc(a.S.title)}</a><div class="st">${a.cur?`<span>After knot ${a.i+1}, <a href="#event-${a.cur.id}">${esc(a.cur.h)}</a>, ${a.cur.y}</span>`:`<span>Opens with <a href="#event-${a.nxt.id}">${esc(a.nxt.h)}</a>, ${a.nxt.y}</span>`}${a.cur&&a.nxt?`<span>${gradeTag(a.gr,a.gr==="none"?"toward":a.gr+", toward")} <a href="#event-${a.nxt.id}">${esc(a.nxt.h)}</a>, ${a.nxt.y}</span>`:(a.cur?`<span class="quiet">the last knot</span>`:"")}</div>${a.cur?`<p class="s1">${esc(a.S.chapters[a.i].s1||"")}</p>`:""}</div>`).join("")}</div>`).join("")||`<p class="quiet">No arc spans this year.</p>`;
    const es=EV.filter(e=>Math.abs(fy(e)-year)<=win&&(showAll||e.tier<3)&&hasTag(e,tag));
    $("#rh").textContent=`Every region, ${year-win} to ${year+win}: ${es.length} ${tag?tagName(tag).toLowerCase()+" ":""}events`;
    $("#regions").innerHTML=DATA.regions.map(r=>{ const rs=es.filter(e=>e.r===r.id).sort((a,b)=>fy(a)-fy(b)); return `<div class="rcol"><h4><span class="dot" style="background:var(--${r.id})"></span>${esc(r.name)}<i>${rs.length}</i></h4>${rs.length?`<ul>${rs.map(e=>`<li class="t${e.tier}"><span class="yr">${fmtY(e.y)}</span><a href="#event-${e.id}">${esc(e.h)}</a></li>`).join("")}</ul>`:`<p class="quiet small">Nothing recorded in this window.</p>`}</div>`; }).join(""); }
  function renderGlobeLayers(){ const ms=EV.filter(e=>e.lat!=null&&(showAll||e.tier<3)&&hasTag(e,tag)&&Math.abs(fy(e)-year)<=win).map(e=>({id:e.id,tier:e.tier,lon:+e.lon,lat:+e.lat,label:e.tier===1?e.h:null})).sort((a,b)=>b.tier-a.tier); g.setMarkers(ms); const s=snap(year); g.setCities((year<WORLD.snaps[0].y?[]:(s.cities||[])).slice(0,8).map(c=>({name:c[0],lat:c[1],lon:c[2],m:c[3]}))); g.setLines(focus?threadLines(focus,{strong:true}):[]); }
  let focus=null;
  function spark(S){ const [a,b]=S.span, w=150, span=Math.max(1,b-a); const hs=S.chapters.map(c=>byId[c.hinge]).filter(Boolean); let paths="", dots=""; for(let i=0;i<hs.length;i++){ const x=(hs[i].y-a)/span*w; dots+=`<circle cx="${x.toFixed(1)}" cy="17" r="3"/>`; if(i<hs.length-1){ const x2=(hs[i+1].y-a)/span*w; const gr=S.graded?arrowBetween(hs[i].id,hs[i+1].id).grade:"none"; paths+=`<path class="${gr}" d="M${x.toFixed(1)} 17H${x2.toFixed(1)}"/>`; } } return `<svg viewBox="0 0 ${w} 34" aria-hidden="true">${paths}${dots}</svg>`; }
  const arcRow=S=>`<li><a href="#story-${S.id}" title="Hover to draw this arc's thread on the globe"><span><b>${esc(S.title)}</b><span class="s">${esc(S.graded?S.sub:S.thesis.split(". ")[0]+".")}</span><span class="m">${S.span[0]} to ${S.span[1]}; ${S.chapters.length} knots${S.graded?"; graded":""}</span></span>${spark(S)}</a></li>`;
  $("#arcs").innerHTML=STORIES.filter(s=>s.graded).map(arcRow).join("")||`<li class="quiet">No arc has been graded yet.</li>`;
  $("#stories").innerHTML=STORIES.filter(s=>!s.graded).map(arcRow).join("");
  $$("#arcs a, #stories a").forEach(a=>{ const S=SB[a.getAttribute("href").slice(7)]; a.addEventListener("pointerenter",()=>{ focus=S; renderGlobeLayers(); }); a.addEventListener("pointerleave",()=>{ focus=null; renderGlobeLayers(); }); });
  $("#themes").innerHTML=THEMES.map(t=>`<li><a href="#theme-${t.id}"><b>${esc(t.title)}</b><span class="s">Between ${esc(t.tension[0])} and ${esc(t.tension[1])}.</span></a></li>`).join("");
  let tmr=null; const setYear=(y,now)=>{ y=snapY(Math.max(YMIN,Math.min(YMAX,y))); year=y; const A=ageOf(y); $("#yv").textContent=fmtY(y); $("#yr").value=yPos(y); $("#yr").setAttribute("aria-valuetext",fmtY(y)+", "+A.n); $("#age").textContent=A.n; $("#age").title=A.d; store.set("ma-year",y); renderWorld(); renderMotion(); renderGlobeLayers(); renderLedger(); if(sel) showPlace(sel,true); clearTimeout(tmr); tmr=setTimeout(()=>g.setYear(year),now?0:120); };
  $("#yr").addEventListener("input",e=>{ if(playT) stopPlay(); setYear(posY(+e.target.value)); });
  $$(".ctl .seg button[data-b]").forEach(b=>b.onclick=()=>{ by=b.dataset.b; store.set("ma-mby",by); $$(".ctl .seg button[data-b]").forEach(x=>x.setAttribute("aria-pressed",x===b)); renderMotion(); });
  $$(".ctl .seg button[data-w]").forEach(b=>b.onclick=()=>{ win=+b.dataset.w; store.set("ma-win",win); $$(".ctl .seg button[data-w]").forEach(x=>x.setAttribute("aria-pressed",x===b)); renderMotion(); renderGlobeLayers(); });
  $("#tall").onchange=e=>{ showAll=e.target.checked; store.set("ma-tall",showAll); renderMotion(); renderGlobeLayers(); };
  $("#tagsel").onchange=e=>{ tag=e.target.value; store.set("ma-tag",tag); renderMotion(); renderGlobeLayers(); SND.tick(); };
  const chint=()=>{ $("#chint").textContent={empire:"each state its own tint; an empire and its dependencies share one",gov:"monarchy, republic, one-party rule, theocracy, colony, peoples without a state",bloc:"the alliances of the world wars, the Cold War and after"}[COLORBY]; }; chint();
  $$(".ctl .seg button[data-c]").forEach(b=>b.onclick=()=>{ COLORBY=b.dataset.c; store.set("ma-colorby",COLORBY); $$(".ctl .seg button[data-c]").forEach(x=>x.setAttribute("aria-pressed",x===b)); chint(); g.draw(); });
  setYear(year,true);
  const keys=e=>{ if(e.target&&/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)&&e.target.type!=="range") return; let d=0; if(e.key==="ArrowRight"||e.key==="ArrowUp") d=1; else if(e.key==="ArrowLeft"||e.key==="ArrowDown") d=-1; else if(e.key==="PageUp") d=10; else if(e.key==="PageDown") d=-10; else return; if(e.shiftKey) d*=10; e.preventDefault(); const gs=gridStep(d<0?year-1:year); setYear(Math.max(YMIN,Math.min(YMAX,year+d*gs)),false); SND.step(); };
  document.addEventListener("keydown",keys);
  /* the event card under the globe */
  function showEvent(id){ const e=byId[id]; if(!e) return; const mem=(MEM[e.id]||[]).map(m=>Object.assign({S:SB[m.story]},m)).filter(m=>m.S); const primary=mem.find(m=>m.role==="knot"&&m.S.graded)||mem.find(m=>m.S.graded)||mem[0]; const ins=inLinks(e.id).length+(e.causes||[]).length, outs=outLinks(e.id).length;
    g.setMarkers(g.markers.map(x=>Object.assign(x,{cur:x.id===id}))); SND.bead();
    const card=$("#evcard"); card.hidden=false; card.innerHTML=`<div class="kind">${fmtY(e.y)}${e.where?", "+esc(e.where):""}${rname(e)&&e.where!==rname(e)?", "+esc(rname(e)):""}; ${["","a knot","a strand","a fibre"][e.tier]||""}</div><h3><a href="#event-${e.id}">${esc(e.h)}</a></h3>${chips(e)}${e.bluf||e.hook?`<p>${esc(e.bluf||e.hook)}</p>`:""}${mem.length?`<p class="in">${mem.map(m=>`${m.role==="knot"?"Knot "+(m.chapter+1):"A strand of knot "+(m.chapter+1)} in <a href="#story-${m.S.id}">${esc(m.S.title)}</a>`).join("; ")}.</p>`:`<p class="in quiet">In no arc yet.</p>`}<div class="deeper"><a class="btn" href="#event-${e.id}">Read the event</a>${primary?`<a class="btn soft" href="#story-${primary.S.id}">Open ${primary.S.kind==="arc"?"the arc":"the story"}</a>`:""}<a class="btn soft" href="#event-${e.id}">Trace: ${ins} ${ins===1?"cause":"causes"}, ${outs} ${outs===1?"effect":"effects"}</a><button class="btn soft" id="evclose">Close</button></div>`;
    $("#evclose").onclick=()=>{ card.hidden=true; g.setMarkers(g.markers.map(x=>Object.assign(x,{cur:false}))); };
    if(innerWidth<900) card.scrollIntoView({behavior:REDUCED?"auto":"smooth",block:"nearest"}); }
  /* the place card */
  function showPlace(f,keep){ sel=f; const pr=profileFor(f,year); const okf=d3.geoArea(f)<2*Math.PI; const inside=EV.filter(e=>okf&&e.lat!=null&&(showAll||e.tier<=2)&&d3.geoContains(f,[+e.lon,+e.lat])).sort((a,b)=>Math.abs(a.y-year)-Math.abs(b.y-year)).slice(0,8).sort((a,b)=>fy(a)-fy(b));
    const arcsHere=okf?STORIES.filter(S=>S.chapters.some(c=>{ const h=byId[c.hinge]; return h&&h.lat!=null&&d3.geoContains(f,[+h.lon,+h.lat]); })):[];
    const facts=[["Government",pr.gov],["Head",pr.head],["Capital",pr.cap],["Religion",pr.rel],["People",pr.pop],["Economy",pr.econ]].filter(x=>x[1]);
    $("#place").hidden=false; $("#worldcard").hidden=true; $("#place").innerHTML=`<div class="pc"><div class="kind">${esc(pr.kindline)}</div><h2>${esc(pr.title)}</h2>${pr.sub?`<p class="sub">${esc(pr.sub)}</p>`:""}${facts.length?`<dl class="facts">${facts.map(([k,v])=>`<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join("")}</dl>`:""}${pr.now?`<p class="now">${esc(pr.now)}</p>`:""}${pr.how?`<h3>How it got here</h3><p>${esc(pr.how)}</p>`:""}${pr.next?`<h3>What comes next</h3><p>${esc(pr.next)}</p>`:""}${pr.note?`<h3>${esc(pr.noteTitle)}</h3><p>${esc(pr.note)}</p>`:""}${pr.periods&&pr.periods.length>1?`<h3>Over time</h3><ol class="periods">${pr.periods.map(p=>`<li class="${p===pr.p?"cur":""}"><button data-y="${p.a}"><span class="yrs">${p.a} to ${p.b>=2025?"now":p.b}</span><span class="pt">${esc(p.t)}</span><span class="pg">${esc(p.gov||"")}</span></button></li>`).join("")}</ol>`:""}<h3>Events here, nearest to ${year}</h3>${inside.length?`<ul class="century">${inside.map(e=>`<li><a href="#event-${e.id}"><span class="yr">${fmtY(e.y)}</span>${esc(e.h)}</a></li>`).join("")}</ul>`:`<p class="quiet">No event in the atlas is placed inside this border.</p>`}${arcsHere.length?`<h3>Arcs that turn here</h3><ul class="century">${arcsHere.map(S=>`<li><a href="#story-${S.id}">${esc(S.title)}</a> <span class="small quiet">${S.span[0]} to ${S.span[1]}</span></li>`).join("")}</ul>`:""}<p class="exits">${pr.wk?`<a href="https://en.wikipedia.org/wiki/${encodeURIComponent(pr.wk.replace(/ /g,"_"))}" target="_blank" rel="noopener">Wikipedia</a>`:""}<button class="btn soft" id="pclose">Back to the world</button></p></div>`;
    $("#pclose").onclick=()=>{ sel=null; $("#place").hidden=true; $("#worldcard").hidden=false; };
    $$(".periods button").forEach(b=>b.onclick=()=>setYear(+b.dataset.y,true));
    if(!keep&&innerWidth<900) $("#place").scrollIntoView({behavior:REDUCED?"auto":"smooth",block:"start"}); }
  page={destroy(){ g.destroy(); clearInterval(playT); document.removeEventListener("keydown",keys); }};
}
/* a profile for any feature at any year */
const PEOPLE_RX=/hunter|gatherer|peoples|cultures|nomad|aboriginal|tribes|^maori$|^polynesians$|^papuans$|^inuit|^san$/i;
function profileFor(f,y){ const name=f.properties.NAME||"Unnamed", subj=f.properties.SUBJECTO||"", em=empireOf(f,y);
  const aka=f.properties.AKA||""; const p=POLS.find(p=>p.re.test(name)&&y>=p.a&&y<=p.b)||(aka?POLS.find(p=>p.re.test(aka)&&y>=p.a&&y<=p.b):null)||null; const periods=p?POLS.filter(q=>q.key===p.key).sort((a,b)=>a.a-b.a):POLS.filter(q=>q.re.test(name)).sort((a,b)=>a.a-b.a);
  const note=em&&(RULES.empnote||{})[em.k]?(RULES.empnote[em.k].find(n=>y>=n.a&&y<n.b)||{}).t:"";
  const out={name,p,periods,gov:p&&p.gov,head:p&&p.head,cap:p&&p.cap,rel:p&&p.rel,pop:p&&p.pop,econ:p&&p.econ,now:p&&p.now,how:p&&p.how,next:p&&p.next,wk:p&&p.wk};
  if(p){ out.title=p.t; out.sub=[p.gov,p.a+" to "+(p.b>=2025?"now":p.b)].filter(Boolean).join("; "); out.kindline=`On the globe in ${y}`; }
  else if(subj&&subj!==name&&em){ out.title=name; out.sub=`Dependency of ${em.label}`; out.kindline=`On the globe in ${y}`; const mp=POLS.find(q=>q.re.test(subj)&&y>=q.a&&y<=q.b); if(mp){ out.gov=`Ruled from ${mp.cap||mp.t}`; out.head=mp.head; } }
  else if(PEOPLE_RX.test(name)){ out.title=name; out.sub="A people, mapped by territory"; out.kindline=`On the globe in ${y}`; out.now="The map marks the land of a people rather than a state. The atlas has no profile for them yet; the events placed inside this border are the record."; }
  else { out.title=name; out.sub=em&&em.label!==name?em.label:""; out.kindline=`On the globe in ${y}`; out.now="No profile for this polity in this year yet. The events placed inside its border are the record."; }
  if(note){ out.note=note; out.noteTitle=em.label; }
  return out; }
/* ---------- page: story ---------- */
function storyPage(id){
  const S=SB[id]; if(!S){ missing("story"); return; }
  const tierNames=["Knots","Strands","Fibres"]; let tier=store.get("ma-tier",0);
  const th=S.themes?[S.themes.primary,...(S.themes.secondary||[])].map(t=>TB[t]).filter(Boolean):[];
  where([["Atlas","#atlas"],[S.title,"#story-"+S.id]]);
  const hinges=S.chapters.map(c=>byId[c.hinge]).filter(Boolean);
  const kindLine=`${S.kind==="arc"?"Arc":"Story"}, ${S.span[0]} to ${S.span[1]}.${th.length?" "+th.map((t,i)=>`<a href="#theme-${t.id}" style="color:inherit">${esc(t.title)}</a>`).join(", ")+".":""}${S.graded?"":" Ungraded: the arrows here carry no verdicts yet."}`;
  const present=new Set(); if(S.graded) for(let i=0;i<hinges.length-1;i++) present.add(arrowBetween(hinges[i].id,hinges[i+1].id).grade);
  main.innerHTML=`<div class="ledger" id="ledger"><div class="margin"><svg class="thread" id="thread" aria-hidden="true"></svg></div>
  <article class="text">
   <header class="storyhead"><div class="kind">${kindLine}</div><h1>${esc(S.title)}</h1>${S.sub?`<p class="sub">${esc(S.sub)}</p>`:""}
   <p class="thesis">${esc(S.thesis)}</p>
   ${S.assumptions||S.disconfirm?`<details class="assume"><summary>What the thesis assumes, and what would disprove it</summary>${S.assumptions?`<ul>${S.assumptions.map(a=>`<li>${esc(a)}</li>`).join("")}</ul>`:""}${S.disconfirm?`<p style="margin-top:8px">${esc(S.disconfirm)}</p>`:""}</details>`:""}
   ${S.fig?lineChart(S.fig,{knots:S.chapters.map((c,i)=>({id:c.hinge,y:(byId[c.hinge]||{}).y,n:i+1,t:c.title})).filter(k=>k.y),x0:S.span[0]-10,x1:Math.max(S.span[1]+10,2025)}):""}
   <div class="tierbar"><span class="l">Open every knot at</span><div class="seg" role="group" aria-label="Depth">${tierNames.map((n,i)=>`<button data-t="${i}" aria-pressed="${i===tier}">${n}<i>${["the turning points only","with the events between","with details and arrows"][i]}</i></button>`).join("")}</div></div>
   ${present.size?`<div class="legend">${[...present].sort((a,b)=>GRADES.indexOf(a)-GRADES.indexOf(b)).map(g=>gradeTag(g,g+", "+GRADEHELP[g])).join("")}</div>`:""}
   </header>
   <div id="chapters"></div>
   <footer class="foot">${S.today?`<div><h4>Today</h4><p>${esc(S.today)}</p></div>`:""}${S.awkward?`<div class="awk"><h4>The awkward fact</h4><p>${esc(S.awkward)}</p></div>`:""}</footer>
  </article>
  <aside class="aside"><div class="medal" id="medal"><div class="cap" id="mcap"></div></div><div class="mean" id="mean"></div></aside></div>`;
  const g=new Globe($("#medal"),{zoom:1.7,relief:false,hatch:false,onMarker:m=>{ const k=$(`#k-${m.ch}`); if(k) k.scrollIntoView({behavior:REDUCED?"auto":"smooth",block:"start"}); }});
  let open=S.chapters.map(()=>tier);
  function renderChapters(){ const out=[]; S.chapters.forEach((c,i)=>{ const h=byId[c.hinge]; if(!h) return; const lv=open[i]; const next=S.chapters[i+1]; const arrow=next?arrowBetween(c.hinge,next.hinge):null; const sup=(c.support||[]).map(s=>byId[s]).filter(Boolean).sort((a,b)=>fy(a)-fy(b));
      const strands=lv>=1&&sup.length?`<p class="ah">${lv===1?"The strands":"Strands and fibres"}</p>`+sup.map(e=>`<div class="strand t${e.tier}"><div class="bead"><i></i></div><div><span class="yr">${fmtY(e.y)}</span><a class="t" href="#event-${e.id}">${esc(e.h)}</a><p class="hk">${esc(e.hook||e.what||"")}</p>${lv>=2?`${e.bluf?`<p class="why">${esc(e.bluf)}</p>`:""}${e.figs&&e.figs.kv?`<div class="figs">${e.figs.kv.slice(0,3).map(([v,l])=>`<span><b>${esc(v)}</b> ${esc(l)}</span>`).join("")}</div>`:""}`:""}</div></div>`).join(""):"";
      const arrowBlock=lv>=1&&arrow&&arrow.link?`<p class="ah">The arrow to knot ${i+2}, ${esc(next.title.toLowerCase())}</p>`+noteHTML(Object.assign({_via:arrow.via},arrow.link),lv>=2):"";
      const ctl=`<div class="kctl">${lv===0?`<button class="kbtn" data-i="${i}" data-to="1">Open the knot</button>`:""}${lv===1?`<button class="kbtn" data-i="${i}" data-to="2">Show the details</button><button class="kbtn soft" data-i="${i}" data-to="0">Close</button>`:""}${lv===2?`<button class="kbtn soft" data-i="${i}" data-to="0">Close the knot</button>`:""}</div>`;
      out.push(`<section class="knot lv${lv}" id="k-${c.id}" data-i="${i}"><button class="num" data-i="${i}" data-to="${lv===0?1:0}" aria-expanded="${lv>0}" title="${lv===0?"Open this knot":"Close this knot"}">${i+1}<i></i></button>${c.conn?`<p class="conn ${c.conn==="but"?"but":""}">${esc(c.conn)}</p>`:""}<h2>${esc(c.title)} <span class="yr">${h.y}</span></h2><p class="s1">${esc(c.s1)}</p><p class="hinge">The event: ${evLink(h)}${h.where?", "+esc(h.where):""}.</p>${lv>=1&&c.s2?`<p class="s2">${esc(c.s2)}</p>`:""}${strands}${arrowBlock}${ctl}</section>`); });
    $("#chapters").innerHTML=out.join(""); $$("#chapters .kbtn, #chapters .num").forEach(b=>b.onclick=()=>{ const i=+b.dataset.i; open[i]=+b.dataset.to; const y=window.scrollY; renderChapters(); window.scrollTo(0,y); const k=$(`#k-${S.chapters[i].id}`); if(k&&k.getBoundingClientRect().top<0) k.scrollIntoView({block:"start"}); }); requestAnimationFrame(()=>drawThread(true)); spy(); }
  /* the thread down the margin */
  let drawn=false;
  function drawThread(animate){ const svg=$("#thread"), led=$("#ledger"); if(!svg||!led) return; const L=led.getBoundingClientRect(); const dots=$$(".knot .num",led).map(n=>{ const d=n.querySelector("i"); const r=d.getBoundingClientRect(), nr=n.getBoundingClientRect(); return {x:r.left+r.width/2-L.left,y:r.top+r.height/2-L.top,nt:nr.top-L.top}; }); svg.setAttribute("width",84); svg.setAttribute("height",Math.ceil(L.height)); svg.style.height=L.height+"px"; svg.setAttribute("viewBox",`0 0 84 ${Math.ceil(L.height)}`); let h=`<defs><clipPath id="cp"><rect id="cpr" x="0" y="0" width="84" height="${animate&&!drawn&&!REDUCED?0:L.height}"/></clipPath></defs><g clip-path="url(#cp)">`; for(let i=0;i<dots.length-1;i++){ const a=dots[i], b=dots[i+1]; const gr=S.graded?arrowBetween(S.chapters[i].hinge,S.chapters[i+1].hinge).grade:"none"; const y1=a.y+12, y2=b.nt-4; h+=`<path class="${gr}" d="M${a.x} ${y1}V${y2}"/>`; if(S.graded&&gr!=="none") h+=`<text class="${gr}" x="${a.x}" y="${(y1+y2)/2+4}" text-anchor="middle">${gr.toLowerCase()}</text>`; } h+=`</g>`; svg.innerHTML=h; if(animate&&!drawn&&!REDUCED){ drawn=true; const r=$("#cpr",svg), t0=performance.now(), H=L.height, dur=1300; const step=t=>{ const k=Math.min(1,(t-t0)/dur); r.setAttribute("height",H*d3.easeCubicOut(k)); if(k<1) requestAnimationFrame(step); }; requestAnimationFrame(step); } else drawn=true; }
  let ro; if(typeof ResizeObserver!=="undefined"){ ro=new ResizeObserver(()=>drawThread(false)); ro.observe($("#ledger")); }
  /* scroll spy: the medallion follows the knot you are reading */
  let io=null, cur=-1;
  function setCur(i){ if(i===cur) return; if(cur>=0) SND.bead(); cur=i; const c=S.chapters[i], h=byId[c.hinge]; $$(".knot").forEach(k=>k.classList.toggle("cur",+k.dataset.i===i)); g.setYear(h.y); g.rotateTo(+h.lon,+h.lat); g.setMarkers(hinges.map((e,j)=>({id:e.id,ch:S.chapters[j].id,lon:+e.lon,lat:+e.lat,cur:j===i,dim:j!==i}))); g.setLines(threadLines(S)); $("#mcap").textContent=`${h.y}, ${h.where||rname(h)}`; $("#mean").innerHTML=meanHTML(h); where([["Atlas","#atlas"],[S.title,"#story-"+S.id],[`${i+1}. ${c.title}`,"#story-"+S.id]]); }
  function spy(){ if(io) io.disconnect(); io=new IntersectionObserver(es=>{ const vis=es.filter(x=>x.isIntersecting).sort((a,b)=>a.boundingClientRect.top-b.boundingClientRect.top); if(vis.length) setCur(+vis[0].target.dataset.i); },{rootMargin:"-10% 0px -60% 0px",threshold:0}); $$(".knot").forEach(k=>io.observe(k)); if(cur<0) setCur(0); }
  $$(".seg button").forEach(b=>b.onclick=()=>{ tier=+b.dataset.t; store.set("ma-tier",tier); $$(".seg button").forEach(x=>x.setAttribute("aria-pressed",x===b)); open=S.chapters.map(()=>tier); renderChapters(); });
  renderChapters();
  page={destroy(){ g.destroy(); if(io) io.disconnect(); if(ro) ro.disconnect(); }};
}


/* ---------- trace: the graph around an event ---------- */
const RANK={Coincident:0,Contested:1,none:2,Contributing:3,Sufficient:4,Necessary:5};
const edgesIn=id=>inLinks(id).map(l=>({f:l.f,t:id,grade:l.grade,link:l})).concat(((byId[id]||{}).causes||[]).filter(c=>byId[c.f]&&!inLinks(id).some(l=>l.f===c.f)).map(c=>({f:c.f,t:id,grade:"none",why:c.why})));
const edgesOut=id=>outLinks(id).map(l=>({f:id,t:l.t,grade:l.grade,link:l})).concat(EV.filter(x=>(x.causes||[]).some(c=>c.f===id)&&!outLinks(id).some(l=>l.t===x.id)).map(x=>({f:id,t:x.id,grade:"none",why:(x.causes.find(c=>c.f===id)||{}).why})));
function buildTrace(id,depth){ const cols={0:[id]}, seen=new Set([id]), edges=[], parent={}; const CAP=9, more={};
  for(const dir of [-1,1]){ let frontier=[id]; for(let d=1;d<=depth&&frontier.length;d++){ const next=[]; for(const n of frontier){ const es=(dir<0?edgesIn(n):edgesOut(n)).sort((a,b)=>RANK[b.grade]-RANK[a.grade]); for(const ed of es){ const o=dir<0?ed.f:ed.t; if(!seen.has(o)){ const col=cols[dir*d]=cols[dir*d]||[]; if(col.length>=CAP){ more[dir*d]=(more[dir*d]||0)+1; continue; } seen.add(o); col.push(o); next.push(o); parent[o]={via:n,grade:ed.grade,ed}; } if(seen.has(o)&&!edges.some(x=>x.f===ed.f&&x.t===ed.t)) edges.push(ed); } } frontier=next; } }
  return {cols,edges,parent,more}; }
function traceSVG(e,T){ const ks=Object.keys(T.cols).map(Number).sort((a,b)=>a-b); const CW=200, NW=168, RH=44, PAD=14; const W=ks.length*CW, rows=Math.max(...ks.map(k=>T.cols[k].length+(T.more[k]?1:0))); const H=rows*RH+PAD*2;
  const pos={}, colOf={}; ks.forEach((k,ci)=>{ T.cols[k].forEach(id=>colOf[id]=ci); const col=T.cols[k].slice().sort((a,b)=>fy(byId[a])-fy(byId[b])); const n=col.length+(T.more[k]?1:0); const top=(H-n*RH)/2; col.forEach((id,ri)=>{ pos[id]={x:ci*CW+16,y:top+ri*RH+RH/2}; }); if(T.more[k]) pos["more"+k]={x:ci*CW+16,y:top+col.length*RH+RH/2}; });
  const clip=(s,n)=>s.length>n?s.slice(0,n-1).trimEnd()+"…":s;
  let h=""; for(const ed of T.edges){ const a=pos[ed.f], b=pos[ed.t]; if(!a||!b||!(colOf[ed.f]<colOf[ed.t])) continue; const x1=a.x+NW, x2=b.x, mx=(x1+x2)/2; const t=ed.link?ed.link.note.claim:(ed.why||""); h+=`<path class="${ed.grade}" d="M${x1} ${a.y}C${mx} ${a.y} ${mx} ${b.y} ${x2} ${b.y}"><title>${esc(ed.grade==="none"?"In the record, ungraded. ":ed.grade+". ")}${esc(t)}</title></path>`; }
  for(const k of ks){ for(const id of T.cols[k]){ const p=pos[id], o=byId[id], cur=id===e.id; h+=`<a href="#event-${id}" class="n${cur?" cur":""}"><rect x="${p.x}" y="${p.y-RH/2+4}" width="${NW}" height="${RH-8}" rx="2"/><text x="${p.x+10}" y="${p.y-4}">${esc(clip(o.h,26))}</text><text class="y" x="${p.x+10}" y="${p.y+12}">${o.y}, ${esc(clip(o.where||rname(o),22))}</text><title>${esc(o.h)}, ${o.y}</title></a>`; } if(T.more[k]){ const p=pos["more"+k]; h+=`<text class="y" x="${p.x+10}" y="${p.y+4}">and ${T.more[k]} more</text>`; } }
  const labels=ks.map((k,ci)=>`<text class="col" x="${ci*CW+16}" y="10">${k<0?(k===-1?"caused by":Math.abs(k)+" hops back"):(k===0?"this event":(k===1?"led to":k+" hops on"))}</text>`).join("");
  return `<svg class="trace" viewBox="0 -4 ${W} ${H+4}" width="${W}" height="${H+4}">${labels}${h}</svg>`; }
function weakest(e,T){ const roots=Object.keys(T.parent).filter(id=>Object.keys(T.cols).some(k=>+k<0&&T.cols[k].includes(id))&&!edgesIn(id).some(x=>T.parent[x.f]||x.f===e.id)); const out=[]; for(const r of roots){ let n=r, steps=[], w=null; while(T.parent[n]){ const p=T.parent[n]; steps.push({f:n,t:p.via,grade:p.grade}); if(!w||RANK[p.grade]<RANK[w.grade]) w=steps[steps.length-1]; n=p.via; } if(!steps.length) continue; const ungraded=steps.filter(s=>s.grade==="none").length; out.push({root:byId[r],steps,w,ungraded}); } return out.sort((a,b)=>fy(a.root)-fy(b.root)).slice(0,6); }

/* ---------- page: event ---------- */
function eventPage(id){
  const e=byId[id]; if(!e){ missing("event"); return; }
  let depth=store.get("ma-depth",2);
  const mem=(MEM[e.id]||[]).map(m=>Object.assign({S:SB[m.story]},m)).filter(m=>m.S);
  const primary=mem.find(m=>m.role==="knot"&&m.S.graded)||mem.find(m=>m.S.graded)||mem[0];
  where(primary?[["Atlas","#atlas"],[primary.S.title,"#story-"+primary.S.id],[e.h,"#event-"+e.id]]:[["Atlas","#atlas"],[e.h,"#event-"+e.id]]);
  const ins=inLinks(e.id), outs=outLinks(e.id);
  const recIn=(e.causes||[]).map(c=>Object.assign({e:byId[c.f]},c)).filter(c=>c.e&&!ins.some(l=>l.f===c.f));
  const recOut=EV.filter(x=>(x.causes||[]).some(c=>c.f===e.id)&&!outs.some(l=>l.t===x.id));
  const tierWord=["","Knot","Strand","Fibre"][e.tier]||"";
  const inLine=mem.length?mem.map(m=>`${m.role==="knot"?"Knot "+(m.chapter+1):"A strand of knot "+(m.chapter+1)} in <a href="#story-${m.S.id}">${esc(m.S.title)}</a>`).join("; "):"";
  const guessRow=(l,dir)=>{ const o=byId[dir==="in"?l.f:l.t]; if(!o) return ""; return `<li data-l="${l.id}"><div class="row"><span class="yr">${o.y}</span><a href="#event-${o.id}">${esc(o.h)}</a><span class="small quiet ital">${esc(l.type)}</span></div><p class="claim">${esc(l.note.claim)}</p><div class="guess" data-g="${l.grade}"><span>Grade this arrow:</span>${GRADES.map(g=>`<button data-pick="${g}">${g}</button>`).join("")}</div><div class="verdict" hidden></div><div class="full" hidden>${noteHTML(l,true)}</div></li>`; };
  const recRow=(o,why)=>`<li><div class="row"><span class="yr">${o.y}</span><a href="#event-${o.id}">${esc(o.h)}</a>${gradeTag("none","in the record, ungraded")}</div>${why?`<p class="claim">${esc(why)}</p>`:""}</li>`;
  const sib=primary&&primary.role==="knot"?(()=>{ const S=primary.S, i=primary.chapter; const p=S.chapters[i-1], n=S.chapters[i+1]; return `<nav class="pn">${p?`<a href="#event-${p.hinge}"><i>Knot ${i} of ${esc(S.title)}</i>${esc(p.title)}</a>`:"<span></span>"}${n?`<a href="#event-${n.hinge}" style="text-align:right"><i>Knot ${i+2} of ${esc(S.title)}</i>${esc(n.title)}</a>`:""}</nav>`; })():"";
  main.innerHTML=`<div class="ledger" id="ledger"><div class="margin"><svg class="thread" id="thread" aria-hidden="true"></svg></div>
  <article class="text">
   <header class="evhead"><div class="kind"><span>${fmtY(e.y)}${e.m?", "+["January","February","March","April","May","June","July","August","September","October","November","December"][e.m-1]:""}</span><span>${esc(e.where||"")}</span>${e.where&&e.where.toLowerCase()===rname(e).toLowerCase()?"":`<span>${esc(rname(e))}</span>`}${tierWord?`<span>${tierWord}</span>`:""}</div><h1>${esc(e.h)}</h1>${chips(e)}${inLine?`<p class="in">${inLine}.</p>`:""}
   </header>
   <section class="part"><h2 class="parth">The brief</h2>
   ${e.bluf?`<div class="bl"><h3>Bottom line</h3><p class="bluf">${esc(e.bluf)}</p></div>`:""}${e.now?`<div class="bl"><h3>Why it matters</h3><p class="sig">${esc(e.now)}</p></div>`:""}</section>
   <section class="part"><h2 class="parth">In depth</h2><div class="sec">
    ${e.story||e.what?`<h3>What happened</h3><p>${esc(e.story||e.what)}${e.who?` <span class="trig"><em>Who:</em> ${esc(e.who)}.</span>`:""}</p>`:""}
    ${e.why?`<h3>Why</h3><p>${esc(e.why)}${e.trig?` <span class="trig"><em>The trigger:</em> ${esc(e.trig)}</span>`:""}</p>`:""}
    ${e.then?`<h3>What followed</h3><p>${esc(e.then)}</p>`:""}
    ${e.figs?`<h3>By the numbers</h3>${figsHTML(e)}`:""}
    ${e.myth?`<h3>A common misreading</h3><p>${esc(e.myth)}</p>`:""}
    ${e.sites&&e.sites.length?`<h3>Places</h3><ul class="century">${e.sites.map(s=>`<li><b style="font-weight:400">${esc(s.n)}</b> <span class="quiet">${esc(s.d||"")}</span></li>`).join("")}</ul>`:""}
    ${e.fact?`<h3>Interesting fact</h3><p>${esc(e.fact)}</p>`:""}
   </div></section>
   <section class="part"><h2 class="parth">Causes and effects</h2>
   <div class="sec"><div class="tracehead"><h3>The trace</h3><span class="quiet small">causes to the left, effects to the right; the line carries the grade</span><div class="seg small" role="group" aria-label="Hops">${[2,3,4].map(d=>`<button data-d="${d}" aria-pressed="${d===depth}">${["","","Two hops","Three","Four"][d]}</button>`).join("")}</div></div><div class="tracewrap" id="tracewrap"></div><div id="weak"></div></div>
   <div class="sec"><h3>What caused this</h3>${ins.length||recIn.length?`<ul class="lk">${ins.map(l=>guessRow(l,"in")).join("")}${recIn.map(c=>recRow(c.e,c.why)).join("")}</ul>`:`<p class="quiet">No arrow into this event has been written yet.</p>`}</div>
   <div class="sec"><h3>What this caused</h3>${outs.length||recOut.length?`<ul class="lk">${outs.map(l=>guessRow(l,"out")).join("")}${recOut.map(o=>recRow(o,(o.causes.find(c=>c.f===e.id)||{}).why)).join("")}</ul>`:`<p class="quiet">No arrow out of this event has been written yet.</p>`}</div>
   </section>
   <p class="exits">Go deeper: ${e.wk?`<a href="https://en.wikipedia.org/wiki/${encodeURIComponent(e.wk.replace(/ /g,"_"))}" target="_blank" rel="noopener">Wikipedia</a>`:""}${e.bt?`<a href="https://www.britannica.com/${esc(e.bt)}" target="_blank" rel="noopener">Britannica${e.btt&&e.btt!==e.h?", "+esc(e.btt):""}</a>`:""}${e.src?`<a href="${esc(e.src)}" target="_blank" rel="noopener">Source</a>`:""}</p>
   ${sib}
  </article>
  <aside class="aside"><div class="medal" id="medal"><div class="cap">${fmtY(e.y)}, ${esc(e.where||rname(e))}</div></div><div class="mean" id="mean">${meanHTML(e)}</div></aside></div>`;
  function renderTrace(){ const T=buildTrace(e.id,depth); const ks=Object.keys(T.cols); $("#tracewrap").innerHTML=ks.length>1?traceSVG(e,T):`<p class="quiet ital">No arrow touches this event yet; it stands alone in the record.</p>`; const ws=weakest(e,T); const pathHTML=c=>{ const steps=c.steps.slice().reverse(); let h=`<a href="#event-${c.root.id}">${esc(c.root.h)}</a> <span class="yr">${c.root.y}</span>`; for(const s of c.steps){ const t=byId[s.t]; h+=` ${gradeTag(s.grade,s.grade==="none"?"ungraded":s.grade.toLowerCase())} ${t.id===e.id?`<b>this event</b>`:`<a href="#event-${t.id}">${esc(t.h)}</a> <span class="yr">${t.y}</span>`}`; } return h; };
    $("#weak").innerHTML=ws.length?`<p class="ah">Chains into this event</p><p class="quiet small" style="max-width:66ch;margin:0 0 8px">Each chain is read left to right; the tag between two events is the grade of that arrow. A chain is as strong as its weakest arrow.</p><ul class="chains">${ws.map(c=>`<li><div class="path">${pathHTML(c)}</div><div class="weak">${c.ungraded===c.steps.length?"Every arrow here is from the record and ungraded.":`Weakest arrow: ${gradeTag(c.w.grade)} from ${esc(byId[c.w.f].h)} to ${esc(byId[c.w.t].h)}${c.ungraded?`; ${c.ungraded} of the ${c.steps.length} arrows ungraded`:""}.`}</div></li>`).join("")}</ul>`:""; const tw=$("#tracewrap"), cur=$(".trace a.cur rect",tw); if(cur&&tw.scrollWidth>tw.clientWidth){ tw.classList.add("wide"); tw.scrollLeft=(+cur.getAttribute("x"))-tw.clientWidth/2+84; } else tw.classList.remove("wide"); }
  renderTrace();
  $$(".tracehead .seg button").forEach(b=>b.onclick=()=>{ depth=+b.dataset.d; store.set("ma-depth",depth); $$(".tracehead .seg button").forEach(x=>x.setAttribute("aria-pressed",x===b)); renderTrace(); });
  /* guess the grade */
  $$(".lk .guess button").forEach(b=>b.onclick=()=>{ const li=b.closest("li"), g=li.querySelector(".guess"), truth=g.dataset.g, pick=b.dataset.pick, v=li.querySelector(".verdict"); const hit=pick===truth; v.hidden=false; v.innerHTML=hit?`You graded it <b>${truth}</b>, as the editors did. ${esc(GRADEHELP[truth])}.`:`You graded it ${pick}; the editors graded it <b class="miss">${truth}</b>: ${esc(GRADEHELP[truth])}.`; g.hidden=true; li.querySelector(".full").hidden=false; });
  $$(".lk li[data-l] .row a").forEach(a=>{});
  $$(".lk li[data-l]").forEach(li=>{ const open=document.createElement("button"); open.className="open"; open.textContent="Show the editors' note"; open.onclick=()=>{ li.querySelector(".guess").hidden=true; li.querySelector(".full").hidden=false; open.remove(); }; li.querySelector(".guess").appendChild(open); });
  const g=new Globe($("#medal"),{zoom:2.2,relief:false,hatch:false,onMarker:m=>{ if(m.id&&m.id!==e.id) location.hash="#event-"+m.id; }});
  g.setYear(e.y); if(e.lat!=null){ g.rotateTo(+e.lon,+e.lat,false); g.setMarkers([{id:e.id,lon:+e.lon,lat:+e.lat,cur:true},...(e.sites||[]).map(s=>({lon:+s.lon,lat:+s.lat,kind:"site"}))]); }
  /* the margin: this event's place on its story's thread */
  if(primary&&primary.S){ const S=primary.S, hs=S.chapters.map(c=>byId[c.hinge]).filter(Boolean), svg=$("#thread"); const x=(svg.clientWidth||84)/2, step=34, top=40; let h=""; for(let i=0;i<hs.length-1;i++){ const gr=S.graded?arrowBetween(hs[i].id,hs[i+1].id).grade:"none"; h+=`<path class="${gr}" d="M${x} ${top+i*step+6}V${top+(i+1)*step-6}"/>`; } hs.forEach((e2,i)=>{ const isCur=e2.id===e.id||(primary.role==="strand"&&i===primary.chapter); h+=`<a href="#event-${e2.id}"><circle class="${isCur?"cur":""}" cx="${x}" cy="${top+i*step}" r="${isCur?6:4}"><title>${esc(i+1+". "+S.chapters[i].title)}</title></circle></a>`; }); svg.innerHTML=h; svg.style.pointerEvents="auto"; svg.style.height=(top+hs.length*step)+"px"; svg.setAttribute("height",top+hs.length*step); svg.setAttribute("viewBox",`0 0 84 ${top+hs.length*step}`); }
  page={destroy(){ g.destroy(); }};
}

/* ---------- page: themes ---------- */
function themesPage(){
  where([["Atlas","#atlas"],["Themes","#themes"]]);
  main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text about"><h1>Themes: the long arguments people have had with their condition.</h1><p class="lede">Each theme is a tension that no age has settled. The arcs below it are the cases; the ideas are events too, placed in time and linked to what shaped them.</p><ul class="themes" style="margin-top:20px">${THEMES.map(t=>`<li><a href="#theme-${t.id}"><b>${esc(t.title)}</b><span class="s">Between ${esc(t.tension[0])} and ${esc(t.tension[1])}. ${esc(t.passage.split(". ")[0])}.</span></a></li>`).join("")}</ul></article></div>`;
  page={destroy(){}};
}
function themePage(id){
  const t=TB[id]; if(!t){ missing("theme"); return; }
  where([["Atlas","#atlas"],["Themes","#themes"],[t.title,"#theme-"+t.id]]);
  const ss=storiesOfTheme(t.id); const knots=ss.flatMap(S=>S.chapters.map(c=>byId[c.hinge]).filter(Boolean).map(e=>({e,S}))).sort((a,b)=>fy(a.e)-fy(b.e));
  main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text"><header class="storyhead"><div class="kind">Theme. Between ${esc(t.tension[0])} and ${esc(t.tension[1])}.</div><h1>${esc(t.title)}</h1></header>
   <p class="passage">${esc(t.passage)}</p>
   <div class="poles">${t.cases.map(c=>`<div><b>${esc(c.pole)}</b><span>${esc(c.case)}</span></div>`).join("")}</div>
   ${t.covers?`<p class="quiet" style="max-width:62ch">Covers ${esc(t.covers)}.</p>`:""}
   <div class="sec"><h3>Arcs and stories under this theme</h3>${ss.length?`<ul class="arcs">${ss.map(S=>`<li><a href="#story-${S.id}"><span><b>${esc(S.title)}</b><span class="s">${esc(S.sub||"")}</span><span class="m">${S.themes.primary===t.id?"primary theme":"secondary theme"}; ${S.span[0]} to ${S.span[1]}</span></span><span></span></a></li>`).join("")}</ul>`:`<p class="quiet ital">No graded arc carries this theme yet. The German Question is the first graded arc; the rest follow.</p>`}</div>
   ${knots.length?`<div class="sec"><h3>The knots</h3><ul class="century">${knots.map(({e,S})=>`<li><a href="#event-${e.id}"><span class="yr">${fmtY(e.y)}</span>${esc(e.h)}</a> <span class="small quiet ital">${esc(S.title)}</span></li>`).join("")}</ul></div>`:""}
  </article></div>`;
  page={destroy(){}};
}


/* ---------- page: timeline ---------- */
const TSCALE=d3.scaleLinear().domain([-3400,1,1440,1800,1900,2000,2026]);
function timelinePage(){
  where([["Atlas","#atlas"],["Timeline","#timeline"]]);
  let year=store.get("ma-year",1914), theme=store.get("ma-ttheme",""), showAll=store.get("ma-tall",false), order=store.get("ma-torder","region");
  main.innerHTML=`<section class="tl">
   <div class="tlhead"><div><h1>The chart</h1><p class="lede">Every arc as a lane, every knot as a bead, the arrows between them graded. The scale widens toward the present: a century at the back takes less room than a decade at the front.</p></div>
    <div class="tlctl"><span class="l">Arrange</span><div class="seg small"><button data-o="region" aria-pressed="${order==="region"}">By region</button><button data-o="start" aria-pressed="${order==="start"}">By start</button></div><label>Theme <select id="tth"><option value="">all</option>${THEMES.map(t=>`<option value="${t.id}"${t.id===theme?" selected":""}>${esc(t.title)}</option>`).join("")}</select></label><label><input type="checkbox" id="tall"${showAll?" checked":""}> show fibres</label><span class="quiet small ital">Click the axis to set the year; <a href="#atlas">open the globe</a> at it.</span></div></div>
   <div class="tlwrap" id="tlwrap"><div class="tlgrid" id="tlgrid"></div><div class="tip" id="ttip" hidden></div></div></section>`;
  const wrap=$("#tlwrap"), grid=$("#tlgrid"), tip=$("#ttip");
  const LW=innerWidth<900?130:260, LH=44, W=Math.max(1100,wrap.clientWidth-LW-2);
  TSCALE.range([0,W*.1,W*.24,W*.4,W*.58,W*.88,W]);
  const x=y=>TSCALE(y);
  const ticks=[-3000,-2000,-1000,1,500,1000]; for(let y=1500;y<1800;y+=100) ticks.push(y); for(let y=1800;y<1900;y+=20) ticks.push(y); for(let y=1900;y<2000;y+=10) ticks.push(y); for(let y=2000;y<=2025;y+=5) ticks.push(y);
  const bands=[[-3400,1,"millennia"],[1,1440,"centuries"],[1440,1800,"half-centuries"],[1800,1900,"decades"],[1900,2000,"years"],[2000,2026,"the present"]];
  const regionOf=S=>S.region||(byId[S.chapters[0].hinge]||{}).r||"eu";
  const stories=STORIES.filter(S=>!theme||(S.themes&&(S.themes.primary===theme||(S.themes.secondary||[]).includes(theme)))).slice().sort((a,b)=>(b.graded-a.graded)||(a.span[0]-b.span[0]));
  const groups=order==="region"?DATA.regions.map(r=>[r.name,stories.filter(S=>regionOf(S)===r.id)]).filter(g=>g[1].length):[["",stories]];
  const lane=S=>{ const hs=S.chapters.map(c=>byId[c.hinge]).filter(Boolean); let h=""; for(let i=0;i<hs.length-1;i++){ const gr=S.graded?arrowBetween(hs[i].id,hs[i+1].id).grade:"none"; h+=`<path class="${gr}" d="M${x(fy(hs[i])).toFixed(1)} ${LH/2}H${x(fy(hs[i+1])).toFixed(1)}"/>`; } const sup=S.chapters.flatMap(c=>(c.support||[]).map(s=>byId[s]).filter(Boolean)); sup.forEach(e=>{ if(e.tier===3&&!showAll) return; h+=`<circle class="s t${e.tier}" data-id="${e.id}" cx="${x(fy(e)).toFixed(1)}" cy="${LH/2}" r="${e.tier===3?1.8:2.6}"/>`; }); hs.forEach((e,i)=>{ h+=`<circle class="k" data-id="${e.id}" data-n="${i+1}" cx="${x(fy(e)).toFixed(1)}" cy="${LH/2}" r="4.5"/>`; }); return `<div class="lane"><a class="lt" href="#story-${S.id}"><b>${esc(S.title)}</b><i>${S.span[0]} to ${S.span[1]}${S.graded?", graded":""}</i></a><svg width="${W}" height="${LH}" viewBox="0 0 ${W} ${LH}">${h}</svg></div>`; };
  const regions=DATA.regions.map(r=>{ const es=EV.filter(e=>e.r===r.id&&(showAll||e.tier<3)); return `<div class="lane reg"><div class="lt"><b>${esc(r.short||r.name)}</b><i>${es.length} events</i></div><svg width="${W}" height="${LH}" viewBox="0 0 ${W} ${LH}">${es.map(e=>`<circle class="e t${e.tier}" data-id="${e.id}" cx="${x(fy(e)).toFixed(1)}" cy="${LH/2+(e.tier===1?0:(e.tier===2?-7:7))}" r="${e.tier===1?3.2:(e.tier===2?2.2:1.5)}" style="fill:var(--${r.id})"/>`).join("")}</svg></div>`; }).join("");
  grid.innerHTML=`<div class="lane axis"><div class="lt"><b>Year</b><i id="ycur">${fmtY(year)}</i></div><svg id="axis" width="${W}" height="44" viewBox="0 0 ${W} 44">${bands.map(([a,b,l])=>`<rect x="${x(a)}" y="0" width="${x(b)-x(a)}" height="44" class="band"/><text x="${x(a)+6}" y="12" class="bl">${l}</text>`).join("")}${ticks.map(t=>`<line x1="${x(t)}" x2="${x(t)}" y1="28" y2="44"/><text x="${x(t)+3}" y="39">${t<0?-t+" BCE":t===1?"1 CE":t}</text>`).join("")}</svg></div>
   ${groups.map(([name,ss])=>`${name?`<div class="lane grp"><div class="lt"><b>${esc(name)}</b><i>${ss.length} ${ss.length===1?"story":"stories"}</i></div><svg width="${W}" height="24"></svg></div>`:""}<div class="lanes">${ss.map(lane).join("")}</div>`).join("")}<div class="lane sep"><div class="lt"><b>Every event</b><i>by region</i></div><svg width="${W}" height="20"></svg></div><div class="lanes">${regions}</div><div class="cursor" id="cursor"></div>`;
  function placeCursor(){ const c=$("#cursor"); c.style.left=(LW+x(year))+"px"; $("#ycur").textContent=fmtY(year); }
  placeCursor();
  $("#axis").addEventListener("click",e=>{ const r=$("#axis").getBoundingClientRect(); year=Math.round(TSCALE.invert(e.clientX-r.left)); year=Math.max(-3400,Math.min(2025,year)); store.set("ma-year",year); placeCursor(); });
  $("#tth").onchange=e=>{ store.set("ma-ttheme",e.target.value); timelinePage(); };
  $$(".tlctl .seg button").forEach(b=>b.onclick=()=>{ store.set("ma-torder",b.dataset.o); timelinePage(); });
  $("#tall").onchange=e=>{ store.set("ma-tall",e.target.checked); timelinePage(); };
  grid.addEventListener("pointermove",e=>{ const c=e.target.closest("circle[data-id]"); if(!c){ tip.hidden=true; return; } const ev=byId[c.dataset.id]; const r=wrap.getBoundingClientRect(); tip.hidden=false; tip.style.left=Math.min(wrap.clientWidth-260,e.clientX-r.left+wrap.scrollLeft+12)+"px"; tip.style.top=(e.clientY-r.top+wrap.scrollTop+12)+"px"; tip.innerHTML=`<b>${esc(ev.h)}</b><span>${fmtY(ev.y)}, ${esc(ev.where||rname(ev))}${c.dataset.n?"; knot "+c.dataset.n:""}</span>`; });
  grid.addEventListener("pointerleave",()=>{ tip.hidden=true; });
  grid.addEventListener("click",e=>{ const c=e.target.closest("circle[data-id]"); if(c) location.hash="#event-"+c.dataset.id; });
  if(x(year)+LW>wrap.clientWidth-40) wrap.scrollLeft=x(year)-wrap.clientWidth/2+LW;
  page={destroy(){}};
}



/* ---------- page: tag ---------- */
function tagPage(id){
  if(!CATS[id]&&!THREADS[id]){ missing("tag"); return; }
  where([["Atlas","#atlas"],[tagName(id),"#tag-"+id]]);
  const es=EV.filter(e=>hasTag(e,id)).sort((a,b)=>fy(a)-fy(b)); const groups=d3.groups(es,e=>Math.floor(e.y/100)*100); const ord=n=>n===1?"st":n===2?"nd":n===3?"rd":"th";
  const knots=es.filter(e=>e.tier===1).length;
  main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text about"><div class="kind quiet small">${CATS[id]?"Category":"Thread"}</div><h1>${esc(tagName(id))}</h1><p class="lede">${es.length} events from ${es[0].y} to ${es[es.length-1].y}, ${knots} of them knots. <a href="#atlas" id="tagatlas">See them on the globe</a>.</p>${groups.map(([c,gs])=>`<section class="century"><h2>The ${c/100+1}${ord(c/100+1)} century</h2><ul>${gs.map(e=>`<li class="t${e.tier}"><a href="#event-${e.id}"><span class="yr">${fmtY(e.y)}</span>${esc(e.h)}</a> <span class="small quiet">${esc(rname(e))}</span></li>`).join("")}</ul></section>`).join("")}</article></div>`;
  $("#tagatlas").onclick=()=>{ store.set("ma-tag",id); };
  page={destroy(){}};
}

/* ---------- page: every knot ---------- */
function knotsPage(){
  where([["Atlas","#atlas"],["Every knot","#knots"]]);
  const set=new Map(); EV.filter(e=>e.tier===1).forEach(e=>set.set(e.id,e)); STORIES.filter(s=>s.graded).forEach(S=>S.chapters.forEach(c=>{ if(byId[c.hinge]) set.set(c.hinge,byId[c.hinge]); }));
  const all=[...set.values()].sort((a,b)=>fy(a)-fy(b)); const cent=y=>Math.floor(y/100)*100; const groups=d3.groups(all,e=>cent(e.y));
  const ord=n=>n===1?"st":n===2?"nd":n===3?"rd":"th";
  main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text about"><h1>Every knot, in order.</h1><p class="lede">${all.length} turning points from ${all[0].y} to ${all[all.length-1].y}. A knot is an event that a story turns on; most belong to more than one.</p>${groups.map(([c,es])=>`<section class="century"><h2>The ${c/100+1}${ord(c/100+1)} century</h2><ul>${es.map(e=>{ const m=(MEM[e.id]||[]).filter(x=>x.role==="knot"&&SB[x.story]&&SB[x.story].graded); return `<li><a href="#event-${e.id}"><span class="yr">${fmtY(e.y)}</span>${esc(e.h)}</a> <span class="small quiet ital">${esc(rname(e))}${m.length?"; knot "+(m[0].chapter+1)+" of "+esc(SB[m[0].story].title):""}</span></li>`; }).join("")}</ul></section>`).join("")}</article></div>`;
  page={destroy(){}};
}

/* ---------- page: about ---------- */
function aboutPage(){
  where([["Atlas","#atlas"],["About","#about"]]);
  main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text about">
   <h1>An atlas of causes.</h1>
   <p>Meanwhile Atlas places ${EV.length} events from ${fmtY(Math.min(...EV.map(e=>e.y)))} to the present in their year and on the map, profiles ${POLS.length} states and periods behind the borders, and writes the arrows between events. Each arrow carries a claim, the best objection to it, the warrant that answers the objection, and a graded verdict. The purpose is analytic: a reader who finishes an arc should be able to say what carried the outcome, what merely accompanied it, and where the serious schools still disagree.</p>
   <p class="credo">History read as a chain of causes, with the weak links marked.</p>
   <h2>How the atlas is organised</h2>
   <div class="vocab">
    <div><b>Atlas</b><p>The whole: the globe, the years, and every arc, story and event.</p></div>
    <div><b>Arc</b><p>A long argument across centuries, built from turning points. The German Question runs from 1517 to 1990.</p></div>
    <div><b>Story</b><p>A shorter run of cause and effect inside an arc, or on its own. A thread is the smallest: one place, one decade, one question.</p></div>
    <div><b>Event</b><p>The unit. Each has a year, a place, a brief, its figures, its arrows in and out, and exits to Wikipedia and Britannica.</p></div>
   </div>
   <h2>Three depths inside a story</h2>
   <div class="vocab">
    <div><b>Knots</b><p>The turning points. Read only these and you have the story start to finish, with the grade of each arrow between them.</p></div>
    <div><b>Strands</b><p>The events between the knots, each with a line on why it belongs, and the claim behind each arrow.</p></div>
    <div><b>Fibres</b><p>The details: figures, the full arrow notes with objection, warrant, verdict and tests, and the audit trail.</p></div>
   </div>
   <h2>The grades</h2>
   <p>The thread in the margin changes with the grade of each arrow, so a story can be read by its line alone.</p>
   <div class="legend" style="flex-direction:column;align-items:flex-start;gap:8px">${GRADES.map(g=>gradeTag(g,g+": "+GRADEHELP[g])).join("")}</div>
   <p style="margin-top:14px">A Necessary or Sufficient arrow is solid. Contributing is dashed. Contested is dotted. Coincident is marked in red: the event came first and the reader should resist the inference. Every graded arrow records who graded it, whether a red team has checked it, and the date.</p>
   <h2>Themes</h2>
   <p>Ten themes cut across the arcs: Man and Power, Man and War, Man and Scarcity, and the rest. Each is a tension between two poles that no century has settled. Ideas are events in this atlas, placed in their year and linked to what shaped them, so a reader who meets Locke can follow the arrows back to the wars that produced him.</p>
   <h2>The globe</h2>
   <p>Borders change year by year. From 1886 they follow a dated record of every state and colony, so a border moves on the day a treaty, annexation or independence took effect. Before 1886 they follow a peer-reviewed geospatial record of the world's polities, in which each state's territory is drawn and dated period by period, often decade by decade; members of a larger union, such as the duchies of the Holy Roman Empire, are drawn inside it with the union's outer border. Where no state is recorded, the land is shaded faintly with the peoples of its region. Coastlines, rivers, lakes, mountain ranges and deserts come from a public-domain physical atlas. Every state on it has a profile for the period: its form of government, head, capital, religion, population and economy, where it came from and where it went next, with a timeline of its regimes. The globe colours either by empire or by form of government, the latter by the dominant form in each profile's period. Peoples mapped by territory rather than by state are marked as such.</p>
   <h2>Sources</h2>
   <p>Event briefs are written from the standard references and checked against Wikipedia and Britannica, both linked from every event. City sizes before 1950 follow Tertius Chandler; from 1950 they follow the UN's World Urbanization Prospects. Shares of world output follow Maddison. Religious shares follow the World Christian Database. Borders before 1886 are adapted from Cliopatria, the polity borders dataset of the Seshat Global History Databank (Bennett et al., <i>Scientific Data</i>, 2025), licensed CC BY 4.0; the atlas clips them to the coastline and colours them. From 1886 borders follow CShapes 2.0. Land outside any recorded state before 1886 is named from the historical-basemaps project (A. Ourednik, GPL-3.0). Every border was checked against dated research on 797 places from 1400 to 2025: names the dataset filed wrongly were corrected, changes were moved to the year of the treaty or conquest, and where a researched place shows a state that Cliopatria omits, that state's shape is taken from historical-basemaps. The colouring by empire is a rule set applied to the states' own names.</p>
   <h2>What this is for</h2>
   <p>The atlas is a tool for analysis before it is a tool for learning. It should give a reader a foundation for judging the present: which causes carried outcomes, how often the same mechanism recurs, and where confident narratives rest on contested links.</p>
  </article></div>`;
  page={destroy(){}};
}
function missing(kind){ where([["Atlas","#atlas"]]); main.innerHTML=`<div class="ledger plain"><div class="margin"></div><article class="text"><h1 style="font-size:32px;margin-top:20px">That ${kind} is not in the atlas.</h1><p class="lede" style="margin-top:10px">The link may be from an older edition. <a href="#atlas">Open the atlas</a> and search for it.</p></article></div>`; page={destroy(){}}; }

/* ---------- router ---------- */
let firstRoute=true;
function route(){ page.destroy(); sRes.hidden=true; if(!firstRoute) SND.page(); firstRoute=false; const h=(location.hash||"#atlas").slice(1); const m=h.match(/^(atlas|story|event|theme|themes|knots|about|timeline|meanwhile|tag)(?:-(.+))?$/); window.scrollTo(0,0);
  if(!m) return atlasPage(); const [,p,id]=m;
  if(p==="story"&&id) storyPage(id); else if(p==="event"&&id) eventPage(id); else if(p==="theme"&&id) themePage(id); else if(p==="themes") themesPage(); else if(p==="knots") knotsPage(); else if(p==="about") aboutPage(); else if(p==="timeline") timelinePage(); else if(p==="tag"&&id) tagPage(id); else atlasPage(); }
addEventListener("hashchange",route); route();
})();
