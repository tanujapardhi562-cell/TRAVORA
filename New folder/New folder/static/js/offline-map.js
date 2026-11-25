const places = [
  {name:"Lonavala",city:"Pune",category:"Hill Station",latitude:18.7546,longitude:73.4062},
  {name:"Khandala",city:"Pune",category:"Hill Station",latitude:18.7580,longitude:73.3760},
  {name:"Karla Caves",city:"Lonavala",category:"Historical",latitude:18.7897,longitude:73.4789},
  {name:"Pawna Lake",city:"Maval, Pune",category:"Lake",latitude:18.6380,longitude:73.4880},
  {name:"Rajmachi Fort",city:"Lonavala",category:"Fort",latitude:18.8326,longitude:73.3945},
  {name:"Gateway of India",city:"Mumbai",category:"Historical",latitude:18.9220,longitude:72.8347},
  {name:"Alibaug",city:"Raigad",category:"Beach",latitude:18.6414,longitude:72.8722},
  {name:"Sinhagad Fort",city:"Pune",category:"Fort",latitude:18.3663,longitude:73.7559},
  {name:"Mahabaleshwar",city:"Satara",category:"Hill Station",latitude:17.9307,longitude:73.6477},
  {name:"Ajanta Caves",city:"Chhatrapati Sambhajinagar",category:"Historical",latitude:20.5519,longitude:75.7033},
  {name:"Ellora Caves",city:"Chhatrapati Sambhajinagar",category:"Historical",latitude:20.0268,longitude:75.1793}
];

const map = L.map("map", {
  zoomControl:true,
  preferCanvas:true,
  attributionControl:true,
  dragging:true,
  touchZoom:true,
  scrollWheelZoom:true,
  doubleClickZoom:true,
  boxZoom:true,
  keyboard:true,
  zoomAnimation:true,
  markerZoomAnimation:true
}).setView([19.2,74.0],7);

// Keep the map fully pannable after zooming/focusing a place.
map.dragging.enable();
map.touchZoom.enable();
map.scrollWheelZoom.enable();
map.doubleClickZoom.enable();

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom:19,
  minZoom:5,
  attribution:'&copy; OpenStreetMap contributors'
}).addTo(map);

const search = document.getElementById("search");
const suggestions = document.getElementById("suggestions");
const status = document.getElementById("status");
const listBox = document.getElementById("placeList");
const resultCount = document.getElementById("resultCount");
let markers = [];

function makeIcon(){
  return L.divIcon({
    className:"",
    html:'<div class="travora-pin"></div>',
    iconSize:[28,38],
    iconAnchor:[14,36],
    popupAnchor:[0,-32]
  });
}

function clearMarkers(){
  markers.forEach(m=>map.removeLayer(m));
  markers=[];
}

function addMarker(place, open=false){
  const marker=L.marker([place.latitude,place.longitude],{icon:makeIcon()}).addTo(map);
  marker.bindTooltip(place.name,{permanent:true,direction:"right",offset:[10,-2],className:"pin-label"});
  marker.bindPopup(
    `<strong>${escapeHtml(place.name)}</strong><br>${escapeHtml(place.city)}<br><small>${escapeHtml(place.category)}</small>`
  );
  marker.on("click",()=>focusPlace(place,false));
  markers.push(marker);
  if(open) marker.openPopup();
  return marker;
}

function showAll(list=places){
  clearMarkers();
  list.forEach(p=>addMarker(p));
}

function score(place,q){
  const n=place.name.toLowerCase(), c=place.city.toLowerCase(), cat=place.category.toLowerCase();
  if(n===q)return 100;
  if(n.startsWith(q))return 90;
  if(n.includes(q))return 75;
  if(c===q)return 70;
  if(c.includes(q))return 60;
  if(cat.includes(q))return 40;
  return 0;
}

function resultsFor(q){
  const query=q.trim().toLowerCase();
  if(!query)return places;
  return places.filter(p=>score(p,query)>0).sort((a,b)=>score(b,query)-score(a,query));
}

function renderSuggestions(list){
  suggestions.innerHTML="";
  if(!list.length){suggestions.hidden=true;return;}
  list.slice(0,8).forEach(place=>{
    const b=document.createElement("button");
    b.type="button";
    b.innerHTML=`<strong>📍 ${escapeHtml(place.name)}</strong><small>${escapeHtml(place.city)} • ${escapeHtml(place.category)}</small>`;
    b.onclick=()=>focusPlace(place,true);
    suggestions.appendChild(b);
  });
  suggestions.hidden=false;
}

function renderList(list){
  listBox.innerHTML="";
  resultCount.textContent=list.length;
  list.slice(0,30).forEach(place=>{
    const b=document.createElement("button");
    b.className="place-card";
    b.type="button";
    b.innerHTML=`<strong>📍 ${escapeHtml(place.name)}</strong><small>${escapeHtml(place.city)} • ${escapeHtml(place.category)}</small>`;
    b.onclick=()=>focusPlace(place,true);
    listBox.appendChild(b);
  });
}

function focusPlace(place,openPopup=true){
  search.value=place.name;
  suggestions.hidden=true;
  clearMarkers();
  const marker=addMarker(place,openPopup);
  map.flyTo([place.latitude,place.longitude],15,{duration:1.2});
  setTimeout(()=>{if(openPopup) marker.openPopup();},1250);
  status.textContent=`📍 ${place.name} • map focused on ${place.latitude.toFixed(4)}, ${place.longitude.toFixed(4)}`;
}

function searchPlaces(){
  const q=search.value.trim();
  const list=resultsFor(q);
  renderSuggestions(list);
  renderList(list);
  if(!q){
    showAll();
    map.setView([19.2,74.0],7);
    status.textContent="Maharashtra road map ready.";
    return;
  }
  if(list.length){
    // Exact match first; otherwise best matching place.
    focusPlace(list[0],false);
    status.textContent=`Found ${list.length} place${list.length>1?"s":""}. Showing ${list[0].name}.`;
    renderSuggestions(list);
  }else{
    clearMarkers();
    status.textContent="No matching place found. Try Lonavala, Khandala, Alibaug, Mahabaleshwar or Ajanta Caves.";
  }
}

function escapeHtml(v){
  return String(v).replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[c]));
}

search.addEventListener("input",()=>{
  const list=resultsFor(search.value);
  renderSuggestions(list);
  renderList(list);
});
search.addEventListener("keydown",e=>{
  if(e.key==="Enter"){
    const list=resultsFor(search.value);
    if(list.length)focusPlace(list[0],true);
    else searchPlaces();
  }
  if(e.key==="Escape")suggestions.hidden=true;
});
document.addEventListener("click",e=>{
  if(!e.target.closest(".search-wrap"))suggestions.hidden=true;
});
document.getElementById("reset").onclick=()=>{
  search.value="";
  suggestions.hidden=true;
  renderList(places);
  showAll();
  map.flyTo([19.2,74.0],7,{duration:0.8});
  status.textContent="Maharashtra road map reset.";
};
document.getElementById("locate").onclick=()=>{
  if(!navigator.geolocation){
    status.textContent="Geolocation is not supported by this browser.";
    return;
  }
  status.textContent="📍 Requesting your location...";
  navigator.geolocation.getCurrentPosition(pos=>{
    const lat=pos.coords.latitude,lng=pos.coords.longitude;
    map.flyTo([lat,lng],15,{duration:1});
    L.marker([lat,lng],{icon:makeIcon()}).addTo(map).bindPopup("<strong>You are here</strong>").openPopup();
    status.textContent=`📍 Your location: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;
  },()=>{
    status.textContent="Location permission was not available.";
  });
};

// Single-place mode is used from a destination detail page.
// It shows only the selected destination marker instead of the full Maharashtra map index.
const params = new URLSearchParams(window.location.search);
const requested = params.get("place");
const singlePlace = params.get("single") === "1";

if (singlePlace && requested) {
  const q = requested.trim().toLowerCase();
  const found = places.find(p=>p.name.toLowerCase()===q) ||
                places.find(p=>p.name.toLowerCase().includes(q));
  if (found) {
    document.body.classList.add("single-place");
    search.value = found.name;
    suggestions.hidden = true;
    renderList([found]);
    resultCount.textContent = "1";
    clearMarkers();
    const marker = addMarker(found, true);
    map.setView([found.latitude, found.longitude], 14);
    status.textContent = `📍 ${found.name} map`;
  } else {
    showAll();
    renderList(places);
  }
} else {
  showAll();
  renderList(places);
  if(requested){
    const q=requested.trim().toLowerCase();
    const found=places.find(p=>p.name.toLowerCase()===q) ||
                places.find(p=>p.name.toLowerCase().includes(q));
    if(found) setTimeout(()=>focusPlace(found,true),500);
  }
}
