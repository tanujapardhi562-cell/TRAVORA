const CACHE='travora-offline-v6';
const LOCAL=['/','/offline-map','/static/css/map.css','/static/js/offline-map.js','/static/js/app.js','/maps/style.json','/maps/travora-west.pmtiles'];
const CDN=['https://unpkg.com/maplibre-gl@5.11.0/dist/maplibre-gl.js','https://unpkg.com/maplibre-gl@5.11.0/dist/maplibre-gl.css','https://unpkg.com/pmtiles@4.3.0/dist/pmtiles.js'];
self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(async c=>{for(const u of LOCAL)try{await c.add(u)}catch(e){}for(const u of CDN)try{await c.add(new Request(u,{mode:'cors'}))}catch(e){}await self.skipWaiting()})));
self.addEventListener('activate',event=>event.waitUntil(self.clients.claim()));
self.addEventListener('fetch',event=>{if(event.request.method!=='GET')return;event.respondWith(caches.match(event.request).then(cached=>cached||fetch(event.request).then(res=>{if(res.ok && (event.request.url.includes('unpkg.com')||event.request.url.includes('/maps/')||event.request.url.includes('/static/'))){const copy=res.clone();caches.open(CACHE).then(c=>c.put(event.request,copy));}return res}).catch(()=>caches.match('/'))));});
