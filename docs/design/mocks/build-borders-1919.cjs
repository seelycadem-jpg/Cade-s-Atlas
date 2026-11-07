const fs=require('fs'); const tc=require('./lib/node_modules/topojson-client'); const ts=require('./lib/node_modules/topojson-server'); const tsi=require('./lib/node_modules/topojson-simplify');
const t=JSON.parse(fs.readFileSync('/home/user/Cade-s-Atlas/site/maps/cs.json','utf8')); const key=Object.keys(t.objects)[0];
const fc=tc.feature(t,t.objects[key]); const Y=1919.5;
const alive=fc.features.filter(f=>f.properties.a<=Y && Y<(f.properties.b||9999)).map(f=>({type:'Feature',properties:{r:f.properties.r,o:f.properties.o||'',st:f.properties.st},geometry:f.geometry}));
let topo=ts.topology({cs:{type:'FeatureCollection',features:alive}},1e4);
topo=tsi.presimplify(topo); topo=tsi.simplify(topo, tsi.quantile(topo,0.35));
const out=JSON.stringify(topo); fs.writeFileSync('borders1919.json',out);
console.log('polities in 1919:',alive.length,'| size',Math.round(out.length/1024),'KB | arcs',topo.arcs.length);
console.log(alive.map(f=>f.properties.r).filter(r=>/German|Poland|Czech|Austria|Hungary|Turkey|Ottoman|Yugo|Serb/.test(r)).join(', '));
