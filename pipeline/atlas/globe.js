/* ---------- the world map: data ---------- */
const MAPY=[1400,1500,1530,1600,1650,1700,1715,1783,1800,1815,1880,1900,1914,1920,1930,1938,1945,1960,1994,2000,2010];
const CS0=1886;
const mapYear=y=>{ let b=MAPY[0]; for(const m of MAPY) if(m<=y) b=m; return b; };
const JC={}; const getJ=u=>JC[u]||(JC[u]=fetch(u).then(r=>{ if(!r.ok) throw new Error(u); return r.json(); }));
let LAND=null;
let LANDW=null, LANDLO=null, LANDLOW=null;
const fixLand=L=>{ const fixP=p=>{ const a=d3.geoArea({type:"Polygon",coordinates:p}); return a>2*Math.PI?p.map(r=>r.slice().reverse()):p; }; for(const f of (L.type==="FeatureCollection"?L.features:[L])){ const g=f.geometry; if(!g) continue; if(g.type==="Polygon") g.coordinates=fixP(g.coordinates); else if(g.type==="MultiPolygon") g.coordinates=g.coordinates.map(fixP); } return L; };
const bigLand=L=>{ const gs=L.type==="FeatureCollection"?L.features.map(f=>f.geometry):[L.geometry]; return {type:"MultiPolygon",coordinates:gs.flatMap(g=>g.type==="MultiPolygon"?g.coordinates:[g.coordinates]).filter(p=>{ const a=d3.geoArea({type:"Polygon",coordinates:p}); return Math.min(a,4*Math.PI-a)>4e-5; })}; };
getJ("maps/landlo.json").then(t=>{ LANDLO=fixLand(topojson.feature(t,t.objects.land)); LANDLOW=bigLand(LANDLO); GLOBES.forEach(g=>g.draw()); }).catch(()=>{});
const landP=getJ("maps/land.json").then(t=>{ LAND=fixLand(topojson.feature(t,t.objects.land)); LAND.__src={t,make:tt=>fixLand(topojson.feature(tt,tt.objects.land))}; const gs=LAND.type==="FeatureCollection"?LAND.features.map(f=>f.geometry):[LAND.geometry]; const polys=gs.flatMap(g=>g.type==="MultiPolygon"?g.coordinates:[g.coordinates]).filter(p=>{ const a=d3.geoArea({type:"Polygon",coordinates:p}); return Math.min(a,4*Math.PI-a)>4e-5; }); LANDW={type:"MultiPolygon",coordinates:polys}; LANDW.__src={t,make:tt=>bigLand(fixLand(topojson.feature(tt,tt.objects.land)))}; window.__L=[LAND,LANDW]; }).catch(()=>{});
/* every polygon must wind so that it encloses the smaller side of the sphere */
function rewind(f){ const g=f.geometry; if(!g) return f; const fixP=p=>d3.geoArea({type:"Polygon",coordinates:p})>2*Math.PI?p.map(r=>r.slice().reverse()):p; if(g.type==="Polygon") g.coordinates=fixP(g.coordinates); else if(g.type==="MultiPolygon") g.coordinates=g.coordinates.map(fixP); return f; }
const decRing=(r,st)=>{ if(r.length<12) return r; const o=[]; for(let i=0;i<r.length-1;i+=st) o.push(r[i]); o.push(r[r.length-1]); return o.length<4?r:o; };
function lowOf(g,st=4){ if(!g) return g; if(g.__lo) return g.__lo; const geo=g.geometry||g; let out;
  if(geo.type==="Polygon") out={type:"Polygon",coordinates:geo.coordinates.map(r=>decRing(r,st))};
  else if(geo.type==="MultiPolygon") out={type:"MultiPolygon",coordinates:geo.coordinates.map(p=>p.map(r=>decRing(r,st)))};
  else if(geo.type==="FeatureCollection") out={type:"FeatureCollection",features:geo.features.map(f=>({type:"Feature",properties:{},geometry:lowOf(f.geometry,st)}))};
  else out=geo; g.__lo=out; return out; }
/* fast globe projection: each vertex becomes a unit vector once (long edges densified along the great circle),
   then every frame is a rotation and a scale; polygons that cross the horizon go through d3 for exact clipping */
const DR=Math.PI/180;
function xyzOf(r){ if(r.__x) return r.__x; const out=[]; let px=0,py=0,pz=0,has=false;
  for(const c of r){ const l=c[0]*DR, p=c[1]*DR, cp=Math.cos(p), x=cp*Math.cos(l), y=cp*Math.sin(l), z=Math.sin(p);
    if(has){ const dot=Math.max(-1,Math.min(1,px*x+py*y+pz*z)), ang=Math.acos(dot); if(ang>.5*DR&&ang<Math.PI-1e-6){ const n=Math.ceil(ang/(.5*DR)), s=Math.sin(ang); for(let i=1;i<n;i++){ const t=i/n, a=Math.sin((1-t)*ang)/s, b=Math.sin(t*ang)/s; out.push(px*a+x*b,py*a+y*b,pz*a+z*b); } } }
    out.push(x,y,z); px=x; py=y; pz=z; has=true; }
  return r.__x=Float64Array.from(out); }
function fastPath(geo,p,R,gp){ /* R = {cl,sl,cf,sf,k,tx,ty}; returns nothing; writes into Path2D p */
  const vis=a=>{ let pos=0,neg=0; for(let i=0;i<a.length;i+=3){ const x=a[i],y=a[i+1],z=a[i+2], x1=x*R.cl-y*R.sl, X=x1*R.cf-z*R.sf; if(X>1e-9) pos++; else neg++; if(pos&&neg) return 0; } return pos?1:-1; };
  const put=(a,close)=>{ for(let i=0;i<a.length;i+=3){ const x=a[i],y=a[i+1],z=a[i+2], x1=x*R.cl-y*R.sl, y1=x*R.sl+y*R.cl, Z=z*R.cf+x1*R.sf, sx=R.tx+R.k*y1, sy=R.ty-R.k*Z; if(i) p.lineTo(sx,sy); else p.moveTo(sx,sy); } };  /* rings are already closed (last point = first); closePath is slow in Path2D */
  /* a ring that crosses the horizon: hidden points slide onto the rim, and the rim between them is drawn as an arc,
     which is exactly the edge that clipping to the visible hemisphere would add */
  const step=Math.max(.004,Math.sqrt(2.4/Math.max(1,R.k)));
  const putRim=a=>{ let pa=null, first=true;
    for(let i=0;i<a.length;i+=3){ const x=a[i],y=a[i+1],z=a[i+2], x1=x*R.cl-y*R.sl, y1=x*R.sl+y*R.cl, X=x1*R.cf-z*R.sf, Z=z*R.cf+x1*R.sf;
      if(X>0){ const sx=R.tx+R.k*y1, sy=R.ty-R.k*Z; if(first){ p.moveTo(sx,sy); first=false; } else p.lineTo(sx,sy); pa=null; continue; }
      const an=Math.atan2(Z,y1);
      if(pa!==null){ let d=an-pa; if(d>Math.PI) d-=2*Math.PI; else if(d<-Math.PI) d+=2*Math.PI; const n=Math.floor(Math.abs(d)/step); for(let j=1;j<=n;j++){ const b=pa+d*j/(n+1); p.lineTo(R.tx+R.k*Math.cos(b),R.ty-R.k*Math.sin(b)); } }
      const sx=R.tx+R.k*Math.cos(an), sy=R.ty-R.k*Math.sin(an); if(first){ p.moveTo(sx,sy); first=false; } else p.lineTo(sx,sy); pa=an; } };
  const poly=(rings,slow)=>{ const xs=rings.map(xyzOf), v=xs.map(vis); if(v[0]<0&&!v.some(q=>q===0)) return; xs.forEach((a,i)=>{ if(v[i]>0) put(a,true); else if(v[i]===0) putRim(a); }); };
  const line=(L,slow)=>{ const a=xyzOf(L), v=vis(a); if(v>0){ put(a,false); return; } if(v<0) return;
    let pen=false, px=0,py=0,pz=0,pX=0;
    for(let i=0;i<a.length;i+=3){ const x=a[i],y=a[i+1],z=a[i+2], x1=x*R.cl-y*R.sl, y1=x*R.sl+y*R.cl, X=x1*R.cf-z*R.sf, Z=z*R.cf+x1*R.sf;
      if(i){ if((X>0)!==(pX>0)){ const t=pX/(pX-X), ix=px+(y1-px)*t, iz=pz+(Z-pz)*t, n=Math.hypot(ix,iz)||1, sx=R.tx+R.k*ix/n, sy=R.ty-R.k*iz/n; if(pen) p.lineTo(sx,sy); else p.moveTo(sx,sy); pen=X>0; } }
      if(X>0){ const sx=R.tx+R.k*y1, sy=R.ty-R.k*Z; if(pen) p.lineTo(sx,sy); else { p.moveTo(sx,sy); pen=true; } } else pen=false;
      px=y1; pz=Z; pX=X; } };
  const walk=g=>{ if(!g) return; const t=g.type;
    if(t==="Feature") return walk(g.geometry); if(t==="FeatureCollection") return g.features.forEach(walk); if(t==="GeometryCollection") return g.geometries.forEach(walk);
    if(t==="Polygon"){ const sl=[]; poly(g.coordinates,sl); if(sl.length) gp.context(p)({type:"Polygon",coordinates:sl[0]}); return; }
    if(t==="MultiPolygon"){ const sl=[]; for(const q of g.coordinates) poly(q,sl); if(sl.length) gp.context(p)({type:"MultiPolygon",coordinates:sl}); return; }
    if(t==="LineString"){ const sl=[]; line(g.coordinates,sl); if(sl.length) gp.context(p)({type:"LineString",coordinates:sl[0]}); return; }
    if(t==="MultiLineString"){ const sl=[]; for(const L of g.coordinates) line(L,sl); if(sl.length) gp.context(p)({type:"MultiLineString",coordinates:sl}); return; }
    gp.context(p)(g); };
  walk(geo); }
/* level of detail: each topology's points are ranked once by how much they change the outline (Visvalingam),
   then thinned to what a pixel at the current zoom can show (under half a pixel), the same moving or still */
function absArcs(t){ if(t.__abs) return t.__abs; const tr=t.transform; return t.__abs=t.arcs.map(a=>{ if(!tr) return a.map(p=>[p[0],p[1]]); let x=0,y=0; return a.map(p=>{ x+=p[0]; y+=p[1]; return [x*tr.scale[0]+tr.translate[0],y*tr.scale[1]+tr.translate[1]]; }); }); }
function rankArc(P){ const n=P.length, w=new Float64Array(n); w[0]=w[n-1]=Infinity; if(n<3) return w; const pv=new Int32Array(n), nx=new Int32Array(n); for(let i=0;i<n;i++){ pv[i]=i-1; nx[i]=i+1; }
  const ar=i=>{ const a=P[pv[i]], b=P[i], c=P[nx[i]]; return Math.abs((a[0]-c[0])*(b[1]-a[1])-(a[0]-b[0])*(c[1]-a[1]))*.5*Math.cos(b[1]*DR); };
  const H=[], pos=new Int32Array(n).fill(-1); const sw=(i,j)=>{ const t=H[i]; H[i]=H[j]; H[j]=t; pos[H[i]]=i; pos[H[j]]=j; };
  const up=i=>{ while(i>0){ const p=(i-1)>>1; if(w[H[p]]<=w[H[i]]) break; sw(i,p); i=p; } }, dn=i=>{ for(;;){ const l=2*i+1, r=l+1; let m=i; if(l<H.length&&w[H[l]]<w[H[m]]) m=l; if(r<H.length&&w[H[r]]<w[H[m]]) m=r; if(m===i) break; sw(i,m); i=m; } };
  for(let i=1;i<n-1;i++){ w[i]=ar(i); pos[i]=H.length; H.push(i); up(H.length-1); }
  let mx=0; while(H.length){ const i=H[0], last=H.pop(); pos[i]=-1; if(H.length){ H[0]=last; pos[last]=0; dn(0); } if(w[i]<mx) w[i]=mx; else mx=w[i];
    const p=pv[i], q=nx[i]; nx[p]=q; pv[q]=p; for(const j of [p,q]){ if(j>0&&j<n-1&&pos[j]>=0){ w[j]=Math.max(ar(j),mx); up(pos[j]); dn(pos[j]); } } }
  return w; }
const LODK=new Map(); window.__lod={get lodLevel(){return lodLevel},get geomOf(){return geomOf},get reliefGL(){return reliefGL}};
function lodTopo(t,thr){ const C=t.__lod||(t.__lod=new Map()); if(C.has(thr)) return C.get(thr); const A=absArcs(t), W=t.__w||(t.__w=A.map(rankArc));
  const arcs=A.map((a,j)=>{ const w=W[j]; let k=a.filter((p,i)=>w[i]>=thr); if(k.length<4&&a.length>=4&&a[0][0]===a[a.length-1][0]&&a[0][1]===a[a.length-1][1]){ const idx=[...a.keys()].slice(1,-1).sort((x,y)=>w[y]-w[x]).slice(0,2).sort((x,y)=>x-y); k=[a[0],...idx.map(i=>a[i]),a[a.length-1]]; } return k; });
  const out={type:"Topology",objects:t.objects,arcs}; C.set(thr,out); LODK.set(out,thr); return out; }
function lodLevel(R){ const L=Math.max(0,Math.floor(Math.log2(Math.max(1,R)/150))), Rl=150*Math.pow(2,L); return {L,thr:.25*Math.pow(.35/Rl,2)/(DR*DR)}; }
function geomOf(g,lv){ const s=g&&g.__src; if(!s) return g; const c=g.__lod||(g.__lod={}); if(!(lv.L in c)) c[lv.L]=s.make(lodTopo(s.t,lv.thr)); return c[lv.L]; }
const BASE=["#D4C08A","#A9C4B0","#B9B0D2","#D0B3A4","#A9BFD3","#CFCDA0","#C8B6C9"];
/* greedy colouring so that neighbours differ; geoms sharing a key share a colour */
function colourise(geoms,feats,keyOf){ const nb=topojson.neighbors(geoms); const groups=new Map(); feats.forEach((f,i)=>{ const k=keyOf(f,i); if(!groups.has(k)) groups.set(k,{k,ids:[],ar:0}); const g=groups.get(k); g.ids.push(i); g.ar+=f.properties.ar||0; });
  const gOf=feats.map((f,i)=>keyOf(f,i)); const col=new Map(); [...groups.values()].sort((a,b)=>b.ar-a.ar).forEach(g=>{ const used=new Set(); g.ids.forEach(i=>nb[i].forEach(j=>{ const c=col.get(gOf[j]); if(c!=null&&gOf[j]!==g.k) used.add(c); })); let c=0; while(used.has(c)) c++; col.set(g.k,c%BASE.length); });
  feats.forEach((f,i)=>{ f.base=col.get(gOf[i]); f.nbs=nb[i]; f.all=feats; }); }
const HB={};
function hbLoad(my){ if(!HB[my]) HB[my]=getJ(`maps/w${my}.json`).then(t=>{ const o=t.objects["world_"+my], feats=topojson.feature(t,o).features.map(rewind); const T={t,o}; feats.forEach((f,i)=>{ f.src="hb"; f.my=my; f.properties=f.properties||{}; f.T=T; f.gi=i; }); colourise(o.geometries,feats,(f,i)=>f.properties.NAME||"_"+i); return feats; }).catch(()=>[]); return HB[my]; }
let CSP=null, CSN=[];
function csLoad(){ if(!CSP) CSP=Promise.all([getJ("maps/cs.json"),getJ("maps/csnames.json")]).then(([t,nm])=>{ CSN=nm.map(r=>({re:new RegExp(r[0]),o:r[1]?new RegExp(r[1]):null,a:r[2],b:r[3],n:r[4]})); const o=t.objects.cshapes_2_gw, feats=topojson.feature(t,o).features.map(rewind); const T={t,o}; feats.forEach((f,i)=>{ f.src="cs"; f.cid=i; f.T=T; f.gi=i; f.__src={t,make:tt=>rewind(topojson.feature(tt,o.geometries[i])).geometry}; }); colourise(o.geometries,feats,f=>"g"+f.properties.g); return feats; }).catch(()=>[]); return CSP; }
function csClean(n){ return n.replace(/ \((Soviet Union|Prussia|Ottoman Empire|Persia|Kampuchea|Zaire|Malagasy|Upper Volta|Byelorussia|FYROM\/North Macedonia|Rhodesia|Ceylon|Burma|Tanganyika|Eswatini|Somaliland Republic|North Borneo|Annam\/Cochin China\/Tonkin|Arab Republic of Yemen|Dutch New Guinea)\)/g,"").replace(/ \(German New Guinea\) \(Kaiser Wilhelmsland\)/,"").replace(/^Congo, Democratic Republic of/,"DR Congo").replace(/^Korea, People's Republic of/,"North Korea").replace(/^Korea, Republic of/,"South Korea").replace(/^Italy\/Sardinia$/,"Italy").replace(/^Rumania$/,"Romania"); }
function csName(raw,owner,y){ for(const r of CSN) if(r.re.test(raw)&&y>=r.a&&y<r.b&&(!r.o||r.o.test(owner||""))) return r.n; return csClean(raw); }
let GPP=null; function gapsLoad(){ if(!GPP) GPP=getJ("maps/csgaps.json").then(t=>topojson.feature(t,t.objects.gaps).features.map(rewind)).catch(()=>[]); return GPP; }
let ISP=null; function islandsLoad(){ if(!ISP) ISP=getJ("maps/islands.json").then(t=>topojson.feature(t,t.objects.islands).features.map(rewind).map(f=>{ f.src="is"; return f; })).catch(()=>[]); return ISP; }
let PCP=null;
function piecesLoad(){ if(!PCP) PCP=getJ("maps/pieces.json").then(t=>{ const o=t.objects.pieces; return topojson.feature(t,o).features.map(rewind).map(f=>{ f.src="pc"; return f; }); }).catch(()=>[]); return PCP; }
let CHG=null; const chgP=getJ("maps/changes.json").then(c=>{ CHG=c; return c; }).catch(()=>{ CHG=[]; return []; });
let PHYS=null, PPTS=null; const physP=Promise.all([getJ("maps/phys.json"),getJ("maps/physpts.json")]).then(([t,pp])=>{ PHYS={regions:topojson.feature(t,t.objects.regions).features.map(rewind),rivers:topojson.feature(t,t.objects.rivers).features,lakes:topojson.feature(t,t.objects.lakes).features.map(rewind)}; PHYS.rivers.forEach((f,i)=>{ f.__src={t,make:tt=>topojson.feature(tt,t.objects.rivers.geometries[i]).geometry}; }); PHYS.lakes.forEach((f,i)=>{ f.__src={t,make:tt=>rewind(topojson.feature(tt,t.objects.lakes.geometries[i])).geometry}; }); PPTS=pp; GLOBES.forEach(g=>g.draw()); }).catch(()=>{});
let SHOWPHYS=store.get("ma-phys",true);
/* hillshade: a grey relief texture, reprojected per pixel when the view settles */
/* relief on the graphics card: the hillshade texture reprojected per pixel every frame, so it looks the same moving or still */
let RGL;
function reliefGL(gb,layer=0){ if(!RELIEF||window.__nogl) return null; if(RGL===null) return null; if(layer&&RGL&&!RGL.coast) return null;
  if(!RGL){ try{ const cv=document.createElement("canvas"), gl=cv.getContext("webgl",{premultipliedAlpha:false,preserveDrawingBuffer:true,antialias:false}); if(!gl) throw 0;
      const sh=(t,src)=>{ const o=gl.createShader(t); gl.shaderSource(o,src); gl.compileShader(o); if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)) throw gl.getShaderInfoLog(o); return o; };
      const pg=gl.createProgram(); gl.attachShader(pg,sh(gl.VERTEX_SHADER,"attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}"));
      gl.attachShader(pg,sh(gl.FRAGMENT_SHADER,`precision highp float;uniform sampler2D tx,cx;uniform float mode,layer,dpr,hdev,R,l0,p0,r0,ka;uniform vec2 C;uniform vec3 rc;const float PI=3.14159265359;
        float A1=1.340264,A2=-0.081106,A3=0.000893,A4=0.003796,M=0.8660254037844386;
        void main(){ vec2 q=vec2(gl_FragCoord.x,hdev-gl_FragCoord.y)/dpr; float lon,lat;
          if(mode<.5){ float xv=(q.x-C.x)/R, yv=-(q.y-C.y)/R, rho=length(vec2(xv,yv)); if(rho>=1.){ gl_FragColor=vec4(0.); return; }
            float c=asin(rho), sc=sin(c), cc=cos(c); lat=rho>0.?asin(clamp(cc*sin(p0)+yv*sc*cos(p0)/rho,-1.,1.)):p0; lon=l0+atan(xv*sc,rho*cos(p0)*cc-yv*sin(p0)*sc); }
          else { float x=(q.x-C.x)/R, y=-(q.y-C.y)/R, l=y, l2,l6,fy,fpy; for(int i=0;i<12;i++){ l2=l*l; l6=l2*l2*l2; fy=l*(A1+A2*l2+l6*(A3+A4*l2))-y; fpy=A1+3.*A2*l2+l6*(7.*A3+9.*A4*l2); l-=fy/fpy; }
            l2=l*l; l6=l2*l2*l2; fpy=A1+3.*A2*l2+l6*(7.*A3+9.*A4*l2); float lam=M*x*fpy/cos(l); float s=sin(l)/M; if(abs(lam)>PI+1e-4||abs(s)>1.){ gl_FragColor=vec4(0.); return; } lat=asin(s); lon=lam-r0; }
          float u=fract((lon/PI*180.+180.)/360.), v=clamp((90.-lat/PI*180.)/180.,0.,1.);
          if(layer<.5){ float g=texture2D(tx,vec2(u,v)).r; gl_FragColor=vec4(g,g,g,1.); return; }
          float d=texture2D(cx,vec2(u,v)).r*255./6371.*R*(mode<.5?1.:.9); float keep=1.;
          keep*=1.-.05*ka*(1.-smoothstep(7.6,8.4,d)); keep*=1.-.07*ka*(1.-smoothstep(5.1,5.9,d)); keep*=1.-.09*ka*(1.-smoothstep(3.1,3.9,d)); keep*=1.-.12*ka*(1.-smoothstep(1.35,2.15,d));
          gl_FragColor=vec4(rc,1.-keep); }`));
      gl.linkProgram(pg); if(!gl.getProgramParameter(pg,gl.LINK_STATUS)) throw gl.getProgramInfoLog(pg); gl.useProgram(pg);
      const b=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,b); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array([-1,-1,1,-1,-1,1,1,1]),gl.STATIC_DRAW); const loc=gl.getAttribLocation(pg,"p"); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc,2,gl.FLOAT,false,0,0);
      const {W,H,g}=RELIEF, mx=gl.getParameter(gl.MAX_TEXTURE_SIZE); let tw=W, th=H, data=g; if(W>mx){ const f=Math.ceil(W/mx); tw=Math.floor(W/f); th=Math.floor(H/f); data=new Uint8Array(tw*th); for(let y=0;y<th;y++) for(let x=0;x<tw;x++) data[y*tw+x]=g[y*f*W+x*f]; }
      const tx=gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,tx); gl.pixelStorei(gl.UNPACK_ALIGNMENT,1); gl.texImage2D(gl.TEXTURE_2D,0,gl.LUMINANCE,tw,th,0,gl.LUMINANCE,gl.UNSIGNED_BYTE,data);
      gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
      const U={}; for(const n of ["mode","layer","dpr","hdev","R","l0","p0","r0","C","tx","cx","ka","rc"]) U[n]=gl.getUniformLocation(pg,n); gl.uniform1i(U.tx,0); gl.uniform1i(U.cx,1); RGL={cv,gl,U,coast:false};
      const ci=new Image(); ci.onload=()=>{ try{ let src=ci; if(ci.naturalWidth>mx){ const k=document.createElement("canvas"); k.width=mx; k.height=mx/2; k.getContext("2d").drawImage(ci,0,0,k.width,k.height); src=k; } const t2=gl.createTexture(); gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D,t2); gl.pixelStorei(gl.UNPACK_ALIGNMENT,1); gl.texImage2D(gl.TEXTURE_2D,0,gl.LUMINANCE,gl.LUMINANCE,gl.UNSIGNED_BYTE,src); for(const [p,v] of [[gl.TEXTURE_MIN_FILTER,gl.LINEAR],[gl.TEXTURE_MAG_FILTER,gl.LINEAR],[gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE],[gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE]]) gl.texParameteri(gl.TEXTURE_2D,p,v); gl.activeTexture(gl.TEXTURE0); RGL.coast=true; GLOBES.forEach(g=>g.draw()); }catch(e){} }; ci.src="maps/coast.png"; }catch(e){ RGL=null; return null; } }
  const {cv,gl,U}=RGL, d=gb.dpr, W=Math.round(gb.w*d), H=Math.round(gb.h*d); if(cv.width!==W||cv.height!==H){ cv.width=W; cv.height=H; } gl.viewport(0,0,W,H);
  const pr=gb.proj, D=Math.PI/180, r=pr.rotate(), T=pr.translate(), flat=gb.flat>.5;
  gl.uniform1f(U.mode,flat?1:0); gl.uniform1f(U.layer,layer); const dk=isDark(); gl.uniform1f(U.ka,dk?1.2:1); gl.uniform3f(U.rc,dk?170/255:60/255,dk?200/255:95/255,dk?190/255:90/255); gl.uniform1f(U.dpr,d); gl.uniform1f(U.hdev,H); gl.uniform1f(U.R,pr.scale()); gl.uniform2f(U.C,T[0],T[1]); gl.uniform1f(U.l0,-r[0]*D); gl.uniform1f(U.p0,-r[1]*D); gl.uniform1f(U.r0,r[0]*D);
  gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT); gl.drawArrays(gl.TRIANGLE_STRIP,0,4); return cv; }
let RELIEF=null, RELIEF_ASKED=false; const reliefLoad=()=>{ if(RELIEF_ASKED) return; RELIEF_ASKED=true; const im=new Image(); im.onload=()=>{ try{ const W=im.naturalWidth, H=im.naturalHeight, cv=document.createElement("canvas"); cv.width=W; cv.height=H; const x=cv.getContext("2d",{willReadFrequently:true}); x.drawImage(im,0,0); const g=new Uint8Array(W*H); const step=540; for(let y0=0;y0<H;y0+=step){ const hh=Math.min(step,H-y0), d=x.getImageData(0,y0,W,hh).data; for(let i=0,j=y0*W;i<d.length;i+=4,j++) g[j]=d[i]; } RELIEF={W,H,g}; GLOBES.forEach(gl=>gl.draw()); }catch(e){} }; im.src="maps/relief.jpg"; }; /* decoded only for the canvas globes (story pages); the main globe draws relief on the graphics card */
const CITIES=[]; getJ("maps/cities.json").then(c=>{ CITIES.push(...c); GLOBES.forEach(g=>g.draw()); }).catch(()=>{});
const cityName=(c,y)=>{ for(const [u,n] of c.n) if(y<u) return n; return c.n[c.n.length-1][1]; };
const PEOPLES=/hunter|gatherer|peoples|cultures|culture$|nomad|aboriginal|tribes|^maori$|^polynesians$|^papuans$|^inuit|^san$|^khoisan$|^siberians$|cereal farmers|chiefdoms|^bantu|herders|pastoralists|foragers/i;
/* lands of peoples rather than states: drawn faintly. In the Americas and Australia before 1886 every
   unit that is neither a colony nor a profiled state is treated as a people's land. */
const isPeople=(f,y)=>{ if(f.src==="cs"||f.src==="cl"||f.src==="un") return false; if(f.src==="pp") return true; const n=f.properties.NAME||""; if(PEOPLES.test(n)) return true; const lp=f.properties.lp; if(!lp) return false; const [lo,la]=lp;
  const amer=lo<-50&&lo>-170&&la>-56&&la<75, aus=lo>112&&lo<155&&la<-10&&la>-45; if(!amer&&!aus) return false; if(f._pk!==undefined&&f._py===y) return f._pk;
  const k=!(empireOf(f,y)||f.properties.SUBJECTO||POLS.some(p=>p.re.test(n)&&y>=p.a&&y<=p.b)||/viceroyalty|united states|canada|mexic|brazil|argentin|chile|peru|colombia|venezuela|bolivia|ecuador|paraguay|uruguay|confedera|republic|kingdom|empire|colony|louisiana|florida|guiana|texas|rupert|quebec|new france|new spain|new granada|haiti|cuba|jamaica|aztec|maya|inca|tenochtitlan|purépecha|tarascan|mixtec|zapotec/i.test(n)); f._pk=k; f._py=y; return k; };
const STATUS_NOTE={"Congo Free State":"personal possession of Belgian King Leopold II"};
const STATUS={colony:"colony",protectorate:"protectorate",mandate:"League of Nations mandate",occupied:"under occupation",independent:"independent","N/A":"contested"};
/* the political world of one year */
async function worldAt(y){
  if(y>=CS0){ const [cs,gaps]=await Promise.all([csLoad(),gapsLoad()]); const yy=Math.min(y,2019), t=yy+.5, feats=[];
    for(const f of cs){ const p=f.properties; if(p.a<=t&&t<p.b){ p.NAME=csName(p.r,p.o,t); p.SUBJECTO=p.o?csName(p.o,"",t):null; feats.push(f); } }
    /* land the dated record leaves empty: slivers and islands go to the state that holds them; land outside every recognised state keeps the name the survey of the time gives it */
    const extra=[];
    for(const g of gaps){ const q=g.properties; if(!(q.a<=yy&&yy<q.b)) continue;
      if(q.own){ const o=feats.find(f=>f.properties.r===q.own[0]&&(f.properties.o||"")===(q.own[1]||"")); if(o){ const c={type:"Feature",geometry:g.geometry,src:"cs",gapOf:o,cid:o.cid};
          if(q.NAME){ c.ownName=q.NAME; c.dep=!!q.dep; c.properties=Object.assign({},o.properties,{NAME:q.NAME,lp:q.lp,ar:q.ar,bl:q.bl,st:q.dep?"dependency":o.properties.st,SUBJECTO:q.dep?o.properties.NAME:o.properties.SUBJECTO}); }
          else c.properties=o.properties;
          extra.push(c); continue; } }
      if(q.NAME){ g.src="gap"; extra.push(g); } }
    return {y,src:"cs",feats:feats.concat(extra),under:[],pieces:[],hatch:[]}; }
  /* before 1886: the survey period's atoms, each with its ruler year by year, merged by ruler */
  const my=mapYear(y), A=await atomsLoad(my); if(!A) return {y,src:"hb",feats:[],under:[],pieces:[],hatch:[],changed:[],nchg:0,next:MAPY.find(m=>m>my)};
  const G=A.o.geometries, n=G.length, ow=new Int32Array(n), ch=new Int32Array(n);
  for(let i=0;i<n;i++){ const t=G[i].properties.t; let o=-1, c=-1; for(const e of t){ if(e[0]>y) break; o=e[1]; if(e[2]>=0) c=e[2]; } ow[i]=o; ch[i]=c; }
  const by=new Map(); for(let i=0;i<n;i++){ const o=ow[i]; if(o<0) continue; if(!by.has(o)) by.set(o,[]); by.get(o).push(i); }
  const feats=[], polOf=new Array(n).fill(null);
  for(const [o,ids] of by){ const [N,S,I]=A.owners[o]; let ar=0, best=ids[0], lc=-1; for(const i of ids){ const p=G[i].properties; ar+=p.ar||0; if((p.ar||0)>(G[best].properties.ar||0)) best=i; if(ch[i]>=0&&(lc<0||(A.changes[ch[i]].y||0)>(A.changes[lc].y||0))) lc=ch[i]; }
    const geom=topojson.merge(A.t,ids.map(i=>G[i])); const f=rewind({type:"Feature",geometry:geom,properties:{NAME:N,SUBJECTO:S,INF:I||undefined,ar,lp:G[best].properties.lp}});
    let bl=0; if(geom.coordinates.length>1){ for(const pc of geom.coordinates){ const a=d3.geoArea({type:"Polygon",coordinates:pc})*40589641; if(a>bl&&a<2e8){ bl=a; } } } else bl=ar; f.properties.bl=Math.min(ar,Math.round(bl));
    if(lc>=0){ const C=A.changes[lc]; if(C.t){ f.properties.t=C.t; f.properties.y=C.y; } }
    f.src="hb"; f.my=my; f.atoms=ids; f.__src={t:A.t,make:tt=>rewind({type:"Feature",geometry:topojson.merge(tt,ids.map(i=>G[i]))}).geometry}; feats.push(f); for(const i of ids) polOf[i]=f; }
  /* neighbours, for keeping adjacent states in different colours */
  const fi=new Map(feats.map((f,i)=>[f,i])); feats.forEach(f=>{ f.nbs=[]; f.all=feats; f.base=hashS(f.properties.NAME)%BASE.length; });
  for(let i=0;i<n;i++){ const f=polOf[i]; if(!f) continue; for(const j of A.nb[i]){ const g=polOf[j]; if(g&&g!==f){ const k=fi.get(g); if(!f.nbs.includes(k)) f.nbs.push(k); } } }
  /* land that changed hands at an unrecorded date, and land that changed hands this very year */
  const hz=new Map(), now=[]; for(let i=0;i<n;i++){ const p=G[i].properties; if(p.hz>=0){ if(!hz.has(p.hz)) hz.set(p.hz,[]); hz.get(p.hz).push(i); } if(p.t.some(e=>e[0]===y&&e[0]>my&&e[2]>=0)) now.push(i); }
  const hatch=[...hz].map(([k,ids])=>{ const C=A.changes[k]; return rewind({type:"Feature",geometry:topojson.merge(A.t,ids.map(i=>G[i])),properties:{a:C.a,b:C.b,frm:C.frm,to:C.to}}); });
  const changed=now.length?[rewind({type:"Feature",geometry:topojson.merge(A.t,now.map(i=>G[i])),properties:{}})]:[];
  const nchg=A.changes.filter(c=>c.k==="dated"&&c.y<=y).length;
  return {y,src:"hb",feats,under:[],pieces:[],hatch,changed,nchg,atoms:{A,polOf},next:MAPY.find(m=>m>my)}; }
const ATP={}; function atomsLoad(my){ if(!ATP[my]) ATP[my]=getJ(`maps/a${my}.json`).then(t=>{ const o=t.objects.atoms; return {t,o,owners:t.owners,changes:t.changes,nb:topojson.neighbors(o.geometries)}; }).catch(()=>null); return ATP[my]; }
const changesIn=y=>(CHG||[]).filter(c=>c.y===y);

/* borders of one year as meshes: no line between two pieces of the same state; the strongest style wins on a shared edge */
function bordersOf(W,y,dep){ if(W.mesh&&W.meshY===y) return W.mesh; const out={ppl:null,dep:null,ind:null};
  if(W.atoms){ const {A,polOf}=W.atoms, G=A.o.geometries, ix=new Map(G.map((g,i)=>[g,i])); const cls=f=>isPeople(f,y)?0:dep(f)?1:2;
    const mk=K=>{ const flt=(a,b)=>{ const fa=polOf[ix.get(a)], fb=polOf[ix.get(b)]; if(!fa&&!fb) return false; if(fa===fb&&a!==b) return false; if(fa&&fb&&fa.properties.NAME===fb.properties.NAME&&dep(fa)===dep(fb)) return false; return Math.max(fa?cls(fa):-1,fb?cls(fb):-1)===K; }; const m={type:"Feature",properties:{},geometry:topojson.mesh(A.t,A.o,flt)}; m.__src={t:A.t,make:tt=>topojson.mesh(tt,A.o,flt)}; return m; };
    out.ppl=mk(0); out.dep=mk(1); out.ind=mk(2); }
  W.mesh=out; W.meshY=y; return out; }
/* colour of a feature */
function fillOf(f,y,present){ if(f.gapOf){ const o=f.gapOf, p=o.properties, st=p.st; if(f.dep) p.st="dependency"; const col=fillOf(o,y,present); p.st=st; return col; } const n=f.properties.NAME; if(!n) return null;
  const home=f.src==="cs"?f.properties.st==="independent":null;
  if(COLORBY==="gov"){ let k=classOf(f,y); if(f.src==="cs"&&f.properties.st!=="independent") k="colony"; if(!k) k=/kingdom|empire|sultanate|khanate|emirate|caliphate|shogunate|dynasty|principality|duchy/i.test(n)?"monarchy":"stateless"; present.set(k,CLS[k].name); return tint(CLS[k].color); }
  if(COLORBY==="bloc"){ const B=blocTable(y); if(B){ const k=blocOf(f,y); present.set(k,B.cls[k].name); const e=empireOf(f,y); const isHome=home!=null?home:(!(e&&EMP[e.k]&&EMP[e.k].he&&!EMP[e.k].he.test(n))&&!f.properties.SUBJECTO); return tint(B.cls[k].color,isHome?"home":"colony"); } return tint(BASE[f.base||0],"soft"); }
  const e=empireOf(f,y); if(e&&EMP[e.k]){ present.set(e.k,EMP[e.k].name); const isHome=home!=null?(home&&(!EMP[e.k].he||EMP[e.k].he.test(n)||!f.properties.SUBJECTO)):(EMP[e.k].he?EMP[e.k].he.test(n):true); return tint(EMP[e.k].color,isHome?"home":"colony"); }
  const ik=identityOf(f,y), ic=(fillOf.ids&&fillOf.ids.get(f))||KEYCOL[ik]||KEYMEMO[ik]; const depd=f.src==="cs"?f.properties.st!=="independent":!!(f.properties.SUBJECTO&&f.properties.SUBJECTO!==f.properties.NAME); return tint(ic||BASE[f.base||0],depd?"colony":"home"); }
/* one colour per polity, kept across the centuries: the same state keeps its hue whatever map it is drawn from */
const PAL=["#C9A66B","#8FB39A","#A99BC9","#D19A86","#8EAFC9","#C2C27A","#BF9FB8","#9CC1B9","#D6B07E","#A4B28A","#B8A1D6","#C88E8E","#9DB0A0","#C7A88F"];
const KEYCOL={england:"#C0504D",english:"#C0504D",britain:"#C0504D",british:"#C0504D",great:"#C0504D",scotland:"#8EAFC9",netherland:"#E08A3C",netherlands:"#E08A3C",dutch:"#E08A3C",golden:"#D6B07E",timurid:"#A4B28A",sweden:"#8EAFC9",norway:"#A4B28A",denmark:"#D19A86",finland:"#9CC1B9",poland:"#C88E8E",lithuania:"#A4B28A",hungary:"#8FB39A",czech:"#B8A1D6",switzerland:"#D19A86",greece:"#8EAFC9",serbia:"#C2C27A",yugoslavia:"#C2C27A",romania:"#D6B07E",bulgaria:"#8FB39A",persia:"#C2C27A",iran:"#C2C27A",safavid:"#C2C27A",china:"#C9B458",ming:"#C9B458",turkey:"#2A9D8F",russia:"#9C4A5A",ussr:"#9C4A5A",egypt:"#D6B07E",ethiopia:"#8FB39A",afghanistan:"#BF9FB8",siam:"#A99BC9",thailand:"#A99BC9",korea:"#8EAFC9",mexico:"#8FB39A",brazil:"#C2C27A",argentina:"#8EAFC9",chile:"#D19A86",peru:"#B8A1D6",colombia:"#D6B07E",venezuela:"#BF9FB8",canada:"#D19A86",australia:"#C9A66B",india:"#D6B07E",pakistan:"#8FB39A",indonesia:"#C88E8E",saudi:"#9CC1B9",morocco:"#A99BC9",nigeria:"#9CC1B9",kenya:"#C2C27A",tanzania:"#8EAFC9",southafrica:"#B5835A"};
const STRIPK=/\b(new|colonial|colony|colonies|kingdom|empire|sultanate|khanate|emirate|duchy|grand|principality|republic|federal|democratic|people's|socialist|united|state|states|of|the|and|union)\b|[^a-z ]/g;
function identityOf(f,y){ if(f._ik&&f._iy===y) return f._ik; const n=f.properties.NAME||"", aka=f.properties.AKA||""; const p=POLS.find(q=>q.re.test(n)&&y>=q.a&&y<=q.b)||(aka?POLS.find(q=>q.re.test(aka)&&y>=q.a&&y<=q.b):null); let k; if(p&&p.key) k=p.key; else { const t=n.toLowerCase().replace(STRIPK," ").replace(/\s+/g," ").trim(); k=t.split(" ")[0]||t; } f._ik=k; f._iy=y; return k; }
const hashS=s=>{ let h=2166136261; for(let i=0;i<s.length;i++){ h^=s.charCodeAt(i); h=Math.imul(h,16777619); } return h>>>0; };
const KEYMEMO={};
function assignColours(feats,y){ const out=new Map(); const order=feats.filter(f=>f.properties.NAME&&!f.gapOf).sort((a,b)=>(b.properties.ar||0)-(a.properties.ar||0));
  for(const f of order){ const k=identityOf(f,y); let col=KEYCOL[k]||KEYMEMO[k]; if(!col){ col=PAL[hashS(k)%PAL.length]; KEYMEMO[k]=col; }
    const clash=c=>(f.nbs||[]).some(j=>{ const g=f.all&&f.all[j]; return g&&g!==f&&out.has(g)&&out.get(g)===c&&g.properties.NAME!==f.properties.NAME; });
    if(clash(col)){ const i=Math.max(0,PAL.indexOf(col)); for(let t=1;t<PAL.length;t++){ const c2=PAL[(i+t)%PAL.length]; if(!clash(c2)){ col=c2; break; } } }
    out.set(f,col); }
  return out; }
const labelInk=hex=>{ const c=d3.hsl(hex); if(isDark()){ c.l=.86; c.s=Math.min(c.s,.35); } else { c.l=.26; c.s=Math.min(c.s*1.1,.45); } return c.formatHex(); };
const darker=hex=>{ const c=d3.hsl(hex); c.l=isDark()?Math.min(.7,c.l+.14):Math.max(.25,c.l-.2); c.s=Math.min(1,c.s*1.25); return c.formatHex(); };
let HATCH=null; function hatchPattern(ctx,col){ const k=col+(isDark()?"d":"l"); if(HATCH&&HATCH.k===k) return HATCH.p; const c=document.createElement("canvas"); c.width=c.height=8; const x=c.getContext("2d"); x.strokeStyle=col; x.globalAlpha=.55; x.lineWidth=1; x.beginPath(); x.moveTo(0,8); x.lineTo(8,0); x.moveTo(-2,2); x.lineTo(2,-2); x.moveTo(6,10); x.lineTo(10,6); x.stroke(); HATCH={k,p:ctx.createPattern(c,"repeat")}; return HATCH.p; }

/* ---------- the world map: drawing ---------- */
const GLOBES=new Set();
const lerpRaw=t=>{ const f=(x,y)=>{ if(t<=0) return d3.geoOrthographicRaw(x,y); if(t>=1) return d3.geoEqualEarthRaw(x,y); const a=d3.geoOrthographicRaw(x,y), b=d3.geoEqualEarthRaw(x,y); return [a[0]*(1-t)+b[0]*t,a[1]*(1-t)+b[1]*t]; }; f.invert=t<.5?d3.geoOrthographicRaw.invert:d3.geoEqualEarthRaw.invert; return f; };
class Globe{
  constructor(host,opts={}){ reliefLoad(); this.host=host; this.o=opts; this.canvas=document.createElement("canvas"); this.canvas.setAttribute("aria-hidden","true"); host.prepend(this.canvas); this.ctx=this.canvas.getContext("2d");
    this.rot=[-15,-35]; this.zoom=opts.zoom||1; this.flat=0; this.pan=[0,0]; this.year=1900; this.W=null; this.feats=[]; this.markers=[]; this.lines=[]; this.cities=[]; this.hover=null; this.compareW=null; this.pulse=null; this.busy=false;
    this.mut=d3.geoProjectionMutator(lerpRaw); this.proj=this.mut(0).clipAngle(90).precision(.4);
    this.resize(); this.bind(); GLOBES.add(this); landP.then(()=>this.draw()); if(document.fonts) document.fonts.ready.then(()=>this.draw());
    if(typeof ResizeObserver!=="undefined"){ this.ro=new ResizeObserver(()=>this.resize()); this.ro.observe(host); } }
  destroy(){ GLOBES.delete(this); if(this.ro) this.ro.disconnect(); [this.timer,this.ptimer,this.mtimer].forEach(t=>t&&t.stop()); }
  resize(){ const r=this.host.getBoundingClientRect(); const w=Math.max(40,Math.round(r.width||300)), h=Math.max(40,Math.round(r.height||w)); if(w===this.w&&h===this.h&&this.dpr===devicePixelRatio) return; const dpr=this.dpr=devicePixelRatio||1; this.w=w; this.h=h; this.size=Math.min(w,h); this.canvas.width=w*dpr; this.canvas.height=h*dpr; this.canvas.style.width=w+"px"; this.canvas.style.height=h+"px"; this.ctx.setTransform(dpr,0,0,dpr,0,0); if(!this.bc){ this.bc=document.createElement("canvas"); } this.bc.width=w*dpr; this.bc.height=h*dpr; this.bx=this.bc.getContext("2d"); this.bx.setTransform(dpr,0,0,dpr,0,0); this.place(); this.draw(); }
  /* projection state: morph t between globe (0) and flat (1) */
  place(){ const t=this.flat, w=this.w, h=this.h; const sG=Math.min(w,h)/2*.94, sF=Math.min(w/(2*2.7066),h/(2*1.3173))*.96; const s=(sG*(1-t)+sF*t)*this.zoom;
    this.proj=this.mut(t); this.proj.clipAngle(t<.999?90+t*89.9:null).precision(.45).scale(s).translate([w/2+this.pan[0]*t,h/2+this.pan[1]*t]).rotate([this.rot[0],this.rot[1]*(1-t),0]).clipExtent([[-12,-12],[w+12,h+12]]); this.path=d3.geoPath(this.proj,this.ctx); this.pxkm=s/6371; }
  setZoom(z,at){ const z0=this.zoom; this.zoom=Math.max(1,Math.min(14,z)); if(this.flat>.5&&at){ const k=this.zoom/z0; this.pan=[(this.pan[0]+this.w/2-at[0])*k-(this.w/2-at[0]),(this.pan[1]+this.h/2-at[1])*k-(this.h/2-at[1])]; this.clampPan(); } if(this.zoom===1) this.pan=[0,0]; this.place();
    /* zooming redraws at full quality every frame, like dragging */
    if(false){ this.scaled=true; this.drawOverlay(); clearTimeout(this.idle); this.idle=setTimeout(()=>{ this.scaled=false; this.busy=false; this.place(); this.draw(); },180); return; }
    this.touch(); }
  clampPan(){ const lim=(this.zoom-1)*this.h/2+20; this.pan[1]=Math.max(-lim,Math.min(lim,this.pan[1])); this.pan[0]=0; }
  setFlat(on){ const to=on?1:0; if(this.mtimer) this.mtimer.stop(); if(REDUCED){ this.flat=to; this.place(); this.draw(); return; } const from=this.flat, t0=performance.now(); this.busy=true; this.mtimer=d3.timer(()=>{ const k=Math.min(1,(performance.now()-t0)/950); this.flat=from+(to-from)*d3.easeCubicInOut(k); this.place(); this.draw(); if(k>=1){ this.mtimer.stop(); this.busy=false; this.draw(); } }); }
  async setYear(y){ const prev=this.year0; this.year0=y; this.year=y; const W=await worldAt(y); if(this.year!==y) return; this.W=W; this.feats=W.feats; if(prev!=null&&prev!==y&&this.o.pulse!==false) this.startPulse(y); this.draw(); }
  async setCompare(y){ this.compareY=y; if(y==null){ this.compareW=null; this.draw(); return; } const W=await worldAt(y); if(this.compareY===y){ this.compareW=W; this.draw(); } }
  setMarkers(m){ this.markers=m; this.draw(); }
  setLines(l){ this.lines=l; this.draw(); }
  setCities(c){ this.cities=c; this.draw(); }
  centre(){ return [-this.rot[0],-this.rot[1]*(1-this.flat)]; }
  visible(p){ if(this.flat>.5) return true; return d3.geoDistance(p,this.centre())<Math.PI/2-.03; }
  rotateTo(lon,lat,animate=true,zoom){ const to=[-lon,-lat]; if(this.timer) this.timer.stop(); const z0=this.zoom, z1=zoom||this.zoom; if(!animate||REDUCED){ this.rot=to; this.zoom=z1; if(this.flat>.5) this.pan=[0,lat*this.pxkm*111*.0]; this.place(); this.draw(); return; } const ip=d3.interpolate(this.rot.slice(),[this.rot[0]+((to[0]-this.rot[0]+540)%360-180),to[1]]), t0=Date.now(); this.busy=true; this.timer=d3.timer(()=>{ const t=Math.min(1,(Date.now()-t0)/900), k=d3.easeCubicInOut(t); this.rot=ip(k); this.zoom=z0+(z1-z0)*k; if(this.flat>.5){ const p=this.proj([lon,lat]); if(p&&k>.02) this.pan[1]+= (this.h/2-p[1])*.12; this.clampPan(); } this.place(); this.draw(); if(t>=1){ this.timer.stop(); this.busy=false; this.draw(); } }); }
  touch(){ if(!this.busy){ this.busy=true; this.place(); } this.draw(); clearTimeout(this.idle); this.idle=setTimeout(()=>{ this.busy=false; this.place(); this.draw(); },160); }
  startPulse(y){ if(this.ptimer) this.ptimer.stop(); const W=this.W; if(!W) return; const fs=W.src==="cs"?W.feats.filter(f=>f.src==="cs"&&!f.gapOf&&Math.floor(f.properties.a)===y&&f.properties.a>CS0+.01):(W.changed||[]); if(!fs.length){ this.pulse=null; return; } this.pulse={fs,t0:performance.now()}; if(REDUCED){ this.pulse=null; return; } this.ptimer=d3.timer(()=>{ if(!this.pulse){ this.ptimer.stop(); return; } const e=performance.now()-this.pulse.t0; if(e>2600){ this.ptimer.stop(); this.pulse=null; } this.drawOverlay(); }); }
  flash(c){ /* highlight one ledger change */ this.flashAt={lon:c.lon,lat:c.lat,t0:performance.now()}; this.rotateTo(c.lon,c.lat,true,Math.max(this.zoom,2)); if(REDUCED) return; if(this.ftimer) this.ftimer.stop(); this.ftimer=d3.timer(()=>{ if(performance.now()-this.flashAt.t0>2400){ this.ftimer.stop(); this.flashAt=null; } this.drawOverlay(); }); }
  k(){ return this.zoom*(1+this.flat*.15); }
  reliefLayer(key,coarse){ if(!RELIEF) return null; if(this.rl&&this.rl.key===key) return this.rl.cv; const flat=this.flat>.5, sc=coarse?(flat?5:3):(flat?2:1), w=Math.ceil(this.w/sc), h=Math.ceil(this.h/sc);
    const cv=document.createElement("canvas"); cv.width=w; cv.height=h; const x=cv.getContext("2d"); const img=x.createImageData(w,h), d=img.data; const {W,H,g}=RELIEF; const pr=this.proj, D=Math.PI/180;
    if(!flat){ const [cx,cy]=pr.translate(), R=pr.scale(), r=pr.rotate(), l0=-r[0]*D, p0=-r[1]*D, sp0=Math.sin(p0), cp0=Math.cos(p0);
      for(let py=0;py<h;py++){ const yv=-(py+.5-cy)/R; for(let px=0;px<w;px++){ const xv=(px+.5-cx)/R, rho=Math.sqrt(xv*xv+yv*yv); if(rho>=1) continue; const c=Math.asin(rho), sc_=Math.sin(c), cc=Math.cos(c); const lat=rho?Math.asin(cc*sp0+yv*sc_*cp0/rho):p0; const lon=l0+Math.atan2(xv*sc_,rho*cp0*cc-yv*sp0*sc_);
        const fu=((lon/D+180)%360+360)%360/360*W-.5, fv=Math.min(H-1.001,Math.max(0,(90-lat/D)/180*H-.5)); const u0=fu<0?W-1:fu|0, u1=u0+1>=W?0:u0+1, v0=fv|0, ax=fu-Math.floor(fu), ay=fv-v0; const r0=v0*W, r1=Math.min(H-1,v0+1)*W; const val=(g[r0+u0]*(1-ax)+g[r0+u1]*ax)*(1-ay)+(g[r1+u0]*(1-ax)+g[r1+u1]*ax)*ay, o=(py*w+px)*4; d[o]=d[o+1]=d[o+2]=val; d[o+3]=255; } } }
    else { for(let py=0;py<h;py++) for(let px=0;px<w;px++){ const ll=pr.invert([(px+.5)*sc,(py+.5)*sc]); if(!ll||isNaN(ll[0])||Math.abs(ll[1])>90) continue; const u=((ll[0]+180)%360+360)%360/360*W|0, v=Math.min(H-1,Math.max(0,(90-ll[1])/180*H|0)); const val=g[v*W+u], o=(py*w+px)*4; d[o]=d[o+1]=d[o+2]=val; d[o+3]=255; } }
    x.putImageData(img,0,0); this.rl={key,cv}; return cv; }
  draw(){ this.dirty=true; this.drawOverlay(); }
  drawOverlay(){ if(this.raf) return; this.raf=requestAnimationFrame(()=>{ this.raf=0; this.render(); }); }
  render(){ const c=this.ctx, w=this.w, h=this.h; if(!c||!w) return; let lo=false; if(this.dirty){ this.dirty=false; this.scaled=false;
      if(false){ const q=this.dpr>1?1:.75, lw=Math.ceil(w*q), lh=Math.ceil(h*q); if(!this.lc){ this.lc=document.createElement("canvas"); } if(this.lc.width!==lw||this.lc.height!==lh){ this.lc.width=lw; this.lc.height=lh; this.lx=this.lc.getContext("2d"); } this.lx.setTransform(q,0,0,q,0,0); this.renderBase(this.lx); this.loShown=true; }
      else { this.renderBase(this.bx); this.loShown=false; this.lastView={s:this.proj.scale(),t:this.proj.translate().slice(),rot:this.rot.join(),flat:this.flat}; } }
    lo=this.loShown;
    c.setTransform(1,0,0,1,0,0); c.clearRect(0,0,this.canvas.width,this.canvas.height);
    if(this.scaled&&this.lastView){ const L=this.lastView, f=this.proj.scale()/L.s, T=this.proj.translate(), d=this.dpr; c.imageSmoothingQuality="high"; c.setTransform(f,0,0,f,d*(T[0]-L.t[0]*f),d*(T[1]-L.t[1]*f)); c.drawImage(this.bc,0,0); }
    else if(lo&&this.lc){ c.imageSmoothingQuality="low"; c.drawImage(this.lc,0,0,this.lc.width,this.lc.height,0,0,this.canvas.width,this.canvas.height); }
    else c.drawImage(this.bc,0,0);
    c.setTransform(this.dpr,0,0,this.dpr,0,0);
    const v=css(), wax=v.getPropertyValue("--wax").trim(), ink=v.getPropertyValue("--ink").trim(), pr=this.proj, P=d3.geoPath(pr,c);
    c.save(); c.beginPath(); P({type:"Sphere"}); c.clip();
    if(this.pulse){ const e=performance.now()-this.pulse.t0, a=e<2600?.5+.5*Math.cos(e/260):0; c.beginPath(); for(const f of this.pulse.fs) P(f); c.strokeStyle=wax; c.lineWidth=2.2; c.globalAlpha=.35+.55*Math.max(0,a); c.stroke(); if(e<2600){ c.fillStyle=wax; c.globalAlpha=.10*Math.max(0,a); c.fill(); } c.globalAlpha=1; }
    if(this.flashAt){ const e=performance.now()-this.flashAt.t0, p=pr([this.flashAt.lon,this.flashAt.lat]); if(p&&this.visible([this.flashAt.lon,this.flashAt.lat])){ for(let i=0;i<3;i++){ const r=((e/14)+i*30)%90; c.beginPath(); c.arc(p[0],p[1],r,0,7); c.strokeStyle=wax; c.globalAlpha=Math.max(0,1-r/90)*.8; c.lineWidth=1.6; c.stroke(); } c.globalAlpha=1; } }
    if(this.hover&&this.hover.feature){ c.beginPath(); P(this.hover.feature); c.strokeStyle=ink; c.lineWidth=1.8; c.stroke(); }
    c.restore(); }
  renderBase(c){ const w=this.w, h=this.h; const v=css(), V=n=>v.getPropertyValue(n).trim(); const pr=this.proj, y=this.year, busy=this.busy, k=this.k();
    /* every shape is projected once per frame into a Path2D and reused */
    const vkey=[this.rot[0].toFixed(3),this.rot[1].toFixed(3),this.zoom.toFixed(4),this.flat.toFixed(4),this.pan[0].toFixed(1),this.pan[1].toFixed(1),w,h].join();
    if(!this.pc||this.pc.key!==vkey) this.pc={key:vkey,map:new Map(),geo:new Map()}; const PC=this.pc.map;
    const gp=d3.geoPath(pr); const fastOK=this.flat===0&&!window.__nofast; let FR=null; if(fastOK){ const r=pr.rotate(), T=pr.translate(); FR={cl:Math.cos(r[0]*DR),sl:Math.sin(r[0]*DR),cf:Math.cos(r[1]*DR),sf:Math.sin(r[1]*DR),k:pr.scale(),tx:T[0],ty:T[1]}; }
    const LV=lodLevel(pr.scale()); const pth=g=>{ let p=PC.get(g); if(!p){ p=new Path2D(); const q=geomOf(g,LV); if(FR&&g.type!=="Sphere") fastPath(q,p,FR,gp); else gp.context(p)(q); PC.set(g,p); } return p; };
    const P=g=>{ c.__p=c.__p||new Path2D(); c.__p.addPath(pth(g)); };
    const begin=()=>{ c.__p=new Path2D(); }, fill=()=>c.fill(c.__p), stroke=()=>c.stroke(c.__p), clip=()=>c.clip(c.__p);
    const ink=V("--ink"), ink2=V("--ink-2"), chart=V("--chart"), tide=V("--tide"), wax=V("--wax"), verd=V("--verd"), ocean=V("--ocean"), land=V("--land"), grat=V("--grat"), rule=V("--rule");
    c.clearRect(0,0,w,h); const sphere={type:"Sphere"};
    /* sea, with a little light on the globe */
    begin(); P(sphere); c.fillStyle=ocean; fill();
    if(this.flat<.6){ const sc=pr.scale(), [cx,cy]=pr.translate(); const g=c.createRadialGradient(cx-sc*.35,cy-sc*.4,sc*.1,cx,cy,sc*1.05); g.addColorStop(0,isDark()?"rgba(255,255,255,.05)":"rgba(255,255,255,.35)"); g.addColorStop(1,"rgba(0,0,0,0)"); c.globalAlpha=1-this.flat/.6; c.fillStyle=g; fill(); c.globalAlpha=1; }
    c.save(); begin(); P(sphere); clip();
    /* graticule */
    const step=k<2?30:k<5?10:5; begin(); P(d3.geoGraticule().step([step,step])()); c.strokeStyle=grat; c.lineWidth=.6; stroke();
    /* engraved water lines along every coast */
    const LD=LAND, LW=LANDW||LAND;
    if(LAND){ const rg=SHOWPHYS!==null&&reliefGL(this,1); if(rg) c.drawImage(rg,0,0,w,h); const rings=rg?[]:[[16,.05],[11,.07],[7,.09],[3.5,.12]]; c.lineJoin="round"; for(const [lw,a] of rings){ begin(); P(LW); c.strokeStyle=isDark()?`rgba(170,200,190,${a*1.2})`:`rgba(60,95,90,${a})`; c.lineWidth=lw; stroke(); }
      begin(); P(LD); c.fillStyle=land; fill(); }
    const present=new Map(), W=this.W;
    c.save(); if(LAND){ begin(); P(LD); clip(); }
    /* land outside any recognised state (from 1886, the older survey shows through) */
    if(W&&W.under.length){ for(const f of W.under){ if(!f.properties.NAME) continue; begin(); P(f); c.fillStyle=tint(BASE[f.base||0],"soft"); c.globalAlpha=.55; fill(); c.globalAlpha=1; } }
    const fills=new Map();
    if(this.W&&(this.W.idsY!==y||!this.W.ids)){ this.W.ids=assignColours(this.feats,y); this.W.idsY=y; } fillOf.ids=this.W&&this.W.ids;
    for(const f of this.feats){ const col=fillOf(f,y,present); if(col) fills.set(f,col); }
    /* bleed each colour a little outward so it meets the coastline (the land clip keeps it off the sea) */
    if(fills.size&&this.W&&this.W.src==="cs"){ c.lineJoin="round"; c.lineWidth=2.4; const byC=new Map(); for(const [f,col] of fills){ if(!byC.has(col)) byC.set(col,[]); byC.get(col).push(f); } for(const [col,fs] of byC){ begin(); for(const f of fs) P(f); c.strokeStyle=col; stroke(); } }
    for(const [f,col] of fills){ c.fillStyle=col; const pp=isPeople(f,y); if(pp) c.globalAlpha=.66; c.fill(pth(f)); if(pp) c.globalAlpha=1; }
    if(W) for(const f of W.pieces){ const col=fillOf(f,y,present); if(!col) continue; fills.set(f,col); begin(); P(f); c.fillStyle=col; fill(); }
    /* the atlas wash: a deeper tint inside each border */
    { const lw=Math.min(9,2.5+k*1.2), byC=new Map(); for(const [f,col] of fills){ if((f.properties.ar||1e6)*this.pxkm*this.pxkm<60||isPeople(f,y)||(f.gapOf&&!f.ownName)) continue; if(!byC.has(col)) byC.set(col,[]); byC.get(col).push(f); }
      /* one clip per colour: neighbours never share a colour, so each band stays inside its own state */
      for(const [col,fs] of byC){ c.save(); begin(); for(const f of fs) P(f); clip(); c.strokeStyle=darker(col); c.globalAlpha=.32; c.lineWidth=lw; stroke(); c.restore(); } }
    /* the land in relief */
    if(SHOWPHYS&&this.o.relief!==false&&this.flat%1===0){ const rc=window.__nogl?null:(reliefGL(this)||this.reliefLayer(vkey,false)); if(rc){ c.save(); c.globalCompositeOperation="soft-light"; c.globalAlpha=isDark()?.75:.9; c.imageSmoothingEnabled=true; c.drawImage(rc,0,0,w,h); c.restore(); } }
    /* land that changed hands at an unrecorded date between two surveys */
    if(W&&W.hatch.length&&this.o.hatch!==false){ begin(); for(const f of W.hatch) P(f); c.fillStyle=hatchPattern(c,ink2); fill(); }
    /* rivers and lakes */
    const river=V("--river")||"#5F8FA6";
    if(SHOWPHYS&&PHYS&&this.o.relief!==false){ const maxR=k<1.5?1:k<2.2?2:k<3.2?3:k<4.5?4:k<6?5:6; begin(); for(const r of PHYS.rivers) if(r.properties.sr<=maxR) P(r); c.strokeStyle=river; c.globalAlpha=Math.min(.7,.35+k*.06); c.lineWidth=Math.min(1.2,.45+k*.1); c.lineJoin="round"; c.lineCap="round"; stroke(); c.globalAlpha=1;
      begin(); for(const l of PHYS.lakes) if(l.properties.sr<=(k<2?2:4)) P(l); c.fillStyle=ocean; fill(); c.strokeStyle=river; c.globalAlpha=.6; c.lineWidth=.6; stroke(); c.globalAlpha=1; }
    /* borders: sovereign solid, dependent dashed */
    const lw0=Math.min(1.4,.55+k*.12);
    if(W&&W.under.length){ begin(); for(const f of W.under) if(f.properties.NAME) P(f); c.strokeStyle=rule; c.lineWidth=.5; c.setLineDash([2,3]); stroke(); c.setLineDash([]); }
    const dep=f=>f.src==="cs"?f.properties.st!=="independent":!!(f.properties.SUBJECTO&&f.properties.SUBJECTO!==f.properties.NAME);
    const slv=f=>f.gapOf&&!f.ownName, isPc=f=>f.src==="pc"||f.src==="is";
    c.save();
    const M=this.W?bordersOf(this.W,y,dep):{}, loose=[...fills.keys()].filter(f=>!(M.ind&&f.src==="hb")&&!isPc(f)&&!slv(f));
    begin(); if(M.ppl) P(M.ppl); for(const f of loose) if(isPeople(f,y)) P(f); c.strokeStyle=ink2; c.globalAlpha=.35; c.lineWidth=lw0*.7; c.setLineDash([1.5,3]); stroke(); c.setLineDash([]); c.globalAlpha=1;
    begin(); if(M.dep) P(M.dep); for(const f of loose) if(dep(f)&&!isPeople(f,y)) P(f); c.strokeStyle=ink2; c.globalAlpha=.55; c.lineWidth=lw0*.85; c.setLineDash([3,2.5]); stroke(); c.setLineDash([]);
    begin(); if(M.ind) P(M.ind); for(const f of loose) if(!dep(f)&&!isPeople(f,y)) P(f); c.strokeStyle=ink2; c.globalAlpha=.8; c.lineWidth=lw0; stroke(); c.globalAlpha=1;
    c.restore();
    c.restore();
    if(LAND){ begin(); P(LD); c.strokeStyle=ink2; c.globalAlpha=.55; c.lineWidth=.5; stroke(); c.globalAlpha=1; }
    /* another year's borders, for comparison */
    if(this.compareW){ const CW=this.compareW; begin(); for(const f of CW.feats) if(f.properties.NAME) P(f); for(const f of CW.pieces) P(f); c.strokeStyle=wax; c.lineWidth=1.3; c.globalAlpha=.85; c.setLineDash([5,3]); stroke(); c.setLineDash([]); c.globalAlpha=1; }
    /* threads of an arc */
    const DASH={Necessary:[],Sufficient:[],Contributing:[8,6],Contested:[2,5],Coincident:[8,6],none:[]};
    for(const L of this.lines){ c.save(); begin(); P({type:"LineString",coordinates:L.coords}); c.strokeStyle=L.grade==="Coincident"?wax:(L.grade==="none"?tide:verd); c.lineWidth=L.strong?2.4:1.6; c.globalAlpha=L.faint?.45:1; c.setLineDash(DASH[L.grade]||[]); c.lineCap="round"; stroke(); c.restore(); }
    c.restore();
    /* rim */
    begin(); P(sphere); c.strokeStyle=ink2; c.globalAlpha=.6; c.lineWidth=1; stroke(); c.globalAlpha=1;
    /* labels, places and events */
    const placed=[[w-58,0,w,190],[0,0,96,96]]; const free=(x0,y0,x1,y1)=>{ for(const r of placed) if(x0<r[2]&&x1>r[0]&&y0<r[3]&&y1>r[1]) return false; placed.push([x0,y0,x1,y1]); return true; };
    const halo=(t,x,yy)=>{ c.lineWidth=3; c.strokeStyle=chart; c.lineJoin="round"; c.strokeText(t,x,yy); c.fillText(t,x,yy); };
    const showLabels=this.o.labels;
    /* markers first so labels make room for them */
    const MR={1:5,2:3.4,3:2.4}, mk=[];
    for(const m of this.markers){ if(!this.visible([m.lon,m.lat])) continue; if(m.tier===3&&k<2.2&&!m.cur) continue; const p=pr([m.lon,m.lat]); if(!p) continue; const r=m.kind==="site"?3:(m.cur?6.5:(MR[m.tier]||4)); mk.push([m,p,r]); placed.push([p[0]-r,p[1]-r,p[0]+r,p[1]+r]); }
    /* capitals and cities */
    const csCaps=showLabels&&W&&W.src==="cs"&&k>=1.7?this.feats.filter(f=>f.properties.cap&&f.properties.st==="independent").map(f=>({name:f.properties.cap[0],lon:f.properties.cap[1],lat:f.properties.cap[2],cap:true})):[];
    const hist=showLabels?CITIES.filter(ct=>y>=ct.a&&y<ct.b&&(ct.r===1?k>=1.5:k>=2.6)).map(ct=>({name:cityName(ct,y),lon:ct.lon,lat:ct.lat,r:ct.r})):[];
    const seenC=new Set(); const town=[...csCaps,...hist].filter(t=>{ const key=Math.round(t.lon*2)+","+Math.round(t.lat*2); if(seenC.has(key)) return false; seenC.add(key); return true; });
    /* names of states, sized to their land */
    c.textBaseline="middle";
    const physLabel=(L,fs,col,spacing,kind,alpha=.9)=>{ if("letterSpacing" in c) c.letterSpacing="0px"; if(!this.visible([L.lon,L.lat])) return; const p=pr([L.lon,L.lat]); if(!p||p[0]<10||p[0]>w-10||p[1]<10||p[1]>h-10) return; const txt=L.n.toUpperCase(); c.font=`italic ${fs}px 'Libre Caslon Text',Georgia,serif`; if("letterSpacing" in c) c.letterSpacing=(fs*spacing).toFixed(1)+"px"; const tw=c.measureText(txt).width; const a=(this.flat>.5||kind==="ocean")?0:-(L.ang||0)*Math.PI/180*(1-this.flat); const ca=Math.abs(Math.cos(a)), sa=Math.abs(Math.sin(a)); const bw=tw*ca+fs*sa, bh=tw*sa+fs*ca; if(!free(p[0]-bw/2,p[1]-bh/2,p[0]+bw/2,p[1]+bh/2)) return; c.save(); c.translate(p[0],p[1]); c.rotate(a); c.textAlign="center"; c.lineWidth=3; c.strokeStyle=kind==="sea"||kind==="ocean"||kind==="gulf"||kind==="bay"||kind==="strait"||kind==="channel"?ocean:chart; c.globalAlpha=.5*alpha; c.strokeText(txt,0,0); c.globalAlpha=alpha; c.fillStyle=col; c.fillText(txt,0,0); c.restore(); if("letterSpacing" in c) c.letterSpacing="0px"; };
    const seaInk=V("--sea-ink")||"#3F6F7C", relief=V("--relief")||"#6B563B";
    if(showLabels&&SHOWPHYS&&PPTS){ for(const L of PPTS.labels){ const sm=Math.max(.72,Math.min(1,this.size/640)); if(L.k==="ocean"&&k<5&&(this.size>=480||k>=1.5)) physLabel(L,13.5*sm,seaInk,.32,"ocean",.7); else if(L.k==="sea"&&k>=(L.sr<=1?1.8:2.8)) physLabel(L,11*sm,seaInk,.22,"sea",.7); else if(/gulf|bay|strait|channel/.test(L.k)&&k>=(L.sr<=2?3.2:4.5)) physLabel(L,10*sm,seaInk,.12,L.k,.65); } }
    if(showLabels&&busy&&this.labCache){ c.textAlign="center"; for(const L of this.labCache){ if(!this.visible(L.ll)) continue; const q=pr(L.ll); if(!q) continue; c.font=L.font; if("letterSpacing" in c) c.letterSpacing=L.ls; L.lines.forEach((l,i)=>{ const yy=q[1]-L.hh/2+L.lh*(i+.5); c.lineWidth=L.whisper?2.2:3.2; c.strokeStyle=chart; c.globalAlpha=L.whisper?.45:.6; c.strokeText(l,q[0],yy); c.fillStyle=L.ink||ink2; c.globalAlpha=L.whisper?.62:.9; c.fillText(l,q[0],yy); }); } c.globalAlpha=1; if("letterSpacing" in c) c.letterSpacing="0px"; c.textAlign="left"; }
    if(showLabels&&!busy){ this.labCache=[]; const cand=[...fills.keys()].filter(f=>f.properties.NAME&&f.properties.lp&&!(f.gapOf&&!f.ownName)).sort((a,b)=>(b.properties.bl||b.properties.ar||0)-(a.properties.bl||a.properties.ar||0));
      const sp=d3.geoPath(pr), [cx0,cy0]=pr.translate(), R=pr.scale(), inDisc=(x,yy,pad)=>this.flat>.5||Math.hypot(x-cx0,yy-cy0)<R-pad;
      const baseIds=new Set(this.feats.map(g=>identityOf(g,y)));
      for(const f of cand){ const pp=f.properties; if(Math.sqrt(pp.bl||pp.ar||0)*this.pxkm<30) continue; if((f.src==="pc"||f.src==="is")&&baseIds.has(identityOf(f,y))) continue;
        /* place the name on the part of the land that is in view */
        let p=null, size=0; let gm=this.pc.geo.get(f); if(!gm){ const vis=this.visible(pp.lp); gm={va:vis?(pp.bl||pp.ar||0)*this.pxkm*this.pxkm*Math.max(.2,Math.cos(d3.geoDistance(pp.lp,[-this.rot[0],-this.rot[1]]))):sp.area(f),q:null}; this.pc.geo.set(f,gm); } const va=gm.va; if(va<900) continue; size=Math.sqrt(va)*.9;
        if(this.visible(pp.lp)){ const q=pr(pp.lp); if(q&&q[0]>20&&q[0]<w-20&&q[1]>14&&q[1]<h-14&&inDisc(q[0],q[1],size*.25)) p=q; }
        if(!p){ if(!gm.q) gm.q=sp.centroid(f); const q=gm.q, ll=q&&pr.invert(q); if(q&&ll&&!isNaN(q[0])&&d3.geoContains(f,ll)&&q[0]>20&&q[0]<w-20&&q[1]>14&&q[1]<h-14) p=q; }
        if(!p) continue;
        /* the name must sit inside its own border: try the full size, then smaller, down to a whisper you can zoom in to read */
        const ppl=isPeople(f,y), ital=dep(f)||ppl, name=pp.NAME; const fp=pth(f), TT=c.getTransform(); let inF=(x,yy)=>c.isPointInPath(fp,x*TT.a+TT.e,yy*TT.d+TT.f);
        if(f.src==="hb"&&this.W&&this.W.pieces.length){ const base=inF; const pcs=this.W.pieces; inF=(x,yy)=>{ if(!base(x,yy)) return false; const ll=pr.invert([x,yy]); return !pcs.some(p=>d3.geoContains(p,ll)); }; }
        const fitsIn=(qx,qy,tw,hh)=>inF(qx-tw/2,qy)&&inF(qx+tw/2,qy)&&inF(qx,qy-hh/2)&&inF(qx,qy+hh/2)&&inF(qx-tw*.4,qy-hh*.4)&&inF(qx+tw*.4,qy+hh*.4)&&inF(qx-tw*.4,qy+hh*.4)&&inF(qx+tw*.4,qy-hh*.4);
        const fs0=Math.min(22,size/6.5); let done=false;
        for(const fs of [fs0,fs0*.82,fs0*.66,fs0*.52,7.5].filter((v,i,a)=>v>=7.5||i===a.length-1).map(v=>Math.max(7.5,v)).filter((v,i,a)=>a.indexOf(v)===i)){
          const up=fs>=12.5&&!ital, whisper=fs<9.5||ppl; const font=`${ital?"italic ":""}${fs.toFixed(1)}px 'Libre Caslon Text',Georgia,serif`; c.font=font; if("letterSpacing" in c) c.letterSpacing=up?(fs*.14).toFixed(1)+"px":"0px"; const txt=up?name.toUpperCase():name;
          let lines=[txt], tw=c.measureText(txt).width; if(txt.includes(" ")&&tw>size*.7){ const ws=txt.split(" "); let best=null; for(let i=1;i<ws.length;i++){ const A=ws.slice(0,i).join(" "), B=ws.slice(i).join(" "); const m=Math.max(c.measureText(A).width,c.measureText(B).width); if(!best||m<best[0]) best=[m,[A,B]]; } if(best[0]<tw*.8){ lines=best[1]; tw=best[0]; } }
          if(tw>size*1.1) continue; const lh=fs*1.12, hh=lh*lines.length;
          for(const [ox,oy] of [[0,0],[0,-.8],[0,.8],[-.25,0],[.25,0],[0,-1.6],[0,1.6]]){ const qx=p[0]+ox*tw, qy=p[1]+oy*hh; if(!inDisc(qx-tw/2,qy,4)||!inDisc(qx+tw/2,qy,4)||qx-tw/2<4||qx+tw/2>w-4||qy-hh/2<2||qy+hh/2>h-2) continue; if(!fitsIn(qx,qy,tw,hh)) continue; if(!free(qx-tw/2-2,qy-hh/2-1,qx+tw/2+2,qy+hh/2+1)) continue;
            { const ll=pr.invert([qx,qy]); if(ll) this.labCache.push({ll,lines,font,ls:up?(fs*.14).toFixed(1)+"px":"0px",lh,hh,whisper,ital,ink:whisper?null:labelInk(fills.get(f)||"#777777")}); }
            c.textAlign="center"; lines.forEach((l,i)=>{ const yy=qy-hh/2+lh*(i+.5); c.lineWidth=whisper?2.2:3.2; c.strokeStyle=chart; c.globalAlpha=whisper?.45:.6; c.strokeText(l,qx,yy); c.fillStyle=whisper?ink2:labelInk(fills.get(f)||"#777777"); c.globalAlpha=whisper?.62:.9; c.fillText(l,qx,yy); }); c.globalAlpha=1; done=true; break; }
          if(done) break; }
      }
      if("letterSpacing" in c) c.letterSpacing="0px"; c.textAlign="left"; }
    if(showLabels&&SHOWPHYS&&PPTS){ for(const L of PPTS.labels){ if(L.k==="mtn"&&k>=(L.sr<=2?2.2:L.sr<=3?3.4:5)) physLabel(L,L.sr<=2?10.5:9.5,relief,.3,"mtn",.62); else if((L.k==="desert"||L.k==="plateau")&&k>=(L.sr<=2?2.6:L.sr<=3?3.8:5.5)) physLabel(L,L.sr<=2?10.5:9.5,relief,.3,L.k,.55); } }
    c.textBaseline="middle"; c.textAlign="left"; if("letterSpacing" in c) c.letterSpacing="0px";
    for(const t of town){ if(!this.visible([t.lon,t.lat])) continue; const p=pr([t.lon,t.lat]); if(!p||p[0]<0||p[0]>w||p[1]<0||p[1]>h) continue; c.font=`${t.cap||t.r===1?12.5:11.5}px 'Source Sans 3',system-ui,sans-serif`; const tw=c.measureText(t.name).width; if(!free(p[0]-3,p[1]-7,p[0]+6+tw,p[1]+7)) continue; if(t.cap){ c.fillStyle=ink; c.fillRect(p[0]-2.5,p[1]-2.5,5,5); c.fillStyle=chart; c.fillRect(p[0]-1,p[1]-1,2,2); } else { c.beginPath(); c.arc(p[0],p[1],2.4,0,7); c.fillStyle=chart; c.fill(); c.strokeStyle=ink; c.lineWidth=1.2; c.stroke(); } if(k>=1.9||t.r===1||t.cap){ c.fillStyle=ink2; halo(t.name,p[0]+5,p[1]); } }
    /* event markers on top */
    if("letterSpacing" in c) c.letterSpacing="0px";
    const seen=[]; for(const [m,p,r] of mk){ c.beginPath(); c.arc(p[0],p[1],r+(m.cur?3:1.3),0,7); c.fillStyle=chart; c.fill(); c.beginPath(); c.arc(p[0],p[1],r,0,7); c.fillStyle=m.kind==="site"?ink:(m.dim?tide:(m.tier===2?ink:(m.tier===3?ink2:wax))); c.fill();
      const lab=m.label||(k>=2.4&&m.tier===2?m.title:null); if(lab&&showLabels&&(this.size>=520||k>=1.3)&&!m.dim){ c.font="13px 'Source Sans 3',system-ui,sans-serif"; const tw=c.measureText(lab).width; const left=p[0]+r+6+tw>w-56; const x0=left?p[0]-r-6-tw:p[0]+r+3; if(x0>=4&&x0+tw<=w-4&&!seen.some(q=>Math.abs(q[0]-p[0])<90&&Math.abs(q[1]-p[1])<13)&&free(x0,p[1]-8,x0+tw+3,p[1]+8)){ seen.push(p); c.fillStyle=ink; halo(lab,x0+1,p[1]); } } }
    this.present=present; this.hasUnnamed=this.feats.some(f=>!f.properties.NAME); if(this.o.onDraw) this.o.onDraw(present,this.hasUnnamed,W); }
  pick(x,y){ for(const m of this.markers){ if(!this.visible([m.lon,m.lat])) continue; const p=this.proj([m.lon,m.lat]); if(p&&Math.hypot(p[0]-x,p[1]-y)<(m.tier===3?5:9)) return {marker:m}; }
    const ll=this.proj.invert([x,y]); if(!ll||isNaN(ll[0])||!this.visible(ll)) return null; if(this.flat>.5){ const back=this.proj(ll); if(!back||Math.hypot(back[0]-x,back[1]-y)>2) return null; }
    const ok=f=>d3.geoArea(f)<2*Math.PI&&d3.geoContains(f,ll); const W=this.W||{pieces:[],under:[],hatch:[]};
    const pc=W.pieces.find(ok); if(pc) return {feature:pc,ll};
    const f=this.feats.find(ok); const ht=W.hatch.find(ok);
    if(f&&f.properties.NAME) return {feature:f.gapOf&&!f.ownName?f.gapOf:f,ll,hatch:ht||null,gap:f.src==="gap"};
    const u=W.under.find(ok); if(u&&u.properties.NAME) return {feature:u,ll,under:true};
    if(f) return {unnamed:true,ll}; return {ll}; }
  bind(){ const cv=this.canvas; let down=null, moved=false, pinch=null; const pts=new Map(); const k=()=>.25/Math.sqrt(this.zoom);
    cv.addEventListener("pointerdown",e=>{ pts.set(e.pointerId,[e.clientX,e.clientY]); if(pts.size===2){ const [a,b]=[...pts.values()]; pinch={d:Math.hypot(a[0]-b[0],a[1]-b[1]),z:this.zoom}; down=null; return; } down=[e.clientX,e.clientY,this.rot[0],this.rot[1],this.pan[1]]; moved=false; if(this.hover){ this.hover=null; this.drawOverlay(); } if(this.o.onHover) this.o.onHover(null); cv.setPointerCapture(e.pointerId); [this.timer,this.mtimer].forEach(t=>t&&t.stop()); });
    cv.addEventListener("pointermove",e=>{ if(pts.has(e.pointerId)) pts.set(e.pointerId,[e.clientX,e.clientY]); if(pinch&&pts.size===2){ const [a,b]=[...pts.values()]; this.setZoom(pinch.z*Math.hypot(a[0]-b[0],a[1]-b[1])/pinch.d); return; }
      if(down){ const dx=e.clientX-down[0], dy=e.clientY-down[1]; if(Math.hypot(dx,dy)>3) moved=true; if(!moved) return; if(this.flat>.5){ this.rot=[down[2]+dx*.6/this.zoom*(360/(this.w||600))*1.1,down[3]]; this.pan[1]=down[4]+dy; this.clampPan(); } else this.rot=[down[2]+dx*k(),Math.max(-90,Math.min(90,down[3]-dy*k()))]; this.place(); this.touch(); }
      else if(this.o.onHover){ if(this.hv) return; this.hv=requestAnimationFrame(()=>{ this.hv=0; const r=cv.getBoundingClientRect(); const hit=this.pick(e.clientX-r.left,e.clientY-r.top); const hf=hit&&hit.feature||null; if(hf!==(this.hover&&this.hover.feature)){ this.hover=hit&&hit.feature?hit:null; this.drawOverlay(); } this.o.onHover(hit,e); }); } });
    const up=e=>{ pts.delete(e.pointerId); if(pts.size<2) pinch=null; if(!down) return; const wasMoved=moved; down=null; if(wasMoved) return; const r=cv.getBoundingClientRect(); const hit=this.pick(e.clientX-r.left,e.clientY-r.top); if(hit&&hit.marker&&this.o.onMarker) this.o.onMarker(hit.marker); else if(hit&&hit.feature&&this.o.onCountry) this.o.onCountry(hit.feature,hit.ll,hit); };
    cv.addEventListener("pointerup",up); cv.addEventListener("pointercancel",e=>{ pts.delete(e.pointerId); down=null; pinch=null; });
    cv.addEventListener("pointerleave",()=>{ if(this.hover){ this.hover=null; this.drawOverlay(); } if(this.o.onHover) this.o.onHover(null); });
    cv.addEventListener("dblclick",e=>{ if(!this.o.wheel) return; const r=cv.getBoundingClientRect(), at=[e.clientX-r.left,e.clientY-r.top]; if(this.flat<.5){ const ll=this.proj.invert(at); if(ll) this.rotateTo(ll[0],ll[1],true,Math.min(14,this.zoom*1.8)); } else this.setZoom(this.zoom*1.8,at); });
    cv.addEventListener("wheel",e=>{ if(!this.o.wheel) return; e.preventDefault(); const r=cv.getBoundingClientRect(); this.setZoom(this.zoom*Math.pow(1.0015,-e.deltaY),[e.clientX-r.left,e.clientY-r.top]); },{passive:false}); }
}
matchMedia("(prefers-color-scheme: dark)").addEventListener("change",()=>GLOBES.forEach(g=>g.draw()));
new MutationObserver(()=>GLOBES.forEach(g=>g.draw())).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]});
