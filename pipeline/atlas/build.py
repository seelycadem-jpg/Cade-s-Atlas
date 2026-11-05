import shutil,os
css=open('app.css').read()+open('/home/claude/atlas/maplibre-gl.css').read(); js=open('app.js').read().replace('/*GLOBE*/',open('globe.js').read()+'\n'+open('globegl.js').read()+'\n'+open('globeprov.js').read()); p=open('page.html').read()
assert '</script>' not in js
out=p.replace('/*CSS*/',css).replace('/*JS*/',js)
open('index.html','w').write(out)
for f in ['data.json','world.json','rules.json','graph.json']: shutil.copy('/home/claude/site/'+f,f)
# test copy
t='/tmp/t/www3'; os.makedirs(t,exist_ok=True)
open(t+'/index.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{padding:0}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'+out)
for f in ['data.json','world.json','rules.json','graph.json','polities.json']: shutil.copy(f,t+'/'+f)
shutil.rmtree(t+'/maps',ignore_errors=True); shutil.copytree('maps',t+'/maps')
shutil.copy('/tmp/t/www/d3.min.js',t+'/d3.min.js'); shutil.copy('/tmp/ml524/package/dist/maplibre-gl.js',t+'/maplibre-gl.js'); shutil.copy('/tmp/t/www/topojson-client.min.js',t+'/topojson-client.min.js')
test=out.replace('https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js','d3.min.js').replace('https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js','topojson-client.min.js').replace('https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/maplibre-gl.js','maplibre-gl.js')
open(t+'/index.html','w').write('<!doctype html><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>:root{padding:0}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>'+test)
print('built',len(out)//1024,'KB')
