/* ================= the GPU globe =================
   MapLibre GL draws land, states, borders, relief and rivers on the graphics card; changing the year only
   changes which shapes are shown (a filter), so it is instant, and dragging and zooming never redraw on the CPU.
   Names, cities and event markers are drawn on a light canvas above it, from positions the map projects. */
/* ship canals: opened to traffic 17 November 1869 (Suez) and 15 August 1914 (Panama) */
const CANALS=[{n:"Suez Canal",y:1869,dx:0,dy:0,c:[[32.304,31.265],[32.316,30.95],[32.272,30.6],[32.33,30.42],[32.4,30.33],[32.53,30.08],[32.565,29.94]]},
  {n:"Panama Canal",y:1914,dx:0,dy:0,c:[[-79.917,9.38],[-79.92,9.27],[-79.86,9.17],[-79.76,9.11],[-79.68,9.07],[-79.64,9.02],[-79.585,8.97],[-79.565,8.92]]}];
const GL_OK=(()=>{ try{ if(!window.maplibregl) return false; const c=document.createElement("canvas"); return !!(c.getContext("webgl2")||c.getContext("webgl")); }catch(e){ return false; } })();
let CHI=null; const CHUNK={};
const chunkIndex=()=>CHI||(CHI=getJ("maps/g/index.json"));
/* only the last three chunks stay in memory: a phone browser drops the page when every period is kept */
const CHUNK_KEEP=3, chunkUse=[];
function chunkLoad(s){ const i=chunkUse.indexOf(s); if(i>=0) chunkUse.splice(i,1); chunkUse.push(s); while(chunkUse.length>CHUNK_KEEP) delete CHUNK[chunkUse.shift()];
  /* shapes stay in their compact shared-border form; full outlines are unpacked only for the map's own copy, for a clicked state and for a comparison year */
  if(!CHUNK[s]) CHUNK[s]=fetch(`maps/g/c${s}.json`).then(r=>{ if(!r.ok) throw new Error("chunk "+s); return r.json(); }).then(t=>{ const features=t.objects.c.geometries.map((g,i)=>{ const p=g.properties; return {type:"Feature",id:p.id,properties:p,geometry:null,src:p.k==="p"?"pp":"cl",gi:i}; }); return {type:"FeatureCollection",features,topo:t}; }); return CHUNK[s]; }
window.__gl={CHUNK,chunkUse,JC};
const chunkGeom=(f,W)=>f.geometry||(W&&W.fc&&f.gi!=null?topojson.feature(W.fc.topo,W.fc.topo.objects.c.geometries[f.gi]).geometry:null);
const RINGS=[[11,.035],[6.5,.05],[2.8,.08]];
const yearFilter=(y)=>["all",["<=",["get","a"],y],[">",["get","b"],y]];
const CX=(hex,a)=>{ const c=d3.rgb(hex); return `rgba(${c.r},${c.g},${c.b},${a})`; };
class GlobeGL{
  constructor(host,opts={}){
    this.host=host; this.o=opts; this.markers=[]; this.cities=[]; this.lines=[]; this.W=null; this.feats=[]; this.year=null; this.cmpY=null; this.isFlat=false; this.pan=[0,0]; this.hover=null; this.flashAt=null; this.pulse=null; this.stateIds={};
    GLOBES.add(this);
    const under=document.createElement("canvas"); under.className="glov glunder"; under.setAttribute("aria-hidden","true"); host.prepend(under); this.under=under; this.uc=under.getContext("2d");
    const div=document.createElement("div"); div.className="glmap"; under.after(div); this.div=div;
    const ov=document.createElement("canvas"); ov.className="glov"; ov.setAttribute("aria-hidden","true"); div.after(ov); this.ov=ov; this.oc=ov.getContext("2d");
    this.z0=this.baseZoom();
    this.map=new maplibregl.Map({container:div,style:this.style(),center:[15,32],zoom:this.z0,minZoom:this.z0-.25,maxZoom:this.z0+Math.log2(16),attributionControl:false,dragRotate:false,pitchWithRotate:false,touchPitch:false,maxPitch:0,renderWorldCopies:false,fadeDuration:0,scrollZoom:!!opts.wheel,boxZoom:false,doubleClickZoom:true});
    this.map.touchZoomRotate.disableRotation(); if(this.map.keyboard&&this.map.keyboard.disableRotation) this.map.keyboard.disableRotation();
    this.ready=new Promise(res=>this.map.on("load",()=>{ try{ this.map.setProjection(this.projSpec()); }catch(e){} this.addLayers().then(res); }));
    this.map.on("render",()=>{ this.drawUnder(); this.drawOverlay(); });
    this.map.on("moveend",()=>{ this.labKey=null; this.drawOverlay(); });
    /* close in, swap the blended projection for a plain flat one: MapLibre cuts shapes into a fine mesh for the sphere,
       and some phone GPUs leave cracks between its pieces; the flat map draws shapes whole */
    this.map.on("zoomend",()=>{ if(this.isFlat||!this.layersOn) return; const z=this.map.getZoom(), near=z>=(this.z0||1)+3.25; if(near!==!!this.nearFlat){ this.nearFlat=near; try{ this.map.setProjection(near?{type:"mercator"}:this.projSpec()); }catch(e){} } });
    this.map.on("mousemove",e=>this.hoverAt(e));
    this.map.on("mouseout",()=>{ this.setHover(null); if(this.o.onHover) this.o.onHover(null); });
    this.map.on("dragstart",()=>{ this.setHover(null); if(this.o.onHover) this.o.onHover(null); });
    this.map.on("click",e=>this.clickAt(e));
    this.ro=new ResizeObserver(()=>this.resize()); this.ro.observe(host);
    matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>this.restyle());
    this.resize(); }
  /* our zoom 1 is the globe filling the box; MapLibre's zoom is logarithmic */
  /* the globe flattens into a plain map once you are close in: some phone GPUs drop triangles of large shapes drawn on the sphere at high zoom */
  projSpec(){ if(this.isFlat||this.nearFlat) return {type:"mercator"}; const z=this.z0||1; return {type:["interpolate",["linear"],["zoom"],z+2.2,"vertical-perspective",z+3.2,"mercator"]}; }
  baseZoom(){ const r=this.host.getBoundingClientRect(), s=Math.max(240,Math.min(r.width||600,r.height||600)); return Math.log2(s*.47*2*Math.PI/512); }
  get zoom(){ return Math.pow(2,this.map.getZoom()-this.z0); }
  set zoom(v){}
  get flat(){ return this.isFlat?1:0; } set flat(v){ this.setFlat(!!v); }
  get pxkm(){ const z=this.map.getZoom(); return 512*Math.pow(2,z)/40075; }
  colors(){ const v=css(), V=n=>v.getPropertyValue(n).trim(); return {ocean:V("--ocean")||"#C9DBDA",land:V("--land")||"#EFE6D2",ink2:V("--ink-2")||"#4a4038",panel:V("--panel")||"#F6F0E3",grat:V("--grat")||"rgba(0,0,0,.08)",river:V("--river")||"#5F8FA6",wax:V("--wax")||"#a33",chart:V("--chart")||"#F6F0E3",seaInk:V("--sea-ink")||"#3F6F7C",relief:V("--relief")||"#6B563B",tide:V("--tide")||"#2c6",verd:V("--verd")||"#476",ink:V("--ink")||"#222"}; }
  style(){ return {version:8,sources:{},layers:[{id:"space",type:"background",paint:{"background-color":"rgba(0,0,0,0)"}}],sky:{"atmosphere-blend":0}}; }
  async addLayers(){ const m=this.map, C=this.colors(), dk=isDark();
    const grat={type:"FeatureCollection",features:[]}; for(let lo=-180;lo<180;lo+=10) grat.features.push({type:"Feature",properties:{m:lo%30===0?1:0},geometry:{type:"LineString",coordinates:d3.range(-85,86,5).map(la=>[lo,la])}}); for(let la=-80;la<=80;la+=10) grat.features.push({type:"Feature",properties:{m:la%30===0?1:0},geometry:{type:"LineString",coordinates:d3.range(-180,181,5).map(lo=>[lo,la])}});
        m.addSource("grat",{type:"geojson",data:grat});
    m.addLayer({id:"grat",type:"line",source:"grat",paint:{"line-color":C.grat,"line-width":.6,"line-opacity":["interpolate",["linear"],["zoom"],this.z0+1,["case",["==",["get","m"],1],1,0],this.z0+1.4,1]}});
    const lt=await getJ("maps/landgl.json"), land=topojson.feature(lt,lt.objects.land);
    m.addSource("land",{type:"geojson",data:land,tolerance:.3});
    /* engraved water lines along every coast: four soft bands, wider ones fainter */
    RINGS.forEach(([w,a],i)=>m.addLayer({id:"ring"+i,type:"line",source:"land",paint:{"line-color":dk?`rgba(170,200,190,${a*1.2})`:`rgba(60,95,90,${a})`,"line-width":w,"line-blur":.6},layout:{"line-join":"round"}}));
    m.addLayer({id:"land",type:"fill",source:"land",paint:{"fill-color":C.land}});
    /* the states: one source for the period's polities, one for the dated record from 1886, one for land the record leaves empty */
    const empty={type:"FeatureCollection",features:[]};
    m.addSource("pol",{type:"geojson",data:empty,promoteId:"id",tolerance:.3});
    m.addSource("cs",{type:"geojson",data:empty,promoteId:"id",tolerance:.3});
    m.addSource("gap",{type:"geojson",data:empty,promoteId:"id",tolerance:.3});
    m.addSource("cmp",{type:"geojson",data:empty,tolerance:.3});
    const fillC=["coalesce",["feature-state","c"],"rgba(0,0,0,0)"], washC=["coalesce",["feature-state","w"],"rgba(0,0,0,0)"];
    m.addLayer({id:"peo",type:"fill",source:"pol",filter:["==",["get","k"],"p"],paint:{"fill-color":fillC,"fill-opacity":1}});
    m.addLayer({id:"pol",type:"fill",source:"pol",filter:["==",["get","k"],"b"],paint:{"fill-color":fillC}});
    m.addLayer({id:"cs",type:"fill",source:"cs",paint:{"fill-color":fillC}});
    m.addLayer({id:"csb",type:"line",source:"cs",paint:{"line-color":fillC,"line-width":0},layout:{"line-join":"round","visibility":"none"}});
    m.addLayer({id:"gap",type:"fill",source:"gap",paint:{"fill-color":fillC}});
    /* the atlas wash: a deeper tint just inside each border */
    const ww=["interpolate",["exponential",2],["zoom"],this.z0,3,this.z0+3,9];
    m.addLayer({id:"wash",type:"line",source:"pol",filter:["==",["get","k"],"b"],layout:{"visibility":"none"},paint:{"line-color":washC,"line-opacity":0,"line-width":ww,"line-offset":["interpolate",["exponential",2],["zoom"],this.z0,-1.5,this.z0+3,-4.5]},layout:{"line-join":"round"}});
    m.addLayer({id:"cswash",type:"line",source:"cs",paint:{"line-color":washC,"line-opacity":0,"line-width":ww,"line-offset":["interpolate",["exponential",2],["zoom"],this.z0,-1.5,this.z0+3,-4.5]},layout:{"line-join":"round"}});
    /* the land in relief */
    m.addSource("relief",{type:"image",url:"maps/relief_m.webp",coordinates:[[-180,85.0511],[180,85.0511],[180,-85.0511],[-180,-85.0511]]});
    m.addLayer({id:"relief",type:"raster",source:"relief",paint:{"raster-opacity":["interpolate",["linear"],["zoom"],this.z0+1.5,dk?.7:.85,this.z0+3.5,dk?.3:.35],"raster-fade-duration":0}});
    /* rivers and lakes, more of them as you come closer */
    await physP; if(PHYS){ const clean=fs=>({type:"FeatureCollection",features:fs.map(f=>({type:"Feature",properties:{sr:f.properties.sr,n:f.properties.n},geometry:f.geometry}))}); /* shapes and names only: the canvas globe hangs large caches on these features */ m.addSource("rivers",{type:"geojson",data:clean(PHYS.rivers),tolerance:.4,maxzoom:8}); m.addSource("lakes",{type:"geojson",data:clean(PHYS.lakes),maxzoom:8});
      const rop=["interpolate",["linear"],["zoom"]]; [[0,1],[.6,2],[1.2,3],[1.8,4],[2.4,5],[3,6]].forEach(([dz,sr])=>{ rop.push(this.z0+dz,["case",["<=",["get","sr"],sr],.55,0]); });
      m.addLayer({id:"rivers",type:"line",source:"rivers",paint:{"line-color":C.river,"line-opacity":rop,"line-width":["interpolate",["linear"],["zoom"],this.z0,.5,this.z0+4,1.3]},layout:{"line-cap":"round","line-join":"round"}});
      m.addLayer({id:"lakes",type:"fill",source:"lakes",paint:{"fill-color":C.ocean,"fill-outline-color":C.river}}); }
    /* borders: sovereign solid, dependencies dashed, unions a broader line, peoples dotted */
    const lw=["interpolate",["linear"],["zoom"],this.z0,.6,this.z0+4,1.4];
    m.addLayer({id:"peo-l",type:"line",source:"pol",filter:["==",["get","k"],"p"],paint:{"line-color":C.ink2,"line-opacity":.3,"line-width":lw,"line-dasharray":[1,2.5]}});
    m.addLayer({id:"pol-dep",type:"line",source:"pol",filter:["all",["==",["get","k"],"b"],["has","SUBJECTO"]],paint:{"line-color":C.ink2,"line-opacity":.5,"line-width":lw,"line-dasharray":[3,2]}});
    m.addLayer({id:"pol-ind",type:"line",source:"pol",filter:["all",["==",["get","k"],"b"],["!",["has","SUBJECTO"]]],paint:{"line-color":C.ink2,"line-opacity":.8,"line-width":lw}});
    m.addSource("un",{type:"geojson",data:empty,tolerance:.3});
    m.addLayer({id:"pol-u",type:"line",source:"un",paint:{"line-color":C.ink2,"line-opacity":.55,"line-width":["interpolate",["linear"],["zoom"],this.z0,1.4,this.z0+4,2.6]}});
    m.addLayer({id:"cs-dep",type:"line",source:"cs",filter:["!=",["get","st"],"independent"],paint:{"line-color":C.ink2,"line-opacity":.5,"line-width":lw,"line-dasharray":[3,2]}});
    m.addLayer({id:"cs-ind",type:"line",source:"cs",filter:["==",["get","st"],"independent"],paint:{"line-color":C.ink2,"line-opacity":.8,"line-width":lw}});
    m.addLayer({id:"gap-l",type:"line",source:"gap",filter:["!",["get","sl"]],paint:{"line-color":C.ink2,"line-opacity":.45,"line-width":lw,"line-dasharray":[2,2]}});
    m.addLayer({id:"coast",type:"line",source:"land",paint:{"line-color":C.ink2,"line-opacity":.5,"line-width":.5}});
    /* another year's borders, for comparison */
    m.addLayer({id:"cmp",type:"line",source:"cmp",paint:{"line-color":C.wax,"line-opacity":.85,"line-width":1.3,"line-dasharray":[3,2]}});
    /* land that changed hands this year, and the state under the pointer */
    m.addLayer({id:"pulse",type:"line",source:"pol",filter:["==",["get","id"],-1],paint:{"line-color":C.wax,"line-width":2.2,"line-opacity":0}});
    m.addLayer({id:"pulse-cs",type:"line",source:"cs",filter:["==",["get","id"],-1],paint:{"line-color":C.wax,"line-width":2.2,"line-opacity":0}});
    for(const s of ["pol","cs","gap"]) m.addLayer({id:"hov-"+s,type:"line",source:s,filter:["==",["get","id"],-1],paint:{"line-color":C.ink,"line-width":1.8}});
    this.layersOn=true; this.applyPhys(); if(this.year!=null){ const y=this.year; this.year=null; await this.setYear(y); } }
  restyle(){ if(!this.layersOn) return; const C=this.colors(), m=this.map, dk=isDark();  m.setPaintProperty("land","fill-color",C.land); m.setPaintProperty("grat","line-color",C.grat);
    RINGS.forEach(([w,a],i)=>m.setPaintProperty("ring"+i,"line-color",dk?`rgba(170,200,190,${a*1.2})`:`rgba(60,95,90,${a})`));
    for(const id of ["peo-l","pol-dep","pol-ind","pol-u","cs-dep","cs-ind","gap-l","coast"]) m.setPaintProperty(id,"line-color",C.ink2);
    m.setPaintProperty("relief","raster-opacity",["interpolate",["linear"],["zoom"],this.z0+1.5,dk?.7:.85,this.z0+3.5,dk?.3:.35]); if(m.getLayer("rivers")){ m.setPaintProperty("rivers","line-color",C.river); m.setPaintProperty("lakes","fill-color",C.ocean); }
    this.paint(); }
  applyPhys(){ if(!this.layersOn) return; const on=SHOWPHYS&&this.o.relief!==false; for(const id of ["relief","rivers","lakes"]) if(this.map.getLayer(id)) this.map.setLayoutProperty(id,"visibility",on?"visible":"none"); }
  /* ---------- the world of one year ---------- */
  async worldOf(y){
    if(y>=CS0){ const [cs,gaps]=await Promise.all([csLoad(),gapsLoad()]); const yy=Math.min(y,2019), t=yy+.5, feats=[];
      for(const f of cs){ const p=f.properties; if(p.a<=t&&t<p.b){ p.NAME=csName(p.r,p.o,t); p.SUBJECTO=p.o?csName(p.o,"",t):null; feats.push(f); } }
      const extra=[]; gaps.forEach((g,i)=>{ const q=g.properties; g.gid=100000+i; if(!(q.a<=yy&&yy<q.b)) return;
        if(q.own){ const o=feats.find(f=>f.properties.r===q.own[0]&&(f.properties.o||"")===(q.own[1]||"")); if(o){ const c={type:"Feature",geometry:g.geometry,src:"cs",gapOf:o,cid:o.cid,gid:g.gid};
            if(q.NAME){ c.ownName=q.NAME; c.dep=!!q.dep; c.properties=Object.assign({},o.properties,{NAME:q.NAME,lp:q.lp,ar:q.ar,bl:q.bl,st:q.dep?"dependency":o.properties.st,SUBJECTO:q.dep?o.properties.NAME:o.properties.SUBJECTO}); } else c.properties=o.properties;
            extra.push(c); return; } }
        if(q.NAME){ g.src="gap"; extra.push(g); } });
      return {y,src:"cs",feats:feats.concat(extra),unions:[],peoples:[],pieces:[],hatch:[],under:[],t}; }
    const I=await chunkIndex(), ch=I.chunks.find(c=>y>=c[0]&&y<c[1])||I.chunks[I.chunks.length-1], fc=await chunkLoad(ch[0]);
    const act=fc.features.filter(f=>f.properties.a<=y&&y<f.properties.b);
    const feats=act.filter(f=>f.src==="cl"), peoples=act.filter(f=>f.src==="pp");
    /* a peoples' name is shown only where no state is drawn over the spot it would sit */
    const bb=f=>f.__bb||(f.__bb=d3.geoBounds(f)), inB=(b,p)=>p[1]>=b[0][1]&&p[1]<=b[1][1]&&(b[0][0]<=b[1][0]?p[0]>=b[0][0]&&p[0]<=b[1][0]:p[0]>=b[0][0]||p[0]<=b[1][0]);
    for(const q of peoples){ const lp=q.properties.lp; q.covered=!lp; } /* each period's peoples are the land outside its states, so their names never sit under a state */
    /* unions (an empire with its members): merged from the members drawn this year, so the outer border is exactly theirs */
    const byU=new Map(); for(const f of feats){ const u=f.properties.un; if(!u) continue; if(!byU.has(u)) byU.set(u,[]); byU.get(u).push(f); }
    const G=fc.topo.objects.c.geometries, unions=[];
    for(const [u,fs] of byU){ if(fs.length<2) continue; const geom=topojson.merge(fc.topo,fs.map(f=>G[f.gi])); let ar=0; for(const f of fs) ar+=f.properties.ar||0;
      let big=null, ba=0; for(const pc of (geom.type==="MultiPolygon"?geom.coordinates:[geom.coordinates])){ const a=d3.geoArea({type:"Polygon",coordinates:pc}); if(a<2*Math.PI&&a>ba){ ba=a; big=pc; } }
      let lp=big?d3.geoCentroid({type:"Polygon",coordinates:big}):null; if(!lp||!d3.geoContains({type:"Polygon",coordinates:big},lp)) lp=fs.slice().sort((a,b)=>(b.properties.ar||0)-(a.properties.ar||0))[0].properties.lp;
      unions.push({type:"Feature",src:"un",geometry:geom,properties:{NAME:u,ar,bl:Math.round(ba*40589641),lp}}); }
    return {y,src:"hb",chunk:ch[0],fc,feats,unions,peoples,pieces:[],hatch:[],under:[],nchg:0}; }
  async setYear(y){ const prev=this.year; this.year=y; const W=await this.worldOf(y); if(this.year!==y) return; this.W=W; this.feats=W.feats;
    if(!this.layersOn) return; const m=this.map;
    if(W.src==="hb"){ { /* the map holds only this period's shapes: a period is the span over which no border in the record changes */
        const act=W.fc.features.filter(f=>f.properties.a<=y&&y<f.properties.b); let a0=-1e9,b0=1e9; for(const f of act){ if(f.properties.a>a0) a0=f.properties.a; if(f.properties.b<b0) b0=f.properties.b; }
        const pk=W.chunk+":"+a0+":"+b0; if(this.polKey!==pk){ const G=W.fc.topo.objects.c.geometries; m.getSource("pol").setData(topojson.feature(W.fc.topo,{type:"GeometryCollection",geometries:act.map(f=>G[f.gi])})); this.polKey=pk; } } m.setFilter("pol",["all",["==",["get","k"],"b"],yearFilter(y)]); m.setFilter("peo",["all",["==",["get","k"],"p"],yearFilter(y)]); m.setFilter("wash",["all",["==",["get","k"],"b"],yearFilter(y)]);
      m.setFilter("peo-l",["all",["==",["get","k"],"p"],yearFilter(y)]); m.setFilter("pol-dep",["all",["==",["get","k"],"b"],["has","SUBJECTO"],yearFilter(y)]); m.setFilter("pol-ind",["all",["==",["get","k"],"b"],["!",["has","SUBJECTO"]],yearFilter(y)]); m.getSource("un").setData({type:"FeatureCollection",features:W.unions.map(f=>({type:"Feature",properties:{},geometry:f.geometry}))});
      for(const id of ["cs","csb","cswash","cs-dep","cs-ind","gap","gap-l"]) m.setLayoutProperty(id,"visibility","none"); for(const id of ["pol","peo","wash","peo-l","pol-dep","pol-ind","pol-u"]) m.setLayoutProperty(id,"visibility","visible"); }
    else { if(!this.csSet){ const cs=await csLoad(), gaps=await gapsLoad(); m.getSource("cs").setData({type:"FeatureCollection",features:cs.map(f=>({type:"Feature",geometry:f.geometry,properties:{id:f.cid+1,a:f.properties.a,b:f.properties.b,st:f.properties.st}}))});
        m.getSource("gap").setData({type:"FeatureCollection",features:gaps.map((g,i)=>({type:"Feature",geometry:g.geometry,properties:{id:100000+i,a:g.properties.a,b:g.properties.b,sl:!!(g.properties.own&&!g.properties.NAME)}}))}); this.csSet=true; }
      const t=W.t, yy=Math.min(y,2019), f2=["all",["<=",["get","a"],t],[">",["get","b"],t]], fg=["all",["<=",["get","a"],yy],[">",["get","b"],yy]];
      for(const id of ["cs","csb","cswash"]) m.setFilter(id,f2); m.setFilter("cs-dep",["all",["!=",["get","st"],"independent"],f2]); m.setFilter("cs-ind",["all",["==",["get","st"],"independent"],f2]); m.setFilter("gap",fg); m.setFilter("gap-l",["all",["!",["get","sl"]],fg]);
      for(const id of ["pol","peo","wash","peo-l","pol-dep","pol-ind","pol-u"]) m.setLayoutProperty(id,"visibility","none"); for(const id of ["cs","csb","cswash","cs-dep","cs-ind","gap","gap-l"]) m.setLayoutProperty(id,"visibility","visible"); }
    this.paint(); this.labKey=null;
    if(prev!=null&&prev!==y&&this.o.pulse!==false) this.startPulse(y,prev);
    this.drawOverlay(); }
  /* colours, computed by the same rules as everywhere else in the atlas and handed to the map as feature state */
  paint(){ const W=this.W, m=this.map; if(!W||!this.layersOn) return; const y=W.y, present=new Map();
    const src=W.src==="hb"?"pol":"cs";
    if(W.src==="hb"){ const ix=new Map(W.feats.map((f,i)=>[f.id,i])); W.feats.forEach(f=>{ f.all=W.feats; f.nbs=(f.properties.nb||[]).map(id=>ix.get(id)).filter(i=>i!=null); f.base=hashS(f.properties.NAME)%BASE.length; }); }
    if(W.idsY!==y||!W.ids||this.colorBy!==COLORBY){ W.ids=assignColours(W.feats.filter(f=>!f.gapOf),y); W.idsY=y; this.colorBy=COLORBY; } fillOf.ids=W.ids;
    const next={pol:new Map(),cs:new Map(),gap:new Map()};
    for(const f of W.feats){ const col=fillOf(f,y,present); if(!col) continue; const st={c:col,w:darker(col)};
      if(W.src==="hb") next.pol.set(f.id,st); else if(f.gid!=null) next.gap.set(f.gid,st); else next.cs.set(f.cid+1,st); }
    /* land outside any state: one quiet neutral, as an uncolonised province on a strategy map */ const unc=isDark()?"#4a4844":"#d8d4c9"; for(const f of W.peoples) next.pol.set(f.id,{c:unc,w:unc});
    for(const s of ["pol","cs","gap"]){ const old=this.stateIds[s]||new Set(); for(const id of old) if(!next[s].has(id)) m.removeFeatureState({source:s,id}); for(const [id,st] of next[s]) m.setFeatureState({source:s,id},st); this.stateIds[s]=new Set(next[s].keys()); }
    this.present=present; if(this.o.onDraw) this.o.onDraw(present,false,W); }
  draw(){ this.applyPhys(); this.paint(); this.labKey=null; this.drawOverlay(); }
  place(){} resize(){ const r=this.host.getBoundingClientRect(), d=Math.min(2,devicePixelRatio||1); this.w=r.width; this.h=r.height; this.dpr=d; for(const cv of [this.ov,this.under]){ cv.width=Math.round(r.width*d); cv.height=Math.round(r.height*d); cv.style.width=r.width+"px"; cv.style.height=r.height+"px"; } const z0=this.baseZoom(); if(this.map){ const k=this.zoom; this.z0=z0; this.map.setMinZoom(z0-.25); this.map.setMaxZoom(z0+Math.log2(16)); this.map.resize(); try{ if(this.map.loaded()) this.map.setProjection(this.projSpec()); }catch(e){} if(isFinite(k)) this.map.jumpTo({zoom:z0+Math.log2(Math.max(1,k))}); } this.labKey=null; this.drawOverlay(); }
  setZoom(k){ this.map.easeTo({zoom:this.z0+Math.log2(Math.max(.85,Math.min(16,k))),duration:REDUCED?0:350}); }
  rotateTo(lon,lat,animate=true,zoom){ const o={center:[lon,Math.max(-80,Math.min(80,lat))]}; if(zoom) o.zoom=this.z0+Math.log2(zoom); if(!animate||REDUCED) this.map.jumpTo(o); else this.map.easeTo(Object.assign(o,{duration:900})); }
  setFlat(on){ this.isFlat=!!on; if(this.layersOn||this.map.loaded()){ try{ this.map.setProjection(this.projSpec()); }catch(e){} } this.labKey=null; this.drawOverlay(); }
  async setCompare(y){ this.cmpY=y; if(!this.layersOn) return; if(y==null){ this.map.getSource("cmp").setData({type:"FeatureCollection",features:[]}); return; } const W=await this.worldOf(y); if(this.cmpY!==y) return; const fs=W.feats.filter(f=>!f.gapOf||f.ownName); this.map.getSource("cmp").setData({type:"FeatureCollection",features:fs.map(f=>({type:"Feature",properties:{},geometry:chunkGeom(f,W)}))}); }
  setMarkers(ms){ this.markers=ms||[]; this.drawOverlay(); }
  setCities(cs){ this.cities=cs||[]; this.labKey=null; this.drawOverlay(); }
  setLines(ls){ this.lines=ls||[]; this.drawOverlay(); }
  flash(c){ this.flashAt={lon:c.lon,lat:c.lat,t0:performance.now()}; if(c.lon!=null) this.rotateTo(c.lon,c.lat,true); const tick=()=>{ if(!this.flashAt) return; this.drawOverlay(); if(performance.now()-this.flashAt.t0<2600) requestAnimationFrame(tick); else { this.flashAt=null; this.drawOverlay(); } }; requestAnimationFrame(tick); }
  startPulse(y,prev){ const W=this.W; if(!W) return; let ids=[], layer;
    if(W.src==="hb"){ layer="pulse"; ids=W.feats.filter(f=>f.properties.a===y&&y>1400).map(f=>f.id); }
    else { layer="pulse-cs"; ids=W.feats.filter(f=>!f.gapOf&&Math.floor(f.properties.a)===y&&f.properties.a>CS0+.01).map(f=>f.cid+1); }
    if(!ids.length||REDUCED) return; const m=this.map; m.setFilter(layer,["in",["get","id"],["literal",ids]]); const t0=performance.now(); cancelAnimationFrame(this.pulseRaf);
    const step=()=>{ const e=performance.now()-t0, a=e<2600?.5+.5*Math.cos(e/260):0; m.setPaintProperty(layer,"line-opacity",Math.max(0,.35+.55*a)*(e<3200?1:0)); if(e<3200) this.pulseRaf=requestAnimationFrame(step); else m.setFilter(layer,["==",["get","id"],-1]); }; step(); }
  /* ---------- pointer ---------- */
  featAt(pt){ const m=this.map, L=this.W&&this.W.src==="hb"?["pol","peo"]:["cs","gap"]; const hits=m.queryRenderedFeatures(pt,{layers:L.filter(l=>m.getLayer(l))}); if(!hits.length) return null; const h=hits.find(x=>x.layer.id!=="peo")||hits[0];
    const W=this.W; if(!W) return null; if(W.src==="hb") return (h.layer.id==="peo"?W.peoples:W.feats).find(f=>f.id===h.id)||null;
    if(h.layer.id==="gap"){ const f=W.feats.find(f=>f.gid===h.id); return f?(f.gapOf&&!f.ownName?f.gapOf:f):null; } return W.feats.find(f=>!f.gapOf&&f.cid+1===h.id)||null; }
  markerAt(x,y){ for(const m of this.markers){ const p=this.proj([m.lon,m.lat]); if(p&&Math.hypot(p[0]-x,p[1]-y)<(m.tier===3?6:10)) return m; } return null; }
  hoverAt(e){ const mk=this.markerAt(e.point.x,e.point.y); if(mk){ this.setHover(null); this.map.getCanvas().style.cursor="pointer"; if(this.o.onHover) this.o.onHover({marker:mk},e.originalEvent); return; }
    const f=this.featAt(e.point); this.setHover(f); this.map.getCanvas().style.cursor=f?"pointer":""; if(this.o.onHover) this.o.onHover(f?{feature:f,ll:[e.lngLat.lng,e.lngLat.lat],gap:f.src==="gap"}:null,e.originalEvent); }
  setHover(f){ const m=this.map; if(!this.layersOn) return; const key=f?(f.src==="cs"?"cs:"+(f.cid+1):f.src==="gap"?"gap:"+f.gid:"pol:"+f.id):null; if(key===this.hk) return; this.hk=key;
    for(const s of ["pol","cs","gap"]) m.setFilter("hov-"+s,["==",["get","id"],key&&key.startsWith(s+":")?+key.split(":")[1]:-1]); }
  clickAt(e){ const mk=this.markerAt(e.point.x,e.point.y); if(mk&&this.o.onMarker){ this.o.onMarker(mk); return; } const f=this.featAt(e.point); if(f&&!f.geometry) f.geometry=chunkGeom(f,this.W); if(f&&this.o.onCountry) this.o.onCountry(f,[e.lngLat.lng,e.lngLat.lat],{feature:f}); }
  /* ---------- the overlay: names, cities, events ---------- */
  proj(ll){ const m=this.map; if(!this.isFlat){ const c=m.getCenter(); if(d3.geoDistance(ll,[c.lng,c.lat])>Math.PI/2-.22) return null; } const p=m.project(ll); return [p.x,p.y]; }
  visible(ll){ return !!this.proj(ll); }
  drawUnder(){ const c=this.uc, d=this.dpr||1, w=this.w, h=this.h; if(!w) return; const C=this.colors(); c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,this.under.width,this.under.height); c.setTransform(d,0,0,d,0,0); c.fillStyle=C.ocean;
    if(this.isFlat){ const a=this.map.project([-180,85.05]), b=this.map.project([180,-85.05]); c.fillRect(a.x,a.y,b.x-a.x,b.y-a.y); return; }
    /* the globe's visible radius on screen, found where the horizon is (the camera's perspective makes it a little smaller than the sphere) */
    const ce=this.map.getCenter(), P0=this.map.project(ce); let R=0; for(let t=60;t<=90;t+=1.5){ const q=d3.geoRotation([-ce.lng,-ce.lat]).invert([-t,0]); if(!q) continue; const p=this.map.project(q); const r=Math.hypot(p.x-P0.x,p.y-P0.y); if(r>R) R=r; }
    if(!R) R=512*Math.pow(2,this.map.getZoom())/(2*Math.PI); c.beginPath(); c.arc(P0.x,P0.y,R+.5,0,7); c.fill();
    const g=c.createRadialGradient(P0.x-R*.35,P0.y-R*.4,R*.1,P0.x,P0.y,R*1.05); g.addColorStop(0,isDark()?"rgba(255,255,255,.05)":"rgba(255,255,255,.3)"); g.addColorStop(1,"rgba(0,0,0,0)"); c.fillStyle=g; c.fill(); }
  drawOverlay(){ if(this.raf) return; this.raf=requestAnimationFrame(()=>{ this.raf=0; this.renderOverlay(); }); }
  renderOverlay(){ const c=this.oc, d=this.dpr||1, w=this.w, h=this.h; if(!w) return; c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,this.ov.width,this.ov.height); c.setTransform(d,0,0,d,0,0);
    const C=this.colors(), k=this.zoom, pxkm=this.pxkm, boxes=[]; const free=(x0,y0,x1,y1)=>{ if(x0<4||y0<4||x1>w-4||y1>h-4) return false; for(const b of boxes) if(x0<b[2]&&x1>b[0]&&y0<b[3]&&y1>b[1]) return false; boxes.push([x0,y0,x1,y1]); return true; };
    boxes.push([w-54,0,w,150]); boxes.push([0,0,70,70]);
    c.textBaseline="middle"; c.lineJoin="round";
    const text=(t,x,y,font,ink,halo,alpha=.9,ls=0)=>{ c.font=font; if("letterSpacing" in c) c.letterSpacing=ls+"px"; c.lineWidth=3; c.strokeStyle=halo; c.globalAlpha=alpha*.6; c.strokeText(t,x,y); c.globalAlpha=alpha; c.fillStyle=ink; c.fillText(t,x,y); c.globalAlpha=1; if("letterSpacing" in c) c.letterSpacing="0px"; };
    /* threads of an arc */
    const DASH={Necessary:[],Sufficient:[],Contributing:[8,6],Contested:[2,5],Coincident:[8,6],none:[]};
    for(const L of this.lines){ c.save(); c.beginPath(); let pen=false; const pts=[]; for(let i=0;i<L.coords.length-1;i++){ const it=d3.geoInterpolate(L.coords[i],L.coords[i+1]); for(let j=0;j<=12;j++) pts.push(it(j/12)); } for(const q of pts){ const p=this.proj(q); if(!p){ pen=false; continue; } if(pen) c.lineTo(p[0],p[1]); else { c.moveTo(p[0],p[1]); pen=true; } }
      c.strokeStyle=L.grade==="Coincident"?C.wax:(L.grade==="none"?C.tide:C.verd); c.lineWidth=L.strong?2.4:1.6; c.globalAlpha=L.strong?.95:.6; c.setLineDash(DASH[L.grade]||[]); c.stroke(); c.restore(); }
    /* ship canals, drawn from the year they opened */
    for(const K of CANALS){ if(this.year==null||this.year<K.y) continue; const pts=K.c.map(q=>this.proj(q)); if(pts.some(p=>!p)) continue;
      c.save(); c.beginPath(); pts.forEach((p,i)=>i?c.lineTo(p[0],p[1]):c.moveTo(p[0],p[1])); c.lineCap="round";
      c.strokeStyle=C.ink; c.globalAlpha=.75; c.lineWidth=Math.min(6,2.6+k*.25); c.stroke(); c.strokeStyle=C.ocean; c.globalAlpha=1; c.lineWidth=Math.min(3.6,1.2+k*.18); c.stroke();
      const m=pts[Math.floor(pts.length/2)]; c.beginPath(); c.moveTo(m[0],m[1]-5); c.lineTo(m[0]+4,m[1]); c.lineTo(m[0],m[1]+5); c.lineTo(m[0]-4,m[1]); c.closePath(); c.fillStyle=C.chart; c.fill(); c.lineWidth=1.3; c.strokeStyle=C.ink; c.stroke(); c.restore();
      if(k>=1.3){ const f="italic 11.5px Inter,system-ui,sans-serif"; c.font=f; const t=`${K.n}, ${K.y}`, tw=c.measureText(t).width, x=m[0]+8+K.dx*(tw+16), y=m[1]+K.dy;
        if(free(Math.min(x,x+tw)-2,y-7,Math.max(x,x+tw)+2,y+7)){ c.textAlign="left"; text(t,x,y,f,C.ink,C.chart,.92); } } }
    /* event markers first so names make room for them */
    const ms=this.markers.map(m=>({m,p:this.proj([m.lon,m.lat])})).filter(x=>x.p);
    for(const {m,p} of ms){ const r=m.kind==="site"?3:m.tier===1?6:m.tier===2?4.5:3; boxes.push([p[0]-r-2,p[1]-r-2,p[0]+r+2,p[1]+r+2]); }
    if(this.o.labels){ const lab=ms.filter(x=>x.m.label||x.m.cur); for(const {m,p} of lab){ const t=m.label||""; if(!t) continue; c.font="500 13px Inter,system-ui,sans-serif"; const tw=c.measureText(t).width; if(free(p[0]+9,p[1]-9,p[0]+12+tw,p[1]+9)){ c.textAlign="left"; text(t,p[0]+11,p[1],"500 13px Inter,system-ui,sans-serif",C.ink,C.chart,.95); } } }
    if(this.o.labels!==false&&this.W){
      /* sea names, then the names of states sized to their land, then mountains and deserts when close */
      const sm=Math.max(.72,Math.min(1,Math.min(w,h)/640));
      if(SHOWPHYS&&PPTS) for(const L of PPTS.labels){ let fs=0, sp=0, a=.7; if(L.k==="ocean"&&k<5) { fs=13.5*sm; sp=.32; } else if(L.k==="sea"&&k>=(L.sr<=1?1.8:2.8)){ fs=11*sm; sp=.22; } else if(/gulf|bay|strait|channel/.test(L.k)&&k>=(L.sr<=2?3.2:4.5)){ fs=10*sm; sp=.12; a=.65; } if(!fs) continue;
        const p=this.proj([L.lon,L.lat]); if(!p) continue; const t=L.n.toUpperCase(), f=`italic ${fs.toFixed(1)}px 'Libre Caslon Text',Georgia,serif`; c.font=f; if("letterSpacing" in c) c.letterSpacing=(fs*sp).toFixed(1)+"px"; const tw=c.measureText(t).width; if("letterSpacing" in c) c.letterSpacing="0px"; if(!free(p[0]-tw/2,p[1]-fs/2,p[0]+tw/2,p[1]+fs/2)) continue; c.textAlign="center"; text(t,p[0],p[1],f,C.seaInk,C.ocean,a,fs*sp); }
      const W=this.W, y=W.y, cand=[];
      for(const f of W.unions) cand.push({f,u:1}); for(const f of W.feats) if(!(f.gapOf&&!f.ownName)) cand.push({f}); if(k>=2.2) for(const f of W.peoples) if(!f.covered) cand.push({f,ppl:1});
      cand.sort((a,b)=>((b.u?3:1)*(b.f.properties.bl||b.f.properties.ar||0))-((a.u?3:1)*(a.f.properties.bl||a.f.properties.ar||0)));
      const seen=new Set();
      for(const {f,u,ppl} of cand){ const pp=f.properties; if(!pp.lp||!pp.NAME) continue; const span=Math.sqrt(pp.bl||pp.ar||0)*pxkm; if(span<(u?90:34)) continue; if(u&&k>2.6) continue;
        const name=pp.NAME; if(seen.has(name)) continue; const p=this.proj(pp.lp); if(!p) continue;
        const dep=f.src==="cs"?pp.st!=="independent":!!pp.SUBJECTO, ital=dep||ppl||f.src==="pp";
        let fs=Math.max(7.5,Math.min(u?20:22,span/(u?9:7.5))); const up=(fs>=12.5&&!ital)||u, whisper=fs<9.5||ital&&!u;
        const font=`${ital?"italic ":""}${fs.toFixed(1)}px 'Libre Caslon Text',Georgia,serif`; c.font=font; const ls=up?fs*(u?.2:.14):0; if("letterSpacing" in c) c.letterSpacing=ls.toFixed(1)+"px";
        const txt=up?name.toUpperCase():name; let lines=[txt], tw=c.measureText(txt).width; if(txt.includes(" ")&&tw>span*.8){ const ws=txt.split(" "); let best=null; for(let i=1;i<ws.length;i++){ const A=ws.slice(0,i).join(" "), B=ws.slice(i).join(" "); const mm=Math.max(c.measureText(A).width,c.measureText(B).width); if(!best||mm<best[0]) best=[mm,[A,B]]; } if(best&&best[0]<tw*.8){ lines=best[1]; tw=best[0]; } }
        if("letterSpacing" in c) c.letterSpacing="0px"; if(tw>span*1.15&&!u) continue;
        const lh=fs*1.12, hh=lh*lines.length; if(!free(p[0]-tw/2-2,p[1]-hh/2-1,p[0]+tw/2+2,p[1]+hh/2+1)) continue; seen.add(name);
        let ink=C.ink2; if(!u&&f.col) ink=labelInk(f.col); else if(!u){ const st=f.src==="hb"||f.src==="cl"?(this.map.getFeatureState({source:"pol",id:f.id})||{}):null; if(st&&st.c) ink=labelInk(st.c); }
        c.textAlign="center"; lines.forEach((l,i)=>text(l,p[0],p[1]-hh/2+lh*(i+.5),font,ink,C.chart,u?.62:(whisper?.7:.9),ls)); }
      if(SHOWPHYS&&PPTS) for(const L of PPTS.labels){ let fs=0; if(L.k==="mtn"&&k>=(L.sr<=2?2.2:L.sr<=3?3.4:5)) fs=L.sr<=2?10.5:9.5; else if((L.k==="desert"||L.k==="plateau")&&k>=(L.sr<=2?2.6:L.sr<=3?3.8:5.5)) fs=L.sr<=2?10.5:9.5; if(!fs) continue;
        const p=this.proj([L.lon,L.lat]); if(!p) continue; const t=L.n.toUpperCase(), f=`italic ${fs}px 'Libre Caslon Text',Georgia,serif`; c.font=f; if("letterSpacing" in c) c.letterSpacing=(fs*.3).toFixed(1)+"px"; const tw=c.measureText(t).width; if("letterSpacing" in c) c.letterSpacing="0px"; if(!free(p[0]-tw/2,p[1]-fs/2,p[0]+tw/2,p[1]+fs/2)) continue; c.textAlign="center"; text(t,p[0],p[1],f,C.relief,C.chart,.62,fs*.3); }
      /* capitals and cities */
      for(const ct of this.cities){ const p=this.proj([ct.lon,ct.lat]); if(!p) continue; c.font="11.5px Inter,system-ui,sans-serif"; const tw=c.measureText(ct.name).width; if(!free(p[0]-3,p[1]-7,p[0]+8+tw,p[1]+7)) continue; c.beginPath(); c.arc(p[0],p[1],2.6,0,7); c.fillStyle=C.chart; c.fill(); c.lineWidth=1.2; c.strokeStyle=C.ink; c.stroke(); c.textAlign="left"; text(ct.name,p[0]+6,p[1],"11.5px Inter,system-ui,sans-serif",C.ink,C.chart,.9); } }
    /* event markers on top */
    for(const {m,p} of ms){ const r=m.kind==="site"?3:m.tier===1?6:m.tier===2?4.5:3; c.beginPath(); c.arc(p[0],p[1],r,0,7); c.fillStyle=m.kind==="site"?C.verd:(m.tier===3?C.ink2:(m.dim?C.ink2:C.wax)); c.globalAlpha=m.dim?.5:1; c.fill(); c.lineWidth=1.4; c.strokeStyle=C.chart; c.stroke(); c.globalAlpha=1; if(m.cur){ c.beginPath(); c.arc(p[0],p[1],r+4,0,7); c.strokeStyle=C.wax; c.lineWidth=1.6; c.stroke(); } }
    if(this.flashAt){ const e=performance.now()-this.flashAt.t0, p=this.proj([this.flashAt.lon,this.flashAt.lat]); if(p){ for(let i=0;i<3;i++){ const r=((e/14)+i*30)%90; c.beginPath(); c.arc(p[0],p[1],r,0,7); c.strokeStyle=C.wax; c.globalAlpha=Math.max(0,1-r/90)*.8; c.lineWidth=1.6; c.stroke(); } c.globalAlpha=1; } }
    c.textAlign="left"; }
  destroy(){ try{ this.ro.disconnect(); this.map.remove(); }catch(e){} GLOBES.delete(this); }
}
