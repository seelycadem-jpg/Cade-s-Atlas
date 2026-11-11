/* Copies the events and links the chain web needs out of atlas-data.js and into event-v12.html,
   between the DATA markers. Nothing is changed on the way: each event keeps its id, year, title,
   old tier and tags, plus the first sentence of its bottom line; each link is copied whole.
   Run from this folder:  node build-chain-data.cjs */
const fs = require('fs');
const path = require('path');
global.window = {};
require(path.join(__dirname, 'atlas-data.js'));
const A = window.ATLAS;
const events = A.events.map(e => ({
  id: e.id, y: e.y, h: e.h, tier: e.tier, c: e.c,
  l: String(e.bluf || '').split(/(?<=\.)\s/)[0],
}));
const data = JSON.stringify({ events, links: A.links }).replace(/</g, '\\u003c');
const file = path.join(__dirname, 'event-v12.html');
const html = fs.readFileSync(file, 'utf8');
const out = html.replace(/\/\*DATA\*\/[\s\S]*?\/\*END\*\//, () => '/*DATA*/' + data + '/*END*/');
if (out === html && !html.includes(data)) throw new Error('DATA markers not found in event-v12.html');
fs.writeFileSync(file, out);
console.log('event-v12.html: ' + events.length + ' events, ' + A.links.length + ' links');
