// add label points and areas to the survey maps
const fs=require("fs"), topo=require("topojson-client"), d3=require("d3-geo"); const _pl=require("polylabel"), polylabel=_pl.default||_pl;
const dir=__dirname+"/../atlas/maps/";
for(const f of fs.readdirSync(dir).filter(f=>/^w\d+\.json$/.test(f))){
  const T=JSON.parse(fs.readFileSync(dir+f)); const k=Object.keys(T.objects)[0]; const G=T.objects[k].geometries; const F=topo.feature(T,T.objects[k]).features;
  F.forEach((ft,i)=>{ const g=G[i]; if(!ft.geometry||!ft.geometry.coordinates||!ft.geometry.coordinates.length) return; const polys=ft.geometry.type==="Polygon"?[ft.geometry.coordinates]:ft.geometry.coordinates; let best=null,ba=-1; for(const p of polys){ let a=d3.geoArea({type:"Polygon",coordinates:p}); if(a>2*Math.PI) a=4*Math.PI-a; if(a>ba){ba=a;best=p;} } if(!best) return;
    let area=d3.geoArea(ft); if(area>2*Math.PI) area=4*Math.PI-area; const lat0=d3.geoCentroid({type:"Polygon",coordinates:best})[1], kk=Math.cos(lat0*Math.PI/180)||1; const pl=polylabel(best.map(r=>r.map(c=>[c[0]*kk,c[1]])),0.05);
    g.properties=Object.assign(g.properties||{},{lp:[+(pl[0]/kk).toFixed(2),+pl[1].toFixed(2)],ar:Math.round(area*6371*6371),bl:Math.round(ba*6371*6371)}); });
  fs.writeFileSync(dir+f,JSON.stringify(T)); }
console.log("ok");
