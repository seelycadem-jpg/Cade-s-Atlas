/* ================= the province globe =================
   The world's land is one fixed set of provinces (maps/prov.json, drawn once). Each year every province has an owner
   (maps/own.json); the globe only recolours provinces and switches border lines on where neighbouring owners differ,
   so a year change costs a few thousand state updates and nothing is redrawn or reloaded. */
let PROVP=null, PROVT=null;
/* the page keeps only small tables (areas, centres, neighbours, owners); the map's worker loads the shapes itself */
const provLoad=()=>PROVP||(PROVP=Promise.all([getJ("maps/prov_meta.json"),getJ("maps/own.json")]).then(([M,O])=>{
  const n=M.id.length, ix=new Map(); M.id.forEach((id,i)=>ix.set(id,i));
  const ar=Float64Array.from(M.ar), cx=Float64Array.from(M.cx), cy=Float64Array.from(M.cy);
  const m=M.ea.length, EA=new Int32Array(m), EB=new Int32Array(m), adj=Array.from({length:n},()=>[]);
  for(let k=0;k<m;k++){ const a=ix.get(M.ea[k]), b=M.eb[k]?ix.get(M.eb[k]):-1; EA[k]=a==null?-1:a; EB[k]=b==null?-1:b; if(EA[k]>=0&&EB[k]>=0){ adj[EA[k]].push(EB[k]); adj[EB[k]].push(EA[k]); } }
  /* one realm, one entry: the same name and overlord from different sources (record, research, review) count as one owner */
  const CAN=new Int32Array(O.pol.length), seen=new Map(); O.pol.forEach((p,o)=>{ if(!o) return; const k=(p[0]==="pp"?"pp":p[0]==="cs"?"cs":"s")+"|"+p[1]+"|"+(p[2]||""); if(!seen.has(k)) seen.set(k,o); CAN[o]=seen.get(k); });
  const TY=new Array(n), TP=new Array(n);
  for(let i=0;i<n;i++){ const tl=O.prov[M.id[i]]||[[1400,0]]; TY[i]=Int16Array.from(tl.map(x=>x[0])); TP[i]=Int32Array.from(tl.map(x=>CAN[x[1]])); }
  return {n,ix,ids:M.id,ar,cx,cy,EA,EB,adj,TY,TP,POL:O.pol};
}));
/* full province outlines, only when someone opens a state */
const provTopo=()=>PROVT||(PROVT=getJ("maps/prov.json"));
function ownersAt(D,y){ const own=new Int32Array(D.n); for(let i=0;i<D.n;i++){ const ys=D.TY[i]; let lo=0,hi=ys.length-1,r=-1; while(lo<=hi){ const m=(lo+hi)>>1; if(ys[m]<=y){ r=m; lo=m+1; } else hi=m-1; } own[i]=r<0?0:D.TP[i][r]; } return own; }
class GlobeProv extends GlobeGL{
  setZoom(k){ this.map.easeTo({zoom:this.z0+Math.log2(Math.max(.85,Math.min(64,k))),duration:REDUCED?0:350}); }
  resize(){ super.resize(); if(this.map) this.map.setMaxZoom(this.z0+6); }
  async addLayers(){ const m=this.map, C=this.colors(), dk=isDark(); m.setMaxZoom(this.z0+6);
    const grat={type:"FeatureCollection",features:[]}; for(let lo=-180;lo<180;lo+=10) grat.features.push({type:"Feature",properties:{m:lo%30===0?1:0},geometry:{type:"LineString",coordinates:d3.range(-85,86,5).map(la=>[lo,la])}}); for(let la=-80;la<=80;la+=10) grat.features.push({type:"Feature",properties:{m:la%30===0?1:0},geometry:{type:"LineString",coordinates:d3.range(-180,181,5).map(lo=>[lo,la])}});
    m.addSource("grat",{type:"geojson",data:grat});
    m.addLayer({id:"grat",type:"line",source:"grat",paint:{"line-color":C.grat,"line-width":.6,"line-opacity":["interpolate",["linear"],["zoom"],this.z0+1,["case",["==",["get","m"],1],1,0],this.z0+1.4,1]}});
    const D=await provLoad(); this.D=D;
    m.addSource("prov",{type:"geojson",data:"maps/prov_p.json",promoteId:"id",tolerance:.3,maxzoom:8});
    m.addSource("edge",{type:"geojson",data:"maps/prov_e.json",promoteId:"id",tolerance:.3,maxzoom:8});
    /* one engraved water line along every coast, under the land so only its sea half shows */
    m.addLayer({id:"ring0",type:"line",source:"edge",filter:["all",["==",["get","b"],0],["==",["get","s"],0]],paint:{"line-color":dk?"rgba(170,200,190,.07)":"rgba(60,95,90,.07)","line-width":7,"line-blur":2},layout:{"line-join":"round"}});
    m.addLayer({id:"prov",type:"fill",source:"prov",paint:{"fill-color":["coalesce",["feature-state","c"],C.land],"fill-antialias":true}});
    m.addSource("relief",{type:"image",url:"maps/relief_m.webp",coordinates:[[-180,85.0511],[180,85.0511],[180,-85.0511],[-180,-85.0511]]});
    m.addLayer({id:"relief",type:"raster",source:"relief",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],this.z0+1.5,dk?.7:.85,this.z0+3.5,dk?.3:.35],"raster-fade-duration":0}});
    await physP; if(PHYS){ const clean=fs=>({type:"FeatureCollection",features:fs.map(f=>({type:"Feature",properties:{sr:f.properties.sr,n:f.properties.n},geometry:f.geometry}))}); /* shapes and names only: the canvas globe hangs large caches on these features */ m.addSource("rivers",{type:"geojson",data:clean(PHYS.rivers),tolerance:.4,maxzoom:8}); m.addSource("lakes",{type:"geojson",data:clean(PHYS.lakes),maxzoom:8});
      const rop=["interpolate",["linear"],["zoom"]]; [[0,1],[.6,2],[1.2,3],[1.8,4],[2.4,5],[3,6]].forEach(([dz,sr])=>{ rop.push(this.z0+dz,["case",["<=",["get","sr"],sr],.55,0]); });
      m.addLayer({id:"rivers",type:"line",source:"rivers",paint:{"line-color":C.river,"line-opacity":rop,"line-width":["interpolate",["linear"],["zoom"],this.z0,.5,this.z0+4,1.3]},layout:{"line-cap":"round","line-join":"round"}});
      m.addLayer({id:"lakes",type:"fill",source:"lakes",paint:{"fill-color":C.ocean,"fill-outline-color":C.river}}); }
    const inner=["all",["==",["get","b"],1],["==",["get","s"],0]], st=["coalesce",["feature-state","t"],0];
    /* every inland border in one layer: between sovereigns strong, between an overlord and its dependants lighter, around land of no state faint;
       provinces only carry colour: no line is drawn inside one owner's land */
    const z=this.z0, op=(far)=>["case",["==",st,2],.85,["==",st,1],.42,["==",st,3],.28,far];
    m.addLayer({id:"bord",type:"line",source:"edge",filter:inner,paint:{"line-color":C.ink2,"line-opacity":op(0),
      "line-width":["interpolate",["linear"],["zoom"],z,["case",["==",st,2],.8,.55],z+4,["case",["==",st,2],1.7,.9],z+6,["case",["==",st,2],2.4,1.1]]},layout:{"line-join":"round"}});
    m.addLayer({id:"coast",type:"line",source:"edge",filter:["all",["==",["get","b"],0],["==",["get","s"],0]],paint:{"line-color":C.ink2,"line-opacity":.5,"line-width":.5}});
    m.addLayer({id:"cmp",type:"line",source:"edge",filter:["all",inner,["==",["get","id"],-1]],layout:{visibility:"none"},paint:{"line-color":C.wax,"line-width":1.3,"line-dasharray":[3,2],"line-opacity":.85}});
    m.addLayer({id:"pulse",type:"fill",source:"prov",layout:{visibility:"none"},paint:{"fill-color":C.wax,"fill-antialias":false,"fill-opacity":["*",["coalesce",["feature-state","pl"],0],this.pulseA||0]}});
    m.addLayer({id:"hov",type:"line",source:"edge",filter:["==",["get","id"],-1],paint:{"line-color":C.ink,"line-width":["interpolate",["linear"],["zoom"],z,1.5,z+5,2.6],"line-opacity":.9},layout:{"line-join":"round"}});
    this.layersOn=true; this.applyPhys(); if(this.year!=null){ const y=this.year; this.year=null; await this.setYear(y); } }
  restyle(){ if(!this.layersOn) return; const C=this.colors(), m=this.map, dk=isDark(); m.setPaintProperty("prov","fill-color",["coalesce",["feature-state","c"],C.land]); m.setPaintProperty("grat","line-color",C.grat);
    m.setPaintProperty("ring0","line-color",dk?"rgba(170,200,190,.07)":"rgba(60,95,90,.07)");
    for(const id of ["bord","coast"]) m.setPaintProperty(id,"line-color",C.ink2);
    m.setPaintProperty("relief","raster-opacity",["interpolate",["linear"],["zoom"],this.z0+1.5,dk?.7:.85,this.z0+3.5,dk?.3:.35]); if(m.getLayer("rivers")){ m.setPaintProperty("rivers","line-color",C.river); m.setPaintProperty("lakes","fill-color",C.ocean); }
    this.pc=null; this.paint(); }
  /* ---------- the world of one year: polities read off their provinces ---------- */
  async worldOf(y){ const D=await provLoad(), yy=Math.min(y,2019), own=ownersAt(D,yy), t=yy+.5;
    const by=new Map(); for(let i=0;i<D.n;i++){ const o=own[i]; if(!o) continue; let L=by.get(o); if(!L){ L=[]; by.set(o,L); } L.push(i); }
    const feats=[], peoples=[], fOf=new Map();
    for(const [o,L] of by){ const [src,name,ov,un,extra]=D.POL[o]; let ar=0; for(const i of L) ar+=D.ar[i];
      /* the largest connected block of provinces carries the name */
      const seen=new Set(); let best=null, bestA=-1;
      for(const s of L){ if(seen.has(s)) continue; const comp=[s]; seen.add(s); let a=0; for(let q=0;q<comp.length;q++){ const i=comp[q]; a+=D.ar[i]; for(const j of D.adj[i]) if(own[j]===o&&!seen.has(j)){ seen.add(j); comp.push(j); } } if(a>bestA){ bestA=a; best=comp; } }
      let sx=0,sy=0,sw=0; for(const i of best){ sx+=D.cx[i]*D.ar[i]; sy+=D.cy[i]*D.ar[i]; sw+=D.ar[i]; } const mx=sx/sw, my=sy/sw; let li=best[0], ld=1e9; for(const i of best){ const d=(D.cx[i]-mx)**2+(D.cy[i]-my)**2; if(d<ld){ ld=d; li=i; } }
      const props={NAME:name,a:yy,b:yy+1,ar:Math.round(ar),bl:Math.round(bestA),lp:[D.cx[li],D.cy[li]]};
      let f;
      if(src==="cs"){ props.NAME=csName(name,ov,t); props.r=name; props.o=ov; props.SUBJECTO=ov?csName(ov,"",t):null; props.st=extra&&extra!=="gap"?extra:(ov?"dependency":"independent"); f={type:"Feature",src:"cs",id:o,properties:props,provs:L}; }
      else if(src==="pp"){ if(extra) props.fx=extra; f={type:"Feature",src:"pp",id:o,properties:props,provs:L}; peoples.push(f); fOf.set(o,f); continue; }
      else { if(ov) props.SUBJECTO=ov; if(un) props.un=un; if(extra) props.fx=extra; f={type:"Feature",src:src==="gap"?"cl":"cl",id:o,properties:props,provs:L}; }
      feats.push(f); fOf.set(o,f); }
    /* neighbours, so adjacent states take different colours */
    const nb=new Map(); for(let k=0;k<D.EA.length;k++){ const b=D.EB[k]; if(b<0) continue; const oa=own[D.EA[k]], ob=own[b]; if(oa===ob||!oa||!ob) continue; if(!nb.has(oa)) nb.set(oa,new Set()); if(!nb.has(ob)) nb.set(ob,new Set()); nb.get(oa).add(ob); nb.get(ob).add(oa); }
    const ix=new Map(feats.map((f,i)=>[f.id,i])); feats.forEach(f=>{ f.all=feats; f.nbs=[...(nb.get(f.id)||[])].map(o=>ix.get(o)).filter(i=>i!=null); f.base=hashS(f.properties.NAME||"")%BASE.length; });
    /* unions (an empire with its members): named over the members' block */
    const unions=[]; if(yy<CS0){ const U=new Map(); for(const f of feats){ const u=f.properties.un; if(!u) continue; if(!U.has(u)) U.set(u,[]); U.get(u).push(f); }
      for(const [u,fs] of U){ if(fs.length<2) continue; let sx=0,sy=0,sw=0,ar=0,bl=0; for(const f of fs){ for(const i of f.provs){ sx+=D.cx[i]*D.ar[i]; sy+=D.cy[i]*D.ar[i]; sw+=D.ar[i]; } ar+=f.properties.ar; bl=Math.max(bl,f.properties.bl); }
        const mx=sx/sw,my=sy/sw; let li=-1,ld=1e9; for(const f of fs) for(const i of f.provs){ const d=(D.cx[i]-mx)**2+(D.cy[i]-my)**2; if(d<ld){ ld=d; li=i; } }
        unions.push({type:"Feature",src:"un",properties:{NAME:u,ar,bl:ar,lp:[D.cx[li],D.cy[li]]}}); } }
    return {y,src:yy>=CS0?"cs":"hb",own,feats,peoples,unions,fOf,pieces:[],hatch:[],under:[],t}; }
  async setYear(y){ const prev=this.year; this.year=y; const W=await this.worldOf(y); if(this.year!==y) return; const oldOwn=this.W&&this.W.own; this.W=W; this.feats=W.feats;
    if(!this.layersOn) return; this.paint(); this.labKey=null;
    if(prev!=null&&prev!==y&&oldOwn&&this.o.pulse!==false&&!REDUCED) this.startPulse(oldOwn);
    if(this.cmpY!=null) this.setCompare(this.cmpY);
    this.drawOverlay(); }
  paint(){ const W=this.W, m=this.map, D=this.D; if(!W||!this.layersOn||!D) return; const y=W.y, present=new Map();
    if(W.idsY!==y||!W.ids||this.colorBy!==COLORBY){ W.ids=assignColours(W.feats,y); W.idsY=y; this.colorBy=COLORBY; } fillOf.ids=W.ids;
    const unc=isDark()?"#4a4844":"#d8d4c9", col=new Map();
    for(const f of W.feats){ const c=fillOf(f,y,present); f.col=c||unc; col.set(f.id,f.col); }
    for(const f of W.peoples){ f.col=unc; col.set(f.id,unc); }
    /* provinces: only those whose colour changed */
    const pc=this.pc||(this.pc=new Array(D.n).fill(null));
    for(let i=0;i<D.n;i++){ const o=W.own[i], c=o?(col.get(o)||unc):null; if(pc[i]!==c){ pc[i]=c; if(c) m.setFeatureState({source:"prov",id:D.ids[i]},{c}); else m.removeFeatureState({source:"prov",id:D.ids[i]},"c"); } }
    /* borders: 2 between sovereigns, 1 between an overlord and its dependants or members, 3 between a state and land of no state */
    const top=o=>{ const f=W.fOf.get(o); if(!f) return 0; const p=f.properties; return f.src==="pp"?0:(p.SUBJECTO||p.NAME); };
    const et=this.et||(this.et=new Int8Array(D.EA.length));
    for(let k=0;k<D.EA.length;k++){ const b=D.EB[k]; if(b<0) continue; const oa=W.own[D.EA[k]], ob=W.own[b]; let t=0;
      if(oa!==ob){ const ta=top(oa), tb=top(ob); if(!ta&&!tb) t=0; else if(!ta||!tb) t=3; else t=ta!==tb?2:1; }
      if(et[k]!==t){ et[k]=t; m.setFeatureState({source:"edge",id:k+1},{t}); } }
    this.present=present; if(this.o.onDraw) this.o.onDraw(present,false,W); }
  startPulse(oldOwn){ const W=this.W, D=this.D, m=this.map; const ch=[]; for(let i=0;i<D.n;i++) if(oldOwn[i]!==W.own[i]&&W.own[i]) ch.push(i); if(!ch.length||ch.length>2500) return;
    if(this.plIds) for(const i of this.plIds) m.setFeatureState({source:"prov",id:D.ids[i]},{pl:0});
    for(const i of ch) m.setFeatureState({source:"prov",id:D.ids[i]},{pl:1}); this.plIds=ch;
    const t0=performance.now(); cancelAnimationFrame(this.pulseRaf); m.setLayoutProperty("pulse","visibility","visible");
    const step=()=>{ const e=performance.now()-t0, a=e<2600?.5+.5*Math.cos(e/260):0; m.setPaintProperty("pulse","fill-opacity",["*",["coalesce",["feature-state","pl"],0],Math.max(0,.12+.22*a)*(e<3200?1:0)]); if(e<3200) this.pulseRaf=requestAnimationFrame(step); else m.setLayoutProperty("pulse","visibility","none"); }; step(); }
  async setCompare(y){ this.cmpY=y; if(!this.layersOn||!this.D) return; const D=this.D, m=this.map;
    if(y==null){ m.setLayoutProperty("cmp","visibility","none"); return; }
    const own=ownersAt(D,Math.min(y,2019)), ids=[]; for(let k=0;k<D.EA.length;k++){ const b=D.EB[k]; if(b>=0&&D.EA[k]>=0&&own[D.EA[k]]!==own[b]&&own[D.EA[k]]&&own[b]) ids.push(k+1); }
    m.setFilter("cmp",["all",["==",["get","b"],1],["in",["get","id"],["literal",ids]]]); m.setLayoutProperty("cmp","visibility","visible"); }
  /* ---------- pointer ---------- */
  featAt(pt){ const m=this.map, W=this.W, D=this.D; if(!W||!D) return null; const hits=m.queryRenderedFeatures(pt,{layers:["prov"]}); if(!hits.length) return null; const i=D.ix.get(hits[0].id!=null?hits[0].id:hits[0].properties.id); if(i==null) return null; const o=W.own[i]; if(!o) return null; return W.fOf.get(o)||null; }
  setHover(f){ const m=this.map; if(!this.layersOn) return; const key=f?f.id:null; if(key===this.hk) return; this.hk=key; const D=this.D;
    if(!f||!f.provs){ m.setFilter("hov",["==",["get","id"],-1]); return; }
    /* the outline of the whole realm: edges with the realm on one side only, and its coasts */
    const own=this.W.own, o=f.id, ids=[]; for(let k=0;k<D.EA.length;k++){ const a=D.EA[k], b=D.EB[k]; if(a<0) continue; const ia=own[a]===o, ib=b>=0&&own[b]===o; if(ia!==ib||(b<0&&ia)) ids.push(k+1); }
    m.setFilter("hov",["all",["==",["get","s"],0],["in",["get","id"],["literal",ids]]]); }
  clickAt(e){ const mk=this.markerAt(e.point.x,e.point.y); if(mk&&this.o.onMarker){ this.o.onMarker(mk); return; } const f=this.featAt(e.point);
    if(!f||!this.o.onCountry) return; const ll=[e.lngLat.lng,e.lngLat.lat];
    if(f.geometry){ this.o.onCountry(f,ll,{feature:f}); return; }
    provTopo().then(t=>{ const D=this.D, G=t.objects.p.geometries; if(!t.__ix){ t.__ix=new Map(); G.forEach((g,k)=>t.__ix.set(g.properties.id,k)); }
      f.geometry=topojson.merge(t,f.provs.map(i=>G[t.__ix.get(D.ids[i])]).filter(Boolean)); this.o.onCountry(f,ll,{feature:f}); }); }
}
