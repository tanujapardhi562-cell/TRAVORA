function openMap(){
  const place = document.body.dataset.mapPlace;
  if(!place){
    console.error("Travora: map place is not configured.");
    return;
  }
  window.location.href = `offline-map.html?place=${encodeURIComponent(place)}&single=1`;
}
