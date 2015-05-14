
window.addEventListener("load", function() {
    var output = document.getElementById("map");
    var map;

    showMap(49.457, 31.765, 7);
    
    if (!navigator.geolocation){
        map.setView([49.457, 31.765], 7);
        return;
      }

    function success(position) {
        var latitude  = position.coords.latitude;
        var longitude = position.coords.longitude;
        var range = 9;
        map.setView([latitude, longitude], range);
    }

    function showMap(x,y,z) {
        map = L.map('map').setView([x, y], z);
        L.tileLayer('https://{s}.tiles.mapbox.com/v4/mdemitc.m0cg2hm8/{z}/{x}/{y}.png?access_token={id}', {
                id: 'pk.eyJ1IjoibWRlbWl0YyIsImEiOiJNR2thSnB3In0.IzaWDdO6nh0lGHnCO0V4Mw'
            }).addTo(map);
        
            new L.Control.GeoSearch ({
                provider : new L.GeoSearch.Provider.OpenStreetMap(),
                position : 'topcenter',
                showMarker : false
            }).addTo(map);

        addMarkers(49.957, 28.465); 
    }

    function addMarkers(x, y) {
        var markerIcon = L.icon({
            iconUrl: '/static/images/marker_icon.png',
            iconSize: [25, 41]
        });

        L.marker([x, y], {icon: markerIcon}).addTo(map);
    }

    function error() {
        map.setView([49.457, 31.765], 7);
    };


    navigator.geolocation.getCurrentPosition(success, error);
});
