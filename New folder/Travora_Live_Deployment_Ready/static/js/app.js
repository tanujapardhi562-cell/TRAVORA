const destinations={lonavala:true,lonavla:true,mahabaleshwar:true,mahabaleshwer:true,alibaug:true,alibag:true,ajanta:true,'ajanta caves':true,ellora:true,'ellora caves':true,khandala:true,'karla caves':true,'pawna lake':true,'rajmachi fort':true,'sinhagad fort':true,'gateway of india':true};

function searchDestination(){
  const input=document.getElementById('destinationSearch');
  const msg=document.getElementById('searchMessage');
  if(!input)return;
  const value=input.value.toLowerCase().trim();
  if(!value){if(msg)msg.textContent='Please enter a destination.';input.focus();return;}
  const key=Object.keys(destinations).find(k=>k===value || k.includes(value) || value.includes(k));
  if(key) window.location.href='offline-map.html?place='+encodeURIComponent(key);
  else if(msg) msg.textContent='Try Lonavala, Khandala, Mahabaleshwar, Alibaug, Ajanta Caves, Ellora Caves or Rajmachi Fort.';
}

const searchInput=document.getElementById('destinationSearch');
if(searchInput) searchInput.addEventListener('keydown',e=>{if(e.key==='Enter')searchDestination();});

if('serviceWorker' in navigator) window.addEventListener('load',()=>navigator.serviceWorker.register('./js/service-worker.js').catch(()=>{}));

// Kept for older pages only; authentication is now handled by Flask.
function logoutUser(){ window.location.href='/logout'; }
