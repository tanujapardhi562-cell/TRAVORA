const places=[
{name:'Lonavala',city:'Pune',category:'Hill Station',latitude:18.7546,longitude:73.4062},
{name:'Khandala',city:'Pune',category:'Hill Station',latitude:18.7580,longitude:73.3760},
{name:'Karla Caves',city:'Lonavala',category:'Historical',latitude:18.7897,longitude:73.4789},
{name:'Pawna Lake',city:'Maval, Pune',category:'Lake',latitude:18.6380,longitude:73.4880},
{name:'Rajmachi Fort',city:'Lonavala',category:'Fort',latitude:18.8326,longitude:73.3945},
{name:'Gateway of India',city:'Mumbai',category:'Historical',latitude:18.9220,longitude:72.8347},
{name:'Alibaug',city:'Raigad',category:'Beach',latitude:18.6414,longitude:72.8722},
{name:'Sinhagad Fort',city:'Pune',category:'Fort',latitude:18.3663,longitude:73.7559},
{name:'Mahabaleshwar',city:'Satara',category:'Hill Station',latitude:17.9307,longitude:73.6477},
{name:'Ajanta Caves',city:'Chhatrapati Sambhajinagar',category:'Historical',latitude:20.5519,longitude:75.7033},
{name:'Ellora Caves',city:'Chhatrapati Sambhajinagar',category:'Historical',latitude:20.0268,longitude:75.1793}
];
const badge=document.getElementById('offlineBadge'),status=document.getElementById('status');
const protocol=new pmtiles.Protocol(); maplibregl.addProtocol('pmtiles',protocol.tile);
const map=new maplibregl.Map({container:'map',style:'/static/../maps/style.json',center:[74,19.2],zoom:7,attributionControl:false,dragRotate:false});
map.addControl(new maplibregl.NavigationControl(),'top-right');
map.addControl(new maplibregl.AttributionControl({customAttribution:'© OpenStreetMap contributors • Extract by BBBike'}));
const markers=[];
function clearMarkers(){markers.splice(0).forEach(m=>m.remove());}
function addMarker(p,open=false){const el=document.createElement('div');el.className='travora-pin';el.style.cssText='width:18px;height:18px;border-radius:50%;background:#0b7a4b;border:3px solid white;box-shadow:0 2px 7px #0006;cursor:pointer';const m=new maplibregl.Marker({element:el}).setLngLat([p.longitude,p.latitude]).setPopup(new maplibregl.Popup({offset:24}).setHTML('<div class="popup-card"><strong>'+esc(p.name)+'</strong><br>'+esc(p.city)+'<br><small>'+esc(p.category)+'</small></div>')).addTo(map);el.onclick=()=>focusPlace(p,true);markers.push(m);if(open)m.togglePopup();return m;}
function esc(v){return String(v).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));}
function renderList(list){const box=document.getElementById('placeList');box.innerHTML='';document.getElementById('resultCount').textContent=list.length;list.forEach(p=>{const b=document.createElement('button');b.className='place-card';b.type='button';b.innerHTML='<strong>📍 '+esc(p.name)+'</strong><small>'+esc(p.city)+' • '+esc(p.category)+'</small>';b.onclick=()=>focusPlace(p,true);box.appendChild(b);});}
function focusPlace(p,open){clearMarkers();addMarker(p,open);map.flyTo({center:[p.longitude,p.latitude],zoom:14,duration:900});document.getElementById('search').value=p.name;status.textContent='📍 '+p.name+' • local road map';}
function find(q){q=q.trim().toLowerCase();if(!q)return places;return places.filter(p=>(p.name+' '+p.city+' '+p.category).toLowerCase().includes(q));}
function init(){clearMarkers();places.forEach(p=>addMarker(p));renderList(places);status.textContent='Local road map ready.';badge.textContent=navigator.onLine?'Offline map ready after cache':'Offline mode • local map data';badge.className='offline-badge '+(navigator.onLine?'online':'ready');}
map.on('load',()=>{init();const req=new URLSearchParams(location.search).get('place');if(req){const p=find(req)[0];if(p)focusPlace(p,true);}});
document.getElementById('search').addEventListener('input',e=>{const list=find(e.target.value);renderList(list);if(list.length===1)focusPlace(list[0],false);});
document.getElementById('search').addEventListener('keydown',e=>{if(e.key==='Enter'){const p=find(e.target.value)[0];if(p)focusPlace(p,true);}});
document.getElementById('reset').onclick=()=>{document.getElementById('search').value='';map.flyTo({center:[74,19.2],zoom:7,duration:700});init();};
document.getElementById('locate').onclick=()=>navigator.geolocation?.getCurrentPosition(pos=>map.flyTo({center:[pos.coords.longitude,pos.coords.latitude],zoom:15,duration:900}));
